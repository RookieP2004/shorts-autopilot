"""Deep Dive 2026-11-14-L (16:9): "Why You're 99.9999% Empty Space (And Still Solid)".
Built from the long pilot's helpers (jobs/2026-11-11-longpilot/build_job.py): same Ved, same townspeople and outfits, same look.
Sets: town-square cafe + stadium (from the sugar-cube Short, re-shot 16:9), a 1909 Manchester lab, deep space, plus the
pilot's island market plates. Run: python jobs/2026-11-14-L/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(14)
J = "jobs/2026-11-14-L/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_space.json") else "/tmp/claude-0/pv/"
PA = "jobs/2026-11-11-longpilot/assets/"     # the island market plates (same town as the pilot)
SA = "jobs/2026-11-11-a/assets/"             # sugar cube / marble / electron / nucleus cut-outs
OWN = ("cafe_wide", "cafe_mid", "cafe_table", "cafe_crushed", "stadium_wide", "stadium_pitch", "stadium_marble",
       "lab_wide", "lab_mid", "lab_close", "space")
PILOT = ("market_wide", "market_mid", "market_close")
ST = {n: Stage(SRC + f"plate_{n}.json") for n in OWN}
ST.update({n: Stage(PA + f"plate_{n}.json") for n in PILOT})
HAS_FG = {"market_wide", "market_mid", "market_close", "cafe_wide", "cafe_mid", "lab_wide", "lab_mid"}

# ---- the town: the same people as the Shorts (jobs/2026-11-08-m3)
OUT = {
    "seller": {"skin": "#c98e62", "build": "round", "hair": ["#1d1712", "short"], "hat": ["cap", "#2f6f8f"],
               "top": ["#e8e2d4", "shirt"], "apron": "#f6efe2", "bottom": ["#3a3e48", "trousers"]},
    "amina": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "necklace": "#6fc3c0",
              "earrings": "#f2b04a", "bag": "#8a5a3c", "hair": ["#140f0c", "long"]},
    "tomas": {"skin": "#e2b48d", "hat": ["straw", "#e6c27a"], "top": ["#6fc3c0", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "omar": {"skin": "#a0694a", "hat": ["fez", "#b03a2e"], "top": ["#f6efe2", "vest"], "bottom": ["#5a4636", "trousers"], "build": "round"},
    "lena": {"skin": "#e6b996", "top": ["#9b59b6", "dress"], "hair": ["#6b4423", "bun"], "earrings": "#f2b04a"},
    "ravi": {"skin": "#b97a55", "top": ["#7c2533", "kurta"], "bottom": ["#efe3c8", "trousers"], "hair": ["#2a2320", "curly"]},
    "banker": {"skin": "#f0c8a8", "hat": ["bowler", "#25262b"], "top": ["#34425c", "jacket"], "tie": "#c0392b",
               "bottom": ["#25262b", "trousers"], "belt": "#1a1a1a"},
    # 1600s London
    "goldsmith": {"skin": "#e8bfa0", "hat": ["beret", "#3a2a4a"], "top": ["#6b2e2e", "jacket"], "apron": "#3a2a1a",
                  "bottom": ["#2a2320", "trousers"], "necklace": "#e0b040", "build": "regular", "hair": ["#cfcfcf", "short"]},
    "merchant": {"skin": "#d9a882", "hat": ["tophat", "#2a2320"], "top": ["#2f5f4f", "jacket"], "bottom": ["#2a2320", "trousers"],
                 "belt": "#8a5a3c", "bag": "#5a3a22", "build": "round"},
    "lady": {"skin": "#f0cdb0", "hat": ["bowler", "#7c2533"], "top": ["#34425c", "dress"], "necklace": "#f6efe2", "earrings": "#e0b040"},
    # Manchester, 1909 (faceless, like everyone in the town)
    "rutherford": {"skin": "#ecc4a2", "build": "round", "hair": ["#8a8a8a", "short"], "top": ["#6b5a44", "jacket"], "tie": "#2a2320",
                   "bottom": ["#4a4038", "trousers"], "belt": "#1a1a1a"},
    "geiger": {"skin": "#f0cdb0", "build": "slim", "hair": ["#3a2a1e", "short"], "top": ["#2f3a48", "vest"], "tie": "#7c2533",
               "bottom": ["#2a2d33", "trousers"]},
    "marsden": {"skin": "#e8bfa0", "build": "slim", "hair": ["#7a4a24", "curly"], "top": ["#efe3c8", "shirt"], "tie": "#2f6f8f",
                "bottom": ["#5a4636", "trousers"]},
}


def _dir(name):
    return PA if name in PILOT else A


def plate(name, blur=0, **k):
    return {"type": "image", "path": _dir(name) + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": _dir(name) + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


SHARED = {"sugar_cube": SA, "marble": SA, "electron": SA, "nucleus": SA, "apple": PA, "coin": PA}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": SHARED.get(name, A) + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=84, x=0.5, **k):
    return {"type": "text", "text": t, "font": "display", "x": x, "y": y, "size": size, "max_w": k.pop("max_w", 0.62),
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


def ved(set_, wx, wy, acting="auto", walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0] if isinstance(acting, list) else "idle",
         "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none", "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def close_ved(acting="auto", x=0.27, **k):
    """Talking to camera: Ved big on one side of the frame, the set blurred behind."""
    return {"type": "character", "id": "ved", "pose": acting[0][0] if isinstance(acting, list) else "idle",
            "x": x, "y": 0.86, "h": 1.2, "enter": "none", "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def staged(set_, behind=(), front=(), top=()):
    """Plate, people behind the counter, the counter foreground layer, then everyone in front (far to near), then overlays."""
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if set_ in HAS_FG:
        out.append(fg(set_))
    out += sorted(front, key=lambda L: -L["_depth"])
    out += list(top)
    for L in out:
        L.pop("_depth", None)
    return out


def talk(set_, acting="auto", x=0.27, top=(), zoom=(1.0, 1.04)):
    return [plate(set_, blur=9, keys=[{"t": 0, "scale": zoom[0] * 1.15}, {"t": 6, "scale": zoom[1] * 1.15}]),
            close_ved(acting, x=x)] + list(top)


def fly(name, x0, y0, x1, y1, w, t0, dur=0.9, rot0=0, rot1=200, arc=0.12, keep=False, **k):
    xm, ym = (x0 + x1) / 2, min(y0, y1) - arc
    extra = {} if keep else {"until": t0 + dur, "exit": "fade", "exit_dur": 0.1}
    return sprite(name, x0, y0, w, at=t0, **extra,
                  keys=[{"t": 0, "x": x0, "y": y0, "rot": rot0, "scale": 0.5},
                        {"t": dur * 0.45, "x": xm, "y": ym, "rot": (rot0 + rot1) / 2, "scale": 1.0, "ease": "out"},
                        {"t": dur, "x": x1, "y": y1, "rot": rot1, "scale": 1.0, "ease": "in"}], **k)


def pop(name, x, y, w, at, **k):
    return sprite(name, x, y, w, enter="pop", at=at, sfx=k.pop("sfx", "pop"), **k)


def panel(svg, x, y, w, at, **k):
    return {"type": "image", "svg": svg, "x": x, "y": y, "w": w, "enter": "pop", "at": at, "sfx": "pop", **k}


def held(item, who_layer, w, dy=-0.03, dx=0.0):
    """A prop carried along by a walking person (follows their keys)."""
    L = who_layer
    if "keys" not in L:
        return sprite(item, L["x"] + dx, L["y"] + dy * L["h"] / 0.5, w)
    return sprite(item, L["keys"][0]["x"] + dx, L["keys"][0]["y"] + dy, w,
                  keys=[{"t": k["t"], "x": k["x"] + dx, "y": k["y"] + dy * k["scale"], "scale": k["scale"],
                         **({"walk": True} if k.get("walk") else {})} for k in L["keys"]])


F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
FS = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='600'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def card(w, h, body):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect width='{w}' height='{h}' rx='30' fill='#f6efe2'/>"
            f"<rect x='3' y='3' width='{w - 6}' height='{h - 6}' rx='28' fill='none' stroke='#1a1410' stroke-width='6'/>{body}</svg>")


def arrow(x, y, col="#f2b04a"):
    return f"<path d='M{x},{y - 8} L{x + 46},{y - 8} L{x + 46},{y - 22} L{x + 72},{y} L{x + 46},{y + 22} L{x + 46},{y + 8} L{x},{y + 8} Z' fill='{col}'/>"


S, CH = [], []


def chapter(title):
    CH.append({"scene": len(S), "title": title})


def scene(say, layers, **k):
    s = {"say": say, "layers": layers, **k}
    S.append(s)
    return s


def beat(set_, kind, text, x=0.3, text_x=0.66, text_y=0.3, dur=1.9):
    S.append({"dur": dur, "transition": "cut", "captions": False,
              "layers": [plate(set_, blur=9, keys=[{"t": 0, "scale": 1.15}]), dict(close_ved([["idle", 0]], x=x), acting="none")],
              "beat": {"kind": kind, "at": 0.1, "dur": dur - 0.4, "zoom": 1.08, "focus": [x, 0.3], "text": text,
                       "text_x": text_x, "text_y": text_y, "text_w": 0.4, "text_size": 54}})




def tag(t, x, y, at, col="#2c8f8a"):
    """Small honesty tag (PROVEN / THEORY) in the channel's flat style."""
    w = 30 * len(t) + 60
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 70'><rect width='{w}' height='70' rx='35' fill='{col}'/>"
           f"<text x='{w / 2}' y='48' font-size='38' text-anchor='middle' fill='#f6efe2' {F}>{t}</text></svg>")
    return {"type": "image", "svg": svg, "x": x, "y": y, "w": w / 1920 * 0.9, "enter": "pop", "at": at, "sfx": "click"}


