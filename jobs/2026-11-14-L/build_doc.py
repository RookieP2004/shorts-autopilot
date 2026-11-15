"""Deep Dive 2026-11-14-L, documentary cut (owner's request 2026-11-15: long videos in a documentary style that feels
hand-made). Same verified script and the same 3D world as build_job.py, re-edited with the doc toolkit (autopilot/doc.py):
chapter title cards, archival "reconstruction" shots of the 1909 lab, an evidence board (photos, clippings, red string,
marker annotations), a timeline, lower-third supers and source tags, serif type instead of Shorts headlines, no burned
captions, film grain and a scored soundtrack that changes with the story.
Run: python jobs/2026-11-14-L/build_doc.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from PIL import Image
import numpy as np

# reuse the original build's helpers, people, plates and diagrams (it also writes the old job.json, overwritten below)
NS = {"__name__": "old_build"}
exec(open("jobs/2026-11-14-L/build_job.py").read(), NS)
J, A, ST = NS["J"], NS["A"], NS["ST"]
plate, fg, sprite, person, ved, close_ved, staged, talk, electrons, clean = (NS[k] for k in (
    "plate", "fg", "sprite", "person", "ved", "close_ved", "staged", "talk", "electrons", "clean"))
SVG = {k: NS[k] for k in ("pud", "nuc", "rep", "pau", "ns", "pie")}
random.seed(141)

S, CH, CUES = [], [], []
DOCA = J + "assets/doc/"
os.makedirs(DOCA, exist_ok=True)


# ------------------------------------------------------------------ doc helpers
def png(name, svg, width=1400):
    """Render one of the build's SVG diagram cards to a PNG once, so it can be printed and taped to the board."""
    from autopilot import sprites
    path = DOCA + name + ".png"
    if not os.path.exists(path):
        sprites.svg_image(svg, width).convert("RGB").save(path)
    return path


