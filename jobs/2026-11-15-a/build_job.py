"""2026-11-15-a: "You've been told DNA is tiny" (scale-shock, "you've been told X" hook). A warm genetics lab with a giant
double-helix sculpture (3 angles) + deep space (Sun to Neptune), cut-outs: nucleus, histone spool, tennis ball, bobbin.
Run after the assets exist: python jobs/2026-11-15-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-15-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("lab_wide", "lab_mid")}

OUT = {   # recurring townspeople: same outfit in every shot
    "noor": {"skin": "#a8714b", "build": "slim", "hair": ["#1a1410", "bun"], "top": ["#f6efe2", "jacket"],
             "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "necklace": "#f2b04a"},
    "leo": {"skin": "#e0b48c", "build": "round", "hair": ["#7a4e2a", "curly"], "hat": ["beret", "#d9534f"],
            "top": ["#6fc3c0", "tshirt"], "bottom": ["#3a3e48", "trousers"], "shoes": "#f6efe2"},
}
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": k.pop("x", 0.5), "y": y, "size": size, "max_w": 0.88,
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
    return L, p


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": k.pop("x", 0.5), "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def card(body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{body}</svg>")


def label(t, color="#1a1410", w=600, fs=60):
    return card(f"<text x='{w/2}' y='{int(fs*1.45)}' text-anchor='middle' font-size='{fs}' fill='{color}' {AN}>{t}</text>", w, int(fs * 2.1))


def stamp(word, color="#d9534f", w=640, fs=110):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='#f6efe2' fill-opacity='0.85' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='126' text-anchor='middle' font-size='{fs}' "
            f"fill='{color}' {AN}>{word}</text></svg>")


HOOK_CARD = card(f"<text x='450' y='106' text-anchor='middle' font-size='84' fill='#1a1410' {AN}>YOU'VE BEEN TOLD...</text>")

# a 2-metre measuring staff (drawn next to Ved, scaled by the stage)
RULER = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 1000'>"
         "<rect x='30' y='0' width='60' height='1000' rx='8' fill='#f2b04a' stroke='#1a1410' stroke-width='6'/>"
         + "".join(f"<line x1='30' y1='{k*50}' x2='{70 if k % 2 else 90}' y2='{k*50}' stroke='#1a1410' stroke-width='5'/>" for k in range(1, 20))
         + "</svg>")

# tennis-ball scale panel
SCALE = card(
    f"<text x='450' y='80' text-anchor='middle' font-size='44' fill='#1a1410' {AN}>NUCLEUS BLOWN UP TO A TENNIS BALL</text>"
    f"<text x='450' y='420' text-anchor='middle' font-size='46' fill='#3a3e48' {F}>thread thinner than a hair</text>",
    900, 470)

FLOW = card(
    f"<text x='130' y='94' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>WIND</text>"
    f"<text x='250' y='94' text-anchor='middle' font-size='50' fill='#d9534f' {AN}>&gt;</text>"
    f"<text x='380' y='94' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>COIL</text>"
    f"<text x='510' y='94' text-anchor='middle' font-size='50' fill='#d9534f' {AN}>&gt;</text>"
    f"<text x='690' y='94' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>COIL AGAIN</text>", 900, 140)

THREAD = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 1400'>"
          "<path d='M70,140 C300,300 150,500 420,640 C700,780 520,980 900,1240' stroke='#ffcf5a' stroke-width='14' fill='none' "
          "stroke-linecap='round' stroke-dasharray='34 14'/></svg>")

DIST = card(f"<text x='450' y='70' text-anchor='middle' font-size='44' fill='#1a1410' {AN}>SUN TO NEPTUNE: 4.5 BILLION KM</text>"
            f"<text x='450' y='138' text-anchor='middle' font-size='44' fill='#d9534f' {AN}>YOUR DNA: EVEN FARTHER</text>", 900, 175)

S = []
# 0. hook (lab mid): "you've been told" card + DNA = TINY at frame 0, then 2 METRES lands
v0, p0 = ved("lab_mid", -0.25, -1.6, [["explain", 0], ["point", 2.4]])
S.append({"say": "You've been told DNA is tiny. Each cell nucleus in you holds *two metres* of it.",
          "caption": "You've been told DNA is tiny. Each cell nucleus in you holds *2 metres* of it.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": [plate("lab_mid"),
                     person("lab_mid", "noor", 2.3, 1.3, [["idle", 0], ["surprised", 2.6]]),
                     v0,
                     {"type": "image", "svg": HOOK_CARD, "x": 0.5, "y": 0.12, "w": 0.78, "rotate": -2, "enter": "none"},
                     txt("DNA = *TINY*", 0.225, 150, enter="none", until=2.3, exit="pop"),
                     txt("*2 METRES*", 0.225, 160, enter="zoom", at=2.4, sfx="boom"),
                     txt("IN EVERY NUCLEUS", 0.3, 64, enter="pop", at=2.8)]})
# 1. lab wide: Ved walks in beside a 2 m staff; then the nucleus, 6 microns
st = ST["lab_wide"]
v1, p1 = ved("lab_wide", -1.2, -3.2, [["welcome", 0], ["point", 1.0], ["explain", 2.4]], walk=[(0, -3.4, -3.4), (1.0, -1.2, -3.2)])
rh = p1["h"] * 2.0 / 1.78
S.append({"say": "Taller than you, in a nucleus six microns wide.", "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": [plate("lab_wide"),
                     {"type": "image", "svg": RULER, "x": p1["x"] + 0.16, "y": p1["y"] + p1["h"] * 0.5 - rh / 2, "w": rh * 0.12 * 1920 / 1080,
                      "enter": "slide_up", "at": 0.3, "sfx": "pop", "allow_outside_safe": True},
                     {"type": "image", "svg": label("2 M", "#d9534f", 300, 60), "x": p1["x"] + 0.16, "y": p1["y"] + p1["h"] * 0.5 - rh - 0.03,
                      "w": 0.2, "enter": "pop", "at": 0.6},
                     v1,
                     sprite("nucleus", 0.68, 0.17, 0.3, enter="zoom", at=1.9, sfx="pop", loop="float", loop_amp=0.006),
                     {"type": "image", "svg": label("6 MICRONS WIDE"), "x": 0.68, "y": 0.29, "w": 0.48, "rotate": 2, "enter": "pop", "at": 2.5, "sfx": "pop"}]})
# 2. lab close: tennis ball = 20 km of thread
S.append({"say": "Scale that nucleus up to a tennis ball, and the DNA becomes *twenty kilometres* of thread.",
          "caption": "Scale that nucleus up to a tennis ball, and the DNA becomes *20 km* of thread.",
          "transition": "zoom", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.5, "zoom": 1.08, "focus": [0.5, 0.48]}]},
          "layers": [plate("lab_close", blur=6),
                     {"type": "image", "svg": SCALE, "x": 0.5, "y": 0.22, "w": 0.86, "enter": "slide_down", "at": 0.05, "sfx": "whoosh"},
                     sprite("nucleus", 0.22, 0.22, 0.13, enter="pop", at=0.4),
                     {"type": "shape", "shape": "arrow", "x": 0.36, "y": 0.22, "w": 0.1, "h": 0.03, "color": "accent", "enter": "pop", "at": 0.9},
                     sprite("tennis", 0.5, 0.22, 0.18, enter="drop", at=1.1, sfx="pop"),
                     {"type": "shape", "shape": "arrow", "x": 0.64, "y": 0.22, "w": 0.1, "h": 0.03, "color": "accent", "enter": "pop", "at": 2.6},
                     sprite("bobbin", 0.79, 0.22, 0.15, enter="pop", at=2.9, sfx="pop"),
                     {"type": "counter", "from": 0, "to": 20, "suffix": " KM", "x": 0.5, "y": 0.385, "size": 120, "color": "accent",
                      "at": 3.0, "count_dur": 1.6, "enter": "pop"}]})
# 3. comic beat: smirk reaction cut-away
S.append({"dur": 1.5, "transition": "cut", "captions": False,
          "layers": [plate("lab_close", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["smirk", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.35, "who": "ved",
                   "text": "my suitcase after one holiday:\n*could never*", "text_y": 0.2}})
# 4. lab close (sharp, the helix sculpture): the spool trick
S.append({"say": "The trick? It winds around protein spools, then coils, and coils again.",
          "transition": "cut", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.1, "focus": [0.52, 0.45]}]},
          "layers": [plate("lab_close"),
                     sprite("spool", 0.5, 0.17, 0.62, enter="slide_left", at=0.5, sfx="whoosh", loop="float", loop_amp=0.006),
                     {"type": "image", "svg": FLOW, "x": 0.5, "y": 0.29, "w": 0.86, "enter": "pop", "at": 2.6, "sfx": "pop"},
                     {"type": "image", "svg": label("PROTEIN SPOOL", w=560, fs=52), "x": 0.3, "y": 0.07, "w": 0.4, "rotate": -3,
                      "enter": "pop", "at": 1.2}]})
# 5. lab wide: count every nucleus, trillions (nuclei rain down, Leo cheers)
v5, _ = ved("lab_wide", -1.2, -3.2, [["explain", 0], ["surprised", 1.8]], hops=[[1.9, 0.05, 0.4]])
S.append({"say": "Now count every cell with a nucleus. *Trillions*.", "transition": "slide_up", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": [plate("lab_wide"),
                     person("lab_wide", "leo", 2.6, 0.2, [["idle", 0], ["surprised", 1.4], ["cheer", 2.2]], hops=[[2.2, 0.05, 0.4]]),
                     v5]
                    + [sprite("nucleus", x, y, 0.09, enter="drop", at=0.2 + k * 0.22, sfx="pop" if k % 3 == 0 else None)
                       for k, (x, y) in enumerate([(0.2, 0.12), (0.42, 0.09), (0.66, 0.13), (0.82, 0.08), (0.3, 0.2), (0.55, 0.19),
                                                   (0.76, 0.22), (0.14, 0.27), (0.4, 0.29), (0.64, 0.3)])]
                    + [txt("*TRILLIONS*", 0.33, 140, enter="zoom", at=2.0, sfx="boom")]})
# 6. space: end to end, billions of km, past Neptune
S.append({"say": "End to end: *billions* of kilometres. Farther than the Sun is from Neptune.",
          "caption": "End to end: *billions of km*. Farther than the Sun is from Neptune.",
          "transition": "zoom", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.52, 0.52]}]},
          "layers": [plate("space"),
                     {"type": "image", "svg": THREAD, "x": 0.5, "y": 0.48, "w": 0.92, "enter": "fade", "at": 0.3, "enter_dur": 1.2, "sfx": "whoosh"},
                     {"type": "image", "svg": DIST, "x": 0.5, "y": 0.3, "w": 0.86, "enter": "slide_down", "at": 2.4, "sfx": "pop"},
                     {"type": "image", "svg": label("NEPTUNE", w=420, fs=50), "x": 0.66, "y": 0.72, "w": 0.3, "enter": "pop", "at": 1.6}]})
# 7. payoff close-up (loops to the hook)
S.append({"say": "All of it, folded inside you. Tiny? Not even close.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["warm", 1.6], ["smirk", 2.8]]),
                     txt("DNA = TINY?", 0.15, 130, enter="pop", at=0.1, sfx="pop"),
                     {"type": "image", "svg": stamp("NOT EVEN CLOSE", w=960, fs=92), "x": 0.5, "y": 0.27, "w": 0.8, "rotate": -8,
                      "enter": "zoom", "at": 2.2, "sfx": "boom"}]})

SRC = ["https://www.sciencefocus.com/the-human-body/how-long-is-your-dna",
       "https://scienceinsights.org/how-long-is-your-dna-if-you-stretched-it-out/",
       "https://www.sciencenews.org/article/body's-bacteria-don't-outnumber-human-cells-so-much-after-all",
       "https://openoregon.pressbooks.pub/mhccbiology112/chapter/how-dna-is-arranged-in-a-cell/",
       "https://en.wikipedia.org/wiki/Neptune"]
job = {"id": ID, "title": "You've been told DNA is tiny. It's 2 metres 🧬",
       "description": "Each nucleus in your cells holds about 2 metres of DNA, packed into a space ~6 microns wide. Scale the "
                      "nucleus up to a tennis ball and that's ~20 km of thread. It fits by winding around protein spools "
                      "(histones) and coiling again and again. Add up the trillions of cells with a nucleus (red blood cells "
                      "have none) and it's billions of km, farther than the Sun is from Neptune (~4.5 billion km).\n\n"
                      "Sources: BBC Science Focus; Sender, Fuchs & Milo 2016 (via Science News); OpenOregon Biology.",
       "tags": ["how long is your dna", "dna length", "dna packing", "histones", "cell nucleus", "human body",
                "biology", "science explained", "scale of the universe"],
       "hashtags": ["#science", "#biology"],
       "instagram": {"hashtags": ["#science", "#biology", "#dna", "#humanbody", "#explained"]},
       "meta": {"format": "scale-shock", "topic": "how long your DNA is: ~2 m per nucleus in ~6 microns (tennis ball = ~20 km of thread), histone spools and coiling, billions of km in total (past Sun-Neptune)",
                "hook": "you've been told X",
                "idea_source": "backlog (ideas.md 'How long is all the DNA in your body?') + viral-shaped (an invisible molecule made measurable: 2 m, tennis ball = 20 km) + the review's hook test ('you've been told X' on a scale-shock)",
                "characters": ["ved", "extra"],
                "sources": SRC,
                "experiment": "'you've been told X' hook test (review 2026-11-15), 2 of 2 (scale-shock)",
                "humour": {"trend": "timeless dry reaction (no current meme fit the topic naturally): smirk card 'my suitcase after one holiday: could never'",
                           "beat": "smirk", "scene": 3},
                "claims": [
                    {"claim": "a human cell nucleus holds ~2 m of DNA (46 chromosomes, ~6 billion base pairs)", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "the nucleus is ~6 microns across", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "scaled to a tennis ball (~6.5 cm), 2 m of DNA becomes ~20 km of thread ~0.02 mm thick (our arithmetic: x ~10,800)", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "DNA wraps around histone proteins and is coiled further into chromatin", "tag": "PROVEN", "source": SRC[3]},
                    {"claim": "~30 trillion human cells, ~84% red blood cells (no nucleus), so trillions of nucleated cells", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "total DNA length estimates range ~14 to 74 billion km depending on counting; even the low end is far past Sun-Neptune (~4.5 billion km)", "tag": "PROVEN", "source": SRC[1]}]},
       "thumbnail": {"title": "2 METRES *INSIDE?*", "title_y": 0.15, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#ffcf5a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.35,
                     "bg": [plate("lab_close")],
                     "fg": [sprite("spool", 0.72, 0.5, 0.5),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.4, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
for sc in S:
    for L in sc.get("layers", []):
        if L.get("sfx") is None:
            L.pop("sfx", None)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
