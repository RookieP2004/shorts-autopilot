"""Pilot v2 2026-11-16-pilot: the house style (Ved inside the 3D world, townspeople, captions, his normal voice, a comic beat)
WITH the reference-reel touches mixed in, not replacing anything (owner, 2026-11-16):
  - the label + condensed-headline system with one red accent on the key beats (instead of plain big text there)
  - real foley under the actions (cash, thud, splash/bubbles, stomp, paper slam)
  - a travelling camera: rack-focus open, push transitions, an iris that flies into the washer drum
  - stats as objects (a counter, bundles dropping), darker Dark-Files sets lit so Ved sits in them
Facts: US DOJ (Dec 2012), US Senate PSI report (Jul 2012).  v1 (full reference look) is build_job_v1.py.
Run: python jobs/2026-11-16-pilot/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-16-pilot"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("teller_wide", "laundry_wide", "cash_table", "courthouse")}

OUT = {   # recurring people: same outfit in every shot
    "courier": {"skin": "#c68a5e", "build": "regular", "hair": ["#1a1410", "short"], "hat": ["cap", "#2b2f2a"],
                "top": ["#3a3e48", "jacket"], "bottom": ["#2a2c33", "trousers"], "shoes": "#1a1410"},
    "counter1": {"skin": "#d9a27a", "build": "round", "hair": ["#2a2320", "short"], "top": ["#e9e6df", "vest"],
                 "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b"},
    "counter2": {"skin": "#8d5a3b", "build": "slim", "hair": ["#1a1410", "bun"], "top": ["#6b2f2f", "shirt"],
                 "bottom": ["#2a2c33", "trousers"], "shoes": "#25262b"},
    "banker": {"skin": "#e2b48c", "build": "regular", "hair": ["#9aa0a8", "short"], "top": ["#23262d", "jacket"],
               "bottom": ["#23262d", "trousers"], "shoes": "#111111", "tie": "#d63a2f"},
}


def plate(name, blur=0, lit=True, **k):
    return {"type": "image", "path": A + f"plate_{name}{'_lit' if lit else ''}.png", "x": 0.5, "y": 0.5, "w": 1.0,
            "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def head(label, text, at=0.1, y=0.13, **k):
    """Reference-reel headline: mono label box + condensed caps, one *red* word underlined."""
    return {"type": "headline", "label": label, "text": text, "y": y, "at": at, **k}


def person(set_, who, wx, wy, acting, walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    L.update(k)
    return L


def ved(set_, wx, wy, acting, walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    L.update(k)
    return L


def close_ved(acting, x=0.5, y=0.8, h=1.06, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def staged(set_, people=(), extra_top=(), **pk):
    out = [plate(set_, **pk)] + sorted(people, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 84'><rect x='4' y='4' width='292' height='76' rx='38' "
           f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
           f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
           f"<text x='172' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")
    return {"type": "image", "svg": svg, "x": x, "y": y, "w": 0.24, "enter": "pop", "at": at, "sfx": "click"}


def step_card(t, color="#1a1410"):
    return card(f"<text x='170' y='96' text-anchor='middle' font-size='72' fill='{color}' {AN}>{t}</text>", 340, 140)


S = []
# 0. hook: teller hall; a courier slides a box onto the counter, Ved walks in. Rack-focus open.
S.append({"say": "Drug cartels built cardboard boxes to fit a bank's *teller window*.",
          "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.08, "focus": [0.48, 0.52]}]},
          "layers": staged("teller_wide", blur_keys=[[0, 9], [0.9, 0]],
                           people=[person("teller_wide", "courier", -0.7, -0.75, [["hold", 0], ["idle", 2.2]],
                                          walk=[(0, -2.4, -1.6), (1.4, -0.7, -0.75)]),
                                   ved("teller_wide", 1.1, -2.3, [["welcome", 0], ["point", 2.0], ["surprised", 3.4]],
                                       walk=[(0, 3.4, -2.8), (1.3, 1.1, -2.3)])],
                           extra_top=[head("HSBC Mexico · 2006-2010", "BOXES BUILT TO FIT\nTHE *TELLER WINDOW*", at=0.0)]),
          "sfx": "footsteps", "sfx_at": 0.1})
# 1. teller close cutaway: the box, cash landing on the counter
S.append({"say": "Stuffed with cash. Hundreds of thousands of dollars, in a *single day*.",
          "transition": "push", "transition_frames": 12, "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.0, "zoom": 1.06, "focus": [0.48, 0.56]}]},
          "layers": [plate("teller_close"),
                     sprite("bundle", 0.66, 0.56, 0.22, enter="drop", at=0.6, sfx="thud", rotate=-6),
                     sprite("bundle", 0.8, 0.575, 0.22, enter="drop", at=1.0, sfx="thud", rotate=8),
                     sprite("bundle", 0.73, 0.535, 0.22, enter="drop", at=1.4, sfx="cash", rotate=2),
                     {"type": "image", "svg": card(f"<text x='460' y='98' text-anchor='middle' font-size='60' fill='#d63a2f' {AN}>ONE ACCOUNT. ONE DAY.</text>", 920, 140),
                      "x": 0.5, "y": 0.2, "w": 0.78, "rotate": -3, "enter": "pop", "at": 2.0, "sfx": "pop"}]})
# 2. laundromat: Ved walks to the glowing washer; iris flies us into the drum
S.append({"say": "Dirty money needs a wash. In, spin it around, and out comes *clean* money.",
          "transition": "push", "transition_frames": 12, "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.0, "zoom": 1.08, "focus": [0.52, 0.45]}]},
          "layers": staged("laundry_wide",
                           people=[ved("laundry_wide", 1.0, -1.05, [["welcome", 0], ["point", 1.3]],
                                       walk=[(0, 2.4, -1.5), (1.1, 1.0, -1.05)])],
                           extra_top=[plate("laundry_door", lit=False,
                                            iris={"x": 0.5, "y": 0.47, "r0": 0.0, "r1": 0.8, "at": 2.0, "dur": 0.9}),
                                      head("Money laundering", "DIRTY IN.\n*CLEAN* OUT.", at=0.1),
                                      {"type": "image", "svg": step_card("IN"), "x": 0.22, "y": 0.75, "w": 0.26, "rotate": -4,
                                       "enter": "pop", "at": 2.6, "sfx": "splash"},
                                      {"type": "image", "svg": step_card("SPIN"), "x": 0.5, "y": 0.78, "w": 0.26, "rotate": 3,
                                       "enter": "pop", "at": 3.3, "sfx": "bubbles"},
                                      {"type": "image", "svg": step_card("OUT", "#2f8f5a"), "x": 0.78, "y": 0.75, "w": 0.26, "rotate": -2,
                                       "enter": "pop", "at": 4.0, "sfx": "pop"}]),
          "sfx": "drone", "sfx_at": 1.8})
# 3. counting room: $7 billion counter, people counting, Ved points
S.append({"say": "HSBC Mexico shipped *seven billion* dollars in cash to the US in just two years.",
          "caption": "HSBC Mexico shipped *$7 billion* in cash to the US in just two years.",
          "transition": "cut", "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.6, "zoom": 1.06, "focus": [0.5, 0.58]}]},
          "layers": staged("cash_table",
                           people=[ved("cash_table", 0.75, -1.25, [["explain", 0], ["point", 1.0], ["surprised", 3.2]])],
                           extra_top=[head("US Senate report · 2012", "IN PHYSICAL DOLLARS", at=0.1, y=0.19),
                                      {"type": "counter", "from": 0, "to": 7, "decimals": 0, "prefix": "$", "suffix": " BILLION",
                                       "x": 0.5, "y": 0.1, "size": 130, "font": "fonts/Anton-Regular.ttf", "color": "accent", "at": 0.2, "count_dur": 1.6, "enter": "none",
                                       "stroke": "#0b0f12", "stroke_width": 8, "sfx": "tick"},
                                      tag_layer(0.5, 0.31, 2.4)])})
# 4. cash close: traced to two cartels; three bundles slam down
S.append({"say": "At least *881 million* came from two cartels, Sinaloa and Norte del Valle.",
          "caption": "At least *$881 million* came from two cartels, Sinaloa and Norte del Valle.",
          "transition": "push", "transition_frames": 12, "caption_y": 0.64,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.6, "zoom": 1.08, "focus": [0.5, 0.6]}]},
          "layers": [plate("cash_close"),
                     head("US Justice Department", "*$881 MILLION*\nFROM TWO CARTELS", at=0.1),
                     sprite("bundle", 0.28, 0.5, 0.3, enter="drop", at=1.2, sfx="thud", rotate=-8),
                     sprite("bundle", 0.7, 0.54, 0.3, enter="drop", at=1.6, sfx="thud", rotate=6),
                     sprite("bundle", 0.5, 0.46, 0.32, enter="drop", at=2.0, sfx="cash", rotate=-3),
                     tag_layer(0.5, 0.36, 2.8)]})
# 5. comic beat: side-eye ("looks fine to me")
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("teller_wide", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved",
                   "text": "the bank, seeing boxes of cash daily:\n*looks normal*", "text_y": 0.2}})
# 6. courthouse: the fine vs zero jailed; the banker walks off free
S.append({"say": "The bank paid *1.9 billion* dollars. Bankers sent to prison? *Zero.*",
          "caption": "The bank paid *$1.9 billion*. Bankers sent to prison? *Zero.*",
          "transition": "push", "transition_frames": 12, "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.07, "focus": [0.5, 0.55]}]},
          "layers": staged("courthouse",
                           people=[person("courthouse", "banker", -0.6, -2.0, [["idle", 0], ["happy", 3.2]],
                                          walk=[(0, -0.3, 0.8), (2.2, -0.6, -2.0)]),
                                   ved("courthouse", 1.6, -3.4, [["explain", 0], ["shrug", 2.6], ["crossed", 3.6]],
                                       walk=[(0, 3.6, -4.0), (1.0, 1.6, -3.4)])],
                           extra_top=[head("December 2012", "$1.9 BILLION PAID.\n*0* JAILED.", at=0.1)]),
          "sfx": "stomp", "sfx_at": 3.4})
# 7. why it matters to you: the source-of-funds form slams onto the desk
S.append({"say": "That's why your bank now asks... where your money *comes from*.",
          "transition": "cut", "caption_y": 0.36,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 3.6, "zoom": 1.06, "focus": [0.45, 0.6]}]},
          "layers": [plate("desk"),
                     {"type": "paper", "kind": "doc", "title": "SOURCE OF FUNDS", "text": "Where does this money come from? ____________",
                      "w": 0.52, "x": 0.42, "y": 0.6, "rotate": -6, "at": 0.4, "enter": "slam", "sfx": "paper", "tape": []},
                     close_ved([["explain", 0], ["point", 1.4]], x=0.8, y=0.88, h=0.72),
                     head("Know your customer", "“SOURCE OF *FUNDS?*”", at=0.1)]})
# 8. share prompt (house close-up), the reference's "send this to..." ending
S.append({"say": "Send this to someone who thinks banks are *boring*.",
          "transition": "cut", "caption_y": 0.64, "min_dur": 3.0,
          "layers": [plate("teller_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.5, "scale": 1.42}]),
                     close_ved([["point", 0], ["smirk", 2.0]]),
                     head("Send this", "TO SOMEONE WHO THINKS\nBANKS ARE *BORING*", at=0.1)]})

job = {
    "id": ID,
    "title": "Cartels built boxes to fit a bank's window \U0001f4e6",
    "description": "Mexican drug cartels used boxes designed to fit HSBC Mexico's teller windows. What happened next, and why your "
                   "bank now asks where your money comes from.\n\nSources: US Department of Justice, HSBC deferred prosecution "
                   "announcement (Dec 2012); US Senate Permanent Subcommittee on Investigations, HSBC case history (Jul 2012).",
    "tags": ["money laundering", "hsbc", "cartels", "dark files", "true crime", "banking", "explained"],
    "hashtags": ["#truecrime", "#moneylaundering"],
    "instagram": {"hashtags": ["#truecrime", "#moneylaundering", "#hsbc", "#cartel", "#explained"]},
    "meta": {"format": "dark-files", "topic": "HSBC and the cartel cash boxes (money laundering explained)", "hook": "story",
             "idea_source": "owner request: reference-reel style mixed into the house style; dark-files backlog",
             "characters": ["ved", "extra"],
             "overrides": "pilot v2: house style + reference touches (headline system, foley, push/iris camera, counters)",
             "sources": ["https://www.justice.gov/opa/speech/assistant-attorney-general-lanny-breuer-speaks-hsbc-press-conference",
                         "https://www.hsgac.senate.gov/subcommittees/investigations/rep/hsbc-exposed-u-s-financial-system-to-money-laundering-drug-terrorist-financing-risks/",
                         "https://www.foxbusiness.com/markets/hsbc-became-bank-to-drug-cartels-pays-big-for-lapses"],
             "claims": [{"claim": "traffickers used boxes designed to fit HSBC Mexico teller windows", "tag": "PROVEN", "source": "DOJ 2012"},
                        {"claim": "hundreds of thousands of dollars in cash in a single day, into a single account", "tag": "PROVEN", "source": "DOJ 2012"},
                        {"claim": "HSBC Mexico shipped $7B in physical US dollars to HSBC US in 2007-2008", "tag": "PROVEN", "source": "Senate PSI 2012"},
                        {"claim": "at least $881M laundered by the Sinaloa and Norte del Valle cartels (2006-2010)", "tag": "PROVEN", "source": "DOJ 2012"},
                        {"claim": "$1.92B total ($1.256B forfeiture + $665M civil); no bank or executive indicted", "tag": "PROVEN", "source": "DOJ/Reuters 2012"}],
             "humour": {"trend": "side-eye 'looks normal to me' cut-away", "beat": "side_eye", "scene": 5}},
    "thumbnail": {"title": "WHY THESE *BOXES?*", "title_y": 0.15, "title_size": 180, "max_w": 0.95, "blur": 14,
                  "glow": "#ffcf5a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.3, "bg_saturation": 1.3,
                  "bg": [plate("teller_close")],
                  "fg": [sprite("box", 0.72, 0.55, 0.42), sprite("bundle", 0.25, 0.4, 0.28, rotate=-12),
                         {"type": "character", "id": "ved", "pose": "surprised", "x": 0.4, "y": 0.93, "h": 0.95, "enter": "none",
                          "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
    "privacy": "private", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
for sc in S:
    if "say" in sc:
        sc.setdefault("pad", 0.14); sc.setdefault("lead", 0.06)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "words", sum(len(s.get("say", "").split()) for s in S))
