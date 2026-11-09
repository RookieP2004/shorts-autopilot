# 2026-11-09-a: "How heavy is a cloud?" Sets: a sunny hilltop meadow with one huge cumulus cloud overhead (wide, a low
# "looking up" sky angle), and a giant wooden see-saw on the meadow (level, and tipped with the left end down).
# Cut-outs: a puffy cloud, an elephant, a glass marble, an AIR crate.
import math, os, random

# tree(), bush(), house(), seg(), crate(), sunny(), bunting() from the earlier town jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def cloud_mat():
    return mat("cloud", "#ffffff", rough=1.0, sss=0.25, emit="#fff7ec", emit_strength=0.18)


def cumulus(cx, cy, cz, s=1.0, seed=3, m=None):
    """A puffy cumulus: a flat-ish base and stacked round puffs. s = overall radius scale."""
    random.seed(seed)
    m = m or cloud_mat()
    parts = []
    for k in range(9):                                            # base row
        a = k / 9 * 2 * math.pi
        parts.append(sphere(s * random.uniform(0.55, 0.75), (cx + math.cos(a) * s * 1.1, cy + math.sin(a) * s * 0.5,
                            cz + random.uniform(-0.05, 0.1) * s), (1.2, 1.0, 0.75), m, seg=32))
    for k in range(6):                                            # middle
        a = k / 6 * 2 * math.pi + 0.4
        parts.append(sphere(s * random.uniform(0.6, 0.8), (cx + math.cos(a) * s * 0.6, cy + math.sin(a) * s * 0.3,
                            cz + s * random.uniform(0.45, 0.65)), 1, m, seg=32))
    parts.append(sphere(s * 0.85, (cx - s * 0.15, cy, cz + s * 1.05), 1, m, seg=32))   # top towers
    parts.append(sphere(s * 0.6, (cx + s * 0.55, cy - s * 0.1, cz + s * 0.95), 1, m, seg=32))
    parts.append(sphere(s * 0.5, (cx - s * 0.8, cy - s * 0.1, cz + s * 0.75), 1, m, seg=32))
    return parts


def windmill(x, y):
    body = mat("mill", "#f6efe2", rough=0.7)
    lathe([(0.0, 0.0), (1.1, 0.0), (0.95, 3.0), (0.75, 5.2), (0.0, 5.2)], 32, (x, y, 0), body, 1, "mill")
    cone(0.95, 1.4, (x, y, 5.85), material=mat("mill_roof", "#b5533c", rough=0.6))
    hub = (x, y - 0.95, 5.0)
    sphere(0.16, hub, 1, wood("#6e4624", "#4a2e16", "hub", 2.0))
    for k in range(4):
        a = math.radians(20 + k * 90)
        b = box((0.42, 0.05, 2.6), (hub[0] + math.sin(a) * 1.35, hub[1] - 0.05, hub[2] + math.cos(a) * 1.35),
                (0, math.degrees(a), 0), wood("#d8c49c", "#a8875a", "sail", 6.0), bevel=0.02)


def seesaw(state):
    """A giant see-saw at (0, 2, 0). Plank 9 m. 'level' or 'tipped' (left end down)."""
    th = math.radians(13 if state == "tipped" else 0)
    red = mat("seesaw_red", "#d9534f", rough=0.45, coat=0.4)
    piv = lathe([(0.0, 0.0), (0.95, 0.0), (0.9, 0.12), (0.3, 1.12), (0.18, 1.25), (0.0, 1.3)], 40, (0, 2.0, 0), red, 1, "fulcrum")
    cylinder(0.14, 1.5, (0, 2.0, 1.3), (90, 0, 0), metal("#3b3f46", 0.4, "axle"), verts=24)
    plank = box((9.0, 1.0, 0.2), (0, 2.0, 1.42), (0, 0, 0), wood("#c58b4e", "#9a6634", "plank", 3.0), bevel=0.06)
    plank.rotation_euler = (0, th, 0)                       # +y rotation raises the -x end (right end goes down)
    return [plank, piv]


