"""Deep Dive 2026-11-21-L (16:9), documentary cut: "Why Doctors Refused to Wash Their Hands".
Semmelweis, Vienna 1846-1849, Pest, the proof (Pasteur, Lister, Koch) and the Semmelweis reflex. Same Ved, same townspeople and
outfits, same 3D world; edited with the documentary toolkit (reference: jobs/2026-11-14-L/build_doc.py).
Run: python jobs/2026-11-21-L/build_doc.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(211)
ID = "2026-11-21-L"
J = f"jobs/{ID}/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_dissect_close.json") else "/tmp/pv21/"
LA = "jobs/2026-11-14-L/assets/"     # 1860s lab (reconstruction) + the town cafe, same plates as last week's Deep Dive
SA = "jobs/2026-11-18-a/assets/"     # chlorine jar + soap cut-outs from the Semmelweis Short
OWN = ("ward_wide", "ward_mid", "ward_bed", "ward2_wide", "wash", "wash_close", "dissect", "dissect_close")
LAST = ("lab_wide", "lab_mid", "lab_close", "cafe_wide", "cafe_mid", "cafe_table")
ST = {n: Stage(SRC + f"plate_{n}.json") for n in OWN}
ST.update({n: Stage(LA + f"plate_{n}.json") for n in LAST})
HAS_FG = {"cafe_wide", "cafe_mid", "lab_wide", "lab_mid"}

OUT = {
    # the town (same people, same outfits as every Short)
    "seller": {"skin": "#c98e62", "build": "round", "hair": ["#1d1712", "short"], "hat": ["cap", "#2f6f8f"],
               "top": ["#e8e2d4", "shirt"], "apron": "#f6efe2", "bottom": ["#3a3e48", "trousers"]},
    "amina": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "necklace": "#6fc3c0",
              "earrings": "#f2b04a", "bag": "#8a5a3c", "hair": ["#140f0c", "long"]},
    "tomas": {"skin": "#e2b48d", "hat": ["straw", "#e6c27a"], "top": ["#6fc3c0", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "omar": {"skin": "#a0694a", "hat": ["fez", "#b03a2e"], "top": ["#f6efe2", "vest"], "bottom": ["#5a4636", "trousers"], "build": "round"},
    "lena": {"skin": "#e6b996", "top": ["#9b59b6", "dress"], "hair": ["#6b4423", "bun"], "earrings": "#f2b04a"},
    "ravi": {"skin": "#b97a55", "top": ["#7c2533", "kurta"], "bottom": ["#efe3c8", "trousers"], "hair": ["#2a2320", "curly"]},
    # Vienna 1846-47 (same outfits as the Semmelweis Short, jobs/2026-11-18-a)
    "semmel": {"skin": "#ecc6a2", "build": "round", "hair": ["#5a3e28", "short"], "top": ["#2a2f3a", "jacket"], "tie": "#7c2533",
               "bottom": ["#2a2f3a", "trousers"], "shoes": "#1a1410"},
    "student": {"skin": "#e2b48d", "build": "slim", "hair": ["#2b1d14", "short"], "top": ["#5a4636", "jacket"], "tie": "#25262b",
                "bottom": ["#3a3e48", "trousers"], "shoes": "#1a1410"},
    "midwife": {"skin": "#c98e62", "hat": ["headscarf", "#f6efe2"], "top": ["#5b86b8", "dress"], "apron": "#f6efe2", "hair": ["#2b1d14", "bun"]},
    "kolle": {"skin": "#f0cdb0", "build": "regular", "hair": ["#9a9a9a", "short"], "top": ["#3a3e48", "jacket"], "tie": "#25262b",
              "bottom": ["#25262b", "trousers"], "shoes": "#1a1410"},
    "mother": {"skin": "#e8bfa0", "hat": ["headscarf", "#7c2533"], "top": ["#efe3c8", "dress"], "hair": ["#5a3e28", "long"]},
    "mother2": {"skin": "#d9a882", "hat": ["headscarf", "#2f6f8f"], "top": ["#c9b7e3", "dress"], "hair": ["#2b1d14", "bun"]},
    "senior": {"skin": "#f0c8a8", "build": "round", "hair": ["#cfcfcf", "short"], "top": ["#25262b", "jacket"], "tie": "#f6efe2",
               "bottom": ["#25262b", "trousers"], "belt": "#1a1a1a"},
    # 1860s-70s labs (faceless reconstructions)
    "pasteur": {"skin": "#ecc4a2", "hair": ["#3a2a1e", "short"], "top": ["#2a2d33", "jacket"], "tie": "#25262b", "bottom": ["#2a2d33", "trousers"]},
    "lister": {"skin": "#f0cdb0", "build": "slim", "hair": ["#6b4423", "short"], "top": ["#34425c", "jacket"], "tie": "#f6efe2",
               "bottom": ["#25262b", "trousers"]},
    "koch": {"skin": "#e8bfa0", "build": "round", "hair": ["#5a4636", "short"], "top": ["#efe3c8", "shirt"], "apron": "#f6efe2",
             "bottom": ["#4a4038", "trousers"]},
}


def _dir(name):
    return LA if name in LAST else A


def plate(name, blur=0, **k):
    return {"type": "image", "path": _dir(name) + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": _dir(name) + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": SA + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


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


def ved(set_, wx, wy, acting="auto", walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0] if isinstance(acting, list) else "idle",
         "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none", "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    L.update(k)
    return L


def close_ved(acting="auto", x=0.27, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0] if isinstance(acting, list) else "idle",
            "x": x, "y": 0.86, "h": 1.2, "enter": "none", "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def staged(set_, behind=(), front=(), top=()):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if set_ in HAS_FG:
        out.append(fg(set_))
    out += sorted(front, key=lambda L: -L["_depth"])
    out += list(top)
    for L in out:
        L.pop("_depth", None)
    return out


def talk(set_, acting="auto", x=0.27, top=(), zoom=(1.0, 1.04)):
    return [plate(set_, blur=9, keys=[{"t": 0, "scale": zoom[0] * 1.15}, {"t": 6, "scale": zoom[1] * 1.15}]),
            close_ved(acting, x=x)] + list(top)


def clean(layers):
    for L in layers:
        L.pop("_depth", None)
    return layers


S, CH, CUES = [], [], []


def chapter(title):
    CH.append({"scene": len(S), "title": title})


def cue(style, **k):
    CUES.append({"scene": len(S), "style": style, **k})


def scene(say, layers, **k):
    s = {"say": say, "layers": layers, **k}
    S.append(s)
    return s


def dtxt(t, x, y, size=70, font="serif", at=0.3, **k):
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


def photo(name, x, y, w, at, rot=0.0, caption=None, tone="sepia", **k):
    return {"type": "paper", "kind": "photo", "path": _dir(name) + f"plate_{name}.png", "tone": tone, "x": x, "y": y, "w": w,
            "rotate": rot, "at": at, "enter": "slam", "enter_dur": 0.35, "sfx": "paper", "tape": ["tl", "tr"],
            **({"caption": caption} if caption else {}), **k}


def doc(title, text, x, y, w, at, rot=0.0, **k):
    return {"type": "paper", "kind": "doc", "title": title, "text": text, "w": w, "x": x, "y": y, "rotate": rot, "at": at,
            "enter": "slam", "sfx": "paper", "tape": ["tl", "tr"], **k}


def sticky(text, x, y, at, rot=-4, w=0.26, **k):
    return {"type": "paper", "kind": "note", "text": text, "paper": "#f6e27f", "font": "hand", "text_size": 0.11,
            "w": w, "x": x, "y": y, "rotate": rot, "at": at, "enter": "slam", "enter_dur": 0.3, "sfx": "paper", "tape": ["tc"], **k}


def mark(shape, at, **k):
    return {"type": "marker", "shape": shape, "at": at, "sfx": k.pop("sfx", "marker"), **k}


def chapter_card(num, title, under, music=None, **mk):
    chapter(title)
    if music:
        cue(music, **mk)
    S.append({"dur": 2.8, "transition": "dip", "transition_frames": 14, "captions": False,
              "layers": [dict(plate(under), blur_keys=[[0, 4], [1.2, 16]], pan=[0, 0, 0.05]),
                         {"type": "chapter", "num": num, "title": title, "at": 0.15}],
              "sfx": "hit", "camera": {"zoom": [1.02, 1.05], "focus": [0.5, 0.5]}})


def board_bg():
    return {"type": "image", "path": "jobs/2026-11-14-L/assets/doc/cork.png", "x": 0.5, "y": 0.5, "w": 1.04, "enter": "none",
            "pan": [0.01, 0, 0.03]}


def gag(under, text, rot=-4):
    """Dry sticky-note insert (the film's comic beats), 2.8 s, no voice."""
    S.append({"dur": 2.8, "captions": False, "transition": "cut",
              "layers": [plate(under, blur=10), sticky(text, 0.5, 0.45, 0.2, rot=rot, w=0.34)],
              "camera": {"zoom": [1.04, 1.08], "focus": [0.5, 0.45]}})


# =================================================================== cold open (letterboxed, no titles yet)
chapter("Vienna, 1846")
cue("wonder", key="D", scale="dorian", bpm=64)
scene("Vienna, eighteen forty-six. A young mother arrives at one of the biggest hospitals in Europe... and begs, on her knees, not to be taken through one particular door.",
      staged("ward_wide",
             behind=[person("ward_wide", "midwife", 1.0, 9.0, [["idle", 0]])],
             front=[person("ward_wide", "mother", -0.3, 1.4, [["idle", 0], ["sad", 5.2]], walk=[(0, -0.3, -1.6), (3.4, -0.3, 1.4)]),
                    person("ward_wide", "student", 0.7, 3.2, [["idle", 0], ["point", 5.6]])],
             top=[dict(plate("ward_wide"), blur_keys=[[0, 10], [1.6, 0]], until=1.8, exit="fade", exit_dur=0.6)]),
      letterbox=0.11, letterbox_in=1.2, lead=0.9, camera={"zoom": [1.0, 1.07], "focus": [0.5, 0.52]}, transition="cut")
scene("Because everyone in the city knew: behind that door, mothers died. And the reason was hiding in plain sight... on the doctors' own hands.",
      talk("ward_mid", [["serious", 0], ["point", 4.4]], x=0.27,
           top=[dtxt("behind that door,", 0.7, 0.3, 62, at=1.4, font="serif_i"),
                dtxt("mothers *died*.", 0.7, 0.42, 74, at=2.4, font="serif")]),
      letterbox=0.11, transition="cut")
scene("This is the story of the doctor who worked it out, why almost nobody believed him, and why the hardest thing to wash off... isn't germs.",
      staged("ward_wide",
             front=[ved("ward_wide", 0.0, 0.2, [["welcome", 0], ["explain", 2.4], ["shrug", 6.0]], walk=[(0, 0.0, 4.0), (2.0, 0.0, 0.2)])]),
      letterbox=0.11, transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.5]})
