# v3 sets and cut-outs: a lively island market (stall, seller's counter as a foreground layer), bank hall, vault.
import math, os, random

def sunny(sky_top="#3f9be0", sky_horizon="#bfe4fb", sun=4.2):
    w = world_color(hexrgb(sky_horizon), 1.0)
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    coord = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(coord.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].color = (*hexrgb(sky_horizon), 1); ramp.color_ramp.elements[0].position = 0.5
    ramp.color_ramp.elements[1].color = (*hexrgb(sky_top), 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    d = bpy.data.lights.new("sun", "SUN"); d.energy = sun; d.angle = math.radians(6); d.color = hexrgb("#fff0d8")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(48), math.radians(-10), math.radians(-38))

def palm(x, y, h=4.2, seed=1):
    random.seed(seed)
    trunk_m = wood("#a07a52", "#7d5a3a", "trunk", 2.0, 0.8)
    leaf_m = plastic("#3f9a4a", 0.5, "palm_leaf")
    for i in range(9):
        t = i / 9
        cylinder(0.17 - 0.06 * t, h / 9 * 1.06, (x + 0.35 * t * t, y, h / 9 * (i + 0.5)), (0, 6 * t, 0), trunk_m, verts=16, bevel=0)
    top = (x + 0.35, y, h)
    for k in range(9):
        a = k / 9 * 2 * math.pi + random.uniform(-0.2, 0.2); L = random.uniform(1.4, 2.0)
        leaf = sphere(0.5, (top[0] + math.cos(a) * L * 0.5, top[1] + math.sin(a) * L * 0.5, top[2] - 0.25), (L * 0.55, 0.24, 0.04), leaf_m)
        leaf.rotation_euler = (0, math.radians(25), a)

def basket(x, y, n=7, seed=0):
    random.seed(seed)
    b = lathe([(0.0, 0.0), (0.22, 0.0), (0.3, 0.08), (0.33, 0.22), (0.31, 0.24), (0.27, 0.06), (0.0, 0.04)], 32, (x, y, 0),
              wood("#c99a5b", "#9c7040", "basket", 30.0, 0.7), 1, "basket")
    for k in range(n):
        a = k / n * 2 * math.pi
        apple2((x + 0.13 * math.cos(a), y + 0.13 * math.sin(a), 0.1), 0.075, f"bapple{seed}_{k}",
               red=random.choice(["#b3121b", "#c22a1a", "#9e1420"]))
    apple2((x, y, 0.16), 0.075, f"bapple{seed}_top")

def crate(x, y, rot=0, h=0.4):
    m = wood("#b8864e", "#8a6036", "crate", 4.0)
    box((0.6, 0.45, h), (x, y, h / 2), (0, 0, rot), m, bevel=0.025)
    for dz in (0.1, 0.3):
        box((0.62, 0.47, 0.035), (x, y, dz * h / 0.4), (0, 0, rot), wood("#9c6c3c", "#7a5230", "crate_slat", 4.0), bevel=0.01)

def barrel(x, y):
    lathe([(0.0, 0.0), (0.28, 0.0), (0.34, 0.25), (0.35, 0.4), (0.34, 0.55), (0.28, 0.8), (0.0, 0.8)], 32, (x, y, 0),
          wood("#9c6a3a", "#6e4624", "barrel", 2.0), 1, "barrel")
    for z in (0.12, 0.68):
        torus(0.3, 0.015, (x, y, z), material=metal("#5a5f66", 0.4, "hoop"))

