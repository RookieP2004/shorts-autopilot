"""The director's checks, run on every render after the ears (learned from Lemo-Opuscar's directing method and
written our own way): does the film hook, can people read what is on screen, does the pace breathe, does the
camera move with variety, does sound carry at least two cuts, are there real silences before the turns, and are
there blank frames. Measured, never blocking: the result goes to out/director.json and one log line, and the
weekly review reads them.
"""
import json
import os
import re
import subprocess

import numpy as np


def _pcm(path, sr=16000):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)


def silences(x, sr=16000, win=0.05, min_len=0.35, drop_db=24):
    """Near-silences: stretches at least min_len long that sit drop_db under the film's median level."""
    k = int(win * sr)
    n = len(x) // k
    if n < 10:
        return []
    r = np.sqrt(np.mean(x[: n * k].reshape(n, k) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(r)
    ref = np.median(db[db > -80]) if np.any(db > -80) else -40
    q = db < ref - drop_db
    out, i = [], 0
    while i < n:
        if q[i]:
            j = i
            while j < n and q[j]:
                j += 1
            a, b = i * win, j * win
            if b - a >= min_len and a > 0.5 and b < n * win - 0.5:
                out.append((round(a, 2), round(b - a, 2)))
            i = j
        else:
            i += 1
    return out


def freezes(path, min_s=1.2):
    """Stretches where nothing on screen moves for min_s or longer (a still frame reads as a stall)."""
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-vf", f"freezedetect=n=0.002:d={min_s}", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    st = re.findall(r"freeze_start: ([\d.]+)", r.stderr)
    du = re.findall(r"freeze_duration: ([\d.]+)", r.stderr)
    return [(round(float(a), 2), round(float(b), 2)) for a, b in zip(st, du)]


def blackframes(path):
    # picture_black_ratio 0.998: a dark set (night look, a Cutaway dark bench) is not a blank frame
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-vf", "blackdetect=d=0.08:pix_th=0.04:pic_th=0.998", "-an",
                        "-f", "null", "-"], capture_output=True, text=True)
    return [(round(float(a), 2), round(float(d), 2))
            for a, d in re.findall(r"black_start:([\d.]+).*?black_duration:([\d.]+)", r.stderr)]


def camera_moves(scenes):
    """The kinds of camera move the film uses: push, pull, pan, tilt, hold (2D has a camera too)."""
    kinds = []
    for s in scenes:
        keys = (s.get("camera") or {}).get("keys") or []
        if len(keys) < 2:
            kinds.append("hold")
            continue
        a, b = keys[0], keys[-1]
        dz = b.get("zoom", 1) - a.get("zoom", 1)
        fa, fb = a.get("focus", [.5, .5]), b.get("focus", [.5, .5])
        dx, dy = fb[0] - fa[0], fb[1] - fa[1]
        k = []
        if dz > 0.03:
            k.append("push")
        elif dz < -0.03:
            k.append("pull")
        if abs(dx) > 0.04:
            k.append("pan")
        if abs(dy) > 0.04:
            k.append("tilt")
        if len(keys) > 2 and any(abs(keys[i].get("zoom", 1) - keys[i - 1].get("zoom", 1)) > 0.12 for i in range(1, len(keys))):
            k.append("snap")
        kinds.append("+".join(k) or "hold")
    return kinds


TEXT_KEYS = ("text", "title", "label", "value", "headline")