S.append({"dur": 3.6, "captions": False, "transition": "dip", "transition_frames": 16, "sfx": "hit", "sfx_at": 0.3,
          "bg": {"type": "solid", "colors": ["#0b0d10"]},
          "layers": [dict(plate("wash"), blur_keys=[[0, 18]], opacity=0.55),
                     {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 0.6, "color": "#07090b", "opacity": 0.55, "enter": "none"},
                     dtxt("WASH YOUR HANDS", 0.5, 0.45, 120, at=0.35, font="serif", enter_dur=1.2, max_w=0.9),
                     dtxt("THE IDEA THAT MEDICINE REFUSED", 0.5, 0.57, 30, at=1.2, font="cond", color="accent", max_w=0.8)],
          "camera": {"zoom": [1.0, 1.03], "focus": [0.5, 0.5]}, "letterbox": 0.11})

# =================================================================== 1. Two doors
chapter_card(1, "Two doors", "ward_wide", "doc", key="D")
scene("The Vienna General Hospital had two maternity clinics, side by side. The First Clinic trained doctors and medical students. The Second trained midwives.",
      staged("ward_wide",
             behind=[person("ward_wide", "student", 0.6, 7.0, [["idle", 0], ["explain", 3.0]]),
                     person("ward_wide", "semmel", -0.4, 7.4, [["explain", 0]])],
             front=[person("ward_wide", "student", 0.9, 1.6, [["idle", 0]], walk=[(0, 2.6, 0.4), (2.6, 0.9, 1.6)])],
             top=[lower("Vienna General Hospital", "1846. The First Clinic: doctors and medical students", at=1.0, until=6.0),
                  lower("The Second Clinic", "midwives in training", at=6.6)]),
      look="archival", sfx="projector", transition="cut")
