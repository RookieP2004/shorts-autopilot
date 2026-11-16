# 2026-11-16-a: "12 colour sensors... and worse colour vision than you" (myth-bust, mantis shrimp).
# Sets: a bright marine "REEF LAB" (coral-red wainscot, sea-green walls, shelves of little reef tanks, a big reef tank on
# a bench as the foreground layer with a mantis shrimp inside and two optic-fibre lights hanging into the water), 2 angles
# (wide, mid on the tank); an underwater reef close-up inside the tank (sand, rubble burrow, corals, two fibre-light tips).
# Cut-outs: the hero peacock mantis shrimp (side view), a food pellet.
import math, os, random

# drop_cams(), gravel(), weed(), lever() ... (frozen helpers from 2026-11-09-c)
_src = open(os.path.join(ROOT, "jobs/2026-11-09-c/assets.py")).read().split("\ndef tank(")[0]
exec(compile(_src, "c09_helpers", "exec"), globals())


def mantis(loc=(0, 0, 0), s=1.0, yaw=0, name="mantis"):
    """Peacock mantis shrimp facing +X, body length ~0.5*s, resting on z=loc.z. Returns all parts."""
    x0, y0, z0 = loc
    parts = []
    green = mat("ms_green", "#2fa36b", rough=0.3, coat=0.7, sss=0.15)
    teal = mat("ms_teal", "#1f8f8a", rough=0.3, coat=0.7, sss=0.15)
    orange = mat("ms_orange", "#f08a24", rough=0.35, coat=0.5)
    red = mat("ms_red", "#e0455a", rough=0.3, coat=0.6)
    blue = mat("ms_blue", "#2f7fe0", rough=0.25, coat=0.8)
    spot = mat("ms_spot", "#f2d04a", rough=0.3, coat=0.5)
    # segmented abdomen + carapace: a gentle arch from tail (-x) to head (+x)
    n = 9
    for k in range(n):
        u = k / (n - 1)
        x = -0.26 + u * 0.44
        z = 0.06 + 0.025 * math.sin(u * math.pi)
        r = 0.05 + 0.012 * math.sin(u * math.pi)
        o = sphere(r * s, (x * s, 0, z * s), (0.95, 1.15, 0.7), green if k % 2 == 0 else teal, seg=32)
        parts.append(o)
        if 2 <= k <= 6:      # yellow side spots
            for sy in (-1, 1):
                parts.append(sphere(0.012 * s, (x * s, sy * r * 0.95 * s, (z + 0.01) * s), 1, spot, seg=12))
    # head shield
    parts.append(sphere(0.065 * s, (0.22 * s, 0, 0.075 * s), (1.2, 0.9, 0.6), green, seg=32))
    # tail fan: blue paddles with orange edges
    for k, a in enumerate((-50, -20, 0, 20, 50)):
        p = sphere(0.09 * s, (-0.31 * s, 0, 0.05 * s), (1.0, 0.4, 0.1), blue if k % 2 else orange, seg=24)
        p.rotation_euler = (0, math.radians(-10), math.radians(a))
        p.location = (s * (-0.33 - 0.05 * math.cos(math.radians(a))), s * 0.09 * math.sin(math.radians(a)), 0.06 * s)
        parts.append(p)
    # walking legs (orange) and swimmerets
    for k in range(5):
        for sy in (-1, 1):
            c = cylinder(0.008 * s, 0.045 * s, ((-0.02 + k * 0.045) * s, sy * 0.05 * s, 0.03 * s), (sy * 30, 0, 0), orange, verts=10, bevel=0)
            parts.append(c)
    # raptorial clubs: folded red arms with a heavy club under the head
    for sy in (-1, 1):
        a = cylinder(0.016 * s, 0.11 * s, (0.28 * s, sy * 0.045 * s, 0.06 * s), (0, 60, 0), red, verts=16, bevel=0.003)
        parts.append(a)
        parts.append(sphere(0.026 * s, (0.31 * s, sy * 0.045 * s, 0.025 * s), (1.4, 0.9, 0.9), red, seg=24))
    # antennal scales (orange flaps) and antennae
    for sy in (-1, 1):
        f = sphere(0.06 * s, (0.31 * s, sy * 0.05 * s, 0.1 * s), (1.0, 0.35, 0.15), orange, seg=20)
        f.rotation_euler = (0, math.radians(-25), math.radians(sy * 25)); parts.append(f)
        ant = cylinder(0.004 * s, 0.22 * s, (0.38 * s, sy * 0.05 * s, 0.17 * s), (sy * 15, 55, 0), orange, verts=8, bevel=0)
        parts.append(ant)
    # the famous eyes: stalks + split eyes with a dark mid-band
    eye_m = mat("ms_eye", "#3fbf7f", rough=0.15, coat=1.0)
    band = mat("ms_band", "#1a2a2a", rough=0.2, coat=1.0)
    for sy in (-1, 1):
        parts.append(cylinder(0.012 * s, 0.1 * s, (0.3 * s, sy * 0.035 * s, 0.15 * s), (sy * -25, 15, 0), teal, verts=12, bevel=0))
        e = sphere(0.045 * s, (0.315 * s, sy * 0.06 * s, 0.215 * s), (0.85, 0.85, 1.3), eye_m, seg=32); parts.append(e)
        parts.append(torus(0.043 * s, 0.009 * s, (0.315 * s, sy * 0.06 * s, 0.215 * s), (0, 0, 0), band))
    for p in parts:
        p.location = (p.location.x + x0, p.location.y + y0, p.location.z + z0)
    return parts


