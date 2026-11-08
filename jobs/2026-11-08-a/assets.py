# 2026-11-08-a: "The prisoner's dilemma". Sets: a police station cutaway (two interrogation rooms side by side, divided by a
# wall, hanging lamps, one-way mirrors), a market with two rival apple stalls (price war). Cut-out: a 1980 home computer.
import math, os, random

# market helpers (sunny, palm, basket, crate, barrel, stall, bunting) from the reference job m3 (frozen)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-m3/assets.py")).read().split("def build_market")[0]
exec(compile(_src, "m3_helpers", "exec"), globals())

ROOMS = {"left": -2.05, "right": 2.05}

def lamp(x, y, name):
    cylinder(0.012, 1.3, (x, y, 3.65), material=metal("#25262b", 0.4, "cord"), verts=8, bevel=0)
    lathe([(0.0, 0.32), (0.06, 0.32), (0.1, 0.26), (0.3, 0.02), (0.32, 0.0), (0.0, 0.1)], 40, (x, y, 2.72),
          metal("#2f6f6a", 0.35, "shade"), 1, name + "_shade")
    sphere(0.08, (x, y, 2.76), 1, glow("#fff1c4", 12.0, "bulb"))
    d = bpy.data.lights.new(name, "SPOT"); d.energy = 900; d.spot_size = math.radians(75); d.spot_blend = 0.5
    d.color = hexrgb("#ffd49a"); d.shadow_soft_size = 0.15
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = (x, y, 2.7)
    look_at(o, (x, y, 0))

def room(side, wall):
    cx = ROOMS[side]
    box((4.0, 0.25, 5.0), (cx, 3.1, 2.5), material=mat("back_" + side, wall, rough=0.8), bevel=0)
    box((4.0, 0.28, 0.22), (cx, 2.96, 0.11), material=mat("skirt", "#1f2a33"), bevel=0)
    # one-way mirror on the back wall
    box((2.0, 0.08, 1.05), (cx, 2.97, 1.75), material=mat("mframe", "#1f2a33", rough=0.4), bevel=0.02)
    box((1.85, 0.05, 0.92), (cx, 2.93, 1.75), material=mat("mirror", "#1a2a36", rough=0.04, coat=1.0), bevel=0)
    text3d("ROOM " + ("1" if side == "left" else "2"), 0.28, (cx, 2.95, 2.62), (90, 0, 0), mat("rno", "#f2b04a", rough=0.5),
           font="body", extrude=0.01)
    # wall clock
    cylinder(0.2, 0.05, (cx + 1.45, 2.96, 2.5), (90, 0, 0), mat("clk", "#f6efe2", rough=0.4), verts=40)
    torus(0.2, 0.025, (cx + 1.45, 2.93, 2.5), (90, 0, 0), metal("#25262b", 0.4, "clkr"))
    box((0.02, 0.01, 0.13), (cx + 1.45, 2.92, 2.55), material=mat("hand", "#1a1410"), bevel=0)
    box((0.1, 0.01, 0.02), (cx + 1.49, 2.92, 2.5), material=mat("hand", "#1a1410"), bevel=0)
    # table + interrogator's empty chair in front (these form the foreground layer)
    tm = mat("table", "#8a8f98", rough=0.35, metal=0.6)
    fg = [box((1.5, 0.85, 0.06), (cx, 0.75, 0.78), material=tm, bevel=0.015)]
    for lx in (-0.68, 0.68):
        for ly in (-0.36, 0.36):
            fg.append(cylinder(0.025, 0.76, (cx + lx, 0.75 + ly, 0.38), material=metal("#5a5f66", 0.3, "leg"), verts=12, bevel=0))
    cm = plastic("#2f3640", 0.5, "chair")
    fg.append(box((0.48, 0.45, 0.05), (cx - 0.25, -0.05, 0.47), material=cm, bevel=0.02))
    fg.append(box((0.48, 0.05, 0.5), (cx - 0.25, -0.28, 0.75), material=cm, bevel=0.02))
    for lx in (-0.2, 0.2):
        for ly in (-0.18, 0.18):
            fg.append(cylinder(0.018, 0.46, (cx - 0.25 + lx, -0.05 + ly, 0.23), material=metal("#5a5f66", 0.3, "leg"), verts=10, bevel=0))
    # a cup and a folder on the table
    fg.append(lathe([(0.0, 0.0), (0.05, 0.0), (0.055, 0.11), (0.0, 0.1)], 24, (cx + 0.5, 0.65, 0.81), mat("cup", "#f6efe2", rough=0.3), 1, "cup"))
    fg.append(box((0.32, 0.24, 0.015), (cx - 0.35, 0.7, 0.815), (0, 0, 8), mat("folder", "#e6c27a", rough=0.6), bevel=0.003))
    lamp(cx, 0.75, "lamp_" + side)
    return fg