scene("In eighteen forty-six, the First Clinic lost *eleven point four percent* of its mothers to childbed fever. The Second Clinic? About *two point eight*.",
      [board_bg(),
       doc("FIRST CLINIC", "Doctors and medical students.\n1846: 4,010 births, 459 mothers died.", 0.3, 0.42, 0.32, 0.4, rot=-3),
       doc("SECOND CLINIC", "Midwives.\n1846: 3,754 births, 105 mothers died.", 0.72, 0.46, 0.32, 3.4, rot=3),
       {"type": "bignum", "text": "11.4%", "x": 0.3, "y": 0.72, "size": 120, "tone": "gold", "at": 2.6},
       {"type": "bignum", "text": "2.8%", "x": 0.72, "y": 0.74, "size": 120, "tone": "cream", "at": 5.4},
       source("SOURCE: SEMMELWEIS'S CLINIC TABLES, VIA WIKIPEDIA", at=1.0)],
      transition="paper", transition_frames=14, camera={"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 6.0, "zoom": 1.07, "focus": [0.4, 0.55]}]})
scene("Same city. Same building. Mothers from the same streets. And about *four times* the deaths, just for going through the wrong door.",
      staged("ward2_wide",
             behind=[person("ward2_wide", "midwife", -0.5, 8.0, [["idle", 0], ["give", 2.0]])],
             front=[person("ward2_wide", "midwife", 0.4, 2.6, [["explain", 0]], walk=[(0, 0.4, 5.0), (2.6, 0.4, 2.6)]),
                    person("ward2_wide", "mother2", -0.6, 1.2, [["idle", 0], ["happy", 3.0]])],
             top=[dtxt("about *4×* the deaths", 0.5, 0.14, 76, at=4.2, font="serif_i", max_w=0.8)]),
      transition="cut", camera={"zoom": [1.06, 1.0], "focus": [0.5, 0.5]})
scene("So mothers begged to be sent to the Second Clinic. Some would rather give birth in the street on the way in. And strangely... those street births rarely caught the fever.",
      staged("ward_wide",
             behind=[person("ward_wide", "midwife", 1.0, 9.0, [["idle", 0]])],
             front=[person("ward_wide", "mother", -0.4, 1.0, [["sad", 0], ["give", 3.0]]),
                    person("ward_wide", "student", 0.6, 1.6, [["point", 0], ["shrug", 3.4]])],
             top=[hand("street births: fever was *rare*", 0.5, 0.14, 80, at=6.6, color="#f2d06a", max_w=0.8)]),
      look="archival", transition="cut")
scene("A street was safer than a hospital. That should have set off every alarm in medicine.",
      talk("ward2_wide", [["serious", 0], ["shrug", 2.6]], x=0.73,
           top=[dtxt("a street was *safer*", 0.33, 0.36, 76, at=1.0, font="serif_i")]),
      transition="cut")
gag("ward_wide", "Hospital review: 1 star.\nThe street was cleaner.", rot=-5)

# =================================================================== 2. The detective
chapter_card(2, "The detective", "ward_mid", "tension", key="A", scale="minor")
scene("One young doctor couldn't let it go. Ignaz Semmelweis, a Hungarian assistant in the First Clinic. He treated the deaths like a crime... and went through the suspects one by one.",
      staged("ward_mid",
             front=[person("ward_mid", "semmel", -1.0, 4.8, [["idle", 0], ["explain", 3.6], ["point", 7.0]], walk=[(0, 0.4, 7.4), (3.0, -1.0, 4.8)])],
             top=[lower("Ignaz Semmelweis", "assistant, First Clinic. Hungarian, born 1818", at=2.6, until=8.2)]),
      look="archival", transition="cut")
scene("Overcrowding? No. The Second Clinic was *more* crowded.",
      [board_bg(),
       doc("SUSPECT 1: OVERCROWDING", "The Second Clinic was MORE crowded.", 0.3, 0.45, 0.32, 0.3, rot=-3),
       mark("cross", 2.2, box=[0.17, 0.33, 0.43, 0.57], color="#c0392b"),
       photo("ward2_wide", 0.72, 0.45, 0.32, 0.9, rot=3, caption="Second Clinic: fuller")],
      transition="paper", transition_frames=12, camera={"zoom": [1.0, 1.05], "focus": [0.35, 0.47]})
scene("The weather, or bad city air? Both clinics sat in the same hospital, breathing the same air.",
      [board_bg(),
       doc("SUSPECT 1: OVERCROWDING", "The Second Clinic was MORE crowded.", 0.2, 0.3, 0.26, 0.0, rot=-3, enter="none", sfx="none"),
       mark("cross", 0.0, box=[0.1, 0.2, 0.3, 0.4], color="#c0392b", sfx="none"),
       doc("SUSPECT 2: CLIMATE & AIR", "Same hospital, same city air.", 0.5, 0.52, 0.3, 0.3, rot=2),
       mark("cross", 3.4, box=[0.38, 0.41, 0.62, 0.63], color="#c0392b")],
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.47]})
scene("The way mothers lay to give birth? He changed it in the First Clinic. The deaths didn't change.",
      [board_bg(),
       doc("SUSPECT 1: OVERCROWDING", "The Second Clinic was MORE crowded.", 0.2, 0.3, 0.26, 0.0, rot=-3, enter="none", sfx="none"),
       mark("cross", 0.0, box=[0.1, 0.2, 0.3, 0.4], color="#c0392b", sfx="none"),
       doc("SUSPECT 2: CLIMATE & AIR", "Same hospital, same city air.", 0.5, 0.52, 0.3, 0.0, rot=2, enter="none", sfx="none"),
       mark("cross", 0.0, box=[0.38, 0.41, 0.62, 0.63], color="#c0392b", sfx="none"),
       doc("SUSPECT 3: BIRTH POSITION", "Changed it in the First Clinic. No effect.", 0.8, 0.34, 0.28, 0.3, rot=4),
       mark("cross", 3.6, box=[0.68, 0.23, 0.92, 0.45], color="#c0392b")],
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.7, 0.47]})
scene("He even wondered whether the priest, ringing a bell on his way to the dying, was frightening mothers to death. Every suspect had an alibi.",
      talk("ward_mid", [["think", 0], ["shrug", 4.8], ["side_eye", 7.0]], x=0.27,
           top=[dtxt("every suspect", 0.7, 0.3, 66, at=5.6, font="serif_i"),
                dtxt("had an *alibi*.", 0.7, 0.42, 76, at=6.4)]),
      transition="cut")

