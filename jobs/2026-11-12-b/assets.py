# 2026-11-12-b: "Why do we get goosebumps?" (big-question). Sets: a snowy winter town square (snow-white cobbles, houses with
# snowy roofs, frosted trees, a snowman, lamps, a cocoa stall whose counter is a foreground layer), wide + medium; a giant
# cut-away skin block on a plinth in a cool studio (epidermis, dermis, fat, one big hair follicle with its hair, the red
# arrector pili muscle and a yellow nerve), the same camera in two states (relaxed: hair lying flat; cold: muscle squeezed,
# hair upright, a bump on the surface); a macro "skin landscape" with tree-sized hairs, relaxed and goosebumped.
# Cut-outs: cocoa mug, thermometer, headphones.
import math, os, random

# tree(), bush(), house(), bench(), seg(), checker_mat() + sunny(), stall(), bunting(), crate(), barrel() (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\ndef cake")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


SNOW = "#dde7f0"


def snowy_house(x, y, w, h, col):
    house(x, y, w, h, col, "#f4f7fb")


def snowy_tree(x, y, h=3.4, r=1.2, seed=1):
    tree(x, y, h, r, seed, "#e3ecf2")


def pine(x, y, h=3.2, seed=0):
    cylinder(0.12, h * 0.3, (x, y, h * 0.15), material=wood("#7a5236", "#553826", "pine_bark", 2.0), verts=12)
    g = mat("pine", "#2f6b4a", rough=0.75)
    s = mat("pine_snow", SNOW, rough=0.9)
    for k in range(3):
        z = h * (0.25 + k * 0.22); r = h * (0.32 - k * 0.08)
        cone(r, h * 0.36, (x, y, z + h * 0.18), material=g)
        cone(r * 0.72, h * 0.2, (x, y, z + h * 0.3), material=s)


def snowman(x, y):
    s = mat("snowman", "#f7fafc", rough=0.8, sss=0.1)
    sphere(0.5, (x, y, 0.45), 1, s); sphere(0.36, (x, y, 1.12), 1, s); sphere(0.25, (x, y, 1.6), 1, s)
    cone(0.05, 0.3, (x, y - 0.35, 1.62), (90, 0, 0), mat("carrot", "#f08a24", rough=0.5))
    coal = mat("coal", "#1a1410", rough=0.5)
    for dx in (-0.09, 0.09):
        sphere(0.035, (x + dx, y - 0.21, 1.7), 1, coal, seg=12)
    for k in range(3):
        sphere(0.04, (x, y - 0.35, 1.0 + k * 0.14), 1, coal, seg=12)
    torus(0.27, 0.06, (x, y, 1.4), material=mat("scarf_sm", "#d9534f", rough=0.7))
    cylinder(0.2, 0.26, (x, y, 1.92), material=mat("hat_sm", "#34425c", rough=0.6), verts=24)
    cylinder(0.3, 0.03, (x, y, 1.8), material=mat("hat_sm", "#34425c", rough=0.6), verts=24)


def lamp(x, y):
    cylinder(0.05, 3.4, (x, y, 1.7), material=metal("#3b3f46", 0.4, "lamp"), verts=12)
    sphere(0.18, (x, y, 3.45), 1, mat("globe", "#f6efe2", rough=0.2, emit="#ffd9a0", emit_strength=4.0))


def mug(loc=(0, 0, 0), s=1.0, name="mug"):
    x, y, z = loc
    body = lathe([(0.0, 0.0), (0.16 * s, 0.0), (0.18 * s, 0.03 * s), (0.18 * s, 0.32 * s), (0.165 * s, 0.32 * s),
                  (0.165 * s, 0.04 * s), (0.0, 0.04 * s)], 40, (x, y, z), mat("mug", "#d9534f", rough=0.3, coat=0.5), 1, name)
    cylinder(0.163 * s, 0.01, (x, y, z + 0.28 * s), material=mat("cocoa", "#6b3a1e", rough=0.25, coat=0.4), verts=40, bevel=0)
    torus(0.08 * s, 0.022 * s, (x + 0.2 * s, y, z + 0.17 * s), (90, 0, 0), mat("mug", "#d9534f", rough=0.3, coat=0.5))
    m = mat("marsh", "#fff8ee", rough=0.7)
    for k, (dx, dy) in enumerate(((-0.05, 0.02), (0.05, -0.03), (0.0, 0.06))):
        box((0.06 * s, 0.06 * s, 0.05 * s), (x + dx * s, y + dy * s, z + 0.3 * s), (0, 0, k * 25), m, bevel=0.012 * s)
    return body


