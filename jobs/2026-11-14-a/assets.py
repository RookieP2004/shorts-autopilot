# 2026-11-14-a: "Why is gold gold? Blame Einstein" (big-question). Sets: a warm town goldsmith's shop (cream walls, navy
# wainscot, a lit back shelf with a row of metal bars: silver, iron, aluminium, tin, and one gold bar; gold vases, a big
# window with blue sky, a glass display counter with rings and coins as the foreground layer), 2 angles + a shelf close-up;
# a moody atom studio (dark cyclorama, a giant glossy gold nucleus with tilted orbit rings and glowing electrons), 2 angles.
# Cut-outs: gold ring, silver ring, gold bar, silver bar, nucleus, electron.
import math, os, random

# sunny(), gold(), coin(), coin_pile(), coin_stack(), house(), tree(), bunting(), drop_cams() ... (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-09-b/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "b09_helpers", "exec"), globals())


def silver():
    return bpy.data.materials.get("silver_m") or metal("#d9dde2", 0.18, "silver_m")


def bar(loc, s=1.0, material=None, rot=0, name="bar"):
    """A trapezoid ingot: a bevelled box with a slightly smaller top."""
    x, y, z = loc
    b = box((0.52 * s, 0.24 * s, 0.13 * s), (x, y, z + 0.065 * s), (0, 0, rot), material, bevel=0.03 * s, name=name)
    box((0.44 * s, 0.18 * s, 0.05 * s), (0, 0, 0.08 * s), (0, 0, 0), material, bevel=0.02 * s).parent = b
    return b


def ring(loc, r=0.1, material=None, rot=(70, 0, 0), stone=None, name="ring"):
    o = torus(r, r * 0.16, loc, rot, material, name=name)
    if stone:
        sphere(r * 0.22, (0, r * 1.05, 0), 1, stone, seg=24).parent = o
    return o


def vase(x, y, z, s=1.0, material=None):
    return lathe([(0, 0), (0.12 * s, 0), (0.2 * s, 0.12 * s), (0.17 * s, 0.32 * s), (0.08 * s, 0.42 * s), (0.11 * s, 0.5 * s), (0, 0.5 * s)],
                 40, (x, y, z), material, 1, "vase")


