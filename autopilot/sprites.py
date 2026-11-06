"""Everything drawn on screen is a sprite: an RGBA PIL image, built once and cached."""
import io
import os
import re
import math
import hashlib
from functools import lru_cache

import cairosvg
from PIL import Image, ImageDraw, ImageFont

from .spec import ROOT, color, hex_rgba


def _key(*parts):
    return hashlib.md5(repr(parts).encode()).hexdigest()


_cache = {}


def cached(key, fn):
    if key not in _cache:
        if len(_cache) > 600:
            _cache.clear()
        _cache[key] = fn()
    return _cache[key]


def svg_image(svg_text, width):
    width = max(2, int(width))
    k = _key("svg", svg_text, width)

    def make():
        png = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"), output_width=width)
        return Image.open(io.BytesIO(png)).convert("RGBA")
    return cached(k, make)


@lru_cache(maxsize=256)
def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


@lru_cache(maxsize=64)
def font(path, size):
    p = path if os.path.isabs(path) else os.path.join(ROOT, path)
    return ImageFont.truetype(p, int(size))


def resolve_font(style, name):
    return style["fonts"].get(name, name or style["fonts"]["body"])


# ---------- text ----------
MARK = re.compile(r"\*([^*]+)\*")


def _tokens(text):
    """'Octopus have *three* hearts' -> [(word, highlighted), ...]"""
    out = []
    pos = 0
    for m in MARK.finditer(text):
        for w in text[pos:m.start()].split():
            out.append((w, False))
        for w in m.group(1).split():
            out.append((w, True))
        pos = m.end()
    for w in text[pos:].split():
        out.append((w, False))
    return out


def text_image(style, text, size=110, font_name="display", fill="primary",
               highlight="accent", stroke="#000000", stroke_width=0, max_w=0.86,
               align="center", uppercase=False, line_gap=0.08, shadow=True,
               highlight_index=None):
    """Render (possibly multi-line) text. *word* marks highlighted words.
    highlight_index highlights one word by index (used for captions)."""
    k = _key("txt", text, size, font_name, fill, highlight, stroke, stroke_width,
             max_w, align, uppercase, highlight_index, shadow)

    def make():
        f = font(resolve_font(style, font_name), size)
        W = style["canvas"]["w"]
        maxpx = int(W * max_w)
        toks = _tokens(text.upper() if uppercase else text)
        if highlight_index is not None:
            toks = [(w, i == highlight_index) for i, (w, _) in enumerate(toks)]
        space = f.getlength(" ")
        lines, cur, cw = [], [], 0
        for w, h in toks:
            wl = f.getlength(w)
            add = wl if not cur else cw + space + wl
            if cur and add > maxpx:
                lines.append((cur, cw))
                cur, cw = [(w, h, wl)], wl
            else:
                cur.append((w, h, wl))
                cw = add
        if cur:
            lines.append((cur, cw))
        asc, desc = f.getmetrics()
        lh = asc + desc
        gap = int(size * line_gap)
        pad = stroke_width + int(size * 0.12) + 4
        width = int(max((c for _, c in lines), default=1)) + pad * 2
        height = lh * len(lines) + gap * (len(lines) - 1) + pad * 2
        img = Image.new("RGBA", (max(1, width), max(1, height)), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        fc = hex_rgba(color(style, fill))
        hc = hex_rgba(color(style, highlight))
        sc = hex_rgba(color(style, stroke)) if stroke else None
        y = pad
        for words, lw in lines:
            if align == "left":
                x = pad
            elif align == "right":
                x = width - pad - lw
            else:
                x = (width - lw) / 2
            for w, h, wl in words:
                if shadow:
                    d.text((x + size * 0.04, y + size * 0.06), w, font=f, fill=(0, 0, 0, 110),
                           stroke_width=stroke_width, stroke_fill=(0, 0, 0, 110))
                d.text((x, y), w, font=f, fill=hc if h else fc,
                       stroke_width=stroke_width if sc else 0, stroke_fill=sc)
                x += wl + space
            y += lh + gap
        return img
    return cached(k, make)


# ---------- shapes (drawn as SVG for clean anti-aliasing) ----------
def shape_svg(style, L, W, H):
    sh = L["shape"]
    fill = color(style, L.get("color", "accent"))
    stroke = color(style, L.get("stroke", L.get("color", "accent")))
    sw = L.get("stroke_width", 14)
    w = L.get("w", 0.3) * W
    h = L.get("h", L.get("w", 0.3)) * W if sh not in ("rect", "line") else L.get("h", 0.1) * W
    if sh == "circle":
        body = f'<circle cx="{w/2}" cy="{w/2}" r="{w/2}" fill="{fill}"/>'
        vb = (w, w)
    elif sh == "ring":
        r = w / 2 - sw / 2
        body = f'<circle cx="{w/2}" cy="{w/2}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>'
        vb = (w, w)
    elif sh == "rect":
        rad = L.get("radius", 0.12) * min(w, h)
        if L.get("outline"):
            body = (f'<rect x="{sw/2}" y="{sw/2}" width="{w-sw}" height="{h-sw}" rx="{rad}" '
                    f'fill="none" stroke="{stroke}" stroke-width="{sw}"/>')
        else:
            body = f'<rect width="{w}" height="{h}" rx="{rad}" fill="{fill}"/>'
        vb = (w, h)
    elif sh == "line":
        body = f'<rect width="{w}" height="{max(2, sw)}" rx="{sw/2}" fill="{fill}"/>'
        vb = (w, max(2, sw))
    elif sh == "arrow":
        hh = w * 0.42
        shaft = hh * 0.36
        body = (f'<path d="M0 {hh/2-shaft/2} H{w*0.62} V0 L{w} {hh/2} L{w*0.62} {hh} '
                f'V{hh/2+shaft/2} H0 Z" fill="{fill}"/>')
        vb = (w, hh)
    elif sh == "burst":
        n = L.get("points", 14)
        pts = []
        for i in range(n * 2):
            r = w / 2 if i % 2 == 0 else w / 2 * 0.72
            a = math.pi * i / n
            pts.append(f"{w/2 + r*math.cos(a):.1f},{w/2 + r*math.sin(a):.1f}")
        body = f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'
        vb = (w, w)
    else:
        raise ValueError(sh)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb[0]:.1f} {vb[1]:.1f}" '
            f'width="{vb[0]:.1f}" height="{vb[1]:.1f}">{body}</svg>'), int(vb[0])