def text_holds(ctx, fast=True):
    """Every on-screen text stays up long enough to read: letters/18 + 0.8 s in a Short (fast, few words),
    letters/15 + 1.5 s in a long video. Returns the ones that leave too soon."""
    rate, base = (18, 0.8) if fast else (15, 1.5)
    bad = []
    for i, s in enumerate(ctx.job["scenes"]):
        for L in s.get("layers", []):
            if L.get("type") == "look" and L.get("_frames_dir"):      # a look reports its own text boxes
                from .looks import texts
                at = L.get("at", 0.0)
                end = (L["at"] + L["dur"]) if "dur" in L else ctx.dur[i]
                first, last = {}, {}
                for fr in texts(L["_frames_dir"]):
                    for b in fr.get("boxes") or []:
                        if b.get("pass"):
                            continue
                        k = (b["id"], b["text"])
                        first.setdefault(k, fr["t"])
                        last[k] = fr["t"]
                for (bid, txt), t0 in first.items():
                    seen = min(last[(bid, txt)] + 0.1, end - at) - t0
                    need = len(txt.replace(" ", "")) / rate + base
                    if seen < need - 0.05:
                        bad.append({"scene": i, "type": f"look {L['look']}", "text": txt[:40], "seen": round(seen, 2),
                                    "need": round(need, 2)})
                continue
            txt = next((L[k] for k in TEXT_KEYS if isinstance(L.get(k), str)), None)
            if not txt or L.get("type") in ("caption", "captions") or L.get("readable") is False:
                continue
            at = L.get("at", 0.0)
            end = L["until"] if "until" in L else at + L["dur"] if "dur" in L else ctx.dur[i]
            seen = end - at - 0.35                       # minus the animation in
            need = len(txt.replace(" ", "")) / rate + base
            if seen < need - 0.05:
                bad.append({"scene": i, "type": L.get("type"), "text": txt[:40], "seen": round(seen, 2),
                            "need": round(need, 2)})
    return bad


