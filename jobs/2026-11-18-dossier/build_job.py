"""DEMO 2026-11-18-dossier (private, not posted): the case-file pieces mixed into the house style (owner, 2026-11-18).
Learned from a reference documentary: noir desk cut by blind-stripe light, dot-matrix labels that decode, big serif numbers,
date/place stamps, numbered takeaways, day tiles, routes as gold arcs. Mixed with: Ved, a bright town beat, house captions,
the comic beat. Story = our own verified case (SEBI final order, 5 Feb 2026, Telegram stock tips in Unison Metals).
Run: python jobs/2026-11-18-dossier/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-18-dossier"
J = f"jobs/{ID}/"
A = J + "assets/"
M = "jobs/2026-11-08-m3/assets/"


def plate(path, blur=0, **k):
    return {"type": "image", "path": path + ".png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def close_ved(acting, x=0.5, y=0.8, h=1.06, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none", "acting": acting,
            "ground": False, "allow_outside_safe": True, **k}


BLINDS = {"type": "blinds", "angle": -34, "count": 8, "strength": 0.16, "shade": 0.12, "drift": 0.015}
S = []
S.append({"say": "February 2026. India's market regulator closes a case built on Telegram stock tips.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5, "zoom": 1.08, "focus": [0.48, 0.55]}]},
          "layers": [plate(A + "plate_desk_docs"),
                     {"type": "dateline", "date": "5 FEB 2026", "place": "Mumbai", "x": 0.36, "y": 0.27, "at": 0.1},
                     {"type": "dottext", "text": "SEBI FINAL ORDER", "size": 54, "x": 0.5, "y": 0.72, "at": 1.2}]})
S.append({"say": "Unlawful gains: four point two nine crore rupees.",
          "caption": "Unlawful gains: ₹4.29 crore.",
          "transition": "push", "transition_frames": 12,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.55]}, {"t": 4, "zoom": 1.12, "focus": [0.52, 0.6]}]},
          "layers": [plate(A + "plate_desk_phone"), dict(BLINDS),
                     {"type": "bignum", "text": "₹4.29 CRORE", "size": 100, "tone": "gold", "label": "UNLAWFUL GAINS",
                      "x": 0.5, "y": 0.27, "at": 0.2},
                     close_ved([["serious", 0], ["explain", 1.4]], x=0.82, y=0.93, h=0.58)]})
S.append({"say": "Seventeen people and firms were named, across the whole country.",
          "transition": "cut",
          "layers": [plate(A + "plate_desk_docs", blur=16, keys=[{"t": 0, "scale": 1.2}]),
                     {"type": "flows", "points": {"MUMBAI": [0.24, 0.62], "DELHI": [0.36, 0.3], "KOLKATA": [0.72, 0.44],
                                                  "AHMEDABAD": [0.18, 0.44], "CHENNAI": [0.5, 0.78], "JAIPUR": [0.28, 0.36]},
                      "routes": [["MUMBAI", "DELHI", 0.3], ["MUMBAI", "KOLKATA", 0.6], ["MUMBAI", "CHENNAI", 0.9],
                                 ["MUMBAI", "AHMEDABAD", 1.1], ["DELHI", "JAIPUR", 1.3]]},
                     {"type": "bignum", "value": 17, "size": 200, "label": "NAMED IN THE ORDER", "x": 0.5, "y": 0.24, "at": 0.1},
                     {"type": "tag", "text": "CITY DOTS: ILLUSTRATIVE", "x": 0.5, "y": 0.76, "at": 0.4, "size": 22}]})
# the bright town, with the case-file labels mixed in
st = Stage(M + "plate_market_wide.json")
p = st.place(1.0, -2.3, "ved")
S.append({"say": "Back in the real world, the tips looked like free advice in a group chat.",
          "transition": "dip", "transition_frames": 10, "look": "town",
          "layers": [plate(M + "plate_market_wide"),
                     {"type": "character", "id": "ved", "pose": "explain", "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
                      "acting": [["explain", 0], ["shrug", 2.2]], "allow_outside_safe": True},
                     {"type": "dottext", "text": "FREE TIP: *BUY NOW*", "size": 58, "x": 0.5, "y": 0.22, "at": 0.3, "accent": "red", "plate": True},
                     {"type": "tiles", "n": 5, "unit": "DAY", "progress": [[0.6, 1], [1.2, 2], [1.8, 3], [2.4, 4], [3.0, 5]],
                      "end": "SELL", "x": 0.5, "y": 0.34, "w": 0.7, "at": 0.4}]})
S.append({"dur": 1.6, "captions": False, "transition": "cut", "look": "town",
          "layers": [plate(M + "plate_market_mid", blur=12, keys=[{"t": 0, "scale": 1.3}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved", "text": "'free' tips, every single day:\n*hmm, who pays for this?*", "text_y": 0.2}})
S.append({"say": "Lesson one: paid stock tips need a SEBI registration. Check it.",
          "transition": "push", "transition_frames": 12,
          "layers": [plate(A + "plate_envelope"), dict(BLINDS, phase=0.3),
                     {"type": "tipnum", "n": 1, "title": "CHECK THE\nSEBI REG. NO.", "sub": "BEFORE YOU PAY ANYONE FOR A TIP",
                      "x": 0.42, "y": 0.26, "at": 0.1},
                     close_ved([["point", 0]], x=0.8, y=0.93, h=0.55)]})
S.append({"say": "The fine came later. The losses came first.",
          "transition": "cut", "min_dur": 3.0,
          "layers": [plate(A + "plate_cloche"), dict(BLINDS, phase=0.6),
                     {"type": "clock", "time": "11:15", "from": "09:15", "dur": 2.0, "label": "MARKET CLOSE", "x": 0.5, "y": 0.22,
                      "r": 0.16, "at": 0.1},
                     {"type": "dottext", "text": "PENALTY: *₹3.65 CR*", "size": 46, "x": 0.5, "y": 0.72, "at": 1.0, "accent": "gold"}]})

job = {"id": ID, "title": "DEMO case-file style", "description": "demo (not posted)", "tags": [], "privacy": "private",
       "speaker": "ved", "look": "night", "assets_script": J + "assets.py",
       "meta": {"format": "demo", "humour": {"beat": "side_eye", "scene": 4},
                "sources": ["https://www.sebi.gov.in/enforcement/orders/feb-2026/final-order-in-the-matter-of-stock-recommendation-tips-in-the-scrip-of-unison-metals-ltd-_99518.html",
                            "https://www.moneylife.in/article/telegram-stocktip-scam-in-unison-metals-busted-sebi-imposes-365-crore-penalty-on-17-including-2-promoters/79584.html"]},
       "music": {"cues": [{"scene": 0, "style": "doc", "key": "D", "scale": "minor", "bpm": 72}], "volume": 0.12},
       "scenes": S}
for sc in S:
    if "say" in sc:
        sc.setdefault("pad", 0.14)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
