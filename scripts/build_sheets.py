"""Build the two reference sheets into docs/sheets/:
  1. professor_ved_character_sheet.png  - turnaround, expressions, poses, palette, proportions
  2. vast_world_style_guide.png         - lighting, shading steps, line weights, grade, depth, layout
Run after characters/ved/make.py and assets/bg/make_backgrounds.py.
"""
import copy
import io
import os
import sys

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "characters", "ved"))
import make as ved  # noqa: E402

OUT = os.path.join(ROOT, "docs", "sheets")
os.makedirs(OUT, exist_ok=True)
PAPER = (241, 233, 218)
INK = (43, 29, 22)
MUTED = (120, 100, 84)
ACCENT = (178, 112, 34)
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, "fonts", n), s)
SERIF, BOLD, SEMI = "DMSerifDisplay-Regular.ttf", "Poppins-ExtraBold.ttf", "Poppins-SemiBold.ttf"


def svg_img(svg_text=None, url=None, width=None, height=None):
    kw = dict(output_width=width) if width else dict(output_height=height)
    png = cairosvg.svg2png(bytestring=svg_text.encode() if svg_text else None, url=url, **kw)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def label(d, xy, text, size=34, font=SEMI, fill=MUTED, anchor="la"):
    d.text(xy, text, font=F(font, size), fill=fill, anchor=anchor)


def heading(d, xy, text, size=56):
    d.text(xy, text, font=F(SERIF, size), fill=INK)
    x, y = xy
    w = d.textlength(text, font=F(SERIF, size))
    d.line([(x, y + size + 14), (x + w, y + size + 14)], fill=ACCENT, width=4)


def paste(c, im, xy):
    c.alpha_composite(im, (int(xy[0]), int(xy[1])))


def card(d, box, r=26):
    d.rounded_rectangle(box, r, fill=(250, 245, 236), outline=(214, 200, 178), width=3)


