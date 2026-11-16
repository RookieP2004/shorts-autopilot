# 2026-11-17-c: "Your body makes 2 million red blood cells a second" (scale-shock, number-shock).
# Sets: "MARROW WORKS", a bright factory inside a bone (cream porous bone vault, spongy-bone struts, a teal conveyor belt
# carrying glossy red blood cells as the foreground layer, a lilac stem-cell dome feeding the belt, a nucleus press with a
# bin of ejected purple nuclei, crates of finished cells, a big red pipe "TO BLOOD"), 2 angles (wide, mid on the belt);
# inside a blood vessel (a glossy red tunnel full of cells), 1 angle. Cut-outs: red blood cell, nucleus, stem cell.
import math, os, random

# rbc(), rbc_mat(), cell_mats() ... (frozen helpers from 2026-11-10-a)
_src = open(os.path.join(ROOT, "jobs/2026-11-10-a/assets.py")).read()
_src = _src[_src.index("def drop_cams("):_src.index("def bacterium(")]
exec(compile(_src, "a10_helpers", "exec"), globals())
_c = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read()
exec(compile(_c[_c.index("def seg("):_c.index("def tree(")], "seg", "exec"), globals())


def bone_mat():
    return bpy.data.materials.get("bone") or mat("bone", "#f3e6cf", rough=0.55, sss=0.1, noise_bump=0.5)


def pore_mat():
    return bpy.data.materials.get("pore") or mat("pore", "#d98a7a", rough=0.5, sss=0.2)


def nuc_mat():
    return bpy.data.materials.get("nuc2") or mat("nuc2", "#7a3fa0", rough=0.25, coat=0.7, sss=0.2, noise_bump=0.3)


def strut(x, y, h=4.0, r=0.35):
    """A spongy-bone strut (trabecula): an organic hourglass column."""
    prof = [(r * 1.6, 0), (r * 1.1, h * 0.12), (r * 0.8, h * 0.35), (r * 0.7, h * 0.5), (r * 0.8, h * 0.65),
            (r * 1.1, h * 0.88), (r * 1.6, h)]
    return lathe(prof, 32, (x, y, 0), bone_mat(), 1, "strut")


def belt(x0, x1, y, z=0.9):
    """Teal conveyor with rollers and red blood cells riding on it. Returns its parts (for the foreground layer)."""
    frame = metal("#2f8f9a", 0.35, "belt_frame")
    rub = mat("rubber", "#2a2d33", rough=0.8)
    L = x1 - x0
    cx = (x0 + x1) / 2
    out = [box((L, 0.9, 0.12), (cx, y, z), material=frame, bevel=0.03),
           box((L - 0.1, 0.8, 0.03), (cx, y, z + 0.075), material=rub, bevel=0.01)]
    for k in range(int(L / 0.8) + 1):
        xx = x0 + 0.2 + k * 0.8
        if xx > x1 - 0.1:
            break
        out.append(box((0.1, 0.1, z - 0.06), (xx, y - 0.38, (z - 0.06) / 2), material=frame, bevel=0.02))
        out.append(box((0.1, 0.1, z - 0.06), (xx, y + 0.38, (z - 0.06) / 2), material=frame, bevel=0.02))
    out.append(box((L, 0.06, 0.06), (cx, y - 0.46, z + 0.1), material=metal("#f2b04a", 0.3, "belt_rail"), bevel=0.01))
    random.seed(5)
    k = 0
    xx = x0 + 0.5
    while xx < x1 - 0.3:
        out.append(rbc((xx, y + random.uniform(-0.15, 0.15), z + 0.16), 0.22, (random.uniform(20, 35), 0, random.uniform(0, 180)), f"belt_rbc{k}"))
        xx += 0.55
        k += 1
    return out


def stem_machine(x, y):
    lil = mat("stem_dome", "#c9a3e6", rough=0.15, coat=0.9, sss=0.3)
    out = [lathe([(0.0, 0), (0.75, 0), (0.75, 0.9), (0.6, 1.0), (0.0, 1.0)], 40, (x, y, 0), metal("#3f7fbf", 0.3, "stem_base"), 1, "stem_base"),
           sphere(0.9, (x, y, 1.75), 1, lil, seg=48),
           sphere(0.32, (x - 0.25, y - 0.6, 1.95), (1, 0.6, 1), nuc_mat(), seg=32),
           cylinder(0.18, 1.1, (x + 0.85, y, 1.1), (0, 70, 0), metal("#c9a24a", 0.25, "brass"), verts=24)]
    for k in range(3):
        out.append(sphere(0.07, (x - 0.5 + k * 0.5, y - 0.72, 0.6), 1, mat(f"lamp{k}", ("#4f9e4a", "#f2b04a", "#d9534f")[k],
                                                                              emit=("#6fdc6a", "#ffd060", "#ff5a5a")[k], emit_strength=2.5), seg=16))
    return out


