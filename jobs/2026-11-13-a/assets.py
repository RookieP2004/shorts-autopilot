# 2026-11-13-a: "Shooting stars are just sand" (myth-bust). Set: a grassy hilltop at night (deep-blue sky full of stars,
# a teal glow on the horizon), a picnic blanket with a basket and two warm lanterns, a brass telescope on a tripod, round
# trees, a little town with lit windows in the valley and far hills bluer with distance; 3 angles (wide, mid, looking up
# at the sky over the tree tops). Cut-outs: a single sand grain (cool, and glowing white-hot), a comet nucleus, the telescope.
import math, os, random

# dusk_sky(), seg(), tree(), bush(), house(), checker_mat(), picnic_basket(), drop_cams() ... (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-13-c/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "c13_helpers", "exec"), globals())


def night_sky():
    dusk_sky(top="#0c1440", mid="#1f2c6a", horizon="#2f6f84")
    nt = bpy.context.scene.world.node_tree
    for n in nt.nodes:
        if n.type == "VALTORGB":
            e = n.color_ramp.elements
            e[0].position = 0.5; e[1].position = 0.535; e[-1].position = 0.6
    # cool moonlight instead of the warm dusk sun
    for o in [o for o in bpy.data.objects if o.type == "LIGHT" and o.name.startswith("sun")]:
        o.data.color = hexrgb("#a9c4ff"); o.data.energy = 1.6
        o.rotation_euler = (math.radians(55), 0, math.radians(-40))


def night_stars(n=420, seed=9):
    random.seed(seed)
    sm = mat("nstar", "#ffffff", emit="#fff6e8", emit_strength=9.0)
    for k in range(n):
        a = random.uniform(-1.3, 1.3); e = random.uniform(0.12, 1.45)
        R = 260
        sphere(random.uniform(0.22, 0.6), (R * math.sin(a) * math.cos(e), R * math.cos(a) * math.cos(e), R * math.sin(e)), 1, sm, seg=6)


def lantern(x, y, s=1.0):
    frame = metal("#2b2f36", 0.4, "lantern_frame")
    box((0.22 * s, 0.22 * s, 0.04 * s), (x, y, 0.02 * s), material=frame, bevel=0.01)
    box((0.24 * s, 0.24 * s, 0.04 * s), (x, y, 0.34 * s), material=frame, bevel=0.01)
    box((0.17 * s, 0.17 * s, 0.28 * s), (x, y, 0.18 * s), material=mat("lantern_glow", "#ffd27a", emit="#ffb64a", emit_strength=14.0), bevel=0.02)
    torus(0.07 * s, 0.012 * s, (x, y, 0.42 * s), (90, 0, 0), frame)
    L = bpy.data.lights.new("lan", "POINT"); L.energy = 70 * s; L.color = hexrgb("#ffb35a"); L.shadow_soft_size = 0.2
    o = bpy.data.objects.new("lan", L); bpy.context.scene.collection.objects.link(o); o.location = (x, y, 0.5 * s)


def telescope(x, y, s=1.0):
    brass = metal("#d9a441", 0.28, "brass")
    dark = mat("scope_dark", "#25262b", rough=0.35, coat=0.4)
    legw = wood("#8a6142", "#5e3f2a", "tripod", 3.0, 0.6)
    top = (x, y, 1.15 * s)
    for k in range(3):
        a = k / 3 * 2 * math.pi + 0.4
        seg((x + 0.45 * s * math.cos(a), y + 0.45 * s * math.sin(a), 0.0), top, 0.025 * s, legw)
    t = cylinder(0.075 * s, 1.0 * s, (x, y, 1.32 * s), (0, -52, 25), brass, verts=32, bevel=0.01)
    import mathutils
    R = t.rotation_euler.to_matrix()
    end = mathutils.Vector((x, y, 1.32 * s)) + R @ mathutils.Vector((0, 0, 0.52 * s))
    cylinder(0.095 * s, 0.14 * s, tuple(end), t.rotation_euler[:], dark, verts=32, bevel=0.01).rotation_euler = t.rotation_euler
    back = mathutils.Vector((x, y, 1.32 * s)) + R @ mathutils.Vector((0, 0, -0.52 * s))
    cylinder(0.035 * s, 0.14 * s, tuple(back), (0, 0, 0), dark, verts=16).rotation_euler = t.rotation_euler


