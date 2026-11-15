# 2026-11-16-pilot (reference-reel style test, Dark Files): moody night sets, single practical lights, deep shadows.
# Sets: a bank teller window at night, a laundromat (the "washing" analogy), a cash table under one lamp,
# a courthouse at night, a bank desk with a form. Cut-outs: a taped cardboard box, a banded cash bundle.
import math, os, random

NOTE = os.path.join(TEX, "note_1.png")


def spot(loc, target, power=800, size_deg=40, blend=0.35, color="#ffd6a0", radius=0.15, name="spot"):
    d = bpy.data.lights.new(name, "SPOT")
    d.energy = power; d.spot_size = math.radians(size_deg); d.spot_blend = blend
    d.color = hexrgb(color); d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o)
    o.location = loc; look_at(o, target)
    return o


def point(loc, power=60, color="#ffcf8a", radius=0.1, name="pt"):
    d = bpy.data.lights.new(name, "POINT"); d.energy = power; d.color = hexrgb(color); d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    return o


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def night(rgb="#06080b", strength=0.6):
    world_color(hexrgb(rgb), strength)


def hanging_lamp(x, y, z, shade="#2b2f2a", power=420, color="#ffc98a"):
    lathe([(0, 0.0), (0.32, 0.0), (0.12, 0.22), (0.03, 0.26), (0, 0.26)], 40, (x, y, z), mat("shade", shade, rough=0.35, metal=0.6), 1, "shade")
    cylinder(0.006, 2.0, (x, y, z + 1.25), material=mat("cord", "#111111"), verts=8, bevel=0)
    sphere(0.07, (x, y, z + 0.02), 1, mat("bulb", "#fff1d0", emit="#ffd9a0", emit_strength=20.0), seg=16)
    return spot((x, y, z - 0.02), (x, y, 0), power, 70, 0.6, color, 0.06, "lamp_spot")


def cardboard():
    return mat("cardboard", "#9c7448", rough=0.85, noise_bump=0.15)


def cash_box(loc, size=(0.55, 0.38, 0.32), rot=0, name="cbox"):
    x, y, z = loc
    b = box(size, (x, y, z + size[2] / 2), (0, 0, rot), cardboard(), bevel=0.012, name=name)
    t = box((size[0] * 1.002, 0.07, size[2] * 0.12), (0, 0, size[2] / 2 - size[2] * 0.06), material=mat("tape", "#c9b27a", rough=0.3, coat=0.4), bevel=0.002)
    t.parent = b
    return b


def bundle(loc, rot=0, name="bun"):
    x, y, z = loc
    notes = []
    for k in range(10):
        n = banknote(NOTE, (x, y, z + 0.004 + k * 0.004), (0, 0, rot + random.uniform(-1.5, 1.5)), 0.3, f"{name}_{k}")
        notes.append(n)
    band = box((0.06, 0.135, 0.045), (x, y, z + 0.022), (0, 0, rot), mat("band", "#c9a24a", rough=0.5), bevel=0.003, name=name + "_band")
    return notes + [band]


