# 2026-11-15-b: "You have way more than 5 senses" (big-question, "you've been told X" hook). Sets: the sunny town park
# (picnic blanket, cake, basket, round trees, fountain, houses) from 2026-11-08-c, now with a bright playground roundabout
# (merry-go-round) on the grass, 2 angles (wide by the roundabout, mid by the picnic); an inner-ear close-up: three glossy
# semicircular canals + the cochlea snail on a dark plum studio, fluid glowing blue inside. Cut-outs: the inner ear, a
# heart, a thermometer.
import math, os, random

# build_park(), sunny(), tree(), bush(), house(), bench(), cake(), prop_scene() ... (frozen helpers from 2026-11-08-c)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def roundabout(x, y):
    """A playground merry-go-round: a round painted deck in four colour wedges, a central post and a ring of grab bars."""
    parts = [cylinder(0.92, 0.08, (x, y, 0.32), material=plastic("#f2b04a", 0.35, "rb_deck"), verts=64, bevel=0.02)]
    for k, c in enumerate(("#d9534f", "#3d7fd1")):
        parts.append(box((1.8, 0.34, 0.012), (x, y, 0.365), (0, 0, 45 + k * 90), plastic(c, 0.35, f"rb_stripe{k}"), bevel=0))
    parts.append(cylinder(0.95, 0.06, (x, y, 0.27), material=metal("#c9ced6", 0.3, "rb_rim"), verts=64, bevel=0.02))
    parts.append(cylinder(0.2, 0.3, (x, y, 0.14), material=metal("#5a6068", 0.4, "rb_base"), verts=32))
    steel = metal("#e6e9ee", 0.2, "rb_bar")
    parts.append(cylinder(0.06, 1.1, (x, y, 0.9), material=steel, verts=20))
    parts.append(sphere(0.1, (x, y, 1.47), 1, plastic("#d9534f", 0.3, "rb_knob")))
    for k in range(4):
        a = math.radians(k * 90 + 45)
        px, py = x + 0.8 * math.cos(a), y + 0.8 * math.sin(a)
        parts.append(seg((px, py, 0.36), (px * 0.5 + x * 0.5, py * 0.5 + y * 0.5, 1.0), 0.035, steel))
        parts.append(seg((px * 0.5 + x * 0.5, py * 0.5 + y * 0.5, 1.0), (x, y, 1.2), 0.035, steel))
    cylinder(1.4, 0.03, (x, y, 0.015), material=mat("rb_sand", "#e8d3a6", rough=0.95, noise_bump=0.3), verts=64, bevel=0)
    return parts


def park_b_angles():
    fgp, hill, b1 = build_park()
    for o in list(bpy.data.objects):
        if o.name.startswith("anthill"):
            bpy.data.objects.remove(o)
    rb = roundabout(2.3, 1.6)
    for name, loc, tgt, lens, fs, fg in (("park_wide", (0.9, -9.4, 2.5), (0.6, 1.4, 1.2), 30, 6.0, fgp + b1),
                                         ("park_mid", (-0.6, -4.6, 1.75), (0.15, 0.3, 0.95), 34, 4.0, fgp)):
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=fg)
    drop_cams()
    camera((4.6, -2.4, 1.3), (2.3, 1.6, 0.7), lens=30, fstop=3.0)
    still("plate_round_close", 1080, 1920, 40)


def canal_mat():
    return bpy.data.materials.get("canal") or mat("canal", "#f7d2cc", rough=0.06, coat=0.8, sss=0.1, transmission=0.8)


def fluid_mat():
    return bpy.data.materials.get("ear_fluid") or mat("ear_fluid", "#4fb6ff", rough=0.1, emit="#4fb6ff", emit_strength=5.0)


