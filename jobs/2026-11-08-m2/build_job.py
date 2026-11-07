"""Writes job.json for the v2 money video (Rick's Clips-style: 2D Ved acting inside 3D sets made of rendered stills + cut-outs)."""
import json, math, random
random.seed(7)
A = "jobs/2026-11-08-m2/assets/"
def plate(name, blur=0, **k):
    return {"type": "image", "path": A + name + ".png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}
def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}
def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}
def ved(x, y, h, acting, keys=None, hops=None, **k):
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none", "acting": acting}
    if keys: L["keys"] = keys
    if hops: L["hops"] = hops
    L.update(k)
    return L
def drop(name, x, y, w, t0, fall=0.55, from_y=-0.15, spin=0, **k):
    """A cut-out that falls into place and bounces."""
    return sprite(name, x, y, w, at=t0, keys=[{"t": 0, "y": from_y, "rot": spin}, {"t": fall, "y": y, "rot": 0, "ease": "bounce"}], **k)
def fly(name, x0, y0, x1, y1, w, t0, dur=0.9, rot0=0, rot1=200, arc=0.12, **k):
    """A cut-out flying along an arc (via a mid key) with spin, then gone."""
    xm, ym = (x0 + x1) / 2, min(y0, y1) - arc
    return sprite(name, x0, y0, w, at=t0, until=t0 + dur, exit="fade", exit_dur=0.1,
                  keys=[{"t": 0, "x": x0, "y": y0, "rot": rot0, "scale": 0.4},
                        {"t": dur * 0.45, "x": xm, "y": ym, "rot": (rot0 + rot1) / 2, "scale": 1.0, "ease": "out"},
                        {"t": dur, "x": x1, "y": y1, "rot": rot1, "scale": 1.1, "ease": "in"}], **k)

S = []
# 1. medium: Ved walks in from the right and asks
S.append({"say": "Hey! Ever wondered why a country can't just *print more money*?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.08, "focus": [0.54, 0.5]}]},
          "layers": [plate("plate_market_mid"),
                     txt("WHY NOT JUST *PRINT MORE MONEY?*", 0.17, 92, enter="none"),
                     ved(0.62, 0.66, 0.42, [["warm", 0], ["explain", 1.3], ["point", 2.6]],
                         keys=[{"t": 0, "x": 1.18}, {"t": 1.15, "x": 0.62, "walk": True}])]})
# 2. close-up on Ved
S.append({"say": "I mean, free money for everyone. What could go *wrong*?", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("plate_market_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3, "scale": 1.42}]),
                     ved(0.5, 0.8, 1.06, [["explain", 0], ["welcome", 1.4], ["smirk", 2.5]], ground=False, allow_outside_safe=True)]})
# 3. counter close-up: ten apples drop in
apples = []
for i in range(10):
    row, col = divmod(i, 5)
    x = 0.2 + col * 0.15 + (0.075 if row else 0)
    y = 0.47 - row * 0.045
    apples.append(drop("apple", x, y, 0.13 - row * 0.012, 0.25 + i * 0.13, spin=random.uniform(-40, 40),
                       sfx="pop" if i % 3 == 0 else "none"))
apples.sort(key=lambda L: L["y"])          # back row first
S.append({"say": "Picture a tiny island with just *ten apples*...", "transition": "slide_left", "caption_y": 0.27,
          "camera": {"zoom": [1.0, 1.06], "focus": [0.5, 0.5]},
          "layers": [plate("plate_market_close")] + apples + [txt("10 APPLES", 0.12, 110, enter="pop", at=1.7, sfx="ding")]})
