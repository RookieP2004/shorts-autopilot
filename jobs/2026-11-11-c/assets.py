# 2026-11-11-c: "Why is nothing ever really free?" (big-question, opportunity cost). Sets: a golden-hour town plaza with a
# pizza stall (left) and a little cinema kiosk with a glowing marquee (right), houses, lamps, bunting, trees: a wide plus a
# medium on each stall (pizza counter as a foreground layer); an economists' lecture hall (chalkboard with the 4 answer
# options, desk, books). Cut-outs: pizza, cinema ticket, popcorn bucket, alarm clock, phone.
import math, os, random

# tree(), bush(), house(), bench(), seg(), checker_mat() + sunny(), stall(), bunting(), crate(), barrel() (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\ndef cake")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def pizza(loc=(0, 0, 0), r=0.3, name="pizza"):
    x, y, z = loc
    crust = mat("crust", "#d9a35a", rough=0.7, noise_bump=0.3)
    sauce = mat("sauce", "#c8361f", rough=0.45, coat=0.3)
    cheese = mat("cheese", "#f4cf6a", rough=0.4, coat=0.3, sss=0.1)
    pep = mat("pepperoni", "#9e1f1a", rough=0.35, coat=0.4)
    basil = mat("basil", "#3f8a3e", rough=0.5)
    parts = [lathe([(0.0, 0.0), (r * 0.92, 0.0), (r, r * 0.06), (r * 0.97, r * 0.12), (r * 0.88, r * 0.13), (r * 0.85, r * 0.08),
                    (0.0, r * 0.08)], 48, (x, y, z), crust, 1, name + "_crust"),
             cylinder(r * 0.84, r * 0.02, (x, y, z + r * 0.09), material=sauce, verts=48, bevel=0),
             cylinder(r * 0.8, r * 0.025, (x, y, z + r * 0.105), material=cheese, verts=48, bevel=0)]
    random.seed(len(name))
    for k in range(9):
        a = k / 9 * 2 * math.pi + 0.3
        d = r * (0.5 if k % 2 else 0.25)
        parts.append(cylinder(r * 0.11, r * 0.02, (x + math.cos(a) * d, y + math.sin(a) * d, z + r * 0.13), material=pep, verts=24, bevel=0))
    for k in range(5):
        a = random.uniform(0, 6.28); d = random.uniform(0.1, 0.6) * r
        sphere(r * 0.05, (x + math.cos(a) * d, y + math.sin(a) * d, z + r * 0.14), (1.4, 0.8, 0.25), basil, seg=12)
    return parts


def cinema(x, y):
    """A small cinema kiosk: teal body, red marquee with glowing bulbs, a poster and a ticket window."""
    body = mat("kiosk", "#2f8f8a", rough=0.5, coat=0.3)
    trim = mat("kiosk_trim", "#f2b04a", rough=0.4, coat=0.4)
    red = mat("marquee", "#b3121b", rough=0.4, coat=0.4)
    parts = [box((2.0, 1.3, 2.3), (x, y, 1.15), material=body, bevel=0.06),
             box((2.3, 1.5, 0.12), (x, y, 2.36), material=trim, bevel=0.04),
             box((2.2, 0.35, 0.7), (x, y - 0.75, 2.8), material=red, bevel=0.06),
             box((0.8, 0.06, 0.62), (x - 0.35, y - 0.67, 1.35), material=mat("window", "#cfe6f2", rough=0.08, coat=0.8), bevel=0.02),
             box((0.95, 0.08, 0.12), (x - 0.35, y - 0.7, 0.98), material=trim, bevel=0.02)]
    text3d("CINEMA", 0.44, (x, y - 0.94, 2.8), (90, 0, 0), mat("marq_ink", "#ffd04a", rough=0.35),
           font="display", extrude=0.02)
    bulb = mat("bulb", "#fff2c8", rough=0.2, emit="#ffd27a", emit_strength=6.0)
    for k in range(12):
        sphere(0.045, (x - 1.02 + k * 0.186, y - 0.94, 3.12), 1, bulb, seg=12)
        sphere(0.045, (x - 1.02 + k * 0.186, y - 0.94, 2.48), 1, bulb, seg=12)
    # poster: a moon over mountains (fictional film)
    box((0.62, 0.05, 0.9), (x + 0.55, y - 0.67, 1.4), material=mat("poster", "#34425c", rough=0.6), bevel=0.02)
    sphere(0.11, (x + 0.6, y - 0.7, 1.62), (1, 0.3, 1), mat("moon", "#f6efe2", rough=0.4, emit="#fff2c8", emit_strength=0.4), seg=20)
    cone(0.26, 0.4, (x + 0.48, y - 0.71, 1.12), (90, 0, 0), mat("mount", "#6fc3c0", rough=0.6))
    box((0.66, 0.06, 0.08), (x + 0.55, y - 0.7, 0.92), material=trim, bevel=0.01)
    return parts


