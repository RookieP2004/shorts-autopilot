"""Ved (and the cast) drawn in the look of the scene: a character layer with "style" set to one of STYLES is
re-drawn from its own flat-vector art, so a whiteboard shot gets a marker Ved, a chalk shot a chalk Ved, and so on.
Same character, same poses and lip-sync: only the rendering changes.  Results are cached per sprite."""
import weakref

import numpy as np
import cv2
from PIL import Image

STYLES = ("marker", "chalk", "riso", "film", "ink")

_cache = {}


def _edges(rgba, width_px, step=24, lo=12, hi=36):
    a = rgba[..., 3]
    rgb = rgba[..., :3].copy()
    rgb[a < 128] = 255
    q = (rgb // step) * step                                  # flat colour regions -> clean edges between them
    g = cv2.cvtColor(q.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    g = cv2.medianBlur(g, 3)
    e = cv2.Canny(g, lo, hi)
    e |= cv2.Canny((a > 128).astype(np.uint8) * 255, 50, 150)   # silhouette
    k = max(1, int(round(width_px)))
    d = cv2.dilate(e, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))).astype(np.float32) / 255
    return cv2.GaussianBlur(d, (0, 0), 0.7)              # soft, anti-aliased line (0..1)


def _noise(shape, seed, scale):
    rng = np.random.default_rng(seed)
    h, w = shape
    sm = rng.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    return cv2.resize(sm, (w, h), interpolation=cv2.INTER_CUBIC)


def _lum(rgb):
    return (rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114) / 255.0


def marker(rgba, seed=7):
    """Whiteboard: black marker outline, light marker fills, gold accents kept."""
    h, w = rgba.shape[:2]
    lw = max(2, w / 300)
    e = _edges(rgba, lw, step=40, lo=30, hi=80)
    a = rgba[..., 3].astype(np.float32) / 255
    rgb = rgba[..., :3].astype(np.float32)
    fill = 255 - (255 - rgb) * 0.28                       # pale wash of the real colours
    dark = _lum(rgb) < 0.22                                # hair, beard, trousers: marker hatch
    yy, xx = np.mgrid[0:h, 0:w]
    hatch = ((xx + yy) % max(5, int(w / 70))) < max(1.5, w / 400)
    fill[dark & hatch] = (40, 42, 54)
    out = np.dstack([fill, a * 255])
    ink = np.array([27, 27, 34], np.float32)
    m = e[..., None]
    out[..., :3] = out[..., :3] * (1 - m) + ink * m
    out[..., 3] = np.maximum(out[..., 3], e * 255)
    return out.clip(0, 255).astype(np.uint8)


def chalk(rgba, seed=7):
    """Chalkboard: broken off-white chalk lines, a faint dust fill so the figure still reads as solid."""
    h, w = rgba.shape[:2]
    e = _edges(rgba, max(2, w / 150)).astype(np.float32)
    grain = _noise((h, w), seed, 2) * 0.6 + _noise((h, w), seed + 1, 9) * 0.4
    line = e * np.clip(grain * 1.6 - 0.15, 0, 1)
    a = rgba[..., 3].astype(np.float32) / 255
    lum = _lum(rgba[..., :3].astype(np.float32))
    dust = a * (0.10 + 0.22 * lum) * np.clip(grain * 1.3, 0, 1)
    al = np.clip(line + dust, 0, 1)
    col = np.zeros((h, w, 3), np.float32) + (238, 236, 226)
    accent = (rgba[..., 0] > 180) & (rgba[..., 2] < 110) & (rgba[..., 1] > 130)     # gold -> yellow chalk
    col[accent] = (247, 214, 102)
    return np.dstack([col, al * 255]).clip(0, 255).astype(np.uint8)