# =================================================================== 3. A cut finger
chapter_card(3, "A cut finger", "dissect", "tension", key="E", scale="minor")
scene("Then, in eighteen forty-seven, a tragedy cracked the case. His friend, Professor Jakob Kolletschka, was poked by a student's scalpel during an autopsy.",
      staged("dissect",
             front=[person("dissect", "kolle", -0.9, 0.8, [["explain", 0], ["surprised", 6.6]]),
                    person("dissect", "student", 0.9, 0.8, [["hold", 0], ["surprised", 6.8]])],
             top=[lower("Jakob Kolletschka", "professor of forensic medicine, Vienna", at=3.0, until=7.6)]),
      look="archival", transition="cut", camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.48]})
scene("Soon after, Kolletschka was dead. And the illness that killed him looked just like the fever that was killing the mothers.",
      [plate("dissect_close", pan=[0, 0, 0.06]),
       dtxt("the *same* fever", 0.5, 0.16, 84, at=4.6, font="serif_i")],
      transition="cut")
cue("none")
scene("And Semmelweis saw it.",
      talk("dissect", [["serious", 0]], x=0.5),
      transition="cut", lead=1.0, pad=0.8, camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.35]})
cue("tension", key="E", scale="minor", gain=1.2)
scene("Doctors and students started their mornings in the autopsy room. Then they walked straight to the maternity ward, and examined mothers with the same hands. Midwives never did autopsies.",
      [board_bg(),
       photo("dissect", 0.2, 0.36, 0.28, 0.2, rot=-4, caption="the autopsy room, morning"),
       doc("THE ROUTE", "Autopsy -> no wash -> delivery ward.\nMidwives: no autopsies.", 0.5, 0.66, 0.3, 3.0, rot=2),
       photo("ward_wide", 0.8, 0.38, 0.28, 5.0, rot=4, caption="First Clinic, afternoon"),
       {"type": "string", "points": [[0.2, 0.46], [0.5, 0.58], [0.8, 0.48]], "at": 7.0, "sfx": "tape"},
       {"type": "stamp", "text": "THE HANDS", "x": 0.5, "y": 0.24, "tone": "red", "angle": -8, "size": 110, "at": 9.4, "sfx": "thud", "sting": "turn"}],
      transition="paper", transition_frames=14,
      camera={"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 9.2, "zoom": 1.04, "focus": [0.5, 0.45]},
                       {"t": 9.6, "zoom": 1.12, "focus": [0.5, 0.32]}]})
scene("He called it *cadaverous particles*. Something invisible, carried from the dead to the living, on doctors' hands.",
      [plate("ward_bed", pan=[0, 0, 0.06]),
       dtxt("“cadaverous particles”", 0.5, 0.16, 80, at=1.0, font="serif_i", max_w=0.8),
       source("SEMMELWEIS'S TERM, 1847", at=1.6)],
      transition="cut")