def inner_ear(c=(0, 0, 0), s=1.0):
    """Three semicircular canals at right angles + a vestibule bulb + a cochlea snail."""
    cx, cy, cz = c
    cm, fm = canal_mat(), fluid_mat()
    sphere(0.28 * s, (cx, cy, cz), (1.2, 1.0, 0.9), cm)
    # canals: tori, each a different plane, sitting on the vestibule
    for loc, rot, R in (((cx - 0.1 * s, cy, cz + 0.5 * s), (90, 0, 35), 0.4),
                        ((cx - 0.42 * s, cy + 0.05 * s, cz + 0.42 * s), (90, 0, -55), 0.36),
                        ((cx - 0.55 * s, cy - 0.05 * s, cz + 0.1 * s), (0, 0, 0), 0.3)):
        torus(R * s, 0.075 * s, loc, rot, cm)
        torus(R * s, 0.04 * s, loc, rot, fm)
    # cochlea: a tapering spiral tube to the right
    pts, n = [], 60
    for k in range(n + 1):
        t = k / n
        a = t * 2.6 * 2 * math.pi
        r = (0.42 - 0.3 * t) * s
        pts.append((cx + 0.6 * s + r * math.cos(a), cy - r * math.sin(a) * 0.3, cz - 0.15 * s + r * math.sin(a) + 0.12 * s * t))
    cu = bpy.data.curves.new("cochlea", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.085 * s; cu.bevel_resolution = 4
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS"); sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (*q, 1)
    sp.order_u = 4; sp.use_endpoint_u = True
    ob = bpy.data.objects.new("cochlea", cu); bpy.context.collection.objects.link(ob); ob.data.materials.append(cm)
    seg((cx + 0.2 * s, cy, cz - 0.05 * s), (cx + 0.75 * s, cy, cz - 0.1 * s), 0.12 * s, cm)


def ear_close():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2)
    world_color(hexrgb("#2a1530"), 0.5)
    floor("#3a1c3e", 0.5)
    inner_ear((0, 0, 1.0), 1.0)
    # soft pink walls of the "inside of your head": a few blurred blobs behind
    wall = mat("tissue", "#8a3a5a", rough=0.5, sss=0.3)
    for k, (x, y, z, r) in enumerate(((-2.2, 3.5, 1.5, 1.6), (2.4, 3.8, 2.4, 1.9), (0.2, 5.0, 3.4, 2.2), (-1.6, 3.0, 3.6, 1.2))):
        sphere(r, (x, y, z), 1, wall, seg=40)
    area_light((-3, -3, 4), (0, 0, 1), 700, 3, "#ffe2c2", "key")
    area_light((3, 2, 3), (0, 0, 1), 400, 2.5, "#8fd3ff", "rim")
    drop_cams(); camera((1.2, -4.8, 0.9), (0.0, 0, 0.95), lens=38, fstop=2.4)
    still("plate_ear_close", 1080, 1920, 40)


def heart(c=(0, 0, 0.3), s=1.0):
    m = organic("#c8323c", "heart_mat")
    x, y, z = c
    sphere(0.22 * s, (x - 0.12 * s, y, z + 0.1 * s), 1, m)
    sphere(0.22 * s, (x + 0.12 * s, y, z + 0.1 * s), 1, m)
    cone(0.3 * s, 0.42 * s, (x, y, z - 0.18 * s), (180, 0, 0), m)
    cylinder(0.06 * s, 0.25 * s, (x - 0.05 * s, y + 0.02 * s, z + 0.38 * s), (0, 15, 0), organic("#d9707a", "aorta"), verts=20)


def thermometer(c=(0, 0, 0.5)):
    x, y, z = c
    lathe([(0, 0), (0.07, 0.0), (0.075, 0.02), (0.035, 0.12), (0.035, 0.95), (0.0, 0.98)], 32, (x, y, z - 0.5),
          glass("#eaf6ff", 0.03, "therm_glass"), 1, "therm")
    sphere(0.06, (x, y, z - 0.45), 1, plastic("#d9534f", 0.2, "therm_red"))
    cylinder(0.018, 0.55, (x, y, z - 0.18), material=plastic("#d9534f", 0.2, "therm_red"), verts=16)
    for k in range(8):
        box((0.04, 0.005, 0.006), (x + 0.04, y - 0.03, z - 0.3 + k * 0.08), material=mat("therm_ink", "#1a1410"), bevel=0)


if not os.environ.get("BK_PROPS_ONLY"):
    park_b_angles()
    ear_close()
prop_scene(); inner_ear((0, 0, 0.4), 0.5); sprite_camera((0.05, 0, 0.45), 2.4, 0.5, 50, azimuth=-5)
still("inner_ear", 700, 600, 28, transparent=True, crop=True)
prop_scene(); heart((0, 0, 0.35), 1.0); sprite_camera((0, 0, 0.35), 2.6, 0.4, 50, azimuth=-15)
still("heart", 500, 500, 28, transparent=True, crop=True)