def station():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#0e1418"), 0.4)
    plane(60, 60, (0, 0, 0), material=paper(os.path.join(TEX, "floor_checker.png"), 0.35, "tiles"), name="floor")
    fg = room("left", "#34425c") + room("right", "#2d5a5e")
    box((0.3, 4.6, 5.0), (0, 0.85, 2.5), material=mat("divider", "#e6dccb", rough=0.7), bevel=0.02)   # the wall between them
    for sx in (-4.15, 4.15):
        box((0.3, 4.6, 5.0), (sx, 0.85, 2.5), material=mat("side", "#e6dccb", rough=0.7), bevel=0.02)
    box((0.34, 0.1, 5.0), (0, -1.45, 2.5), material=mat("cap", "#f2b04a", rough=0.5), bevel=0.02)
    for sx in (-4.15, 4.15):
        box((0.34, 0.1, 5.0), (sx, -1.45, 2.5), material=mat("cap", "#f2b04a", rough=0.5), bevel=0.02)
    area_light((-5, -8, 5), (0, 1, 1.5), 900, 5, "#fff0dc", "key")
    area_light((5, -7, 3), (0, 1, 1.2), 350, 5, "#bcd6ff", "fill")
    return fg

def station_angles():
    fg = station()
    for name, loc, tgt, lens, fs in (("station_wide", (0.0, -9.4, 2.1), (0.0, 0.8, 1.6), 22.5, 0),
                                     ("station_left", (-2.25, -4.3, 1.75), (-2.05, 0.9, 1.45), 30, 4.0),
                                     ("station_right", (2.25, -4.3, 1.75), (2.05, 0.9, 1.45), 30, 4.0)):
        for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(o)
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=fg)

def market():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny()
    plane(400, 400, (0, 0, 0), material=mat("sand", "#efd3a0", rough=0.9, noise_bump=0.1), name="sand")
    plane(400, 160, (0, 115, 0.04), material=mat("sea", "#1f8fbf", rough=0.05, coat=0.8), name="sea")
    fg = stall(-1.55, 0.0, "awning_stripes.png", "APPLES", 0.8) + stall(1.55, 0.0, "awning_blue.png", "APPLES", 0.8)
    for sx in (-1.55, 1.55):
        for i in range(8):
            row, col = divmod(i, 4)
            apple2((sx - 0.36 + col * 0.24 + (0.12 if row else 0), 0.1 + row * 0.18, 0.765), 0.07, f"disp{sx}{i}")
    basket(-3.1, -0.4, 7, 1); basket(3.1, -0.5, 6, 2)
    crate(-3.0, 0.7, 0.3); barrel(3.2, 0.8)
    bunting(-2.6, 2.6, -0.9, 3.0)
    palm(-3.8, 5.5, 4.6, 1); palm(3.4, 7.5, 5.2, 2); palm(-7.0, 10.0, 5.4, 3); palm(7.5, 6.0, 4.8, 4)
    camera((0.0, -6.9, 1.9), (0.0, 0.0, 1.3), lens=22, fstop=6.0)
    still("plate_market_two", 1080, 1920, 40)
    still("fg_market_two", 1080, 1920, 24, only=fg)

def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")

def computer():
    beige = plastic("#e8dcc0", 0.45, "beige")
    box((0.62, 0.55, 0.5), (0, 0.05, 0.42), material=beige, bevel=0.06)               # CRT body
    box((0.5, 0.06, 0.38), (0, -0.23, 0.44), material=mat("bezel", "#3a3f46", rough=0.4), bevel=0.03)
    box((0.42, 0.03, 0.3), (0, -0.26, 0.44), material=glow("#3ccf7a", 1.4, "crt"), bevel=0.01)
    for k in range(4):
        box((0.22 - 0.04 * (k % 2), 0.005, 0.02), (-0.08 + 0.02 * (k % 2), -0.28, 0.54 - k * 0.055), material=glow("#d9ffe6", 3, "txt"), bevel=0)
    box((0.66, 0.6, 0.17), (0, 0.05, 0.085), material=beige, bevel=0.03)              # base unit
    box((0.2, 0.01, 0.025), (0.15, -0.255, 0.09), material=mat("slot", "#3a3f46"), bevel=0)
    box((0.7, 0.26, 0.05), (0, -0.48, 0.03), (8, 0, 0), material=beige, bevel=0.02)  # keyboard
    for r in range(3):
        for c in range(10):
            box((0.05, 0.05, 0.02), (-0.27 + c * 0.06, -0.54 + r * 0.06, 0.065 + r * 0.008), material=mat("key", "#8a7f6a", rough=0.5), bevel=0.006)

station_angles()
market()
prop_scene(); computer(); sprite_camera((0, -0.1, 0.35), 2.6, 0.9, 50, azimuth=-22)
still("computer", 700, 700, 28, transparent=True, crop=True)