def cork():
    path = DOCA + "cork.png"
    if not os.path.exists(path):
        rng = np.random.default_rng(5)
        W, H = 1920, 1080
        base = np.array([150, 108, 70], np.float32)
        n1 = rng.standard_normal((H // 4, W // 4)).astype(np.float32)
        n1 = np.asarray(Image.fromarray(((n1 * 30) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) - 128
        speck = rng.random((H, W)).astype(np.float32)
        a = base[None, None, :] + n1[..., None] * 0.6
        a[speck > 0.985] *= 0.55
        a[speck < 0.012] *= 1.25
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
        a *= (1 - 0.6 * np.clip(d - 0.2, 0, 1))[..., None]
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path)
    return path


def chapter(title):
    CH.append({"scene": len(S), "title": title})


def cue(style, **k):
    CUES.append({"scene": len(S), "style": style, **k})


def scene(say, layers, **k):
    s = {"say": say, "layers": layers, **k}
    S.append(s)
    return s


def dtxt(t, x, y, size=70, font="serif", at=0.3, **k):
    """Documentary type: book serif, no outline, soft shadow, drifts up as it fades in."""
    return {"type": "text", "text": t, "font": font, "x": x, "y": y, "size": size, "max_w": k.pop("max_w", 0.6),
            "color": k.pop("color", "primary"), "highlight": k.pop("highlight", "accent"), "enter": k.pop("enter", "rise"),
            "enter_dur": k.pop("enter_dur", 0.7), "at": at, "shadow": True, "align": k.pop("align", "center"),
            "stroke": k.pop("stroke", "#120e0a"), "stroke_width": k.pop("stroke_width", 3), **k}


def hand(t, x, y, size=78, at=0.3, color="primary", **k):
    return dtxt(t, x, y, size, font="hand", at=at, color=color, **k)


def lower(title, sub, at=0.6, until=None, x=0.055, y=0.78):
    L = {"type": "lower_third", "title": title, "sub": sub, "x": x, "y": y, "at": at}
    if until:
        L.update(until=until, exit_dur=0.4)
    return L


def source(text, at=0.8, until=None):
    L = {"type": "tag", "text": text, "x": 0.965, "y": 0.84, "align": "right", "at": at}
    if until:
        L.update(until=until, exit_dur=0.3)
    return L


def card_paper(name, x, y, w, at, rot=0.0, caption=None, sfx="paper", **k):
    return {"type": "paper", "kind": "photo", "path": png(name, SVG[name]), "x": x, "y": y, "w": w, "rotate": rot,
            "at": at, "enter": "slam", "enter_dur": 0.35, "sfx": sfx, "tape": ["tl", "tr"], **({"caption": caption} if caption else {}), **k}


def sticky(text, x, y, at, rot=-4, w=0.26, **k):
    return {"type": "paper", "kind": "note", "text": text, "paper": "#f6e27f", "font": "hand", "text_size": 0.11,
            "w": w, "x": x, "y": y, "rotate": rot, "at": at, "enter": "slam", "enter_dur": 0.3, "sfx": "paper", "tape": ["tc"], **k}


def mark(shape, at, **k):
    return {"type": "marker", "shape": shape, "at": at, "sfx": k.pop("sfx", "marker"), **k}


def chapter_card(num, title, under, music=None):
    """2.6 s title card: the chapter's world, blurred and dimmed, the title set in serif. Low hit, music changes here."""
    chapter(title)
    if music:
        cue(music)
    S.append({"dur": 2.8, "transition": "dip", "transition_frames": 14, "captions": False,
              "layers": [dict(plate(under), blur_keys=[[0, 4], [1.2, 16]], pan=[0, 0, 0.05]),
                         {"type": "chapter", "num": num, "title": title, "at": 0.15}],
              "sfx": "hit", "camera": {"zoom": [1.02, 1.05], "focus": [0.5, 0.5]}})


def board_bg():
    return {"type": "image", "path": cork(), "x": 0.5, "y": 0.5, "w": 1.04, "enter": "none", "pan": [0.01, 0, 0.03]}


# =================================================================== cold open (letterboxed, no titles yet)
chapter("A sugar cube")
cue("wonder", key="D", scale="dorian", bpm=64)
scene("This sugar cube could hold every human on Earth. All *eight billion* of us.",
      [plate("cafe_table", blur_keys=[[0, 9], [1.4, 0]]),
       dtxt("Every human on Earth.", 0.5, 0.2, 64, at=1.6, font="serif_i"),
       dtxt("*8,000,000,000* of us.", 0.5, 0.31, 76, at=3.0)],
      letterbox=0.11, letterbox_in=1.2, lead=0.9, camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.56]}, transition="cut")
scene("Sounds impossible. But stick with me, and you'll see why it's true, why you've never really touched anything, "
      "and why you still don't fall through your chair.",
      talk("cafe_mid", [["explain", 0], ["shrug", 2.0], ["point", 6.0]],
           top=[dtxt("why it's true", 0.7, 0.24, 58, at=1.6, font="serif_i"),
                dtxt("why you've never touched anything", 0.7, 0.36, 58, at=4.2, font="serif_i", max_w=0.48),
                dtxt("why you don't fall through", 0.7, 0.48, 58, at=6.6, font="serif_i", max_w=0.48)]),
      letterbox=0.11, transition="cut")
scene("Because almost everything around you, the table, the cup, the people... you. It's mostly empty space. So let's find out how empty.",
      staged("cafe_wide",
             behind=[person("cafe_wide", "seller", -1.4, 2.4, [["idle", 0], ["wave", 1.0]]),
                     person("cafe_wide", "lena", 3.5, 2.0, [["explain", 0]]),
                     person("cafe_wide", "ravi", 4.9, 2.2, [["happy", 0]]),
                     person("cafe_wide", "omar", -2.6, 3.0, [["hold", 0]])],
             front=[person("cafe_wide", "amina", 1.5, -0.4, [["idle", 0], ["surprised", 4.6]]),
                    person("cafe_wide", "tomas", -3.2, -1.2, [["idle", 0]], walk=[(0, -5.4, -1.6), (2.6, -2.6, -1.0)]),
                    ved("cafe_wide", -0.6, -1.6, [["welcome", 0], ["point", 2.6], ["explain", 5.0]], walk=[(0, 2.6, -2.2), (1.4, -0.6, -1.6)])]),
      letterbox=0.11, transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.52]})
S.append({"dur": 3.6, "captions": False, "transition": "dip", "transition_frames": 16, "sfx": "hit", "sfx_at": 0.3, "bg": {"type": "solid", "colors": ["#0b0d10"]}, 
          "layers": [dict(plate("cafe_wide"), blur_keys=[[0, 18]], opacity=0.55),
                     {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 0.6, "color": "#07090b", "opacity": 0.55, "enter": "none"},
                     dtxt("99.9999% EMPTY", 0.5, 0.45, 120, at=0.35, font="serif", enter_dur=1.2),
                     dtxt("A FILM ABOUT NOTHING (AND EVERYTHING)", 0.5, 0.57, 30, at=1.2, font="cond", color="accent", max_w=0.8)],
          "camera": {"zoom": [1.0, 1.03], "focus": [0.5, 0.5]}, "letterbox": 0.11})

# =================================================================== 2. How small is an atom?
chapter_card(1, "How small is an atom?", "cafe_mid", "doc")
scene("Everything is made of atoms, and atoms are tiny. Line up *ten million* of them, and you'd cover just one millimetre.",
      staged("cafe_mid",
             behind=[person("cafe_mid", "seller", 1.6, 2.6, [["idle", 0]])],
             front=[ved("cafe_mid", -0.7, -0.6, [["explain", 0], ["point", 2.4]], walk=[(0, -2.4, -1.0), (1.2, -0.7, -0.6)])],
             top=[sticky("1 mm = 10,000,000 atoms side by side", 0.68, 0.26, 2.8, rot=3, w=0.3),
                  mark("underline", 3.8, box=[0.58, 0.31, 0.74, 0.31], color="#2a6fd6")]),
      transition="cut")