def clean(layers):
    for L in layers:
        L.pop("_depth", None)
    return layers


def electrons(n, t0, x0=0.5, y0=0.55, rx=0.42, ry=0.3, w=0.03, spin=2.6):
    """Electrons buzzing round the back rows (elliptical paths, desynced)."""
    out = []
    for i in range(n):
        ph = i / n * 6.283 + random.uniform(-0.3, 0.3)
        keys = []
        for k in range(13):
            a = ph + k / 12 * 6.283
            import math
            keys.append({"t": k * spin / 12, "x": x0 + rx * math.cos(a), "y": y0 + ry * math.sin(a), "ease": "linear"})
        loop = [dict(kk, t=kk["t"] + spin * r) for r in range(4) for kk in keys]
        out.append(sprite("electron", keys[0]["x"], keys[0]["y"], w, at=t0, enter="fade", keys=loop))
    return out


# =================================================================== 1. Cold open
chapter("A sugar cube")
scene("This sugar cube could hold every human on Earth. All *eight billion* of us.",
      [plate("cafe_table", keys=[{"t": 0, "scale": 1.0}, {"t": 5, "scale": 1.08}]),
       txt("8,000,000,000 PEOPLE", 0.13, 96, x=0.5, max_w=0.8, enter="pop", at=2.4, sfx="boom"),
       txt("IN *THIS?*", 0.25, 110, x=0.5, enter="pop", at=3.4, sfx="ding")],
      camera={"zoom": [1.0, 1.04], "focus": [0.5, 0.55]})
scene("Sounds impossible. But stick with me, and you'll see why it's true, why you've never really touched anything, "
      "and why you still don't fall through your chair.",
      talk("cafe_mid", [["explain", 0], ["shrug", 2.0], ["point", 6.0]],
           top=[txt("WHY IT'S *TRUE*", 0.2, 76, x=0.68, enter="pop", at=1.6, sfx="pop"),
                txt("WHY YOU NEVER *TOUCH* ANYTHING", 0.36, 70, x=0.68, max_w=0.5, enter="pop", at=4.2, sfx="pop"),
                txt("WHY YOU DON'T *FALL THROUGH*", 0.54, 70, x=0.68, max_w=0.5, enter="pop", at=6.6, sfx="pop")]),
      transition="cut")