# ------------------------------------------------------------------ teller window at night
def teller_set():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2, exposure=0.0)
    night("#0a0d10", 1.0)
    floor_m = mat("floor_dark", "#2a2622", rough=0.35, coat=0.3)
    plane(40, 40, (0, 0, 0), material=floor_m, name="floor")
    wall = mat("wall_green", "#1f3330", rough=0.75)
    box((20, 0.3, 8), (0, 3.2, 4), material=wall, bevel=0)
    # counter + glass + brass window
    wood_m = wood("#5a3220", "#3a1e12", "teller_wood", 3.0)
    counter = [box((6, 0.8, 1.1), (0, 0.4, 0.55), material=wood_m, bevel=0.03),
               box((6.2, 0.95, 0.07), (0, 0.38, 1.13), material=mat("marble_dark", "#d8d0c2", rough=0.2, coat=0.6), bevel=0.02)]
    glass_m = glass("#cfe3e6", 0.06)
    brass = metal("#b8903e", 0.28, "brass")
    box((6, 0.04, 1.5), (0, 0.85, 1.95), material=glass_m, bevel=0.005)
    for k in range(13):
        cylinder(0.014, 1.5, (-2.9 + k * 0.48, 0.82, 1.95), material=brass, verts=10, bevel=0)
    box((6, 0.06, 0.06), (0, 0.82, 2.72), material=brass, bevel=0.01)
    box((0.9, 0.08, 0.36), (0, 0.84, 1.33), material=mat("window_hole", "#0b0b0b", rough=0.9), bevel=0.01)   # the slot
    box((0.96, 0.12, 0.04), (0, 0.8, 1.52), material=brass, bevel=0.005)
    text3d("TELLER", 0.14, (0, 0.78, 2.6), (90, 0, 0), brass, font="serif", extrude=0.01)
    # boxes waiting on the customer side
    cash_box((0.0, -0.05, 1.17), (0.62, 0.36, 0.3), 0, "box_counter")
    cash_box((-1.6, -1.0, 0.0), (0.62, 0.42, 0.4), 12, "box_floor1")
    cash_box((-1.5, -1.05, 0.4), (0.55, 0.38, 0.34), -8, "box_floor2")
    hanging_lamp(0, 1.6, 3.0, power=900)
    hanging_lamp(0, -0.3, 2.6, power=1100)
    spot((0.6, -3.0, 3.6), (0, 0.4, 1.3), 900, 30, 0.8, "#9fb8d6", 0.4, "rim")
    area_light((-4, -2, 2.5), (0, 0.5, 1.2), 160, 3, "#6d86a8", "fill")
    area_light((3, 2.5, 3), (0, 3.1, 2), 220, 3, "#c98a50", "wallwash")
    return counter


def teller_angles():
    teller_set()
    for name, loc, tgt, lens, fs in (("teller_wide", (0.5, -6.2, 1.9), (0.0, 0.6, 1.5), 30, 4.0),
                                     ("teller_close", (0.55, -2.3, 1.8), (0.0, 0.6, 1.55), 34, 2.8)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 32)


# ------------------------------------------------------------------ laundromat (the "washing" analogy)
def washer(x, y, glow=False, name="washer"):
    body = box((0.7, 0.65, 0.88), (x, y, 0.44), material=mat("washer_white", "#e9e6df", rough=0.3, coat=0.4), bevel=0.04, name=name)
    torus(0.24, 0.035, (x, y - 0.36, 0.47), (90, 0, 0), metal("#c8ccd0", 0.25, "chrome"))
    drum_m = mat("drum_glow" if glow else "drum", "#2a3a44", rough=0.4, metal=0.6,
                 emit="#7fd3ff" if glow else None, emit_strength=7.0 if glow else 0)
    cylinder(0.205, 0.02, (x, y - 0.33, 0.47), (90, 0, 0), drum_m, verts=48)
    box((0.6, 0.02, 0.1), (x, y - 0.33, 0.8), material=mat("panel", "#bfc3c6", rough=0.4), bevel=0.01)
    return body


