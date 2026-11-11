# Long-form pilot sets (16:9): the island market (3 angles), central bank hall, vault, a 1600s goldsmith shop, plus prop cut-outs.
# Market props are the v3 ones (jobs/2026-11-08-m3/assets.py).
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



W, H = 1920, 1080          # long videos are 16:9

def shoot(name, loc, tgt, lens, fs=0, samples=40, fg_objs=None):
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)
    camera(loc, tgt, lens=lens, fstop=fs)
    still("plate_" + name, W, H, samples)
    if fg_objs:
        still("fg_" + name, W, H, 24, only=fg_objs)

def market_angles():
    reset(W, H, 30, 0.1, samples=40, bloom=0)
    counter = build_market()
    # landscape is wider: more of the town either side
    stall(-8.0, 1.5, "awning_green.png", None, 0.9); stall(8.2, 1.0, "awning_blue.png", None, 0.9)
    crate(-6.4, -0.6, 0.6); barrel(6.5, -0.4); basket(-6.0, -1.2, 6, 5); basket(7.0, -1.3, 5, 6)
    palm(-11.0, 4.0, 5.0, 5); palm(11.5, 3.0, 5.2, 6); palm(-9.5, 9.0, 4.4, 7); palm(10.0, 10.0, 4.6, 8)
    bunting(-5.0, -1.6, 2.0, 3.0); bunting(1.6, 5.0, 2.5, 3.0)
    shoot("market_wide", (0.4, -8.8, 1.75), (0, 0, 1.55), 24, 6.0, fg_objs=counter)
    shoot("market_mid", (-0.9, -6.3, 1.95), (0.1, 0, 1.6), 28, 4.0, fg_objs=counter)
    shoot("market_close", (0.5, -3.1, 2.0), (0.1, 0.1, 1.25), 32, 2.4, fg_objs=counter)

