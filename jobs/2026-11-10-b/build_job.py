"""2026-11-10-b: "Is your blood blue inside you?" (myth-bust).
2D Ved + a lab nurse and a lab tech staged in depth inside Blender sets (blood lab, rack macro, giant cut-away skin model)
built from stills + cut-outs; vials and a horseshoe crab are animated cut-outs; light rays and panels are 2D.
Run after the assets exist: python jobs/2026-11-10-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-10-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("lab_wide", "lab_mid", "rack_close", "skin_wide", "skin_close")}

OUT = {
    "mira": {"skin": "#c98e62", "top": ["#6fc3c0", "tshirt"], "bottom": ["#6fc3c0", "trousers"], "hair": ["#2a1d17", "bun"],
             "earrings": "#f2b04a", "shoes": "#f6efe2"},
    "omar": {"skin": "#8d5a3b", "top": ["#f6efe2", "jacket"], "bottom": ["#34425c", "trousers"], "hair": ["#1a1410", "short"],
             "tie": "#7c2533", "build": "round"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def staged(set_, behind=(), front=(), extra_top=(), fg_layer=True):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if fg_layer:
        out.append(fg(set_))
    out += sorted(front, key=lambda L: -L["_depth"])
    out += list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def clean(layers):
    for L in layers:
        L.pop("_depth", None)
    return layers


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def stamp(word, color="#d9534f", w=520):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='128' text-anchor='middle' font-size='118' "
            f"fill='{color}' {AN}>{word}</text></svg>")


def full_svg(body):
    return {"type": "image", "svg": f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1080 1920'>{body}</svg>",
            "x": 0.5, "y": 0.5, "w": 1.0}


def px(p):
    return p[0] * 1080, p[1] * 1920


def beam(pts, color, width=34):
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in (px(p) for p in pts))
    x1, y1 = px(pts[-2]); x2, y2 = px(pts[-1])
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 + 40 * math.cos(a), y2 + 40 * math.sin(a)
    l = (x2 + 30 * math.cos(a + 2.4), y2 + 30 * math.sin(a + 2.4)); r = (x2 + 30 * math.cos(a - 2.4), y2 + 30 * math.sin(a - 2.4))
    return (f"<path d='{d}' fill='none' stroke='#1a1410' stroke-width='{width+12}' stroke-linecap='round' stroke-linejoin='round' opacity='0.55'/>"
            f"<path d='{d}' fill='none' stroke='{color}' stroke-width='{width}' stroke-linecap='round' stroke-linejoin='round'/>"
            f"<polygon points='{hx:.0f},{hy:.0f} {l[0]:.0f},{l[1]:.0f} {r[0]:.0f},{r[1]:.0f}' fill='{color}' stroke='#1a1410' stroke-width='6'/>")


def photon(pts, color, t0, seg=0.55, size=0.06):
    keys = [{"t": 0, "x": pts[0][0], "y": pts[0][1]}]
    for i, p in enumerate(pts[1:]):
        keys.append({"t": round(seg * (i + 1), 2), "x": p[0], "y": p[1], "ease": "linear"})
    return {"type": "shape", "shape": "circle", "x": pts[0][0], "y": pts[0][1], "w": size, "h": size, "color": color,
            "at": t0, "enter": "pop", "keys": keys, "until": t0 + seg * (len(pts) - 1) + 0.15, "exit": "fade"}


EYE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 180'><path d='M10,90 Q150,-30 290,90 Q150,210 10,90 Z' fill='#f6efe2' stroke='#1a1410' stroke-width='12'/>"
       "<circle cx='150' cy='90' r='52' fill='#4f9cff' stroke='#1a1410' stroke-width='8'/><circle cx='150' cy='90' r='24' fill='#1a1410'/>"
       "<circle cx='166' cy='74' r='10' fill='#ffffff'/></svg>")
LAMP = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 240'><circle cx='120' cy='120' r='62' fill='#f2b04a' stroke='#1a1410' stroke-width='10'/>"
        + "".join(f"<rect x='114' y='8' width='12' height='36' rx='6' fill='#f2b04a' stroke='#1a1410' stroke-width='4' transform='rotate({k*45} 120 120)'/>" for k in range(8))
        + "</svg>")


def bars(red_h, blue_h):
    """Reflected-light bar chart card: how much red vs blue light comes back from above a vein."""
    body = (f"<text x='450' y='70' text-anchor='middle' font-size='44' fill='#1a1410' {F}>LIGHT BOUNCING BACK</text>"
            f"<text x='450' y='112' text-anchor='middle' font-size='32' fill='#34425c' {F}>from skin above a vein</text>"
            f"<line x1='120' y1='520' x2='780' y2='520' stroke='#1a1410' stroke-width='8'/>"
            f"<rect x='200' y='{520-red_h}' width='190' height='{red_h}' rx='14' fill='#d9534f' stroke='#1a1410' stroke-width='6'/>"
            f"<rect x='510' y='{520-blue_h}' width='190' height='{blue_h}' rx='14' fill='#4f9cff' stroke='#1a1410' stroke-width='6'/>"
            f"<text x='295' y='580' text-anchor='middle' font-size='52' fill='#d9534f' {AN}>RED</text>"
            f"<text x='605' y='580' text-anchor='middle' font-size='52' fill='#2f6fd6' {AN}>BLUE</text>")
    return card(body, 900, 620)


DIAGRAM = card(
    "<text x='450' y='70' text-anchor='middle' font-size='42' fill='#1a1410' " + F + ">SCHOOL DIAGRAM</text>"
    "<path d='M450,330 C380,270 330,230 360,180 C390,140 440,160 450,200 C460,160 510,140 540,180 C570,230 520,270 450,330 Z' fill='#e8a39a' stroke='#1a1410' stroke-width='8'/>"
    "<path d='M360,210 C250,210 200,300 150,420' fill='none' stroke='#2f6fd6' stroke-width='22' stroke-linecap='round'/>"
    "<path d='M540,210 C650,210 700,300 750,420' fill='none' stroke='#d9534f' stroke-width='22' stroke-linecap='round'/>"
    "<text x='150' y='480' text-anchor='middle' font-size='40' fill='#2f6fd6' " + AN + ">VEINS</text>"
    "<text x='750' y='480' text-anchor='middle' font-size='40' fill='#d9534f' " + AN + ">ARTERIES</text>", 900, 520)


def label(t, color, w=620):
    return card(f"<text x='{w/2}' y='92' text-anchor='middle' font-size='62' fill='{color}' {AN}>{t}</text>", w, 140)


S = []
# 1. hook (lab mid): MYTH stamp at frame 0, Ved arms crossed in front of the bench, nurse behind
S.append({"say": "Your blood is *blue* until it hits the air? Total myth.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "mira", -2.0, 1.4, [["idle", 0], ["shrug", 1.8]])],
                           front=[ved("lab_mid", -0.4, -0.5, [["crossed", 0], ["deadpan", 2.2]])],
                           extra_top=[txt("YOUR BLOOD IS *BLUE* INSIDE YOU", 0.2, 100, enter="none"),
                                      {"type": "image", "svg": stamp("MYTH"), "x": 0.5, "y": 0.1, "w": 0.42, "rotate": -6,
                                       "enter": "none", "keys": [{"t": 0, "scale": 1.0}, {"t": 2.4, "scale": 1.0}, {"t": 2.65, "scale": 1.15, "ease": "back"}]},
                                      sprite("vial_blue", 0.8, 0.3, 0.1, at=0.0, rotate=8,
                                             keys=[{"t": 0, "opacity": 1}, {"t": 2.5, "opacity": 1}, {"t": 2.9, "opacity": 0}])])})
# 2. rack macro: always red
S.append({"say": "Your blood is *always* red.", "transition": "slide_left", "caption_y": 0.74,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.45]}, {"t": 2.2, "zoom": 1.08, "focus": [0.5, 0.42]}]},
          "layers": [plate("rack_close"), txt("ALWAYS *RED*", 0.1, 130, enter="pop", at=0.3, sfx="pop")]})
# 3. infographic: bright vs dark (two vials drop in, labels)
S.append({"say": "Full of oxygen, it's bright cherry red. Low on oxygen, in your veins, it's a darker, *maroon* red.",
          "transition": "zoom", "caption_y": 0.45,
          "layers": [plate("lab_mid", blur=14, keys=[{"t": 0, "scale": 1.2}]),
                     sprite("vial_bright", 0.3, 0.215, 0.15, at=0.2, sfx="pop", keys=[{"t": 0, "y": -0.15}, {"t": 0.6, "y": 0.215, "ease": "bounce"}]),
                     {"type": "image", "svg": label("ARTERY: BRIGHT", "#d9534f"), "x": 0.27, "y": 0.36, "w": 0.44, "enter": "pop", "at": 0.9, "sfx": "pop"},
                     sprite("vial_dark", 0.7, 0.215, 0.15, at=2.6, sfx="pop", keys=[{"t": 0, "y": -0.15}, {"t": 0.6, "y": 0.215, "ease": "bounce"}]),
                     {"type": "image", "svg": label("VEIN: MAROON", "#7c2533"), "x": 0.73, "y": 0.36, "w": 0.44, "enter": "pop", "at": 3.3, "sfx": "pop"},
                     {"type": "image", "svg": stamp("NEVER BLUE", "#2f6fd6", 840), "x": 0.5, "y": 0.58, "w": 0.66, "rotate": -5, "enter": "zoom", "at": 4.6, "sfx": "boom"},
                     {"type": "character", "id": "ved", "pose": "explain", "x": 0.5, "y": 0.78, "h": 0.36, "enter": "none",
                      "acting": [["explain", 0], ["point", 0.8], ["explain", 2.4], ["point", 3.0]], "allow_outside_safe": True}]})
# 4. lab wide: so why do veins look blue? Ved walks in, nurse holds up her wrist (point), tech shrugs
S.append({"say": "So why do your veins *look* blue? Blame the *light*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.55]}]},
          "layers": staged("lab_wide",
                           behind=[person("lab_wide", "mira", -1.8, 1.5, [["point", 0], ["shrug", 1.6]]),
                                   person("lab_wide", "omar", 0.6, 1.6, [["idle", 0], ["shrug", 1.2]])],
                           front=[ved("lab_wide", 1.2, -1.6, [["welcome", 0], ["think", 1.4], ["point", 2.4]],
                                      walk=[(0, 4.0, -1.6), (1.3, 1.2, -1.6)])],
                           extra_top=[txt("WHY DO VEINS *LOOK* BLUE?", 0.13, 104, enter="pop", at=0.2, sfx="pop"),
                                      {"type": "image", "svg": LAMP, "x": 0.5, "y": 0.27, "w": 0.16, "enter": "pop", "at": 2.0, "sfx": "pop",
                                       "loop": "pulse"}])})
# skin close geometry (vein centre on the front cut face, top-surface entry points)
sc = ST["skin_close"]
vein = sc.point(0.35, -0.82, 0.96)
red_in = sc.point(0.0, -0.82, 1.37)
blue_in = sc.point(0.62, -0.82, 1.37)
blue_dip = sc.point(0.7, -0.82, 1.27)
lamp_xy = (0.16, 0.2)
eye_xy = (0.8, 0.2)
# 5. skin wide: Ved walks up to the giant skin model
sw = ST["skin_wide"]
S.append({"say": "Here's your skin, cut open.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 2.4, "zoom": 1.08, "focus": [0.5, 0.58]}]},
          "layers": clean([plate("skin_wide"),
                           ved("skin_wide", 1.75, -1.5, [["welcome", 0], ["point", 1.2]], walk=[(0, 3.2, -1.7), (1.0, 1.75, -1.5)]),
                           txt("YOUR SKIN, *CUT OPEN*", 0.13, 104, enter="pop", at=0.3, sfx="pop")])})
# 6. skin close: red light dives deep and gets soaked up by the vein
red_path = [lamp_xy, red_in, vein]
S.append({"say": "Red light dives *deep* into your skin... and the blood in the vein soaks it up.", "transition": "cut", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.52, 0.5]}]},
          "layers": [plate("skin_close"),
                     {"type": "image", "svg": LAMP, "x": lamp_xy[0], "y": lamp_xy[1], "w": 0.18, "enter": "pop", "at": 0.0, "loop": "pulse"},
                     dict(full_svg(beam(red_path, "#ff3b3b")), enter="fade", at=0.4, enter_dur=0.5, sfx="whoosh"),
                     photon(red_path, "#ffe0e0", 0.4, 0.6),
                     {"type": "shape", "shape": "burst", "x": vein[0], "y": vein[1], "w": 0.3, "color": "#ff3b3b", "at": 2.6, "enter": "pop", "sfx": "pop",
                      "until": 3.6, "exit": "fade"},
                     txt("RED: *ABSORBED*", 0.13, 100, enter="pop", at=2.6, color="primary", highlight="#ff6b6b")]})
# 7. comic beat: reaction cut-away (smirk) with a current meme caption
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("skin_close", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["crossed", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.5, "zoom": 1.08, "focus": [0.5, 0.42],
                   "text": "red light walking into your skin like:\n*what's up brah*", "text_y": 0.18}})
# 8. skin close: blue light barely gets in, bounces back to the eye
blue_path = [lamp_xy, blue_in, blue_dip, (eye_xy[0], eye_xy[1] + 0.06)]
S.append({"say": "Blue light barely gets in. It *bounces* right back to your eyes.", "transition": "cut", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.06, "focus": [0.55, 0.45]}]},
          "layers": [plate("skin_close"),
                     dict(full_svg(beam([lamp_xy, red_in, vein], "#ff3b3b")), enter="none", opacity=0.35),
                     {"type": "image", "svg": LAMP, "x": lamp_xy[0], "y": lamp_xy[1], "w": 0.18, "enter": "none", "loop": "pulse"},
                     {"type": "image", "svg": EYE, "x": eye_xy[0], "y": eye_xy[1], "w": 0.24, "enter": "pop", "at": 0.2, "sfx": "pop"},
                     dict(full_svg(beam(blue_path, "#4f9cff")), enter="fade", at=0.5, enter_dur=0.5, sfx="whoosh"),
                     photon(blue_path, "#e0f0ff", 0.5, 0.5),
                     txt("BLUE: *BOUNCES BACK*", 0.34, 92, enter="pop", at=2.0, sfx="ding", highlight="#4f9cff")]})
# 9. infographic: more blue comes back than red -> your brain says blue
S.append({"say": "So above a vein, more blue comes back than red. And your brain goes: *blue*.", "transition": "zoom", "caption_y": 0.51,
          "layers": [plate("skin_wide", blur=14, keys=[{"t": 0, "scale": 1.2}]),
                     {"type": "image", "svg": bars(150, 380), "x": 0.5, "y": 0.22, "w": 0.8, "enter": "slide_up", "at": 0.1, "sfx": "pop"},
                     {"type": "character", "id": "ved", "pose": "point", "x": 0.5, "y": 0.8, "h": 0.34, "enter": "none",
                      "acting": [["explain", 0], ["point", 1.0], ["think", 2.8], ["smirk", 3.6]], "allow_outside_safe": True},
                     txt("BRAIN: *BLUE*", 0.43, 96, enter="pop", at=3.5, sfx="ding")]})
# 10. lab mid: textbook diagram = a colour code (tech points)
S.append({"say": "And the blue veins in your school diagrams? Just a *colour code*.", "transition": "slide_left", "caption_y": 0.45,
          "camera": {"zoom": [1.0, 1.05], "focus": [0.5, 0.52]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "omar", -2.2, 1.4, [["explain", 0], ["point", 1.0]]),
                                   person("lab_mid", "mira", 0.4, 1.6, [["idle", 0], ["happy", 2.4]])],
                           front=[ved("lab_mid", -0.4, -0.5, [["explain", 0], ["point", 1.2], ["warm", 2.8]])],
                           extra_top=[{"type": "image", "svg": DIAGRAM, "x": 0.5, "y": 0.2, "w": 0.66, "enter": "pop", "at": 0.3, "sfx": "pop", "rotate": -2},
                                      txt("JUST A *COLOUR CODE*", 0.355, 84, enter="pop", at=2.3, sfx="pop")])})
# 11. lab mid: the horseshoe crab has truly blue blood (crab drops on the bench, blue vial pops)
lm = ST["lab_mid"]
bx, by = lm.point(-1.45, 0.3, 0.93)
S.append({"say": "Want *truly* blue blood? Meet the horseshoe crab. Its blood runs on copper, not iron.", "transition": "cut", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "mira", -2.0, 1.4, [["idle", 0], ["surprised", 1.6]], hops=[[1.7, 0.04, 0.4]]),
                                   person("lab_mid", "omar", 0.5, 1.5, [["idle", 0], ["surprised", 1.7]])],
                           front=[ved("lab_mid", -0.4, -0.5, [["warm", 0], ["surprised", 1.5], ["explain", 2.6]], hops=[[1.55, 0.05, 0.4]])],
                           extra_top=[sprite("crab", bx, by - 0.05, 0.42, at=1.2, sfx="boom",
                                             keys=[{"t": 0, "y": -0.2, "rot": -20}, {"t": 0.6, "y": by - 0.05, "rot": 0, "ease": "bounce"}]),
                                      sprite("vial_blue", 0.82, 0.22, 0.12, at=2.4, enter="pop", sfx="pop", loop="float", loop_amp=0.01),
                                      txt("HORSESHOE *CRAB*", 0.1, 100, enter="pop", at=1.4),
                                      txt("COPPER, NOT *IRON*", 0.19, 84, enter="pop", at=3.6, sfx="ding")])})
# 12. close: payoff
S.append({"say": "You, though? *Red*. All the way through.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["smirk", 1.4], ["crossed", 2.2]]),
                     sprite("vial_bright", 0.84, 0.2, 0.14, at=0.8, enter="pop", sfx="pop", rotate=-8),
                     txt("RED. *ALL THE WAY.*", 0.13, 104, enter="pop", at=1.2, sfx="ding")]})

job = {"id": ID, "title": "Is your blood blue inside you? Total myth 🩸",
       "description": "Your blood is never blue: it's bright red with oxygen and dark red without. Veins only look blue because of how light travels through skin.\n\n"
                      "Sources: The Naked Scientists, 'Mythconception: Venous blood is blue'; Science ABC, 'If blood is red, why do veins appear blue?'; "
                      "Kienle et al. 1996, 'Why do veins appear blue? A new look at an old question'; Discover Wildlife on horseshoe crab blood.",
       "tags": ["blood", "blue blood", "why are veins blue", "myth busting", "human body", "biology", "science explained", "horseshoe crab"],
       "hashtags": ["#science", "#humanbody"],
       "meta": {"format": "myth-bust", "topic": "the blue-blood myth (why veins look blue)", "hook": "myth-bust",
                "idea_source": "backlog", "characters": ["ved", "extra"],
                "sources": ["https://www.thenakedscientists.com/node/195994",
                            "https://www.scienceabc.com/humans/if-blood-is-red-why-do-veins-appear-blue-through-the-skin.html",
                            "https://experts.mcmaster.ca/display/publication276400",
                            "https://www.discoverwildlife.com/animal-facts/marine-animals/horseshoe-crab-blue-blood"],
                "humour": {"trend": "'What's up brah?' (unbothered loudmouth walks into a confrontation, Nov 2026 wave)",
                           "beat": "smirk", "scene": 6}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
