"""2026-11-18-b: "Your foot never falls asleep" (big-question: why a foot 'falls asleep').
2D Ved + Lena (a townsperson on movie night) staged in depth in a Blender living room at dusk (wide, mid by the sofa), and
inside the leg: a yellow nerve cable over a bone, free and then squashed under the other knee (same camera).
2D on top: the question headline, BLOOD vs NERVE option cards, a cream leg card (the nerve wrapping the fibular head, just
under the skin), signal dots streaming along the cable (then stopping, red), a BLOCKED stamp, a live phone chat (BRAIN ->
FOOT, unread), a 4-step tracker (squeeze, blocked, release, fizz), sparks for pins and needles, honesty tags, the comic beat.
Facts: The Conversation / ScienceAlert (neurologists R. Traub, S. Vernino): a foot 'falls asleep' because a nerve is
compressed, not because of a lack of blood flow; signals are blocked like a kinked hose; tingling (paresthesia) comes as the
nerve regains function; the discomfort makes you shift; prolonged compression can injure a nerve (people who can't move).
Colorado Orthopedics / Penn Medicine: the common fibular (peroneal) nerve wraps around the fibular head just below the
outside of the knee, close to the skin; crossing the legs is a common cause of compression.
Run after the assets exist: python jobs/2026-11-18-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-18-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("movie_wide", "movie_mid", "nerve_open", "nerve_squeeze")}

OUT = {   # recurring person: same outfit in every shot
    "lena": {"skin": "#c68a5e", "build": "slim", "hair": ["#2b1d14", "bun"], "top": ["#7a5cc4", "hoodie"],
             "bottom": ["#34425c", "trousers"], "shoes": "#f6efe2"},
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


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 330 84'><rect x='4' y='4' width='322' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='188' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.26, "enter": "pop", "at": at, "sfx": "click"}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


def dot(color):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><radialGradient id='g'>"
            f"<stop offset='0' stop-color='#ffffff'/><stop offset='0.35' stop-color='{color}'/>"
            f"<stop offset='1' stop-color='{color}' stop-opacity='0'/></radialGradient></defs><circle cx='50' cy='50' r='50' fill='url(#g)'/></svg>")


SPARK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50,0 L58,42 L100,50 L58,58 L50,100 L42,58 L0,50 L42,42 Z' "
         "fill='#fff6d8' stroke='#f2b04a' stroke-width='4'/></svg>")

# the leg card: a side view of crossed legs (top leg resting on the bottom knee), bone shown, the nerve glowing as it wraps
# around the fibular head just under the skin; a label with a pointer
LEG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 620'>"
       "<rect x='6' y='6' width='888' height='608' rx='36' fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>"
       "<text x='450' y='76' text-anchor='middle' font-size='52' fill='#1a1410' " + AN + ">CROSSED LEGS, SIDE VIEW</text>"
       # bottom leg: thigh from the left to the knee, shin down to the foot
       "<path d='M60,300 L470,300 Q540,300 560,350 L610,560 L500,560 L460,390 Q450,370 420,372 L60,372 Z' fill='#e3a27f' stroke='#1a1410' stroke-width='5'/>"
       # the fibula inside the shin + its head under the knee
       "<path d='M505,385 L560,545' stroke='#efe4cf' stroke-width='22' stroke-linecap='round'/>"
       "<circle cx='502' cy='378' r='20' fill='#efe4cf' stroke='#b9ad96' stroke-width='3'/>"
       # the nerve: comes down the back of the thigh, wraps the fibular head, runs down the shin (glowing yellow)
       "<path d='M80,360 L430,360 Q480,358 492,396 Q500,420 528,440 L585,548' stroke='#f2b04a' stroke-width='16' fill='none' "
       "stroke-linecap='round' opacity='0.45'/>"
       "<path d='M80,360 L430,360 Q480,358 492,396 Q500,420 528,440 L585,548' stroke='#ffd23a' stroke-width='7' fill='none' stroke-linecap='round'/>"
       # top leg resting across, its calf pressing on the knee (semi-transparent so the nerve shows)
       "<path d='M120,228 L560,250 Q640,256 700,300 L860,330 L850,384 L690,362 Q610,350 540,330 Q505,322 470,322 L120,300 Z' "
       "fill='#d99872' stroke='#1a1410' stroke-width='5' opacity='0.92'/>"
       # pressure mark
       "<circle cx='498' cy='384' r='46' fill='none' stroke='#d6483e' stroke-width='8' stroke-dasharray='14 10'/>"
       "<path d='M640,470 L540,410' stroke='#1a1410' stroke-width='6'/>"
       "<rect x='600' y='450' width='280' height='118' rx='20' fill='#1a1410'/>"
       "<text x='740' y='502' text-anchor='middle' font-size='40' fill='#ffd23a' " + AN + ">FIBULAR NERVE</text>"
       "<text x='740' y='548' text-anchor='middle' font-size='28' fill='#f6efe2' " + F + ">just under the skin</text>"
       "</svg>")

CHAT = {"kind": "chat", "name": "FOOT", "sub": "last seen 2 min ago",
        "msgs": [{"text": "move.", "side": "out", "time": "21:14", "ticks": 1, "at": 0.3},
                 {"text": "hello??", "side": "out", "time": "21:14", "ticks": 1, "at": 1.1},
                 {"text": "MOVE.", "side": "out", "time": "21:15", "ticks": 1, "at": 1.9}],
        "input": "Message"}

no, sq = ST["nerve_open"], ST["nerve_squeeze"]
CABLE = [no.point(x, 0.1, 1.12) for x in (-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0)]
CL, CR = CABLE[0], CABLE[-1]
PRESS = sq.point(0.0, 0.1, 1.12)


def stream(t0, t1, color, n=7, stop=None, rev=False):
    """signal dots running along the cable from left to right (rev: right to left)."""
    out = []
    a, b = (CR, CL) if rev else (CL, CR)
    for k in range(n):
        start = t0 + k * (t1 - t0) / n
        L = {"type": "image", "svg": dot(color), "x": a[0], "y": a[1], "w": 0.07, "enter": "fade", "enter_dur": 0.1, "at": start,
             "keys": [{"t": 0, "x": a[0], "y": a[1]}, {"t": 1.4, "x": b[0], "y": b[1], "ease": "linear"}],
             "until": start + 1.4, "exit": "fade"}
        if stop is not None:
            # stops at the squeeze point
            L["keys"] = [{"t": 0, "x": a[0], "y": a[1]}, {"t": 0.7, "x": PRESS[0] - 0.06, "y": PRESS[1], "ease": "out"}]
            L["until"] = start + 1.6
        out.append(L)
    return out


S = []
# 0. hook (movie mid): headline at frame 0; Lena wobbles by the sofa on one leg; Ved points
S.append({"say": "Your foot never falls *asleep*. You just *kinked its cable*.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.07, "focus": [0.55, 0.58]}]},
          "layers": [plate("movie_mid"),
                     person("movie_mid", "lena", 1.9, 1.7, [["surprised", 0], ["sad", 1.4], ["shrug", 2.6]], hops=[[0.5, 0.05, 0.35], [1.6, 0.04, 0.35]]),
                     ved("movie_mid", 0.95, 0.35, [["point", 0], ["explain", 1.5], ["smirk", 2.7]]),
                     {"type": "stamp", "text": "ASLEEP?", "tone": "red", "angle": -6, "size": 72, "x": 0.5, "y": 0.085, "at": 0.0, "enter": "none"},
                     txt("WHY DOES YOUR FOOT *FALL ASLEEP?*", 0.19, 84, enter="none"),
                     {"type": "image", "svg": SPARK, "x": 0.73, "y": 0.62, "w": 0.06, "enter": "pop", "at": 1.6, "loop": "pulse", "loop_amp": 0.25},
                     {"type": "image", "svg": SPARK, "x": 0.79, "y": 0.66, "w": 0.045, "enter": "pop", "at": 1.8, "loop": "pulse", "loop_amp": 0.25}]})
# 1. movie wide: BLOOD vs NERVE option cards; Ved walks in
S.append({"say": "Not the blood, like most people think. A *squashed nerve*.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.05, "focus": [0.5, 0.55]}]},
          "layers": [plate("movie_wide"),
                     person("movie_wide", "lena", 1.9, 1.7, [["sad", 0], ["shrug", 2.0]]),
                     ved("movie_wide", 0.2, -1.6, [["explain", 0], ["point", 1.8]], walk=[(0, 2.6, -2.2), (1.2, 0.2, -1.6)]),
                     {"type": "optcard", "label": "most people think", "text": "BLOOD", "tone": "red", "x": 0.28, "y": 0.14,
                      "w": 0.42, "rotate": -3, "enter": "pop", "at": 0.1, "sfx": "pop", "verdict": "cross", "verdict_at": 1.0},
                     {"type": "optcard", "label": "neurologists say", "text": "NERVE", "tone": "green", "x": 0.72, "y": 0.14,
                      "w": 0.42, "rotate": 3, "enter": "pop", "at": 1.5, "sfx": "pop", "verdict": "tick", "verdict_at": 0.6},
                     tag_layer(0.5, 0.27, 2.2)]})
# 2. the leg card over the blurred room: the nerve wraps the bone just under the skin
S.append({"say": "Cross your legs, and below the knee, a nerve sits on bone, just under the skin.",
          "transition": "slide_up", "caption_y": 0.56,
          "layers": [plate("movie_mid", blur=12, keys=[{"t": 0, "scale": 1.2}, {"t": 5, "scale": 1.26}]),
                     txt("THE *FIBULAR NERVE*", 0.105, 92, enter="pop", at=0.0, sfx="pop"),
                     {"type": "image", "svg": LEG, "x": 0.5, "y": 0.31, "w": 0.86, "rotate": -1.5, "enter": "slide_up", "at": 0.15, "sfx": "whoosh",
                      "keys": [{"t": 0, "scale": 1.0}, {"t": 4.5, "scale": 1.04}]},
                     dict(close_ved([["explain", 0], ["point", 2.2]]), y=0.94, h=0.55, x=0.3),
                     tag_layer(0.78, 0.53, 2.6)]})
# 3. inside the leg (open): the cable, signals streaming both ways
S.append({"say": "It's the cable between your *brain* and your *foot*.",
          "transition": "zoom", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.08, "focus": [0.5, 0.5]}]},
          "layers": [plate("nerve_open")]
                    + stream(0.1, 2.6, "#7fe8ff", 8) + stream(0.5, 2.8, "#7dffb0", 6, rev=True)
                    + [hud("signals", y=0.1, text="FLOWING", tone="green", at=0.2, width_of="BLOCKED!"),
                       txt("BRAIN", 0.2, 64, x=0.16, enter="pop", at=0.4, sfx="pop"),
                       txt("FOOT", 0.2, 64, x=0.84, enter="pop", at=0.8, sfx="pop")]})
# 4. squeezed: the knee slams down, the dots pile up and stop (red); BLOCKED stamp
S.append({"say": "Press on it, like stepping on a *hose*, and the messages *stop*.",
          "transition": "flash", "sfx": "boom", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.0, "focus": [0.5, 0.5]}], "shake": [0.0, 0.3]},
          "layers": [plate("nerve_squeeze")]
                    + stream(0.2, 2.4, "#ff5a4a", 6, stop=True)
                    + [hud("signals", y=0.1, text="BLOCKED!", tone="red", at=0.0, enter="none", width_of="BLOCKED!"),
                       {"type": "stamp", "text": "BLOCKED", "tone": "red", "angle": -7, "size": 92, "x": 0.5, "y": 0.8 - 0.06,
                        "at": 1.6, "sfx": "thud"},
                       tag_layer(0.8, 0.2, 2.4)]})
# 5. movie mid: the phone chat BRAIN -> FOOT, unread; Lena's leg won't work
S.append({"say": "Brain says move. *No reply*. Numb, and floppy.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.1, "focus": [0.55, 0.55]}]},
          "layers": [plate("movie_mid"),
                     person("movie_mid", "lena", 1.9, 1.7, [["sad", 0], ["surprised", 1.6]], hops=[[1.7, 0.03, 0.3]]),
                     {"type": "phone", "sprite": A + "phone.png", "screen": CHAT, "x": 0.3, "y": 0.3, "w": 0.3,
                      "enter": "slide_up", "at": 0.0, "sfx": "whoosh", "tilt": [[0, -14, 4], [3.0, -6, 2]]},
                     hud("delivered", x=0.74, y=0.12, text="0 / 3", tone="red", at=0.6, width_of="0 / 3")]})
# 6. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("movie_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "foot.exe has stopped *responding*", "text_y": 0.2}})
# 7. back inside, released: the knee is gone, signals rush back scrambled, sparks fizz; the 4-step tracker ticks
SPK = [(-0.22, -0.05, 0.6), (0.18, -0.08, 0.8), (-0.05, 0.06, 1.0), (0.3, 0.04, 1.2), (-0.32, 0.03, 1.35), (0.08, -0.12, 1.5),
       (0.24, 0.1, 1.7), (-0.15, 0.1, 1.9)]
S.append({"say": "Uncross, and it wakes up *noisy*. That fizz is *pins and needles*.",
          "transition": "flash", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.1, "focus": [0.5, 0.5]}], "shake": [0.6, 1.4]},
          "layers": [plate("nerve_open")]
                    + stream(0.3, 2.8, "#ffd23a", 10) + stream(0.4, 2.9, "#ff8fd0", 8, rev=True)
                    + [{"type": "image", "svg": SPARK, "x": PRESS[0] + dx, "y": PRESS[1] + dy, "w": 0.06, "enter": "pop", "at": t,
                        "sfx": "pop" if k in (0, 4) else None, "loop": "pulse", "loop_amp": 0.3, "until": t + 1.6, "exit": "fade"}
                       for k, (dx, dy, t) in enumerate(SPK)]
                    + [hud("signals", y=0.1, text="NOISY!", tone="gold", at=0.0, enter="none", width_of="BLOCKED!"),
                       {"type": "tracker", "n": 4, "done": [0.2, 0.5, 0.9, 2.2], "x": 0.5, "y": 0.2, "at": 0.1, "enter": "fade"},
                       txt("PINS & *NEEDLES*", 0.78 - 0.04, 84, enter="pop", at=2.2, sfx="pop")]})
# 8. close payoff: the buzz makes you move; loops to the hook
S.append({"say": "That buzz makes you move, before the squeeze hurts the nerve. Not asleep. *Kinked*.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("movie_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 2.0], ["smirk", 3.8]]),
                     {"type": "optcard", "label": "the buzz", "text": "MOVE!", "tone": "gold", "x": 0.28, "y": 0.12,
                      "w": 0.4, "rotate": -3, "enter": "pop", "at": 0.2, "sfx": "pop"},
                     {"type": "optcard", "label": "the nerve", "text": "SAFE", "tone": "green", "x": 0.72, "y": 0.12,
                      "w": 0.4, "rotate": 3, "enter": "pop", "at": 1.6, "sfx": "pop", "verdict": "tick", "verdict_at": 0.5},
                     {"type": "stamp", "text": "KINKED", "tone": "red", "angle": -6, "size": 84, "x": 0.5, "y": 0.25,
                      "at": 3.6, "sfx": "thud"}]})

job = {"id": ID, "title": "Your foot never falls asleep. Here's what does 🦶",
       "description": "Why does your foot 'fall asleep'? It isn't the blood: neurologists say it's a squashed nerve. Cross "
                      "your legs and the common fibular (peroneal) nerve, which wraps around the bone just below the outside of "
                      "your knee, close to the skin, gets pressed. Like a kinked hose, its signals between brain and foot stop, "
                      "so the foot goes numb and floppy. When you move, the nerve wakes up and the tingling, pins and needles "
                      "(paresthesia), is it coming back online. That annoying buzz makes you shift before a long squeeze can "
                      "injure the nerve. (How the body works, not medical advice.)\n\n"
                      "Sources: The Conversation (What happens when your foot falls asleep); ScienceAlert (neurologists "
                      "Rebecca Traub and Steven Vernino); Colorado Orthopedics (peroneal nerve palsy); Penn Medicine "
                      "(common peroneal nerve dysfunction).",
       "tags": ["foot fell asleep", "pins and needles", "why does your foot fall asleep", "nerves", "human body",
                "paresthesia", "body facts", "science facts", "biology"],
       "hashtags": ["#science", "#humanbody"],
       "instagram": {"hashtags": ["#science", "#humanbody", "#pinsandneedles", "#biologyfacts", "#explained"]},
       "meta": {"format": "big-question", "topic": "why a foot 'falls asleep': not blood flow but a compressed nerve; crossed "
                                                   "legs press the common fibular nerve where it wraps the fibular head just "
                                                   "under the skin; signals blocked like a kinked hose (numb, floppy); on release "
                                                   "the nerve wakes up noisy = pins and needles (paresthesia); the buzz makes you "
                                                   "move before prolonged compression injures the nerve",
                "hook": "question",
                "idea_source": "viral-shaped + unique: a universal everyday feeling everyone has had, explained in one picture "
                               "(kinked cable), with a myth flip (it's not the blood); backlog idea; body niche after a run of "
                               "space Shorts",
                "characters": ["ved", "extra"],
                "sources": ["https://theconversation.com/what-happens-when-your-foot-falls-asleep-164655",
                            "https://www.sciencealert.com/here-s-what-happens-when-your-foot-falls-asleep",
                            "https://www.cortho.org/foot-and-ankle/conditions/peroneal-nerve-palsy/",
                            "https://www.pennmedicine.org/conditions/common-peroneal-nerve-dysfunction"],
                "humour": {"trend": "timeless dry aside (no rising meme fits a body topic this week; 'W chews' already used): "
                                    "side-eye + 'foot.exe has stopped responding'",
                           "beat": "side_eye", "scene": 6},
                "claims": [
                    {"claim": "a foot 'falls asleep' because a nerve is compressed; lack of blood flow is a common misconception", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/here-s-what-happens-when-your-foot-falls-asleep"},
                    {"claim": "the common fibular (peroneal) nerve wraps around the fibular head below the outside of the knee, close to the skin; crossing the legs compresses it", "tag": "PROVEN",
                     "source": "https://www.cortho.org/foot-and-ankle/conditions/peroneal-nerve-palsy/"},
                    {"claim": "compression blocks the nerve's signals like a kinked hose: numbness and trouble moving", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/here-s-what-happens-when-your-foot-falls-asleep"},
                    {"claim": "pins and needles (paresthesia) happen as the nerve regains function", "tag": "PROVEN",
                     "source": "https://theconversation.com/what-happens-when-your-foot-falls-asleep-164655"},
                    {"claim": "the discomfort makes you shift position; prolonged compression (e.g. someone who can't move) can injure a nerve", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/here-s-what-happens-when-your-foot-falls-asleep"}]},
       "thumbnail": {"title": "FOOT *ASLEEP?*", "title_y": 0.15, "title_size": 190, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#7a3fa0", "#f08a24"], "tint_amount": 0.28,
                     "bg": [plate("nerve_squeeze")],
                     "fg": [{"type": "image", "svg": SPARK, "x": 0.22, "y": 0.42, "w": 0.14, "enter": "none"},
                            {"type": "image", "svg": SPARK, "x": 0.8, "y": 0.36, "w": 0.1, "enter": "none"},
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.8, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