def riso(rgba, seed=7):
    """Two-ink risograph: blue plate for shadows and line, fluorescent pink for warm areas; halftone, misregistered."""
    h, w = rgba.shape[:2]
    a = rgba[..., 3].astype(np.float32) / 255
    rgb = rgba[..., :3].astype(np.float32)
    lum = _lum(rgb)
    warm = np.clip((rgb[..., 0] - rgb[..., 2]) / 120, 0, 1)
    cell = max(4, int(w / 110))
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx % cell) / cell - 0.5
    v = (yy % cell) / cell - 0.5
    dot = np.sqrt(u * u + v * v) / 0.707                    # 0 centre -> 1 corner
    blue_amt = np.clip(1.0 - lum * 1.05, 0, 1)
    pink_amt = np.clip(warm * 0.85 + (1 - lum) * 0.2, 0, 1)
    blue = (dot < blue_amt).astype(np.float32)
    pink = (dot < pink_amt).astype(np.float32)
    shift = max(2, int(w / 220))
    pink = np.roll(pink, (shift, -shift), (0, 1))
    pa = np.roll(a, (shift, -shift), (0, 1))
    paper = np.array([246, 240, 228], np.float32)
    B = np.array([0, 120, 191], np.float32)
    P = np.array([255, 72, 176], np.float32)
    col = paper * np.ones((h, w, 1), np.float32)
    kp = (pink * pa * 0.9)[..., None]
    kb = (blue * a * 0.85)[..., None]
    col = col * (1 - kp + kp * P / 255)                   # inks multiply like real overprint
    col = col * (1 - kb + kb * B / 255)
    al = np.clip(np.maximum(a, pa * pink), 0, 1)
    return np.dstack([col, al * 255]).clip(0, 255).astype(np.uint8)


def film(rgba, seed=7):
    """Silent film: orthochromatic black and white, crushed blacks, warm-silver highlights, fine grain."""
    h, w = rgba.shape[:2]
    rgb = rgba[..., :3].astype(np.float32)
    lum = 0.15 * rgb[..., 0] + 0.45 * rgb[..., 1] + 0.40 * rgb[..., 2]   # ortho film: reds go dark
    lum = lum / 255
    lum = np.clip((lum - 0.08) / 0.86, 0, 1) ** 1.15
    lum = lum + (_noise((h, w), seed, 1) - 0.5) * 0.09
    lum = np.clip(lum, 0, 1)
    col = np.dstack([lum * 242 + 8, lum * 236 + 8, lum * 222 + 10])
    return np.dstack([col, rgba[..., 3]]).clip(0, 255).astype(np.uint8)


def ink(rgba, seed=7):
    """Ink wash: three grey washes on rice-paper white, dry-brush outline, gold kept as vermilion seal red."""
    h, w = rgba.shape[:2]
    rgb = rgba[..., :3].astype(np.float32)
    lum = _lum(rgb)
    levels = np.select([lum < 0.22, lum < 0.55, lum < 0.8], [0.12, 0.45, 0.78], 0.97)
    bleed = cv2.GaussianBlur(levels.astype(np.float32), (0, 0), max(1.0, w / 400))
    tone = bleed + (_noise((h, w), seed, 24) - 0.5) * 0.10
    e = _edges(rgba, max(2, w / 220), step=40, lo=30, hi=80)
    dry = np.clip(_noise((h, w), seed + 3, 5) * 1.6, 0, 1)             # dry brush: the stroke thins, never dots
    e = e * (0.55 + 0.45 * dry)
    tone = tone * (1 - e) + 0.06 * e
    paper = np.array([243, 236, 220], np.float32)
    inkc = np.array([22, 20, 24], np.float32)
    col = inkc + (paper - inkc) * tone[..., None]
    gold = (rgba[..., 0] > 180) & (rgba[..., 2] < 110) & (rgba[..., 1] > 130)
    col[gold] = (196, 46, 36)
    a = rgba[..., 3].astype(np.float32)
    a = np.maximum(a, 255 * e)
    return np.dstack([col, a]).clip(0, 255).astype(np.uint8)


FN = {"marker": marker, "chalk": chalk, "riso": riso, "film": film, "ink": ink}


def apply(img, style, seed=7):
    """img: RGBA PIL image of a character sprite -> the same sprite drawn in `style` (cached per sprite)."""
    if not style or style not in FN:
        return img
    k = (id(img), style, seed)
    hit = _cache.get(k)
    if hit and hit[0]() is img:
        return hit[1]
    out = Image.fromarray(FN[style](np.asarray(img.convert("RGBA")), seed), "RGBA")
    if len(_cache) > 400:
        _cache.clear()
    _cache[k] = (weakref.ref(img), out)
    return out
