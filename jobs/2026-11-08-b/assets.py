# 2026-11-08-b: "Do we only use 10% of our brain?" Sets: a bright brain lab (giant brain model, dark + lit), a night town
# (the city analogy: windows lit district by district, then everywhere). Cut-outs: brain (dark, lit), old book.
import math, os, random

def brain(loc=(0, 0, 0), s=1.0, lit=False, name="brain"):
    """A stylised brain, side view along -y: two folded hemispheres (Voronoi ridges, darker grooves), cerebellum, stem.
    lit = scan hotspots glowing all over it."""
    x, y, z = loc
    base = mat(name + "_m", "#ec9ea4", rough=0.3, sss=0.25, coat=0.5)
    nt = base.node_tree; p = nt.nodes.get("Principled BSDF")
    geo = nt.nodes.new("ShaderNodeNewGeometry"); r = nt.nodes.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].position = 0.45; r.color_ramp.elements[0].color = (*hexrgb("#b4555f"), 1)
    r.color_ramp.elements[1].position = 0.53; r.color_ramp.elements[1].color = (*hexrgb("#f2a9ae"), 1)
    nt.links.new(geo.outputs["Pointiness"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], p.inputs["Base Color"])
    if lit:
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 2
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.42; ramp.color_ramp.elements[0].color = (*hexrgb("#000000"), 1)
        ramp.color_ramp.elements[1].position = 0.56; ramp.color_ramp.elements[1].color = (*hexrgb("#ff6a00"), 1)
        nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], p.inputs["Emission Color"])
        p.inputs["Emission Strength"].default_value = 2.5
        r2 = nt.nodes.new("ShaderNodeValToRGB")
        r2.color_ramp.elements[0].position = 0.42; r2.color_ramp.elements[0].color = (*hexrgb("#e88f8f"), 1)
        r2.color_ramp.elements[1].position = 0.56; r2.color_ramp.elements[1].color = (*hexrgb("#ff5a00"), 1)
        nt.links.new(nz.outputs["Fac"], r2.inputs["Fac"]); nt.links.new(r2.outputs["Color"], p.inputs["Base Color"])
    tex = bpy.data.textures.new(name + "_folds", "VORONOI")
    tex.distance_metric = "DISTANCE"; tex.noise_scale = 0.18 * s; tex.color_mode = "INTENSITY"
    tex.weight_1 = -1; tex.weight_2 = 1; tex.noise_intensity = 1.0
    parts = []
    for side in (-1, 1):
        h = sphere(0.5 * s, (x, y + side * 0.2 * s, z + 0.5 * s), (0.85, 0.42, 0.62), base, seg=96, name=f"{name}_h{side}")
        sub = h.modifiers.new("sub", "SUBSURF"); sub.levels = sub.render_levels = 3
        d = h.modifiers.new("folds", "DISPLACE"); d.texture = tex; d.strength = 0.12 * s; d.mid_level = 0.5
        sm = h.modifiers.new("sm", "SMOOTH"); sm.factor = 0.8; sm.iterations = 4
        parts.append(h)
    cbm = mat(name + "_cb", "#d9868d", rough=0.35, sss=0.2, coat=0.4)
    parts.append(sphere(0.22 * s, (x + 0.33 * s, y, z + 0.2 * s), (1.0, 1.35, 0.58), cbm, name=name + "_cb"))
    parts.append(cylinder(0.08 * s, 0.3 * s, (x + 0.14 * s, y, z + 0.06 * s), (0, -18, 0), mat(name + "_st", "#d07d83", rough=0.4), name=name + "_st"))
    return parts

def pot_plant(x, y, h=1.0, seed=0):
    random.seed(seed)
    lathe([(0.0, 0.0), (0.2, 0.0), (0.27, 0.36), (0.29, 0.4), (0.0, 0.38)], 32, (x, y, 0), clay("#c96f4a", "pot"), 1, "pot")
    leaf = plastic("#3f9a4a", 0.5, "leafm")
    for k in range(7):
        a = k / 7 * 2 * math.pi
        sphere(0.22 * h, (x + 0.16 * math.cos(a), y + 0.16 * math.sin(a), 0.5 + random.uniform(0.1, 0.5) * h), (1, 1, 1.3), leaf)