def build_square():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny("#4f8fd6", "#cfe2f2", sun=2.2)
    sun = bpy.data.objects.get("sun"); sun.data.color = hexrgb("#ffe6c8")
    sun.rotation_euler = (math.radians(58), math.radians(-8), math.radians(-46))
    plane(300, 300, (0, 0, 0), material=mat("snow", SNOW, rough=0.85, sss=0.05, noise_bump=0.25), name="snow")
    counter = stall(-2.3, 1.2, "awning_stripes.png", "COCOA", 0.85)
    for k, dx in enumerate((-0.7, -0.25, 0.2, 0.65)):
        mug((-2.3 + dx, 1.05 + (k % 2) * 0.12, 0.81), 0.7, f"disp_mug{k}")
    snowman(2.3, 1.4)
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#c9b7e3", "#9fd39a", "#e3c99a", "#f6efe2"]
    for k in range(9):
        snowy_house(-12 + k * 3.0, 9.5 + (k % 2) * 0.8, 2.7, 4 + (k * 53 % 4), cols[k % 7])
    bunting(-4.2, 4.2, 4.0, 4.4)
    snowy_tree(-5.4, 4.5, 4.0, 1.4, 7); pine(5.4, 4.6, 4.4); pine(-3.6, 6.4, 3.6); snowy_tree(0.6, 7.0, 3.6, 1.3, 9)
    pine(4.0, 7.5, 3.4)
    bench(0.2, 3.4)
    box((1.8, 0.5, 0.06), (0.2, 3.4, 0.5), material=mat("bench_snow", SNOW, rough=0.9), bevel=0.03)
    random.seed(11)
    sm = mat("snow_drift", SNOW, rough=0.9)
    for k in range(14):                                # soft snow drifts
        sphere(random.uniform(0.3, 0.7), (random.uniform(-6, 6), random.uniform(2.5, 8), 0), (1.6, 1.0, 0.35), sm, seg=24)
    for x in (-3.9, 3.9):
        lamp(x, 2.0)
    lamp(0.0, 5.0)
    return counter


def square_angles():
    counter = build_square()
    for name, loc, tgt, lens in (("square_wide", (0.2, -9.6, 2.4), (0, 1.6, 1.7), 26),
                                 ("cocoa_mid", (-1.4, -3.9, 1.6), (-2.15, 1.2, 1.25), 30)):
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=0)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=counter)


# ---------------------------------------------------------------- the cut-away skin block
Z0 = 0.18
EPI_TOP = Z0 + 1.34


