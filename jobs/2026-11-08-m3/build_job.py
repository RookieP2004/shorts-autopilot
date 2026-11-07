"""v3: "Why can't we just print more money?" with a living town.
2D Ved + faceless townspeople staged in depth inside Blender sets (stills + cut-outs), placed by floor position (autopilot.stage).
Run after the assets exist (or with /tmp previews for planning): python jobs/2026-11-08-m3/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(11)
J = "jobs/2026-11-08-m3/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_market_mid.json") else "/tmp/m3pv/"
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("market_wide", "market_mid", "market_close", "bank", "vault")}

# ---- the town (same people in every shot)
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
}


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
    """A townsperson standing at floor point (wx, wy) on set_. walk = [(t, wx, wy), ...] path (ends anywhere)."""
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


def staged(set_, behind=(), front=(), extra_top=()):
    """Plate, characters behind the counter, the counter foreground layer, then everyone in front (far to near)."""
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if set_.startswith("market"):
        out.append(fg(set_))
    out += sorted(front, key=lambda L: -L["_depth"])
    out += list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def drop(name, x, y, w, t0, fall=0.55, from_y=-0.15, spin=0, **k):
    return sprite(name, x, y, w, at=t0, keys=[{"t": 0, "y": from_y, "rot": spin}, {"t": fall, "y": y, "rot": 0, "ease": "bounce"}], **k)


def fly(name, x0, y0, x1, y1, w, t0, dur=0.9, rot0=0, rot1=200, arc=0.12, **k):
    xm, ym = (x0 + x1) / 2, min(y0, y1) - arc
    return sprite(name, x0, y0, w, at=t0, until=t0 + dur, exit="fade", exit_dur=0.1,
                  keys=[{"t": 0, "x": x0, "y": y0, "rot": rot0, "scale": 0.4},
                        {"t": dur * 0.45, "x": xm, "y": ym, "rot": (rot0 + rot1) / 2, "scale": 1.0, "ease": "out"},
                        {"t": dur, "x": x1, "y": y1, "rot": rot1, "scale": 1.1, "ease": "in"}], **k)


S = []
# 1. hook (medium): the seller at his stall, Amina waiting; Ved walks in and asks
S.append({"say": "Hey! Ever wondered why a country can't just *print more money*?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.07, "focus": [0.55, 0.5]}]},
          "layers": staged("market_mid",
                           behind=[person("market_mid", "seller", 0.3, 0.8, [["idle", 0], ["wave", 1.4], ["idle", 2.6]])],
                           front=[person("market_mid", "amina", -0.62, -0.85, [["idle", 0], ["hold", 1.0]]),
                                  ved("market_mid", 0.55, -1.55, [["warm", 0], ["explain", 1.3], ["point", 2.5]],
                                      walk=[(0, 2.2, -1.9), (1.2, 0.55, -1.55)])],
                           extra_top=[txt("WHY NOT JUST *PRINT MORE MONEY?*", 0.15, 92, enter="none")])})
# 2. close-up on Ved
S.append({"say": "Free money for everyone, right?", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("market_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.5, "scale": 1.4}]),
                     close_ved([["welcome", 0], ["smirk", 1.2]])]})
# 3. wide: the tiny island, people strolling
S.append({"say": "Picture a tiny island. It has *ten apples*, and *ten dollars* in total.", "transition": "slide_left",
          "camera": {"zoom": [1.0, 1.05], "focus": [0.5, 0.52]},
          "layers": staged("market_wide",
                           behind=[person("market_wide", "seller", 0.25, 0.8, [["idle", 0], ["explain", 2.0]])],
                           front=[person("market_wide", "tomas", -2.6, -2.8, [["idle", 0]], walk=[(0, -3.4, -3.2), (3.0, -1.4, -1.9)]),
                                  person("market_wide", "lena", 2.6, -1.0, [["idle", 0]], walk=[(0, 3.6, -0.6), (2.6, 1.7, -1.4)]),
                                  person("market_wide", "omar", -1.9, 0.9, [["hold", 0]]),
                                  person("market_wide", "ravi", 2.4, 1.6, [["idle", 0], ["explain", 1.8]]),
                                  person("market_wide", "amina", -0.6, -1.0, [["hold", 0]])],
                           extra_top=[txt("10 APPLES", 0.12, 110, enter="pop", at=1.3, sfx="ding"),
                                      txt("*$10* IN TOTAL", 0.2, 88, enter="pop", at=2.6, sfx="pop")])})
# 4. close on the counter: Amina pays $1, gets an apple
stc = ST["market_close"]
sel = stc.place(0.25, 0.85, "extra")
bx, by = 0.16, 0.64
S.append({"say": "So one apple costs *one dollar*.", "transition": "cut", "caption_y": 0.27,
          "layers": staged("market_close",
                           behind=[person("market_close", "seller", 0.25, 0.85, [["idle", 0], ["take", 0.7], ["give", 1.5]])],
                           front=[],
                           extra_top=[sprite("tag_1", 0.73, 0.5, 0.2, rot=-6),
                                      fly("bill", bx, by, sel["x"] - 0.1, 0.5, 0.18, 0.4, dur=0.6, rot0=-10, rot1=10, arc=0.06),
                                      sprite("apple", 0.55, 0.52, 0.12, at=1.5, keys=[{"t": 0, "x": 0.55, "y": 0.52},
                                             {"t": 0.6, "x": 0.12, "y": 0.66, "ease": "out"}])])})
# 5. bank: the banker presses print; Ved walks in and jumps
stb = ST["bank"]
pr_x, pr_y = stb.point(0.2, 1.0, 0.55)
bills = [fly("bill", pr_x, pr_y + 0.02, random.uniform(0.1, 0.95), random.uniform(1.05, 1.15), 0.17, 1.3 + k * 0.15,
             dur=random.uniform(0.8, 1.1), rot0=random.uniform(-30, 30), rot1=random.uniform(-260, 260), arc=random.uniform(0.15, 0.3))
         for k in range(14)]
pw = abs(stb.point(1.05, 1.0, 0.5)[0] - stb.point(-0.65, 1.0, 0.5)[0]) * 1.12
S.append({"say": "Now the government prints ten more dollars, and hands them out.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 1.4, "zoom": 1.08, "focus": [0.5, 0.5]}]},
          "layers": [plate("bank"),
                     person("bank", "banker", 1.6, 1.2, [["idle", 0], ["point", 0.8], ["cheer", 1.6]]),
                     sprite("printer", pr_x, pr_y, pw, loop="shake", loop_amp=0.5)] + bills + [
                     txt("*+$10* PRINTED", 0.29, 96, enter="pop", at=1.3, sfx="boom"),
                     ved("bank", -1.6, -1.2, [["warm", 0], ["point", 1.2], ["surprised", 1.6]],
                         walk=[(0, -3.6, -1.6), (1.0, -1.6, -1.2)], hops=[[1.5, 0.05, 0.45]])]})
for L in S[-1]["layers"]:
    L.pop("_depth", None)
# 6. wide: money rains, everyone cheers
rain = [sprite("bill", random.uniform(0.05, 0.95), 0.0, random.uniform(0.07, 0.11), at=random.uniform(0, 2.4),
               keys=[{"t": 0, "y": -0.06, "rot": random.uniform(0, 360)},
                     {"t": random.uniform(1.6, 2.4), "y": random.uniform(0.62, 0.72), "rot": random.uniform(200, 600), "ease": "out"}],
               until=4.6, exit="fade") for _ in range(26)]
S.append({"say": "Everyone feels richer! Twice the money...", "transition": "zoom",
          "layers": staged("market_wide",
                           behind=[person("market_wide", "seller", 0.25, 0.8, [["surprised", 0], ["happy", 1.0]])],
                           front=[person("market_wide", "tomas", -1.4, -1.9, [["happy", 0], ["cheer", 1.2]], hops=[[0.4, 0.03, 0.45], [1.5, 0.03, 0.45]]),
                                  person("market_wide", "lena", 1.7, -1.4, [["cheer", 0], ["happy", 1.0]], hops=[[0.8, 0.03, 0.45]]),
                                  person("market_wide", "omar", -1.9, 0.9, [["happy", 0]], hops=[[1.1, 0.025, 0.45]]),
                                  person("market_wide", "ravi", 2.4, 1.6, [["cheer", 0]], hops=[[0.3, 0.025, 0.45], [1.6, 0.025, 0.45]]),
                                  person("market_wide", "amina", -0.6, -1.0, [["happy", 0], ["cheer", 1.4]], hops=[[1.9, 0.03, 0.45]]),
                                  ved("market_wide", 0.6, -2.6, [["welcome", 0], ["warm", 1.6]])],
                           extra_top=rain + [txt("*2x* THE MONEY", 0.13, 110, enter="pop", at=0.6, sfx="ding")])})
# 7. medium: they all rush to the stall; still ten apples
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
panel = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 330'><rect width='900' height='330' rx='34' fill='#f6efe2'/>
<rect width='900' height='330' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>
<g transform='translate(70,70)'><rect width='120' height='62' rx='8' fill='#cfe3c6' stroke='#265c40' stroke-width='5'/><circle cx='60' cy='31' r='16' fill='none' stroke='#265c40' stroke-width='5'/></g>
<text x='230' y='120' font-size='60' fill='#1a1410' {F}>MONEY</text><text x='500' y='122' font-size='74' fill='#1a1410' {AN}>$10</text>
<path d='M615,100 L660,100 L660,86 L685,108 L660,130 L660,116 L615,116 Z' fill='#f2b04a'/><text x='705' y='122' font-size='74' fill='#d98a1a' {AN}>$20</text>
<line x1='60' y1='168' x2='840' y2='168' stroke='#1a1410' stroke-width='3' opacity='0.25'/>
<g transform='translate(100,205)'><circle cx='30' cy='42' r='38' fill='#c0212a'/><path d='M30,6 C28,-6 34,-14 40,-16' stroke='#4a3220' stroke-width='6' fill='none' stroke-linecap='round'/><ellipse cx='50' cy='-4' rx='18' ry='8' fill='#3f8a3a'/></g>
<text x='230' y='268' font-size='60' fill='#1a1410' {F}>APPLES</text><text x='515' y='270' font-size='74' fill='#1a1410' {AN}>10</text>
<path d='M615,248 L660,248 L660,234 L685,256 L660,278 L660,264 L615,264 Z' fill='#9aa3ab'/><text x='720' y='270' font-size='74' fill='#1a1410' {AN}>10</text></svg>"""
S.append({"say": "...but there are still only *ten apples*.", "transition": "cut",
          "layers": staged("market_mid",
                           behind=[person("market_mid", "seller", 0.3, 0.8, [["surprised", 0], ["shrug", 1.3]])],
                           front=[person("market_mid", "tomas", -0.75, -0.9, [["happy", 0]], walk=[(0, -2.6, -1.4), (0.9, -0.75, -0.9)]),
                                  person("market_mid", "lena", 0.45, -0.95, [["happy", 0]], walk=[(0, 2.4, -1.2), (1.0, 0.45, -0.95)]),
                                  person("market_mid", "amina", -0.15, -1.25, [["cheer", 0]], walk=[(0, -1.8, -2.4), (0.8, -0.15, -1.25)])],
                           extra_top=[{"type": "image", "svg": panel, "w": 0.82, "x": 0.5, "y": 0.17, "enter": "pop", "at": 0.7, "sfx": "pop"}])})
