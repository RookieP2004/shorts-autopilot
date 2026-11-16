"""2026-11-16-a: "12 colour sensors... and it sees colour WORSE than you" (myth-bust, mantis shrimp).
2D Ved + a lab scientist staged in depth in a bright Blender REEF LAB (wide, mid on the reef tank) and an underwater reef
close-up with two optic-fibre lights, built from stills + cut-outs. 2D on top: MYTH stamp, hud chips 12 vs 3, a rainbow
"?" card, glowing test lights that change colour, a gap hud that ticks 100 -> 15 nm with an eqbar, a GUESSING stamp,
option cards (SHRIMP 15-25 nm cross / YOU ~5 nm tick), a 3-sensor nodes diagram, a scanner beam over the shrimp, tags.
Facts: Thoen, How, Chiou & Marshall, Science 343:411 (2014, University of Queensland): mantis shrimp have 12 colour
photoreceptor types (humans 3); trained with food rewards to pick a coloured light from optic fibres; they failed to tell
colours apart closer than ~12-25 nm (NatGeo: 15-25 nm), humans ~5 nm (NatGeo) / 1-4 nm; hypothesis: they recognise colours
directly from the pattern of all 12 receptors (look-up / barcode-like) instead of comparing channels (THEORY).
Run after the assets exist: python jobs/2026-11-16-a/build_job.py
"""
import json, math, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-16-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("lab_wide", "lab_mid", "reef")}

OUT = {   # recurring people: same outfit in every shot
    "hanne": {"skin": "#f0c8a0", "build": "slim", "hair": ["#c99a3a", "long"], "hat": None,
              "top": ["#f6efe2", "jacket"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "necklace": "#6fc3c0"},
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


def staged(set_, behind=(), front=(), extra_top=(), fg=True):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if fg:
        out.append({"type": "image", "path": A + f"fg_{set_}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"})
    out += sorted(front, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 84'><rect x='4' y='4' width='292' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='172' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.24, "enter": "pop", "at": at, "sfx": "click"}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


def glow(color):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'><defs><radialGradient id='g'>"
            f"<stop offset='0' stop-color='#ffffff'/><stop offset='0.22' stop-color='{color}'/>"
            f"<stop offset='0.55' stop-color='{color}' stop-opacity='0.45'/><stop offset='1' stop-color='{color}' stop-opacity='0'/>"
            "</radialGradient></defs><circle cx='150' cy='150' r='150' fill='url(#g)'/></svg>")


def light(x, y, color, at=0.0, until=None, w=0.3, enter="fade", **k):
    L = {"type": "image", "svg": glow(color), "x": x, "y": y, "w": w, "enter": enter, "at": at, "enter_dur": 0.2,
         "loop": "pulse", "loop_amp": 0.04, **k}
    if until is not None:
        L["until"] = until; L["exit"] = "fade"
    return L


RAINBOW = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 330'>"
           + "".join(f"<path d='M{40 + k*26},300 A{260 - k*26},{260 - k*26} 0 0,1 {560 - k*26},300' fill='none' stroke='{c}' stroke-width='28'/>"
                     for k, c in enumerate(("#d9534f", "#f08a24", "#f2d04a", "#4f9e4a", "#3f7fbf", "#6a4fb8", "#e86aa6")))
           + f"<text x='300' y='300' text-anchor='middle' font-size='150' fill='#f6efe2' stroke='#1a1410' stroke-width='8' {AN}>?</text></svg>")

BEAM = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 60'><defs><linearGradient id='b' x1='0' x2='0' y1='0' y2='1'>"
        "<stop offset='0' stop-color='#ff5a5a' stop-opacity='0'/><stop offset='0.5' stop-color='#ff5a5a'/>"
        "<stop offset='1' stop-color='#ff5a5a' stop-opacity='0'/></linearGradient></defs>"
        "<rect x='0' y='0' width='800' height='60' fill='url(#b)'/><rect x='0' y='28' width='800' height='4' fill='#ffffff'/></svg>")

MS = "mantis"
rf = ST["reef"]
LX, LY = rf.point(-0.5, 0.5, 2.15)       # left fibre tip on the reef plate
RX, RY = rf.point(0.5, 0.5, 2.15)        # right fibre tip
BX, BY = rf.point(-0.4, 0.05, 0.1)       # burrow mouth

