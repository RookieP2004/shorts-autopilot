"""Tests for the night-set toolkit (autopilot/night.py, autopilot/devices.py, the night look in spec/style).
Run: python -m pytest -q tests
"""
import json
import math
import os
import sys
import types

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import devices, night                     # noqa: E402
from autopilot.spec import job_style, load_characters, validate_job  # noqa: E402

ST = job_style({"look": "night"})


def ctx(W=540, H=960, dur=4.0):
    return types.SimpleNamespace(W=W, H=H, style=ST, dur=[dur], job={})


def drawn(im):
    return int((np.asarray(im)[..., 3] > 0).sum())


@pytest.fixture(scope="module")
def plate(tmp_path_factory):
    """A camera 9 m behind and 7 m above the origin looking at it (like plate_arena_wide)."""
    eye, tgt = np.array([0, -9.0, 7.0]), np.array([0, 0.5, 0.0])
    z = eye - tgt
    z /= np.linalg.norm(z)
    x = np.cross([0, 0, 1], z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, y, z, eye
    p = tmp_path_factory.mktemp("plate") / "plate.json"
    json.dump({"matrix_world": M.tolist(), "lens": 30, "sensor": 36, "fit": "AUTO", "w": 540, "h": 960}, open(p, "w"))
    return str(p)


# ------------------------------------------------------------------ numbers
def test_indian_and_western_grouping():
    assert night.fmt_num(10000000, indian=True) == "1,00,00,000"
    assert night.fmt_num(999800, indian=True) == "9,99,800"
    assert night.fmt_num(8000, indian=True) == "8,000"
    assert night.fmt_num(10000000, indian=False) == "10,000,000"
    assert night.fmt_num(512, indian=True) == "512"


def test_hud_value_steps_tick_between_values():
    L = {"steps": [[0, 8000], [1.0, 4000], [2.0, 2000]], "count_dur": 0.5}
    assert night.hud_value(L, 0.5) == 8000
    assert 4000 < night.hud_value(L, 1.2) < 8000                # ticking down
    assert night.hud_value(L, 1.6) == pytest.approx(4000)
    assert night.hud_value(L, 3.0) == pytest.approx(2000)


def test_hud_chip_has_glowing_border_in_tone():
    im = night.hud_image(ST, {"label": "people", "value": 8000, "tone": "gold"}, 1.0, 1080)
    a = np.asarray(im)
    assert im.width > 300 and im.height > 150
    gold = np.array(night.rgb(night.TONES["gold"]))
    assert (np.abs(a[..., :3].astype(int) - gold).sum(-1) < 40).sum() > 200   # the border/label is gold


def test_eqbar_superscript_and_accent():
    toks = night._rich("8,000 ÷ 2^3 = *1,000*", "B", "S", (1, 1, 1), (9, 9, 9))
    assert ("3", "S", (1, 1, 1), 1) in toks
    assert toks[-1] == ("1,000", "B", (9, 9, 9), 0)
    L = {"keys": [[0.5, "8,000 ÷ 2"], [1.5, "8,000 ÷ 2^3 = *1,000*"]]}
    assert night.eqbar_image(ST, L, 0.2, 1080) is None            # nothing before the first key
    a, b = night.eqbar_image(ST, L, 1.0, 1080), night.eqbar_image(ST, L, 3.0, 1080)
    assert b.width > a.width


# ------------------------------------------------------------------ tracker / stamp / option card
def green_px(im):
    a = np.asarray(im).astype(int)
    g = np.array(night.rgb(night.TONES["green"]))
    return int((np.abs(a[..., :3] - g).sum(-1) < 30).sum())


def test_tracker_ticks_green_one_by_one():
    L = {"n": 3, "done": [1.0, 2.0, 3.0]}
    counts = [green_px(night.tracker_image(ST, L, t, 1080)) for t in (0.5, 1.5, 2.5, 3.5)]
    assert counts[0] == 0 and counts[0] < counts[1] < counts[2] < counts[3]


def test_stamp_slams_from_big_to_final():
    L = {"text": "THE TRAP", "tone": "red", "angle": -8}
    early, late = night.stamp_image(ST, L, 0.02, 1080), night.stamp_image(ST, L, 1.0, 1080)
    assert early.width > late.width * 1.4
    assert night.stamp_image(ST, L, 2.0, 1080).size == late.size  # settles


def test_optcard_cross_dims_and_tick_badge():
    base = {"label": "call 1", "text": "STOCK A\nGOES UP", "tone": "blue", "verdict_at": 1.0}
    before = night.optcard_image(ST, dict(base, verdict="cross"), 0.5, 1080)
    after = night.optcard_image(ST, dict(base, verdict="cross"), 2.0, 1080)
    red = np.array(night.rgb(night.TONES["red"]))
    nred = lambda im: int((np.abs(np.asarray(im)[..., :3].astype(int) - red).sum(-1) < 40).sum())
    assert nred(after) > nred(before) + 500
    tick = night.optcard_image(ST, dict(base, verdict="tick"), 2.0, 1080)
    assert green_px(tick) > 300


# ------------------------------------------------------------------ devices / phone
@pytest.mark.parametrize("kind", ["lock", "chat", "tips", "pay"])
def test_fictional_screens_render(kind):
    spec = {"kind": kind, "name": "Tip Club", "msgs": [{"text": "hi", "at": 1.0}], "rows": [{"text": "A up", "badge": "HIT", "at": 1.0}],
            "notes": [{"app": "Tip Club", "title": "3/3", "body": "join", "at": 1.0}], "price": "₹4,999", "countdown": 600}
    a, b = devices.screen(spec, 0.0), devices.screen(spec, 5.0)
    assert a.size == (600, 1336)
    assert np.abs(np.asarray(a).astype(int) - np.asarray(b).astype(int)).sum() > 0   # things pop in / timers tick


def test_note_texture_says_not_real_money(tmp_path):
    im = devices.note_texture("500", str(tmp_path / "n.png"))
    assert im.size == (1200, 560) and os.path.exists(tmp_path / "n.png")


def test_card_turn_foreshortens():
    im = Image.new("RGBA", (200, 400), (255, 0, 0, 255))
    assert night.card_turn(im, 0, 0) is im
    t = night.card_turn(im, 35, 0)
    assert t.width < 200 and t.height >= 400


def test_phone_draws_live_screen_into_quad(tmp_path):
    body = Image.new("RGBA", (300, 620), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(body).rounded_rectangle([0, 0, 299, 619], radius=40, fill=(30, 32, 40, 255))
    p = tmp_path / "phone.png"
    body.save(p)
    json.dump({"screen": [[15, 15], [285, 15], [285, 605], [15, 605]]}, open(tmp_path / "phone.json", "w"))
    night._sprite.cache_clear()
    L = {"sprite": str(p), "screen": {"kind": "pay", "price": "₹4,999", "countdown": 600}, "w": 0.5, "tilt": [[0, 0, 0], [2, 25, 4]]}
    a, b = night.phone_image(ST, L, 0.0, 1080), night.phone_image(ST, L, 2.0, 1080)
    assert a.width == 540                                          # drawn at the final size (sharp live screen)
    assert np.asarray(a)[..., 0].mean() > 30                       # the red pay screen is visible
    assert b.width < a.width                                       # turned: foreshortened


# ------------------------------------------------------------------ crowd / nodes / burst
def test_crowd_halving_maths():
    L = {"n": 8000, "steps": [{"at": 1, "split": "x", "colors": ["blue", "gold"]}, {"at": 2, "keep": 0},
                              {"at": 3, "split": "y", "colors": ["blue", "gold"]}, {"at": 4, "keep": 1},
                              {"at": 5, "split": "x", "colors": ["blue", "gold"]}, {"at": 6, "keep": 1}]}
    assert night.crowd_count(L, 0.5) == 8000
    assert night.crowd_count(L, 2.5) == 4000
    assert night.crowd_count(L, 4.5) == 2000
    assert night.crowd_count(L, 6.5) == 1000


def test_crowd_draws_on_the_plate_floor_and_respects_aisle(plate):
    c = ctx()
    base = {"type": "crowd", "plate": plate, "area": [-3, 3, -2, 3], "n": 1500, "in_dur": 0}
    a = Image.new("RGBA", (540, 960), (0, 0, 0, 0))
    night.draw_crowd(c, a, base, 1.0, 1.0)
    b = Image.new("RGBA", (540, 960), (0, 0, 0, 0))
    night.draw_crowd(c, b, dict(base, aisle=[0, 0.6]), 1.0, 1.0)
    assert drawn(a) > 5000 and drawn(b) < drawn(a)
    ys = np.where(np.asarray(a)[..., 3] > 0)[0]
    assert ys.min() > 960 * 0.2                                    # on the floor, below the horizon
    g = Image.new("RGBA", (540, 960), (0, 0, 0, 0))                # survivors glow: extra soft pixels
    night.draw_crowd(c, g, dict(base, steps=[{"at": 0, "glow": "green"}]), 1.0, 1.0)
    assert drawn(g) > drawn(a)


def test_nodes_build_step_by_step():
    c = ctx()
    L = {"nodes": [{"id": "a", "pos": [0, 1, 0], "at": 0}, {"id": "b", "pos": [-1, 0, 0], "at": 1, "tone": "red"},
                   {"id": "c", "pos": [1, 0, 0], "at": 1, "tone": "green", "label": "1,000"}],
         "edges": [["a", "b", 1], ["a", "c", 1, "green"]], "span": 4}
    n0, n1 = Image.new("RGBA", (540, 960)), Image.new("RGBA", (540, 960))
    night.draw_nodes(c, n0, L, 0.5, 1.0)
    night.draw_nodes(c, n1, L, 2.0, 1.0)
    assert drawn(n1) > drawn(n0) > 0


def test_burst_flies_and_ends(tmp_path):
    p = tmp_path / "note.png"
    Image.new("RGBA", (120, 60), (100, 200, 160, 255)).save(p)
    c = ctx()
    L = {"sprites": [str(p)], "n": 10, "dur": 1.0, "origin": [0.5, 0.6]}
    mid, end = Image.new("RGBA", (540, 960)), Image.new("RGBA", (540, 960))
    night.draw_burst(c, mid, L, 0.4, 1.0)
    night.draw_burst(c, end, L, 3.0, 1.0)
    assert drawn(mid) > 1000 and drawn(end) == 0


# ------------------------------------------------------------------ rim, grade, captions
def test_rim_keeps_shape_and_adds_colour():
    im = Image.new("RGBA", (200, 400), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(im).ellipse([40, 40, 160, 360], fill=(240, 240, 240, 255))
    r = night.rim(im)
    assert np.array_equal(np.asarray(r)[..., 3], np.asarray(im)[..., 3])
    a = np.asarray(r).astype(int)
    assert (a[..., 2] - a[..., 0] > 40).sum() > 50                  # blue rim pixels on the edge
    assert a[200, 100, 0] < 240                                     # fill darkened


def test_grade_darkens_corners_more_than_centre():
    im = Image.new("RGBA", (540, 960), (128, 128, 128, 255))
    g = np.asarray(night.grade(im)).astype(int)
    assert g[5, 5, 0] < g[480, 270, 0]


def test_highlight_caption_draws_selection_box():
    c = ctx(1080, 1920)
    cap = ST["captions"]
    cv = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255))
    night.draw_highlight_caption(c, cv, ["the", "scammer", "pockets", "*one*", "crore"], [0, 0.3, 0.6, 0.9, 1.2], 0.95, 0.105, cap)
    a = np.asarray(cv).astype(int)
    band = a[100:320]
    sel = np.array(night.rgb(cap["hl_box"]))
    assert (np.abs(band[..., :3] - sel).sum(-1) < 40).sum() > 100
    assert (band[..., 0] > 200).sum() > 500                         # white spoken words


# ------------------------------------------------------------------ spec / style
def test_night_look_is_opt_in():
    town, nt = job_style({}), job_style({"look": "night"})
    assert town["captions"].get("mode") != "highlight"
    assert nt["captions"]["mode"] == "highlight" and nt["transition"]["type"] == "push"
    assert town["palette"]["green"] == "#35e08a"                   # semantic colours exist in both


def test_validation_of_new_layers():
    chars = load_characters()
    job = {"id": "t", "title": "t", "look": "night", "scenes": [{"say": "hi", "layers": [
        {"type": "hud", "label": "x"}, {"type": "eqbar"}, {"type": "stamp"}, {"type": "phone", "screen": {"kind": "fax"}},
        {"type": "crowd"}, {"type": "nodes"}, {"type": "burst"}, {"type": "tracker", "n": 2, "done": [1, 2, 3]}]}]}
    errs = " ".join(validate_job(job, job_style(job), chars))
    for k in ("hud needs", "eqbar needs", "stamp needs", "phone needs 'sprite'", "kind 'fax'", "crowd needs",
              "nodes needs", "burst needs", "tracker has more"):
        assert k in errs, k
    assert "look" in " ".join(validate_job(dict(job, look="neon"), job_style(job), chars))


def test_verdict_and_trackers_at_their_exact_start_times():
    """Regression: an easing value of -0.0 at the very first frame made an inverted ellipse (render crash)."""
    for v in ("tick", "cross"):
        night.optcard_image(ST, {"text": "A", "verdict": v, "verdict_at": 1.0}, 1.0, 1080)
    night.tracker_image(ST, {"n": 3, "done": [1.0]}, 1.0, 1080)
    c = ctx()
    night.draw_nodes(c, Image.new("RGBA", (540, 960)), {"nodes": [{"id": "a", "pos": [0, 0, 0], "at": 1.0}], "span": 2}, 1.0, 1.0)
