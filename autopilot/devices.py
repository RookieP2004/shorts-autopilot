"""Fictional on-screen devices: phone screen UIs drawn in code (PIL), live or as textures.

Used by the `phone` layer (a Blender phone cut-out with its screen drawn live into it, so messages pop in and timers tick)
and by blendkit.phone(screen_image=...) for a still texture. Everything here is a FICTIONAL app: our own dark-navy UI,
our own names, no real app's logo, colours or layout. Money shown on screens is always fictional.

A screen spec is a dict:
  {"kind": "lock", "time": "9:41", "date": "Monday", "notes": [{"app": "TIP CLUB", "title": "...", "body": "...", "at": 1.0}]}
  {"kind": "chat", "name": "Multibagger Club", "sub": "8,214 members", "msgs": [{"text": "...", "side": "in"|"out",
                   "time": "9:12", "ticks": 2, "badge": "HIT"|"MISS"|None, "at": 0.5}], "input": "Message"}
  {"kind": "tips", "name": "...", "sub": "...", "rows": [{"label": "CALL 1", "text": "STOCK A will go UP", "badge": "HIT", "at": 0.4}]}
  {"kind": "pay", "name": "...", "title": "VIP ACCESS", "price": "₹4,999", "note": "...", "countdown": 589, "button": "PAY NOW"}
`at` = seconds into the layer when that element appears (pops in); omit for always shown. lt=None draws the final state.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {"b": "fonts/Poppins-ExtraBold.ttf", "s": "fonts/Poppins-SemiBold.ttf", "mono": "fonts/CourierPrime-Bold.ttf"}
C = {"bg": (9, 14, 26), "bg2": (17, 25, 43), "bar": (14, 21, 37), "in": (30, 41, 64), "out": (31, 92, 82),
     "text": (236, 240, 247), "dim": (139, 152, 176), "green": (53, 224, 138), "red": (255, 59, 74), "gold": (244, 192, 78),
     "blue": (74, 163, 255), "tick": (98, 197, 255)}
_FC = {}


def font(kind, size):
    k = (kind, size)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(os.path.join(ROOT, F[kind]), size)
    return _FC[k]


def _shown(el, lt):
    return lt is None or lt >= el.get("at", -1)


def _pop(el, lt, dur=0.22):
    if lt is None or "at" not in el:
        return 1.0
    p = max(0.0, min(1.0, (lt - el["at"]) / dur))
    return 1 - (1 - p) ** 3


def _wrap(text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if f.getlength(t) <= maxw or not line:
            line = t
        else:
            out.append(line)
            line = w
    if line:
        out.append(line)
    return out


def ticks(d, x, y, s, col, n=2):
    """Double (or single) check marks, like a 'seen' receipt. Our own drawing."""
    for i in range(n):
        ox = x + i * s * 0.45
        d.line([(ox, y + s * 0.5), (ox + s * 0.3, y + s * 0.8), (ox + s * 0.85, y + s * 0.15)], fill=col, width=max(2, int(s * 0.14)))


def check_badge(d, cx, cy, r, ok=True):
    col = C["green"] if ok else C["red"]
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    if ok:
        d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.35), (cx + r * 0.5, cy - r * 0.35)], fill=(255, 255, 255), width=max(2, int(r * 0.28)))
    else:
        for sgn in (1, -1):
            d.line([(cx - r * 0.38, cy - sgn * r * 0.38), (cx + r * 0.38, cy + sgn * r * 0.38)], fill=(255, 255, 255), width=max(2, int(r * 0.26)))


def _status(d, W, s, time="9:41"):
    d.text((W * 0.08, s * 28), time, font=font("s", int(s * 26)), fill=C["text"])
    x = W * 0.86
    for i in range(4):                                   # signal bars
        h = s * (8 + i * 5)
        d.rectangle([x - s * 40 + i * s * 8, s * 52 - h, x - s * 35 + i * s * 8, s * 52], fill=C["text"])
    d.rounded_rectangle([x, s * 32, x + s * 40, s * 52], radius=s * 5, outline=C["text"], width=max(1, int(s * 2)))
    d.rectangle([x + s * 4, s * 36, x + s * 30, s * 48], fill=C["text"])


def _header(img, d, W, s, name, sub, color=None):
    d.rectangle([0, s * 70, W, s * 170], fill=C["bar"])
    r = s * 32
    cx, cy = s * 70, s * 120
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color or C["gold"])
    ini = "".join(w[0] for w in name.split()[:2]).upper()
    f = font("b", int(s * 26))
    d.text((cx, cy), ini, font=f, fill=C["bg"], anchor="mm")
    d.text((s * 120, s * 92), name, font=font("b", int(s * 28)), fill=C["text"])
    d.text((s * 120, s * 128), sub, font=font("s", int(s * 20)), fill=C["dim"])


def screen(spec, lt=None, w=600, h=1336):
    """Draw a fictional phone screen. Returns an RGB image (w x h)."""
    s = w / 600
    img = Image.new("RGB", (w, h), C["bg"])
    d = ImageDraw.Draw(img)
    k = spec.get("kind", "chat")
    if k == "lock":
        # deep gradient wallpaper
        for y in range(h):
            f = y / h
            d.line([(0, y), (w, y)], fill=(int(14 + 40 * f), int(16 + 6 * f), int(40 + 60 * f)))
        _status(d, w, s, spec.get("status_time", ""))
        d.text((w / 2, s * 250), spec.get("time", "9:41"), font=font("s", int(s * 150)), fill=C["text"], anchor="mm")
        d.text((w / 2, s * 350), spec.get("date", ""), font=font("s", int(s * 26)), fill=C["text"], anchor="mm")
        y = s * 430
        for n in spec.get("notes", []):
            if not _shown(n, lt):
                continue
            p = _pop(n, lt)
            card = Image.new("RGBA", (int(w * 0.9), int(s * 150)), (0, 0, 0, 0))
            cd = ImageDraw.Draw(card)
            cd.rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=s * 26, fill=(40, 46, 78, 225))
            cd.rounded_rectangle([s * 20, s * 22, s * 64, s * 66], radius=s * 12, fill=n.get("color", C["gold"]))
            cd.text((s * 42, s * 44), n.get("app", "?")[:1], font=font("b", int(s * 24)), fill=C["bg"], anchor="mm")
            cd.text((s * 80, s * 22), n.get("app", "").upper(), font=font("s", int(s * 18)), fill=C["dim"])
            cd.text((card.width - s * 20, s * 22), n.get("when", "now"), font=font("s", int(s * 18)), fill=C["dim"], anchor="ra")
            cd.text((s * 80, s * 50), n.get("title", ""), font=font("b", int(s * 22)), fill=C["text"])
            for i, ln in enumerate(_wrap(n.get("body", ""), font("s", int(s * 20)), card.width - s * 100)[:2]):
                cd.text((s * 80, s * 82 + i * s * 28), ln, font=font("s", int(s * 20)), fill=C["text"])
            yy = int(y + (1 - p) * s * 40)
            img.paste(card, (int(w * 0.05), yy), card.split()[3].point(lambda a: int(a * p)))
            y += s * 165
        if spec.get("cta"):
            f = font("b", int(s * 24))
            tw = f.getlength(spec["cta"]) + s * 60
            p = _pop(spec, lt) if "cta_at" not in spec else _pop({"at": spec["cta_at"]}, lt)
            if lt is None or "cta_at" not in spec or lt >= spec["cta_at"]:
                x0, y0 = w / 2 - tw / 2, h * 0.62
                d.rounded_rectangle([x0, y0, x0 + tw, y0 + s * 64], radius=s * 32, fill=(246, 246, 250))
                d.text((w / 2, y0 + s * 32), spec["cta"], font=f, fill=C["bg"], anchor="mm")
        d.rounded_rectangle([w * 0.35, h - s * 26, w * 0.65, h - s * 18], radius=s * 4, fill=C["text"])
        return img
    _status(d, w, s, spec.get("status_time", "9:41"))
    _header(img, d, w, s, spec.get("name", "Tip Club"), spec.get("sub", ""), spec.get("color"))
    if k == "chat":
        y = s * 200
        for m in spec.get("msgs", []):
            if not _shown(m, lt):
                continue
            p = _pop(m, lt)
            f = font("s", int(s * 24))
            lines = _wrap(m["text"], f, w * 0.62)
            bw = max(f.getlength(ln) for ln in lines) + s * 40
            bw = max(bw, s * 170)
            bh = len(lines) * s * 34 + s * 58
            out = m.get("side", "in") == "out"
            x0 = w - bw - s * 24 if out else s * 24
            yy = y + (1 - p) * s * 30
            d.rounded_rectangle([x0, yy, x0 + bw, yy + bh], radius=s * 22, fill=C["out"] if out else C["in"])
            for i, ln in enumerate(lines):
                d.text((x0 + s * 20, yy + s * 16 + i * s * 34), ln, font=f, fill=C["text"])
            d.text((x0 + bw - s * 70, yy + bh - s * 34), m.get("time", ""), font=font("s", int(s * 16)), fill=C["dim"])
            ticks(d, x0 + bw - s * 34, yy + bh - s * 32, s * 22, C["tick"], m.get("ticks", 2))
            if m.get("badge"):
                ok = m["badge"] in ("HIT", "WON", "TRUE", "UP")
                bf = font("b", int(s * 18))
                tw = bf.getlength(m["badge"]) + s * 50
                bx, by = x0 + s * 20, yy + bh - s * 40
                d.rounded_rectangle([bx, by, bx + tw, by + s * 30], radius=s * 15, fill=C["green"] if ok else C["red"])
                d.text((bx + tw / 2, by + s * 15), m["badge"], font=bf, fill=C["bg"], anchor="mm")
            y += bh + s * 18
        d.rectangle([0, h - s * 110, w, h], fill=C["bar"])
        d.rounded_rectangle([s * 20, h - s * 90, w - s * 100, h - s * 34], radius=s * 28, fill=C["in"])
        d.text((s * 46, h - s * 62), spec.get("input", "Message"), font=font("s", int(s * 20)), fill=C["dim"], anchor="lm")
        d.ellipse([w - s * 84, h - s * 92, w - s * 24, h - s * 32], fill=C["blue"])
        return img
    if k == "tips":
        y = s * 200
        for r in spec.get("rows", []):
            if not _shown(r, lt):
                continue
            p = _pop(r, lt)
            yy = y + (1 - p) * s * 24
            d.rounded_rectangle([s * 24, yy, w - s * 24, yy + s * 118], radius=s * 20, fill=C["bg2"])
            d.text((s * 48, yy + s * 18), r.get("label", ""), font=font("mono", int(s * 20)), fill=C["dim"])
            d.text((s * 48, yy + s * 50), r.get("text", ""), font=font("b", int(s * 28)), fill=C["text"])
            if r.get("badge"):
                ok = r["badge"] in ("HIT", "WON", "TRUE", "UP")
                bp = 1.0 if lt is None or "badge_at" not in r else (1.0 if lt >= r["badge_at"] else 0.0)
                if bp:
                    check_badge(d, w - s * 76, yy + s * 59, s * 26, ok)
                    d.text((w - s * 76, yy + s * 100), r["badge"], font=font("b", int(s * 14)), fill=C["green"] if ok else C["red"], anchor="mm")
            y += s * 132
        return img
    if k == "pay":
        for y in range(int(s * 170), h):                  # red alarm wash
            f = (y - s * 170) / h
            d.line([(0, y), (w, y)], fill=(int(60 + 50 * f), int(10 + 4 * f), int(18 + 6 * f)))
        cy = s * 360
        d.text((w / 2, cy), spec.get("title", "VIP ACCESS"), font=font("b", int(s * 56)), fill=C["text"], anchor="mm")
        d.text((w / 2, cy + s * 70), spec.get("note", ""), font=font("s", int(s * 24)), fill=C["gold"], anchor="mm")
        cd = spec.get("countdown")
        if cd is not None:
            left = max(0, cd - (lt or 0))
            d.text((w / 2, cy + s * 150), f"ENDS IN {int(left // 60):02d}:{int(left % 60):02d}", font=font("mono", int(s * 40)), fill=C["gold"], anchor="mm")
        d.rounded_rectangle([w * 0.18, cy + s * 230, w * 0.82, cy + s * 360], radius=s * 22, fill=(20, 8, 12), outline=C["red"], width=max(2, int(s * 3)))
        d.text((w / 2, cy + s * 260), spec.get("price_label", "ONE-TIME FEE"), font=font("mono", int(s * 18)), fill=C["red"], anchor="mm")
        d.text((w / 2, cy + s * 310), spec.get("price", ""), font=font("b", int(s * 56)), fill=C["text"], anchor="mm")
        pulse = 1.0 if lt is None else 0.85 + 0.15 * (0.5 + 0.5 * math.sin(lt * 6))
        bx0, by0 = w * 0.12, h - s * 250
        col = tuple(int(c * pulse) for c in (240, 240, 245))
        d.rounded_rectangle([bx0, by0, w - bx0, by0 + s * 90], radius=s * 45, fill=col)
        d.text((w / 2, by0 + s * 45), spec.get("button", "PAY NOW"), font=font("b", int(s * 34)), fill=C["red"], anchor="mm")
        return img
    return img


def note_texture(value="500", path=None, w=1200, h=560, tint=(102, 196, 168)):
    """A FICTIONAL banknote texture: our own design, big value, 'NOT REAL MONEY' printed on it, no portrait, no real issuer."""
    img = Image.new("RGB", (w, h), tint)
    d = ImageDraw.Draw(img)
    dark = tuple(int(c * 0.55) for c in tint)
    pale = tuple(min(255, int(c * 1.25)) for c in tint)
    for i in range(0, w + h, 14):                          # guilloche-ish line pattern
        d.line([(i, 0), (i - h, h)], fill=pale, width=1)
    for r in range(40, 260, 18):
        d.ellipse([w * 0.72 - r, h / 2 - r, w * 0.72 + r, h / 2 + r], outline=dark, width=2)
    d.rectangle([14, 14, w - 15, h - 15], outline=dark, width=8)
    d.text((60, 40), "₹" + value, font=font("b", 150), fill=dark)
    d.text((60, h - 140), "NOT REAL MONEY", font=font("b", 64), fill=dark)
    d.text((62, h - 64), "THE EXPLAINER · FOR ILLUSTRATION ONLY", font=font("s", 28), fill=dark)
    d.text((w * 0.72, h / 2), value, font=font("b", 120), fill=(250, 250, 245), anchor="mm")
    if path:
        img.save(path)
    return img