scene("Because almost everything around you, the table, the cup, the people... you. It's mostly empty space. So let's find out how empty.",
      staged("cafe_wide",
             behind=[person("cafe_wide", "seller", -1.4, 2.4, [["idle", 0], ["wave", 1.0]]),
                     person("cafe_wide", "lena", 3.5, 2.0, [["explain", 0]]),
                     person("cafe_wide", "ravi", 4.9, 2.2, [["happy", 0]]),
                     person("cafe_wide", "omar", -2.6, 3.0, [["hold", 0]])],
             front=[person("cafe_wide", "amina", 1.5, -0.4, [["idle", 0], ["surprised", 4.6]]),
                    person("cafe_wide", "tomas", -3.2, -1.2, [["idle", 0]], walk=[(0, -5.4, -1.6), (2.6, -2.6, -1.0)]),
                    ved("cafe_wide", -0.6, -1.6, [["welcome", 0], ["point", 2.6], ["explain", 5.0]], walk=[(0, 2.6, -2.2), (1.4, -0.6, -1.6)])],
             top=[txt("WHY YOU'RE *99.9999%* EMPTY", 0.12, 100, max_w=0.85, enter="zoom", at=5.6, sfx="boom")]),
      transition="slide_left", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.52]})

# =================================================================== 2. How small is an atom?
chapter("How small is an atom?")
ruler = card(1000, 300, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>ONE MILLIMETRE</text>
<line x1='60' y1='150' x2='940' y2='150' stroke='#1a1410' stroke-width='8'/>
<line x1='60' y1='120' x2='60' y2='180' stroke='#1a1410' stroke-width='8'/><line x1='940' y1='120' x2='940' y2='180' stroke='#1a1410' stroke-width='8'/>
{''.join(f"<circle cx='{80 + i * 20}' cy='150' r='9' fill='#6fc3c0'/>" for i in range(44))}
<text x='60' y='255' font-size='60' fill='#d98a1a' {AN}>= 10,000,000 ATOMS IN A ROW</text>""")
scene("Everything is made of atoms, and atoms are tiny. Line up *ten million* of them, and you'd cover just one millimetre.",
      staged("cafe_mid",
             behind=[person("cafe_mid", "seller", 1.6, 2.6, [["idle", 0]])],
             front=[ved("cafe_mid", -0.7, -0.6, [["explain", 0], ["point", 2.4]], walk=[(0, -2.4, -1.0), (1.2, -0.7, -0.6)])],
             top=[panel(ruler, 0.66, 0.24, 0.5, 2.6)]),
      transition="slide_left")
scene("Your body holds about seven billion billion billion atoms. That's a seven with twenty-seven zeros.",
      talk("cafe_mid", [["serious", 0], ["surprised", 3.0]], x=0.73,
           top=[{"type": "counter", "from": 1, "to": 7, "count_dur": 1.6, "at": 0.6, "x": 0.34, "y": 0.3,
                 "suffix": ",000,000,000,000,000,000,000,000,000", "size": 56, "stroke": "#0b0f12", "stroke_width": 6, "enter": "pop", "sfx": "riser"},
                txt("ATOMS IN *YOU*", 0.45, 84, x=0.34, enter="pop", at=3.0, sfx="ding")]),
      transition="cut")
scene("Too small to picture. So let's cheat. Let's blow one single atom up to the size of a *football stadium*.",
      [plate("stadium_wide", keys=[{"t": 0, "scale": 1.12}, {"t": 6, "scale": 1.0}]),
       txt("1 ATOM = 1 *STADIUM*", 0.12, 104, enter="zoom", at=2.6, sfx="boom")],
      transition="zoom")
scene("Walk down to the centre spot... and there's the nucleus. About the size of a *marble*.",
      staged("stadium_pitch",
             front=[ved("stadium_pitch", -4.0, 0.9, [["explain", 0], ["point", 2.6]], walk=[(0, -6.0, -0.4), (2.2, -4.0, 0.9)])],
             top=[{"type": "shape", "shape": "ring", "x": ST["stadium_pitch"].point(0, 0, 0.1)[0], "y": ST["stadium_pitch"].point(0, 0, 0.1)[1],
                   "w": 0.05, "color": "accent", "stroke_width": 6, "enter": "pop", "at": 2.8, "loop": "pulse"},
                  txt("THE *NUCLEUS*", 0.12, 100, enter="pop", at=3.0, sfx="ding")]),
      transition="cut")
scene("It's about a hundred thousand times smaller than the atom itself. And that marble holds more than *99.9 percent* of the atom's mass.",
      [plate("stadium_marble", keys=[{"t": 0, "scale": 1.0}, {"t": 4, "scale": 1.1}]),
       txt("100,000x SMALLER", 0.13, 96, enter="pop", at=0.6, until=3.6, exit="fade"),
       txt("*99.9%* OF THE MASS", 0.13, 104, enter="zoom", at=4.0, sfx="boom"), tag("PROVEN", 0.5, 0.25, 4.8)],
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.55]})
scene("The electrons? They're way out in the back rows of the stands. And between the marble and the seats...",
      [plate("stadium_wide", keys=[{"t": 0, "scale": 1.0}, {"t": 6, "scale": 1.04}])] + electrons(7, 0.6, y0=0.48, rx=0.44, ry=0.36) +
      [txt("ELECTRONS: *THE BACK ROWS*", 0.12, 92, max_w=0.8, enter="pop", at=1.0, sfx="pop")],
      transition="cut")
scene("...there's no air. No stuff. Just a whole stadium of *nothing*.",
      staged("stadium_pitch",
             front=[ved("stadium_pitch", -4.0, 0.9, [["shrug", 0], ["welcome", 1.6]])],
             top=[txt("*NOTHING*", 0.14, 150, enter="zoom", at=1.6, sfx="boom")]),
      transition="cut", camera={"zoom": [1.0, 1.08], "focus": [0.45, 0.5]})
beat("stadium_pitch", "deadpan", "Personal space?\n*Atoms invented it.*")

# =================================================================== 3. The gold foil surprise
chapter("The gold foil surprise")
scene("But how do we actually know this? In 1909, in Manchester, the physicist Ernest Rutherford gave two of his team a strange job.",
      staged("lab_wide",
             behind=[person("lab_wide", "rutherford", 0.9, 1.7, [["explain", 0], ["point", 4.4]])],
             front=[person("lab_wide", "geiger", -1.0, -0.4, [["idle", 0]], walk=[(0, -3.6, -1.0), (3.0, -1.0, -0.4)]),
                    person("lab_wide", "marsden", 2.6, -0.5, [["idle", 0], ["surprised", 5.2]], walk=[(0, 4.8, -0.9), (3.4, 2.6, -0.5)])],
             top=[txt("MANCHESTER, *1909*", 0.12, 96, enter="pop", at=1.6, sfx="ding")]),
      transition="fade")
scene("Hans Geiger and a twenty-year-old student, Ernest Marsden, fired tiny *alpha particles* at a sheet of gold, beaten thinner than paper.",
      staged("lab_mid",
             behind=[person("lab_mid", "geiger", 0.2, 1.5, [["point", 0], ["explain", 3.0]]),
                     person("lab_mid", "marsden", 1.5, 1.5, [["hold", 0], ["point", 4.0]])],
             top=[pop("alpha", 0.2, 0.3, 0.07, 3.6), txt("ALPHA PARTICLE", 0.42, 52, x=0.2, enter="pop", at=3.8, font="body"),
                  pop("goldfoil", 0.84, 0.3, 0.11, 5.6), txt("GOLD FOIL", 0.5, 52, x=0.84, enter="pop", at=5.8, font="body")]),
      transition="cut")
scene("Each particle that hit a screen made a tiny flash of light. So they sat in the dark, counting flashes through a microscope. One. By. One.",
      staged("lab_mid",
             behind=[person("lab_mid", "marsden", 1.5, 1.5, [["point", 0], ["explain", 3.4]]),
                     person("lab_mid", "geiger", 0.2, 1.5, [["idle", 0], ["shrug", 5.6]])],
             top=[{"type": "shape", "shape": "circle", "x": 0.5, "y": 0.5, "w": 1.6, "color": "#05070f", "opacity": 0.55, "enter": "fade", "at": 1.8},
                  {"type": "shape", "shape": "burst", "x": 0.62, "y": 0.5, "w": 0.04, "color": "#7dffb0", "enter": "pop", "at": 5.2, "until": 5.5},
                  {"type": "shape", "shape": "burst", "x": 0.6, "y": 0.52, "w": 0.04, "color": "#7dffb0", "enter": "pop", "at": 6.0, "until": 6.3},
                  {"type": "shape", "shape": "burst", "x": 0.63, "y": 0.49, "w": 0.04, "color": "#7dffb0", "enter": "pop", "at": 6.8, "until": 7.1},
                  txt("COUNTING *FLASHES*", 0.12, 96, enter="pop", at=2.4, sfx="pop")]),
      transition="cut")
pud = card(900, 380, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>THE ATOM, AS PICTURED IN 1909</text>
<ellipse cx='240' cy='225' rx='160' ry='120' fill='#e8a598'/>
{''.join(f"<circle cx='{170 + (i * 53) % 150}' cy='{150 + (i * 37) % 150}' r='14' fill='#1fa8ff'/>" for i in range(9))}
<text x='450' y='200' font-size='58' fill='#1a1410' {F}>soft "pudding"</text><text x='450' y='265' font-size='58' fill='#1a1410' {F}>of charge</text>
<text x='450' y='335' font-size='40' fill='#d98a1a' {AN}>(THOMSON, 1904)</text>""")
scene("At the time, scientists pictured the atom as a soft pudding of charge. So the particles should sail straight through. And almost all of them did.",
      [plate("lab_close", keys=[{"t": 0, "scale": 1.0}, {"t": 8, "scale": 1.06}]), panel(pud, 0.27, 0.26, 0.42, 0.4)] +
      [sprite("alpha", 0.0, 0.52, 0.03, at=4.6 + i * 0.45, keys=[{"t": 0, "x": -0.05, "y": 0.5 + 0.02 * (i % 3)},
              {"t": 0.9, "x": 1.08, "y": 0.47 + 0.03 * (i % 3), "ease": "linear"}], until=4.6 + i * 0.45 + 0.9) for i in range(8)] +
      [txt("STRAIGHT *THROUGH*", 0.12, 92, x=0.74, max_w=0.45, enter="pop", at=6.0)],
      transition="cut")