scene("Your body holds about seven billion billion billion atoms. That's a seven with twenty-seven zeros.",
      talk("cafe_mid", [["serious", 0], ["surprised", 3.0]], x=0.73,
           top=[{"type": "counter", "from": 1, "to": 7, "count_dur": 1.6, "at": 0.6, "x": 0.34, "y": 0.32, "font": "cond",
                 "suffix": ",000,000,000,000,000,000,000,000,000", "size": 54, "color": "primary", "enter": "fade", "sfx": "type"},
                dtxt("atoms in *you*", 0.34, 0.45, 66, at=3.0, font="serif_i"),
                source("SOURCE: JEFFERSON LAB (70 KG ADULT)", at=1.2)]),
      transition="cut")
scene("Too small to picture. So let's cheat. Let's blow one single atom up to the size of a *football stadium*.",
      [plate("stadium_wide", pan=[0, 0, -0.08]),
       dtxt("one atom", 0.3, 0.16, 70, at=2.4, font="serif_i"), dtxt("=", 0.5, 0.16, 70, at=2.9),
       dtxt("one *stadium*", 0.7, 0.16, 70, at=3.2, font="serif_i")],
      transition="whip", transition_frames=9, sfx="swoosh_soft", camera={"zoom": [1.0, 1.0], "drift": 1.4})
pt = ST["stadium_pitch"].point(0, 0, 0.1)
scene("Walk down to the centre spot... and there's the nucleus. About the size of a *marble*.",
      staged("stadium_pitch",
             front=[ved("stadium_pitch", -4.0, 0.9, [["explain", 0], ["point", 2.6]], walk=[(0, -6.0, -0.4), (2.2, -4.0, 0.9)])],
             top=[mark("circle", 2.8, box=[pt[0] - 0.035, pt[1] - 0.05, pt[0] + 0.035, pt[1] + 0.04]),
                  hand("the nucleus", pt[0] + 0.13, pt[1] - 0.12, 74, at=3.2, color="#f2d06a"),
                  mark("arrow", 3.4, **{"from": [pt[0] + 0.1, pt[1] - 0.09], "to": [pt[0] + 0.035, pt[1] - 0.03]}, bend=-0.3, sfx="none")]),
      transition="cut")
scene("It's about a hundred thousand times smaller than the atom itself. And that marble holds more than *99.9 percent* of the atom's mass.",
      [plate("stadium_marble", pan=[0, 0, 0.08]),
       dtxt("100,000× smaller than the atom", 0.5, 0.15, 64, at=0.6, until=3.8, exit_dur=0.4, font="serif_i", max_w=0.8),
       dtxt("*99.9%* of the mass", 0.5, 0.15, 86, at=4.2),
       source("VERIFIED: OPENSTAX UNIVERSITY PHYSICS VOL. 3", at=4.6)],
      transition="cut")
scene("The electrons? They're way out in the back rows of the stands. And between the marble and the seats...",
      [plate("stadium_wide")] + electrons(7, 0.6, y0=0.48, rx=0.44, ry=0.36) +
      [hand("electrons: the back rows", 0.5, 0.14, 80, at=1.0, color="#f2d06a", max_w=0.8)],
      transition="cut", camera={"zoom": [1.04, 1.0], "focus": [0.5, 0.5]})
cue("none")
scene("...there's no air. No stuff. Just a whole stadium of *nothing*.",
      staged("stadium_pitch",
             front=[ved("stadium_pitch", -4.0, 0.9, [["shrug", 0], ["welcome", 1.6]])],
             top=[dtxt("nothing.", 0.5, 0.17, 130, at=1.8, font="serif_i", enter_dur=1.4)]),
      transition="cut", camera={"zoom": [1.0, 1.1], "focus": [0.45, 0.5]}, pad=1.0)
cue("doc", key="D")
S.append({"dur": 2.6, "captions": False, "transition": "cut",
          "layers": [plate("stadium_pitch", blur=10), sticky("Personal space? Atoms invented it.", 0.5, 0.45, 0.2, rot=-5, w=0.34)],
          "camera": {"zoom": [1.04, 1.08], "focus": [0.5, 0.45]}})

# =================================================================== 3. The gold foil surprise
chapter_card(2, "The gold foil surprise", "lab_wide", "tension")
scene("But how do we actually know this? In 1909, in Manchester, the physicist Ernest Rutherford gave two of his team a strange job.",
      staged("lab_wide",
             behind=[person("lab_wide", "rutherford", 0.9, 1.7, [["explain", 0], ["point", 4.4]])],
             front=[person("lab_wide", "geiger", -1.0, -0.4, [["idle", 0]], walk=[(0, -3.6, -1.0), (3.0, -1.0, -0.4)]),
                    person("lab_wide", "marsden", 2.6, -0.5, [["idle", 0], ["surprised", 5.2]], walk=[(0, 4.8, -0.9), (3.4, 2.6, -0.5)])],
             top=[lower("Manchester, England", "1909. The physics laboratory of Ernest Rutherford", at=1.2)]),
      look="archival", sfx="projector", transition="cut")
