# 2026-11-18-c: "Meteorites land red-hot? This one grew frost" (myth-bust, Colby meteorite, 4 July 1917).
# Sets: a Wisconsin farm meadow on a summer evening (golden-hour sky, red barn, white farmhouse, fence, trees, rolling
# hills, a 4th-of-July picnic table with bunting strung between two poles, a fresh little crater with the dark meteorite
# in the grass in front), 3 angles (wide with lots of sky for the fireball, mid on the crater, low close-up on the rock).
# Cut-outs: the meteorite (black fusion crust), the same rock frosted white, a cut-open slice (thin black crust, grey
# speckled stone inside), a pie.
import math, os, random

# sunny(), tree(), barn(), fence(), tufts(), flowers(), rocks(), hills(), drop_cams() (frozen helpers from 2026-11-10-c)
_src = open(os.path.join(ROOT, "jobs/2026-11-10-c/assets.py")).read().split("\ndef pasture(")[0]
exec(compile(_src, "c10_helpers", "exec"), globals())


def lump(r, loc, material, seed=1, amount=0.25, scale=(1.25, 1.0, 0.85)):
    o = sphere(r, loc, scale, material, seg=64)
    tex = bpy.data.textures.new(f"lump{seed}", "CLOUDS"); tex.noise_scale = 0.55 * r; tex.noise_depth = 2
    d = o.modifiers.new("disp", "DISPLACE"); d.texture = tex; d.strength = amount * r; d.mid_level = 0.5
    random.seed(seed)
    o.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3))
    return o


def crust_mat():
    return bpy.data.materials.get("crust") or mat("crust", "#2b2520", rough=0.78, coat=0.08, noise_bump=1.2)


def frost_mat():
    return bpy.data.materials.get("frost") or mat("frost", "#f2f8ff", rough=0.9, alpha=0.62, noise_bump=1.4)


def meteorite(loc=(0, 0, 0), r=0.3, frost=False):
    o = lump(r, (loc[0], loc[1], loc[2] + r * 0.7), crust_mat(), seed=21, amount=0.45, scale=(1.35, 1.0, 0.75))
    if frost:   # a thin, see-through white frost coat over the same rock
        lump(r * 1.03, (loc[0], loc[1], loc[2] + r * 0.7), frost_mat(), seed=21, amount=0.45, scale=(1.35, 1.0, 0.75))
    return o


def bunting(x0, x1, y, z, colors=("#d6483e", "#f6efe2", "#3f6fb8", "#f2b04a")):
    n = 14
    for k in range(n):
        t = k / (n - 1); xx = x0 + (x1 - x0) * t; zz = z - 0.35 * math.sin(math.pi * t)
        cone(0.12, 0.22, (xx, y, zz - 0.11), (0, 180, 0), mat(f"flag{k%4}", colors[k % 4], rough=0.6))


def farmhouse(x, y):
    white = mat("house_white", "#f6efe2", rough=0.6)
    box((3.4, 2.6, 2.6), (x, y, 1.3), material=white, bevel=0.04)
    for sgn in (-1, 1):
        box((2.0, 2.9, 0.14), (x + sgn * 0.86, y, 3.15), (0, sgn * 35, 0), mat("house_roof", "#34425c", rough=0.7), bevel=0.03)
    win = mat("house_win", "#ffd27a", emit="#ffb64a", emit_strength=1.2)
    for wx in (-0.9, 0.9):
        box((0.6, 0.06, 0.7), (x + wx, y - 1.31, 1.6), material=win, bevel=0.01)
    box((0.7, 0.06, 1.3), (x, y - 1.31, 0.65), material=mat("house_door", "#7c2533", rough=0.6), bevel=0.01)


def crater(x, y, r=0.75):
    dirt = mat("crater_dirt", "#7a5a3c", rough=0.95, noise_bump=0.5)
    rim = mat("crater_rim", "#8f6a46", rough=0.95, noise_bump=0.6)
    out = [cylinder(r, 0.02, (x, y, 0.005), material=dirt, verts=48, bevel=0)]
    random.seed(41)
    for k in range(16):
        a = k / 16 * 2 * math.pi
        out.append(sphere(random.uniform(0.12, 0.2), (x + math.cos(a) * r, y + math.sin(a) * r * 0.9, 0.02), (1.4, 1.0, 0.45), rim, seg=16))
    for k in range(10):   # thrown-up clods
        a = random.uniform(0, 2 * math.pi); d = random.uniform(1.1, 1.6) * r
        out.append(sphere(random.uniform(0.04, 0.08), (x + math.cos(a) * d, y + math.sin(a) * d, 0.03), 1, rim, seg=10))
    out.append(meteorite((x, y, -0.08), 0.3))
    return out


