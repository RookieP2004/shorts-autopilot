"""Load and validate the channel style, characters and a video job."""
import json
import os
import copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_STYLE = {
    "canvas": {"w": 1080, "h": 1920, "fps": 30},
    "palette": {"bg1": "#0f172a", "bg2": "#1e293b", "primary": "#f8fafc",
                "accent": "#facc15", "accent2": "#38bdf8", "danger": "#f43f5e",
                "ink": "#0b1020"},
    "background": {"type": "gradient", "colors": ["bg1", "bg2"], "angle": 160,
                   "pattern": "dots", "pattern_color": "#ffffff", "pattern_opacity": 0.05},
    "fonts": {"display": "fonts/Anton-Regular.ttf", "body": "fonts/Poppins-ExtraBold.ttf",
              "light": "fonts/Poppins-SemiBold.ttf"},
    "captions": {"enabled": True, "font": "body", "size": 76, "color": "primary",
                 "highlight": "accent", "stroke": "#000000", "stroke_width": 9,
                 "y": 0.45, "words_per_chunk": 3, "uppercase": True},
    "voice": {"voice": "am_michael", "speed": 1.05, "lang": "en-us"},
    "music": {"enabled": True, "style": "lofi", "key": "A", "scale": "minor", "bpm": 90,
              "progression": [1, 6, 3, 7], "volume": 0.16, "duck": 0.4, "seed": 7},
    "sfx": {"volume": 0.45},
    "transition": {"type": "slide_left", "frames": 8},
    "progress_bar": {"enabled": True, "color": "accent", "height": 10},
    "watermark": {"text": "", "size": 34, "opacity": 0.55, "y": 0.05},
    "grade": {"enabled": False, "shadows": "#1d4a52", "highlights": "#ffb36b", "strength": 0.12, "contrast": 1.06},
    "loudness_lufs": -14,
    "max_duration": 58,
    "safe_zone": {"top": 0.08, "bottom": 0.78, "left": 0.05, "right": 0.86},
    "scene_lead": 0.12,
    "scene_pad": 0.28,
    "youtube": {"categoryId": "24", "privacy": "public", "synthetic_media": False,
                "made_for_kids": False, "default_language": "en",
                "hashtags": ["#shorts"]},
}

ENTER = {"none", "pop", "fade", "slide_up", "slide_down", "slide_left", "slide_right",
         "zoom", "drop", "typewriter"}
LOOP = {"none", "bob", "pulse", "shake", "spin", "float", "wiggle"}
LAYER_TYPES = {"character", "text", "shape", "image", "counter", "scene3d"}
SHAPES3D = {"box", "sphere", "cylinder", "cone", "plane", "terrain", "person", "tree", "building"}
SHAPES = {"circle", "ring", "rect", "arrow", "line", "burst"}
TRANSITIONS = {"cut", "fade", "slide_left", "slide_up", "zoom", "flash"}
SFX = {"pop", "whoosh", "ding", "click", "boom", "riser", "scratch", "crickets", "wah", "none"}
# comedy beats: a short, unexpected moment (see docs/job-spec.md "Beats"). Defaults per kind.
BEATS = {
    "deadpan":    {"dur": 1.3, "sfx": "none",     "music": "cut",  "zoom": 1.55},   # flat stare at camera, arms cross
    "side_eye":   {"dur": 1.1, "sfx": "none",     "music": "cut",  "zoom": 1.55},   # slow side glance
    "smirk":      {"dur": 0.9, "sfx": "none",     "music": "keep", "zoom": 1.3},   # one brow up, half smile
    "freeze":     {"dur": 1.4, "sfx": "scratch",  "music": "cut",  "zoom": 1.05},   # freeze-frame, colour drains
    "zoom_punch": {"dur": 0.5, "sfx": "boom",     "music": "keep", "zoom": 1.28},   # hard snap zoom
    "silence":    {"dur": 1.4, "sfx": "crickets", "music": "cut",  "zoom": 1.0},    # awkward pause
}
FACE_BEATS = {"deadpan", "side_eye", "smirk"}


def scene_beats(s):
    out = list(s.get("beats", []))
    if s.get("beat"):
        out.insert(0, s["beat"])
    return out



def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_style(root=ROOT):
    p = os.path.join(root, "channel", "style.json")
    user = load_json(p) if os.path.exists(p) else {}
    return deep_merge(DEFAULT_STYLE, user)


def load_characters(root=ROOT):
    chars = {}
    base = os.path.join(root, "characters")
    if not os.path.isdir(base):
        return chars
    for cid in sorted(os.listdir(base)):
        d = os.path.join(base, cid)
        if not os.path.isdir(d):
            continue
        meta_p = os.path.join(d, "character.json")
        meta = load_json(meta_p) if os.path.exists(meta_p) else {}
        poses = sorted(f[:-4] for f in os.listdir(d) if f.endswith(".svg"))
        chars[cid] = {"id": cid, "dir": d, "meta": meta, "poses": poses}
    return chars