# ---------- backgrounds ----------
def background(style, bg, W, H):
    bg = bg or style["background"]
    k = _key("bg", repr(sorted(bg.items(), key=lambda x: x[0])), W, H)

    def make():
        t = bg.get("type", "gradient")
        cols = [color(style, c) for c in bg.get("colors", ["bg1", "bg2"])]
        if t == "solid" or len(cols) == 1:
            svg_fill = cols[0]
            defs = ""
        elif t == "radial":
            defs = (f'<defs><radialGradient id="g" cx="50%" cy="40%" r="75%">'
                    + "".join(f'<stop offset="{i/(len(cols)-1)}" stop-color="{c}"/>'
                              for i, c in enumerate(cols)) + '</radialGradient></defs>')
            svg_fill = "url(#g)"
        else:
            a = math.radians(bg.get("angle", 160) - 90)
            x1, y1 = 0.5 - 0.5 * math.cos(a), 0.5 - 0.5 * math.sin(a)
            x2, y2 = 0.5 + 0.5 * math.cos(a), 0.5 + 0.5 * math.sin(a)
            defs = (f'<defs><linearGradient id="g" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
                    + "".join(f'<stop offset="{i/(len(cols)-1)}" stop-color="{c}"/>'
                              for i, c in enumerate(cols)) + '</linearGradient></defs>')
            svg_fill = "url(#g)"
        pat = ""
        p = bg.get("pattern", "none")
        pc = color(style, bg.get("pattern_color", "#ffffff"))
        po = bg.get("pattern_opacity", 0.05)
        if p == "dots":
            pat = (f'<defs><pattern id="p" width="54" height="54" patternUnits="userSpaceOnUse">'
                   f'<circle cx="27" cy="27" r="4" fill="{pc}" fill-opacity="{po}"/></pattern></defs>'
                   f'<rect width="{W}" height="{H}" fill="url(#p)"/>')
        elif p == "grid":
            pat = (f'<defs><pattern id="p" width="90" height="90" patternUnits="userSpaceOnUse">'
                   f'<path d="M90 0 H0 V90" fill="none" stroke="{pc}" stroke-opacity="{po}" '
                   f'stroke-width="3"/></pattern></defs><rect width="{W}" height="{H}" fill="url(#p)"/>')
        elif p == "rays":
            rays = []
            for i in range(24):
                a0, a1 = 2 * math.pi * i / 24, 2 * math.pi * (i + 0.5) / 24
                R = H * 1.2
                cx, cy = W / 2, H * 0.42
                rays.append(f'<polygon points="{cx},{cy} {cx+R*math.cos(a0):.0f},{cy+R*math.sin(a0):.0f} '
                            f'{cx+R*math.cos(a1):.0f},{cy+R*math.sin(a1):.0f}" fill="{pc}" fill-opacity="{po}"/>')
            pat = "".join(rays)
        vign = ('<defs><radialGradient id="v" cx="50%" cy="50%" r="75%"><stop offset="0.6" '
                'stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" '
                'stop-opacity="0.45"/></radialGradient></defs>'
                f'<rect width="{W}" height="{H}" fill="url(#v)"/>') if bg.get("vignette", True) else ""
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
               f'{defs}<rect width="{W}" height="{H}" fill="{svg_fill}"/>{pat}{vign}</svg>')
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=W, output_height=H)
        return Image.open(io.BytesIO(png)).convert("RGBA")
    return cached(k, make)
