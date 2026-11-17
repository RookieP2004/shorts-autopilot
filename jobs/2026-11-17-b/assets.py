# 2026-11-17-b: "Voyager 1 is one light-DAY away. How do we still hear it?" (frontier).
# Sets: a blue-hour desert tracking station (one giant 70 m-style white dish tipped at the sky, two smaller dishes far off,
# a long control building with lit windows, rocks, a path), 3 angles (wide, mid by the building, a low hero looking up the
# dish); deep space with a detailed Voyager-style probe (gold-foil decagon bus, big white high-gain dish, RTG boom, science
# boom with scan platform, long magnetometer boom) and the Sun as a far, bright star, 2 angles (hero close, lonely wide).
# Cut-outs: the probe, a fridge bulb, a plutonium power unit (RTG), a phone (live screen).
import math, os, random

# dusk_sky(), radio_dish(), hut(), seg(), drop_cams(), stars() ... from earlier jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-13-c/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "c13_helpers", "exec"), globals())

DISH = (-2.2, 15.0)          # big dish position (x, y); scale below
DISH_S = 2.3


def control_building(x, y):
    wall = mat("cb_wall", "#ece3d2", rough=0.8, noise_bump=0.15)
    box((5.2, 2.2, 2.4), (x, y, 1.2), material=wall, bevel=0.06)
    box((5.5, 2.5, 0.2), (x, y, 2.5), material=mat("cb_roof", "#34425c", rough=0.6), bevel=0.05)
    win = mat("cb_win", "#ffd27a", emit="#ffc35a", emit_strength=7.0)
    for k in range(4):
        box((0.8, 0.06, 0.7), (x - 1.9 + k * 1.15, y - 1.11, 1.45), material=win, bevel=0.01)
    box((0.7, 0.06, 1.5), (x + 2.2, y - 1.11, 0.75), material=mat("cb_door", "#d9534f", rough=0.5), bevel=0.02)
    cylinder(0.035, 1.8, (x - 2.1, y + 0.6, 3.4), material=metal("#9aa3ad", 0.3, "cb_mast"), verts=10)
    sphere(0.09, (x - 2.1, y + 0.6, 4.33), 1, mat("cb_beacon", "#ff5a4a", emit="#ff4a3a", emit_strength=12.0), seg=12)
    # a little bench and a crate by the door
    w = wood("#9a6a44", "#6b4529", "cb_bench", 4.0, 0.55)
    box((1.3, 0.35, 0.08), (x + 0.7, y - 1.55, 0.45), material=w, bevel=0.015)
    for sx in (-0.55, 0.55):
        box((0.08, 0.3, 0.42), (x + 0.7 + sx, y - 1.55, 0.21), material=w, bevel=0.01)
    box((0.6, 0.6, 0.55), (x - 1.0, y - 1.6, 0.28), material=wood("#b8834f", "#7a4e2a", "cb_crate", 5.0), bevel=0.03)


def build_dsn():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    dusk_sky(top="#101a4a", mid="#3d5a9e", horizon="#f3a46e")
    dusk_stars(260, seed=9)
    plane(200, 200, (0, 40, 0), material=mat("dsand", "#c98f63", rough=0.95, noise_bump=0.35), name="ground")
    for k, (mx, my, sc) in enumerate(((-34, 80, 10), (-10, 95, 7), (16, 85, 11), (42, 100, 9))):
        box((sc * 2.4, sc, sc * 0.9), (mx, my, sc * 0.45), material=mat(f"dmesa{k}", "#6f6a92", rough=1.0), bevel=0.6)
    radio_dish(DISH[0], DISH[1], DISH_S)
    radio_dish(14.0, 40.0, 1.1)
    radio_dish(-17.0, 46.0, 0.9)
    control_building(4.6, 4.2)
    rocks()
    for k in range(7):
        cylinder(0.3, 0.04, (2.2 - k * 0.5, 2.4 + k * 0.9, 0.02), material=mat("dpath", "#ece3d2", rough=0.9), verts=20)
    area_light((-8, -6, 6), (0, 5, 2), 900, 7, "#ffcf9e", "key")
    area_light((7, -5, 4), (0, 5, 2), 380, 6, "#8fb0ff", "fill")


def dsn_angles():
    build_dsn()
    drop_cams(); camera((1.2, -9.0, 1.7), (-0.6, 10.0, 5.2), lens=22, fstop=8.0)
    still("plate_dsn_wide", 1080, 1920, 40)
    drop_cams(); camera((2.2, -3.6, 1.45), (3.4, 6.0, 2.4), lens=28, fstop=4.0)
    still("plate_dsn_mid", 1080, 1920, 40)
    drop_cams(); camera((0.4, 3.0, 0.5), (DISH[0], DISH[1], 9.5), lens=18, fstop=0)
    still("plate_dsn_up", 1080, 1920, 40)


