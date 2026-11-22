"""Real reference photos as small accents (owner, 2026-11-22): when a Short talks about a real incident, place, object or
document, a real photo of it can appear for a moment, framed as a polaroid, a postage stamp, a photo under a sticky note
or a newspaper clipping, the way a human editor drops in a reference.

Rules (also in the Bible):
- Only freely licensed files from Wikimedia Commons: public domain, CC0 or CC BY (no BY-SA, no NC, no press photos,
  no "fair use" uploads). The licence and author are read from the file's Commons page (WebFetch) and passed here.
- Never a photo of a person's face, famous or not: for a real person show a name card, their date, their invention,
  their place or a document instead. Never graphic, violent or victim imagery, never logos or brand marks.
- Accents, not wallpaper: one to three per Short, a second or two each, in the shot that talks about it.
- Credits go into jobs/<id>/photo_credits.json and are appended to the YouTube description automatically.

The workspace can only fetch Wikimedia's standard thumbnail sizes (upload.wikimedia.org); the Commons pages and API are
read with WebFetch.

  python -m autopilot refphoto get "Apollo 11 Launch - GPN-2000-000630.jpg" --license "Public domain" --author "NASA" \
      --frame polaroid --caption "16 July 1969" --job jobs/<id> --out apollo.png
"""
import hashlib
import io
import json
import math
import os
import random
import subprocess
import urllib.parse

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "fonts")
OK_LICENSES = ("public domain", "pd", "cc0", "cc by 1.0", "cc by 2.0", "cc by 2.5", "cc by 3.0", "cc by 4.0", "cc-by")
THUMB = (1280, 960, 500)                       # Wikimedia's standard thumbnail steps (other sizes are refused)
FRAMES = ("polaroid", "stamp", "sticky", "clipping", "plain")
UA = "TheExplainerBot/1.0 (https://github.com/RookieP2004/shorts-autopilot)"


def license_ok(lic):
    l = lic.lower().replace("-", " ").strip()
    if "sa" in l.split() or "share" in l or "nc" in l.split() or "nd" in l.split() or "fair use" in l:
        return False
    return any(l.startswith(x.replace("-", " ")) for x in OK_LICENSES)


def thumb_url(name, width):
    name = name.replace("File:", "").strip().replace(" ", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    q = urllib.parse.quote(name)
    tail = f"{width}px-{q}" + (".png" if name.lower().endswith((".svg", ".tif", ".tiff")) else "")
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{tail}"


def download(name):
    last = ""
    for w in THUMB:
        r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, "-w", "%{http_code}", "-o", "-", thumb_url(name, w)],
                           capture_output=True)
        code, body = r.stdout[-3:].decode(errors="ignore"), r.stdout[:-3]
        if code == "200" and body[:4] not in (b"<!DO", b"<htm"):
            return Image.open(io.BytesIO(body)).convert("RGB")
        last = code
    raise SystemExit(f"could not fetch {name} (HTTP {last}); check the exact Commons file name")


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def _shadow(card, blur=18, off=(10, 14), alpha=110):
    W, H = card.size
    pad = blur * 3
    out = Image.new("RGBA", (W + pad * 2, H + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    m = card.split()[3].point(lambda v: alpha if v > 0 else 0)
    sh.paste((0, 0, 0, 255), (pad + off[0], pad + off[1]), m)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh)
    out.alpha_composite(card, (pad, pad))
    return out


def _crop(img, w, h, focus=(0.5, 0.45)):
    return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=focus)


def _tape(d, x, y, w, h, ang, rng):
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        a = math.radians(ang)
        pts.append((x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a)))
    d.polygon(pts, fill=(238, 228, 196, 190))