# =================================================================== 4. The chlorine bowl
chapter_card(4, "The chlorine bowl", "wash", "wonder", key="G", scale="dorian")
scene("So in mid-May, eighteen forty-seven, he put a bowl by the door. Chlorinated lime solution. Wash your hands in it before you touch a patient. Every time.",
      staged("wash",
             top=[lower("Mid-May 1847", "the First Clinic's new rule", at=1.0, until=5.0),
                  hand("wash. every. time.", 0.3, 0.16, 84, at=7.4, color="#f2d06a")]),
      transition="cut", camera={"zoom": [1.0, 1.12], "focus": [0.5, 0.55]})
scene("Why chlorine? Because it was the best thing he'd found for getting rid of the smell of the autopsy room. If the smell was gone, he reasoned, so was whatever caused it.",
      [plate("wash_close", pan=[0, 0, 0.05]),
       sprite("jar", 0.8, 0.52, 0.12, enter="fade", at=0.8, pan=[0, -0.01, 0.04]),
       hand("chlorine kills the smell...", 0.36, 0.16, 70, at=3.4, color="#f6efe2"),
       hand("...and the cause?", 0.36, 0.28, 70, at=6.8, color="#f2d06a")],
      transition="cut")
scene("In April, *eighteen point three percent* of mothers in the First Clinic had died. Then the bowl arrived. June: *two point two*. July: *one point two*.",
      [board_bg(),
       {"type": "bignum", "text": "18.3%", "x": 0.22, "y": 0.45, "size": 110, "tone": "gold", "at": 0.6},
       hand("April 1847", 0.22, 0.28, 64, at=0.8, color="#f6efe2"),
       {"type": "bignum", "text": "2.2%", "x": 0.52, "y": 0.45, "size": 110, "tone": "cream", "at": 5.4},
       hand("June", 0.52, 0.28, 64, at=5.4, color="#f6efe2"),
       {"type": "bignum", "text": "1.2%", "x": 0.8, "y": 0.45, "size": 110, "tone": "cream", "at": 7.4},
       hand("July", 0.8, 0.28, 64, at=7.4, color="#f6efe2"),
       mark("arrow", 4.6, **{"from": [0.3, 0.62], "to": [0.45, 0.62]}, color="#2f8f4a"),
       mark("arrow", 7.0, **{"from": [0.6, 0.62], "to": [0.75, 0.62]}, color="#2f8f4a", sfx="none"),
       source("SOURCE: SEMMELWEIS (1861), VIA BRITANNICA & WIKIPEDIA", at=1.4)],
      transition="paper", transition_frames=14, camera={"keys": [{"t": 0, "zoom": 1.0, "focus": [0.3, 0.45]}, {"t": 8.5, "zoom": 1.06, "focus": [0.7, 0.45]}]})
scene("In the year that followed, there were even months with *no* deaths from the fever at all.",
      staged("ward_wide",
             behind=[person("ward_wide", "midwife", 1.0, 9.0, [["happy", 0]])],
             front=[person("ward_wide", "semmel", -0.3, 3.2, [["happy", 0], ["cheer", 1.2]], hops=[[1.3, 0.04, 0.4]]),
                    person("ward_wide", "mother", 0.6, 1.2, [["happy", 0.6]]),
                    person("ward_wide", "student", -0.9, 1.8, [["cheer", 1.6]])],
             top=[hand("zero.", 0.5, 0.14, 120, at=2.8, color="#f2d06a")]),
      look="archival", transition="cut", leak=[0.6, 2.4, 0.4])
scene("About ten times fewer deaths. From a bowl of water. You'd think they'd build him a statue.",
      talk("wash", [["explain", 0], ["warm", 2.6], ["smirk", 4.6]], x=0.73,
           top=[sprite("jar", 0.3, 0.42, 0.1, enter="fade", at=1.6),
                dtxt("about *10×* fewer deaths", 0.33, 0.7, 60, at=0.6, font="serif_i", max_w=0.5)]),
      transition="cut")
gag("wash_close", "Statue status: pending.", rot=4)

# =================================================================== 5. Why they said no
chapter_card(5, "Why they said no", "ward_mid", "tension", key="A", scale="minor")
scene("Instead, many senior doctors pushed back. Some were insulted. A gentleman's hands, they felt, were clean.",
      [dict(plate("ward_mid"), blur=18, opacity=0.45),
       {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 0.6, "color": "#07090b", "opacity": 0.6, "enter": "none"},
       dtxt("“Doctors are gentlemen, and gentlemen's hands are clean.”", 0.5, 0.44, 58, at=0.6, font="serif_i", max_w=0.72, enter_dur=1.6),
       dtxt("ATTRIBUTED TO CHARLES MEIGS, PHILADELPHIA OBSTETRICIAN", 0.5, 0.62, 26, at=2.4, font="cond", color="accent", max_w=0.8)],
      bg={"type": "solid", "colors": ["#0b0d10"]}, transition="dip", transition_frames=12, camera={"zoom": [1.0, 1.04], "focus": [0.5, 0.45]}, pad=0.6)
scene("But to be fair, they had reasons. Medicine then blamed disease on bad air and imbalances in the body. Germs weren't part of the picture yet. Semmelweis had a result... but no mechanism to explain it.",
      [board_bg(),
       doc("THE DOCTORS' CASE", "Disease = bad air (miasma) and imbalance of the body's humours. No known germs. A result without a cause.", 0.29, 0.44, 0.34, 0.6, rot=-3),
       doc("SEMMELWEIS'S CASE", "18.3% -> 1.2% after hand washing. Clear numbers. But WHY? No mechanism yet.", 0.71, 0.48, 0.34, 6.4, rot=3),
       mark("underline", 11.0, box=[0.6, 0.6, 0.84, 0.6], color="#c0392b")],
      transition="paper", transition_frames=14, camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.5]})