def build_farm():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.1)
    sunny(sky_top="#3f7fd0", sky_horizon="#ffd2a0", sun=3.6)
    sun = bpy.data.objects["sun"]; sun.data.color = hexrgb("#ffd9a8")
    sun.rotation_euler = (math.radians(66), math.radians(-12), math.radians(-52))     # low evening sun from the left
    plane(400, 400, (0, 0, 0), material=mat("meadow", "#62ad4f", rough=0.95, noise_bump=0.12), name="ground")
    sky = mat("skywall_eve", "#7fb4ea", rough=1.0, emit="#8cbcf0", emit_strength=1.0)
    box((400, 1, 160), (0, 70, 40), material=sky, bevel=0)
    cl = mat("cloud_eve", "#fff1e0", rough=0.9, emit="#ffe2c8", emit_strength=0.6)
    random.seed(5)
    for cx, cz in ((-18, 20), (16, 24), (-6, 34)):
        for k in range(4):
            c = sphere(random.uniform(2.0, 3.0), (cx + k * 2.2 - 3.3, 66, cz + random.uniform(-0.6, 0.8)), (1.4, 0.45, 0.6), cl, seg=24)
            c.visible_shadow = False
    hills(False)
    barn(-6.2, 10.0, 1.1)
    farmhouse(5.6, 11.0)
    for i, (x, y, h) in enumerate(((-10, 8, 3.6), (2.0, 13, 3.2), (9.5, 8.0, 3.8), (-2.8, 15, 3.0), (13, 15, 3.6))):
        tree(x, y, h, i)
    fence(-13, 13, 5.2)
    tufts(560, -8, 8, -10, 5, False, 2)
    flowers(70, -7, 7, -9, 4.5)
    # 4th-of-July picnic: table with a pie, two poles with bunting
    tw = wood("#b07a48", "#8a5a30", "picnic", 3.0)
    box((2.2, 0.9, 0.08), (2.6, 2.4, 0.78), material=tw, bevel=0.02)
    for sx in (-0.9, 0.9):
        box((0.08, 0.8, 0.76), (2.6 + sx, 2.4, 0.38), material=tw, bevel=0.01)
    box((2.2, 0.3, 0.06), (2.6, 1.7, 0.45), material=tw, bevel=0.01)
    box((2.0, 0.85, 0.01), (2.6, 2.4, 0.83), material=mat("cloth", "#d6483e", rough=0.8), bevel=0)
    cylinder(0.22, 0.08, (2.2, 2.4, 0.88), material=mat("pie", "#d9a05a", rough=0.6, noise_bump=0.3), verts=32)
    cylinder(0.12, 0.25, (3.1, 2.5, 0.96), material=mat("jug", "#6fc3c0", rough=0.3, coat=0.5), verts=24)
    pole = wood("#f6efe2", "#d8cfc0", "pole", 2.0)
    for px in (0.6, 4.8):
        cylinder(0.05, 3.0, (px, 3.1, 1.5), material=pole, verts=12)
    bunting(0.6, 4.8, 3.1, 2.9)
    front = crater(-0.7, -1.6)
    return front


def farm_angles():
    front = build_farm()
    shots = (("farm_wide", (0.2, -11.5, 2.4), (0.0, 2.0, 4.2), 26, 6.0),
             ("farm_mid", (-0.4, -6.4, 1.6), (-0.2, 0.6, 1.0), 34, 4.0),
             ("farm_close", (-0.45, -4.3, 0.95), (-0.68, -1.5, 0.3), 35, 2.8))
    for name, loc, tgt, lens, fs in shots:
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40 if name == "farm_wide" else 20)
        if name == "farm_mid":
            still("fg_" + name, 1080, 1920, 24, only=front)


def prop_scene(bg="#dfe8f2"):
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb(bg), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def slice_():
    """A cut slice seen face-on: thin black crust ring, grey speckled stone inside (chondrules)."""
    crust = crust_mat()
    stone = mat("stone_in", "#8e8a82", rough=0.7, noise_bump=0.6)
    a = lump(0.5, (0, 0, 0), crust, seed=33, amount=0.12, scale=(1.3, 1.0, 0.12))
    a.rotation_euler = (0, 0, 0)
    b = lump(0.47, (0, 0, 0.035), stone, seed=33, amount=0.12, scale=(1.3, 1.0, 0.1))
    b.rotation_euler = (0, 0, 0)
    random.seed(9)
    cols = [mat("ch1", "#7d7a74", rough=0.5), mat("ch2", "#c9c3b6", rough=0.5), mat("metal_fleck", "#d8dde2", metal=1.0, rough=0.25)]
    for k in range(70):
        ang = random.uniform(0, 2 * math.pi); d = math.sqrt(random.uniform(0, 1)) * 0.82
        sphere(random.uniform(0.012, 0.03), (math.cos(ang) * d * 0.58, math.sin(ang) * d * 0.44, 0.085), (1, 1, 0.3),
               random.choice(cols), seg=10)


if not os.environ.get("BK_PROPS_ONLY"):
    farm_angles()
prop_scene(); meteorite((0, 0, 0), 0.5); camera((0.3, -3.0, 1.3), (0, 0, 0.35), lens=55, fstop=0)
still("meteorite", 700, 600, 32, transparent=True, crop=True)
prop_scene(); meteorite((0, 0, 0), 0.5, frost=True); camera((0.3, -3.0, 1.3), (0, 0, 0.35), lens=55, fstop=0)
still("meteorite_frost", 700, 600, 32, transparent=True, crop=True)
prop_scene(); slice_(); camera((0, -0.4, 3.0), (0, 0, 0.05), lens=55, fstop=0)
still("slice", 700, 600, 32, transparent=True, crop=True)
