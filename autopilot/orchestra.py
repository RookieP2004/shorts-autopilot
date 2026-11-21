"""Real-instrument score: the same music settings as audio.music (style, key, scale, bpm, progression), played
on sampled instruments instead of synth tones. Engine: Lemo-Opuscar's sampler (MIT, vendored in third_party/lemo),
with the CC0 packs VSCO 2 CE, VCSL and FreePats only, so the channel's music needs no attribution.

Each style is a palette (which instruments play bass, chords, melody figure, sparkle and percussion) and a
written pattern. The score is written for the whole length (not a loop pasted end to end): every fourth bar
varies (a fill, a dropped beat, a sparkle), velocities breathe, and round-robins rotate, so it never machine-guns.

available() is False when the packs are missing; audio.music then falls back to the synth.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LEMO = os.path.join(os.path.dirname(HERE), "third_party", "lemo")
INST = os.path.join(LEMO, "core", "audio", "instruments")
PACKS = ("vsco2ce", "vcsl", "freepats")       # all CC0
USED = set()                                  # libraries played in this process (render writes the credits from it)
_S = None

# style -> palette. Parts: bass (root per chord), pad (held chord), fig (arpeggio figure), spark (bar-start
# bell), perc (list of (instrument, variant, pattern on 16ths, velocity)). Every instrument here is CC0.
PALETTES = {
    # the bright town (Shorts default): wooden mallets, plucked strings, a little shaker
    "ambient": dict(bass=("cellos_pizz", .55), pad=("violas", .22), fig=("marimba", .42, "up8"),
                    spark=("glockenspiel", .30), perc=[("shaker", "down", "x.x.x.x.x.x.x.x.", .16),
                                                       ("woodblock", "b", "............x...", .20)]),
    "lofi": dict(bass=("jazz_bass", .55), pad=("piano", .30, "comp"), fig=("vibraphone", .26, "sparse"),
                 spark=None, perc=[("hihat", "closed", "x.x.x.x.x.x.x.x.", .22), ("claves", None, "....x.......x...", .22),
                                   ("frame_drum", None, "x.......x.x.....", .38)]),
    "upbeat": dict(bass=("contrabass_pizz", .60), pad=None, fig=("xylophone", .40, "up16"),
                   spark=("glockenspiel", .30), perc=[("conga", None, "x..x..x.x..x..x.", .36),
                                                      ("tambourine", None, "....x.......x...", .26),
                                                      ("shaker", "down", "xxxxxxxxxxxxxxxx", .12)]),
    "suspense": dict(bass=("contrabass_pizz", .55, "pulse"), pad=("violins_trem", .20), fig=None,
                     spark=("triangle", .18), perc=[("timpani", "ROOT", "x...............", .30)]),
    "doc": dict(bass=("contrabass", .45), pad=("cellos", .34), fig=("piano", .30, "motif"),
                spark=("tubular_bells", .22), perc=[("frame_drum", None, "x.......x.......", .34)], swell=("horn", .30)),
    "tension": dict(bass=("contrabass", .45), pad=("violins_trem", .24), fig=("cellos_spic", .40, "ostinato"),
                    spark=None, perc=[("timpani", "ROOT", "x.......x.......", .40), ("toms", None, "..........x..x..", .24)],
                    riser=("gran_cassa", "roll")),
    "wonder": dict(bass=("cellos", .30), pad=("violins", .22), fig=("harp", .38, "up8"), spark=("glockenspiel", .26),
                   perc=[], swell=("horn", .24)),
    # warm, hand-played: finger-picked guitar (physically modelled), plucked bass, kalimba (stories, people, places)
    "folk": dict(bass=("jazz_bass", .50), pad=None, fig=("pluck:acoustic_guitar", .55, "up8"), spark=("kalimba", .30),
                 perc=[("frame_drum", "hand", "x.....x...x.....", .30), ("shaker", "down", "..x...x...x...x.", .14)]),
    "night": dict(bass=("electric_bass", .55), pad=("vibraphone_bowed", .26), fig=("hang", .30, "sparse"),
                  spark=None, perc=[("hihat", "closed", "x.x.x.x.x.x.x.x.", .18), ("cajon", None, "x.......x.......", .34)]),
}


def libs_of(names):
    S = sampler()
    return {S._lic(n) for n in names}


def credits():
    """Lines a video description must carry for the instruments it used (CC BY ones; CC0 needs none)."""
    S = sampler()
    return [S.LIC[l][2] for l in sorted(USED) if l in S.LIC and S.LIC[l][2]]


def available():
    return all(os.path.isdir(os.path.join(INST, p)) for p in PACKS) and os.path.isfile(os.path.join(INST, "index.json"))


def sampler():
    global _S
    if _S is None:
        if LEMO not in sys.path:
            sys.path.insert(0, LEMO)
        os.environ.setdefault("LEMO_FETCH", "0")        # never download in the middle of a render
        from core.audio import sampler as S            # noqa: E402  (vendored, MIT)
        _S = S
    return _S


def _deg(root, sc, d, octave=0):
    d0 = d - 1
    return root + sc[d0 % 7] + 12 * (d0 // 7 + octave)


def _fit(m, lo, hi):
    while m < lo:
        m += 12
    while m > hi:
        m -= 12
    return m


def write(duration, cfg, root, sc, prog, bars_per_chord, beat):
    """The score as sampler events (t, inst, pitch, dur, vel, pan)."""
    style = cfg.get("style", "ambient")
    P = PALETTES.get(style, PALETTES["ambient"])
    rng = np.random.default_rng(cfg.get("seed", 7) + 101)
    bar = 4 * beat
    s16 = beat / 4
    ev = []
    nbars = int(np.ceil(duration / bar)) + 1
    hum = lambda v: float(np.clip(v * (0.88 + 0.24 * rng.random()), 0.05, 1))   # noqa: E731
    for b in range(nbars):
        t0 = b * bar
        d = prog[(b // bars_per_chord) % len(prog)]
        first = b % bars_per_chord == 0
        chord = [_deg(root, sc, d), _deg(root, sc, d + 2), _deg(root, sc, d + 4), _deg(root, sc, d + 6)]
        phrase = (b // 4) % 2                 # A / B halves of every 8 bars
        last = b % 4 == 3                     # every fourth bar: the turnaround
        # bass
        if P.get("bass"):
            inst, v = P["bass"][:2]
            mode = P["bass"][2] if len(P["bass"]) > 2 else "root"
            m = _fit(chord[0] - 12, 31, 50)
            if mode == "pulse":
                for k in range(8):
                    ev.append((t0 + k * beat / 2, inst, m, beat / 2, hum(v * (1 if k % 2 == 0 else .7)), 0))
            elif inst in ("contrabass", "cellos"):
                if first:
                    ev.append((t0, inst, m, bar * bars_per_chord + .3, hum(v), 0))
            else:
                hits = [0, 2.5] if style in ("ambient", "lofi") else [0, 1, 2, 3]
                for h in hits:
                    if last and h > 2:
                        continue
                    ev.append((t0 + h * beat, inst, m if h != 2.5 else _fit(chord[2] - 12, 31, 52), beat * .9, hum(v), 0))
        # pad: the chord, held
        if P.get("pad") and first:
            inst, v = P["pad"][:2]
            mode = P["pad"][2] if len(P["pad"]) > 2 else "hold"
            if mode == "comp":                  # lo-fi piano: chord stabs on 1 and the and-of-2, swung
                for h in (0, 1.5, 2.66):
                    for i, m in enumerate(chord):
                        ev.append((t0 + h * beat + .012 * i, inst, _fit(m, 52, 72), beat * .8, hum(v), -.2 + .13 * i))
            else:
                for i, m in enumerate(chord[:3]):
                    ev.append((t0, inst, _fit(m, 50, 76), bar * bars_per_chord + .5, hum(v), -.3 + .3 * i))
        # figure
        if P.get("fig"):
            inst, v, mode = P["fig"]
            ns = [_fit(m, 60, 84) for m in chord]
            if mode in ("up8", "up16"):
                step = beat / 2 if mode == "up8" else s16
                order = [0, 1, 2, 3, 2, 1, 2, 3] if phrase == 0 else [0, 2, 1, 3, 2, 3, 1, 2]
                n = int(round(bar / step))
                for k in range(n):
                    if last and k >= n - 2:
                        continue                # a breath at the end of each phrase
                    acc = 1.0 if k % 4 == 0 else .72
                    ev.append((t0 + k * step, inst, ns[order[k % 8]] + (12 if k % 8 == 7 and phrase else 0),
                               step * 1.8, hum(v * acc), .25 if k % 2 else -.25))
            elif mode == "sparse":
                for k, h in enumerate((0.5, 2.0, 3.25)):
                    if rng.random() < .75:
                        ev.append((t0 + h * beat, inst, ns[(k + b) % 4] + 12 * (k == 2), beat * 1.5, hum(v), .3 - .3 * k))
            elif mode == "motif":              # a slow four-note piano idea, answered in the B half
                if first:
                    mot = [ns[0], ns[2], ns[1], ns[3]] if phrase == 0 else [ns[3], ns[1], ns[2], ns[0]]
                    for k, m in enumerate(mot):
                        ev.append((t0 + k * beat, inst, m, beat * 1.6, hum(v * (1 if k == 0 else .8)), 0))
            elif mode == "ostinato":           # driving spiccato eighths on root/fifth
                for k in range(8):
                    m = _fit(chord[0], 48, 64) + (7 if k in (3, 6) else 0) + (12 if last and k >= 6 else 0)
                    ev.append((t0 + k * beat / 2, inst, m, beat / 2, hum(v * (1 if k % 2 == 0 else .75)), 0))
        # sparkle: a bell on the first bar of each chord, every other time
        if P.get("spark") and first and (b // bars_per_chord) % 2 == 0:
            inst, v = P["spark"]
            m = _fit(chord[2], 79, 96) if inst != "tubular_bells" else _fit(chord[0], 62, 74)
            ev.append((t0 + (0 if inst == "tubular_bells" else beat * .5), inst, None if inst == "triangle" else m,
                       2.0, hum(v), .4))
        # swell: horn every 8 bars
        if P.get("swell") and b % 8 == 4:
            inst, v = P["swell"]
            ev.append((t0, inst, _fit(chord[0], 41, 57), bar * 1.6, hum(v), -.1))
        # percussion
        for inst, var, pat, v in P.get("perc", []):
            for k, ch in enumerate(pat):
                if ch != "x":
                    continue
                if last and k >= 12 and style not in ("tension",):
                    continue
                pv = _fit(chord[0], 41, 55) if var == "ROOT" else var          # timpani are tuned to the chord
                ev.append((t0 + k * s16 + (0.018 if style == "lofi" and k % 4 == 2 else 0), inst, pv, 1.2 if var == "ROOT" else None,
                           hum(v * (1 if k % 4 == 0 else .7)), .15 if k % 2 else -.15))
        # tension: a bass-drum roll swelling into every eighth bar
        if P.get("riser") and b % 8 == 7:
            inst, var = P["riser"]
            ev.append((t0, inst, var, bar, .45, 0))
    return [e for e in ev if e[0] < duration + 0.2]


def music(duration, cfg, root, sc, prog, bars_per_chord, beat, SR):
    """Mono float32 at SR, levelled to the synth's loudness so 'volume' in style.json means the same."""
    S = sampler()
    ev = write(duration, cfg, root, sc, prog, bars_per_chord, beat)
    S.seed(int(cfg.get("seed", 7)))
    pl = [e for e in ev if e[1].startswith("pluck:")]
    ev = [e for e in ev if not e[1].startswith("pluck:")]
    USED.update(libs_of({e[1] for e in ev}))
    st = S.render(ev, dur=duration + 1.5)
    if pl:                                         # physically modelled strings (Karplus-Strong; no samples, no licence)
        from core.audio import pluck as PL
        from core.audio.sfx import add as sadd
        for t, inst, p, d, v, pan in pl:
            sadd(st, PL.pluck(inst.split(":", 1)[1], p, max(0.4, d), vel=v), t, 1.0, pan)
    room = {"doc": .32, "tension": .26, "wonder": .45, "suspense": .3, "night": .22}.get(cfg.get("style"), .18)
    st = S.room(st, size=.4 + room / 2, mix=room)
    x = st.mean(axis=1).astype(np.float32)
    if S.SR != SR:
        from .audio import resample
        x = resample(x, S.SR, SR)
    # low end: keep 20-120 Hz about 3 dB under the rest (bass-heavy beds turn narration muddy and vanish on phones)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    P = np.abs(X) ** 2
    el, er = float(P[(f > 20) & (f < 120)].sum()), float(P[f >= 120].sum())
    if er > 0 and el / er > 10 ** (-3 / 10):
        g = np.sqrt(10 ** (-3 / 10) * er / el)
        w = np.clip((f - 100) / 40, 0, 1)                      # a smooth shelf, 100-140 Hz
        X *= g + (1 - g) * w
        x = np.fft.irfft(X, len(x)).astype(np.float32)
    # level: RMS of the busy part to -15.5 dBFS (where the synth bed sits, so 'volume' keeps its meaning);
    # real instruments have more crest than synth tones, so a look-ahead limiter holds the peaks under 0.9
    body = x[int(.5 * SR):]
    r = float(np.sqrt(np.mean(body ** 2))) if len(body) else 0
    if r > 1e-6:
        x *= 10 ** (-15.5 / 20) / r
    from core.audio.sfx import limit               # vendored with the sampler (MIT)
    x = limit(x, .9).astype(np.float32)
    return x[: int(duration * SR)]