def lab(lit=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#dff0f2"), 0.7)
    plane(40, 40, (0, 0, 0), material=paper(os.path.join(TEX, "floor_checker.png"), 0.3, "tiles"), name="floor")
    box((3.0, 2.2, 0.03), (1.0, 0.4, 0.015), material=mat("rug", "#34425c", rough=0.9), bevel=0.01)
    # scanner ring + bed (MRI-style), back left
    torus(1.05, 0.32, (-2.3, 2.4, 1.35), (90, 0, 0), plastic("#f6efe2", 0.25, "mri"))
    box((1.3, 0.9, 0.5), (-2.3, 2.4, 0.25), material=plastic("#e6e1d6", 0.3, "mribase"), bevel=0.06)
    box((0.7, 2.6, 0.12), (-2.3, 1.2, 0.85), material=plastic("#6fc3c0", 0.3, "bed"), bevel=0.05)
    box((0.5, 0.4, 0.7), (-2.3, 0.2, 0.42), material=plastic("#e6e1d6", 0.3, "bedleg"), bevel=0.05)
    torus(1.06, 0.05, (-2.3, 2.05, 1.35), (90, 0, 0), glow("#6fc3c0", 3.0, "mriglow"))
    box((30, 0.3, 9), (0, 4.0, 4.5), material=mat("wallb", "#7cc6c2", rough=0.8), bevel=0)
    box((0.3, 30, 9), (-5.2, 0, 4.5), material=mat("walls", "#9fd6d2", rough=0.8), bevel=0)
    box((30, 0.32, 0.25), (0, 3.85, 0.12), material=mat("skirt", "#f6efe2"), bevel=0)
    # big wall screen with a scan
    box((2.6, 0.12, 1.6), (1.2, 3.8, 3.3), material=mat("bezel", "#25262b", rough=0.3), bevel=0.04)
    box((2.4, 0.05, 1.4), (1.2, 3.72, 3.3), material=glow("#2a5d7a", 1.2, "screen"), bevel=0)
    for k in range(6):
        sphere(0.17, (0.2 + k * 0.4, 3.68, 3.0 + 0.4 * math.sin(k * 1.3)), (1, 0.2, 1),
               glow(["#f2b04a", "#6fc3c0", "#ffe066"][k % 3], 4.0, f"blip{k}"))
    # shelves with books and jars
    shelf = wood("#c58b4e", "#9a6634", "shelf", 4.0)
    for z in (1.4, 2.1):
        box((2.2, 0.4, 0.06), (3.6, 3.65, z), material=shelf, bevel=0.01)
        random.seed(int(z * 10))
        xx = 2.65
        while xx < 4.5:
            w = random.uniform(0.07, 0.13); hh = random.uniform(0.3, 0.45)
            box((w, 0.28, hh), (xx, 3.6, z + 0.03 + hh / 2), material=mat(f"bk{xx:.2f}", random.choice(["#d9534f", "#34425c", "#f2b04a", "#46965a", "#7c2533"]), rough=0.6), bevel=0.01)
            xx += w + 0.02
    # lab bench with glassware
    box((2.4, 0.9, 0.9), (-3.9, 0.2, 0.45), material=mat("bench", "#f6efe2", rough=0.4), bevel=0.04)
    box((2.5, 1.0, 0.06), (-3.9, 0.2, 0.93), material=mat("benchtop", "#34425c", rough=0.3), bevel=0.02)
    for k, c in enumerate(["#6fc3c0", "#f2b04a", "#d9534f"]):
        lathe([(0.0, 0.0), (0.14, 0.0), (0.15, 0.12), (0.06, 0.32), (0.05, 0.45), (0.0, 0.45)], 32, (-4.4 + k * 0.5, 0.2, 0.96), glass(), 1, f"flask{k}")
        lathe([(0.0, 0.0), (0.12, 0.0), (0.13, 0.1), (0.0, 0.1)], 32, (-4.4 + k * 0.5, 0.2, 0.97), glow(c, 1.5, f"liq{k}"), 1, f"liq{k}")
    pot_plant(3.2, 2.6, 1.1, 1); pot_plant(-4.5, -1.2, 0.9, 2); pot_plant(4.6, 1.0, 1.2, 3)
    # pedestal + giant brain model
    lathe([(0.0, 0.0), (0.55, 0.0), (0.55, 0.08), (0.38, 0.14), (0.34, 0.95), (0.48, 1.0), (0.48, 1.06), (0.0, 1.06)], 40,
          (1.0, 0.6, 0), mat("ped", "#f6efe2", rough=0.3, coat=0.4), 1, "pedestal")
    bparts = brain((1.0, 0.6, 1.06), 1.1, lit, "bigbrain")
    area_light((-4, -5, 6), (0.5, 0.5, 1.2), 1500, 4, "#fff0dc", "key")
    area_light((4, -3, 4), (0.5, 0.5, 1.2), 500, 4, "#dbe8ff", "fill")
    area_light((2.5, 3.0, 3.5), (1.0, 0.6, 1.6), 300, 1.5, "#ffd2b0", "rim")
    return bparts

def lab_angles(lit):
    lab(lit)
    angles = (("lab_wide", (0.2, -9.5, 2.6), (0.0, 0.5, 1.4), 30, 0),
              ("lab_mid", (-0.4, -5.0, 1.8), (0.4, 0.5, 1.2), 34, 0),
              ("lab_close", (0.6, -2.4, 1.85), (1.0, 0.6, 1.62), 45, 3.0))
    for name, loc, tgt, lens, fs in angles:
        if lit and name != "lab_close":
            continue
        for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(o)
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name + ("_lit" if lit else ""), 1080, 1920, 40)

