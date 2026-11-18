"""Tests for the case-file toolkit (autopilot/dossier.py) and the fictional paper textures. Run: python -m pytest -q tests"""
import os
import sys
import types

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import devices, dossier as D           # noqa: E402
from autopilot.spec import job_style, load_characters, validate_job  # noqa: E402


def drawn(im):
    return int((np.asarray(im)[..., 3] > 0).sum())


def test_dottext_decodes_then_settles():
    L = {"text": "NEW SIM: *ON*", "accent": "green", "seed": 1}
    early, late, later = (D.dottext_image(L, t) for t in (0.05, 3.0, 3.5))
    assert np.array_equal(np.asarray(late), np.asarray(later))         # settled text no longer changes
    assert not np.array_equal(np.asarray(early), np.asarray(late))      # scrambling at the start
    g = np.array(D.tone("green"))
    assert (np.abs(np.asarray(late)[..., :3].astype(int) - g).sum(-1) < 40).sum() > 50   # accent word in green


def test_dottext_types_in():
    L = {"text": "NO SERVICE", "anim": "type", "cps": 10, "glow": False}
    assert drawn(D.dottext_image(L, 0.25)) < drawn(D.dottext_image(L, 2.0))


def test_bignum_counts_with_lining_figures():
    a = D.bignum_image({"to": 16, "count_dur": 1.0, "label": "TRANSACTIONS"}, 0.1)
    b = D.bignum_image({"to": 16, "count_dur": 1.0, "label": "TRANSACTIONS"}, 2.0)
    assert a.size[1] == b.size[1] and drawn(b) > 0
    assert D._num_text({"value": 16000000, "prefix": "₹"}, 0) == "₹1,60,00,000"


def test_dateline_tiles_tipnum_clock_render():
    assert drawn(D.dateline_image({"date": "5 FEB 2026", "place": "Mumbai"}, 2.0)) > 2000
    t1 = D.tiles_image({"n": 7, "progress": [[0, 1]]}, 1.0)
    t4 = D.tiles_image({"n": 7, "progress": [[0, 1], [0.5, 4]]}, 2.0)
    gold = np.array(D.tone("gold"))
    ng = lambda im: int((np.abs(np.asarray(im)[..., :3].astype(int) - gold).sum(-1) < 40).sum())
    assert ng(t4) > ng(t1) * 2                                          # more tiles filled
    assert drawn(D.tipnum_image({"n": 1, "title": "CUT THE\nCALL", "sub": "x"}, 2.0)) > 2000
    c0 = np.asarray(D.clock_image({"time": "11:15", "from": "10:00"}, 0.0))
    c1 = np.asarray(D.clock_image({"time": "11:15", "from": "10:00"}, 3.0))
    assert not np.array_equal(c0, c1)                                   # hands sweep


def test_blinds_light_stripes_and_shade():
    ctx = types.SimpleNamespace(W=540, H=960, style={}, job={})
    cv = Image.new("RGBA", (540, 960), (60, 60, 60, 255))
    D.draw_blinds(ctx, cv, {"count": 6, "strength": 0.3, "shade": 0.3}, 1.0, 1.0)
    a = np.asarray(cv)[..., 0].astype(int)
    assert a.max() > 75 and a.min() < 50                                # light stripes + shaded gaps


def test_flows_draw_routes_only_between_known_points():
    ctx = types.SimpleNamespace(W=540, H=960, style={}, job={})
    cv = Image.new("RGBA", (540, 960), (0, 0, 0, 255))
    D.draw_flows(ctx, cv, {"points": {"A": [0.2, 0.3], "B": [0.8, 0.7]}, "routes": [["A", "B", 0]]}, 2.0, 1.0)
    assert (np.asarray(cv)[..., 0] > 100).sum() > 300


@pytest.mark.parametrize("kind", ["slips", "ledger", "statement", "form"])
def test_fictional_papers(kind, tmp_path):
    im = devices.doc_texture(kind, str(tmp_path / "d.png"), red_rows=(2,))
    assert os.path.exists(tmp_path / "d.png") and im.width == 900


def test_validation_of_case_layers():
    job = {"id": "t", "title": "t", "scenes": [{"say": "hi", "layers": [
        {"type": "dottext"}, {"type": "bignum"}, {"type": "dateline"}, {"type": "clock", "time": "noon"},
        {"type": "flows", "points": {"A": [0, 0]}, "routes": [["A", "Z", 0]]}]}]}
    errs = " ".join(validate_job(job, job_style(job), load_characters()))
    for k in ("dottext needs", "bignum needs", "dateline needs", "clock needs", "flows needs"):
        assert k in errs, k