scene("Hans Geiger and a twenty-year-old student, Ernest Marsden, fired tiny *alpha particles* at a sheet of gold, beaten thinner than paper.",
      staged("lab_mid",
             behind=[person("lab_mid", "geiger", 0.2, 1.5, [["point", 0], ["explain", 3.0]]),
                     person("lab_mid", "marsden", 1.5, 1.5, [["hold", 0], ["point", 4.0]])],
             top=[lower("Hans Geiger", "physicist, 26", at=0.4, until=2.6),
                  lower("Ernest Marsden", "undergraduate student, 20", at=2.9, until=5.2),
                  sprite("alpha", 0.2, 0.3, 0.07, enter="fade", at=5.4), hand("alpha particle", 0.2, 0.42, 58, at=5.6),
                  sprite("goldfoil", 0.84, 0.3, 0.11, enter="fade", at=6.6), hand("gold foil", 0.84, 0.47, 58, at=6.8)]),
      look="archival", transition="cut")
scene("Each particle that hit a screen made a tiny flash of light. So they sat in the dark, counting flashes through a microscope. One. By. One.",
      staged("lab_mid",
             behind=[person("lab_mid", "marsden", 1.5, 1.5, [["point", 0], ["explain", 3.4]]),
                     person("lab_mid", "geiger", 0.2, 1.5, [["idle", 0], ["shrug", 5.6]])],
             top=[{"type": "shape", "shape": "circle", "x": 0.5, "y": 0.5, "w": 1.6, "color": "#05070f", "opacity": 0.62, "enter": "fade", "at": 1.8},
                  {"type": "shape", "shape": "burst", "x": 0.62, "y": 0.5, "w": 0.04, "color": "#d8ffe6", "enter": "pop", "at": 5.2, "until": 5.45, "sfx": "click"},
                  {"type": "shape", "shape": "burst", "x": 0.6, "y": 0.52, "w": 0.04, "color": "#d8ffe6", "enter": "pop", "at": 6.0, "until": 6.25, "sfx": "click"},
                  {"type": "shape", "shape": "burst", "x": 0.63, "y": 0.49, "w": 0.04, "color": "#d8ffe6", "enter": "pop", "at": 6.8, "until": 7.05, "sfx": "click"}]),
      look="archival", transition="cut")
scene("At the time, scientists pictured the atom as a soft pudding of charge. So the particles should sail straight through.",
      [board_bg(),
       card_paper("pud", 0.33, 0.47, 0.42, 0.3, rot=-3),
       {"type": "paper", "kind": "doc", "title": "J. J. THOMSON, 1904", "text": "The atom: a sphere of positive charge, with electrons dotted through it like plums in a pudding.",
        "w": 0.3, "x": 0.74, "y": 0.42, "rotate": 4, "at": 1.6, "enter": "slam", "sfx": "paper", "tape": ["tl", "tr"]},
       mark("underline", 3.6, box=[0.62, 0.54, 0.86, 0.54])],
      transition="paper", transition_frames=14, camera={"zoom": [1.0, 1.05], "focus": [0.48, 0.48]})
scene("And almost all of them did.",
      [plate("lab_close")] +
      [sprite("alpha", 0.0, 0.52, 0.03, at=0.2 + i * 0.32, keys=[{"t": 0, "x": -0.05, "y": 0.5 + 0.02 * (i % 3)},
              {"t": 0.9, "x": 1.08, "y": 0.47 + 0.03 * (i % 3), "ease": "linear"}], until=0.2 + i * 0.32 + 0.9) for i in range(7)] +
      [source("VISUALISATION", at=0.2)],
      transition="cut", min_dur=2.6)
cue("tension", key="D", gain=1.2)
scene("But about one in every *eight thousand*... bounced right back.",
      [plate("lab_close")] +
      [sprite("alpha", 0.0, 0.52, 0.03, at=0.2 + i * 0.5, keys=[{"t": 0, "x": -0.05, "y": 0.5}, {"t": 0.9, "x": 1.08, "y": 0.48, "ease": "linear"}],
              until=0.2 + i * 0.5 + 0.9) for i in range(3)] +
      [sprite("alpha", 0.0, 0.52, 0.045, at=2.0, keys=[{"t": 0, "x": -0.05, "y": 0.52}, {"t": 0.55, "x": 0.5, "y": 0.52, "ease": "linear"},
              {"t": 1.2, "x": -0.08, "y": 0.3, "ease": "out"}], sfx="thud"),
       {"type": "shape", "shape": "burst", "x": 0.5, "y": 0.52, "w": 0.1, "color": "accent", "enter": "pop", "at": 2.5, "until": 3.0},
       mark("arrow", 2.9, **{"from": [0.47, 0.45], "to": [0.12, 0.3]}, bend=0.25, color="#f2d06a"),
       dtxt("1 in *8,000*", 0.5, 0.16, 96, at=3.0), source("GEIGER & MARSDEN, PROC. ROYAL SOCIETY, 1909", at=3.4)],
      transition="cut", camera={"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.4, "zoom": 1.02, "focus": [0.5, 0.5]},
                                         {"t": 2.7, "zoom": 1.12, "focus": [0.5, 0.5]}]})
