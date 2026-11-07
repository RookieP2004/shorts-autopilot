"""Procedural textures for 3D shots: fictional banknotes and price tags (never copies of real currency)."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(D, "..", "..", "fonts")
def font(name, size): return ImageFont.truetype(os.path.join(F, name), size)

def guilloche(dr, cx, cy, R, r, d, col, w=2, n=2400):
    pts = []
    for i in range(n + 1):
        t = i / n * 2 * math.pi * 7
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        pts.append((cx + x, cy + y))
    dr.line(pts, fill=col, width=w)

def banknote(path, amount, words, issuer="CENTRAL RESERVE", tint=(214, 232, 206), ink=(38, 92, 64), W=1600, H=700, big=None):
    im = Image.new("RGB", (W, H), tint)
    dr = ImageDraw.Draw(im)
    for y in range(0, H, 6):                      # fine engraving lines
        dr.line([(0, y), (W, y + 40 * math.sin(y / 37))], fill=tuple(int(c * 0.93) for c in tint), width=1)
    dr.rectangle([18, 18, W - 18, H - 18], outline=ink, width=8)
    dr.rectangle([36, 36, W - 36, H - 36], outline=ink, width=3)
    guilloche(dr, W * 0.72, H * 0.5, 230, 61, 140, (*ink, ), 2)
    guilloche(dr, W * 0.72, H * 0.5, 170, 47, 90, tuple(min(255, c + 60) for c in ink), 2)
    guilloche(dr, 210, 190, 120, 33, 70, ink, 2)
    guilloche(dr, W - 210, H - 170, 110, 29, 60, ink, 2)
    dr.ellipse([W * 0.72 - 120, H * 0.5 - 120, W * 0.72 + 120, H * 0.5 + 120], fill=tint, outline=ink, width=5)
    # emblem: a stylised globe instead of a portrait
    cx, cy = W * 0.72, H * 0.5
    for k in range(-3, 4):
        dr.arc([cx - 95 + abs(k) * 0, cy - 95, cx + 95, cy + 95], 0, 360, fill=ink, width=2)
        dr.ellipse([cx - 95 * math.cos(k / 3.5 * 1.4), cy - 95, cx + 95 * math.cos(k / 3.5 * 1.4), cy + 95], outline=ink, width=2)
    for k in range(-2, 3):
        y = cy + k * 38
        hw = math.sqrt(max(0, 95 ** 2 - (k * 38) ** 2))
        dr.line([(cx - hw, y), (cx + hw, y)], fill=ink, width=2)
    dr.text((90, 70), issuer, font=font("Poppins-ExtraBold.ttf", 54), fill=ink)
    big = big or amount
    fs = 190 if len(big) <= 4 else max(70, int(1500 / len(big)))
    dr.text((90, H * 0.52), big, font=font("Anton-Regular.ttf", fs), fill=ink, anchor="lm")
    dr.text((90, H - 95), words, font=font("Poppins-ExtraBold.ttf", 40), fill=ink, anchor="lm")
    dr.text((W - 90, 80), amount if len(amount) < 6 else "", font=font("Anton-Regular.ttf", 110), fill=ink, anchor="rt")
    dr.text((W - 330, H - 70), "A 0042 7781", font=font("Poppins-SemiBold.ttf", 34), fill=(150, 40, 40), anchor="lm")
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(path)

def price_tag(path, text, bg=(250, 246, 236), ink=(26, 20, 16), W=600, H=360):
    im = Image.new("RGB", (W, H), bg)
    dr = ImageDraw.Draw(im)
    dr.rectangle([10, 10, W - 10, H - 10], outline=(220, 70, 60), width=14)
    dr.text((W / 2, H / 2 + 10), text, font=font("Anton-Regular.ttf", 220), fill=ink, anchor="mm")
    im.save(path)

if __name__ == "__main__":
    banknote(os.path.join(D, "note_1.png"), "$1", "ONE DOLLAR", "ISLAND RESERVE BANK")
    banknote(os.path.join(D, "note_100t.png"), "", "ONE HUNDRED TRILLION DOLLARS", "RESERVE BANK",
             tint=(228, 212, 236), ink=(88, 40, 96), big="100 000 000 000 000")
    price_tag(os.path.join(D, "tag_1.png"), "$1")
    price_tag(os.path.join(D, "tag_2.png"), "$2")
    print("ok")