scene("And he made it harder. His full book only came out in eighteen sixty-one. And he wrote furious open letters, calling his critics *murderers*.",
      staged("ward_mid",
             front=[person("ward_mid", "senior", -0.9, 4.6, [["idle", 0], ["shrug", 4.0]]),
                    person("ward_mid", "semmel", 0.3, 3.0, [["point", 0], ["explain", 3.0], ["point", 6.0]])],
             top=[{"type": "paper", "kind": "clip", "masthead": "Open letter, 1861", "title": "To all professors of obstetrics",
                   "w": 0.24, "x": 0.2, "y": 0.34, "rotate": -4, "at": 4.4, "enter": "slam", "sfx": "paper", "stamp": "1861"}]),
      look="archival", transition="cut")
scene("In eighteen forty-nine, his post in Vienna wasn't renewed. He went home to Hungary.",
      staged("ward_mid",
             front=[person("ward_mid", "semmel", -1.5, 5.6, [["sad", 0.0]], walk=[(0, -1.0, 3.2), (4.0, -1.6, 9.0)])],
             top=[lower("Vienna, 1849", "his assistant's post is not renewed", at=0.8)]),
      look="archival", transition="cut", min_dur=4.2)
scene("And there, he did it again. At St. Rochus Hospital in Pest, from eighteen fifty-one to fifty-five, just eight mothers died out of nine hundred and thirty-three births. Under *one percent*.",
      [plate("ward2_wide", pan=[0, 0, 0.06]),
       lower("Pest, Hungary", "St. Rochus Hospital, 1851-1855", at=0.8, until=5.0),
       {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.27, "w": 0.5, "h": 0.3, "color": "#07090b", "opacity": 0.55, "enter": "fade", "at": 6.8},
       {"type": "bignum", "text": "0.85%", "x": 0.5, "y": 0.23, "size": 120, "tone": "cream", "at": 7.0},
       dtxt("8 deaths in 933 births", 0.5, 0.36, 46, at=7.4, font="serif_i"),
       source("SOURCE: BRITANNICA; MED. J. AUSTRALIA (2018)", at=7.6)],
      look="archival", transition="cut")
cue("none")
scene("But the fight wore him down. In eighteen sixty-five, his health and behaviour failing, he was taken to an asylum. Two weeks later he died, aged forty-seven... from an infected wound.",
      [dict(plate("ward_bed"), blur=6, opacity=0.6, pan=[0, 0, 0.04]),
       {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "color": "#07090b", "opacity": 0.45, "enter": "none"},
       dtxt("Ignaz Semmelweis", 0.5, 0.42, 72, at=6.8, font="serif"),
       dtxt("1818 - 1865", 0.5, 0.53, 44, at=7.6, font="serif_i")],
      bg={"type": "solid", "colors": ["#0b0d10"]}, transition="dip", transition_frames=16, letterbox=0.11, letterbox_in=1.0, pad=1.0)
scene("The kind of infection he'd spent his life fighting.",
      talk("ward_bed", [["serious", 0]], x=0.5), transition="cut", letterbox=0.11, pad=0.8)

# =================================================================== 6. The proof arrives
chapter_card(6, "The proof arrives", "lab_wide", "doc", key="D")
scene("Science caught up only around the time he died. In the eighteen-sixties, Louis Pasteur showed that tiny living microbes cause fermentation and decay.",
      staged("lab_wide",
             front=[person("lab_wide", "pasteur", -2.5, 0.8, [["explain", 0], ["point", 4.0]])],
             top=[lower("Louis Pasteur", "chemist, Paris. 1860s", at=1.4, until=7.0)]),
      look="archival", sfx="projector", transition="cut", camera={"zoom": [1.7, 1.75], "focus": [0.2, 0.6]})
scene("In eighteen sixty-seven, the surgeon Joseph Lister published his method of killing germs in wounds with carbolic acid.",
      staged("lab_mid",
             behind=[person("lab_mid", "lister", -0.6, 1.2, [["hold", 0], ["explain", 3.0]])],
             top=[lower("Joseph Lister", "surgeon, Glasgow. The Lancet, 1867", at=1.0, until=6.4)]),
      look="archival", transition="cut", camera={"zoom": [1.6, 1.65], "focus": [0.3, 0.62]})
scene("And Robert Koch proved that one specific germ causes one specific disease, starting with anthrax in eighteen seventy-six.",
      [board_bg(),
       doc("ROBERT KOCH, 1876", "Anthrax: one specific germ causes one specific disease.", 0.36, 0.42, 0.34, 0.4, rot=-2),
       doc("ROBERT KOCH, 1882", "Tuberculosis: he finds the bacterium behind it.", 0.7, 0.5, 0.3, 2.4, rot=3),
       lower("Robert Koch", "physician, Germany. Anthrax, 1876", at=0.8, until=6.0)],
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.5]})
scene("Germ theory finally gave Semmelweis the mechanism he never had. He was right. He just couldn't show why.",
      [{"type": "image", "path": "jobs/2026-11-14-L/assets/doc/cork.png", "x": 0.5, "y": 0.5, "w": 1.04, "enter": "none", "opacity": 0.45},
       {"type": "timeline", "x0": 0.1, "x1": 0.9, "y": 0.78, "draw_dur": 1.6, "at": 0.2, "active": 5,
        "events": [{"pos": 0.0, "year": "1846", "label": "two doors"}, {"pos": 0.17, "year": "1847", "label": "the bowl"},
                   {"pos": 0.4, "year": "1861", "label": "his book"}, {"pos": 0.6, "year": "1865", "label": "he dies"},
                   {"pos": 0.8, "year": "1867", "label": "Lister"}, {"pos": 1.0, "year": "1876", "label": "Koch"}]},
       dtxt("he was *right*.", 0.5, 0.34, 96, at=4.2, font="serif_i"),
       hand("he just couldn't show why", 0.5, 0.5, 70, at=5.4, color="#f2d06a")],
      bg={"type": "solid", "colors": ["#120e0b"]}, transition="paper", transition_frames=14, camera={"zoom": [1.0, 1.04], "focus": [0.5, 0.5]})

