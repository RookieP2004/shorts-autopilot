"""Turn a job.json into a finished vertical Short (final.mp4)."""
import json
import multiprocessing as mp
import os
import re
import shutil
import subprocess
import sys
import wave

import numpy as np

from . import audio
from .scene import render_frame
from .spec import ROOT, deep_merge, job_style, load_characters, load_style, validate_job, load_json, BEATS, scene_beats


class Ctx:
    def __init__(self, job, style, chars, root=ROOT):
        self.job, self.style, self.chars, self.root = job, style, chars, root
        c = style["canvas"]
        self.W, self.H, self.fps = c["w"], c["h"], c["fps"]
        self.default_speaker = job.get("speaker") or style.get("default_speaker") or (
            next(iter(chars)) if chars else None)
        self.vo, self.env, self.captions, self.vis = [], [], [], []
        self.dur, self.start, self.frames = [], [], []
        self.beats = []
        self.total = 1.0
        self.shots_dir = None

    def envelope(self, i, t):
        e = self.env[i]
        k = int((t - self.lead_of(i)) * self.fps)
        return float(e[k]) if 0 <= k < len(e) else 0.0

    def viseme(self, i, t):
        v = self.vis[i]
        k = int((t - self.lead_of(i)) * self.fps)
        return v[k] if 0 <= k < len(v) else None

    def lead_of(self, i):
        return self.job["scenes"][i].get("lead", self.style["scene_lead"])


def render_assets(ctx, log=print):
    """Run the job's `assets_script` (Blender stills: sets and prop cut-outs) into jobs/<id>/assets/ (cached)."""
    sp = ctx.job.get("assets_script")
    if not sp or not ctx.shots_dir:
        return
    script = sp if os.path.isabs(sp) else os.path.join(ctx.root, sp)
    out = os.path.join(os.path.dirname(ctx.shots_dir), "..", "assets")
    out = os.path.normpath(out)
    log(f"  3D assets: {os.path.basename(script)}")
    r = subprocess.run([sys.executable, "-m", "autopilot.blendrun", "--assets", script, out], cwd=ctx.root,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"assets script failed ({script}):\n" + r.stdout[-1500:] + r.stderr[-3000:])
    log("   " + (r.stdout.strip().splitlines() or [""])[-1])


def render_shots(ctx, log=print):
    """Render every `blender` layer (cached per script + duration) before frames are drawn."""
    render_assets(ctx, log)
    if not ctx.shots_dir:
        return
    for i, s in enumerate(ctx.job["scenes"]):
        for j, L in enumerate(s.get("layers", [])):
            if L.get("type") != "blender":
                continue
            dur = L.get("dur", ctx.dur[i] - L.get("at", 0.0))
            fps = L.get("fps", ctx.fps)
            res = L.get("res", 0.5)
            w = int(round(ctx.W * L.get("w", 1.0) * res / 2)) * 2
            h = int(round(ctx.H * L.get("h", 1.0) * res / 2)) * 2
            out = os.path.join(ctx.shots_dir, f"s{i:02d}_l{j:02d}")
            L["_frames_dir"], L["_fps"] = out, fps
            script = L["script"] if os.path.isabs(L["script"]) else os.path.join(ctx.root, L["script"])
            cmd = [sys.executable, "-m", "autopilot.blendrun", script, out, f"{dur:.3f}", str(fps), str(w), str(h),
                   str(L.get("samples", 24))]
            log(f"  3D shot scene {i} layer {j}: {os.path.basename(script)} {w}x{h} {dur:.1f}s")
            r = subprocess.run(cmd, cwd=ctx.root, capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"blender shot failed ({script}):\n" + r.stdout[-1500:] + r.stderr[-3000:])
            log("   " + (r.stdout.strip().splitlines() or [""])[-1])


def voice_for(ctx, scene):
    v = dict(ctx.style["voice"])
    sp = scene.get("speaker", ctx.default_speaker)
    if sp and sp in ctx.chars:
        v.update(ctx.chars[sp]["meta"].get("voice", {}))
    v.update(ctx.job.get("voice", {}))
    v.update(scene.get("voice", {}))
    return v


