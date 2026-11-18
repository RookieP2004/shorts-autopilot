"""2026-11-19-c: "What if Jupiter became a star?" (what-if).
2D Ved + two stargazers staged on a Blender rooftop terrace at night (wide, mid, a long-lens look at Jupiter), then deep
space (Jupiter banded and sunlit; the same shot ignited as a red dwarf), then the rooftop again with a small red star in
the sky (SPECULATION). Mass hud + eqbar, squeeze arrows, size-comparison card, honesty tags, stamps are 2D.
Run after the assets exist: python jobs/2026-11-19-c/build_job.py
"""
import json, math, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-19-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("roof_wide", "roof_mid", "roof_sky", "roof_widered", "space_jup")}

JAZ, JEL, RS = 8.0, 26.0, 240.0


def sky_point(az, el, R=RS):
    a, e = math.radians(az), math.radians(el)
    return (R * math.sin(a) * math.cos(e), R * math.cos(a) * math.cos(e), R * math.sin(e))


def scr(set_, p):
    x, y = ST[set_].point(*p)
    return round(x, 3), round(y, 3)


JUP = {s: scr(s, sky_point(JAZ, JEL)) for s in ("roof_wide", "roof_mid", "roof_sky", "roof_widered")}
JC = scr("space_jup", (0, 0, 0))

