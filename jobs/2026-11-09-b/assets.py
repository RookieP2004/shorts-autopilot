# 2026-11-09-b sets and cut-outs: a warm town-bank hall (teller counter as foreground layer, round vault door),
# a sunny bakery street (bread stall, little houses), and props: gold coin, coin pile, loaf, brick oven.
import math, os, random


def sunny(sky_top="#3f9be0", sky_horizon="#cfe9fb", sun=4.0):
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


GOLD = None


def gold():
    m = bpy.data.materials.get("coin_gold")
    return m or metal("#e2b041", 0.22, "coin_gold")


def coin(loc, rot=(0, 0, 0), r=0.1, name="coin"):
    c = cylinder(r, r * 0.16, loc, rot, gold(), verts=40, bevel=r * 0.03, name=name)
    torus(r * 0.82, r * 0.05, (0, 0, r * 0.08), material=gold()).parent = c
    torus(r * 0.82, r * 0.05, (0, 0, -r * 0.08), material=gold()).parent = c
    return c


def coin_pile(x, y, n=40, spread=0.32, seed=3, r=0.07):
    random.seed(seed)
    out = []
    for k in range(n):
        a = random.uniform(0, 2 * math.pi); d = spread * math.sqrt(random.random())
        z = max(0.0, (spread - d) * 1.3) + random.uniform(0, 0.03)
        out.append(coin((x + d * math.cos(a), y + d * math.sin(a), z + r * 0.08),
                        (random.uniform(-25, 25), random.uniform(-25, 25), random.uniform(0, 360)), r, f"pc{seed}_{k}"))
    return out


def coin_stack(x, y, n=8, r=0.08, seed=0):
    random.seed(seed)
    return [coin((x + random.uniform(-0.006, 0.006), y + random.uniform(-0.006, 0.006), r * 0.08 + k * r * 0.17),
                 (0, 0, random.uniform(0, 360)), r, f"st{seed}_{k}") for k in range(n)]


def bread_mat():
    m = bpy.data.materials.get("bread")
    return m or mat("bread", "#b8742e", rough=0.6, coat=0.1, noise_bump=0.2)


def loaf(loc, r=0.16, rot=0, name="loaf"):
    x, y, z = loc
    hz = 0.42
    o = sphere(r, (x, y, z + r * hz), (1.0, 0.58, hz), bread_mat(), name=name)
    o.rotation_euler = (0, 0, math.radians(rot))
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    cm = bpy.data.materials.get("crust") or mat("crust", "#f3d39a", rough=0.8)
    for k in range(3):                                     # scored top
        dx = (k - 1) * r * 0.45
        box((r * 0.09, r * 0.62, r * 0.05), (x + dx * ca, y + dx * sa, z + r * hz * 1.95), (0, 0, rot + 25), cm, bevel=0.004)
    return o


def oven(x, y, s=1.0):
    """A rounded brick bread oven with a glowing mouth."""
    brick = mat("oven_brick", "#a84a2a", rough=0.75, noise_bump=0.3)
    base = box((1.4 * s, 1.3 * s, 0.6 * s), (x, y, 0.3 * s), material=mat("oven_base", "#9a8a78", rough=0.85, noise_bump=0.2), bevel=0.06 * s)
    dome = lathe([(0.0, 0.0), (0.62, 0.0), (0.64, 0.2), (0.58, 0.45), (0.42, 0.68), (0.2, 0.8), (0.0, 0.82)], 40,
                 (x, y, 0.6 * s), brick, 1, "oven_dome")
    dome.scale = (s, s, s)
    mouth = cylinder(0.26 * s, 0.1 * s, (x, y - 0.6 * s, 0.82 * s), (90, 0, 0), mat("oven_mouth", "#2a120a", emit="#ff5a14", emit_strength=1.1), verts=32)
    rim = torus(0.29 * s, 0.05 * s, (x, y - 0.63 * s, 0.82 * s), (90, 0, 0), mat("oven_rim", "#e8d6b8", rough=0.6))
    chim = cylinder(0.1 * s, 0.5 * s, (x + 0.2 * s, y + 0.2 * s, 1.5 * s), material=brick, verts=20)
    return [base, dome, mouth, rim, chim]