S = []
# 0. hook (lab mid): MYTH stamp + headline + 12 vs 3 at frame 0; Ved in front of the reef tank, Hanne behind the bench
S.append({"say": "This shrimp has *twelve* colour sensors. You have *three*.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "hanne", -1.9, 1.4, [["idle", 0], ["point", 1.4]])],
                           front=[ved("lab_mid", -0.4, -0.2, [["surprised", 0], ["point", 1.2], ["explain", 2.6]], hops=[[0.15, 0.05, 0.4]])],
                           extra_top=[{"type": "stamp", "text": "MYTH?", "tone": "red", "angle": -6, "size": 70, "x": 0.5, "y": 0.085,
                                       "at": 0.0, "enter": "none"},
                                      txt("IT SEES *SUPER COLOURS*", 0.165, 92, enter="none"),
                                      hud("shrimp sensors", x=0.3, y=0.29, value=12, tone="gold", enter="none", width_of="12"),
                                      hud("your sensors", x=0.7, y=0.29, steps=[[0, 12], [0.05, 3]], count_dur=0.5, tone="blue", at=1.6,
                                          width_of="12")])})
# 1. reef: the shrimp at its burrow; a rainbow "?" card -> the myth
S.append({"say": "So it sees colours we can't *imagine*... right?",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.07, "focus": [0.5, 0.6]}]},
          "layers": [plate("reef"),
                     sprite(MS, BX + 0.12, BY - 0.08, 0.62, enter="slide_left", at=0.0, sfx="whoosh",
                            keys=[{"t": 0, "rot": 0}, {"t": 1.2, "rot": -3}, {"t": 2.4, "rot": 1}]),
                     {"type": "image", "svg": RAINBOW, "x": 0.5, "y": 0.22, "w": 0.72, "enter": "pop", "at": 0.4, "sfx": "pop"}]})
# 2. lab wide: 2014, University of Queensland, the test begins (Hanne walks to the tank)
S.append({"say": "In 2014, scientists in Australia *tested* it.",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.06, "focus": [0.45, 0.55]}]},
          "layers": staged("lab_wide",
                           behind=[person("lab_wide", "hanne", -2.2, 1.3, [["idle", 0], ["explain", 1.3]],
                                          walk=[(0, -4.2, 1.6), (1.2, -2.2, 1.3)])],
                           front=[ved("lab_wide", 1.6, -1.6, [["explain", 0], ["point", 1.0]])],
                           extra_top=[{"type": "image", "svg": card(
                                          "<text x='40' y='80' font-size='54' fill='#1a1410' " + AN + ">SCIENCE JOURNAL, 2014</text>"
                                          "<text x='40' y='124' font-size='30' fill='#34425c' " + F + ">UNIVERSITY OF QUEENSLAND</text>", 820, 150),
                                       "x": 0.45, "y": 0.18, "w": 0.74, "rotate": -2, "enter": "slide_right", "at": 0.3, "sfx": "pop"},
                                      tag_layer(0.76, 0.27, 1.0)])})
# 3. reef: two lights, pick the trained colour, get a snack
S.append({"say": "Two lights. Pick the right *colour*, get a snack.",
          "transition": "slide_up", "caption_y": 0.45,
          "layers": [plate("reef"),
                     light(LX, LY, "#3f7fbf", at=0.1, sfx="pop"), light(RX, RY, "#d9534f", at=0.4, sfx="pop"),
                     sprite(MS, BX + 0.12, BY - 0.08, 0.62,
                            keys=[{"t": 0, "x": BX + 0.12, "y": BY - 0.08, "rot": 0}, {"t": 1.4, "x": LX + 0.05, "y": LY + 0.33, "rot": -12},
                                  {"t": 1.7, "x": LX + 0.06, "y": LY + 0.31, "rot": -16}, {"t": 2.0, "x": LX + 0.05, "y": LY + 0.33, "rot": -10}]),
                     sprite("pellet", LX, LY + 0.06, 0.05, enter="drop", at=1.8, sfx="ding",
                            keys=[{"t": 0, "y": LY + 0.06}, {"t": 0.8, "y": LY + 0.24, "ease": "out"}]),
                     {"type": "tracker", "n": 3, "done": [1.8], "x": 0.5, "y": 0.1, "at": 0.2, "enter": "fade"},
                     txt("SNACK *UNLOCKED*", 0.17, 84, enter="pop", at=1.9, sfx="pop")]})
