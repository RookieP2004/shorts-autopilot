"""SAMPLE 2026-11-18-doc (private, not posted): the opening of a long documentary (16:9, fast pace) using EVERYTHING, mixed:
house (Ved presenting, townspeople, cream cards, chapters, comic beat) + night pieces (hud, stamp, optcards) + case-file
pieces (noir desk + blind light, dateline, dottext, tiles, tipnum, flows) + motion clips from the Remotion / GSAP / three.js
engine (KineticTitle slam, FlowDiagram, NumberSlam, Stack3D, Hero3D globe). Story: HSBC and the cartel cash (verified).
Facts: US DOJ press release + Breuer remarks (11 Dec 2012); US Senate PSI report (Jul 2012).
Run: python jobs/2026-11-18-doc/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-18-doc"
J = f"jobs/{ID}/"
A = J + "assets/"
C = "jobs/2026-11-14-L/assets/"          # the long video's town cafe (Ved's home turf)


def plate(name, blur=0, lit=False, base=A, **k):
    return {"type": "image", "path": base + f"plate_{name}{'_lit' if lit else ''}.png", "x": 0.5, "y": 0.5, "w": 1.0,
            "enter": "none", "blur": blur, **k}


def push(z0=1.0, z1=1.08, fx=0.5, fy=0.5, t=4.0):
    return {"keys": [{"t": 0, "zoom": z0, "focus": [fx, fy]}, {"t": t, "zoom": z1, "focus": [fx, fy]}]}


def ved_close(acting, x=0.2, y=0.9, h=1.05, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none", "acting": acting,
            "ground": False, "allow_outside_safe": True, **k}


def person(plate_name, who, wx, wy, acting, outfit=None, walk=None, **k):
    st = Stage(A + f"plate_{plate_name}.json")
    p = st.place(wx, wy, who)
    L = {"type": "character", "id": who, "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True, **k}
    if who == "extra":
        L.update(talk=False, rig_args={"outfit": outfit})
    if walk:
        L["keys"] = st.walk(walk, p, who)
    return L


def motion(comp, props, x=0.5, y=0.5, w=1.0, h=1.0, at_=0.0, **k):
    return {"type": "motion", "comp": comp, "props": props, "x": x, "y": y, "w": w, "h": h, "at": at_, "enter": "none", **k}


def card(text, x, y, w=0.36, at_=0.2, ink="#1a1410", size=70, rot=-2):
    AN = "font-family='Anton, DejaVu Sans, sans-serif'"
    lines = text.split("\n")
    H = 60 + 90 * len(lines)
    body = "".join(f"<text x='450' y='{100 + i * 90}' text-anchor='middle' font-size='{size}' fill='{ink}' {AN}>{ln}</text>"
                   for i, ln in enumerate(lines))
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 {H}'><rect x='6' y='6' width='888' height='{H - 12}' rx='34' "
           f"fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>{body}</svg>")
    return {"type": "image", "svg": svg, "x": x, "y": y, "w": w, "enter": "pop", "at": at_, "rotate": rot, "sfx": "pop"}


BLINDS = {"type": "blinds", "angle": -30, "count": 9, "strength": 0.14, "shade": 0.1, "drift": 0.015}
COURIER = {"skin": "#c68a5e", "build": "regular", "hair": ["#1a1410", "short"], "hat": ["cap", "#2b2f2a"],
           "top": ["#3a3e48", "jacket"], "bottom": ["#2a2c33", "trousers"], "shoes": "#1a1410"}
BANKER = {"skin": "#e2b48c", "build": "regular", "hair": ["#9aa0a8", "short"], "top": ["#23262d", "jacket"],
          "bottom": ["#23262d", "trousers"], "shoes": "#111111", "tie": "#d63a2f"}
S = []
# ---------------------------------------------------------------- cold open
S.append({"say": "Mexico, 2006. The drug cartels have a problem. Too much cash.", "music_hit": True,
          "camera": push(1.0, 1.1, 0.45, 0.55, 4.5),
          "layers": [plate("desk_case"), dict(BLINDS),
                     {"type": "dateline", "date": "2006", "place": "Mexico", "x": 0.27, "y": 0.22, "at": 0.1, "size": 96},
                     {"type": "dottext", "text": "PROBLEM: *TOO MUCH CASH*", "size": 40, "x": 0.66, "y": 0.84, "at": 1.4}]})
S.append({"say": "Their answer? Boxes. Built to fit exactly through a bank's teller window.",
          "transition": "whip", "transition_frames": 8, "camera": push(1.02, 1.14, 0.48, 0.55, 4.5),
          "layers": [plate("teller_close", lit=True),
                     {"type": "dottext", "text": "SIZE: *TELLER WINDOW*", "size": 46, "x": 0.5, "y": 0.16, "at": 1.2, "plate": True},
                     {"type": "tag", "text": "US DEPT OF JUSTICE, 2012", "x": 0.86, "y": 0.92, "at": 1.6, "size": 22}]})
S.append({"say": "And a global bank kept taking it.", "transition": "cut", "min_dur": 2.6,
          "layers": [plate("laundry_door", blur=6),
                     motion("KineticTitle", {"lines": ["THE BANK THAT", "*WASHED* CARTEL CASH"], "size": 120, "y": 0.45, "style": "slam",
                                             "stagger": 0.022})],
          "sfx": "stomp", "sfx_at": 0.5})
S.append({"say": "I'm Professor Ved. Let's open the case file.", "transition": "push", "transition_frames": 10,
          "layers": [plate("cafe_mid", blur=8, base=C, keys=[{"t": 0, "scale": 1.12}, {"t": 4, "scale": 1.18}]),
                     ved_close([["welcome", 0], ["point", 1.6]]),
                     {"type": "lower_third", "title": "Professor Ved", "sub": "The Explainer", "at": 0.3},
                     card("CASE FILE:\nHSBC, 2006-2012", 0.66, 0.4, w=0.42, at_=0.9)]})
# ---------------------------------------------------------------- chapter 1
S.append({"say": "Step one of laundering: get the dirty cash into a bank.", "transition": "whip", "transition_frames": 8,
          "layers": [plate("laundry_wide", blur=10),
                     {"type": "chapter", "num": "CHAPTER 1", "title": "How dirty money gets clean", "at": 0.0, "dur": 1.6},
                     motion("FlowDiagram", {"nodes": [{"id": "a", "label": "DIRTY CASH", "x": 0.2, "y": 0.62, "w": 0.24},
                                                      {"id": "b", "label": "BANK DEPOSIT", "x": 0.44, "y": 0.34, "w": 0.24},
                                                      {"id": "c", "label": "WIRED AWAY", "x": 0.66, "y": 0.62, "w": 0.24},
                                                      {"id": "d", "label": "CLEAN MONEY", "x": 0.86, "y": 0.34, "w": 0.22, "color": "#d8f2df"}],
                                            "edges": [["a", "b"], ["b", "c"], ["c", "d"]], "step": 0.42}, at_=1.4)]})
S.append({"say": "And this bank's Mexican arm was taking in cash on a huge scale.", "transition": "cut",
          "camera": push(1.0, 1.06, 0.5, 0.5, 4),
          "layers": [plate("teller_wide", lit=True),
                     person("teller_wide", "extra", -0.8, -0.9, [["hold", 0], ["idle", 2.2]], COURIER,
                            walk=[(0, -3.0, -2.0), (1.6, -0.8, -0.9)]),
                     person("teller_wide", "ved", 1.3, -2.2, [["explain", 0], ["point", 1.6]], walk=[(0, 3.6, -2.8), (1.2, 1.3, -2.2)])],
          "sfx": "footsteps", "sfx_at": 0.0})
S.append({"say": "In 2007 and 2008, it shipped seven billion dollars in physical US cash north to the bank's US side.",
          "transition": "push", "transition_frames": 10,
          "layers": [plate("cash_table", blur=12),
                     motion("Stack3D", {"n": 34, "move": "rise", "every": 0.05}, x=0.66, y=0.5, w=0.68, h=1.0),
                     {"type": "hud", "label": "physical US dollars", "steps": [[0.3, 0], [0.4, 7]], "count_dur": 1.6, "prefix": "$",
                      "suffix": " BILLION", "indian": False, "tone": "gold", "x": 0.3, "y": 0.34, "enter": "pop", "width_of": "$7 BILLION"},
                     {"type": "dottext", "text": "2007 - 2008", "size": 40, "x": 0.3, "y": 0.5, "at": 1.0},
                     {"type": "tag", "text": "US SENATE REPORT, JULY 2012", "x": 0.3, "y": 0.6, "at": 1.4, "size": 22}]})
S.append({"say": "The route ran from Mexico and Colombia straight into the US banking system.", "transition": "cut",
          "layers": [plate("desk_ledger", blur=16),
                     motion("Hero3D", {"object": "globe", "arcs": [[24.8, -107.4, 40.7, -74.0], [19.4, -99.1, 40.7, -74.0],
                                                                   [4.7, -74.1, 40.7, -74.0]], "tone": "#e0b25a", "zoom": 0.72},
                            x=0.68, y=0.5, w=0.62, h=1.0),
                     {"type": "dottext", "text": "SINALOA (MX)\nNORTE DEL VALLE (CO)\n> US BANK", "size": 32, "x": 0.27, "y": 0.45,
                      "at": 0.6, "accent": "gold"}]})
S.append({"say": "From 2006 to 2010, at least eight hundred and eighty-one million dollars of drug money went through.",
          "caption": "2006-2010: at least $881 million", "transition": "whip", "transition_frames": 8,
          "layers": [plate("desk_ledger"), dict(BLINDS, phase=0.4),
                     {"type": "tiles", "n": 5, "labels": ["06", "07", "08", "09", "10"], "unit": "YEAR",
                      "progress": [[0.3, 1], [0.6, 2], [0.9, 3], [1.2, 4], [1.5, 5]], "x": 0.5, "y": 0.22, "w": 0.5, "at": 0.0},
                     motion("NumberSlam", {"text": "$881 MILLION", "label": "LAUNDERED THROUGH THE BANK", "y": 0.55, "roll": 0.8},
                            at_=1.6)]})
S.append({"say": "Prosecutors later called the bank's controls a record of dysfunction that was astonishing.",
          "transition": "cut", "camera": push(1.0, 1.06, 0.5, 0.5, 4),
          "layers": [plate("cloche_cash"), dict(BLINDS, phase=0.7),
                     {"type": "dottext", "text": "\"A RECORD OF DYSFUNCTION\"", "size": 52, "x": 0.5, "y": 0.16, "at": 0.4},
                     {"type": "tag", "text": "ASST. ATTORNEY GENERAL LANNY BREUER, 2012", "x": 0.5, "y": 0.25, "at": 1.4, "size": 22}]})
# ---------------------------------------------------------------- chapter 2
S.append({"say": "December 2012. The US Justice Department announces the deal.", "transition": "dip", "transition_frames": 10,
          "camera": push(1.0, 1.08, 0.5, 0.45, 4),
          "layers": [plate("courthouse", lit=True),
                     {"type": "chapter", "num": "CHAPTER 2", "title": "The bill", "at": 0.0, "dur": 1.4},
                     {"type": "dateline", "date": "11 DEC 2012", "place": "Brooklyn", "x": 0.28, "y": 0.24, "at": 1.4, "size": 90},
                     person("courthouse", "extra", -0.8, -2.2, [["idle", 0], ["happy", 2.4]], BANKER, walk=[(0, -0.4, 0.6), (2.0, -0.8, -2.2)])]})
S.append({"say": "HSBC pays one point nine two billion dollars.", "caption": "HSBC pays $1.92 billion",
          "transition": "cut",
          "layers": [plate("desk_case", blur=10),
                     motion("NumberSlam", {"text": "$1.92 BILLION", "label": "FORFEIT $1.256B + CIVIL PENALTIES $665M", "y": 0.46}),
                     {"type": "tag", "text": "US DEPT OF JUSTICE", "x": 0.86, "y": 0.92, "at": 1.4, "size": 22}]})
S.append({"say": "But the bank wasn't prosecuted. And no banker was charged.", "transition": "cut",
          "layers": [plate("courthouse", blur=12, lit=True),
                     {"type": "optcard", "label": "the bank", "text": "PROSECUTED?", "tone": "blue", "x": 0.3, "y": 0.4, "w": 0.32,
                      "verdict": "cross", "verdict_at": 0.6, "enter": "pop"},
                     {"type": "optcard", "label": "any banker", "text": "CHARGED?", "tone": "blue", "x": 0.7, "y": 0.4, "w": 0.32,
                      "verdict": "cross", "verdict_at": 1.6, "enter": "pop", "at": 0.9},
                     {"type": "stamp", "text": "NO CHARGES", "tone": "red", "angle": -7, "size": 110, "x": 0.5, "y": 0.72, "at": 2.2,
                      "sfx": "thud"}]})
S.append({"say": "Instead: a deferred prosecution agreement, and five years under a monitor.", "transition": "push",
          "transition_frames": 10,
          "layers": [plate("desk_ledger", blur=6), dict(BLINDS, phase=0.2),
                     {"type": "tiles", "n": 5, "unit": "YEAR", "progress": [[0.4, 1], [0.7, 2], [1.0, 3], [1.3, 4], [1.6, 5]],
                      "end": "DONE", "x": 0.5, "y": 0.6, "w": 0.6, "at": 0.2},
                     {"type": "dottext", "text": "DEFERRED PROSECUTION", "size": 54, "x": 0.5, "y": 0.22, "at": 0.1}]})
S.append({"dur": 1.6, "captions": False, "transition": "cut",
          "layers": [plate("cafe_mid", blur=12, base=C, keys=[{"t": 0, "scale": 1.3}]), dict(ved_close([["side_eye", 0]], x=0.5, h=1.0), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved", "text": "me after a ₹500 parking fine:\n*my life is over*",
                   "text_y": 0.2}})
S.append({"say": "Lesson one: it's why your bank now asks where your money comes from.", "transition": "cut",
          "layers": [plate("cafe_mid", blur=8, base=C, keys=[{"t": 0, "scale": 1.12}]),
                     ved_close([["explain", 0], ["point", 1.4]]),
                     {"type": "tipnum", "n": 1, "title": "KNOW YOUR\nCUSTOMER", "sub": "WHY BANKS ASK: SOURCE OF FUNDS", "plate": True, "x": 0.66, "y": 0.42,
                      "at": 0.2}]})
S.append({"say": "Next: how it stayed hidden for so long.", "transition": "whip", "transition_frames": 8, "min_dur": 2.8,
          "layers": [plate("laundry_door", blur=8),
                     motion("KineticTitle", {"lines": ["NEXT:", "HOW IT STAYED *HIDDEN*"], "size": 110, "y": 0.45, "style": "pop"})]})

job = {"id": ID, "kind": "long", "title": "SAMPLE: The Bank That Washed Cartel Cash (documentary opening)",
       "description": "Sample (not posted). Sources: US Department of Justice press release and Lanny Breuer remarks (11 Dec 2012); "
                      "US Senate Permanent Subcommittee on Investigations, HSBC case history (Jul 2012).",
       "tags": [], "privacy": "private", "speaker": "ved", "voice": {"speed": 1.03}, "assets_script": J + "assets.py",
       "chapters": [{"scene": 0, "title": "Cold open"}, {"scene": 4, "title": "How dirty money gets clean"}, {"scene": 10, "title": "The bill"}],
       "meta": {"format": "dark-files", "humour": {"beat": "side_eye", "scene": 14},
                "sources": ["https://www.justice.gov/archives/opa/pr/hsbc-holdings-plc-and-hsbc-bank-usa-na-admit-anti-money-laundering-and-sanctions-violations",
                            "https://www.justice.gov/opa/speech/assistant-attorney-general-lanny-breuer-speaks-hsbc-press-conference",
                            "https://www.hsgac.senate.gov/subcommittees/investigations/rep/hsbc-exposed-u-s-financial-system-to-money-laundering-drug-terrorist-financing-risks/"]},
       "music": {"cues": [{"scene": 0, "style": "tension", "key": "D", "scale": "minor", "bpm": 96},
                          {"scene": 4, "style": "doc", "key": "D", "scale": "minor", "bpm": 92},
                          {"scene": 10, "style": "tension", "key": "D", "scale": "minor", "bpm": 100}], "volume": 0.13},
       "scenes": S}
for sc in S:
    sc.pop("music_hit", None)
    if "say" in sc:
        sc.setdefault("pad", 0.1)
        sc.setdefault("lead", 0.04)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "words", sum(len(s.get("say", "").split()) for s in S))
