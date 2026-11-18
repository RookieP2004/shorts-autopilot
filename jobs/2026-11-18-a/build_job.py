"""2026-11-18-a: "He told doctors to wash their hands" (wild-story: Ignaz Semmelweis, Vienna 1847).
2D Ved + Dr Semmelweis, a midwife and a student doctor (townspeople) staged in depth in a Blender 1840s maternity ward
(wide down the aisle, mid by the beds), a dissection hall in the night mood (stone table under a cloth, oil lamp, one hard
spot), and the washstand close-up (porcelain basin of chlorine water, jug, soap, a brown jar marked Cl).
2D on top: the 18% -> 2% hud that ticks, DOCTORS vs MIDWIVES option cards, a cream route card (dissection room -> delivery
room, no wash), a 3-step tracker (autopsy, hands, mothers), a REJECTED stamp, honesty tags, the comic beat.
Facts (ScienceAlert; PMC review 2024): two maternity clinics at Vienna General Hospital; in the doctors' clinic about
1 in 10 mothers died of childbed fever, in the midwives' clinic far fewer; doctors and students came from autopsies; in 1847 his
colleague Jakob Kolletschka cut himself during a post-mortem and died of a similar illness; Semmelweis ordered hand washing in
chlorine solution; deaths fell from ~18% (April 1847) to under 2% (by July); senior doctors resisted (it blamed doctors; they
believed in 'bad air'); his post was not renewed and he left Vienna in 1849; Pasteur's germ theory and Lister's antisepsis
(1867) later proved him right.
Run after the assets exist: python jobs/2026-11-18-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-18-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("ward_wide", "ward_mid", "dissect", "wash")}

OUT = {   # recurring people: same outfit in every shot
    "semmel": {"skin": "#ecc6a2", "build": "round", "hair": ["#5a3e28", "short"], "top": ["#2a2f3a", "jacket"], "tie": "#7c2533",
               "bottom": ["#2a2f3a", "trousers"], "shoes": "#1a1410"},
    "student": {"skin": "#e2b48d", "build": "slim", "hair": ["#2b1d14", "short"], "top": ["#5a4636", "jacket"], "tie": "#25262b",
                "bottom": ["#3a3e48", "trousers"], "shoes": "#1a1410"},
    "midwife": {"skin": "#c98e62", "hat": ["headscarf", "#f6efe2"], "top": ["#5b86b8", "dress"], "apron": "#f6efe2", "hair": ["#2b1d14", "bun"]},
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


# the route card: dissection room -> (no wash) -> delivery room, with a hand icon carrying invisible dots
ROUTE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 420'>"
         "<rect x='6' y='6' width='888' height='408' rx='34' fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>"
         "<text x='450' y='70' text-anchor='middle' font-size='46' fill='#1a1410' " + AN + ">A DOCTOR'S MORNING, 1847</text>"
         "<rect x='40' y='120' width='250' height='170' rx='22' fill='#34425c'/>"
         "<text x='165' y='195' text-anchor='middle' font-size='40' fill='#f6efe2' " + AN + ">AUTOPSY</text>"
         "<text x='165' y='245' text-anchor='middle' font-size='26' fill='#cfe6ff' " + F + ">dissecting room</text>"
         "<rect x='610' y='120' width='250' height='170' rx='22' fill='#5b86b8'/>"
         "<text x='735' y='195' text-anchor='middle' font-size='40' fill='#f6efe2' " + AN + ">BIRTHS</text>"
         "<text x='735' y='245' text-anchor='middle' font-size='26' fill='#f6efe2' " + F + ">delivery ward</text>"
         "<path d='M300,205 L590,205' stroke='#d6483e' stroke-width='12' stroke-dasharray='26 14'/>"
         "<path d='M580,180 L610,205 L580,230 Z' fill='#d6483e'/>"
         "<rect x='345' y='255' width='210' height='62' rx='16' fill='#d6483e'/>"
         "<text x='450' y='298' text-anchor='middle' font-size='34' fill='#f6efe2' " + AN + ">NO WASH</text>"
         "<text x='450' y='375' text-anchor='middle' font-size='30' fill='#1a1410' " + F + ">same hands, straight to the mothers</text>"
         "</svg>")

S = []
# 0. hook (ward wide): the ticking 18% -> 2% hud at frame 0, the headline, Semmelweis walks down the aisle
S.append({"say": "Eighteen forty-seven. One doctor cut deaths on his ward from *18%* to under *2%*.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.08, "focus": [0.5, 0.6]}]},
          "layers": [plate("ward_wide"),
                     person("ward_wide", "midwife", 1.0, 8.5, [["idle", 0], ["surprised", 3.2]]),
                     person("ward_wide", "semmel", -0.3, 4.0, [["explain", 0], ["point", 3.0]], walk=[(0, -0.3, 7.0), (2.4, -0.3, 3.2)]),
                     ved("ward_wide", 0.75, -0.6, [["point", 0], ["explain", 1.8], ["surprised", 3.4]]),
                     txt("THE DOCTOR WHO SAID *WASH YOUR HANDS*", 0.145, 70, enter="none"),
                     hud("deaths on the ward", y=0.29, steps=[[0.0, 18], [2.2, 2]], suffix="%", tone="red", at=0.0, enter="none",
                         sub="1847, Vienna", width_of="18%"),
                     {"type": "stamp", "text": "SOAP?!", "tone": "green", "angle": -6, "size": 70, "x": 0.76, "y": 0.37,
                      "at": 2.8, "sfx": "thud"}]})
# 1. ward mid: two clinics, option cards; the student and the midwife
S.append({"say": "Doctors' clinic: *1 in 10* mothers died of fever. Midwives' clinic: far *fewer*.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.55, 0.55]}]},
          "layers": [plate("ward_mid"),
                     person("ward_mid", "student", -1.3, 4.0, [["idle", 0], ["shrug", 2.4]]),
                     person("ward_mid", "midwife", -1.75, 6.8, [["idle", 0], ["happy", 3.4]]),
                     {"type": "optcard", "label": "doctors' clinic", "text": "1 IN 10", "sub": "mothers died", "tone": "red",
                      "x": 0.28, "y": 0.14, "w": 0.42, "rotate": -3, "enter": "pop", "at": 0.6, "sfx": "pop"},
                     {"type": "optcard", "label": "midwives' clinic", "text": "FAR FEWER", "tone": "green", "x": 0.72, "y": 0.14,
                      "w": 0.42, "rotate": 3, "enter": "pop", "at": 3.0, "sfx": "pop", "verdict": "tick", "verdict_at": 0.6},
                     tag_layer(0.5, 0.29, 3.8)]})
# 2. dissection hall (night): doctors came straight from autopsies; the route card
S.append({"say": "Doctors came *straight from autopsies*.",
          "transition": "flash", "sfx": "boom", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("dissect"),
                     person("dissect", "student", -0.55, -1.45, [["explain", 0], ["point", 1.2]]),
                     {"type": "image", "svg": ROUTE, "x": 0.5, "y": 0.2, "w": 0.86, "rotate": -1.5, "enter": "slide_up", "at": 0.5,
                      "sfx": "whoosh", "keys": [{"t": 0, "scale": 1.0}, {"t": 2.5, "scale": 1.04}]}]})
# 3. dissection hall: Kolletschka's cut; tracker of the chain
S.append({"say": "Then his friend cut himself at one, and died of the *same fever*.",
          "transition": "push", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.1, "focus": [0.45, 0.55]}]},
          "layers": [plate("dissect", blur=9, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.22}]),
                     {"type": "character", "id": "extra", "pose": "surprised", "x": 0.3, "y": 1.0, "h": 1.0, "enter": "none",
                      "acting": [["surprised", 0], ["sad", 1.8]], "talk": False, "ground": False, "rig_args": {"outfit": OUT["semmel"]},
                      "allow_outside_safe": True},
                     hud("his friend, 1847", y=0.175, text="KOLLETSCHKA", tone="blue", at=0.1, width_of="KOLLETSCHKA"),
                     {"type": "tracker", "n": 3, "done": [0.6, 1.6, 2.6], "x": 0.5, "y": 0.255, "at": 0.3, "enter": "fade"},
                     txt("CORPSES  >  HANDS  >  *MOTHERS*", 0.315, 62, enter="pop", at=2.6, sfx="pop"),
                     tag_layer(0.78, 0.7, 3.0)]})
# 4. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("ward_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "\"wash hands? sir, we are *DOCTORS*\"", "text_y": 0.2}})
# 5. the washstand: chlorine before touching patients; jar drops in
S.append({"say": "So Semmelweis ordered: *wash in chlorine*.",
          "transition": "slide_up", "caption_y": 0.36,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 3.8, "zoom": 1.1, "focus": [0.45, 0.55]}]},
          "layers": [plate("wash"),
                     sprite("jar", 0.8, 0.24, 0.13, enter="pop", at=0.6, sfx="pop",
                            keys=[{"t": 0, "y": 0.17, "rot": -8}, {"t": 0.6, "y": 0.24, "rot": 0, "ease": "bounce"}]),
                     sprite("soap", 0.2, 0.24, 0.17, enter="pop", at=1.4, sfx="pop",
                            keys=[{"t": 0, "rot": 10}, {"t": 0.5, "rot": -4, "ease": "back"}]),
                     txt("*CHLORINE* WASH", 0.135, 88, enter="pop", at=0.2, sfx="pop"),
                     dict(close_ved([["explain", 0], ["point", 1.8]]), y=0.98, h=0.55, x=0.26),
                     tag_layer(0.72, 0.3, 2.4)]})
# 6. ward wide: the hud ticks 18 -> 2; Semmelweis cheers, the midwife too
S.append({"say": "April: *18%*. July: under *2%*.",
          "transition": "flash", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.55]}, {"t": 3.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("ward_wide"),
                     person("ward_wide", "midwife", 1.0, 8.5, [["happy", 0], ["cheer", 1.4]], hops=[[1.5, 0.04, 0.35]]),
                     person("ward_wide", "semmel", -0.3, 3.2, [["happy", 0], ["cheer", 1.2]], hops=[[1.3, 0.05, 0.35]]),
                     hud("deaths on the ward", y=0.13, steps=[[0.0, 18], [1.2, 2]], suffix="%", tone="green", at=0.0,
                         count_dur=1.0, width_of="18%"),
                     {"type": "eqbar", "x": 0.5, "y": 0.22, "tone": "green", "at": 0.2,
                      "keys": [[0.0, "APRIL 18%"], [1.3, "APRIL 18%  >  JULY *UNDER 2%*"]]},
                     tag_layer(0.5, 0.3, 1.8)]})
# 7. ward mid: senior doctors reject it; REJECTED stamp; out by 1849
S.append({"say": "Senior doctors *rejected* it. By eighteen forty-nine, he was *out*.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.07, "focus": [0.5, 0.55]}]},
          "layers": [plate("ward_mid"),
                     person("ward_mid", "student", -1.3, 4.0, [["shrug", 0], ["idle", 1.8]]),
                     person("ward_mid", "semmel", -1.5, 5.6, [["sad", 0.0]], walk=[(0, -1.5, 5.6), (3.2, -1.6, 9.0)]),
                     {"type": "optcard", "label": "their theory", "text": "BAD AIR", "tone": "red", "x": 0.3, "y": 0.13,
                      "w": 0.42, "rotate": -3, "enter": "pop", "at": 0.2, "sfx": "pop", "verdict": "cross", "verdict_at": 2.4},
                     {"type": "stamp", "text": "REJECTED", "tone": "red", "angle": -7, "size": 88, "x": 0.62, "y": 0.27,
                      "at": 0.9, "sfx": "thud"}]})
# 8. close payoff: germ theory proved him right
S.append({"say": "Germ theory proved him right. So when you wash your hands, thank *Semmelweis*.",
          "transition": "cut", "caption_y": 0.6,
          "layers": [plate("wash", blur=10, keys=[{"t": 0, "scale": 1.3}, {"t": 5.0, "scale": 1.38}]),
                     close_ved([["explain", 0], ["point", 2.2], ["smirk", 4.0]]),
                     {"type": "optcard", "label": "germ theory", "text": "HE WAS RIGHT", "tone": "green", "x": 0.5, "y": 0.13,
                      "w": 0.6, "rotate": -2, "enter": "pop", "at": 0.3, "sfx": "pop", "verdict": "tick", "verdict_at": 0.8},
                     txt("THANK *SEMMELWEIS*", 0.245, 84, enter="pop", at=3.4, sfx="ding")]})

job = {"id": ID, "title": "He told doctors to wash their hands. They pushed him out 🧼",
       "description": "In 1847 Ignaz Semmelweis worked in Vienna's maternity clinics. In the doctors' clinic about 1 in 10 "
                      "mothers died of childbed fever; in the midwives' clinic far fewer. The difference: doctors and students "
                      "came straight from autopsies. When his colleague Jakob Kolletschka cut himself during a post-mortem and "
                      "died of a similar illness, Semmelweis ordered hand washing in chlorine solution before touching patients. "
                      "Deaths fell from about 18% in April 1847 to under 2% by July. Senior doctors resisted, his post wasn't "
                      "renewed and he left Vienna in 1849. Germ theory (Pasteur) and antiseptic surgery (Lister, 1867) later "
                      "proved him right.\n\n"
                      "Sources: ScienceAlert (Ignaz Semmelweis); PMC review of Semmelweis (2024).",
       "tags": ["Semmelweis", "handwashing", "history of medicine", "germ theory", "science history", "true story",
                "childbed fever", "hand hygiene", "science facts"],
       "hashtags": ["#science", "#history"],
       "instagram": {"hashtags": ["#history", "#semmelweis", "#historyofmedicine", "#handwashing", "#explained"]},
       "meta": {"format": "wild-story", "topic": "Ignaz Semmelweis and handwashing (Vienna 1847): doctors' clinic ~1 in 10 mothers died "
                                                  "of childbed fever vs far fewer with midwives; doctors came from autopsies; "
                                                  "Kolletschka's autopsy cut and death; chlorine hand wash; ~18% (April 1847) to "
                                                  "under 2% (July); rejected by senior doctors, out of Vienna 1849; germ theory "
                                                  "later proved him right",
                "hook": "number-shock",
                "idea_source": "viral-shaped + unique: a famous 'impossible' turnaround (deaths cut ~10x) from the simplest "
                               "everyday act, told as a mini-drama; backlog idea (wild-story); new topic area after a run of "
                               "space and body Shorts",
                "characters": ["ved", "extra"],
                "sources": ["https://www.sciencealert.com/ignaz-semmelweis",
                            "https://pmc.ncbi.nlm.nih.gov/articles/PMC11568873/"],
                "humour": {"trend": "timeless dry aside (no rising meme fits 1840s medicine this week; 'Remember November' "
                                    "and 'W chews' already used): deadpan + '\"wash hands? sir, we are DOCTORS\"'",
                           "beat": "deadpan", "scene": 4},
                "claims": [
                    {"claim": "in Vienna General Hospital's doctors' maternity clinic about 1 in 10 mothers died of childbed fever; far fewer in the midwives' clinic", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/ignaz-semmelweis"},
                    {"claim": "doctors and medical students went from autopsies to the delivery ward", "tag": "PROVEN",
                     "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11568873/"},
                    {"claim": "in 1847 his colleague Jakob Kolletschka cut himself during a post-mortem and died of a similar illness", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/ignaz-semmelweis"},
                    {"claim": "Semmelweis ordered hand washing in chlorine solution; deaths fell from ~18% (April 1847) to under 2% by July", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/ignaz-semmelweis"},
                    {"claim": "senior colleagues resisted; his post was not renewed and he left Vienna in 1849; Pasteur and Lister later vindicated him", "tag": "PROVEN",
                     "source": "https://www.sciencealert.com/ignaz-semmelweis"}]},
       "thumbnail": {"title": "JUST *WASH?*", "title_y": 0.15, "title_size": 190, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.3,
                     "tint": ["#2f6f8f", "#f08a24"], "tint_amount": 0.28,
                     "bg": [plate("ward_wide")],
                     "fg": [sprite("jar", 0.2, 0.5, 0.22), sprite("soap", 0.82, 0.48, 0.22),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.8, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
