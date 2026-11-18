"""Case-file toolkit (v5): typography and motion for documentary beats, learned from a reference (owner, 2026-11-18).
Mixed INTO the house style (town or night look); never a replacement. Pairs with blendkit.noir_desk (a dark desk cut by
warm venetian-blind light) and devices.doc_texture (fictional papers).

Layers (frame fractions; times inside a layer are seconds after its `at`):
  dottext   dot-matrix label text that DECODES (letters scramble, then lock left to right) or TYPES in:
            {"text": "NEW SIM: *ON*", "size", "tone": "cream", "accent": "green", "anim": "decode"|"type"|"none", "cps", "align"}
            *x* = accent colour (e.g. red for NO SERVICE, green for ON); "\n" = new line.
  bignum    a big serif number (Playfair) that counts, with a dot-matrix caption: {"value"|"to"|"steps", "prefix", "suffix",
            "indian", "label", "tone": "cream"|"gold", "size", "align", "label_side": "below"|"right"}
  dateline  date + place stamp (top-left by default): {"date": "27 DEC 2018", "place": "MUMBAI"}
  tiles     a row of day / step tiles lying on the desk in perspective, filling in gold: {"n": 7, "progress": [[t, k]],
            "labels": [...], "end": "PORT", "pitch": 50, "w"}
  tipnum    a numbered takeaway: big serif numeral + decoding dot-matrix title + small sub: {"n": 1, "title", "sub"}
  clock     a thin analog clock whose hands sweep to a time, with a label: {"time": "11:15", "from": "10:40", "label", "r"}
  blinds    (world) warm venetian-blind light stripes over the whole frame, slowly drifting (gives any shot the look):
            {"angle": -32, "count": 9, "strength": 0.22, "shade": 0.18, "color": "#ffb46b", "drift": 0.02}
  flows     (world) money / call routes as gold arcs between city dots with travelling pulses (no map outline):
            {"points": {"MUMBAI": [x, y], ...}, "routes": [["MUMBAI", "DUBAI", t0], ...], "tone": "gold"}
"""
import math
import os
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .night import TONES as _NT, eout, eback, clamp, hud_value, fmt_num, rgb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TONES = dict(_NT, cream="#efe6d2", gold="#e0b25a", slate="#2a3242", amber="#ffb46b", red="#e2484d", green="#3ecf8e")
IMAGE = {"dottext", "bignum", "dateline", "tiles", "tipnum", "clock"}
DIRECT = {"blinds", "flows"}
SCRAMBLE = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&*+<>/"
LN = ["lnum"]                                                      # lining figures: 1,60,00,000 sits on the line


def tone(name, default="cream"):
    return rgb(TONES.get(name or default, name or default))


@lru_cache(maxsize=64)
def dot_font(size, weight=b"Bold"):
    f = ImageFont.truetype(os.path.join(ROOT, "fonts/Doto.ttf"), max(8, int(size)))
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


@lru_cache(maxsize=16)
def alt_font(size):
    return ImageFont.truetype(os.path.join(ROOT, "fonts/DotGothic16-Regular.ttf"), max(8, int(size)))


@lru_cache(maxsize=64)
def serif(size, weight=b"Bold"):
    f = ImageFont.truetype(os.path.join(ROOT, "fonts/PlayfairDisplay.ttf"), max(8, int(size)))
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


@lru_cache(maxsize=16)
def ui_font(size):
    return ImageFont.truetype(os.path.join(ROOT, "fonts/Poppins-SemiBold.ttf"), max(8, int(size * 0.92)))


def _glyph_font(ch, size):
    if ch == "\u20b9":                                               # the dot fonts have no rupee sign
        return ui_font(size)
    return alt_font(size) if ch in ":;,.'\"!?()-" else dot_font(size)


def _parse(text):
    """'NEW SIM: *ON*' -> list of (char, accent?) with the * marks removed."""
    out, acc = [], False
    for ch in text:
        if ch == "*":
            acc = not acc
            continue
        out.append((ch, acc))
    return out