scene("But about one in every *eight thousand*... bounced right back.",
      [plate("lab_close", keys=[{"t": 0, "scale": 1.06}, {"t": 4, "scale": 1.14}])] +
      [sprite("alpha", 0.0, 0.52, 0.03, at=0.2 + i * 0.5, keys=[{"t": 0, "x": -0.05, "y": 0.5}, {"t": 0.9, "x": 1.08, "y": 0.48, "ease": "linear"}],
              until=0.2 + i * 0.5 + 0.9) for i in range(3)] +
      [sprite("alpha", 0.0, 0.52, 0.045, at=2.0, keys=[{"t": 0, "x": -0.05, "y": 0.52}, {"t": 0.55, "x": 0.5, "y": 0.52, "ease": "linear"},
              {"t": 1.2, "x": -0.08, "y": 0.3, "ease": "out"}], sfx="boom"),
       {"type": "shape", "shape": "burst", "x": 0.5, "y": 0.52, "w": 0.12, "color": "accent", "enter": "pop", "at": 2.5, "until": 3.1},
       txt("1 IN *8,000*", 0.13, 120, enter="zoom", at=2.8, sfx="ding"), tag("PROVEN", 0.5, 0.26, 3.4)],
      transition="cut", camera={"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.5, "zoom": 1.0, "focus": [0.5, 0.5]},
                                         {"t": 2.7, "zoom": 1.1, "focus": [0.5, 0.5]}]})