cue("doc", key="A", scale="minor")
scene("Rutherford later said it was as incredible as firing a fifteen-inch shell at a piece of tissue paper... and having it come back and hit you.",
      [dict(plate("lab_mid"), blur=18, opacity=0.45),
       {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 0.6, "color": "#07090b", "opacity": 0.6, "enter": "none"},
       dtxt("“It was quite the most incredible event that has ever happened to me in my life. It was almost as incredible "
            "as if you fired a 15-inch shell at a piece of tissue paper and it came back and hit you.”",
            0.5, 0.42, 50, at=0.4, font="serif_i", max_w=0.72, enter_dur=1.6),
       dtxt("ERNEST RUTHERFORD, 1936 LECTURE", 0.5, 0.66, 28, at=2.4, font="cond", color="accent", max_w=0.8)],
      bg={"type": "solid", "colors": ["#0b0d10"]}, transition="dip", transition_frames=12, camera={"zoom": [1.0, 1.04], "focus": [0.5, 0.45]}, pad=0.8)
scene("The only explanation: nearly all the atom's mass is packed into one tiny, dense core.",
      [board_bg(),
       {"type": "paper", "kind": "photo", "path": A + "plate_lab_close.png", "tone": "sepia", "caption": "Manchester, 1909",
        "w": 0.28, "x": 0.2, "y": 0.36, "rotate": -5, "at": 0.1, "enter": "slam", "sfx": "paper"},
       sticky("1 in 8,000 bounced back!", 0.2, 0.76, 0.6, rot=4, w=0.24),
       {"type": "paper", "kind": "clip", "masthead": "Philosophical Magazine, May 1911",
        "title": "The Scattering of Alpha and Beta Particles by Matter and the Structure of the Atom", "w": 0.3, "x": 0.53, "y": 0.4,
        "rotate": 2, "at": 1.4, "enter": "slam", "sfx": "paper", "stamp": "1911"},
       card_paper("nuc", 0.83, 0.62, 0.3, 2.6, rot=-3),
       {"type": "string", "points": [[0.2, 0.68], [0.5, 0.2], [0.79, 0.45]], "at": 3.4, "sfx": "tape"},
       mark("circle", 4.6, box=[0.7, 0.54, 0.79, 0.71])],
      transition="paper", transition_frames=14, camera={"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]},
                                                                {"t": 5.5, "zoom": 1.08, "focus": [0.6, 0.52]}]})
scene("In 1911, Rutherford published the idea. We call that core the *nucleus*.",
      staged("lab_wide",
             behind=[person("lab_wide", "rutherford", 0.9, 1.7, [["explain", 0], ["cheer", 2.6]], hops=[[2.8, 0.03, 0.45]])],
             front=[person("lab_wide", "geiger", -1.0, -0.4, [["happy", 2.8]]),
                    person("lab_wide", "marsden", 2.6, -0.5, [["cheer", 2.8]])],
             top=[dtxt("the *nucleus*", 0.5, 0.14, 92, at=2.4)]),
      transition="cut", leak=[0.4, 2.4, 0.45])

# =================================================================== 4. Is it really empty?
chapter_card(3, "Is it really empty?", "stadium_wide", "doc")
scene("Now, a fair warning. 'Mostly empty space' is the classic picture. But many physicists say it's a little misleading.",
      talk("stadium_pitch", [["serious", 0], ["point", 3.4]],
           top=[dtxt("a fair warning", 0.7, 0.3, 74, at=0.6, font="serif_i")]),
      transition="cut")
scene("Electrons aren't little balls zooming round the stands. Quantum physics says each one is *spread out*, like a fog, filling the whole atom.",
      [plate("stadium_wide")] + electrons(6, 0.0, y0=0.48, rx=0.44, ry=0.36) +
      [{"type": "image", "svg": NS["fog"], "x": 0.5, "y": 0.5, "w": 0.95, "enter": "fade", "enter_dur": 1.8, "at": 3.0},
       hand("not a ball: a cloud", 0.5, 0.14, 84, at=4.0, color="#bfe8ff"),
       source("SEE: E. SIEGEL, 'YOU ARE NOT MOSTLY EMPTY SPACE'", at=4.6)],
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.48]})
scene("So which is it? If you ask where the mass sits, the atom is almost all empty. If you ask where the electron can be, it fills the space. Both are true. They just answer different questions.",
      [board_bg(),
       {"type": "paper", "kind": "doc", "title": "Q: WHERE IS THE MASS?", "text": "Almost all of it in the nucleus. By mass, the atom is nearly empty.",
        "w": 0.34, "x": 0.29, "y": 0.42, "rotate": -3, "at": 0.8, "enter": "slam", "sfx": "paper"},
       {"type": "paper", "kind": "doc", "title": "Q: WHERE CAN THE ELECTRON BE?", "text": "Everywhere in the atom. By where the electron can be, it is full.",
        "w": 0.34, "x": 0.71, "y": 0.47, "rotate": 3, "at": 4.4, "enter": "slam", "sfx": "paper"},
       mark("check", 3.0, box=[0.4, 0.58, 0.45, 0.64], color="#2f8f4a"),
       mark("check", 7.4, box=[0.82, 0.63, 0.87, 0.69], color="#2f8f4a"),
       hand("both true.", 0.5, 0.85, 90, at=9.6, color="#f6efe2")],
      transition="paper", transition_frames=14, camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.5]})

