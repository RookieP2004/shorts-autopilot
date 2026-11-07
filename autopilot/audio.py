"""Voice (Kokoro TTS), procedural music and sound effects, all generated in code."""
import os
import re

import numpy as np

from .spec import ROOT

SR = 48000
_kokoro = None


def _model_dir():
    return os.environ.get("AUTOPILOT_MODELS", os.path.join(ROOT, "models"))


def kokoro():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        d = _model_dir()
        _kokoro = Kokoro(os.path.join(d, "kokoro-v1.0.onnx"), os.path.join(d, "voices-v1.0.bin"))
    return _kokoro


def clean_for_tts(text):
    text = text.replace("*", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def resample(x, sr_in, sr_out=SR):
    if sr_in == sr_out:
        return x.astype(np.float32)
    n = int(round(len(x) * sr_out / sr_in))
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def tts(text, voice="am_michael", speed=1.0, lang="en-us"):
    """Return mono float32 at SR. Voices can be blended: 'af_heart:0.6,af_bella:0.4'."""
    k = kokoro()
    v = voice
    if "," in voice:
        parts = [p.split(":") for p in voice.split(",")]
        v = sum(k.get_voice_style(n) * float(w) for n, w in parts)
    samples, sr = k.create(clean_for_tts(text), voice=v, speed=speed, lang=lang)
    x = resample(np.asarray(samples, dtype=np.float32), sr)
    # trim leading/trailing silence
    a = np.abs(x)
    idx = np.where(a > 0.01)[0]
    if len(idx):
        x = x[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.06 * SR)]
    return x


def envelope(x, fps):
    """Loudness per video frame, 0..1 (drives mouth animation)."""
    hop = SR / fps
    n = int(np.ceil(len(x) / hop))
    env = np.array([np.sqrt(np.mean(x[int(i * hop):int((i + 1) * hop)] ** 2) + 1e-12) for i in range(n)])
    if env.max() > 0:
        env = env / np.percentile(env, 95).clip(1e-6)
    return np.clip(env, 0, 1)


def brightness(x, fps):
    """Per-frame spectral centroid, 0..1 (low = round vowels 'o/oo', high = 'ee/s/t' sounds)."""
    hop = int(SR / fps)
    n = int(np.ceil(len(x) / hop))
    win = np.hanning(hop * 2)
    freqs = np.fft.rfftfreq(hop * 2, 1 / SR)
    out = np.zeros(n)
    for i in range(n):
        seg = x[i * hop: i * hop + hop * 2]
        if len(seg) < hop * 2:
            seg = np.pad(seg, (0, hop * 2 - len(seg)))
        mag = np.abs(np.fft.rfft(seg * win))
        band = (freqs > 80) & (freqs < 6000)
        tot = mag[band].sum()
        out[i] = (mag[band] * freqs[band]).sum() / tot if tot > 1e-6 else 0
    return np.clip((out - 500) / 2500, 0, 1)


def visemes(env, bright, hold=2):
    """Pick a mouth shape per frame from loudness + brightness, holding each shape >= `hold` frames."""
    import numpy as _np
    voiced = _np.array([b for e, b in zip(env, bright) if e >= 0.12])
    if len(voiced) > 4:                       # brightness relative to THIS voice line (deep voices read dark)
        lo, hi = _np.percentile(voiced, 15), _np.percentile(voiced, 85)
        bright = _np.clip((_np.asarray(bright) - lo) / max(1e-6, hi - lo), 0, 1)
    raw = []
    for e, b in zip(env, bright):
        if e < 0.12:
            raw.append(None)                      # closed
        elif e < 0.32:
            raw.append("m1")
        elif e < 0.62:
            raw.append("oo" if b < 0.18 else ("ee" if b > 0.8 else "talk"))
        else:
            raw.append("oo" if b < 0.12 else ("ee" if b > 0.88 else "m3"))
    out, cur, left = [], None, 0
    for v in raw:
        if left > 0 and v != cur:
            out.append(cur)
            left -= 1
            continue
        if v != cur:
            cur, left = v, hold - 1
        else:
            left = max(0, left - 1)
        out.append(cur)
    return out


# ---------------- music ----------------
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
SCALES = {"minor": [0, 2, 3, 5, 7, 8, 10], "major": [0, 2, 4, 5, 7, 9, 11],
          "dorian": [0, 2, 3, 5, 7, 9, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10],
          "mixolydian": [0, 2, 4, 5, 7, 9, 10], "harmonic_minor": [0, 2, 3, 5, 7, 8, 11]}


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tone(freq, dur, harmonics=(1, 0.5, 0.25), attack=0.01, decay=None, release=0.08, vib=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = 2 * np.pi * freq * t
    if vib:
        ph = ph + vib * np.sin(2 * np.pi * 5.2 * t)
    y = sum(a * np.sin(ph * (i + 1)) for i, a in enumerate(harmonics))
    env = np.ones(n)
    na = max(1, int(attack * SR))
    env[:na] = np.linspace(0, 1, na)
    if decay:
        env *= np.exp(-t / decay)
    nr = min(n, int(release * SR))
    if nr > 0:
        env[-nr:] *= np.linspace(1, 0, nr)
    return (y * env).astype(np.float32)


def kick(dur=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 9)).astype(np.float32)


