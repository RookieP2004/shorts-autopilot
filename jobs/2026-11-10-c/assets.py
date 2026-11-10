# 2026-11-10-c sets and cut-outs: a sunny village pasture shared by everyone (rolling green meadow full of grass tufts,
# a wooden fence, a red barn, trees and hills), the same pasture grazed bare (brown dirt, dry stubble, rocks), and props:
# a black-and-white cow, a brown cow, a wooden rules sign, a milk can.
import math, os, random


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def sunny(sky_top="#3f9be0", sky_horizon="#d4ecfb", sun=4.2):
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


def tree(x, y, h=3.2, seed=0, bare=False):
    random.seed(seed)
    cylinder(0.13, h * 0.55, (x, y, h * 0.27), material=wood("#7d5a3a", "#5a3e26", "tree_trunk", 2.0), verts=14)
    cols = ["#4f9e4a", "#5aa84f", "#3f8f45"] if not bare else ["#8f9a4a", "#9c8f48", "#7f8a42"]
    leaf = mat(f"leaf{seed%3}{'b' if bare else ''}", cols[seed % 3], rough=0.7, noise_bump=0.2)
    for k in range(5):
        sphere(random.uniform(0.6, 0.85), (x + random.uniform(-0.4, 0.4), y + random.uniform(-0.3, 0.3),
                                           h * 0.68 + random.uniform(-0.2, 0.5)), 1, leaf, seg=24)


def barn(x, y, s=1.0):
    red = mat("barn_red", "#b5402f", rough=0.75, noise_bump=0.1)
    white = mat("barn_white", "#f6efe2", rough=0.6)
    box((3.2 * s, 2.6 * s, 2.4 * s), (x, y, 1.2 * s), material=red, bevel=0.05)
    # gable roof from two slabs
    for sgn in (-1, 1):
        box((1.95 * s, 2.9 * s, 0.14 * s), (x + sgn * 0.82 * s, y, 2.95 * s), (0, sgn * 33, 0),
            mat("barn_roof", "#5a3b2e", rough=0.7), bevel=0.03)
    box((3.0 * s, 0.1, 1.2 * s), (x, y - 1.31 * s, 2.6 * s), material=red, bevel=0.02)
    box((1.2 * s, 0.08, 1.6 * s), (x, y - 1.33 * s, 0.8 * s), material=white, bevel=0.02)
    box((1.0 * s, 0.1, 1.4 * s), (x, y - 1.35 * s, 0.8 * s), material=mat("barn_door", "#8f2f22", rough=0.7), bevel=0.02)
    for a in (45, -45):
        box((1.5 * s, 0.12, 0.08 * s), (x, y - 1.4 * s, 0.8 * s), (0, a, 0), white, bevel=0.01)


def fence(x0, x1, y, name="fence"):
    post = wood("#9a6a3c", "#6e4424", "fence_post", 2.0)
    rail = wood("#b58250", "#8a5a30", "fence_rail", 4.0)
    out = []
    n = max(2, int(abs(x1 - x0) / 1.6) + 1)
    for k in range(n):
        xx = x0 + (x1 - x0) * k / (n - 1)
        out.append(box((0.14, 0.14, 1.15), (xx, y, 0.57), (0, 0, random.uniform(-4, 4)), post, bevel=0.03))
    for z in (0.45, 0.9):
        out.append(box((abs(x1 - x0) + 0.2, 0.07, 0.12), ((x0 + x1) / 2, y - 0.08, z), material=rail, bevel=0.025))
    return out


def tufts(n, x0, x1, y0, y1, bare=False, seed=1):
    random.seed(seed)
    g = [mat("tuft_a", "#5fb04e", rough=0.6), mat("tuft_b", "#4c9a43", rough=0.6), mat("tuft_c", "#78c25a", rough=0.6)]
    d = [mat("dry_a", "#b89b5a", rough=0.8), mat("dry_b", "#9c8048", rough=0.8)]
    for k in range(n):
        x = random.uniform(x0, x1); y = random.uniform(y0, y1)
        m = random.choice(d if bare else g)
        hh = random.uniform(0.12, 0.26) * (0.45 if bare else 1.0)
        for j in range(3):
            cone(0.035, hh, (x + random.uniform(-0.05, 0.05), y + random.uniform(-0.05, 0.05), hh / 2),
                 (random.uniform(-18, 18), random.uniform(-18, 18), 0), m)


