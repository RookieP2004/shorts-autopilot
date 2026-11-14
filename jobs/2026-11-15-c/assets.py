# 2026-11-15-c: "Mars and Jupiter aren't touching" (myth-bust). Sets: a grassy ridge before sunrise (deep-indigo sky that
# warms to peach in the east, bright cream Jupiter with orange Mars just to its upper left and Regulus below, a wooden bench,
# a brass telescope, round trees, a sleeping town in the valley), 3 angles (wide, mid, a long-lens look at the planet pair
# over the tree tops); deep space with Earth, Mars and Jupiter on one line of sight, 2 angles (from behind Earth, where the
# two planets overlap, and from the side, where the real gap shows). Cut-outs: Jupiter, Mars.
import math, os, random

# night hill helpers (tree, house, lantern, telescope, seg, drop_cams, earth_mat, stars ...) from earlier jobs (frozen)
_src = open(os.path.join(ROOT, "jobs/2026-11-13-a/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "a13_helpers", "exec"), globals())


def predawn_sky():
    dusk_sky(top="#0d1546", mid="#3a3478", horizon="#e98a68")
    nt = bpy.context.scene.world.node_tree
    for n in nt.nodes:
        if n.type == "VALTORGB":
            e = n.color_ramp.elements
            e[0].position = 0.01; e[1].position = 0.1; e[-1].position = 0.26
    for o in [o for o in bpy.data.objects if o.type == "LIGHT" and o.name.startswith("sun")]:
        o.data.color = hexrgb("#b9c6ff"); o.data.energy = 1.5
        o.rotation_euler = (math.radians(60), 0, math.radians(-35))


def jupiter_mat(name="jup"):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.6
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = 1.6; wv.inputs["Distortion"].default_value = 3.0; wv.inputs["Detail"].default_value = 3.0
    nt.links.new(tc.outputs["Generated"], wv.inputs["Vector"])
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].color = (*hexrgb("#b9825a"), 1); e[1].color = (*hexrgb("#f4e6cc"), 1); e[1].position = 0.75
    mid = e.new(0.45); mid.color = (*hexrgb("#e2c49a"), 1)
    nt.links.new(wv.outputs["Fac"], r.inputs["Fac"])
    nt.links.new(r.outputs["Color"], pr.inputs["Base Color"])
    return m


def small_earth_mat(name="searth"):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 2.6; n.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Generated"], n.inputs["Vector"])
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].color = (*hexrgb("#1f5f9e"), 1); e[0].position = 0.52; e[1].color = (*hexrgb("#5f8f45"), 1); e[1].position = 0.54
    nt.links.new(n.outputs["Fac"], r.inputs["Fac"])
    c = nt.nodes.new("ShaderNodeTexNoise"); c.inputs["Scale"].default_value = 5.0; c.inputs["Detail"].default_value = 6
    nt.links.new(tc.outputs["Generated"], c.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB"); ce = cr.color_ramp.elements
    ce[0].position = 0.58; ce[0].color = (0, 0, 0, 1); ce[1].position = 0.68; ce[1].color = (1, 1, 1, 1)
    nt.links.new(c.outputs["Fac"], cr.inputs["Fac"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
    nt.links.new(cr.outputs["Color"], mx.inputs[0]); nt.links.new(r.outputs["Color"], mx.inputs[6])
    mx.inputs[7].default_value = (0.95, 0.96, 1.0, 1)
    nt.links.new(mx.outputs[2], pr.inputs["Base Color"])
    return m


def mars_mat(name="mars"):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.85
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 2.2; n.inputs["Detail"].default_value = 6
    nt.links.new(tc.outputs["Generated"], n.inputs["Vector"])
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].color = (*hexrgb("#7a2e1c"), 1); e[0].position = 0.42; e[1].color = (*hexrgb("#e07a4a"), 1); e[1].position = 0.6
    nt.links.new(n.outputs["Fac"], r.inputs["Fac"])
    nt.links.new(r.outputs["Color"], pr.inputs["Base Color"])
    return m


# where the pair sits in the ridge sky: azimuth/elevation from the hilltop (degrees)
PAIR_AZ, PAIR_EL, RS = 14.0, 21.0, 240.0


def sky_point(az, el, R=RS):
    a, e = math.radians(az), math.radians(el)
    return (R * math.sin(a) * math.cos(e), R * math.cos(a) * math.cos(e), R * math.sin(e))


def sky_planets():
    jg = mat("jup_glow", "#fff3dc", emit="#ffe9c4", emit_strength=4.5)
    mg = mat("mars_glow", "#ff8a4a", emit="#ff6a2a", emit_strength=3.5)
    rg = mat("reg_glow", "#dfe9ff", emit="#cfe0ff", emit_strength=4.0)
    sphere(3.0, sky_point(PAIR_AZ, PAIR_EL), 1, jg, seg=24, name="jup_dot")
    sphere(1.8, sky_point(PAIR_AZ - 1.6, PAIR_EL + 1.5), 1, mg, seg=24, name="mars_dot")
    sphere(1.1, sky_point(PAIR_AZ - 3.6, PAIR_EL - 3.4), 1, rg, seg=16, name="regulus")


def bench(x, y, rot=0):
    w = wood("#9a6a44", "#6b4529", "bench_wood", 4.0, 0.55)
    leg = metal("#2b2f36", 0.45, "bench_leg")
    parts = []
    for k in range(3):
        parts.append(box((1.7, 0.12, 0.05), (x, y - 0.14 + k * 0.14, 0.46), (0, 0, rot), w, bevel=0.015))
    for k in range(2):
        parts.append(box((1.7, 0.05, 0.11), (x, y + 0.24, 0.66 + k * 0.17), (0, 0, rot), w, bevel=0.015))
    for sx in (-0.7, 0.7):
        parts.append(box((0.06, 0.5, 0.44), (x + sx, y, 0.22), (0, 0, rot), leg, bevel=0.01))
    return parts


def thermos(x, y):
    o = cylinder(0.07, 0.3, (x, y, 0.64), (0, 0, 0), plastic("#d9534f", 0.3, "thermos"), verts=32, bevel=0.01)
    c = cylinder(0.075, 0.07, (x, y, 0.82), (0, 0, 0), metal("#c9ccd2", 0.3, "thermos_cap"), verts=32, bevel=0.01)
    return [o, c]


def build_ridge():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    predawn_sky()
    night_stars(300, seed=15)
    sky_planets()
    grass = mat("rgrass", "#4a7f55", rough=0.9, noise_bump=0.35)
    plane(400, 400, (0, 60, 0), material=grass, name="meadow")
    fg = bench(0.9, 0.5, 0) + thermos(0.35, 0.45)
    lantern(1.9, -0.2)
    telescope(-1.7, 1.2)
    for (tx, ty, h, r, sd, c) in ((-6.0, 6.0, 4.6, 1.6, 31, "#2c6340"), (6.8, 8.0, 4.0, 1.5, 32, "#2f6b45"),
                                  (-10.0, 13, 5.2, 1.9, 33, "#2a5d3e"), (11.0, 15, 5.0, 1.8, 34, "#2c6340")):
        tree(tx, ty, h, r, sd, c)
    bush(3.6, -0.6, 0.5, "#2f6b45", "#e8857c", 41)
    bush(-3.4, -0.2, 0.45, "#2c6340", "#f6efe2", 42)
    cols = ["#c9b7e3", "#8fb9c9", "#e8a598", "#d9c99a"]
    win = mat("rwin", "#ffd27a", emit="#ffc35a", emit_strength=8.0)
    random.seed(7)
    for k in range(9):
        hx = -15 + k * 3.7 + random.uniform(-0.6, 0.6); hy = 27 + (k % 3) * 2.5
        house(hx, hy, 2.2, 2.6 + (k * 37 % 3) * 0.5, cols[k % 4], ["#7c2533", "#34425c", "#5a3a4a"][k % 3])
        if k % 2 == 0:
            box((0.4, 0.05, 0.45), (hx, hy - 1.13, 1.2), material=win, bevel=0.01)
    for k, (mx, my, sc) in enumerate(((-38, 92, 12), (-8, 102, 9), (22, 96, 13), (48, 106, 10))):
        sphere(1.0, (mx, my, -2), (sc * 2.2, sc, sc), mat(f"rhill{k}", "#3d4a78", rough=1.0), seg=48)
    area_light((-7, -6, 7), (0, 2, 1), 480, 7, "#b8ccff", "moonkey")
    area_light((7, -4, 3), (0, 2, 1), 220, 5, "#ffc79a", "dawnfill")
    drop_cams()
    return fg


def ridge_angles():
    fg = build_ridge()
    camera((0.3, -7.8, 1.6), (0.6, 4.0, 3.4), lens=24, fstop=8.0)
    still("plate_ridge_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.4, -4.6, 1.4), (0.2, 1.0, 1.75), lens=30, fstop=4.5)
    still("plate_ridge_mid", 1080, 1920, 40)
    still("fg_ridge_mid", 1080, 1920, 24, only=fg)
    j = sky_point(PAIR_AZ - 0.8, PAIR_EL - 2.0)
    drop_cams(); camera((0.0, -3.0, 1.2), j, lens=50, fstop=0)
    still("plate_ridge_sky", 1080, 1920, 40)


# ------------------------------------------------ deep space: one line of sight, Earth -> Mars -> Jupiter (1 : 4)
D = (0.0, 0.4472, 0.8944)          # the line of sight
P = (0.0, 0.8944, -0.4472)         # perpendicular to it, in the side camera's view plane


def along(t, s=0.0, x=0.0):
    return (x + D[0] * t + P[0] * s, D[1] * t + P[1] * s, D[2] * t + P[2] * s)


def build_space():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    world_color(hexrgb("#03050c"), 1.0)
    random.seed(21)
    sm = mat("sstar", "#ffffff", emit="#ffffff", emit_strength=8.0)
    for k in range(700):
        a = random.uniform(0, 2 * math.pi); b = random.uniform(-1.4, 1.4); R = 420
        sphere(random.uniform(0.3, 0.9), (R * math.cos(a) * math.cos(b), R * math.sin(a) * math.cos(b), R * math.sin(b)), 1, sm, seg=6)
    e = sphere(1.4, along(0.0), 1, small_earth_mat(), seg=96, name="earth")
    e.rotation_euler = (0.4, 0.2, 1.1)
    sphere(1.46, along(0.0), 1, atmosphere(), seg=96, name="atmo")
    mars = sphere(1.0, along(22.0, 0.0, 0.0), 1, mars_mat(), seg=96, name="mars")
    jup = sphere(5.2, along(89.0, 0.0, 0.0), 1, jupiter_mat(), seg=96, name="jupiter")
    jup.rotation_euler = (math.radians(-26), 0, 0)
    d = bpy.data.lights.new("sun", "SUN"); d.energy = 4.0; d.angle = math.radians(1.5); d.color = hexrgb("#fff1dc")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    import mathutils
    o.rotation_euler = mathutils.Vector((0.75, 0.4472, 0.8944)).normalized().to_track_quat("-Z", "Y").to_euler()
    area_light((40, 30, 40), (0, 40, 40), 1500, 30, "#9fc4ff", "rimfill")


def space_angles():
    build_space()
    # from just behind Earth: Mars sits right on top of Jupiter
    cam = along(-6.0, -1.9, 0.9)
    camera(cam, along(89.0, 0.4, 0.0), lens=50, fstop=0)
    still("plate_space_eye", 1080, 1920, 40)
    # from the side: the same three on one line, Jupiter 4x farther than Mars
    drop_cams(); camera((-118.0, 20.0, 37.0), (0.0, 20.0, 37.0), lens=30, fstop=0)
    still("plate_space_side", 1080, 1920, 40)


def prop_space():
    reset(800, 800, 30, 0.1, samples=28, bloom=0)
    world_color(hexrgb("#0a0d18"), 0.25)
    area_light((-3, -3, 2.5), (0, 0, 0.5), 650, 2.5, "#fff1dc", "key"); area_light((3, 2.5, 1.5), (0, 0, 0.5), 160, 2, "#8fb9ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    ridge_angles()
    space_angles()
prop_space(); s = sphere(0.5, (0, 0, 0.5), 1, jupiter_mat("jup_p"), seg=96); s.rotation_euler = (math.radians(-12), 0, 0)
camera((0.0, -3.4, 0.5), (0, 0, 0.5), lens=55, fstop=0)
still("jupiter", 700, 700, 32, transparent=True, crop=True)
prop_space(); sphere(0.5, (0, 0, 0.5), 1, mars_mat("mars_p"), seg=96)
camera((0.0, -3.4, 0.5), (0, 0, 0.5), lens=55, fstop=0)
still("mars", 700, 700, 32, transparent=True, crop=True)
