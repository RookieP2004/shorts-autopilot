"""2026-11-10-a: "You are 30 trillion cells" (scale-shock). 2D Ved + townspeople on a field trip inside a bright
body-interior world (Blender plates of packed cells), plus a sunny counting square. Props are Blender cut-outs.
Run after the assets exist: python jobs/2026-11-10-a/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(11)
ID = "2026-11-10-a"
J = f"jobs/{ID}/"
A = J + "assets/"
PV = "/tmp/claude-0/-home-claude-shorts-autopilot/91135f34-c0fa-5b06-b568-9a63a86208e8/scratchpad/pv/"
SRC = A if os.path.exists(A + "hourglass.png") else PV
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("tissue_wide", "tissue_mid", "square_wide")}

OUT = {   # same people, same outfits in every shot
    "kofi": {"skin": "#6b4430", "hat": ["straw", "#e6c27a"], "top": ["#f2b04a", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "mei": {"skin": "#f0c8a8", "hair": ["#1d1712", "long"], "hat": ["beret", "#d9534f"], "top": ["#6fc3c0", "shirt"],
            "bottom": ["#34425c", "trousers"]},
    "nani": {"skin": "#a86f4c", "build": "round", "hair": ["#d8d4cc", "bun"], "top": ["#7c2533", "dress"], "necklace": "#f2b04a",
             "bag": "#8a5a3c"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def card(svg, y, w=0.84, at=0.3, **k):
    return {"type": "image", "svg": svg, "w": w, "x": 0.5, "y": y, "enter": "pop", "at": at, "sfx": "pop", **k}


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


def drift(name, x, y, w, at=0.0, dx=0.04, dy=-0.03, rot=25, dur=5.0, **k):
    """A floating cell cut-out that drifts and turns slowly (props may move, characters don't loop)."""
    return sprite(name, x, y, w, at=at, enter=k.pop("enter", "fade"), keys=[{"t": 0, "x": x, "y": y, "rot": 0},
                  {"t": dur, "x": x + dx, "y": y + dy, "rot": rot, "ease": "linear"}], **k)


S = []
# 1. HOOK (wide, inside the body): the number on screen at frame 0
S.append({"say": "You are made of about *thirty trillion* cells.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "caption_y": 0.5,
          "layers": staged("tissue_wide",
                           [person("tissue_wide", "mei", -2.0, -2.6, [["idle", 0], ["surprised", 0.9]]),
                            person("tissue_wide", "kofi", 2.1, -1.8, [["point", 0], ["surprised", 1.5]]),
                            ved("tissue_wide", 0.2, -5.6, [["welcome", 0], ["explain", 1.6]])],
                           [drift("rbc", 0.2, 0.33, 0.12, enter="none", rot=40),
                            drift("rbc", 0.83, 0.3, 0.09, enter="none", dx=-0.03, rot=-30),
                            txt("YOU ARE", 0.1, 84, enter="none"),
                            {"type": "counter", "from": 29000000000000, "to": 30000000000000, "count_dur": 1.0, "x": 0.5, "y": 0.17,
                             "size": 104, "color": "accent", "stroke": "#0b0f12", "stroke_width": 7, "enter": "none"},
                            txt("*CELLS*", 0.235, 92, enter="none")])})
# 2. close-up: try counting them
S.append({"say": "Sounds made up. So let's try *counting* them.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("tissue_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.6, "scale": 1.4}]),
                     close_ved([["smirk", 0], ["explain", 1.0]]),
                     sprite("clicker", 0.78, 0.16, 0.2, enter="pop", at=1.2, sfx="click",
                            keys=[{"t": 0, "rot": -10}, {"t": 0.5, "rot": 8}]),
                     txt("LET'S *COUNT*", 0.14, 110, enter="pop", at=0.9, sfx="pop", x=0.42)]})
# 3. the counting square: one per second
sq = ST["square_wide"]
S.append({"say": "One cell per second. No sleep, no snacks, no weekends.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "caption_y": 0.22,
          "layers": staged("square_wide",
                           [person("square_wide", "kofi", 0.9, -0.2, [["hold", 0], ["shrug", 2.6]]),
                            person("square_wide", "nani", 3.0, -1.5, [["idle", 0], ["point", 1.8]]),
                            ved("square_wide", -1.1, -3.4, [["explain", 0], ["point", 1.2]], walk=[(0, -4.4, -3.4), (1.1, -1.1, -3.4)])],
                           [sprite("clicker", sq.point(1.25, -0.2, 1.05)[0], sq.point(1.25, -0.2, 1.05)[1], 0.06, enter="pop", at=0.4, sfx="click"),
                            txt("*1* CELL / SECOND", 0.12, 100, enter="pop", at=0.2, sfx="pop"),
                            ])})
