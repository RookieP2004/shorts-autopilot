"""2026-11-11-c: "Why is nothing ever really free?" (big-question, opportunity cost). 2D Ved + townspeople in a golden-hour
town plaza (Blender plates: pizza stall + cinema kiosk) and an economists' lecture hall. Props are Blender cut-outs.
Run after the assets exist: python jobs/2026-11-11-c/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-11-c"
J = f"jobs/{ID}/"
A = J + "assets/"
PV = "/tmp/claude-0/-home-claude-shorts-autopilot/dd40f5dc-e1f3-532a-912c-a0fe3516b4c6/scratchpad/pv/"
SRC = A if os.path.exists(A + "phone.png") else PV
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("plaza_wide", "pizza_mid", "cinema_mid", "hall")}

OUT = {   # same people, same outfits in every shot
    "kofi": {"skin": "#6b4430", "hat": ["cap", "#34425c"], "top": ["#f2b04a", "tshirt"], "bottom": ["#34425c", "trousers"], "build": "slim"},
    "nani": {"skin": "#a86f4c", "build": "round", "hair": ["#d8d4cc", "bun"], "top": ["#7c2533", "dress"], "apron": "#f6efe2"},
    "mei": {"skin": "#f0c8a8", "hair": ["#1d1712", "long"], "hat": ["beret", "#d9534f"], "top": ["#6fc3c0", "shirt"],
            "bottom": ["#34425c", "trousers"], "bag": "#8a5a3c"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "_depth": 0.6}


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


def staged(set_, people=(), extra_top=(), with_fg=False):
    layers = list(people) + ([fg(set_)] if with_fg else [])
    out = [plate(set_)] + sorted(layers, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


S = []
pw = ST["plaza_wide"]
# 1. HOOK (wide plaza): the question on screen at frame 0
S.append({"say": "Why is nothing ever *really* free?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "caption_y": 0.41,
          "layers": staged("plaza_wide",
                           [person("plaza_wide", "nani", -2.3, 1.75, [["idle", 0], ["wave", 0.8]]),
                            person("plaza_wide", "mei", 1.4, -0.4, [["idle", 0]], walk=[(0, 3.6, -0.4), (2.4, 1.4, -0.4)]),
                            person("plaza_wide", "kofi", -0.3, -1.6, [["hold", 0], ["shrug", 1.2]]),
                            ved("plaza_wide", 1.3, -4.6, [["welcome", 0], ["think", 1.0]])],
                           [sprite("ticket", 0.3, 0.27, 0.22, enter="none", keys=[{"t": 0, "rot": -12}, {"t": 2.0, "rot": 6}]),
                            sprite("pizza", 0.72, 0.29, 0.2, enter="none", keys=[{"t": 0, "rot": 8}, {"t": 2.0, "rot": -6}]),
                            txt("WHY IS NOTHING", 0.1, 100, enter="none"),
                            txt("*REALLY* FREE?", 0.17, 118, enter="none")], with_fg=True)})
# 2. close-up: the name of the idea
S.append({"say": "Because every choice has a hidden price tag. Economists call it *opportunity cost*.", "transition": "cut",
          "caption_y": 0.64,
          "layers": [plate("plaza_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 2.6]]),
                     txt("HIDDEN *PRICE TAG*", 0.1, 84, enter="pop", at=0.8, sfx="pop"),
                     txt("OPPORTUNITY *COST*", 0.2, 88, enter="pop", at=2.8, sfx="pop")]})
# 3. pizza stall: Kofi's budget
pm = ST["pizza_mid"]
budget = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 300'><rect width='900' height='300' rx='32' fill='#f6efe2'/>"
          "<rect width='900' height='300' rx='32' fill='none' stroke='#1a1410' stroke-width='6'/>"
          f"<text x='450' y='70' text-anchor='middle' font-size='40' fill='#1a1410' {F}>KOFI HAS</text>"
          "<rect x='90' y='105' width='300' height='140' rx='18' fill='#46965a'/>"
          f"<text x='240' y='200' text-anchor='middle' font-size='76' fill='#f6efe2' {AN}>$10</text>"
          f"<text x='450' y='200' text-anchor='middle' font-size='64' fill='#d98a1a' {AN}>+</text>"
          "<rect x='510' y='105' width='300' height='140' rx='18' fill='#34425c'/>"
          f"<text x='660' y='170' text-anchor='middle' font-size='44' fill='#f6efe2' {AN}>1 FREE</text>"
          f"<text x='660' y='225' text-anchor='middle' font-size='44' fill='#f2b04a' {AN}>EVENING</text></svg>")
S.append({"say": "Meet Kofi. He has ten dollars and one free evening. Pizza...", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "caption_y": 0.41,
          "layers": staged("pizza_mid",
                           [person("pizza_mid", "nani", -2.35, 1.75, [["idle", 0], ["give", 2.6]]),
                            person("pizza_mid", "kofi", -1.6, -0.6, [["idle", 0], ["point", 2.8]], walk=[(0, -0.2, -0.9), (1.4, -1.6, -0.6)])],
                           [card(budget, 0.2, w=0.82, at=0.6),
                            sprite("pizza", 0.42, 0.33, 0.24, enter="drop", at=2.6, sfx="pop",
                                   keys=[{"t": 0, "rot": -8}, {"t": 0.6, "rot": 0}])], with_fg=True)})
# 4. cinema kiosk: or a movie
S.append({"say": "...or a *movie*. Not both.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.07, "focus": [0.5, 0.48]}]},
          "caption_y": 0.72,
          "layers": staged("cinema_mid",
                           [person("cinema_mid", "kofi", 1.9, 0.0, [["idle", 0], ["surprised", 0.6], ["shrug", 1.6]],
                                   walk=[(0, 0.6, -0.3), (0.7, 1.9, 0.0)])],
                           [sprite("ticket", 0.26, 0.56, 0.26, enter="pop", at=0.2, sfx="pop",
                                   keys=[{"t": 0, "rot": -18, "y": 0.6}, {"t": 0.5, "rot": -6, "y": 0.56, "ease": "back"}]),
                            sprite("popcorn", 0.78, 0.6, 0.15, enter="drop", at=0.5, sfx="pop"),
                            txt("NOT *BOTH*", 0.37, 120, enter="pop", at=1.2, sfx="pop")])})
# 5. wide: he walks to the cinema; the pizza night disappears
S.append({"say": "He picks the movie. The ticket cost ten dollars. But the *real* cost?", "transition": "cut",
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "caption_y": 0.41,
          "layers": staged("plaza_wide",
                           [person("plaza_wide", "nani", -2.3, 1.75, [["idle", 0], ["sad", 1.4]]),
                            person("plaza_wide", "kofi", 2.0, 0.1, [["happy", 0], ["hold", 1.6]],
                                   walk=[(0, -0.3, -1.6), (1.6, 2.0, 0.1)], hops=[[1.7, 0.04, 0.4]]),
                            ved("plaza_wide", -0.9, -4.8, [["explain", 0], ["think", 3.2]])],
                           [sprite("pizza", pw.point(-2.3, 1.2, 1.6)[0], pw.point(-2.3, 1.2, 1.6)[1], 0.14, enter="pop", at=0.2,
                                   until=2.4, exit="fade"),
                            txt("$10", 0.13, 120, enter="pop", at=1.6, sfx="pop", color="#9fe07a"),
                            txt("REAL COST: *?*", 0.21, 90, enter="pop", at=3.0, sfx="pop")], with_fg=True)})
# 6. infographic: price vs opportunity cost
oc = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 520'><rect width='900' height='520' rx='34' fill='#f6efe2'/>"
      "<rect width='900' height='520' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
      f"<text x='225' y='80' text-anchor='middle' font-size='38' fill='#5a4636' {F}>PRICE</text>"
      f"<text x='675' y='80' text-anchor='middle' font-size='38' fill='#d9534f' {F}>OPPORTUNITY COST</text>"
      "<line x1='450' y1='40' x2='450' y2='420' stroke='#1a1410' stroke-width='4' stroke-dasharray='14 12'/>"
      "<rect x='95' y='150' width='260' height='150' rx='18' fill='#46965a'/>"
      f"<text x='225' y='255' text-anchor='middle' font-size='84' fill='#f6efe2' {AN}>$10</text>"
      "<circle cx='675' cy='225' r='92' fill='#d9a35a'/><circle cx='675' cy='225' r='76' fill='#f4cf6a'/>"
      "<circle cx='640' cy='195' r='14' fill='#9e1f1a'/><circle cx='705' cy='205' r='14' fill='#9e1f1a'/>"
      "<circle cx='660' cy='255' r='14' fill='#9e1f1a'/><circle cx='712' cy='258' r='14' fill='#9e1f1a'/>"
      "<line x1='590' y1='140' x2='760' y2='310' stroke='#d9534f' stroke-width='14' stroke-linecap='round'/>"
      f"<text x='675' y='370' text-anchor='middle' font-size='36' fill='#1a1410' {F}>THE PIZZA NIGHT</text>"
      f"<text x='225' y='370' text-anchor='middle' font-size='36' fill='#1a1410' {F}>WHAT YOU PAY</text>"
      f"<text x='450' y='480' text-anchor='middle' font-size='44' fill='#d98a1a' {AN}>THE BEST THING YOU SAID NO TO</text></svg>")
S.append({"say": "The pizza night he gave up. Opportunity cost is the best thing you said *no* to.", "transition": "slide_up",
          "caption_y": 0.64,
          "layers": [plate("cinema_mid", blur=8, keys=[{"t": 0, "scale": 1.15}, {"t": 5, "scale": 1.21}]),
                     card(oc, 0.29, w=0.9, at=0.2),
                     sprite("pizza", 0.78, 0.53, 0.18, enter="pop", at=0.5, sfx="pop",
                            keys=[{"t": 0, "rot": 0, "opacity": 1}, {"t": 1.6, "rot": 40, "y": 0.5, "opacity": 0.0, "ease": "in"}]),
                     sprite("ticket", 0.24, 0.52, 0.2, enter="pop", at=0.4, keys=[{"t": 0, "rot": -10}, {"t": 4, "rot": 4}])]})
# 7. time works the same way
tm = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 260'><rect width='900' height='260' rx='30' fill='#f6efe2'/>"
      "<rect width='900' height='260' rx='30' fill='none' stroke='#1a1410' stroke-width='6'/>"
      f"<text x='220' y='110' text-anchor='middle' font-size='54' fill='#1a1410' {AN}>1 HOUR</text>"
      f"<text x='220' y='170' text-anchor='middle' font-size='34' fill='#5a4636' {F}>SCROLLING</text>"
      "<path d='M390 125 L520 125' stroke='#d9534f' stroke-width='14' stroke-linecap='round'/>"
      "<path d='M500 95 L540 125 L500 155' fill='none' stroke='#d9534f' stroke-width='14' stroke-linecap='round' stroke-linejoin='round'/>"
      f"<text x='690' y='110' text-anchor='middle' font-size='38' fill='#2f8f8a' {AN}>COSTS 1 HOUR</text>"
      f"<text x='690' y='170' text-anchor='middle' font-size='34' fill='#5a4636' {F}>OF SLEEP</text>"
      f"<text x='450' y='232' text-anchor='middle' font-size='28' fill='#d98a1a' {F}>(or study, or a walk, or...)</text></svg>")
S.append({"say": "Time works the same way. An hour of scrolling costs the hour you could have *slept*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.08, "focus": [0.5, 0.52]}]},
          "caption_y": 0.41,
          "layers": staged("plaza_wide",
                           [person("plaza_wide", "mei", 0.4, 2.2, [["hold", 0], ["shrug", 3.4]]),
                            person("plaza_wide", "kofi", 3.0, 0.4, [["idle", 0]]),
                            ved("plaza_wide", -1.4, -3.6, [["explain", 0], ["point", 2.4]], walk=[(0, -4.2, -3.6), (1.2, -1.4, -3.6)])],
                           [sprite("clock", 0.44, 0.5, 0.13, enter="drop", at=0.5, sfx="pop", keys=[{"t": 0, "rot": -8}, {"t": 0.3, "rot": 8}, {"t": 0.6, "rot": -6}, {"t": 0.9, "rot": 0}]),
                            sprite("phone", 0.8, 0.52, 0.1, enter="pop", at=1.6, sfx="pop", keys=[{"t": 0, "rot": 12}, {"t": 3, "rot": -4}]),
                            card(tm, 0.18, w=0.86, at=1.4)], with_fg=True)})
# 8. hall: the economists' puzzle
hl = ST["hall"]
S.append({"say": "Sounds easy? In 2005, almost *two hundred* economists were given a simple puzzle about it.", "transition": "zoom",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "caption_y": 0.6,
          "layers": staged("hall",
                           [ved("hall", -0.85, -1.8, [["think", 0], ["point", 2.6]], walk=[(0, -3.6, -1.8), (1.4, -0.85, -1.8)])],
                           [txt("~200 *ECONOMISTS*", 0.12, 100, enter="pop", at=1.4, sfx="pop"),
                            txt("ONE SIMPLE PUZZLE", 0.19, 70, enter="pop", at=3.0)])})
# 9. the result: worse than guessing
res = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 470'><rect width='900' height='470' rx='34' fill='#f6efe2'/>"
       "<rect width='900' height='470' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
       "<rect x='170' y='160' width='220' height='190' rx='12' fill='#d9534f'/>"
       "<rect x='510' y='122' width='220' height='228' rx='12' fill='#6fc3c0'/>"
       f"<text x='280' y='145' text-anchor='middle' font-size='58' fill='#1a1410' {AN}>21.6%</text>"
       f"<text x='620' y='107' text-anchor='middle' font-size='58' fill='#1a1410' {AN}>25%</text>"
       "<line x1='120' y1='350' x2='780' y2='350' stroke='#1a1410' stroke-width='5'/>"
       f"<text x='280' y='405' text-anchor='middle' font-size='34' fill='#1a1410' {F}>ECONOMISTS</text>"
       f"<text x='620' y='405' text-anchor='middle' font-size='34' fill='#1a1410' {F}>RANDOM GUESS</text>"
       f"<text x='450' y='450' text-anchor='middle' font-size='26' fill='#5a4636' {F}>who got it right (4 options: $0, $10, $40, $50)</text></svg>")
S.append({"say": "Only about *one in five* got it right. That's worse than random guessing.", "transition": "slide_up",
          "caption_y": 0.64,
          "layers": [plate("hall", blur=6, keys=[{"t": 0, "scale": 1.12}, {"t": 4, "scale": 1.18}]),
                     card(res, 0.27, w=0.88, at=0.2),
                     {"type": "counter", "from": 0, "to": 21.6, "decimals": 1, "suffix": "%", "count_dur": 1.0, "at": 0.4, "x": 0.5,
                      "y": 0.52, "size": 120, "color": "#ff5a5a", "stroke": "#0b0f12", "stroke_width": 7, "enter": "pop"}]})
# 10. comic beat (reaction cut-away)
S.append({"dur": 1.7, "transition": "cut", "captions": False,
          "layers": [plate("hall", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.5, "text": "Experts: 0. *Random guessing:* 1.", "text_y": 0.18}})
# 11. close payoff
S.append({"say": "So next time something's free, ask one question. Free... compared to *what*?",
          "transition": "cut", "caption_y": 0.64,
          "layers": [plate("plaza_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5.0, "scale": 1.43}]),
                     close_ved([["warm", 0], ["explain", 1.8], ["smirk", 3.6]]),
                     sprite("ticket", 0.8, 0.12, 0.18, enter="pop", at=0.6, sfx="pop", keys=[{"t": 0, "rot": 10}, {"t": 4, "rot": -4}]),
                     txt("FREE?", 0.1, 100, enter="pop", at=0.4, x=0.4),
                     txt("COMPARED TO *WHAT?*", 0.2, 80, enter="pop", at=3.0, sfx="ding")]})

SRCS = ["https://www.econlib.org/library/Enc/OpportunityCost.html",
        "https://www.viet-studies.com/kinhte/Econ_OpCost_NYT.pdf"]
job = {"id": ID, "title": "Why is nothing ever really free? 🎟️",
       "description": "Every choice has a hidden price tag: opportunity cost, the value of the best option you gave up. "
                      "Even economists trip on it: in a 2005 survey of almost 200 economists, only 21.6% got a simple opportunity-cost "
                      "question right, fewer than random guessing would.\n\nSources: " + " ; ".join(SRCS),
       "tags": ["opportunity cost", "economics", "economics explained", "decision making", "money", "behavioral economics",
                "explained", "learn economics"],
       "hashtags": ["#economics", "#money"],
       "meta": {"format": "big-question", "topic": "opportunity cost (and the 2005 economists' survey)",
                "hook": "question", "idea_source": "backlog (ideas.md: What is opportunity cost?)",
                "characters": ["ved", "extra"], "sources": SRCS,
                "humour": {"trend": "timeless (no current trend fit naturally this week): dry scoreboard card 'Experts: 0. Random guessing: 1.'",
                           "beat": "side_eye", "scene": 9}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