def flowers(n, x0, x1, y0, y1, seed=4):
    random.seed(seed)
    cols = [mat("fl_y", "#f7d046", rough=0.5), mat("fl_w", "#fbf6ec", rough=0.5), mat("fl_p", "#e98bb0", rough=0.5)]
    for k in range(n):
        sphere(0.045, (random.uniform(x0, x1), random.uniform(y0, y1), 0.12), 1, random.choice(cols), seg=12)


def rocks(n, x0, x1, y0, y1, seed=7):
    random.seed(seed)
    m = mat("rock", "#8d877c", rough=0.85, noise_bump=0.3)
    for k in range(n):
        r = random.uniform(0.08, 0.22)
        sphere(r, (random.uniform(x0, x1), random.uniform(y0, y1), r * 0.3), (1.2, 1.0, 0.6), m, seg=16)


def hills(bare=False):
    cols = ["#7cbf5e", "#69b257", "#8cc96b"] if not bare else ["#b5a067", "#a8935c", "#c2ad72"]
    for k, (x, y, r, sz) in enumerate(((-14, 30, 14, 0.32), (10, 34, 16, 0.3), (-2, 44, 20, 0.28), (24, 40, 14, 0.35))):
        sphere(r, (x, y, -r * sz * 0.6), (1.4, 1.0, sz), mat(f"hill{k}{'b' if bare else ''}", cols[k % 3], rough=0.9), seg=48)


def pasture(bare=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sun=4.6 if bare else 4.2)
    ground = mat("dirt" if bare else "meadow", "#a57c52" if bare else "#62ad4f", rough=0.95, noise_bump=0.25 if bare else 0.12)
    plane(400, 400, (0, 0, 0), material=ground, name="ground")
    sky = mat("skywall", "#7fc0ec", rough=1.0, emit="#8cc8f0", emit_strength=0.9)
    box((400, 1, 160), (0, 70, 40), material=sky, bevel=0)
    cl = mat("cloud", "#ffffff", rough=0.9, emit="#ffffff", emit_strength=0.6)
    random.seed(5)
    for cx, cz in ((-16, 22), (6, 27), (20, 19), (-4, 34)):
        for k in range(4):
            c = sphere(random.uniform(2.2, 3.4), (cx + k * 2.4 - 3.6, 66, cz + random.uniform(-0.6, 0.8)), (1.3, 0.5, 0.75), cl, seg=24)
            c.visible_shadow = False
    hills(bare)
    barn(-5.6, 9.0, 1.1)
    for i, (x, y, h) in enumerate(((-9, 7, 3.6), (4.6, 10, 3.4), (8.5, 7.5, 3.8), (-2.2, 13, 3.0), (12, 14, 3.6))):
        tree(x, y, h, i, bare)
    fence(-12, 12, 4.2)
    if bare:
        tufts(110, -8, 8, -10, 4, True, 2)
        rocks(55, -8, 8, -10, 4)
        # a trough, empty
    else:
        tufts(620, -8, 8, -10, 4, False, 2)
        flowers(90, -7, 7, -9, 3.5)
    trough = [box((1.6, 0.55, 0.5), (2.6, 2.2, 0.25), material=wood("#9a6436", "#6e4424", "trough", 3.0), bevel=0.04)]
    if not bare:
        trough.append(box((1.45, 0.42, 0.04), (2.6, 2.2, 0.47), material=mat("water", "#5fb6d6", rough=0.05, coat=0.8), bevel=0.0))
    front = fence(-4.6, -2.0, -2.6, "front_fence")
    return front


def pasture_angles(bare=False):
    front = pasture(bare)
    tag = "bare" if bare else "lush"
    shots = (("wide", (0.2, -11.5, 2.7), (0.0, 0.5, 1.0), 28, 6.0),
             ("mid", (-0.6, -6.2, 1.7), (0.2, 0.3, 0.95), 34, 4.0))
    for name, loc, tgt, lens, fs in shots:
        if bare and name == "mid":
            continue
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still(f"plate_{tag}_{name}", 1080, 1920, 40)
        still(f"fg_{tag}_{name}", 1080, 1920, 24, only=front)


