# Sets (plates) and prop cut-outs for "Why can't we just print more money?" v2: bright little 3D world.
import math, os, random

def sunny(sky_top="#7fc4ee", sky_horizon="#d9f0ff", sun_strength=3.2):
    w = world_color(hexrgb(sky_horizon), 0.9)
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    grad = nt.nodes.new("ShaderNodeTexGradient")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(coord.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].color = (*hexrgb(sky_horizon), 1)
    ramp.color_ramp.elements[1].color = (*hexrgb(sky_top), 1)
    ramp.color_ramp.elements[0].position = 0.5
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    d = bpy.data.lights.new("sun", "SUN"); d.energy = sun_strength; d.angle = math.radians(8)
    d.color = hexrgb("#fff1dc")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(50), math.radians(-12), math.radians(-35))

def palm(x, y, h=4.2, seed=1):
    random.seed(seed)
    trunk_m = mat("trunk", "#9c7650", rough=0.8)
    leaf_m = plastic("#3f9a4a", 0.5, "palm_leaf")
    segs = 9
    for i in range(segs):
        t = i / segs
        cylinder(0.16 - 0.06 * t, h / segs * 1.05, (x + 0.35 * t * t, y, h / segs * (i + 0.5)), (0, 6 * t, 0), trunk_m, verts=16, bevel=0)
    top = (x + 0.35, y, h)
    for k in range(8):
        a = k / 8 * 2 * math.pi + random.uniform(-0.2, 0.2)
        L = random.uniform(1.4, 1.9)
        leaf = sphere(0.5, (top[0] + math.cos(a) * L * 0.5, top[1] + math.sin(a) * L * 0.5, top[2] - 0.25), (L * 0.55 / 0.5 * 0.5, 0.22, 0.04), leaf_m)
        leaf.rotation_euler = (0, math.radians(25), a)

def stall(x=0.0, y=0.0):
    wood = mat("wood", "#a8743f", rough=0.55, coat=0.3, noise_bump=0.06)
    wood_dark = mat("wood_dark", "#7a5230", rough=0.6)
    box((2.4, 1.0, 0.1), (x, y, 0.92), material=wood, bevel=0.02)                     # counter top
    box((2.3, 0.9, 0.8), (x, y + 0.02, 0.48), material=wood_dark, bevel=0.03)         # counter body
    for sx in (-1.1, 1.1):
        for sy in (-0.42, 0.42):
            cylinder(0.05, 2.3, (x + sx, y + sy, 1.15), material=wood_dark, verts=16)
    aw = paper(os.path.join(TEX, "awning_stripes.png"), 0.6, "awning")
    a = box((2.7, 1.3, 0.06), (x, y - 0.1, 2.32), (12, 0, 0), material=aw, bevel=0.01)

def market_plate(name, cam_loc, cam_target, lens, fstop, w=1080, h=1920, samples=32):
    reset(w, h, 30, 0.1, samples=samples, bloom=0)
    sunny()
    plane(400, 400, (0, 0, 0), material=mat("sand", "#efd6a4", rough=0.9, noise_bump=0.08), name="sand")
    plane(400, 160, (0, 105, 0.03), material=mat("sea", "#1f8fbf", rough=0.05, coat=0.8), name="sea")
    stall(0.0, 0.0)
    palm(-3.2, 3.5, 4.4, 1); palm(3.6, 5.5, 5.0, 2); palm(-6, 9, 5.5, 3)
    for k in range(5):
        sphere(random.uniform(0.25, 0.5), (random.uniform(-5, 5), random.uniform(3, 8), 0.05), (1, 1, 0.5), clay("#cfb27c"))
    camera(cam_loc, cam_target, lens=lens, fstop=fstop)
    still(name, w, h, samples)

