import io
import os
import sys

import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "characters", "ved"))
sys.path.insert(0, ROOT)

import make                                   # noqa: E402
from autopilot import charstyle               # noqa: E402


def _png(svg, w=240):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=w))).convert("RGBA")


def test_signature_on_by_default():
    svg = make.figure(**make.POSES["explain"])
    assert "#d4a64a" in svg and "translate(262,326)" in svg      # gold pencil + spark pin


def test_layers_split_the_figure():
    full = make.figure(**make.POSES["think"])
    parts = [make.figure(**make.POSES["think"], layer=l, shadow=False) for l in ("body", "head", "front")]
    assert all(len(p) < len(full) for p in parts)
    assert "<path" in parts[2]                                    # think has a forearm in front


def test_every_look_keeps_the_silhouette():
    im = _png(make.figure(**make.POSES["explain"]))
    a0 = (im.getchannel("A").point(lambda v: v > 128)).getbbox()
    for st in charstyle.STYLES:
        out = charstyle.apply(im, st)
        assert out.size == im.size
        bb = out.getchannel("A").point(lambda v: v > 60).getbbox()
        assert bb and abs(bb[1] - a0[1]) < 12 and abs(bb[3] - a0[3]) < 12, st


def test_mascot_renders():
    for v in ("badge", "wink"):
        im = _png(make.mascot(variant=v), 256)
        assert im.getpixel((128, 128))[3] == 255