def laundromat_angles():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3, exposure=0.0)
    night("#05080a", 0.8)
    plane(40, 40, (0, 0, 0), material=mat("lino", "#3a4144", rough=0.4, coat=0.2), name="floor")
    box((20, 0.3, 6), (0, 0.6, 3), material=mat("tiles_wall", "#2c3f44", rough=0.6), bevel=0)
    for i in range(6):
        washer(-2.0 + i * 0.8, 0.0, glow=(i == 3), name=f"w{i}")
    random.seed(11)
    for k in range(9):                                     # banknotes tumbling in the lit drum
        a = random.uniform(0, 2 * math.pi); r = random.uniform(0.03, 0.15)
        banknote(NOTE, (0.4 + r * math.cos(a), -0.35 - k * 0.002, 0.47 + r * math.sin(a)), (90 + random.uniform(-25, 25), random.uniform(0, 360), random.uniform(-20, 20)), 0.11, f"drum_note{k}", bend=25)
    for x in (-1.2, 1.2):                                  # flickery fluorescent tubes
        cylinder(0.03, 1.4, (x, -0.4, 2.7), (0, 90, 0), mat("tube", "#e8fbff", emit="#d8f6ff", emit_strength=6), verts=12, bevel=0)
    area_light((0, -0.6, 2.6), (0.4, 0.0, 0.5), 160, 2.5, "#bfe9ff", "flu")
    spot((1.0, -2.6, 1.5), (0.4, -0.3, 0.47), 120, 25, 0.7, "#ffd09a", 0.2, "warm")
    drop_cams(); camera((0.55, -3.4, 1.05), (0.25, 0.0, 0.55), lens=32, fstop=3.2)
    still("plate_laundry_wide", 1080, 1920, 32)
    drop_cams(); camera((0.42, -1.05, 0.5), (0.4, -0.3, 0.47), lens=45, fstop=2.2)
    still("plate_laundry_door", 1080, 1920, 32)


