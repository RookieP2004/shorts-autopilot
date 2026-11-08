# 2026-11-08-c: "How many ants live on Earth?" Sets: a sunny town park with a picnic (gingham blanket, cake, basket,
# lemonade, an ant hill, round trees, bench, fountain, houses behind), 3 angles + foreground layers; a town square with a
# giant brass balance scale (level/empty, and tipped by two crates). Cut-outs: hero ant, walking ant (side), two crates.
import math, os, random

# sunny() sky + sun from the reference job m3 (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-m3/assets.py")).read().split("def build_market")[0]
exec(compile(_src, "m3_helpers", "exec"), globals())


def gingham(path, a="#d9534f", b="#f6efe2", n=12, size=512):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (size, size), b)
    d = ImageDraw.Draw(im, "RGBA")
    s = size // n
    for i in range(n):
        if i % 2 == 0:
            d.rectangle((i * s, 0, i * s + s - 1, size), fill=(217, 83, 79, 150))
            d.rectangle((0, i * s, size, i * s + s - 1), fill=(217, 83, 79, 150))
    im.save(path)
    return path


def checker_mat(name, a, b, scale):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.8
    tc = nt.nodes.new("ShaderNodeTexCoord"); ck = nt.nodes.new("ShaderNodeTexChecker")
    ck.inputs["Scale"].default_value = scale
    ck.inputs["Color1"].default_value = (*hexrgb(a), 1); ck.inputs["Color2"].default_value = (*hexrgb(b), 1)
    nt.links.new(tc.outputs["Object"], ck.inputs["Vector"]); nt.links.new(ck.outputs["Color"], pr.inputs["Base Color"])
    return m


def seg(p0, p1, r, material):
    """A cylinder from point p0 to p1."""
    import mathutils
    a, b = mathutils.Vector(p0), mathutils.Vector(p1)
    d = b - a
    c = cylinder(r, d.length, tuple((a + b) / 2), material=material, verts=10, bevel=0)
    c.rotation_mode = "QUATERNION"
    c.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(d.normalized())
    sphere(r * 1.15, tuple(b), 1, material, seg=12)
    return c


def tree(x, y, h=3.6, r=1.3, seed=1, col="#4f9a45"):
    random.seed(seed)
    cylinder(0.16, h * 0.6, (x, y, h * 0.3), material=wood("#8a6142", "#5e3f2a", "bark", 2.0, 0.8), verts=20)
    leaf = mat(f"canopy{seed}", col, rough=0.75, noise_bump=0.25)
    for k in range(7):
        a = k / 7 * 2 * math.pi
        sphere(r * random.uniform(0.55, 0.7), (x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.45,
               h * 0.72 + random.uniform(-0.2, 0.35)), 1, leaf, seg=32)
    sphere(r * 0.8, (x, y, h * 0.92), 1, leaf, seg=32)


def bush(x, y, r=0.5, col="#3f8a3e", flowers="#f2b04a", seed=0):
    random.seed(seed)
    parts = []
    m = mat(f"bush{seed}", col, rough=0.8, noise_bump=0.25)
    for k in range(5):
        parts.append(sphere(r * random.uniform(0.6, 0.85), (x + random.uniform(-r, r) * 0.7, y + random.uniform(-r, r) * 0.3,
                            r * random.uniform(0.45, 0.8)), 1, m, seg=24))
    fm = plastic(flowers, 0.4, f"flower{seed}")
    for k in range(9):
        parts.append(sphere(0.05, (x + random.uniform(-r, r) * 0.9, y - r * 0.55, random.uniform(0.25, r * 1.2)), 1, fm, seg=12))
    return parts


