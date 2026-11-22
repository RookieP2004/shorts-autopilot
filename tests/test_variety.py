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
