# 2026-11-14-L Deep Dive (16:9): "Why You're 99.9999% Empty Space (And Still Solid)".
# Sets at 1920x1080: the town-square cafe from 2026-11-11-a (wide / mid / table close-up + the "crushed" table), the football
# stadium (wide / pitch / marble close-up), a new 1909 Manchester physics lab (wide / mid / apparatus close-up) and a deep-space
# plate with a neutron star. Cut-outs: alpha particle, gold foil, neutron star. Sugar cube / marble / electron / nucleus
# cut-outs are reused from jobs/2026-11-11-a/assets. The island market plates are reused from the long pilot.
import math, os, random

# cafe + stadium builders, sugar cube, marble, nucleus (frozen helpers from the sugar-cube Short, which pull in the town helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-11-a/assets.py")).read().split("\ncafe_plates()\n")[0]
exec(compile(_src, "a_helpers", "exec"), globals())

W, H = 1920, 1080


def shoot(name, loc, tgt, lens, fs=0, samples=40, fg_objs=None):
    drop_cams()
    camera(loc, tgt, lens=lens, fstop=fs)
    still("plate_" + name, W, H, samples)
    if fg_objs:
        still("fg_" + name, W, H, 24, only=fg_objs)


def cafe16():
    fg = build_cafe()
    # landscape shows more of the square: extra houses, trees and a second parasol table either side
    cols = ["#e8a598", "#9fd39a", "#f2b04a", "#c9b7e3"]
    for k, x in enumerate((-15.5, -13.0, 13.5, 16.0)):
        house(x, 9.0 + (k % 2) * 0.7, 2.7, 4 + k % 3, cols[k], ["#34425c", "#b5533c"][k % 2])
    tree(-8.5, 5.5, 4.2, 1.5, 11); tree(8.8, 6.0, 4.0, 1.4, 12, "#5aa64a")
    table(4.2, 2.6); bistro_chair(3.7, 2.7, 90); bistro_chair(4.7, 2.9, -90); parasol(4.2, 2.6)
    bush(-6.2, 2.0, 0.55, seed=6); bush(6.6, 1.6, 0.5, "#46965a", "#d9534f", 7)
    shoot("cafe_wide", (0.3, -7.2, 1.75), (0.15, 1.5, 1.4), 28, 0, 40, fg)
    shoot("cafe_mid", (-0.2, -3.9, 1.4), (0.4, 0.6, 1.0), 30, 0, 40, fg)
    drop_cams()
    camera((TX + 0.18, TY - 0.78, 0.92), (TX, TY - 0.12, 0.8), lens=50, fstop=2.2)
    still("plate_cafe_table", W, H, 48)
    build_cafe(crushed=True)
    shoot("cafe_crushed", (-0.2, -3.9, 1.4), (0.4, 0.6, 1.0), 30, 0, 40)


def stadium16():
    stadium()
    shoot("stadium_wide", (-66, -10, 38), (8, 0, 0), 22, 0, 40)
    shoot("stadium_pitch", (-9.0, -4.0, 1.6), (2, 0.6, 1.3), 26, 0, 40)
    shoot("stadium_marble", (-0.8, -0.3, 0.24), (0, 0, 0.12), 50, 2.0, 40)


# ------------------------------------------------------------------ 1909 Manchester lab
def bottle(x, y, z, h, col, k):
    lathe([(0, 0), (0.06, 0), (0.07, 0.02), (0.07, h * 0.7), (0.03, h * 0.85), (0.025, h), (0.0, h)], 24, (x, y, z),
          mat(f"bottle{k}", col, rough=0.05, transmission=0.85, ior=1.45, coat=0.5), 1, f"bottle{k}")