def stall(x, y, stripes="awning_stripes.png", sign=None, scale=1.0):
    s = scale
    top_m = wood("#c58b4e", "#9a6634", "counter_top", 5.0)
    body_m = wood("#9a6436", "#6e4424", "counter_body", 3.0)
    post_m = wood("#8a5a30", "#5e3a1c", "post", 2.0)
    counter = [box((2.5 * s, 1.0 * s, 0.86 * s), (x, y, 0.43 * s), material=body_m, bevel=0.06 * s),
               box((2.7 * s, 1.16 * s, 0.09 * s), (x, y - 0.02 * s, 0.905 * s), material=top_m, bevel=0.035 * s)]
    for k in range(5):
        counter.append(box((0.03 * s, 0.03 * s, 0.7 * s), (x - 1.0 * s + k * 0.5 * s, y - 0.505 * s, 0.43 * s), material=post_m, bevel=0.01 * s))
    for sx in (-1.18, 1.18):
        for sy in (-0.45, 0.45):
            cylinder(0.055 * s, 2.4 * s, (x + sx * s, y + sy * s, 1.2 * s), material=post_m, verts=20, bevel=0.01)
    aw = paper(os.path.join(TEX, stripes), 0.6, f"awning_{stripes}")
    box((2.8 * s, 1.4 * s, 0.05 * s), (x, y - 0.12 * s, 2.42 * s), (14, 0, 0), material=aw, bevel=0.015 * s)
    for k in range(13):
        xx = x - 1.38 * s + k * 0.23 * s
        cylinder(0.115 * s, 0.03 * s, (xx, y - 0.81 * s, 2.25 * s), (90, 0, 0),
                 material=mat("val_r" if k % 2 == 0 else "val_w", "#d6483e" if k % 2 == 0 else "#f6efe2", rough=0.6), verts=24, bevel=0)
    if sign:
        box((1.4 * s, 0.06 * s, 0.32 * s), (x, y - 0.55 * s, 2.82 * s), material=wood("#efe0c0", "#d8c49c", "board", 3.0), bevel=0.02 * s)
        text3d(sign, 0.2 * s, (x, y - 0.6 * s, 2.82 * s), (90, 0, 0), mat("sign_ink", "#7c2533", rough=0.5), font="display", extrude=0.01)
    return counter