# 4. reef: the colours move closer (right light walks red -> orange -> green -> teal) + gap hud + eqbar
ramp = [("#d9534f", 0.0, 0.8), ("#f2b04a", 0.8, 1.6), ("#4fb08a", 1.6, 2.4), ("#3f9fb0", 2.4, 9)]
S.append({"say": "Then they moved the colours closer... and *closer*.",
          "transition": "cut", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.08, "focus": [0.5, 0.35]}]},
          "layers": [plate("reef"), light(LX, LY, "#3f7fbf", enter="none")]
                    + [light(RX, RY, c, at=a, until=(u if u < 9 else None), enter="none" if a == 0 else "fade", sfx=None if a == 0 else "click")
                       for c, a, u in ramp]
                    + [sprite(MS, LX + 0.05, LY + 0.33, 0.62, keys=[{"t": 0, "rot": -10}, {"t": 1.5, "rot": -4}, {"t": 3.0, "rot": -9}]),
                       hud("colour gap", y=0.1, steps=[[0, 100], [0.8, 60], [1.6, 35], [2.4, 20]], count_dur=0.5, tone="blue",
                           enter="none", suffix=" nm", width_of="100 nm"),
                       {"type": "eqbar", "keys": [[0.2, "red vs blue: easy"], [1.6, "closer..."], [2.4, "almost *the same*"]],
                        "tone": "blue", "x": 0.5, "y": 0.19, "enter": "fade"},
                       {"type": "tracker", "n": 3, "done": [0, 1.0], "x": 0.5, "y": 0.62, "enter": "none"}]})
# 5. reef: 15-25 nm apart, it's guessing (shrimp swings between the two lights) + GUESSING stamp
S.append({"say": "Around twenty nanometres apart? It just *guessed*.",
          "transition": "cut", "caption_y": 0.45,
          "layers": [plate("reef"), light(LX, LY, "#3f7fbf", enter="none"), light(RX, RY, "#3f9fb0", enter="none"),
                     sprite(MS, LX + 0.05, LY + 0.33, 0.62,
                            keys=[{"t": 0, "x": LX + 0.05, "rot": -9}, {"t": 0.9, "x": RX - 0.05, "rot": 9}, {"t": 1.8, "x": LX + 0.05, "rot": -9},
                                  {"t": 2.7, "x": RX - 0.05, "rot": 9}, {"t": 3.6, "x": 0.5, "rot": 0}]),
                     hud("shrimp's limit", y=0.1, text="15-25 nm", tone="red", enter="pop", at=0.2),
                     {"type": "stamp", "text": "50/50 GUESS", "tone": "red", "angle": -7, "size": 84, "x": 0.5, "y": 0.22,
                      "at": 2.4, "sfx": "thud"},
                     {"type": "tracker", "n": 3, "done": [0, 0, 2.4], "x": 0.5, "y": 0.62, "enter": "none"},
                     tag_layer(0.8, 0.3, 1.0)]})
# 6. comic beat: smirk cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["smirk", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "eyes: *premium*\nbrain: *free trial*", "text_y": 0.2}})
# 7. lab mid: you vs the shrimp (option cards), Ved points at the viewer
S.append({"say": "Your eyes? About *five*.",
          "transition": "slide_left", "caption_y": 0.42,
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "hanne", -1.9, 1.4, [["surprised", 0], ["happy", 1.0]], hops=[[0.9, 0.04, 0.4]])],
                           front=[ved("lab_mid", -0.4, -0.2, [["point", 0], ["warm", 1.2]])],
                           extra_top=[{"type": "optcard", "label": "mantis shrimp", "text": "15-25 nm", "tone": "red", "x": 0.28, "y": 0.2,
                                       "w": 0.42, "rotate": -3, "enter": "pop", "at": 0.0, "sfx": "pop", "verdict": "cross", "verdict_at": 1.0},
                                      {"type": "optcard", "label": "you", "text": "~5 nm", "tone": "green", "x": 0.72, "y": 0.2,
                                       "w": 0.42, "rotate": 3, "enter": "pop", "at": 0.3, "sfx": "pop", "verdict": "tick", "verdict_at": 1.3}])})
# 8. how: your brain compares 3 channels (nodes), the shrimp likely just matches (scanner beam) - THEORY
NODES = [{"id": "r", "pos": [-1.3, 0.8, 0.2], "at": 0.2, "tone": "red", "label": "RED"},
         {"id": "g", "pos": [0.0, 1.0, -0.2], "at": 0.35, "tone": "green", "label": "GREEN"},
         {"id": "b", "pos": [1.3, 0.8, 0.2], "at": 0.5, "tone": "blue", "label": "BLUE"},
         {"id": "o", "pos": [0, -0.5, 0], "at": 0.9, "tone": "gold", "label": "COMPARE"}]
S.append({"say": "You *compare* three sensors. The shrimp likely just *matches*, like a scanner.",
          "transition": "slide_up", "caption_y": 0.45,
          "layers": [plate("reef", blur=6),
                     {"type": "nodes", "nodes": NODES, "x": 0.5, "y": 0.27, "yaw": [-12, 10], "until": 2.4, "exit": "fade",
                      "edges": [["r", "o", 0.7, "red"], ["g", "o", 0.8, "green"], ["b", "o", 0.9, "blue"]]},
                     sprite(MS, 0.5, 0.68, 0.7, enter="pop", at=2.2, sfx="pop"),
                     {"type": "image", "svg": BEAM, "x": 0.5, "y": 0.6, "w": 0.8, "enter": "fade", "at": 2.6, "sfx": "click",
                      "keys": [{"t": 0, "y": 0.6}, {"t": 0.9, "y": 0.76}, {"t": 1.8, "y": 0.6}, {"t": 2.7, "y": 0.76}]},
                     txt("*BEEP.* THAT ONE.", 0.2, 96, enter="pop", at=3.0, sfx="pop"),
                     tag_layer(0.78, 0.3, 3.2, "THEORY", "#f2b04a")]})