def caption_chunks(text, t0, t1, per_chunk):
    words = text.replace("*", "").split()
    if not words:
        return []
    weights = []
    for w in words:
        wt = len(re.sub(r"[^\w]", "", w)) + 2
        if re.search(r"[,.;:!?]$", w):
            wt += 3
        weights.append(wt)
    tot = sum(weights)
    times, acc = [], t0
    for wt in weights:
        times.append(acc)
        acc += (t1 - t0) * wt / tot
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if len(cur) >= per_chunk or re.search(r"[,.;:!?]$", w) or i == len(words) - 1:
            chunks.append(cur)
            cur = []
    out = []
    for k, idxs in enumerate(chunks):
        s = times[idxs[0]]
        e = times[chunks[k + 1][0]] if k + 1 < len(chunks) else t1 + 0.25
        out.append((s, e, [words[i] for i in idxs], [times[i] for i in idxs]))
    return out


def prepare(ctx, log=print):
    st = ctx.style
    per = st["captions"].get("words_per_chunk", 3)
    t = 0.0
    for i, s in enumerate(ctx.job["scenes"]):
        lead = ctx.lead_of(i)
        if s.get("say"):
            v = voice_for(ctx, s)
            x = audio.tts(s["say"], v.get("voice"), v.get("speed", 1.0), v.get("lang", "en-us"))
            log(f"  scene {i}: voice {v.get('voice')} {len(x)/audio.SR:.2f}s")
        else:
            x = np.zeros(0, dtype=np.float32)
        speech = len(x) / audio.SR
        dur = max(s.get("dur", 0), s.get("min_dur", 1.2), lead + speech + s.get("pad", st["scene_pad"]))
        bl = []
        for b in scene_beats(s):                      # comedy beats: resolve time, stretch the scene to fit
            d = {**BEATS[b["kind"]], **b}
            at = d.get("at", "after_say")
            d["at"] = lead + speech + 0.15 if at == "after_say" else float(at)
            bl.append(d)
        dur = max([dur] + [b["at"] + b["dur"] + 0.3 for b in bl])
        ctx.beats.append(bl)
        frames = int(round(dur * ctx.fps))
        dur = frames / ctx.fps
        ctx.vo.append(x)
        env = audio.envelope(x, ctx.fps) if len(x) else np.zeros(0)
        ctx.env.append(env)
        ctx.vis.append(audio.visemes(env, audio.brightness(x, ctx.fps)) if len(x) else [])
        ctx.captions.append(caption_chunks(s.get("caption", s.get("say", "")), lead, lead + speech, per)
                            if s.get("say") else [])
        ctx.dur.append(dur)
        ctx.frames.append(frames)
        ctx.start.append(t)
        t += dur
    ctx.total = t
    render_shots(ctx, log)
    return t


_CTX = None


