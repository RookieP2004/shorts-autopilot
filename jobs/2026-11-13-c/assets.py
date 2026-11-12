# 2026-11-13-c: "How could we really reach another star?" (frontier). Sets: a desert plateau at dusk with a big white radio
# dish, a little control hut with a lit window and a field of laser emitters (fictional), 3 angles (dish wide, dish mid,
# laser field looking up with the beams on); deep space (stars + a small red star, far away), 1 angle.
# Cut-outs: a Voyager-style probe, a tiny square light sail with its chip, one laser emitter.
import math, os, random

# checker_mat(), seg(), sunny() ... from earlier jobs; stars() from the space job (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-11-b/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "b_helpers", "exec"), globals())


def dusk_sky(top="#1d2457", mid="#7a4f8a", horizon="#f5a463"):
    w = world_color(hexrgb(horizon), 1.0)
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    coord = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(coord.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    e = ramp.color_ramp.elements
    e[0].color = (*hexrgb(horizon), 1); e[0].position = 0.5
    e[1].color = (*hexrgb(top), 1); e[1].position = 0.72
    m = e.new(0.57); m.color = (*hexrgb(mid), 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    d = bpy.data.lights.new("sun", "SUN"); d.energy = 2.2; d.angle = math.radians(8); d.color = hexrgb("#ffb877")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(78), math.radians(0), math.radians(-62))      # low, from the left


def dusk_stars(n=220, seed=5):
    random.seed(seed)
    sm = mat("star", "#ffffff", emit="#fff6e8", emit_strength=6.0)
    for k in range(n):
        a = random.uniform(-1.2, 1.2); e = random.uniform(0.35, 1.25)
        R = 260
        sphere(random.uniform(0.25, 0.55), (R * math.sin(a) * math.cos(e), R * math.cos(a) * math.cos(e), R * math.sin(e)), 1, sm, seg=6)


def radio_dish(x, y, s=1.0):
    white = mat("dish_white", "#eef1f4", rough=0.35, coat=0.3)
    grey = metal("#9aa3ad", 0.35, "dish_grey")
    cylinder(0.55 * s, 2.2 * s, (x, y, 1.1 * s), material=mat("pedestal", "#d9dee4", rough=0.4), verts=40, bevel=0.03)
    box((1.3 * s, 0.9 * s, 0.5 * s), (x, y, 2.35 * s), material=white, bevel=0.06)
    for sx in (-1, 1):
        box((0.18 * s, 0.6 * s, 1.0 * s), (x + sx * 0.6 * s, y, 2.9 * s), material=white, bevel=0.04)
    # paraboloid dish, tilted up toward the sky (and a little toward camera)
    prof = [(0.0, 0.0)] + [(r * s, (0.11 * r * r) * s) for r in (0.4, 0.9, 1.5, 2.1, 2.6, 2.9)] + [(2.95 * s, 0.98 * s)]
    d = lathe(prof, 64, (x, y, 3.3 * s), white, subdiv=1, name="dish")
    sol = d.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.05 * s
    d.rotation_euler = (math.radians(42), 0, math.radians(-14))
    import mathutils
    R = d.rotation_euler.to_matrix()
    c = mathutils.Vector((x, y, 3.3 * s))
    feed = c + R @ mathutils.Vector((0, 0, 2.3 * s))
    for k in range(3):
        a = k / 3 * 2 * math.pi
        rim = c + R @ mathutils.Vector((2.4 * s * math.cos(a), 2.4 * s * math.sin(a), 0.65 * s))
        seg(tuple(rim), tuple(feed), 0.04 * s, grey)
    f = cylinder(0.2 * s, 0.45 * s, tuple(feed), material=mat("feed", "#f2b04a", rough=0.4), verts=24, bevel=0.02)
    f.rotation_euler = d.rotation_euler


def hut(x, y):
    wall = mat("hut_wall", "#e9dcc4", rough=0.8, noise_bump=0.2)
    box((2.6, 2.0, 1.9), (x, y, 0.95), material=wall, bevel=0.05)
    box((2.9, 2.3, 0.18), (x, y, 1.98), material=mat("hut_roof", "#7c2533", rough=0.6), bevel=0.04)
    box((0.9, 0.06, 0.6), (x - 0.5, y - 1.01, 1.15), material=mat("win", "#ffd27a", emit="#ffcf7a", emit_strength=6.0), bevel=0.01)
    box((0.55, 0.06, 1.2), (x + 0.65, y - 1.01, 0.6), material=mat("door", "#34425c", rough=0.6), bevel=0.02)
    cylinder(0.03, 1.4, (x + 1.0, y + 0.6, 2.7), material=metal("#9aa3ad", 0.3, "mast"), verts=10)
    sphere(0.08, (x + 1.0, y + 0.6, 3.42), 1, mat("beacon", "#ff5a4a", emit="#ff4a3a", emit_strength=10.0), seg=12)


def emitter(x, y, s=1.0, tilt=(0, 0), name="emitter"):
    base = mat("emit_base", "#d9dee4", rough=0.4, coat=0.2)
    dark = mat("emit_dark", "#25262b", rough=0.3, coat=0.5)
    box((0.7 * s, 0.7 * s, 0.35 * s), (x, y, 0.18 * s), material=base, bevel=0.05)
    t = cylinder(0.24 * s, 0.9 * s, (x, y, 0.75 * s), (tilt[0], tilt[1], 0), dark, verts=32, bevel=0.03)
    cylinder(0.2 * s, 0.03 * s, (x + math.sin(math.radians(tilt[1])) * 0.45 * s, y - math.sin(math.radians(tilt[0])) * 0.45 * s, 1.2 * s),
             (tilt[0], tilt[1], 0), mat("lens_glow", "#9fe8ff", emit="#7fe0ff", emit_strength=8.0), verts=32, bevel=0)
    return t


TARGET = (0.0, 60.0, 70.0)       # where all the laser beams meet, high in the sky


def laser_field(beams=False):
    random.seed(4)
    pts = []
    for i in range(-4, 5):
        for j in range(5):
            x = i * 1.25 + (0.4 if j % 2 else 0); y = 11 + j * 1.6
            pts.append((x, y))
    for (x, y) in pts:
        emitter(x, y, 0.8)
    if beams:
        bm = mat("beam", "#3fd0ff", emit="#35c8ff", emit_strength=3.5)
        for (x, y) in pts:
            seg((x, y, 1.0), TARGET, 0.022, bm)


def rocks():
    rm = mat("rock", "#b2765a", rough=0.9, noise_bump=0.5)
    random.seed(8)
    for (x, y, r) in ((-6.5, 2.0, 0.7), (5.8, 1.0, 0.5), (-2.0, -1.0, 0.25), (7.5, 8.0, 1.1), (-8.5, 10, 1.3), (3.0, 3.5, 0.3),
                      (-10, 22, 3.0), (11, 25, 3.5), (0, 40, 5)):
        o = sphere(r, (x, y, r * 0.25), (1.3, 1.0, 0.6), rm, seg=24)
        o.rotation_euler = (0, 0, random.uniform(0, 3))


def build_site(beams=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2)
    dusk_sky()
    dusk_stars()
    ground = mat("sand", "#d39a6a", rough=0.95, noise_bump=0.35)
    plane(160, 160, (0, 30, 0), material=ground, name="ground")
    # far mesas, bluer with distance
    for k, (mx, my, sc) in enumerate(((-30, 70, 9), (-8, 85, 7), (18, 75, 10), (40, 90, 8))):
        box((sc * 2.4, sc, sc * 0.9), (mx, my, sc * 0.45), material=mat(f"mesa{k}", "#8a6f86", rough=1.0), bevel=0.6)
    global DISH_OBJS
    before = set(bpy.data.objects)
    radio_dish(-2.6, 6.5, 0.8)
    DISH_OBJS = [o for o in bpy.data.objects if o not in before]
    hut(3.6, 4.6)
    laser_field(beams)
    rocks()
    # path stones + a little bench by the hut
    for k in range(6):
        cylinder(0.28, 0.04, (1.0 + k * 0.45, 1.0 + k * 0.6, 0.02), material=mat("path", "#e9dcc4", rough=0.9), verts=20)
    area_light((-6, -6, 5), (0, 3, 1), 600, 6, "#ffd2a8", "key")
    area_light((6, -4, 4), (0, 3, 1), 250, 5, "#9fb4ff", "fill")


def site_angles():
    build_site(False)
    drop_cams(); camera((0.4, -8.5, 1.9), (0.0, 6.0, 2.6), lens=22, fstop=8.0)
    still("plate_dish_wide", 1080, 1920, 40)
    drop_cams(); camera((0.9, -4.2, 1.5), (-0.8, 5.0, 2.2), lens=28, fstop=5.0)
    still("plate_dish_mid", 1080, 1920, 40)
    build_site(True)
    for o in DISH_OBJS:
        o.hide_render = True
    drop_cams(); camera((0.3, 4.0, 1.4), (0.0, 30.0, 18.0), lens=20, fstop=8.0)
    still("plate_lasers", 1080, 1920, 40)


def build_deep():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.35)
    world_color(hexrgb("#03050c"), 1.0)
    random.seed(12)
    sm = mat("star_d", "#ffffff", emit="#ffffff", emit_strength=9.0)
    for k in range(520):
        sphere(random.uniform(0.15, 0.5), (random.uniform(-90, 90), 200, random.uniform(-160, 160)), 1, sm, seg=6)
    # a faint band of dust (milky way) across the frame
    # the red dwarf: a small red-orange glowing ball top-right
    sphere(4.5, (24, 190, 58), 1, mat("proxima", "#ff6a3a", emit="#ff4a1a", emit_strength=3.0), seg=32)
    drop_cams(); camera((0, 0, 0), (0, 200, 0), lens=24, fstop=0)
    still("plate_deep", 1080, 1920, 40)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#c9d4e2"), 0.7)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def probe():
    gold = metal("#d9a441", 0.3, "foil")
    white = mat("p_white", "#eef1f4", rough=0.35, coat=0.3)
    grey = metal("#9aa3ad", 0.35, "p_grey")
    cylinder(0.32, 0.22, (0, 0, 0), material=gold, verts=10, bevel=0.01)                      # the bus
    prof = [(0.0, 0.0)] + [(r, 0.16 * r * r) for r in (0.2, 0.45, 0.7, 0.95, 1.1)]
    d = lathe(prof, 64, (0, 0, 0.14), white, subdiv=1, name="hga")
    s = d.modifiers.new("thick", "SOLIDIFY"); s.thickness = 0.02
    seg((0, 0, 0.14), (0, 0, 0.62), 0.02, grey)
    cylinder(0.05, 0.08, (0, 0, 0.64), material=mat("p_feed", "#f2b04a", rough=0.4), verts=16)
    seg((0.25, 0, 0), (2.2, 0, -0.25), 0.015, grey)                                         # magnetometer boom
    seg((-0.25, 0, 0), (-1.0, 0, -0.15), 0.025, grey)                                       # RTG boom
    for k in range(3):
        cylinder(0.08, 0.14, (-0.75 - k * 0.15, 0, -0.12), (0, 90, 0), mat("rtg", "#5a5f66", rough=0.5), verts=16)
    seg((0, 0.2, -0.05), (0, 0.9, -0.3), 0.012, grey)