# 9. close payoff: fast, not fine -> your 3 win (loops to the 12 vs 3 hook)
S.append({"say": "Fast, not fine. Twelve sensors... and your *three* still win.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 1.6], ["smirk", 3.2]]),
                     hud("shrimp sensors", x=0.3, y=0.12, value=12, tone="gold", at=0.3, width_of="12"),
                     hud("your sensors", x=0.7, y=0.12, value=3, tone="green", at=0.6, width_of="12"),
                     {"type": "stamp", "text": "YOU WIN", "tone": "green", "angle": -6, "size": 96, "x": 0.5, "y": 0.26,
                      "at": 2.6, "sfx": "thud"}]})

job = {"id": ID, "title": "12 colour sensors... and worse colour vision than you 🦐",
       "description": "Mantis shrimp have 12 kinds of colour receptor; you have 3. So they must see colours we can't imagine? "
                      "In a 2014 test (University of Queensland, published in Science), mantis shrimp were trained to pick a coloured "
                      "light for food. When two colours were about 15-25 nm apart they could no longer tell them apart, while humans "
                      "can split colours roughly 5 nm apart. Researchers think they recognise colours directly from the pattern of all "
                      "12 receptors (fast, like a barcode scanner) instead of comparing channels like we do.\n\n"
                      "Sources: Thoen et al., Science (2014); University of Queensland; National Geographic.",
       "tags": ["mantis shrimp", "mantis shrimp eyes", "mantis shrimp colour vision", "color vision", "animal facts",
                "myth busted", "biology", "science facts", "how eyes work"],
       "hashtags": ["#science", "#animals"],
       "instagram": {"hashtags": ["#science", "#mantisshrimp", "#animalfacts", "#marinebiology", "#explained"]},
       "meta": {"format": "myth-bust", "topic": "the mantis shrimp super-colour-vision myth: 12 colour receptors vs our 3, yet in "
                                                "Thoen et al. 2014 (Science) they could not tell colours ~15-25 nm apart vs ~5 nm for "
                                                "humans; likely recognise colours directly (look-up/scanner) instead of comparing",
                "hook": "number-shock",
                "idea_source": "viral-shaped + unique: the famous '12/16 colour receptors' meme fact turned upside down; backlog idea "
                               "(mantis shrimp myth); few Shorts show the actual test",
                "characters": ["ved", "extra"],
                "sources": ["https://news.uq.edu.au/2014-01-24-shrimp-gives-insight-colour-vision",
                            "https://www.nationalgeographic.com/science/article/the-mantis-shrimp-sees-like-a-satellite",
                            "https://mappingignorance.org/2014/03/24/mantis-shrimps-part-2-lords-colour-perhaps/",
                            "https://www.nature.com/articles/nature.2014.14578"],
                "humour": {"trend": "timeless dry aside on a freemium format ('premium / free trial'); no rising meme fit this topic",
                           "beat": "smirk", "scene": 6},
                "claims": [
                    {"claim": "mantis shrimp have 12 colour photoreceptor types; humans have 3", "tag": "PROVEN",
                     "source": "https://news.uq.edu.au/2014-01-24-shrimp-gives-insight-colour-vision"},
                    {"claim": "2014 University of Queensland study (Thoen et al., Science) trained shrimp with food rewards to choose coloured lights", "tag": "PROVEN",
                     "source": "https://mappingignorance.org/2014/03/24/mantis-shrimps-part-2-lords-colour-perhaps/"},
                    {"claim": "they could not tell apart colours ~15-25 nm apart; humans ~5 nm", "tag": "PROVEN",
                     "source": "https://www.nationalgeographic.com/science/article/the-mantis-shrimp-sees-like-a-satellite"},
                    {"claim": "they likely recognise colours directly from the receptor pattern (look-up, scanner-like) instead of comparing channels", "tag": "THEORY",
                     "source": "https://www.nationalgeographic.com/science/article/the-mantis-shrimp-sees-like-a-satellite"}]},
       "thumbnail": {"title": "12 COLOURS *WORSE?*", "title_y": 0.15, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#1f6fb8", "#f08a24"], "tint_amount": 0.28,
                     "bg": [plate("reef")],
                     "fg": [sprite(MS, 0.5, 0.42, 0.85),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.8, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