def build_shop():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#f2e6d4"), 0.5)
    plane(40, 40, (0, 0, 0), material=paper(os.path.join(TEX, "floor_checker.png"), 0.3, "tiles"), name="tiles")
    box((30, 0.3, 9), (0, 5, 4.5), material=mat("wall", "#3d7f7c", rough=0.7), bevel=0)
    box((30, 0.1, 1.3), (0, 4.82, 0.65), material=mat("wainscot", "#7c2533", rough=0.5, coat=0.3), bevel=0.02)
    box((30, 0.14, 0.08), (0, 4.8, 1.32), material=metal("#c9a24a", 0.3, "trim"), bevel=0.01)
    box((0.3, 20, 9), (-7.5, -2, 4.5), material=mat("wall_l", "#356f6c", rough=0.7), bevel=0)
    text3d("GOLDSMITH", 0.7, (0.6, 4.75, 5.3), (90, 0, 0), metal("#c9a24a", 0.3, "sign"), font="serif", extrude=0.05)
    # the window (left of the back wall)
    sky = mat("win_sky", "#8fd0f0", rough=0.5, emit="#bfe6ff", emit_strength=1.6)
    box((2.4, 0.05, 2.2), (-4.4, 4.83, 2.9), material=sky, bevel=0)
    fr = mat("win_frame", "#f6efe2", rough=0.4, coat=0.3)
    for zz in (1.8, 4.0):
        box((2.6, 0.12, 0.1), (-4.4, 4.78, zz), material=fr, bevel=0.02)
    for xx in (-5.6, -4.4, -3.2):
        box((0.1, 0.12, 2.3), (xx, 4.78, 2.9), material=fr, bevel=0.02)
    # the lit back shelf: a row of metal bars (all silvery... except one)
    shelf = wood("#8a4f2c", "#5e321a", "shelf_wood", 3.0)
    box((5.6, 0.7, 0.1), (1.0, 4.45, 2.2), material=shelf, bevel=0.02)
    box((5.6, 0.04, 2.9), (1.0, 4.8, 3.0), material=mat("shelf_back", "#efe3cf", rough=0.6), bevel=0.01)
    box((5.6, 0.7, 0.1), (1.0, 4.45, 3.5), material=shelf, bevel=0.02)
    mats = [silver(), metal("#8f959c", 0.35, "iron_m"), metal("#c8cdd2", 0.3, "alu_m"), metal("#b4b8bb", 0.25, "tin_m"),
            metal("#a9aeb3", 0.3, "nickel_m"), gold()]
    for k, m in enumerate(mats):
        bar((-0.55 + k * 0.62, 4.35, 2.25), 1.05, m, 0, f"shelf_bar{k}")
    for k in range(4):
        vase(-0.6 + k * 1.1, 4.4, 3.55, 1.1 if k % 2 else 0.9, gold() if k % 2 == 0 else silver())
    lampm = mat("lamp", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    box((5.4, 0.2, 0.05), (1.0, 4.2, 3.43), material=lampm, bevel=0.01)
    box((5.4, 0.2, 0.05), (1.0, 4.2, 4.82), material=lampm, bevel=0.01)
    # goldsmith's workbench on the right, with a little furnace glow
    bench = wood("#a8743f", "#7a4e2a", "bench_w", 4.0)
    box((2.2, 1.0, 0.9), (5.4, 3.8, 0.45), material=bench, bevel=0.03)
    box((0.9, 0.8, 0.9), (5.9, 3.8, 1.35), material=mat("furnace", "#5a6068", rough=0.5, metal=0.4), bevel=0.06)
    box((0.5, 0.05, 0.35), (5.9, 3.39, 1.35), material=mat("furnace_glow", "#ff9a3a", emit="#ffb24a", emit_strength=6), bevel=0.02)
    coin_stack(4.7, 3.7, 7, 0.1, 1)
    plant = mat("plant", "#4f9e4a", rough=0.6)
    random.seed(2)
    for px in (-6.6, 7.2):
        lathe([(0, 0), (0.3, 0), (0.38, 0.55), (0.0, 0.55)], 32, (px, 3.4, 0), mat("pot", "#c4623a", rough=0.6), 1, "pot")
        for k in range(6):
            sphere(0.35, (px + random.uniform(-0.25, 0.25), 3.4 + random.uniform(-0.2, 0.2), 0.9 + k * 0.12), 1, plant, seg=20)
    # the glass display counter (foreground layer)
    body_m = wood("#8a4f2c", "#5e321a", "counter_wood", 3.0)
    velvet = mat("velvet", "#7c2533", rough=0.9)
    counter = [box((3.6, 0.9, 0.85), (-0.6, 0.6, 0.425), material=body_m, bevel=0.05),
               box((3.5, 0.8, 0.04), (-0.6, 0.6, 0.87), material=velvet, bevel=0.01),
               box((3.7, 0.95, 0.03), (-0.6, 0.6, 1.25), material=glass("#f4fbff", 0.02, "case_glass"), bevel=0.005)]
    for xx in (-2.42, 1.22):
        counter.append(box((0.05, 0.95, 0.4), (xx, 0.6, 1.06), material=metal("#c9a24a", 0.3, "case_trim"), bevel=0.01))
    counter.append(box((3.7, 0.05, 0.05), (-0.6, 0.13, 1.25), material=metal("#c9a24a", 0.3, "case_trim"), bevel=0.01))
    random.seed(7)
    for k in range(6):
        counter.append(ring((-2.0 + k * 0.5, 0.55 + random.uniform(-0.1, 0.1), 0.94), 0.07, gold() if k % 3 else silver(), (70, 0, 20 * k)))
    for k in range(3):
        counter.append(bar((0.4 + k * 0.28, 0.75, 0.89), 0.45, gold(), 20, f"cbar{k}"))
    counter += [coin((-0.9 + k * 0.17, 0.4, 0.9), (0, 0, k * 40), 0.06, f"cc{k}") for k in range(4)]
    area_light((-3, -4, 6), (0, 1, 1.5), 1300, 4, "#fff0dc", "key")
    cylinder(2.2, 0.02, (-0.4, -1.4, 0.01), material=mat("rug", "#f2b04a", rough=0.9), verts=64, bevel=0)
    cylinder(1.9, 0.025, (-0.4, -1.4, 0.012), material=mat("rug_in", "#c4623a", rough=0.9), verts=64, bevel=0)
    for lx in (-2.4, 1.0, 4.2):
        cylinder(0.01, 2.2, (lx, 1.5, 6.9), material=mat("cord", "#1a1410"), verts=8, bevel=0)
        lathe([(0, 0), (0.45, 0), (0.25, 0.35), (0.05, 0.4), (0, 0.4)], 32, (lx, 1.5, 5.4), metal("#c9a24a", 0.3, "shade"), 1, "shade")
        sphere(0.14, (lx, 1.5, 5.42), 1, lampm, seg=20); area_light((4, -2, 4), (0, 1, 1.5), 480, 4, "#dbe8ff", "fill")
    area_light((1.0, 2.6, 3.0), (1.0, 4.4, 2.6), 260, 2.5, "#ffe2b0", "shelf_spot")
    area_light((-4.4, 3.6, 3.0), (0, 0, 1.0), 260, 2.5, "#e6f4ff", "window_bounce")
    return counter


def shop_angles():
    counter = build_shop()
    for name, loc, tgt, lens, fs in (("shop_wide", (-0.2, -8.6, 2.3), (-0.2, 1.5, 2.0), 26, 6.0),
                                     ("shop_mid", (-0.9, -4.6, 1.8), (-0.6, 0.8, 1.3), 34, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=counter)
    drop_cams(); camera((1.0, -1.0, 2.6), (1.0, 4.4, 2.6), lens=26, fstop=2.8)
    still("plate_shelf_close", 1080, 1920, 40)


def nucleus(loc=(0, 0, 0.5), r=0.12, n=40, seed=5):
    random.seed(seed)
    p = bpy.data.materials.get("proton") or mat("proton", "#d9534f", rough=0.22, coat=0.7)
    q = bpy.data.materials.get("neutron") or mat("neutron", "#f2b04a", rough=0.22, coat=0.7)
    pts = [(0, 0, 0)]
    k = 0
    R = r * (n ** (1 / 3)) * 0.62
    while len(pts) < n and k < 6000:
        k += 1
        v = (random.uniform(-R, R), random.uniform(-R, R), random.uniform(-R, R))
        if math.sqrt(sum(c * c for c in v)) > R:
            continue
        if all(math.dist(v, o) > r * 1.05 for o in pts):
            pts.append(v)
    for i, v in enumerate(pts):
        sphere(r, (loc[0] + v[0], loc[1] + v[1], loc[2] + v[2]), 1, p if i % 2 else q, seg=24)


def build_atom():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#101a22"), 0.5)
    # cyclorama: floor + a curved back
    cyc = mat("cyc", "#1f2f3a", rough=0.8)
    plane(60, 60, (0, 0, 0), material=cyc, name="cyc_floor")
    cylinder(14, 30, (0, 16, 0), (0, 0, 0), cyc, verts=96, bevel=0)
    ctr = (0, 1.5, 2.6)
    nucleus(ctr, 0.24, 79, 11)
    ringm = mat("orbit", "#6fc3c0", rough=0.3, emit="#6fc3c0", emit_strength=1.6)
    em = mat("electron", "#1fa8ff", rough=0.2, coat=0.6, emit="#5cc8ff", emit_strength=4.0)
    for k, (rad, tilt, spin_) in enumerate(((1.5, 70, 0), (2.0, 62, 55), (2.5, 75, -40))):
        torus(rad, 0.022, ctr, (tilt, 0, spin_), ringm, name=f"orbit{k}")
        o = bpy.data.objects[f"orbit{k}"]
        for j in range(2):
            a = j * math.pi + k
            local = mathutils.Vector((rad * math.cos(a), rad * math.sin(a), 0))
            wpos = o.matrix_world @ local if False else None
            # place electrons on the tilted ring (rotate the local point by the ring's euler)
            e = mathutils.Euler((math.radians(tilt), 0, math.radians(spin_)), "XYZ")
            p = local.copy(); p.rotate(e)
            sphere(0.16, (ctr[0] + p.x, ctr[1] + p.y, ctr[2] + p.z), 1, em, seg=24)
    # a gold "79" plinth label on the floor
    area_light((-4, -4, 6), ctr, 1300, 3, "#ffe2c2", "key")
    area_light((4, 6, 5), ctr, 1100, 3, "#8fd3ff", "rim")
    area_light((5, -3, 2), ctr, 200, 5, "#9fb4c8", "fill")


def atom_angles():
    build_atom()
    drop_cams(); camera((0, -9.0, 2.2), (0, 1.5, 2.9), lens=30, fstop=4.0)
    still("plate_atom_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.9, -2.6, 2.9), (0, 1.5, 2.6), lens=34, fstop=2.2)
    still("plate_atom_close", 1080, 1920, 40)


def prop_scene2(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#e6ecf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


import mathutils  # noqa: E402

if not os.environ.get("BK_PROPS_ONLY"):
    shop_angles()
    atom_angles()
prop_scene2(); ring((0, 0, 0.3), 0.3, gold(), (75, 0, 10)); sprite_camera((0, 0, 0.3), 2.4, 0.4, 50, azimuth=-10)
still("gold_ring", 600, 600, 32, transparent=True, crop=True)
prop_scene2(); ring((0, 0, 0.3), 0.3, silver(), (75, 0, 10)); sprite_camera((0, 0, 0.3), 2.4, 0.4, 50, azimuth=-10)
still("silver_ring", 600, 600, 32, transparent=True, crop=True)
prop_scene2(); bar((0, 0, 0), 1.0, gold(), 15); sprite_camera((0, 0, 0.08), 2.0, 1.0, 50)
still("gold_bar", 600, 500, 32, transparent=True, crop=True)
prop_scene2(); bar((0, 0, 0), 1.0, silver(), 15); sprite_camera((0, 0, 0.08), 2.0, 1.0, 50)
still("silver_bar", 600, 500, 32, transparent=True, crop=True)
prop_scene2(); nucleus((0, 0, 0.5), 0.1, 79, 11); sprite_camera((0, 0, 0.5), 3.0, 0.6, 50, azimuth=-15)
still("nucleus", 600, 600, 32, transparent=True, crop=True)
prop_scene2(); sphere(0.4, (0, 0, 0.5), 1, mat("electron", "#1fa8ff", rough=0.2, coat=0.6, emit="#5cc8ff", emit_strength=1.2), seg=40)
sprite_camera((0, 0, 0.5), 3.0, 0.4, 50, azimuth=0)
still("electron", 500, 500, 24, transparent=True, crop=True)