OUT = {   # recurring stargazers on the roof: same outfit in every shot
    "meera": {"skin": "#b97a52", "build": "slim", "hair": ["#1a1410", "bun"], "top": ["#6fc3c0", "jacket"],
              "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "necklace": "#f2b04a"},
    "omar": {"skin": "#8d5a3b", "build": "round", "hair": ["#1a1410", "short"], "hat": ["beret", "#d9534f"],
             "top": ["#f2b04a", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "bag": "#8a5a3c"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": k.pop("enter", "none"), "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": k.pop("x", 0.5), "y": y, "size": size, "max_w": k.pop("max_w", 0.88),
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


def staged(set_, people=(), extra_top=()):
    out = [plate(set_)] + sorted(people, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def ring(color="#f2b04a"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='100' r='84' fill='none' "
            f"stroke='{color}' stroke-width='9' stroke-dasharray='18 12'/></svg>")


TAGC = {"PROVEN": "#46965a", "SPECULATION": "#d9534f"}


def tag(word, at=0.0):
    """Small honesty pill, top-left."""
    w = 150 + 40 * len(word)
    c = TAGC[word]
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 110'><rect x='5' y='5' width='{w-10}' height='100' rx='50' "
           f"fill='{c}' stroke='#1a1410' stroke-width='6'/><circle cx='55' cy='55' r='16' fill='#f6efe2'/>"
           f"<text x='{(w+60)/2}' y='77' text-anchor='middle' font-size='60' fill='#f6efe2' {AN}>{word}</text></svg>")
    return {"type": "image", "svg": svg, "x": 0.06 + w / 110 * 0.085 / 2, "y": 0.075, "w": w / 110 * 0.085,
            "enter": "pop", "at": at, "sfx": "click"}


def hud(label, y, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": k.pop("enter", "pop"), "sfx": k.pop("sfx", "click"),
            "indian": False, **k}


def arrow_in(cx, cy, r_out, r_in, at=0.0, color="#8fd3ff"):
    """Four arrows squeezing toward a point (gravity)."""
    W, H = 1080, 1920
    body = ""
    for a in (45, 135, 225, 315):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        x0, y0 = cx * W + ca * r_out * W, cy * H + sa * r_out * W
        x1, y1 = cx * W + ca * r_in * W, cy * H + sa * r_in * W
        body += (f"<line x1='{x0:.0f}' y1='{y0:.0f}' x2='{x1:.0f}' y2='{y1:.0f}' stroke='{color}' stroke-width='22' stroke-linecap='round'/>"
                 f"<polygon points='{x1 - ca*10 + sa*34:.0f},{y1 - sa*10 - ca*34:.0f} {x1 - ca*10 - sa*34:.0f},{y1 - sa*10 + ca*34:.0f} "
                 f"{x1 + ca*44:.0f},{y1 + sa*44:.0f}' fill='{color}'/>")
    return {"type": "image", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "fade", "at": at, "sfx": "whoosh",
            "svg": f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}'>{body}</svg>",
            "keys": [{"t": 0, "scale": 1.06}, {"t": 0.6, "scale": 1.0, "ease": "out"}]}


# size comparison: Jupiter vs the smallest known star (OGLE-TR-122b)
CMP = card(
    "<text x='450' y='74' text-anchor='middle' font-size='52' fill='#1a1410' " + AN + ">SAME SIZE CLUB</text>"
    "<text x='230' y='372' text-anchor='middle' font-size='42' fill='#34425c' " + F + ">JUPITER</text>"
    "<text x='230' y='430' text-anchor='middle' font-size='54' fill='#c98a5e' " + AN + ">1X MASS</text>"
    "<text x='670' y='372' text-anchor='middle' font-size='42' fill='#34425c' " + F + ">SMALLEST STAR</text>"
    "<text x='670' y='430' text-anchor='middle' font-size='54' fill='#d9534f' " + AN + ">96X MASS</text>", 900, 470)

S = []
# 0. hook (roof mid): the question at frame 0, Jupiter ringed in the sky, the mass hud ticks to 80x
jx, jy = JUP["roof_mid"]
S.append({"say": "What if Jupiter became a star? It needs to get *80 times* heavier.",
          "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.06, "focus": [0.52, 0.48]}]},
          "layers": staged("roof_mid",
                           people=[ved("roof_mid", -0.6, -1.2, [["think", 0], ["point", 1.3], ["explain", 2.6]])],
                           extra_top=[{"type": "image", "svg": ring(), "x": jx, "y": jy, "w": 0.13, "enter": "none",
                                       "loop": "pulse", "loop_amp": 0.06},
                                      txt("WHAT IF JUPITER *IGNITED?*", 0.265, 100, enter="none"),
                                      hud("jupiter's mass", 0.365, steps=[[0, 1], [2.3, 1], [3.6, 80]], prefix="x", tone="gold",
                                          enter="pop", at=0.0, width_of="x80"),
                                      tag("PROVEN", 2.3)])})
# 1. space: Jupiter, mini Jupiters rain in; it barely grows
drops = []
for k, (dx, d) in enumerate(((-0.18, 0.0), (0.12, 0.25), (-0.04, 0.5), (0.2, 0.75), (-0.22, 1.0), (0.06, 1.25))):
    drops.append(sprite("jupiter", JC[0] + dx, JC[1], 0.09, at=0.5 + d, sfx="pop" if k % 2 == 0 else None,
                        keys=[{"t": 0, "y": 0.02, "opacity": 1}, {"t": 0.55, "y": JC[1] - 0.05, "ease": "in"},
                              {"t": 0.7, "y": JC[1] - 0.05, "opacity": 0}]))
for L in drops:
    if L.get("sfx") is None:
        L.pop("sfx")
S.append({"say": "Weird part: pile on mass, and Jupiter barely *grows*.",
          "transition": "zoom", "caption_y": 0.36,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": [plate("space_jup")] + drops + [
                     hud("mass", 0.18, steps=[[0, 1], [0.8, 2], [1.4, 3], [2.0, 4]], prefix="x", tone="gold", enter="pop", at=0.1,
                         width_of="x4"),
                     {"type": "eqbar", "keys": [[0.4, "mass x2"], [1.4, "mass x4 = width *about the same*"]], "tone": "blue",
                      "x": 0.5, "y": 0.255, "at": 0.1, "enter": "fade"},
                     tag("PROVEN", 0.2)]})
# 2. Jupiter cut-out squeezed: gravity arrows, it shrinks a little; SMALLER stamp
S.append({"say": "Gravity squeezes it. Add enough, and it gets *smaller*.",
          "transition": "cut", "caption_y": 0.71,
          "bg": {"type": "radial", "colors": ["#16224a", "#03050c"]},
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "layers": [plate("space_jup", blur=14, keys=[{"t": 0, "scale": 1.3}], opacity=0.55),
                     sprite("jupiter", 0.5, 0.47, 0.6, enter="pop", keys=[{"t": 0, "scale": 1.0}, {"t": 1.0, "scale": 1.0},
                                                                         {"t": 2.4, "scale": 0.86, "ease": "in_out"}]),
                     arrow_in(0.5, 0.47, 0.42, 0.3, at=0.5),
                     txt("GRAVITY *SQUEEZES*", 0.13, 100, enter="pop", at=0.0, sfx="pop"),
                     {"type": "stamp", "text": "SMALLER", "tone": "red", "angle": -7, "size": 96, "x": 0.5, "y": 0.24,
                      "at": 2.3, "enter": "pop", "sfx": "thud"},
                     tag("PROVEN", 0.2)]})
# 3. comic beat: smirk cut-away, the glow-up arc
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("roof_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["smirk", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "jupiter's glow-up arc:\ngain weight, get *smaller*", "text_y": 0.2}})
# 4. roof wide: stargazers; the size-comparison card (smallest known star)
S.append({"say": "The smallest known star weighs *96* Jupiters, and it's only 16 percent wider.",
          "caption": "The smallest known star weighs *96* Jupiters, and it's only *16% wider*.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.05, "focus": [0.5, 0.47]}]},
          "layers": staged("roof_wide",
                           people=[person("roof_wide", "meera", -1.2, -0.4, [["point", 0], ["surprised", 2.6]]),
                                   person("roof_wide", "omar", 0.2, -1.4, [["idle", 0], ["shrug", 2.8]]),
                                   ved("roof_wide", 1.4, -2.6, [["explain", 0], ["point", 1.6]],
                                       walk=[(0, 3.6, -2.8), (1.0, 1.4, -2.6)])],
                           extra_top=[{"type": "image", "svg": CMP, "x": 0.5, "y": 0.205, "w": 0.84, "enter": "slide_down",
                                       "at": 0.2, "sfx": "whoosh"},
                                      sprite("jupiter", 0.29, 0.188, 0.2, enter="pop", at=0.6, sfx="pop"),
                                      sprite("redstar", 0.71, 0.188, 0.232, enter="pop", at=1.3, sfx="pop"),
                                      {"type": "image", "x": 0.7, "y": 0.375, "w": 0.3, "enter": "pop", "at": 2.8, "sfx": "pop",
                                       "rotate": -4,
                                       "svg": card("<text x='250' y='92' text-anchor='middle' font-size='70' fill='#d9534f' " + AN
                                                   + ">+16% WIDER</text>", 500, 140)},
                                      tag("PROVEN", 0.3)])})
# 5. space: ignition at ~80 Jupiter masses (Jupiter plate -> red-dwarf plate with a flash)
S.append({"say": "At about 80, its core gets hot enough to fuse hydrogen. *Ignition.*",
          "transition": "zoom", "caption_y": 0.41,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.56]}, {"t": 2.6, "zoom": 1.05, "focus": [0.5, 0.52]},
                              {"t": 4.5, "zoom": 1.08, "focus": [0.5, 0.52]}], "shake": [2.7, 0.4]},
          "layers": [plate("space_jup"),
                     plate("space_star", at=2.6, enter="fade", enter_dur=0.35),
                     {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "color": "#fff2d6", "at": 2.55,
                      "until": 2.85, "exit": "fade", "enter": "fade", "enter_dur": 0.1, "opacity": 0.8},
                     hud("mass", 0.175, steps=[[0, 4], [1.6, 80]], prefix="x", tone="gold", enter="none", width_of="x80"),
                     {"type": "eqbar", "keys": [[0.6, "core: hydrogen"], [1.6, "hydrogen -> helium + *light*"]], "tone": "gold",
                      "x": 0.5, "y": 0.255, "at": 0.2, "enter": "fade"},
                     {"type": "stamp", "text": "IGNITION", "tone": "gold", "angle": -6, "size": 100, "x": 0.5, "y": 0.315,
                      "at": 2.7, "enter": "pop", "sfx": "boom"},
                     tag("PROVEN", 0.2)]})
