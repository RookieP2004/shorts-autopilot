"""'Same wave' v2: Ved hosts in the night kitchen, cut with 3D shots of the wave (rendered from the owner's private
Cutaway install; only the rendered clips live here). Short cuts every 2-5 s, one continuous camera inside each 3D shot.
Sound is mixed afterwards by mix.py (voice first, quiet score, few placed sounds), so the renderer makes the voice only."""
import json, os, sys

ID = "2026-11-22-m1"
A = f"jobs/{ID}/assets/"
ONLY_VED = "--ved" in sys.argv


def ved(pose, x, y, h, acting, keys=None, flip=False, **kw):
    L = {"type": "character", "id": "ved", "pose": pose, "x": x, "y": y, "h": h, "enter": "none", "acting": acting,
         "ground": False, "allow_outside_safe": True, "rim": ["#f2b04a", "#3a6fb0"]}
    if keys:
        L["keys"] = keys
    if flip:
        L["flip"] = True
    L.update(kw)
    return L


def plate(name, blur, s0, s1, dur, fx=0.5, fy=0.5):
    return {"type": "image", "path": A + name, "x": fx, "y": fy, "w": 1.0, "enter": "none", "blur": blur,
            "keys": [{"t": 0, "scale": s0}, {"t": dur, "scale": s1}]}


def clip(name, frm, speed):
    return {"type": "video", "path": A + name, "x": 0.5, "y": 0.5, "w": 1, "h": 1, "at": 0, "from": frm, "speed": speed,
            "sfx": "none", "enter": "none"}


def push(z0, z1, dur, f0=(0.5, 0.5), f1=(0.5, 0.5)):
    return {"keys": [{"t": 0, "zoom": z0, "focus": list(f0)}, {"t": dur, "zoom": z1, "focus": list(f1)}]}


S = []
# 1. HOOK - Ved walks into the dark kitchen and points up at the router on the shelf
S.append({"name": "hook", "say": "Your Wi-Fi router fires *microwaves.*", "pad": 0.15, "camera": push(1.0, 1.06, 3.0, (0.5, 0.5), (0.58, 0.45)),
          "layers": [plate("plate_kitchen.png", 2.5, 1.04, 1.08, 3.0),
                     ved("explain", 0.0, 0.83, 0.84, [["explain", 0], ["point", 0.75]], flip=True,
                         keys=[{"t": 0, "x": 0.02}, {"t": 0.7, "x": 0.3, "walk": True}])]})
# 2. 3D: the wave leaves the router and crosses the kitchen into the oven
S.append({"name": "same", "say": "The same wave your oven uses to boil *water.*", "pad": 0.12, "captions": True,
          "layers": [clip("shot_router_wave.mp4", 1.6, 0.95)]})
# 3. Ved close-up: the shrug
S.append({"name": "why", "say": "So... why aren't you *cooking?*", "pad": 0.3, "camera": push(1.0, 1.05, 2.0),
          "layers": [plate("plate_oven.png", 9, 1.35, 1.4, 2.0),
                     ved("shrug", 0.5, 0.82, 1.06, [["side_eye", 0], ["shrug", 0.55]])]})
# 4. 3D: the router's tiny power, 0.1 W
S.append({"name": "power", "say": "Power. Your router *whispers* a tenth of a watt.", "pad": 0.1,
          "layers": [clip("shot_router_power.mp4", 0.0, 0.74)]})
# 5-6. 3D: the oven, 1,000 W ... then 10,000x lands on the cut
S.append({"name": "shouts", "say": "But the oven *shouts* a thousand watts.", "pad": 0.05,
          "layers": [clip("shot_oven.mp4", 0.0, 0.54)]})
S.append({"name": "ten", "say": "*Ten thousand* times more.", "lead": 0.05, "pad": 0.25,
          "layers": [clip("shot_oven.mp4", 1.52, 0.95)]})
# 7. Ved beside the oven: sealed box, then he walks out of shot
S.append({"name": "box", "say": "Into a sealed metal *box.* And it can't *escape.*", "pad": 0.75, "camera": push(1.0, 1.05, 4.0, (0.5, 0.5), (0.42, 0.5)),
          "layers": [plate("plate_oven.png", 2.5, 1.04, 1.07, 4.0),
                     ved("explain", 0.72, 0.83, 0.84, [["explain", 0], ["point", 0.25], ["serious", 2.0]],
                         keys=[{"t": 0, "x": 0.72}, {"t": 3.25, "x": 0.72}, {"t": 4.1, "x": 1.3, "walk": True}])]})
