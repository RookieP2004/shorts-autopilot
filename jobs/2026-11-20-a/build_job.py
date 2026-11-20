"""2026-11-20-a: "A drug lord bought 4 hippos. Now there are 200" (dark-files, number-shock hook).
2D Ved + two townspeople (Lucia the ranch keeper, Mateo the fisherman) in two Blender sets: the sunny ranch with its
pond and 4 hippos (Hacienda Napoles), and the wide tropical river with a herd of ~30 hippos and a fishing boat.
2D on top: ticking hud chips (4 -> 200, 200 -> 1,000, cull 80), an eqbar, datelines (1980s, 1993), option cards with
ticks/crosses, a stamp, hippo cut-outs that pop in and multiply, the comic beat.
Facts (AP via Fortune 2026-04-13; Global News 2026-04-14; NPR/OPB 2026-05-08; AFP via Malay Mail 2026-08-06):
4 hippos brought in by Escobar in the 1980s to his Hacienda Napoles zoo; after he was killed by police in 1993 nobody
captured them; no natural predators, they bred along the Magdalena River; ~200 today (Environment Ministry), the largest
herd outside Africa; minister Irene Velez: could reach ~1,000 by 2035 without control; they pollute water and compete
with manatees and displace native species; sterilising has been costly and slow; 13 April 2026: culling of up to 80
authorised; Anant Ambani offered to relocate 80 to his Vantara reserve in Gujarat, India.
Documentary view: no glamour, Escobar only as the cause.
Run after the assets exist: python jobs/2026-11-20-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-20-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("ranch_wide", "ranch_mid", "river_wide", "river_close")}

OUT = {   # recurring townspeople: same outfit in every shot
    "lucia": {"skin": "#c68a5e", "build": "slim", "hair": ["#1a1410", "bun"], "hat": ["straw", "#e8c77a"],
              "top": ["#46965a", "shirt"], "bottom": ["#5a4632", "trousers"], "shoes": "#25262b", "belt": "#7a4e2a"},
    "mateo": {"skin": "#8d5a3b", "build": "round", "hair": ["#1a1410", "short"], "hat": ["straw", "#d9b46a"],
              "top": ["#f6efe2", "shirt"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "necklace": "#d9534f"},
}
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


def hippo_pop(x, y, w, at, flip=False):
    L = sprite("hippo", x, y, w, enter="pop", at=at, sfx="pop")
    if flip:
        L["flip"] = True
    return L


# cream card: what the hippos do to the river
RIVER_CARD = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 300'>"
              "<rect x='6' y='6' width='588' height='288' rx='30' fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>"
              f"<text x='300' y='70' text-anchor='middle' font-size='46' fill='#1a1410' {AN}>THE RIVER PAYS</text>"
              "<path d='M40,120 Q120,95 200,120 T360,120 T560,120' stroke='#3f7fbf' stroke-width='12' fill='none'/>"
              f"<text x='150' y='200' text-anchor='middle' font-size='40' fill='#d9534f' {AN}>OXYGEN DOWN</text>"
              f"<text x='450' y='200' text-anchor='middle' font-size='40' fill='#d9534f' {AN}>MANATEES OUT</text>"
              f"<text x='300' y='265' text-anchor='middle' font-size='34' fill='#5a4632' {AN}>+ NATIVE SPECIES PUSHED ASIDE</text></svg>")

S = []
# 0. hook: the herd on the river, blurred; headline + ticking chip at frame 0; Ved to camera
S.append({"say": "A drug lord bought *4 hippos*. Now there are *200*.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.08, "focus": [0.5, 0.45]}]},
          "layers": [plate("river_wide", blur=5, keys=[{"t": 0, "scale": 1.1}, {"t": 3.4, "scale": 1.16}]),
                     txt("4 HIPPOS -> *200*", 0.12, 104, enter="none"),
                     hud("escobar's hippos", y=0.25, at=0.0, enter="none", tone="gold", width_of="200",
                         steps=[[0.0, 4], [1.2, 4], [2.6, 200]]),
                     dict(close_ved([["surprised", 0], ["point", 1.4], ["explain", 2.4]]), y=1.0, h=0.6, x=0.5)]})
# 1. ranch wide: the private zoo in the 1980s; Lucia by the pond; Ved walks in
S.append({"say": "Escobar kept them in his *private zoo*.",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "layers": [plate("ranch_wide"),
                     {"type": "dateline", "date": "1980s", "place": "COLOMBIA", "x": 0.5, "y": 0.22, "at": 0.1, "enter": "fade", "sfx": "type"},
                     person("ranch_wide", "lucia", 2.4, -3.0, [["idle", 0], ["point", 1.4], ["idle", 2.8]]),
                     ved("ranch_wide", -1.4, -3.4, [["explain", 0], ["point", 1.6]], walk=[(0, -4.6, -3.4), (1.3, -1.4, -3.4)]),
                     {"type": "image", "svg": tag("PROVEN"), "x": 0.5, "y": 0.62, "w": 0.26, "enter": "pop", "at": 2.4, "sfx": "click"}]})
# 2. ranch mid: 1993, nobody caught the hippos; one walks out of frame
S.append({"say": "In *1993* he was killed. Nobody caught the hippos.",
          "transition": "cut", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.1, "focus": [0.55, 0.6]}]},
          "layers": [plate("ranch_mid"),
                     {"type": "dateline", "date": "DEC 1993", "place": "MEDELLIN", "x": 0.5, "y": 0.22, "at": 0.0, "enter": "fade", "sfx": "type"},
                     sprite("hippo", 0.45, 0.66, 0.42, keys=[{"t": 0, "x": 0.45}, {"t": 1.4, "x": 0.45}, {"t": 3.4, "x": 1.25}]),
                     {"type": "stamp", "text": "NOBODY CAUGHT THEM", "tone": "red", "angle": -6, "size": 66, "x": 0.5, "y": 0.34,
                      "at": 1.5, "sfx": "thud"}]})
# 3. river close: why they boomed, three ticks; Mateo in his boat; hippos multiply
S.append({"say": "Warm rivers, food all year, no lions. *They bred.*",
          "transition": "slide_up", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.08, "focus": [0.45, 0.6]}]},
          "layers": [plate("river_close"),
                     {"type": "optcard", "label": "river", "text": "WARM", "tone": "green", "x": 0.2, "y": 0.14, "w": 0.28,
                      "rotate": -3, "enter": "pop", "at": 0.1, "sfx": "pop", "verdict": "tick", "verdict_at": 0.3},
                     {"type": "optcard", "label": "food", "text": "ALL YEAR", "tone": "green", "x": 0.5, "y": 0.14, "w": 0.28,
                      "enter": "pop", "at": 0.8, "sfx": "pop", "verdict": "tick", "verdict_at": 0.3},
                     {"type": "optcard", "label": "predators", "text": "NONE", "tone": "green", "x": 0.8, "y": 0.14, "w": 0.28,
                      "rotate": 3, "enter": "pop", "at": 1.5, "sfx": "pop", "verdict": "tick", "verdict_at": 0.3},
                     person("river_close", "mateo", -2.6, 1.4, [["idle", 0], ["surprised", 2.0]]),
                     hippo_pop(0.62, 0.56, 0.2, 2.1), hippo_pop(0.8, 0.6, 0.18, 2.3, True), hippo_pop(0.5, 0.66, 0.22, 2.5),
                     hippo_pop(0.72, 0.7, 0.24, 2.7, True), hippo_pop(0.28, 0.62, 0.18, 2.9)]})
# 4. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("river_wide", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "Escobar's longest-running *operation*", "text_y": 0.2}})
# 5. river wide: biggest herd outside Africa, heading for 1,000 by 2035
S.append({"say": "Now it's the biggest herd outside Africa. It could hit *1,000 by 2035*.",
          "transition": "cut", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.12, "focus": [0.5, 0.45]}]},
          "layers": [plate("river_wide"),
                     hud("hippos in colombia", y=0.13, steps=[[0.0, 200], [2.4, 200], [3.8, 1000]], at=0.1, tone="red", width_of="1,000"),
                     {"type": "eqbar", "x": 0.5, "y": 0.23, "at": 0.4, "tone": "red",
                      "keys": [[0.0, "200 today"], [2.2, "200 -> *1,000* by 2035"]]},
                     txt("BIGGEST HERD OUTSIDE AFRICA", 0.72, 48, enter="pop", at=0.9, sfx="pop", color="#ffd23a"),
                     tag_layer(0.5, 0.31, 3.0, "THEORY", "#f2b04a")]})
# 6. close Ved over the blurred river: the damage + why neutering doesn't keep up
S.append({"say": "They foul rivers and push out manatees. Neutering? *Too slow*.",
          "transition": "cut", "caption_y": 0.42,
          "layers": [plate("river_close", blur=10, keys=[{"t": 0, "scale": 1.25}, {"t": 4.5, "scale": 1.32}]),
                     {"type": "image", "svg": RIVER_CARD, "x": 0.5, "y": 0.18, "w": 0.74, "enter": "pop", "at": 0.2, "sfx": "pop"},
                     {"type": "optcard", "label": "neuter one by one?", "text": "SLOW + COSTLY", "tone": "red", "x": 0.5, "y": 0.56,
                      "w": 0.5, "rotate": -3, "enter": "pop", "at": 2.4, "sfx": "pop", "verdict": "cross", "verdict_at": 0.6},
                     dict(close_ved([["explain", 0], ["think", 2.2], ["serious", 3.6]]), y=1.02, h=0.6, x=0.5)]})
# 7. ranch wide: April 2026, culling of up to 80 approved; the India offer; Lucia shrugs
S.append({"say": "So Colombia approved culling up to *80*. An Indian billionaire offered to take them.",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("ranch_wide"),
                     hud("cull approved, april 2026", y=0.13, to=80, prefix="UP TO ", count_dur=1.2, at=0.3, tone="red", width_of="UP TO 80"),
                     {"type": "optcard", "label": "the offer", "text": "MOVE THEM\nTO INDIA", "sub": "Vantara, Gujarat", "tone": "gold",
                      "x": 0.5, "y": 0.3, "w": 0.46, "rotate": 3, "enter": "pop", "at": 2.4, "sfx": "pop"},
                     person("ranch_wide", "lucia", 2.4, -3.0, [["idle", 0], ["shrug", 2.6]]),
                     ved("ranch_wide", -1.4, -3.4, [["explain", 0], ["point", 2.4], ["think", 3.6]])]})
# 8. payoff: river close, loops back to the start
S.append({"say": "30 years later, his hippos are *still multiplying*.",
          "transition": "zoom", "caption_y": 0.42, "sfx": "ding",
          "camera": {"keys": [{"t": 0, "zoom": 1.12, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("river_wide"),
                     txt("STILL *GROWING*", 0.13, 96, enter="pop", at=1.6, sfx="pop"),
                     hud("escobar's hippos", y=0.24, steps=[[0.0, 4], [0.8, 200]], at=0.2, tone="gold", width_of="200"),
                     person("river_close", "mateo", -2.6, 1.4, [["idle", 0], ["shrug", 1.8]], x=0.2, y=0.9, h=0.4),
                     dict(close_ved([["warm", 0], ["smirk", 2.6]]), y=1.0, h=0.55, x=0.64)]})

job = {"id": ID, "title": "A drug lord bought 4 hippos. Now there are 200 🦛",
       "description": "In the 1980s Pablo Escobar brought four hippos to the private zoo at his ranch, Hacienda Napoles. After "
                      "he was killed by police in 1993, nobody caught them. With warm rivers, food all year and no predators, "
                      "they bred along the Magdalena River: about 200 today, the largest hippo herd outside Africa, and Colombia's "
                      "environment minister warned it could reach about 1,000 by 2035. They pollute rivers and compete with "
                      "manatees, and sterilising them has been slow and costly, so in April 2026 Colombia authorised culling up "
                      "to 80, while Indian billionaire Anant Ambani offered to move 80 to his Vantara reserve in Gujarat.\n\n"
                      "Sources: AP (Fortune, 13 Apr 2026); Global News (14 Apr 2026); NPR/OPB (8 May 2026); AFP (Malay Mail, 6 Aug 2026).",
       "tags": ["escobar hippos", "cocaine hippos", "pablo escobar", "hippos in colombia", "invasive species",
                "hacienda napoles", "wildlife", "true story", "explained"],
       "hashtags": ["#hippo", "#truestory"],
       "instagram": {"hashtags": ["#wildlife", "#hippo", "#pabloescobar", "#colombia", "#explained"]},
       "meta": {"format": "dark-files", "topic": "Pablo Escobar's hippos: 4 brought to his Hacienda Napoles zoo in the 1980s; after "
                                                 "he was killed (1993) nobody caught them; no predators, warm rivers, food all year; "
                                                 "~200 now, biggest herd outside Africa; could reach ~1,000 by 2035 (minister Velez); "
                                                 "pollute rivers, compete with manatees; sterilising slow and costly; April 2026 cull "
                                                 "of up to 80 authorised; Ambani's offer to move 80 to Vantara, Gujarat",
                "hook": "number-shock",
                "idea_source": "trending + viral-shaped: the 2026 cull decision and the India relocation offer keep the 'cocaine "
                               "hippos' in the news (strong India share of the audience); a crime boss's strange legacy made "
                               "picturable (4 -> 200 -> 1,000); dark-files backlog example 'Pablo Escobar's hippos'",
                "characters": ["ved", "extra"],
                "sources": ["https://fortune.com/2026/04/13/colombia-cocaine-hippos-pablo-escobar/",
                            "https://globalnews.ca/news/11800768/cocaine-hippos-pablo-escobar-euthanized-colombia/",
                            "https://www.opb.org/article/2026/05/08/from-doradal-to-gujarat-cocaine-hippos-get-a-billionaire-sponsored-lifeline/",
                            "https://www.malaymail.com/amp/news/life/2026/08/06/escobars-escaped-hippos-keep-making-headlines-this-time-with-a-tragic-loss/230379",
                            "https://en.wikipedia.org/wiki/Hippopotamuses_in_Colombia"],
                "humour": {"trend": "timeless dry aside (no fresh rising meme fits a cartel topic cleanly): deadpan + "
                                    "'Escobar's longest-running operation' card on the hippos multiplying",
                           "beat": "deadpan", "scene": 4},
                "claims": [
                    {"claim": "Escobar brought 4 hippos to his ranch's private zoo (Hacienda Napoles) in the 1980s", "tag": "PROVEN",
                     "source": "https://fortune.com/2026/04/13/colombia-cocaine-hippos-pablo-escobar/"},
                    {"claim": "after Escobar was killed by police in 1993 nobody captured the hippos", "tag": "PROVEN",
                     "source": "https://www.opb.org/article/2026/05/08/from-doradal-to-gujarat-cocaine-hippos-get-a-billionaire-sponsored-lifeline/"},
                    {"claim": "about 200 hippos today, the largest colony outside Africa", "tag": "PROVEN",
                     "source": "https://www.malaymail.com/amp/news/life/2026/08/06/escobars-escaped-hippos-keep-making-headlines-this-time-with-a-tragic-loss/230379"},
                    {"claim": "could increase to as many as 1,000 by 2035 without control (Environment Minister Irene Velez)", "tag": "THEORY",
                     "source": "https://globalnews.ca/news/11800768/cocaine-hippos-pablo-escobar-euthanized-colombia/"},
                    {"claim": "they pollute water and compete with manatees, displacing native species; sterilisation costly", "tag": "PROVEN",
                     "source": "https://fortune.com/2026/04/13/colombia-cocaine-hippos-pablo-escobar/"},
                    {"claim": "13 April 2026: culling of up to 80 hippos authorised", "tag": "PROVEN",
                     "source": "https://fortune.com/2026/04/13/colombia-cocaine-hippos-pablo-escobar/"},
                    {"claim": "Anant Ambani offered to relocate 80 hippos to Vantara in Gujarat, India", "tag": "PROVEN",
                     "source": "https://www.opb.org/article/2026/05/08/from-doradal-to-gujarat-cocaine-hippos-get-a-billionaire-sponsored-lifeline/"}]},
       "thumbnail": {"title": "4 HIPPOS -> *200*", "title_y": 0.2, "title_size": 150, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.3,
                     "tint": ["#2f8fe0", "#f08a24"], "tint_amount": 0.25,
                     "bg": [plate("river_wide")],
                     "fg": [sprite("hippo", 0.2, 0.47, 0.34),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