def skin_block(state):
    """state 'relaxed' (hair lying flat) or 'cold' (muscle squeezed, hair up, goosebump)."""
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.1)
    world_color(hexrgb("#1f3340"), 0.7)
    floor("#27404c", 0.5)
    box((3.8, 2.1, 0.18), (0, 0, 0.09), material=mat("plinth", "#34425c", rough=0.4, coat=0.3), bevel=0.04)
    W, D = 3.2, 1.6
    fat = mat("fat", "#f2d48a", rough=0.5, sss=0.2)
    derm = mat("dermis", "#eaa7a0", rough=0.5, sss=0.25)
    epi = mat("epidermis", "#dba07e", rough=0.45, sss=0.2, coat=0.2)
    box((W, D, 0.5), (0, 0, Z0 + 0.25), material=fat, bevel=0.01)
    box((W, D, 0.7), (0, 0, Z0 + 0.5 + 0.35), material=derm, bevel=0.01)
    box((W, D, 0.14), (0, 0, Z0 + 1.2 + 0.07), material=epi, bevel=0.03)
    random.seed(5)
    fm = mat("fat_lob", "#f6dd9a", rough=0.45, sss=0.2)
    for k in range(26):
        sphere(random.uniform(0.07, 0.11), (random.uniform(-W / 2 + 0.12, W / 2 - 0.12), -D / 2 + 0.01, Z0 + random.uniform(0.08, 0.44)),
               (1, 0.35, 1), fm, seg=20)
    cold = state == "cold"
    # follicle + hair rotate about the point where the hair leaves the skin
    P = (-0.15, -D / 2 - 0.02, EPI_TOP)
    a = math.radians(8 if cold else 42)            # tilt from vertical (hair leans to +x)
    ux, uz = math.sin(a), math.cos(a)               # unit vector along the hair (outwards)
    fol = mat("follicle", "#b55a64", rough=0.45, sss=0.2)
    bulb_c = (P[0] - ux * 0.95, P[1], P[2] - uz * 0.95)
    seg((P[0] - ux * 0.1, P[1], P[2] - uz * 0.1), (bulb_c[0] + ux * 0.12, P[1], bulb_c[2] + uz * 0.12), 0.085, fol)
    sphere(0.13, bulb_c, (1, 0.6, 1), fol, seg=32)                                   # the bulb
    hair = mat("hair", "#3b2716", rough=0.45, coat=0.3)
    seg((bulb_c[0] + ux * 0.05, P[1] - 0.02, bulb_c[2] + uz * 0.05), (P[0] + ux * 1.05, P[1] - 0.02, P[2] + uz * 1.05), 0.032, hair)
    # sebaceous gland (little yellow lobes) on the follicle
    gl = mat("gland", "#f2c95a", rough=0.4, sss=0.2)
    gx, gz = P[0] - ux * 0.35 - uz * 0.11, P[2] - uz * 0.35 + ux * 0.11
    sphere(0.07, (gx, P[1], gz), (1, 0.5, 1), gl, seg=20); sphere(0.055, (gx - 0.06, P[1], gz - 0.06), (1, 0.5, 1), gl, seg=20)
    # arrector pili: from the follicle (below the gland, on the side the hair leans to) up to the base of the epidermis
    mid = (P[0] - ux * 0.55, P[1], P[2] - uz * 0.55)
    anchor = (P[0] + (0.42 if cold else 0.62), P[1], Z0 + 1.2)
    mus = mat("muscle", "#c8303a", rough=0.4, sss=0.15, coat=0.2)
    import mathutils
    A, B = mathutils.Vector(mid), mathutils.Vector(anchor)
    L = (B - A).length
    m = sphere(0.5, tuple((A + B) / 2), (L * 1.04, 0.2, 0.13 if not cold else 0.22), mus, seg=32)
    m.rotation_euler = (0, -math.atan2(B.z - A.z, B.x - A.x), 0)
    # muscle stripes
    for k in range(4):
        t = 0.2 + k * 0.2
        c = A + (B - A) * t
        sphere(0.5, (c.x, c.y - 0.05, c.z), (0.02, 0.06, 0.1 if not cold else 0.17), mat("mus_line", "#9e1f2a", rough=0.4), seg=12).rotation_euler = m.rotation_euler
    # the nerve: a yellow fibre from the left that ends on the muscle
    nv = mat("nerve", "#f2d23c", rough=0.35, emit="#ffd84a", emit_strength=0.6 if cold else 0.15)
    pts = [(-W / 2, P[1], Z0 + 0.62), (-0.9, P[1], Z0 + 0.66), (-0.4, P[1], Z0 + 0.76), (0.15, P[1], Z0 + 0.84),
           ((A.x + B.x) / 2, P[1], (A.z + B.z) / 2 - 0.04)]
    for p0, p1 in zip(pts, pts[1:]):
        seg(p0, p1, 0.025, nv)
    # the epidermis surface: a goosebump when cold
    if cold:
        sphere(0.36, (P[0] + 0.03, -D / 2 + 0.36, EPI_TOP - 0.02), (1, 1.0, 0.24), epi, seg=40)
        sphere(0.36, (P[0] + 0.03, -D / 2 - 0.005, EPI_TOP - 0.02), (1, 0.2, 0.24), epi, seg=40)
    # little hairs on top (relaxed: lying flat; cold: standing, with small bumps)
    random.seed(9)
    for k in range(14):
        hx = random.uniform(-W / 2 + 0.15, W / 2 - 0.15); hy = random.uniform(-D / 2 + 0.3, D / 2 - 0.1)
        tilt = random.uniform(5, 15) if cold else random.uniform(55, 70)
        if cold:
            sphere(0.12, (hx, hy, EPI_TOP - 0.01), (1, 1, 0.3), epi, seg=20)
        L2 = 0.32
        seg((hx, hy, EPI_TOP + 0.02), (hx + math.sin(math.radians(tilt)) * L2, hy, EPI_TOP + 0.02 + math.cos(math.radians(tilt)) * L2),
            0.012, hair)
    area_light((-3.5, -4, 4.5), (0, 0, 0.9), 1500, 3.5, "#ffe2c2", "key")
    area_light((3.5, 4, 3), (0, 0, 0.9), 700, 2.5, "#8fd3ff", "rim")
    area_light((4, -3, 1.5), (0, 0, 0.9), 260, 4, "#9fb4c8", "fill")


def skin_angles():
    for state in ("relaxed", "cold"):
        skin_block(state)
        drop_cams(); camera((0.0, -4.3, 1.55), (0.0, 0, 1.15), lens=32, fstop=6.0)
        still(f"plate_skin_{state}", 1080, 1920, 40)
    # a wide of the cold block for Ved to stand next to
    drop_cams(); camera((0.9, -6.6, 1.7), (0.5, 0, 1.0), lens=26, fstop=7.0)
    still("plate_skin_wide", 1080, 1920, 36)


