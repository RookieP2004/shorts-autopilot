# 2026-11-14-c: "How long to become a trillionaire at $1 a second?" (scale-shock). Set: a sunny town square with a tall
# clock tower (big white clock face, brass hands), a giant glass coin jar on a stone pedestal fed by a brass coin chute,
# cobbles, bunting, little houses and round trees; 3 angles (wide, mid by the jar, looking up at the clock).
# Cut-outs: a gold coin, the coin jar (few coins / full), a coin pile.
import math, os, random

# sunny(), coin(), coin_pile(), coin_stack(), house(), tree(), bunting(), drop_cams() ... (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-09-b/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "b09_helpers", "exec"), globals())


def clock_tower(x, y, s=1.0):
    stone = mat("tower_stone", "#e9d8b8", rough=0.8, noise_bump=0.15)
    trim = mat("tower_trim", "#c4623a", rough=0.6)
    box((2.4 * s, 2.4 * s, 9.0 * s), (x, y, 4.5 * s), material=stone, bevel=0.06)
    box((2.7 * s, 2.7 * s, 0.35 * s), (x, y, 9.1 * s), material=trim, bevel=0.06)
    cone(2.1 * s, 2.6 * s, (x, y, 10.6 * s), (0, 0, 45), mat("tower_roof", "#34425c", rough=0.6))
    for z in (2.2, 5.0):
        box((0.7 * s, 0.08 * s, 1.0 * s), (x, y - 1.2 * s, z * s), material=mat("tower_win", "#8fd0e8", rough=0.1, coat=0.6), bevel=0.02)
    box((1.2 * s, 0.1 * s, 1.9 * s), (x, y - 1.2 * s, 0.95 * s), material=wood("#8a4f2c", "#5e321a", "tower_door", 3.0), bevel=0.03)
    # the clock face
    cz = 7.5 * s; fy = y - 1.25 * s
    cylinder(1.0 * s, 0.12 * s, (x, fy, cz), (90, 0, 0), metal("#c9a24a", 0.25, "clock_rim"), verts=64)
    cylinder(0.9 * s, 0.14 * s, (x, fy - 0.02 * s, cz), (90, 0, 0), mat("clock_face", "#fbf6ea", rough=0.4), verts=64)
    ink = mat("clock_ink", "#1a1410", rough=0.5)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        L = 0.16 if k % 3 == 0 else 0.09
        box((0.05 * s, 0.04 * s, L * s), (x + 0.72 * s * math.sin(a), fy - 0.1 * s, cz + 0.72 * s * math.cos(a)), (0, math.degrees(a), 0), ink, bevel=0)
    box((0.07 * s, 0.04 * s, 0.5 * s), (x + 0.2 * s, fy - 0.12 * s, cz + 0.12 * s), (0, 60, 0), ink, bevel=0.01)   # hour hand
    box((0.05 * s, 0.04 * s, 0.75 * s), (x - 0.0 * s, fy - 0.14 * s, cz + 0.36 * s), (0, -2, 0), mat("clock_red", "#d9534f", rough=0.5), bevel=0.01)
    sphere(0.06 * s, (x, fy - 0.16 * s, cz), 1, metal("#c9a24a", 0.25, "clock_rim"))


def coin_jar(x, y, s=1.0, fill=0.35, seed=4, z0=0.0):
    g = glass("#e8f6ff", 0.03, "jar_glass")
    lathe([(0, 0), (0.55, 0), (0.62, 0.08), (0.62, 1.15), (0.5, 1.32), (0.38, 1.38), (0.38, 1.5), (0.0, 1.5)],
          48, (x, y, z0), g, 1, "jar").scale = (s, s, s)
    # coins inside: a mound to the fill level
    random.seed(seed)
    n = int(260 * fill)
    for k in range(n):
        a = random.uniform(0, 2 * math.pi); d = 0.5 * s * math.sqrt(random.random())
        z = z0 + random.uniform(0.04, 1.1 * fill) * s
        coin((x + d * math.cos(a), y + d * math.sin(a), z), (random.uniform(-60, 60), random.uniform(-60, 60), random.uniform(0, 360)), 0.07 * s, f"jc{seed}_{k}")
    box((0.5 * s, 0.5 * s, 0.06 * s), (x, y, z0 + 1.5 * s), material=metal("#c9a24a", 0.25, "jar_lid"), bevel=0.02)


