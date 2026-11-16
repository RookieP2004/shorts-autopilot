"""2026-11-17-c: "Your body makes 2 million blood cells a SECOND" (scale-shock, number-shock).
2D Ved + Rosa the foreman staged in depth in a bright Blender bone-marrow factory ("MARROW WORKS": belt of red blood cells,
nucleus press, stem-cell dome, pipe TO BLOOD) and inside a blood vessel, built from stills + cut-outs. 2D on top: a hud that
ticks to 2,000,000, a cell burst, a BONE MARROW card, a hemoglobin hud to 270 million with oxygen bubbles flying in, the
nucleus knocked out into a bin + NO DNA stamp, cells flying at camera in the vessel with a days hud to 120, a recycle card,
a 25 trillion hud with an eqbar (25 trillion / (120 x 86,400 s) = 2.4 million / s), EVERY SECOND stamp, step tracker.
Facts: ~2 million red blood cells made per second in the bone marrow (Stanford Blood Center; ~2.4 million by the maths),
~270 million hemoglobin molecules per cell (>250 million, Stanford), mature cells expel the nucleus to make room for
hemoglobin, live ~120 days, ~84% of ~30 trillion human cells are red blood cells (Sender, Fuchs & Milo 2016 via Science
News) = ~25 trillion; old cells are removed by macrophages in the spleen and liver and the iron is recycled (MGH 2016).
Run after the assets exist: python jobs/2026-11-17-c/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-17-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("marrow_wide", "marrow_mid")}

OUT = {   # recurring people: same outfit in every shot
    "rosa": {"skin": "#b9784e", "build": "regular", "hair": ["#2a1d17", "bun"], "hat": ["cap", "#f2b04a"],
             "top": ["#3f7fbf", "shirt"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "apron": "#f08a24"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
RBC = A + "rbc.png"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


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


def staged(set_, behind=(), front=(), extra_top=(), fg=True):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if fg:
        out.append({"type": "image", "path": A + f"fg_{set_}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"})
    out += sorted(front, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 84'><rect x='4' y='4' width='292' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='172' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.24, "enter": "pop", "at": at, "sfx": "click"}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


O2 = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='100' r='92' fill='#8fd3ff' "
      "stroke='#1a1410' stroke-width='8'/><circle cx='70' cy='68' r='22' fill='#ffffff' opacity='0.7'/>"
      f"<text x='100' y='128' text-anchor='middle' font-size='84' fill='#1a1410' {AN}>O2</text></svg>")

BONE = ("<g transform='translate(40,28)'><path d='M30,22 a20,20 0 1,1 26,-6 L124,-6 a20,20 0 1,1 26,6 a20,20 0 1,1 -26,6 "
        "L56,28 a20,20 0 1,1 -26,-6 z' fill='#f3e6cf' stroke='#1a1410' stroke-width='5' transform='translate(0,40)'/></g>")


def o2(x0, y0, x1, y1, at):
    return {"type": "image", "svg": O2, "x": x0, "y": y0, "w": 0.1, "enter": "pop", "at": at, "sfx": "pop",
            "keys": [{"t": 0, "x": x0, "y": y0, "scale": 1.0, "opacity": 1}, {"t": 0.7, "x": x1, "y": y1, "scale": 0.35, "opacity": 0.0, "ease": "in"}]}


def flyer(dx, dy, at, w=0.34, dur=1.6, rot=40):
    """A red blood cell rushing out of the vessel towards the camera."""
    return {"type": "image", "path": RBC, "x": 0.5, "y": 0.43, "w": w, "enter": "fade", "enter_dur": 0.15, "at": at,
            "keys": [{"t": 0, "x": 0.5 + dx * 0.08, "y": 0.43 + dy * 0.08, "scale": 0.12, "rot": 0},
                     {"t": dur, "x": 0.5 + dx, "y": 0.43 + dy, "scale": 1.7, "rot": rot, "ease": "in"}]}


ROSA_W = (2.0, 2.2)      # Rosa behind the belt in the wide
S = []
# 0. hook (wide): the counter ticks to 2,000,000 at frame 0, a burst of cells, Ved surprised in front of the belt
S.append({"say": "In the last second, your body built over *two million* red blood cells.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": staged("marrow_wide",
                           behind=[person("marrow_wide", "rosa", *ROSA_W, [["idle", 0], ["cheer", 2.0]], hops=[[2.0, 0.05, 0.45]])],
                           front=[ved("marrow_wide", -0.8, -4.0, [["surprised", 0], ["point", 1.6], ["explain", 3.0]], hops=[[0.1, 0.05, 0.4]])],
                           extra_top=[txt("2 MILLION *A SECOND*", 0.14, 84, enter="none", max_w=0.95),
                                      hud("made in the last second", y=0.27, to=2000000, count_dur=3.2,
                                          tone="red", enter="none", width_of="2,000,000"),
                                      {"type": "burst", "sprites": [RBC], "n": 18, "origin": [0.62, 0.56], "at": 0.6, "dur": 2.0,
                                       "spread": 1.0, "sizes": [0.7], "sfx": "pop"}])})
# 1. mid on the belt: the factory is your bones -> BONE MARROW card
S.append({"say": "The factory? Inside your *bones*.",
          "transition": "slide_left", "caption_y": 0.52,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.06, "focus": [0.5, 0.55]}]},
          "layers": staged("marrow_mid",
                           front=[ved("marrow_mid", 0.5, -1.6, [["welcome", 0], ["point", 0.9]])],
                           extra_top=[{"type": "image", "svg": card(BONE + "<text x='250' y='98' font-size='68' fill='#1a1410' " + AN + ">BONE</text><text x='440' y='98' font-size='68' fill='#d9534f' " + AN + ">MARROW</text>", 820, 150),
                                       "x": 0.5, "y": 0.15, "w": 0.76, "rotate": -2, "enter": "slide_right", "at": 0.3, "sfx": "pop"},
                                      tag_layer(0.76, 0.25, 0.9),
                                      {"type": "tracker", "n": 3, "done": [0.8], "x": 0.5, "y": 0.31, "at": 0.2, "enter": "fade"}])})
# 2. close-up: one cell gets packed with hemoglobin (oxygen bubbles fly in, hud ticks to 270 million)
S.append({"say": "Each one gets packed with *270 million* hemoglobin molecules.",
          "transition": "zoom", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.08, "focus": [0.5, 0.5]}]},
          "layers": [plate("marrow_mid", blur=12, keys=[{"t": 0, "scale": 1.3}]),
                     sprite("rbc", 0.5, 0.64, 0.62, enter="pop", at=0.0, keys=[{"t": 0, "rot": -6}, {"t": 3.5, "rot": 6}]),
                     hud("hemoglobin per cell", y=0.15, to=270000000, count_dur=2.6, tone="red", enter="none", width_of="270,000,000"),
                     o2(0.12, 0.42, 0.45, 0.62, 0.4), o2(0.88, 0.38, 0.56, 0.6, 0.8), o2(0.14, 0.76, 0.45, 0.68, 1.2),
                     o2(0.86, 0.76, 0.58, 0.68, 1.6), o2(0.5, 0.3, 0.5, 0.6, 2.0),
                     {"type": "eqbar", "keys": [[0.6, "each one grabs *oxygen*"]], "tone": "blue", "x": 0.5, "y": 0.24, "enter": "fade"},
                     {"type": "tracker", "n": 3, "done": [0, 1.0], "x": 0.5, "y": 0.31, "enter": "none"}]})
# 3. mid: the press knocks the nucleus out -> it flies into the bin; NO DNA stamp
mid = ST["marrow_mid"]
PX, PY = mid.point(0.6, 0.9, 1.15)          # under the press, on the belt
BX, BY = mid.point(0.8, -0.1, 0.75)         # the bin of nuclei
S.append({"say": "Then it does something wild. It throws out its own *nucleus*. No DNA. More room for oxygen.",
          "transition": "slide_up", "caption_y": 0.52,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.0, "zoom": 1.08, "focus": [PX, 0.5]},
                              {"t": 5.5, "zoom": 1.04, "focus": [0.5, 0.5]}]},
          "layers": staged("marrow_mid",
                           front=[ved("marrow_mid", 0.5, -1.6, [["explain", 0], ["surprised", 1.9], ["point", 3.4]], hops=[[1.9, 0.05, 0.4]])],
                           extra_top=[sprite("nucleus", PX, PY, 0.11, enter="pop", at=1.5, sfx="pop",
                                             keys=[{"t": 0, "x": PX, "y": PY, "rot": 0},
                                                   {"t": 0.35, "x": (PX + BX) / 2, "y": PY - 0.12, "rot": 120, "ease": "out"},
                                                   {"t": 0.8, "x": BX, "y": BY, "rot": 260, "ease": "bounce"}]),
                                      txt("NUCLEUS: *OUT*", 0.13, 96, enter="pop", at=1.7, sfx="pop"),
                                      {"type": "stamp", "text": "NO DNA", "tone": "red", "angle": -7, "size": 110, "x": 0.4, "y": 0.6,
                                       "at": 3.0, "sfx": "thud"},
                                      {"type": "tracker", "n": 3, "done": [0, 0, 1.8], "x": 0.5, "y": 0.31, "enter": "none"},
                                      tag_layer(0.8, 0.31, 2.0)])})
# 4. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("marrow_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "storage full?\ndelete the *DNA*", "text_y": 0.2}})
# 5. vessel: cells rush at the camera, days hud ticks to 120
S.append({"say": "Then it races around your body for about *120 days*.",
          "transition": "zoom", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.45]}, {"t": 3.2, "zoom": 1.12, "focus": [0.5, 0.45]}]},
          "layers": [plate("vessel")]
                    + [flyer(dx, dy, at, w, dur, rot) for dx, dy, at, w, dur, rot in
                       ((-0.55, -0.35, 0.0, 0.3, 1.5, 50), (0.6, 0.25, 0.3, 0.34, 1.6, -40), (-0.45, 0.45, 0.7, 0.3, 1.5, 70),
                        (0.5, -0.45, 1.0, 0.32, 1.6, -60), (-0.6, 0.05, 1.4, 0.34, 1.5, 30), (0.55, 0.5, 1.8, 0.3, 1.6, -30),
                        (0.1, -0.6, 2.2, 0.3, 1.5, 45), (-0.3, 0.55, 2.6, 0.32, 1.5, -50))]
                    + [hud("days on the road", y=0.12, to=120, count_dur=2.8, tone="blue", enter="pop", at=0.2, width_of="120")]})
# 6. vessel (blurred): spleen + liver recycle it, iron kept
S.append({"say": "Then your spleen and liver *recycle* it.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("vessel", blur=8, keys=[{"t": 0, "scale": 1.15}, {"t": 2.6, "scale": 1.22}]),
                     sprite("rbc", 0.5, 0.36, 0.42, keys=[{"t": 0, "rot": 0, "scale": 1.0, "opacity": 1},
                                                          {"t": 1.6, "rot": 160, "scale": 0.3, "opacity": 0.0, "ease": "in"}]),
                     {"type": "optcard", "label": "after 120 days", "text": "SPLEEN\n+ LIVER", "tone": "gold", "x": 0.5, "y": 0.15,
                      "w": 0.52, "rotate": -2, "enter": "pop", "at": 0.2, "sfx": "pop", "verdict": "tick", "verdict_at": 1.3},
                     {"type": "image", "svg": card("<text x='250' y='98' text-anchor='middle' font-size='64' fill='#1a1410' " + AN + ">IRON</text>"
                                                   "<text x='520' y='98' text-anchor='middle' font-size='64' fill='#4f9e4a' " + AN + ">KEPT</text>", 820, 150),
                      "x": 0.5, "y": 0.36, "w": 0.7, "rotate": 2, "enter": "slide_left", "at": 1.4, "sfx": "pop"},
                     tag_layer(0.8, 0.45, 1.8)]})
# 7. wide: 25 trillion of them / 120 days -> the eqbar builds the maths; Ved walks in, Rosa explains
S.append({"say": "You carry about *25 trillion* of them. Divide by 120 days...",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": staged("marrow_wide",
                           behind=[person("marrow_wide", "rosa", *ROSA_W, [["explain", 0], ["point", 1.6]])],
                           front=[ved("marrow_wide", -0.8, -4.0, [["explain", 0], ["think", 2.2]],
                                      walk=[(0, -3.2, -4.2), (1.3, -0.8, -4.0)])],
                           extra_top=[hud("your red blood cells", y=0.13, to=25000000000000, count_dur=2.0, tone="red", enter="pop",
                                          at=0.1, width_of="25,000,000,000,000"),
                                      {"type": "eqbar", "keys": [[0.4, "25 trillion"], [2.0, "25 trillion ÷ 120 days"]],
                                       "tone": "blue", "x": 0.5, "y": 0.22, "enter": "fade", "at": 0.3}])})
# 8. close payoff: over two million every second (loops to the hook)
S.append({"say": "...that's over *two million*. Every. Single. *Second*.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("marrow_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.6, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 1.0], ["smirk", 2.6]]),
                     {"type": "eqbar", "keys": [[0.0, "25 trillion ÷ (120 x 86,400 s)"], [0.8, "= *2.4 million / s*"]],
                      "tone": "blue", "x": 0.5, "y": 0.175, "enter": "none"},
                     hud("made in the last second", y=0.085, steps=[[0, 0], [0.4, 2000000], [1.6, 0], [1.65, 2000000], [2.6, 0], [2.65, 2000000]],
                         count_dur=0.8, tone="red", enter="none", width_of="2,000,000"),
                     {"type": "stamp", "text": "EVERY SECOND", "tone": "green", "angle": -6, "size": 72, "x": 0.5, "y": 0.255,
                      "at": 2.2, "sfx": "thud"}]})

job = {"id": ID, "title": "Your body makes 2 million blood cells a SECOND 🩸",
       "description": "In the last second your bone marrow built over two million new red blood cells. Each one is packed with about "
                      "270 million hemoglobin molecules, then throws out its own nucleus (no DNA, more room for oxygen), races "
                      "around your body for about 120 days and is recycled by your spleen and liver, which keep the iron. "
                      "You carry about 25 trillion of them, so 25 trillion / 120 days = about 2.4 million new ones every second.\n\n"
                      "Sources: Stanford Blood Center; Sender, Fuchs & Milo 2016 (via Science News); Massachusetts General Hospital (2016).",
       "tags": ["red blood cells", "bone marrow", "human body", "how blood works", "hemoglobin", "biology", "science facts",
                "body facts", "scale"],
       "hashtags": ["#science", "#humanbody"],
       "instagram": {"hashtags": ["#science", "#humanbody", "#redbloodcells", "#bonemarrow", "#explained"]},
       "meta": {"format": "scale-shock", "topic": "how many red blood cells you make: ~2 million a second in the bone marrow, "
                                                  "~270 million hemoglobin each, nucleus thrown out (no DNA), ~120-day life, spleen + "
                                                  "liver recycle them, ~25 trillion in you -> 25T / 120 days = ~2.4 million/s",
                "hook": "number-shock",
                "idea_source": "viral-shaped + unique: a body number people share ('your body is a factory') made visible as a "
                               "bone-marrow factory with the maths done on screen; backlog runner-up 2026-11-15",
                "characters": ["ved", "extra"],
                "sources": ["https://stanfordbloodcenter.org/red_blood_cells-2/",
                            "https://www.sciencenews.org/article/body's-bacteria-don't-outnumber-human-cells-so-much-after-all",
                            "https://www.newworldencyclopedia.org/entry/Red_blood_cell",
                            "https://csb.mgh.harvard.edu/highlights/iron"],
                "humour": {"trend": "timeless dry aside on the 'storage full? delete X' phone format; no rising meme fit this topic",
                           "beat": "deadpan", "scene": 4},
                "claims": [
                    {"claim": "the bone marrow makes about 2 million red blood cells every second", "tag": "PROVEN",
                     "source": "https://stanfordbloodcenter.org/red_blood_cells-2/"},
                    {"claim": "each red blood cell holds about 270 million hemoglobin molecules (Stanford: over 250 million)", "tag": "PROVEN",
                     "source": "https://www.newworldencyclopedia.org/entry/Red_blood_cell"},
                    {"claim": "maturing red blood cells expel their nucleus (and DNA), making room for hemoglobin", "tag": "PROVEN",
                     "source": "https://stanfordbloodcenter.org/red_blood_cells-2/"},
                    {"claim": "they live about 120 days", "tag": "PROVEN", "source": "https://stanfordbloodcenter.org/red_blood_cells-2/"},
                    {"claim": "old red blood cells are removed in the spleen and liver and their iron is recycled", "tag": "PROVEN",
                     "source": "https://csb.mgh.harvard.edu/highlights/iron"},
                    {"claim": "~84% of ~30 trillion human cells are red blood cells (~25 trillion); 25T/(120*86,400 s) = ~2.4 million/s", "tag": "PROVEN",
                     "source": "https://www.sciencenews.org/article/body's-bacteria-don't-outnumber-human-cells-so-much-after-all"}]},
       "thumbnail": {"title": "2 MILLION *A SECOND?*", "title_y": 0.15, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#c4323f", "#f08a24"], "tint_amount": 0.28,
                     "bg": [plate("marrow_mid")],
                     "fg": [sprite("rbc", 0.5, 0.42, 0.6),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.8, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
