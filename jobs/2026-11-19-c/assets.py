# 2026-11-19-c: "What if Jupiter became a star?" (what-if).
# Sets: a town rooftop terrace at night (terracotta tiles, a low parapet, warm string lights between two poles, potted
# plants, a brass telescope, a bench, a water tank, neighbouring roofs with lit windows, round trees), Jupiter a bright
# cream dot in the sky; 3 angles (wide, mid, long lens on Jupiter) + the same wide and sky angles with Jupiter swapped for
# a small red star (SPECULATION shot). Deep space: Jupiter big and banded, lit from the side; the same shot with Jupiter
# ignited as a red dwarf (glowing, churning surface). Cut-outs: Jupiter, the red star.
import math, os, random

# jupiter_mat(), bench(), thermos(), sky_point(), telescope(), lantern(), house(), tree(), bush(), seg(), drop_cams(),
# dusk_sky(), night_stars() ... (frozen helpers from earlier jobs)
_src = open(os.path.join(ROOT, "jobs/2026-11-15-c/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "c15_helpers", "exec"), globals())

JAZ, JEL = 8.0, 26.0


def jupiter_mat(name="jup2"):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.6
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = 3.4; wv.inputs["Distortion"].default_value = 4.0; wv.inputs["Detail"].default_value = 6.0
    wv.inputs["Detail Scale"].default_value = 1.6
    nt.links.new(tc.outputs["Generated"], wv.inputs["Vector"])
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].color = (*hexrgb("#9a5a3a"), 1); e[1].color = (*hexrgb("#f6ead6"), 1); e[1].position = 0.8
    a = e.new(0.35); a.color = (*hexrgb("#c98a5e"), 1)
    b = e.new(0.55); b.color = (*hexrgb("#e9d2ac"), 1)
    nt.links.new(wv.outputs["Fac"], r.inputs["Fac"])
    nt.links.new(r.outputs["Color"], pr.inputs["Base Color"])
    return m


def star_mat(name="rstar", strength=9.0):
    """Churning red-dwarf surface: noise between deep red and orange-yellow, emissive."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 7.0; nz.inputs["Detail"].default_value = 9.0
    nt.links.new(tc.outputs["Generated"], nz.inputs["Vector"])
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].color = (*hexrgb("#6e0f06"), 1); e[0].position = 0.35
    e[1].color = (*hexrgb("#ffa040"), 1); e[1].position = 0.75
    mid = e.new(0.52); mid.color = (*hexrgb("#e8340e"), 1)
    nt.links.new(nz.outputs["Fac"], r.inputs["Fac"])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = strength
    nt.links.new(r.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return m


def string_lights(x0, x1, y, z, sag=0.45, n=16):
    pole = wood("#6b4529", "#4a2f1c", "pole", 3.0, 0.6)
    for x in (x0, x1):
        cylinder(0.05, z, (x, y, z / 2), material=pole, verts=12)
    bulb = mat("sl_bulb", "#ffe1a0", emit="#ffc35a", emit_strength=16.0)
    wire = mat("sl_wire", "#1a1410", rough=0.6)
    pts = []
    for k in range(n + 1):
        t = k / n
        pts.append((x0 + (x1 - x0) * t, y, z - sag * 4 * t * (1 - t)))
    for a, b in zip(pts, pts[1:]):
        seg(a, b, 0.008, wire)
    for p in pts[1:-1]:
        sphere(0.045, (p[0], p[1], p[2] - 0.06), 1, bulb, seg=10)
    L = bpy.data.lights.new("sl", "AREA"); L.energy = 160; L.size = abs(x1 - x0); L.color = hexrgb("#ffb35a")
    o = bpy.data.objects.new("sl", L); bpy.context.scene.collection.objects.link(o); o.location = ((x0 + x1) / 2, y - 0.3, z - 0.4)


def pot_plant(x, y, s=1.0, col="#2f7a4a"):
    cylinder(0.22 * s, 0.36 * s, (x, y, 0.18 * s), material=mat("pot", "#c9643f", rough=0.7), verts=32, bevel=0.02)
    sphere(0.36 * s, (x, y, 0.6 * s), (1, 1, 0.9), mat("pl_" + col, col, rough=0.8, noise_bump=0.4), seg=24)


def build_roof():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.35)
    dusk_sky(top="#081038", mid="#1c2a66", horizon="#5a4a8a")
    for o in [o for o in bpy.data.objects if o.type == "LIGHT" and o.name.startswith("sun")]:
        o.data.color = hexrgb("#a9c4ff"); o.data.energy = 1.4
        o.rotation_euler = (math.radians(55), 0, math.radians(-40))
    night_stars(380, seed=19)
    jup = sphere(2.4, sky_point(JAZ, JEL), 1, mat("jup_glow", "#fff3dc", emit="#ffe9c4", emit_strength=6.0), seg=24, name="jup_dot")
    star = sphere(4.2, sky_point(JAZ, JEL), 1, star_mat("rstar_sky", 5.0), seg=32, name="red_star")
    halo = star
    star.hide_render = True
    # the roof
    tiles = mat("roof_tiles", "#b5654a", rough=0.85, noise_bump=0.3)
    plane(12, 20, (0, -5.0, 0), material=tiles, name="roof")
    para = mat("parapet", "#e8dcc6", rough=0.8, noise_bump=0.15)
    box((12, 0.3, 0.8), (0, 5.0, 0.4), material=para, bevel=0.04)
    for sx in (-6.0, 6.0):
        box((0.3, 20, 0.8), (sx, -5.0, 0.4), material=para, bevel=0.04)
    string_lights(-4.6, 4.4, 4.6, 2.6)
    telescope(-1.9, 1.6)
    bench(1.6, 2.4, 0)
    thermos(1.1, 2.35)
    lantern(2.7, 1.8)
    cylinder(0.75, 1.5, (4.6, 3.6, 0.75), material=metal("#9aa3ad", 0.4, "tank"), verts=40, bevel=0.03)
    for (px, py, s, c) in ((-4.8, 4.2, 1.1, "#2f7a4a"), (-3.9, 4.3, 0.8, "#3f8a3e"), (3.4, 4.3, 0.9, "#2f6b45"),
                           (-5.3, -1.2, 1.0, "#3f8a3e")):
        pot_plant(px, py, s, c)
    # neighbouring roofs and the town beyond
    cols = ["#c9b7e3", "#8fb9c9", "#e8a598", "#d9c99a", "#9fc49a"]
    win = mat("twin", "#ffd27a", emit="#ffc35a", emit_strength=8.0)
    random.seed(11)
    for k in range(11):
        hx = -22 + k * 4.4 + random.uniform(-0.8, 0.8); hy = 12 + (k % 3) * 4.0
        hh = 2.6 + (k * 37 % 4) * 0.7
        house(hx, hy, 2.6, hh, cols[k % 5], ["#7c2533", "#34425c", "#5a3a4a"][k % 3])
        if k % 2 == 0:
            box((0.45, 0.05, 0.5), (hx - 0.4, hy - 1.33, hh * 0.55), material=win, bevel=0.01)
    for (tx, ty, h, r, sd, c) in ((-9.0, 9.0, 4.4, 1.6, 31, "#2c6340"), (9.5, 10.0, 4.2, 1.5, 32, "#2f6b45"),
                                  (-15.0, 22, 5.2, 1.9, 33, "#2a5d3e"), (15.0, 24, 5.0, 1.8, 34, "#2c6340")):
        tree(tx, ty, h, r, sd, c)
    for k, (mx, my, sc) in enumerate(((-38, 92, 12), (-8, 102, 9), (22, 96, 13), (48, 106, 10))):
        sphere(1.0, (mx, my, -2), (sc * 2.2, sc, sc), mat(f"rhill{k}", "#2f3a68", rough=1.0), seg=48)
    area_light((-7, -6, 7), (0, 2, 1), 520, 7, "#b8ccff", "moonkey")
    area_light((6, -4, 3), (0, 2, 1), 200, 5, "#ffc79a", "warmfill")
    drop_cams()
    return jup, star, halo


def roof_angles():
    jup, star, halo = build_roof()
    camera((0.3, -7.6, 1.7), (0.5, 4.0, 3.3), lens=24, fstop=8.0)
    still("plate_roof_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.4, -4.4, 1.4), (0.3, 1.5, 1.8), lens=30, fstop=4.5)
    still("plate_roof_mid", 1080, 1920, 40)
    j = sky_point(JAZ, JEL - 4.0)
    drop_cams(); camera((0.0, -3.0, 1.2), j, lens=50, fstop=0)
    still("plate_roof_sky", 1080, 1920, 40)
    # the speculation: Jupiter is now a small red star
    jup.hide_render = True; star.hide_render = False; halo.hide_render = False
    still("plate_roof_skyred", 1080, 1920, 40)
    drop_cams(); camera((0.3, -7.6, 1.7), (0.5, 4.0, 3.3), lens=24, fstop=8.0)
    still("plate_roof_widered", 1080, 1920, 40)


def build_space(ignited=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.6 if ignited else 0.3)
    world_color(hexrgb("#03050c"), 1.0)
    random.seed(23)
    sm = mat("sstar", "#ffffff", emit="#ffffff", emit_strength=8.0)
    for k in range(700):
        a = random.uniform(0, 2 * math.pi); b = random.uniform(-1.4, 1.4); R = 420
        sphere(random.uniform(0.3, 0.9), (R * math.cos(a) * math.cos(b), R * math.sin(a) * math.cos(b), R * math.sin(b)), 1, sm, seg=6)
    if ignited:
        j = sphere(5.0, (0, 0, 0), 1, star_mat("rstar_space", 1.6), seg=128, name="star")
    else:
        j = sphere(5.0, (0, 0, 0), 1, jupiter_mat(), seg=128, name="jupiter")
        d = bpy.data.lights.new("sun", "SUN"); d.energy = 4.2; d.angle = math.radians(1.5); d.color = hexrgb("#fff1dc")
        o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
        o.rotation_euler = (math.radians(70), 0, math.radians(-60))
        area_light((14, 10, 6), (0, 0, 0), 900, 10, "#6f8fff", "rim")
    j.rotation_euler = (math.radians(-14), 0, 0)
    # a tiny moon for scale
    sphere(0.32, (-7.5, 3.0, 4.8), 1, mat("io", "#e8c86a", rough=0.8, noise_bump=0.3, emit="#ffb35a" if ignited else None,
                                         emit_strength=0.0), seg=48, name="moon")
    if ignited:
        P = bpy.data.lights.new("starlight", "POINT"); P.energy = 60000; P.color = hexrgb("#ff6a2a"); P.shadow_soft_size = 5
        o = bpy.data.objects.new("starlight", P); bpy.context.scene.collection.objects.link(o); o.location = (0, 0, 0)
        j.visible_shadow = False
    camera((0.0, -17.0, 2.0), (0.0, 0.0, 2.6), lens=30, fstop=0)


def space_angles():
    build_space(False)
    still("plate_space_jup", 1080, 1920, 40)
    build_space(True)
    still("plate_space_star", 1080, 1920, 40)


if not os.environ.get("BK_PROPS_ONLY"):
    roof_angles()
    space_angles()
prop_space(); s = sphere(0.5, (0, 0, 0.5), 1, jupiter_mat("jup_p"), seg=96); s.rotation_euler = (math.radians(-12), 0, 0)
camera((0.0, -3.4, 0.5), (0, 0, 0.5), lens=55, fstop=0)
still("jupiter", 700, 700, 32, transparent=True, crop=True)
reset(800, 800, 30, 0.1, samples=28, bloom=0)
world_color(hexrgb("#0a0d18"), 0.0)
sphere(0.5, (0, 0, 0.5), 1, star_mat("rstar_p", 1.2), seg=96)
camera((0.0, -3.4, 0.5), (0, 0, 0.5), lens=55, fstop=0)
still("redstar", 700, 700, 32, transparent=True, crop=True)