# ======================================================================================
def character_sheet():
    Wc, Hc = 4000, 2600
    c = Image.new("RGBA", (Wc, Hc), PAPER + (255,))
    d = ImageDraw.Draw(c)
    d.text((120, 70), "PROFESSOR VED", font=F(SERIF, 120), fill=INK)
    label(d, (124, 210), "Character model sheet  ·  Main explainer  ·  The Vast World", 40, SEMI, ACCENT)
    label(d, (124, 268), "Mid 20s, muscular-fit. Black hair, short textured top with a skin fade. Groomed stubble beard joined to the moustache. White shirt, sleeves rolled, black trousers.",
          32, SEMI, MUTED)

    # turnaround with proportion guides
    card(d, (100, 340, 1900, 2500))
    heading(d, (150, 370), "Turnaround")
    FH = 1640
    figs = [("FRONT", svg_img(ved.figure("down", "neutral"), height=FH)),
            ("SIDE", svg_img(ved.side_view(), height=FH)),
            ("BACK", svg_img(ved.back_view(), height=FH))]
    head_px = FH * 252 / ved.H  # head (crown->chin) in sheet px
    top = 520
    for i in range(8):
        y = top + FH * 26 / ved.H + i * head_px
        if y > 2440:
            break
        d.line([(140, y), (1860, y)], fill=(214, 200, 178), width=2)
        label(d, (150, y + 6), f"{i}", 24, SEMI, (190, 172, 150))
    for i, (name, im) in enumerate(figs):
        x = 150 + i * 570
        paste(c, im, (x, top))
        label(d, (x + im.width / 2, 2450), name, 34, BOLD, INK, "ma")
    label(d, (1860, 470), "≈ 5.6 heads tall: compact & strong · broad chest and shoulders, thick arms · grounded, confident stance",
          26, SEMI, MUTED, "ra")

    # expressions
    card(d, (1980, 340, 3900, 1290))
    heading(d, (2030, 370), "Expressions")
    names = [("neutral", "Neutral"), ("warm", "Warm"), ("smile", "Smile"), ("talk", "Explaining"),
             ("think", "Sceptical / thinking"), ("surprised", "Amazed"), ("serious", "Serious"), ("laugh", "Laugh")]
    for i, (e, nm) in enumerate(names):
        im = svg_img(ved.head_only(e), width=400)
        x = 2040 + (i % 4) * 465
        y = 470 + (i // 4) * 400
        paste(c, im.resize((290, 346)), (x + 60, y))
        label(d, (x + 205, y + 352), nm, 26, SEMI, INK, "ma")

    # poses
    card(d, (1980, 1330, 3900, 2500))
    heading(d, (2030, 1360), "Acting poses  (renderer pose names)")
    poses = [("explain", "explain"), ("point", "point"), ("think", "think"), ("welcome", "welcome"), ("surprised", "surprised")]
    for i, (p, nm) in enumerate(poses):
        im = svg_img(open(os.path.join(ROOT, "characters", "ved", p + ".svg")).read(), height=900)
        x = 2010 + i * 375
        paste(c, im, (x + 175 - im.width / 2, 1470))
        label(d, (x + 180, 2390), nm, 30, BOLD, INK, "ma")
    label(d, (2030, 2440), "Each pose has _talk (mouth open) and blink frames. Sleeves always rolled below the elbow; watch on his left wrist.",
          24, SEMI, MUTED)

    # palette strip
    pal = [("Skin", ved.SKIN), ("Hair & beard", ved.HAIR), ("Sheen", ved.SHEEN), ("Watch", ved.GOLD),
           ("White shirt", ved.SHIRT), ("Black trousers", ved.TROUSER), ("Belt", ved.BELT), ("Watch strap", ved.STRAP),
           ("Shoes", ved.SHOE), ("Line", ved.LINE), ("Rim light", ved.RIM)]
    x0, y0 = 100, 2530
    for i, (nm, hx) in enumerate(pal):
        x = x0 + i * 350
        base = ved.rgb(hx)
        sh = ved.rgb(ved.shade(hx))
        d.rounded_rectangle((x, y0 - 10, x + 120, y0 + 50), 10, fill=tuple(base), outline=INK, width=2)
        d.rectangle((x + 80, y0 - 8, x + 118, y0 + 48), fill=tuple(sh))
        label(d, (x + 132, y0 - 8), nm, 24, BOLD, INK)
        label(d, (x + 132, y0 + 22), hx.upper(), 22, SEMI, MUTED)
    p = os.path.join(OUT, "professor_ved_character_sheet.png")
    c.convert("RGB").save(p, quality=92)
    return p


# ======================================================================================
def demo_shapes():
    """Sphere + cylinder in the house style, built up step by step."""
    base = "#c98d68"
    steps = []
    sphere = "M0,-90 A90,90 0 1 1 0,90 A90,90 0 1 1 0,-90 Z"
    shadow = "M0,-130 C56,-70 64,40 8,130 L140,140 L140,-140 Z"
    for k in range(5):
        s = ved.Svg()
        s.defs.append('<clipPath id="sp"><path d="' + sphere + '"/></clipPath>')
        g = [f'<path d="{sphere}" fill="{base}"/>']
        inner = []
        if k >= 1:
            inner.append(f'<path d="{shadow}" fill="{ved.shade(base)}"/>')
        if k >= 2:
            inner.append(f'<ellipse cx="-34" cy="-40" rx="26" ry="16" fill="{ved.light(base, 0.45)}" transform="rotate(-30 -34 -40)"/>')
        if k >= 3:
            inner.append('<rect x="-100" y="-100" width="200" height="200" fill="url(#f2)"/>')
        g.append(f'<g clip-path="url(#sp)">{"".join(inner)}</g>')
        if k >= 4:
            g.append(f'<path d="M64,-50 A80,80 0 0 1 50,72" fill="none" stroke="{ved.RIM}" stroke-width="5" stroke-linecap="round" opacity="0.8"/>')
        g.append(f'<path d="{sphere}" fill="none" stroke="{ved.LINE}" stroke-width="5"/>')
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-130 -130 260 260" width="260" height="260"><defs>'
               '<clipPath id="sp"><path d="' + sphere + '"/></clipPath>'
               '<linearGradient id="f2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1d6" stop-opacity="0.25"/>'
               '<stop offset="0.5" stop-color="#fff1d6" stop-opacity="0"/><stop offset="1" stop-color="#0b1030" stop-opacity="0.35"/>'
               '</linearGradient></defs>' + "".join(g) + '</svg>')
        steps.append(svg_img(svg, width=300))
    return steps


