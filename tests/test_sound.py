"""Sound library, peak sync, ears and the Openverse client. Run: python -m pytest -q tests"""
import json
import os
import sys
import types

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import audio, ears, openverse  # noqa: E402
from autopilot.spec import SFX  # noqa: E402


def test_library_ranks_sources_and_varies_takes():
    takes = audio.lib_takes("whoosh")
    assert takes and all(os.path.basename(t).startswith(("ov_", "ui_", "cw_", "es_")) for t in takes)
    pre = os.path.basename(takes[0])[:3]
    assert all(os.path.basename(t)[:3] == pre for t in takes)            # only the best source is used
    a, b = audio.sfx("whoosh", 0), audio.sfx("whoosh", 1)
    assert len(a) != len(b) or not np.allclose(a[:1000], b[:1000])       # a different take per use


def test_every_library_name_is_a_valid_sfx_and_synth_fallback_works():
    lib = audio.LIB
    for name in os.listdir(lib):
        if os.path.isdir(os.path.join(lib, name)):
            assert name in SFX, name
    assert len(audio.sfx("scratch", 1)) > 100                            # not in the library: synth
    assert len(audio.sfx("whoosh", 1, source="synth")) > 100


def test_peak_time():
    x = np.zeros(audio.SR, dtype=np.float32)
    x[int(0.3 * audio.SR)] = 1.0
    assert abs(audio.peak_time(x) - 0.3) < 0.01


FAKE = json.dumps({"results": [
    {"id": "a", "title": "Coins", "url": "u1", "creator": "x", "license": "cc0", "duration": 1200, "source": "freesound",
     "foreign_landing_url": "l1"},
    {"id": "b", "title": "Long", "url": "u2", "creator": "y", "license": "cc0", "duration": 90000, "source": "freesound"},
    {"id": "c", "title": "NC", "url": "u3", "creator": "z", "license": "by-nc", "duration": 1000, "source": "freesound"}]}).encode()


def test_openverse_keeps_only_short_free_recordings():
    got = openverse.search_audio("coins", max_s=6, fetch=lambda url, timeout=25: FAKE)
    assert [g["id"] for g in got] == ["a"]
    assert openverse.credit_line({"license": "cc0"}) is None
    assert "CC BY 4.0" in openverse.credit_line({"license": "by", "license_version": "4.0", "title": "T", "creator": "C",
                                                 "source": "flickr", "foreign_landing_url": "L"})


def test_openverse_blocked_is_a_clear_error():
    def boom(url, timeout=25):
        raise openverse.OpenverseBlocked("cannot reach api.openverse.org")
    with pytest.raises(openverse.OpenverseBlocked):
        openverse.search_audio("x", fetch=boom)


def test_ears_measures_sync_and_balance(tmp_path):
    sr = audio.SR
    total = 6.0
    n = int(total * sr)
    fx = np.zeros(n, dtype=np.float32)
    cues = []
    for t in (1.0, 2.0, 4.5):
        x = audio.sfx("thud", int(t))
        pk = audio.peak_time(x)
        audio.add(fx, x, t - pk)
        cues.append((t, "thud", t - pk, pk))
    vo = [np.random.default_rng(0).standard_normal(int(2 * sr)).astype(np.float32) * 0.1]
    ctx = types.SimpleNamespace(style={"loudness_lufs": -14}, fx_stem=fx, sfx_cues=cues, total=total, vo=vo, start=[0.5],
                                lead_of=lambda i: 0.0)
    rep = ears.check(ctx, "/nonexistent.mp4", str(tmp_path), log=lambda *a: None)
    assert rep["sfx_count"] == 3 and rep["sync_median_ms"] <= 15
    assert "sfx_vs_voice_db" in rep and os.path.exists(tmp_path / "ears.json")