def _render_scene(args):
    i, out_dir = args
    ctx = _CTX
    W, H, fps = ctx.W, ctx.H, ctx.fps
    final = os.path.join(out_dir, f"scene_{i:03d}.mp4")
    tmp = os.path.join(out_dir, f"scene_{i:03d}.part.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(ctx.frames[i]):
        img = render_frame(ctx, i, f / fps)
        p.stdin.write(img.convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg failed on scene {i}")
    os.replace(tmp, final)
    return final


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(audio.SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def mix(ctx):
    st = ctx.style
    n = int(round(ctx.total * audio.SR))
    vo = np.zeros(n, dtype=np.float32)
    fx = np.zeros(n, dtype=np.float32)
    for i, s in enumerate(ctx.job["scenes"]):
        audio.add(vo, ctx.vo[i], ctx.start[i] + ctx.lead_of(i))
        name = s.get("sfx")
        if name is None and i > 0:
            tr = s.get("transition", st["transition"]["type"])
            name = "whoosh" if tr in ("slide_left", "slide_up", "zoom") else None
        if name and name != "none":
            audio.add(fx, audio.sfx(name, i) * st["sfx"]["volume"], ctx.start[i] + s.get("sfx_at", 0))
        for b in ctx.beats[i]:
            if b.get("sfx", "none") != "none":
                audio.add(fx, audio.sfx(b["sfx"], i) * st["sfx"]["volume"] * b.get("sfx_gain", 1.0), ctx.start[i] + b["at"])
        for L in s.get("layers", []):
            if L.get("sfx") and L["sfx"] != "none":
                audio.add(fx, audio.sfx(L["sfx"], i) * st["sfx"]["volume"], ctx.start[i] + L.get("at", 0))
    m = st["music"]
    jm = ctx.job.get("music", {})
    m = {**m, **jm}
    out = vo + fx
    if m.get("enabled", True):
        mus = audio.music(ctx.total, m)[:n]
        mus = np.pad(mus, (0, n - len(mus)))
        gain = np.ones(n, dtype=np.float32)            # beats with music "cut": a sudden, comic silence
        r = int(0.05 * audio.SR)
        for i, bl in enumerate(ctx.beats):
            for b in bl:
                if b.get("music") == "cut":
                    a = int((ctx.start[i] + b["at"]) * audio.SR)
                    e = int((ctx.start[i] + b["at"] + b["dur"]) * audio.SR)
                    a0, e1 = max(0, a - r), min(n, e + 4 * r)
                    gain[a0:a] = np.minimum(gain[a0:a], np.linspace(1, 0, a - a0))
                    gain[a:e] = 0
                    gain[e:e1] = np.minimum(gain[e:e1], np.linspace(0, 1, e1 - e))
        out = out + mus * gain * m.get("volume", 0.16) * audio.duck_curve(vo, m.get("duck", 0.4))
    return out


def render(job_path, out_dir, root=ROOT, workers=None, log=print):
    global _CTX
    job = load_json(job_path)
    style = job_style(job, root)   # channel style (+ long-form profile) + this job's one-off overrides
    chars = load_characters(root)
    errs = validate_job(job, style, chars, root)
    if errs:
        raise SystemExit("job invalid:\n  " + "\n  ".join(errs))
    os.makedirs(out_dir, exist_ok=True)
    ctx = Ctx(job, style, chars, root)
    ctx.shots_dir = os.path.join(os.path.dirname(os.path.abspath(job_path)), "out", "shots")
    log("voice + timing")
    total = prepare(ctx, log)
    log(f"total {total:.2f}s, {sum(ctx.frames)} frames")
    if total > style["max_duration"]:
        raise SystemExit(f"video is {total:.1f}s, over max_duration {style['max_duration']}s - cut lines")
    _CTX = ctx
    work = os.path.join(out_dir, "scenes")
    os.makedirs(work, exist_ok=True)
    n = len(job["scenes"])
    workers = workers or max(1, min(os.cpu_count() or 1, n))
    log(f"drawing {n} scenes on {workers} workers")
    with mp.get_context("fork").Pool(workers) as pool:
        files = pool.map(_render_scene, [(i, work) for i in range(n)])
    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{os.path.abspath(p)}'\n")
    silent = os.path.join(work, "video.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", silent], check=True)
    log("mixing audio")
    wav = os.path.join(work, "mix.wav")
    write_wav(wav, mix(ctx))
    final = os.path.join(out_dir, "final.mp4")
    tmp = os.path.join(out_dir, "final.part.mp4")
    lufs = style["loudness_lufs"]
    cap_mb = style.get("target_mb")       # long videos: keep the file small enough for Zapier and GitHub
    vargs = ["-c:v", "copy"]
    abr = "192k"
    if cap_mb:
        abr = "160k"
        kbps = min(4500, int(cap_mb * 8000 * 0.94 / total) - 160)
        log(f"encoding for <= {cap_mb} MB: {kbps} kb/s video")
    for attempt in range(3):
        if cap_mb:
            vargs = ["-c:v", "libx264", "-preset", "veryfast", "-tune", "animation", "-b:v", f"{kbps}k",
                     "-maxrate", f"{int(kbps * 1.4)}k", "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p", "-g", "60"]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                        *vargs, "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11", "-ar", "48000",
                        "-c:a", "aac", "-b:a", abr, "-shortest", "-movflags", "+faststart", tmp], check=True)
        mb = os.path.getsize(tmp) / 1e6
        if not cap_mb or mb <= cap_mb:
            break
        kbps = int(kbps * cap_mb / mb * 0.92)
        log(f"{mb:.1f} MB is over {cap_mb} MB, re-encoding at {kbps} kb/s")
    os.replace(tmp, final)
    info = {"duration": round(total, 2), "frames": sum(ctx.frames), "scenes": n,
            "size_mb": round(os.path.getsize(final) / 1e6, 1), "w": ctx.W, "h": ctx.H,
            "scene_starts": [round(s, 2) for s in ctx.start]}
    with open(os.path.join(out_dir, "render.json"), "w") as f:
        json.dump(info, f, indent=2)
    log(f"done -> {final}")
    return final, info


def draw_guides(img, style):
    """Shade the areas YouTube's Shorts UI covers (title, buttons) so previews show them."""
    from PIL import Image, ImageDraw
    W, H = img.size
    sz = style.get("safe_zone", {})
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    red = (255, 0, 60, 70)
    d.rectangle([0, int(sz.get("bottom", 0.78) * H), W, H], fill=red)
    d.rectangle([int(sz.get("right", 0.86) * W), int(H * 0.45), W, int(sz.get("bottom", 0.78) * H)], fill=red)
    d.rectangle([0, 0, W, int(sz.get("top", 0.08) * H)], fill=(255, 0, 60, 35))
    out = img.copy()
    out.alpha_composite(ov)
    return out


