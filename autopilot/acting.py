"""Acting: the character changes gestures while he talks, easing smoothly between poses.

A character whose folder has a rig (characters/<id>/make.py exposing figure(arms=...), ARMS and BASES)
is drawn fresh every frame from interpolated arm positions, so pose changes are real motion,
not cuts or crossfades. Nothing wobbles frame to frame: the body only moves during a gesture change.

Layer options (job.json, type "character"):
  "acting": "auto"   (default) pick gestures at natural pauses in the speech, every ~1.6-2.8 s
  "acting": "none"   hold the layer's pose for the whole scene
  "acting": [["explain", 0.0], ["point", 1.4], ["crossed", 3.2]]   explicit gestures at scene times
Gesture names are the rig's BASES keys (idle, warm, serious, explain, point, think, welcome, surprised, crossed).
"""
import importlib.util
import math
import os
import random
import zlib

_RIGS = {}
TRANSITION = 0.42                     # seconds to move from one pose to the next
WEIGHTS = {"explain": 3.0, "warm": 2.0, "welcome": 1.2, "point": 1.2, "crossed": 1.0,
           "think": 0.6, "surprised": 0.45, "serious": 0.6, "idle": 0.8}


def rig(ch):
    """Load characters/<id>/make.py as a rig (cached), or None if it isn't one."""
    cid = ch["id"]
    if cid not in _RIGS:
        p = os.path.join(ch["dir"], "make.py")
        mod = None
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location(f"rig_{cid}", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if not all(hasattr(mod, a) for a in ("figure", "ARMS", "BASES")):
                mod = None
        _RIGS[cid] = mod
    return _RIGS[cid]


def base_of(pose, r):
    """'explain_talk' -> 'explain'; unknown -> 'idle'."""
    for b in sorted(r.BASES, key=len, reverse=True):
        if pose == b or pose.startswith(b + "_"):
            return b
    return "idle"


def track(ctx, scene_idx, L, r):
    """List of (start_time, gesture) for this layer in this scene."""
    key = (scene_idx, id(L))
    cache = ctx.__dict__.setdefault("_tracks", {})
    if key in cache:
        return cache[key]
    start = base_of(L.get("pose", "idle"), r)
    mode = L.get("acting", "auto")
    if isinstance(mode, list):
        tr = [(float(t), g) for g, t in mode]
        if not tr or tr[0][0] > 0:
            tr.insert(0, (0.0, start))
    elif mode == "none" or not ctx.job["scenes"][scene_idx].get("say"):
        tr = [(0.0, start)]
    else:
        tr = [(0.0, start)]
        env = ctx.env[scene_idx]
        lead, dur, fps = ctx.lead_of(scene_idx), ctx.dur[scene_idx], ctx.fps
        rng = random.Random(zlib.crc32(f"{ctx.job.get('id')}/{scene_idx}".encode()))
        pool = [g for g in WEIGHTS if g in r.BASES]
        last, cur = 0.0, start
        while True:
            lo, hi = last + 1.6, last + 2.8
            if lo > dur - 0.9:
                break
            hi = min(hi, dur - 0.9)
            # switch on the quietest moment in the window (a pause between words)
            best, best_e = lo, 9.0
            t = lo
            while t <= hi:
                k = int((t - lead) * fps)
                e = env[k] if 0 <= k < len(env) else 0.0
                if e < best_e:
                    best, best_e = t, e
                t += 1 / fps
            choices = [g for g in pool if g != cur and not (g == "surprised" and cur == "surprised")]
            w = [WEIGHTS[g] for g in choices]
            nxt = rng.choices(choices, weights=w)[0]
            tr.append((best, nxt))
            last, cur = best, nxt
    for b in getattr(ctx, "beats", [])[scene_idx] if scene_idx < len(getattr(ctx, "beats", [])) else []:
        if b["kind"] not in r.BASES or (b.get("who") and b["who"] != L.get("id")):
            continue
        a, e = b["at"], b["at"] + b["dur"]
        before = [g for ts, g in tr if ts <= a][-1]
        tr = [(ts, g) for ts, g in tr if ts == 0 or not (a - 0.6 < ts < e + 0.6)]
        tr += [(a, b["kind"]), (e, before)]
        tr.sort(key=lambda x: x[0])
    cache[key] = tr
    return tr


def _lerp(a, b, p):
    return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)


def blend_arms(a_arms, b_arms, p):
    """Interpolate two arm configs (matched by side), easing p in 0..1."""
    ea = sorted(a_arms, key=lambda x: x[0][0])
    eb = sorted(b_arms, key=lambda x: x[0][0])
    out = []
    for (s1, e1, w1, k1, f1), (s2, e2, w2, k2, f2) in zip(ea, eb):
        out.append((_lerp(s1, s2, p), _lerp(e1, e2, p), _lerp(w1, w2, p),
                    k1 if p < 0.5 else k2, f1 if p < 0.5 else f2))
    order = a_arms if p < 0.5 else b_arms                 # keep the target's drawing order (who is on top)
    side = {round(x[0][0]) > 300: x for x in out}
    return [side[round(o[0][0]) > 300] for o in order]


def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def arms_at(r, tr, t):
    """(arms, gesture) at scene time t."""
    idx = 0
    for i, (ts, _) in enumerate(tr):
        if t >= ts:
            idx = i
    g = tr[idx][1]
    tgt = r.ARMS[r.BASES[g][0]]
    if idx > 0 and t - tr[idx][0] < TRANSITION:
        prev = r.ARMS[r.BASES[tr[idx - 1][1]][0]]
        return blend_arms(prev, tgt, ease((t - tr[idx][0]) / TRANSITION)), g
    return tgt, g
