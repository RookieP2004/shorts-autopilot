"""Documentary toolkit for long videos: the things that make an edit feel hand-made rather than generated.

Turned on by the style's "doc" block (the long-form profile has it). Everything here is deterministic per frame.

Frame finish (doc.finish, after captions):    film grain, vignette, letterbox, archival "reconstruction" look, light leaks,
                                              gate weave.
Direct layers (drawn straight onto the frame): "marker" (hand-drawn circle / underline / arrow / box / cross / tick /
                                              highlight / scribble that draws itself on and "boils" at 12 fps),
                                              "string" (red string between pins on an evidence board), "timeline",
                                              "lower_third" (name/source super), "chapter" (chapter title card),
                                              "tag" (small label such as RECONSTRUCTION or a source line).
Raster layers (pasted like images):          "paper" (note / photo print / typed document / newspaper clipping, with
                                              tape and a real shadow).
Transitions:                                  "whip", "paper", "dip", "burn".
"""
import math
import os
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import sprites
from .spec import color, hex_rgba

DIRECT = {"marker", "string", "timeline", "lower_third", "chapter", "tag"}

FONT = {  # documentary type: tracked condensed caps, a book serif, a typewriter, handwriting, a marker
    "cond": "fonts/Oswald.ttf",
    "serif": "fonts/LibreBaskerville.ttf",
    "serif_i": "fonts/LibreBaskerville-Italic.ttf",
    "type": "fonts/SpecialElite-Regular.ttf",
    "hand": "fonts/Caveat.ttf",
    "marker": "fonts/PermanentMarker-Regular.ttf",
    "mono": "fonts/CourierPrime-Regular.ttf",
}


def on(style):
    return bool(style.get("doc", {}).get("enabled"))


def _f(name, size):
    return sprites.font(FONT.get(name, name), int(size))


def _rgba(style, c, a=None):
    v = hex_rgba(color(style, c))
    return v if a is None else (v[0], v[1], v[2], int(a))


def _seed(*parts):
    return zlib.crc32(repr(parts).encode()) & 0xFFFFFFFF


def _clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def _ease(p):
    return 3 * p * p - 2 * p * p * p


def _eout(p):
    return 1 - (1 - p) ** 3


# ------------------------------------------------------------------ frame finish
_CACHE = {}


def _vignette(W, H, amount):
    k = ("vig", W, H, amount)
    if k not in _CACHE:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.66)) ** 2)
        _CACHE[k] = (1 - amount * np.clip((d - 0.45) / 0.75, 0, 1) ** 1.6)[..., None].astype(np.float32)
    return _CACHE[k]


