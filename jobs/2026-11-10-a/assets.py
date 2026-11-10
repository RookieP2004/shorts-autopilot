# 2026-11-10-a: "You are 30 trillion cells" (scale-shock). Sets: a bright body-interior world (a floor and a curved back
# wall of packed, glossy cells with nuclei, red blood cells and gut bacteria drifting in the warm air), 3 angles; a sunny
# counting square (cobbles, a clock tower, houses, a bench). Cut-outs: red blood cell, bacterium, body cell, tally
# clicker, hourglass.
import math, os, random

# tree(), bush(), house(), bench(), seg(), checker_mat() + sunny(), bunting() from earlier town jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def cell_mats():
    g = bpy.data.materials.get
    return (g("cellA") or mat("cellA", "#f3a6a0", rough=0.18, coat=0.7, sss=0.35),
            g("cellB") or mat("cellB", "#f7c1a8", rough=0.18, coat=0.7, sss=0.35),
            g("cellC") or mat("cellC", "#eb8f95", rough=0.18, coat=0.7, sss=0.35),
            g("nucleus") or mat("nucleus", "#9a3a6a", rough=0.3, coat=0.5, sss=0.2))


def rbc_mat():
    return bpy.data.materials.get("rbc") or mat("rbc", "#c8141f", rough=0.15, coat=0.8, sss=0.25, emit="#ff2a2a", emit_strength=0.06)


def bac_mat(c="#7cc35a"):
    return bpy.data.materials.get("bac" + c) or mat("bac" + c, c, rough=0.2, coat=0.6, sss=0.2)


def rbc(loc, r=0.3, rot=(0, 0, 0), name="rbc"):
    """A red blood cell: a disc with a dimple on both sides (lathe profile, radius r)."""
    p = [(0.0, 0.11 * r), (0.35 * r, 0.16 * r), (0.7 * r, 0.3 * r), (0.92 * r, 0.3 * r), (1.0 * r, 0.12 * r), (1.0 * r, 0.0)]
    p = p + [(x, -z) for x, z in reversed(p[:-1])]
    o = lathe(p, 48, loc, rbc_mat(), 2, name)
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    return o


def bacterium(loc, L=0.6, r=0.14, rot=(0, 0, 0), col="#7cc35a", name="bac"):
    m = bac_mat(col)
    parts = [cylinder(r, L, (0, 0, 0), (0, 90, 0), m, verts=32, bevel=0),
             sphere(r, (-L / 2, 0, 0), 1, m, seg=32), sphere(r, (L / 2, 0, 0), 1, m, seg=32)]
    hair = bac_mat("#4f8f3a")
    for k in range(6):
        a = k / 6 * 2 * math.pi
        parts.append(seg((L / 2 + r * 0.6, math.cos(a) * r * 0.5, math.sin(a) * r * 0.5),
                         (L / 2 + r * 2.4, math.cos(a) * r * 1.6, math.sin(a) * r * 1.6), r * 0.08, hair))
    g = group(parts, name, loc)
    g.rotation_euler = tuple(math.radians(a) for a in rot)
    return g


def body_cell(loc, r=0.5, m=None, nuc=True):
    A, B, C, N = cell_mats()
    o = sphere(r, loc, (1.0, 1.0, 0.82), m or A, seg=40)
    if nuc:
        sphere(r * 0.3, (loc[0] - r * 0.12, loc[1] - r * 0.86, loc[2] + r * 0.12), (1.0, 0.45, 0.9), N, seg=24)
    return o