# ------------------------------------------------------------------ the probe
def voyager(name="vgr"):
    """Voyager-style probe at the origin, high-gain dish facing +Z. Returns the objects."""
    before = set(bpy.data.objects)
    gold = mat(name + "_foil", "#d9a441", rough=0.28, metal=1.0, noise_bump=0.25)
    white = mat(name + "_white", "#f1f3f6", rough=0.32, coat=0.3)
    grey = metal("#a7aeb8", 0.35, name + "_grey")
    dark = mat(name + "_dark", "#3a3f48", rough=0.45, metal=0.6)
    cylinder(0.45, 0.42, (0, 0, -0.05), material=gold, verts=10, bevel=0.015)                     # decagon bus
    cylinder(0.2, 0.25, (0, 0, -0.4), material=mat(name + "_tank", "#e9edf2", rough=0.3), verts=24)  # tank
    prof = [(0.0, 0.0)] + [(r, 0.2 * r * r) for r in (0.15, 0.35, 0.55, 0.75, 0.9, 0.95)]
    d = lathe(prof, 72, (0, 0, 0.18), white, subdiv=1, name=name + "_hga")
    s = d.modifiers.new("thick", "SOLIDIFY"); s.thickness = 0.025
    for k in range(4):
        a = k / 4 * 2 * math.pi + 0.4
        seg((0.85 * math.cos(a), 0.85 * math.sin(a), 0.33), (0, 0, 0.78), 0.008, grey)
    cylinder(0.06, 0.12, (0, 0, 0.8), material=mat(name + "_feed", "#f2b04a", rough=0.4), verts=16)
    # RTG boom (3 finned plutonium units)
    seg((-0.42, 0, -0.1), (-1.55, 0, -0.35), 0.03, grey)
    for k in range(3):
        cx = -0.85 - k * 0.27
        cylinder(0.09, 0.22, (cx, 0, -0.2 - k * 0.05), (0, 90, 0), dark, verts=20)
        for f in range(6):
            a = f / 6 * 2 * math.pi
            box((0.2, 0.012, 0.09), (cx, 0.13 * math.cos(a), -0.2 - k * 0.05 + 0.13 * math.sin(a)), (math.degrees(a), 0, 0), dark, bevel=0.003)
    # science boom with the scan platform (two camera barrels)
    seg((0.42, 0.05, -0.1), (1.5, 0.15, -0.3), 0.03, grey)
    box((0.3, 0.25, 0.22), (1.6, 0.15, -0.3), material=dark, bevel=0.02)
    for k, r in enumerate((0.06, 0.045)):
        cylinder(r, 0.32, (1.6 + (k - 0.5) * 0.16, 0.05, -0.12), (0, 0, 0), material=white, verts=20)
    # long magnetometer boom + two whip antennas
    seg((0.0, 0.42, -0.1), (0.5, 3.4, -0.45), 0.012, grey)
    seg((-0.2, -0.35, -0.2), (-1.4, -2.4, -1.0), 0.006, grey)
    seg((0.2, -0.35, -0.2), (1.2, -2.5, -1.1), 0.006, grey)
    return [o for o in bpy.data.objects if o not in before]


SUN_DIR = (0.55, 1.0, 0.25)       # where the Sun (and Earth) are, seen from the probe


def build_space():
    reset(1080, 1920, 30, 0.1, samples=48, bloom=0.45)
    world_color(hexrgb("#02040b"), 1.0)
    random.seed(31)
    sm = mat("vstar", "#ffffff", emit="#ffffff", emit_strength=7.0)
    sm2 = mat("vstar2", "#cfe0ff", emit="#cfe0ff", emit_strength=3.0)
    for k in range(int(os.environ.get('NSTAR', 900))):
        a = random.uniform(0, 2 * math.pi); b = random.uniform(-1.4, 1.4); R = 420
        sphere(random.uniform(0.25, 0.8), (R * math.cos(a) * math.cos(b), R * math.sin(a) * math.cos(b), R * math.sin(b)), 1,
               sm if k % 3 else sm2, seg=6)
    # a faint milky band
    mb = mat("band", "#9fb4ff", emit="#9fb4ff", emit_strength=1.2)
    for k in range(int(os.environ.get('NBAND', 700))):
        t = random.uniform(-1, 1); a = 2.2 + t * 1.6; b = 0.35 * t + random.gauss(0, 0.08); R = 410
        sphere(random.uniform(0.2, 0.5), (R * math.cos(a) * math.cos(b), R * math.sin(a) * math.cos(b), R * math.sin(b)), 1, mb, seg=5)
    import mathutils
    sd = mathutils.Vector(SUN_DIR).normalized()
    sphere(6.5, tuple(sd * 400), 1, mat("vsun", "#fff6e0", emit="#fff2d6", emit_strength=40.0), seg=24, name="sun_ball")
    sphere(1.3, tuple(sd * 400 + mathutils.Vector((16, 0, 7))), 1, mat("vearth", "#7fc0ff", emit="#6fb2ff", emit_strength=12.0),
           seg=12, name="earth_dot")
    objs = voyager()
    g = group([o for o in objs if o.parent is None], "probe")
    # dish faces the Sun/Earth
    g.rotation_euler = sd.to_track_quat("Z", "Y").to_euler()
    d = bpy.data.lights.new("sun", "SUN"); d.energy = 3.2; d.angle = math.radians(0.6); d.color = hexrgb("#fff1dc")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (-sd).to_track_quat("-Z", "Y").to_euler()
    o.rotation_euler = sd.to_track_quat("Z", "Y").to_euler()
    area_light((-4, -3, -2), (0, 0, 0), 120, 4, "#6f8fff", "cool_fill")
    return sd