def _grain(W, H, idx):
    """Film grain: 8 pre-made frames of soft 2x2 noise, picked per frame (so it dances, never repeats visibly)."""
    k = ("grain", W, H)
    if k not in _CACHE:
        rng = np.random.default_rng(7)
        tiles = []
        for _ in range(8):
            n = rng.standard_normal((H // 2 + 1, W // 2 + 1)).astype(np.float32)
            n = np.repeat(np.repeat(n, 2, 0), 2, 1)[:H, :W]
            tiles.append(n)
        _CACHE[k] = tiles
    return _CACHE[k][idx % 8]


def finish(ctx, img, scene_idx, t):
    """Grain, vignette, letterbox, archival look and light leaks over the finished frame."""
    style = ctx.style
    d = style.get("doc", {})
    scene = ctx.job["scenes"][scene_idx]
    W, H = img.size
    fidx = int(round((ctx.start[scene_idx] + t) * ctx.fps))
    look = scene.get("look")
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    if look == "archival":                                    # a reconstruction shot as if on old film
        rnd = np.random.default_rng(_seed("arch", fidx // 2))
        lum = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11
        lum = np.clip((lum - 128) * 1.12 + 128, 0, 255) * (1 + rnd.uniform(-0.035, 0.035))
        a = np.stack([lum * 1.06 + 6, lum * 0.95 + 2, lum * 0.78], -1)
        for _ in range(rnd.integers(0, 3)):                   # vertical scratches
            x = int(rnd.uniform(0.05, 0.95) * W)
            a[:, x:x + 1] = a[:, x:x + 1] * 0.55 + 150
        for _ in range(rnd.integers(2, 7)):                   # dust specks
            x, y, r = int(rnd.uniform(0, W)), int(rnd.uniform(0, H)), int(rnd.integers(1, 4))
            a[max(0, y - r):y + r, max(0, x - r):x + r] *= 0.35
        sh = int(rnd.integers(-2, 3))                         # gate weave
        if sh:
            a = np.roll(a, sh, axis=0)
        a *= _vignette(W, H, 0.55)
        a += _grain(W, H, fidx)[..., None] * 16
    else:
        if d.get("vignette", 0):
            a *= _vignette(W, H, d["vignette"])
        if d.get("grain", 0):
            a += _grain(W, H, fidx)[..., None] * (255 * d["grain"])
    lk = scene.get("leak")                                    # a warm light leak drifting across, [start, dur]
    if lk:
        p = (t - lk[0]) / lk[1]
        if 0 <= p <= 1:
            k = math.sin(p * math.pi) * lk[2] if len(lk) > 2 else math.sin(p * math.pi) * 0.55
            cx = (-0.2 + 1.4 * p) * W
            yy, xx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
            g = np.exp(-(((xx - cx) / (W * 0.28)) ** 2 + ((yy - H * 0.35) / (H * 0.7)) ** 2))
            g = np.repeat(np.repeat(g, 4, 0), 4, 1)[:H, :W]
            a += g[..., None] * k * np.array([255, 150, 70], np.float32)
    lb = scene.get("letterbox", d.get("letterbox", 0))       # cinematic bars, fraction of height each
    if lb:
        lin = scene.get("letterbox_in")
        k = _ease(_clamp(t / lin)) if lin else 1.0
        bh = int(H * lb * k)
        if bh > 0:
            a[:bh] = 0
            a[H - bh:] = 0
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if look == "archival" and scene.get("archival_label", True):
        o = out.convert("RGBA")
        draw_tag(ctx, o, {"text": scene.get("archival_label") if isinstance(scene.get("archival_label"), str)
                          else "RECONSTRUCTION", "size": 30, "track": 5, "x": 0.035, "y": 0.06}, 1.0, 1.0)
        out = o
    return out.convert("RGBA")


def camera_drift(scene_idx, t, amount):
    """Slow, organic 'operator' float: two incommensurate sines per axis (never a loop you can spot)."""
    ph = scene_idx * 1.7
    dx = (math.sin(2 * math.pi * 0.071 * t + ph) + 0.55 * math.sin(2 * math.pi * 0.183 * t + ph * 2.3)) * 0.0045
    dy = (math.sin(2 * math.pi * 0.059 * t + ph * 1.3) + 0.5 * math.sin(2 * math.pi * 0.151 * t + ph)) * 0.0035
    return dx * amount, dy * amount


# ------------------------------------------------------------------ text helper
def _text_img(style, text, font, size, fill, track=0, shadow=False, max_w=None):
    k = ("t", text, font, size, fill, track, shadow, max_w)
    if k in _CACHE:
        return _CACHE[k]
    f = _f(font, size)
    if track:
        w = int(sum(f.getlength(ch) + track for ch in text)) + 8
    else:
        w = int(f.getlength(text)) + 8
    asc, desc = f.getmetrics()
    img = Image.new("RGBA", (max(1, w + 8), asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = hex_rgba(color(style, fill)) if isinstance(fill, str) else fill
    x = 4
    if track:
        for ch in text:
            if shadow:
                d.text((x + 2, 6), ch, font=f, fill=(0, 0, 0, 120))
            d.text((x, 4), ch, font=f, fill=col)
            x += f.getlength(ch) + track
    else:
        if shadow:
            d.text((x + 2, 6), text, font=f, fill=(0, 0, 0, 120))
        d.text((x, 4), text, font=f, fill=col)
    if len(_CACHE) > 600:
        for kk in [kk for kk in _CACHE if kk[0] == "t"][:200]:
            _CACHE.pop(kk, None)
    _CACHE[k] = img
    return img


def _wrap(text, f, maxpx):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if cur and f.getlength(trial) > maxpx:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ paper (raster layer)
def _paper_tex(w, h, base, seed, aged=0.25):
    """Paper: base colour, fibre noise, darker uneven edges."""
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((h // 3 + 2, w // 3 + 2)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 18) + 128).clip(0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
                   ).astype(np.float32) - 128
    fib = rng.standard_normal((h, w)).astype(np.float32) * 4
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    edge = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)) / max(8.0, min(w, h) * 0.12)
    edge = np.clip(edge, 0, 1)
    shade = (1 - aged * (1 - edge) ** 2)[..., None]
    a = np.array(base[:3], np.float32)[None, None, :] + (n * 0.35 + fib)[..., None]
    a = a * shade
    return np.clip(a, 0, 255).astype(np.uint8)


def _tape(w, h, seed):
    rng = np.random.default_rng(seed)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(7):                                   # torn left edge
        pts.append((int(rng.uniform(0, w * 0.06)), int(h * i / 6)))
    for i in range(7):                                   # torn right edge
        pts.append((int(w - rng.uniform(0, w * 0.06)), int(h * (6 - i) / 6)))
    d.polygon(pts, fill=(236, 226, 196, 170))
    return img


def paper_image(ctx, L):
    """A physical card on the board. kinds: note | photo | doc | clip. Returns RGBA with shadow and tape."""
    st = ctx.style
    W = ctx.W
    k = ("paper", repr(sorted((kk, repr(v)) for kk, v in L.items() if not kk.startswith("_") and kk not in
                              ("x", "y", "at", "until", "enter", "enter_dur", "keys", "pan", "rotate", "opacity",
                               "exit", "exit_dur", "sfx", "scale"))), W)
    if k in _CACHE:
        return _CACHE[k]
    kind = L.get("kind", "note")
    w = int(L.get("w", 0.3) * W)
    seed = _seed(L.get("text", ""), L.get("path", ""), kind)
    ink = _rgba(st, L.get("ink", "#2a2119"))
    pad = int(w * 0.07)
    body = None
    if kind == "photo":
        border = int(w * 0.045)
        iw = w - 2 * border
        src = Image.open(os.path.join(ctx.root, L["path"])).convert("RGB")
        ih = int(L.get("h", 0) * W) - 2 * border if L.get("h") else int(iw * src.height / src.width)
        # crop-to-fill the print window, with an optional focus point
        fx, fy = L.get("focus", [0.5, 0.5])
        r = max(iw / src.width, ih / src.height)
        s2 = src.resize((max(iw, int(src.width * r + 1)), max(ih, int(src.height * r + 1))), Image.LANCZOS)
        ox = int(_clamp(fx * s2.width - iw / 2, 0, s2.width - iw))
        oy = int(_clamp(fy * s2.height - ih / 2, 0, s2.height - ih))
        photo = s2.crop((ox, oy, ox + iw, oy + ih))
        tone = L.get("tone")
        if tone in ("sepia", "bw"):
            g = np.asarray(photo.convert("L")).astype(np.float32)
            g = np.clip((g - 128) * 1.1 + 128, 0, 255)
            arr = np.stack([g * 1.07 + 8, g * 0.96 + 3, g * 0.8], -1) if tone == "sepia" else np.stack([g] * 3, -1)
            photo = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        cap_h = int(w * 0.16) if L.get("caption") else border
        h = border + ih + cap_h
        tex = Image.fromarray(_paper_tex(w, h, hex_rgba("#f3efe6"), seed, 0.18))
        tex.paste(photo, (border, border))
        body = tex.convert("RGBA")
        if L.get("caption"):
            f = _f("hand", int(w * 0.085))
            d = ImageDraw.Draw(body)
            tw = f.getlength(L["caption"])
            d.text(((w - tw) / 2, border + ih + int(cap_h * 0.12)), L["caption"], font=f, fill=_rgba(st, "#2a2a3a"))
    else:
        base = {"note": "#f1e7cf", "doc": "#ece3cd", "clip": "#e9e2d0"}.get(kind, "#f1e7cf")
        base = hex_rgba(color(st, L.get("paper", base)))
        lines = []                                          # (text, font, size, colour, align, gap_after)
        if kind == "clip":
            if L.get("masthead"):
                lines.append((L["masthead"].upper(), "cond", int(w * 0.05), ink, "center", 0.3))
            lines.append((L.get("title", L.get("text", "")), "serif", int(w * 0.078), ink, "left", 0.5))
        elif kind == "doc":
            if L.get("title"):
                lines.append((L["title"], "type", int(w * 0.06), ink, "left", 0.6))
            if L.get("text"):
                lines.append((L["text"], "type", int(w * L.get("text_size", 0.05)), ink, "left", 0.2))
        else:
            if L.get("title"):
                lines.append((L["title"], "marker", int(w * 0.075), _rgba(st, L.get("title_color", "#b8322b")), "left", 0.4))
            if L.get("text"):
                lines.append((L["text"], L.get("font", "hand"), int(w * L.get("text_size", 0.085)), ink, "left", 0.2))
        tw = w - 2 * pad
        laid, hh = [], pad
        for text, fn, sz, col, al, gap in lines:
            f = _f(fn, sz)
            asc, desc = f.getmetrics()
            for ln in _wrap(text, f, tw):
                laid.append((ln, f, col, al, hh))
                hh += int((asc + desc) * 1.05)
            hh += int(sz * gap)
        if kind == "clip":                                  # body text as grey column lines, newspaper-style
            cols, rows = 2, L.get("rows", 7)
            colw = (tw - pad * 0.5) / cols
            body_h = int(rows * w * 0.034)
            fake = (hh, body_h, cols, colw, rows)
            hh += body_h
        hh += pad
        h = int(L.get("h", 0) * W) or hh
        tex = Image.fromarray(_paper_tex(w, h, base, seed, 0.3 if kind != "note" else 0.2))
        body = tex.convert("RGBA")
        d = ImageDraw.Draw(body)
        if L.get("lined") and laid:
            f0 = laid[-1][1]
            step = int(sum(f0.getmetrics()) * 1.05)
            yy = laid[-1][4] + step
            first = laid[0][4] + int(sum(laid[0][1].getmetrics()) * 1.05)
            for y_ in [l[4] + int(sum(l[1].getmetrics()) * 0.98) for l in laid[1:]] + list(range(yy, h - pad // 2, step)):
                if y_ >= first:
                    d.line([(pad // 2, y_), (w - pad // 2, y_)], fill=(120, 150, 190, 70), width=2)
        for ln, f, col, al, y in laid:
            x = pad if al == "left" else (w - f.getlength(ln)) / 2
            d.text((x, y), ln, font=f, fill=col)
        if kind == "clip":
            y0, bh, cols, colw, rows = fake
            rng = np.random.default_rng(seed)
            for c in range(cols):
                for r_ in range(rows):
                    x0 = pad + c * (colw + pad * 0.5)
                    ll = colw * (rng.uniform(0.55, 0.98) if r_ == rows - 1 else rng.uniform(0.88, 1.0))
                    yy = y0 + r_ * w * 0.034
                    d.rectangle([x0, yy, x0 + ll, yy + w * 0.012], fill=(90, 82, 70, 150))
        if L.get("stamp"):                                  # red ink stamp, slightly rotated
            sf = _f("cond", int(w * 0.07))
            sw_ = int(sf.getlength(L["stamp"]) + w * 0.06)
            st_img = Image.new("RGBA", (sw_, int(w * 0.12)), (0, 0, 0, 0))
            sd = ImageDraw.Draw(st_img)
            sd.rectangle([3, 3, sw_ - 4, st_img.height - 4], outline=(184, 40, 36, 200), width=5)
            sd.text((w * 0.03, w * 0.012), L["stamp"], font=sf, fill=(184, 40, 36, 210))
            st_img = st_img.rotate(L.get("stamp_rot", -12), expand=True, resample=Image.BICUBIC)
            body.alpha_composite(st_img, (int(w - st_img.width - pad * 0.6), int(h - st_img.height - pad * 0.4)))
    # tape
    tp = L.get("tape", ["tl", "tr"] if kind != "photo" else ["tc"])
    if tp:
        bw, bh = body.size
        m = int(bw * 0.12)
        out = Image.new("RGBA", (bw + 2 * m, bh + 2 * m), (0, 0, 0, 0))
        # shadow
        sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([m + 6, m + 10, m + bw + 6, m + bh + 10], fill=(0, 0, 0, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(max(4, bw // 60)))
        out.alpha_composite(sh)
        out.alpha_composite(body, (m, m))
        tw_, th_ = int(bw * 0.24), int(bw * 0.07)
        for i, pos in enumerate(tp if isinstance(tp, list) else ["tl", "tr"]):
            tape = _tape(tw_, th_, seed + i)
            ang = {"tl": 38, "tr": -38, "bl": -38, "br": 38, "tc": 4}.get(pos, 0)
            tape = tape.rotate(ang, expand=True, resample=Image.BICUBIC)
            cx = {"tl": m, "tr": m + bw, "bl": m, "br": m + bw, "tc": m + bw / 2}[pos]
            cy = {"tl": m, "tr": m, "bl": m + bh, "br": m + bh, "tc": m}[pos]
            out.alpha_composite(tape, (int(cx - tape.width / 2), int(cy - tape.height / 2)))
        img = out
    else:
        bw, bh = body.size
        m = int(bw * 0.05)
        img = Image.new("RGBA", (bw + 2 * m, bh + 2 * m), (0, 0, 0, 0))
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([m + 6, m + 10, m + bw + 6, m + bh + 10], fill=(0, 0, 0, 120))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(4, bw // 60))))
        img.alpha_composite(body, (m, m))
    _CACHE[k] = img
    return img


# ------------------------------------------------------------------ hand-drawn strokes
def _boil(seed, t, n, amp):
    """Per-point jitter that changes 12 times a second (drawn 'on twos', like hand animation)."""
    fr = int(t * 12)
    rng = np.random.default_rng(_seed(seed, fr))
    return rng.normal(0, amp, (n, 2))


def _marker_paths(L, W, H):
    """Return a list of strokes (each an (n,2) array of px points), drawn in order."""
    sh = L.get("shape", "circle")
    rng = np.random.default_rng(_seed("mk", sh, repr(L.get("box")), repr(L.get("to"))))
    if sh == "circle":
        x0, y0, x1, y1 = L["box"]
        cx, cy = (x0 + x1) / 2 * W, (y0 + y1) / 2 * H
        rx, ry = (x1 - x0) / 2 * W * 1.08, (y1 - y0) / 2 * H * 1.12
        a0 = math.radians(L.get("start", -120))
        sweep = math.radians(L.get("sweep", 385))
        n = 90
        th = a0 + sweep * np.linspace(0, 1, n)
        wob = 1 + 0.035 * np.sin(np.linspace(0, 3 * math.pi, n) + rng.uniform(0, 6)) + np.linspace(0, 0.07, n)
        pts = np.stack([cx + rx * wob * np.cos(th), cy + ry * wob * np.sin(th)], 1)
        return [pts]
    if sh in ("underline", "line"):
        x0, y0, x1, y1 = L["box"] if "box" in L else (*L["from"], *L["to"])
        if sh == "underline":
            y1 = y0 = y1 if "box" in L else y0
        n = 40
        s = np.linspace(0, 1, n)
        xs = (x0 + (x1 - x0) * s) * W
        ys = (y0 + (y1 - y0) * s) * H + np.sin(s * math.pi) * H * 0.006 * rng.uniform(-1, 1)
        return [np.stack([xs, ys], 1)]
    if sh == "arrow":
        (ax, ay), (bx, by) = L["from"], L["to"]
        ax, ay, bx, by = ax * W, ay * H, bx * W, by * H
        bend = L.get("bend", 0.25)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        nx, ny = -(by - ay), (bx - ax)
        cx, cy = mx + nx * bend, my + ny * bend
        s = np.linspace(0, 1, 50)[:, None]
        p = (1 - s) ** 2 * np.array([ax, ay]) + 2 * (1 - s) * s * np.array([cx, cy]) + s ** 2 * np.array([bx, by])
        d = p[-1] - p[-6]
        ang = math.atan2(d[1], d[0])
        hl = L.get("head", 0.028) * W
        h1 = np.array([[bx, by], [bx - hl * math.cos(ang - 0.5), by - hl * math.sin(ang - 0.5)]])
        h2 = np.array([[bx, by], [bx - hl * math.cos(ang + 0.5), by - hl * math.sin(ang + 0.5)]])
        return [p, h1, h2]
    if sh == "box":
        x0, y0, x1, y1 = [v * (W if i % 2 == 0 else H) for i, v in enumerate(L["box"])]
        o = W * 0.006
        pts = np.array([[x0 - o, y0], [x1 + o, y0 + o * 0.4], [x1, y1 + o], [x0 + o * 0.5, y1], [x0, y0 - o * 1.2]])
        return [np.concatenate([np.linspace(pts[i], pts[i + 1], 18) for i in range(4)])]
    if sh == "cross":
        x0, y0, x1, y1 = [v * (W if i % 2 == 0 else H) for i, v in enumerate(L["box"])]
        return [np.linspace([x0, y0], [x1, y1], 20), np.linspace([x1, y0], [x0, y1], 20)]
    if sh == "check":
        x0, y0, x1, y1 = [v * (W if i % 2 == 0 else H) for i, v in enumerate(L["box"])]
        a = np.linspace([x0, (y0 + y1) / 2], [x0 + (x1 - x0) * 0.35, y1], 10)
        b = np.linspace([x0 + (x1 - x0) * 0.35, y1], [x1, y0], 22)
        return [np.concatenate([a, b])]
    if sh == "scribble":
        x0, y0, x1, y1 = [v * (W if i % 2 == 0 else H) for i, v in enumerate(L["box"])]
        rows = L.get("rows", 4)
        pts = []
        for r in range(rows * 2 + 1):
            y = y0 + (y1 - y0) * r / (rows * 2)
            pts.append([x0 if r % 2 == 0 else x1, y])
        pts = np.array(pts, np.float32)
        return [np.concatenate([np.linspace(pts[i], pts[i + 1], 12) for i in range(len(pts) - 1)])]
    return []


def _partial(strokes, p):
    """The first p (0..1) of the strokes by arc length."""
    lens = [np.sum(np.linalg.norm(np.diff(s, axis=0), axis=1)) for s in strokes]
    tot = sum(lens) or 1
    want = p * tot
    out = []
    for s, ln in zip(strokes, lens):
        if want <= 0:
            break
        if want >= ln:
            out.append(s)
            want -= ln
            continue
        seg = np.linalg.norm(np.diff(s, axis=0), axis=1)
        cum = np.concatenate([[0], np.cumsum(seg)])
        j = int(np.searchsorted(cum, want))
        j = max(1, min(len(s) - 1, j))
        f = (want - cum[j - 1]) / max(1e-6, seg[j - 1])
        tip = s[j - 1] + (s[j] - s[j - 1]) * f
        out.append(np.vstack([s[:j], tip[None]]))
        want = 0
    return out


def _draw_strokes(canvas, strokes, width, rgba, alpha=1.0, ss=2):
    if not strokes:
        return
    allp = np.concatenate(strokes)
    pad = width * 2 + 4
    x0, y0 = int(allp[:, 0].min() - pad), int(allp[:, 1].min() - pad)
    x1, y1 = int(allp[:, 0].max() + pad), int(allp[:, 1].max() + pad)
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    img = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = (rgba[0], rgba[1], rgba[2], int(rgba[3] * alpha))
    for s in strokes:
        pts = [((x - x0) * ss, (y - y0) * ss) for x, y in s]
        if len(pts) > 1:
            d.line(pts, fill=col, width=int(width * ss), joint="curve")
        r = width * ss / 2
        for px, py in (pts[0], pts[-1]):
            d.ellipse([px - r, py - r, px + r, py + r], fill=col)
    img = img.resize((w, h), Image.LANCZOS)
    canvas.alpha_composite(img, (x0, y0)) if x0 >= 0 and y0 >= 0 and x0 + w <= canvas.width and \
        y0 + h <= canvas.height else _clip_comp(canvas, img, x0, y0)


def _clip_comp(canvas, img, x, y):
    cx0, cy0 = max(0, x), max(0, y)
    cx1, cy1 = min(canvas.width, x + img.width), min(canvas.height, y + img.height)
    if cx1 > cx0 and cy1 > cy0:
        canvas.alpha_composite(img.crop((cx0 - x, cy0 - y, cx1 - x, cy1 - y)), (cx0, cy0))


def draw_marker(ctx, canvas, L, lt, alpha):
    W, H = ctx.W, ctx.H
    p = _eout(_clamp(lt / L.get("draw_dur", 0.55)))
    if L.get("shape") == "highlight":                       # highlighter swipe, left to right
        x0, y0, x1, y1 = L["box"]
        xe = x0 + (x1 - x0) * p
        rng = np.random.default_rng(_seed("hl", repr(L["box"])))
        top = [(x * W, (y0 + rng.uniform(-0.004, 0.004)) * H) for x in np.linspace(x0, xe, 8)]
        bot = [(x * W, (y1 + rng.uniform(-0.004, 0.004)) * H) for x in np.linspace(xe, x0, 8)]
        ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        c = _rgba(ctx.style, L.get("color", "#f7d84a"))
        ImageDraw.Draw(ov).polygon(top + bot, fill=(c[0], c[1], c[2], int(110 * alpha)))
        canvas.alpha_composite(ov)
        return
    strokes = _marker_paths(L, W, H)
    if L.get("boil", True):
        amp = L.get("boil_amp", 1.3)
        strokes = [s + _boil((L.get("shape"), i), lt, len(s), amp) for i, s in enumerate(strokes)]
    strokes = _partial(strokes, p)
    c = _rgba(ctx.style, L.get("color", "#d8443a"))
    _draw_strokes(canvas, strokes, L.get("width", 7) * W / 1920, c, alpha)


def draw_string(ctx, canvas, L, lt, alpha):
    """Red string pinned between points (evidence board), drawn from pin to pin."""
    W, H = ctx.W, ctx.H
    pts = [(x * W, y * H) for x, y in L["points"]]
    segs = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        dist = math.hypot(bx - ax, by - ay)
        sag = dist * L.get("sag", 0.06)
        s = np.linspace(0, 1, 30)
        xs = ax + (bx - ax) * s
        ys = ay + (by - ay) * s + np.sin(s * math.pi) * sag
        segs.append(np.stack([xs, ys], 1))
    p = _clamp(lt / L.get("draw_dur", 0.25 * len(segs) + 0.3))
    part = _partial(segs, _eout(p))
    c = _rgba(ctx.style, L.get("color", "#b8302a"))
    _draw_strokes(canvas, part, 3.2 * W / 1920, c, alpha)
    lens = [np.sum(np.linalg.norm(np.diff(s, axis=0), axis=1)) for s in segs]
    tot, acc = sum(lens) or 1, 0
    d = ImageDraw.Draw(canvas)
    r = 9 * W / 1920
    for i, (x, y) in enumerate(pts):
        reach = acc / tot
        if i < len(lens):
            acc += lens[i]
        if _eout(p) + 1e-6 >= reach:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 26, 24, int(255 * alpha)))
            d.ellipse([x - r * 0.75, y - r * 0.8, x + r * 0.55, y + r * 0.45], fill=(214, 52, 46, int(255 * alpha)))
            d.ellipse([x - r * 0.45, y - r * 0.55, x - r * 0.05, y - r * 0.15], fill=(255, 220, 210, int(220 * alpha)))


def draw_timeline(ctx, canvas, L, lt, alpha):
    st = ctx.style
    W, H = ctx.W, ctx.H
    x0, x1, y = L.get("x0", 0.1) * W, L.get("x1", 0.9) * W, L.get("y", 0.5) * H
    p = _eout(_clamp(lt / L.get("draw_dur", 1.2)))
    col = _rgba(st, L.get("color", "primary"))
    acc = _rgba(st, L.get("accent", "accent"))
    d = ImageDraw.Draw(canvas)
    lw = max(2, int(3 * W / 1920))
    xe = x0 + (x1 - x0) * p
    d.line([(x0, y), (xe, y)], fill=(col[0], col[1], col[2], int(220 * alpha)), width=lw)
    for i, ev in enumerate(L.get("events", [])):
        ex = x0 + (x1 - x0) * ev["pos"]
        if ex > xe + 1:
            continue
        k = _clamp((xe - ex) / (W * 0.05))
        active = i == L.get("active")
        tick = H * (0.022 if active else 0.014)
        d.line([(ex, y - tick), (ex, y + tick)], fill=(col[0], col[1], col[2], int(230 * alpha * k)), width=lw)
        if active:
            r = 10 * W / 1920
            d.ellipse([ex - r, y - r, ex + r, y + r], fill=(acc[0], acc[1], acc[2], int(255 * alpha * k)))
        yr = _text_img(st, ev.get("year", ""), "cond", int(46 * W / 1920), acc if active else col, track=2)
        a_img = yr if alpha * k > 0.99 else _fade(yr, alpha * k)
        canvas.alpha_composite(a_img, (int(ex - yr.width / 2), int(y - tick - yr.height - 6))) if ex - yr.width / 2 > 0 \
            else None
        if ev.get("label"):
            lb = _text_img(st, ev["label"], "type", int(26 * W / 1920), col)
            canvas.alpha_composite(_fade(lb, alpha * k), (int(ex - lb.width / 2), int(y + tick + 8)))


def _fade(img, a):
    if a >= 0.999:
        return img
    o = img.copy()
    o.putalpha(img.getchannel("A").point(lambda v: int(v * max(0.0, a))))
    return o


def draw_lower_third(ctx, canvas, L, lt, alpha):
    """Name / source super: a growing accent rule, condensed caps title, italic serif line under it."""
    st = ctx.style
    W, H = ctx.W, ctx.H
    x, y = L.get("x", 0.06) * W, L.get("y", 0.8) * H
    p1 = _eout(_clamp(lt / 0.45))
    p2 = _eout(_clamp((lt - 0.15) / 0.5))
    p3 = _eout(_clamp((lt - 0.35) / 0.5))
    acc = _rgba(st, L.get("accent", "accent"))
    d = ImageDraw.Draw(canvas)
    rule = L.get("rule_w", 0.06) * W
    d.rectangle([x, y, x + rule * p1, y + max(3, 4 * W / 1920)], fill=(acc[0], acc[1], acc[2], int(255 * alpha)))
    t = _text_img(st, L["title"].upper(), "cond", int(L.get("size", 48) * W / 1920), L.get("color", "primary"),
                  track=3, shadow=True)
    canvas.alpha_composite(_fade(t, alpha * p2), (int(x - 4), int(y + 14 + (1 - p2) * 14)))
    if L.get("sub"):
        s = _text_img(st, L["sub"], "serif_i", int(L.get("sub_size", 28) * W / 1920), L.get("sub_color", "#d9cdb4"),
                      shadow=True)
        canvas.alpha_composite(_fade(s, alpha * p3), (int(x - 2), int(y + 14 + t.height - 4 + (1 - p3) * 10)))


def draw_chapter(ctx, canvas, L, lt, alpha):
    """Chapter title card over a darkened (usually blurred) shot."""
    st = ctx.style
    W, H = ctx.W, ctx.H
    k = _ease(_clamp(lt / 0.6)) * alpha
    dark = Image.new("RGBA", canvas.size, (8, 10, 12, int(255 * L.get("dim", 0.62) * k)))
    canvas.alpha_composite(dark)
    p1 = _eout(_clamp((lt - 0.2) / 0.7))
    p2 = _eout(_clamp((lt - 0.45) / 0.9))
    cx, cy = L.get("x", 0.5) * W, L.get("y", 0.5) * H
    num = _text_img(st, f"CHAPTER {L.get('num', 1):02d}" if isinstance(L.get("num"), int) else str(L.get("num", "")),
                    "cond", int(34 * W / 1920), L.get("accent", "accent"), track=10)
    canvas.alpha_composite(_fade(num, alpha * p1), (int(cx - num.width / 2), int(cy - H * 0.11)))
    title = _text_img(st, L["title"], "serif", int(L.get("size", 84) * W / 1920), "primary", shadow=True)
    canvas.alpha_composite(_fade(title, alpha * p2), (int(cx - title.width / 2), int(cy - H * 0.05 + (1 - p2) * 18)))
    d = ImageDraw.Draw(canvas)
    lw = W * 0.12 * p2
    acc = _rgba(st, L.get("accent", "accent"))
    yl = cy - H * 0.05 + title.height + H * 0.025
    d.line([(cx - lw / 2, yl), (cx + lw / 2, yl)], fill=(acc[0], acc[1], acc[2], int(220 * alpha * p2)), width=2)


def draw_tag(ctx, canvas, L, lt, alpha):
    st = ctx.style
    W, H = ctx.W, ctx.H
    k = _eout(_clamp(lt / 0.35)) * alpha
    t = _text_img(st, L["text"], L.get("font", "type"), int(L.get("size", 26) * W / 1920), L.get("color", "primary"),
                  track=L.get("track", 2))
    pad = int(10 * W / 1920)
    box = Image.new("RGBA", (t.width + pad * 2, t.height + pad), (10, 12, 14, int(150 * k)))
    box.alpha_composite(_fade(t, k), (pad, pad // 2))
    x, y = L.get("x", 0.035) * W, L.get("y", 0.05) * H
    if L.get("align") == "right":
        x -= box.width
    canvas.alpha_composite(box, (int(x), int(y)))


def draw_direct(ctx, canvas, L, lt, alpha):
    fn = {"marker": draw_marker, "string": draw_string, "timeline": draw_timeline,
          "lower_third": draw_lower_third, "chapter": draw_chapter, "tag": draw_tag}[L["type"]]
    fn(ctx, canvas, L, lt, alpha)


# ------------------------------------------------------------------ transitions
def _hblur(img, k):
    W, H = img.size
    if k < 2:
        return img
    return img.resize((max(8, int(W / k)), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)


_TEAR = {}


def _tear_edge(H, seed=3):
    if (H, seed) not in _TEAR:
        rng = np.random.default_rng(seed)
        n = np.cumsum(rng.normal(0, 1, H // 6 + 2))
        n = np.interp(np.arange(H), np.linspace(0, H, len(n)), n)
        n = (n - n.mean()) / (np.abs(n).max() + 1e-6)
        _TEAR[(H, seed)] = n
    return _TEAR[(H, seed)]


def transition(kind, prev, cur, p, W, H):
    if kind == "whip":                                       # fast pan with motion blur, direction left
        off = int(W * _ease(p))
        blur = 3 + 34 * math.sin(p * math.pi)
        a, b = _hblur(prev, blur), _hblur(cur, blur)
        out = Image.new("RGBA", (W, H))
        out.paste(a, (-off, 0))
        out.paste(b, (W - off, 0))
        return out
    if kind == "dip":
        if p < 0.5:
            return Image.blend(prev, Image.new("RGBA", (W, H), (0, 0, 0, 255)), _ease(p * 2))
        return Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), cur, _ease(p * 2 - 1))
    if kind == "burn":                                       # over-exposed warm flash, like a film splice
        k = math.sin(p * math.pi)
        base = prev if p < 0.5 else cur
        a = np.asarray(base.convert("RGB")).astype(np.float32)
        a = a + k * np.array([255, 190, 120], np.float32) * 0.85
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    if kind == "paper":                                      # a torn-paper edge sweeps across
        edge = _tear_edge(H)
        xs = (-0.1 + 1.2 * _ease(p)) * W + edge * W * 0.03
        cols = np.arange(W)[None, :]
        mask = (cols < xs[:, None]).astype(np.uint8) * 255
        m = Image.fromarray(mask, "L")
        out = prev.copy()
        out.paste(cur, (0, 0), m)
        rim = Image.fromarray(((np.abs(cols - xs[:, None]) < 7) & (cols >= xs[:, None] - 1)).astype(np.uint8) * 230, "L")
        out.paste(Image.new("RGBA", (W, H), (240, 232, 214, 255)), (0, 0), rim)
        return out
    return None