def frames(job_path, out_dir, times=None, root=ROOT, log=print, guides=True):
    """Draw stills for review. times=None -> the busiest moment of every scene."""
    job = load_json(job_path)
    style = job_style(job, root)   # channel style (+ long-form profile) + this job's one-off overrides
    chars = load_characters(root)
    errs = validate_job(job, style, chars, root)
    if errs:
        raise SystemExit("job invalid:\n  " + "\n  ".join(errs))
    ctx = Ctx(job, style, chars, root)
    ctx.shots_dir = os.path.join(os.path.dirname(os.path.abspath(job_path)), "out", "shots")
    prepare(ctx, log=lambda *a: None)
    os.makedirs(out_dir, exist_ok=True)
    outs = []
    if times is None:
        picks = []
        for i, s in enumerate(job["scenes"]):
            last_in = max([L.get("at", 0) + L.get("enter_dur", 0.4) for L in s.get("layers", [])] + [0.5])
            picks.append((i, min(ctx.dur[i] - 0.05, last_in + 0.15)))
    else:
        picks = []
        for T in times:
            i = max(k for k in range(len(ctx.start)) if ctx.start[k] <= T)
            picks.append((i, T - ctx.start[i]))
    for i, t in picks:
        p = os.path.join(out_dir, f"frame_s{i:02d}_{ctx.start[i]+t:05.2f}s.jpg")
        img = render_frame(ctx, i, t)
        if guides:
            img = draw_guides(img, style)
        img.convert("RGB").save(p, quality=88)
        outs.append(p)
    log(f"total {ctx.total:.2f}s")
    return outs


def thumbnail(job_path, out_path=None, root=ROOT, log=print):
    """YouTube thumbnail (1280x720 JPEG, under 2 MB) for a long video: one caption-free frame of the video at
    job["thumbnail"]["at"] seconds, with a big punchy title. *word* = accent colour.
      "thumbnail": {"at": 12.5, "text": "WHY IS PAPER *WORTH* ANYTHING?", "x": 0.30, "y": 0.30, "size": 150,
                    "max_w": 0.55, "zoom": 1.0, "focus": [0.5, 0.5]}"""
    from PIL import Image, ImageEnhance
    from . import sprites
    job = load_json(job_path)
    style = job_style(job, root)
    th = job.get("thumbnail") or {}
    ctx = Ctx(job, style, load_characters(root), root)
    ctx.shots_dir = os.path.join(os.path.dirname(os.path.abspath(job_path)), "out", "shots")
    prepare(ctx, log=lambda *a: None)
    ctx.captions = [[] for _ in ctx.captions]          # no captions on a thumbnail
    T = th.get("at") or ctx.total * 0.3
    i = max(k for k in range(len(ctx.start)) if ctx.start[k] <= T)
    img = render_frame(ctx, i, T - ctx.start[i]).convert("RGBA")
    W, H = img.size
    z = th.get("zoom", 1.0)
    if z > 1:
        fx, fy = th.get("focus", [0.5, 0.5])
        cw, ch = W / z, H / z
        x0 = min(max(0, fx * W - cw / 2), W - cw)
        y0 = min(max(0, fy * H - ch / 2), H - ch)
        img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(th.get("saturation", 1.18))
    img = ImageEnhance.Contrast(img).enhance(th.get("contrast", 1.08))
    if th.get("text"):
        t = sprites.text_image(style, th["text"], size=th.get("size", 150), font_name=th.get("font", "display"),
                               fill="primary", highlight="accent", stroke=th.get("stroke", "#1a1410"),
                               stroke_width=th.get("stroke_width", 14), max_w=th.get("max_w", 0.55),
                               align=th.get("align", "center"), uppercase=th.get("uppercase", True))
        from .scene import paste
        paste(img, t, th.get("x", 0.3) * W, th.get("y", 0.3) * H, 1.0, th.get("rot", 0), 1.0)
    out_path = out_path or os.path.join(os.path.dirname(os.path.abspath(job_path)), "out", "thumbnail.jpg")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = img.convert("RGB").resize((1280, 720), Image.LANCZOS)
    q = 92
    while True:
        img.save(out_path, quality=q, optimize=True)
        if os.path.getsize(out_path) < 1.9e6 or q < 60:
            break
        q -= 8
    log(f"thumbnail -> {out_path} ({os.path.getsize(out_path) / 1e3:.0f} KB)")
    return out_path