# 6. roof wide (red): SPECULATION, a small red sun in our sky; the stargazers react
rx, ry = JUP["roof_widered"]
S.append({"say": "From here, we're guessing: a tiny red *sun* in our sky. Earth would barely feel it.",
          "transition": "slide_up", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [rx, 0.42]}]},
          "layers": staged("roof_widered",
                           people=[person("roof_widered", "meera", -1.2, -0.4, [["surprised", 0], ["point", 1.0], ["cheer", 2.4]],
                                          hops=[[2.5, 0.05, 0.4]]),
                                   person("roof_widered", "omar", 0.2, -1.4, [["point", 0], ["happy", 1.8]]),
                                   ved("roof_widered", 1.4, -2.6, [["serious", 0], ["point", 0.9], ["explain", 3.0]])],
                           extra_top=[tag("SPECULATION", 0.1),
                                      {"type": "image", "svg": ring("#ff6a2a"), "x": rx, "y": ry, "w": 0.13, "enter": "pop", "at": 0.9,
                                       "sfx": "pop", "loop": "pulse", "loop_amp": 0.06},
                                      txt("A SECOND *SUN?*", 0.17, 112, enter="pop", at=1.0, sfx="pop"),
                                      {"type": "optcard", "label": "earth's extra heat", "text": "TINY", "tone": "blue",
                                       "x": 0.3, "y": 0.31, "w": 0.36, "at": 3.2, "enter": "pop", "sfx": "pop"}])})