def build_square():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny("#2f8fe0", "#cfe8fb", 4.6)
    plane(400, 400, (0, 0, 0), material=mat("cobbles", "#d8c19a", rough=0.9, noise_bump=0.3), name="cobbles")
    cylinder(2.4, 0.04, (0.6, 0.2, 0.02), material=mat("plaza_ring", "#c9b08a", rough=0.85), verts=64, bevel=0)
    # the pedestal + the jar + the chute from a little brass box
    stone = mat("ped_stone", "#efe3cf", rough=0.7)
    box((1.6, 1.6, 0.8), (0.6, 0.6, 0.4), material=stone, bevel=0.06)
    box((1.8, 1.8, 0.12), (0.6, 0.6, 0.84), material=mat("ped_trim", "#3d7f7c", rough=0.5, coat=0.3), bevel=0.03)
    coin_jar(0.6, 0.6, 1.0, 0.35, 4, z0=0.9)
    brass = metal("#c9a24a", 0.25, "chute_brass")
    box((0.6, 0.6, 0.7), (1.9, 0.9, 3.4), material=brass, bevel=0.05)
    cylinder(0.08, 1.4, (1.3, 0.75, 3.0), (0, -55, 0), brass, verts=20)
    cylinder(0.05, 3.0, (2.1, 1.1, 1.6), material=metal("#5a6068", 0.4, "pole"), verts=16)
    text3d("$1 / SEC", 0.2, (1.9, 0.58, 3.35), (90, 0, 0), mat("sign_ink", "#7c2533", rough=0.5), font="display", extrude=0.01)
    clock_tower(-2.2, 5.5, 1.0)
    house(3.6, 6.2, 4.0, 4.6, "#f2c88a", "#b5533c", 1)
    house(-7.6, 7.2, 4.4, 5.6, "#e8a39a", "#7c2533", 2)
    house(8.4, 8.0, 4.0, 4.2, "#a8d5d1", "#34425c", 3)
    house(-12, 10, 4.2, 5.0, "#d9c6ea", "#6b4c8a", 4)
    house(12.5, 11, 4.5, 5.0, "#f6e3a8", "#b5533c", 5)
    tree(-5.0, 3.2, 3.4, 1); tree(5.4, 3.6, 3.0, 2); tree(-9.6, 4.6, 3.6, 3); tree(9.8, 5.0, 3.4, 4)
    bunting(-4.6, 2.0, 2.8, 4.2)
    area_light((-5, -6, 7), (0, 1, 1.5), 900, 6, "#fff0dc", "key")
    area_light((5, -4, 3), (0, 1, 1.5), 300, 5, "#dbe8ff", "fill")


def square_angles():
    build_square()
    for name, loc, tgt, lens, fs in (("square_wide", (0.0, -10.5, 2.4), (-0.4, 2.0, 3.6), 24, 6.0),
                                     ("square_mid", (-1.2, -4.6, 1.7), (-0.2, 0.8, 1.6), 30, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
    drop_cams(); camera((-1.2, -2.2, 1.4), (-2.2, 4.25, 7.4), lens=26, fstop=0)
    still("plate_clock_up", 1080, 1920, 40)


if not os.environ.get("BK_PROPS_ONLY"):
    square_angles()
prop_scene(); coin((0, 0, 0.2), (80, 0, -15), 0.2, "hero_coin"); camera((0, -1.8, 0.3), (0, 0, 0.2), lens=60, fstop=0)
still("coin", 400, 400, 24, transparent=True, crop=True)
prop_scene(); coin_pile(0, 0, 130, 0.38, 9, 0.07); sprite_camera((0, 0, 0.12), 2.2, 1.1, 55); still("coin_pile", 700, 500, 28, transparent=True, crop=True)
prop_scene(); coin_jar(0, 0, 1.0, 0.12, 7); sprite_camera((0, 0, 0.75), 4.2, 1.2, 45); still("jar_low", 500, 700, 32, transparent=True, crop=True)
prop_scene(); coin_jar(0, 0, 1.0, 0.95, 8); sprite_camera((0, 0, 0.75), 4.2, 1.2, 45); still("jar_full", 500, 700, 32, transparent=True, crop=True)