def stall(x, y, stripes="awning_stripes.png", sign=None, scale=1.0):
    """A rounded market stall. Returns the counter objects (for the foreground layer)."""
    s = scale
    top_m = wood("#c58b4e", "#9a6634", "counter_top", 5.0)
    body_m = wood("#9a6436", "#6e4424", "counter_body", 3.0)
    post_m = wood("#8a5a30", "#5e3a1c", "post", 2.0)
    counter = [box((2.5 * s, 1.0 * s, 0.86 * s), (x, y, 0.43 * s), material=body_m, bevel=0.06 * s),
               box((2.7 * s, 1.16 * s, 0.09 * s), (x, y - 0.02 * s, 0.905 * s), material=top_m, bevel=0.035 * s)]
    for k in range(5):                                       # front planks
        counter.append(box((0.03 * s, 0.03 * s, 0.7 * s), (x - 1.0 * s + k * 0.5 * s, y - 0.505 * s, 0.43 * s), material=post_m, bevel=0.01 * s))
    for sx in (-1.18, 1.18):
        for sy in (-0.45, 0.45):
            cylinder(0.055 * s, 2.4 * s, (x + sx * s, y + sy * s, 1.2 * s), material=post_m, verts=20, bevel=0.01)
    aw = paper(os.path.join(TEX, stripes), 0.6, f"awning_{stripes}")
    box((2.8 * s, 1.4 * s, 0.05 * s), (x, y - 0.12 * s, 2.42 * s), (14, 0, 0), material=aw, bevel=0.015 * s)
    for k in range(13):                                      # scalloped valance
        xx = x - 1.38 * s + k * 0.23 * s
        cylinder(0.115 * s, 0.03 * s, (xx, y - 0.81 * s, 2.25 * s), (90, 0, 0),
                 material=mat("val_r" if k % 2 == 0 else "val_w", "#d6483e" if k % 2 == 0 and "stripes" in stripes else
                              ("#4682b4" if k % 2 == 0 and "blue" in stripes else ("#46965a" if k % 2 == 0 else "#f6efe2")), rough=0.6),
                 verts=24, bevel=0)
    if sign:
        board = box((1.3 * s, 0.06 * s, 0.32 * s), (x, y - 0.55 * s, 2.82 * s), material=wood("#efe0c0", "#d8c49c", "board", 3.0), bevel=0.02 * s)
        text3d(sign, 0.2 * s, (x, y - 0.6 * s, 2.82 * s), (90, 0, 0), mat("sign_ink", "#7c2533", rough=0.5), font="display", extrude=0.01)
    return counter

def bunting(x0, x1, y, z, colors=("#d6483e", "#f2b04a", "#6fc3c0", "#46965a")):
    n = 14
    for k in range(n):
        t = k / (n - 1); xx = x0 + (x1 - x0) * t; zz = z - 0.35 * math.sin(math.pi * t)
        cone(0.12, 0.22, (xx, y, zz - 0.11), (0, 180, 0), mat(f"flag{k%4}", colors[k % 4], rough=0.6))

def build_market():
    sunny()
    plane(400, 400, (0, 0, 0), material=mat("sand", "#efd3a0", rough=0.9, noise_bump=0.1), name="sand")
    plane(400, 160, (0, 115, 0.04), material=mat("sea", "#1f8fbf", rough=0.05, coat=0.8), name="sea")
    counter = stall(0.0, 0.0, "awning_stripes.png", "FRESH APPLES")
    stall(-4.2, 3.2, "awning_blue.png", None, 0.9)
    stall(4.0, 4.0, "awning_green.png", None, 0.9)
    for i in range(10):                                       # the ten apples on display, two rows
        row, col = divmod(i, 5)
        apple2((-0.55 + col * 0.27 + (0.13 if row else 0), 0.12 + row * 0.2, 0.95), 0.085, f"disp{i}")
    basket(-1.75, -0.3, 7, 1); basket(1.7, -0.45, 6, 2)
    crate(1.9, 0.55, 0.3); crate(1.9, 0.55, 0.3, 0.8)
    barrel(-2.0, 0.8)
    bunting(-1.4, 1.4, -0.65, 3.25)
    palm(-3.6, 5.5, 4.6, 1); palm(3.2, 8.0, 5.2, 2); palm(-7.0, 10.0, 5.4, 3); palm(7.5, 6.0, 4.8, 4)
    return counter

def market_angles():
    counter = build_market()
    for name, loc, tgt, lens, fs in (("market_wide", (0.5, -9.8, 2.7), (0, 0, 1.35), 30, 6.0),
                                     ("market_mid", (-0.7, -4.8, 1.8), (0.15, 0, 1.08), 34, 4.0),
                                     ("market_close", (0.45, -2.5, 2.05), (0.05, 0.05, 1.0), 40, 2.4)):
        for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(o)
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=counter)