# =================================================================== 5. Why you don't fall through your chair
chapter_card(4, "Why you don't fall through your chair", "cafe_mid", "doc")
CUES[-1].update(key="G", scale="dorian")
scene("So if atoms are that roomy... why don't you sink straight through your chair?",
      staged("cafe_mid",
             behind=[person("cafe_mid", "seller", 1.6, 2.6, [["idle", 0], ["shrug", 2.0]])],
             front=[ved("cafe_mid", -1.1, -0.3, [["think", 0], ["shrug", 2.4]], walk=[(0, -2.8, -0.8), (1.6, -1.1, -0.3)])],
             top=[dtxt("why don't you *sink?*", 0.62, 0.15, 78, at=2.0, font="serif_i")]),
      transition="cut")
scene("Two reasons. First: the outside of every atom is electrons, and electrons all carry a *negative* charge. Like charges push each other away. Hard.",
      talk("cafe_mid", [["explain", 0], ["point", 3.0], ["crossed", 7.0]], x=0.27,
           top=[card_paper("rep", 0.68, 0.38, 0.44, 1.2, rot=2), mark("underline", 6.6, box=[0.6, 0.47, 0.77, 0.47])]),
      transition="cut")
scene("Second: a quantum rule called the *Pauli exclusion principle*. No two electrons can squeeze into the same state. So atoms refuse to collapse into each other.",
      staged("market_wide",
             behind=[person("market_wide", "seller", 0.3, 0.8, [["shrug", 0]])],
             front=[person("market_wide", "tomas", -1.6, -1.4, [["idle", 0], ["shrug", 4.0]], walk=[(0, -4.0, -2.0), (2.4, -1.6, -1.4)]),
                    person("market_wide", "amina", -0.6, -1.2, [["idle", 0], ["point", 4.4]]),
                    ved("market_wide", 2.2, -2.6, [["explain", 0], ["point", 5.0]])],
             top=[card_paper("pau", 0.5, 0.24, 0.46, 1.6, rot=-1.5),
                  lower("Wolfgang Pauli", "physicist, proposed the exclusion principle in 1925", at=3.4, until=8.0)]),
      transition="cut")
scene("In 1967, the physicists Freeman Dyson and Andrew Lenard proved that without this rule, ordinary matter would *collapse*. Putting two objects together would release energy like an atomic bomb.",
      [{"type": "image", "path": cork(), "x": 0.5, "y": 0.5, "w": 1.04, "enter": "none", "opacity": 0.45},
       {"type": "timeline", "x0": 0.12, "x1": 0.88, "y": 0.8, "draw_dur": 1.6, "at": 0.2, "active": 4,
        "events": [{"pos": 0.0, "year": "1904", "label": "Thomson's pudding"}, {"pos": 0.2, "year": "1909", "label": "gold foil"},
                   {"pos": 0.4, "year": "1911", "label": "the nucleus"}, {"pos": 0.64, "year": "1925", "label": "Pauli's rule"},
                   {"pos": 1.0, "year": "1967", "label": "Dyson & Lenard"}]},
       {"type": "paper", "kind": "clip", "masthead": "Journal of Mathematical Physics, 1967",
        "title": "Stability of Matter", "w": 0.32, "x": 0.34, "y": 0.38, "rotate": -2, "at": 1.8, "enter": "slam", "sfx": "paper", "stamp": "1967"},
       sticky("No Pauli rule = matter collapses. Two objects meeting = an atomic bomb.", 0.71, 0.38, 4.6, rot=4, w=0.3),
       mark("underline", 9.0, box=[0.6, 0.49, 0.83, 0.49])],
      bg={"type": "solid", "colors": ["#120e0b"]}, transition="paper", transition_frames=14, camera={"zoom": [1.0, 1.04], "focus": [0.5, 0.48]})
scene("So when you shake someone's hand, your atoms never bump like two billiard balls. What you feel as touch... is electrons pushing back.",
      staged("market_mid",
             behind=[person("market_mid", "seller", 0.35, 0.8, [["idle", 0]])],
             front=[person("market_mid", "tomas", -0.9, -0.7, [["give", 0.4], ["happy", 3.0]], walk=[(0, -2.8, -1.2), (1.6, -0.9, -0.7)]),
                    person("market_mid", "amina", 0.3, -0.7, [["take", 0.4], ["happy", 3.0]]),
                    ved("market_mid", 1.6, -1.6, [["explain", 0], ["point", 4.6]])],
             top=[hand("touch = electrons pushing back", 0.5, 0.13, 80, at=5.0, color="#f2d06a", max_w=0.8)]),
      transition="cut")