def check(ctx, final_mp4, out_dir, log=print):
    long_form = ctx.W > ctx.H
    scenes = ctx.job["scenes"]
    rep = {}
    cues = getattr(ctx, "sfx_cues", []) or []
    first_voice = ctx.start[0] + ctx.lead_of(0) if scenes else 0
    first_fx = min([c[0] for c in cues], default=99)
    rep["hook"] = {"voice_s": round(first_voice, 2), "first_sound_s": round(first_fx, 2),
                   "ok": first_voice < 1.0 and min(first_fx, first_voice) < 3.0}
    durs = np.array(ctx.dur, float)
    cv = float(durs.std() / durs.mean()) if len(durs) > 1 else 0
    rep["pace"] = {"scene_cv": round(cv, 2), "breath_s": round(float(durs.max()), 2),
                   "ok": cv >= 0.25 and durs.max() >= 1.5 * np.median(durs)}
    kinds = camera_moves(scenes)
    distinct = sorted({p for k in kinds for p in k.split("+")} - {"hold"})
    want_moves = 4 if long_form else 3
    rep["camera"] = {"moves": distinct, "ok": len(distinct) >= want_moves}
    cuts = [ctx.start[i] for i in range(1, len(scenes))]
    sound_cuts = sum(1 for c in cuts if any(c - 0.5 <= t < c + 0.05 for t, *_ in cues))
    rep["sound_transitions"] = {"cuts": len(cuts), "carried_by_sound": sound_cuts, "ok": sound_cuts >= 2}
    try:
        x = _pcm(final_mp4)
        sil = silences(x)
    except Exception:
        sil = []
    want_sil = 2 if long_form else 1
    rep["silences"] = {"at": sil, "ok": len(sil) >= want_sil}
    bad = text_holds(ctx, fast=not long_form)
    rep["reading"] = {"too_short": bad, "ok": not bad}
    try:
        bl = blackframes(final_mp4)
    except Exception:
        bl = []
    dips = [ctx.start[i] for i, s in enumerate(scenes) if i and s.get("transition") in ("dip", "fade_black")]
    bl = [b for b in bl if not any(abs(b[0] - d) < 0.4 for d in dips)]      # a dip to black is meant
    rep["black_frames"] = {"spans": bl, "ok": not bl}
    try:                                                 # learned from Cutaway's verdict: nothing may stand still > 1.2 s
        fz = freezes(final_mp4)
    except Exception:
        fz = []
    rep["motion"] = {"frozen": fz, "ok": not fz}
    rep["stings"] = getattr(ctx, "stings", [])
    for v in rep.values():
        if isinstance(v, dict) and "ok" in v:
            v["ok"] = bool(v["ok"])
    rep["score"] = sum(1 for v in rep.values() if isinstance(v, dict) and v.get("ok"))
    rep["of"] = sum(1 for v in rep.values() if isinstance(v, dict) and "ok" in v)
    with open(os.path.join(out_dir, "director.json"), "w") as f:
        json.dump(rep, f, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    miss = [k for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False]
    log(f"director: {rep['score']}/{rep['of']}" + (f"; to look at: {', '.join(miss)}" if miss else "")
        + f"; {len(rep['stings'])} stings, {len(sil)} silences, camera {'/'.join(distinct) or 'hold'}")
    return rep


TEXTY = {"text", "hud", "optcard", "stamp", "dateline", "tipnum", "bignum", "dottext", "eqbar", "tracker", "lower_third",
         "card", "panel", "quote", "source", "chapter", "tiles", "clock", "nodes"}
MOVING_3D = {"video", "scene3d", "motion"}


def gate(ctx, log=print):
    """The showcase gate (owner, 2026-11-23: the bar is the 2026-11-22 Wi-Fi Short). Shorts only. Returns a list of misses;
    the run must fix them before posting (skill 3f/3g)."""
    job, scenes = ctx.job, ctx.job["scenes"]
    if ctx.W > ctx.H:
        return []
    miss = []
    total = float(sum(ctx.dur))
    want = int(total // 3.5)                                     # a new shot at least every 3.5 s
    shots = len(scenes)
    if shots < want:
        miss.append(f"only {shots} shots in {total:.0f} s (need >= {want}: a new shot every 2-4 s)")
    worst, where = 0, None                                       # on-screen text load, captions not counted
    for i, sc in enumerate(scenes):
        spans = []
        for L in sc.get("layers", []):
            if L.get("type") in TEXTY or (L.get("type") == "look" and L.get("texts", True)):
                a = float(L.get("at", 0)); b = float(L.get("until", L.get("at", 0) + L.get("dur", ctx.dur[i])))
                spans.append((a, b))
        for a, _ in spans:
            n = sum(1 for x, y in spans if x <= a + 0.05 < y)
            if n > worst:
                worst, where = n, i
    if worst > 2:
        miss.append(f"{worst} text pieces on screen at once in scene {where} (max 2 besides the captions)")
    mov = 0.0
    for i, sc in enumerate(scenes):
        if any(L.get("type") in MOVING_3D or (L.get("type") == "blender" and float(L.get("dur", 0.034)) > 0.05)
               for L in sc.get("layers", [])):
            mov += ctx.dur[i]
    if mov < 8.0:
        miss.append(f"only {mov:.1f} s of real moving 3D (need >= 8 s: Cutaway / animated Blender / scene3d / motion 3D)")
    m = job.get("meta", {})
    if m.get("role") and not (m.get("role_visual") or "").strip():
        miss.append(f"role '{m['role']}' is not shown: set meta.role_visual to the set, prop or wear piece that shows it")
    fam = set()                                                  # the owner's mix rules still apply under the bar
    for sc in scenes:
        for L in sc.get("layers", []):
            t = L.get("type")
            if t == "video" or (t == "blender" and float(L.get("dur", 0.034)) > 0.05) or t == "scene3d":
                fam.add("moving 3D")
            elif t == "character":
                fam.add("Ved in the world")
            elif t == "look":
                fam.add("look " + str(L.get("look", ""))[:5])
            elif t == "motion":
                fam.add("motion clip")
            elif t in ("hud", "eqbar", "crowd", "nodes", "tracker"):
                fam.add("data graphics")
            elif t in ("card", "panel", "optcard"):
                fam.add("cards")
            elif t == "image" and "photo" in str(L.get("path", "")).lower():
                fam.add("real photo")
            elif t in ("phone", "burst", "stamp", "dateline", "bignum", "tipnum", "dottext"):
                fam.add("case / device pieces")
    fam.discard("Ved in the world")
    if len(fam) < 3:
        miss.append(f"only {len(fam)} visual style(s) besides Ved ({', '.join(sorted(fam)) or 'none'}): mix at least 3")
    for k in ("lane", "role", "explain", "styles"):
        if not m.get(k):
            miss.append(f"meta.{k} missing: run `python -m autopilot variety` and record the choice")
    cap = {**ctx.style.get("captions", {}), **(job.get("style_override", {}).get("captions", {}))}
    if int(cap.get("words_per_chunk", 3)) > 2:
        miss.append("captions show more than 2 words at a time")
    log("gate: PASS" if not miss else "gate: FAIL; " + " | ".join(miss))
    return miss