# stingers: short orchestral hits the score plays ON a key picture moment (a number slam, a chapter title, a reveal)
STINGERS = {
    "slam":   [(0, "gran_cassa", "hit", None, .85, 0), (0, "timpani", "D2", 1.5, .7, 0), (0, "contrabass", "D1", 1.2, .6, 0)],
    "reveal": [(0, "tubular_bells", "D5", 3.0, .55, .2), (0, "glockenspiel", "A6", 2.0, .4, -.2), (0, "harp", "D4", 2.5, .45, 0)],
    "chapter": [(0, "timpani", "A2", 1.5, .6, 0), (0, "cellos", "D2", 1.6, .5, 0), (0.0, "sus_cymbal", "hit", None, .35, 0)],
    "turn":   [(0, "violins_trem", "A5", 1.8, .45, .2), (0, "cellos", "D2", 1.8, .45, -.2), (0, "gran_cassa", "roll", 1.4, .35, 0)],
}


def stinger(kind, key_root, SR):
    S = sampler()
    shift = key_root - 62            # stingers are written in D; move them into the score's key
    ev = []
    for t, inst, p, d, v, pan in STINGERS[kind]:
        if isinstance(p, str) and p[:1] in "ABCDEFG" and len(p) <= 3 and inst not in ("gran_cassa", "sus_cymbal"):
            p = S.midi(p) + shift
        ev.append((t, inst, p, d, v, pan))
    USED.update(libs_of({e[1] for e in ev}))
    st = S.render(ev, dur=3.5)
    x = st.mean(axis=1).astype(np.float32)
    if S.SR != SR:
        from .audio import resample
        x = resample(x, S.SR, SR)
    pk = float(np.max(np.abs(x))) or 1
    return x * (.8 / pk)
