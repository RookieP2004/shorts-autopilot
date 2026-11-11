"""Long-form pilot (16:9 Deep Dive): "How money actually works".
Same world, cast and style as the approved Shorts (jobs/2026-11-08-m3), framed for landscape.
Run after the assets exist (or with /tmp/lp_pv previews for planning): python jobs/2026-11-11-longpilot/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(21)
J = "jobs/2026-11-11-longpilot/"
A = os.environ.get("LP_ASSETS", J + "assets/")
SRC = A if os.path.exists(A + "plate_goldsmith_mid.json") else "/tmp/lp_pv/"
SETS = ("market_wide", "market_mid", "market_close", "bank", "bank_desk", "vault", "goldsmith_wide", "goldsmith_mid")
ST = {n: Stage(SRC + f"plate_{n}.json") for n in SETS}
HAS_FG = {"market_wide", "market_mid", "market_close", "bank_desk", "goldsmith_wide", "goldsmith_mid"}

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
}


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


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


# =================================================================== 1. Intro
chapter("A piece of paper")
mm = ST["market_mid"]
scene("Hey. This... is a piece of paper.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["idle", 0]])],
             front=[person("market_mid", "amina", -0.9, -0.9, [["idle", 0]]),
                    ved("market_mid", 0.9, -1.4, [["warm", 0], ["point", 1.4]], walk=[(0, 3.2, -1.8), (1.2, 0.9, -1.4)])],
             top=[pop("bill", 0.72, 0.3, 0.2, 1.5, keys=[{"t": 0, "rot": -8}, {"t": 2.5, "rot": 6}])]),
      camera={"zoom": [1.0, 1.05], "focus": [0.55, 0.5]})
scene("And yet, this man will hand you an apple for it.",
      staged("market_close",
             behind=[person("market_close", "seller", 0.3, 0.85, [["idle", 0], ["take", 0.9], ["give", 1.9]])],
             top=[fly("bill", 0.12, 0.7, 0.42, 0.5, 0.14, 0.5, dur=0.7, rot0=-10, rot1=12, arc=0.08),
                  sprite("apple", 0.47, 0.56, 0.06, at=1.9, keys=[{"t": 0, "x": 0.47, "y": 0.56}, {"t": 0.7, "x": 0.1, "y": 0.72, "ease": "out"}])]),
      transition="cut")
scene("Paper doesn't taste good. You can't plant it. So what makes money... money?",
      talk("market_mid", [["explain", 0], ["shrug", 2.3], ["point", 4.2]],
           top=[txt("WHAT MAKES MONEY *MONEY?*", 0.3, 92, x=0.68, max_w=0.5, enter="pop", at=3.6, sfx="ding")]),
      transition="cut")
scene("Let's build money from scratch, right here, on our little island. And by the end, you'll know who really creates most of the world's money. Hint: it's probably not who you think.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["wave", 0], ["idle", 1.4]])],
             front=[person("market_wide", "tomas", -3.4, -2.2, [["idle", 0]], walk=[(0, -5.2, -2.6), (3.2, -2.6, -1.9)]),
                    person("market_wide", "lena", 3.3, -1.2, [["idle", 0]], walk=[(0, 5.4, -0.9), (3.0, 2.6, -1.5)]),
                    person("market_wide", "omar", -2.2, 1.0, [["hold", 0]]),
                    person("market_wide", "ravi", 2.6, 1.4, [["explain", 0]]),
                    person("market_wide", "amina", -0.9, -1.2, [["idle", 0]]),
                    ved("market_wide", 0.9, -3.0, [["welcome", 0]])],
             top=[txt("HOW MONEY *ACTUALLY* WORKS", 0.12, 100, max_w=0.8, enter="zoom", at=0.4, sfx="boom", until=5.0, exit="fade"),
                  txt("WHO *REALLY* MAKES MONEY?", 0.12, 92, max_w=0.8, enter="pop", at=5.2, sfx="ding")]),
      transition="slide_left", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.52]})

# =================================================================== 2. Barter
chapter("The barter problem")
tom = person("market_mid", "tomas", -0.7, -0.9, [["hold", 0], ["give", 2.0]], walk=[(0, -3.0, -1.4), (1.6, -0.7, -0.9)])
scene("Before money, the story goes, people simply swapped. Tomas has a fish. He wants apples.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["idle", 0], ["surprised", 3.8]])],
             front=[tom, ved("market_mid", 1.3, -1.6, [["explain", 0], ["point", 3.2]])],
             top=[held("fish", tom, 0.07, dy=-0.06, dx=0.035),
                  txt("BARTER", 0.12, 96, enter="pop", at=0.6, sfx="ding")]),
      transition="slide_left")
scene("But the seller doesn't want fish. He wants a clay pot.",
      staged("market_close",
             behind=[person("market_close", "seller", 0.3, 0.85, [["shrug", 0], ["point", 1.6]])],
             top=[sprite("fish", 0.2, 0.62, 0.12, rot=-8),
                  {"type": "shape", "shape": "circle", "x": 0.72, "y": 0.27, "w": 0.15, "color": "primary", "enter": "pop", "at": 1.4},
                  pop("pot", 0.72, 0.27, 0.07, 1.5)]),
      transition="cut")
chain = card(1100, 300, f"""
<text x='70' y='70' font-size='34' fill='#5a4636' {FS}>WHO WANTS WHAT</text>
<text x='70' y='175' font-size='54' fill='#1a1410' {F}>TOMAS</text>{arrow(260, 160)}
<text x='350' y='175' font-size='54' fill='#1a1410' {F}>SELLER</text>{arrow(570, 160)}
<text x='660' y='175' font-size='54' fill='#1a1410' {F}>OMAR</text>{arrow(835, 160, '#d9534f')}
<text x='925' y='175' font-size='54' fill='#d9534f' {F}>???</text>
<text x='70' y='255' font-size='30' fill='#5a4636' {FS}>fish for apples? apples for a pot? pots for bread?</text>""")
scene("Omar makes pots... but he wants bread. Nobody's wants line up.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["shrug", 0]])],
             front=[person("market_wide", "omar", -2.2, 1.0, [["hold", 0], ["shrug", 2.2]]),
                    person("market_wide", "tomas", -1.0, -1.6, [["hold", 0], ["sad", 2.6]]),
                    ved("market_wide", 1.6, -2.6, [["shrug", 0]])],
             top=[panel(chain, 0.5, 0.2, 0.56, 0.5)]),
      transition="cut")
scene("Economists call this the double coincidence of wants. Both of you must want exactly what the other one has.",
      talk("market_mid", [["explain", 0], ["point", 3.0]],
           top=[txt("THE *DOUBLE COINCIDENCE* OF WANTS", 0.32, 84, x=0.68, max_w=0.5, enter="pop", at=0.8, sfx="ding")]),
      transition="cut")
scene("Here's the twist. Anthropologists have never found a society that ran purely on barter. When people did barter, it was usually with strangers they'd never see again.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["idle", 0]])],
             front=[ved("market_mid", 0.2, -1.3, [["serious", 0], ["point", 2.2]], walk=[(0, 1.6, -1.6), (1.0, 0.2, -1.3)])],
             top=[txt("NO PURE BARTER ECONOMY *EVER FOUND*", 0.13, 84, max_w=0.7, enter="pop", at=2.8, sfx="boom")]),
      transition="cut", camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.5], "punch": [3.0]})
ledger = card(820, 380, f"""
<text x='60' y='80' font-size='36' fill='#5a4636' {FS}>THE VILLAGE MEMORY</text>
<line x1='60' y1='105' x2='760' y2='105' stroke='#1a1410' stroke-width='3' opacity='0.3'/>
<text x='60' y='175' font-size='46' fill='#1a1410' {F}>Tomas owes seller</text><text x='560' y='175' font-size='54' fill='#d98a1a' {AN}>3 apples</text>
<text x='60' y='250' font-size='46' fill='#1a1410' {F}>Seller owes Omar</text><text x='560' y='250' font-size='54' fill='#d98a1a' {AN}>1 pot</text>
<text x='60' y='325' font-size='46' fill='#1a1410' {F}>Omar owes Tomas</text><text x='560' y='325' font-size='54' fill='#d98a1a' {AN}>2 fish</text>""")
scene("Real villages ran on trust. Take the apples now, help me later. Everyone just remembered who owed whom.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["give", 0], ["happy", 1.6]])],
             front=[person("market_wide", "tomas", -0.7, -1.3, [["take", 0], ["happy", 1.8]]),
                    person("market_wide", "omar", -2.2, 1.0, [["wave", 0]]),
                    ved("market_wide", 1.8, -2.4, [["warm", 0]])],
             top=[panel(ledger, 0.74, 0.3, 0.38, 2.4)]),
      transition="cut")

# =================================================================== 3. Something everyone accepts
chapter("Something everyone accepts")
scene("But trust is hard with strangers. So people settled on one thing that everyone would accept.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["idle", 0], ["shrug", 1.4]])],
             front=[person("market_wide", "merchant", 3.0, -1.4, [["wave", 0]], walk=[(0, 5.6, -1.0), (2.4, 2.6, -1.5)]),
                    person("market_wide", "amina", -0.9, -1.2, [["surprised", 0]]),
                    ved("market_wide", -2.0, -2.6, [["explain", 0]])],
             top=[txt("ONE THING *EVERYONE* ACCEPTS", 0.12, 88, max_w=0.7, enter="pop", at=3.0)]),
      transition="slide_left")
traits = card(900, 330, f"""
<text x='60' y='78' font-size='36' fill='#5a4636' {FS}>GOOD MONEY IS...</text>
<text x='60' y='165' font-size='54' fill='#1a1410' {F}>DURABLE</text><text x='440' y='165' font-size='48' fill='#1a1410' {F}>EASY TO CARRY</text>
<text x='60' y='270' font-size='54' fill='#1a1410' {F}>SPLITTABLE</text><text x='440' y='270' font-size='48' fill='#d98a1a' {F}>HARD TO FAKE</text>""")
scene("Shells. Salt. Cattle. And eventually... metal.",
      [plate("market_mid", blur=9, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.2}]),
       pop("shell", 0.2, 0.45, 0.13, 0.2), txt("SHELLS", 0.68, 64, x=0.2, enter="pop", at=0.3),
       pop("salt", 0.4, 0.45, 0.1, 0.8), txt("SALT", 0.68, 64, x=0.4, enter="pop", at=0.9),
       txt("CATTLE", 0.47, 64, x=0.6, enter="pop", at=1.4, color="accent2"),
       pop("coin", 0.8, 0.45, 0.14, 2.3, loop="float", loop_amp=0.6), txt("*METAL*", 0.68, 72, x=0.8, enter="pop", at=2.4, sfx="ding")],
      transition="cut")
scene("Good money has to last, be easy to carry, split into small amounts, and be hard to fake. Metal ticks every box.",
      talk("market_close", [["explain", 0], ["point", 3.4]], top=[panel(traits, 0.68, 0.36, 0.44, 0.5)]),
      transition="cut")
scene("Around 600 BC, the kingdom of Lydia, in today's Turkey, began stamping gold and silver into coins.",
      [plate("market_close", blur=10, keys=[{"t": 0, "scale": 1.2}]),
       sprite("coin", 0.68, 0.45, 0.24, enter="zoom", at=0.2, keys=[{"t": 0, "sx": 1}, {"t": 0.4, "sx": -1}, {"t": 0.8, "sx": 1},
              {"t": 1.2, "sx": -1}, {"t": 1.6, "sx": 1, "ease": "out"}], sfx="ding"),
       txt("LYDIA, *~600 BC*", 0.13, 92, x=0.68, max_w=0.5, enter="pop", at=0.5),
       close_ved([["explain", 0], ["point", 2.4]], x=0.25)],
      transition="cut")
scene("A coin of known weight meant no more arguing over every nugget. Prices could finally be counted.",
      staged("market_close",
             behind=[person("market_close", "seller", 0.3, 0.85, [["take", 0], ["happy", 1.6]])],
             top=[sprite("tag_1", 0.75, 0.48, 0.13, rot=-6), fly("coin", 0.1, 0.72, 0.4, 0.52, 0.06, 0.6, dur=0.7),
                  txt("PRICE = *COUNTED*", 0.13, 88, enter="pop", at=2.6, sfx="pop")]),
      transition="cut")

# =================================================================== 4. Paper promises
chapter("Paper promises")
mer = person("goldsmith_wide", "merchant", -0.6, -0.5, [["hold", 0], ["give", 3.4]], walk=[(0, -3.4, -1.0), (2.2, -0.6, -0.5)])
scene("But coins are heavy, and easy to steal. In 1600s London, merchants left their gold with goldsmiths, who had strong vaults.",
      staged("goldsmith_wide",
             behind=[person("goldsmith_wide", "goldsmith", 0.7, 1.55, [["idle", 0], ["wave", 2.0], ["take", 3.6]])],
             front=[mer, ved("goldsmith_wide", 2.2, -1.2, [["explain", 0], ["point", 4.4]])],
             top=[held("coinstack", mer, 0.045, dy=-0.05, dx=0.03),
                  txt("LONDON, *1600s*", 0.12, 92, enter="pop", at=1.0, sfx="ding")]),
      transition="fade")
scene("The goldsmith handed back a receipt: a written promise to return the gold.",
      staged("goldsmith_mid",
             behind=[person("goldsmith_mid", "goldsmith", 0.8, 1.45, [["give", 0], ["point", 1.8]])],
             front=[person("goldsmith_mid", "merchant", -0.3, -0.2, [["take", 0], ["happy", 1.6]])],
             top=[sprite("receipt", 0.7, 0.3, 0.3, enter="zoom", at=0.8, sfx="whoosh", loop="float", loop_amp=0.5)]),
      transition="cut")
scene("Soon people stopped fetching the gold at all. They just traded the receipts. Paper money had arrived in Europe.",
      staged("goldsmith_wide",
             behind=[person("goldsmith_wide", "goldsmith", 0.7, 1.55, [["happy", 0]])],
             front=[person("goldsmith_wide", "merchant", -2.0, -0.8, [["give", 0], ["happy", 2.0]]),
                    person("goldsmith_wide", "lady", -0.4, -1.2, [["take", 0], ["give", 2.4]]),
                    person("goldsmith_wide", "ravi", 1.4, -0.9, [["take", 2.4], ["happy", 3.4]])],
             top=[fly("receipt_small", 0.27, 0.62, 0.43, 0.6, 0.06, 0.6, dur=0.8, rot1=30),
                  fly("receipt_small", 0.45, 0.6, 0.62, 0.6, 0.06, 2.6, dur=0.8, rot1=-30),
                  txt("RECEIPTS *=* MONEY", 0.12, 92, enter="pop", at=4.0, sfx="ding")]),
      transition="cut")
scene("China actually got there first. Its Song dynasty government was issuing paper notes in the 1020s.",
      talk("goldsmith_mid", [["point", 0], ["smirk", 2.2]],
           top=[txt("CHINA, *1020s*", 0.3, 100, x=0.68, enter="pop", at=0.6, sfx="ding"),
                txt("THE FIRST GOVERNMENT PAPER MONEY", 0.45, 52, x=0.68, max_w=0.45, enter="pop", at=1.6, font="body")]),
      transition="cut")
scene("And the goldsmiths noticed something. Only a few owners ever came back for their gold at the same time.",
      staged("goldsmith_mid",
             behind=[person("goldsmith_mid", "goldsmith", 0.8, 1.45, [["idle", 0], ["point", 2.4]])],
             front=[person("goldsmith_mid", "lady", -0.4, -0.4, [["take", 0]], walk=[(0, -0.4, -0.4), (2.4, -2.8, -1.4)])],
             top=[txt("ONLY *A FEW* COME BACK", 0.12, 88, enter="pop", at=3.0)]),
      transition="cut")
beat("goldsmith_mid", "side_eye", "The goldsmith, lending\nyour gold out:\n*\"They don't know.\"*")
scene("So they lent some of it out, and wrote more receipts than they had gold. More paper than metal. That was the seed of modern banking.",
      staged("goldsmith_wide",
             behind=[person("goldsmith_wide", "goldsmith", 0.7, 1.55, [["give", 0], ["happy", 2.4]])],
             front=[person("goldsmith_wide", "omar", -1.4, -0.9, [["take", 0.6], ["happy", 1.6]]),
                    ved("goldsmith_wide", 2.2, -1.2, [["serious", 0], ["explain", 3.0]])],
             top=[fly("receipt_small", 0.5, 0.5, 0.3, 0.62, 0.06, 0.5, dur=0.7),
                  fly("receipt_small", 0.5, 0.5, 0.25, 0.6, 0.06, 1.0, dur=0.7),
                  txt("PAPER *>* GOLD", 0.12, 100, enter="pop", at=2.6, sfx="boom")]),
      transition="cut")

# =================================================================== 5. Fiat
chapter("Money with nothing behind it")
scene("For a long time, many countries promised their paper could be swapped for gold.",
      staged("bank",
             front=[person("bank", "banker", -1.6, -1.9, [["idle", 0], ["explain", 1.4]]),
                    ved("bank", 1.7, -2.9, [["explain", 0]], walk=[(0, 4.4, -3.2), (1.2, 1.7, -2.9)])],
             top=[pop("bill", 0.38, 0.45, 0.12, 0.8), txt("=", 0.45, 110, x=0.5, enter="pop", at=1.3),
                  pop("goldbar", 0.62, 0.45, 0.14, 1.6, sfx="ding")]),
      transition="slide_left")
scene("Then on August 15th, 1971, US President Richard Nixon stopped letting other countries trade their dollars for gold.",
      staged("bank",
             front=[person("bank", "banker", -1.6, -1.9, [["surprised", 2.8]]),
                    ved("bank", 1.7, -2.9, [["point", 0], ["serious", 3.0]])],
             top=[sprite("bill", 0.38, 0.45, 0.12), txt("=", 0.45, 110, x=0.5, until=3.6, exit="fade"),
                  sprite("goldbar", 0.62, 0.45, 0.14, until=3.6, exit="fade",
                         keys=[{"t": 3.0, "y": 0.45}, {"t": 3.6, "y": 1.2, "ease": "in"}]),
                  txt("AUG 15, *1971*", 0.26, 100, enter="pop", at=0.6, sfx="ding")]),
      transition="cut", camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.45], "punch": [3.4]})
beat("bank", "deadpan", "He called it *temporary.*\nThat was 55 years ago.")
scene("Today, most money isn't backed by anything you can hold. Economists call it fiat money. It's worth whatever people believe it can buy.",
      talk("bank", [["explain", 0], ["shrug", 2.6]],
           top=[txt("*FIAT* MONEY", 0.3, 120, x=0.68, enter="zoom", at=2.6, sfx="boom"),
                txt("backed by nothing you can hold", 0.45, 50, x=0.68, max_w=0.45, enter="pop", at=3.2, font="body")]),
      transition="cut")
three = card(860, 420, f"""
<text x='60' y='78' font-size='36' fill='#5a4636' {FS}>WHY PAPER STILL WORKS</text>
<circle cx='95' cy='160' r='34' fill='#f2b04a'/><text x='95' y='176' font-size='46' text-anchor='middle' fill='#1a1410' {AN}>1</text>
<text x='160' y='176' font-size='50' fill='#1a1410' {F}>TAXES are paid in it</text>
<circle cx='95' cy='262' r='34' fill='#6fc3c0'/><text x='95' y='278' font-size='46' text-anchor='middle' fill='#1a1410' {AN}>2</text>
<text x='160' y='278' font-size='50' fill='#1a1410' {F}>The LAW says take it</text>
<circle cx='95' cy='364' r='34' fill='#d9534f'/><text x='95' y='380' font-size='46' text-anchor='middle' fill='#f6efe2' {AN}>3</text>
<text x='160' y='380' font-size='50' fill='#1a1410' {F}>We TRUST tomorrow</text>""")
scene("So why does paper still work? First, the government accepts it for taxes, so everyone needs some.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["idle", 0]])],
             front=[ved("market_mid", -1.2, -1.5, [["explain", 0], ["point", 2.6]], walk=[(0, -3.2, -1.9), (1.0, -1.2, -1.5)])],
             top=[panel(three, 0.72, 0.3, 0.42, 1.2)]),
      transition="slide_left")
scene("Second, the law says it must be accepted for debts. And most of all, we trust it will buy about as much tomorrow as it does today.",
      staged("market_close",
             behind=[person("market_close", "seller", 0.3, 0.85, [["take", 0], ["give", 2.0], ["happy", 4.0]])],
             top=[fly("bill", 0.1, 0.72, 0.42, 0.52, 0.12, 0.6, dur=0.7),
                  sprite("apple", 0.47, 0.56, 0.06, at=2.0, keys=[{"t": 0, "x": 0.47, "y": 0.56}, {"t": 0.7, "x": 0.1, "y": 0.72, "ease": "out"}]),
                  txt("*TRUST*", 0.13, 130, enter="zoom", at=4.4, sfx="boom")]),
      transition="cut")

# =================================================================== 6. When trust breaks
chapter("When trust breaks")
vrain = [sprite("bill_100t", random.uniform(0.03, 0.97), 0.0, random.uniform(0.05, 0.08), at=random.uniform(0, 4.5),
                keys=[{"t": 0, "y": -0.1, "rot": random.uniform(0, 360)},
                      {"t": random.uniform(2.5, 3.6), "y": 1.12, "rot": random.uniform(200, 700), "ease": "linear"}], opacity=0.9)
         for _ in range(22)]
scene("Break that trust, and money melts. In the 2000s, Zimbabwe printed money to pay the government's bills.",
      [plate("vault")] + vrain[:12] + [
          sprite("printer", 0.5, 0.52, 0.2, enter="pop", at=0.4, loop="shake", loop_amp=0.5),
          txt("ZIMBABWE", 0.12, 100, enter="pop", at=1.0, sfx="ding"),
          ved("vault", 2.4, -1.4, [["serious", 0], ["point", 3.0]], walk=[(0, 4.8, -1.8), (1.2, 2.4, -1.4)])],
      transition="fade")
for L in S[-1]["layers"]:
    L.pop("_depth", None)
scene("By November 2008, prices were doubling roughly every day. Imagine your savings losing half their value overnight, every night. It printed a one hundred trillion dollar note.",
      [plate("vault")] + vrain + [
          sprite("note_100t", 0.5, 0.4, 0.5, enter="zoom", at=6.4, loop="float", loop_amp=0.8, sfx="boom"),
          {"type": "counter", "from": 1, "to": 100000000000000, "count_dur": 1.8, "at": 6.8, "x": 0.5, "y": 0.12,
           "size": 92, "stroke": "#0b0f12", "stroke_width": 6, "enter": "pop", "prefix": "Z$"},
          txt("PRICES *x2* EVERY DAY", 0.12, 92, enter="pop", at=0.4, until=6.6, exit="fade"),
          ved("vault", 2.4, -1.4, [["serious", 0], ["surprised", 6.4]], hops=[[6.8, 0.05, 0.45]])],
      transition="cut")
for L in S[-1]["layers"]:
    L.pop("_depth", None)
scene("People simply stopped using it. In 2009, the country switched to foreign currencies.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["shrug", 0]])],
             front=[person("market_wide", "tomas", -1.2, -1.8, [["sad", 0]], walk=[(0, -1.2, -1.8), (3.4, -4.6, -2.8)]),
                    person("market_wide", "lena", 1.8, -1.4, [["sad", 0]], walk=[(0, 1.8, -1.4), (3.4, 5.2, -0.9)]),
                    person("market_wide", "amina", -0.6, -1.0, [["sad", 0]]),
                    person("market_wide", "ravi", 2.6, 1.4, [["shrug", 0]]),
                    person("market_wide", "omar", -2.2, 1.0, [["sad", 0]])],
             top=[sprite("note_100t", 0.5, 0.75, 0.16, rot=-12, opacity=0.9),
                  txt("NOBODY *WANTED* IT", 0.12, 92, enter="pop", at=1.2)]),
      transition="cut")
scene("That's why central banks try to keep prices rising slowly and steadily. Many big ones aim for about two percent a year: enough to keep money moving, small enough that you barely notice.",
      talk("market_mid", [["explain", 0], ["crossed", 3.0]], x=0.73,
           top=[txt("SLOW AND *STEADY*", 0.3, 100, x=0.32, max_w=0.5, enter="pop", at=1.8, sfx="ding"),
                txt("~2% A YEAR", 0.45, 72, x=0.32, enter="pop", at=4.6, color="accent2")]),
      transition="cut")

# =================================================================== 7. Where money comes from
chapter("Where money really comes from")
scene("Now, the plot twist. Most money today isn't paper at all.",
      staged("bank",
             front=[person("bank", "banker", -1.6, -1.9, [["idle", 0]]),
                    ved("bank", 0.3, -2.8, [["point", 0], ["smirk", 2.0]], walk=[(0, 3.8, -3.1), (1.2, 0.3, -2.8)], hops=[[1.6, 0.04, 0.45]])],
             top=[txt("*PLOT TWIST*", 0.26, 110, enter="zoom", at=0.3, sfx="boom")]),
      transition="slide_left")
donut = card(760, 420, f"""
<circle cx='200' cy='215' r='130' fill='none' stroke='#6fc3c0' stroke-width='70'/>
<circle cx='200' cy='215' r='130' fill='none' stroke='#f2b04a' stroke-width='72' stroke-dasharray='24.5 792' transform='rotate(-90 200 215)'/>
<text x='200' y='235' font-size='62' text-anchor='middle' fill='#1a1410' {AN}>UK</text>
<text x='400' y='170' font-size='96' fill='#2c8f8a' {AN}>97%</text><text x='400' y='215' font-size='34' fill='#1a1410' {F}>bank deposits</text>
<text x='400' y='320' font-size='96' fill='#d98a1a' {AN}>3%</text><text x='400' y='365' font-size='34' fill='#1a1410' {F}>notes and coins</text>""")
scene("In the UK, about 97 percent of the money people hold is bank deposits. Just numbers in accounts.",
      [plate("bank", blur=9, keys=[{"t": 0, "scale": 1.15}]), close_ved([["explain", 0], ["point", 2.0]], x=0.25),
       panel(donut, 0.68, 0.42, 0.42, 0.6)],
      transition="cut")
acct = card(760, 360, f"""
<text x='60' y='80' font-size='36' fill='#5a4636' {FS}>AMINA'S ACCOUNT</text>
<line x1='60' y1='105' x2='700' y2='105' stroke='#1a1410' stroke-width='3' opacity='0.3'/>
<text x='60' y='190' font-size='44' fill='#1a1410' {F}>Balance</text>
<text x='60' y='290' font-size='44' fill='#1a1410' {F}>Owes the bank</text>""")
scene("And where do those numbers come from? Mostly, from banks making loans.",
      staged("bank_desk",
             behind=[person("bank_desk", "banker", 2.75, 2.3, [["explain", 0], ["point", 2.0]])],
             front=[person("bank_desk", "amina", 1.25, 0.8, [["idle", 0], ["surprised", 2.4]])],
             top=[txt("LOANS *CREATE* MONEY", 0.12, 92, enter="pop", at=2.4, sfx="ding")]),
      transition="cut")
scene("When a bank lends you a thousand, it doesn't hand over someone else's savings. It types a brand new thousand into your account, and writes down that you owe it a thousand. Two numbers, created together.",
      staged("bank_desk",
             behind=[person("bank_desk", "banker", 2.75, 2.3, [["explain", 0], ["give", 3.6]])],
             front=[person("bank_desk", "amina", 1.25, 0.8, [["idle", 0], ["happy", 4.2]], hops=[[4.4, 0.03, 0.45]])],
             top=[panel(acct, 0.27, 0.32, 0.4, 0.4),
                  {"type": "counter", "from": 0, "to": 1000, "count_dur": 1.2, "at": 3.8, "x": 0.40, "y": 0.325, "size": 60,
                   "prefix": "$", "stroke": "#0b0f12", "stroke_width": 5, "enter": "pop", "sfx": "ding"},
                  {"type": "counter", "from": 0, "to": 1000, "count_dur": 1.2, "at": 3.8, "x": 0.40, "y": 0.425, "size": 60,
                   "prefix": "$", "color": "danger", "stroke": "#0b0f12", "stroke_width": 5, "enter": "pop"}]),
      transition="cut")
beat("bank_desk", "deadpan", "Wait, money is just numbers? *Always has been.*")
scene("Pay the loan back, and that money disappears again. The Bank of England explained exactly this in 2014.",
      talk("bank", [["explain", 0], ["point", 3.2]], x=0.73,
           top=[txt("REPAY = MONEY *DISAPPEARS*", 0.3, 84, x=0.32, max_w=0.5, enter="pop", at=1.4, sfx="pop"),
                txt("Bank of England, 2014", 0.45, 46, x=0.32, enter="pop", at=3.6, font="body")]),
      transition="cut")
limits = card(1000, 330, f"""
<text x='60' y='78' font-size='36' fill='#5a4636' {FS}>WHAT KEEPS IT IN CHECK</text>
<text x='60' y='160' font-size='50' fill='#1a1410' {F}>Interest rates</text>
<text x='60' y='230' font-size='50' fill='#1a1410' {F}>Banking rules</text>
<text x='60' y='300' font-size='50' fill='#1a1410' {F}>How much people want to borrow</text>""")
scene("So what stops banks from creating endless money? Interest rates, banking rules, and how much people actually want to borrow. Some economists say banks hold too much of this power. Others say the rules keep it safe. Either way, now you know where the numbers come from.",
      staged("bank",
             front=[person("bank", "banker", -1.6, -1.9, [["shrug", 0], ["explain", 2.4]]),
                    ved("bank", 1.7, -2.9, [["explain", 0], ["point", 2.6]])],
             top=[panel(limits, 0.36, 0.3, 0.46, 2.2)]),
      transition="cut")

# =================================================================== 8. So what is money?
chapter("So, what is money?")
scene("So, back to our island. Money isn't the apples. It's a promise between people, that everyone agrees to keep.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["give", 0], ["happy", 2.4]])],
             front=[person("market_wide", "amina", -0.6, -1.0, [["take", 0], ["happy", 2.0]]),
                    person("market_wide", "tomas", -2.0, -1.8, [["happy", 0]], walk=[(0, -5.0, -2.6), (2.6, -2.0, -1.8)]),
                    person("market_wide", "lena", 2.0, -1.4, [["happy", 0]], walk=[(0, 5.0, -1.0), (2.6, 2.0, -1.4)]),
                    person("market_wide", "omar", -2.2, 1.0, [["wave", 0]]),
                    person("market_wide", "ravi", 2.6, 1.4, [["happy", 0]]),
                    ved("market_wide", 0.9, -3.0, [["warm", 0], ["explain", 2.2]])],
             top=[txt("MONEY = A *PROMISE*", 0.12, 100, enter="pop", at=3.4, sfx="ding")]),
      transition="slide_left", camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.52]})
scene("That piece of paper works because we all believe that tomorrow, someone else will take it too.",
      staged("market_close",
             behind=[person("market_close", "seller", 0.3, 0.85, [["take", 0], ["give", 1.6], ["happy", 3.0]])],
             top=[fly("bill", 0.1, 0.72, 0.42, 0.52, 0.12, 0.4, dur=0.7),
                  sprite("apple", 0.47, 0.56, 0.06, at=1.6, keys=[{"t": 0, "x": 0.47, "y": 0.56}, {"t": 0.7, "x": 0.1, "y": 0.72, "ease": "out"}])]),
      transition="cut")
scene("Money is trust you can carry. Next time you tap your card, remember: you're moving a promise. And now you know how money actually works.",
      talk("market_mid", [["warm", 0], ["crossed", 2.4]],
           top=[txt("MONEY IS *TRUST* YOU CAN CARRY", 0.3, 92, x=0.68, max_w=0.5, enter="pop", at=0.6, sfx="ding")]),
      transition="cut")

scene("If money finally clicked, subscribe. Every week, one big idea, made simple.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["wave", 0]])],
             front=[person("market_mid", "amina", -0.9, -0.9, [["wave", 0.4]]),
                    ved("market_mid", 0.6, -1.4, [["welcome", 0], ["warm", 2.0]], hops=[[0.3, 0.03, 0.45]])],
             top=[txt("*SUBSCRIBE*", 0.12, 110, enter="zoom", at=0.5, sfx="ding"),
                  txt("ONE BIG IDEA, EVERY WEEK", 0.22, 60, enter="pop", at=2.0, font="body")]),
      transition="cut")

job = {"id": "2026-11-11-longpilot", "kind": "long",
       "title": "How Money Actually Works (From Barter to Bank Loans)",
       "description": "Why will a stranger hand you real apples for a piece of paper? Professor Ved builds money from scratch on a tiny "
                      "island: barter (and why no pure barter economy has ever been found), the first coins, goldsmith receipts, the end of gold in 1971, "
                      "Zimbabwe's 100 trillion dollar note, and the plot twist: most money today is created when banks make loans.\n\n"
                      "Sources: Bank of England Quarterly Bulletin 2014 Q1 (Money in the modern economy; Money creation in the modern economy); "
                      "Federal Reserve History, Nixon Ends Convertibility of U.S. Dollars to Gold (1971); Hanke & Kwok, Cato Journal (2009) on "
                      "Zimbabwe's hyperinflation; Caroline Humphrey, Barter and Economic Disintegration (1985); Herodotus, Histories 1.94.",
       "tags": ["how money works", "money explained", "economics", "inflation", "banks create money", "fiat money", "gold standard",
                "barter", "history of money", "zimbabwe", "nixon shock", "explained", "education"],
       "chapters": CH,
       "thumbnail": {
           "title": "JUST *PAPER?*", "title_y": 0.14, "title_size": 220, "glow": "#f2b04a", "glow_x": 0.45, "glow_y": 0.58, "blur": 16,
           "glow_strength": 1.6, "bg_saturation": 1.8, "bg_brightness": 0.9,
           "tint": ["#2a5bd7", "#f08a24"], "tint_amount": 0.45,
           "bg": staged("market_mid",
                        behind=[person("market_mid", "seller", 0.35, 0.8, [["surprised", 0]])],
                        front=[person("market_mid", "amina", -1.2, -0.6, [["surprised", 0]]),
                               person("market_mid", "tomas", 1.6, -0.4, [["take", 0]])]),
           "fg": [sprite("apple", 0.15, 0.66, 0.15, rot=-8),
                  dict(close_ved([["surprised", 0]], x=0.43), y=1.2, h=1.7, acting="none", talk=False),
                  sprite("bill", 0.77, 0.6, 0.38, rot=-14)]},
       "meta": {"format": "deep-dive", "topic": "how money works: barter, coins, receipts, fiat, hyperinflation, bank money",
                "hook": "question", "idea_source": "owner (manual): first long video", "characters": ["ved", "extra"],
                "sources": ["https://www.bankofengland.co.uk/-/media/boe/files/quarterly-bulletin/2014/quarterly-bulletin-2014-q1",
                            "https://www.federalreservehistory.org/essays/gold-convertibility-ends",
                            "https://clips.cato.org/sites/default/files/Hanke_bulawayo_inflation.pdf",
                            "https://en.wikipedia.org/wiki/Barter",
                            "https://en.wikipedia.org/wiki/Goldsmith_banker",
                            "https://www.thecollector.com/paper-money-history-develop-premodern-world/"],
                "humour": {"trend": "'They don't know' (rising Nov 2026), 'Always Has Been' (rising on Imgflip), plus a timeless dry 'temporary' line",
                           "beat": "side_eye, deadpan, deadpan", "scene": [n for n, s in enumerate(S) if s.get("beat")]},
                "overrides": "pilot: first long-form (16:9) Deep Dive"},
       "privacy": "private", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "chapters", len(CH), "words", sum(len(s.get("say", "").split()) for s in S), "using", SRC)