def noise_hit(dur, decay, hp=True, rng=None):
    rng = rng or np.random.default_rng(0)
    n = int(dur * SR)
    x = rng.standard_normal(n)
    if hp:
        x = np.diff(x, prepend=0)
    t = np.arange(n) / SR
    return (x * np.exp(-t / decay) * 0.5).astype(np.float32)


def snare(rng):
    x = noise_hit(0.22, 0.05, True, rng) * 0.8
    body = tone(185, 0.12, (1,), 0.001, 0.04, 0.02) * 0.5
    x[: len(body)] += body
    return x


def add(buf, x, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]


def music(duration, cfg):
    """Procedural loop: pad + bass + keys arp + drums. Same cfg = same sound every video."""
    style = cfg.get("style", "lofi")
    rng = np.random.default_rng(cfg.get("seed", 7))
    bpm = cfg.get("bpm", 90)
    beat = 60 / bpm
    bar = 4 * beat
    root = 48 + NOTE.get(cfg.get("key", "A"), 9)  # around C3
    sc = SCALES.get(cfg.get("scale", "minor"), SCALES["minor"])
    prog = cfg.get("progression", [1, 6, 3, 7])
    bars_per_chord = cfg.get("bars_per_chord", 1)
    loop_bars = len(prog) * bars_per_chord
    loop_len = loop_bars * bar
    buf = np.zeros(int(loop_len * SR) + SR, dtype=np.float32)

    def deg(d, octave=0):
        d0 = d - 1
        return root + sc[d0 % 7] + 12 * (d0 // 7 + octave)

    arp_pat = rng.permutation([0, 1, 2, 3, 2, 1, 0, 2])
    swing = 0.08 if style == "lofi" else 0.0
    for ci, d in enumerate(prog):
        t0 = ci * bars_per_chord * bar
        cl = bars_per_chord * bar
        chord = [deg(d), deg(d + 2), deg(d + 4), deg(d + 6)]
        # pad
        pad_h = (1, 0.35, 0.15, 0.06) if style != "upbeat" else (1, 0.5, 0.3, 0.15)
        for m in chord[:3]:
            for det in (-0.06, 0.06):
                add(buf, tone(mtof(m + 12 + det), cl + 0.4, pad_h, attack=0.35, release=0.5, vib=0.002) * 0.07, t0)
        # bass
        bass_hits = [0, 2] if style in ("lofi", "suspense") else [0, 1, 2, 3] if style == "upbeat" else [0]
        for b in range(bars_per_chord):
            for h in bass_hits:
                add(buf, tone(mtof(chord[0] - 12), beat * 0.95, (1, 0.25), 0.005, 0.5, 0.05) * 0.32,
                    t0 + b * bar + h * beat)
        # arp keys
        if style != "suspense":
            steps = int(cl / (beat / 2))
            for s in range(steps):
                if style == "ambient" and s % 2:
                    continue
                m = chord[arp_pat[s % 8] % 4] + 12
                off = swing * beat if s % 2 else 0
                vel = 0.10 * (0.8 + 0.4 * rng.random())
                add(buf, tone(mtof(m), beat * 0.9, (1, 0.3, 0.1), 0.004, 0.28, 0.05) * vel,
                    t0 + s * beat / 2 + off)
        else:
            for b in range(int(cl / beat)):
                add(buf, tone(mtof(chord[0] + 24), 0.12, (1, 0.2), 0.002, 0.05, 0.03) * 0.08, t0 + b * beat)
        # drums
        if style in ("lofi", "upbeat", "suspense"):
            for b in range(int(cl / beat)):
                bt = t0 + b * beat
                if style == "upbeat" or b % 4 in (0, 2) and style == "lofi" or (style == "suspense" and b % 4 == 0):
                    add(buf, kick() * 0.55, bt)
                if b % 4 in (1, 3) and style != "suspense":
                    add(buf, snare(rng) * (0.32 if style == "lofi" else 0.4), bt)
                for hh in (0, 1):
                    off = (swing * beat if hh else 0)
                    add(buf, noise_hit(0.05, 0.012, True, rng) * 0.10, bt + hh * beat / 2 + off)
    loop = buf[: int(loop_len * SR)]
    # soften loop seam: carry the tail of the buffer into the start
    tail = buf[int(loop_len * SR):]
    loop[: len(tail)] += tail
    reps = int(np.ceil(duration / loop_len)) + 1
    full = np.tile(loop, reps)[: int(duration * SR)]
    if style == "lofi":  # gentle low-pass + vinyl hiss
        k = np.ones(5) / 5
        full = np.convolve(full, k, mode="same")
        full += rng.standard_normal(len(full)).astype(np.float32) * 0.003
    fo = min(len(full), int(1.5 * SR))
    full[-fo:] *= np.linspace(1, 0, fo)
    fi = min(len(full), int(0.3 * SR))
    full[:fi] *= np.linspace(0, 1, fi)
    peak = np.abs(full).max()
    return (full / peak * 0.9).astype(np.float32) if peak > 0 else full


# ---------------- sfx ----------------
def sfx(name, seed=1):
    rng = np.random.default_rng(seed)
    if name == "pop":
        n = int(0.12 * SR)
        t = np.arange(n) / SR
        f = 900 * np.exp(-t * 25) + 300
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35)).astype(np.float32) * 0.8
    if name == "click":
        return noise_hit(0.03, 0.004, True, rng) * 1.5
    if name == "ding":
        return (tone(1318, 0.9, (1, 0.0, 0.3, 0, 0.1), 0.002, 0.35, 0.1) * 0.5)
    if name == "boom":
        x = kick(0.9)
        nz = noise_hit(0.6, 0.15, False, rng) * 0.25
        x[: len(nz)] += nz
        return x
    if name in ("whoosh", "riser"):
        dur = 0.45 if name == "whoosh" else 1.2
        n = int(dur * SR)
        x = rng.standard_normal(n)
        spec = np.fft.rfft(x)
        freqs = np.fft.rfftfreq(n, 1 / SR)
        out = np.zeros(n)
        # sweep a band through the noise in 8 slices
        for k in range(8):
            fc = 300 * (12 ** (k / 7)) if name == "riser" else 3000 * (0.25 ** (abs(k - 3.5) / 3.5))
            band = np.exp(-((freqs - fc) / (fc * 0.6)) ** 2)
            seg = np.fft.irfft(spec * band, n)
            w = np.zeros(n)
            a, b = int(n * k / 8), int(n * (k + 1) / 8)
            w[a:b] = 1
            w = np.convolve(w, np.hanning(n // 8) / (n // 16), mode="same")
            out += seg * w
        env = np.sin(np.linspace(0, np.pi, n)) ** (1.5 if name == "whoosh" else 0.6)
        out = out * env
        return (out / (np.abs(out).max() + 1e-9) * 0.6).astype(np.float32)
    if name == "scratch":
        # record scratch: a short "recording" (warm chord + crackle) scrubbed forward, back, forward
        src_n = int(1.2 * SR)
        ts = np.arange(src_n) / SR
        src = sum(np.sin(2 * np.pi * f * ts) for f in (196, 247, 294, 392)) * 0.25
        src = src + np.convolve(rng.standard_normal(src_n), np.ones(6) / 6, mode="same") * 0.35
        n = int(0.42 * SR)
        t = np.arange(n) / SR
        rate = 1.0 - 2.6 * np.sin(np.pi * np.clip(t / 0.22, 0, 1)) + 1.8 * np.clip((t - 0.22) / 0.2, 0, 1)
        pos = 0.3 * SR + np.cumsum(rate * 3.0)
        x = np.interp(np.clip(pos, 0, src_n - 1), np.arange(src_n), src)
        env = np.minimum(1, t / 0.01) * np.exp(-np.maximum(0, t - 0.3) * 18)
        return (x / (np.abs(x).max() + 1e-9) * env * 0.8).astype(np.float32)
    if name == "crickets":
        # awkward-silence crickets: two far-off chirps
        n = int(1.4 * SR)
        x = np.zeros(n)
        for c0, f in ((0.12, 4300), (0.62, 4550)):
            for k in range(3):
                a = int((c0 + k * 0.045) * SR)
                m = int(0.03 * SR)
                tt = np.arange(m) / SR
                x[a:a + m] += np.sin(2 * np.pi * f * tt) * np.sin(np.pi * tt / 0.03) ** 2
        return (x * 0.22).astype(np.float32)
    if name == "wah":
        # comic "wah-wah" droop: two falling notes with a wobble
        out = []
        for f0, f1, d in ((233, 220, 0.32), (220, 165, 0.75)):
            n = int(d * SR)
            t = np.arange(n) / SR
            f = np.linspace(f0, f1, n) * (1 + 0.025 * np.sin(2 * np.pi * 6 * t) * (t / d))
            ph = 2 * np.pi * np.cumsum(f) / SR
            v = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
            out.append(v * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.08))
        x = np.concatenate(out)
        return (x / np.abs(x).max() * 0.45).astype(np.float32)
    return np.zeros(1, dtype=np.float32)


def duck_curve(vo, amount, smooth=0.18):
    a = np.abs(vo)
    w = int(smooth * SR)
    k = np.ones(w) / w
    e = np.convolve(a, k, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-4], 50) if np.any(e > 1e-4) else 1), 0, 1)
    return 1 - amount * e