beat("lab_mid", "side_eye", "The gold atom:\n*\"You want to pass through?\nYou sure?\"*", dur=2.4)
scene("Rutherford later said it was as incredible as firing a fifteen-inch shell at a piece of tissue paper... and having it come back and hit you.",
      talk("lab_mid", [["explain", 0], ["surprised", 5.0], ["point", 6.6]],
           top=[txt("\"...IT CAME BACK AND *HIT YOU.*\"", 0.3, 80, x=0.68, max_w=0.5, enter="pop", at=5.4, sfx="boom"),
                txt("Ernest Rutherford, 1936 lecture", 0.47, 44, x=0.68, enter="pop", at=6.4, font="body")]),
      transition="cut")
nuc = card(900, 380, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>RUTHERFORD'S ATOM, 1911</text>
<circle cx='230' cy='230' r='120' fill='none' stroke='#6fc3c0' stroke-width='5' stroke-dasharray='12 12'/>
<circle cx='230' cy='230' r='10' fill='#d9534f'/><circle cx='350' cy='230' r='13' fill='#1fa8ff'/><circle cx='150' cy='140' r='13' fill='#1fa8ff'/>
<text x='420' y='190' font-size='52' fill='#1a1410' {F}>tiny, heavy core</text><text x='420' y='265' font-size='52' fill='#1a1410' {F}>+ mostly empty</text>
<text x='420' y='335' font-size='40' fill='#d98a1a' {AN}>= THE NUCLEUS</text>""")
scene("The only explanation: nearly all the atom's mass is packed into one tiny, dense core. In 1911, Rutherford published the idea. We call that core the *nucleus*.",
      staged("lab_wide",
             behind=[person("lab_wide", "rutherford", 0.9, 1.7, [["explain", 0], ["cheer", 6.0]], hops=[[6.2, 0.03, 0.45]])],
             front=[person("lab_wide", "geiger", -1.0, -0.4, [["happy", 6.2]]),
                    person("lab_wide", "marsden", 2.6, -0.5, [["cheer", 6.2]])],
             top=[panel(nuc, 0.5, 0.24, 0.46, 1.0)]),
      transition="cut")

# =================================================================== 4. Is it really empty?
chapter("Is it really empty?")
scene("Now, a fair warning. 'Mostly empty space' is the classic picture. But many physicists say it's a little misleading.",
      talk("stadium_pitch", [["serious", 0], ["point", 3.4]],
           top=[txt("A FAIR *WARNING*", 0.3, 100, x=0.68, enter="pop", at=0.6, sfx="ding")]),
      transition="slide_left")
fog = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'><defs><radialGradient id='g'>"
       "<stop offset='0' stop-color='#1fa8ff' stop-opacity='0.85'/><stop offset='0.55' stop-color='#1fa8ff' stop-opacity='0.35'/>"
       "<stop offset='1' stop-color='#1fa8ff' stop-opacity='0'/></radialGradient></defs>"
       "<circle cx='300' cy='300' r='300' fill='url(#g)'/><circle cx='300' cy='300' r='10' fill='#d9534f'/></svg>")
scene("Electrons aren't little balls zooming round the stands. Quantum physics says each one is *spread out*, like a fog, filling the whole atom.",
      [plate("stadium_wide", keys=[{"t": 0, "scale": 1.04}])] + electrons(6, 0.0, y0=0.48, rx=0.44, ry=0.36) +
      [{"type": "image", "svg": fog, "x": 0.5, "y": 0.5, "w": 0.95, "enter": "fade", "enter_dur": 1.6, "at": 3.0, "loop": "pulse", "loop_amp": 0.3},
       txt("ELECTRONS = *A FOG*", 0.12, 100, enter="pop", at=4.0, sfx="ding"), tag("PROVEN", 0.5, 0.88, 4.6)],
      transition="cut")
both = card(1100, 380, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>SO, IS AN ATOM EMPTY?</text>
<text x='60' y='160' font-size='42' fill='#1a1410' {F}>Where is the MASS?</text><text x='640' y='160' font-size='48' fill='#d98a1a' {AN}>MOSTLY EMPTY</text>
<text x='60' y='260' font-size='42' fill='#1a1410' {F}>Where's the ELECTRON?</text><text x='640' y='260' font-size='48' fill='#2c8f8a' {AN}>EVERYWHERE</text>
<text x='60' y='340' font-size='34' fill='#5a4636' {FS}>Both true. Different questions.</text>""")
scene("So which is it? If you ask where the mass sits, the atom is almost all empty. If you ask where the electron can be, it fills the space. Both are true. They just answer different questions.",
      talk("stadium_wide", [["think", 0], ["explain", 3.0], ["point", 6.4], ["warm", 10.0]], x=0.24,
           top=[panel(both, 0.66, 0.36, 0.54, 0.8)]),
      transition="cut")

# =================================================================== 5. Why you don't fall through your chair
chapter("Why you don't fall through your chair")
scene("So if atoms are that roomy... why don't you sink straight through your chair?",
      staged("cafe_mid",
             behind=[person("cafe_mid", "seller", 1.6, 2.6, [["idle", 0], ["shrug", 2.0]])],
             front=[ved("cafe_mid", -1.1, -0.3, [["think", 0], ["shrug", 2.4]], walk=[(0, -2.8, -0.8), (1.6, -1.1, -0.3)])],
             top=[txt("WHY DON'T YOU *SINK?*", 0.12, 100, enter="pop", at=2.0, sfx="ding")]),
      transition="slide_left")