def build_tissue():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#e7a2a6"), 0.9)
    A, B, C, N = cell_mats()
    plane(200, 200, (0, 0, -0.02), material=mat("tissue_base", "#d97c84", rough=0.5), name="tissue_base")
    random.seed(4)
    # floor: a hex grid of flat glossy cells (tops ~0.12 m) so feet stay visible
    R = 0.62
    for j in range(-6, 22):
        for i in range(-12, 13):
            x = i * R * 1.75 + (R * 0.87 if j % 2 else 0)
            y = j * R * 1.5
            if abs(x) > 7 + max(0, y) * 0.6:
                continue
            m = random.choice((A, B, C))
            sphere(R * random.uniform(0.9, 1.0), (x, y, -0.02), (1.0, 1.0, 0.22), m, seg=24)
            if random.random() < 0.6:
                sphere(R * 0.32, (x + random.uniform(-0.1, 0.1), y + random.uniform(-0.1, 0.1), 0.06), (1, 1, 0.35), N, seg=16)
    # curved back wall of big cells, rising in rows
    for row in range(10):
        rr = 1.25 + row * 0.12
        for k in range(-9, 10):
            a = k * 0.13 + (0.065 if row % 2 else 0)
            dist = 16 + row * 0.6
            x, y = math.sin(a) * dist, math.cos(a) * dist
            body_cell((x, y, 0.8 + row * 1.9), rr * random.uniform(0.92, 1.05), random.choice((A, B, C)), nuc=True)
    # side mounds of cells
    for side in (-1, 1):
        for k in range(10):
            body_cell((side * random.uniform(6.5, 9.5), random.uniform(1, 13), random.uniform(0.2, 1.6)), random.uniform(0.7, 1.2),
                      random.choice((A, B, C)))
    # drifting red blood cells and a few bacteria in the air
    for k in range(26):
        rbc((random.uniform(-6, 6), random.uniform(2, 14), random.uniform(1.6, 7.5)), random.uniform(0.22, 0.38),
            (random.uniform(-70, 70), random.uniform(-70, 70), random.uniform(0, 180)), f"air_rbc{k}")
    for k in range(7):
        bacterium((random.uniform(-5.5, 5.5), random.uniform(4, 13), random.uniform(2.5, 7)), random.uniform(0.45, 0.65), 0.13,
                  (random.uniform(-40, 40), random.uniform(-30, 30), random.uniform(0, 180)), random.choice(("#7cc35a", "#6fc3c0")), f"air_bac{k}")
    area_light((-6, -6, 9), (0, 4, 1), 2600, 6, "#fff0dc", "key")
    area_light((7, 8, 6), (0, 3, 2), 1400, 6, "#9fd8ff", "rim")
    area_light((0, -10, 3), (0, 2, 1.5), 600, 8, "#ffd7c2", "fill")


def tissue_plates():
    build_tissue()
    for name, loc, tgt, lens, fs in (("tissue_wide", (0.4, -10.0, 2.6), (0, 3, 2.2), 26, 0),
                                     ("tissue_mid", (-0.6, -5.2, 1.7), (0.2, 2.0, 1.4), 32, 0),
                                     ("tissue_up", (1.0, -3.0, 0.5), (-0.5, 8, 5.0), 26, 0)):
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)


def clock_tower(x, y):
    stone = mat("tower", "#efe3cf", rough=0.6)
    box((2.4, 2.4, 8.0), (x, y, 4.0), material=stone, bevel=0.06)
    box((2.7, 2.7, 0.3), (x, y, 8.1), material=mat("tower_trim", "#c9b28a", rough=0.6), bevel=0.04)
    r = cone(2.0, 2.6, (x, y, 9.55), (0, 0, 45), mat("tower_roof", "#34425c", rough=0.5))
    face = cylinder(0.9, 0.08, (x, y - 1.23, 6.4), (90, 0, 0), mat("clockface", "#f6efe2", rough=0.3), verts=48)
    torus(0.92, 0.07, (x, y - 1.26, 6.4), (90, 0, 0), metal("#d9a441", 0.3, "clockrim"))
    ink = mat("clockink", "#1a1410", rough=0.4)
    box((0.07, 0.03, 0.62), (x, y - 1.3, 6.65), (0, 0, 0), ink, bevel=0.01)
    box((0.07, 0.03, 0.45), (x + 0.17, y - 1.3, 6.3), (0, 52, 0), ink, bevel=0.01)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        box((0.05, 0.03, 0.14), (x + math.sin(a) * 0.75, y - 1.29, 6.4 + math.cos(a) * 0.75), (0, -math.degrees(a), 0), ink, bevel=0)
    box((1.0, 0.1, 1.8), (x, y - 1.2, 0.9), material=wood("#8a5a30", "#5e3a1c", "door", 3.0), bevel=0.03)