def bank():
    reset(1080, 1920, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#f2e6d4"), 1.0)
    plane(30, 30, (0, 0, 0), material=paper(os.path.join(TEX, "floor_checker.png"), 0.3, "tiles"), name="tiles")
    box((30, 0.3, 9), (0, 5, 4.5), material=mat("wall", "#efe3cf", rough=0.7), bevel=0)
    marble = mat("marble", "#f7f2ea", rough=0.25, coat=0.4)
    for x in (-4.5, -1.5, 1.5, 4.5):
        cylinder(0.32, 5.6, (x, 4.4, 2.8), material=marble, verts=32)
        box((0.9, 0.9, 0.25), (x, 4.4, 5.65), material=marble); box((0.9, 0.9, 0.25), (x, 4.4, 0.12), material=marble)
    box((12, 0.6, 0.5), (0, 4.4, 6.0), material=marble)
    text3d("CENTRAL BANK", 0.85, (0, 4.05, 6.75), (90, 0, 0), metal("#c9a24a", 0.3, "sign"), font="serif", extrude=0.05)
    box((3.0, 0.9, 0.08), (0, 3.6, 0.04), material=mat("rug", "#7c2533", rough=0.9), bevel=0.01)
    area_light((-3, -4, 6), (0, 1, 1.5), 1600, 4, "#fff0dc", "key"); area_light((4, -2, 4), (0, 1, 1.5), 500, 4, "#dbe8ff", "fill")
    camera((0, -7.5, 2.4), (0, 1.5, 1.6), lens=30, fstop=0)
    still("plate_bank", 1080, 1920, 32)

def vault():
    reset(1080, 1920, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#3a2350"), 1.0)
    floor("#4a3060", rough=0.45)
    d = bpy.data.lights.new("spot", "SPOT"); d.energy = 9000; d.spot_size = math.radians(50); d.spot_blend = 0.6; d.color = hexrgb("#ffd9a8")
    o = bpy.data.objects.new("spot", d); bpy.context.scene.collection.objects.link(o); o.location = (0, -1.0, 7.5); look_at(o, (0, 0.5, 0))
    area_light((4, 4, 3), (0, 0, 1.5), 1200, 4, "#b98bff", "rim"); area_light((-4, 3, 4), (0, 2, 2), 900, 5, "#ff9a6b", "rim2")
    camera((0, -7.0, 2.0), (0, 0.5, 1.5), lens=32, fstop=0)
    still("plate_vault", 1080, 1920, 32)

def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")

reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
market_angles()
bank()
vault()
prop_scene(); apple2((0, 0, 0), 0.16, "hero_apple"); sprite_camera((0, 0, 0.16), 1.6, 0.5, 60); still("apple", 500, 500, 28, transparent=True, crop=True)
prop_scene()
for k in range(10):
    banknote(loc=(0, 0, 0.004 + k * 0.006), rot=(0, 0, 3 * math.sin(k * 1.7)), w=0.7, name=f"n{k}")
sprite_camera((0, 0, 0.03), 1.7, 0.85, 55); still("stack10", 700, 500, 24, transparent=True, crop=True)
prop_scene(); banknote(loc=(0, 0, 0), rot=(70, 0, -12), w=0.7); sprite_camera((0, 0, 0), 1.7, 0.3, 55); still("bill", 600, 500, 24, transparent=True, crop=True)
prop_scene(); pr, slot = printer((0, 0, 0), 1.0); sprite_camera((0, 0, 0.7), 4.6, 1.6, 50, azimuth=-22); still("printer", 900, 900, 28, transparent=True, crop=True)
for side in ("1", "2"):
    prop_scene(); price_tag(os.path.join(TEX, f"tag_{side}.png"), None, loc=(0, 0, 0.3), w=0.5)
    camera((0, -1.6, 0.42), (0, 0, 0.3), lens=60, fstop=0); still(f"tag_{side}", 600, 450, 24, transparent=True, crop=True)
prop_scene(); banknote(os.path.join(TEX, "note_100t.png"), loc=(0, 0, 0.5), rot=(84, 0, -10), w=1.4, bend=14)
camera((0, -2.6, 0.62), (0, 0, 0.5), lens=55, fstop=0); still("note_100t", 1000, 600, 28, transparent=True, crop=True)
prop_scene(); banknote(os.path.join(TEX, "note_100t.png"), loc=(0, 0, 0), rot=(60, 20, 30), w=0.7); sprite_camera((0, 0, 0), 1.8, 0.4, 55); still("bill_100t", 500, 500, 24, transparent=True, crop=True)
