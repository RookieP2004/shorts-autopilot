"""Night-set toolkit (v4): the second house mood for dark-files, scams, money traps and big reveals.

The bright town stays the default; a job opts in with "look": "night" (merges style.looks.night: highlight captions,
night grade, rim light on Ved and the townspeople). Every piece below also works in a bright video.

Layers (all positions are frame fractions; `at` = when the layer appears; times inside a layer are seconds after `at`):
  hud      a number chip: dark rounded card, thin glowing border, small caps label + big number that ticks.
           {"label", "value" | "steps": [[t, v], ...], "prefix", "suffix", "indian": true, "tone", "size", "sub"}
  eqbar    the running equation under a hud: {"keys": [[t, "8,000 ÷ 2"], ...]}; "^3" = superscript, *answer* = tone colour
  tracker  step circles that tick green one by one: {"n": 3, "done": [t1, t2, t3], "size"}
  stamp    a slanted rubber-stamp verdict that slams in: {"text": "THE TRAP", "tone": "red", "angle": -8, "size"}
  optcard  an option card that gets a red cross or green tick: {"label", "text", "sub", "tone", "verdict": "cross"|"tick", "verdict_at", "w"}
  phone    a glossy 3D phone cut-out (blendkit.phone_sprite) with a LIVE fictional screen (autopilot.devices) composited
           into it; it can turn: {"sprite", "screen": {...}, "w", "tilt": [[t, yaw_deg, pitch_deg], ...], "sheen": true}
  crowd    (world) a carpet of tiny figures standing on a plate's floor, projected with the plate's camera; steps do the
           maths on screen: {"plate", "area": [x0, x1, y0, y1], "n", "fig_h", "steps": [{"at", "split": "x"|"y",
           "colors": [..]}, {"at", "keep": 0, "lost": "red"}, {"at", "glow": "green"}], "aisle": [x, half_w], "depth": [y0, y1]}
  nodes    (world) a decision tree / flow as glowing nodes and lines floating in 3D, built step by step, slowly orbiting:
           {"nodes": [{"id", "pos": [x, y, z], "at", "tone", "label"}], "edges": [[a, b, at, tone]], "yaw": [d0, d1]}
  burst    (world) cash / coin burst with motion blur: {"sprites": [png, ...], "n", "origin": [x, y], "dur", "spread"}
Colour meaning is fixed inside a video: green = survives / true, red = scam / danger, gold = money, blue = neutral data.
"""
import math
import os
import json
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .spec import color, hex_rgba

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TONES = {"green": "#35e08a", "red": "#ff3b4a", "gold": "#f4c04e", "blue": "#4aa3ff", "white": "#eef2f8", "grey": "#5b6372",
         "violet": "#9b6bff"}
FONTS = {"num": "fonts/Poppins-ExtraBold.ttf", "ui": "fonts/Poppins-SemiBold.ttf", "mono": "fonts/CourierPrime-Bold.ttf",
         "stamp": "fonts/Anton-Regular.ttf"}
DIRECT = {"crowd", "nodes", "burst"}                          # drawn straight into the world (under the camera move)
IMAGE = {"hud", "eqbar", "tracker", "stamp", "optcard", "phone"}


def tone(style, name, default="blue"):
    c = name or default
    c = TONES.get(c, c)
    return color(style, c) if style else c


def rgb(c):
    return hex_rgba(c)[:3]


@lru_cache(maxsize=64)
def font(kind, size):
    return ImageFont.truetype(os.path.join(ROOT, FONTS.get(kind, kind)), max(6, int(size)))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eout(p):
    return 1 - (1 - clamp(p)) ** 3


def eback(p, s=1.7):
    p = clamp(p) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def fmt_num(v, indian=False, dec=0):
    """1,00,00,000 (Indian grouping) or 10,000,000."""
    neg = v < 0
    v = abs(v)
    s = f"{v:.{dec}f}"
    ip, _, fp = s.partition(".")
    if indian and len(ip) > 3:
        head, tail = ip[:-3], ip[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        ip = ",".join(parts + [tail])
    elif not indian:
        ip = f"{int(ip):,}"
    return ("-" if neg else "") + ip + ("." + fp if fp else "")


def _glow_box(w, h, r, border, col, fill=(8, 12, 22, 236), glow=14):
    """A dark rounded card with a thin glowing border."""
    pad = glow * 2
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    g = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle([pad, pad, pad + w, pad + h], radius=r, outline=(*col, 200), width=max(2, border * 2))
    g = g.filter(ImageFilter.GaussianBlur(glow / 2))
    im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], radius=r, fill=fill, outline=(*col, 255), width=border)
    return im, pad


# ------------------------------------------------------------------ hud chip + equation bar
def hud_value(L, lt):
    if "steps" in L:
        st = sorted(L["steps"])
        v = st[0][1]
        prev = v
        for t, val in st:
            if lt >= t:
                prev, v = v, val
                p = eout((lt - t) / L.get("count_dur", 0.5))
                v = prev + (val - prev) * p
        return v
    if "to" in L:
        p = eout(lt / L.get("count_dur", 1.0))
        return L.get("from", 0) + (L["to"] - L.get("from", 0)) * p
    return L.get("value", 0)