def build_meadow(state="level", sky_cloud=True, with_seesaw=True):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sky_top="#3a93dc", sky_horizon="#c9e8fb", sun=4.2)
    plane(400, 400, (0, 0, 0), material=mat("grass", "#86c45a", rough=0.9, noise_bump=0.35), name="grass")
    for k, (hx, hy, r, c) in enumerate(((-30, 60, 26, "#6fae4c"), (25, 75, 30, "#79b955"), (-5, 95, 34, "#8cc467"))):
        sphere(r, (hx, hy, -r * 0.82), (1.6, 1.0, 1.0), mat(f"hill{k}", c, rough=0.9, noise_bump=0.2), seg=64)
    plane(1.8, 60, (2.8, 18, 0.008), (0, 0, -10), mat("path", "#e3cfa6", rough=0.9, noise_bump=0.2), name="path")
    fg = seesaw(state) if with_seesaw else []
    tree(-5.8, 6.5, 4.0, 1.4, 11); tree(6.4, 8.5, 4.4, 1.5, 12, "#5aa64a"); tree(-9.5, 14, 4.6, 1.6, 13, "#4c9440")
    tree(10.5, 17, 4.6, 1.6, 14)
    windmill(-4.5, 24)
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#f6efe2", "#c9b7e3"]
    for k in range(5):
        house(5 + k * 3.1, 30 + (k % 2) * 1.5, 2.6, 3.5 + (k * 37 % 3), cols[k % 5], ["#b5533c", "#34425c", "#7c2533"][k % 3])
    bush(-3.2, -0.8, 0.5, seed=21); bush(4.6, 0.4, 0.55, "#46965a", "#d9534f", 22); bush(-6.5, 2.5, 0.6, "#3f8a3e", "#f6efe2", 23)
    random.seed(5)
    fl = [plastic(c, 0.4, f"wf{c}") for c in ("#f6efe2", "#f2b04a", "#e8857c", "#c9b7e3")]
    for k in range(70):                                     # wildflowers
        sphere(0.05, (random.uniform(-7, 7), random.uniform(-4, 9), 0.06), 1, fl[k % 4], seg=10)
    if sky_cloud:
        cumulus(-4.0, 70, 32, 9.0, seed=4)
        cumulus(30, 110, 40, 6.0, seed=7)
    return fg


def cams_clear():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def meadow_plates():
    build_meadow("level", with_seesaw=False)
    for name, loc, tgt, lens, fs in (("meadow_wide", (0.5, -11.0, 1.9), (-0.6, 6, 6.0), 24, 0),
                                     ("meadow_sky", (1.5, -4.0, 0.6), (-3.6, 70, 37), 30, 0)):
        cams_clear()
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
    build_meadow("level")
    cams_clear()
    camera((0.0, -10.5, 2.3), (0, 2.0, 2.4), lens=24, fstop=0)
    still("plate_seesaw_level", 1080, 1920, 40)


def tipped_plate():
    build_meadow("tipped")
    cams_clear()
    camera((0.0, -10.5, 2.3), (0, 2.0, 2.4), lens=24, fstop=0)
    still("plate_seesaw_tipped", 1080, 1920, 40)


def elephant():
    skin = mat("eleskin", "#8f949c", rough=0.7, noise_bump=0.3)
    ear = mat("eleear", "#9aa0a8", rough=0.7)
    tusk = mat("tusk", "#f6efe2", rough=0.3, coat=0.4)
    parts = [sphere(1.0, (0, 0, 1.75), (1.35, 0.85, 0.85), skin),                     # body
             sphere(0.62, (1.25, 0, 2.15), (1.0, 0.85, 0.95), skin)]                  # head
    for sx in (-0.75, 0.7):
        for sy in (-0.42, 0.42):
            parts.append(cylinder(0.27, 1.25, (sx, sy, 0.62), material=skin, verts=28, bevel=0.08))
    pts = [(1.75, 0, 2.05), (2.0, 0, 1.6), (2.1, 0, 1.1), (2.05, 0, 0.7), (2.2, 0, 0.45)]
    for k in range(len(pts) - 1):
        seg(pts[k], pts[k + 1], 0.2 - k * 0.035, skin)
    for side in (-1, 1):
        e = sphere(0.62, (0.95, side * 0.55, 2.2), (0.35, 0.12, 1.0), ear)
        e.rotation_euler = (0, 0, math.radians(side * -20))
        seg((1.6, side * 0.25, 1.85), (1.95, side * 0.3, 1.45), 0.06, tusk)
        sphere(0.07, (1.62, side * 0.42, 2.38), 1, mat("eleeye", "#1a1410", rough=0.1, coat=1.0))
    seg((-1.3, 0, 2.0), (-1.55, 0, 1.3), 0.05, skin)
    return parts


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


meadow_plates()
tipped_plate()
prop_scene(); cumulus(0, 0, 0.6, 1.0, seed=4); sprite_camera((0, 0, 1.0), 9.0, 0.6, 50, azimuth=0)
still("cloud", 900, 700, 32, transparent=True, crop=True)
prop_scene(); elephant(); sprite_camera((0.4, 0, 1.6), 11.0, 0.8, 50, azimuth=35)
still("elephant", 800, 700, 28, transparent=True, crop=True)
prop_scene(); sphere(0.3, (0, 0, 0.3), 1, mat("marble", "#6fc3c0", rough=0.02, transmission=0.85, coat=1.0))
sprite_camera((0, 0, 0.3), 2.6, 0.5, 60, azimuth=-20); still("marble", 500, 500, 32, transparent=True, crop=True)
prop_scene(); crate(0, 0, 0, "AIR", "c_air"); sprite_camera((0, 0, 0.45), 4.0, 0.9, 50, azimuth=0)
still("crate_air", 600, 600, 24, transparent=True, crop=True)