def square_plate():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sun=4.0)
    plane(300, 300, (0, 0, 0), material=checker_mat("cobbles", "#e6d3b0", "#d2bb92", 0.9), name="cobbles")
    clock_tower(0.0, 9.0)
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#f6efe2", "#c9b7e3", "#9fd39a", "#e3c99a"]
    for k in range(8):
        if abs(-10.5 + k * 3.0) < 2.4:
            continue
        house(-10.5 + k * 3.0, 11 + (k % 2) * 0.8, 2.7, 4 + (k * 53 % 4), cols[k % 7], ["#b5533c", "#34425c", "#7c2533"][k % 3])
    bunting(-5.5, 5.5, 6.5, 4.6)
    tree(-5.0, 4.5, 4.0, 1.4, 7); tree(5.2, 5.5, 4.2, 1.5, 8, "#5aa64a")
    bench(1.6, 0.6)
    bush(-2.8, 0.8, 0.5, seed=4); bush(3.6, 1.4, 0.5, "#46965a", "#d9534f", 5)
    for x in (-3.6, 3.6):
        cylinder(0.05, 3.4, (x, 2.0, 1.7), material=metal("#3b3f46", 0.4, "lamp"), verts=12)
        sphere(0.18, (x, 2.0, 3.45), 1, mat("globe", "#f6efe2", rough=0.2, emit="#ffe2a8", emit_strength=1.0))
    drop_cams()
    camera((0.3, -9.0, 2.2), (0, 2.0, 2.6), lens=26, fstop=0)
    still("plate_square_wide", 1080, 1920, 40)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#f1e4dc"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def clicker():
    body = metal("#c9ced6", 0.25, "clicker_body")
    parts = [cylinder(0.32, 0.2, (0, 0, 0.32), (90, 0, 0), body, verts=48, bevel=0.03),
             box((0.36, 0.05, 0.13), (0, -0.11, 0.36), material=mat("clk_win", "#1a1410", rough=0.3), bevel=0.01),
             cylinder(0.07, 0.16, (0.16, 0, 0.67), (0, 0, 0), metal("#9aa0a8", 0.3, "plunger"), verts=24),
             torus(0.18, 0.03, (-0.08, 0, -0.1), (90, 0, 0), metal("#9aa0a8", 0.3, "ring"))]
    for k in range(4):
        box((0.065, 0.02, 0.09), (-0.12 + k * 0.08, -0.14, 0.36), material=mat("digit", "#f6efe2", rough=0.4), bevel=0.005)
    return parts


def hourglass():
    wd = wood("#a8743f", "#7a4e2a", "hg_wood", 4.0)
    parts = [cylinder(0.42, 0.08, (0, 0, 0.04), material=wd, verts=48), cylinder(0.42, 0.08, (0, 0, 1.36), material=wd, verts=48)]
    for k in range(3):
        a = k / 3 * 2 * math.pi
        parts.append(cylinder(0.035, 1.3, (math.cos(a) * 0.36, math.sin(a) * 0.36, 0.7), material=wd, verts=16))
    g = mat("hg_glass", "#dff1ff", rough=0.1, coat=0.6, alpha=0.4)
    parts.append(lathe([(0.0, 0.08), (0.3, 0.12), (0.32, 0.3), (0.06, 0.68), (0.06, 0.72), (0.32, 1.1), (0.3, 1.28), (0.0, 1.32)],
                       48, (0, 0, 0), g, 1, "hg_bulb"))
    sand = mat("hg_sand", "#f2b04a", rough=0.8)
    parts.append(lathe([(0.0, 0.08), (0.28, 0.12), (0.2, 0.3), (0.0, 0.42)], 32, (0, 0, 0), sand, 1, "hg_sand_lo"))
    parts.append(lathe([(0.0, 0.72), (0.06, 0.74), (0.22, 0.95), (0.0, 0.95)], 32, (0, 0, 0), sand, 1, "hg_sand_hi"))
    return parts


tissue_plates()
square_plate()
prop_scene(); rbc((0, 0, 0.5), 0.5, (30, 0, 15)); sprite_camera((0, 0, 0.5), 3.4, 2.4, 50, azimuth=0)
still("rbc", 700, 700, 32, transparent=True, crop=True)
prop_scene(); bacterium((0, 0, 0.4), 0.9, 0.22, (0, -12, 15)); sprite_camera((0.15, 0, 0.4), 4.2, 0.8, 50, azimuth=0)
still("bacterium", 800, 600, 32, transparent=True, crop=True)
prop_scene(); body_cell((0, 0, 0.5), 0.5); sprite_camera((0, 0, 0.5), 3.2, 1.0, 50, azimuth=0)
still("cell", 700, 700, 32, transparent=True, crop=True)
prop_scene(); clicker(); sprite_camera((0, 0, 0.35), 3.0, 0.7, 50, azimuth=-15)
still("clicker", 600, 700, 32, transparent=True, crop=True)
prop_scene(); hourglass(); sprite_camera((0, 0, 0.7), 5.2, 1.2, 50, azimuth=-15)
still("hourglass", 600, 800, 32, transparent=True, crop=True)