def apparatus(x, y, z, s=1.0):
    """Geiger-Marsden scattering set-up on the bench: brass chamber, lead source box, gold foil, zinc-sulphide screen + microscope."""
    brass = metal("#c9a24a", 0.28, "brass")
    lead = metal("#4a4f57", 0.5, "lead")
    gold = metal("#f0c040", 0.15, "foil_gold")
    objs = []
    objs.append(cylinder(0.32 * s, 0.07 * s, (x, y, z + 0.035 * s), material=brass, verts=48, bevel=0.01))          # base plate
    objs.append(box((0.22 * s, 0.2 * s, 0.2 * s), (x - 0.42 * s, y, z + 0.1 * s), material=lead, bevel=0.015))          # source box
    objs.append(cylinder(0.02 * s, 0.14 * s, (x - 0.3 * s, y, z + 0.13 * s), (0, 90, 0), brass, verts=16))             # collimator
    objs.append(cylinder(0.012 * s, 0.24 * s, (x, y, z + 0.19 * s), material=brass, verts=12))                          # foil stand
    objs.append(box((0.006 * s, 0.2 * s, 0.2 * s), (x, y, z + 0.3 * s), (0, 0, -55), gold, bevel=0.002))             # gold foil
    objs.append(torus(0.14 * s, 0.012 * s, (x, y, z + 0.3 * s), (0, 90, -55), brass))
    # screen + microscope on a swinging arm
    objs.append(seg((x, y, z + 0.08 * s), (x - 0.2 * s, y - 0.32 * s, z + 0.08 * s), 0.012 * s, brass))
    objs.append(cylinder(0.07 * s, 0.01 * s, (x - 0.2 * s, y - 0.3 * s, z + 0.3 * s), (90, 0, 30),
                         mat("zns", "#9be8b0", rough=0.4, emit="#7dffb0", emit_strength=0.6), verts=32))
    objs.append(cylinder(0.035 * s, 0.32 * s, (x - 0.27 * s, y - 0.42 * s, z + 0.3 * s), (90, 0, 30), brass, verts=24))
    objs.append(cylinder(0.045 * s, 0.05 * s, (x - 0.35 * s, y - 0.56 * s, z + 0.3 * s), (90, 0, 30), mat("eyepiece", "#1a1a1a", rough=0.3), verts=24))
    return objs


