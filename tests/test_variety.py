from autopilot import variety


def test_suggest_avoids_recent_roles_and_fills_styles():
    rec = variety.recent()
    role, mode, styles = variety.suggest(seed=1)
    assert role in variety.ROLES and mode in variety.EXPLAIN
    assert role not in {r for r, _, _ in rec[-10:] if r}
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