def house(x, y, w, h, col, roof="#b5533c"):
    box((w, 2.2, h), (x, y, h / 2), material=mat(f"house{x}", col, rough=0.8), bevel=0.05)
    r = cylinder(w * 0.62, 2.4, (x, y, h + 0.02), (90, 0, 0), mat(f"roof{roof}", roof, rough=0.6), verts=3, bevel=0.03)
    r.rotation_euler = (math.radians(90), math.radians(30), 0)
    win = mat("window", "#cfe6f2", rough=0.1, coat=0.6)
    for fz in range(int(h // 1.5)):
        for fx in (-0.28, 0.28):
            box((0.42 * w * 0.5, 0.06, 0.6), (x + fx * w, y - 1.12, 1.0 + fz * 1.5), material=win, bevel=0.02)


def bench(x, y):
    m = wood("#b8864e", "#8a6036", "bench", 4.0)
    ir = metal("#3b3f46", 0.4, "iron")
    for k in range(3):
        box((1.8, 0.12, 0.05), (x, y - 0.15 + k * 0.15, 0.46), material=m, bevel=0.015)
    for k in range(2):
        box((1.8, 0.05, 0.12), (x, y + 0.24, 0.62 + k * 0.17), (12, 0, 0), material=m, bevel=0.015)
    for sx in (-0.8, 0.8):
        box((0.06, 0.5, 0.46), (x + sx, y, 0.23), material=ir, bevel=0.01)


def cake(x, y, s=1.0):
    parts = [lathe([(0.0, 0.0), (0.26 * s, 0.0), (0.27 * s, 0.02 * s), (0.27 * s, 0.17 * s), (0.25 * s, 0.19 * s), (0.0, 0.19 * s)], 40,
                   (x, y, 0.02), mat("sponge", "#f4d6a0", rough=0.6), 1, "cake_low")]
    parts.append(lathe([(0.0, 0.0), (0.275 * s, 0.0), (0.28 * s, 0.03 * s), (0.27 * s, 0.05 * s), (0.0, 0.055 * s)], 40,
                       (x, y, 0.2 * s), mat("icing", "#f7b6c2", rough=0.3, coat=0.5), 1, "icing"))
    for k in range(8):
        a = k / 8 * 2 * math.pi
        parts.append(sphere(0.035 * s, (x + 0.19 * s * math.cos(a), y + 0.19 * s * math.sin(a), 0.27 * s), 1,
                            mat("cherry", "#b3121b", rough=0.15, coat=0.8), seg=16))
    parts.append(cylinder(0.33 * s, 0.02, (x, y, 0.01), material=mat("plate", "#f6efe2", rough=0.2, coat=0.5), verts=40))
    return parts


def picnic_basket(x, y):
    m = wood("#c99a5b", "#9c7040", "wicker", 30.0, 0.7)
    parts = [box((0.62, 0.4, 0.34), (x, y, 0.17), material=m, bevel=0.04),
             box((0.64, 0.42, 0.05), (x, y, 0.36), (0, -6, 0), material=wood("#b3824a", "#8a6036", "lid", 30.0), bevel=0.02),
             torus(0.24, 0.02, (x, y, 0.38), (90, 0, 0), wood("#8a6036", "#5e3f2a", "handle", 8.0))]
    parts.append(box((0.3, 0.02, 0.18), (x + 0.1, y - 0.21, 0.42), (0, 0, 8), mat("napkin", "#d9534f", rough=0.8), bevel=0.01))
    return parts


def jug(x, y):
    g = mat("lemon", "#f4d35e", rough=0.05, transmission=0.6, coat=0.5)
    return [lathe([(0.0, 0.0), (0.11, 0.0), (0.13, 0.05), (0.13, 0.22), (0.1, 0.3), (0.0, 0.3)], 32, (x, y, 0.02), g, 1, "jug")]


def anthill(x, y, r=0.38):
    return lathe([(0.0, 0.0), (r, 0.0), (r * 0.7, r * 0.18), (r * 0.35, r * 0.42), (r * 0.12, r * 0.52), (0.06, r * 0.5), (0.0, r * 0.42)],
                 40, (x, y, 0), mat("soil", "#9a6a42", rough=0.95, noise_bump=0.5), 1, "anthill")


def build_park():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny()
    plane(300, 300, (0, 0, 0), material=mat("grass", "#7cbf55", rough=0.9, noise_bump=0.35), name="grass")
    plane(2.2, 60, (-4.6, 10, 0.008), (0, 0, 16), mat("gravel", "#e3cfa6", rough=0.9, noise_bump=0.2), name="path")
    blanket = plane(2.6, 2.0, (0, 0.15, 0.025), (0, 0, 4), checker_mat("gingham", "#e8857c", "#f6efe2", 7.0), "blanket")
    fgp = cake(0.35, 0.25) + picnic_basket(-0.75, 0.45) + jug(-0.2, 0.75)
    for k, (px, py) in enumerate(((0.75, -0.25), (-0.15, -0.35))):
        cylinder(0.14, 0.015, (px, py, 0.02), material=mat("plate2", "#f6efe2", rough=0.2, coat=0.4), verts=32)
    hill = anthill(1.75, -0.55)
    tree(-3.4, 4.2, 3.8, 1.4, 1); tree(3.6, 5.5, 4.2, 1.5, 2, "#5aa64a"); tree(-6.5, 9, 4.6, 1.6, 3); tree(6.8, 11, 4.4, 1.6, 4, "#4c9440")
    tree(0.8, 13, 4.8, 1.7, 5, "#5aa64a")
    bench(2.6, 3.0)
    fountain = [lathe([(0.0, 0.0), (1.3, 0.0), (1.35, 0.45), (1.2, 0.5), (0.25, 0.45), (0.2, 1.3), (0.6, 1.4), (0.62, 1.5), (0.0, 1.5)],
                      48, (-2.6, 8.5, 0), mat("stone", "#e8e0d2", rough=0.6), 1, "fountain")]
    cylinder(1.18, 0.05, (-2.6, 8.5, 0.42), material=mat("water", "#5fb8d8", rough=0.05, coat=0.9), verts=48)
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#f6efe2", "#c9b7e3", "#9fd39a"]
    for k in range(7):
        house(-9 + k * 3.0, 20 + (k % 2) * 1.2, 2.6, 3.5 + (k * 37 % 3), cols[k % 6], ["#b5533c", "#34425c", "#7c2533"][k % 3])
    b1 = bush(-1.9, -1.4, 0.45, seed=1)
    bush(4.0, 1.0, 0.6, "#46965a", "#d9534f", 2)
    bush(-4.4, 2.0, 0.55, "#3f8a3e", "#f6efe2", 3)
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)
    return fgp, hill, b1


def park_angles():
    fgp, hill, b1 = build_park()
    for name, loc, tgt, lens, fs, fg in (("park_wide", (0.5, -9.6, 2.6), (0, 1.2, 1.25), 30, 6.0, fgp + b1),
                                         ("park_mid", (-0.6, -4.6, 1.75), (0.15, 0.3, 0.95), 34, 4.0, fgp),
                                         ("park_close", (2.5, -2.7, 0.62), (1.05, -0.12, 0.18), 28, 2.4, [hill])):
        for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(o)
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=fg)