# =================================================================== 7. The Semmelweis reflex
chapter_card(7, "The Semmelweis reflex", "cafe_wide", "wonder", key="D", scale="dorian")
scene("Today, there's a name for what happened to him. The *Semmelweis reflex*: the urge to reject new evidence, because it clashes with what everyone already believes.",
      staged("cafe_wide",
             behind=[person("cafe_wide", "seller", -1.4, 2.4, [["idle", 0], ["shrug", 4.0]]),
                     person("cafe_wide", "lena", 3.5, 2.0, [["explain", 0]]),
                     person("cafe_wide", "ravi", 4.9, 2.2, [["shrug", 3.0]])],
             front=[person("cafe_wide", "amina", 1.5, -0.4, [["idle", 0], ["point", 5.0]]),
                    ved("cafe_wide", -0.6, -1.6, [["explain", 0], ["point", 3.0], ["shrug", 7.0]], walk=[(0, 2.6, -2.2), (1.4, -0.6, -1.6)])],
             top=[dtxt("the *Semmelweis reflex*", 0.5, 0.13, 80, at=2.2, font="serif_i", max_w=0.8)]),
      transition="cut", camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.52]})
scene("And his lesson still isn't finished. The World Health Organization says that out of every hundred patients in acute-care hospitals, *seven* in richer countries and *fifteen* in poorer ones catch an infection there.",
      [board_bg(),
       doc("WHO GLOBAL REPORT, 2022", "Per 100 patients in acute-care hospitals, at least one health-care-associated infection:", 0.5, 0.3, 0.44, 0.4, rot=-1.5),
       {"type": "bignum", "text": "7", "x": 0.3, "y": 0.64, "size": 140, "tone": "cream", "at": 6.4},
       hand("richer countries", 0.3, 0.8, 60, at=6.6, color="#f6efe2"),
       {"type": "bignum", "text": "15", "x": 0.7, "y": 0.64, "size": 140, "tone": "gold", "at": 8.6},
       hand("poorer countries", 0.7, 0.8, 60, at=8.8, color="#f6efe2"),
       source("SOURCE: WHO, 6 MAY 2022", at=1.0)],
      transition="paper", transition_frames=14, camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.5]})
scene("Where good hand hygiene and other simple practices are followed, the WHO says about *seventy percent* of those infections can be prevented.",
      talk("cafe_mid", [["explain", 0], ["point", 3.4]], x=0.27,
           top=[sprite("soap", 0.68, 0.3, 0.12, enter="fade", at=1.0),
                {"type": "bignum", "text": "70%", "x": 0.68, "y": 0.54, "size": 130, "tone": "gold", "at": 4.6},
                dtxt("preventable", 0.68, 0.7, 60, at=5.0, font="serif_i"),
                source("SOURCE: WHO, 2022", at=5.0)]),
      transition="cut")
scene("So the next time a fact feels inconvenient, check the evidence... before the reflex.",
      staged("cafe_mid",
             front=[ved("cafe_mid", -0.7, -0.6, [["serious", 0], ["point", 2.4]])],
             top=[hand("evidence first. reflex second.", 0.62, 0.16, 74, at=2.6, color="#f2d06a", max_w=0.6)]),
      transition="cut")
scene("Because the hardest thing to wash off... is *we've always done it this way*.",
      [dict(plate("wash"), blur=16, opacity=0.5),
       {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "color": "#07090b", "opacity": 0.55, "enter": "none"},
       dtxt("The hardest thing to wash off", 0.5, 0.42, 76, at=0.2, font="serif", max_w=0.85),
       dtxt("is *“we've always done it this way.”*", 0.5, 0.56, 76, at=2.0, font="serif_i", max_w=0.85)],
      bg={"type": "solid", "colors": ["#0b0d10"]}, transition="dip", transition_frames=12, letterbox=0.11, min_dur=5.0, pad=1.2)
scene("If this changed how you see a bar of soap, subscribe. Every week, one big idea, made simple.",
      staged("cafe_mid",
             behind=[],
             front=[ved("cafe_mid", -0.7, -0.6, [["welcome", 0], ["warm", 2.0]])],
             top=[dtxt("THE EXPLAINER", 0.62, 0.14, 46, at=0.5, font="cond", color="accent"),
                  dtxt("one big idea, every week", 0.62, 0.23, 58, at=1.4, font="serif_i")]),
      transition="cut")

for s in S:
    clean(s["layers"])