def build_hill():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.25)
    night_sky()
    night_stars()
    grass = mat("ngrass", "#4f8a55", rough=0.9, noise_bump=0.35)
    # the hilltop: a broad gentle dome, the valley falls away behind it
    plane(400, 400, (0, 60, 0), material=grass, name="meadow")
    blanket = plane(2.4, 1.8, (0.4, 0.4, 0.03), (0, 0, -6), checker_mat("ngingham", "#e8857c", "#f6efe2", 7.0), "blanket")
    fg = [blanket] + picnic_basket(-0.4, 0.75)
    lantern(1.35, 0.05); lantern(-0.65, -0.2, 0.85)
    telescope(-2.0, 1.4)
    for (tx, ty, h, r, sd, c) in ((-5.0, 5.5, 4.2, 1.5, 11, "#2f6b45"), (5.2, 6.5, 4.6, 1.6, 12, "#2c6340"),
                                  (-8.5, 10, 5.0, 1.8, 13, "#2a5d3e"), (8.8, 12, 4.8, 1.7, 14, "#2f6b45")):
        tree(tx, ty, h, r, sd, c)
    bush(3.2, -0.8, 0.45, "#2f6b45", "#f6efe2", 21)
    bush(-3.6, -0.4, 0.5, "#2c6340", "#f2b04a", 22)
    # the little town in the valley with lit windows
    cols = ["#c9b7e3", "#8fb9c9", "#e8a598", "#d9c99a"]
    win = mat("townwin", "#ffd27a", emit="#ffc35a", emit_strength=9.0)
    random.seed(3)
    for k in range(10):
        hx = -16 + k * 3.4 + random.uniform(-0.6, 0.6); hy = 26 + (k % 3) * 2.5
        house(hx, hy, 2.2, 2.6 + (k * 37 % 3) * 0.5, cols[k % 4], ["#7c2533", "#34425c", "#5a3a4a"][k % 3])
        for w in range(2):
            box((0.4, 0.05, 0.45), (hx - 0.5 + w * 1.0, hy - 1.13, 1.2), material=win, bevel=0.01)
    for k, (mx, my, sc) in enumerate(((-36, 90, 12), (-10, 100, 9), (20, 95, 13), (46, 105, 10))):
        sphere(1.0, (mx, my, -2), (sc * 2.2, sc, sc), mat(f"nhill{k}", "#3a4f7a", rough=1.0), seg=48)
    area_light((-7, -6, 7), (0, 2, 1), 520, 7, "#b8ccff", "moonkey")
    area_light((6, -5, 3), (0, 2, 1), 160, 5, "#ffcf9a", "warmfill")
    drop_cams()
    return fg


def hill_angles():
    fg = build_hill()
    camera((0.4, -7.6, 1.7), (0.0, 4.0, 3.0), lens=24, fstop=8.0)
    still("plate_hill_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.3, -4.4, 1.45), (-0.2, 1.0, 1.4), lens=30, fstop=4.5)
    still("plate_hill_mid", 1080, 1920, 40)
    still("fg_hill_mid", 1080, 1920, 24, only=fg)
    drop_cams(); camera((0.0, -3.0, 1.0), (0.0, 30.0, 34.0), lens=18, fstop=0)
    still("plate_hill_up", 1080, 1920, 40)


def prop_scene(bg="#c9d4e2"):
    reset(800, 800, 30, 0.1, samples=24, bloom=0.2)
    world_color(hexrgb(bg), 0.7)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def lump(r, loc, material, seed=1, amount=0.25, scale=(1.25, 1.0, 0.85)):
    o = sphere(r, loc, scale, material, seg=64)
    tex = bpy.data.textures.new(f"lump{seed}", "CLOUDS"); tex.noise_scale = 0.55 * r; tex.noise_depth = 2
    d = o.modifiers.new("disp", "DISPLACE"); d.texture = tex; d.strength = amount * r; d.mid_level = 0.5
    random.seed(seed)
    o.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3))
    return o


def grain(hot=False):
    if hot:
        m = mat("grain_hot", "#ffb35a", emit="#ff8a2a", emit_strength=5.0)
    else:
        m = mat("grain", "#d9b98a", rough=0.35, sss=0.2, transmission=0.15, coat=0.4, noise_bump=0.4)
    lump(0.5, (0, 0, 0.5), m, seed=5, amount=0.35)


def comet():
    m = mat("comet_rock", "#5b5560", rough=0.85, noise_bump=0.7)
    lump(0.6, (0, 0, 0.6), m, seed=8, amount=0.45, scale=(1.5, 0.9, 0.8))


if not os.environ.get("BK_PROPS_ONLY"):
    hill_angles()
prop_scene(); grain(False); camera((0.0, -3.2, 1.4), (0, 0, 0.5), lens=55, fstop=0)
still("grain", 600, 600, 32, transparent=True, crop=True)
prop_scene("#30304a"); grain(True); camera((0.0, -3.2, 1.4), (0, 0, 0.5), lens=55, fstop=0)
still("grain_hot", 600, 600, 32, transparent=True, crop=True)
prop_scene(); comet(); camera((0.4, -3.6, 1.8), (0, 0, 0.6), lens=50, fstop=0)
still("comet", 700, 600, 28, transparent=True, crop=True)
prop_scene(); telescope(0, 0, 1.0); camera((1.2, -3.6, 1.4), (0, 0, 0.9), lens=45, fstop=0)
still("telescope", 600, 800, 24, transparent=True, crop=True)