def bank():
    reset(W, H, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#f2e6d4"), 1.0)
    plane(30, 30, (0, 0, 0), material=paper(os.path.join(TEX, "floor_checker.png"), 0.3, "tiles"), name="tiles")
    box((30, 0.3, 9), (0, 5, 4.5), material=mat("wall", "#efe3cf", rough=0.7), bevel=0)
    marble = mat("marble", "#f7f2ea", rough=0.25, coat=0.4)
    for x in (-7.5, -4.5, -1.5, 1.5, 4.5, 7.5):
        cylinder(0.32, 5.6, (x, 4.4, 2.8), material=marble, verts=32)
        box((0.9, 0.9, 0.25), (x, 4.4, 5.65), material=marble); box((0.9, 0.9, 0.25), (x, 4.4, 0.12), material=marble)
    box((18, 0.6, 0.5), (0, 4.4, 6.0), material=marble)
    text3d("CENTRAL BANK", 0.75, (0, 4.05, 6.75), (90, 0, 0), metal("#c9a24a", 0.3, "sign"), font="serif", extrude=0.05)
    box((3.0, 0.9, 0.08), (0, 3.6, 0.04), material=mat("rug", "#7c2533", rough=0.9), bevel=0.01)
    # a teller desk with a glowing screen (for the "banks type money" chapter)
    dm = wood("#7a4a2a", "#55311a", "desk", 3.0)
    desk = [box((2.6, 0.9, 0.95), (2.6, 1.6, 0.475), material=dm, bevel=0.04),
            box((2.75, 1.0, 0.07), (2.6, 1.6, 0.985), material=wood("#9a6a40", "#6e4628", "desktop", 4.0), bevel=0.02)]
    desk.append(box((0.9, 0.06, 0.55), (2.6, 1.85, 1.38), (-8, 0, 0), material=plastic("#22262c", 0.4, "monitor"), bevel=0.02))
    desk.append(box((0.82, 0.02, 0.47), (2.6, 1.81, 1.38), (-8, 0, 0), material=glow("#9fe3df", 1.6, "screen"), bevel=0))
    area_light((-3, -4, 6), (0, 1, 1.5), 1800, 4, "#fff0dc", "key"); area_light((4, -2, 4), (0, 1, 1.5), 600, 4, "#dbe8ff", "fill")
    shoot("bank", (0, -8.5, 2.1), (0, 1.5, 2.9), 22, 0, 32)
    shoot("bank_desk", (0.6, -2.6, 1.75), (2.4, 1.6, 1.25), 30, 0, 32, fg_objs=desk[:2])

def vault():
    reset(W, H, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#3a2350"), 1.0)
    floor("#4a3060", rough=0.45)
    d = bpy.data.lights.new("spot", "SPOT"); d.energy = 9000; d.spot_size = math.radians(60); d.spot_blend = 0.6; d.color = hexrgb("#ffd9a8")
    o = bpy.data.objects.new("spot", d); bpy.context.scene.collection.objects.link(o); o.location = (0, -1.0, 7.5); look_at(o, (0, 0.5, 0))
    area_light((5, 4, 3), (0, 0, 1.5), 1200, 4, "#b98bff", "rim"); area_light((-5, 3, 4), (0, 2, 2), 900, 5, "#ff9a6b", "rim2")
    door = metal("#8a8f98", 0.3, "vault_door")
    cylinder(2.2, 0.5, (0, 4.5, 2.4), (90, 0, 0), door, verts=96, bevel=0.06)
    torus(2.0, 0.08, (0, 4.22, 2.4), (90, 0, 0), metal("#c9a24a", 0.3, "door_ring"))
    cylinder(0.35, 0.3, (0, 4.1, 2.4), (90, 0, 0), metal("#c9a24a", 0.3, "hub"), verts=48)
    for k in range(6):
        a = k / 6 * math.pi
        box((1.6, 0.08, 0.1), (0, 4.0, 2.4), (0, math.degrees(a), 0), metal("#c9a24a", 0.3, "spoke"), bevel=0.02)
    cash = paper(os.path.join(TEX, "note_100t.png"), 0.6, "cash_top")
    for x in (-4.2, -3.2, 3.2, 4.2):
        for z in range(4):
            box((0.8, 0.4, 0.22), (x, 2.2 + (z % 2) * 0.1, 0.11 + z * 0.23), material=cash, bevel=0.01)
    shoot("vault", (0, -7.5, 2.0), (0, 0.5, 1.9), 26, 0, 32)

def goldsmith():
    """A 1600s London goldsmith's shop: plank floor, plaster wall, shelves of gold, an iron strongbox, a counter."""
    reset(W, H, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#2a1c14"), 0.6)
    plane(30, 30, (0, 0, 0), material=wood("#8a6038", "#5e3e22", "planks", 1.2, 0.6), name="planks")
    box((16, 0.3, 6), (0, 3.2, 3), material=mat("plaster", "#e6d6b8", rough=0.85, noise_bump=0.15), bevel=0)
    for x in (-6, -2, 2, 6):                                   # timber beams
        box((0.28, 0.32, 6), (x, 3.0, 3), material=wood("#4a2e18", "#2e1a0c", "beam", 1.5), bevel=0.03)
    box((16, 0.34, 0.3), (0, 3.0, 4.2), material=wood("#4a2e18", "#2e1a0c", "beam", 1.5), bevel=0.03)
    gold = metal("#e0b040", 0.22, "gold")
    shelf_m = wood("#6e4626", "#4a2c16", "shelf", 3.0)
    for z in (1.4, 2.1, 2.8):
        box((3.2, 0.45, 0.07), (-2.6, 2.75, z), material=shelf_m, bevel=0.015)
        for k in range(6):
            n = 3 + (k * 7 + int(z * 10)) % 5
            for j in range(n):
                cylinder(0.075, 0.018, (-3.8 + k * 0.48, 2.7, z + 0.045 + j * 0.02), material=gold, verts=32, bevel=0.004)
    for k, (x, h) in enumerate(((-1.4, 0.35), (-1.1, 0.25))):  # goblets
        lathe([(0, 0), (0.09, 0), (0.09, 0.02), (0.02, 0.05), (0.02, 0.16), (0.08, 0.22), (0.1, 0.32), (0.0, 0.3)], 32,
              (x, 2.7, 2.135), gold, 1, f"goblet{k}")
    iron = metal("#3c4046", 0.45, "iron")
    sb = box((1.5, 0.9, 1.1), (2.9, 2.4, 0.55), material=iron, bevel=0.05)
    for z in (0.25, 0.85):
        box((1.54, 0.94, 0.07), (2.9, 2.4, z), material=metal("#2a2d31", 0.4, "band"), bevel=0.01)
    torus(0.12, 0.025, (2.9, 1.93, 0.62), (90, 0, 0), metal("#c9a24a", 0.3, "lockring"))
    text3d("THE GOLDEN KEY", 0.32, (0.9, 3.03, 3.55), (90, 0, 0), mat("sign_gold", "#c9a24a", rough=0.35, metal=1.0), font="serif", extrude=0.02)
    # the counter (foreground layer) with coin stacks and scales on top
    top_m = wood("#8a5a30", "#5e3a1c", "g_counter_top", 4.0)
    counter = [box((3.4, 0.9, 1.0), (0.4, 0.6, 0.5), material=wood("#6e4224", "#46280f", "g_counter", 3.0), bevel=0.05),
               box((3.6, 1.05, 0.08), (0.4, 0.58, 1.04), material=top_m, bevel=0.03)]
    for k, n in enumerate((6, 9, 4)):
        for j in range(n):
            counter.append(cylinder(0.08, 0.02, (-0.6 + k * 0.32, 0.45, 1.09 + j * 0.022), material=gold, verts=32, bevel=0.004))
    counter.append(cylinder(0.02, 0.5, (1.4, 0.55, 1.33), material=metal("#c9a24a", 0.3, "scale"), verts=16))
    counter.append(box((0.7, 0.03, 0.03), (1.4, 0.55, 1.57), material=metal("#c9a24a", 0.3, "scale"), bevel=0.005))
    for dx in (-0.33, 0.33):
        counter.append(cylinder(0.13, 0.02, (1.4 + dx, 0.55, 1.36), material=metal("#c9a24a", 0.3, "scale"), verts=32))
    area_light((-2.5, -3.5, 4.5), (0, 1, 1.2), 1300, 3.5, "#ffcf8a", "lamp_key")
    area_light((3.5, -1.5, 3.0), (0, 1.5, 1.2), 500, 3, "#ffb36b", "lamp_fill")
    area_light((0, 2.6, 5.5), (0, 3, 2), 400, 6, "#ffe2b0", "wall_wash")
    shoot("goldsmith_wide", (0.3, -6.8, 2.1), (0.2, 1.0, 1.65), 26, 0, 40, fg_objs=counter)
    shoot("goldsmith_mid", (-0.3, -3.9, 1.8), (0.5, 0.8, 1.45), 30, 3.0, 40, fg_objs=counter)

def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")

def props():
    gold = lambda: metal("#e0b040", 0.22, "gold")
    # coin (front view, slight tilt) and a coin stack
    prop_scene(); c = cylinder(0.3, 0.04, (0, 0, 0.3), (78, 0, 0), gold(), verts=64, bevel=0.012)
    torus(0.25, 0.012, (0, -0.02, 0.3), (78, 0, 0), gold())
    text3d("L", 0.26, (0, -0.03, 0.29), (78, 0, 0), mat("coin_mark", "#b88a20", rough=0.3, metal=1.0), font="serif", extrude=0.01)
    camera((0, -2.2, 0.62), (0, 0, 0.3), lens=60, fstop=0); still("coin", 500, 500, 28, transparent=True, crop=True)
    prop_scene()
    for j in range(9):
        cylinder(0.3, 0.05, (0.01 * math.sin(j * 2.1), 0.01 * math.cos(j * 1.7), 0.025 + j * 0.052), material=gold(), verts=64, bevel=0.01)
    sprite_camera((0, 0, 0.25), 2.3, 0.9, 55); still("coinstack", 500, 600, 28, transparent=True, crop=True)
    # gold bar
    prop_scene(); box((0.9, 0.42, 0.22), (0, 0, 0.11), material=gold(), bevel=0.05)
    text3d("999.9", 0.12, (0, 0, 0.225), (0, 0, 0), mat("bar_mark", "#b88a20", rough=0.3, metal=1.0), font="display", extrude=0.006)
    sprite_camera((0, 0, 0.1), 2.6, 1.3, 55); still("goldbar", 700, 500, 28, transparent=True, crop=True)
    # fish
    prop_scene()
    body = sphere(0.5, (0, 0, 0.3), (0.62, 0.17, 0.24), mat("fish", "#7fa8c4", rough=0.25, coat=0.6))
    cone(0.22, 0.32, (-0.42, 0, 0.3), (0, 90, 0), mat("fish_tail", "#5d89a8", rough=0.3))
    cone(0.08, 0.16, (0.0, 0, 0.47), (0, 0, 0), mat("fish_fin", "#5d89a8", rough=0.3))
    sphere(0.035, (0.22, -0.07, 0.36), 1, mat("fish_eye", "#111111", rough=0.1))
    camera((0, -2.2, 0.5), (0, 0, 0.3), lens=55, fstop=0); still("fish", 600, 400, 28, transparent=True, crop=True)
    # clay pot
    prop_scene(); lathe([(0, 0), (0.16, 0), (0.26, 0.12), (0.3, 0.3), (0.24, 0.48), (0.15, 0.56), (0.17, 0.62), (0.13, 0.6), (0.0, 0.6)],
                        40, (0, 0, 0), clay("#c8693a", "pot"), 1, "pot")
    sprite_camera((0, 0, 0.3), 2.4, 0.8, 55); still("pot", 500, 600, 28, transparent=True, crop=True)
    # cowrie shell
    prop_scene(); sphere(0.5, (0, 0, 0.2), (0.34, 0.22, 0.16), mat("shell", "#f3e7d3", rough=0.15, coat=1.0))
    box((0.24, 0.022, 0.02), (0, 0, 0.276), material=mat("shell_slit", "#8a6a4a", rough=0.4), bevel=0.008)
    for k in range(-5, 6):
        box((0.006, 0.05, 0.012), (k * 0.02, 0, 0.276), material=mat("shell_teeth", "#f7efe2", rough=0.2), bevel=0)
    sprite_camera((0, 0, 0.2), 1.6, 1.2, 55, azimuth=-10); still("shell", 500, 400, 28, transparent=True, crop=True)
    # salt sack
    prop_scene(); lathe([(0, 0), (0.28, 0.02), (0.36, 0.2), (0.34, 0.45), (0.18, 0.62), (0.12, 0.7), (0.17, 0.8), (0.0, 0.8)],
                        40, (0, 0, 0), mat("sack", "#d9c39a", rough=0.9, noise_bump=0.3), 1, "sack")
    torus(0.135, 0.022, (0, 0, 0.66), material=mat("rope", "#8a6a3a", rough=0.8))
    for k in range(7):
        sphere(0.05, (0.05 * math.cos(k), 0.05 * math.sin(k), 0.8 + 0.02 * (k % 3)), 1, mat("salt_grain", "#ffffff", rough=0.3))
    sprite_camera((0, 0, 0.35), 2.6, 0.6, 55, azimuth=0); still("salt", 500, 600, 28, transparent=True, crop=True)
    # goldsmith's receipt (paper money's ancestor)
    prop_scene(); banknote(os.path.join(TEX, "receipt.png"), loc=(0, 0, 0.5), rot=(84, 0, -8), w=1.2, bend=10)
    camera((0, -2.6, 0.6), (0, 0, 0.5), lens=55, fstop=0); still("receipt", 900, 650, 28, transparent=True, crop=True)
    prop_scene(); banknote(os.path.join(TEX, "receipt.png"), loc=(0, 0, 0), rot=(60, 20, 30), w=0.7); sprite_camera((0, 0, 0), 1.8, 0.4, 55)
    still("receipt_small", 500, 450, 24, transparent=True, crop=True)

market_angles()
bank()
vault()
goldsmith()
props()