# 8. close: the seller flips the tag to $2; Amina's hope sinks
S.append({"say": "So the seller raises the price. Each apple now costs *two dollars*. That's *inflation*.", "transition": "cut",
          "caption_y": 0.27, "camera": {"zoom": [1.0, 1.06], "focus": [0.5, 0.5], "punch": [4.3]},
          "layers": staged("market_close",
                           behind=[person("market_close", "seller", 0.25, 0.85, [["shrug", 0], ["point", 1.8], ["shrug", 3.2]])],
                           front=[],
                           extra_top=[
                               sprite("tag_1", 0.73, 0.5, 0.2, keys=[{"t": 0, "sx": 1, "rot": -6}, {"t": 2.3, "sx": 1, "rot": -6},
                                      {"t": 2.5, "sx": 0.0, "rot": 0, "ease": "in"}], until=2.5, exit_dur=0.01),
                               sprite("tag_2", 0.73, 0.5, 0.2, at=2.5, keys=[{"t": 0, "sx": 0.0, "scale": 1.25}, {"t": 0.22, "sx": 1.0, "scale": 1.25, "ease": "out"},
                                      {"t": 0.6, "sx": 1.0, "scale": 1.0, "ease": "back"}], sfx="whoosh"),
                               txt("*INFLATION*", 0.13, 150, enter="zoom", at=4.2, sfx="boom")])})
