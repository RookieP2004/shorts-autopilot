"""2026-11-19-b: "Cracking your knuckles = arthritis? One doctor tested it for 60 years" (myth-bust).
2D Ved + Dr Unger (a faceless townsperson in a white coat) staged in depth in a Blender clinic (wide, mid on the X-ray
lightbox), and inside a knuckle: the joint closed, then pulled with a gas bubble snapping open in the joint fluid.
2D on top: MYTH? stamp + headline, cream hand cards (LEFT cracked / RIGHT never), a ticking crack counter, X-ray verdict
option cards, a crowd of 215 X-rayed people, a 20-minute reset chip, the comic beat, a gold trophy drop and MYTH BUSTED.
Facts: Unger (Arthritis & Rheumatism 1998 letter; Ig Nobel Medicine 2009): cracked the knuckles of his left hand at least
twice a day for 60+ years, never the right; ~36,500 cracks by his estimate; no arthritis in either hand, no difference.
deWeber et al. 2011 (J Am Board Fam Med): 215 people, hand X-rays, no link between habitual cracking and hand OA.
Kawchuk et al. 2015 (PLOS ONE, real-time MRI): the crack happens as a gas cavity forms in the joint fluid when the
joint surfaces separate; ~20 minutes before the same knuckle can crack again.
Run after the assets exist: python jobs/2026-11-19-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-19-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("clinic_wide", "clinic_mid", "joint_closed", "joint_pulled")}

OUT = {   # recurring person: same outfit in every shot
    "unger": {"skin": "#e2b48c", "build": "regular", "hair": ["#d8d3cb", "short"], "top": ["#f6efe2", "jacket"],
              "tie": "#3f7fbf", "bottom": ["#34425c", "trousers"], "shoes": "#25262b"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
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


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 330 84'><rect x='4' y='4' width='322' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='188' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.26, "enter": "pop", "at": at, "sfx": "click"}


def hand(label, sub, accent, crack=True, flip=False):
    """A cream card with a flat hand (palm up, fingers up), knuckle dots, a label and a sub-label."""
    sk, sh = "#e2b48c", "#c99670"
    g = "<g transform='translate(400,0) scale(-1,1)'>" if flip else "<g>"
    fingers = ""
    for k, (x, top) in enumerate(((120, 130), (172, 100), (224, 112), (274, 150))):
        fingers += f"<rect x='{x - 22}' y='{top}' width='44' height='{300 - top}' rx='22' fill='{sk}'/>"
        fingers += f"<circle cx='{x}' cy='300' r='9' fill='{accent if crack else sh}'/>"
        fingers += f"<path d='M{x - 14},{top + (300 - top) * 0.45} h28' stroke='{sh}' stroke-width='4' stroke-linecap='round'/>"
    burst = ""
    if crack:
        for (x1, y1, x2, y2) in ((100, 268, 70, 245), (196, 262, 196, 232), (292, 268, 322, 245)):
            burst += f"<path d='M{x1},{y1} L{x2},{y2}' stroke='{accent}' stroke-width='9' stroke-linecap='round'/>"
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 560'>"
            "<rect x='6' y='6' width='388' height='548' rx='34' fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>"
            + g + fingers +
            f"<rect x='92' y='280' width='206' height='170' rx='60' fill='{sk}'/>"
            f"<path d='M98,350 Q40,300 52,250 Q70,236 92,262 L120,320 Z' fill='{sk}'/>" + burst + "</g>"
            f"<text x='200' y='510' text-anchor='middle' font-size='62' fill='#1a1410' {AN}>{label}</text>"
            f"<rect x='70' y='26' width='260' height='54' rx='27' fill='{accent}'/>"
            f"<text x='200' y='66' text-anchor='middle' font-size='36' fill='#1a1410' {AN}>{sub}</text></svg>")


CRACK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 160'>"
         "<path d='M20,80 L70,40 L80,70 L140,20 L130,70 L200,30 L190,90 L280,70 L200,120 L210,95 L130,140 L140,100 L60,130 L70,100 Z' "
         "fill='#ffd23a' stroke='#1a1410' stroke-width='7' stroke-linejoin='round'/>"
         f"<text x='150' y='96' text-anchor='middle' font-size='54' fill='#1a1410' {AN}>CRACK!</text></svg>")

cw = ST["clinic_wide"]
S = []
# 0. hook (clinic mid, the X-ray lightbox behind): MYTH? stamp + headline at frame 0, Ved points, a hand cracks
S.append({"say": "Knuckle cracking causes *arthritis*? A doctor tested it for *60 years*.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.45, 0.45]}]},
          "layers": [plate("clinic_mid"),
                     ved("clinic_mid", -0.8, -0.6, [["point", 0], ["explain", 1.8], ["smirk", 3.4]]),
                     {"type": "stamp", "text": "MYTH?", "tone": "red", "angle": -6, "size": 80, "x": 0.5, "y": 0.1, "at": 0.0, "enter": "none"},
                     txt("KNUCKLE CRACKING = *ARTHRITIS?*", 0.2, 84, enter="none"),
                     {"type": "image", "svg": hand("ONE HAND", "60 YEARS", "#f2b04a"), "x": 0.2, "y": 0.6, "w": 0.22, "rotate": -6,
                      "enter": "pop", "at": 1.4, "sfx": "pop"},
                     {"type": "image", "svg": CRACK, "x": 0.2, "y": 0.66, "w": 0.24, "enter": "pop", "at": 0.5, "sfx": "pop",
                      "until": 1.3, "exit": "fade"}]})
# 1. clinic wide: Dr Unger walks in; LEFT HAND chip; cracks pop
S.append({"say": "Dr Donald Unger cracked his *left hand*, daily.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.8, "zoom": 1.06, "focus": [0.45, 0.6]}]},
          "layers": [plate("clinic_wide"),
                     person("clinic_wide", "unger", -1.2, -0.6, [["idle", 0], ["hold", 1.2], ["happy", 2.6]],
                            walk=[(0, -4.0, -1.0), (1.4, -1.2, -0.6)]),
                     ved("clinic_wide", 1.3, -2.4, [["explain", 0], ["point", 1.6]]),
                     {"type": "dottext", "text": "DR DONALD *UNGER*", "size": 52, "plate": True, "anim": "decode", "x": 0.5, "y": 0.13,
                      "at": 0.1, "enter": "fade", "sfx": "type"},
                     hud("cracks a day", y=0.24, to=2, prefix="", suffix="+", count_dur=0.8, at=1.6, tone="gold", sub="LEFT HAND ONLY"),
                     {"type": "image", "svg": CRACK, "x": 0.28, "y": 0.42, "w": 0.2, "enter": "pop", "at": 2.2, "sfx": "pop", "rotate": -8,
                      "until": 3.2, "exit": "fade"}]})
# 2. two hand cards over the blurred clinic: LEFT cracked vs RIGHT never
S.append({"say": "His *right hand*? Never. That was his *control*.",
          "transition": "slide_up", "caption_y": 0.6,
          "layers": [plate("clinic_wide", blur=12, keys=[{"t": 0, "scale": 1.2}, {"t": 4, "scale": 1.25}]),
                     {"type": "image", "svg": hand("LEFT", "CRACKED", "#f2b04a"), "x": 0.28, "y": 0.3, "w": 0.4, "rotate": -3,
                      "enter": "slide_up", "at": 0.0, "sfx": "whoosh"},
                     {"type": "image", "svg": hand("RIGHT", "NEVER", "#6fc3c0", crack=False, flip=True), "x": 0.72, "y": 0.3, "w": 0.4,
                      "rotate": 3, "enter": "pop", "at": 0.6, "sfx": "pop"},
                     {"type": "stamp", "text": "CONTROL", "tone": "blue", "angle": -8, "size": 64, "x": 0.72, "y": 0.52, "at": 1.0, "sfx": "thud"},
                     dict(close_ved([["explain", 0], ["point", 1.4]]), y=0.95, h=0.5, x=0.5)]})
# 3. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("clinic_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "right hand: *just here for the data*", "text_y": 0.2}})
# 4. clinic mid: the crack counter ticks to 36,500
S.append({"say": "About *36,500 cracks* later...",
          "transition": "cut", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.1, "focus": [0.4, 0.4]}]},
          "layers": [plate("clinic_mid"),
                     person("clinic_mid", "unger", -1.4, -0.3, [["hold", 0], ["explain", 1.4]]),
                     hud("left-hand cracks", y=0.13, to=36500, count_dur=2.2, at=0.1, tone="gold", sub="HIS OWN ESTIMATE"),
                     {"type": "tracker", "n": 6, "done": [0.3, 0.6, 0.9, 1.2, 1.5, 1.8], "x": 0.5, "y": 0.25, "at": 0.1, "enter": "fade"},
                     txt("60 YEARS", 0.31, 60, enter="pop", at=1.9, sfx="pop")]})
# 5. the X-rays: no arthritis in either hand
S.append({"say": "*No arthritis.* In *either* hand.",
          "transition": "zoom", "caption_y": 0.6, "sfx": "ding",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.06, "focus": [0.45, 0.45]}]},
          "layers": [plate("clinic_mid"),
                     {"type": "optcard", "label": "left hand", "text": "HEALTHY", "tone": "green", "x": 0.27, "y": 0.14,
                      "w": 0.38, "rotate": -3, "enter": "pop", "at": 0.1, "sfx": "pop", "verdict": "tick", "verdict_at": 0.4},
                     {"type": "optcard", "label": "right hand", "text": "HEALTHY", "tone": "green", "x": 0.71, "y": 0.14,
                      "w": 0.38, "rotate": 3, "enter": "pop", "at": 0.7, "sfx": "pop", "verdict": "tick", "verdict_at": 0.4},
                     {"type": "stamp", "text": "NO DIFFERENCE", "tone": "green", "angle": -6, "size": 70, "x": 0.5, "y": 0.72,
                      "at": 1.4, "sfx": "thud"},
                     tag_layer(0.5, 0.27, 1.8)]})
# 6. a bigger study: a crowd of 215 X-rayed people on the clinic floor, the habitual crackers glow gold
S.append({"say": "A study of *215 people* found *no link* either.",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.55]}]},
          "layers": [plate("clinic_wide"),
                     {"type": "crowd", "plate": A + "plate_clinic_wide.json", "area": [-1.0, 2.0, -2.0, -0.3], "n": 215, "fig_h": 0.34,
                      "seed": 3, "color": "#9fb4c8", "shadow": 0.3, "at": 0.0, "in_dur": 0.8,
                      "steps": [{"at": 1.2, "split": "x", "colors": ["#f2b04a", "#9fb4c8"]}]},
                     ved("clinic_wide", 2.1, -2.5, [["point", 0], ["explain", 2.0]]),
                     hud("people x-rayed", y=0.15, to=215, count_dur=0.9, at=0.1, tone="blue"),
                     {"type": "eqbar", "x": 0.5, "y": 0.25, "at": 1.4, "tone": "blue",
                      "keys": [[0.0, "crackers vs non-crackers"], [1.2, "hand arthritis: *same*"]]},
                     tag_layer(0.5, 0.31, 2.4)]})
# 7. inside the knuckle: closed, then pulled: the gas bubble snaps open
S.append({"say": "The pop? Pulling the joint snaps open a *gas bubble* in its fluid.",
          "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.1, "focus": [0.5, 0.5]}]},
          "layers": [plate("joint_closed"),
                     plate("joint_pulled", at=1.8, enter="fade", enter_dur=0.12, sfx="boom"),
                     txt("INSIDE A *KNUCKLE*", 0.13, 80, enter="pop", at=0.0, sfx="pop"),
                     hud("joint gap", y=0.23, at=0.3, text="CLOSED", tone="blue", width_of="CAVITY!"),
                     hud("joint gap", y=0.23, at=1.8, enter="none", text="CAVITY!", tone="gold", width_of="CAVITY!"),
                     {"type": "image", "svg": CRACK, "x": 0.75, "y": 0.33, "w": 0.26, "enter": "pop", "at": 1.85, "sfx": "pop",
                      "until": 3.4, "exit": "fade"},
                     tag_layer(0.5, 0.38, 2.6, "MRI 2015", "#f2b04a")]})
# 8. the bubble lingers: 20-minute reset chip, a glass of fizz
S.append({"say": "*20 minutes* later, it can pop again.",
          "transition": "cut", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.1, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.18, "focus": [0.5, 0.5]}]},
          "layers": [plate("joint_pulled"),
                     hud("ready to crack again", y=0.17, steps=[[0, 0], [0.4, 5], [0.8, 10], [1.2, 15], [1.6, 20]], suffix=" MIN", at=0.1, tone="gold",
                         width_of="20 MIN"),
                     {"type": "clock", "time": "00:20", "from": "00:00", "dur": 1.8, "label": "RESET", "r": 0.09, "x": 0.8, "y": 0.27, "at": 0.2,
                      "enter": "pop"},
                     sprite("fizz_glass", 0.18, 0.3, 0.16, enter="pop", at=0.5, sfx="pop")]})
# 9. payoff close: not damage, a bubble; the trophy drops; MYTH BUSTED
S.append({"say": "Not damage. A *bubble*. And it won him an *Ig Nobel Prize*.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("clinic_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.5, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 1.6], ["smirk", 3.2]]),
                     {"type": "optcard", "label": "the pop", "text": "BUBBLE", "tone": "blue", "x": 0.27, "y": 0.14,
                      "w": 0.37, "rotate": -3, "enter": "pop", "at": 0.2, "sfx": "pop", "verdict": "tick", "verdict_at": 0.5},
                     {"type": "optcard", "label": "the joint", "text": "DAMAGE", "tone": "red", "x": 0.71, "y": 0.14,
                      "w": 0.37, "rotate": 3, "enter": "pop", "at": 0.6, "sfx": "pop", "verdict": "cross", "verdict_at": 0.5},
                     sprite("trophy", 0.82, 0.36, 0.18, at=1.8, sfx="ding",
                            keys=[{"t": 0, "y": -0.1}, {"t": 0.5, "y": 0.36, "ease": "bounce"}]),
                     txt("IG NOBEL *2009*", 0.47, 52, x=0.8, enter="pop", at=2.4, sfx="pop"),
                     {"type": "stamp", "text": "MYTH BUSTED", "tone": "red", "angle": -6, "size": 62, "x": 0.27, "y": 0.29,
                      "at": 3.0, "sfx": "thud"}]})

job = {"id": ID, "title": "Knuckle cracking = arthritis? He tested it 60 years 🖐️",
       "description": "Does cracking your knuckles cause arthritis? Dr Donald Unger cracked the knuckles of his left hand at "
                      "least twice a day for more than 60 years, and never his right hand, as a control. By his estimate that's "
                      "about 36,500 cracks. Result: no arthritis in either hand, and no difference between them (Arthritis & "
                      "Rheumatism, 1998). It won him the 2009 Ig Nobel Prize in Medicine. A larger study that X-rayed the hands "
                      "of 215 people found no link between habitual knuckle cracking and hand osteoarthritis (2011). The pop? "
                      "Real-time MRI (2015) shows a gas cavity forming in the joint fluid as the joint surfaces separate; it "
                      "takes about 20 minutes before that knuckle can crack again. (How the body works, not medical advice.)\n\n"
                      "Sources: Improbable Research (Ig Nobel 2009, Donald Unger); deWeber et al., J Am Board Fam Med 2011; "
                      "Kawchuk et al., PLOS ONE 2015 (University of Alberta), via Science News and ScienceDaily.",
       "tags": ["knuckle cracking", "does cracking knuckles cause arthritis", "cracking knuckles", "arthritis myth",
                "human body", "ig nobel", "body facts", "myth busted", "science facts"],
       "hashtags": ["#science", "#humanbody"],
       "instagram": {"hashtags": ["#science", "#humanbody", "#crackingknuckles", "#mythbusting", "#explained"]},
       "meta": {"format": "myth-bust", "topic": "the knuckle-cracking arthritis myth: Donald Unger cracked only his left hand's "
                                                "knuckles at least twice a day for 60+ years (~36,500 cracks), right hand as "
                                                "control; no arthritis in either hand (1998 letter, Ig Nobel 2009); 2011 study of "
                                                "215 people X-rayed: no link; the pop = a gas cavity forming in the joint fluid "
                                                "(real-time MRI 2015); ~20 minutes to reset",
                "hook": "myth-bust",
                "idea_source": "viral-shaped + unique: a habit almost everyone has and a warning almost everyone has heard, busted "
                               "by a real one-man 60-year experiment (a story few Shorts tell properly); backlog idea; body niche "
                               "with a myth-bust after today's space what-if",
                "characters": ["ved", "extra"],
                "sources": ["https://improbable.com/2009/11/05/interview-with-dr-knuckle-cracker/",
                            "https://improbable.com/2010/02/15/ig-nobel-acceptance-speech-knuckle-cracking/",
                            "https://acibademinternational.com/blog/is-it-bad-to-crack-your-knuckles-the-60-year-experiment-that-answered-it/",
                            "https://www.jabfm.org/content/24/2/169",
                            "https://www.sciencenews.org/article/researchers-pull-fingers-solve-why-knuckles-crack",
                            "https://sciencedaily.com/releases/2015/04/150415155320.htm"],
                "humour": {"trend": "timeless dry aside (no rising meme fits; 'I Got So Mad' / 'My Type Quiz' already used this "
                                    "week): side-eye + 'right hand: just here for the data'",
                           "beat": "side_eye", "scene": 3},
                "claims": [
                    {"claim": "Donald Unger cracked the knuckles of his left hand (never the right) at least twice a day for more than 60 years", "tag": "PROVEN",
                     "source": "https://improbable.com/2009/11/05/interview-with-dr-knuckle-cracker/"},
                    {"claim": "about 36,500 cracks by his estimate; no arthritis in either hand and no difference (Arthritis & Rheumatism 1998)", "tag": "PROVEN",
                     "source": "https://acibademinternational.com/blog/is-it-bad-to-crack-your-knuckles-the-60-year-experiment-that-answered-it/"},
                    {"claim": "Ig Nobel Prize in Medicine 2009", "tag": "PROVEN",
                     "source": "https://improbable.com/2010/02/15/ig-nobel-acceptance-speech-knuckle-cracking/"},
                    {"claim": "a 2011 study X-rayed 215 people's hands: no link between habitual knuckle cracking and hand osteoarthritis", "tag": "PROVEN",
                     "source": "https://www.jabfm.org/content/24/2/169"},
                    {"claim": "real-time MRI (2015): the crack coincides with a gas cavity forming in the joint fluid as the joint separates", "tag": "PROVEN",
                     "source": "https://www.sciencenews.org/article/researchers-pull-fingers-solve-why-knuckles-crack"},
                    {"claim": "about 20 minutes before the same knuckle can crack again", "tag": "PROVEN",
                     "source": "https://www.sciencenews.org/article/researchers-pull-fingers-solve-why-knuckles-crack"}]},
       "thumbnail": {"title": "60 YEARS *CRACKING*", "title_y": 0.2, "title_size": 150, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#1f6670", "#f08a24"], "tint_amount": 0.28,
                     "bg": [plate("joint_pulled")],
                     "fg": [{"type": "image", "svg": hand("LEFT", "CRACKED", "#f2b04a"), "x": 0.2, "y": 0.45, "w": 0.3, "rotate": -8, "enter": "none"},
                            {"type": "image", "svg": CRACK, "x": 0.8, "y": 0.42, "w": 0.32, "rotate": 8, "enter": "none"},
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
