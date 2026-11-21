"""Build Professor Ved's model sheet (docs/sheets/professor_ved_model_sheet_v9.png) from the rig, the icon, the look
styles and the 3D renders in docs/sheets/ved3d/ (made with characters/ved/ved3d_model.py)."""
import io
import os
import sys

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "characters", "ved"))
sys.path.insert(0, ROOT)
import make                                    # noqa: E402
from autopilot import charstyle, night        # noqa: E402

F = os.path.join(ROOT, "fonts/PlayfairDisplaySC-Bold.ttf")
B = os.path.join(ROOT, "fonts/OldStandard-Regular.ttf")
CREAM, INK = "#efe3c8", "#1d1919"


def png(svg, w):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=w))).convert("RGBA")


def main(out=os.path.join(ROOT, "docs/sheets/professor_ved_model_sheet_v9.png")):
    W = 3000
    sheet = Image.new("RGB", (W, 5300), CREAM)
    d = ImageDraw.Draw(sheet)

    def title(t, y, sub=None):
        d.text((80, y), t, font=ImageFont.truetype(F, 64), fill=INK)
        if sub:
            d.text((80, y + 78), sub, font=ImageFont.truetype(B, 34), fill="#5a4a3a")
        d.line([(80, y + 128), (W - 80, y + 128)], fill="#b8892f", width=4)

    d.text((W // 2, 90), "PROFESSOR VED", font=ImageFont.truetype(F, 120), fill=INK, anchor="mm")
    d.text((W // 2, 180), "model sheet v9  ·  The Explainer", font=ImageFont.truetype(B, 40), fill="#5a4a3a", anchor="mm")
    title("TURNAROUND & POSES", 250, "front · side · back · explain · point · think · crossed")
    views = [png(make.figure(**make.POSES["idle"]), 300),
             png(open(os.path.join(ROOT, "characters/ved/sheet/turn_side.svg")).read(), 300),
             png(open(os.path.join(ROOT, "characters/ved/sheet/turn_back.svg")).read(), 300)]
    views += [png(make.figure(**make.POSES[p]), 300) for p in ["explain", "point", "think", "crossed"]]
    for i, v in enumerate(views):
        sheet.paste(v, (120 + i * 400, 420), v)
    title("EXPRESSIONS", 1230)
    for i, e in enumerate(["neutral", "warm", "smile", "think", "surprised", "serious", "laugh", "deadpan", "side_eye", "smirk"]):
        h = png(make.head_only(e), 260)
        x = 110 + i * 282
        sheet.paste(h, (x, 1400), h)
        d.text((x + 130, 1790), e.replace("_", " "), font=ImageFont.truetype(B, 32), fill=INK, anchor="mm")
    title("SIGNATURE & ICON", 1870, "gold pencil in the pocket + spark pin by the collar · badge, laugh badge, gold watermark")
    full = png(make.figure(**make.POSES["explain"]), 1400).crop((380, 700, 880, 1150)).resize((700, 630))
    sheet.paste(full, (100, 2030), full)
    for i, f in enumerate(["ved_icon_badge.png", "ved_icon_laugh.png", "ved_icon_mono.png"]):
        im = Image.open(os.path.join(ROOT, "assets/brand", f)).convert("RGBA").resize((560, 560))
        if i == 2:
            bg = Image.new("RGBA", (560, 560), "#3b6e8f")
            bg.alpha_composite(im)
            im = bg
        sheet.paste(im, (900 + i * 680, 2060), im)
    title("VED IN EVERY LOOK", 2730, "night · marker (whiteboard) · chalk · riso · silent film · ink brush")
    base = png(make.figure(**make.POSES["explain"]), 340)
    for i, (st, bg) in enumerate([("night", "#141c2b"), ("marker", "#f7f7f4"), ("chalk", "#2c3a33"), ("riso", "#f6f0e4"),
                                  ("film", "#3a3733"), ("ink", "#f3ecdc")]):
        cell = Image.new("RGB", (440, 880), bg)
        im = night.rim(base, ["#3fa9ff", "#9b6bff"], 1.0, 0.8) if st == "night" else charstyle.apply(base, st)
        cell.paste(im, (50, 10), im)
        sheet.paste(cell, (100 + i * 470, 2900))
    title("3D VED", 3820, "modelled in Blender: front · three-quarter · side · back · close-up")
    y = 3990
    for i, v in enumerate(["front", "three_q", "side", "back"]):
        im = Image.open(os.path.join(ROOT, f"docs/sheets/ved3d/ved3d_{v}.png")).convert("RGB")
        im = im.crop((150, 180, 570, 1000)).resize((440, 860))
        sheet.paste(im, (100 + i * 470, y))
    hd = Image.open(os.path.join(ROOT, "docs/sheets/ved3d/ved3d_head.png")).convert("RGB").crop((0, 120, 720, 1000))
    hd = hd.resize((int(720 * 860 / 880), 860))
    sheet.paste(hd, (100 + 4 * 470, y))
    sheet = sheet.crop((0, 0, W, y + 960))
    sheet.save(out)
    return out


if __name__ == "__main__":
    print(main())