scene("Some physicists say that push is simply what touching means. Fair enough. Either way, it's a force you feel, not a wall of stuff.",
      talk("market_close", [["shrug", 0], ["warm", 3.2]],
           top=[dtxt("a *force,* not a wall", 0.68, 0.32, 76, at=4.2, font="serif_i")]),
      transition="cut")
S.append({"dur": 2.8, "captions": False, "transition": "cut",
          "layers": [plate("market_close", blur=10), sticky("Me: touching grass.\nThe grass: technically, no.", 0.5, 0.45, 0.2, rot=4, w=0.34)],
          "camera": {"zoom": [1.04, 1.08], "focus": [0.5, 0.45]}})

# =================================================================== 6. Squeeze out the space
chapter_card(5, "Squeeze out the space", "cafe_table", "doc")
scene("Now, back to our sugar cube. Take every atom in every person on Earth, and squeeze out all that empty space.",
      [plate("cafe_table")] +
      [person("cafe_mid", ["amina", "tomas", "lena", "omar", "ravi", "seller"][i], 0, 0, [["idle", 0]],
              x=[0.1, 0.9, 0.2, 0.8, 0.05, 0.95][i], y=0.78, h=0.3, ground=False, at=1.6 + i * 0.3, enter="fade",
              keys=[{"t": 0, "x": [0.1, 0.9, 0.2, 0.8, 0.05, 0.95][i], "y": 0.78, "scale": 1.0},
                    {"t": 3.0 - i * 0.1, "x": [0.1, 0.9, 0.2, 0.8, 0.05, 0.95][i], "y": 0.78, "scale": 1.0},
                    {"t": 4.0 - i * 0.1, "x": 0.5, "y": 0.6, "scale": 0.05, "ease": "in"}]) for i in range(6)] +
      [dtxt("squeeze out the space", 0.5, 0.14, 74, at=0.6, font="serif_i")],
      transition="cut")
clean(S[-1]["layers"])
scene("All eight billion of us would fit in a cube about this size. But it would still weigh as much as all of us. *Hundreds of millions* of tonnes.",
      talk("cafe_table", [["explain", 0], ["point", 2.0], ["surprised", 5.4]], x=0.27,
           top=[sprite("sugar_cube", 0.68, 0.32, 0.14, enter="fade", at=1.6),
                hand("all of us, compressed", 0.68, 0.16, 62, at=2.2, color="#f2d06a"),
                dtxt("~ *hundreds of millions* of tonnes", 0.68, 0.56, 54, at=6.0, font="serif_i", max_w=0.5)]),
      transition="cut")
scene("Which is bad news for the table.",
      [plate("cafe_crushed")],
      transition="burn", transition_frames=8, sfx="thud", camera={"shake": [0.0, 0.5]}, min_dur=2.6)
cue("tension", key="E", scale="minor")
scene("And the universe actually does this. When a giant star dies, its core can collapse into a *neutron star*.",
      [plate("space", pan=[0, 0, -0.1]), dtxt("a *neutron star*", 0.5, 0.15, 90, at=4.0, font="serif_i")],
      transition="dip", transition_frames=16, letterbox=0.11, letterbox_in=1.0)
scene("Gravity squeezes so hard that electrons are pushed into protons, turning them into neutrons, packed shoulder to shoulder. Almost no empty space left.",
      [plate("space", blur=4, pan=[0, 0, 0.1]),
       sprite("electron", 0.3, 0.45, 0.05, enter="fade", at=1.6, keys=[{"t": 0, "x": 0.3}, {"t": 1.4, "x": 0.45, "ease": "in"}], until=3.2),
       sprite("nucleus", 0.5, 0.45, 0.08, enter="fade", at=1.2),
       dtxt("electron + proton = neutron", 0.5, 0.15, 66, at=3.2, font="serif_i", max_w=0.8),
       hand("no room left", 0.5, 0.72, 86, at=7.0, color="#f2d06a")],
      letterbox=0.11, transition="cut")
scene("A neutron star packs more mass than our Sun into a ball about *twenty kilometres* across. Roughly the size of a city.",
      [plate("space"), card_paper("ns", 0.3, 0.42, 0.42, 0.6, rot=-2), source("SOURCE: NASA", at=2.2)],
      letterbox=0.11, transition="cut")