def press(x, y, z=0.9):
    """An arch over the belt that knocks the nucleus out of each new cell, plus a bin of ejected nuclei."""
    fr = metal("#f08a24", 0.35, "press")
    out = [box((0.2, 0.2, 1.5), (x - 0.5, y, z + 0.75), material=fr, bevel=0.04),
           box((0.2, 0.2, 1.5), (x + 0.5, y, z + 0.75), material=fr, bevel=0.04),
           box((1.3, 0.35, 0.3), (x, y, z + 1.55), material=fr, bevel=0.06),
           cylinder(0.14, 0.5, (x, y, z + 1.15), material=metal("#9aa3ab", 0.25, "steel"), verts=24)]
    binm = mat("bin", "#3f7fbf", rough=0.4, coat=0.3)
    bx, by = x + 0.2, y - 1.0
    out.append(lathe([(0.0, 0), (0.45, 0), (0.52, 0.55), (0.48, 0.58), (0.0, 0.05)], 36, (bx, by, 0), binm, 1, "bin"))
    random.seed(9)
    for k in range(9):
        a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, 0.28)
        out.append(sphere(0.11, (bx + math.cos(a) * rr, by + math.sin(a) * rr, 0.55 + random.uniform(0, 0.12)), 1, nuc_mat(), seg=20))
    return out


def crate(x, y, s=1.0):
    w = wood("#c58b4e", "#9a6634", "crate_wood", 3.0)
    out = [box((0.9 * s, 0.7 * s, 0.6 * s), (x, y, 0.3 * s), material=w, bevel=0.03)]
    random.seed(int(x * 10) + 3)
    for k in range(5):
        out.append(rbc((x + random.uniform(-0.3, 0.3) * s, y + random.uniform(-0.2, 0.2) * s, 0.62 * s + k * 0.03), 0.2 * s,
                       (random.uniform(30, 70), random.uniform(-30, 30), random.uniform(0, 180)), f"crate_rbc{x}{k}"))
    return out