# 8. 3D: the door's metal screen, holes 1 mm vs the 12 cm wave
S.append({"name": "holes", "say": "The door's holes are a *millimetre.* The wave? *Twelve* centimetres.", "pad": 0.15,
          "layers": [clip("shot_door.mp4", 0.0, 0.91)]})
# 9. 3D: through the door, trapped, 2.45 billion flips a second
S.append({"name": "flips", "say": "Trapped, it flips back and forth, two and a half *billion* times a second.", "pad": 0.12,
          "layers": [clip("shot_inside.mp4", 0.0, 0.92)]})
# 10. 3D: the water molecules can't keep up -> heat
S.append({"name": "water", "say": "Water molecules try to turn with it. They can't keep up. That struggle is *heat.*", "pad": 0.2,
          "layers": [clip("shot_molecules.mp4", 0.0, 1.0)]})
# 11. PAYOFF - Ved back in the kitchen, Wi-Fi bubble behind him; points router, then oven; walks off
S.append({"name": "end", "say": "Same wave. One *whispers.* One *shouts.*", "pad": 0.55, "camera": push(1.0, 1.05, 3.4),
          "layers": [plate("plate_wifi.png", 2.5, 1.04, 1.08, 3.4),
                     ved("warm", 0.4, 0.83, 0.84, [["warm", 0], ["explain", 0.9], ["point", 1.75], ["smirk", 2.6]],
                         keys=[{"t": 0, "x": 0.4}, {"t": 2.85, "x": 0.4}, {"t": 3.4, "x": 0.75, "walk": True}])]})

for s in S:
    s.setdefault("transition", "cut")
    s["sfx"] = "none"

if ONLY_VED:
    S = [s for s in S if s["name"] in ("hook", "why", "box", "end")]

job = {
    "id": ID,
    "title": "Your Wi-Fi router fires MICROWAVES 📶",
    "description": ("Wi-Fi and microwave ovens both use the 2.4 GHz band. So why doesn't your router cook you? Power: an oven "
                    "pumps roughly 1,000 watts into a sealed metal box, while a Wi-Fi router is capped at about 0.1 watt, spread "
                    "through your house. The wave is ~12 cm long and the holes in the door screen ~1 mm, so it stays inside, "
                    "flipping 2.45 billion times a second; water molecules try to turn with it, and that jostling is heat.\n\n"
                    "Sources: Illinois Physics Van (door screen); FCC Part 15 power limits; Physics Forums summary (oven vs router power)."),
    "tags": ["wifi", "microwave", "microwave oven", "how microwaves work", "2.4 ghz", "wifi router", "physics", "science explained"],
    "hashtags": ["#physics", "#wifi"],
    "meta": {"format": "big-question", "topic": "why Wi-Fi doesn't cook you though microwave ovens use the same band",
             "hook": "contradiction", "idea_source": "owner showcase (manual)", "characters": ["ved"],
             "overrides": "documentary edit: Cutaway 3D shots between Ved's kitchen shots; captions 2 words, low; sound mixed by hand",
             "sources": ["https://van.physics.illinois.edu/", "https://www.fcc.gov/"]},
    "speaker": "ved",
    "music": {"enabled": False},
    "style_override": {"sfx": {"auto": False}, "scene_pad": 0.2,
                       "captions": {"y": 0.7, "words_per_chunk": 2, "uppercase": False, "size": 80, "stroke_width": 10}},
    "instagram": {"hashtags": ["#science", "#wifi", "#microwave", "#physics", "#explained"]},
    "thumbnail": {"title": "WI-FI = *MICROWAVES*", "title_y": 0.2, "title_size": 140, "max_w": 0.95, "blur": 10,
                  "glow": "#ffb45a", "glow_x": 0.3, "glow_y": 0.62, "glow_strength": 1.2, "bg_saturation": 1.2,
                  "tint": ["#2f6fe0", "#f08a24"], "tint_amount": 0.2,
                  "bg": [{"type": "image", "path": A + "plate_wifi.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": 0}],
                  "fg": [{"type": "character", "id": "ved", "pose": "surprised", "x": 0.62, "y": 0.95, "h": 0.95, "enter": "none",
                          "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True, "rim": ["#f2b04a", "#3a6fb0"]}]},
    "scenes": S,
}
out = f"jobs/{ID}/job{'_ved' if ONLY_VED else ''}.json"
json.dump(job, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(S), "scenes")
