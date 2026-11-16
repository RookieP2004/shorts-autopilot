"""PILOT 2026-11-16-n: the night-set look (owner, 2026-11-16) on survivorship bias in stock-tip channels.
House style kept: Ved and townspeople, his normal voice, a comic beat; the night mood is the opt-in second look.
New pieces used: night plates (one hard spot, blue rim, Dutch tilt), rim light on Ved, highlight captions, hud chips,
equation bar, step tracker, option cards with cross/tick, rubber stamp, glossy phone with a live fictional screen,
crowd-as-data (8,000 -> 1,000 on the set floor, Ved walking through it), a 3D node tree, cash burst (NOT REAL MONEY).
Documentary, never a how-to: we show why a perfect streak proves nothing; no tips, no channel names, no steps to run it.
Facts: the 'Baltimore stockbroker' parable (Paulos 1988, Ellenberg 2014 - who notes no confirmed real case, so we call it
a maths trick, not a documented Telegram scam); SEBI: no paid advice without IA/RA registration; SEBI final order
5 Feb 2026 (Unison Metals, Telegram tips, Rs 4.29 crore unlawful gains).
Run: python jobs/2026-11-16-n/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-16-n"
J = f"jobs/{ID}/"
A = J + "assets/"
P = {n: A + f"plate_{n}.json" for n in ("arena_wide", "arena_mid", "arena_hero")}
ST = {n: Stage(p) for n, p in P.items()}
AREA = [-3.6, 3.6, -2.4, 3.2]
NOTES = [A + "note1.png", A + "note2.png", A + "coin.png"]
CLUB = "Multibagger Club"            # fictional


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def ved(set_, wx, wy, acting, walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    L.update(k)
    return L


def extra(set_, wx, wy, acting, outfit, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    return {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
            "acting": acting, "talk": False, "rig_args": {"outfit": outfit}, "allow_outside_safe": True, **k}


def close_ved(acting, x=0.5, y=0.8, h=1.06, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def crowd(plate_name, steps, **k):
    return {"type": "crowd", "plate": P[plate_name], "area": AREA, "n": k.pop("n", 2600), "fig_h": 0.3, "seed": 4,
            "color": "#b9c2d3", "steps": steps, **k}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", **k}


VIEWER = {"skin": "#c68a5e", "build": "regular", "hair": ["#1a1410", "short"], "top": ["#2f3a52", "jacket"],
          "bottom": ["#23262d", "trousers"], "shoes": "#151515"}
TIPS = {"kind": "tips", "name": CLUB, "sub": "8,000 members · FREE calls",
        "rows": [{"label": "CALL 1", "text": "Stock A will go UP", "badge": "HIT", "at": 0.5},
                 {"label": "CALL 2", "text": "Stock B will go UP", "badge": "HIT", "at": 1.3},
                 {"label": "CALL 3", "text": "Stock C will go UP", "badge": "HIT", "at": 2.1}]}
PAY = {"kind": "pay", "name": CLUB, "sub": "VIP", "title": "VIP ACCESS", "note": "Only 12 seats left", "price": "₹4,999",
       "countdown": 588, "button": "PAY NOW"}
LOCK = {"kind": "lock", "time": "9:41", "date": "Monday, market day",
        "notes": [{"app": CLUB, "title": "3/3 calls HIT",
                   "body": "You're selected for VIP. Seats close tonight.", "at": 0.4}]}

S = []
# 0. hook: the perfect record on a phone; a townsperson reads it, Ved walks in under the spot
S.append({"say": "This Telegram tip channel called three stocks in a row. All three went up.",
          "layers": [plate("arena_hero"),
                     ved("arena_hero", 1.0, -1.2, [["welcome", 0], ["point", 1.6]], walk=[(0, 2.4, -1.6), (1.1, 1.0, -1.2)]),
                     {"type": "phone", "sprite": A + "phone.png", "screen": TIPS, "x": 0.34, "y": 0.43, "w": 0.42,
                      "tilt": [[0, -22, 6], [3.5, 12, 2]], "enter": "rise", "at": 0.1, "sfx": "swoosh_soft",
                      "loop": "float"},
                     {"type": "tracker", "n": 3, "done": [0.6, 1.4, 2.2], "x": 0.36, "y": 0.75, "at": 0.0, "enter": "fade"}],
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.06, "focus": [0.45, 0.48]}]},
          "sfx": "footsteps", "sfx_at": 0.0})
# 1. the crowd appears: 8,000 people; Ved stands at the edge for scale
S.append({"say": "Genius? Nope. It starts with eight thousand people.",
          "layers": [plate("arena_wide"), crowd("arena_wide", [], in_dur=1.4),
                     ved("arena_wide", 2.9, -3.4, [["explain", 0], ["point", 1.2]]),
                     hud("people in the channel", to=8000, count_dur=1.4, tone="blue", at=0.3)]})
# 2. split: half hear "rise", half hear "fall"
S.append({"say": "Half are told a stock will rise. Half are told it'll fall.",
          "transition": "cut",
          "layers": [plate("arena_wide"),
                     crowd("arena_wide", [{"at": 0.4, "split": "x", "colors": ["blue", "violet"]}], in_dur=0),
                     ved("arena_wide", 2.9, -3.4, [["explain", 0], ["shrug", 2.0]]),
                     {"type": "optcard", "label": "group A", "text": "STOCK\nWILL RISE", "tone": "blue", "x": 0.27, "y": 0.27,
                      "w": 0.4, "enter": "pop", "at": 0.5, "sfx": "pop", "rotate": -3},
                     {"type": "optcard", "label": "group B", "text": "STOCK\nWILL FALL", "tone": "violet", "x": 0.73, "y": 0.27,
                      "w": 0.4, "enter": "pop", "at": 1.6, "sfx": "pop", "rotate": 3},
                     hud("each group", value=4000, tone="blue", at=0.6, y=0.74)]})
# 3. the market rises: group B fades out; 4,000 saw a correct call
S.append({"say": "Either way, four thousand people just saw a correct call.",
          "transition": "cut",
          "layers": [plate("arena_wide"),
                     crowd("arena_wide", [{"at": 0, "dur": 0, "split": "x", "colors": ["blue", "violet"]},
                                          {"at": 0.5, "keep": 0, "lost": "red"}], in_dur=0),
                     ved("arena_wide", 2.9, -3.4, [["point", 0], ["surprised", 1.4]]),
                     {"type": "optcard", "label": "group A", "text": "STOCK\nWILL RISE", "tone": "blue", "x": 0.27, "y": 0.27,
                      "w": 0.4, "enter": "none", "rotate": -3, "verdict": "tick", "verdict_at": 0.5, "sfx": "ding", "sfx_at": 0.5},
                     {"type": "optcard", "label": "group B", "text": "STOCK\nWILL FALL", "tone": "violet", "x": 0.73, "y": 0.27,
                      "w": 0.4, "enter": "none", "rotate": 3, "verdict": "cross", "verdict_at": 0.5},
                     hud("saw a correct call", steps=[[0, 8000], [0.7, 4000]], tone="green", y=0.74),
                     {"type": "tracker", "n": 3, "done": [0.9], "x": 0.5, "y": 0.84, "enter": "none", "allow_outside_safe": True}]})
# 4. repeat twice; Ved walks through the crowd as it shrinks; the equation builds
WALK = [(0, 1.8, 2.2), (3.6, 1.8, -1.6)]
S.append({"say": "Repeat. Two thousand. Then one thousand... with a perfect record.",
          "caption": "Repeat. 2,000. Then 1,000... with a perfect record.",
          "transition": "push", "transition_frames": 12, "min_dur": 4.8,
          "layers": [plate("arena_mid"),
                     crowd("arena_mid", [{"at": 0, "dur": 0, "split": "x", "colors": ["blue", "violet"]}, {"at": 0, "keep": 0, "lost_alpha": 0.0, "dur": 0},
                                         {"at": 0.4, "split": "y", "colors": ["blue", "violet"]}, {"at": 1.1, "keep": 0},
                                         {"at": 1.9, "split": "x", "colors": ["blue", "violet"]}, {"at": 2.6, "keep": 0},
                                         {"at": 3.3, "glow": "green"}],
                           in_dur=0, aisle=[1.8, 0.5], n=3200, area=[0.0, 7.2, -2.4, 3.2]),
                     ved("arena_mid", 1.8, 2.2, [["explain", 0], ["point", 2.0], ["surprised", 3.4]], walk=WALK),
                     hud("still “winning”", steps=[[0, 4000], [1.1, 2000], [2.6, 1000]], tone="green", y=0.2, width_of="8,000"),
                     {"type": "eqbar", "keys": [[0.2, "8,000 ÷ 2"], [1.1, "8,000 ÷ 2 ÷ 2"], [2.6, "8,000 ÷ 2 ÷ 2 ÷ 2"],
                                                [3.4, "8,000 ÷ 2^3 = *1,000*"]], "x": 0.5, "y": 0.29, "enter": "fade"},
                     {"type": "tracker", "n": 3, "done": [0, 1.2, 2.7], "x": 0.5, "y": 0.75, "enter": "none"}],
          "sfx": "footsteps", "sfx_at": 0.0})
# 5. the survivors (3D crowd still) and the trap: the VIP fee
S.append({"say": "Now comes the VIP fee.",
          "transition": "cut", "min_dur": 2.6,
          "layers": [plate("crowd_survivors"),
                     hud("saw 3 out of 3", value=1000, tone="green", y=0.24),
                     {"type": "phone", "sprite": A + "phone.png", "screen": PAY, "x": 0.5, "y": 0.62, "w": 0.5,
                      "tilt": [[0, 18, 4], [2.5, -6, 0]], "enter": "rise", "at": 0.2, "sfx": "swoosh_soft"},
                     {"type": "stamp", "text": "THE TRAP", "tone": "red", "angle": -9, "size": 130, "x": 0.5, "y": 0.42,
                      "at": 1.1, "sfx": "thud"}],
          "camera": {"shake": [1.1, 0.25]}})
# 6. the maths of the payout (fictional notes)
S.append({"say": "Two hundred pay? That's ten lakh rupees. From coin tosses.",
          "caption": "200 pay? That's ₹10 lakh. From coin tosses.",
          "transition": "cut",
          "layers": [plate("arena_hero"),
                     extra("arena_hero", -0.8, -0.3, [["hold", 0], ["sad", 2.4]], VIEWER),
                     extra("arena_hero", -0.2, 0.9, [["hold", 0], ["sad", 2.6]], dict(VIEWER, top=["#5b2f3a", "jacket"], build="slim")),
                     ved("arena_hero", 1.0, -1.2, [["explain", 0], ["surprised", 1.4], ["shrug", 2.8]]),
                     {"type": "burst", "sprites": NOTES, "n": 26, "origin": [0.45, 0.62], "at": 1.0, "dur": 2.2, "spread": 1.1, "sfx": "cash", "sizes": [1.0, 1.0, 0.45]},
                     hud("if 200 people pay", steps=[[0, 0], [0.9, 999800]], prefix="₹", tone="gold", y=0.27, count_dur=1.0,
                         width_of="₹9,99,800"),
                     {"type": "eqbar", "keys": [[0.4, "200 × ₹4,999"], [1.8, "200 × ₹4,999 ≈ *₹10 lakh*"]],
                      "tone": "gold", "x": 0.5, "y": 0.37, "enter": "fade"},
                     {"type": "stamp", "text": "NOT REAL MONEY", "tone": "gold", "angle": -4, "size": 46, "x": 0.5, "y": 0.45, "at": 1.3}]})
# 7. comic beat
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("arena_hero", blur=12, keys=[{"t": 0, "scale": 1.3}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved",
                   "text": "me after ONE lucky trade:\n*i'm basically a fund manager*", "text_y": 0.2}})
# 8. survivorship bias: the tree of 8,000 coin tosses; only one branch is ever shown
NODES = [{"id": "r", "pos": [0, 1.7, 0], "at": 0.2, "tone": "blue", "label": "8,000"},
         {"id": "a", "pos": [-1.4, 0.6, 0.3], "at": 0.6, "tone": "green", "label": "4,000"},
         {"id": "b", "pos": [1.4, 0.6, -0.3], "at": 0.6, "tone": "red"},
         {"id": "c", "pos": [-2.1, -0.5, 0.6], "at": 1.0, "tone": "red"},
         {"id": "d", "pos": [-0.6, -0.5, 0.0], "at": 1.0, "tone": "green", "label": "2,000"},
         {"id": "e", "pos": [-1.1, -1.6, 0.4], "at": 1.4, "tone": "red"},
         {"id": "f", "pos": [0.2, -1.6, -0.2], "at": 1.4, "tone": "green", "label": "1,000"}]
S.append({"say": "That's survivorship bias. You only ever see the lucky branch.",
          "transition": "dip", "transition_frames": 10,
          "layers": [plate("arena_hero", blur=14),
                     {"type": "nodes", "nodes": NODES, "x": 0.5, "y": 0.44, "yaw": [-18, 12],
                      "edges": [["r", "a", 0.6, "green"], ["r", "b", 0.6, "red"], ["a", "c", 1.0, "red"], ["a", "d", 1.0, "green"],
                                ["d", "e", 1.4, "red"], ["d", "f", 1.4, "green"]]},
                     close_ved([["explain", 0], ["point", 1.6]], x=0.84, y=0.9, h=0.62),
                     {"type": "stamp", "text": "SURVIVORSHIP BIAS", "tone": "gold", "angle": -6, "size": 70, "x": 0.42, "y": 0.73,
                      "at": 2.2, "sfx": "thud"}]})
# 9. what is real: SEBI rules + a real case
S.append({"say": "Paid stock tips need SEBI registration. Check it before you pay.",
          "transition": "cut",
          "layers": [plate("arena_hero"),
                     ved("arena_hero", 1.0, -1.2, [["explain", 0], ["point", 1.4]]),
                     {"type": "optcard", "label": "before you pay", "text": "CHECK THE SEBI\nREG. NUMBER", "tone": "green",
                      "x": 0.35, "y": 0.3, "w": 0.6, "enter": "pop", "at": 0.3, "verdict": "tick", "verdict_at": 1.2, "sfx": "pop"},
                     hud("SEBI order · Feb 2026", text="₹4.29 crore", tone="red", y=0.73, at=1.6,
                         sub="unlawful gains via Telegram stock tips")]})
# 10. payoff on the viewer's lock screen
S.append({"say": "Got a message like this? Comment YES or NO.",
          "transition": "push", "transition_frames": 12, "min_dur": 3.2,
          "layers": [plate("arena_hero", blur=16),
                     {"type": "phone", "sprite": A + "phone.png", "screen": dict(LOCK, cta="Comment YES or NO", cta_at=1.2),
                      "x": 0.5, "y": 0.5, "w": 0.6, "tilt": [[0, 8, 6], [3.0, -3, 2]], "enter": "rise", "at": 0.0,
                      "sfx": "ding", "sfx_at": 0.4, "allow_outside_safe": True},
                     close_ved([["point", 0], ["smirk", 2.0]], x=0.85, y=0.92, h=0.5)]})

job = {
    "id": ID,
    "title": "How a stock tip channel gets a perfect record \U0001f4c9",
    "description": "Three calls in a row, all correct. Genius, or maths? The split-list trick (the old 'Baltimore stockbroker' "
                   "parable) and survivorship bias, explained.\n\nSources: Jordan Ellenberg, How Not to Be Wrong (2014); "
                   "John Allen Paulos, Innumeracy (1988); SEBI (Investment Advisers) Regulations and SEBI investor cautions; "
                   "SEBI final order in the matter of stock recommendation tips in Unison Metals Ltd (5 Feb 2026).",
    "tags": ["survivorship bias", "stock tips", "telegram", "sebi", "scam", "stock market", "explained"],
    "hashtags": ["#stockmarket", "#scamalert"],
    "instagram": {"hashtags": ["#stockmarket", "#scamalert", "#survivorshipbias", "#sebi", "#explained"]},
    "look": "night",
    "meta": {"format": "dark-files", "topic": "Why a perfect tip streak proves nothing (split-list trick, survivorship bias)",
             "hook": "question", "idea_source": "owner request: night-set style pilot",
             "characters": ["ved", "extra"], "overrides": "PILOT of the night-set look (2026-11-16)",
             "sources": ["https://www.sebi.gov.in/enforcement/orders/feb-2026/final-order-in-the-matter-of-stock-recommendation-tips-in-the-scrip-of-unison-metals-ltd-_99518.html",
                         "https://www.business-standard.com/article/pti-stories/sebi-cautions-public-against-unregistered-investment-advisors-116060900804_1.html",
                         "https://ofdollarsanddata.com/scams-damn-scams-and-investors/"],
             "claims": [{"claim": "split-list maths: 8,000 halved 3 times = 1,000 with a perfect 3/3 record", "tag": "PROVEN", "source": "arithmetic"},
                        {"claim": "the 'Baltimore stockbroker' is a classic parable (Paulos, Ellenberg); no confirmed real case of the exact trick", "tag": "PROVEN", "source": "Ellenberg 2014"},
                        {"claim": "no person can act as an investment adviser / research analyst without SEBI registration", "tag": "PROVEN", "source": "SEBI IA & RA Regulations"},
                        {"claim": "SEBI final order 5 Feb 2026: Telegram stock tips in Unison Metals, Rs 4.29 crore unlawful gains", "tag": "PROVEN", "source": "SEBI order"},
                        {"claim": "200 x Rs 4,999 = Rs 9,99,800 (about Rs 10 lakh)", "tag": "PROVEN", "source": "arithmetic (illustrative fee)"}],
             "humour": {"trend": "side-eye 'basically a fund manager'", "beat": "side_eye", "scene": 7}},
    "thumbnail": {"title": "3/3 CORRECT. *HOW?*", "title_y": 0.14, "title_size": 170, "max_w": 0.95, "blur": 10,
                  "glow": "#35e08a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.2, "bg_saturation": 1.2,
                  "bg": [plate("crowd_survivors")],
                  "fg": [{"type": "phone", "sprite": A + "phone.png", "screen": TIPS, "x": 0.32, "y": 0.6, "w": 0.48,
                          "tilt": [[0, -14, 4]], "enter": "none"},
                         {"type": "character", "id": "ved", "pose": "surprised", "x": 0.74, "y": 0.92, "h": 0.8, "enter": "none",
                          "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
    "music": {"cues": [{"scene": 0, "style": "tension", "key": "E", "scale": "minor", "bpm": 92},
                       {"scene": 8, "style": "doc", "key": "E", "scale": "minor"}], "volume": 0.12},
    "privacy": "private", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
for sc in S:
    if "say" in sc:
        sc.setdefault("pad", 0.14); sc.setdefault("lead", 0.06)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "words", sum(len(s.get("say", "").split()) for s in S))
