# 2026-11-23-a: "Sugar makes kids hyper? Scientists tested it" (myth-bust, chef Ved).
# Set: the town kitchen from 2026-11-21-m1 re-dressed for a kids' party: bunting on the wall, a two-tier birthday cake with
# candles, cupcakes, a candy bowl and two identical red party cups (the placebo drink). 3 angles: wide, mid on the cake,
# close on the two cups. Cut-outs: a red party cup, a cupcake.
import math, os, random

_src = open(os.path.join(ROOT, "jobs/2026-11-21-m1/assets.py")).read().split("\nif not os.environ.get")[0]
_src = _src.replace('A = os.path.join(ROOT, "jobs/2026-11-21-m1/assets")', 'A = os.path.join(ROOT, "jobs/2026-11-23-a/assets")')
exec(compile(_src, "m21_helpers", "exec"), globals())          # kitchen(), microwave(), sunny(), bunting(), drop_cams() ...


def hide(prefixes):
    for o in list(bpy.data.objects):
        if any(o.name.startswith(p) for p in prefixes):
            bpy.data.objects.remove(o)


def red_cup(x, y, z, s=1.0, name="cup"):
    m = mat("cup_red", "#d6302c", rough=0.3, coat=0.6)
    inner = mat("cup_in", "#f6efe2", rough=0.4)
    lathe([(0.0, 0.0), (0.03 * s, 0.0), (0.032 * s, 0.004 * s), (0.046 * s, 0.11 * s), (0.049 * s, 0.114 * s),
           (0.0, 0.114 * s)], 40, (x, y, z), m, name=name)
    cylinder(0.044 * s, 0.004, (x, y, z + 0.106 * s), material=mat("drink", "#8a1e3c", rough=0.08, coat=0.9), verts=32, bevel=0)
    torus(0.047 * s, 0.003 * s, (x, y, z + 0.113 * s), (0, 0, 0), inner)


def cupcake(x, y, z, s=1.0, icing="#f4a6c0", name="cc"):
    lathe([(0.0, 0.0), (0.03 * s, 0.0), (0.04 * s, 0.045 * s), (0.0, 0.045 * s)], 32, (x, y, z),
          mat("cc_wrap", "#6fc3c0", rough=0.5), name=name)
    lathe([(0.0, 0.0), (0.046 * s, 0.0), (0.04 * s, 0.025 * s), (0.026 * s, 0.045 * s), (0.008 * s, 0.06 * s), (0.0, 0.062 * s)],
          32, (x, y, z + 0.044 * s), mat("icing" + icing, icing, rough=0.35, coat=0.4, sss=0.1), name=name + "_ice")
    sphere(0.011 * s, (x, y, z + 0.11 * s), 1, mat("cherry", "#b3121b", rough=0.15, coat=0.9), seg=16)


def cake(x, y, z):
    sponge = mat("cake_ice", "#fbe9d6", rough=0.35, coat=0.3, sss=0.1)
    pink = mat("cake_pink", "#f4a6c0", rough=0.35, coat=0.3)
    lathe([(0.0, 0.0), (0.22, 0.0), (0.225, 0.13), (0.21, 0.145), (0.0, 0.145)], 64, (x, y, z), sponge, name="cake1")
    torus(0.215, 0.018, (x, y, z + 0.14), (0, 0, 0), pink)
    lathe([(0.0, 0.0), (0.15, 0.0), (0.155, 0.11), (0.14, 0.12), (0.0, 0.12)], 64, (x, y, z + 0.145), pink, name="cake2")
    torus(0.147, 0.014, (x, y, z + 0.262), (0, 0, 0), sponge)
    random.seed(4)
    for k in range(18):           # sprinkles
        a = random.uniform(0, 6.28); r = random.uniform(0.02, 0.13)
        box((0.016, 0.005, 0.005), (x + math.cos(a) * r, y + math.sin(a) * r, z + 0.268), (0, 0, random.uniform(0, 180)),
            mat(f"spr{k % 4}", ["#46965a", "#f2b04a", "#3f7fbf", "#ffffff"][k % 4], rough=0.4), bevel=0)
    for k in range(5):            # candles
        a = k / 5 * 6.28
        cx, cy = x + math.cos(a) * 0.08, y + math.sin(a) * 0.08
        cylinder(0.007, 0.07, (cx, cy, z + 0.3), material=mat(f"cdl{k % 3}", ["#3f7fbf", "#f2b04a", "#46965a"][k % 3], rough=0.4), verts=12, bevel=0)
        sphere(0.009, (cx, cy, z + 0.345), (0.8, 0.8, 1.5), glow("#ffc35a", 25.0, "flame"), seg=12)
    cylinder(0.25, 0.012, (x, y, z), material=mat("cake_plate", "#f6efe2", rough=0.25, coat=0.6), verts=64, bevel=0.004)


