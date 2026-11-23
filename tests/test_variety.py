from autopilot import variety


def test_suggest_avoids_recent_roles_and_fills_styles():
    rec = variety.recent()
    role, mode, styles, lane = variety.suggest(seed=1)
    assert role in variety.ROLES and mode in variety.EXPLAIN and lane in variety.LANES
    assert role not in {x[0] for x in rec[-10:] if x[0]}
    assert lane not in {x[3] for x in rec[-4:] if x[3]}
    assert len(styles) == 4 and len(set(styles)) == 4
    assert not (set(styles) - set(variety.STYLES.values()))


def test_report_has_meta_line():
    assert '"role":' in variety.report(seed=2)


def test_ved_wardrobe_draws_and_is_limited():
    import importlib.util, os
    spec_ = importlib.util.spec_from_file_location("vedmake", os.path.join(os.path.dirname(__file__), "..", "characters", "ved", "make.py"))
    m = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(m)
    plain = m.figure(pose="explain", expr="warm")
    worn = m.figure(pose="explain", expr="warm", wear="jacket,goggles")
    assert worn != plain and "#3d2a20" in worn and "#3d2a20" not in plain
    assert m.figure(pose="explain", expr="warm") == plain          # the shirt colours come back after a coat


def test_refphoto_licences_and_credits(tmp_path):
    from autopilot import refphoto
    assert refphoto.license_ok("Public domain") and refphoto.license_ok("CC BY 4.0") and refphoto.license_ok("CC0")
    for bad in ("CC BY-SA 4.0", "CC BY-NC 2.0", "Fair use", "All rights reserved"):
        assert not refphoto.license_ok(bad)
    assert refphoto.thumb_url("Apollo 11 Launch - GPN-2000-000630.jpg", 960).endswith("/960px-Apollo_11_Launch_-_GPN-2000-000630.jpg")
    (tmp_path / "photo_credits.json").write_text('["NASA (Public domain), via Wikimedia Commons: x"]')
    assert refphoto.credits(str(tmp_path))


def test_gate_fails_old_style_and_passes_a_mixed_short():
    import json
    from types import SimpleNamespace
    from autopilot import director
    style = json.load(open("channel/style.json"))
    good = {"meta": {"lane": "the body", "role": "scientist", "role_visual": "lab bench, goggles", "explain": "experiment",
                     "styles": ["cutaway", "hud", "RS-05"]},
            "scenes": [{"layers": [{"type": "video"}]}, {"layers": [{"type": "character"}, {"type": "hud"}]},
                       {"layers": [{"type": "look", "look": "RS-05"}]}, {"layers": [{"type": "video"}]}] * 3}
    n = len(good["scenes"])
    assert director.gate(SimpleNamespace(job=good, style=style, W=1080, H=1920, dur=[3.0] * n), log=lambda *a: None) == []
    old = {"meta": {"role": "chef"}, "scenes": [{"layers": [{"type": "text"}, {"type": "hud"}, {"type": "stamp"}]}] * 4}
    miss = director.gate(SimpleNamespace(job=old, style=style, W=1080, H=1920, dur=[8.0] * 4), log=lambda *a: None)
    assert len(miss) >= 4
