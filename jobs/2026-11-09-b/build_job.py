"""2026-11-09-b: "Why does the bank pay YOU interest?" (big-question).
2D Ved + townspeople staged in depth inside Blender sets (town bank hall, vault, bakery street) built from stills + cut-outs.
Run after the assets exist (or with previews for planning): python jobs/2026-11-09-b/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(9)
ID = "2026-11-09-b"
J = f"jobs/{ID}/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_bank_mid.json") else "/tmp/claude-0/pv/"
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("bank_wide", "bank_mid", "bank_vault", "bakery_wide", "bakery_mid")}

# ---- the town (same people, same outfits in every shot)
OUT = {
    "amina": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "necklace": "#6fc3c0",
              "earrings": "#f2b04a", "bag": "#8a5a3c", "hair": ["#140f0c", "long"]},
    "ravi": {"skin": "#b97a55", "hat": ["cap", "#f6efe2"], "top": ["#7c2533", "kurta"], "apron": "#f6efe2",
             "bottom": ["#efe3c8", "trousers"], "hair": ["#2a2320", "curly"], "build": "round"},
    "banker": {"skin": "#f0c8a8", "hat": ["bowler", "#25262b"], "top": ["#34425c", "jacket"], "tie": "#c0392b",
               "bottom": ["#25262b", "trousers"], "belt": "#1a1a1a"},
    "tomas": {"skin": "#e2b48d", "hat": ["straw", "#e6c27a"], "top": ["#6fc3c0", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "lena": {"skin": "#e6b996", "top": ["#9b59b6", "dress"], "hair": ["#6b4423", "bun"], "earrings": "#f2b04a", "bag": "#d9534f"},
    "omar": {"skin": "#a0694a", "hat": ["fez", "#b03a2e"], "top": ["#f6efe2", "vest"], "bottom": ["#5a4636", "trousers"], "build": "round"},
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


def drop(name, x, y, w, t0, fall=0.55, from_y=-0.15, spin=0, **k):
    return sprite(name, x, y, w, at=t0, keys=[{"t": 0, "y": from_y, "rot": spin}, {"t": fall, "y": y, "rot": 0, "ease": "bounce"}], **k)


def fly(name, x0, y0, x1, y1, w, t0, dur=0.9, rot0=0, rot1=200, arc=0.12, **k):
    xm, ym = (x0 + x1) / 2, min(y0, y1) - arc
    return sprite(name, x0, y0, w, at=t0, until=t0 + dur, exit="fade", exit_dur=0.1,
                  keys=[{"t": 0, "x": x0, "y": y0, "rot": rot0, "scale": 0.5},
                        {"t": dur * 0.45, "x": xm, "y": ym, "rot": (rot0 + rot1) / 2, "scale": 1.0, "ease": "out"},
                        {"t": dur, "x": x1, "y": y1, "rot": rot1, "scale": 1.0, "ease": "in"}], **k)


def coins(x0, y0, x1, y1, t0, n=6, w=0.06, gap=0.09, **k):
    return [fly("coin", x0 + random.uniform(-0.02, 0.02), y0, x1 + random.uniform(-0.03, 0.03), y1, w, t0 + i * gap,
                dur=random.uniform(0.6, 0.8), rot0=random.uniform(-40, 40), rot1=random.uniform(-200, 200),
                arc=random.uniform(0.08, 0.16), **k) for i in range(n)]


def badge(word, color="#1a1410", w=560):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 150'><rect x='6' y='6' width='{w-12}' height='138' rx='26' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/><text x='{w/2}' y='112' text-anchor='middle' font-size='96' "
            f"fill='{color}' {AN}>{word}</text></svg>")


ICON = {
    "loaf": "<ellipse cx='60' cy='66' rx='40' ry='22' fill='#b8742e'/><path d='M40,58 L48,74 M58,54 L66,72 M76,56 L82,72' stroke='#f3d39a' stroke-width='6' stroke-linecap='round'/>",
    "coin": "<circle cx='60' cy='60' r='34' fill='#e2b041'/><circle cx='60' cy='60' r='24' fill='none' stroke='#b8862a' stroke-width='5'/>",
    "bank": "<path d='M24,48 L60,24 L96,48 Z' fill='#34425c'/><rect x='30' y='52' width='10' height='34' fill='#34425c'/><rect x='55' y='52' width='10' height='34' fill='#34425c'/>"
            "<rect x='80' y='52' width='10' height='34' fill='#34425c'/><rect x='22' y='88' width='76' height='10' fill='#34425c'/>",
}


def row(icon, label, value, color, bar=None):
    """One infographic row: icon, who, a bar sized by the rate, the rate."""
    b = ""
    if bar is not None:
        b = (f"<rect x='150' y='100' width='520' height='22' rx='11' fill='#1a1410' opacity='0.12'/>"
             f"<rect x='150' y='100' width='{int(520 * bar)}' height='22' rx='11' fill='{color}'/>")
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 150'><rect x='5' y='5' width='890' height='140' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/><g transform='translate(16,15)'>{ICON[icon]}</g>"
            f"<text x='150' y='{78 if bar is not None else 96}' font-size='46' fill='#1a1410' {F}>{label}</text>{b}"
            f"<text x='860' y='112' text-anchor='end' font-size='96' fill='{color}' {AN}>{value}</text></svg>")


S = []
# 1. hook (bank mid): the banker behind the teller counter, Ved walks in and asks
sm = ST["bank_mid"]
S.append({"say": "Why does a bank *pay you*... just for keeping your money there?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.07, "focus": [0.52, 0.5]}]},
          "layers": staged("bank_mid",
                           behind=[person("bank_mid", "banker", -1.4, 1.35, [["idle", 0], ["wave", 1.6], ["idle", 2.6]])],
                           front=[ved("bank_mid", -0.55, -1.25, [["warm", 0], ["explain", 1.2], ["think", 2.6]],
                                      walk=[(0, 1.2, -1.6), (1.1, -0.55, -1.25)])],
                           extra_top=[txt("WHY DOES THE BANK *PAY YOU?*", 0.15, 104, enter="none"),
                                      drop("coin_stack", 0.24, 0.47, 0.11, 0.6, sfx="pop")])})
# 2. close-up on Ved
S.append({"say": "Sounds way too generous, right? Here's the trick.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("bank_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.8, "scale": 1.4}]),
                     close_ved([["welcome", 0], ["smirk", 1.5]])]})
# 3. wide: Amina carries her coins to the counter and deposits 100
sw = ST["bank_wide"]
am_end = sw.place(-0.3, -0.5, "extra")
top_x, top_y = sw.point(-1.6, 0.55, 1.15)
amina = person("bank_wide", "amina", -0.3, -0.5, [["hold", 0], ["give", 1.6], ["happy", 2.4]],
               walk=[(0, 2.8, -1.8), (1.5, -0.3, -0.5)])
S.append({"say": "Amina puts *100 coins* in the bank.", "transition": "slide_left",
          "camera": {"zoom": [1.0, 1.04], "focus": [0.5, 0.52]},
          "layers": staged("bank_wide",
                           behind=[person("bank_wide", "banker", -1.6, 1.35, [["idle", 0], ["take", 1.8], ["happy", 2.6]])],
                           front=[amina, ved("bank_wide", 1.1, -2.4, [["explain", 0], ["point", 1.6]])],
                           extra_top=coins(am_end["x"], am_end["y"] - 0.05, top_x, top_y, 1.6, n=7) + [
                               sprite("coin_pile", top_x, top_y - 0.01, 0.11, at=2.2, enter="pop", sfx="pop"),
                               txt("*100* COINS", 0.13, 120, enter="pop", at=0.3, sfx="pop")])})
# 4. vault: a few coins stay in the vault
sv = ST["bank_vault"]
S.append({"say": "The bank keeps a few safe in the vault...", "transition": "cut", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.8, "zoom": 1.08, "focus": [0.5, 0.5]}]},
          "layers": clean([plate("bank_vault")] +
                          [drop("coin", random.uniform(0.48, 0.8), random.uniform(0.66, 0.72), 0.07, 0.4 + i * 0.12,
                                from_y=-0.08, spin=random.uniform(-200, 200)) for i in range(10)] + [
                          txt("*10* KEPT SAFE", 0.12, 110, enter="pop", at=0.5, sfx="pop"),
                          ved("bank_vault", 1.3, 1.6, [["point", 0], ["explain", 1.6]], walk=[(0, 0.3, 1.6), (0.9, 1.3, 1.6)])])})
# 5. mid: Ravi the baker borrows the rest
rv = sm.place(-1.95, -0.5, "extra")
bk_x, bk_y = sm.point(-1.4, 0.6, 1.2)
S.append({"say": "...and *lends* the rest to Ravi, the baker.", "transition": "cut", "caption_y": 0.27,
          "layers": staged("bank_mid",
                           behind=[person("bank_mid", "banker", -1.4, 1.35, [["give", 0], ["idle", 1.4]])],
                           front=[person("bank_mid", "ravi", -1.95, -0.5, [["idle", 0], ["take", 0.6], ["cheer", 1.4]],
                                         walk=[(0, -3.6, -0.9), (0.6, -1.95, -0.5)], hops=[[1.5, 0.04, 0.45]])],
                           extra_top=coins(bk_x, bk_y, rv["x"], rv["y"] - 0.05, 0.6, n=8) + [
                               txt("*90* LENT", 0.14, 120, enter="pop", at=0.5, sfx="pop")])})
# 6. bakery wide: Ravi buys a bigger oven, bakes twice the bread
sb = ST["bakery_wide"]
ov_x, ov_y = sb.point(-2.4, 0.2, 0.75)
ovw = abs(sb.point(-1.6, 0.2, 0.7)[0] - sb.point(-3.2, 0.2, 0.7)[0]) * 1.2
loaves = [fly("loaf", ov_x - 0.04, ov_y, random.uniform(0.15, 0.85), random.uniform(0.2, 0.32), 0.12, 2.3 + i * 0.18,
              dur=0.8, rot0=0, rot1=random.uniform(-40, 40), arc=0.1) for i in range(8)]
for L in loaves:
    L["until"] += 2.5; L["keys"][-1]["scale"] = 1.0
S.append({"say": "Ravi buys a bigger oven... and bakes *twice* the bread.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.52]}, {"t": 3.5, "zoom": 1.06, "focus": [0.55, 0.52]}]},
          "layers": staged("bakery_wide",
                           behind=[person("bakery_wide", "ravi", 0.2, 0.75, [["idle", 0], ["point", 0.9], ["cheer", 2.4]], hops=[[2.5, 0.03, 0.45]])],
                           front=[ved("bakery_wide", 1.4, -1.8, [["warm", 0], ["surprised", 1.2], ["explain", 2.6]], hops=[[1.25, 0.04, 0.4]])],
                           extra_top=[sprite("oven", ov_x, ov_y, ovw, at=0.8, keys=[{"t": 0, "y": -0.2}, {"t": 0.6, "y": ov_y, "ease": "bounce"}], sfx="boom"),
                                      txt("*2x* THE BREAD", 0.13, 116, enter="pop", at=2.2, sfx="ding")] + loaves)})
# 7. bakery mid: customers queue and buy; coins pour in; he pays the bank back plus interest
sbm = ST["bakery_mid"]
rv2 = sbm.place(0.3, 0.8, "extra")
buy = []
for i, (who, wx, wy, t) in enumerate((("tomas", -0.82, -0.6, 0.4), ("lena", 0.85, -0.6, 0.9))):
    buy.append(person("bakery_mid", who, wx, wy, [["idle", 0], ["give", t + 0.6], ["happy", t + 1.4]],
                      walk=[(0, wx + (-2.4 if wx < 0 else 2.4), wy - 0.4), (t + 0.5, wx, wy)], hops=[[t + 1.6, 0.03, 0.45]]))
S.append({"say": "Business booms! So he pays the bank back... *plus interest*.", "transition": "cut",
          "layers": staged("bakery_mid",
                           behind=[person("bakery_mid", "ravi", 0.3, 0.8, [["happy", 0], ["take", 1.0], ["cheer", 2.2]])],
                           front=buy,
                           extra_top=coins(0.2, 0.52, rv2["x"], rv2["y"] - 0.08, 1.0, n=6) + coins(0.8, 0.52, rv2["x"], rv2["y"] - 0.08, 1.6, n=5) + [
                               txt("90 COINS BACK", 0.12, 104, enter="pop", at=2.2, sfx="pop"),
                               txt("+ *INTEREST*", 0.215, 92, enter="pop", at=2.9)])})
# 8. infographic: who earns what (example rates)
S.append({"say": "Say Ravi pays *8%*. The bank gives Amina *3%*... and keeps the *gap*.", "transition": "zoom",
          "caption_y": 0.45,
          "layers": [plate("bank_mid", blur=14, keys=[{"t": 0, "scale": 1.2}]),
                     {"type": "image", "svg": row("loaf", "RAVI PAYS", "8%", "#d9534f", 0.8), "w": 0.86, "x": 0.5, "y": 0.12, "enter": "slide_right", "at": 0.2, "sfx": "pop"},
                     {"type": "image", "svg": row("coin", "AMINA EARNS", "3%", "#46965a", 0.3), "w": 0.86, "x": 0.5, "y": 0.215, "enter": "slide_right", "at": 1.5, "sfx": "pop"},
                     {"type": "image", "svg": row("bank", "BANK KEEPS THE GAP", "5%", "#34425c"), "w": 0.86, "x": 0.5, "y": 0.31, "enter": "slide_right", "at": 3.4, "sfx": "ding"},
                     {"type": "text", "text": "example rates", "font": "light", "size": 38, "x": 0.8, "y": 0.37, "color": "primary",
                      "stroke": "#0b0f12", "stroke_width": 4, "enter": "fade", "at": 0.6},
                     {"type": "character", "id": "ved", "pose": "point", "x": 0.5, "y": 0.72, "h": 0.42, "enter": "none",
                      "acting": [["explain", 0], ["point", 1.4], ["warm", 3.4]], "allow_outside_safe": True}]})
# 9. comic beat: reaction cut-away
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("bakery_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["idle", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.5, "zoom": 1.12, "focus": [0.5, 0.42], "sfx": "pop",
                   "text": "Your coins 0.1 sec after deposit:\n*\"I work at a bakery now\"*", "text_y": 0.18}})
# 10. wide: everyone wins; Amina gets her interest
am2 = sw.place(-0.3, -0.5, "extra")
S.append({"say": "Amina earns. Ravi grows. The bank profits.", "transition": "cut",
          "camera": {"zoom": [1.04, 1.0], "focus": [0.5, 0.52]},
          "layers": staged("bank_wide",
                           behind=[person("bank_wide", "banker", -1.6, 1.35, [["give", 0], ["happy", 1.6]])],
                           front=[person("bank_wide", "amina", -0.3, -0.5, [["take", 0], ["cheer", 0.7]], hops=[[0.8, 0.04, 0.45]]),
                                  person("bank_wide", "ravi", 0.6, -1.1, [["happy", 0], ["cheer", 1.3]], walk=[(0, 3.2, -1.8), (1.2, 0.6, -1.1)], hops=[[1.4, 0.03, 0.45]]),
                                  ved("bank_wide", 1.6, -2.6, [["welcome", 0], ["warm", 2.0]])],
                           extra_top=coins(top_x, top_y, am2["x"], am2["y"] - 0.06, 0.1, n=3, w=0.07) + [
                               txt("AMINA *+3*", 0.12, 100, enter="pop", at=0.3, sfx="pop"),
                               txt("RAVI *+OVEN*", 0.2, 88, enter="pop", at=1.2, sfx="pop"),
                               txt("BANK *+GAP*", 0.28, 88, enter="pop", at=2.2, sfx="pop")])})
# 11. close: payoff
S.append({"say": "So interest isn't a gift. It's *rent*... for borrowing your money.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("bank_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4, "scale": 1.42}]),
                     close_ved([["explain", 0], ["serious", 1.8], ["crossed", 3.2]]),
                     txt("INTEREST = *RENT* FOR YOUR MONEY", 0.14, 100, enter="pop", at=2.0, sfx="ding")]})

job = {"id": ID, "title": "Why does the bank pay YOU interest? 🏦",
       "description": "One deposit, one baker, one bigger oven: the simplest way to see where the interest on your savings actually comes from.\n\n"
                      "Rates in the video are example numbers. Sources: Reserve Bank of Australia, 'What are interest margins?'; "
                      "Capital One, 'How does savings interest work?'",
       "tags": ["interest", "banks", "how banks work", "savings", "economics", "money", "finance explained", "net interest margin"],
       "hashtags": ["#economics", "#money"],
       "meta": {"format": "big-question", "topic": "why banks pay interest on deposits (net interest margin)", "hook": "question",
                "idea_source": "backlog", "characters": ["ved", "extra"],
                "sources": ["https://www.rba.gov.au/publications/submissions/financial-sector/international-comparisons-of-bank-margins/what-are-interest-margins.html",
                            "https://www.capitalone.com/bank/money-management/banking-basics/how-does-savings-interest-work/",
                            "https://www.fool.com/money/banks/articles/explain-it-to-me-like-im-five-heres-how-interest-rates-work"],
                "humour": {"trend": "'how X acts 0.1 seconds after...' captions from the Skull Cap trend (rising, late Oct-Nov 2026)",
                           "beat": "smirk", "scene": 8}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