scene("A sugar cube of neutron star would weigh about a *billion tonnes*. As much as the whole human race.",
      talk("space", [["serious", 0], ["surprised", 3.2]], x=0.27,
           top=[sprite("sugar_cube", 0.68, 0.24, 0.09, enter="fade", at=0.8), dtxt("one sugar cube weighs", 0.68, 0.4, 52, at=2.2, font="serif_i"),
                {"type": "counter", "from": 0, "to": 1000, "count_dur": 1.4, "at": 2.6, "x": 0.68, "y": 0.52, "size": 72, "font": "cond",
                 "suffix": ",000,000 tonnes", "color": "accent", "enter": "fade", "sfx": "type"},
                source("SOURCE: NASA (VIA SPACE.COM)", at=3.4)]),
      letterbox=0.11, transition="cut")

# =================================================================== 7. So what are you made of?
chapter_card(6, "So what are you made of?", "stadium_marble", "wonder")
CUES[-1].update(key="D", scale="dorian")
scene("One last twist. Even the marble isn't really solid stuff. It's made of protons and neutrons, and they're made of *quarks*.",
      [plate("stadium_marble", pan=[0, 0, -0.08]),
       sprite("nucleus", 0.78, 0.3, 0.14, enter="fade", at=3.0), hand("protons + neutrons", 0.78, 0.5, 60, at=3.2),
       dtxt("*quarks*", 0.5, 0.15, 110, at=5.4, font="serif_i")],
      transition="cut")
scene("And the quarks' own mass is only about one percent of it. The other ninety-nine percent is *energy*: the strong force, holding them together. E equals m c squared, at work inside you.",
      talk("stadium_marble", [["explain", 0], ["point", 4.0], ["surprised", 9.0]], x=0.27,
           top=[card_paper("pie", 0.68, 0.34, 0.44, 0.6, rot=2), hand("E = mc²", 0.68, 0.66, 96, at=8.2, color="#f2d06a"),
                mark("circle", 8.8, box=[0.6, 0.6, 0.76, 0.72], color="#f2d06a", sfx="none")]),
      transition="cut")
scene("So you're not made of tiny hard balls. You're made of *forces*: electric pushes, quantum rules, and trapped energy.",
      staged("cafe_wide",
             behind=[person("cafe_wide", "seller", -1.4, 2.4, [["happy", 0]]),
                     person("cafe_wide", "lena", 3.5, 2.0, [["happy", 0]]),
                     person("cafe_wide", "ravi", 4.9, 2.2, [["cheer", 2.0]]),
                     person("cafe_wide", "omar", -2.6, 3.0, [["wave", 0]])],
             front=[person("cafe_wide", "amina", 1.5, -0.4, [["happy", 0]]),
                    person("cafe_wide", "tomas", -2.6, -1.0, [["cheer", 1.0]], hops=[[1.4, 0.03, 0.45]]),
                    ved("cafe_wide", -0.6, -1.6, [["explain", 0], ["welcome", 3.0]])],
             top=[dtxt("you are made of *forces*", 0.5, 0.13, 80, at=3.0, font="serif_i", max_w=0.8)]),
      transition="cut", leak=[1.0, 3.0, 0.4])
scene("Solid isn't stuff. It's a *push* you can feel.",
      [dict(plate("cafe_mid"), blur=16, opacity=0.5),
       {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "color": "#07090b", "opacity": 0.55, "enter": "none"},
       dtxt("Solid isn't stuff.", 0.5, 0.42, 84, at=0.2, font="serif"),
       dtxt("It's a *push* you can feel.", 0.5, 0.56, 84, at=1.5, font="serif_i")],
      bg={"type": "solid", "colors": ["#0b0d10"]}, transition="dip", transition_frames=12, letterbox=0.11, min_dur=4.6, pad=1.2)
scene("If that blew your mind a little, subscribe. Every week, one big idea, made simple.",
      staged("cafe_mid",
             behind=[person("cafe_mid", "seller", 1.6, 2.6, [["wave", 0]])],
             front=[person("cafe_mid", "amina", 1.4, 0.2, [["wave", 0.4]]),
                    ved("cafe_mid", -0.7, -0.6, [["welcome", 0], ["warm", 2.0]])],
             top=[dtxt("THE EXPLAINER", 0.62, 0.14, 46, at=0.5, font="cond", color="accent"),
                  dtxt("one big idea, every week", 0.62, 0.23, 58, at=1.4, font="serif_i")]),
      transition="cut")

for s in S:
    clean(s["layers"])

job = json.load(open(J + "job.json"))      # the old build's metadata (title, description, sources, thumbnail)
job["chapters"] = CH
job["scenes"] = S
job["music"] = {"cues": CUES}
job["meta"]["overrides"] = "documentary cut (doc toolkit v1): owner asked for a hand-made documentary style for long videos"
job["meta"]["humour"] = {"trend": "dry handwritten sticky notes: 'Personal space? Atoms invented it.', 'touching grass' slang",
                         "beat": "sticky-note inserts", "scene": [i for i, s in enumerate(S) if s.get("dur") in (2.6, 2.8) and not s.get("say")]}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("doc cut: scenes", len(S), "chapters", len(CH), "cues", len(CUES), "words", sum(len(s.get("say", "").split()) for s in S))