# 9. wide: nobody got richer; everyone walks off, slumped
S.append({"say": "Nobody got richer. Prices just went up.", "transition": "cut",
          "camera": {"zoom": [1.05, 1.0], "focus": [0.5, 0.52]},
          "layers": staged("market_wide",
                           behind=[person("market_wide", "seller", 0.25, 0.8, [["shrug", 0], ["idle", 1.8]])],
                           front=[person("market_wide", "tomas", -1.4, -1.9, [["sad", 0]], walk=[(0, -1.4, -1.9), (3.0, -3.6, -2.9)]),
                                  person("market_wide", "lena", 1.7, -1.4, [["sad", 0]], walk=[(0, 1.7, -1.4), (3.0, 3.7, -0.8)]),
                                  person("market_wide", "amina", -0.6, -1.0, [["sad", 0]]),
                                  person("market_wide", "ravi", 2.4, 1.6, [["sad", 0]]),
                                  person("market_wide", "omar", -1.9, 0.9, [["sad", 0]]),
                                  ved("market_wide", 0.6, -2.6, [["shrug", 0], ["serious", 1.6]])],
                           extra_top=[txt("SAME APPLES. *HIGHER PRICES.*", 0.14, 88, enter="pop", at=0.4, sfx="pop")])})
for L in S[-1]["layers"]:
    if L.get("id") == "ved":
        L["acting"] = [["surprised", 0], ["serious", 1.6]]