# 7. close payoff that loops to the hook
S.append({"say": "So Jupiter isn't a failed star. It's *80 times* too light to even try.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("roof_sky", blur=8, keys=[{"t": 0, "scale": 1.3}, {"t": 3.8, "scale": 1.38}]),
                     close_ved([["warm", 0], ["point", 1.6], ["smirk", 3.0]]),
                     sprite("jupiter", 0.76, 0.27, 0.17, at=1.6, enter="pop", sfx="pop"),
                     txt("80X *TOO LIGHT*", 0.13, 120, enter="pop", at=2.0, sfx="ding")]})

job = {"id": ID, "title": "What if Jupiter became a star? Add 80 Jupiters ⭐",
       "description": "Jupiter would need about 80 times its mass to fuse hydrogen and become a (tiny, red) star. The weird part: "
                      "adding mass barely makes it bigger, because gravity squeezes it; past a point it even shrinks. The smallest "
                      "known star, OGLE-TR-122b, is 96 times Jupiter's mass but only 16% wider. What our sky would look like is "
                      "speculation, tagged as such.\n\n"
                      "Sources: BBC Science Focus (could Jupiter become a star?); ESO press release eso0507 (OGLE-TR-122b); "
                      "Ethan Siegel, Starts With A Bang (largest possible planet).",
       "tags": ["jupiter", "what if jupiter was a star", "failed star", "red dwarf", "brown dwarf", "astronomy", "space",
                "science explained", "astrophysics"],
       "hashtags": ["#space", "#astronomy"],
       "instagram": {"hashtags": ["#space", "#jupiter", "#astronomy", "#astrophysics", "#explained"]},
       "meta": {"format": "what-if", "topic": "what if Jupiter became a star: needs ~80 Jupiter masses to fuse hydrogen; adding mass barely grows it (gravity compresses; past a point it shrinks); smallest known star OGLE-TR-122b = 96 MJ, 16% wider than Jupiter; ignition; speculative tiny red second sun, Earth barely affected",
                "hook": "what-if",
                "idea_source": "viral-shaped + unique: 'Jupiter is a failed star' is a famous claim; the counter-intuitive 'heavier = smaller' angle is rare in Shorts; idea from ideas.md (what-if Jupiter were a star)",
                "characters": ["ved", "extra"],
                "sources": ["https://www.sciencefocus.com/space/could-jupiter-become-a-star",
                            "https://eso.org/public/news/eso0507/",
                            "https://www.forbes.com/sites/startswithabang/2017/04/24/whats-the-largest-planet-in-the-universe/",
                            "https://askamathematician.com/2011/06/q-how-close-is-jupiter-to-being-a-star-what-would-happen-to-us-if-it-were"],
                "humour": {"trend": "'___ arc' / 'glow-up' slang (landed before: trillion '___ arc'), bent literally: Jupiter's glow-up "
                                    "means gaining weight and getting smaller; smirk + card",
                           "beat": "smirk", "scene": 3},
                "claims": [
                    {"claim": "Jupiter would need ~80 times its mass to become a (red dwarf) star fusing hydrogen", "tag": "PROVEN",
                     "source": "https://www.sciencefocus.com/space/could-jupiter-become-a-star"},
                    {"claim": "adding mass to Jupiter would barely grow it; past a point more mass makes a planet smaller (compression)",
                     "tag": "PROVEN", "source": "https://www.forbes.com/sites/startswithabang/2017/04/24/whats-the-largest-planet-in-the-universe/"},
                    {"claim": "OGLE-TR-122b: 96 times heavier than Jupiter, only 16% larger", "tag": "PROVEN",
                     "source": "https://eso.org/public/news/eso0507/"},
                    {"claim": "a smallest-star Jupiter would add only ~0.02% to the energy Earth gets; shown as a small red second sun",
                     "tag": "SPECULATION",
                     "source": "https://askamathematician.com/2011/06/q-how-close-is-jupiter-to-being-a-star-what-would-happen-to-us-if-it-were"}]},
       "thumbnail": {"title": "JUPITER *IGNITES?*", "title_y": 0.14, "title_size": 170, "max_w": 0.95, "blur": 12,
                     "glow": "#ff7a3a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f3fb8", "#f06a24"], "tint_amount": 0.3,
                     "bg": [plate("roof_widered")],
                     "fg": [sprite("redstar", 0.74, 0.4, 0.34), sprite("jupiter", 0.24, 0.36, 0.22),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.45, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "JUP", JUP, "JC", JC)
