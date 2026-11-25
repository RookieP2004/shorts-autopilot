"""2026-11-25-a: "Skyscrapers stand still? This one hides a 660-ton ball" (myth-bust; Ved as an enthusiast in his model room).
Lane: engineering and megaprojects. Explain mode: analogy demo (his model tower with a little gold ball in its clear top).
Styles mixed: animated Blender shots (moving 3D: the tower swaying in the wind, the golden damper swinging inside, the
cut-away tower and ball moving opposite), Ved's model room (3D plates), a Reelsmith RS-05 Blueprint, hud chips, stamps and a
dateline, the comic beat.
Facts (verified 2026-11-25):
- Taipei 101 is 508 m tall (Guinness World Records; Business Insider via Yahoo).
- Its tuned mass damper is a 660-tonne steel sphere (41 steel plates, ~5.5 m wide) hanging between the 87th and 92nd floors;
  Guinness: the largest tuned mass damper; it lags as the building sways and moves opposite to it, and hydraulic dampers turn
  the motion into heat (Guinness; Yahoo/Business Insider citing Taipei 101).
- It reduces the sway by up to 40% (A+H, the builder, quoted by Business Insider).
- Biggest recorded swing: 100 cm on 8 Aug 2015, Typhoon Soudelor (Guinness; Taiwan News); max design swing 1.5 m.
Run after the assets exist: python jobs/2026-11-25-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-25-a"
J = f"jobs/{ID}/"
A = J + "assets/"
SH = J + "shots/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("room_wide", "room_low")}
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
WEAR = {"wear": "badge"}


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
            f"<text x='188' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.26, "enter": "pop", "at": at, "sfx": "click"}


S = []
# 0. hook (moving 3D): the tiered tower sways in the wind; the myth headline at frame 0; BUSTED slams in
S.append({"say": "Skyscrapers stand still? *Nope.* They *sway*.",
          "layers": [shot("a_sway.py", 3.8),
                     txt("MYTH: SKYSCRAPERS STAND *STILL*", 0.15, 96, enter="none"),
                     {"type": "stamp", "text": "BUSTED", "tone": "red", "angle": -7, "size": 72, "x": 0.5, "y": 0.29,
                      "at": 1.5, "sfx": "thud"},
                     dict(close_ved([["deadpan", 0], ["point", 1.6]]), x=0.82, y=1.0, h=0.55)]})
# 1. Ved's model room, wide: he walks in to his model tower (badge on: the superfan); height ticks up
S.append({"say": "Taipei 101: *508 meters* tall, and it fights *back*.",
          "transition": "slide_left", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.45]}]},
          "layers": [plate("room_wide"),
                     ved("room_wide", -0.55, 0.9, [["idle", 0], ["explain", 1.2], ["point", 2.6]],
                         walk=[(0, -2.4, 0.9), (1.1, -0.55, 0.9)], rig_args=WEAR),
                     {"type": "hud", "label": "taipei 101", "to": 508, "suffix": " M", "count_dur": 1.0, "x": 0.5, "y": 0.14,
                      "at": 0.4, "enter": "pop", "sfx": "click", "tone": "blue", "indian": False}]})
# 2. the damper (moving 3D): the golden ball swings inside the top floors; 660 tonnes ticks
S.append({"say": "With *this*: a *660-ton* steel ball near the top.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("b_ball.py", 4.2),
                     {"type": "hud", "label": "the damper ball", "to": 660, "suffix": " TONNES", "count_dur": 1.0,
                      "x": 0.5, "y": 0.13, "at": 0.5, "enter": "pop", "sfx": "click", "tone": "gold", "indian": False},
                     tag_layer(0.5, 0.235, 1.8)]})
# 3. analogy demo: close on Ved's model, its clear top showing the little gold ball; Ved leans in
S.append({"say": "Watch my model. Wind shoves the tower *one* way...",
          "transition": "zoom", "caption_y": 0.72,
          "layers": [plate("room_model", keys=[{"t": 0, "scale": 1.0}, {"t": 3.2, "scale": 1.07}]),
                     dict(close_ved([["explain", 0], ["point", 1.0]]), x=0.25, y=1.02, h=0.62, rig_args=WEAR)]})
# 4. cut-away (moving 3D): the tower leans one way, the ball swings the other
S.append({"say": "the heavy ball swings the *other* way, pulling it back.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("c_opposite.py", 4.8),
                     txt("BALL SWINGS *OPPOSITE*", 0.13, 88, enter="pop", at=0.2, sfx="pop")]})
# 5. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("room_model", blur=10, keys=[{"t": 0, "scale": 1.2}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "the ball in every group project: *does all of it*", "text_y": 0.2}})
# 6. Reelsmith RS-05 Blueprint: the parts, pistons -> heat
S.append({"say": "Then giant pistons turn that swing into *heat*.",
          "transition": "cut", "caption_y": 0.74, "pad": 1.0,
          "layers": [{"type": "look", "look": "RS-05", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "at": 0.0,
                      "props": {"title": "TUNED MASS DAMPER",
                                "parts": [{"label": "STEEL BALL", "shape": "circle", "note": "41 plates"},
                                          {"label": "CABLES", "shape": "cyl", "note": "hang it"},
                                          {"label": "PISTONS", "shape": "cyl", "note": "swing -> heat"},
                                          {"label": "BUMPER RING", "shape": "circle", "note": "max 1.5 m"}]}}]})
# 7. low hero angle of the room: up to 40% less sway; Ved jumps
S.append({"say": "Result? Up to *40 percent* less sway.",
          "transition": "slide_up", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.55]}, {"t": 3.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("room_low"),
                     ved("room_low", -0.6, 0.75, [["explain", 0], ["surprised", 1.4]], hops=[[1.5, 0.06, 0.45]]),
                     {"type": "hud", "label": "less sway", "prefix": "UP TO ", "to": 40, "suffix": "%", "count_dur": 0.9,
                      "x": 0.5, "y": 0.14, "at": 0.4, "enter": "pop", "sfx": "click", "tone": "green", "indian": False}]})
# 8. the typhoon: the ball sprite swings wide over the blurred model close-up; dateline + 1 m
S.append({"say": "In a 2015 typhoon, it swung a full *meter*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [plate("room_model", blur=12, keys=[{"t": 0, "scale": 1.25}, {"t": 3.2, "scale": 1.32}]),
                     sprite("ball", 0.5, 0.46, 0.5, keys=[{"t": 0, "x": 0.34, "rot": 8}, {"t": 0.9, "x": 0.66, "rot": -8},
                                                          {"t": 1.8, "x": 0.34, "rot": 8}, {"t": 2.7, "x": 0.64, "rot": -7},
                                                          {"t": 3.4, "x": 0.4, "rot": 5}]),
                     {"type": "hud", "label": "august 2015", "text": "TYPHOON SOUDELOR", "x": 0.5, "y": 0.13, "at": 0.1,
                      "enter": "pop", "sfx": "click", "tone": "blue"},
                     {"type": "hud", "label": "record swing", "text": "1 METER", "x": 0.5, "y": 0.25, "at": 1.4,
                      "enter": "pop", "sfx": "click", "tone": "red"}]})
# 9. payoff, back in the room: Ved by his model, MYTH BUSTED
S.append({"say": "They don't stand still. They *dance*, with a 660-ton partner.",
          "transition": "cut", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("room_wide"),
                     ved("room_wide", -0.55, 0.9, [["explain", 0], ["warm", 2.2], ["smirk", 3.6]]),
                     {"type": "stamp", "text": "MYTH BUSTED", "tone": "green", "angle": -6, "size": 70, "x": 0.5, "y": 0.2,
                      "at": 2.3, "sfx": "thud"}]})

SRC = ["https://www.guinnessworldrecords.com/world-records/774616-largest-tuned-mass-damper",
       "https://ca.news.yahoo.com/660-ton-pendulum-protects-taiwans-180430672.html",
       "https://www.taiwannews.com.tw/news/5963038",
       "https://boingboing.net/2022/09/19/watch-the-tuned-mass-damper-inside-a-taipei-skyscraper-react-to-this-weekends-6-9-magnitude-earthquake.html"]
job = {"id": ID, "title": "Skyscrapers stand still? This one hides a 660-ton ball 🏙️",
       "description": "Tall buildings sway in the wind, and Taipei 101 (508 m) fights back with the world's largest tuned mass "
                      "damper: a 660-tonne steel ball made of 41 steel plates, hanging between the 87th and 92nd floors. When "
                      "the tower moves one way, the heavy ball lags and swings the other way, and hydraulic pistons turn that "
                      "motion into heat. The builder says it cuts the sway by up to 40%. Its biggest recorded swing was about "
                      "1 metre, during Typhoon Soudelor in August 2015 (design maximum: 1.5 m).\n\n"
                      "Sources: Guinness World Records (largest tuned mass damper); Business Insider via Yahoo News; "
                      "Taiwan News; Boing Boing.",
       "tags": ["Taipei 101", "tuned mass damper", "skyscraper", "engineering", "how buildings work", "physics",
                "architecture", "myth busting", "science explained"],
       "hashtags": ["#engineering", "#physics"],
       "instagram": {"hashtags": ["#engineering", "#taipei101", "#skyscraper", "#architecture", "#explained"]},
       "meta": {"format": "myth-bust",
                "topic": "skyscrapers sway: Taipei 101 (508 m) and its 660-tonne tuned mass damper (41 steel plates, floors "
                         "87-92, Guinness largest); the ball lags and swings opposite, hydraulic pistons turn motion into heat; "
                         "up to 40% less sway (A+H); record swing ~1 m in Typhoon Soudelor (Aug 2015)",
                "hook": "myth-bust",
                "idea_source": "viral-shaped + unique: a famous engineering marvel made simple with one model and one gold "
                               "ball; most Shorts only show the ball, few explain why it swings the other way; lane "
                               "engineering and megaprojects",
                "lane": "engineering and megaprojects", "role": "enthusiast", "explain": "analogy demo",
                "role_visual": "Ved's model room: a work table with his model of the tiered tower (clear top with a tiny gold "
                               "ball), other skyscraper models, blueprint posters signed 'drawn by Ved'; fan badge in two scenes",
                "styles": ["blender-3d", "model-room", "RS-05", "hud", "stamp", "comic"],
                "characters": ["ved"],
                "sources": SRC,
                "humour": {"trend": "timeless US school-life card (no rising US trend fit cleanly this week): "
                                    "\"the ball in every group project: does all of it\"",
                           "beat": "deadpan", "scene": 5},
                "claims": [
                    {"claim": "Taipei 101 is 508 m tall", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "its tuned mass damper is a 660-tonne steel sphere of 41 plates hung between floors 87 and 92; the largest TMD (Guinness)", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "it lags and moves opposite to the building's sway; hydraulic dampers turn the motion into heat", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "reduces sway by up to 40% (builder A+H)", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "largest recorded swing ~100 cm in Typhoon Soudelor, 8 Aug 2015; design max 1.5 m", "tag": "PROVEN", "source": SRC[2]}]},
       "thumbnail": {"title": "660-TON *BALL?*", "title_y": 0.2, "title_size": 165, "max_w": 0.95, "blur": 14,
                     "glow": "#f2b04a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.2, "bg_saturation": 1.3,
                     "tint": ["#1c3f73", "#f2b04a"], "tint_amount": 0.22,
                     "bg": [plate("room_wide")],
                     "fg": [sprite("ball", 0.22, 0.46, 0.34, rotate=-6),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.6, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