def dottext_image(L, lt, W=1080):
    s = W / 1080
    size = L.get("size", 56) * s
    base, acc = tone(L.get("tone"), "cream"), tone(L.get("accent"), "red")
    lines = [_parse(ln) for ln in L["text"].split("\n")]
    anim, cps = L.get("anim", "decode"), L.get("cps", 26)
    rnd = random.Random(int(lt * 30) + L.get("seed", 0))
    lh = size * 1.18
    adv = dot_font(size).getlength("M") * 1.0
    width = max(len(ln) for ln in lines) * adv
    im = Image.new("RGBA", (int(width + size), int(lh * len(lines) + size * 0.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = 0
    for li, ln in enumerate(lines):
        n = len(ln)
        x0 = {"left": 0, "center": (width - n * adv) / 2, "right": width - n * adv}[L.get("align", "left")]
        for ci, (ch, a) in enumerate(ln):
            t_lock = k / cps
            k += 1
            if ch == " ":
                continue
            col = acc if a else base
            if anim == "type":
                if lt < t_lock:
                    if lt >= t_lock - 1 / cps:                       # block cursor at the typing position
                        d.rectangle([x0 + ci * adv, li * lh + size * 0.1, x0 + ci * adv + adv * 0.8, li * lh + size * 1.0],
                                    fill=(*col, 200))
                    continue
                g = ch
            elif anim == "decode":
                if lt < t_lock - 0.5:                                # not started yet
                    continue
                g = ch if lt >= t_lock else rnd.choice(SCRAMBLE)
                if g != ch:
                    col = tuple(int(c * 0.7) for c in col)
            else:
                g = ch
            d.text((x0 + ci * adv + adv / 2, li * lh + size * 0.55), g, font=_glyph_font(g, size), fill=(*col, 255), anchor="mm")
    if L.get("plate"):                                               # dark backing pill: legible on bright town sets
        bg = Image.new("RGBA", (im.width + int(size * 0.8), im.height + int(size * 0.3)), (0, 0, 0, 0))
        ImageDraw.Draw(bg).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], radius=int(size * 0.3), fill=(10, 14, 22, 225),
                                             outline=(*tone(L.get("plate_tone"), "gold"), 160), width=max(1, int(size / 26)))
        bg.alpha_composite(im, (int(size * 0.4), int(size * 0.12)))
        im = bg
    if L.get("glow", True):
        g = im.filter(ImageFilter.GaussianBlur(size * 0.12))
        out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        out.alpha_composite(g)
        out.alpha_composite(im)
        im = out
    return im


def _num_text(L, lt):
    if "text" in L:
        return L["text"]
    v = hud_value(L, lt)
    return f"{L.get('prefix', '')}{fmt_num(round(v, L.get('decimals', 0)), L.get('indian', True), L.get('decimals', 0))}{L.get('suffix', '')}"


def bignum_image(L, lt, W=1080):
    s = W / 1080
    size = L.get("size", 190) * s
    f = serif(size)
    txt = _num_text(L, lt)
    col = tone(L.get("tone"), "cream")
    tw = f.getlength(L.get("width_of", txt), features=LN)
    label = L.get("label", "")
    lab = dottext_image({"text": label, "size": L.get("label_size", 48), "anim": L.get("label_anim", "decode"), "tone": "cream",
                         "accent": L.get("accent", "red")}, lt - L.get("label_at", 0.25), W) if label else None
    side = L.get("label_side", "below")
    bw = tw + 20 * s
    bh = size * 1.12
    if lab is not None and side == "right":
        W2, H2 = int(bw + lab.width + 30 * s), int(max(bh, lab.height))
    else:
        W2, H2 = int(max(bw, lab.width if lab else 0)), int(bh + (lab.height if lab else 0))
    im = Image.new("RGBA", (W2 + 20, H2 + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    al = L.get("align", "center")
    nx = {"left": 10, "center": (im.width - tw) / 2, "right": im.width - tw - 10}[al] if side != "right" else 10
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((nx + 4 * s, 10 + 6 * s), txt, font=f, fill=(0, 0, 0, 150), features=LN)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6 * s)))
    d.text((nx, 10), txt, font=f, fill=(*col, 255), features=LN)
    if lab is not None:
        if side == "right":
            im.alpha_composite(lab, (int(bw + 30 * s), int(10 + bh * 0.62 - lab.height / 2)))
        else:
            lx = {"left": 10, "center": (im.width - lab.width) // 2, "right": im.width - lab.width - 10}[al]
            im.alpha_composite(lab, (int(lx), int(10 + bh * 0.98)))
    return im


def dateline_image(L, lt, W=1080):
    s = W / 1080
    date = dottext_image({"text": L.get("date", ""), "size": L.get("date_size", 46), "anim": "type", "cps": 22,
                          "tone": "cream"}, lt, W)
    pf = serif(L.get("size", 120) * s, b"Black")
    place = L.get("place", "").upper()
    pw = pf.getlength(place)
    im = Image.new("RGBA", (int(max(date.width, pw) + 30), int(date.height + L.get("size", 120) * s * 1.2)), (0, 0, 0, 0))
    a = eout((lt - 0.35) / 0.5)
    if a > 0:
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((6, date.height + (1 - a) * 30 * s), place, font=pf, fill=(*tone("cream"), int(255 * a)))
        sh = layer.filter(ImageFilter.GaussianBlur(5 * s))
        sh = Image.merge("RGBA", (*[Image.new("L", im.size, 0)] * 3, sh.getchannel("A").point(lambda v: int(v * 0.6))))
        im.alpha_composite(sh, (3, 5))
        im.alpha_composite(layer)
    im.alpha_composite(date, (0, 0))
    return im


def tiles_image(L, lt, W=1080):
    from .night import card_turn
    s = W / 1080
    n = L.get("n", 7)
    k = 0
    for t, kk in sorted(L.get("progress", [])):
        if lt >= t:
            k = kk
    tw = int(L.get("w", 0.86) * W)
    gap = tw * 0.025
    cw = (tw - gap * (n - 1)) / n
    ch = cw * 1.05
    extra = int(cw * 1.3) if L.get("end") else 0
    im = Image.new("RGBA", (tw + extra + 20, int(ch + 40 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    gold, slate, cream = tone("gold"), tone("slate"), tone("cream")
    labels = L.get("labels") or [str(i + 1) for i in range(n)]
    f = serif(ch * 0.55)
    fs = dot_font(ch * 0.14)
    for i in range(n):
        x = 10 + i * (cw + gap)
        on = i < k
        p = eback((lt - [t for t, kk in sorted(L.get("progress", [])) if kk > i][0]) / 0.3) if on and L.get("progress") else 1
        lift = (1 - min(1, p)) * 10 * s
        d.rounded_rectangle([x, 10 - lift, x + cw, 10 + ch - lift], radius=cw * 0.14,
                            fill=(*(gold if on else slate), 255), outline=(*tone("cream"), 90), width=max(1, int(2 * s)))
        d.text((x + cw / 2, 10 + ch * 0.58 - lift), labels[i], font=f, fill=(*((20, 20, 24) if on else cream), 255), anchor="mm", features=LN)
        d.text((x + cw / 2, 10 + ch * 0.16 - lift), L.get("unit", "DAY"), font=fs, fill=(*((40, 30, 10) if on else (150, 160, 178)), 255), anchor="mm")
    if L.get("end"):
        x = 10 + n * (cw + gap) + gap
        d.rounded_rectangle([x, 10, x + cw * 1.2, 10 + ch], radius=cw * 0.1, outline=(*gold, 255), width=max(2, int(3 * s)))
        d.text((x + cw * 0.6, 10 + ch / 2), L["end"], font=dot_font(ch * 0.2), fill=(*gold, 255), anchor="mm")
    return card_turn(im, L.get("yaw", -8), L.get("pitch", 48), f_mult=1.6)


def tipnum_image(L, lt, W=1080):
    s = W / 1080
    num = str(L.get("n", 1))
    f = serif(L.get("size", 300) * s)
    nw = f.getlength(num, features=LN)
    a = eout(lt / 0.35)
    title = dottext_image({"text": L.get("title", ""), "size": L.get("title_size", 60), "anim": "decode", "tone": "cream",
                           "accent": L.get("accent", "red"), "plate": L.get("plate")}, lt - 0.25, W)
    sub = None
    if L.get("sub"):
        sub = dottext_image({"text": L["sub"], "size": 30, "anim": "type", "cps": 40, "tone": "cream", "glow": False},
                            lt - 0.9, W)
    h = int(L.get("size", 300) * s * 1.25)
    im = Image.new("RGBA", (int(max(nw, title.width, sub.width if sub else 0) + 40), h + title.height + (sub.height if sub else 0)),
                   (0, 0, 0, 0))
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((10, -L.get("size", 300) * s * 0.12 + (1 - a) * 40 * s), num, font=f, fill=(*tone(L.get("tone"), "gold"), int(255 * a)), features=LN)
    im.alpha_composite(layer)
    im.alpha_composite(title, (6, h - int(20 * s)))
    if sub:
        im.alpha_composite(sub, (10, h - int(10 * s) + title.height))
    return im


def _hm(t):
    h, m = t.split(":")
    return int(h) % 12 + int(m) / 60, int(m)


def clock_image(L, lt, W=1080):
    s = W / 1080
    r = L.get("r", 0.22) * W
    pad = int(r * 0.25)
    sz = int(2 * r + 2 * pad)
    im = Image.new("RGBA", (sz, sz + int(110 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (sz / 2, sz / 2)
    cream, gold = tone("cream"), tone(L.get("tone"), "gold")
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=(*cream, 230), width=max(2, int(4 * s)))
    for i in range(60):
        a = math.radians(i * 6)
        r0 = r * (0.86 if i % 5 == 0 else 0.93)
        d.line([(c[0] + math.sin(a) * r0, c[1] - math.cos(a) * r0), (c[0] + math.sin(a) * r * 0.97, c[1] - math.cos(a) * r * 0.97)],
               fill=(*cream, 230 if i % 5 == 0 else 120), width=max(1, int((4 if i % 5 == 0 else 2) * s)))
    h1, _ = _hm(L["time"])
    h0, _ = _hm(L.get("from", L["time"]))
    if h1 < h0:
        h1 += 12
    p = eout(lt / L.get("dur", 1.4))
    hh = h0 + (h1 - h0) * p
    for ang, ln, wd, col in ((hh * 30, 0.5, 9, cream), ((hh % 1) * 360, 0.78, 5, gold)):
        a = math.radians(ang)
        d.line([c, (c[0] + math.sin(a) * r * ln, c[1] - math.cos(a) * r * ln)], fill=(*col, 255), width=max(2, int(wd * s)))
    d.ellipse([c[0] - 9 * s, c[1] - 9 * s, c[0] + 9 * s, c[1] + 9 * s], fill=(*gold, 255))
    if L.get("label"):
        lab = dottext_image({"text": L["label"], "size": 40, "anim": "decode", "tone": "cream", "accent": "gold"}, lt - 0.6, W)
        im.alpha_composite(lab, (int((sz - lab.width) / 2), sz))
    return im


def layer_image(style, L, lt, W):
    return {"dottext": dottext_image, "bignum": bignum_image, "dateline": dateline_image, "tiles": tiles_image,
            "tipnum": tipnum_image, "clock": clock_image}[L["type"]](L, lt, W)


# ------------------------------------------------------------------ full-frame layers
@lru_cache(maxsize=8)
def _stripe_field(W, H, angle):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    a = math.radians(angle)
    return (x * math.cos(a) + y * math.sin(a)) / max(W, H)


def draw_blinds(ctx, canvas, L, lt, alpha):
    W, H = ctx.W, ctx.H
    u = _stripe_field(W, H, L.get("angle", -32))
    count = L.get("count", 9)
    ph = (u * count + L.get("drift", 0.02) * lt * count + L.get("phase", 0.0)) % 1.0
    duty, soft = L.get("duty", 0.42), L.get("soft", 0.06)
    m = np.clip((duty / 2 - np.abs(ph - 0.5)) / soft + 0.5, 0, 1)     # soft-edged stripes
    m = m * (0.55 + 0.45 * np.clip(1.2 - u * 1.4, 0, 1))              # brighter near the window side
    st, sh = L.get("strength", 0.22) * alpha, L.get("shade", 0.18) * alpha
    arr = np.asarray(canvas).astype(np.float32)
    col = np.array(tone(L.get("color"), "amber"), np.float32)
    rgb_ = arr[..., :3] * (1 - sh * (1 - m[..., None]))
    rgb_ = rgb_ + (col - rgb_) * (st * m[..., None]) * 0.6 + col * (st * m[..., None]) * 0.25
    arr[..., :3] = np.clip(rgb_, 0, 255)
    canvas.paste(Image.fromarray(arr.astype(np.uint8), "RGBA"))


def draw_flows(ctx, canvas, L, lt, alpha):
    W, H = ctx.W, ctx.H
    s = W / 1080
    pts = {k: (v[0] * W, v[1] * H) for k, v in L["points"].items()}
    col = tone(L.get("tone"), "gold")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, gd = ImageDraw.Draw(lay), ImageDraw.Draw(glow)
    used = set()
    for r in L.get("routes", []):
        a, b, t0 = r[0], r[1], r[2] if len(r) > 2 else 0
        if lt < t0:
            continue
        used |= {a, b}
        (ax, ay), (bx, by) = pts[a], pts[b]
        mx, my = (ax + bx) / 2, (ay + by) / 2
        dist = math.hypot(bx - ax, by - ay)
        cx, cy = mx - (by - ay) * 0.25, my + (bx - ax) * 0.25 - dist * 0.15
        p = eout((lt - t0) / L.get("draw", 0.8))
        n = 40
        seg = []
        for i in range(int(n * p) + 1):
            q = i / n
            seg.append(((1 - q) ** 2 * ax + 2 * (1 - q) * q * cx + q * q * bx, (1 - q) ** 2 * ay + 2 * (1 - q) * q * cy + q * q * by))
        if len(seg) > 1:
            gd.line(seg, fill=(*col, int(150 * alpha)), width=int(10 * s))
            d.line(seg, fill=(*col, int(255 * alpha)), width=max(2, int(3 * s)))
        if p >= 1 and L.get("pulse", True):                         # a bright pulse travels along the route
            q = ((lt - t0) * 0.6) % 1.0
            px = (1 - q) ** 2 * ax + 2 * (1 - q) * q * cx + q * q * bx
            py = (1 - q) ** 2 * ay + 2 * (1 - q) * q * cy + q * q * by
            gd.ellipse([px - 14 * s, py - 14 * s, px + 14 * s, py + 14 * s], fill=(255, 240, 200, int(220 * alpha)))
            d.ellipse([px - 5 * s, py - 5 * s, px + 5 * s, py + 5 * s], fill=(255, 250, 235, int(255 * alpha)))
    for k, (x, y) in pts.items():
        on = k in used or not L.get("routes")
        r = 9 * s if on else 5 * s
        c = col if on else (140, 150, 170)
        gd.ellipse([x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2], fill=(*c, int(120 * alpha)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*c, int(255 * alpha)))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8 * s)))
    canvas.alpha_composite(lay)
    if L.get("labels", True):
        for k, (x, y) in pts.items():
            if k in used or not L.get("routes"):
                lab = dottext_image({"text": k, "size": 30, "anim": "none", "tone": "cream", "glow": False}, 9, W)
                canvas.alpha_composite(lab, (int(x + 16 * s), int(y - lab.height / 2)))


def draw_direct(ctx, canvas, L, lt, alpha):
    {"blinds": draw_blinds, "flows": draw_flows}[L["type"]](ctx, canvas, L, lt, alpha)