def color(style, c, default="#ffffff"):
    if c is None:
        c = default
    pal = style["palette"]
    seen = 0
    while isinstance(c, str) and c in pal and seen < 5:
        c = pal[c]
        seen += 1
    return c


def hex_rgba(c, alpha=1.0):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    a = int(c[6:8], 16) / 255 if len(c) == 8 else 1.0
    return (r, g, b, int(round(255 * a * alpha)))


def validate_job(job, style, chars, root=ROOT):
    """Return a list of problems (empty list = valid)."""
    errs = []
    for k in ("id", "title", "scenes"):
        if k not in job:
            errs.append(f"job missing '{k}'")
    if errs:
        return errs
    if len(job["title"]) > 100:
        errs.append("title longer than 100 chars")
    if len(job.get("description", "")) > 4800:
        errs.append("description too long")
    if not job["scenes"]:
        errs.append("no scenes")
    for i, s in enumerate(job["scenes"]):
        where = f"scene {i}"
        if not s.get("say") and not s.get("dur"):
            errs.append(f"{where}: needs 'say' or 'dur'")
        sp = s.get("speaker")
        if sp and sp not in chars:
            errs.append(f"{where}: speaker '{sp}' is not a character in characters/")
        bg = s.get("bg") or {}
        if bg.get("type") == "image" and not os.path.exists(os.path.join(root, bg.get("path", ""))):
            errs.append(f"{where}: background {bg.get('path')} not found")
        tr = s.get("transition")
        if tr and tr not in TRANSITIONS:
            errs.append(f"{where}: transition '{tr}' not in {sorted(TRANSITIONS)}")
        if s.get("sfx") and s["sfx"] not in SFX:
            errs.append(f"{where}: sfx '{s['sfx']}' not in {sorted(SFX)}")
        for b in scene_beats(s):
            if b.get("kind") not in BEATS:
                errs.append(f"{where}: beat kind '{b.get('kind')}' not in {sorted(BEATS)}")
            if b.get("sfx") and b["sfx"] not in SFX:
                errs.append(f"{where}: beat sfx '{b['sfx']}' not in {sorted(SFX)}")
            at = b.get("at", "after_say")
            if at != "after_say" and not isinstance(at, (int, float)):
                errs.append(f"{where}: beat 'at' must be seconds or \"after_say\"")
            if len(b.get("text", "")) > 60:
                errs.append(f"{where}: beat text over 60 characters - keep it punchy")
        for j, L in enumerate(s.get("layers", [])):
            w = f"{where} layer {j}"
            t = L.get("type")
            if t not in LAYER_TYPES:
                errs.append(f"{w}: type '{t}' not in {sorted(LAYER_TYPES)}")
                continue
            if L.get("enter", "none") not in ENTER:
                errs.append(f"{w}: enter '{L['enter']}' not in {sorted(ENTER)}")
            if L.get("loop", "none") not in LOOP:
                errs.append(f"{w}: loop '{L['loop']}' not in {sorted(LOOP)}")
            sz = style.get("safe_zone", {})
            if L.get("y", 0.5) > sz.get("bottom", 0.78) and not L.get("allow_outside_safe"):
                errs.append(f"{w}: y={L.get('y')} is under YouTube's Shorts UI (keep y <= {sz.get('bottom')}, "
                            f"or set allow_outside_safe)")
            if t == "character":
                cid = L.get("id")
                if cid not in chars:
                    errs.append(f"{w}: character '{cid}' not found")
                else:
                    pose = L.get("pose", "idle")
                    if pose not in chars[cid]["poses"]:
                        errs.append(f"{w}: pose '{pose}' missing for '{cid}' "
                                    f"(has {chars[cid]['poses']})")
            elif t == "text" and not L.get("text"):
                errs.append(f"{w}: text layer needs 'text'")
            elif t == "shape" and L.get("shape") not in SHAPES:
                errs.append(f"{w}: shape '{L.get('shape')}' not in {sorted(SHAPES)}")
            elif t == "image":
                if not L.get("svg") and not L.get("path"):
                    errs.append(f"{w}: image needs 'svg' (inline) or 'path'")
                elif L.get("path") and not os.path.exists(os.path.join(root, L["path"])):
                    errs.append(f"{w}: file {L['path']} not found")
            elif t == "scene3d":
                for k, o in enumerate(L.get("objects", [])):
                    if o.get("shape", "box") not in SHAPES3D:
                        errs.append(f"{w}: 3D object {k} shape '{o.get('shape')}' not in {sorted(SHAPES3D)}")
                if not L.get("objects"):
                    errs.append(f"{w}: scene3d needs 'objects'")
            elif t == "counter" and "to" not in L:
                errs.append(f"{w}: counter needs 'to'")
    return errs