# 4. the timeline card: 950,000 years
tl = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 560'><rect width='900' height='560' rx='34' fill='#f6efe2'/>"
      "<rect width='900' height='560' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
      f"<text x='450' y='86' text-anchor='middle' font-size='48' fill='#1a1410' {F}>COUNTING 30 TRILLION</text>"
      "<rect x='80' y='250' width='740' height='22' rx='11' fill='#34425c'/>"
      "<rect x='80' y='250' width='506' height='22' rx='11' fill='#f2b04a'/>"
      "<circle cx='92' cy='261' r='26' fill='#d9534f'/><circle cx='586' cy='261' r='22' fill='#6fc3c0'/><circle cx='808' cy='261' r='26' fill='#46965a'/>"
      f"<text x='92' y='200' text-anchor='middle' font-size='34' fill='#d9534f' {F}>START</text>"
      f"<text x='92' y='340' text-anchor='middle' font-size='30' fill='#1a1410' {F}>950,000</text>"
      f"<text x='92' y='378' text-anchor='middle' font-size='26' fill='#5a4636' {F}>YEARS AGO</text>"
      f"<text x='586' y='200' text-anchor='middle' font-size='30' fill='#2f8f8a' {F}>FIRST HUMANS</text>"
      f"<text x='586' y='340' text-anchor='middle' font-size='30' fill='#1a1410' {F}>~300,000</text>"
      f"<text x='586' y='378' text-anchor='middle' font-size='26' fill='#5a4636' {F}>YEARS AGO</text>"
      f"<text x='808' y='200' text-anchor='middle' font-size='34' fill='#46965a' {F}>DONE</text>"
      f"<text x='808' y='340' text-anchor='middle' font-size='30' fill='#1a1410' {F}>TODAY</text>"
      f"<text x='450' y='500' text-anchor='middle' font-size='42' fill='#d98a1a' {AN}>1 PER SECOND = ~950,000 YEARS</text></svg>")
S.append({"say": "You'd finish in about *nine hundred and fifty thousand* years.", "transition": "slide_up", "caption_y": 0.64,
          "layers": [plate("square_wide", blur=7, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.21}]),
                     card(tl, 0.27, w=0.88, at=0.15),
                     sprite("hourglass", 0.8, 0.5, 0.16, enter="drop", at=1.4, sfx="pop",
                            keys=[{"t": 0, "rot": 0}, {"t": 0.6, "rot": 0}, {"t": 1.1, "rot": 180}])]})
# 5. close: before humans existed
S.append({"say": "You'd have to start before *humans* even existed.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("square_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.6, "scale": 1.4}]),
                     close_ved([["surprised", 0], ["point", 1.3]]),
                     txt("BEFORE *HUMANS*", 0.13, 110, enter="pop", at=0.5, sfx="pop")]})
# 6. medium, inside: 25 trillion are red blood cells
tm = ST["tissue_mid"]
bar = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 250'><rect width='900' height='250' rx='30' fill='#f6efe2'/>"
       "<rect width='900' height='250' rx='30' fill='none' stroke='#1a1410' stroke-width='6'/>"
       f"<text x='60' y='72' font-size='40' fill='#1a1410' {F}>YOUR 30 TRILLION CELLS</text>"
       "<rect x='60' y='110' width='780' height='70' rx='14' fill='#34425c'/>"
       "<rect x='60' y='110' width='655' height='70' rx='14' fill='#c8141f'/>"
       f"<text x='387' y='160' text-anchor='middle' font-size='44' fill='#f6efe2' {AN}>RED BLOOD CELLS 84%</text>"
       f"<text x='778' y='160' text-anchor='middle' font-size='28' fill='#f6efe2' {F}>REST</text>"
       f"<text x='450' y='226' text-anchor='middle' font-size='28' fill='#5a4636' {F}>skin, brain, muscle, bone... all in that last slice</text></svg>")