def build_marrow():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.12)
    world_color(hexrgb("#f6e3d6"), 1.0)
    plane(60, 60, (0, 0, 0), material=mat("marrow_floor", "#f0b9a6", rough=0.45, coat=0.3), name="floor")
    # walkway stripes
    for k in range(-6, 7):
        box((0.9, 30, 0.01), (k * 2.0, 6, 0.005), material=mat("tile", "#f6cdb9", rough=0.5), bevel=0)
    # bone vault behind: a big curved wall with pores
    for k in range(-14, 15):
        a = k * 0.085
        R = 13.0
        x, y = math.sin(a) * R, math.cos(a) * R - 4.5
        box((1.2, 0.8, 12), (x, y, 6), (0, 0, -math.degrees(a)), bone_mat(), bevel=0.2)
    random.seed(3)
    for k in range(70):
        a = random.uniform(-1.1, 1.1); z = random.uniform(1.2, 10)
        R = 12.55
        sphere(random.uniform(0.25, 0.6), (math.sin(a) * R, math.cos(a) * R - 4.5, z), (1, 0.4, 1), pore_mat(), seg=20)
    # spongy bone struts left and right, with cross braces
    for (sx, sy, h) in ((-5.2, 5.5, 7), (-3.6, 7.2, 8), (4.6, 5.0, 7), (3.2, 7.5, 8), (-6.5, 2.5, 6), (6.0, 2.2, 6)):
        strut(sx, sy, h, 0.42)
    for (a, b) in (((-5.2, 5.5, 4.2), (-3.6, 7.2, 5.5)), ((4.6, 5.0, 3.8), (3.2, 7.5, 5.0))):
        seg(a, b, 0.22, bone_mat())
    text3d("MARROW WORKS", 0.75, (0.0, 7.55, 4.6), (90, 0, 0), mat("sign_ink3", "#c4523f", rough=0.5), font="display", extrude=0.06)
    box((7.2, 0.15, 1.3), (0.0, 7.75, 4.95), material=mat("sign_bg", "#fff4e2", rough=0.5), bevel=0.06)
    # big red pipe on the right: "to the blood"
    pipe = mat("pipe", "#d9534f", rough=0.25, coat=0.6)
    cylinder(0.55, 5.0, (3.7, 3.0, 2.2), (90, 0, 0), pipe, verts=40)
    torus(0.6, 0.12, (3.7, 0.55, 2.2), (90, 0, 0), metal("#c9a24a", 0.25, "brass"))
    text3d("TO BLOOD", 0.32, (3.7, 0.4, 3.05), (90, 0, 0), mat("sign_w", "#fff4e2", rough=0.5), font="display", extrude=0.03)
    # machines + belt (belt, press, stem dome = the foreground layer)
    fg = belt(-2.6, 3.2, 0.9)
    fg += press(0.6, 0.9)
    fg += stem_machine(-3.3, 1.2)
    for (cx, cy) in ((3.9, -0.7), (4.6, 0.2)):
        crate(cx, cy)
    # warm hanging lamps
    lampm = mat("lamp_w", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    for x in (-2.5, 1.5):
        sphere(0.14, (x, 1.5, 3.4), 1, lampm, seg=24)
        cylinder(0.012, 2.6, (x, 1.5, 4.8), material=mat("cord", "#25262b"), verts=8, bevel=0)
    # a few cells drifting high in the air (the bone is busy)
    for k in range(10):
        rbc((random.uniform(-5, 5), random.uniform(3, 8), random.uniform(3.5, 7.5)), random.uniform(0.2, 0.3),
            (random.uniform(-60, 60), random.uniform(-60, 60), random.uniform(0, 180)), f"air_rbc{k}")
    area_light((-4, -5, 7), (0, 2, 1), 2400, 5, "#fff0dc", "key")
    area_light((5, -3, 4), (0, 2, 1.5), 700, 5, "#dbe8ff", "fill")
    area_light((0, 6, 6), (0, 0, 1), 500, 6, "#ffd7c2", "back")
    return fg


def marrow_angles():
    fg = build_marrow()
    for name, loc, tgt, lens, fs in (("marrow_wide", (0.0, -8.2, 2.3), (0.0, 2.5, 2.1), 24, 0),
                                     ("marrow_mid", (0.2, -4.2, 1.7), (0.2, 1.0, 1.25), 30, 0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=fg)


def vessel():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.25)
    world_color(hexrgb("#5a0f18"), 0.5)
    wall = mat("vessel_wall", "#b01e2c", rough=0.3, coat=0.6, sss=0.3, noise_bump=0.35)
    # tunnel along +Y made of rings, slightly wavy
    for k in range(60):
        y = -2 + k * 0.5
        torus(2.6, 0.45, (math.sin(k * 0.25) * 0.3, y, 2.6 + math.cos(k * 0.2) * 0.2), (90, 0, 0), wall)
    random.seed(12)
    for k in range(90):
        y = random.uniform(1, 28)
        a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, 1.7)
        rbc((math.cos(a) * rr, y, 2.6 + math.sin(a) * rr), random.uniform(0.24, 0.34),
            (random.uniform(-80, 80), random.uniform(-80, 80), random.uniform(0, 180)), f"v_rbc{k}")
    for k in range(6):
        sphere(0.35, (random.uniform(-1.2, 1.2), random.uniform(4, 20), 2.6 + random.uniform(-1.2, 1.2)), 1,
               mat("wbc", "#f6efe2", rough=0.3, sss=0.3, noise_bump=0.6), seg=24)
    area_light((0, -1.5, 3.6), (0, 6, 2.6), 650, 2.5, "#ffe6d6", "key")
    area_light((0, 10, 2.6), (0, 0, 2.6), 400, 3, "#ff9a7a", "deep")
    drop_cams(); camera((0, -1.2, 2.6), (0, 10, 2.6), lens=22, fstop=0)
    still("plate_vessel", 1080, 1920, 40)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#f2e6e0"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    marrow_angles()
    vessel()
prop_scene(); rbc((0, 0, 0.3), 0.3, (-75, 0, 10), "hero_rbc"); camera((0, -1.8, 1.2), (0, 0, 0.3), lens=55, fstop=0)
still("rbc", 700, 700, 32, transparent=True, crop=True)
prop_scene(); sphere(0.22, (0, 0, 0.3), 1, nuc_mat(), seg=40); camera((0, -2.0, 0.9), (0, 0, 0.3), lens=60, fstop=0)
still("nucleus", 400, 400, 28, transparent=True, crop=True)
prop_scene(); sphere(0.35, (0, 0, 0.35), 1, mat("stem_cell", "#c9a3e6", rough=0.15, coat=0.9, sss=0.3), seg=48)
sphere(0.15, (-0.08, -0.25, 0.42), (1, 0.6, 1), nuc_mat(), seg=32); camera((0, -2.0, 0.9), (0, 0, 0.35), lens=55, fstop=0)
still("stemcell", 500, 500, 28, transparent=True, crop=True)