def lamp(x, y):
    cylinder(0.05, 3.4, (x, y, 1.7), material=metal("#3b3f46", 0.4, "lamp"), verts=12)
    sphere(0.18, (x, y, 3.45), 1, mat("globe", "#f6efe2", rough=0.2, emit="#ffd9a0", emit_strength=4.0))


def build_plaza():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny("#3f8fe0", "#ffe2bc", sun=3.4)
    sun = bpy.data.objects.get("sun"); sun.data.color = hexrgb("#ffd3a0")
    sun.rotation_euler = (math.radians(66), math.radians(-6), math.radians(-48))      # low golden-hour sun from the left
    plane(300, 300, (0, 0, 0), material=checker_mat("cobbles", "#e6cfa6", "#d2b78c", 0.9), name="cobbles")
    counter = stall(-2.3, 1.2, "awning_stripes.png", "PIZZA", 0.85)
    for k, (dx, dy) in enumerate(((-0.6, 0.15), (0.0, 0.05), (0.6, 0.18))):
        pizza((-2.3 + dx, 1.2 + dy, 0.81), 0.24, f"disp_pizza{k}")
    cylinder(0.32, 0.5, (-2.3 + 1.25, 1.0, 0.25), material=wood("#8a5a30", "#5e3a1c", "logs", 3.0), verts=24)
    cinema(2.35, 1.7)
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#f6efe2", "#c9b7e3", "#9fd39a", "#e3c99a"]
    for k in range(9):
        house(-12 + k * 3.0, 9.5 + (k % 2) * 0.8, 2.7, 4 + (k * 53 % 4), cols[k % 7], ["#b5533c", "#34425c", "#7c2533"][k % 3])
    bunting(-4.2, 4.2, 4.0, 4.4)
    tree(-5.4, 4.5, 4.0, 1.4, 7); tree(5.6, 5.0, 4.2, 1.5, 8, "#5aa64a"); tree(0.2, 7.0, 3.6, 1.3, 9)
    bench(0.1, 3.4)
    bush(-4.0, 2.2, 0.5, seed=4); bush(4.3, 2.6, 0.5, "#46965a", "#d9534f", 5)
    for x in (-3.9, 3.9, 0.0):
        lamp(x, 2.0 if x else 5.0)
    return counter


def plaza_angles():
    counter = build_plaza()
    for name, loc, tgt, lens in (("plaza_wide", (0.2, -9.6, 2.4), (0, 1.6, 1.7), 26),
                                 ("pizza_mid", (-1.4, -3.9, 1.6), (-2.15, 1.2, 1.25), 30),
                                 ("cinema_mid", (1.5, -3.8, 1.6), (2.25, 1.7, 1.35), 30)):
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=0)
        still("plate_" + name, 1080, 1920, 40)
        if name != "cinema_mid":
            still("fg_" + name, 1080, 1920, 24, only=counter)


