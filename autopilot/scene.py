"""Draw one frame of one scene. Pure function of (scene, t): no hidden state,
so any frame can be drawn on its own (used for previews and transitions)."""
import math
import os

from PIL import Image, ImageEnhance

from . import sprites
from . import motion
from .spec import color, hex_rgba


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out_cubic(p):
    return 1 - (1 - p) ** 3


def ease_out_back(p, s=1.9):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def ease_in_out(p):
    return 3 * p * p - 2 * p * p * p


def anim_state(L, t, W, H):
    """Return (dx, dy, scale, rot_deg, alpha, reveal) for a layer at scene time t."""
    at = L.get("at", 0.0)
    until = L.get("until")
    if t < at or (until is not None and t > until + L.get("exit_dur", 0.25)):
        return None
    dx = dy = 0.0
    sc = 1.0
    rot = L.get("rotate", 0.0)
    alpha = L.get("opacity", 1.0)
    reveal = 1.0
    enter = L.get("enter", "fade")
    ed = L.get("enter_dur", 0.4 if enter != "typewriter" else 0.9)
    p = clamp((t - at) / ed) if ed > 0 else 1.0
    if enter == "pop":
        sc *= max(0.0, ease_out_back(p))
        alpha *= clamp(p * 3)
    elif enter == "fade":
        alpha *= ease_out_cubic(p)
    elif enter == "zoom":
        sc *= 0.6 + 0.4 * ease_out_cubic(p)
        alpha *= ease_out_cubic(p)
    elif enter in ("slide_up", "slide_down", "slide_left", "slide_right"):
        e = 1 - ease_out_cubic(p)
        dist = 0.35
        if enter == "slide_up":
            dy += e * H * dist
        elif enter == "slide_down":
            dy -= e * H * dist
        elif enter == "slide_left":
            dx += e * W * dist * 1.6
        else:
            dx -= e * W * dist * 1.6
        alpha *= clamp(p * 2.5)
    elif enter == "drop":
        # falls in from above with a small bounce
        if p < 1:
            b = 1 - abs(math.cos(p * math.pi * 1.5)) * (1 - p)
            dy -= (1 - ease_out_cubic(p)) * H * 0.5
            sc *= 1 + 0.06 * (1 - b)
    elif enter == "typewriter":
        reveal = p
    if until is not None and t > until:
        q = clamp((t - until) / L.get("exit_dur", 0.25))
        ex = L.get("exit", "fade")
        if ex == "pop":
            sc *= 1 - ease_out_cubic(q)
        alpha *= 1 - q
    loop = L.get("loop", "none")
    lt = t - at
    spd = L.get("loop_speed", 1.0)
    amp = L.get("loop_amp", 1.0)
    if loop == "bob":
        dy += math.sin(lt * 2 * math.pi * 0.9 * spd) * H * 0.008 * amp
    elif loop == "float":
        dy += math.sin(lt * 2 * math.pi * 0.35 * spd) * H * 0.014 * amp
        rot += math.sin(lt * 2 * math.pi * 0.25 * spd) * 2.5 * amp
    elif loop == "pulse":
        sc *= 1 + 0.045 * amp * math.sin(lt * 2 * math.pi * 1.6 * spd)
    elif loop == "shake":
        dx += math.sin(lt * 61) * W * 0.006 * amp
        dy += math.cos(lt * 47) * W * 0.004 * amp
    elif loop == "spin":
        rot += lt * 90 * spd
    elif loop == "wiggle":
        rot += math.sin(lt * 2 * math.pi * 1.4 * spd) * 6 * amp
    sx = 1.0
    if L.get("keys"):                                    # keyframed path / scale / rotation / card flips
        kv = motion.keyed(L, lt)
        if "x" in kv:
            dx += (kv["x"] - L.get("x", 0.5)) * W
        if "y" in kv:
            dy += (kv["y"] - L.get("y", 0.5)) * H
        sc *= kv.get("scale", 1.0)
        rot += kv.get("rot", 0.0)
        alpha *= kv.get("opacity", 1.0)
        sx = kv.get("sx", 1.0)
    if L.get("type") == "character" and (L.get("keys") or L.get("hops")):
        _, bob, _ = motion.legs_and_bob(L, lt)
        hh, _ = motion.hop(L, lt)
        dy -= (bob + hh) * H
    return dx, dy, sc, rot, alpha, reveal, sx