def house(x, y, w, h, color, roof="#b5533c", seed=0):
    random.seed(seed)
    box((w, 2.2, h), (x, y, h / 2), material=mat(f"house{seed}", color, rough=0.8, noise_bump=0.08), bevel=0.05)
    r = box((w * 1.08, 2.4, 0.5), (x, y, h + 0.2), material=mat(f"roof{seed}", roof, rough=0.7), bevel=0.12)
    win = mat("win", "#8fd0e8", rough=0.1, coat=0.6); frame = mat("winframe", "#f6efe2", rough=0.6)
    for k in range(max(1, int(w // 1.3))):
        wx = x - w / 2 + 0.75 + k * 1.3
        for wz in (h * 0.35, h * 0.72):
            if wz + 0.4 < h:
                box((0.62, 0.06, 0.74), (wx, y - 1.11, wz), material=frame, bevel=0.02)
                box((0.5, 0.08, 0.62), (wx, y - 1.12, wz), material=win, bevel=0.01)


def tree(x, y, h=3.2, seed=0):
    random.seed(seed)
    cylinder(0.12, h * 0.55, (x, y, h * 0.27), material=wood("#7d5a3a", "#5a3e26", "tree_trunk", 2.0), verts=14)
    leaf = mat(f"leaf{seed%3}", ["#4f9e4a", "#5aa84f", "#3f8f45"][seed % 3], rough=0.7, noise_bump=0.2)
    for k in range(5):
        sphere(random.uniform(0.6, 0.85), (x + random.uniform(-0.4, 0.4), y + random.uniform(-0.3, 0.3), h * 0.68 + random.uniform(-0.2, 0.5)), 1, leaf, seg=24)


def bunting(x0, x1, y, z, colors=("#d6483e", "#f2b04a", "#6fc3c0", "#46965a")):
    n = 14
    for k in range(n):
        t = k / (n - 1); xx = x0 + (x1 - x0) * t; zz = z - 0.35 * math.sin(math.pi * t)
        cone(0.12, 0.22, (xx, y, zz - 0.11), (0, 180, 0), mat(f"flag{k%4}", colors[k % 4], rough=0.6))


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


# ---------------------------------------------------------------- bank hall
def build_bank():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#f2e6d4"), 1.0)
    plane(40, 40, (0, 0, 0), material=paper(os.path.join(TEX, "floor_checker.png"), 0.3, "tiles"), name="tiles")
    box((30, 0.3, 9), (0, 5, 4.5), material=mat("wall", "#efe3cf", rough=0.7), bevel=0)
    box((30, 0.1, 1.3), (0, 4.82, 0.65), material=mat("wainscot", "#3d7f7c", rough=0.5, coat=0.3), bevel=0.02)
    box((30, 0.14, 0.08), (0, 4.8, 1.32), material=metal("#c9a24a", 0.3, "trim"), bevel=0.01)
    box((6.0, 3.2, 0.02), (-1.2, -1.2, 0.01), material=mat("rug", "#7c2533", rough=0.9), bevel=0.005)
    box((5.6, 2.8, 0.025), (-1.2, -1.2, 0.012), material=mat("rug_in", "#a8423a", rough=0.9), bevel=0.005)
    box((0.3, 20, 9), (-7.5, -2, 4.5), material=mat("wall_l", "#e8d9c0", rough=0.7), bevel=0)
    marble = mat("marble", "#f7f2ea", rough=0.25, coat=0.4)
    for x in (-5.5, -2.0):
        cylinder(0.32, 5.6, (x, 4.4, 2.8), material=marble, verts=32)
        box((0.9, 0.9, 0.25), (x, 4.4, 5.65), material=marble); box((0.9, 0.9, 0.25), (x, 4.4, 0.12), material=marble)
    box((14, 0.6, 0.5), (0, 4.4, 6.0), material=marble)
    text3d("TOWN BANK", 0.8, (-0.6, 4.05, 6.75), (90, 0, 0), metal("#c9a24a", 0.3, "sign"), font="serif", extrude=0.05)
    # round vault door on the back wall, right side
    steel = metal("#9aa3ab", 0.3, "steel"); brass = metal("#c9a24a", 0.25, "brass")
    cylinder(1.55, 0.25, (2.2, 4.78, 1.75), (90, 0, 0), mat("vault_frame", "#5a6068", rough=0.4, metal=0.8), verts=64)
    cylinder(1.35, 0.3, (2.2, 4.6, 1.75), (90, 0, 0), steel, verts=64)
    for k in range(3):
        torus(1.1 - k * 0.32, 0.03, (2.2, 4.43, 1.75), (90, 0, 0), mat("vault_ring", "#7d858d", metal=0.9, rough=0.35))
    cylinder(0.16, 0.12, (2.2, 4.38, 1.75), (90, 0, 0), brass, verts=32)
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        cylinder(0.035, 0.85, (2.2 + 0.42 * math.cos(a), 4.34, 1.75 + 0.42 * math.sin(a)), (0, 90 - math.degrees(a), 0), brass, verts=12)
        cylinder(0.07, 0.07, (2.2 + 0.85 * math.cos(a), 4.34, 1.75 + 0.85 * math.sin(a)), (90, 0, 0), brass, verts=16)
    pile = coin_pile(1.6, 3.7, 90, 0.5, 5) + coin_pile(2.85, 3.85, 60, 0.4, 6)
    # teller counter (foreground layer)
    top_m = mat("counter_marble", "#f2ebdf", rough=0.2, coat=0.5)
    body_m = wood("#8a4f2c", "#5e321a", "teller_wood", 3.0)
    counter = [box((3.2, 0.9, 1.05), (-1.4, 0.6, 0.525), material=body_m, bevel=0.05),
               box((3.4, 1.05, 0.08), (-1.4, 0.58, 1.09), material=top_m, bevel=0.03)]
    for k in range(4):
        counter.append(box((0.6, 0.04, 0.7), (-2.6 + k * 0.8, 0.13, 0.52), material=wood("#9c5e36", "#6e3e20", "panel", 3.0), bevel=0.03))
    for k in range(7):                                        # brass grille
        counter.append(cylinder(0.018, 0.75, (-2.9 + k * 0.5, 0.75, 1.5), material=brass, verts=10, bevel=0))
    counter.append(box((3.1, 0.05, 0.05), (-1.4, 0.75, 1.88), material=brass, bevel=0.01))
    lampm = mat("lamp", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    for x in (-2.6, -0.2):
        sphere(0.13, (x, 0.85, 2.05), 1, lampm, seg=24)
    plant = mat("plant", "#4f9e4a", rough=0.6)
    for px in (-6.4, 5.8):
        lathe([(0, 0), (0.3, 0), (0.38, 0.55), (0.0, 0.55)], 32, (px, 3.2, 0), mat("pot", "#c4623a", rough=0.6), 1, "pot")
        for k in range(6):
            sphere(0.35, (px + random.uniform(-0.25, 0.25), 3.2 + random.uniform(-0.2, 0.2), 0.9 + k * 0.12), 1, plant, seg=20)
    area_light((-3, -4, 6), (0, 1, 1.5), 1700, 4, "#fff0dc", "key"); area_light((4, -2, 4), (0, 1, 1.5), 520, 4, "#dbe8ff", "fill")
    area_light((2.2, 2.0, 4.0), (2.2, 4.5, 1.5), 300, 2, "#ffd9a8", "vault_spot")
    return counter


def bank_angles():
    counter = build_bank()
    for name, loc, tgt, lens, fs in (("bank_wide", (-0.4, -9.5, 2.5), (-0.4, 1.5, 1.6), 26, 6.0),
                                     ("bank_mid", (-1.0, -4.4, 1.75), (-1.3, 0.8, 1.2), 34, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=counter)
    drop_cams(); camera((1.6, -1.6, 1.5), (2.2, 4.0, 1.3), lens=36, fstop=3.0)
    still("plate_bank_vault", 1080, 1920, 40)


# ---------------------------------------------------------------- bakery street
def bakery_angles():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny()
    plane(400, 400, (0, 0, 0), material=mat("street", "#d9c4a0", rough=0.9, noise_bump=0.12), name="street")
    counter = stall(0.0, 0.0, "awning_stripes.png", "FRESH BREAD")
    for i in range(7):
        loaf((-0.85 + i * 0.28, 0.1 + (i % 2) * 0.18, 0.95), 0.14, 10 * (i % 3) - 10, f"disp{i}")
    for k in range(4):                                         # bread basket each side
        loaf((-1.85 + k * 0.08, -0.35 + (k % 2) * 0.1, 0.45 + k * 0.05), 0.14, 40 * k, f"bl{k}")
    box((0.6, 0.45, 0.42), (-1.85, -0.3, 0.21), material=wood("#b8864e", "#8a6036", "crate", 4.0), bevel=0.025)
    bunting(-1.4, 1.4, -0.65, 3.25)
    house(-4.6, 5.6, 4.0, 4.6, "#f2c88a", "#b5533c", 1)
    house(0.2, 7.2, 4.4, 5.8, "#e8a39a", "#7c2533", 2)
    house(5.0, 5.8, 4.0, 4.2, "#a8d5d1", "#34425c", 3)
    house(-9.0, 9.0, 4.0, 5.4, "#d9c6ea", "#6b4c8a", 4)
    house(9.5, 9.5, 4.5, 5.0, "#f6e3a8", "#b5533c", 5)
    tree(-2.6, 3.4, 3.4, 1); tree(3.0, 3.2, 3.0, 2); tree(7.4, 3.8, 3.6, 3)
    for name, loc, tgt, lens, fs in (("bakery_wide", (0.4, -9.8, 2.7), (0.2, 0, 1.35), 30, 6.0),
                                     ("bakery_mid", (-0.7, -4.8, 1.8), (0.15, 0, 1.08), 34, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=counter)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    bank_angles()
    bakery_angles()
prop_scene(); coin((0, 0, 0.2), (80, 0, -15), 0.2, "hero_coin"); camera((0, -1.8, 0.3), (0, 0, 0.2), lens=60, fstop=0)
still("coin", 400, 400, 24, transparent=True, crop=True)
prop_scene(); coin_pile(0, 0, 130, 0.38, 9, 0.07); sprite_camera((0, 0, 0.12), 2.2, 1.1, 55); still("coin_pile", 700, 500, 28, transparent=True, crop=True)
prop_scene(); coin_stack(0, 0, 9, 0.12, 2); sprite_camera((0, 0, 0.1), 1.4, 0.55, 55); still("coin_stack", 400, 500, 24, transparent=True, crop=True)
prop_scene(); loaf((0, 0, 0), 0.3, 15, "hero_loaf"); sprite_camera((0, 0, 0.12), 1.8, 0.6, 55); still("loaf", 500, 400, 24, transparent=True, crop=True)
prop_scene(); oven(0, 0, 1.0); sprite_camera((0, 0, 0.8), 6.5, 1.1, 45, azimuth=-15); still("oven", 800, 800, 28, transparent=True, crop=True)