rep = card(900, 340, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>REASON 1: LIKE CHARGES PUSH</text>
<circle cx='200' cy='210' r='70' fill='#1fa8ff'/><text x='200' y='235' font-size='90' text-anchor='middle' fill='#f6efe2' {AN}>-</text>
<circle cx='700' cy='210' r='70' fill='#1fa8ff'/><text x='700' y='235' font-size='90' text-anchor='middle' fill='#f6efe2' {AN}>-</text>
<path d='M300,210 L380,180 L380,240 Z' fill='#d9534f'/><path d='M600,210 L520,180 L520,240 Z' fill='#d9534f'/>
<text x='450' y='310' font-size='40' text-anchor='middle' fill='#d98a1a' {AN}>PUSH! PUSH!</text>""")
scene("Two reasons. First: the outside of every atom is electrons, and electrons all carry a *negative* charge. Like charges push each other away. Hard.",
      talk("cafe_mid", [["explain", 0], ["point", 3.0], ["crossed", 7.0]], x=0.27,
           top=[panel(rep, 0.68, 0.34, 0.46, 1.4)]),
      transition="cut")
pau = card(900, 360, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>REASON 2: THE PAULI EXCLUSION PRINCIPLE</text>
<rect x='80' y='120' width='160' height='130' rx='20' fill='#6fc3c0'/><rect x='300' y='120' width='160' height='130' rx='20' fill='#6fc3c0'/>
<rect x='520' y='120' width='160' height='130' rx='20' fill='#6fc3c0'/>
<circle cx='160' cy='185' r='34' fill='#1fa8ff'/><circle cx='380' cy='185' r='34' fill='#1fa8ff'/>
<circle cx='600' cy='185' r='34' fill='#1fa8ff' opacity='0.35'/><text x='705' y='205' font-size='58' fill='#d9534f' {AN}>FULL</text>
<text x='80' y='320' font-size='42' fill='#1a1410' {F}>No two electrons in the same state.</text>""")
scene("Second: a quantum rule called the *Pauli exclusion principle*. No two electrons can squeeze into the same state. So atoms refuse to collapse into each other.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["shrug", 0]])],
             front=[person("market_wide", "tomas", -1.6, -1.4, [["idle", 0], ["shrug", 4.0]], walk=[(0, -4.0, -2.0), (2.4, -1.6, -1.4)]),
                    person("market_wide", "amina", -0.6, -1.2, [["idle", 0], ["point", 4.4]]),
                    ved("market_wide", 2.2, -2.6, [["explain", 0], ["point", 5.0]])],
             top=[panel(pau, 0.5, 0.2, 0.5, 1.6), tag("PROVEN", 0.5, 0.41, 2.6)]),
      transition="cut")
scene("In 1967, the physicists Freeman Dyson and Andrew Lenard proved that without this rule, ordinary matter would *collapse*. Putting two objects together would release energy like an atomic bomb.",
      talk("market_mid", [["serious", 0], ["point", 3.2]], x=0.73,
           top=[txt("WITHOUT IT: *COLLAPSE*", 0.3, 92, x=0.32, max_w=0.5, enter="pop", at=4.2, sfx="boom"),
                txt("Dyson & Lenard, 1967", 0.45, 50, x=0.32, enter="pop", at=1.8, font="body"),
                txt("= AN *ATOMIC BOMB*", 0.58, 64, x=0.32, max_w=0.5, enter="pop", at=8.4, sfx="boom")]),
      transition="cut")
scene("So when you shake someone's hand, your atoms never bump like two billiard balls. What you feel as touch... is electrons pushing back.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["idle", 0]])],
             front=[person("market_mid", "tomas", -0.9, -0.7, [["give", 0.4], ["happy", 3.0]], walk=[(0, -2.8, -1.2), (1.6, -0.9, -0.7)]),
                    person("market_mid", "amina", 0.3, -0.7, [["take", 0.4], ["happy", 3.0]]),
                    ved("market_mid", 1.6, -1.6, [["explain", 0], ["point", 4.6]])],
             top=[txt("TOUCH = *ELECTRONS PUSHING*", 0.12, 92, max_w=0.8, enter="pop", at=5.0, sfx="ding")]),
      transition="cut")
scene("Some physicists say that push is simply what touching means. Fair enough. Either way, it's a force you feel, not a wall of stuff.",
      talk("market_close", [["shrug", 0], ["warm", 3.2]],
           top=[txt("A *FORCE*, NOT A WALL", 0.3, 92, x=0.68, max_w=0.5, enter="pop", at=4.2, sfx="pop")]),
      transition="cut")
beat("market_close", "deadpan", "Me: *touching grass.*\nThe grass: technically, no.", x=0.27)

# =================================================================== 6. Squeeze out the space
chapter("Squeeze out the space")
scene("Now, back to our sugar cube. Take every atom in every person on Earth, and squeeze out all that empty space.",
      [plate("cafe_table", keys=[{"t": 0, "scale": 1.08}, {"t": 6, "scale": 1.0}])] +
      [person("cafe_mid", ["amina", "tomas", "lena", "omar", "ravi", "seller"][i], 0, 0, [["idle", 0]],
              x=[0.1, 0.9, 0.2, 0.8, 0.05, 0.95][i], y=0.78, h=0.3, ground=False, at=1.6 + i * 0.3, enter="pop",
              keys=[{"t": 0, "x": [0.1, 0.9, 0.2, 0.8, 0.05, 0.95][i], "y": 0.78, "scale": 1.0},
                    {"t": 3.0 - i * 0.1, "x": [0.1, 0.9, 0.2, 0.8, 0.05, 0.95][i], "y": 0.78, "scale": 1.0},
                    {"t": 4.0 - i * 0.1, "x": 0.5, "y": 0.6, "scale": 0.05, "ease": "in"}]) for i in range(6)] +
      [txt("SQUEEZE OUT *THE SPACE*", 0.12, 96, enter="pop", at=0.6, sfx="whoosh")],
      transition="slide_left")
clean(S[-1]["layers"])
scene("All eight billion of us would fit in a cube about this size. But it would still weigh as much as all of us. *Hundreds of millions* of tonnes.",
      talk("cafe_table", [["explain", 0], ["point", 2.0], ["surprised", 5.4]], x=0.27,
           top=[pop("sugar_cube", 0.68, 0.32, 0.14, 1.6, loop="float", loop_amp=0.6),
                txt("~ *HUNDREDS OF MILLIONS* OF TONNES", 0.56, 66, x=0.68, max_w=0.5, enter="pop", at=6.0, sfx="boom")]),
      transition="cut")
scene("Which is bad news for the table.",
      [plate("cafe_crushed", keys=[{"t": 0, "scale": 1.0}])],
      transition="flash", sfx="boom", camera={"shake": [0.0, 0.6]}, min_dur=2.6)