def lab():
    reset(W, H, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#2a2018"), 0.5)
    plane(30, 30, (0, 0, 0), material=wood("#7a5232", "#553820", "lab_planks", 1.2, 0.6), name="planks")
    box((18, 0.3, 6), (0, 3.4, 3), material=mat("lab_plaster", "#d8cdb4", rough=0.85, noise_bump=0.15), bevel=0)
    box((18, 0.34, 1.2), (0, 3.22, 0.6), material=wood("#5a3a22", "#3a2414", "wainscot", 2.0), bevel=0.02)
    # tall window with daylight
    box((2.2, 0.1, 3.0), (-3.6, 3.22, 3.0), material=glow("#dfeeff", 2.2, "window_light"), bevel=0)
    for dx in (-0.55, 0.55):
        box((0.08, 0.14, 3.0), (-3.6 + dx, 3.16, 3.0), material=wood("#3a2414", "#2a180c", "mullion", 2.0), bevel=0.01)
    box((2.2, 0.14, 0.08), (-3.6, 3.16, 3.0), material=wood("#3a2414", "#2a180c", "mullion", 2.0), bevel=0.01)
    box((2.4, 0.18, 0.12), (-3.6, 3.12, 1.48), material=wood("#3a2414", "#2a180c", "sill", 2.0), bevel=0.02)
    # blackboard
    box((2.8, 0.08, 1.6), (2.4, 3.2, 2.6), material=mat("board", "#22302a", rough=0.9), bevel=0.02)
    box((2.95, 0.12, 1.75), (2.4, 3.24, 2.6), material=wood("#5a3a22", "#3a2414", "board_frame", 2.0), bevel=0.02)
    chalk = mat("chalk", "#e8e4d8", rough=0.9)
    text3d("ALPHA -> GOLD", 0.34, (2.4, 3.15, 3.0), (90, 0, 0), chalk, font="display", extrude=0.004)
    text3d("1909", 0.42, (2.9, 3.15, 2.3), (90, 0, 0), chalk, font="display", extrude=0.004)
    torus(0.28, 0.014, (1.65, 3.15, 2.35), (90, 0, 0), chalk); sphere(0.05, (1.65, 3.15, 2.35), 1, chalk)
    for k in range(4):
        box((0.5, 0.01, 0.014), (1.0 + 0.0 * k, 3.15, 2.0 + k * 0.17), (0, 0, 0), chalk, bevel=0)
    # second bench on the left with glassware, a radiator, a hanging chart, crates
    lb = wood("#6e4224", "#46280f", "bench", 3.0)
    box((2.2, 0.8, 0.9), (-4.6, 1.9, 0.45), material=lb, bevel=0.04)
    box((2.35, 0.9, 0.06), (-4.6, 1.9, 0.93), material=wood("#8a5a30", "#5e3a1c", "bench_top", 4.0), bevel=0.02)
    for k in range(5):
        bottle(-5.4 + k * 0.38, 1.9, 0.96, 0.3 + 0.06 * (k % 2), ["#7fb7c9", "#c98a4a", "#9fd39a", "#b58bd3", "#e8e4d8"][k], 40 + k)
    lathe([(0, 0), (0.16, 0), (0.18, 0.05), (0.06, 0.3), (0.05, 0.42), (0.0, 0.42)], 32, (-3.8, 1.8, 0.96),
          mat("flask", "#bfe6f2", rough=0.03, transmission=0.9, ior=1.45), 1, "flask")
    for k in range(9):
        box((0.06, 0.12, 0.7), (-1.2 + k * 0.12, 3.05, 0.55), material=metal("#8a8f98", 0.4, "radiator"), bevel=0.02)
    box((1.1, 0.04, 1.4), (5.6, 3.18, 2.9), material=mat("chart", "#efe3c8", rough=0.8), bevel=0.005)
    for k in range(3):
        torus(0.12 + k * 0.12, 0.012, (5.6, 3.15, 2.9), (90, 0, 0), mat("chart_ink", "#7c2533", rough=0.6))
    sphere(0.04, (5.6, 3.15, 2.9), 1, mat("chart_ink", "#7c2533", rough=0.6))
    for k, (cx, cy) in enumerate(((6.4, 0.9), (6.9, 1.4))):
        box((0.7, 0.55, 0.5), (cx, cy, 0.25 + 0.5 * (k == 2)), (0, 0, 10 * k), wood("#b8864e", "#8a6036", "crate", 4.0), bevel=0.025)
    # shelves of bottles
    sh = wood("#5e3e24", "#3e2614", "lab_shelf", 3.0)
    for z in (1.7, 2.4):
        box((2.4, 0.4, 0.06), (-0.4, 3.0, z), material=sh, bevel=0.01)
    random.seed(4)
    cols = ["#7fb7c9", "#c98a4a", "#9fd39a", "#e8e4d8", "#b58bd3", "#d9534f"]
    for k in range(14):
        z = 1.73 if k < 7 else 2.43
        bottle(-1.45 + (k % 7) * 0.34, 3.0, z, random.uniform(0.22, 0.36), cols[k % 6], k)
    # gas lamp on a bracket
    cylinder(0.02, 0.5, (0.9, 3.05, 3.6), (90, 0, 0), metal("#c9a24a", 0.3, "brass"), verts=12)
    sphere(0.14, (0.9, 2.78, 3.5), 1, mat("lamp_glass", "#fff2d0", rough=0.1, emit="#ffd890", emit_strength=3.0))
    # side cabinet + stool + coat stand
    box((1.2, 0.6, 1.0), (-6.0, 2.6, 0.5), material=wood("#6e4626", "#4a2c16", "cabinet", 3.0), bevel=0.03)
    box((1.6, 0.6, 1.0), (6.0, 2.6, 0.5), material=wood("#6e4626", "#4a2c16", "cabinet", 3.0), bevel=0.03)
    for k in range(3):
        bottle(5.5 + k * 0.4, 2.6, 1.0, 0.3, cols[(k + 2) % 6], 20 + k)
    cylinder(0.2, 0.05, (-1.9, 0.9, 0.7), material=wood("#7a4a2a", "#55311a", "stool", 3.0), verts=24)
    for k in range(3):
        a = k / 3 * 2 * math.pi
        seg((-1.9 + 0.12 * math.cos(a), 0.9 + 0.12 * math.sin(a), 0.68), (-1.9 + 0.2 * math.cos(a), 0.9 + 0.2 * math.sin(a), 0.0),
            0.02, wood("#7a4a2a", "#55311a", "stool", 3.0))
    # the bench (foreground layer) with the apparatus
    top_m = wood("#8a5a30", "#5e3a1c", "bench_top", 4.0)
    bench_objs = [box((3.6, 1.0, 0.92), (0.3, 0.7, 0.46), material=wood("#6e4224", "#46280f", "bench", 3.0), bevel=0.05),
                  box((3.8, 1.12, 0.07), (0.3, 0.68, 0.955), material=top_m, bevel=0.03)]
    bench_objs += apparatus(0.6, 0.6, 0.99)
    for k in range(3):
        bench_objs.append(cylinder(0.05, 0.12, (-1.0 + k * 0.14, 0.75, 1.05), material=mat(f"jar{k}", cols[k], rough=0.05, transmission=0.8), verts=24))
    bench_objs.append(box((0.42, 0.3, 0.04), (1.5, 0.55, 1.01), (0, 0, 8), mat("notebook", "#7c2533", rough=0.6), bevel=0.01))
    bench_objs.append(box((0.4, 0.28, 0.01), (1.5, 0.55, 1.035), (0, 0, 8), mat("pages", "#f6efe2", rough=0.8), bevel=0.002))
    area_light((-3.6, 1.0, 3.2), (0, 0.6, 1.0), 900, 2.5, "#dfeeff", "window_key")
    area_light((-2.5, -3.5, 4.5), (0, 1, 1.2), 900, 3.5, "#ffcf8a", "warm_key")
    area_light((3.5, -1.5, 3.0), (0, 1.5, 1.2), 400, 3, "#ffb36b", "fill")
    shoot("lab_wide", (0.3, -7.0, 2.0), (0.2, 1.2, 1.6), 26, 0, 40, fg_objs=bench_objs)
    shoot("lab_mid", (-0.6, -4.0, 1.75), (0.4, 0.9, 1.35), 30, 3.0, 40, fg_objs=bench_objs)
    shoot("lab_close", (0.05, -0.85, 1.32), (0.55, 0.6, 1.25), 32, 2.0, 48)


# ------------------------------------------------------------------ deep space + neutron star
def space():
    reset(W, H, 30, 0.1, samples=40, bloom=0.5)
    world_color(hexrgb("#05070f"), 1.0)
    random.seed(7)
    star_m = mat("star", "#ffffff", rough=0.5, emit="#ffffff", emit_strength=12.0)
    warm_m = mat("star_w", "#ffe0b0", rough=0.5, emit="#ffd8a0", emit_strength=10.0)
    for k in range(420):
        x, z = random.uniform(-60, 60), random.uniform(-35, 35)
        sphere(random.uniform(0.04, 0.12), (x, 60, z), 1, star_m if k % 4 else warm_m, seg=8)
    # nebula wash: big soft emissive discs far behind
    core = mat("ns_core", "#cfe6ff", rough=0.3, emit="#a8d4ff", emit_strength=4.0)
    sphere(0.8, (2.1, 0, -0.7), 1, core, seg=64, name="ns")
    for k in range(2):
        torus(1.3 + k * 0.5, 0.008, (2.1, 0, -0.7), (80, 25, 0), mat(f"field{k}", "#6fb8ff", rough=1.0, emit="#6fb8ff", emit_strength=1.2 - 0.35 * k))
    # a distant ringed planet and a small moon for scale and colour
    sphere(2.6, (-14, 30, 5), 1, mat("planet", "#d98a4a", rough=0.7), seg=48)
    torus(4.0, 0.25, (-14, 30, 5), (70, 0, 20), mat("ring", "#e8c79a", rough=0.7)).scale = (1, 1, 0.08)
    sphere(0.6, (-7.5, 22, -4), 1, mat("moon", "#8fa0b8", rough=0.8), seg=32)
    d = bpy.data.lights.new("starlight", "SUN"); d.energy = 2.5; d.color = hexrgb("#bfe2ff")
    o = bpy.data.objects.new("starlight", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(60), math.radians(-40), math.radians(-70))
    camera((0, -12, 0.5), (0.6, 0, 0.1), lens=35, fstop=0)
    still("plate_space", W, H, 40)


def alpha_sprite():
    prop_scene(); random.seed(2)
    p = mat("a_proton", "#d9534f", rough=0.25, coat=0.6, emit="#ff6a4a", emit_strength=0.5)
    n = mat("a_neutron", "#9fb4c8", rough=0.25, coat=0.6)
    for (dx, dy, dz), m_ in zip(((0.11, 0, 0.05), (-0.11, 0, -0.05), (0, 0.11, -0.06), (0, -0.09, 0.09)), (p, n, p, n)):
        sphere(0.13, (dx, dy, 0.5 + dz), 1, m_, seg=32)
    sprite_camera((0, 0, 0.5), 2.0, 0.3, 50, azimuth=-15)
    still("alpha", 400, 400, 32, transparent=True, crop=True)


def foil_sprite():
    prop_scene()
    box((0.02, 1.0, 1.0), (0, 0, 0.6), (0, 0, 0), metal("#f0c040", 0.15, "foil_gold"), bevel=0.004)
    torus(0.72, 0.03, (0, 0, 0.6), (0, 90, 0), metal("#c9a24a", 0.28, "brass"))
    cylinder(0.03, 0.6, (0, 0, 0.0), material=metal("#c9a24a", 0.28, "brass"), verts=16)
    camera((-1.8, -2.6, 0.9), (0, 0, 0.55), lens=50, fstop=0)
    still("goldfoil", 600, 700, 32, transparent=True, crop=True)


def ns_sprite():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#000000"), 0.0)
    sphere(1.0, (0, 0, 0), 1, mat("ns_core", "#dff0ff", rough=0.3, emit="#bfe2ff", emit_strength=6.0), seg=64)
    for k in range(2):
        torus(1.45 + k * 0.4, 0.025, (0, 0, 0), (75, 10, 0), mat(f"field{k}", "#6fb8ff", rough=1.0, emit="#6fb8ff", emit_strength=2.0))
    camera((0, -7, 0.3), (0, 0, 0), lens=50, fstop=0)
    still("neutronstar", 700, 700, 24, transparent=True, crop=True)


cafe16()
stadium16()
lab()
space()
alpha_sprite()
foil_sprite()
ns_sprite()
