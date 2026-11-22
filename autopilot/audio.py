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


def narrator(text, voice, speed=1.0, lang="en-us", pitch=0.0, warmth=0.0):
    """TTS with a deeper, fuller 'documentary narrator' delivery, without artefacts: speak faster by the pitch factor,
    then resample slower, so the length is unchanged and the pitch drops (pitch in semitones, e.g. -1.5).
    warmth 0..1 adds low-mid body and gentle compression (a close, intimate mic)."""
    if not pitch and not warmth:
        return tts(text, voice, speed, lang)
    f = 2 ** (pitch / 12.0)                      # < 1 for a lower voice
    x = tts(text, voice, speed / f, lang)
    if pitch:
        n = int(len(x) / f)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    if warmth:
        k = int(SR / 900)                        # body: add a low-passed copy (~<900 Hz)
        lp = np.convolve(x, np.ones(k) / k, mode="same")
        x = x + warmth * 0.6 * lp
        pk = np.abs(x).max() + 1e-9
        x = np.tanh(x / pk * (1 + 1.5 * warmth)) / np.tanh(1 + 1.5 * warmth) * 0.95   # soft compression
    return x.astype(np.float32)


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

    if cfg.get("instruments", "real") == "real" and os.environ.get("MUSIC_SOURCE") != "synth":
        from . import orchestra                    # sampled CC0 instruments (Lemo-Opuscar's sampler)
        if orchestra.available():
            try:
                return orchestra.music(duration, cfg, root, sc, prog, bars_per_chord, beat, SR)
            except Exception as e:                 # a broken pack never blocks a render: fall back to the synth
                print(f"orchestra: {e}; using the synth")

    if style in ("doc", "tension", "wonder"):
        return _doc_music(duration, cfg, rng, root, sc, prog, bars_per_chord, bar, beat)
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


