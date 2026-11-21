"""Real-instrument score, stings and the director's checks. Run: python -m pytest -q tests"""
import os
import sys
import types

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import audio, director, orchestra, render  # noqa: E402
from autopilot.spec import STINGS  # noqa: E402

CFG = {"style": "ambient", "key": "D", "scale": "dorian", "bpm": 78, "progression": [1, 4, 6, 5],
       "bars_per_chord": 2, "seed": 21}
needs_packs = pytest.mark.skipif(not orchestra.available(), reason="sample packs not downloaded")


def test_palettes_use_cc0_or_credited_instruments():
    S = orchestra.sampler()
    for style, P in orchestra.PALETTES.items():
        names = [P[k][0] for k in ("bass", "pad", "fig", "spark", "swell") if P.get(k)] + [p[0] for p in P.get("perc", [])]
        for n in names:
            if n.startswith("pluck:"):
                continue                                                  # modelled in code, no samples
            lic = S.LIC[S._lic(n)]
            assert lic[1] == "CC0 1.0" or lic[2], (style, n)              # CC BY only with its credit line
    orchestra.USED.clear()
    orchestra.USED.update({"salamander", "vsco2ce"})
    assert len(orchestra.credits()) == 1 and "Salamander" in orchestra.credits()[0]
    orchestra.USED.clear()
    assert set(orchestra.STINGERS) | {"none"} == STINGS


def test_score_events_follow_the_key_and_length():
    ev = orchestra.write(20, CFG, 50, audio.SCALES["dorian"], [1, 4, 6, 5], 2, 60 / 78)
    assert ev and max(e[0] for e in ev) < 20.2
    pitched = [e[2] for e in ev if isinstance(e[2], (int, np.integer))]
    allowed = {(50 + d) % 12 for d in audio.SCALES["dorian"]}
    assert all(p % 12 in allowed for p in pitched)


@needs_packs
def test_real_score_is_levelled_and_not_bass_heavy(monkeypatch):
    monkeypatch.delenv("MUSIC_SOURCE", raising=False)
    x = audio.music(16, CFG)
    assert len(x) == 16 * audio.SR and np.isfinite(x).all() and np.abs(x).max() <= 0.91
    rms = 20 * np.log10(np.sqrt(np.mean(x ** 2)))
    assert -18 < rms < -13
    monkeypatch.setenv("MUSIC_SOURCE", "synth")
    y = audio.music(4, CFG)
    assert len(y) >= 4 * audio.SR - 1


def test_auto_sting_rules():
    assert render.auto_sting({"type": "motion", "comp": "NumberSlam", "props": {"roll": 1.0}})[1] == "slam"
    assert render.auto_sting({"type": "chapter"}) == (0.0, "chapter")
    assert render.auto_sting({"type": "stamp", "sting": "none"}) is None
    assert render.auto_sting({"type": "tag", "sting": "reveal", "sting_at": 0.4}) == (0.4, "reveal")
    assert render.auto_sting({"type": "tag"}) is None


def test_director_silences_camera_and_reading():
    sr = 16000
    x = np.random.default_rng(1).normal(0, .1, sr * 6).astype(np.float32)
    x[2 * sr: int(2.6 * sr)] *= 0.001
    sil = director.silences(x, sr)
    assert len(sil) == 1 and abs(sil[0][0] - 2.0) < 0.06
    kinds = director.camera_moves([
        {"camera": {"keys": [{"t": 0, "zoom": 1}, {"t": 3, "zoom": 1.1}]}},
        {"camera": {"keys": [{"t": 0, "zoom": 1.1}, {"t": 3, "zoom": 1.0}]}},
        {"camera": {"keys": [{"t": 0, "focus": [.4, .5]}, {"t": 3, "focus": [.6, .5]}]}},
        {}])
    assert kinds == ["push", "pull", "pan", "hold"]
    ctx = types.SimpleNamespace(job={"scenes": [{"layers": [
        {"type": "chapter", "text": "How dirty money gets clean", "at": 0, "dur": 1.6},
        {"type": "tag", "text": "OK", "at": 0},
        {"type": "stamp", "text": "FLASH", "at": 0, "dur": 0.3, "readable": False}]}]}, dur=[4.0])
    bad = director.text_holds(ctx, fast=False)
    assert [b["type"] for b in bad] == ["chapter"]
