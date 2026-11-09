# 2026-11-09-c sets and cut-outs: a warm, colourful fish lab (bench with a big aquarium as the foreground layer,
# a lever + feeder on the tank, shelves of little tanks, a pink target board on the floor area), an underwater
# close-up inside the tank (gravel, plants, the lever), and props: goldfish, fish-on-wheels cart, food pellet.
import math, os, random


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def gold_mat():
    return bpy.data.materials.get("goldfish") or mat("goldfish", "#f07a1a", rough=0.3, sss=0.25, coat=0.6)


def fin_mat():
    return bpy.data.materials.get("fin") or mat("fin", "#ff8a24", rough=0.35, sss=0.2, coat=0.3, alpha=0.95)


def goldfish(loc=(0, 0, 0), s=1.0, yaw=0, name="fish"):
    """A chubby goldfish facing +X. loc = body centre. Length ~0.32*s m."""
    x, y, z = loc
    prof = [(0.0, -0.16), (0.035, -0.15), (0.07, -0.1), (0.09, -0.02), (0.088, 0.05), (0.07, 0.11), (0.04, 0.15), (0.0, 0.165)]
    body = lathe([(r * s, zz * s) for r, zz in prof], 36, (x, y, z), gold_mat(), 1, name)
    body.rotation_euler = (0, math.radians(90), math.radians(yaw))
    body.scale = (1.0, 0.72, 1.0)                     # flatter side to side
    parts = []
    # tail: two lobes behind the body (the body's +Z after rotation is +X, so local -Z is the tail end)
    for k in (-1, 1):                                  # forked tail, flat in the fish's side plane
        t = sphere(0.085 * s, (k * 0.05 * s, 0, -0.21 * s), (1.0, 0.1, 0.7), fin_mat())
        t.rotation_euler = (0, math.radians(k * 35), 0)
        parts.append(t)
    d = sphere(0.05 * s, (-0.095 * s, 0, -0.01 * s), (0.6, 0.1, 1.0), fin_mat()); parts.append(d)     # dorsal (local -X = up)
    for k in (-1, 1):
        p = sphere(0.035 * s, (0.05 * s, k * 0.06 * s, 0.03 * s), (0.6, 0.15, 1.0), fin_mat())
        p.rotation_euler = (math.radians(k * 40), 0, 0); parts.append(p)
    white = mat("eye_w", "#ffffff", rough=0.2, coat=0.8); black = mat("eye_b", "#0b0b0b", rough=0.1, coat=1.0)
    for k in (-1, 1):
        parts.append(sphere(0.026 * s, (-0.025 * s, k * 0.058 * s, 0.1 * s), 1, white, seg=20))
        parts.append(sphere(0.015 * s, (-0.027 * s, k * 0.078 * s, 0.112 * s), 1, black, seg=16))
    for p in parts:
        p.parent = body
    return body


def gravel(x, y, w, d, z, n=260, seed=1, r=0.018):
    random.seed(seed)
    cols = ["#d9b98a", "#c69a66", "#efe0c0", "#8a6a4a", "#6fc3c0", "#e8a39a"]
    for k in range(n):
        c = cols[k % len(cols)]
        sphere(random.uniform(0.6, 1.2) * r, (x + random.uniform(-w / 2, w / 2), y + random.uniform(-d / 2, d / 2), z),
               (1.0, 1.0, 0.7), bpy.data.materials.get("grv" + c) or mat("grv" + c, c, rough=0.6), seg=10)


def weed(x, y, z, h=0.3, seed=0, color="#4f9e4a"):
    random.seed(seed)
    m = bpy.data.materials.get("weed" + color) or mat("weed" + color, color, rough=0.5, sss=0.2)
    for k in range(5):
        a = random.uniform(-25, 25); b = random.uniform(-25, 25); hh = h * random.uniform(0.6, 1.1)
        o = sphere(1, (x + random.uniform(-0.03, 0.03), y + random.uniform(-0.03, 0.03), z + hh / 2), (0.018, 0.05, hh / 2), m, seg=16)
        o.rotation_euler = (math.radians(a), math.radians(b), random.uniform(0, 3))