def coral(x, y, z, s=1.0, seed=0, color="#e86aa6"):
    random.seed(seed)
    m = bpy.data.materials.get("coral" + color) or mat("coral" + color, color, rough=0.6, sss=0.2, noise_bump=0.2)
    out = []
    for k in range(7):
        a = random.uniform(0, 2 * math.pi); h = random.uniform(0.5, 1.0) * s
        tip = (x + math.cos(a) * 0.12 * s, y + math.sin(a) * 0.12 * s, z + h)
        o = cylinder(0.035 * s, h, (x + math.cos(a) * 0.06 * s, y + math.sin(a) * 0.06 * s, z + h / 2),
                     (math.degrees(math.sin(a)) * 0.4, math.degrees(math.cos(a)) * 0.4, 0), m, verts=12, bevel=0.01)
        out.append(o)
        out.append(sphere(0.05 * s, tip, 1, m, seg=16))
    return out


def brain_coral(x, y, z, r=0.3, color="#f2b04a"):
    return sphere(r, (x, y, z), (1.2, 1.0, 0.7), mat("bcoral" + color, color, rough=0.7, noise_bump=0.8), seg=40)


def fibre(x, y, ztop, zend, name="fibre"):
    """A thin black optic-fibre cable from above, ending in a bright white tip (colour is added in 2D)."""
    cab = mat("cable", "#1d1d22", rough=0.4)
    cylinder(0.012, ztop - zend, (x, y, (ztop + zend) / 2), material=cab, verts=12, bevel=0)
    cylinder(0.02, 0.05, (x, y, zend + 0.02), material=metal("#9aa3ab", 0.3, "ferrule"), verts=16, bevel=0)
    sphere(0.025, (x, y, zend - 0.01), 1, mat("fibre_tip", "#ffffff", emit="#ffffff", emit_strength=3.0), seg=16)


