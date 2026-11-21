"""Reelsmith looks: catalogue, validation, and every look renders without a page error. Run: python -m pytest -q tests"""
import json
import os
import shutil
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import looks, publish  # noqa: E402
from autopilot.spec import SFX  # noqa: E402

needs_chrome = pytest.mark.skipif(not (shutil.which("node") and os.path.isdir(os.path.join(looks.RS, "node_modules", "playwright-core"))
                                       and os.path.exists("/usr/bin/google-chrome")), reason="node / reelsmith deps / chrome missing")


def test_catalogue_and_resolve():
    cat = looks.catalogue()
    assert len(cat) >= 10 and all(k.startswith("RS-") for k in cat)
    assert looks.resolve("RS-03") == looks.resolve("balance") == "RS-03-balance"
    with pytest.raises(KeyError):
        looks.resolve("nope")
    for d in cat:
        assert os.path.isfile(os.path.join(looks.LOOKS_DIR, d, "LOOK.md")), d


@needs_chrome
def test_every_look_renders_and_its_cues_are_real_sounds(tmp_path):
    for d in looks.catalogue():
        out = tmp_path / d
        looks.render_clip(d, {}, str(out), 216, 384, 4, 1.5, log=lambda *a: None)
        pngs = [f for f in os.listdir(out) if f.endswith(".png")]
        assert len(pngs) == 6, d
        for c in looks.cues(str(out)):
            assert c["sfx"] in SFX, (d, c)
        assert isinstance(looks.texts(str(out)), list)


def test_publish_appends_instrument_credits(tmp_path):
    job = tmp_path / "job.json"
    job.write_text(json.dumps({"title": "x", "description": "d"}))
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "render.json").write_text(json.dumps({"credits": ['Piano: "Salamander Grand Piano V3" by Alexander Holm, CC BY 3.0']}))
    f = publish.zapier_fields({"title": "x", "description": "d"}, {}, str(job))
    assert "Music: Piano" in f["description"]


def test_cutaway_cues_map_to_library_sounds(tmp_path):
    from autopilot import cutaway
    (tmp_path / "cue-sheet.json").write_text(json.dumps({"seconds": 10, "ticks": [5.5, 9.9], "events": [
        {"t": 1.0, "role": "press"}, {"t": 5.2, "role": "swoosh"}, {"t": 6.0, "role": "ratchet"}, {"t": 7.0, "role": "click"}]}))
    c = cutaway.cues_from_sheet(str(tmp_path), 5.0, 9.0)
    assert [x["sfx"] for x in c] == ["whoosh", "tick", "ratchet", "latch"] and c[0]["t"] == 0.2
    assert all(x["sfx"] in SFX for x in c)
    assert all(v in SFX for v in cutaway.ROLE.values())