# ---------------------------------------------------------------- macro skin landscape
def macro(state):
    reset(1080, 1920, 30, 0.1, samples=36, bloom=0.1)
    sunny("#e7a98f", "#f6d2bf", sun=2.6)
    cold = state == "cold"
    skin = mat("macro_skin", "#e2a689", rough=0.55, sss=0.25, noise_bump=0.35)
    plane(200, 200, (0, 0, 0), material=skin, name="skin")
    hair = mat("macro_hair", "#3b2716", rough=0.4, coat=0.4)
    random.seed(21)
    for k in range(70):
        x = random.uniform(-7, 7); y = random.uniform(-1, 26)
        if abs(x) < 0.6 and y < 1.5:
            continue
        L = random.uniform(1.6, 2.4)
        tilt = random.uniform(4, 14) if cold else random.uniform(58, 70)
        az = math.radians(random.uniform(-25, 25))
        if cold:
            sphere(0.62, (x, y, -0.05), (1, 1, 0.42), skin, seg=32)
        base_z = 0.2 if cold else 0.0
        tx = math.sin(math.radians(tilt))
        seg((x, y, base_z), (x + tx * L * math.cos(az), y + tx * L * math.sin(az), base_z + math.cos(math.radians(tilt)) * L), 0.06, hair)
    # skin creases
    cr = mat("crease", "#c98a70", rough=0.6)
    for k in range(10):
        box((random.uniform(2, 5), 0.06, 0.02), (random.uniform(-6, 6), random.uniform(1, 20), 0.005), (0, 0, random.uniform(-30, 30)), cr, bevel=0)
    drop_cams(); camera((0.0, -3.2, 1.25), (0.0, 6, 0.9), lens=24, fstop=3.0, focus=6.0)
    still(f"plate_macro_{state}", 1080, 1920, 36)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#e6eef4"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def thermometer():
    gl = mat("thermo_glass", "#eef6ff", rough=0.15, coat=0.8)
    cylinder(0.07, 1.1, (0, 0, 0.75), material=gl, verts=32, bevel=0.02)
    sphere(0.13, (0, 0, 0.16), 1, mat("thermo_bulb", "#4a8fe0", rough=0.2, coat=0.6), seg=32)
    cylinder(0.035, 0.32, (0, -0.06, 0.38), material=mat("thermo_liquid", "#4a8fe0", rough=0.2, coat=0.6), verts=16, bevel=0)
    box((0.22, 0.04, 1.2), (0, 0.06, 0.72), material=mat("thermo_back", "#f6efe2", rough=0.5), bevel=0.03)
    ink = mat("thermo_ink", "#1a1410", rough=0.5)
    for k in range(9):
        box((0.06 if k % 2 else 0.1, 0.01, 0.012), (-0.1, 0.035, 0.36 + k * 0.1), material=ink, bevel=0)


def headphones():
    band = mat("hp_band", "#34425c", rough=0.35, coat=0.4)
    cup = mat("hp_cup", "#f2b04a", rough=0.3, coat=0.5)
    pad = mat("hp_pad", "#1a1410", rough=0.7)
    arc = [(math.cos(math.radians(d)) * 0.44, 0, 0.42 + math.sin(math.radians(d)) * 0.5) for d in range(0, 181, 5)]
    for p0, p1 in zip(arc, arc[1:]):
        seg(p0, p1, 0.045, band)
    for sx in (-1, 1):
        cylinder(0.16, 0.12, (sx * 0.47, 0, 0.36), (0, 90, 0), cup, verts=40, bevel=0.03)
        cylinder(0.14, 0.05, (sx * 0.39, 0, 0.36), (0, 90, 0), pad, verts=40, bevel=0.02)


square_angles()
skin_angles()
macro("relaxed"); macro("cold")
prop_scene(); mug((0, 0, 0), 1.6, "hero_mug"); sprite_camera((0.05, 0, 0.28), 2.6, 1.0, 50, azimuth=-12)
still("mug", 700, 700, 28, transparent=True, crop=True)
prop_scene(); thermometer(); sprite_camera((0, 0, 0.7), 3.4, 0.7, 50, azimuth=-10)
still("thermo", 400, 900, 24, transparent=True, crop=True)
prop_scene(); headphones(); sprite_camera((0, 0, 0.5), 3.2, 0.6, 50, azimuth=-14)
still("headphones", 700, 600, 28, transparent=True, crop=True)
