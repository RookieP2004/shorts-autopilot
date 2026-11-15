"""2026-11-16-c: "Money laundering isn't named after Capone's laundromats" (dark-files, myth-bust hook).
2D Ved + townspeople staged in depth on Blender sets: a 1920s street at dusk with a LAUNDRY shop (wide, mid), the 1910
Treasury basement with its money-washing machine (wide, close on the rollers), a tax agent's desk with an open ledger.
Timeline, laundering-idea and verdict panels, counters, honesty tags and labels are 2D.
Run after the assets exist: python jobs/2026-11-16-c/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-16-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("street_wide", "street_mid", "treasury_wide", "treasury_close", "desk")}

OUT = {   # recurring people: same outfit in every shot
    "boss": {"skin": "#e0b08a", "build": "round", "hair": ["#1a1410", "short"], "hat": ["bowler", "#2b2f36"],
             "top": ["#3a3e48", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#1a1410", "tie": "#d9534f"},
    "clerk": {"skin": "#c98e62", "build": "slim", "hair": ["#2a1d17", "short"], "hat": ["cap", "#46965a"],
              "top": ["#f6efe2", "vest"], "bottom": ["#5a3a4a", "trousers"], "shoes": "#25262b", "apron": "#d9c99a"},
    "clerk2": {"skin": "#8d5a3b", "build": "regular", "hair": ["#1a1410", "bun"], "top": ["#6fc3c0", "dress"],
               "shoes": "#25262b", "apron": "#f6efe2"},
    "agent": {"skin": "#d9a27a", "build": "slim", "hair": ["#6b4529", "short"], "hat": ["bowler", "#7d8597"],
              "top": ["#7d8597", "jacket"], "bottom": ["#5a5f66", "trousers"], "shoes": "#25262b", "tie": "#34425c", "bag": "#8a5a3c"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


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


def stamp(word, color="#d9534f", w=560):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='128' text-anchor='middle' font-size='118' "
            f"fill='{color}' {AN}>{word}</text></svg>")


def fstamp(word, color="#f2b04a", w=480):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='#1a1410' fill-opacity='0.85' stroke='{color}' stroke-width='12'/><text x='{w/2}' y='128' text-anchor='middle' "
            f"font-size='118' fill='{color}' {AN}>{word}</text></svg>")


def label(word, color="#f2b04a", w=420):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 96'><rect x='4' y='4' width='{w-8}' height='88' rx='20' "
            f"fill='#1a1410' fill-opacity='0.82' stroke='{color}' stroke-width='5'/><text x='{w/2}' y='68' text-anchor='middle' "
            f"font-size='56' fill='{color}' {AN}>{word}</text></svg>")


def tag(word, x, y, w=0.3, color="#f2b04a", at=0.0, **k):
    return {"type": "image", "svg": label(word, color, max(300, 34 * len(word) + 80)), "x": x, "y": y, "w": w, "enter": "pop",
            "at": at, "sfx": "pop", **k}


def honesty(word, x, y, at=0.0, color="#46965a"):
    return {"type": "image", "svg": label(word, color, 300), "x": x, "y": y, "w": 0.2, "enter": "pop", "at": at, "rotate": -4}


# timeline: the washing machine, Capone, the word in print, Watergate
def tl_item(cx, year, l1, l2, col):
    return (f"<circle cx='{cx}' cy='120' r='26' fill='{col}' stroke='#1a1410' stroke-width='5'/>"
            f"<text x='{cx}' y='72' text-anchor='middle' font-size='54' fill='#1a1410' {AN}>{year}</text>"
            f"<text x='{cx}' y='196' text-anchor='middle' font-size='30' fill='#34425c' {F}>{l1}</text>"
            f"<text x='{cx}' y='234' text-anchor='middle' font-size='30' fill='#34425c' {F}>{l2}</text>")


TIMELINE = card("<line x1='110' y1='120' x2='890' y2='120' stroke='#1a1410' stroke-width='8' stroke-linecap='round'/>"
                + tl_item(130, "1910", "TREASURY", "WASHES CASH", "#6fc3c0")
                + tl_item(370, "1931", "CAPONE", "JAILED", "#c9a24a")
                + tl_item(620, "1970", "WORD IN", "PRINT", "#f2b04a")
                + tl_item(860, "1973", "WATERGATE", "MAKES IT FAMOUS", "#d9534f"), 1000, 270)

# what laundering means: dirty cash -> a normal-looking business -> money that looks earned
IDEA = card(
    "<rect x='40' y='60' width='190' height='110' rx='14' fill='#7a6a52' stroke='#1a1410' stroke-width='5'/>"
    "<text x='135' y='132' text-anchor='middle' font-size='58' fill='#f6efe2' " + AN + ">$$$</text>"
    "<text x='135' y='220' text-anchor='middle' font-size='34' fill='#1a1410' " + F + ">DIRTY CASH</text>"
    "<path d='M250 115 L330 115' stroke='#1a1410' stroke-width='9'/><path d='M322 95 L352 115 L322 135 Z' fill='#1a1410'/>"
    "<rect x='370' y='50' width='240' height='130' rx='16' fill='#b5533c' stroke='#1a1410' stroke-width='5'/>"
    "<rect x='390' y='70' width='200' height='34' rx='8' fill='#34425c'/>"
    "<text x='490' y='98' text-anchor='middle' font-size='28' fill='#f6efe2' " + AN + ">NORMAL SHOP</text>"
    "<circle cx='450' cy='145' r='22' fill='#e9e6df' stroke='#1a1410' stroke-width='4'/><circle cx='530' cy='145' r='22' fill='#e9e6df' stroke='#1a1410' stroke-width='4'/>"
    "<text x='490' y='220' text-anchor='middle' font-size='34' fill='#1a1410' " + F + ">A FRONT</text>"
    "<path d='M630 115 L710 115' stroke='#1a1410' stroke-width='9'/><path d='M702 95 L732 115 L702 135 Z' fill='#1a1410'/>"
    "<rect x='750' y='60' width='210' height='110' rx='14' fill='#46965a' stroke='#1a1410' stroke-width='5'/>"
    "<text x='855' y='132' text-anchor='middle' font-size='58' fill='#f6efe2' " + AN + ">$$$</text>"
    "<text x='855' y='220' text-anchor='middle' font-size='34' fill='#1a1410' " + F + ">'EARNED'</text>", 1000, 260)

VERDICT = card(
    "<text x='450' y='90' text-anchor='middle' font-size='64' fill='#1a1410' " + AN + ">1931: GUILTY</text>"
    "<text x='450' y='150' text-anchor='middle' font-size='38' fill='#34425c' " + F + ">INCOME TAX EVASION</text>"
    "<text x='450' y='236' text-anchor='middle' font-size='84' fill='#d9534f' " + AN + ">11 YEARS</text>"
    "<text x='450' y='290' text-anchor='middle' font-size='36' fill='#34425c' " + F + ">(4.5 OF THEM ON ALCATRAZ)</text>", 900, 320)

S = []
# 0. hook (street mid): the laundry shop, the myth at frame 0
S.append({"say": "Money laundering, named after Capone's *laundromats*? Probably a myth.",
          "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.06, "focus": [0.48, 0.5]}]},
          "layers": staged("street_mid",
                           people=[person("street_mid", "boss", -2.3, -0.9, [["idle", 0], ["shrug", 2.6]]),
                                   ved("street_mid", -0.9, -2.4, [["crossed", 0], ["point", 1.6], ["deadpan", 3.2]])],
                           extra_top=[{"type": "image", "svg": fstamp("MYTH?"), "x": 0.5, "y": 0.13, "w": 0.4, "rotate": -4,
                                       "enter": "none"},
                                      txt("CAPONE'S *LAUNDROMATS*", 0.3, 92, enter="none"),
                                      tag("AL CAPONE", 0.2, 0.75, 0.26, "#f6efe2", at=1.0)])})
# 1. treasury wide: 1910, clerks feed the machine
S.append({"say": "In 1910, the US Treasury really *laundered* money.",
          "transition": "slide_left", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("treasury_wide",
                           people=[person("treasury_wide", "clerk", -0.9, -0.5, [["give", 0], ["hold", 1.2]]),
                                   person("treasury_wide", "clerk2", 0.75, -0.4, [["take", 0], ["happy", 1.6]]),
                                   ved("treasury_wide", 0.35, -1.5, [["explain", 0], ["point", 1.0]],
                                       walk=[(0, 1.5, -1.7), (0.9, 0.35, -1.5)])],
                           extra_top=[txt("*1910*", 0.12, 130, enter="pop", at=0.2, sfx="pop"),
                                      honesty("PROVEN", 0.76, 0.36, at=1.2),
                                      tag("TREASURY, WASHINGTON", 0.32, 0.36, 0.44, "#6fc3c0", at=0.6)])})
# 2. close on the rollers: notes fly through, the counter runs
nx, ny = ST["treasury_close"].point(0.0, 0.72, 1.45)
S.append({"say": "A machine washed *25,000* dirty notes a day.",
          "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.1, "focus": [nx, ny]}]},
          "layers": [plate("treasury_close"),
                     sprite("note", 0.18, 0.62, 0.3, enter="none", at=0.2,
                            keys=[{"t": 0, "x": -0.2, "y": 0.66, "rot": -20}, {"t": 0.8, "x": 0.3, "y": 0.6, "rot": 6, "ease": "out"}]),
                     sprite("note", 0.8, 0.63, 0.3, enter="none", at=1.2,
                            keys=[{"t": 0, "x": 1.2, "y": 0.68, "rot": 25}, {"t": 0.8, "x": 0.72, "y": 0.6, "rot": -8, "ease": "out"}]),
                     {"type": "counter", "from": 0, "to": 25000, "decimals": 0, "suffix": " NOTES A DAY",
                      "x": 0.5, "y": 0.16, "size": 82, "color": "accent", "at": 0.4, "count_dur": 1.6, "enter": "zoom", "sfx": "riser"},
                     txt("WASHED. DRIED. *SPENT AGAIN.*", 0.25, 64, enter="pop", at=2.2, sfx="pop")]})
# 3. street wide: the timeline drops in
S.append({"say": "The crime meaning? In print by *1970*, famous with Watergate.",
          "transition": "slide_up", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": staged("street_wide",
                           people=[ved("street_wide", -1.2, -2.6, [["explain", 0], ["point", 1.8], ["think", 3.6]])],
                           extra_top=[{"type": "image", "svg": TIMELINE, "x": 0.5, "y": 0.19, "w": 0.92, "enter": "slide_down",
                                       "at": 0.2, "sfx": "whoosh"},
                                      honesty("PROVEN", 0.8, 0.34, at=1.6)])})
# 4. street mid: the boss carries a bag into the laundry; the idea panel
S.append({"say": "It means making dirty cash look *earned*.",
          "transition": "slide_left", "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("street_mid",
                           people=[person("street_mid", "boss", -1.8, -0.7, [["hold", 0], ["give", 1.8]],
                                          walk=[(0, -3.3, -1.2), (1.6, -1.8, -0.7)]),
                                   ved("street_mid", -0.7, -2.6, [["explain", 0], ["side_eye", 1.8]])],
                           extra_top=[{"type": "image", "svg": IDEA, "x": 0.5, "y": 0.18, "w": 0.92, "enter": "slide_down", "at": 0.3,
                                       "sfx": "whoosh"}])})
# 5. desk: his tax paid, stamped zero
lx, ly = ST["desk"].point(0.0, 0.1, 0.92)
S.append({"say": "Capone's problem? He never paid *tax* on it.",
          "transition": "zoom", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.12, "focus": [lx, ly]}]},
          "layers": [plate("desk"),
                     {"type": "image", "svg": card("<text x='330' y='92' text-anchor='middle' font-size='62' fill='#1a1410' " + AN
                                                   + ">INCOME TAX PAID:</text><text x='690' y='96' text-anchor='middle' font-size='80' fill='#d9534f' " + AN + ">$0</text>", 800, 140),
                      "x": 0.5, "y": 0.16, "w": 0.8, "enter": "slide_down", "at": 0.6, "sfx": "whoosh"},
                     {"type": "image", "svg": stamp("1925-1929", "#d9534f", 620), "x": 0.5, "y": 0.27, "w": 0.46, "rotate": -6,
                      "enter": "pop", "at": 1.6, "sfx": "boom"}]})
# 6. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("desk", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "IRS: 'hey... your taxes?'\ncapone: *left on read*", "text_y": 0.2}})
# 7. street wide: the agent leads the boss off; verdict card
S.append({"say": "In 1931 tax agents got him: *eleven years*.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("street_wide",
                           people=[person("street_wide", "agent", 0.6, -1.4, [["point", 0], ["hold", 1.8]],
                                          walk=[(1.0, 0.6, -1.4), (4.0, 3.6, -1.9)]),
                                   person("street_wide", "boss", -0.2, -1.2, [["sad", 0]],
                                          walk=[(1.0, -0.2, -1.2), (4.0, 2.8, -1.7)]),
                                   ved("street_wide", -2.3, -2.8, [["serious", 0], ["point", 2.0]])],
                           extra_top=[{"type": "image", "svg": VERDICT, "x": 0.5, "y": 0.19, "w": 0.8, "enter": "pop", "at": 0.3,
                                       "sfx": "boom"},
                                      honesty("PROVEN", 0.78, 0.3, at=1.4)])})
# 8. close payoff
S.append({"say": "Not caught by a gun. Caught by a *ledger*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("desk", blur=8, keys=[{"t": 0, "scale": 1.3}, {"t": 3.2, "scale": 1.38}]),
                     close_ved([["serious", 0], ["point", 1.3], ["smirk", 2.4]]),
                     sprite("ledger", 0.76, 0.31, 0.4, at=1.2, enter="pop", sfx="pop", rotate=-6),
                     txt("CAUGHT BY A *LEDGER*", 0.13, 108, enter="pop", at=1.6, sfx="ding")]})

SRC = ["https://www.mentalfloss.com/crime/myth-how-al-capone-gave-us-term-money-laundering",
       "https://www.historytoday.com/node/57030",
       "https://www.wordorigins.org/big-list-entries/money-laundering",
       "https://prologue.blogs.archives.gov/2011/07/26/the-taxman-cometh-u-s-v-alphonse-capone/"]
job = {"id": ID, "title": "Money laundering isn't named after Al Capone 🧺",
       "description": "The story says Al Capone hid his cash in laundromats and gave us the term \"money laundering\". Probably a myth: "
                      "in 1910 the US Treasury literally washed dirty banknotes (a machine cleaned and pressed about 25,000 a day), "
                      "while the criminal sense of the word shows up in print around 1970 and went mainstream with Watergate in 1973. "
                      "Capone himself was convicted of income tax evasion in 1931: 11 years, part of it on Alcatraz.\n\n"
                      "Sources: Mental Floss (the Capone myth); History Today (the Treasury's money-washing machine); "
                      "Word Origins (earliest uses of the term); US National Archives (U.S. v. Alphonse Capone).",
       "tags": ["money laundering", "al capone", "history of money laundering", "true crime history", "watergate",
                "us treasury", "dark history", "history explained"],
       "hashtags": ["#history", "#truecrime"],
       "instagram": {"hashtags": ["#history", "#alcapone", "#moneylaundering", "#truecrimehistory", "#explained"]},
       "meta": {"format": "dark-files", "topic": "the Al Capone laundromat myth: the Treasury literally washed banknotes from 1910 "
                                                 "(~25,000/day), the criminal term appears ~1970 and spreads with Watergate (1973); "
                                                 "what laundering means; Capone convicted of tax evasion 1931 (11 years, Alcatraz)",
                "hook": "myth-bust",
                "idea_source": "unique + viral-shaped: a famous gangster myth most people repeat, busted with a literal money-washing "
                               "machine; the channel's first dark-files Short (owner's new format)",
                "characters": ["ved", "extra"],
                "sources": SRC,
                "humour": {"trend": "'left on read' slang (still in daily use) as a side-eye card about Capone's tax return",
                           "beat": "side_eye", "scene": 6},
                "claims": [
                    {"claim": "the Capone-laundromat origin of the term is most likely a myth", "tag": "PROVEN (expert view)", "source": SRC[0]},
                    {"claim": "1910: a Treasury (Bureau of Engraving and Printing) machine cleaned and pressed ~25,000 notes a day", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "criminal 'launder' in print by 1970 (Globe and Mail); popularised by Watergate reporting in 1973", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "Capone never paid income tax (1925-1929 indictment); guilty Oct 1931; 11 years, 4.5 of 7.5 served on Alcatraz", "tag": "PROVEN", "source": SRC[3]}]},
       "thumbnail": {"title": "MONEY *LAUNDRY?*", "title_y": 0.14, "title_size": 180, "max_w": 0.95, "blur": 12,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#34425c", "#f08a24"], "tint_amount": 0.3,
                     "bg": [plate("street_mid")],
                     "fg": [sprite("note", 0.76, 0.4, 0.34, rotate=-12), sprite("ledger", 0.24, 0.44, 0.34, rotate=8),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "note", (nx, ny), "ledger", (lx, ly))