def lever(x, y, z, s=1.0):
    """A little brass lever with a red knob, hanging into the water from a feeder box."""
    brass = metal("#c9a24a", 0.25, "brass")
    knob = mat("knob", "#d9534f", rough=0.3, coat=0.6)
    rod = cylinder(0.008 * s, 0.22 * s, (x, y, z - 0.11 * s), material=brass, verts=12, bevel=0)
    sphere(0.026 * s, (x, y, z - 0.23 * s), 1, knob, seg=24)
    return rod


def tank(x, y, zb, w=1.2, d=0.5, h=0.62, fish=True):
    """Aquarium on a bench: zb = bottom of the tank. Returns its objects."""
    out = []
    frame = mat("tank_frame", "#25262b", rough=0.4)
    g = mat("tank_glass", "#e8f6ff", rough=0.03, transmission=1.0, ior=1.2, alpha=0.25)
    water = mat("tank_water", "#7cc6d6", rough=0.05, alpha=0.18, emit="#5ab3c8", emit_strength=0.15)
    out.append(box((w, d, 0.04), (x, y, zb + 0.02), material=frame, bevel=0.01))
    out.append(box((w, d, 0.03), (x, y, zb + h), material=frame, bevel=0.01))
    out.append(box((w - 0.04, d - 0.04, h * 0.86), (x, y, zb + 0.04 + h * 0.43), material=water, bevel=0.005))
    out.append(box((w, 0.01, h), (x, y - d / 2, zb + h / 2), material=g, bevel=0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            out.append(box((0.03, 0.03, h), (x + sx * (w / 2 - 0.015), y + sy * (d / 2 - 0.015), zb + h / 2), material=frame, bevel=0.004))
    # gravel bed, weeds, a little castle
    random.seed(4)
    cols = ["#d9b98a", "#c69a66", "#efe0c0", "#6fc3c0", "#e8a39a"]
    for k in range(120):
        c = cols[k % len(cols)]
        out.append(sphere(random.uniform(0.012, 0.022), (x + random.uniform(-w / 2 + 0.04, w / 2 - 0.04), y + random.uniform(-d / 2 + 0.04, d / 2 - 0.04), zb + 0.05),
                          (1, 1, 0.7), bpy.data.materials.get("grv" + c) or mat("grv" + c, c, rough=0.6), seg=10))
    for k, (wx, col) in enumerate(((-0.45, "#4f9e4a"), (-0.32, "#3f8f45"), (0.42, "#5aa84f"))):
        weed(x + wx, y + 0.12, zb + 0.05, 0.4, k, col)
    # feeder box with the lever on the right end
    fb = mat("feeder", "#f2b04a", rough=0.4, coat=0.4)
    out.append(box((0.18, 0.16, 0.14), (x + w / 2 - 0.18, y, zb + h + 0.08), material=fb, bevel=0.02))
    out.append(lever(x + w / 2 - 0.18, y - 0.02, zb + h + 0.01))
    if fish:
        for k, (fx, fz, yaw) in enumerate(((-0.2, 0.3, 10), (0.15, 0.42, 190), (0.32, 0.22, -15))):
            out.append(goldfish((x + fx, y - 0.05, zb + fz), 0.9, yaw, f"tf{k}"))
    return out


def shelf_tanks(x, y, z):
    frame = mat("tank_frame", "#25262b", rough=0.4)
    water = bpy.data.materials.get("small_water") or mat("small_water", "#8fd0e8", rough=0.05, emit="#6fc3e0", emit_strength=0.6)
    box((3.2, 0.4, 0.05), (x, y, z), material=wood("#c58b4e", "#9a6634", "shelf", 4.0), bevel=0.01)
    for k in range(4):
        xx = x - 1.2 + k * 0.8
        box((0.5, 0.28, 0.32), (xx, y, z + 0.19), material=water, bevel=0.01)
        box((0.52, 0.3, 0.02), (xx, y, z + 0.36), material=frame, bevel=0.005)
        o = sphere(0.035, (xx + random.uniform(-0.1, 0.1), y - 0.15, z + 0.2), (1.4, 0.6, 1.0), gold_mat(), seg=16)


# ---------------------------------------------------------------- the fish lab
def build_lab():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#e8f1f2"), 1.0)
    plane(40, 40, (0, 0, 0), material=wood("#c99a62", "#a87a46", "floor_wood", 1.2, 0.45), name="floor")
    box((7.0, 3.4, 0.02), (0.2, -0.8, 0.01), material=mat("rug", "#34425c", rough=0.9), bevel=0.005)
    box((6.6, 3.0, 0.025), (0.2, -0.8, 0.012), material=mat("rug_in", "#6fc3c0", rough=0.9), bevel=0.005)
    box((30, 0.3, 9), (0, 4.6, 4.5), material=mat("wall", "#cfe7e3", rough=0.7), bevel=0)
    box((30, 0.1, 1.2), (0, 4.42, 0.6), material=mat("wainscot", "#34425c", rough=0.5, coat=0.3), bevel=0.02)
    box((30, 0.14, 0.06), (0, 4.4, 1.22), material=metal("#c9a24a", 0.3, "trim"), bevel=0.01)
    box((0.3, 20, 9), (-6.5, -2, 4.5), material=mat("wall_l", "#bfded9", rough=0.7), bevel=0)
    random.seed(2)
    shelf_tanks(-2.0, 4.2, 1.9); shelf_tanks(-2.0, 4.2, 2.9)
    text3d("FISH LAB", 0.55, (-2.0, 4.35, 4.0), (90, 0, 0), mat("sign_ink", "#7c2533", rough=0.5), font="display", extrude=0.04)
    # round wall clock
    cylinder(0.42, 0.06, (1.8, 4.42, 3.2), (90, 0, 0), mat("clock_face", "#f6efe2", rough=0.4), verts=48)
    torus(0.42, 0.04, (1.8, 4.38, 3.2), (90, 0, 0), mat("clock_rim", "#d9534f", rough=0.3, coat=0.5))
    ink = mat("clock_ink", "#1a1410", rough=0.5)
    box((0.03, 0.02, 0.28), (1.8, 4.36, 3.32), material=ink, bevel=0.005)
    box((0.2, 0.02, 0.03), (1.9, 4.36, 3.2), material=ink, bevel=0.005)
    # pink target board on the right, for the driving test
    box((1.1, 0.06, 1.1), (3.6, 4.3, 0.75), material=mat("target_board", "#f6efe2", rough=0.5), bevel=0.03)
    for k, (r, c) in enumerate(((0.48, "#e86aa6"), (0.32, "#f6efe2"), (0.16, "#e86aa6"))):
        cylinder(r, 0.02, (3.6, 4.26 - k * 0.01, 0.75), (90, 0, 0), mat(f"tg{k}", c, rough=0.4), verts=48)
    # bench with the big tank (foreground layer)
    top_m = mat("bench_top", "#f2ebdf", rough=0.25, coat=0.5)
    body_m = wood("#3d7f7c", "#2c605d", "bench_body", 3.0)
    bench = [box((2.6, 0.8, 0.86), (-1.0, 0.5, 0.43), material=body_m, bevel=0.04),
             box((2.8, 0.95, 0.07), (-1.0, 0.48, 0.895), material=top_m, bevel=0.025)]
    for k in range(3):
        bench.append(box((0.7, 0.03, 0.6), (-1.85 + k * 0.85, 0.09, 0.45), material=wood("#4a918d", "#336e6a", "drawer", 3.0), bevel=0.02))
        bench.append(cylinder(0.03, 0.03, (-1.85 + k * 0.85, 0.06, 0.62), (90, 0, 0), metal("#c9a24a", 0.25, "brass"), verts=16))
    bench += tank(-1.0, 0.55, 0.93)
    # a bowl of fish food and a notebook on the bench
    bench.append(lathe([(0, 0), (0.1, 0), (0.13, 0.07), (0.12, 0.08), (0, 0.04)], 32, (0.6, 0.35, 0.93), mat("bowl", "#d9534f", rough=0.3, coat=0.5), 1, "bowl"))
    bench.append(box((0.3, 0.22, 0.02), (-2.05, 0.2, 0.94), (0, 0, 12), mat("notebook", "#f2b04a", rough=0.6), bevel=0.005))
    plant = mat("plant", "#4f9e4a", rough=0.6)
    for px in (-5.6, 5.4):
        lathe([(0, 0), (0.3, 0), (0.38, 0.55), (0.0, 0.55)], 32, (px, 3.0, 0), mat("pot", "#c4623a", rough=0.6), 1, "pot")
        for k in range(6):
            sphere(0.35, (px + random.uniform(-0.25, 0.25), 3.0 + random.uniform(-0.2, 0.2), 0.9 + k * 0.12), 1, plant, seg=20)
    lampm = mat("lamp", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    for x in (-2.2, 0.2):
        sphere(0.12, (x, 0.9, 2.5), 1, lampm, seg=24)
        cylinder(0.01, 1.6, (x, 0.9, 3.3), material=mat("cord", "#25262b"), verts=8, bevel=0)
    area_light((-3, -4, 6), (0, 1, 1.5), 1700, 4, "#fff0dc", "key"); area_light((4, -2, 4), (0, 1, 1.5), 520, 4, "#dbe8ff", "fill")
    area_light((-1.0, 0.0, 2.2), (-1.0, 0.55, 1.1), 160, 1.5, "#cfeeff", "tank_spot")
    return bench


def lab_angles():
    bench = build_lab()
    for name, loc, tgt, lens, fs in (("lab_wide", (0.2, -9.0, 2.4), (0.2, 1.5, 1.5), 26, 6.0),
                                     ("lab_mid", (-0.6, -4.0, 1.55), (-0.9, 0.6, 1.15), 34, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=bench)
    drop_cams(); camera((2.2, -2.6, 0.7), (3.3, 3.6, 0.7), lens=30, fstop=5.0)        # low floor angle at the target
    still("plate_lab_floor", 1080, 1920, 40)


# ---------------------------------------------------------------- inside the tank (underwater close-up)
def tank_inside():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2)
    world_color(hexrgb("#2f8fa0"), 1.0)
    plane(20, 20, (0, 0, 0), material=mat("sand", "#d9c4a0", rough=0.9, noise_bump=0.15), name="sand")
    box((6, 0.05, 4), (0, 1.4, 2.0), material=mat("backwall", "#3aa2b0", rough=0.3, emit="#5fc6d2", emit_strength=0.35), bevel=0)
    gravel(0, 0.3, 3.0, 2.4, 0.01, 520, 3, 0.03)
    for k, (wx, wy, col) in enumerate(((-0.9, 0.9, "#4f9e4a"), (-0.6, 1.1, "#3f8f45"), (0.9, 1.0, "#5aa84f"), (-1.2, 0.4, "#46965a"), (1.2, 0.6, "#3f8f45"))):
        weed(wx, wy, 0.0, 1.3, k, col)
    rock = mat("rock", "#8a8f96", rough=0.8, noise_bump=0.3)
    sphere(0.32, (0.95, 0.4, 0.1), (1.3, 1.0, 0.6), rock); sphere(0.22, (-0.95, 0.2, 0.05), (1.2, 1.0, 0.7), rock)
    # the lever hanging from the feeder above (top of frame, right of centre)
    brass = metal("#c9a24a", 0.25, "brass")
    box((0.7, 0.5, 0.4), (0.45, 0.5, 2.55), material=mat("feeder", "#f2b04a", rough=0.4, coat=0.4), bevel=0.05)
    cylinder(0.02, 0.9, (0.45, 0.3, 1.9), material=brass, verts=16, bevel=0)
    sphere(0.085, (0.45, 0.3, 1.43), 1, mat("knob", "#d9534f", rough=0.3, coat=0.6), seg=32)
    # light rays from above
    for k in range(4):
        o = cylinder(0.15, 3.5, (-1.0 + k * 0.7, 0.9, 2.2), (0, 18 - k * 4, 0), mat(f"ray{k}", "#ffffff", alpha=0.08, emit="#e8fbff", emit_strength=0.6), verts=16, bevel=0)
    area_light((-1, -2, 4), (0, 0.5, 0.5), 900, 3, "#e8fbff", "key"); area_light((2, -1, 2), (0, 0.5, 1), 220, 2, "#ffd9a8", "warm")
    drop_cams(); camera((0, -3.2, 1.05), (0, 0.8, 1.05), lens=28, fstop=4.0)
    still("plate_tank_close", 1080, 1920, 40)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def fish_car(x=0, y=0):
    """The 'fish operated vehicle': a wheeled cart carrying a round tank with a goldfish."""
    dark = mat("cart", "#34425c", rough=0.4, coat=0.4)
    box((0.7, 0.5, 0.14), (x, y, 0.16), material=dark, bevel=0.03)
    tyre = mat("tyre", "#1d1d22", rough=0.6); hub = metal("#c9a24a", 0.3, "hub")
    for sx in (-0.26, 0.26):
        for sy in (-0.27, 0.27):
            cylinder(0.09, 0.06, (x + sx, y + sy, 0.09), (90, 0, 0), tyre, verts=32, bevel=0.01)
            cylinder(0.045, 0.065, (x + sx, y + sy, 0.09), (90, 0, 0), hub, verts=24, bevel=0.005)
    cylinder(0.02, 0.5, (x - 0.28, y, 0.45), material=metal("#9aa3ab", 0.3, "pole"), verts=12)
    sphere(0.05, (x - 0.28, y, 0.72), 1, mat("cam_eye", "#d9534f", emit="#ff6a5a", emit_strength=1.0), seg=20)
    cylinder(0.27, 0.36, (x + 0.04, y, 0.42), material=mat("bowl_water", "#7cc6d6", rough=0.05, alpha=0.45, emit="#5ab3c8", emit_strength=0.3), verts=48)
    torus(0.27, 0.015, (x + 0.04, y, 0.6), material=mat("bowl_rim", "#e8f6ff", rough=0.1))
    goldfish((x + 0.04, y - 0.06, 0.42), 1.2, -10, "car_fish")


if not os.environ.get("BK_PROPS_ONLY"):
    lab_angles()
    tank_inside()
prop_scene(); goldfish((0, 0, 0.3), 1.6, 0, "hero_fish"); camera((0, -1.6, 0.36), (0, 0, 0.3), lens=60, fstop=0)
still("goldfish", 600, 400, 28, transparent=True, crop=True)
prop_scene(); fish_car(); sprite_camera((0, 0, 0.3), 2.6, 0.7, 50, azimuth=-25); still("fish_car", 700, 600, 28, transparent=True, crop=True)
prop_scene(); sphere(0.05, (0, 0, 0.05), (1, 1, 0.8), mat("pellet", "#b8742e", rough=0.6, noise_bump=0.3)); camera((0, -0.6, 0.2), (0, 0, 0.05), lens=60, fstop=0)
still("pellet", 200, 200, 16, transparent=True, crop=True)