def graded_pair():
    from autopilot import render, scene as sc
    from autopilot.spec import load_characters, load_json, load_style
    job = load_json(os.path.join(ROOT, "jobs", "example", "job.json"))
    style = load_style()
    ctx = render.Ctx(job, style, load_characters())
    render.prepare(ctx, log=lambda *a: None)
    on = sc.render_frame(ctx, 1, 2.6)
    st2 = copy.deepcopy(style)
    st2["grade"]["enabled"] = False
    ctx.style = st2
    off = sc.render_frame(ctx, 1, 2.6)
    return off, on


def style_guide():
    Wc, Hc = 4000, 2700
    c = Image.new("RGBA", (Wc, Hc), PAPER + (255,))
    d = ImageDraw.Draw(c)
    d.text((120, 70), "THE VAST WORLD", font=F(SERIF, 120), fill=INK)
    label(d, (124, 210), "Look & lighting bible  ·  2D animated imitation of the real world", 40, SEMI, ACCENT)

    # 1 lighting
    card(d, (100, 300, 1300, 1260))
    heading(d, (150, 330), "1  Lighting")
    fig = svg_img(ved.figure("explain", "warm"), height=760)
    paste(c, fig, (600, 400))
    d.ellipse((170, 470, 250, 550), fill=(255, 214, 140), outline=INK, width=3)
    for k in range(5):
        d.line([(250 + k * 6, 520 + k * 22), (520 + k * 6, 600 + k * 40)], fill=(240, 180, 90), width=4)
    label(d, (150, 570), "KEY  warm amber", 26, BOLD, INK)
    label(d, (150, 606), "upper-left, ~45°", 24, SEMI, MUTED)
    label(d, (150, 650), "Shadows fall to", 24, SEMI, MUTED)
    label(d, (150, 680), "the viewer's right", 24, SEMI, MUTED)
    d.line([(1230, 520), (1010, 640)], fill=(150, 210, 240), width=5)
    label(d, (1250, 470), "RIM  cool sky-blue", 26, BOLD, INK, "ra")
    label(d, (1250, 506), "thin line on right contours", 24, SEMI, MUTED, "ra")
    label(d, (150, 1000), "No fill light:", 26, BOLD, INK)
    label(d, (150, 1036), "the cool shadow colour", 24, SEMI, MUTED)
    label(d, (150, 1066), "stands in for bounce light", 24, SEMI, MUTED)

    # 2 shading steps
    card(d, (1360, 300, 3900, 860))
    heading(d, (1410, 330), "2  Shading build-up (every surface)")
    names = ["Flat base", "+ cel shadow", "+ warm highlight", "+ light falloff", "+ cool rim & line"]
    for i, (im, nm) in enumerate(zip(demo_shapes(), names)):
        x = 1430 + i * 490
        paste(c, im, (x + 60, 450))
        label(d, (x + 210, 770), nm, 28, BOLD, INK, "ma")
    label(d, (1410, 812), "Shadow = base × 0.68, pushed 28% toward cool blue  ·  Hair & beard: softer shadow (× 0.8) + light sheen strands",
          24, SEMI, MUTED)

    # 3 line weights
    card(d, (1360, 900, 3900, 1260))
    heading(d, (1410, 930), "3  Line weight & colour")
    rows = [(4.5, "Outer silhouette / foreground", "4.5 px @1500 px figure"), (2.2, "Inner forms: lapels, tie, eyes", "2.2 px"),
            (1.3, "Fine detail: wrinkles, hair strands", "1.3 px, 40–80% opacity"), (0, "Far background", "no lines, colour only")]
    for i, (w, a, b) in enumerate(rows):
        y = 1050 + i * 52
        if w:
            d.line([(1430, y + 16), (1830, y + 16)], fill=INK, width=max(1, int(round(w * 2))))
        else:
            d.line([(1430, y + 16), (1830, y + 16)], fill=(160, 186, 196), width=10)
        label(d, (1880, y), a, 28, BOLD, INK)
        label(d, (2560, y + 2), b, 26, SEMI, MUTED)
    d.rounded_rectangle((3380, 1040, 3480, 1140), 10, fill=(43, 29, 22))
    label(d, (3500, 1050), "#2B1D16", 28, BOLD, INK)
    label(d, (3500, 1088), "warm brown, never black", 24, SEMI, MUTED)

    # 4 colour grade before / after
    card(d, (100, 1300, 1700, 2600))
    heading(d, (150, 1330), "4  Colour grade")
    off, on = graded_pair()
    for i, (im, nm) in enumerate(((off, "Ungraded"), (on, "Graded (final)"))):
        t = im.convert("RGB").resize((610, 1084))
        c.paste(t, (160 + i * 680, 1440))
        label(d, (160 + i * 680 + 305, 2536), nm, 30, BOLD, INK, "ma")
    label(d, (150, 1400), "Split-tone: shadows to teal #1D4A52, highlights to amber #FFB36B, contrast 1.06", 24, SEMI, MUTED)

    # 5 depth / worlds
    card(d, (1760, 1300, 3900, 2160))
    heading(d, (1810, 1330), "5  The Vast World: sets & depth")
    sets = [("study", "The Study (home base)"), ("world", "The Open World"), ("cosmos", "The Cosmos")]
    for i, (n, nm) in enumerate(sets):
        im = svg_img(url=os.path.join(ROOT, "assets", "bg", n + ".svg"), width=380).convert("RGB")
        c.paste(im.resize((380, 675)), (1830 + i * 470, 1430))
        label(d, (1830 + i * 470 + 190, 2112), nm, 26, BOLD, INK, "ma")
    label(d, (3290, 1440), "Foreground", 28, BOLD, INK)
    label(d, (3290, 1476), "full colour, 4.5 px line,", 24, SEMI, MUTED)
    label(d, (3290, 1506), "hard shadow", 24, SEMI, MUTED)
    label(d, (3290, 1570), "Midground", 28, BOLD, INK)
    label(d, (3290, 1606), "2 px line at 60%", 24, SEMI, MUTED)
    label(d, (3290, 1670), "Background", 28, BOLD, INK)
    label(d, (3290, 1706), "no line, lighter and bluer", 24, SEMI, MUTED)
    label(d, (3290, 1736), "with distance (aerial", 24, SEMI, MUTED)
    label(d, (3290, 1766), "perspective), mist bands", 24, SEMI, MUTED)

    # 6 type & layout
    card(d, (1760, 2200, 3900, 2600))
    heading(d, (1810, 2230), "6  Type & frame layout")
    d.text((1830, 2330), "Headlines", font=F(SERIF, 70), fill=INK)
    label(d, (1830, 2420), "DM Serif Display · cream + amber highlight", 24, SEMI, MUTED)
    d.text((2560, 2340), "CAPTIONS", font=F(BOLD, 56), fill=(242, 176, 74), stroke_width=4, stroke_fill=INK)
    label(d, (2560, 2420), "Poppins ExtraBold · word highlight", 24, SEMI, MUTED)
    label(d, (3270, 2320), "y 0.10–0.34  visuals & headline", 24, BOLD, INK)
    label(d, (3270, 2356), "y ≈ 0.45  captions", 24, BOLD, INK)
    label(d, (3270, 2392), "y 0.62–0.66  Professor Ved", 24, BOLD, INK)
    label(d, (3270, 2428), "below 0.78: YouTube UI", 24, BOLD, (190, 60, 60))
    p = os.path.join(OUT, "vast_world_style_guide.png")
    c.convert("RGB").save(p, quality=92)
    return p


