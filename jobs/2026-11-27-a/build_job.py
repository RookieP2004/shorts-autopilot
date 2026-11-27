"""2026-11-27-a: "Where do your returns go?" (scale-shock; Detective Ved tails one returned box). Black Friday.
Lane: dark side of the real world (the hidden returns economy). Explain mode: case file / follow the item.
Styles mixed: animated Blender shots (moving 3D: a camera rising over a mountain of returned boxes, a box riding the
roller conveyor, boxes dropping onto a liquidation pallet, boxes tumbling into a skip), the returns warehouse plates with
Detective Ved and a warehouse worker, a Reelsmith RS-01 Receipt, hud chips, stamps, the comic beat.
Facts (verified 2026-11-27):
- NRF + Happy Returns 2025 Retail Returns Landscape: 15.8% of 2025 sales returned, $849.9 billion; 9% of all returns are
  fraudulent. (nrf.com press release, Oct 2025)
- NPR (2022): experts estimate retailers throw away about a quarter of returns; Optoro estimates US returns create almost
  6 billion pounds of landfill waste a year; many returns are resold to middlemen (auction platforms like B-Stock); the
  deciding question is whether the item is worth the cost of shipping + inspecting, cleaning, repairing, testing.
- Mental Floss (2024): an Amazon exec: once the seal is broken it's not going back to the shelf; returns go to
  liquidators, outlets, thrift stores, resellers.
Run after the assets exist: python jobs/2026-11-27-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-27-a"
J = f"jobs/{ID}/"
A = J + "assets/"
SH = J + "shots/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("wh_wide", "wh_low", "wh_table")}
BADGE = {"wear": "badge"}
OUT = {"dana": {"skin": "#8d5a3b", "build": "regular", "hair": ["#1a1410", "bun"], "hat": ["cap", "#f2b04a"],
                "top": ["#f28c28", "vest"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b"}}


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


def hud(label, text, tone, at=0.4):
    return {"type": "hud", "label": label, "text": text, "x": 0.5, "y": 0.13, "at": at, "enter": "pop", "sfx": "click", "tone": tone}


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


def person(set_, who, wx, wy, acting, walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"],
         "enter": "none", "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


S = []
# 0. hook (moving 3D): rise over a mountain of returned boxes; the number at frame 0
S.append({"say": "Americans sent back *850 billion dollars* of stuff in one year.",
          "layers": [shot("a_hook.py", 4.8),
                     txt("*850 BILLION* DOLLARS SENT BACK", 0.15, 96, enter="none")]})
# 1. warehouse wide: Detective Ved walks in (badge), Dana the worker by the conveyor
S.append({"say": "Where does it go? I tailed one box.",
          "transition": "slide_left", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.07, "focus": [0.5, 0.5]}]},
          "layers": [plate("wh_wide"),
                     person("wh_wide", "dana", 1.1, 1.0, [["idle", 0], ["hold", 1.0]]),
                     ved("wh_wide", -0.6, -0.3, [["idle", 0], ["think", 1.2]],
                         walk=[(0, -2.2, -0.3), (1.1, -0.6, -0.3)], rig_args=BADGE)]})
# 2. moving 3D: the box rides the conveyor
S.append({"say": "It rides back to a warehouse to get *checked*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("b_belt.py", 3.6), hud("step 1", "INSPECTION", "blue")]})
# 3. RS-01 Receipt: what it costs to resell
S.append({"say": "Shipping, checking, cleaning, repacking. Often it costs *more* than it's worth.",
          "transition": "zoom", "caption_y": 0.74, "pad": 0.8,
          "layers": [plate("wh_table", blur=14, keys=[{"t": 0, "scale": 1.1}, {"t": 5.0, "scale": 1.18}]),
                     {"type": "look", "look": "RS-01", "x": 0.5, "y": 0.42, "w": 0.9, "h": 0.6, "at": 0.0,
                      "props": {"title": "COST TO RESELL", "subtitle": "one $15 return",
                                "items": [["Shipping back", 8], ["Inspection", 4], ["Clean + repack", 5]], "currency": "$",
                                "total_label": "TOTAL", "note": "ILLUSTRATIVE"}}]})
# 4. table close: the opened box; Ved with the magnifier
S.append({"say": "Seal broken? It rarely goes back on the shelf as *new*.",
          "transition": "cut", "caption_y": 0.72,
          "layers": [plate("wh_table", keys=[{"t": 0, "scale": 1.0}, {"t": 3.2, "scale": 1.06}]),
                     dict(close_ved([["explain", 0], ["point", 1.2]]), x=0.72, y=1.0, h=0.7),
                     {"type": "stamp", "text": "NOT NEW", "tone": "red", "angle": -7, "size": 70, "x": 0.4, "y": 0.18,
                      "at": 1.6, "sfx": "thud"}]})
# 5. moving 3D: liquidation pallet
S.append({"say": "So lots get *auctioned off* in bulk to resellers.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("c_pallet.py", 3.6), hud("liquidation", "SOLD BY THE PALLET", "gold")]})
# 6. moving 3D: into the skip
S.append({"say": "About a *quarter*? Tossed. Nearly *6 billion pounds* a year.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("d_dump.py", 4.4), hud("landfill, est.", "~6 BILLION LB / YEAR", "red", at=1.4)]})
# 7. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("wh_table", blur=10, keys=[{"t": 0, "scale": 1.2}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "the box: \"I was promised a *shelf*\"", "text_y": 0.2, "sfx": "scratch"}})
# 8. low angle: fraud
S.append({"say": "And retailers say *9 percent* of returns? Fraud.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.72,
          "layers": [plate("wh_low"),
                     person("wh_low", "dana", 1.4, 1.6, [["surprised", 0.6]]),
                     ved("wh_low", 0.1, 0.4, [["serious", 0], ["point", 1.0]]),
                     hud("NRF 2025", "9% FRAUD", "red", at=0.8)]})
# 9. payoff, wide: case closed
S.append({"say": "Case closed. A *free* return is never really free.",
          "transition": "cut", "caption_y": 0.72, "pad": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("wh_wide"),
                     person("wh_wide", "dana", 1.1, 1.0, [["shrug", 0]]),
                     ved("wh_wide", -0.6, -0.3, [["explain", 0], ["smirk", 2.0]], rig_args=BADGE),
                     {"type": "stamp", "text": "CASE CLOSED", "tone": "green", "angle": -6, "size": 70, "x": 0.5, "y": 0.2,
                      "at": 0.5, "sfx": "thud"}]})

SRC = ["https://nrf.com/media-center/press-releases/consumers-expected-to-return-nearly-850-billion-in-merchandise-in-2025",
       "https://www.npr.org/2022/01/12/1072066943/from-living-rooms-to-landfills-some-holiday-shopping-returns-take-a-very-sad-path",
       "https://www.mentalfloss.com/culture/business/where-online-shopping-returns-go"]
job = {"id": ID, "title": "Where do your returns actually go? 📦",
       "description": "Americans sent back about $850 billion of merchandise in 2025 (NRF), roughly 16% of everything "
                      "bought. Each return has to be shipped back, inspected, cleaned and repacked, which often costs more "
                      "than the item is worth. Opened items rarely go back on the shelf as new; many are sold in bulk to "
                      "liquidators and resellers, and experts estimate about a quarter are thrown away, nearly 6 billion "
                      "pounds of landfill a year (Optoro estimate). Retailers say 9% of returns are fraudulent. The receipt "
                      "costs in the video are illustrative.\n\n"
                      "Sources: National Retail Federation & Happy Returns, 2025 Retail Returns Landscape; NPR; Mental Floss.",
       "tags": ["returns", "Black Friday", "online shopping", "where do returns go", "retail", "landfill", "free returns",
                "money", "explained"],
       "hashtags": ["#blackfriday", "#shopping"],
       "instagram": {"hashtags": ["#money", "#blackfriday", "#onlineshopping", "#returns", "#explained"]},
       "meta": {"format": "scale-shock",
                "topic": "where returns go: US returns ~$850B in 2025 (NRF, 15.8% of sales); shipping + inspection + cleaning "
                         "often costs more than the item; opened items rarely resold as new; liquidated in bulk; ~a quarter "
                         "thrown away, ~6B lb landfill/yr (Optoro est.); 9% of returns fraudulent (NRF)",
                "hook": "number-shock",
                "idea_source": "trending + unique: posted on Black Friday (most viewers are American, the biggest shopping "
                               "and returns season), wallet-first, a hidden economy few Shorts follow end to end; lane dark side",
                "lane": "dark side of the real world", "role": "detective", "explain": "case file (follow one item)",
                "role_visual": "Detective Ved with a badge and a gold magnifier at an inspection table with a case-file folder "
                               "in the returns warehouse; he 'tails' one box and stamps CASE CLOSED",
                "styles": ["blender-3d", "warehouse", "RS-01", "hud", "stamp", "comic"],
                "characters": ["ved", "extra"],
                "sources": SRC,
                "humour": {"trend": "timeless dry card (this week's rising US memes didn't fit the topic cleanly): "
                                    "the box: \"I was promised a shelf\"",
                           "beat": "deadpan", "scene": 7},
                "claims": [
                    {"claim": "US consumers returned about $850B (15.8% of sales) in 2025", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "9% of all returns are fraudulent (retailer survey)", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "processing a return can cost more than the item is worth", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "opened items rarely go back on the shelf as new", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "many returns are sold in bulk to liquidators/resellers", "tag": "PROVEN", "source": SRC[1]},
                    {"claim": "about a quarter of returns are thrown away; ~6 billion lb landfill a year", "tag": "THEORY (expert / Optoro estimate)", "source": SRC[1]},
                    {"claim": "receipt costs ($8/$4/$5 for a $15 item)", "tag": "ILLUSTRATIVE", "source": SRC[1]}]},
       "thumbnail": {"title": "WHERE'S MY *RETURN?*", "title_y": 0.2, "title_size": 150, "max_w": 0.95, "blur": 14,
                     "glow": "#f2b04a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.2, "bg_saturation": 1.3,
                     "tint": ["#1c3f73", "#e0702e"], "tint_amount": 0.22,
                     "bg": [plate("wh_wide")],
                     "fg": [sprite("returnbox", 0.26, 0.48, 0.42, rotate=-8),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.62, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