S.append({"say": "And most of them aren't skin or brain. About *twenty-five trillion* are red blood cells.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "caption_y": 0.46,
          "layers": staged("tissue_mid",
                           [ved("tissue_mid", 0.25, -1.2, [["explain", 0], ["point", 2.4], ["warm", 4.4]]),
                            person("tissue_mid", "mei", -1.25, 0.8, [["idle", 0], ["surprised", 2.6]], hops=[[2.7, 0.03, 0.45]])],
                           [sprite("rbc", 0.4, 0.6, 0.15, at=2.2, enter="pop", sfx="pop",
                                   keys=[{"t": 0, "y": 0.66, "rot": -20}, {"t": 0.5, "y": 0.6, "rot": 0, "ease": "back"}]),
                            sprite("rbc", 0.28, 0.69, 0.11, at=2.45, enter="pop",
                                   keys=[{"t": 0, "y": 0.76, "rot": 30}, {"t": 0.5, "y": 0.7, "rot": 10, "ease": "back"}]),
                            sprite("rbc", 0.48, 0.72, 0.1, at=2.7, enter="pop",
                                   keys=[{"t": 0, "y": 0.79, "rot": -40}, {"t": 0.5, "y": 0.73, "rot": -15, "ease": "back"}]),
                            card(bar, 0.31, w=0.86, at=2.3),
                            {"type": "counter", "from": 0, "to": 25000000000000, "count_dur": 1.3, "at": 2.0, "x": 0.5, "y": 0.14,
                             "size": 96, "color": "#ff5a5a", "stroke": "#0b0f12", "stroke_width": 7, "enter": "pop"},
                            txt("RED BLOOD CELLS", 0.205, 70, enter="pop", at=2.2)])})
# 7. looking up: 38 trillion bacteria
vs = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 420'><rect width='900' height='420' rx='34' fill='#f6efe2'/>"
      "<rect width='900' height='420' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
      f"<text x='450' y='70' text-anchor='middle' font-size='42' fill='#1a1410' {F}>WHO LIVES IN YOU</text>"
      "<rect x='120' y='190' width='260' height='140' rx='12' fill='#d9534f'/>"
      "<rect x='520' y='150' width='260' height='180' rx='12' fill='#7cc35a'/>"
      f"<text x='250' y='175' text-anchor='middle' font-size='52' fill='#1a1410' {AN}>30 T</text>"
      f"<text x='650' y='135' text-anchor='middle' font-size='52' fill='#1a1410' {AN}>38 T</text>"
      f"<text x='250' y='380' text-anchor='middle' font-size='34' fill='#1a1410' {F}>YOUR CELLS</text>"
      f"<text x='650' y='380' text-anchor='middle' font-size='34' fill='#1a1410' {F}>BACTERIA</text>"
      f"<text x='450' y='272' text-anchor='middle' font-size='44' fill='#d98a1a' {AN}>~1:1</text></svg>")
S.append({"say": "Then there are the guests. Roughly *thirty-eight trillion* bacteria, mostly in your gut.", "transition": "slide_up",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.08, "focus": [0.5, 0.48]}]},
          "caption_y": 0.7,
          "layers": [plate("tissue_up"),
                     drift("bacterium", 0.25, 0.55, 0.22, at=0.3, rot=15, dx=0.05, sfx="pop"),
                     drift("bacterium", 0.72, 0.62, 0.18, at=0.7, rot=-20, dx=-0.04, flip=True),
                     drift("bacterium", 0.55, 0.5, 0.14, at=1.0, rot=30, dy=0.03),
                     card(vs, 0.24, w=0.82, at=1.6),
                     txt("GUESTS", 0.08, 80, enter="pop", at=0.2, sfx="pop", color="#9fe07a")]})