def town(mode):
    """Night town. mode: 'west' (left district lit), 'east' (right district lit), 'all' (every window lit, dawn sky)."""
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    w = world_color(hexrgb("#1a2a4a" if mode != "all" else "#3a3f6a"), 0.5)
    plane(200, 200, (0, 0, 0), material=mat("street", "#2e3440", rough=0.6), name="ground")
    plane(4.0, 200, (0, 0, 0.01), material=mat("road", "#3b4252", rough=0.5), name="road")
    for k in range(-20, 30):
        box((0.12, 0.8, 0.01), (0, k * 2.0, 0.02), material=mat("stripe", "#e5c07b", rough=0.6), bevel=0)
    random.seed(4)
    cols = ["#d9a07a", "#b7c7d9", "#c98e8e", "#a7c4a0", "#e3c99a", "#9aa7c9"]
    on = glow("#ffcf73", 5.0, "win_on"); off = mat("win_off", "#1d2433", rough=0.2, coat=0.6)
    for side in (-1, 1):
        for i in range(7):
            yy = -2 + i * 3.4
            wdt = random.uniform(2.2, 3.0); dep = 2.6; hh = random.uniform(4.0, 8.5)
            cx = side * (2.6 + dep / 2 + random.uniform(0, 0.4))
            box((dep, wdt, hh), (cx, yy, hh / 2), material=mat(f"bld{side}{i}", random.choice(cols), rough=0.7), bevel=0.06)
            box((dep + 0.2, wdt + 0.2, 0.18), (cx, yy, hh + 0.09), material=mat("roof", "#4c566a"), bevel=0.03)
            fx = cx - side * (dep / 2 + 0.02)
            for fz in range(int((hh - 1.0) / 1.2)):
                for fy in (-0.55, 0.55):
                    district = "west" if side < 0 else "east"
                    lit = mode == "all" or (mode == district and random.random() < 0.85) or random.random() < 0.08
                    box((0.06, 0.55, 0.7), (fx, yy + fy * wdt / 2.6, 1.2 + fz * 1.2), material=on if lit else off, bevel=0.01)
    for k in range(6):                                             # street lamps
        yy = -1 + k * 4.5
        for side in (-1, 1):
            cylinder(0.05, 3.2, (side * 2.3, yy, 1.6), material=metal("#3b3f46", 0.4, "lamp"), verts=12)
            sphere(0.16, (side * 2.3, yy, 3.25), 1, glow("#ffe2a8", 8.0, "bulb"))
            d = bpy.data.lights.new(f"pl{k}{side}", "POINT"); d.energy = 120; d.color = hexrgb("#ffd59a")
            o = bpy.data.objects.new(f"pl{k}{side}", d); bpy.context.scene.collection.objects.link(o); o.location = (side * 2.3, yy, 3.0)
    moon = sphere(1.6, (-9, 70, 26), 1, glow("#f6efe2", 3.0, "moon"))
    d = bpy.data.lights.new("moon", "SUN"); d.energy = 0.6 if mode != "all" else 1.2; d.color = hexrgb("#a8c4ff")
    o = bpy.data.objects.new("moonl", d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (math.radians(55), 0, math.radians(20))
    camera((0.6, -9.5, 2.2), (0, 8, 2.6), lens=26, fstop=0)
    still(f"plate_town_{mode}", 1080, 1920, 40)

def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")

def book_tex(path):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (600, 800), "#7c2533"); d = ImageDraw.Draw(im)
    d.rectangle((30, 30, 570, 770), outline="#e6c27a", width=8)
    f = ImageFont.truetype(os.path.join(ROOT, "fonts", "DMSerifDisplay-Regular.ttf"), 180)
    d.text((300, 380), "1936", font=f, fill="#e6c27a", anchor="mm")
    f2 = ImageFont.truetype(os.path.join(ROOT, "fonts", "Poppins-ExtraBold.ttf"), 46)
    d.text((300, 560), "SELF-HELP", font=f2, fill="#efe3c8", anchor="mm")
    im.save(path)

lab_angles(False)
for m in ("west", "east", "all"):
    town(m)
for lit in (False,):
    prop_scene(); brain((0, 0, 0), 1.0, lit, "pb"); sprite_camera((0, 0, 0.45), 3.2, 0.9, 50, azimuth=-14)
    still("brain_lit" if lit else "brain", 700, 600, 32, transparent=True, crop=True)
prop_scene()
bt = os.path.join(ASSETS, "_book_cover.png"); book_tex(bt)
box((0.62, 0.86, 0.12), (0, 0, 0.06), (0, 0, 0), mat("pages", "#efe3c8", rough=0.7), bevel=0.01)
plane(0.6, 0.82, (0, 0, 0.125), material=paper(bt, 0.5, "cover"), name="cover")
camera((0.3, -1.4, 1.6), (0, 0, 0.06), lens=50, fstop=0)
still("book", 600, 700, 24, transparent=True, crop=True)