# ------------------------------------------------------------------ cash table under one lamp
def cash_table_angles():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.25, exposure=0.0)
    night("#060708", 0.8)
    plane(40, 40, (0, 0, 0), material=mat("concrete", "#2b2a28", rough=0.8, noise_bump=0.2), name="floor")
    box((20, 0.3, 6), (0, 3.0, 3), material=mat("brick", "#2a1d18", rough=0.9, noise_bump=0.3), bevel=0)
    top = box((2.0, 1.1, 0.06), (0, 0, 0.8), material=wood("#4a2c1c", "#2d190f", "table_wood", 4.0), bevel=0.01)
    for sx in (-0.9, 0.9):
        for sy in (-0.45, 0.45):
            box((0.06, 0.06, 0.78), (sx, sy, 0.39), material=mat("leg", "#1a1410", rough=0.6), bevel=0.005)
    random.seed(7)
    for i in range(14):
        bundle((-0.7 + (i % 5) * 0.32 + random.uniform(-0.03, 0.03), -0.3 + (i // 5) * 0.28, 0.83 + 0.0), random.uniform(-6, 6), f"b{i}")
    for i in range(4):                                      # a short stack on top
        bundle((0.15, 0.05, 0.875 + i * 0.045), random.uniform(-10, 10), f"s{i}")
    cash_box((-1.6, 0.6, 0.0), (0.7, 0.5, 0.45), 20, "cb1"); cash_box((-1.55, 0.55, 0.45), (0.6, 0.45, 0.4), -10, "cb2")
    cash_box((1.7, 0.8, 0.0), (0.7, 0.5, 0.45), -15, "cb3")
    hanging_lamp(0, 0, 2.2, power=900)
    area_light((3, -3, 2), (0, 0, 0.8), 90, 3, "#5d7aa0", "fill")
    area_light((0, 2.6, 2.5), (0, 3.0, 1.2), 160, 3, "#c07a48", "brickwash")
    drop_cams(); camera((0.3, -2.9, 2.35), (0, 0.05, 0.82), lens=34, fstop=3.5)
    still("plate_cash_table", 1080, 1920, 32)
    drop_cams(); camera((0.55, -1.1, 1.15), (0.05, 0.0, 0.86), lens=50, fstop=2.0)
    still("plate_cash_close", 1080, 1920, 32)


# ------------------------------------------------------------------ courthouse at night
def courthouse_angles():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3, exposure=0.0)
    night("#0b1020", 1.6)
    plane(80, 80, (0, 0, 0), material=mat("plaza", "#22252b", rough=0.6, coat=0.1), name="plaza")
    stone = mat("stone", "#b9b1a2", rough=0.7, noise_bump=0.1)
    for k in range(5):
        box((10 - k * 0.3, 1.0, 0.18), (0, 2.0 + k * 0.35, 0.09 + k * 0.18), material=stone, bevel=0.01)
    box((9, 0.6, 0.6), (0, 4.3, 7.4), material=stone, bevel=0.02)
    for i in range(6):
        cylinder(0.3, 6.0, (-3.6 + i * 1.44, 3.9, 4.0), material=stone, verts=32)
    box((9.4, 3.0, 9), (0, 5.8, 4.5), material=mat("hall", "#3a3833", rough=0.8), bevel=0)
    text3d("COURTHOUSE", 0.5, (0, 3.98, 7.45), (90, 0, 0), mat("letters", "#e7dfcf", rough=0.4), font="serif", extrude=0.03)
    for i in range(6):                                     # uplights on the columns
        spot((-3.6 + i * 1.44, 3.2, 0.1), (-3.6 + i * 1.44, 3.9, 6), 1600, 30, 0.6, "#ffd7a0", 0.1, f"up{i}")
    area_light((0, -6, 9), (0, 4, 4), 900, 6, "#7f97c8", "moon")
    drop_cams(); camera((0.6, -9.5, 1.4), (0.0, 3.5, 4.4), lens=24, fstop=8.0)
    still("plate_courthouse", 1080, 1920, 32)


# ------------------------------------------------------------------ bank desk with a form (know your customer)
def desk_angles():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2, exposure=0.0)
    night("#06070a", 0.8)
    plane(40, 40, (0, 0, 0), material=mat("carpet", "#2a1f22", rough=0.95), name="floor")
    box((2.4, 1.2, 0.06), (0, 0, 0.76), material=wood("#3e2416", "#24130b", "desk_wood", 4.0), bevel=0.01)
    box((2.3, 1.1, 0.72), (0, 0.02, 0.37), material=wood("#3a2214", "#22120a", "desk_body", 4.0), bevel=0.02)
    box((0.42, 0.56, 0.003), (0.05, -0.12, 0.792), (0, 0, -6), mat("form", "#efe9dc", rough=0.7), bevel=0)
    cylinder(0.008, 0.16, (0.33, -0.18, 0.8), (0, 90, 25), mat("pen", "#151515", rough=0.3, metal=0.4), verts=12, bevel=0)
    lathe([(0, 0), (0.1, 0), (0.1, 0.02), (0.012, 0.03), (0.012, 0.42), (0, 0.42)], 32, (-0.7, 0.25, 0.79), metal("#b8903e", 0.3, "lamp_brass"), 1, "lampstem")
    lathe([(0.0, 0.0), (0.16, 0.0), (0.09, 0.12), (0.0, 0.13)], 32, (-0.62, 0.18, 1.2), mat("lamp_green", "#1f5a3c", rough=0.3, coat=0.6), 1, "lampshade")
    spot((-0.55, 0.12, 1.18), (0.05, -0.1, 0.79), 28, 70, 0.7, "#ffd9a0", 0.05, "desk_lamp")
    box((6, 0.3, 4), (0, 1.6, 2), material=mat("wall_panel", "#1e2a2a", rough=0.7), bevel=0)
    area_light((2, -2, 2.2), (0, 0, 0.8), 60, 3, "#6e88aa", "fill")
    drop_cams(); camera((0.1, -0.85, 1.55), (0.05, -0.1, 0.79), lens=38, fstop=3.0)
    still("plate_desk", 1080, 1920, 32)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#141619"), 0.4)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#ffe0bc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#9fc0e8", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    teller_angles()
    laundromat_angles()
    cash_table_angles()
    courthouse_angles()
    desk_angles()
prop_scene(); cash_box((0, 0, 0), (0.62, 0.36, 0.3), 0, "hero_box"); sprite_camera((0, 0, 0.15), 2.0, 0.9, 50, azimuth=-25)
still("box", 600, 500, 24, transparent=True, crop=True)
random.seed(3); prop_scene(); bundle((0, 0, 0), 0, "hero_bundle"); sprite_camera((0, 0, 0.03), 0.9, 0.45, 55, azimuth=-20)
still("bundle", 500, 400, 24, transparent=True, crop=True)