# 8. wide, inside: none of it stays
S.append({"say": "And none of it stays. Your body replaces about *three hundred and thirty billion* cells a day.", "transition": "cut",
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "caption_y": 0.5,
          "layers": staged("tissue_wide",
                           [person("tissue_wide", "mei", -2.0, -2.6, [["idle", 0], ["shrug", 3.0]]),
                            person("tissue_wide", "kofi", 2.1, -1.8, [["idle", 0], ["surprised", 3.2]], hops=[[3.3, 0.03, 0.45]]),
                            ved("tissue_wide", 0.2, -5.6, [["serious", 0], ["explain", 1.8], ["point", 3.4]])]
                           ,
                           [drift("cell", 0.18, 0.34, 0.12, at=0.4, rot=0, dy=-0.02, until=1.8, exit="fade"),
                            drift("cell", 0.82, 0.32, 0.11, at=1.2, rot=0, dy=-0.02, until=2.6, exit="fade"),
                            sprite("cell", 0.18, 0.34, 0.12, at=2.0, enter="pop", sfx="pop"),
                            sprite("cell", 0.82, 0.32, 0.11, at=2.8, enter="pop", sfx="pop"),
                            txt("REPLACED EVERY DAY", 0.11, 76, enter="pop", at=0.6),
                            {"type": "counter", "from": 0, "to": 330000000000, "count_dur": 1.4, "at": 2.6, "x": 0.5, "y": 0.18,
                             "size": 110, "color": "accent", "stroke": "#0b0f12", "stroke_width": 7, "enter": "pop"}])})
# 9. per second
S.append({"say": "That's nearly *four million* every second.", "transition": "zoom", "sfx": "boom",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.1, "focus": [0.5, 0.5]}], "punch": [0.9]},
          "caption_y": 0.64,
          "layers": [plate("tissue_mid", blur=6, keys=[{"t": 0, "scale": 1.15}, {"t": 3, "scale": 1.2}]),
                     {"type": "counter", "from": 0, "to": 3800000, "count_dur": 1.0, "at": 0.3, "x": 0.5, "y": 0.2,
                      "size": 150, "color": "accent", "stroke": "#0b0f12", "stroke_width": 8, "enter": "pop"},
                     txt("EVERY *SECOND*", 0.29, 90, enter="pop", at=1.0, sfx="pop")]
                    + [sprite("cell", random.uniform(0.15, 0.85), random.uniform(0.48, 0.58), random.uniform(0.07, 0.11),
                              enter="pop", at=0.4 + i * 0.18, loop="pulse", loop_amp=0.6) for i in range(9)]})
# 10. comic beat (reaction cut-away): "Remember November 2026" (the polar-bear meme, revived late Aug 2026, peaking this month)
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("tissue_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.6, "text": "Remember November 2026? *Most of your cells won't.*",
                   "text_y": 0.18}})
# 11. close payoff
S.append({"say": "So while you watched this, over a *hundred million* of you got swapped out. Same you. *New parts.*",
          "transition": "cut", "caption_y": 0.64,
          "layers": [plate("tissue_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5.0, "scale": 1.43}]),
                     close_ved([["warm", 0], ["explain", 1.6], ["smirk", 4.4]]),
                     txt("100,000,000+", 0.11, 110, enter="pop", at=1.2, sfx="pop", color="accent"),
                     txt("SWAPPED SINCE YOU HIT PLAY", 0.18, 62, enter="pop", at=1.6),
                     txt("SAME YOU. *NEW PARTS.*", 0.25, 80, enter="pop", at=4.0, sfx="ding")]})

SRCS = ["https://pmc.ncbi.nlm.nih.gov/articles/4991899",
        "https://www.smithsonianmag.com/smart-news/there-are-372-trillion-cells-inyour-body-4941473/",
        "https://wis-wander.weizmann.ac.il/node/11205",
        "https://www.mpg.de/11322481/oldest-homo-sapiens-fossils-at-jebel-irhoud-morocco",
        "https://knowyourmeme.com/memes/remember-november-2026-is-coming"]
job = {"id": ID, "title": "You are 30 trillion cells. Try counting them 🧬",
       "description": "Your body is roughly 30 trillion human cells (about 84% of them red blood cells), plus around 38 trillion "
                      "bacteria, and it replaces about 330 billion cells every day. Counting them at one per second would take "
                      "about 950,000 years.\n\nSources: " + " ; ".join(SRCS[:4]),
       "tags": ["human body", "cells", "how many cells", "red blood cells", "gut bacteria", "biology", "science explained", "facts", "anatomy"],
       "hashtags": ["#biology", "#science"],
       "meta": {"format": "scale-shock", "topic": "how many cells are in your body (~30 trillion) and how fast they're replaced",
                "hook": "number-shock", "idea_source": "backlog (ideas.md: How many cells are in your body?)",
                "characters": ["ved", "extra"], "sources": SRCS[:4],
                "humour": {"trend": "'Remember November 2026' (polar-bear 'meme from the future', revived late Aug 2026, it's now November 2026), as a deadpan text card",
                           "beat": "deadpan", "scene": 9}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