def party_kitchen():
    kitchen()
    hide(["kettle", "bowl", "ap0", "ap1", "ap2", "ap3"])
    bunting(-3.4, 3.0, 2.44, 2.75)
    cake(0.3, 2.2, 0.91)
    for k, (dx, ic) in enumerate(((-0.42, "#f4a6c0"), (-0.28, "#f2b04a"), (-0.62, "#bfe3d6"))):
        cupcake(0.3 + dx, 2.05 + (k % 2) * 0.08, 0.91, 1.0, ic, f"cc{k}")
    lathe([(0, 0), (0.12, 0.0), (0.14, 0.06), (0.0, 0.06)], 40, (1.55, 2.2, 0.91), mat("candy_bowl", "#3f7fbf", rough=0.3, coat=0.4), name="cbowl")
    random.seed(8)
    for k in range(16):
        a = random.uniform(0, 6.28); r = random.uniform(0, 0.09)
        sphere(0.022, (1.55 + math.cos(a) * r, 2.2 + math.sin(a) * r, 0.97 + random.uniform(0, 0.03)), 1,
               mat(f"candy{k % 4}", ["#d6483e", "#f2b04a", "#46965a", "#f4a6c0"][k % 4], rough=0.2, coat=0.9), seg=16)
    red_cup(0.92, 2.08, 0.91, 1.0, "cupA")
    red_cup(1.12, 2.08, 0.91, 1.0, "cupB")


def party_angles():
    party_kitchen()
    drop_cams(); camera((0.35, -2.3, 1.45), (0.35, 2.2, 1.3), lens=24, fstop=8.0)
    still("plate_kit_wide", 1080, 1920, 40)
    drop_cams(); camera((0.3, 0.55, 1.25), (0.3, 2.2, 1.05), lens=32, fstop=2.8)
    still("plate_kit_cake", 1080, 1920, 40)
    drop_cams(); camera((1.02, 1.2, 1.1), (1.02, 2.1, 0.97), lens=40, fstop=2.2)
    still("plate_kit_cups", 1080, 1920, 40)


if not os.environ.get("BK_PROPS_ONLY"):
    party_angles()

# cut-outs
reset(600, 700, 30, 0.1, samples=32, transparent=True, bloom=0)
sunny()
area_light((-1.2, -1.6, 1.6), (0, 0, 0.1), 260, 1.6, "#fff0dc", "key")
area_light((1.4, 0.8, 0.9), (0, 0, 0.1), 140, 0.8, "#bfe6ff", "rim")
red_cup(0, 0, 0, 1.0, "cup_hero")
drop_cams(); camera((0.0, -0.6, 0.2), (0.0, 0.0, 0.06), lens=50, fstop=0)
still("cup", 600, 700, 32, transparent=True, crop=True)
hide(["cup_hero", "Torus", "Cylinder"])
for o in list(bpy.data.objects):
    if o.type == "MESH":
        bpy.data.objects.remove(o)
cupcake(0, 0, 0, 1.0, "#f4a6c0", "cc_hero")
drop_cams(); camera((0.0, -0.55, 0.2), (0.0, 0.0, 0.055), lens=50, fstop=0)
still("cupcake", 600, 700, 32, transparent=True, crop=True)