def hall():
    reset(1080, 1920, 30, 0.1, samples=36, bloom=0)
    world_color(hexrgb("#2a3550"), 1.0)
    floor("#3a4766", rough=0.5)
    board = mat("chalkboard", "#24463a", rough=0.85)
    box((5.2, 0.12, 2.6), (0, 4.0, 2.6), material=board, bevel=0.03)
    box((5.4, 0.16, 0.14), (0, 3.95, 1.24), material=wood("#a8743f", "#7a4e2a", "board_ledge", 4.0), bevel=0.03)
    box((5.4, 0.16, 0.14), (0, 3.95, 3.96), material=wood("#a8743f", "#7a4e2a", "board_top", 4.0), bevel=0.03)
    chalk = mat("chalk", "#f3efe6", rough=0.9, emit="#f3efe6", emit_strength=0.25)
    text3d("OPPORTUNITY COST = ?", 0.34, (0, 3.92, 3.45), (90, 0, 0), chalk, font="body", extrude=0.005, bevel=0)
    for k, t in enumerate(("$0", "$10", "$40", "$50")):
        text3d(t, 0.5, (-1.8 + k * 1.2, 3.92, 2.4), (90, 0, 0), chalk, font="display", extrude=0.005, bevel=0)
    desk = wood("#9a6436", "#6e4424", "desk", 3.0)
    box((2.6, 1.0, 0.1), (0, 0.8, 0.95), material=desk, bevel=0.03)
    for sx in (-1.15, 1.15):
        box((0.12, 0.9, 0.9), (sx, 0.8, 0.45), material=desk, bevel=0.02)
    for k, c in enumerate(("#d9534f", "#f2b04a", "#6fc3c0", "#46965a")):
        box((0.55, 0.38, 0.08), (-0.8, 0.8, 1.04 + k * 0.085), (0, 0, k * 7), mat(f"book{k}", c, rough=0.6), bevel=0.01)
    for k in range(5):
        box((0.3, 0.42, 0.004), (0.5 + k * 0.05, 0.75, 1.01 + k * 0.004), (0, 0, -10 + k * 9), mat("sheet", "#f6efe2", rough=0.8), bevel=0)
    area_light((-4, -4, 5), (0, 2, 1.8), 1700, 4, "#ffe2c2", "key")
    area_light((4, 3, 4), (0, 2, 1.5), 900, 3, "#8fd3ff", "rim")
    area_light((0, -6, 2), (0, 3, 2.4), 400, 6, "#c8d6ff", "fill")
    camera((0, -6.5, 2.1), (0, 2.0, 1.9), lens=26, fstop=0)
    still("plate_hall", 1080, 1920, 36)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#f1e4dc"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def ticket():
    pap = mat("ticket", "#f2b04a", rough=0.6)
    ink = mat("tick_ink", "#7c2533", rough=0.5)
    p = [box((1.2, 0.02, 0.55), (0, 0, 0.3), material=pap, bevel=0.02)]
    box((0.02, 0.03, 0.5), (0.32, -0.002, 0.3), material=ink, bevel=0)
    text3d("ADMIT", 0.16, (-0.12, -0.02, 0.38), (90, 0, 0), ink, font="display", extrude=0.004, bevel=0)
    text3d("ONE", 0.16, (-0.12, -0.02, 0.2), (90, 0, 0), ink, font="display", extrude=0.004, bevel=0)
    text3d("$10", 0.13, (0.47, -0.02, 0.3), (90, 0, 90), ink, font="display", extrude=0.004, bevel=0)
    return p


