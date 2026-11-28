"""2026-11-28-b: "Australia lost a war to emus" (wild-story; Librarian Ved pulls the 1932 file). Explain mode: versus
(Army vs Emus, a running scoreboard). Lane: history's wild stories.
Styles mixed: animated Blender shots (moving 3D: emus charging a low camera through the wheat, the mob scattering from
above, an army truck chasing and losing), Ved's library plates (3D set, Librarian Ved + a reader), a Reelsmith RS-14 Silent
Card (1932 intertitle), an RS-03 Balance (3 soldiers vs 20,000 emus), hud chips + eqbar, a stamp, the comic beat.
Facts (verified 2026-11-28; Wikipedia "Emu War", Britannica "Emu War", History Hit):
- Nov-Dec 1932, Campion district, Western Australia; ~20,000 emus on the wheat farms.
- Major G. P. W. Meredith (Royal Australian Artillery) + two soldiers (3 men), two Lewis guns, 10,000 rounds.
- The emus split into small groups and ran; a gun jammed; a gun on a truck couldn't catch them, too bumpy to fire.
- Meredith's report: 986 kills with 9,860 rounds = exactly 10 rounds per confirmed kill (his claim of 2,500 more dying of
  wounds is disputed, so not used).
- Meredith: "They can face machine guns with the invulnerability of tanks."
- The military withdrew (Dec 1932); bounties (57,034 claimed in six months of 1934) and exclusion fencing did the job;
  the emus were "considered the victors" (Britannica).
Run after the assets exist: python jobs/2026-11-28-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-28-b"
J = f"jobs/{ID}/"
A = J + "assets/"
SH = J + "shots/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("lib_wide", "lib_desk", "lib_low")}
OUT = {"reader": {"skin": "#c68a5e", "build": "slim", "hair": ["#5a3a22", "long"], 
                  "top": ["#2f5a7a", "jacket"], "bottom": ["#3a3530", "skirt"], "shoes": "#25262b"}}


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def shot(script, dur, samples=16, res=0.45):
    return {"dur": dur, "type": "blender", "script": SH + script, "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "enter": "none",
            "fps": 15, "res": res, "samples": samples}


def txt(t, y, size=92, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def hud(label, text, tone, at=0.4, y=0.13):
    return {"type": "hud", "label": label, "text": text, "x": 0.5, "y": y, "at": at, "enter": "pop", "sfx": "click", "tone": tone}


def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def person(set_, who, wx, wy, acting, walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"],
         "enter": "none", "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


S = []
# 0. hook (moving 3D): a mob of emus charges a low camera through the wheat; the versus title at frame 0
S.append({"say": "In 1932, Australia's army fought *emus*. And lost.",
          "layers": [shot("a_hook.py", 4.6),
                     txt("ARMY *VS* EMUS", 0.15, 120, enter="none")]})
# 1. library wide: Librarian Ved walks down the aisle with the file; a reader looks up
S.append({"say": "True story. I pulled the file.",
          "transition": "slide_left", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.07, "focus": [0.5, 0.5]}]},
          "layers": [plate("lib_wide"),
                     person("lib_wide", "reader", 1.3, 6.2, [["idle", 0], ["surprised", 1.0]]),
                     ved("lib_wide", -0.3, 1.2, [["idle", 0], ["point", 1.0]],
                         walk=[(0, 0.1, 3.0), (1.2, -0.3, 1.2)])]})
# 2. RS-14 silent card: the date and the place
S.append({"say": "Emus ate the wheat. The army sent *machine guns*.",
          "transition": "dip", "captions": True, "caption_y": 0.74, "pad": 0.6,
          "layers": [{"type": "image", "path": J + "out/shots/s00_l00/0060.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none",
                      "blur": 10, "keys": [{"t": 0, "scale": 1.15}, {"t": 4.0, "scale": 1.25}]},
                     {"type": "look", "look": "RS-14", "x": 0.5, "y": 0.4, "w": 0.88, "h": 0.5, "at": 0.0,
                      "props": {"lines": ["NOVEMBER 1932", "Western Australia", "20,000 emus vs. the wheat"], "level": 1,
                                "strength": 0.6}}]})
# 3. RS-03 balance: the odds
S.append({"say": "Three soldiers versus *twenty thousand* birds.",
          "transition": "zoom", "caption_y": 0.74, "pad": 0.7,
          "layers": [plate("lib_low", blur=14, keys=[{"t": 0, "scale": 1.1}, {"t": 4.0, "scale": 1.18}]),
                     {"type": "look", "look": "RS-03", "x": 0.5, "y": 0.4, "w": 0.92, "h": 0.6, "at": 0.0,
                      "props": {"title": "THE ODDS", "left": {"label": "SOLDIERS", "value": 3},
                                "right": {"label": "EMUS", "value": 20000}, "verdict": "EMUS",
                                "backdrop": "dim"}}]})
# 4. moving 3D: round one, the mob scatters
S.append({"say": "Round one: the emus split up and *scattered*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("b_scatter.py", 3.4), hud("round 1", "EMUS 1 - ARMY 0", "green", at=1.2)]})
# 5. moving 3D: round two, the truck loses the race
S.append({"say": "Round two: a gun on a truck. The emus *outran* it.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("c_truck.py", 4.0), hud("round 2", "EMUS 2 - ARMY 0", "green", at=2.0)]})
# 6. desk close: Ved and the ledger, the count
S.append({"say": "His own report: *ten* bullets per bird.",
          "transition": "cut", "caption_y": 0.72, "pad": 0.4,
          "layers": [plate("lib_desk", keys=[{"t": 0, "scale": 1.0}, {"t": 4.5, "scale": 1.07}]),
                     hud("Meredith's report", "986 EMUS HIT", "gold", at=0.2, y=0.12),
                     {"type": "eqbar", "x": 0.5, "y": 0.2, "at": 0.3, "tone": "gold",
                      "keys": [[0.0, "9,860 bullets ÷ 986"], [1.3, "9,860 ÷ 986 = *10* each"]]}]})
# 7. low angle: the quote
S.append({"say": "The major said they faced machine guns like *tanks*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.1, "focus": [0.42, 0.5]}, {"t": 3.2, "zoom": 1.1, "focus": [0.58, 0.5]}]},
          "layers": [plate("lib_low", keys=[{"t": 0, "scale": 1.0}, {"t": 3.4, "scale": 1.05}]),
                     ved("lib_low", 0.1, 1.6, [["serious", 0], ["surprised", 1.6]]),
                     txt("\"...the invulnerability of *TANKS*\"", 0.14, 70, enter="pop", at=0.2),
                     txt("MAJ. G.P.W. MEREDITH, 1932", 0.22, 40, enter="pop", at=0.4, stroke_width=4)]})
# 8. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("lib_desk", blur=10, keys=[{"t": 0, "scale": 1.2}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "the emus: \"*skill issue*\"", "text_y": 0.2, "sfx": "scratch"}})
# 9. desk: the file says WITHDRAWN
S.append({"say": "The army pulled *out*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.72, "pad": 0.4,
          "layers": [plate("lib_desk", keys=[{"t": 0, "scale": 1.12}, {"t": 2.0, "scale": 1.2}]),
                     {"type": "stamp", "text": "WITHDRAWN", "tone": "red", "angle": -8, "size": 76, "x": 0.55, "y": 0.2,
                      "at": 0.15, "sfx": "thud"}]})
# 10. payoff, wide: the verdict
S.append({"say": "Fences and farmers did the rest. *Emus win.*",
          "transition": "cut", "caption_y": 0.72, "pad": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("lib_wide"),
                     person("lib_wide", "reader", 1.3, 6.2, [["shrug", 0]]),
                     ved("lib_wide", -0.3, 1.2, [["explain", 0], ["smirk", 1.9]]),
                     {"type": "stamp", "text": "EMUS WIN", "tone": "green", "angle": -6, "size": 80, "x": 0.5, "y": 0.2,
                      "at": 1.9, "sfx": "thud"}]})

SRC = ["https://en.wikipedia.org/wiki/Emu_War",
       "https://www.britannica.com/topic/Emu-War",
       "https://www.historyhit.com/the-great-emu-war/"]
job = {"id": ID, "title": "Australia lost a war to emus 🪶",
       "description": "In November 1932, emus were wrecking wheat farms in Western Australia's Campion district, so the "
                      "army sent Major G. P. W. Meredith, two soldiers, two Lewis guns and 10,000 rounds. The emus split "
                      "into small groups and scattered, a gun jammed, and a gun mounted on a truck couldn't catch them on "
                      "rough ground. Meredith's own report: 986 emus for 9,860 rounds, exactly ten per bird. He said they "
                      "could \"face machine guns with the invulnerability of tanks.\" The army withdrew in December 1932; "
                      "bounties (about 57,000 claimed in six months of 1934) and long exclusion fences did the job "
                      "instead.\n\n"
                      "Sources: Encyclopaedia Britannica, \"Emu War\"; Wikipedia, \"Emu War\"; History Hit, "
                      "\"The Great Emu War\".",
       "tags": ["Emu War", "Great Emu War", "emus", "Australia history", "1932", "history", "true story",
                "weird history", "explained"],
       "hashtags": ["#history", "#emuwar"],
       "instagram": {"hashtags": ["#history", "#emuwar", "#emu", "#australianhistory", "#explained"]},
       "meta": {"format": "wild-story",
                "topic": "the Great Emu War: Nov-Dec 1932, Campion WA, ~20,000 emus on the wheat; Maj. Meredith + 2 soldiers, "
                         "2 Lewis guns, 10,000 rounds; emus split into small groups; truck-mounted gun couldn't catch them; "
                         "his report: 986 kills for 9,860 rounds (10 per bird); 'invulnerability of tanks'; army withdrew; "
                         "bounties and fences did the job; emus 'considered the victors'",
                "hook": "story",
                "idea_source": "viral-shaped + unique angle: a famous absurd true story told as a versus scoreboard (Army vs "
                               "Emus) with the real numbers; lane history's wild stories (ideas.md wide-spread backlog)",
                "lane": "history's wild stories", "role": "librarian", "explain": "versus",
                "role_visual": "Librarian Ved in his library aisle (tall shelves, hanging lamps, red rug) pulls the 1932 file; "
                               "reading desk with the ledger 'FILE 1932', a rubber stamp and a green banker's lamp; a reader "
                               "in the aisle",
                "styles": ["blender-3d", "library", "RS-14", "RS-03", "hud", "eqbar", "stamp", "comic"],
                "characters": ["ved", "extra"],
                "sources": SRC,
                "humour": {"trend": "gaming slang 'skill issue' as the emus' verdict (this week's rising US formats, e.g. "
                                    "'What's up brah?' (used 3x already) and the word-for-word script format, didn't fit "
                                    "cleanly)", "beat": "side_eye", "scene": 8},
                "claims": [
                    {"claim": "Nov-Dec 1932, ~20,000 emus on wheat farms, Campion district, Western Australia", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "Maj. Meredith + 2 soldiers, two Lewis guns, 10,000 rounds", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "the emus split into small groups and scattered", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "a truck-mounted gun couldn't catch the emus; too bumpy to fire", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "Meredith's report: 986 kills for 9,860 rounds, 10 per kill", "tag": "PROVEN (his own report)", "source": SRC[0]},
                    {"claim": "'They can face machine guns with the invulnerability of tanks'", "tag": "PROVEN (quote)", "source": SRC[2]},
                    {"claim": "army withdrew; bounties and fences did the job; emus considered the victors", "tag": "PROVEN", "source": SRC[1]}]},
       "thumbnail": {"title": "EMUS *WON?*", "title_y": 0.2, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#f2b04a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.2, "bg_saturation": 1.3,
                     "tint": ["#1c3f73", "#e0702e"], "tint_amount": 0.22,
                     "bg": [plate("lib_wide")],
                     "fg": [sprite("emu", 0.27, 0.6, 0.5),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.64, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