def three_d_guide():
    from autopilot import three
    from autopilot.spec import load_style
    st = load_style()
    Wc, Hc = 4000, 2500
    c = Image.new("RGBA", (Wc, Hc), PAPER + (255,))
    d = ImageDraw.Draw(c)
    d.text((120, 70), "THE VAST WORLD  ·  3D", font=F(SERIF, 120), fill=INK)
    label(d, (124, 210), "Simple 3D mixed with the 2D style: faceless people, easy locations, same light", 40, SEMI, ACCENT)

    card(d, (100, 300, 2440, 1240))
    heading(d, (150, 330), "1  Faceless people  (shape: person)")
    acts = [("idle", 0, 0, "idle"), ("walk", 1.6, 0.25, "walk"), ("walk", 1.6, 0.55, "walk (other foot)"),
            ("wave", 0, 0.2, "wave"), ("point", 0, 0, "point"), ("cheer", 0, 0.1, "cheer")]
    cols = ["#7c2533", "#3c6e70", "#3c6e70", "#d9a441", "#6e4b33", "#34425c"]
    for i, ((act, walk, tt, nm), col) in enumerate(zip(acts, cols)):
        L = {"sky": ["#efe6d6", "#e2d6c0"], "fog": {"color": "#e2d6c0", "near": 30, "far": 60, "max": 0},
             "camera": {"pos": [2.2, 1.4, 4.6], "target": [0, 0.95, 0], "fov": 36},
             "objects": [{"shape": "plane", "w": 6, "d": 6, "color": "#cbbd9f"},
                         {"shape": "person", "action": "idle" if act == "walk" else act, "walk": walk,
                          "color": col, "legs": "#3a3e48", "rot": [0, 20, 0]}]}
        im = three.render(st, L, tt, 1.0, 340, 640, 2)
        c.alpha_composite(im, (150 + i * 375, 440))
        label(d, (150 + i * 375 + 170, 1100), nm, 28, BOLD, INK, "ma")
    label(d, (150, 1160), "No faces, ever: silhouette + clothing colour tell the story. Skin tones vary. Crowds: set a different phase per person.",
          24, SEMI, MUTED)

    card(d, (2500, 300, 3900, 1240))
    heading(d, (2550, 330), "2  Rules")
    rules = ["Ved is always 2D, in front. 3D sits behind him",
             "   or fills cutaways (crowds, scale, places).",
             "Same key light: upper-left, warm. Cool shadows.",
             "Low-poly flat shading, no outlines on 3D.",
             "Fog = sky colour: far things fade (aerial depth).",
             "Camera: slow. Orbit ≤ 8°/s, gentle dolly.",
             "Palette only: clothes in the channel colours.",
             "Keep it simple: ≤ 40 objects, ≤ 12 people.",
             "One 3D shot per video, at most two.",
             "The colour grade runs over 2D and 3D alike."]
    for i, r in enumerate(rules):
        label(d, (2560, 450 + i * 74), r, 30, SEMI if r.startswith("   ") else BOLD, INK if not r.startswith("   ") else MUTED)

    card(d, (100, 1290, 3900, 2420))
    heading(d, (150, 1320), "3  Easy locations")
    town = {"sky": ["#3e6f8e", "#9fc0c4", "#f3cf96"], "fog": {"color": "#e9dcc4", "near": 14, "far": 70, "max": 0.8},
            "camera": {"pos": [0, 3.0, 13], "target": [0, 1.6, 0], "fov": 46},
            "objects": [{"shape": "terrain", "w": 140, "d": 140, "n": 28, "height": 8, "seed": 4, "flat_center": 14, "color": "#6f8a45"},
                        {"shape": "plane", "w": 6, "d": 40, "color": "#b9a88f", "pos": [0, 0.02, -8]},
                        {"shape": "building", "pos": [-6, 0, -10], "h": 9, "color": "#cdb796"},
                        {"shape": "building", "pos": [6.5, 0, -14], "h": 13, "w": 5, "color": "#a9b3b8", "roof": "#34425c"},
                        {"shape": "tree", "pos": [4, 0, -3], "seed": 1}, {"shape": "tree", "pos": [-4.5, 0, -2], "seed": 2},
                        {"shape": "person", "pos": [-1.2, 0, -4], "walk": 1.6, "color": "#7c2533", "legs": "#3a3e48"},
                        {"shape": "person", "pos": [1.2, 0, 1], "rot": [0, 180, 0], "walk": 1.5, "color": "#3c6e70", "phase": 1.3}]}
    land = {"sky": ["#2f5f80", "#9fc0c4", "#f0a56c"], "fog": {"color": "#efd2a8", "near": 10, "far": 90, "max": 0.85},
            "camera": {"pos": [0, 3.2, 16], "target": [0, 4.5, -20], "fov": 50},
            "objects": [{"shape": "terrain", "w": 260, "d": 260, "n": 36, "height": 26, "seed": 9, "flat_center": 30, "color": "#5f7a3c"}]
            + [{"shape": "tree", "pos": [x, 0, z], "seed": k} for k, (x, z) in enumerate([(-6, 2), (5, -4), (-9, -10), (8, 4), (2, -14)])]
            + [{"shape": "person", "pos": [0, 0, 6], "rot": [0, 180, 0], "action": "cheer", "color": "#d9a441", "legs": "#34425c"}]}
    space = {"sky": ["#070b1e", "#141640", "#241a3e"], "fog": {"color": "#141640", "near": 30, "far": 90, "max": 0.5},
             "camera": {"pos": [0, 1.5, 14], "target": [0, 1.5, 0], "fov": 45},
             "objects": [{"shape": "sphere", "r": 3, "pos": [2.5, 2.5, -4], "color": "#e9a066"},
                         {"shape": "sphere", "r": 1.2, "pos": [-3.5, 4, -2], "color": "#8fb6c8"},
                         {"shape": "sphere", "r": 0.5, "pos": [-1.5, 0.5, 3], "color": "#d3cec7"},
                         {"shape": "cylinder", "r": 4, "h": 0.4, "r2": 3.4, "pos": [0, -2.2, 2], "color": "#6b6a78"},
                         {"shape": "person", "pos": [0, -1.8, 3], "rot": [0, 160, 0], "action": "point", "color": "#3c6e70"}]}
    for i, (L, nm) in enumerate(((town, "Town / street"), (land, "Open land"), (space, "Objects & space"))):
        im = three.render(st, L, 0.6, 2.0, 420, 746, 2)
        c.alpha_composite(im, (170 + i * 520, 1430))
        label(d, (170 + i * 520 + 210, 2190), nm, 28, BOLD, INK, "ma")
    fr = Image.open("/tmp/vout2/mixframe.png").convert("RGBA") if os.path.exists("/tmp/vout2/mixframe.png") else None
    if fr:
        c.alpha_composite(fr.resize((420, 746)), (1830, 1430))
        label(d, (2040, 2190), "Mixed: 2D Ved + 3D scene", 28, BOLD, ACCENT, "ma")
    label(d, (2350, 1440), "Build a location from parts:", 30, BOLD, INK)
    for i, t in enumerate(["terrain  - hills that fade into fog", "plane  - roads, floors, rivers", "building  - walls, roof, lit windows",
                           "tree  - three stacked cones", "sphere / box / cylinder / cone", "person  - faceless crowd member",
                           "", "Animate: spin, bob, move, walk + travel,", "camera orbit / dolly / move"]):
        label(d, (2350, 1500 + i * 52), t, 28, SEMI, MUTED)
    p = os.path.join(OUT, "vast_world_3d_guide.png")
    c.convert("RGB").save(p, quality=92)
    return p


if __name__ == "__main__":
    print(character_sheet())
    print(style_guide())
    print(three_d_guide())