# 10. comic beat
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("market_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["idle", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.5, "zoom": 1.15, "focus": [0.5, 0.42],
                   "text": "The printer: \"I'm the birthday.\"\nPrices: *\"Me too.\"*", "text_y": 0.18}})
# 11. vault: Zimbabwe; Omar hauls a stack of notes; notes rain
stv = ST["vault"]
vrain = [sprite("bill_100t", random.uniform(0.05, 0.95), 0.0, random.uniform(0.08, 0.13), at=random.uniform(0, 3.5),
                keys=[{"t": 0, "y": -0.08, "rot": random.uniform(0, 360)},
                      {"t": random.uniform(2.5, 3.6), "y": 1.1, "rot": random.uniform(200, 700), "ease": "linear"}], opacity=0.9)
         for _ in range(16)]
omar = person("vault", "omar", -1.6, -0.6, [["hold", 0]], walk=[(0, -3.6, -0.3), (4.6, -0.3, -0.8)])
S.append({"say": "Zimbabwe actually tried this. In 2008, prices *doubled* about every single day...", "transition": "fade",
          "caption_y": 0.6,
          "layers": [plate("vault")] + vrain + [
              sprite("note_100t", 0.5, 0.33, 0.86, enter="zoom", at=0.2, loop="float", loop_amp=0.8),
              omar,
              txt("ZIMBABWE, 2008", 0.11, 100, enter="pop", at=0.3, sfx="pop"),
              ved("vault", 1.15, -1.3, [["warm", 0], ["explain", 1.6], ["serious", 3.4]], walk=[(0, 3.4, -1.6), (1.3, 1.15, -1.3)])]})