scene("And the universe actually does this. When a giant star dies, its core can collapse into a *neutron star*.",
      [plate("space", keys=[{"t": 0, "scale": 1.1}, {"t": 7, "scale": 1.0}]),
       txt("A *NEUTRON STAR*", 0.12, 104, enter="zoom", at=4.0, sfx="boom")],
      transition="fade")
ns = card(900, 360, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>A NEUTRON STAR</text>
<text x='60' y='165' font-size='54' fill='#1a1410' {F}>MASS:</text><text x='330' y='165' font-size='60' fill='#d98a1a' {AN}>1-2 x OUR SUN</text>
<text x='60' y='260' font-size='54' fill='#1a1410' {F}>WIDTH:</text><text x='330' y='260' font-size='60' fill='#2c8f8a' {AN}>~20 KM (A CITY)</text>
<text x='60' y='330' font-size='34' fill='#5a4636' {FS}>Our Sun is 1.4 million km wide.</text>""")
scene("Gravity squeezes so hard that electrons are pushed into protons, turning them into neutrons, packed shoulder to shoulder. Almost no empty space left.",
      [plate("space", keys=[{"t": 0, "scale": 1.0}, {"t": 8, "scale": 1.12}], blur=4),
       pop("electron", 0.3, 0.45, 0.05, 1.6, keys=[{"t": 0, "x": 0.3}, {"t": 1.4, "x": 0.45, "ease": "in"}], until=3.2),
       pop("nucleus", 0.5, 0.45, 0.08, 1.2, sfx="pop"),
       txt("e- + p+ = *NEUTRON*", 0.12, 96, enter="pop", at=3.2, sfx="ding"), tag("PROVEN", 0.5, 0.24, 4.0),
       txt("NO ROOM LEFT", 0.72, 80, enter="pop", at=7.0, color="accent", sfx="boom")],
      transition="cut")
scene("A neutron star packs more mass than our Sun into a ball about *twenty kilometres* across. Roughly the size of a city.",
      [plate("space", keys=[{"t": 0, "scale": 1.0}, {"t": 7, "scale": 1.04}]), panel(ns, 0.3, 0.32, 0.46, 0.6), tag("PROVEN", 0.3, 0.6, 2.2)],
      transition="cut")
scene("A sugar cube of neutron star would weigh about a *billion tonnes*. As much as the whole human race.",
      talk("space", [["serious", 0], ["surprised", 3.2]], x=0.27,
           top=[pop("sugar_cube", 0.68, 0.24, 0.09, 0.8), txt("WEIGHS", 0.4, 64, x=0.68, enter="pop", at=2.2),
                {"type": "counter", "from": 0, "to": 1000, "count_dur": 1.4, "at": 2.6, "x": 0.68, "y": 0.52, "size": 72,
                 "suffix": ",000,000 TONNES", "stroke": "#0b0f12", "stroke_width": 6, "enter": "pop", "sfx": "ding"},
                txt("NASA estimate", 0.63, 44, x=0.68, enter="pop", at=3.4, font="body")]),
      transition="cut")

# =================================================================== 7. So what are you made of?
chapter("So what are you made of?")
scene("One last twist. Even the marble isn't really solid stuff. It's made of protons and neutrons, and they're made of *quarks*.",
      [plate("stadium_marble", keys=[{"t": 0, "scale": 1.1}, {"t": 6, "scale": 1.0}]),
       pop("nucleus", 0.78, 0.3, 0.14, 3.0), txt("PROTONS + NEUTRONS", 0.52, 52, x=0.78, enter="pop", at=3.2, font="body"),
       txt("*QUARKS*", 0.12, 110, enter="zoom", at=5.4, sfx="boom")],
      transition="slide_left")
pie = card(900, 400, f"""
<text x='60' y='75' font-size='36' fill='#5a4636' {FS}>WHERE A PROTON'S MASS COMES FROM</text>
<circle cx='210' cy='240' r='110' fill='#f2b04a'/>
<path d='M210,240 L210,130 A110,110 0 0,1 216.9,130.2 Z' fill='#d9534f'/>
<text x='370' y='200' font-size='60' fill='#d98a1a' {AN}>~99% ENERGY</text><text x='370' y='245' font-size='32' fill='#1a1410' {F}>of the strong force</text>
<text x='370' y='330' font-size='50' fill='#d9534f' {AN}>~1% QUARK MASS</text>""")
scene("And the quarks' own mass is only about one percent of it. The other ninety-nine percent is *energy*: the strong force, holding them together. E equals m c squared, at work inside you.",
      talk("stadium_marble", [["explain", 0], ["point", 4.0], ["surprised", 9.0]], x=0.27,
           top=[panel(pie, 0.68, 0.32, 0.46, 0.6), txt("E = mc2", 0.62, 96, x=0.68, enter="pop", at=8.2, sfx="ding"), tag("PROVEN", 0.68, 0.72, 9.0)]),
      transition="cut")
scene("So you're not made of tiny hard balls. You're made of *forces*: electric pushes, quantum rules, and trapped energy.",
      staged("cafe_wide",
             behind=[person("cafe_wide", "seller", -1.4, 2.4, [["happy", 0]]),
                     person("cafe_wide", "lena", 3.5, 2.0, [["happy", 0]]),
                     person("cafe_wide", "ravi", 4.9, 2.2, [["cheer", 2.0]]),
                     person("cafe_wide", "omar", -2.6, 3.0, [["wave", 0]])],
             front=[person("cafe_wide", "amina", 1.5, -0.4, [["happy", 0]]),
                    person("cafe_wide", "tomas", -2.6, -1.0, [["cheer", 1.0]], hops=[[1.4, 0.03, 0.45]]),
                    ved("cafe_wide", -0.6, -1.6, [["explain", 0], ["welcome", 3.0]])],
             top=[txt("YOU = *FORCES*", 0.12, 110, enter="pop", at=3.0, sfx="ding")]),
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.52]})
scene("Solid isn't stuff. It's a *push* you can feel.",
      talk("cafe_mid", [["warm", 0], ["crossed", 1.6]],
           top=[txt("SOLID ISN'T STUFF.", 0.26, 96, x=0.68, max_w=0.5, enter="pop", at=0.2),
                txt("IT'S A *PUSH* YOU CAN FEEL.", 0.44, 96, x=0.68, max_w=0.5, enter="pop", at=1.4, sfx="ding")]),
      transition="cut", min_dur=4.0)
scene("If that blew your mind a little, subscribe. Every week, one big idea, made simple.",
      staged("cafe_mid",
             behind=[person("cafe_mid", "seller", 1.6, 2.6, [["wave", 0]])],
             front=[person("cafe_mid", "amina", 1.4, 0.2, [["wave", 0.4]]),
                    ved("cafe_mid", -0.7, -0.6, [["welcome", 0], ["warm", 2.0]], hops=[[0.3, 0.03, 0.45]])],
             top=[txt("*SUBSCRIBE*", 0.12, 110, x=0.62, enter="zoom", at=0.5, sfx="ding"),
                  txt("ONE BIG IDEA, EVERY WEEK", 0.23, 60, x=0.62, enter="pop", at=2.0, font="body")]),
      transition="cut")

for s in S:
    clean(s["layers"])

job = {"id": "2026-11-14-L", "kind": "long",
       "title": "Why You're 99.9999% Empty Space (And Still Solid)",
       "description": "Every human on Earth could fit inside one sugar cube. Professor Ved shrinks you down to the atom: a stadium-sized atom "
                      "with a marble for a nucleus, the 1909 gold-foil experiment where 1 in 8,000 alpha particles bounced back, why "
                      "'mostly empty' is only half the story (electrons are spread-out clouds), why you don't fall through your chair "
                      "(electric repulsion + the Pauli exclusion principle), neutron stars, and where your mass really comes from.\n\n"
                      "Sources: Geiger & Marsden, 'On a Diffuse Reflection of the alpha-Particles' (Proc. Royal Society, 1909); "
                      "Rutherford (Phil. Mag., 1911) and his 1936 Cambridge lecture; Dyson & Lenard, 'Stability of Matter' (J. Math. Phys., 1967); "
                      "NASA via Space.com on neutron stars; Jefferson Lab on atoms in the body; Ethan Siegel (Big Think), 'You are not mostly empty space'.",
       "tags": ["empty space", "atoms explained", "physics", "rutherford gold foil", "pauli exclusion principle", "neutron star",
                "why don't we fall through chairs", "quantum physics", "science explained", "explained", "education"],
       "chapters": CH,
       "thumbnail": {
           "title": "YOU'RE *EMPTY?*", "title_y": 0.14, "title_size": 220, "glow": "#6fc3c0", "glow_x": 0.45, "glow_y": 0.58, "blur": 16,
           "glow_strength": 1.6, "bg_saturation": 1.8, "bg_brightness": 0.9,
           "tint": ["#2a5bd7", "#f08a24"], "tint_amount": 0.45,
           "bg": clean(staged("cafe_wide",
                              behind=[person("cafe_wide", "seller", -1.4, 2.4, [["surprised", 0]])],
                              front=[person("cafe_wide", "amina", 1.5, -0.4, [["surprised", 0]]),
                                     person("cafe_wide", "tomas", -2.6, -1.0, [["surprised", 0]])])),
           "fg": [sprite("sugar_cube", 0.16, 0.66, 0.17, rot=-8),
                  dict(close_ved([["surprised", 0]], x=0.45), y=1.2, h=1.7, acting="none", talk=False),
                  sprite("nucleus", 0.8, 0.62, 0.2, rot=10)]},
       "meta": {"format": "deep-dive", "topic": "why matter is mostly empty space: atom scale, Rutherford gold foil, electron clouds, "
                                                 "why you don't fall through your chair (Pauli), neutron stars, mass from energy",
                "hook": "number-shock",
                "idea_source": "best-retention Short of the week (2026-11-11-a sugar cube, 36% viewed) taken deeper + backlog follow-ups "
                               "(fall through the floor, neutron-star teaspoon, atoms touch); viral-shaped",
                "characters": ["ved", "extra"],
                "sources": ["https://www.chemteam.info/Chem-History/GM-1909.html",
                            "https://en.wikiquote.org/wiki/Ernest_Rutherford",
                            "https://education.jlab.org/qa/mathatom_04.html",
                            "https://www.space.com/22180-neutron-stars.html",
                            "https://web.math.ku.dk/~solovej/science-news.html",
                            "https://scitechdaily.com/the-strength-of-the-strong-force-accounting-for-99-of-the-ordinary-mass-in-the-universe/",
                            "https://bigthink.com/starts-with-a-bang/you-are-not-mostly-empty-space/",
                            "https://openstax.org/books/university-physics-volume-3/pages/10-1-properties-of-nuclei"],
                "claims": [["~10 million atoms in a row span 1 mm (atoms ~0.1 nm)", "PROVEN", "openstax"],
                           ["~7x10^27 atoms in a 70 kg body", "PROVEN", "jlab"],
                           ["nucleus ~1/100,000 of the atom's width, >99.9% of its mass", "PROVEN", "openstax"],
                           ["1909 Geiger-Marsden: ~1 in 8000 alpha particles reflected", "PROVEN", "chemteam GM-1909"],
                           ["Rutherford 15-inch shell quote (1936 lecture)", "PROVEN", "wikiquote"],
                           ["electrons are spread-out clouds; 'mostly empty' is debated framing", "PROVEN", "bigthink"],
                           ["Dyson & Lenard 1967: Pauli exclusion needed for stability of matter", "PROVEN", "ku.dk"],
                           ["neutron star 1-2 solar masses, ~20 km; sugar cube ~1 billion tonnes", "PROVEN", "space.com/NASA"],
                           ["~99% of proton mass from strong-force energy, ~1% from Higgs/quark masses", "PROVEN", "scitechdaily"]],
                "humour": {"trend": "'You want to pass through? You sure?' (new meme template, memeidea Nov 13 2026), 'touch grass' slang, "
                                    "plus a timeless dry 'personal space' line",
                           "beat": "deadpan, side_eye, deadpan", "scene": [n for n, s in enumerate(S) if s.get("beat")]}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "chapters", len(CH), "words", sum(len(s.get("say", "").split()) for s in S), "using", SRC)
