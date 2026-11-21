# 2026-11-21-m1: "Your Wi-Fi and your microwave use the same wave" (showcase Short).
# Sets: the town kitchen (bright: mint wall, wood counter, cream microwave with a perforated door, a shelf with the
# router, window, retro fridge, fruit, pendant lamp); 3 angles (wide, mid on the microwave, close on the router).
# The night plate: inside the oven cavity (dark metal box, glowing feed, turntable, mug) with a Dutch tilt.
# Cut-outs: microwave (hero 3/4), router (hero), one water molecule.
import math, os, random
from PIL import Image, ImageDraw

_src = open(os.path.join(ROOT, "jobs/2026-11-09-b/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "b09_helpers", "exec"), globals())          # sunny(), house(), tree(), drop_cams() ...

A = os.path.join(ROOT, "jobs/2026-11-21-m1/assets")
os.makedirs(A, exist_ok=True)


def mesh_tex():
    """The door screen: dark glass over a perforated metal sheet (holes far smaller than the 12 cm wave)."""
    p = os.path.join(A, "tex_doormesh.png")
    if not os.path.exists(p):
        im = Image.new("RGB", (1024, 640), "#14161b")
        d = ImageDraw.Draw(im)
        for y in range(8, 640, 14):
            for x in range(8 + (y // 14 % 2) * 7, 1024, 14):
                d.ellipse((x - 4, y - 4, x + 4, y + 4), fill="#353a44")
        d.rectangle((0, 0, 1023, 639), outline="#0b0c0f", width=18)
        im.save(p)
    return p


def microwave(x, y, z, yaw=0.0, s=1.0, name="mw"):
    """A rounded cream countertop microwave (0.56 x 0.34 x 0.42 m at s=1), door on the left, panel on the right; faces -y."""
    body_m = mat("mw_body", "#f1ece2", rough=0.35, coat=0.4)
    dark = mat("mw_dark", "#24262c", rough=0.3, coat=0.5)
    door = mat("mw_door", "#ffffff", rough=0.12, coat=1.0, image=mesh_tex())
    W, H, D = 0.56, 0.34, 0.42
    parts = [box((W, D, H), (0, 0, H / 2), material=body_m, bevel=0.035)]
    parts.append(box((0.38, 0.02, 0.27), (-0.075, -D / 2 - 0.005, H / 2), material=dark, bevel=0.012))
    pl = plane(0.33, 0.22, (-0.075, -D / 2 - 0.017, H / 2), (90, 0, 0), material=door)
    parts.append(pl)
    parts.append(box((0.022, 0.03, 0.22), (0.1, -D / 2 - 0.03, H / 2), material=mat("mw_handle", "#d9dbe0", rough=0.2, metal=0.8), bevel=0.008))
    parts.append(box((0.13, 0.02, 0.29), (0.205, -D / 2 - 0.004, H / 2), material=dark, bevel=0.01))
    parts.append(box((0.1, 0.01, 0.04), (0.205, -D / 2 - 0.016, H - 0.065), material=mat("mw_lcd", "#06140c", rough=0.3), bevel=0.003))
    t = text3d("0:30", 0.028, (0.205, -D / 2 - 0.023, H - 0.077), (90, 0, 0), glow("#6dff9a", 4.0, "lcd_glow"), font="display", extrude=0.001)
    parts.append(t)
    for i in range(9):
        parts.append(box((0.026, 0.01, 0.018), (0.178 + (i % 3) * 0.027, -D / 2 - 0.016, H - 0.12 - (i // 3) * 0.028),
                         material=mat("mw_btn", "#3a3d45", rough=0.5), bevel=0.004))
    parts.append(box((0.09, 0.012, 0.024), (0.205, -D / 2 - 0.017, 0.05), material=glow("#f0b34a", 1.2, "mw_start"), bevel=0.005))
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(cylinder(0.018, 0.012, (sx * (W / 2 - 0.05), sy * (D / 2 - 0.05), -0.004), material=dark, verts=16, bevel=0))
    root = empty((0, 0, 0), name)
    for p in parts:
        p.parent = root
    root.scale = (s, s, s)
    root.rotation_euler = (0, 0, math.radians(yaw))
    root.location = (x, y, z)
    return root


def router(x, y, z, yaw=0.0, s=1.0, name="rt"):
    """A matte black home router with three antennas and a row of status lights; faces -y."""
    blk = mat("rt_body", "#1d1f24", rough=0.45, coat=0.3)
    parts = [box((0.26, 0.16, 0.045), (0, 0, 0.03), material=blk, bevel=0.018)]
    for k, xx in enumerate((-0.09, 0.0, 0.09)):
        a = cylinder(0.006, 0.17, (xx, 0.065, 0.13), (-8 + k * 8, (k - 1) * 10, 0), mat("rt_ant", "#24262c", rough=0.4), verts=12, bevel=0)
        parts.append(a)
        parts.append(sphere(0.008, (xx + (k - 1) * 0.015, 0.053, 0.215), 1, mat("rt_ant", "#24262c", rough=0.4), seg=12))
    for k in range(5):
        parts.append(sphere(0.006, (-0.06 + k * 0.03, -0.081, 0.04), 1, glow(["#6dff9a", "#6dff9a", "#57b8ff", "#57b8ff", "#6dff9a"][k], 8.0, f"led{k}"), seg=10))
    root = empty((0, 0, 0), name)
    for p in parts:
        p.parent = root
    root.scale = (s, s, s)
    root.rotation_euler = (0, 0, math.radians(yaw))
    root.location = (x, y, z)
    return root


def mug(x, y, z, col="#f3e6cf", name="mug"):
    m = mat("mug_" + col, col, rough=0.3, coat=0.5)
    b = lathe([(0.0, 0.0), (0.036, 0.0), (0.04, 0.004), (0.042, 0.09), (0.039, 0.095), (0.0, 0.095)], 40, (x, y, z), m, name=name)
    torus(0.022, 0.006, (x + 0.045, y, z + 0.05), (90, 0, 0), m)
    return b


def kitchen():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_hdri("lounge", 0.35, backdrop=(0.9, 0.85, 0.75))
    floor_w = wood("#c9945c", "#a0703f", "floor_wood", 10.0, 0.55)
    plane(30, 30, (0, 0, 0), material=floor_w, name="floor")
    wall = mat("wall_mint", "#bfe3d6", rough=0.85)
    box((14, 0.2, 5), (0, 2.6, 2.5), material=wall, bevel=0)
    box((0.2, 8, 5), (-4.6, -1.0, 2.5), material=mat("wall_side", "#a9d6c6", rough=0.85), bevel=0)
    # backsplash tiles band
    tile = mat("tile", "#f6efe2", rough=0.4, coat=0.3)
    for i in range(24):
        for j in range(3):
            box((0.29, 0.03, 0.14), (-3.45 + i * 0.3, 2.49, 0.98 + j * 0.15), material=tile, bevel=0.01)
    # counter: cabinets, wood top, knobs
    cab = mat("cab", "#f2c88a", rough=0.5, coat=0.2)
    top = wood("#a8743f", "#7a4e2a", "counter_top", 6.0, 0.4)
    box((7.0, 0.62, 0.86), (0, 2.18, 0.43), material=cab, bevel=0.02)
    box((7.1, 0.7, 0.05), (0, 2.15, 0.885), material=top, bevel=0.012)
    for i in range(7):
        box((0.92, 0.02, 0.7), (-3.0 + i * 1.0, 1.86, 0.44), material=mat("cab_door", "#f5d4a0", rough=0.5), bevel=0.02)
        sphere(0.022, (-2.62 + i * 1.0, 1.84, 0.72), 1, mat("knob", "#d4a64a", rough=0.25, metal=0.9), seg=16)
    # the microwave, a kettle, a fruit bowl, a plant
    microwave(-1.0, 2.2, 0.91, 0, 1.0, "mw_set")
    kettle = lathe([(0, 0), (0.08, 0), (0.09, 0.05), (0.085, 0.16), (0.05, 0.21), (0.0, 0.215)], 40, (0.35, 2.2, 0.91),
                   mat("kettle", "#d6483e", rough=0.25, coat=0.6), name="kettle")
    lathe([(0, 0), (0.15, 0.0), (0.17, 0.07), (0.0, 0.07)], 40, (1.05, 2.15, 0.91), mat("bowl", "#6fc3c0", rough=0.3, coat=0.4), name="bowl")
    for k, (dx, dy) in enumerate(((-0.06, 0.0), (0.06, 0.02), (0.0, -0.06), (0.0, 0.07))):
        apple2((1.05 + dx, 2.15 + dy, 0.95), 0.045, f"ap{k}", red=["#b3121b", "#e0a32a", "#b3121b", "#46965a"][k])
    lathe([(0, 0), (0.09, 0), (0.11, 0.16), (0.0, 0.16)], 32, (2.6, 2.2, 0.91), mat("pot", "#b5533c", rough=0.6), name="pot")
    random.seed(3)
    for k in range(9):
        a = k / 9 * 2 * math.pi
        lf = sphere(0.12, (2.6 + math.cos(a) * 0.08, 2.2 + math.sin(a) * 0.08, 1.15 + random.uniform(0, 0.12)), (0.5, 0.18, 1.0),
                    plastic("#3f9a4a", 0.5, "leaf"))
        lf.rotation_euler = (math.radians(random.uniform(-25, 25)), math.radians(random.uniform(-30, 30)), a)
    # the shelf with the router, books and a small plant
    box((1.5, 0.3, 0.04), (1.9, 2.36, 1.6), material=top, bevel=0.01)
    for sx in (1.3, 2.5):
        box((0.04, 0.24, 0.12), (sx, 2.4, 1.54), material=mat("bracket", "#3a3d45", rough=0.4), bevel=0.005)
    router(1.75, 2.33, 1.62, 0, 1.6, "rt_set")
    for k, c in enumerate(("#7c2533", "#3f7fbf", "#46965a", "#f2b04a")):
        box((0.05, 0.2, 0.26 - k * 0.02), (2.3 + k * 0.055, 2.36, 1.62 + (0.26 - k * 0.02) / 2), material=mat("book" + c, c, rough=0.6), bevel=0.006)
    # window with sky and curtains, pendant lamp, retro fridge
    box((1.4, 0.06, 1.1), (-2.6, 2.5, 1.95), material=mat("win_frame", "#f6efe2", rough=0.5), bevel=0.02)
    plane(1.25, 0.95, (-2.6, 2.46, 1.95), (90, 0, 0), material=glow("#cfe9fb", 2.2, "sky_win"))
    box((0.04, 0.04, 0.95), (-2.6, 2.44, 1.95), material=mat("win_frame", "#f6efe2", rough=0.5), bevel=0)
    for sx in (-3.4, -1.8):
        box((0.3, 0.06, 1.3), (sx, 2.4, 2.0), material=mat("curtain", "#d9534f", rough=0.8), bevel=0.04)
    cylinder(0.005, 1.1, (0.2, 1.6, 2.95), material=mat("cord", "#1a1410", rough=0.6), verts=8, bevel=0)
    lathe([(0.0, 0.0), (0.2, 0.0), (0.12, 0.16), (0.02, 0.2), (0.0, 0.2)], 40, (0.2, 1.6, 2.2), mat("lamp", "#f2b04a", rough=0.4, coat=0.3), name="lamp")
    sphere(0.06, (0.2, 1.6, 2.2), 1, glow("#fff0c8", 30.0, "bulb"), seg=16)
    box((0.85, 0.75, 1.9), (3.6, 2.05, 0.95), material=mat("fridge", "#d6483e", rough=0.3, coat=0.6), bevel=0.12)
    box((0.04, 0.05, 0.5), (3.3, 1.65, 1.25), material=mat("fr_handle", "#d9dbe0", rough=0.2, metal=0.8), bevel=0.01)
    area_light((-3.5, -3.5, 4.0), (0, 2, 1.0), 900, 5, "#fff0dc", "key")
    area_light((3.5, -3.0, 2.2), (0, 2, 1.0), 260, 5, "#dbe8ff", "fill")
    area_light((0.2, 1.6, 2.1), (0, 2, 0.9), 60, 0.4, "#ffe0a8", "lamp")


def kitchen_angles():
    kitchen()
    drop_cams(); camera((0.35, -2.3, 1.45), (0.35, 2.2, 1.3), lens=24, fstop=8.0)
    still("plate_kitchen_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.75, 0.55, 1.22), (-1.0, 2.2, 1.05), lens=32, fstop=2.8)
    still("plate_kitchen_mw", 1080, 1920, 40)
    drop_cams(); camera((1.55, 0.95, 1.55), (1.8, 2.35, 1.66), lens=40, fstop=2.4)
    still("plate_kitchen_router", 1080, 1920, 40)


def cavity():
    """Inside the oven, made huge: dark metal walls with a faint perforation grid, the feed glowing, a mug on the turntable."""
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    night_set(target=(0, 0, 0.4), rim="#ff9a3c", spot_power=9000, spot_height=7.0, spot_angle=40, floor_color="#1a1d24",
              grid=True, grid_color="#3a2a1a", grid_step=0.5, grid_extent=8, fill=0.05)
    metal_wall = mat("cav_wall", "#2a2e36", rough=0.35, metal=0.6)
    box((10, 0.2, 7), (0, 4.0, 3.5), material=metal_wall, bevel=0)
    box((0.2, 10, 7), (-4.0, 0.0, 3.5), material=metal_wall, bevel=0)
    box((0.2, 10, 7), (4.0, 0.0, 3.5), material=metal_wall, bevel=0)
    box((10, 10, 0.2), (0, 0, 5.2), material=metal_wall, bevel=0)
    plane(1.4, 1.0, (0.9, 0.6, 5.08), (0, 0, 0), material=glow("#ffb45c", 14.0, "feed_glow"))
    cylinder(2.6, 0.08, (0, 0.6, 0.12), material=mat("plate_glass", "#dfeaf0", rough=0.05, transmission=0.7), verts=72, bevel=0.02)
    m = lathe([(0.0, 0.0), (0.7, 0.0), (0.78, 0.08), (0.82, 1.6), (0.76, 1.66), (0.0, 1.66)], 48, (0, 0.6, 0.18),
              mat("big_mug", "#f3e6cf", rough=0.3, coat=0.5), name="bigmug")
    torus(0.42, 0.11, (0.88, 0.6, 1.0), (90, 0, 0), mat("big_mug", "#f3e6cf", rough=0.3, coat=0.5))
    cylinder(0.74, 0.02, (0, 0.6, 1.62), material=mat("hot_water", "#ff8a3c", rough=0.05, emit="#ff7a2a", emit_strength=3.0), verts=48, bevel=0)
    area_light((0.9, 0.6, 4.8), (0, 0.6, 1.0), 500, 1.4, "#ffb45c", "feed")


def cavity_angle():
    cavity()
    drop_cams()
    cam, _ = camera((0.0, -6.4, 2.3), (0.0, 0.6, 1.6), lens=26, fstop=2.2)
    dutch(cam, 5)
    still("plate_cavity", 1080, 1920, 40)


if not os.environ.get("BK_PROPS_ONLY"):
    kitchen_angles()
    cavity_angle()
# cut-outs
reset(700, 700, 30, 0.1, samples=32, transparent=True, bloom=0)
sunny()
area_light((-1.2, -1.6, 1.6), (0, 0, 0.2), 260, 1.6, "#fff0dc", "key")
area_light((1.4, 0.8, 0.9), (0, 0, 0.2), 140, 0.8, "#bfe6ff", "rim")
mwh = microwave(0, 0, 0, -28, 1.0, "mw_hero")
camera((0.0, -1.6, 0.55), (0.0, 0.0, 0.17), lens=50, fstop=0)
still("mw_hero", 900, 700, 32, transparent=True, crop=True)
for o in [o for o in bpy.data.objects if o.name.startswith("mw_hero") or (o.parent and o.parent.name.startswith("mw_hero"))]:
    o.hide_render = True
router(0, 0, 0, 24, 1.0, "rt_hero")
drop_cams(); camera((0.0, -0.75, 0.32), (0.0, 0.0, 0.08), lens=50, fstop=0)
still("router_hero", 700, 600, 32, transparent=True, crop=True)
for o in [o for o in bpy.data.objects if o.name.startswith("rt_") or (o.parent and o.parent.name.startswith("rt_hero"))]:
    o.hide_render = True
# one water molecule: oxygen with two hydrogens at 104.5 degrees
om = mat("oxygen", "#e04a3c", rough=0.22, coat=0.8)
hm = mat("hydrogen", "#f4f6f8", rough=0.22, coat=0.8)
sphere(0.5, (0, 0, 0.5), 1, om, seg=48, name="mol_o")
for sgn in (-1, 1):
    a = math.radians(90 + sgn * 52.25)
    sphere(0.32, (math.cos(a) * 0.62, 0.0, 0.5 - math.sin(a) * 0.62), 1, hm, seg=40, name=f"mol_h{sgn}")
drop_cams(); camera((0.0, -4.2, 0.5), (0.0, 0.0, 0.42), lens=60, fstop=0)
still("molecule", 600, 600, 32, transparent=True, crop=True)
