# 2026-11-16-b: "The night the sky fell (1833)" (wild-story). Sets: a little 1833 town square at night (deep-blue starry
# sky, timber/brick shopfronts in palette colours: a GAZETTE newspaper office, a GENERAL STORE, an INN, lanterns on posts,
# a stone well, crates and barrels, round trees, far hills bluer with distance), 3 angles (wide with lots of sky, mid on
# the Gazette door, looking up at the sky over the roofs); deep space: Earth crossing the dust trail left by comet
# Tempel-Tuttle (a ribbon of glowing grains), 1 angle. Cut-outs: the comet nucleus, a stack of newspapers, a barrel.
import math, os, random

# night_sky(), night_stars(), lantern(), lump(), comet() ... (frozen helpers from 2026-11-13-a)
_src = open(os.path.join(ROOT, "jobs/2026-11-13-a/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "a13_helpers", "exec"), globals())
# shopfront(), crate(), pt(), drop_cams() ... (frozen helpers from 2026-11-16-c)
_src = open(os.path.join(ROOT, "jobs/2026-11-16-c/assets.py")).read().split("\n# ------------------------------------------------------------------ the 1910")[0]
exec(compile(_src, "c16_helpers", "exec"), globals())


def post_lantern(x, y):
    w = wood("#6b4529", "#4a2e1a", "post", 3.0)
    frame = metal("#2b2f36", 0.4, "lantern_frame")
    box((0.14, 0.14, 2.6), (x, y, 1.3), material=w, bevel=0.02)
    box((0.6, 0.1, 0.1), (x + 0.25, y, 2.55), material=w, bevel=0.01)
    lx, lz = x + 0.5, 2.15
    box((0.24, 0.24, 0.04), (lx, y, lz + 0.2), material=frame, bevel=0.01)
    box((0.2, 0.2, 0.04), (lx, y, lz - 0.17), material=frame, bevel=0.01)
    box((0.16, 0.16, 0.3), (lx, y, lz), material=mat("plan_glow", "#ffd27a", emit="#ffb64a", emit_strength=14.0), bevel=0.02)
    pt((lx, y - 0.1, lz), 90, "#ffb35a", 0.2, "postlan")


def well(x, y):
    stone = mat("wstone", "#a49a8c", rough=0.9, noise_bump=0.5)
    o = cylinder(0.75, 0.8, (x, y, 0.4), material=stone, verts=40, bevel=0.04)
    cylinder(0.6, 0.02, (x, y, 0.79), material=mat("wwater", "#1b2b4a", rough=0.05, coat=1.0), verts=40)
    w = wood("#8a6142", "#5e3f2a", "wellwood", 3.0)
    parts = [o]
    for sx in (-0.7, 0.7):
        parts.append(box((0.1, 0.1, 1.5), (x + sx, y, 1.5), material=w, bevel=0.01))
    parts.append(cylinder(0.06, 1.5, (x, y, 2.05), (0, 90, 0), w, verts=16))
    roof = mat("wroof", "#7c2533", rough=0.6)
    parts.append(box((1.8, 0.75, 0.06), (x, y - 0.3, 2.45), (35, 0, 0), roof, bevel=0.01))
    parts.append(box((1.8, 0.75, 0.06), (x, y + 0.3, 2.45), (-35, 0, 0), roof, bevel=0.01))
    return parts


def barrel(x, y, s=1.0, name="barrel"):
    prof = [(0.0, 0.0), (0.26, 0.0), (0.31, 0.2), (0.33, 0.4), (0.31, 0.6), (0.26, 0.8), (0.0, 0.8)]
    prof = [(r * s, z * s) for r, z in prof]
    o = lathe(prof, 40, (x, y, 0), wood("#b8864e", "#8a6036", "barrelw", 5.0), name=name)
    band = metal("#3a3e48", 0.4, "band")
    for z in (0.12, 0.68):
        torus(0.3 * s, 0.015 * s, (x, y, z * s), (0, 0, 0), band)
    torus(0.33 * s, 0.015 * s, (x, y, 0.4 * s), (0, 0, 0), band)
    return o


def build_town():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    night_sky()
    nt = bpy.context.scene.world.node_tree
    for n in nt.nodes:
        if n.type == "VALTORGB":
            e = n.color_ramp.elements
            e[0].color = (*hexrgb("#091034"), 1); e[0].position = 0.5; e[1].position = 0.52; e[1].color = (*hexrgb("#16245c"), 1)
            e[-1].color = (*hexrgb("#24406e"), 1); e[-1].position = 0.56
    night_stars(520, seed=33)
    plane(200, 200, (0, 20, 0), material=mat("dirt", "#5e5a62", rough=0.95, noise_bump=0.4), name="square")
    box((40, 2.0, 0.12), (0, -0.5, 0.06), material=mat("boards", "#8a6142", rough=0.8, noise_bump=0.15), bevel=0.02)
    shopfront(-5.2, 0.6, 3.6, 5.4, "#b5533c", sign="INN", sign_col="#34425c", glow="#ffd9a0")
    shopfront(-1.2, 0.6, 4.4, 6.0, "#46965a", sign="GAZETTE", sign_col="#7c2533", glow="#ffe2b0")
    shopfront(3.0, 0.6, 4.0, 5.6, "#c9a24a", sign="STORE", sign_col="#34425c", glow="#ffd9a0")
    shopfront(7.0, 0.6, 3.6, 5.0, "#6fc3c0", glow="#ffe0b0")
    fg = []
    fg += well(-4.6, -3.0)
    fg.append(barrel(-3.3, -0.4)); fg.append(barrel(-2.75, -0.55, 0.9, "barrel2"))
    crate(4.9, -0.4, 0.2); crate(4.9, -0.4, -0.1, 0.8)
    for gx in (-3.2, 1.1, 5.2):
        post_lantern(gx, -1.3)
    for (tx, ty, h, r, sd, c) in ((-9.5, 3.0, 5.0, 1.8, 51, "#2f6b45"), (10.5, 3.5, 4.6, 1.6, 52, "#2c6340"),
                                  (-14, 10, 5.5, 2.0, 53, "#2a5d3e"), (14, 12, 5.2, 1.9, 54, "#2f6b45")):
        tree(tx, ty, h, r, sd, c)
    bush(-6.8, -0.7, 0.5, "#2c6340", "#f6efe2", 61)
    bush(7.6, -0.7, 0.45, "#2f6b45", "#e8857c", 62)
    for k, (mx, my, sc) in enumerate(((-40, 92, 12), (-10, 102, 9), (22, 96, 13), (50, 106, 10))):
        sphere(1.0, (mx, my, -2), (sc * 2.2, sc, sc), mat(f"thill{k}", "#3a4f7a", rough=1.0), seg=48)
    area_light((-8, -9, 9), (0, 1, 1.5), 420, 8, "#9fb6ff", "moonkey")
    area_light((8, -6, 4), (0, 1, 1.5), 140, 6, "#ffcf9a", "warmfill")
    for m in bpy.data.materials:
        if m.name.startswith("interior_") and m.use_nodes:
            pr = m.node_tree.nodes.get("Principled BSDF")
            pr.inputs["Base Color"].default_value = (*hexrgb("#4a3020"), 1)
            pr.inputs["Emission Color"].default_value = (*hexrgb("#ffb860"), 1)
            pr.inputs["Emission Strength"].default_value = 1.6
    drop_cams()
    return fg


def town_angles():
    fg = build_town()
    camera((0.4, -13.5, 1.6), (0.2, 2.0, 4.6), lens=24, fstop=8.0)
    still("plate_town_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.4, -7.6, 1.3), (-0.6, 0.6, 2.4), lens=26, fstop=4.0)
    still("plate_town_mid", 1080, 1920, 40)
    still("fg_town_mid", 1080, 1920, 24, only=fg)
    drop_cams(); camera((0.0, -6.0, 1.0), (0.0, 30.0, 40.0), lens=18, fstop=0)
    still("plate_town_up", 1080, 1920, 40)


# ------------------------------------------------ space: Earth crossing the comet's dust trail
def build_trail():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.45)
    world_color(hexrgb("#03050c"), 1.0)
    random.seed(41)
    sm = mat("sstar", "#ffffff", emit="#ffffff", emit_strength=8.0)
    for k in range(300):
        a = random.uniform(0, 2 * math.pi); b = random.uniform(-1.4, 1.4); R = 420
        sphere(random.uniform(0.3, 0.9), (R * math.cos(a) * math.cos(b), R * math.sin(a) * math.cos(b), R * math.sin(b)), 1, sm, seg=6)
    e = sphere(2.2, (0, 0, 0), 1, earth_mat(), seg=96, name="earth")
    e.rotation_euler = (0.4, 0.2, 2.1)
    sphere(2.3, (0, 0, 0), 1, atmosphere(), seg=96, name="atmo")
    # the dust trail: a long ribbon of glowing grains crossing just in front of Earth, diagonal through the frame
    dm = [mat(f"dust{i}", c, emit=c, emit_strength=s) for i, (c, s) in enumerate((("#fff3c4", 9), ("#bfeaff", 7), ("#ffd27a", 6)))]
    for k in range(700):
        t = random.uniform(-1, 1)
        cx = t * 40.0; cz = 6.0 + t * 18.0
        r = abs(random.gauss(0, 1.0)) * (1.6 + 0.8 * abs(t))
        a = random.uniform(0, 2 * math.pi)
        sphere(random.uniform(0.06, 0.14), (cx + r * math.cos(a) * 0.4, 1.5 + r * math.sin(a), cz + r * math.cos(a)), 1, dm[k % 3], seg=6)
    comet_m = mat("tt_rock", "#5b5560", rough=0.85, noise_bump=0.7)
    lump(1.0, (34, 1.5, 21.3), comet_m, seed=8, amount=0.45, scale=(1.5, 0.9, 0.8))
    d = bpy.data.lights.new("sun", "SUN"); d.energy = 4.0; d.angle = math.radians(1.5); d.color = hexrgb("#fff1dc")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(60), 0, math.radians(-50))
    area_light((30, -20, 30), (0, 0, 0), 1200, 30, "#9fc4ff", "rimfill")


def trail_angles():
    build_trail()
    drop_cams(); camera((-3.0, -30.0, 2.0), (6.0, 0.0, 9.0), lens=28, fstop=0)
    still("plate_trail", 1080, 1920, 40)


def prop_scene2(bg="#c9d4e2"):
    reset(800, 800, 30, 0.1, samples=24, bloom=0.2)
    world_color(hexrgb(bg), 0.7)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    town_angles()
    trail_angles()
prop_scene2(); comet(); camera((0.4, -3.6, 1.8), (0, 0, 0.6), lens=50, fstop=0)
still("comet", 700, 600, 28, transparent=True, crop=True)
prop_scene2(); barrel(0, 0, 1.0); camera((0.6, -3.0, 1.2), (0, 0, 0.4), lens=50, fstop=0)
still("barrel", 500, 600, 24, transparent=True, crop=True)