def popcorn():
    stripes = paper(os.path.join(TEX, "awning_stripes.png"), 0.6, "pop_stripes")
    tub = lathe([(0.0, 0.0), (0.22, 0.0), (0.3, 0.55), (0.28, 0.55), (0.2, 0.03), (0.0, 0.03)], 36, (0, 0, 0),
                mat("tub", "#d6483e", rough=0.5, coat=0.3), 1, "tub")
    for k in range(8):
        a = k / 8 * 2 * math.pi
        seg((math.cos(a) * 0.215, math.sin(a) * 0.215, 0.02), (math.cos(a) * 0.29, math.sin(a) * 0.29, 0.53), 0.03,
            mat("tub_w", "#f6efe2", rough=0.5))
    random.seed(3)
    k_m = mat("kernel", "#fff4d6", rough=0.7, noise_bump=0.4)
    for k in range(70):
        a = random.uniform(0, 6.28); d = random.uniform(0, 0.27)
        sphere(random.uniform(0.045, 0.065), (math.cos(a) * d, math.sin(a) * d, 0.55 + random.uniform(0, 0.16) * (1 - d / 0.3)),
               (1, 0.9, 0.85), k_m, seg=10)
    return tub


def alarm_clock():
    red = mat("clk_red", "#d9534f", rough=0.3, coat=0.6)
    parts = [cylinder(0.4, 0.22, (0, 0, 0.5), (90, 0, 0), red, verts=48, bevel=0.04),
             cylinder(0.33, 0.02, (0, -0.12, 0.5), (90, 0, 0), mat("clk_face", "#f6efe2", rough=0.3), verts=48, bevel=0)]
    ink = mat("clk_ink", "#1a1410", rough=0.4)
    box((0.04, 0.02, 0.24), (0, -0.14, 0.6), material=ink, bevel=0.005)
    box((0.04, 0.02, 0.18), (0.07, -0.14, 0.46), (0, 50, 0), ink, bevel=0.005)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        box((0.025, 0.02, 0.06), (math.sin(a) * 0.28, -0.135, 0.5 + math.cos(a) * 0.28), (0, -math.degrees(a), 0), ink, bevel=0)
    bell = metal("#d9a441", 0.3, "bell")
    for sx in (-1, 1):
        sphere(0.13, (sx * 0.26, 0, 0.9), (1, 1, 0.7), bell, seg=24)
        seg((sx * 0.22, 0, 0.2), (sx * 0.3, 0, 0.05), 0.03, bell)
    return parts


def phone():
    parts = [box((0.42, 0.04, 0.86), (0, 0, 0.45), material=mat("phone", "#1a1410", rough=0.3, coat=0.7), bevel=0.06),
             box((0.37, 0.01, 0.76), (0, -0.022, 0.45), material=glow("#6fc3c0", 1.6, "phone_screen"), bevel=0.04)]
    for k in range(3):
        box((0.3, 0.012, 0.16), (0, -0.03, 0.66 - k * 0.21), material=mat(f"post{k}", ["#f2b04a", "#e8a598", "#f6efe2"][k], rough=0.5), bevel=0.01)
    return parts


plaza_angles()
hall()
prop_scene(); pizza((0, 0, 0), 0.5, "hero_pizza"); sprite_camera((0, 0, 0.05), 3.4, 1.4, 50, azimuth=-10)
still("pizza", 800, 600, 32, transparent=True, crop=True)
prop_scene(); ticket(); sprite_camera((0, 0, 0.3), 3.0, 0.6, 50, azimuth=-12)
still("ticket", 800, 500, 24, transparent=True, crop=True)
prop_scene(); popcorn(); sprite_camera((0, 0, 0.4), 3.0, 1.0, 50, azimuth=-15)
still("popcorn", 600, 700, 28, transparent=True, crop=True)
prop_scene(); alarm_clock(); sprite_camera((0, 0, 0.55), 3.2, 0.6, 50, azimuth=-12)
still("clock", 600, 700, 28, transparent=True, crop=True)
prop_scene(); phone(); sprite_camera((0, 0, 0.45), 3.2, 0.4, 50, azimuth=-15)
still("phone", 500, 700, 24, transparent=True, crop=True)