def space_angles():
    sd = build_space()
    import mathutils
    perp = sd.cross(mathutils.Vector((0, 0, 1))).normalized()
    area_light(tuple(sd * 6 + perp * 3 + mathutils.Vector((0, 0, 2))), (0, 0, 0), 600, 4, "#ffe6c4", "front_key")
    # hero: from the side, a little toward the Sun, so the dish face and gold bus catch the light
    c = perp * -4.2 + sd * 2.4 + mathutils.Vector((0, 0, 1.1))
    drop_cams(); camera(tuple(c), tuple(sd * 0.35 + mathutils.Vector((0, 0, -0.1))), lens=30, fstop=0)
    still("plate_space_hero", 1080, 1920, 48)
    # lonely wide: from far behind, looking toward the Sun-star; the probe small and low in frame
    c = sd * -22 + perp * 3.0 + mathutils.Vector((0, 0, 6.5))
    drop_cams(); camera(tuple(c), tuple(c + sd * 10), lens=26, fstop=0)
    still("plate_space_wide", 1080, 1920, 48)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#0a0d18"), 0.3)
    area_light((-3, -3, 3), (0, 0, 0.3), 700, 2.5, "#fff1dc", "key"); area_light((3, 2.5, 1.5), (0, 0, 0.3), 260, 2, "#8fb9ff", "rim")
    area_light((0.5, -4, 0.5), (0, 0, 0.3), 160, 4, "#ffffff", "fill")


def bulb():
    g = mat("bulb_glass", "#fff1c4", rough=0.08, emit="#ffd98a", emit_strength=4.0, transmission=0.3)
    prof = [(0.0, 0.0), (0.12, 0.01), (0.16, 0.05), (0.15, 0.12), (0.24, 0.3), (0.33, 0.48), (0.35, 0.6), (0.31, 0.74),
            (0.2, 0.84), (0.0, 0.88)]
    lathe(prof, 64, (0, 0, 0.3), g, subdiv=1, name="bulb")
    sm = metal("#c9ccd2", 0.3, "screw")
    for k in range(5):
        torus(0.115, 0.025, (0, 0, 0.08 + k * 0.05), material=sm)
    cylinder(0.11, 0.26, (0, 0, 0.17), material=sm, verts=32)
    cylinder(0.05, 0.05, (0, 0, 0.02), material=mat("tip", "#2b2f36", rough=0.4), verts=24)


def rtg():
    dark = mat("rtg_d", "#4a505a", rough=0.4, metal=0.7)
    cylinder(0.32, 1.1, (0, 0, 0.55), material=dark, verts=40, bevel=0.02)
    for f in range(8):
        a = f / 8 * 2 * math.pi
        box((0.38, 0.03, 0.95), (0.42 * math.cos(a), 0.42 * math.sin(a), 0.55), (0, 0, math.degrees(a)), dark, bevel=0.008)
    for z in (0.05, 1.05):
        cylinder(0.36, 0.08, (0, 0, z), material=metal("#9aa3ad", 0.3, "rtg_cap"), verts=40, bevel=0.01)
    torus(0.33, 0.03, (0, 0, 0.55), material=mat("rtg_glow", "#ff8a3a", emit="#ff6a1a", emit_strength=3.0))


if not os.environ.get("BK_PROPS_ONLY"):
    dsn_angles()
    space_angles()
prop_scene(1000, 800); objs = voyager("vp")
camera((-2.2, -3.4, 2.6), (0.0, 0.0, 0.05), lens=38, fstop=0)
still("probe", 1000, 800, 32, transparent=True, crop=True)
prop_scene(500, 800); bulb(); camera((0.0, -2.6, 0.9), (0, 0, 0.5), lens=50, fstop=0)
still("bulb", 500, 800, 32, transparent=True, crop=True)
prop_scene(600, 800); rtg(); camera((0.8, -3.0, 1.6), (0, 0, 0.55), lens=50, fstop=0)
still("rtg", 600, 800, 32, transparent=True, crop=True)
reset(1080, 1920, samples=40, bloom=0.2, exposure=0.2)
world_color(hexrgb("#1a2238"), 0.3)
area_light((-2.5, -3.0, 2.5), (0, 0, 0), 700, 2.5, "#fff1dc", "key")
area_light((2.5, 2.5, 1.5), (0, 0, 0), 500, 2.0, "#6fc3ff", "rim")
area_light((0.5, -4, 1), (0, 0, 0), 300, 6.0, "#ffffff", "fill")
body, scr = phone((0, 0, 0), (0, 0, 0), w=0.8)
camera((0, -3.4, 0.1), (0, 0, 0), lens=60, fstop=0)
phone_sprite("phone", scr, samples=40)