def frame(img, kind="polaroid", caption="", credit="", seed=0, size=900):
    """returns an RGBA cut-out with soft shadow, ready for an image layer"""
    rng = random.Random(seed)
    if kind == "polaroid":
        pw, ph = size, int(size * 0.92)
        card = Image.new("RGBA", (pw + 80, ph + 230), (250, 248, 242, 255))
        card.paste(_crop(img, pw, ph), (40, 40))
        d = ImageDraw.Draw(card)
        if caption:
            f = font("Caveat.ttf", 92)
            d.text((card.width / 2, ph + 125), caption, font=f, fill=(40, 40, 52), anchor="mm")
        if credit:
            d.text((card.width - 34, card.height - 22), credit, font=font("Poppins-SemiBold.ttf", 20), fill=(150, 150, 150), anchor="rs")
        _tape(d, card.width / 2, 18, 220, 58, rng.uniform(-6, 6), rng)
    elif kind == "stamp":
        pw = ph = size
        inner = _crop(img, pw - 120, ph - 190)
        card = Image.new("RGBA", (pw, ph), (247, 241, 226, 255))
        card.paste(ImageOps.posterize(inner, 6), (60, 60))
        d = ImageDraw.Draw(card)
        r = 22
        for x in range(0, pw + 1, 2 * r + 12):                      # perforations
            for y in (0, ph):
                d.ellipse((x - r, y - r, x + r, y + r), fill=(0, 0, 0, 0))
        for y in range(0, ph + 1, 2 * r + 12):
            for x in (0, pw):
                d.ellipse((x - r, y - r, x + r, y + r), fill=(0, 0, 0, 0))
        if caption:
            d.text((pw / 2, ph - 72), caption.upper(), font=font("Anton-Regular.ttf", 64), fill=(120, 38, 34), anchor="mm")
        if credit:
            d.text((pw - 64, ph - 30), credit, font=font("Poppins-SemiBold.ttf", 18), fill=(150, 140, 120), anchor="rs")
        ov = Image.new("RGBA", card.size, (0, 0, 0, 0))             # a postmark across one corner
        od = ImageDraw.Draw(ov)
        for k in range(3):
            od.ellipse((pw - 360 + k * 14, 40 + k * 14, pw - 80 - k * 14, 320 - k * 14), outline=(40, 40, 60, 120), width=6)
        for k in range(4):
            od.arc((pw - 560, 120 + k * 34, pw - 300, 240 + k * 34), 200, 340, fill=(40, 40, 60, 110), width=6)
        card.alpha_composite(ov)
    elif kind == "sticky":
        pw, ph = size, int(size * 0.7)
        card = Image.new("RGBA", (pw + 40, ph + 300), (0, 0, 0, 0))
        photo = Image.new("RGBA", (pw + 40, ph + 40), (250, 250, 250, 255))
        photo.paste(_crop(img, pw, ph), (20, 20))
        card.alpha_composite(photo, (0, 0))
        note = Image.new("RGBA", (420, 360), (255, 226, 96, 255))
        nd = ImageDraw.Draw(note)
        nd.rectangle((0, 0, 420, 40), fill=(245, 208, 70, 255))
        if caption:
            f = font("PermanentMarker-Regular.ttf", 54)
            words, lines, cur = caption.split(), [], ""
            for w_ in words:
                if nd.textlength((cur + " " + w_).strip(), font=f) > 360:
                    lines.append(cur); cur = w_
                else:
                    cur = (cur + " " + w_).strip()
            lines.append(cur)
            for i, l in enumerate(lines[:4]):
                nd.text((210, 110 + i * 66), l, font=f, fill=(40, 40, 52), anchor="mm")
        note = note.rotate(rng.uniform(4, 9), expand=True, resample=Image.BICUBIC)
        card.alpha_composite(note, (pw - 380, ph - 120))
        d = ImageDraw.Draw(card)
        d.ellipse((pw / 2 - 24, -4, pw / 2 + 24, 44), fill=(210, 50, 50, 255))   # pushpin
        d.ellipse((pw / 2 - 10, 6, pw / 2 + 4, 20), fill=(255, 160, 160, 255))
        if credit:
            d.text((26, ph + 70), credit, font=font("Poppins-SemiBold.ttf", 20), fill=(235, 235, 235), anchor="ls")
    elif kind == "clipping":
        pw, ph = size, int(size * 0.66)
        card = Image.new("RGBA", (pw + 80, ph + 260), (236, 229, 212, 255))
        g = ImageOps.grayscale(_crop(img, pw, ph)).convert("RGB")
        card.paste(ImageOps.colorize(ImageOps.grayscale(g), (40, 34, 28), (236, 229, 212)), (40, 150))
        d = ImageDraw.Draw(card)
        if caption:
            d.text((card.width / 2, 80), caption.upper(), font=font("SpecialElite-Regular.ttf", 58), fill=(30, 26, 22), anchor="mm")
        for y in range(ph + 180, ph + 250, 18):                     # body-text lines (blank, our own clipping)
            d.rectangle((40, y, card.width - 40 - rng.randint(0, 200), y + 6), fill=(150, 142, 126))
        if credit:
            d.text((card.width - 40, ph + 172), credit, font=font("Poppins-SemiBold.ttf", 18), fill=(120, 110, 96), anchor="rs")
        m = Image.new("L", card.size, 255)                            # torn edges
        md = ImageDraw.Draw(m)
        for edge in ("top", "bottom"):
            pts = [(0, 0 if edge == "top" else card.height)]
            for x in range(0, card.width + 20, 20):
                yy = rng.randint(0, 14)
                pts.append((x, yy if edge == "top" else card.height - yy))
            pts.append((card.width, 0 if edge == "top" else card.height))
            md.polygon(pts, fill=0)
        card.putalpha(m)
    else:
        pw, ph = size, int(size * 0.75)
        card = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        m = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), 36, fill=255)
        card.paste(_crop(img, pw, ph), (0, 0), m)
        if credit:
            ImageDraw.Draw(card).text((pw - 24, ph - 20), credit, font=font("Poppins-SemiBold.ttf", 20), fill=(240, 240, 240), anchor="rs")
    card = card.rotate(rng.uniform(-5, 5), expand=True, resample=Image.BICUBIC)
    return _shadow(card)


def credit_line(name, author, lic):
    page = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(name.replace("File:", "").replace(" ", "_"))
    return f"{author} ({lic}), via Wikimedia Commons: {page}"


def get(name, lic, author, kind, caption, out, job=None, seed=0, focus=(0.5, 0.45)):
    if not license_ok(lic):
        raise SystemExit(f"licence '{lic}' not allowed: only public domain, CC0 or CC BY (no SA / NC / ND, no fair use)")
    img = download(name)
    short = author if len(author) <= 28 else author[:26] + "…"
    card = frame(img, kind, caption, f"Photo: {short} · {lic}", seed)
    path = out if os.path.isabs(out) or not job else os.path.join(job, "assets", out)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    card.save(path)
    if job:
        cp = os.path.join(job, "photo_credits.json")
        cr = json.load(open(cp)) if os.path.exists(cp) else []
        line = credit_line(name, author, lic)
        if line not in cr:
            cr.append(line)
        json.dump(cr, open(cp, "w"), indent=1)
    return path


def credits(job_dir):
    cp = os.path.join(job_dir, "photo_credits.json") if job_dir else None
    return json.load(open(cp)) if cp and os.path.exists(cp) else []