def _doc_music(duration, cfg, rng, root, sc, prog, bars_per_chord, bar, beat):
    """Documentary underscore. doc: warm string pad + sparse felt piano. tension: low drone + ticking pulse +
    high shimmer. wonder: open pad + slow rising arpeggio. No drums, lots of air."""
    style = cfg.get("style")
    n_total = int(duration * SR) + SR
    buf = np.zeros(n_total, np.float32)

    def deg(d, octave=0):
        d0 = d - 1
        return root + sc[d0 % 7] + 12 * (d0 // 7 + octave)

    t0 = 0.0
    ci = 0
    while t0 < duration:
        d = prog[ci % len(prog)]
        cl = bars_per_chord * bar
        chord = [deg(d), deg(d + 2), deg(d + 4), deg(d + 6)]
        pad_h = (1, 0.3, 0.12, 0.05)
        for m in chord[:3]:
            for det in (-0.07, 0.07):
                add(buf, tone(mtof(m + 12 + det), cl + 1.2, pad_h, attack=1.2, release=1.4, vib=0.003) *
                    (0.05 if style != "tension" else 0.03), t0)
        add(buf, tone(mtof(chord[0] - 12), cl + 0.8, (1, 0.4, 0.15), 0.8, None, 1.0) * 0.16, t0)   # low string root
        if style == "doc":                     # felt piano: a few notes per chord, never on a grid
            k = 0.0
            while k < cl - 0.2:
                m = chord[int(rng.integers(0, 4))] + 12 * int(rng.integers(1, 3))
                add(buf, tone(mtof(m), 2.4, (1, 0.45, 0.12, 0.05), 0.004, 1.6, 0.9) * rng.uniform(0.05, 0.09), t0 + k)
                k += beat * rng.choice([1.5, 2, 2.5, 3])
        elif style == "tension":               # heartbeat-like low pulse + high glassy shimmer
            for b in range(int(cl / (beat / 2))):
                add(buf, tone(mtof(chord[0] - 12), 0.18, (1, 0.3), 0.003, 0.12, 0.05) * (0.11 if b % 2 == 0 else 0.06),
                    t0 + b * beat / 2)
            add(buf, tone(mtof(chord[2] + 36), cl, (1, 0.2), 1.5, None, 1.0) * 0.012, t0)
        else:                                  # wonder: slow arpeggio climbing through the chord
            steps = int(cl / beat)
            for s_ in range(steps):
                m = chord[s_ % 4] + 12 * (1 + s_ // 4)
                add(buf, tone(mtof(m), beat * 2.2, (1, 0.35, 0.1), 0.01, 1.2, 0.6) * 0.06, t0 + s_ * beat)
        t0 += cl
        ci += 1
    full = buf[: int(duration * SR)]
    full += rng.standard_normal(len(full)).astype(np.float32) * 0.0015       # a little air
    fo = min(len(full), int(2.5 * SR))
    full[-fo:] *= np.linspace(1, 0, fo)
    fi = min(len(full), int(1.0 * SR))
    full[:fi] *= np.linspace(0, 1, fi)
    peak = np.abs(full).max()
    return (full / peak * 0.9).astype(np.float32) if peak > 0 else full


# ---------------- sfx ----------------
LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sfx", "lib")
_LIB_CACHE = {}
SOURCE_RANK = ("ov_", "ui_", "cw_", "es_")   # real recordings (Openverse CC0) > CC0 UI pack > Cutaway CC0 set > earshot renders > synth


def lib_takes(name):
    """Library files for a sound name, best source first (scripts/build_sfx_lib.py, scripts/openverse_fetch.py)."""
    d = os.path.join(LIB, name)
    if not os.path.isdir(d):
        return []
    fs = sorted(f for f in os.listdir(d) if f.endswith((".flac", ".wav", ".ogg")))
    for pre in SOURCE_RANK:
        best = [f for f in fs if f.startswith(pre)]
        if best:
            return [os.path.join(d, f) for f in best]
    return [os.path.join(d, f) for f in fs]


def _load(path):
    if path not in _LIB_CACHE:
        import soundfile as sf
        x, sr = sf.read(path, dtype="float32", always_2d=False)
        if x.ndim > 1:
            x = x.mean(axis=1)
        _LIB_CACHE[path] = resample(x, sr, SR).astype(np.float32) if sr != SR else x
    return _LIB_CACHE[path]


PEAK_SYNC = {"press","latch","ratchet","chime","hit", "thud", "stomp", "stamp", "boom", "pop", "click", "ding", "coin", "cash", "shutter", "door", "splash", "tick",
             "braam", "register", "notify", "error", "success", "lock", "glitch", "slide", "paper", "tape"}
APEX_LATE = {"whoosh", "swoosh_soft", "riser", "sweep"}


def peak_time(x, smooth=0.01):
    """Seconds from the start of a sound to its loudest moment (smoothed envelope)."""
    if len(x) < 4:
        return 0.0
    k = max(1, int(smooth * SR))
    env = np.convolve(np.abs(x), np.ones(k) / k, mode="same")
    return float(np.argmax(env)) / SR


def sfx(name, seed=1, source=None):
    """A sound effect by name. Library first (real recordings, CC0 UI sounds, earshot renders; a different take per seed so
    repeats never sound identical), then the built-in synth. source="synth" forces the old synthesized version."""
    if source != "synth" and os.environ.get("SFX_SOURCE", "library") != "synth":
        takes = lib_takes(name)
        if takes:
            return _load(takes[seed % len(takes)]) * 1.0
    return _sfx_synth(name, seed)


def _sfx_synth(name, seed=1):
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
    doc = _doc_sfx(name, rng)
    if doc is not None:
        return doc
    return np.zeros(1, dtype=np.float32)


def _bandnoise(n, lo, hi, rng):
    x = rng.standard_normal(n)
    sp = np.fft.rfft(x)
    fr = np.fft.rfftfreq(n, 1 / SR)
    sp[(fr < lo) | (fr > hi)] = 0
    y = np.fft.irfft(sp, n)
    return y / (np.abs(y).max() + 1e-9)


def _doc_sfx(name, rng):
    """Foley for the documentary look: paper, tape, marker, camera shutter, typewriter, soft thud, deep hit."""
    if name == "paper":                     # a card or photo laid down: crinkly rustle
        n = int(0.42 * SR)
        x = _bandnoise(n, 1500, 9000, rng)
        t = np.arange(n) / SR
        env = np.zeros(n)
        for c in rng.uniform(0, 0.3, 7):
            env += np.exp(-np.maximum(0, t - c) * 28) * (t >= c) * rng.uniform(0.4, 1)
        return (x * env / (env.max() + 1e-9) * 0.35).astype(np.float32)
    if name == "tape":                      # a strip of tape pulled and pressed
        n = int(0.3 * SR)
        t = np.arange(n) / SR
        x = _bandnoise(n, 800, 7000, rng) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 70 * t)))
        env = np.minimum(1, t / 0.01) * np.exp(-t * 9)
        return (x * env * 0.3).astype(np.float32)
    if name == "marker":                    # felt-tip squeak and scratch while drawing (about 0.6 s)
        n = int(0.6 * SR)
        t = np.arange(n) / SR
        x = _bandnoise(n, 2000, 6000, rng) * (0.55 + 0.45 * np.sin(2 * np.pi * 9 * t + rng.uniform(0, 6)))
        sq = np.sin(2 * np.pi * (1900 + 300 * np.sin(2 * np.pi * 3 * t)) * t) * 0.15
        env = np.minimum(1, t / 0.03) * np.minimum(1, (0.6 - t) / 0.08)
        return ((x * 0.6 + sq) * env * 0.22).astype(np.float32)
    if name == "shutter":                   # film camera: two mechanical clicks
        out = np.zeros(int(0.18 * SR), np.float32)
        for at, g in ((0.0, 1.0), (0.075, 0.7)):
            h = noise_hit(0.04, 0.006, True, rng) * g
            add(out, h, at)
        return out / (np.abs(out).max() + 1e-9) * 0.6
    if name == "type":                      # typewriter: a burst of keys and a carriage ding-less return
        out = np.zeros(int(1.0 * SR), np.float32)
        at = 0.0
        while at < 0.85:
            add(out, noise_hit(0.025, 0.004, True, rng) * rng.uniform(0.5, 1.0), at)
            at += rng.uniform(0.06, 0.13)
        return out / (np.abs(out).max() + 1e-9) * 0.42
    if name == "thud":                      # a soft low thud (a book, a folder on a desk)
        n = int(0.35 * SR)
        t = np.arange(n) / SR
        x = np.sin(2 * np.pi * (90 * np.exp(-t * 6) + 45) * t) * np.exp(-t * 14)
        x = x + _bandnoise(n, 100, 1200, rng) * np.exp(-t * 40) * 0.3
        return (x * 0.6).astype(np.float32)
    if name == "hit":                       # cinematic low hit with a long tail (chapter cards, reveals)
        n = int(2.4 * SR)
        t = np.arange(n) / SR
        x = np.sin(2 * np.pi * (55 * np.exp(-t * 1.5) + 30) * t) * np.exp(-t * 1.6)
        x = x + _bandnoise(n, 40, 600, rng) * np.exp(-t * 2.5) * 0.35
        x = x + _bandnoise(n, 3000, 9000, rng) * np.exp(-t * 18) * 0.15
        return (x / np.abs(x).max() * 0.7).astype(np.float32)
    if name == "swoosh_soft":               # gentle air movement for whip pans
        n = int(0.5 * SR)
        t = np.arange(n) / SR
        x = _bandnoise(n, 300, 4000, rng) * np.sin(np.pi * t / 0.5) ** 2
        return (x * 0.28).astype(np.float32)
    if name == "splash":                    # something hits water: thump + spray
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        thump = np.sin(2 * np.pi * (120 * np.exp(-t * 9) + 50) * t) * np.exp(-t * 12) * 0.7
        spray = _bandnoise(n, 900, 9000, rng) * (np.minimum(1, t / 0.02) * np.exp(-t * 4.5)) * 0.55
        drops = np.zeros(n)
        for c in rng.uniform(0.15, 0.8, 14):
            a = int(c * SR)
            m = min(n - a, int(0.04 * SR))
            tt = np.arange(m) / SR
            drops[a:a + m] += np.sin(2 * np.pi * rng.uniform(900, 2400) * tt * (1 + 6 * tt)) * np.exp(-tt * 90) * 0.25
        x = thump + spray + drops
        return (x / np.abs(x).max() * 0.7).astype(np.float32)
    if name == "bubbles":                   # underwater bubbles rising
        n = int(1.2 * SR)
        x = np.zeros(n)
        for c in rng.uniform(0, 1.05, 22):
            a = int(c * SR)
            m = min(n - a, int(0.06 * SR))
            tt = np.arange(m) / SR
            f0 = rng.uniform(300, 900)
            x[a:a + m] += np.sin(2 * np.pi * f0 * tt * (1 + 9 * tt)) * np.exp(-tt * 55) * rng.uniform(0.3, 1)
        x = np.convolve(x, np.ones(6) / 6, mode="same") + _bandnoise(n, 80, 400, rng) * 0.05
        return (x / np.abs(x).max() * 0.45).astype(np.float32)
    if name in ("footsteps", "stomp"):      # footsteps on a hard floor; stomp = one heavy step
        steps = [0.0] if name == "stomp" else [0.0, 0.42, 0.84, 1.26]
        n = int((steps[-1] + 0.4) * SR)
        x = np.zeros(n)
        for k, c in enumerate(steps):
            m = int(0.25 * SR)
            tt = np.arange(m) / SR
            g = 1.0 if name == "stomp" else rng.uniform(0.6, 0.9)
            hit = np.sin(2 * np.pi * (85 if name == "stomp" else 140) * tt) * np.exp(-tt * (18 if name == "stomp" else 35))
            hit = hit + _bandnoise(m, 300, 3000, rng) * np.exp(-tt * 60) * 0.5
            a = int(c * SR)
            x[a:a + m] += hit[: n - a] * g
        return (x / np.abs(x).max() * (0.75 if name == "stomp" else 0.5)).astype(np.float32)
    if name == "heartbeat":                 # two slow beats (lub-dub)
        n = int(1.9 * SR)
        x = np.zeros(n)
        for c in (0.0, 0.95):
            for d, g in ((0.0, 1.0), (0.24, 0.7)):
                m = int(0.18 * SR)
                tt = np.arange(m) / SR
                a = int((c + d) * SR)
                x[a:a + m] += np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 22) * g
        return (x / np.abs(x).max() * 0.8).astype(np.float32)
    if name == "tick":                      # clock ticking, 4 ticks
        n = int(2.1 * SR)
        x = np.zeros(n)
        for k in range(4):
            a = int(k * 0.5 * SR)
            h = noise_hit(0.02, 0.003, True, rng) * (1.0 if k % 2 == 0 else 0.7)
            x[a:a + len(h)] += h
        return (x / np.abs(x).max() * 0.45).astype(np.float32)
    if name == "slide":                     # a box or object pushed across a counter
        n = int(0.7 * SR)
        t = np.arange(n) / SR
        x = _bandnoise(n, 200, 2500, rng) * np.sin(np.pi * t / 0.7) ** 0.6
        x = x * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * t))
        return (x * 0.32).astype(np.float32)
    if name == "cash":                      # banknotes riffled
        n = int(0.6 * SR)
        x = np.zeros(n)
        for k in range(18):
            a = int(k * 0.028 * SR)
            m = int(0.03 * SR)
            x[a:a + m] += _bandnoise(m, 2000, 9000, rng) * np.exp(-np.arange(m) / (0.008 * SR))
        return (x / np.abs(x).max() * 0.4).astype(np.float32)
    if name == "drone":                     # low tension drone swell (2.5 s)
        n = int(2.5 * SR)
        t = np.arange(n) / SR
        x = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) for f in (55, 55.4, 82.4, 110.3)) / 4
        x = x * np.sin(np.pi * t / 2.5) ** 1.5 + _bandnoise(n, 40, 300, rng) * 0.08
        return (x / np.abs(x).max() * 0.55).astype(np.float32)
    if name == "projector":                 # old projector running (1.6 s of sprocket clatter)
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        clat = np.zeros(n)
        for k in range(int(1.6 * 24)):
            a = int(k / 24 * SR)
            clat[a:a + 120] += np.exp(-np.arange(120) / 25.0) * rng.uniform(0.5, 1)
        x = clat * _bandnoise(n, 1500, 5000, rng) + _bandnoise(n, 60, 300, rng) * 0.08
        return (x * 0.25 * np.minimum(1, t / 0.1) * np.minimum(1, (1.6 - t) / 0.2)).astype(np.float32)
    return None