for L in S[-1]["layers"]:
    L.pop("_depth", None)
# a stack of cash travels in Omar's arms
S[-1]["layers"].insert(S[-1]["layers"].index(omar) + 1,
    sprite("stack10", omar["keys"][0]["x"], omar["keys"][0]["y"] - 0.02, 0.17,
           keys=[{"t": k["t"], "x": k["x"], "y": k["y"] - 0.02 * k["scale"], "scale": k["scale"], **({"walk": True} if k.get("walk") else {})}
                 for k in omar["keys"]]))
# 12. closer on the note: Ved jumps back
S.append({"say": "...and it printed a *one hundred trillion* dollar note.", "transition": "cut", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.15, "focus": [0.5, 0.36]}, {"t": 3.0, "zoom": 1.3, "focus": [0.46, 0.35]}]},
          "layers": [plate("vault")] + vrain[:8] + [
              sprite("note_100t", 0.5, 0.33, 0.86, loop="float", loop_amp=0.8),
              {"type": "counter", "from": 1, "to": 100000000000000, "count_dur": 1.6, "at": 0.9, "x": 0.5, "y": 0.12,
               "size": 92, "stroke": "#0b0f12", "stroke_width": 6, "enter": "pop"},
              ved("vault", 1.15, -1.3, [["surprised", 0]], hops=[[1.0, 0.05, 0.45]])]})
for L in S[-1]["layers"]:
    L.pop("_depth", None)
# 13. medium: back at the stall, the lesson
S.append({"say": "See, money isn't wealth. It's a *ticket* for the stuff we make.", "transition": "slide_left",
          "layers": staged("market_mid",
                           behind=[person("market_mid", "seller", 0.3, 0.8, [["idle", 0], ["hold", 2.2]])],
                           front=[ved("market_mid", -0.65, -1.4, [["explain", 0], ["point", 1.8], ["warm", 3.2]],
                                      walk=[(0, -2.2, -1.8), (0.9, -0.65, -1.4)])],
                           extra_top=[txt("MONEY = A *TICKET*", 0.13, 104, enter="pop", at=1.6, sfx="pop"),
                                      txt("NOT THE *STUFF*", 0.22, 88, enter="pop", at=2.9)])})
# 14. close: payoff
S.append({"say": "Print more tickets... and each one *buys less*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("market_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3, "scale": 1.4}]),
                     close_ved([["explain", 0], ["crossed", 1.9]])]})

job = {"id": "2026-11-08-m3", "title": "Why can't we just print more money? 💸",
       "description": "Ten apples, ten dollars, and a money printer: the simplest way to understand inflation, and what happened when Zimbabwe tried it.\n\nSources: Hanke & Kwok, Cato Journal (2009); Reserve Bank of Zimbabwe Z$100 trillion note, Jan 2009.",
       "tags": ["inflation", "economics", "money", "print money", "zimbabwe", "hyperinflation", "explained", "economy"],
       "hashtags": ["#economics", "#inflation"],
       "meta": {"format": "big-question", "topic": "why printing money causes inflation", "hook": "question",
                "idea_source": "owner (manual)", "characters": ["ved", "extra"],
                "sources": ["https://www.cato.org/publications/commentary/inflation-inferno-roared-away-until-mid-november-2008"],
                "humour": {"trend": "'you the birthday' (TikTok slang, this week)", "beat": "deadpan", "scene": 9},
                "overrides": "style test v3: living town (faceless townspeople), depth staging, smoother stall/apples"},
       "privacy": "private", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