def crate(x, y, z, label, name, s=1.0, rot=0):
    m = wood("#c08b52", "#8a6036", f"crate_{name}", 4.0)
    c = box((1.1 * s, 0.9 * s, 0.9 * s), (x, y, z + 0.45 * s), (0, rot, 0), m, bevel=0.04, name=name)
    for dz in (0.15, 0.75):
        sl = box((1.14 * s, 0.94 * s, 0.08 * s), (0, 0, (dz - 0.45) * s), material=wood("#9c6c3c", "#7a5230", "slat", 4.0), bevel=0.01)
        sl.parent = c
    lines = []   # labels are 2D text layers in the job (3D stencil text read as blobs)
    for i, ln in enumerate(lines):
        t = text3d(ln, (0.36 if len(lines) == 1 else 0.2) * s, (0, -0.47 * s, (0.0 - (i - (len(lines) - 1) / 2) * 0.24) * s),
                   (90, 0, 0), mat("stencil", "#1a1410", rough=0.6), font="display", extrude=0.005)
        t.parent = c
    return c


def scale_set(state):
    """state 'empty' = level, no crates; 'tipped' = ants crate (left) down, wild crate (right) up."""
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sun=4.0)
    plane(300, 300, (0, 0, 0), material=checker_mat("plaza", "#e9dcc4", "#d6c3a0", 0.6), name="plaza")
    plane(300, 300, (0, 0, -0.01), material=mat("cobble", "#d8c7a8", rough=0.8), name="under")
    brass = metal("#d9a441", 0.25, "brass")
    dark = metal("#5a4636", 0.4, "bronze")
    lathe([(0.0, 0.0), (1.0, 0.0), (1.0, 0.25), (0.75, 0.32), (0.5, 0.6), (0.0, 0.6)], 48, (0, 2.0, 0), mat("plinth", "#efe3cf", rough=0.5), 1, "plinth")
    cylinder(0.12, 3.0, (0, 2.0, 2.1), material=brass, verts=32)
    sphere(0.22, (0, 2.0, 3.65), 1, brass)
    th = math.radians(11 if state == "tipped" else 0)
    L = 2.1
    beam = box((2 * L + 0.2, 0.16, 0.16), (0, 2.0, 3.5), (0, -math.degrees(th) * -1, 0), brass, bevel=0.05)
    beam.rotation_euler = (0, -th, 0)                         # left (-x) end goes down
    for side in (-1, 1):
        ex, ez = side * L * math.cos(th), 3.5 + side * L * math.sin(th)
        pz = ez - 2.0
        for dx in (-0.6, 0.6):
            for dy in (-0.3, 0.3):
                cylinder(0.015, 2.0, (ex + dx * 0.75, 2.0 + dy * 0.75, pz + 1.05), material=dark, verts=8, bevel=0)
        lathe([(0.0, 0.0), (0.85, 0.04), (0.98, 0.16), (1.0, 0.2), (0.0, 0.08)], 48, (ex, 2.0, pz - 0.05), brass, 1, f"pan{side}")
        sphere(0.07, (ex, 2.0, ez), 1, brass)
        if state == "tipped":
            if side < 0:
                crate(ex, 2.0, pz + 0.12, "ANTS", "c_ants", 1.25)
            else:
                crate(ex, 2.0, pz + 0.12, "BIRDS +\nMAMMALS", "c_wild", 1.25)
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#f6efe2", "#c9b7e3", "#9fd39a", "#e3c99a"]
    for k in range(8):
        house(-10.5 + k * 3.0, 12 + (k % 2) * 0.8, 2.7, 4 + (k * 53 % 4), cols[k % 7], ["#b5533c", "#34425c", "#7c2533"][k % 3])
    bunting(-6, 6, 9.5, 5.2)
    tree(-5.2, 6, 4.0, 1.4, 7); tree(5.4, 7, 4.2, 1.5, 8, "#5aa64a")
    for k, x in enumerate((-3.8, 3.8)):
        cylinder(0.05, 3.4, (x, 0.5, 1.7), material=metal("#3b3f46", 0.4, "lamp"), verts=12)
        sphere(0.18, (x, 0.5, 3.45), 1, mat("globe", "#f6efe2", rough=0.2, emit="#ffe2a8", emit_strength=1.0))
    camera((0.0, -8.6, 2.1), (0, 2.0, 2.45), lens=26, fstop=0)
    still(f"plate_square_{state}", 1080, 1920, 40)