SOURCES = [
    "https://en.wikipedia.org/wiki/Ignaz_Semmelweis",
    "https://www.britannica.com/biography/Ignaz-Semmelweis",
    "https://www.mja.com.au/journal/2018/209/11/ignaz-philipp-semmelweis-1818-1865-herald-hygienic-medicine",
    "https://en.wikipedia.org/wiki/Semmelweis_reflex",
    "https://www.who.int/news/item/06-05-2022-who-launches-first-ever-global-report-on-infection-prevention-and-control",
    "https://www.britannica.com/science/history-of-medicine/Verification-of-the-germ-theory",
    "https://daily.jstor.org/joseph-lister-antiseptic-revolution/",
]
job = {
    "id": ID, "kind": "long",
    "title": "Why Doctors Refused to Wash Their Hands",
    "description": ("In 1846 Vienna, mothers begged not to be taken through one hospital door. Professor Ved follows Ignaz Semmelweis "
                    "like a detective: two maternity clinics with very different death rates, the suspects he ruled out, the "
                    "autopsy accident that cracked the case, the chlorine bowl that cut deaths about tenfold, why medicine still "
                    "said no (and the fair reasons it had), how germ theory proved him right, and the 'Semmelweis reflex' that "
                    "still trips us up today.\n\nSources: Semmelweis's clinic figures (via Wikipedia and Britannica); Carson & "
                    "Toodayan, 'Ignaz Philipp Semmelweis: herald of hygienic medicine', Medical Journal of Australia (2018); "
                    "Britannica, 'Verification of the germ theory'; WHO, first global report on infection prevention and "
                    "control (6 May 2022). Reconstructions are illustrations, not archival footage."),
    "tags": ["semmelweis", "hand washing", "history of medicine", "germ theory", "childbed fever", "semmelweis reflex",
             "joseph lister", "louis pasteur", "science history", "explained", "documentary"],
    "chapters": CH,
    "thumbnail": {
        "title": "DEADLY *HANDS?*", "title_y": 0.15, "title_size": 175, "glow": "#f2b04a", "glow_x": 0.45, "glow_y": 0.58,
        "blur": 16, "glow_strength": 1.6, "bg_saturation": 1.7, "bg_brightness": 0.9, "tint": ["#1f6f6a", "#d9534f"], "tint_amount": 0.45,
        "bg": clean([plate("ward_wide"),
                     person("ward_wide", "student", 1.0, 3.0, [["surprised", 0]]),
                     person("ward_wide", "mother", -0.9, 1.6, [["sad", 0]]),
                     person("ward_wide", "semmel", 0.3, 5.0, [["point", 0]])]),
        "fg": [sprite("jar", 0.17, 0.66, 0.13, rot=-8),
               {"type": "character", "id": "ved", "pose": "surprised", "x": 0.45, "y": 1.2, "h": 1.7, "enter": "none",
                "acting": "none", "ground": False, "allow_outside_safe": True, "talk": False},
               sprite("soap", 0.8, 0.66, 0.16, rot=10)],
    },
    "privacy": "private",
    "speaker": "ved",
    "assets_script": J + "assets.py",
    "scenes": S,
    "music": {"cues": CUES},
    "meta": {
        "format": "deep-dive", "topic": "Ignaz Semmelweis and hand washing in depth: two clinics (1846: 11.4% vs 2.8%), suspects ruled out, Kolletschka's autopsy death, chlorine hand wash (18.3% -> 1.2%), rejection and the fair reasons, Pest (0.85%), death 1865, Pasteur/Lister/Koch, the Semmelweis reflex, WHO 2022 infection figures",
        "hook": "story", "idea_source": "this week's wild-story Short (2026-11-18-a Semmelweis) taken much deeper; viral-shaped + unique (a detective story with a twist)",
        "characters": ["ved", "extra"], "sources": SOURCES,
        "overrides": "documentary cut (doc toolkit), treatment in TREATMENT.md; style donor: visual investigation (grammar only)",
        "humour": {"trend": "dry handwritten sticky notes: 'Hospital review: 1 star. The street was cleaner.', 'Statue status: pending.'",
                   "beat": "sticky-note inserts", "scene": [i for i, s in enumerate(S) if s.get("dur") == 2.8 and not s.get("say") and len(s["layers"]) == 2]},
        "claims": [
            {"claim": "1846: First Clinic 459 of 4,010 mothers died (11.4%), Second Clinic 105 of 3,754 (2.8%)", "tag": "PROVEN", "source": SOURCES[0]},
            {"claim": "women begged not to enter the First Clinic; street births rarely caught the fever", "tag": "PROVEN", "source": SOURCES[0]},
            {"claim": "he ruled out overcrowding, climate, birth position; considered the priest's bell", "tag": "PROVEN", "source": SOURCES[0]},
            {"claim": "Kolletschka was poked by a student's scalpel at an autopsy (1847) and died of an illness like childbed fever", "tag": "PROVEN", "source": SOURCES[2]},
            {"claim": "chlorinated lime hand washing from mid-May 1847; April 18.3%, June 2.2%, July 1.2%; zero-death months in 1848", "tag": "PROVEN", "source": SOURCES[1]},
            {"claim": "objections: miasma/humours, no mechanism, offended gentlemen; Meigs quote attributed", "tag": "PROVEN", "source": SOURCES[3]},
            {"claim": "book 1861; open letters calling critics murderers; post not renewed 1849", "tag": "PROVEN", "source": SOURCES[0]},
            {"claim": "St. Rochus, Pest 1851-55: 8 deaths in 933 births (0.85%)", "tag": "PROVEN", "source": SOURCES[1]},
            {"claim": "1865 asylum, died two weeks later aged 47 of an infected wound", "tag": "PROVEN", "source": SOURCES[2]},
            {"claim": "Pasteur 1860s microbes; Lister carbolic acid 1867; Koch anthrax 1876", "tag": "PROVEN", "source": SOURCES[5]},
            {"claim": "WHO 2022: per 100 acute-care patients, 7 (high-income) and 15 (LMIC) get an HAI; 70% preventable with good hand hygiene and IPC", "tag": "PROVEN", "source": SOURCES[4]},
        ],
    },
}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("doc: scenes", len(S), "chapters", len(CH), "cues", len(CUES), "words", sum(len(s.get("say", "").split()) for s in S))