def sail():
    sm = metal("#e6e9ee", 0.12, "sail_m")
    import bmesh
    me = bpy.data.meshes.new("sail"); bm = bmesh.new(); N = 12; vs = []
    for j in range(N + 1):
        row = []
        for i in range(N + 1):
            x = -1 + 2 * i / N; y = -1 + 2 * j / N
            row.append(bm.verts.new((x, y, 0.12 * (x * x + y * y))))
        vs.append(row)
    for j in range(N):
        for i in range(N):
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new("sail", me); bpy.context.scene.collection.objects.link(o); o.data.materials.append(sm)
    box((0.16, 0.16, 0.03), (0, 0, 0.02), material=metal("#d9a441", 0.3, "chip"), bevel=0.005)
    box((0.1, 0.1, 0.01), (0, 0, 0.04), material=mat("chip_top", "#25262b", rough=0.3), bevel=0.002)


if not os.environ.get("BK_PROPS_ONLY"):
    site_angles()
    build_deep()
prop_scene(); probe(); camera((0.7, -2.6, 2.9), (0.5, 0, 0.1), lens=40, fstop=0)
still("probe", 900, 600, 24, transparent=True, crop=True)
prop_scene(); sail(); camera((0.0, -2.6, 2.6), (0, 0, 0.0), lens=40, fstop=0)
still("sail", 700, 700, 24, transparent=True, crop=True)
prop_scene(); emitter(0, 0, 1.0, (0, 0)); camera((0.6, -2.4, 1.3), (0, 0, 0.6), lens=45, fstop=0)
still("emitter", 500, 700, 24, transparent=True, crop=True)
