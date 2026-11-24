"""2026-11-24-a: "Scientists hacked eyes to see infrared" (build-it; Ved as a hacker in a dark den).
Lane: bio-engineering what-ifs (night vision). Explain mode: step-by-step build (the bug -> the patch -> mice -> humans ->
eyes closed -> the catch). Styles mixed: animated Blender eye shots (moving 3D: hook, lens patch, eyelid), the hacker den
on the night set with Ved, a Reelsmith RS-12 Terminal, hud chips / optcards / stamps, a cream infographic card, the comic beat.
Facts:
- Humans see roughly 400-700 nm; near-infrared (~800-1600 nm in the 2025 study) is just beyond it (Physics World 2025;
  ScienceDaily / Cell Press 2025).
- 2019, Cell (Ma, Bao, Xue, Han; USTC + UMass): a single injection of upconversion nanoparticles in mice's eyes let them see
  ~980 nm near-infrared light, converted to green (535 nm); effect lasted up to 10 weeks.
- 2025, Cell (Tian Xue, USTC; published 22 May 2025): contact lenses with upconversion nanoparticles let people see
  near-infrared (808 / 980 / 1532 nm -> green / blue / red); vision was better with eyes closed because near-infrared passes
  through the eyelid better than visible light; only bright IR (LED sources) and limited fine detail (scattering).
Run after the assets exist: python jobs/2026-11-24-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-24-a"
J = f"jobs/{ID}/"
A = J + "assets/"
SH = J + "shots/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("den_wide", "den_low")}
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
WEAR = {"wear": "jacket"}


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def shot(script, dur, samples=20, res=0.45):
    return {"dur": dur, "type": "blender", "script": SH + script, "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "enter": "none",
            "fps": 15, "res": res, "samples": samples}


def txt(t, y, size=92, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


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


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 330 84'><rect x='4' y='4' width='322' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='188' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word.replace('&', '&amp;')}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.26, "enter": "pop", "at": at, "sfx": "click"}


# cream infographic card: the eyelid filter (visible light blocked, infrared passes)
LID_CARD = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 620'>"
    "<rect x='10' y='10' width='880' height='600' rx='36' fill='#f6efe2' stroke='#1a1410' stroke-width='8'/>"
    f"<text x='450' y='92' text-anchor='middle' font-size='64' fill='#1a1410' {AN}>YOUR EYELID</text>"
    "<rect x='420' y='130' width='60' height='420' rx='26' fill='#c98e62' stroke='#1a1410' stroke-width='6'/>"
    # visible light: yellow arrows that stop at the lid
    "<g stroke='#e0a31a' stroke-width='16' stroke-linecap='round'>"
    "<line x1='90' y1='220' x2='380' y2='220'/><line x1='90' y1='300' x2='380' y2='300'/></g>"
    "<path d='M372,198 l40,22 l-40,22 z M372,278 l40,22 l-40,22 z' fill='#e0a31a'/>"
    "<path d='M520,210 l40,40 M560,210 l-40,40 M520,290 l40,40 M560,290 l-40,40' stroke='#d6302c' stroke-width='12' stroke-linecap='round'/>"
    f"<text x='90' y='185' font-size='40' fill='#8a6a12' {AN}>NORMAL LIGHT</text>"
    # infrared: red arrows that pass straight through
    "<g stroke='#d6302c' stroke-width='16' stroke-linecap='round'>"
    "<line x1='90' y1='420' x2='800' y2='420'/><line x1='90' y1='490' x2='800' y2='490'/></g>"
    "<path d='M790,398 l40,22 l-40,22 z M790,468 l40,22 l-40,22 z' fill='#d6302c'/>"
    f"<text x='90' y='392' font-size='40' fill='#a3201d' {AN}>INFRARED</text>"
    f"<text x='620' y='575' font-size='38' fill='#2f7f4f' {AN}>GETS THROUGH</text>"
    "</svg>")

S = []
# 0. hook: the hacked eye glowing green (moving 3D), headline at frame 0, hacker Ved at the side in his jacket
S.append({"say": "How do you *hack* a human eye to see in the *dark*?",
          "layers": [shot("a_hook.py", 4.167),
                     txt("HACK YOUR EYES FOR *NIGHT VISION*", 0.17, 96, enter="none"),
                     dict(close_ved([["explain", 0], ["point", 2.2]]), x=0.8, y=1.0, h=0.56, rig_args=WEAR)]})
# 1. the den, wide: Ved walks to his desk; hud: the visible window
S.append({"say": "Bug one: you only see *400 to 700* nanometers.",
          "transition": "slide_left", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.56]}]},
          "layers": [plate("den_wide"),
                     ved("den_wide", 0.35, 0.2, [["idle", 0], ["explain", 1.3], ["point", 2.8]], walk=[(0, 2.0, 0.0), (1.2, 0.35, 0.2)],
                         rig_args=WEAR),
                     {"type": "hud", "label": "your eyes see", "text": "400-700 NM", "x": 0.5, "y": 0.16, "enter": "pop",
                      "at": 0.5, "sfx": "click", "tone": "blue"},
                     {"type": "stamp", "text": "BUG #1", "tone": "red", "angle": -6, "size": 64, "x": 0.5, "y": 0.3,
                      "at": 2.8, "sfx": "thud"}]})
# 2. Reelsmith RS-12 Terminal over the blurred screen close-up: infrared = no signal
S.append({"say": "Infrared? *Pitch black* to you.",
          "transition": "zoom", "caption_y": 0.74, "pad": 1.1,
          "layers": [plate("den_screen", blur=10, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.22}]),
                     {"type": "look", "look": "RS-12", "x": 0.5, "y": 0.36, "w": 1.0, "h": 0.6, "at": 0.0,
                      "props": {"title": "EYE.SCAN", "color": "green", "backdrop": "dim",
                                "lines": ["> scan 550 nm", "  signal OK", "> scan 980 nm (IR)", "  NO SIGNAL"], "key": 3}}]})
# 3. the patch (moving 3D): the nanoparticle lens lands, the IR beam turns green
S.append({"say": "The patch: nanoparticles that make infrared *visible*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.7,
          "layers": [shot("b_patch.py", 4.533),
                     txt("PATCH: *IR -> VISIBLE*", 0.15, 90, enter="pop", at=0.2, sfx="pop"),
                     tag_layer(0.5, 0.26, 1.6, "R&D", "#f2b04a")]})
# 4. low hero angle of the den: mice, 2019; the mouse figurine drops onto the desk; 10 weeks ticks
S.append({"say": "In 2019, injected *mice* saw infrared for up to *ten weeks*.",
          "transition": "cut", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.55]}, {"t": 3.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("den_low"),
                     ved("den_low", -0.85, 0.35, [["point", 0], ["surprised", 1.8]]),
                     sprite("mouse", 0.66, 0.47, 0.24, at=0.3, sfx="pop",
                            keys=[{"t": 0, "y": -0.1}, {"t": 0.55, "y": 0.47, "ease": "bounce"}]),
                     {"type": "dateline", "date": "2019", "place": "MICE  -  CELL JOURNAL", "size": 54, "x": 0.5, "y": 0.13,
                      "at": 0.1, "enter": "fade", "sfx": "type"},
                     {"type": "hud", "label": "weeks of infrared vision", "to": 10, "count_dur": 0.8, "x": 0.5, "y": 0.27,
                      "at": 1.6, "enter": "pop", "sfx": "click", "tone": "green", "indian": False},
                     tag_layer(0.62, 0.38, 2.6)]})
# 5. Ved close at the screens, the contact lens floating by his hand: 2025, humans
S.append({"say": "In 2025, *humans* got them as contact lenses,",
          "transition": "slide_up", "caption_y": 0.62,
          "layers": [plate("den_screen", blur=8, keys=[{"t": 0, "scale": 1.3}, {"t": 3, "scale": 1.36}]),
                     close_ved([["explain", 0], ["point", 1.1]]),
                     sprite("lens", 0.24, 0.38, 0.26, at=0.4, sfx="pop", enter="pop",
                            keys=[{"t": 0, "rot": -10}, {"t": 2.4, "rot": 8}]),
                     {"type": "dateline", "date": "2025", "place": "HUMANS  -  CONTACT LENSES", "size": 50, "x": 0.5, "y": 0.13,
                      "at": 0.1, "enter": "fade", "sfx": "type"}]})
# 6. eyelid closes over the lensed eye (moving 3D); it still glows
S.append({"say": "and saw *better* with eyes *closed*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.7, "pad": 0.4,
          "layers": [shot("c_closed.py", 2.633),
                     txt("EYES *CLOSED* = BETTER", 0.15, 92, enter="pop", at=0.15, sfx="pop")]})
# 7. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("den_wide", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "eyes closed in 1st period: *it's for science*", "text_y": 0.2}})
# 8. the why: cream card (eyelid filter) over the blurred den, Ved medium pointing at it
S.append({"say": "Infrared slips *through* eyelids. Normal light can't.",
          "transition": "cut", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.05, "focus": [0.5, 0.45]}]},
          "layers": [plate("den_wide", blur=9, keys=[{"t": 0, "scale": 1.12}, {"t": 3.4, "scale": 1.18}]),
                     {"type": "image", "svg": LID_CARD, "x": 0.5, "y": 0.27, "w": 0.86, "rotate": -2, "enter": "pop",
                      "at": 0.1, "sfx": "paper"},
                     dict(close_ved([["point", 0], ["explain", 2.0]]), x=0.62, y=0.98, h=0.6)]})
# 9. payoff: the catch, version 1.0, back at the desk
S.append({"say": "The catch: bright infrared only, and *blurry*. Version one.",
          "transition": "cut", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.55]}, {"t": 4.5, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("den_wide"),
                     ved("den_wide", -0.3, 0.1, [["explain", 0], ["crossed", 2.6], ["smirk", 4.0]]),
                     {"type": "optcard", "label": "the catch", "text": "BRIGHT IR\nONLY", "tone": "red", "x": 0.28, "y": 0.18,
                      "w": 0.38, "rotate": -3, "enter": "pop", "at": 0.2, "sfx": "pop", "until": 2.7, "exit": "fade"},
                     {"type": "optcard", "label": "the catch", "text": "BLURRY", "tone": "red", "x": 0.72, "y": 0.18,
                      "w": 0.38, "rotate": 3, "enter": "pop", "at": 0.9, "sfx": "pop", "until": 2.7, "exit": "fade"},
                     {"type": "stamp", "text": "VERSION 1.0", "tone": "green", "angle": -6, "size": 66, "x": 0.5, "y": 0.36,
                      "at": 2.8, "sfx": "thud"}]})

SRC = ["https://www.sciencedaily.com/releases/2025/05/250522124556.htm",
       "https://physicsworld.com/a/new-contact-lenses-allow-wearers-to-see-in-the-near-infrared/",
       "https://www.sciencedaily.com/releases/2019/02/190228141412.htm",
       "https://physicsworld.com/a/upconverting-nanoparticles-allow-mice-to-see-in-infrared",
       "https://www.allaboutvision.com/eye-care/pets-animals/cat-vision/"]
job = {"id": ID, "title": "Scientists hacked human eyes to see infrared 👁️",
       "description": "Your eyes only catch light from about 400 to 700 nanometers, so near-infrared light is invisible to you. "
                      "In 2019, researchers (University of Science and Technology of China and UMass Medical School, in the "
                      "journal Cell) injected tiny upconversion nanoparticles into mice's eyes: the particles turn ~980 nm "
                      "infrared into green light, and the mice could see infrared for up to 10 weeks. In 2025, Tian Xue's team "
                      "(USTC, Cell) put the same kind of nanoparticles into contact lenses, and people could see flashing "
                      "near-infrared light. They saw it even better with their eyes closed, because near-infrared passes "
                      "through the eyelid better than visible light. The catch: it only works with bright infrared sources "
                      "like LEDs, and fine detail is blurry. Research, not a product, and not medical advice.\n\n"
                      "Sources: Cell Press / ScienceDaily (2025); Physics World (2025); ScienceDaily (2019); Physics World (2019).",
       "tags": ["infrared vision", "night vision", "contact lenses", "nanoparticles", "human eye", "science news",
                "biohacking", "how eyes work", "science explained"],
       "hashtags": ["#science", "#eyes"],
       "instagram": {"hashtags": ["#science", "#nightvision", "#infrared", "#biohacking", "#explained"]},
       "meta": {"format": "build-it",
                "topic": "hacking human eyes to see infrared: humans see ~400-700 nm; 2019 Cell: nanoparticle injection let mice "
                         "see ~980 nm IR (as green) for up to 10 weeks; 2025 Cell (Tian Xue, USTC): upconversion contact lenses let "
                         "people see near-infrared, better with eyes closed (IR passes the eyelid); limits: bright IR only, blurry",
                "hook": "build-it",
                "idea_source": "unique + viral-shaped: 'night vision' made shockingly simple with a real lab hack; few Shorts "
                               "explain the eyes-closed twist; lane bio-engineering what-ifs (night vision)",
                "lane": "bio-engineering what-ifs", "role": "hacker", "explain": "step-by-step build",
                "role_visual": "hacker's den on the night set: dark desk, laptop and two monitors running a fictional EYE.PATCH "
                               "terminal, a code wall behind; Ved in a jacket in the first two scenes",
                "styles": ["blender-3d", "night-den", "RS-12", "hud", "cards", "comic"],
                "characters": ["ved"],
                "sources": SRC,
                "humour": {"trend": "timeless US school-life card (no rising trend fit cleanly): "
                                    "\"eyes closed in 1st period: it's for science\"",
                           "beat": "side_eye", "scene": 7},
                "claims": [
                    {"claim": "humans typically see light from about 400 to 700 nm", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "2019: a single injection of upconversion nanoparticles let mice see ~980 nm infrared (as green) for up to 10 weeks", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "2025: contact lenses with upconversion nanoparticles let people see near-infrared light", "tag": "R&D", "source": SRC[0]},
                    {"claim": "infrared vision was better with eyes closed because near-infrared passes through eyelids better than visible light", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "only bright infrared (LED sources) is seen, and fine detail is limited", "tag": "R&D", "source": SRC[0]}]},
       "thumbnail": {"title": "INFRARED *EYES?*", "title_y": 0.2, "title_size": 165, "max_w": 0.95, "blur": 14,
                     "glow": "#35e08a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.3,
                     "tint": ["#0b1a3a", "#35e08a"], "tint_amount": 0.25,
                     "bg": [plate("den_wide")],
                     "fg": [sprite("lens", 0.2, 0.47, 0.3, rotate=-8),
                            sprite("mouse", 0.82, 0.47, 0.28, rotate=6),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