def hud_image(style, L, lt, W=1080):
    s = W / 1080 * L.get("size", 1.0)
    col = rgb(tone(style, L.get("tone"), "blue"))
    v = hud_value(L, lt)
    txt = L["text"] if "text" in L else f"{L.get('prefix', '')}{fmt_num(round(v, L.get('decimals', 0)), L.get('indian', True), L.get('decimals', 0))}{L.get('suffix', '')}"
    fn, fl = font("num", 92 * s), font("mono", 26 * s)
    label = L.get("label", "").upper()
    tw = max(fn.getlength(txt) if "width_of" not in L else fn.getlength(L["width_of"]), fl.getlength(label)) + 80 * s
    h = int((150 if label else 118) * s)
    im, pad = _glow_box(int(tw), h, int(26 * s), max(2, int(3 * s)), col)
    d = ImageDraw.Draw(im)
    cx = pad + tw / 2
    if label:
        d.text((cx, pad + 30 * s), label, font=fl, fill=(*col, 255), anchor="mm")
    d.text((cx, pad + h - 58 * s), txt, font=fn, fill=(246, 248, 252, 255), anchor="mm")
    if L.get("sub"):
        fs = font("ui", 30 * s)
        sub = Image.new("RGBA", (max(im.width, int(fs.getlength(L["sub"]) + 40 * s)), int(54 * s)), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sub)
        sd.rounded_rectangle([0, 0, sub.width - 1, sub.height - 1], radius=int(14 * s), fill=(8, 12, 22, 220))
        sd.text((sub.width / 2, 27 * s), L["sub"], font=fs, fill=(232, 236, 244, 255), anchor="mm")
        out = Image.new("RGBA", (max(im.width, sub.width), im.height + sub.height), (0, 0, 0, 0))
        out.alpha_composite(im, ((out.width - im.width) // 2, 0))
        out.alpha_composite(sub, ((out.width - sub.width) // 2, im.height - int(pad * 0.6)))
        im = out
    return im


def _rich(text, base_font, sup_font, base_col, acc_col):
    """Tokens: '^x' = superscript, *x* = accent colour. Returns list of (text, font, colour, raise)."""
    out, acc = [], False
    i = 0
    buf = ""
    while i < len(text):
        ch = text[i]
        if ch == "*":
            if buf:
                out.append((buf, base_font, acc_col if acc else base_col, 0))
                buf = ""
            acc = not acc
        elif ch == "^":
            if buf:
                out.append((buf, base_font, acc_col if acc else base_col, 0))
                buf = ""
            j = i + 1
            while j < len(text) and text[j].isalnum():
                j += 1
            out.append((text[i + 1:j], sup_font, acc_col if acc else base_col, 1))
            i = j - 1
        else:
            buf += ch
        i += 1
    if buf:
        out.append((buf, base_font, acc_col if acc else base_col, 0))
    return out


def eqbar_image(style, L, lt, W=1080):
    s = W / 1080 * L.get("size", 1.0)
    keys = [k for k in L["keys"] if lt >= k[0]]
    if not keys:
        return None
    t0, text = keys[-1]
    col = rgb(tone(style, L.get("tone"), "green"))
    fb, fs = font("stamp", 74 * s), font("stamp", 42 * s)
    toks = _rich(text, fb, fs, (246, 248, 252), col)
    tw = sum(f.getlength(t) for t, f, _, _ in toks)
    w = max(int(L.get("w", 0.0) * W), int(tw + 90 * s))
    h = int(106 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=(4, 6, 12, 232), outline=(60, 70, 92, 255), width=max(1, int(2 * s)))
    x = (w - tw) / 2
    for t, f, c, up in toks:
        y = h / 2 - (24 * s if up else 0)
        d.text((x, y), t, font=f, fill=(*c, 255), anchor="lm")
        x += f.getlength(t)
    k = eout((lt - t0) / 0.25)                                      # the newest step lands with a small bump
    if k < 1:
        sc = 1 + 0.08 * (1 - k)
        im = im.resize((int(w * sc), int(h * sc)), Image.BICUBIC)
    return im


# ------------------------------------------------------------------ tracker, stamp, option card
def tracker_image(style, L, lt, W=1080):
    s = W / 1080 * L.get("size", 1.0)
    n = L.get("n", 3)
    done = L.get("done", [])
    r = int(34 * s)
    gap = int(22 * s)
    w = n * 2 * r + (n - 1) * gap + 8
    im = Image.new("RGBA", (w + 16, 2 * r + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    green = rgb(TONES["green"])
    ndone = sum(1 for t in done if lt >= t)
    f = font("num", 30 * s)
    for i in range(n):
        cx, cy = 8 + r + i * (2 * r + gap), 8 + r
        if i < ndone:
            p = eback((lt - done[i]) / 0.3)
            rr = r * max(0.2, p)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(*green, 255))
            d.line([(cx - rr * 0.42, cy + rr * 0.02), (cx - rr * 0.1, cy + rr * 0.34), (cx + rr * 0.46, cy - rr * 0.32)],
                   fill=(255, 255, 255, 255), width=max(3, int(rr * 0.2)), joint="curve")
        elif i == ndone:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 248, 252, 255))
            d.text((cx, cy), str(i + 1), font=f, fill=(10, 14, 24, 255), anchor="mm")
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 14, 24, 230), outline=(120, 130, 150, 255), width=max(2, int(2 * s)))
            d.text((cx, cy), str(i + 1), font=f, fill=(220, 226, 236, 255), anchor="mm")
    return im


@lru_cache(maxsize=32)
def _stamp_base(text, col, size, angle, seed):
    f = font("stamp", size)
    tw = f.getlength(text)
    pad = size * 0.32
    w, h = int(tw + pad * 2), int(size * 1.25 + pad * 2)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    b = max(4, size // 14)
    d.rounded_rectangle([b, b, w - b, h - b], radius=size // 8, outline=(*col, 255), width=b)
    d.rounded_rectangle([b * 3, b * 3, w - b * 3, h - b * 3], radius=size // 10, outline=(*col, 255), width=max(2, b // 2))
    d.text((w / 2, h / 2), text, font=f, fill=(*col, 255), anchor="mm")
    rng = np.random.default_rng(seed)                               # worn ink: speckle holes in the stamp
    a = np.asarray(im.getchannel("A")).astype(np.float32)
    noise = rng.random(a.shape)
    a = a * (noise > 0.13) * (0.82 + 0.18 * rng.random(a.shape))
    im.putalpha(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)))
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def stamp_image(style, L, lt, W=1080):
    s = W / 1080
    col = rgb(tone(style, L.get("tone"), "red"))
    im = _stamp_base(L["text"], col, int(L.get("size", 120) * s), L.get("angle", -8), L.get("seed", 3))
    p = clamp(lt / 0.16)                                            # slam: big and faint -> lands hard
    sc = 1.9 - 0.9 * eout(p)
    if sc != 1:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if p < 1:
        a = im.getchannel("A").point(lambda v: int(v * (0.35 + 0.65 * p)))
        im.putalpha(a)
    return im


def optcard_image(style, L, lt, W=1080):
    s = W / 1080
    col = rgb(tone(style, L.get("tone"), "blue"))
    w = int(L.get("w", 0.44) * W)
    fl, fb, fs = font("mono", 22 * s), font("stamp", 92 * s), font("ui", 20 * s)
    lines = L.get("text", "").split("\n")
    h = int((70 + 92 * len(lines) + (40 if L.get("sub") else 10)) * s)
    im, pad = _glow_box(w, h, int(20 * s), max(2, int(3 * s)), col, fill=(*col, 245), glow=10)
    d = ImageDraw.Draw(im)
    ink = (10, 14, 24, 255) if sum(col) > 380 else (250, 250, 252, 255)
    lab = L.get("label", "").upper()
    if lab:
        lw = fl.getlength(lab) + 24 * s
        d.rounded_rectangle([pad + 18 * s, pad + 16 * s, pad + 18 * s + lw, pad + 50 * s], radius=8 * s, fill=(10, 14, 24, 235))
        d.text((pad + 30 * s, pad + 33 * s), lab, font=fl, fill=(*col, 255), anchor="lm")
    y = pad + 64 * s
    for ln in lines:
        while fb.getlength(ln) > w - 40 * s and fb.size > 30:
            fb = font("stamp", fb.size - 4)
        d.text((pad + w / 2, y + 46 * s), ln, font=fb, fill=ink, anchor="mm")
        y += 92 * s
    if L.get("sub"):
        d.text((pad + w / 2, y + 16 * s), L["sub"].upper(), font=fs, fill=ink, anchor="mm")
    v = L.get("verdict")
    if v and lt >= L.get("verdict_at", 0):
        p = eout((lt - L.get("verdict_at", 0)) / 0.25)
        if v == "cross":
            dim = Image.new("RGBA", im.size, (6, 8, 14, int(120 * p)))
            dim.putalpha(Image.fromarray((np.asarray(im.getchannel("A")) * (0.5 * p)).astype(np.uint8)))
            im.alpha_composite(dim)
            red = rgb(TONES["red"])
            x0, y0, x1, y1 = pad + 14 * s, pad + 14 * s, pad + w - 14 * s, pad + h - 14 * s
            wd = max(6, int(14 * s))
            d.line([(x0, y0), (x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)], fill=(*red, 255), width=wd)
            q = eout((lt - L.get("verdict_at", 0) - 0.12) / 0.25)
            if q > 0:
                d.line([(x1, y0), (x1 - (x1 - x0) * q, y0 + (y1 - y0) * q)], fill=(*red, 255), width=wd)
        else:
            green = rgb(TONES["green"])
            r = max(1.0, 34 * s * eback(p))
            cx, cy = pad + w - 14 * s, pad + 14 * s
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*green, 255), outline=(255, 255, 255, 255), width=max(2, int(3 * s)))
            d.line([(cx - r * 0.42, cy), (cx - r * 0.1, cy + r * 0.32), (cx + r * 0.46, cy - r * 0.32)], fill=(255, 255, 255, 255),
                   width=max(3, int(r * 0.2)))
    return im