# 4. medium: the $10 stack lands, Ved points
row_apples = sorted([sprite("apple", 0.54 + (i % 5) * 0.075 + (0.035 if i >= 5 else 0), 0.507 - (i // 5) * 0.022, 0.072) for i in range(10)], key=lambda L: L["y"])
S.append({"say": "...and *ten dollars*. So one apple costs one dollar.", "transition": "cut",
          "layers": [plate("plate_market_mid")] + row_apples + [
                     drop("stack10", 0.36, 0.515, 0.2, 0.3, fall=0.5, from_y=-0.1, sfx="pop"),
                     txt("*$10*", 0.12, 130, enter="pop", at=0.4),
                     txt("1 APPLE = *$1*", 0.21, 84, enter="slide_up", at=2.2, sfx="pop"),
                     ved(0.2, 0.68, 0.42, [["explain", 0], ["point", 0.5], ["warm", 2.4]])]})
# 5. bank: Ved walks to the printer, it prints, he jumps
bills = [fly("bill", 0.5, 0.6, random.uniform(0.15, 0.95), random.uniform(1.05, 1.15), 0.2, 1.4 + k * 0.17,
             dur=random.uniform(0.8, 1.1), rot0=random.uniform(-30, 30), rot1=random.uniform(-260, 260), arc=random.uniform(0.15, 0.3))
         for k in range(12)]
S.append({"say": "Now the government prints ten more dollars.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 1.3, "zoom": 1.1, "focus": [0.5, 0.5]}]},
          "layers": [plate("plate_bank"),
                     sprite("printer", 0.55, 0.6, 0.52, loop="shake", loop_amp=0.5, at=0.0)] + bills + [
                     txt("*+$10* PRINTED", 0.29, 96, enter="pop", at=1.3, sfx="boom"),
                     ved(0.22, 0.7, 0.4, [["warm", 0], ["point", 1.2], ["surprised", 1.6]],
                         keys=[{"t": 0, "x": -0.2}, {"t": 1.0, "x": 0.2, "walk": True}], hops=[[1.5, 0.05, 0.45]])]})
# 6. medium: bills rain on the counter, Ved reacts, 2D panel
rain = [drop("bill", random.uniform(0.28, 0.46), random.uniform(0.49, 0.52), 0.13, 0.2 + k * 0.14, fall=0.6,
             spin=random.uniform(-200, 200), from_y=-0.1) for k in range(10)]
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
panel = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 330'><rect width='900' height='330' rx='34' fill='#f6efe2'/>
<rect width='900' height='330' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>
<g transform='translate(70,70)'><rect width='120' height='62' rx='8' fill='#cfe3c6' stroke='#265c40' stroke-width='5'/><circle cx='60' cy='31' r='16' fill='none' stroke='#265c40' stroke-width='5'/></g>
<text x='230' y='120' font-size='60' fill='#1a1410' {F}>MONEY</text><text x='500' y='122' font-size='74' fill='#1a1410' {AN}>$10</text>
<path d='M615,100 L660,100 L660,86 L685,108 L660,130 L660,116 L615,116 Z' fill='#f2b04a'/><text x='705' y='122' font-size='74' fill='#d98a1a' {AN}>$20</text>
<line x1='60' y1='168' x2='840' y2='168' stroke='#1a1410' stroke-width='3' opacity='0.25'/>
<g transform='translate(100,205)'><circle cx='30' cy='42' r='38' fill='#c0212a'/><path d='M30,6 C28,-6 34,-14 40,-16' stroke='#4a3220' stroke-width='6' fill='none' stroke-linecap='round'/><ellipse cx='50' cy='-4' rx='18' ry='8' fill='#3f8a3a'/></g>
<text x='230' y='268' font-size='60' fill='#1a1410' {F}>APPLES</text><text x='515' y='270' font-size='74' fill='#1a1410' {AN}>10</text>
<path d='M615,248 L660,248 L660,234 L685,256 L660,278 L660,264 L615,264 Z' fill='#9aa3ab'/><text x='720' y='270' font-size='74' fill='#1a1410' {AN}>10</text></svg>"""
S.append({"say": "Everyone feels richer. But look... there are still only *ten apples*.", "transition": "zoom",
          "layers": [plate("plate_market_mid")] + row_apples + [sprite("stack10", 0.36, 0.515, 0.2)] + rain + [
                     {"type": "image", "svg": panel, "w": 0.82, "x": 0.5, "y": 0.17, "enter": "pop", "at": 1.6, "sfx": "pop"},
                     ved(0.82, 0.68, 0.42, [["surprised", 0], ["think", 1.9], ["point", 3.0]], hops=[[0.25, 0.04, 0.4]])]})
# 7. counter close-up: the tag flips $1 -> $2
S.append({"say": "So the seller raises the price. Each apple now costs *two dollars*. That's *inflation*.", "transition": "cut",
          "caption_y": 0.27, "camera": {"zoom": [1.0, 1.08], "focus": [0.5, 0.5], "punch": [4.2]},
          "layers": [plate("plate_market_close"),
                     sprite("apple", 0.38, 0.5, 0.3),
                     sprite("tag_1", 0.7, 0.45, 0.34, keys=[{"t": 0, "sx": 1, "rot": -4}, {"t": 2.35, "sx": 1, "rot": -4},
                                                              {"t": 2.55, "sx": 0.0, "rot": 0, "ease": "in"}], until=2.55, exit_dur=0.01),
                     sprite("tag_2", 0.7, 0.45, 0.34, at=2.55, keys=[{"t": 0, "sx": 0.0, "scale": 1.2},
                                                              {"t": 0.22, "sx": 1.0, "scale": 1.2, "ease": "out"},
                                                              {"t": 0.6, "sx": 1.0, "scale": 1.0, "ease": "back"}], sfx="whoosh"),
                     txt("*INFLATION*", 0.13, 150, enter="zoom", at=4.1, sfx="boom")]})
# 8. comic beat: Ved close, deadpan
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("plate_market_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]),
                     dict(ved(0.5, 0.8, 1.06, [["idle", 0]], ground=False, allow_outside_safe=True), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.5, "zoom": 1.15, "focus": [0.5, 0.42],
                   "text": "The printer: \"I'm the birthday.\"\nPrices: *\"Me too.\"*", "text_y": 0.18}})
# 9. vault: Ved walks in under the giant note, notes rain
vrain = [sprite("bill_100t", random.uniform(0.05, 0.95), 0.0, random.uniform(0.09, 0.14), at=random.uniform(0, 3.5),
                keys=[{"t": 0, "y": -0.08, "rot": random.uniform(0, 360)},
                      {"t": random.uniform(2.5, 3.6), "y": 1.1, "rot": random.uniform(200, 700), "ease": "linear"}],
                opacity=0.9) for _ in range(16)]
S.append({"say": "Zimbabwe actually tried this. In 2008, prices *doubled* about every single day...", "transition": "fade",
          "caption_y": 0.6,
          "layers": [plate("plate_vault")] + vrain + [
                     sprite("note_100t", 0.5, 0.36, 0.86, enter="zoom", at=0.2, loop="float", loop_amp=0.8),
                     txt("ZIMBABWE, 2008", 0.11, 100, enter="pop", at=0.3, sfx="pop"),
                     ved(0.74, 0.72, 0.34, [["warm", 0], ["explain", 1.6], ["serious", 3.4]],
                         keys=[{"t": 0, "x": 1.2}, {"t": 1.3, "x": 0.74, "walk": True}])]})
# 10. closer on the note: Ved jumps back
S.append({"say": "...and it printed a *one hundred trillion* dollar note.", "transition": "cut", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.15, "focus": [0.5, 0.38]}, {"t": 3.0, "zoom": 1.32, "focus": [0.45, 0.36]}]},
          "layers": [plate("plate_vault")] + vrain[:8] + [
                     sprite("note_100t", 0.5, 0.36, 0.86, loop="float", loop_amp=0.8),
                     {"type": "counter", "from": 1, "to": 100000000000000, "count_dur": 1.6, "at": 0.9, "x": 0.5, "y": 0.13,
                      "size": 92, "stroke": "#0b0f12", "stroke_width": 6, "enter": "pop"},
                     ved(0.76, 0.74, 0.34, [["surprised", 0], ["surprised", 1.0]], hops=[[1.0, 0.05, 0.45]])]})
# 11. medium: money is a ticket
S.append({"say": "See, money isn't wealth. It's a *ticket* for the stuff we make.", "transition": "slide_left",
          "layers": [plate("plate_market_mid")] + row_apples + [sprite("stack10", 0.36, 0.515, 0.2),
                     txt("MONEY = A *TICKET*", 0.13, 104, enter="pop", at=1.6, sfx="pop"),
                     txt("NOT THE *STUFF*", 0.22, 88, enter="pop", at=2.9),
                     ved(0.24, 0.68, 0.42, [["explain", 0], ["point", 1.8], ["warm", 3.2]],
                         keys=[{"t": 0, "x": 0.12}, {"t": 0.9, "x": 0.24, "walk": True}])]})
# 12. close: payoff
S.append({"say": "Print more tickets... and each one *buys less*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("plate_market_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3, "scale": 1.4}]),
                     ved(0.5, 0.8, 1.06, [["explain", 0], ["crossed", 1.9]], ground=False, allow_outside_safe=True)]})

job = {"id": "2026-11-08-m2", "title": "Why can't we just print more money? 💸",
       "description": "Ten apples, ten dollars, and a money printer: the simplest way to understand inflation, and what happened when Zimbabwe tried it.\n\nSources: Hanke & Kwok, Cato Journal (2009); Reserve Bank of Zimbabwe Z$100 trillion note, Jan 2009.",
       "tags": ["inflation", "economics", "money", "print money", "zimbabwe", "hyperinflation", "explained", "economy"],
       "hashtags": ["#economics", "#inflation"],
       "meta": {"format": "big-question", "topic": "why printing money causes inflation", "hook": "question",
                "idea_source": "owner (manual)", "characters": ["ved"],
                "sources": ["https://www.cato.org/publications/commentary/inflation-inferno-roared-away-until-mid-november-2008"],
                "humour": {"trend": "'you the birthday' (TikTok slang, this week)", "beat": "deadpan", "scene": 7},
                "overrides": "style test v2: 2D Ved acting inside 3D sets built from Blender stills + cut-outs"},
       "privacy": "private", "speaker": "ved", "assets_script": "jobs/2026-11-08-m2/assets.py", "scenes": S}
json.dump(job, open("jobs/2026-11-08-m2/job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