# ---------------------------------------------------------------- props
def cow(kind="bw", loc=(0, 0, 0)):
    x, y, z = loc
    if kind == "bw":
        body_c, spot_c = "#f6f2ea", "#1d1b1a"
    else:
        body_c, spot_c = "#a0623a", "#f6efe2"
    hide = mat(f"cow_{kind}", body_c, rough=0.55, coat=0.1)
    spot = mat(f"spot_{kind}", spot_c, rough=0.55)
    pink = mat("muzzle", "#eaa7a0", rough=0.45, coat=0.2)
    hoof = mat("hoof", "#2b2420", rough=0.5)
    horn = mat("horn", "#efe3c8", rough=0.4)
    eye = mat("cow_eye", "#141110", rough=0.2, coat=0.6)
    sphere(0.5, (x, y, z + 0.8), (1.0, 0.55, 0.52), hide, seg=48)
    for dx, dy in ((0.33, 0.17), (0.33, -0.17), (-0.33, 0.17), (-0.33, -0.17)):
        cylinder(0.09, 0.5, (x + dx, y + dy, z + 0.3), material=hide, verts=20, bevel=0.03)
        cylinder(0.095, 0.1, (x + dx, y + dy, z + 0.05), material=hoof, verts=20, bevel=0.02)
    random.seed(11 if kind == "bw" else 12)
    for k in range(6 if kind == "bw" else 3):
        a = random.uniform(-2.4, 2.4); zz = random.uniform(-0.12, 0.2)
        sx = x + random.uniform(-0.35, 0.35)
        sphere(0.13, (sx, y - 0.25, z + 0.8 + zz), (1.3, 0.25, 1.0), spot, seg=20)
    # head
    sphere(0.2, (x + 0.6, y, z + 1.05), (1.05, 0.85, 1.0), hide, seg=32)
    sphere(0.14, (x + 0.76, y, z + 0.95), (0.9, 1.05, 0.8), pink, seg=24)
    for sy in (-0.06, 0.06):
        sphere(0.02, (x + 0.88, y + sy, z + 0.97), 1, hoof, seg=10)
    for sy in (-0.1, 0.1):
        sphere(0.03, (x + 0.72, y + sy * 1.15, z + 1.12), 1, eye, seg=12)
        sphere(0.07, (x + 0.52, y + sy * 2.1, z + 1.18), (0.5, 1.0, 0.45), hide, seg=16)
        cone(0.03, 0.14, (x + 0.6, y + sy * 1.2, z + 1.27), (0, 0, 0), horn)
    # tail
    cylinder(0.02, 0.5, (x - 0.52, y, z + 0.7), (0, -18, 0), material=hide, verts=10, bevel=0)
    sphere(0.05, (x - 0.6, y, z + 0.46), (0.8, 0.8, 1.4), spot, seg=12)


def sign(text_lines):
    wd = wood("#d9b98a", "#b08c5c", "sign_board", 3.0)
    cylinder(0.06, 1.4, (0, 0.05, 0.7), material=wood("#8a5a30", "#5e3a1c", "sign_post", 2.0), verts=16)
    box((1.6, 0.08, 0.9), (0, 0, 1.45), material=wd, bevel=0.04)
    ink = mat("sign_ink", "#2a1d17", rough=0.5)
    for i, t in enumerate(text_lines):
        text3d(t, 0.22 if i == 0 else 0.16, (0, -0.05, 1.68 - i * 0.26), (90, 0, 0), ink, font="display", extrude=0.01)


def milk_can():
    lathe([(0, 0), (0.22, 0), (0.24, 0.05), (0.24, 0.5), (0.17, 0.62), (0.11, 0.66), (0.11, 0.76), (0.14, 0.78), (0.0, 0.8)],
          40, (0, 0, 0), metal("#c8cdd2", 0.25, "can_steel"), 1, "can")


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.5), 420, 2.5, "#fff0dc", "key")
    area_light((2.5, 2.5, 2.5), (0, 0, 0.5), 260, 2, "#cfe6ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    pasture_angles(False)
    pasture_angles(True)
for kind in ("bw", "brown"):
    prop_scene(); cow(kind); sprite_camera((0.05, 0, 0.75), 4.2, 0.35, 50, azimuth=-8)
    still(f"cow_{kind}", 700, 560, 28, transparent=True, crop=True)