def score(duration, base, cues, fps_starts):
    """A documentary score: the music changes with the story. cues = [{"at": seconds, "style": "doc"|"tension"|
    "wonder"|"ambient"|"none", "key": ..., "bpm": ...}, ...]; each section is generated with its own settings and
    the sections crossfade over 2 s."""
    n = int(duration * SR)
    out = np.zeros(n, np.float32)
    cues = sorted(cues, key=lambda c: c["at"])
    xf = int(2.0 * SR)
    for i, c in enumerate(cues):
        a = c["at"]
        b = cues[i + 1]["at"] if i + 1 < len(cues) else duration
        if c.get("style") == "none" or b <= a:
            continue
        cfg = {**base, **{k: v for k, v in c.items() if k != "at"}, "seed": base.get("seed", 7) + i}
        seg = music(b - a + 2.5, cfg) * c.get("gain", 1.0)
        i0 = int(a * SR)
        seg = seg[: max(0, min(len(seg), n - i0))].copy()
        if i > 0:
            k = min(xf, len(seg))
            seg[:k] *= np.linspace(0, 1, k)
        end = int((b - a) * SR)
        if i + 1 < len(cues) and cues[i + 1].get("style") == "none":
            k = min(int(0.6 * SR), end)                  # into a held silence: out BEFORE the cue, so the silence is real
            seg[end - k:end] *= np.linspace(1, 0, k)
            seg[end:] = 0
        elif end < len(seg):
            k = min(xf, len(seg) - end)
            seg[end:end + k] *= np.linspace(1, 0, k)
            seg[end + k:] = 0
        out[i0:i0 + len(seg)] += seg
    return out


def duck_curve(vo, amount, smooth=0.18):
    a = np.abs(vo)
    w = int(smooth * SR)
    k = np.ones(w) / w
    e = np.convolve(a, k, mode="same")
    e = np.clip(e / (np.percentile(e[e > 1e-4], 50) if np.any(e > 1e-4) else 1), 0, 1)
    return 1 - amount * e


# Dynamic mix tiers (owner 2026-11-22): 3 = story hits (keep their punch), 2 = motion, 1 = texture / UI (vanish under the voice)
SFX_TIER3 = {"boom", "braam", "hit", "stamp", "stomp", "thud", "ding", "success", "error", "cash", "register", "splash", "door", "glitch"}
SFX_TIER1 = {"tick", "click", "pop", "type", "paper", "marker", "tape", "footsteps", "vibrate", "scratch"}
SFX_BEDS = {"drone", "hum", "crickets", "projector", "bubbles"}


def sfx_priority(name):
    return 3 if name in SFX_TIER3 else 1 if name in SFX_TIER1 else 2
