"""Simple 3D for The Explainer: low-poly, toon-shaded, drawn in code (no GPU, no outside tools).

Same rules as the 2D style so both mix in one frame:
  * key light warm from the upper-left, shadows go cool (same shade()/light() maths as the characters)
  * 3-band cel shading (lit / mid / shadow) instead of smooth gradients
  * distance fades toward the fog/sky colour (atmospheric perspective)
  * people are faceless mannequins: readable silhouettes, no features to get wrong

Rendering is a painter's algorithm: every triangle is projected, shaded, depth-sorted and filled
with PIL at 2x size, then downsampled for clean edges.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from .spec import color, hex_rgba

COOL = np.array([46, 58, 110], dtype=float)
KEY = np.array([255, 241, 214], dtype=float)


# ------------------------------------------------------------------ meshes (verts Nx3, faces Mx3)
def box(sx=1, sy=1, sz=1):
    x, y, z = sx / 2, sy / 2, sz / 2
    v = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z],
                  [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]], float)
    f = np.array([[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4],
                  [3, 6, 2], [3, 7, 6], [0, 4, 7], [0, 7, 3], [1, 2, 6], [1, 6, 5]])
    return v, f


def sphere(r=1, seg=14, rings=9):
    v = [[0, r, 0]]
    for i in range(1, rings):
        th = math.pi * i / rings
        for j in range(seg):
            ph = 2 * math.pi * j / seg
            v.append([r * math.sin(th) * math.cos(ph), r * math.cos(th), r * math.sin(th) * math.sin(ph)])
    v.append([0, -r, 0])
    f = []
    for j in range(seg):
        f.append([0, 1 + (j + 1) % seg, 1 + j])
    for i in range(rings - 2):
        a, b = 1 + i * seg, 1 + (i + 1) * seg
        for j in range(seg):
            j2 = (j + 1) % seg
            f.append([a + j, a + j2, b + j])
            f.append([a + j2, b + j2, b + j])
    last = len(v) - 1
    base = 1 + (rings - 2) * seg
    for j in range(seg):
        f.append([last, base + j, base + (j + 1) % seg])
    return np.array(v, float), np.array(f)


def cylinder(r=1, h=1, seg=12, r2=None, cap=True):
    """Along +y from 0 to h. r2 = top radius (cone if 0)."""
    r2 = r if r2 is None else r2
    v = []
    for j in range(seg):
        a = 2 * math.pi * j / seg
        v.append([r * math.cos(a), 0, r * math.sin(a)])
    for j in range(seg):
        a = 2 * math.pi * j / seg
        v.append([r2 * math.cos(a), h, r2 * math.sin(a)])
    v += [[0, 0, 0], [0, h, 0]]
    f = []
    for j in range(seg):
        j2 = (j + 1) % seg
        f.append([j, seg + j, j2])
        f.append([j2, seg + j, seg + j2])
        if cap:
            f.append([2 * seg, j, j2])
            f.append([2 * seg + 1, seg + j2, seg + j])
    return np.array(v, float), np.array(f)


def plane(w=10, d=10, n=1):
    xs = np.linspace(-w / 2, w / 2, n + 1)
    zs = np.linspace(-d / 2, d / 2, n + 1)
    v = np.array([[x, 0, z] for z in zs for x in xs], float)
    f = []
    for i in range(n):
        for j in range(n):
            a = i * (n + 1) + j
            f += [[a, a + n + 1, a + 1], [a + 1, a + n + 1, a + n + 2]]
    return v, np.array(f)


def terrain(w=60, d=60, n=24, height=4, seed=1, flat_center=0.0):
    rng = np.random.default_rng(seed)
    v, f = plane(w, d, n)
    g = rng.random((n + 1, n + 1))
    for _ in range(3):  # smooth value noise
        g = (g + np.roll(g, 1, 0) + np.roll(g, -1, 0) + np.roll(g, 1, 1) + np.roll(g, -1, 1)) / 5
    g = (g - g.min()) / (np.ptp(g) + 1e-9)
    hgt = g.reshape(-1) * height
    if flat_center:
        rr = np.hypot(v[:, 0], v[:, 2])
        hgt *= np.clip((rr - flat_center) / (flat_center + 1e-9), 0, 1)
    v[:, 1] = hgt
    return v, f


def merge(parts):
    vs, fs, cs, n = [], [], [], 0
    for v, f, c in parts:
        vs.append(v)
        fs.append(f + n)
        cs += [c] * len(f)
        n += len(v)
    return np.vstack(vs), np.vstack(fs), cs


def rot_matrix(rx=0, ry=0, rz=0):
    rx, ry, rz = map(math.radians, (rx, ry, rz))
    X = np.array([[1, 0, 0], [0, math.cos(rx), -math.sin(rx)], [0, math.sin(rx), math.cos(rx)]])
    Y = np.array([[math.cos(ry), 0, math.sin(ry)], [0, 1, 0], [-math.sin(ry), 0, math.cos(ry)]])
    Z = np.array([[math.cos(rz), -math.sin(rz), 0], [math.sin(rz), math.cos(rz), 0], [0, 0, 1]])
    return Y @ X @ Z


def place(v, pos=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
    return (v * scale) @ rot_matrix(*rot).T + np.array(pos, float)


def limb(a, b, r, seg=8):
    """Cylinder from point a to point b."""
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    L = np.linalg.norm(d) or 1e-6
    v, f = cylinder(r, L, seg, r * 0.85)
    y = d / L
    x = np.cross(y, [0, 0, 1.0])
    if np.linalg.norm(x) < 1e-6:
        x = np.cross(y, [1.0, 0, 0])
    x /= np.linalg.norm(x)
    z = np.cross(x, y)
    M = np.stack([x, y, z], axis=1)
    return v @ M.T + a, f


# ------------------------------------------------------------------ faceless person
def person(t, body="#34425c", skin="#c98d68", legs=None, walk=0.0, action="idle", height=1.75, phase=0.0):
    """Mannequin built from primitives, facing +z. walk = steps per second (0 = standing)."""
    s = height / 1.75
    legs = legs or body
    ph = 2 * math.pi * (walk * t) + phase
    sw = math.sin(ph) * (0.45 if walk else 0.0)
    bob = abs(math.sin(ph)) * 0.03 if walk else 0.012 * math.sin(t * 2.2 + phase)
    parts = []
    hip_y, sh_y = 0.92, 1.44
    # legs (hip -> knee -> ankle), knee bends on the back swing
    for side, k in ((-1, 1), (1, -1)):
        a = sw * k
        hip = (0.1 * side, hip_y + bob, 0)
        knee = (0.1 * side, hip_y + bob - 0.45 * math.cos(a), 0.45 * math.sin(a))
        bend = max(0.0, -math.sin(ph) * k) * 0.5 if walk else 0.0
        ankle = (0.1 * side, knee[1] - 0.44 * math.cos(a - bend), knee[2] + 0.44 * math.sin(a - bend))
        parts += [(*limb(hip, knee, 0.075), legs), (*limb(knee, ankle, 0.06), legs)]
        fv, ff = box(0.1, 0.07, 0.24)
        parts.append((place(fv, (ankle[0], ankle[1] - 0.02, ankle[2] + 0.06)), ff, "#2b2420"))
    # torso + hips + neck + head (no face)
    tv, tf = cylinder(0.19, 0.58, 10, 0.21)
    parts.append((place(tv, (0, hip_y + bob - 0.04, 0), scale=1.0) * [1, 1, 0.62] + [0, 0, 0], tf, body))
    nv, nf = cylinder(0.05, 0.1, 8)
    parts.append((place(nv, (0, sh_y + bob + 0.08, 0)), nf, skin))
    hv, hf = sphere(0.115, 14, 10)
    parts.append((place(hv, (0, sh_y + bob + 0.26, 0)) * [1, 1, 1], hf, skin))
    # arms
    for side in (-1, 1):
        sh = (0.23 * side, sh_y + bob + 0.02, 0)
        if action == "wave" and side == 1:
            el = (0.42, sh_y + 0.18, 0.0)
            wr = (0.45 + 0.08 * math.sin(t * 9), sh_y + 0.46, 0.04)
        elif action == "point" and side == 1:
            el = (0.36, sh_y + 0.02, 0.25)
            wr = (0.44, sh_y + 0.08, 0.52)
        elif action == "cheer":
            el = (0.36 * side, sh_y + 0.22, 0.0)
            wr = (0.40 * side, sh_y + 0.52 + 0.04 * math.sin(t * 6 + side), 0.0)
        else:
            a = -sw * side * 0.8 if walk else 0.04 * math.sin(t * 1.7 + side)
            el = (0.25 * side, sh[1] - 0.29 * math.cos(a), 0.29 * math.sin(a))
            wr = (0.25 * side, el[1] - 0.27 * math.cos(a * 1.4 + 0.15), el[2] + 0.27 * math.sin(a * 1.4 + 0.15))
        parts += [(*limb(sh, el, 0.05), body), (*limb(el, wr, 0.042), body)]
        gv, gf = sphere(0.05, 8, 5)
        parts.append((place(gv, wr), gf, skin))
    v, f, c = merge(parts)
    return v * s, f, c


def tree(seed=0, color_leaf="#4f6e3a", trunk="#5a3d29"):
    rng = np.random.default_rng(seed)
    h = 2.2 + rng.random() * 1.6
    tv, tf = cylinder(0.12, h * 0.45, 7)
    parts = [(tv, tf, trunk)]
    for i in range(3):
        cv, cf = cylinder(0.95 - i * 0.22, 0.9, 9, 0.0)
        parts.append((place(cv, (0, h * 0.35 + i * 0.55, 0)), cf, color_leaf))
    return merge(parts)


def building(w=4, d=4, h=8, color_="#b9a88f", roof="#7c2533", windows="#ffd98f"):
    bv, bf = box(w, h, d)
    parts = [(place(bv, (0, h / 2, 0)), bf, color_)]
    rv, rf = cylinder(max(w, d) * 0.75, 1.6, 4, 0.0)
    parts.append((place(rv, (0, h, 0), (0, 45, 0)), rf, roof))
    for fl in range(1, int(h // 2)):
        for k in (-1, 0, 1):
            wv, wf = box(w * 0.16, 0.7, 0.05)
            parts.append((place(wv, (k * w * 0.28, fl * 2, d / 2 + 0.03)), wf, windows))
    return merge(parts)


# ------------------------------------------------------------------ scene description -> triangles
def ease(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def lerp3(a, b, p):
    return [a[i] + (b[i] - a[i]) * p for i in range(3)]


def build_object(o, t, style):
    kind = o.get("shape", "box")
    col = color(style, o.get("color", "#b9a88f"))
    if kind == "box":
        v, f = box(*o.get("size", [1, 1, 1]))
        cs = [col] * len(f)
    elif kind == "sphere":
        v, f = sphere(o.get("r", 0.5), o.get("seg", 20), o.get("rings", 12))
        cs = [col] * len(f)
    elif kind in ("cylinder", "cone"):
        v, f = cylinder(o.get("r", 0.5), o.get("h", 1), o.get("seg", 12), 0.0 if kind == "cone" else o.get("r2"))
        cs = [col] * len(f)
    elif kind == "plane":
        v, f = plane(o.get("w", 40), o.get("d", 40), o.get("n", 12))
        cs = [col] * len(f)
    elif kind == "terrain":
        v, f = terrain(o.get("w", 80), o.get("d", 80), o.get("n", 26), o.get("height", 6), o.get("seed", 1),
                       o.get("flat_center", 0))
        cs = [col] * len(f)
    elif kind == "person":
        v, f, cs = person(t, color(style, o.get("color", "#34425c")), color(style, o.get("skin", "#c98d68")),
                          color(style, o["legs"]) if o.get("legs") else None, o.get("walk", 0.0),
                          o.get("action", "idle"), o.get("height", 1.75), o.get("phase", 0.0))
    elif kind == "tree":
        v, f, cs = tree(o.get("seed", 0), color(style, o.get("color", "#4f6e3a")))
    elif kind == "building":
        v, f, cs = building(o.get("w", 4), o.get("d", 4), o.get("h", 8), col,
                            color(style, o.get("roof", "#7c2533")), color(style, o.get("windows", "#ffd98f")))
    else:
        raise ValueError(f"unknown 3D shape {kind}")
    pos = list(o.get("pos", [0, 0, 0]))
    rot = list(o.get("rot", [0, 0, 0]))
    mv = o.get("move")
    if mv:  # {"to":[x,y,z], "dur": s, "at": s}
        p = ease((t - mv.get("at", 0)) / max(0.01, mv.get("dur", 2)))
        pos = lerp3(pos, mv["to"], p)
    if o.get("walk") and o.get("travel"):  # walk forward along facing
        a = math.radians(rot[1])
        d = o["travel"] * t
        pos = [pos[0] + math.sin(a) * d, pos[1], pos[2] + math.cos(a) * d]
    sp = o.get("spin")
    if sp:
        rot = [rot[i] + sp[i] * t for i in range(3)]
    if o.get("bob"):
        pos[1] += math.sin(t * 2.4) * o["bob"]
    v = place(v, pos, rot, o.get("scale", 1.0))
    # ground layers (terrain, then paths/planes) are painted first in a fixed order: avoids flicker between
    # big terrain triangles and the small path triangles lying on top of them
    ground = o.get("ground_order", {"terrain": 0, "plane": 1}.get(kind))
    return v, f, cs, bool(o.get("two_sided", kind in ("plane", "terrain"))), ground


def camera_at(cam, t, dur):
    pos = list(cam.get("pos", [0, 1.6, 8]))
    target = list(cam.get("target", [0, 1.2, 0]))
    if cam.get("move"):
        p = ease(t / max(0.01, cam["move"].get("dur", dur)))
        pos = lerp3(pos, cam["move"]["to"], p)
        if "target_to" in cam["move"]:
            target = lerp3(target, cam["move"]["target_to"], p)
    if cam.get("orbit"):  # degrees per second around the target (y axis)
        a = math.radians(cam["orbit"] * t)
        dx, dz = pos[0] - target[0], pos[2] - target[2]
        pos[0] = target[0] + dx * math.cos(a) - dz * math.sin(a)
        pos[2] = target[2] + dx * math.sin(a) + dz * math.cos(a)
    if cam.get("dolly"):  # [start_factor, end_factor] on the distance to target
        k = cam["dolly"][0] + (cam["dolly"][1] - cam["dolly"][0]) * ease(t / max(0.01, dur))
        pos = [target[i] + (pos[i] - target[i]) * k for i in range(3)]
    return np.array(pos, float), np.array(target, float), cam.get("fov", 45)


def _rgbarr(c):
    return np.array(hex_rgba(c)[:3], float)


def render(style, L, t, dur, w, h, ss=2):
    """Render a scene3d layer to an RGBA image of size (w, h)."""
    W2, H2 = int(w * ss), int(h * ss)
    sky = L.get("sky")
    if sky:
        cols = [_rgbarr(color(style, c)) for c in sky]
        ys = np.linspace(0, 1, H2)[:, None]
        grad = cols[0] * (1 - ys) + cols[-1] * ys if len(cols) == 2 else \
            np.where(ys < 0.5, cols[0] * (1 - ys * 2) + cols[1] * ys * 2, cols[1] * (2 - ys * 2) + cols[2] * (ys * 2 - 1))
        arr = np.repeat(grad[:, None, :], W2, axis=1)
        img = Image.fromarray(np.dstack([arr, np.full((H2, W2), 255)]).astype(np.uint8), "RGBA")
    else:
        img = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    C, T, fov = camera_at(L.get("camera", {}), t, dur)
    fwd = T - C
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 1.0, 0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    focal = (H2 / 2) / math.tan(math.radians(fov) / 2)
    ld = np.array(L.get("light", [-0.6, -0.8, -0.5]), float)   # direction light travels: from upper-left-front
    ld /= np.linalg.norm(ld)
    fog = L.get("fog", {})
    fog_col = _rgbarr(color(style, fog.get("color", (sky or ["#cfd9cf"])[-1] if sky else "#cfd9cf")))
    fog_near, fog_far, fog_max = fog.get("near", 12), fog.get("far", 70), fog.get("max", 0.85)
    toon = L.get("toon", True)
    polys = []
    for o in L.get("objects", []):
        v, f, cs, two, ground = build_object(o, t, style)
        rel = v - C
        x, y, z = rel @ right, rel @ up, rel @ fwd
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nl = np.linalg.norm(n, axis=1)
        n /= np.maximum(nl, 1e-9)[:, None]
        cen = tri.mean(axis=1)
        facing = np.einsum("ij,ij->i", n, C - cen)
        if two:
            n = np.where((facing < 0)[:, None], -n, n)
        zf = z[f]
        ok = (zf.min(axis=1) > 0.05) & (two | (facing > 0)) & (nl > 1e-12)
        diff = np.clip(-(n @ ld), 0, 1)
        sx = W2 / 2 + x[f] / np.maximum(zf, 1e-3) * focal
        sy = H2 / 2 - y[f] / np.maximum(zf, 1e-3) * focal
        depth = zf.mean(axis=1)
        for i in np.nonzero(ok)[0]:
            base = _rgbarr(cs[i])
            dl = diff[i]
            if toon:   # low-poly: each face gets its own tone between cool shadow and warm lit
                q = dl * dl * (3 - 2 * dl)
                lit = base * 0.84 + KEY * 0.16
                shd = base * 0.68 * 0.72 + COOL * 0.28
                c = shd * (1 - q) + lit * q
            else:
                k = 0.45 + 0.55 * dl
                c = base * k * (1 - 0.2 * (1 - dl)) + COOL * 0.2 * (1 - dl)
            fz = np.clip((depth[i] - fog_near) / max(1e-6, fog_far - fog_near), 0, 1) * fog_max
            c = c * (1 - fz) + fog_col * fz
            key = (0, ground, -depth[i]) if ground is not None else (1, 0, -depth[i])
            polys.append((key, [(sx[i, k], sy[i, k]) for k in range(3)], tuple(int(max(0, min(255, q))) for q in c)))
    polys.sort(key=lambda p: p[0])
    for _, pts, c in polys:
        draw.polygon(pts, fill=c + (255,), outline=c + (255,))
    if ss != 1:
        img = img.resize((w, h), Image.LANCZOS)
    return img