# ------------------------------------------------------------------ phone with a live screen
def _persp_coeffs(src, dst):
    """Coefficients for Image.transform(PERSPECTIVE) mapping output points `dst` back to input points `src`."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


@lru_cache(maxsize=8)
def _sprite(path):
    im = Image.open(path).convert("RGBA")
    meta = json.load(open(path[:-4] + ".json")) if os.path.exists(path[:-4] + ".json") else {}
    return im, meta


def _tilt(L, lt):
    keys = L.get("tilt")
    if not keys:
        return 0.0, 0.0
    if lt <= keys[0][0]:
        return keys[0][1], keys[0][2]
    for (t0, y0, p0), (t1, y1, p1) in zip(keys, keys[1:]):
        if t0 <= lt < t1:
            q = (lt - t0) / max(0.01, t1 - t0)
            q = 3 * q * q - 2 * q * q * q
            return y0 + (y1 - y0) * q, p0 + (p1 - p0) * q
    return keys[-1][1], keys[-1][2]


def card_turn(im, yaw, pitch, f_mult=2.4):
    """Rotate a flat cut-out in 3D (yaw about the vertical axis, pitch about the horizontal) with real perspective."""
    if abs(yaw) < 0.05 and abs(pitch) < 0.05:
        return im
    w, h = im.size
    f = f_mult * max(w, h)
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    pts = []
    for x, y in ((0, 0), (w, 0), (w, h), (0, h)):
        X, Y, Z = x - w / 2, y - h / 2, 0.0
        X, Z = X * cy_ + Z * sy_, -X * sy_ + Z * cy_
        Y, Z = Y * cp - Z * sp, Y * sp + Z * cp
        k = f / (f + Z)
        pts.append((X * k, Y * k))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ox, oy = -min(xs), -min(ys)
    ow, oh = int(math.ceil(max(xs) - min(xs))), int(math.ceil(max(ys) - min(ys)))
    dst = [(x + ox, y + oy) for x, y in pts]
    co = _persp_coeffs([(0, 0), (w, 0), (w, h), (0, h)], dst)
    return im.transform((max(1, ow), max(1, oh)), Image.PERSPECTIVE, co, Image.BICUBIC)


def phone_image(style, L, lt, W=1080):
    from . import devices
    body, meta = _sprite(L["sprite"])
    tw = int(L.get("w", 0.6) * W)
    k = tw / body.width                                             # work at the final size: the live screen stays sharp
    im = body.resize((tw, max(1, int(body.height * k))), Image.LANCZOS) if abs(k - 1) > 0.01 else body.copy()
    q = [[x * k, y * k] for x, y in meta.get("screen", [])]
    if q and L.get("screen"):
        xs, ys = [p[0] for p in q], [p[1] for p in q]
        sw, sh = int(max(xs) - min(xs)), int(max(ys) - min(ys))
        rw = L.get("ui_w", 430)                                   # smaller virtual screen = bigger, legible UI
        scr = devices.screen(L["screen"], lt, rw, int(rw * sh / max(1, sw))).resize((sw, sh), Image.LANCZOS)
        co = _persp_coeffs([(0, 0), (sw, 0), (sw, sh), (0, sh)], [tuple(p) for p in q])
        layer = scr.convert("RGBA").transform(im.size, Image.PERSPECTIVE, co, Image.BICUBIC)
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([min(xs) + 2, min(ys) + 2, max(xs) - 2, max(ys) - 2], radius=int(sw * 0.07), fill=255)
        im.paste(layer, (0, 0), mask)
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))                # glass: a faint diagonal reflection over the screen
        gd = ImageDraw.Draw(gl)
        gd.polygon([(min(xs), min(ys)), (min(xs) + sw * 0.55, min(ys)), (min(xs), min(ys) + sh * 0.42)], fill=(255, 255, 255, 18))
        im.alpha_composite(Image.composite(gl, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask))
    yaw, pitch = _tilt(L, lt)
    if L.get("sheen", True):                                        # a light streak that slides as the phone turns
        a = im.getchannel("A")
        sh_ = Image.new("L", im.size, 0)
        pos = 0.5 + yaw / 60.0 + 0.08 * math.sin(lt * 0.8)
        x = pos * im.width
        ImageDraw.Draw(sh_).polygon([(x - im.width * 0.1, 0), (x + im.width * 0.05, 0), (x - im.width * 0.25, im.height),
                                     (x - im.width * 0.4, im.height)], fill=34)
        sh_ = sh_.filter(ImageFilter.GaussianBlur(im.width * 0.04))
        from PIL import ImageChops
        sh_ = ImageChops.multiply(sh_, a)
        white = Image.new("RGBA", im.size, (255, 255, 255, 0))
        white.putalpha(sh_)
        im.alpha_composite(white)
    return card_turn(im, yaw, pitch)


def layer_image(style, L, lt, W):
    fn = {"hud": hud_image, "eqbar": eqbar_image, "tracker": tracker_image, "stamp": stamp_image, "optcard": optcard_image,
          "phone": phone_image}[L["type"]]
    return fn(style, L, lt, W)


# ------------------------------------------------------------------ crowd: a big number you can see, doing the maths
class _Proj:
    def __init__(self, plate_json):
        d = json.load(open(plate_json))
        self.Minv = np.linalg.inv(np.array(d["matrix_world"]))
        self.w, self.h = d["w"], d["h"]
        self.f = d["lens"] / d["sensor"] * (max(self.w, self.h) if d.get("fit", "AUTO") == "AUTO"
                                            else (self.w if d["fit"] == "HORIZONTAL" else self.h))

    def __call__(self, P):                                          # P: (n, 3) world points -> (n, 2) frame fractions
        Q = np.c_[P, np.ones(len(P))] @ self.Minv.T
        depth = -Q[:, 2]
        sx = self.w / 2 + self.f * Q[:, 0] / depth
        sy = self.h / 2 - self.f * Q[:, 1] / depth
        return np.c_[sx / self.w, sy / self.h]


@lru_cache(maxsize=16)
def _crowd_layout(plate, area, n, fig_h, seed, aisle):
    x0, x1, y0, y1 = area
    aspect = (x1 - x0) / max(0.01, y1 - y0)
    cols = max(1, int(round(math.sqrt(n * aspect))))
    rows = max(1, int(math.ceil(n / cols)))
    rng = np.random.default_rng(seed)
    c, r = np.meshgrid(np.arange(cols), np.arange(rows))
    c, r = c.ravel()[:n], r.ravel()[:n]
    u = (c + 0.5) / cols
    v = (r + 0.5) / rows
    jit = 0.35
    X = x0 + u * (x1 - x0) + (rng.random(len(u)) - 0.5) * (x1 - x0) / cols * jit
    Y = y0 + v * (y1 - y0) + (rng.random(len(u)) - 0.5) * (y1 - y0) / rows * jit
    keep = np.ones(len(u), bool)
    if aisle:
        keep = np.abs(X - aisle[0]) > aisle[1]
    pr = _Proj(plate)
    feet = pr(np.c_[X, Y, np.zeros_like(X)])
    head = pr(np.c_[X, Y, np.full_like(X, fig_h)])
    order = np.argsort(-Y)                                          # far rows first
    return u, v, X, Y, feet, head, keep, order


def _crowd_state(style, L, lt, u, v):
    """Per-figure colour (n, 3), alpha (n,), alive mask, glow mask after applying the steps up to lt."""
    n = len(u)
    base = np.array(rgb(tone(style, L.get("color", "#a9b2c4"))), float)
    col = np.tile(base, (n, 1))
    alpha = np.ones(n)
    alive = np.ones(n, bool)
    group = np.zeros(n, int)
    glow = np.zeros(n, bool)
    for stp in L.get("steps", []):
        t0 = stp.get("at", 0.0)
        if lt < t0:
            break
        dur = max(1e-3, stp.get("dur", 0.7))
        if "split" in stp:
            ax = u if stp["split"] == "x" else v
            k = len(stp.get("colors", [None, None]))
            idx = np.where(alive)[0]
            if len(idx):
                ranks = np.argsort(np.argsort(ax[idx]))
                group[idx] = np.minimum(k - 1, (ranks * k) // len(idx))
                lo, hi = ax[idx].min(), ax[idx].max()
                wave = (ax - lo) / max(1e-6, hi - lo)
                p = np.clip((lt - t0 - wave * dur * 0.6) / (dur * 0.4), 0, 1)
                for g, cname in enumerate(stp.get("colors", [])):
                    m = alive & (group == g)
                    tgt = np.array(rgb(tone(style, cname)), float)
                    col[m] = col[m] + (tgt - col[m]) * p[m, None]
        if "keep" in stp:
            lost = alive & (group != stp["keep"])
            p = clamp((lt - t0) / (dur * 0.5))
            q = clamp((lt - t0 - dur) / 0.6)
            red = np.array(rgb(tone(style, stp.get("lost", "red"))), float)
            grey = np.array(rgb(TONES["grey"]), float)
            c2 = red + (grey - red) * q
            col[lost] = col[lost] + (c2 - col[lost]) * p
            alpha[lost] = 1 - (1 - stp.get("lost_alpha", 0.28)) * q
            if lt >= t0:
                alive = alive & (group == stp["keep"])
                group[:] = 0
        if "glow" in stp:
            p = clamp((lt - t0) / dur)
            tgt = np.array(rgb(tone(style, stp["glow"])), float)
            col[alive] = col[alive] + (tgt - col[alive]) * p
            glow = alive.copy() if p > 0 else glow
        if "color" in stp:                                          # recolour the living
            p = clamp((lt - t0) / dur)
            tgt = np.array(rgb(tone(style, stp["color"])), float)
            col[alive] = col[alive] + (tgt - col[alive]) * p
    return col, alpha, alive, glow


def draw_crowd(ctx, canvas, L, lt, alpha_l):
    W, H = ctx.W, ctx.H
    area = tuple(L["area"])
    u, v, X, Y, feet, head, keep, order = _crowd_layout(L["plate"], area, L.get("n", 2400), L.get("fig_h", 0.3),
                                                        L.get("seed", 3), tuple(L["aisle"]) if L.get("aisle") else None)
    col, alpha, alive, glow = _crowd_state(ctx.style, L, lt, u, v)
    dep = L.get("depth")
    appear = L.get("in_dur", 0.8)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)) if glow.any() else None
    gd = ImageDraw.Draw(gl) if gl is not None else None
    shadow = L.get("shadow", 0.0 if ctx.job.get("look") == "night" else 0.28)   # daylight sets need them; night has one spot
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0)) if shadow else None
    sd = ImageDraw.Draw(sl) if sl is not None else None
    vmax = v.max() if len(v) else 1
    for i in order:
        if not keep[i]:
            continue
        if dep and not (dep[0] <= Y[i] < dep[1]):
            continue
        a = alpha[i] * alpha_l
        if appear:                                                  # rows fill in from the back
            a *= clamp((lt - (1 - v[i] / vmax) * appear * 0.7) / (appear * 0.3))
        if a <= 0.02:
            continue
        fx, fy = feet[i][0] * W, feet[i][1] * H
        hy = head[i][1] * H
        hp = fy - hy
        c = tuple(int(x) for x in col[i]) + (int(255 * a),)
        if shadow and hp >= 3:                                      # contact shadow: figures stand ON the floor
            sw = hp * 0.32
            sd.ellipse([fx - sw, fy - sw * 0.28, fx + sw * 1.15, fy + sw * 0.28], fill=(0, 0, 0, int(shadow * 255 * a)))
        if hp < 4.5:
            r = max(1.0, hp * 0.35)
            d.ellipse([fx - r, fy - hp * 0.7 - r, fx + r, fy - hp * 0.7 + r], fill=c)
        else:
            bw = hp * 0.2
            hr = hp * 0.12
            ol = tuple(int(x * 0.62) for x in col[i]) + (int(255 * a),) if hp >= 7 else None   # outline: each person reads
            olw = max(1, int(hp / 26))
            d.rounded_rectangle([fx - bw, fy - hp * 0.72, fx + bw, fy], radius=bw * 0.8, fill=c, outline=ol, width=olw)
            if hp >= 7:                                             # form shading: the side away from the light
                sh = tuple(int(x * 0.8) for x in col[i]) + (int(255 * a),)
                d.rounded_rectangle([fx + bw * 0.25, fy - hp * 0.68, fx + bw - olw, fy - olw], radius=bw * 0.5, fill=sh)
            hc = tuple(min(255, int(x * 1.12)) for x in col[i]) + (int(255 * a),)
            d.ellipse([fx - hr, hy, fx + hr, hy + hr * 2], fill=hc, outline=ol, width=olw)
        if gd is not None and glow[i]:
            r = max(2.0, hp * 0.45)
            gd.ellipse([fx - r, fy - hp * 0.6 - r, fx + r, fy - hp * 0.6 + r], fill=tuple(int(x) for x in col[i]) + (int(150 * a),))
    if sl is not None:
        canvas.alpha_composite(sl.filter(ImageFilter.GaussianBlur(max(1.5, W / 700))))
    if gl is not None:
        canvas.alpha_composite(gl.filter(ImageFilter.GaussianBlur(max(3, W / 180))))
    canvas.alpha_composite(layer)


def crowd_count(L, lt):
    """How many figures are still 'alive' at lt (for checking the maths in tests / for a hud)."""
    u = np.linspace(0, 1, L.get("n", 2400))
    return int(_crowd_state(None, dict(L, color="#ffffff"), lt, u, u)[2].sum())


# ------------------------------------------------------------------ nodes: a decision tree floating in the dark
@lru_cache(maxsize=64)
def _orb(r, c):
    s = int(r * 4)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([s / 2 - r * 1.6, s / 2 - r * 1.6, s / 2 + r * 1.6, s / 2 + r * 1.6], fill=(*c, 90))
    im = im.filter(ImageFilter.GaussianBlur(r * 0.5))
    d = ImageDraw.Draw(im)
    d.ellipse([s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r], fill=(*c, 255))
    hl = r * 0.45
    d.ellipse([s / 2 - r * 0.55 - hl / 2, s / 2 - r * 0.55 - hl / 2, s / 2 - r * 0.55 + hl / 2, s / 2 - r * 0.55 + hl / 2],
              fill=(255, 255, 255, 170))
    return im


def draw_nodes(ctx, canvas, L, lt, alpha_l):
    W, H = ctx.W, ctx.H
    st = ctx.style
    dur = max(0.1, L.get("span", 4.0))
    y0, y1 = L.get("yaw", [-14, 10])
    yaw = math.radians(y0 + (y1 - y0) * clamp(lt / dur))
    cam = L.get("cam", {})
    dist, fov = cam.get("dist", 7.0), cam.get("fov", 42)
    f = (W / 2) / math.tan(math.radians(fov) / 2)
    cx, cy = L.get("x", 0.5) * W, L.get("y", 0.5) * H
    tilt = math.radians(cam.get("pitch", 8))
    P = {}
    for nd in L["nodes"]:
        x, y, z = nd["pos"]                                         # x right, y up, z towards the viewer
        X, Z = x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw)
        Y, Z = y * math.cos(tilt) - Z * math.sin(tilt), y * math.sin(tilt) + Z * math.cos(tilt)
        k = f / (dist - Z)
        P[nd["id"]] = (cx + X * k, cy - Y * k, k, Z)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, gd = ImageDraw.Draw(layer), ImageDraw.Draw(glow)
    for e in L.get("edges", []):
        a, b, t0 = e[0], e[1], e[2] if len(e) > 2 else 0
        if lt < t0 or a not in P or b not in P:
            continue
        p = eout((lt - t0) / 0.35)
        c = rgb(tone(st, e[3] if len(e) > 3 else "white"))
        (ax, ay, _, _), (bx, by, _, _) = P[a], P[b]
        ex, ey = ax + (bx - ax) * p, ay + (by - ay) * p
        gd.line([(ax, ay), (ex, ey)], fill=(*c, int(200 * alpha_l)), width=int(W / 90))
        d.line([(ax, ay), (ex, ey)], fill=(*c, int(255 * alpha_l)), width=max(2, int(W / 300)))
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(W / 160)), (0, 0))
    canvas.alpha_composite(layer)
    for nd in sorted(L["nodes"], key=lambda n_: P[n_["id"]][3]):     # far nodes first
        t0 = nd.get("at", 0)
        if lt < t0:
            continue
        p = eback((lt - t0) / 0.3)
        sx, sy, k, _ = P[nd["id"]]
        c = rgb(tone(st, nd.get("tone", "white")))
        r = max(4, int(nd.get("r", 0.16) * k * p))
        orb = _orb(r, c)
        if alpha_l < 1:
            orb = orb.copy()
            orb.putalpha(orb.getchannel("A").point(lambda v: int(v * alpha_l)))
        canvas.alpha_composite(orb, (int(sx - orb.width / 2), int(sy - orb.height / 2)))
        if nd.get("label"):
            chip = hud_image(st, {"text": nd["label"], "tone": nd.get("tone", "white"), "size": nd.get("label_size", 0.42)}, 9, W)
            side = nd.get("label_side", "right")
            lx = sx + (r + chip.width * 0.42) * (1 if side == "right" else -1)
            canvas.alpha_composite(chip, (int(lx - chip.width / 2), int(sy - chip.height / 2)))


# ------------------------------------------------------------------ cash / coin burst with motion blur
@lru_cache(maxsize=16)
def _piece(path, w):
    im = Image.open(path).convert("RGBA")
    return im.resize((w, max(1, int(im.height * w / im.width))), Image.LANCZOS)


def draw_burst(ctx, canvas, L, lt, alpha_l):
    W, H = ctx.W, ctx.H
    if lt < 0:
        return
    rng = np.random.default_rng(L.get("seed", 9))
    n = L.get("n", 22)
    ox, oy = L.get("origin", [0.5, 0.6])
    dur = L.get("dur", 1.8)
    spr = L["sprites"]
    sp = L.get("spread", 1.0)
    for i in range(n):
        delay = rng.random() * L.get("stagger", 0.35)
        ang = rng.uniform(-math.pi * 0.95, -math.pi * 0.05) if L.get("up", True) else rng.uniform(0, 2 * math.pi)
        spd = rng.uniform(0.6, 1.25) * sp
        vx, vy = math.cos(ang) * spd * 0.9, math.sin(ang) * spd * 1.15
        rot0, vr = rng.uniform(0, 360), rng.uniform(-420, 420)
        k = i % len(spr)
        size = int(W * rng.uniform(0.12, 0.22) * L.get("size", 1.0) * (L.get("sizes") or [1.0] * len(spr))[k])
        path = spr[k]
        t = lt - delay
        if t < 0 or t > dur:
            continue
        g = L.get("gravity", 0.9)
        x = ox + vx * t * 0.55
        y = oy + vy * t * 0.55 + 0.5 * g * t * t * 0.55
        a = alpha_l * clamp((dur - t) / 0.4)
        base = _piece(path, size)
        for gstep, ga in ((0.05, 0.22), (0.025, 0.4), (0.0, 1.0)):    # motion blur: two faint ghosts behind
            tt = max(0.0, t - gstep)
            gx = ox + vx * tt * 0.55
            gy = oy + vy * tt * 0.55 + 0.5 * g * tt * tt * 0.55
            im = base.rotate(rot0 + vr * tt, expand=True, resample=Image.BILINEAR)
            if ga * a < 0.999:
                im = im.copy()
                im.putalpha(im.getchannel("A").point(lambda v, k=ga * a: int(v * k)))
            canvas.alpha_composite(im, (int(gx * W - im.width / 2), int(gy * H - im.height / 2)))


def draw_direct(ctx, canvas, L, lt, alpha):
    {"crowd": draw_crowd, "nodes": draw_nodes, "burst": draw_burst}[L["type"]](ctx, canvas, L, lt, alpha)


# ------------------------------------------------------------------ rim light, night grade, highlight captions
def rim(img, colors=("#3fa9ff", "#9b6bff"), strength=1.0, dim=0.8):
    """Make a 2D character belong in the night set: darken and cool the fill, add a coloured rim on both edges."""
    a = img.getchannel("A")
    arr = np.asarray(img).astype(np.float32)
    navy = np.array([14, 22, 44], np.float32)
    arr[..., :3] = arr[..., :3] * dim + navy * (1 - dim) * 0.6
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    k = max(2, int(img.height * 0.008))
    an = np.asarray(a).astype(np.float32)
    for c, dx in ((colors[0], -k), (colors[1] if len(colors) > 1 else colors[0], k)):
        sh = np.zeros_like(an)
        if dx < 0:
            sh[:, :dx] = an[:, -dx:]
        else:
            sh[:, dx:] = an[:, :-dx]
        edge = np.clip(an - sh, 0, 255) * strength * (0.9 if dx < 0 else 0.55)
        e = Image.fromarray(edge.astype(np.uint8)).filter(ImageFilter.GaussianBlur(k * 0.35))
        layer = Image.new("RGBA", img.size, rgb(c) + (0,))
        layer.putalpha(e)
        out.alpha_composite(layer)
    out.putalpha(a)
    return out


@lru_cache(maxsize=4)
def _vig(W, H, amount):
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    m = 1 - amount * np.clip((r - 0.55) / 0.85, 0, 1) ** 1.6
    return m[..., None].astype(np.float32)


def grade(img, amount=0.38):
    """Night finish: deeper blacks, a little cooler, vignette. Light touch: the plates already carry the mood."""
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    arr = np.clip((arr - 6) * 1.04, 0, 255)
    arr[..., 2] = np.clip(arr[..., 2] * 1.03 + 2, 0, 255)
    arr *= _vig(img.width, img.height, amount)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")


def draw_highlight_caption(ctx, canvas, words, wt, t, y, cap):
    """Caption mode "highlight": the whole phrase in clean sentence case; words not yet spoken dim, the one being spoken
    (and the one before) inside a thin selection box with handles, like text being selected on a phone."""
    W, H = ctx.W, ctx.H
    s = W / 1080
    f = font(cap.get("hl_font", "ui"), cap.get("size", 46) * s)
    cur = 0
    for i, tw_ in enumerate(wt):
        if t >= tw_:
            cur = i
    shown = [w.replace("*", "") for w in words]
    maxw = W * 0.84
    lines, line = [], []
    for i, w in enumerate(shown):
        test = " ".join(shown[j] for j in line + [i])
        if line and f.getlength(test) > maxw:
            lines.append(line)
            line = [i]
        else:
            line.append(i)
    if line:
        lines.append(line)
    lh = f.size * 1.32
    d = ImageDraw.Draw(canvas)
    sel = rgb(cap.get("hl_box", "#5aa9ff"))
    act = {cur, cur - 1} if cur > 0 else {0}
    y0 = y * H - lh * len(lines) / 2
    sp = f.getlength(" ")
    for li, ln in enumerate(lines):
        total = f.getlength(" ".join(shown[i] for i in ln))
        x = W / 2 - total / 2
        yy = y0 + li * lh
        boxes = []
        for i in ln:
            w = shown[i]
            wl = f.getlength(w)
            spoken = i <= cur
            colr = (246, 248, 252, 255) if spoken else (172, 180, 196, 140)
            d.text((x + 2, yy + 3), w, font=f, fill=(0, 0, 0, 120 if spoken else 60))
            d.text((x, yy), w, font=f, fill=colr)
            if i in act:
                boxes.append((x, x + wl))
            x += wl + sp
        if boxes:
            bx0, bx1 = boxes[0][0] - 8 * s, boxes[-1][1] + 8 * s
            by0, by1 = yy - 2 * s, yy + lh - 6 * s
            d.rectangle([bx0, by0, bx1, by1], outline=(*sel, 230), width=max(2, int(2 * s)))
            r = 5 * s
            d.ellipse([bx0 - r, by0 - r, bx0 + r, by0 + r], fill=(*sel, 255))
            d.ellipse([bx1 - r, by1 - r, bx1 + r, by1 + r], fill=(*sel, 255))