def reef_tank(x, y, zb, w=1.4, d=0.55, h=0.7):
    out = []
    frame = mat("tank_frame2", "#1f2a3a", rough=0.4)
    g = mat("tank_glass", "#e8f6ff", rough=0.03, transmission=1.0, ior=1.2, alpha=0.25)
    water = mat("reef_water", "#6fc3d6", rough=0.05, alpha=0.2, emit="#4fb0d0", emit_strength=0.25)
    out.append(box((w, d, 0.04), (x, y, zb + 0.02), material=frame, bevel=0.01))
    out.append(box((w, d, 0.03), (x, y, zb + h), material=frame, bevel=0.01))
    out.append(box((w - 0.04, d - 0.04, h * 0.86), (x, y, zb + 0.04 + h * 0.43), material=water, bevel=0.005))
    out.append(box((w, 0.01, h), (x, y - d / 2, zb + h / 2), material=g, bevel=0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            out.append(box((0.03, 0.03, h), (x + sx * (w / 2 - 0.015), y + sy * (d / 2 - 0.015), zb + h / 2), material=frame, bevel=0.004))
    random.seed(7)
    cols = ["#efe0c0", "#d9c4a0", "#f6efe2", "#e8a39a"]
    for k in range(140):
        c = cols[k % len(cols)]
        out.append(sphere(random.uniform(0.012, 0.024), (x + random.uniform(-w / 2 + 0.04, w / 2 - 0.04), y + random.uniform(-d / 2 + 0.04, d / 2 - 0.04), zb + 0.05),
                          (1, 1, 0.7), bpy.data.materials.get("grv" + c) or mat("grv" + c, c, rough=0.6), seg=10))
    out += coral(x - 0.48, y + 0.1, zb + 0.05, 0.4, 1, "#e86aa6")
    out += coral(x + 0.5, y + 0.12, zb + 0.05, 0.35, 2, "#f08a24")
    out.append(brain_coral(x - 0.2, y + 0.15, zb + 0.08, 0.1))
    for k, (wx, col) in enumerate(((0.3, "#4f9e4a"), (-0.6, "#3f8f45"))):
        weed(x + wx, y + 0.18, zb + 0.05, 0.4, k + 5, col)
    out += mantis((x + 0.05, y - 0.08, zb + 0.06), 0.55, 15, "tank_ms")
    # two fibre lights into the water from a little black box on the lid
    out.append(box((0.3, 0.2, 0.12), (x + 0.1, y, zb + h + 0.07), material=mat("lightbox", "#25262b", rough=0.4), bevel=0.02))
    for fx in (-0.05, 0.25):
        fibre(x + fx, y - 0.05, zb + h + 0.05, zb + 0.32)
    return out


# ---------------------------------------------------------------- the reef lab
def build_lab():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15)
    world_color(hexrgb("#e3f1ee"), 1.0)
    plane(40, 40, (0, 0, 0), material=wood("#d2a46a", "#b0844e", "floor_wood2", 1.2, 0.45), name="floor")
    box((7.0, 3.4, 0.02), (0.2, -0.8, 0.01), material=mat("rug", "#1f6f78", rough=0.9), bevel=0.005)
    box((6.6, 3.0, 0.025), (0.2, -0.8, 0.012), material=mat("rug_in", "#f2b04a", rough=0.9), bevel=0.005)
    box((30, 0.3, 9), (0, 4.6, 4.5), material=mat("wall2", "#bfe3da", rough=0.7), bevel=0)
    box((30, 0.1, 1.2), (0, 4.42, 0.6), material=mat("wainscot2", "#c4523f", rough=0.5, coat=0.3), bevel=0.02)
    box((30, 0.14, 0.06), (0, 4.4, 1.22), material=metal("#c9a24a", 0.3, "trim"), bevel=0.01)
    box((0.3, 20, 9), (-6.5, -2, 4.5), material=mat("wall_l2", "#a9d6cc", rough=0.7), bevel=0)
    random.seed(2)
    # shelves of small reef tanks (glowing blue water, little corals)
    frame = mat("tank_frame2", "#1f2a3a", rough=0.4)
    sw = mat("small_reef", "#7fd0f0", rough=0.05, emit="#4fb8e8", emit_strength=0.8)
    for z in (1.9, 2.9):
        box((3.2, 0.4, 0.05), (-2.0, 4.2, z), material=wood("#c58b4e", "#9a6634", "shelf", 4.0), bevel=0.01)
        for k in range(4):
            xx = -3.2 + k * 0.8
            box((0.5, 0.28, 0.32), (xx, 4.2, z + 0.19), material=sw, bevel=0.01)
            box((0.52, 0.3, 0.02), (xx, 4.2, z + 0.36), material=frame, bevel=0.005)
            sphere(0.06, (xx - 0.1, 4.05, z + 0.08), (1, 1, 1.4), mat("sc%d" % (k % 3), ("#e86aa6", "#f08a24", "#f2d04a")[k % 3], rough=0.6), seg=16)
    text3d("REEF LAB", 0.55, (-2.0, 4.35, 4.0), (90, 0, 0), mat("sign_ink2", "#1f4f78", rough=0.5), font="display", extrude=0.04)
    # a poster of a rainbow spectrum on the wall (the "colour" theme), plain bands, no text
    for k, c in enumerate(("#d9534f", "#f08a24", "#f2d04a", "#4f9e4a", "#3f7fbf", "#6a4fb8")):
        box((0.16, 0.03, 1.1), (1.45 + k * 0.16, 4.42, 2.9), material=mat("band%d" % k, c, rough=0.5), bevel=0.003)
    box((1.12, 0.02, 1.3), (1.85, 4.44, 2.9), material=mat("poster_bg", "#f6efe2", rough=0.6), bevel=0.01)
    # a porthole window
    cylinder(0.55, 0.06, (3.9, 4.43, 2.8), (90, 0, 0), mat("port_glass", "#2f8fc0", rough=0.1, emit="#6fd0f0", emit_strength=1.4), verts=48)
    torus(0.55, 0.07, (3.9, 4.38, 2.8), (90, 0, 0), metal("#c9a24a", 0.25, "brass"))
    # the bench with the big reef tank (foreground layer)
    top_m = mat("bench_top", "#f2ebdf", rough=0.25, coat=0.5)
    body_m = wood("#2f6f8f", "#245670", "bench_body2", 3.0)
    bench = [box((2.6, 0.8, 0.86), (-1.0, 0.5, 0.43), material=body_m, bevel=0.04),
             box((2.8, 0.95, 0.07), (-1.0, 0.48, 0.895), material=top_m, bevel=0.025)]
    for k in range(3):
        bench.append(box((0.7, 0.03, 0.6), (-1.85 + k * 0.85, 0.09, 0.45), material=wood("#3a83a6", "#2b6a88", "drawer2", 3.0), bevel=0.02))
        bench.append(cylinder(0.03, 0.03, (-1.85 + k * 0.85, 0.06, 0.62), (90, 0, 0), metal("#c9a24a", 0.25, "brass"), verts=16))
    bench += reef_tank(-1.0, 0.55, 0.93)
    bench.append(box((0.3, 0.22, 0.02), (0.55, 0.3, 0.94), (0, 0, 12), mat("notebook", "#f2b04a", rough=0.6), bevel=0.005))
    plant = mat("plant", "#4f9e4a", rough=0.6)
    for px in (-5.6, 5.4):
        lathe([(0, 0), (0.3, 0), (0.38, 0.55), (0.0, 0.55)], 32, (px, 3.0, 0), mat("pot", "#c4623a", rough=0.6), 1, "pot")
        for k in range(6):
            sphere(0.35, (px + random.uniform(-0.25, 0.25), 3.0 + random.uniform(-0.2, 0.2), 0.9 + k * 0.12), 1, plant, seg=20)
    lampm = mat("lamp", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    for x in (-2.2, 0.2):
        sphere(0.12, (x, 0.9, 2.5), 1, lampm, seg=24)
        cylinder(0.01, 1.6, (x, 0.9, 3.3), material=mat("cord", "#25262b"), verts=8, bevel=0)
    area_light((-3, -4, 6), (0, 1, 1.5), 1700, 4, "#fff0dc", "key"); area_light((4, -2, 4), (0, 1, 1.5), 520, 4, "#dbe8ff", "fill")
    area_light((-1.0, 0.0, 2.2), (-1.0, 0.55, 1.1), 160, 1.5, "#cfeeff", "tank_spot")
    return bench


def lab_angles():
    bench = build_lab()
    for name, loc, tgt, lens, fs in (("lab_wide", (0.2, -9.0, 2.4), (0.2, 1.5, 1.5), 26, 6.0),
                                     ("lab_mid", (-0.6, -4.0, 1.55), (-0.9, 0.6, 1.15), 34, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=bench)


# ---------------------------------------------------------------- inside the reef tank (underwater close-up)
def reef_inside():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    world_color(hexrgb("#1f6f8a"), 1.0)
    plane(20, 20, (0, 0, 0), material=mat("sand", "#e3d0aa", rough=0.9, noise_bump=0.15), name="sand")
    box((8, 0.05, 5), (0, 2.2, 2.5), material=mat("backwall", "#2f8fb0", rough=0.3, emit="#4fb8d8", emit_strength=0.45), bevel=0)
    gravel(0, 0.6, 3.6, 2.6, 0.01, 520, 3, 0.03)
    coral(-1.2, 1.2, 0.0, 1.6, 11, "#e86aa6"); coral(1.25, 1.3, 0.0, 1.4, 12, "#f08a24")
    coral(-0.5, 1.8, 0.0, 1.2, 13, "#c4523f")
    brain_coral(0.6, 1.5, 0.1, 0.4); brain_coral(-1.6, 0.4, 0.05, 0.3, "#9fd36a")
    for k, (wx, wy, col) in enumerate(((-0.9, 1.4, "#4f9e4a"), (1.6, 0.9, "#5aa84f"), (0.2, 1.9, "#3f8f45"))):
        weed(wx, wy, 0.0, 1.4, k, col)
    rock = mat("rock", "#8a8f96", rough=0.8, noise_bump=0.4)
    # the rubble burrow (bottom centre-left)
    for k, (rx, ry, rr) in enumerate(((-0.55, 0.2, 0.3), (-0.15, 0.3, 0.22), (-0.85, 0.35, 0.22), (0.2, 0.15, 0.18))):
        sphere(rr, (rx, ry, 0.08), (1.3, 1.0, 0.7), rock)
    cylinder(0.16, 0.04, (-0.4, 0.05, 0.03), (90, 0, 0), mat("burrow", "#1a1a20", rough=1.0), verts=32, bevel=0)
    # two fibre-light tips hanging from above (upper third of the frame)
    for fx in (-0.5, 0.5):
        fibre(fx, 0.5, 4.2, 2.15)
    for k in range(5):
        cylinder(0.08, 4.0, (-1.4 + k * 0.7, 1.6, 2.4), (0, 18 - k * 4, 0), mat(f"ray{k}", "#ffffff", alpha=0.035, emit="#e8fbff", emit_strength=0.25), verts=16, bevel=0)
    area_light((-1, -2, 4), (0, 0.5, 0.5), 900, 3, "#e8fbff", "key"); area_light((2, -1, 2), (0, 0.5, 1), 220, 2, "#ffd9a8", "warm")
    drop_cams(); camera((0, -3.6, 1.3), (0, 0.8, 1.45), lens=26, fstop=4.0)
    still("plate_reef", 1080, 1920, 40)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    lab_angles()
    reef_inside()
prop_scene(); mantis((0, 0, 0), 2.0, 0, "hero_ms"); camera((0.6, -2.4, 1.3), (0.05, 0, 0.18), lens=50, fstop=0)
still("mantis", 900, 600, 32, transparent=True, crop=True)
prop_scene(); sphere(0.05, (0, 0, 0.05), (1, 1, 0.8), mat("pellet", "#b8742e", rough=0.6, noise_bump=0.3)); camera((0, -0.6, 0.2), (0, 0, 0.05), lens=60, fstop=0)
still("pellet", 200, 200, 16, transparent=True, crop=True)
