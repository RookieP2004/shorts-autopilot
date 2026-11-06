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
    return np.zeros(1, dtype=np.float32)


def duck_curve(vo, amount, smooth=0.18):
    a = np.abs(vo)
    w = int(smooth * SR)
    k = np.ones(w) / w
    e = np.convolve(a, k, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-4], 50) if np.any(e > 1e-4) else 1), 0, 1)
    return 1 - amount * e