def paste(canvas, img, cx, cy, scale=1.0, rot=0.0, alpha=1.0, flip=False, sx=1.0):
    if img is None or alpha <= 0.003 or scale <= 0.01:
        return
    if sx < 0:
        flip, sx = not flip, -sx
    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if sx < 0.995:
        if sx < 0.01:
            return
        img = img.resize((max(1, int(img.width * sx)), img.height), Image.BILINEAR)
    if abs(scale - 1.0) > 0.004:
        w, h = max(1, int(img.width * scale)), max(1, int(img.height * scale))
        img = img.resize((w, h), Image.BILINEAR)
    if abs(rot) > 0.05:
        img = img.rotate(-rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.997:
        a = img.getchannel("A").point(lambda v: int(v * alpha))
        img = img.copy()
        img.putalpha(a)
    x, y = int(round(cx - img.width / 2)), int(round(cy - img.height / 2))
    canvas.alpha_composite(img, dest=(x, y)) if x >= 0 and y >= 0 and \
        x + img.width <= canvas.width and y + img.height <= canvas.height else _paste_clip(canvas, img, x, y)


def _paste_clip(canvas, img, x, y):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(canvas.width, x + img.width), min(canvas.height, y + img.height)
    if x1 <= x0 or y1 <= y0:
        return
    crop = img.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    canvas.alpha_composite(crop, dest=(x0, y0))


# ---------- layers ----------
def character_image(ctx, L, scene_idx, t, scene):
    ch = ctx.chars[L["id"]]
    from . import acting
    r = acting.rig(ch)
    if r is not None:
        return rig_image(ctx, L, scene_idx, t, scene, ch, r)
    pose = L.get("pose", "idle")
    d = ch["dir"]
    W, H = ctx.W, ctx.H
    height_px = L.get("h", ch["meta"].get("default_h", 0.42)) * H
    use = pose
    speaking = scene.get("speaker", ctx.default_speaker) == L["id"] and L.get("talk", True)
    if speaking:
        v = ctx.viseme(scene_idx, t)
        if v:
            for cand in (f"{pose}_{v}", f"{pose}_talk", "talk" if pose == "idle" else None):
                if cand and cand in ch["poses"]:
                    use = cand
                    break
    blink_pose = f"{pose}_blink" if f"{pose}_blink" in ch["poses"] else (
        "blink" if pose == "idle" and "blink" in ch["poses"] else None)
    if blink_pose and use == pose:
        phase = (t + hash(L["id"]) % 7 * 0.37) % 3.3
        if phase < 0.13:
            use = blink_pose
    svg = sprites.read_file(os.path.join(d, use + ".svg"))
    # size by height: rasterise at a width that gives the target height
    probe = sprites.svg_image(svg, 200)
    width_px = height_px * probe.width / max(1, probe.height)
    return sprites.svg_image(svg, width_px)


def rig_image(ctx, L, scene_idx, t, scene, ch, r):
    """Draw a rigged character fresh for this frame: acting gesture, lip-sync mouth, blinks."""
    from . import acting
    tr = acting.track(ctx, scene_idx, L, r)
    arms, g = acting.arms_at(r, tr, t)
    _, expr, look = r.BASES[g]
    lt = t - L.get("at", 0.0)
    moving = bool(L.get("keys") or L.get("hops"))
    lift, _, _ = motion.legs_and_bob(L, lt) if moving else ((0.0, 0.0), 0, False)
    swing = motion.arm_swing(r.ARMS["down"], lt, L) if moving else None
    if swing is not None:
        arms = swing
    lift = (round(lift[0] / 6) * 6, round(lift[1] / 6) * 6)
    speaking = scene.get("speaker", ctx.default_speaker) == L["id"] and L.get("talk", True)
    mouth = ctx.viseme(scene_idx, t) if speaking else None
    blink = ((t + (zlib_seed(L["id"]) % 7) * 0.37) % 3.4) < 0.12
    key = (tuple((tuple(round(v) for v in a[0]), tuple(round(v) for v in a[1]), tuple(round(v) for v in a[2]), a[3], a[4])
                 for a in arms), expr, look, mouth, blink, lift, moving)
    cache = ctx.__dict__.setdefault("_rigsvg", {})
    svg = cache.get(key)
    if svg is None:
        if len(cache) > 400:
            cache.clear()
        try:
            svg = r.figure(arms=[(a[0], a[1], a[2], a[3], a[4]) for a in arms], expr=expr, blink=blink, look=look,
                           mouth=mouth, lift=lift, shadow=not moving)
        except TypeError:                                 # older rigs without walking support
            svg = r.figure(arms=[(a[0], a[1], a[2], a[3], a[4]) for a in arms], expr=expr, blink=blink, look=look, mouth=mouth)
        cache[key] = svg
    height_px = L.get("h", ch["meta"].get("default_h", 0.42)) * ctx.H
    return sprites.svg_image(svg, height_px * r.W / r.H)


_RASTER = {}


def raster_image(path, width, blur=0):
    """A PNG/JPG (e.g. a Blender-rendered set or prop cut-out) scaled to `width` px, optionally blurred (cached)."""
    key = (path, width, blur)
    img = _RASTER.get(key)
    if img is None:
        if not os.path.exists(path):
            return None
        src = Image.open(path).convert("RGBA")
        h = max(1, int(src.height * width / src.width))
        img = src.resize((max(1, width), h), Image.LANCZOS)
        if blur:
            from PIL import ImageFilter
            img = img.filter(ImageFilter.GaussianBlur(blur))
        if len(_RASTER) > 64:
            _RASTER.clear()
        _RASTER[key] = img
    return img


_SHADOWS = {}


def ground_shadow(w):
    """Soft elliptical floor shadow, w px wide."""
    w = max(8, w - w % 4)
    img = _SHADOWS.get(w)
    if img is None:
        from PIL import ImageDraw, ImageFilter
        h = max(4, w // 5)
        pad = w // 6
        img = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(img).ellipse((pad, pad, pad + w, pad + h), fill=(0, 0, 0, 120))
        img = img.filter(ImageFilter.GaussianBlur(pad / 2.2))
        _SHADOWS[w] = img
    return img


def zlib_seed(s):
    import zlib
    return zlib.crc32(s.encode())


_SHOT_CACHE = {}


def blender_frame(ctx, L, t):
    """The rendered 3D frame for scene time t, scaled to the layer's size."""
    d = L.get("_frames_dir")
    if not d or not os.path.isdir(d):
        return None
    files = _SHOT_CACHE.get(d)
    if files is None:
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        _SHOT_CACHE[d] = files
    if not files:
        return None
    k = int((t - L.get("at", 0.0)) * L.get("_fps", ctx.fps))
    k = max(0, min(len(files) - 1, k))
    key = (d, k)
    img = _SHOT_CACHE.get(key)
    if img is None:
        if len(_SHOT_CACHE) > 24:
            for kk in [x for x in _SHOT_CACHE if isinstance(x, tuple)][:12]:
                _SHOT_CACHE.pop(kk, None)
        img = Image.open(os.path.join(d, files[k])).convert("RGBA")
        img = img.resize((int(ctx.W * L.get("w", 1.0)), int(ctx.H * L.get("h", 1.0))), Image.LANCZOS)
        _SHOT_CACHE[key] = img
    return img


def layer_image(ctx, L, scene_idx, t, scene, reveal):
    st = ctx.style
    W = ctx.W
    typ = L["type"]
    if typ == "character":
        return character_image(ctx, L, scene_idx, t, scene)
    if typ == "text":
        txt = L["text"]
        if reveal < 1:
            n = int(len(txt) * reveal)
            txt = txt[:n]
            if not txt.strip():
                return None
        return sprites.text_image(
            st, txt, size=L.get("size", 110), font_name=L.get("font", "display"),
            fill=L.get("color", "primary"), highlight=L.get("highlight", "accent"),
            stroke=L.get("stroke", "#000000"), stroke_width=L.get("stroke_width", 0),
            max_w=L.get("max_w", 0.86), align=L.get("align", "center"),
            uppercase=L.get("uppercase", False), shadow=L.get("shadow", True))
    if typ == "counter":
        at = L.get("at", 0)
        p = ease_out_cubic(clamp((t - at) / L.get("count_dur", 1.2)))
        v = L.get("from", 0) + (L["to"] - L.get("from", 0)) * p
        dec = L.get("decimals", 0)
        s = f"{v:,.{dec}f}" if L.get("commas", True) else f"{v:.{dec}f}"
        s = f"{L.get('prefix', '')}{s}{L.get('suffix', '')}"
        return sprites.text_image(st, s, size=L.get("size", 180), font_name=L.get("font", "display"),
                                  fill=L.get("color", "accent"), stroke=L.get("stroke", "#000000"),
                                  stroke_width=L.get("stroke_width", 0), max_w=0.95)
    if typ == "shape":
        svg, w = sprites.shape_svg(st, L, ctx.W, ctx.H)
        return sprites.svg_image(svg, w)
    if typ == "blender":
        return blender_frame(ctx, L, t)
    if typ == "scene3d":
        from .three import render as render3d
        return render3d(ctx.style, L, t - L.get("at", 0.0), ctx.dur[scene_idx],
                        int(L.get("w", 1.0) * ctx.W), int(L.get("h", 1.0) * ctx.H), L.get("ss", 2))
    if typ == "image":
        path = L.get("path", "")
        if path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            return raster_image(os.path.join(ctx.root, path), int(L.get("w", 0.4) * W), L.get("blur", 0))
        svg = L.get("svg") or sprites.read_file(os.path.join(ctx.root, L["path"]))
        return sprites.svg_image(svg, L.get("w", 0.4) * W)
    return None


_LUT = {}


def grade_lut(style):
    g = style.get("grade", {})
    key = repr(sorted(g.items()))
    if key not in _LUT:
        sh = [c / 255 for c in hex_rgba(color(style, g.get("shadows", "#1d4a52")))[:3]]
        hi = [c / 255 for c in hex_rgba(color(style, g.get("highlights", "#ffb36b")))[:3]]
        k, con = g.get("strength", 0.12), g.get("contrast", 1.06)
        lut = []
        for ch in range(3):
            for v in range(256):
                x = v / 255
                x = 0.5 + (x - 0.5) * con                          # contrast around mid grey
                x += k * ((sh[ch] - 0.5) * 2 * (1 - x) ** 2 * 0.6   # tint the shadows
                          + (hi[ch] - 0.5) * 2 * x ** 2 * 0.5)       # tint the highlights
                lut.append(int(max(0, min(255, round(x * 255)))))
        _LUT[key] = lut + list(range(256))  # alpha unchanged
    return _LUT[key]


def apply_grade(style, img):
    if not style.get("grade", {}).get("enabled"):
        return img
    return img.point(grade_lut(style))


def draw_scene(ctx, scene_idx, t):
    """The scene's picture without captions/overlays (camera applied)."""
    scene = ctx.job["scenes"][scene_idx]
    W, H = ctx.W, ctx.H
    fb, _ = active_beat(ctx, scene_idx, t, ("freeze",))
    t_real, t = t, (fb["at"] if fb else t)                # a freeze beat holds the picture still
    canvas = sprites.background(ctx.style, scene.get("bg"), W, H).copy()
    for L in scene.get("layers", []):
        stt = anim_state(L, t, W, H)
        if stt is None:
            continue
        dx, dy, sc, rot, alpha, reveal, sx = stt
        lt = t - L.get("at", 0.0)
        if L.get("type") == "character" and L.get("ground", bool(L.get("keys") or L.get("hops"))):
            hh, _ = motion.hop(L, lt)
            _, bob, _ = motion.legs_and_bob(L, lt)
            hgt = L.get("h", 0.4) * sc * L.get("scale", 1.0)
            gx = L.get("x", 0.5) * W + dx
            gy = L.get("y", 0.5) * H + dy + (hh + bob) * H + hgt * H * 0.485
            shw = hgt * H * 0.36 * (1 - min(0.6, hh * 4))
            paste(canvas, ground_shadow(int(shw)), gx, gy, 1.0, 0, alpha * (1 - min(0.5, hh * 3)))
        img = layer_image(ctx, L, scene_idx, t, scene, reveal)
        if img is None:
            continue
        cx = L.get("x", 0.5) * W + dx
        cy = L.get("y", 0.5) * H + dy
        paste(canvas, img, cx, cy, sc * L.get("scale", 1.0), rot, alpha, L.get("flip", False), sx)
    t = t_real
    cam = scene.get("camera") or {}
    dur = ctx.dur[scene_idx]
    z0, z1 = cam.get("zoom", [1.0, 1.0])
    z = z0 + (z1 - z0) * ease_in_out(clamp(t / max(dur, 0.01)))
    if cam.get("keys"):                                  # camera moves: [{"t", "zoom", "focus": [x, y]}, ...]
        ck = motion.keyed({"keys": [dict(k, x=k.get("focus", [0.5, 0.5])[0], y=k.get("focus", [0.5, 0.5])[1],
                                         scale=k.get("zoom", 1.0)) for k in cam["keys"]]}, t)
        z = ck.get("scale", 1.0)
        cam = dict(cam, focus=[ck.get("x", 0.5), ck.get("y", 0.5)])
    for pt in cam.get("punch", []):  # quick zoom hits at given times
        if 0 <= t - pt < 0.35:
            z *= 1 + 0.07 * math.sin((t - pt) / 0.35 * math.pi)
    ox = oy = 0.0
    sh = cam.get("shake")
    if sh and sh[0] <= t < sh[0] + sh[1]:
        ox = math.sin(t * 73) * 14
        oy = math.cos(t * 59) * 14
    fx, fy = cam.get("focus", [0.5, 0.5])
    b, bt = active_beat(ctx, scene_idx, t)
    if b and b.get("zoom", 1.0) > 1.0:                  # beat camera: push in on the face, or snap zoom
        if b["kind"] == "zoom_punch":
            k = clamp(bt / 0.05) * clamp((b["dur"] - bt) / 0.15)
        else:
            k = ease_in_out(clamp(bt / 0.18)) * ease_in_out(clamp((b["dur"] - bt) / 0.22))
        z *= 1 + (b["zoom"] - 1) * k
        bfx, bfy = b.get("focus") or face_focus(ctx, scene, b)
        fx, fy = fx + (bfx - fx) * k, fy + (bfy - fy) * k
    if True:
        if z > 1.001 or ox or oy:
            cw, chh = W / z, H / z
            x0 = clamp(fx * W - cw / 2 + ox, 0, W - cw)
            y0 = clamp(fy * H - chh / 2 + oy, 0, H - chh)
            canvas = canvas.crop((int(x0), int(y0), int(x0 + cw), int(y0 + chh))).resize((W, H), Image.BILINEAR)
    out = apply_grade(ctx.style, canvas)
    if fb:                                              # freeze-frame: colour drains out, slightly darker
        k = clamp((t_real - fb["at"]) / 0.12)
        grey = ImageEnhance.Brightness(ImageEnhance.Color(out).enhance(0.25)).enhance(0.9)
        out = Image.blend(out, grey, k)
    return out


def active_beat(ctx, scene_idx, t, kinds=None):
    beats = ctx.beats[scene_idx] if scene_idx < len(getattr(ctx, "beats", [])) else []
    for b in beats:
        if b["at"] <= t < b["at"] + b["dur"] and (kinds is None or b["kind"] in kinds):
            return b, t - b["at"]
    return None, 0.0


def face_focus(ctx, scene, b):
    """Where a beat's camera should push in: the face of the reacting character (or the first one)."""
    for L in scene.get("layers", []):
        if L.get("type") == "character" and (not b.get("who") or b["who"] == L.get("id")):
            ch = ctx.chars.get(L.get("id"), {})
            h = L.get("h", ch.get("meta", {}).get("default_h", 0.42))
            return L.get("x", 0.5), L.get("y", 0.5) - h / 2 + h * 0.12
    return 0.5, 0.45


def draw_sticker(ctx, canvas, b, bt):
    """A meme-style caption card for a beat: cream card, ink text, slight tilt, pops in."""
    st = ctx.style
    W, H = ctx.W, ctx.H
    txt = sprites.text_image(st, b["text"], size=b.get("text_size", 58), font_name="body", fill="ink",
                             highlight="accent", shadow=False, max_w=0.66, uppercase=False)
    pad = 28
    card = Image.new("RGBA", (txt.width + pad * 2, txt.height + pad * 2), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=22,
                                           fill=hex_rgba(color(st, "primary")))
    card.alpha_composite(txt, (pad, pad))
    p = clamp(bt / 0.16)
    out_k = clamp((b["dur"] - bt) / 0.12)
    paste(canvas, card, b.get("text_x", 0.5) * W, b.get("text_y", 0.24) * H,
          (0.6 + 0.4 * ease_out_back(p)) * (0.85 + 0.15 * out_k), b.get("tilt", -3), out_k)


def draw_overlays(ctx, canvas, scene_idx, t):
    st = ctx.style
    W, H = ctx.W, ctx.H
    scene = ctx.job["scenes"][scene_idx]
    cap = st["captions"]
    if cap.get("enabled") and scene.get("captions", ctx.job.get("captions", True)):
        for c0, c1, words, wt in ctx.captions[scene_idx]:
            if c0 <= t < c1:
                cur = 0
                for i, wtime in enumerate(wt):
                    if t >= wtime:
                        cur = i
                img = sprites.text_image(st, " ".join(words), size=cap["size"], font_name=cap["font"],
                                         fill=cap["color"], highlight=cap["highlight"], stroke=cap["stroke"],
                                         stroke_width=cap["stroke_width"], max_w=0.84,
                                         uppercase=cap.get("uppercase", True), highlight_index=cur)
                p = clamp((t - c0) / 0.12)
                y = scene.get("caption_y", cap["y"]) * H
                paste(canvas, img, W / 2, y, 0.86 + 0.14 * ease_out_back(p), 0, 1.0)
                break
    b, bt = active_beat(ctx, scene_idx, t)
    if b and b.get("text"):
        draw_sticker(ctx, canvas, b, bt)
    wm = st.get("watermark", {})
    if wm.get("text"):
        img = sprites.text_image(st, wm["text"], size=wm.get("size", 34), font_name="light",
                                 fill="primary", shadow=False)
        paste(canvas, img, W / 2, wm.get("y", 0.955) * H, 1.0, 0, wm.get("opacity", 0.5))
    pb = st.get("progress_bar", {})
    if pb.get("enabled"):
        g = (ctx.start[scene_idx] + t) / ctx.total
        hpx = pb.get("height", 10)
        bar = Image.new("RGBA", (max(1, int(W * clamp(g))), hpx), hex_rgba(color(st, pb.get("color", "accent"))))
        canvas.alpha_composite(bar, (0, 0))
    return canvas


def render_frame(ctx, scene_idx, t):
    scene = ctx.job["scenes"][scene_idx]
    W, H = ctx.W, ctx.H
    cur = draw_scene(ctx, scene_idx, t)
    tr = scene.get("transition", ctx.style["transition"]["type"] if scene_idx > 0 else "cut")
    nfr = scene.get("transition_frames", ctx.style["transition"]["frames"])
    T = nfr / ctx.fps
    if scene_idx > 0 and tr != "cut" and t < T:
        p = ease_in_out(clamp(t / T))
        prev = draw_scene(ctx, scene_idx - 1, ctx.dur[scene_idx - 1] - 1 / ctx.fps)
        if tr == "fade":
            cur = Image.blend(prev, cur, p)
        elif tr == "slide_left":
            out = Image.new("RGBA", (W, H))
            off = int(W * p)
            out.paste(prev, (-off, 0))
            out.paste(cur, (W - off, 0))
            cur = out
        elif tr == "slide_up":
            out = Image.new("RGBA", (W, H))
            off = int(H * p)
            out.paste(prev, (0, -off))
            out.paste(cur, (0, H - off))
            cur = out
        elif tr == "zoom":
            z = 1 + 0.35 * p
            cw, ch = int(W / z), int(H / z)
            pz = prev.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H), Image.BILINEAR)
            cur = Image.blend(pz, cur, p)
        elif tr == "flash":
            base = prev if p < 0.5 else cur
            k = 1 - abs(p - 0.5) * 2
            cur = Image.blend(base, Image.new("RGBA", (W, H), (255, 255, 255, 255)), k * 0.9)
    return draw_overlays(ctx, cur, scene_idx, t)
