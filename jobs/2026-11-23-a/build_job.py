"""2026-11-23-a: "Sugar makes kids hyper? Scientists tested it" (myth-bust; Ved as a chef in a party kitchen).
Styles mixed: the Blender party kitchen with Ved and townspeople (mom, boy, girl), a Reelsmith RS-03 Balance (the two diets
weigh the same), hud chips, option cards and stamps, red-cup cut-outs, the comic beat.
Facts: Wolraich et al., NEJM 1994;330:301-7: 25 preschoolers + 23 school-age children described by parents as sugar-
sensitive; double-blind, three consecutive 3-week diets (high sucrose / aspartame / saccharin placebo); no significant
differences on 39 behavioural and cognitive measures for the sugar-sensitive children.
Hoover & Milich, J Abnorm Child Psychol 1994;22:501-15: 35 boys aged 5-7 reported as sugar-sensitive; all got a placebo
(aspartame); mothers told "a large dose of sugar" rated their sons significantly more hyperactive and kept physically closer.
Wolraich, Wilson & White, JAMA 1995 meta-analysis (16 reports, 23 studies): sugar does not affect behaviour or cognition.
Run after the assets exist: python jobs/2026-11-23-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-23-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("kit_wide", "kit_cake", "kit_cups")}

OUT = {   # recurring people: same outfit in every shot
    "mom": {"skin": "#c98e62", "build": "regular", "hair": ["#2a1d17", "long"], "top": ["#3f7fbf", "dress"],
            "necklace": "#f2b04a", "shoes": "#25262b"},
    "boy": {"skin": "#e2b48c", "build": "slim", "hair": ["#6b4a2b", "short"], "hat": ["cap", "#d6483e"],
            "top": ["#f2b04a", "tshirt"], "bottom": ["#34425c", "shorts"], "shoes": "#f6efe2"},
    "girl": {"skin": "#8d5a3b", "build": "slim", "hair": ["#1a1410", "curly"], "top": ["#46965a", "tshirt"],
             "bottom": ["#f4a6c0", "skirt"], "shoes": "#f6efe2"},
}
KID = 0.62     # kids are drawn at 62% of an adult's height
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
    s = KID if who in ("boy", "girl") else 1.0
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": round(p["h"] * s, 3),
         "enter": "none", "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
    if walk:
        keys = st.walk(walk, p, "extra")
        if s != 1.0:
            for kk in keys:
                if "h" in kk:
                    kk["h"] = round(kk["h"] * s, 3)
        L["keys"] = keys
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


S = []
# 0. hook (cake close-up): MYTH? stamp + headline at frame 0; chef Ved beside the cake
S.append({"say": "Sugar makes kids *hyper*? Scientists tested it. *It doesn't.*",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "layers": [plate("kit_cake"),
                     {"type": "stamp", "text": "MYTH?", "tone": "red", "angle": -6, "size": 80, "x": 0.5, "y": 0.1, "at": 0.0, "enter": "none"},
                     txt("SUGAR MAKES KIDS *HYPER?*", 0.2, 88, enter="none"),
                     dict(close_ved([["point", 0], ["explain", 1.6], ["smirk", 2.8]]), x=0.8, y=0.98, h=0.56),
                     sprite("cupcake", 0.18, 0.62, 0.2, enter="pop", at=0.6, sfx="pop"),
                     {"type": "stamp", "text": "NOPE", "tone": "green", "angle": 6, "size": 70, "x": 0.25, "y": 0.75, "at": 2.6, "sfx": "thud"}]})
# 1. party kitchen wide: kids hop around; chef Ved walks in; 3 diets x 3 weeks
S.append({"say": "In 1994, kids spent three weeks on each of three diets: *sugar*, or *sweeteners*.",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.07, "focus": [0.5, 0.6]}]},
          "layers": [plate("kit_wide"),
                     person("kit_wide", "girl", -0.5, 1.0, [["happy", 0], ["cheer", 2.0]], hops=[[0.6, 0.05, 0.45], [2.4, 0.05, 0.45]]),
                     person("kit_wide", "boy", 0.3, 0.8, [["cheer", 0], ["happy", 1.8]], hops=[[1.2, 0.05, 0.45], [3.0, 0.05, 0.45]]),
                     ved("kit_wide", 0.65, -0.3, [["idle", 0], ["explain", 1.2], ["point", 3.0]], walk=[(0, 2.4, -0.3), (1.1, 0.65, -0.3)]),
                     {"type": "dateline", "date": "1994", "place": "DOUBLE-BLIND STUDY", "size": 56, "x": 0.5, "y": 0.15, "at": 0.1, "enter": "fade", "sfx": "type"},
                     hud("weeks on each diet", y=0.27, to=3, count_dur=0.6, at=1.6, tone="blue", sub="3 DIETS"),
                     {"type": "optcard", "label": "diet 1", "text": "SUGAR", "tone": "gold", "x": 0.27, "y": 0.62, "w": 0.34, "rotate": -3,
                      "enter": "pop", "at": 3.4, "sfx": "pop"},
                     {"type": "optcard", "label": "diets 2 + 3", "text": "SWEETENER", "tone": "blue", "x": 0.73, "y": 0.62, "w": 0.34, "rotate": 3,
                      "enter": "pop", "at": 4.0, "sfx": "pop"}]})
# 2. Reelsmith RS-03 Balance over the blurred kitchen: the diets weigh the same
S.append({"say": "Nobody knew which was which. On *39* behavior and brain tests: *no difference*.",
          "transition": "zoom", "caption_y": 0.74, "pad": 0.8,
          "layers": [plate("kit_wide", blur=12, keys=[{"t": 0, "scale": 1.2}, {"t": 5, "scale": 1.27}]),
                     {"type": "look", "look": "RS-03", "x": 0.5, "y": 0.39, "w": 1.0, "h": 0.6, "at": 0.0,
                      "props": {"title": "39 TESTS", "backdrop": "dim", "left": {"label": "SUGAR", "value": 39, "unit": ""},
                                "right": {"label": "SWEETENER", "value": 39, "unit": ""}, "verdict": "NO DIFFERENCE"}},
                     tag_layer(0.5, 0.12, 2.8)]})
# 3. close on the two identical red cups: same drink, different story for the moms
S.append({"say": "Then *35 boys* got a sugar-free drink. But half their moms were told: *loaded with sugar*.",
          "transition": "slide_up", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.1, "focus": [0.5, 0.55]}]},
          "layers": [plate("kit_cups"),
                     hud("boys, age 5 to 7", y=0.16, to=35, count_dur=0.8, at=0.2, tone="blue"),
                     tag_layer(0.5, 0.27, 1.2, "PLACEBO", "#f2b04a"),
                     {"type": "optcard", "label": "moms told", "text": "NO SUGAR", "tone": "blue", "x": 0.73, "y": 0.68, "w": 0.36,
                      "rotate": 3, "enter": "pop", "at": 2.6, "sfx": "pop"},
                     {"type": "optcard", "label": "moms told", "text": "SUGAR!", "tone": "red", "x": 0.27, "y": 0.68, "w": 0.36,
                      "rotate": -3, "enter": "pop", "at": 3.6, "sfx": "pop"},
                     {"type": "stamp", "text": "SAME DRINK", "tone": "green", "angle": -6, "size": 62, "x": 0.5, "y": 0.35, "at": 1.6, "sfx": "thud"}]})
# 4. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("kit_cake", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "mom's evidence board: *cake -> chaos*", "text_y": 0.2}})
# 5. kitchen wide: the mom hovers over a perfectly calm boy
S.append({"say": "Those moms rated their sons *more hyper*, and hovered *closer*.",
          "transition": "cut", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.05, "focus": [0.45, 0.6]}, {"t": 3.6, "zoom": 1.14, "focus": [0.42, 0.62]}]},
          "layers": [plate("kit_wide"),
                     person("kit_wide", "boy", 0.25, 0.75, [["idle", 0], ["shrug", 2.2]]),
                     person("kit_wide", "mom", -1.4, 0.3, [["surprised", 0], ["point", 1.0], ["explain", 2.4]],
                            walk=[(0, -1.8, 0.4), (1.6, -0.4, 0.55)]),
                     ved("kit_wide", 0.7, -0.3, [["explain", 0], ["side_eye", 2.4]]),
                     hud("mom's hyper rating", y=0.17, steps=[[0, 0], [0.4, 1], [0.8, 2], [1.2, 3]], suffix=" / 3", at=0.2, tone="red",
                         width_of="3 / 3"),
                     {"type": "stamp", "text": "IT'S EXPECTATION", "tone": "red", "angle": -6, "size": 58, "x": 0.5, "y": 0.3, "at": 2.0, "sfx": "thud"}]})
# 6. payoff close: blame the party, not the pie; MYTH BUSTED
S.append({"say": "So the sugar rush? Mostly in the *grown-ups'* heads. Blame the *party*, not the pie.",
          "transition": "cut", "caption_y": 0.6,
          "layers": [plate("kit_cake", blur=10, keys=[{"t": 0, "scale": 1.3}, {"t": 5.0, "scale": 1.38}]),
                     close_ved([["explain", 0], ["point", 2.0], ["smirk", 3.6]]),
                     {"type": "optcard", "label": "the cause", "text": "SUGAR", "tone": "red", "x": 0.27, "y": 0.14,
                      "w": 0.37, "rotate": -3, "enter": "pop", "at": 0.2, "sfx": "pop", "verdict": "cross", "verdict_at": 0.5},
                     {"type": "optcard", "label": "the cause", "text": "PARTY", "tone": "green", "x": 0.71, "y": 0.14,
                      "w": 0.37, "rotate": 3, "enter": "pop", "at": 2.6, "sfx": "pop", "verdict": "tick", "verdict_at": 0.4},
                     sprite("cupcake", 0.84, 0.38, 0.16, at=1.0, sfx="pop", keys=[{"t": 0, "y": -0.1}, {"t": 0.5, "y": 0.38, "ease": "bounce"}]),
                     {"type": "stamp", "text": "MYTH BUSTED", "tone": "red", "angle": -6, "size": 62, "x": 0.27, "y": 0.29,
                      "at": 3.4, "sfx": "thud"}]})

SRC = ["https://pubmed.ncbi.nlm.nih.gov/8277950/", "https://pubmed.ncbi.nlm.nih.gov/7963081/",
       "https://uknowledge.uky.edu/psychology_facpub/13", "https://pubmed.ncbi.nlm.nih.gov/7474248/",
       "https://www.urmc.rochester.edu/news/publications/health-matters/does-halloween-candy-really-cause-a-sugar-rush",
       "https://www.eatright.org/health/wellness/healthful-habits/sugar-does-it-really-cause-hyperactivity"]
job = {"id": ID, "title": "Sugar makes kids hyper? Scientists tested it 🧁",
       "description": "Does sugar make kids hyper? In a 1994 double-blind study (New England Journal of Medicine), children lived "
                      "on three diets for three weeks each: high in sugar, or sweetened with aspartame or saccharin. Nobody knew "
                      "which diet was which. For the children their parents called sugar-sensitive, there was no difference on "
                      "39 behavior and thinking measures. Another 1994 study gave 35 boys a sugar-free drink and told half of "
                      "their mothers it was a big dose of sugar. Those mothers rated their sons as more hyperactive and stayed "
                      "physically closer to them. A 1995 JAMA meta-analysis of the research found that sugar does not affect "
                      "children's behavior or thinking. The likely real culprits: exciting parties and our own expectations. "
                      "(Sugar still matters for teeth and health; this is how the mind works, not medical advice.)\n\n"
                      "Sources: Wolraich et al., NEJM 1994; Hoover & Milich, Journal of Abnormal Child Psychology 1994; "
                      "Wolraich, Wilson & White, JAMA 1995.",
       "tags": ["sugar rush", "does sugar make kids hyper", "sugar hyperactivity myth", "placebo", "psychology",
                "expectation effect", "parenting", "myth busted", "science facts"],
       "hashtags": ["#psychology", "#science"],
       "instagram": {"hashtags": ["#psychology", "#sugarrush", "#mythbusting", "#parentingtips", "#explained"]},
       "meta": {"format": "myth-bust",
                "topic": "the sugar-hyperactivity myth: 1994 NEJM double-blind study, three 3-week diets (sugar / aspartame / "
                         "saccharin), no difference on 39 measures for 'sugar-sensitive' kids; Hoover & Milich 1994: 35 boys "
                         "all got a placebo, mothers told 'sugar' rated sons more hyperactive and stayed closer; JAMA 1995 "
                         "meta-analysis: no effect; it's the party and the expectation",
                "hook": "myth-bust",
                "idea_source": "trending + viral-shaped: Thanksgiving week in the US (most viewers) is peak 'sugar rush' talk; a "
                               "belief nearly every parent holds, busted by a sneaky placebo experiment; ideas.md backlog",
                "lane": "mind and psychology", "role": "chef", "explain": "myth vs fact",
                "styles": ["town", "blender", "RS-03", "hud", "cards"],
                "characters": ["ved", "extra"],
                "sources": SRC,
                "humour": {"trend": "Charlie Conspiracy (Always Sunny) evidence-board meme, rising on Imgflip in Nov 2026, "
                                    "as a text card only: \"mom's evidence board: cake -> chaos\"",
                           "beat": "side_eye", "scene": 4},
                "claims": [
                    {"claim": "1994 NEJM double-blind study: three consecutive 3-week diets (high sucrose / aspartame / saccharin)", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "no significant differences on 39 behavioral and cognitive measures for sugar-sensitive children", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "35 boys aged 5-7 all received a placebo (aspartame); half the mothers were told it was a large dose of sugar", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "those mothers rated their sons significantly more hyperactive and maintained physical closeness", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "1995 JAMA meta-analysis: sugar does not affect children's behavior or cognition", "tag": "PROVEN", "source": SRC[3]},
                    {"claim": "excitement of parties/holidays and expectations are the likely explanation", "tag": "THEORY", "source": SRC[4]}]},
       "thumbnail": {"title": "SUGAR *RUSH?*", "title_y": 0.2, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#3f7fbf", "#f4a6c0"], "tint_amount": 0.28,
                     "bg": [plate("kit_cake")],
                     "fg": [sprite("cupcake", 0.2, 0.47, 0.3, rotate=-8),
                            sprite("cup", 0.8, 0.45, 0.26, rotate=8),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