def bank_plate():
    reset(1080, 1920, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#f2e6d4"), 1.0)
    floor_m = paper(os.path.join(TEX, "floor_checker.png"), 0.35, "tiles")
    fl = plane(30, 30, (0, 0, 0), material=floor_m, name="tiles")
    wall = mat("wall", "#efe3cf", rough=0.7)
    box((30, 0.3, 9), (0, 5, 4.5), material=wall, bevel=0)
    marble = mat("marble", "#f7f2ea", rough=0.25, coat=0.4)
    for x in (-4.5, -1.5, 1.5, 4.5):
        cylinder(0.32, 5.6, (x, 4.4, 2.8), material=marble, verts=32)
        box((0.9, 0.9, 0.25), (x, 4.4, 5.65), material=marble)
        box((0.9, 0.9, 0.25), (x, 4.4, 0.12), material=marble)
    box((12, 0.6, 0.5), (0, 4.4, 6.0), material=marble)
    text3d("CENTRAL BANK", 0.85, (0, 4.05, 6.75), (90, 0, 0), metal("#c9a24a", 0.3, "sign"), font="serif", extrude=0.05)
    area_light((-3, -4, 6), (0, 1, 1.5), 1600, 4, "#fff0dc", "key")
    area_light((4, -2, 4), (0, 1, 1.5), 500, 4, "#dbe8ff", "fill")
    camera((0, -7.5, 2.4), (0, 1.5, 1.6), lens=30, fstop=0)
    still("plate_bank", 1080, 1920, 32)

def vault_plate():
    reset(1080, 1920, 30, 0.1, samples=32, bloom=0)
    world_color(hexrgb("#3a2350"), 1.0)
    floor("#4a3060", rough=0.45)
    d = bpy.data.lights.new("spot", "SPOT"); d.energy = 9000; d.spot_size = math.radians(50); d.spot_blend = 0.6
    d.color = hexrgb("#ffd9a8")
    o = bpy.data.objects.new("spot", d); bpy.context.scene.collection.objects.link(o)
    o.location = (0, -1.0, 7.5); look_at(o, (0, 0.5, 0))
    area_light((4, 4, 3), (0, 0, 1.5), 1200, 4, "#b98bff", "rim")
    area_light((-4, 3, 4), (0, 2, 2), 900, 5, "#ff9a6b", "rim2")
    camera((0, -7.0, 2.0), (0, 0.5, 1.5), lens=32, fstop=0)
    still("plate_vault", 1080, 1920, 32)

def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key")
    area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")

# ---- sets: wide, medium (closer, lower) and a close angle on the counter
market_plate("plate_market_wide", (0.4, -9.5, 2.6), (0, 0, 1.3), 30, 5.6)
market_plate("plate_market_mid", (-0.6, -4.6, 1.75), (0.1, 0, 1.05), 34, 3.2)
market_plate("plate_market_close", (0.5, -2.6, 2.2), (0.1, 0.05, 0.98), 42, 2.0)
bank_plate()
vault_plate()

# ---- cut-outs
prop_scene(); a = apple((0, 0, 0), r=0.16); a.rotation_euler = (0, 0, math.radians(30))
sprite_camera((0, 0, 0.16), 1.6, 0.55, 60); still("apple", 500, 500, 24, transparent=True, crop=True)

prop_scene()
for k in range(10):
    banknote(loc=(0, 0, 0.004 + k * 0.006), rot=(0, 0, 3 * math.sin(k * 1.7)), w=0.7, name=f"n{k}")
sprite_camera((0, 0, 0.03), 1.7, 0.85, 55); still("stack10", 700, 500, 24, transparent=True, crop=True)

prop_scene(); banknote(loc=(0, 0, 0), rot=(70, 0, -12), w=0.7)
sprite_camera((0, 0, 0), 1.7, 0.3, 55); still("bill", 600, 500, 24, transparent=True, crop=True)

prop_scene(); pr, slot = printer((0, 0, 0), 1.0)
sprite_camera((0, 0, 0.7), 4.6, 1.6, 50, azimuth=-22); still("printer", 900, 900, 28, transparent=True, crop=True)

for side in ("1", "2"):
    prop_scene(); price_tag(os.path.join(TEX, f"tag_{side}.png"), None, loc=(0, 0, 0.3), w=0.5)
    camera((0, -1.6, 0.42), (0, 0, 0.3), lens=60, fstop=0); still(f"tag_{side}", 600, 450, 24, transparent=True, crop=True)

prop_scene(); banknote(os.path.join(TEX, "note_100t.png"), loc=(0, 0, 0.5), rot=(84, 0, -10), w=1.4, bend=14)
camera((0, -2.6, 0.62), (0, 0, 0.5), lens=55, fstop=0); still("note_100t", 1000, 600, 28, transparent=True, crop=True)

prop_scene(); banknote(os.path.join(TEX, "note_100t.png"), loc=(0, 0, 0), rot=(60, 20, 30), w=0.7)
sprite_camera((0, 0, 0), 1.8, 0.4, 55); still("bill_100t", 500, 500, 24, transparent=True, crop=True)