def ant(name="ant", s=1.0):
    shell = mat("ant_shell", "#4a1d12", rough=0.25, coat=0.7)
    leg = mat("ant_leg", "#2e140d", rough=0.35, coat=0.4)
    parts = [sphere(0.5 * s, (-0.85 * s, 0, 0.55 * s), (1.15, 0.85, 0.85), shell),     # gaster
             sphere(0.14 * s, (-0.25 * s, 0, 0.52 * s), 1, shell),                     # petiole
             sphere(0.32 * s, (0.15 * s, 0, 0.6 * s), (1.35, 0.7, 0.75), shell),       # thorax
             sphere(0.34 * s, (0.75 * s, 0, 0.78 * s), (1.0, 0.95, 1.05), shell)]      # head
    for side in (-1, 1):
        sphere(0.08 * s, (0.92 * s, side * 0.22 * s, 0.9 * s), 1, mat("eye", "#120806", rough=0.1, coat=1.0))
        for k, (hx, fx) in enumerate(((-0.05, -0.75), (0.15, 0.2), (0.35, 1.05))):
            hip = (hx * s, side * 0.12 * s, 0.5 * s)
            knee = ((hx + (fx - hx) * 0.4) * s, side * 0.55 * s, 0.78 * s)
            foot = (fx * s, side * 0.8 * s, 0.02 * s)
            seg(hip, knee, 0.04 * s, leg); seg(knee, foot, 0.032 * s, leg)
        base = (0.95 * s, side * 0.12 * s, 1.0 * s); elbow = (1.05 * s, side * 0.3 * s, 1.45 * s); tip = (1.55 * s, side * 0.45 * s, 1.35 * s)
        seg(base, elbow, 0.026 * s, leg); seg(elbow, tip, 0.022 * s, leg)
        sphere(0.07 * s, (1.08 * s, side * 0.1 * s, 0.6 * s), (1.4, 0.6, 0.5), leg)
    return parts


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


park_angles()
scale_set("empty")
scale_set("tipped")
prop_scene(); ant(); sprite_camera((0.0, 0, 0.6), 4.6, 1.6, 50, azimuth=-55); still("ant", 800, 600, 28, transparent=True, crop=True)
prop_scene(); ant(); camera((0.0, -5.0, 1.2), (0.0, 0, 0.55), lens=55, fstop=0); still("ant_side", 600, 400, 20, transparent=True, crop=True)
prop_scene(); crate(0, 0, 0, "ANTS", "c_ants"); sprite_camera((0, 0, 0.45), 4.0, 0.9, 50, azimuth=0); still("crate_ants", 600, 600, 24, transparent=True, crop=True)
prop_scene(); crate(0, 0, 0, "BIRDS +\nMAMMALS", "c_wild"); sprite_camera((0, 0, 0.45), 4.0, 0.9, 50, azimuth=0); still("crate_wild", 600, 600, 24, transparent=True, crop=True)
