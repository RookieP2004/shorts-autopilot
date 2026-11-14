# 2026-11-14-b: "He drank bacteria to win an argument" (wild-story). Sets: a sunny 1980s hospital research lab in Perth
# (mint walls, checker floor, a long bench with petri dishes, a microscope, a warm incubator, a beige computer, a big
# window with blue sky and a palm, a 1984 wall calendar), 2 angles + a bench close-up; a glossy stomach interior (pink
# folds/rugae, a yellow-green acid pool with bubbles, mucus, spiral bacteria clinging to the lining), 2 angles.
# Cut-outs: a beaker of cloudy broth, a spiral bacterium, a gold medal (fictional design), a petri dish.
import math, os, random

# checker_mat(), seg(), tree(), bush(), sunny() ... (frozen helpers from an earlier town job)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def tube(points, r, material, name="tube", res=12):
    """A smooth round tube along a list of 3D points (a bevelled poly curve)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new("NURBS"); sp.points.add(len(points) - 1)
    for p, q in zip(sp.points, points):
        p.co = (*q, 1)
    sp.order_u = 4; sp.use_endpoint_u = True; sp.resolution_u = res
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    return ob


def bug_mat():
    return bpy.data.materials.get("hpylori") or mat("hpylori", "#7cc35a", rough=0.2, coat=0.7, sss=0.25)


def spiral_bug(loc, L=0.9, r=0.07, turns=2.2, rot=(0, 0, 0), name="bug"):
    """H. pylori: a short corkscrew body with a tuft of flagella at one end."""
    pts = []
    n = 40
    for k in range(n + 1):
        t = k / n
        a = t * turns * 2 * math.pi
        pts.append((-L / 2 + t * L, math.cos(a) * r * 1.6, math.sin(a) * r * 1.6))
    parts = [tube(pts, r, bug_mat(), name + "_body", 16)]
    fm = bpy.data.materials.get("flag") or mat("flag", "#4f8f3a", rough=0.35)
    end = pts[-1]
    for j in range(4):
        b = j / 4 * 2 * math.pi
        fp = []
        for k in range(14):
            t = k / 13
            fp.append((end[0] + t * L * 0.9, end[1] + math.cos(b) * t * r * 3 + math.sin(t * 9 + j) * r * 0.9,
                       end[2] + math.sin(b) * t * r * 3 + math.cos(t * 9 + j) * r * 0.9))
        parts.append(tube(fp, r * 0.18, fm, name + f"_fl{j}", 8))
    for p in parts:
        p.location = loc
    g = group(parts, name, loc)
    g.rotation_euler = tuple(math.radians(a) for a in rot)
    return g


def petri(x, y, z, s=1.0, col="#f2d48a", seed=0, name="petri"):
    g = bpy.data.materials.get("petri_glass") or mat("petri_glass", "#eef8ff", rough=0.06, coat=0.6, alpha=0.3)
    agar = bpy.data.materials.get("agar" + col) or mat("agar" + col, col, rough=0.25, coat=0.5, sss=0.2)
    cylinder(0.16 * s, 0.03 * s, (x, y, z + 0.015 * s), material=g, verts=40, bevel=0.004)
    cylinder(0.15 * s, 0.018 * s, (x, y, z + 0.012 * s), material=agar, verts=40, bevel=0.002)
    random.seed(seed)
    cm = bpy.data.materials.get("colony") or mat("colony", "#f6efe2", rough=0.4, coat=0.3)
    for k in range(7):
        a = random.uniform(0, 6.28); d = random.uniform(0, 0.11 * s)
        sphere(random.uniform(0.008, 0.016) * s, (x + math.cos(a) * d, y + math.sin(a) * d, z + 0.022 * s), (1, 1, 0.4), cm, seg=12)


def beaker(x, y, z, s=1.0, name="beaker"):
    g = bpy.data.materials.get("beaker_glass") or mat("beaker_glass", "#eef8ff", rough=0.05, coat=0.7, alpha=0.25)
    broth = bpy.data.materials.get("broth") or mat("broth", "#d8c46a", rough=0.15, coat=0.6, sss=0.3, alpha=0.92,
                                                    emit="#e8d77a", emit_strength=0.08)
    r = 0.11 * s; h = 0.3 * s
    lathe([(0, 0), (r * 0.9, 0), (r, r * 0.12), (r, h), (r * 1.12, h + 0.01 * s), (r * 1.12, h + 0.02 * s), (0, h + 0.02 * s)],
          40, (x, y, z), g, 1, name)
    lathe([(0, 0.01 * s), (r * 0.92, 0.012 * s), (r * 0.96, r * 0.12), (r * 0.96, h * 0.62), (0, h * 0.63)], 40, (x, y, z), broth, 1, name + "_liq")
    tm = bpy.data.materials.get("bk_tick") or mat("bk_tick", "#f6efe2", rough=0.4)
    for k in range(4):
        box((0.004 * s, 0.03 * s, 0.006 * s), (x - r * 0.35, y - r * 1.0, z + h * (0.25 + k * 0.17)), material=tm, bevel=0)


# ---------------------------------------------------------------- the 1984 lab
def build_lab():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#dfe8e0"), 0.45)
    plane(40, 40, (0, 0, 0), material=checker_mat("lab_floor", "#e3dccb", "#9fbfa8", 0.9), name="floor")
    box((30, 0.3, 9), (0, 4.6, 4.5), material=mat("lab_wall", "#9fd3b8", rough=0.7), bevel=0)
    box((30, 0.1, 1.1), (0, 4.42, 0.55), material=mat("lab_wains", "#34425c", rough=0.5, coat=0.3), bevel=0.02)
    box((30, 0.14, 0.06), (0, 4.4, 1.12), material=metal("#c9a24a", 0.3, "trim"), bevel=0.01)
    box((0.3, 20, 9), (-6.5, -2, 4.5), material=mat("lab_wall_l", "#8cc7a9", rough=0.7), bevel=0)
    # the big window with sky, a palm and a sun-lit frame
    sky = mat("win_sky", "#8fd0f0", rough=0.5, emit="#bfe6ff", emit_strength=1.6)
    box((2.6, 0.05, 2.0), (2.6, 4.43, 2.7), material=sky, bevel=0)
    fr = mat("win_frame", "#f6efe2", rough=0.4, coat=0.3)
    for zz in (1.7, 3.7):
        box((2.8, 0.12, 0.1), (2.6, 4.38, zz), material=fr, bevel=0.02)
    for xx in (1.3, 2.6, 3.9):
        box((0.1, 0.12, 2.1), (xx, 4.38, 2.7), material=fr, bevel=0.02)
    palm = mat("palm_leaf", "#3f8a3e", rough=0.6, emit="#3f8a3e", emit_strength=0.3)
    trunk = mat("palm_trunk", "#8a5a30", rough=0.7, emit="#8a5a30", emit_strength=0.2)
    cylinder(0.06, 1.6, (3.3, 4.41, 2.3), (0, 8, 0), trunk, verts=12)
    for k in range(6):
        a = k / 6 * 2 * math.pi
        sphere(0.36, (3.42 + math.cos(a) * 0.32, 4.405, 3.15 + math.sin(a) * 0.12), (1.3, 0.15, 0.3), palm, seg=16).rotation_euler = (0, math.cos(a) * 0.5, 0)
    # wall calendar 1984 + a chart poster
    box((0.8, 0.04, 1.0), (-3.4, 4.42, 2.9), material=mat("cal_paper", "#f6efe2", rough=0.6), bevel=0.01)
    box((0.8, 0.05, 0.28), (-3.4, 4.41, 3.29), material=mat("cal_top", "#d9534f", rough=0.5), bevel=0.01)
    text3d("1984", 0.4, (-3.4, 4.37, 2.6), (90, 0, 0), mat("cal_ink", "#1a1410", rough=0.5), font="display", extrude=0.01)
    box((1.0, 0.04, 1.3), (-1.6, 4.42, 2.85), material=mat("poster", "#f2b04a", rough=0.6), bevel=0.01)
    pm = mat("poster_ink", "#7c2533", rough=0.5)
    for k in range(4):
        box((0.12, 0.02, 0.2 + k * 0.18), (-1.95 + k * 0.23, 4.39, 2.4 + (0.2 + k * 0.18) / 2), material=pm, bevel=0.005)
    text3d("RESEARCH", 0.42, (0.4, 4.36, 4.2), (90, 0, 0), mat("sign_ink", "#34425c", rough=0.5), font="display", extrude=0.04)
    # the back bench along the wall: incubator, computer, microscope, petri dishes, bottles
    top_m = mat("bench_top", "#f6efe2", rough=0.25, coat=0.5)
    body_m = wood("#c58b4e", "#9a6634", "bench_body", 3.0)
    box((9.0, 0.8, 0.9), (-0.5, 3.8, 0.45), material=body_m, bevel=0.03)
    box((9.2, 0.9, 0.07), (-0.5, 3.78, 0.93), material=top_m, bevel=0.02)
    inc = mat("incubator", "#e9e2d6", rough=0.35, coat=0.4)
    box((1.0, 0.7, 1.1), (-4.0, 3.85, 1.52), material=inc, bevel=0.05)
    box((0.7, 0.05, 0.7), (-4.0, 3.48, 1.55), material=mat("inc_win", "#ffb45a", rough=0.2, emit="#ffb45a", emit_strength=1.4), bevel=0.02)
    box((0.9, 0.05, 0.12), (-4.0, 3.48, 2.0), material=mat("inc_panel", "#34425c", rough=0.4), bevel=0.01)
    beige = mat("pc_beige", "#e6d8b8", rough=0.45, coat=0.2)
    box((0.9, 0.75, 0.75), (-2.3, 3.9, 1.35), material=beige, bevel=0.06)
    box((0.62, 0.04, 0.48), (-2.3, 3.52, 1.38), material=mat("crt", "#1c3a2a", rough=0.15, emit="#3fbf6a", emit_strength=0.6), bevel=0.04)
    box((0.9, 0.35, 0.05), (-2.3, 3.4, 0.98), material=beige, bevel=0.015)
    random.seed(3)
    for k in range(9):
        petri(-1.2 + k * 0.26 + random.uniform(-0.03, 0.03), 3.65 + random.uniform(-0.12, 0.12), 0.965, 1.0,
              random.choice(("#f2d48a", "#e8a39a", "#f6dd9a")), k, f"pd{k}")
    bcol = ["#d9534f", "#6fc3c0", "#f2b04a", "#7c2533", "#46965a"]
    for k in range(7):
        bm = bpy.data.materials.get("bot" + bcol[k % 5]) or mat("bot" + bcol[k % 5], bcol[k % 5], rough=0.15, coat=0.6, sss=0.1)
        h = random.uniform(0.25, 0.42)
        lathe([(0, 0), (0.08, 0), (0.09, 0.03), (0.09, h), (0.04, h + 0.06), (0.03, h + 0.12), (0, h + 0.12)], 24,
              (1.6 + k * 0.28, 3.9, 0.965), bm, 1, "bottle")
    # shelf above the bench with jars
    shelf = wood("#c58b4e", "#9a6634", "shelf", 4.0)
    box((3.2, 0.4, 0.05), (-0.2, 4.25, 3.6), material=shelf, bevel=0.01)
    for k in range(6):
        col = bcol[(k + 2) % 5]
        jm = bpy.data.materials.get("jar" + col) or mat("jar" + col, col, rough=0.15, coat=0.6, sss=0.1)
        lathe([(0, 0), (0.1, 0), (0.12, 0.05), (0.12, 0.3), (0.08, 0.34), (0, 0.34)], 24, (-1.4 + k * 0.48, 4.2, 3.625), jm, 1, "jar")
    # front-left: a microscope on a small round table, a plant
    tm = wood("#a8743f", "#7a4e2a", "tbl", 4.0)
    cylinder(0.55, 0.06, (-2.6, 0.9, 0.86), material=top_m, verts=48, bevel=0.02)
    cylinder(0.06, 0.84, (-2.6, 0.9, 0.42), material=tm, verts=16)
    cylinder(0.3, 0.04, (-2.6, 0.9, 0.02), material=tm, verts=32)
    mm = mat("scope", "#f6efe2", rough=0.3, coat=0.5); mk = mat("scope_k", "#25262b", rough=0.3)
    box((0.3, 0.26, 0.05), (-2.6, 0.95, 0.915), material=mk, bevel=0.015)
    box((0.07, 0.07, 0.45), (-2.52, 1.02, 1.14), (-12, 0, 0), mm, bevel=0.02)
    cylinder(0.05, 0.28, (-2.6, 0.92, 1.32), (35, 0, 0), mk, verts=24)
    petri(-2.3, 0.75, 0.89, 1.0, "#f2d48a", 21, "pd_front")
    plant = mat("plant", "#4f9e4a", rough=0.6)
    for px in (-5.6, 5.6):
        lathe([(0, 0), (0.3, 0), (0.38, 0.55), (0.0, 0.55)], 32, (px, 2.6, 0), mat("pot", "#c4623a", rough=0.6), 1, "pot")
        for k in range(6):
            sphere(0.35, (px + random.uniform(-0.25, 0.25), 2.6 + random.uniform(-0.2, 0.2), 0.9 + k * 0.12), 1, plant, seg=20)
    lampm = mat("lamp", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    for x in (-2.5, 0.5, 3.5):
        box((1.2, 0.3, 0.06), (x, 2.0, 4.6), material=lampm, bevel=0.02)
    island()
    area_light((-3, -4, 6), (0, 1, 1.5), 1300, 4, "#fff0dc", "key"); area_light((4, -2, 4), (0, 1, 1.5), 380, 4, "#dbe8ff", "fill")
    area_light((2.6, 3.0, 2.8), (0, 0, 0.5), 300, 2.5, "#fff4d8", "window_bounce")


def island():
    """A mid-ground island bench (right) with microscopes, a beaker rack and petri stacks; a coat rack and a trolley."""
    top_m = bpy.data.materials["bench_top"]
    body_m = wood("#3d7f7c", "#2c605d", "island_body", 3.0)
    box((2.6, 0.9, 0.86), (2.4, 2.1, 0.43), material=body_m, bevel=0.04)
    box((2.8, 1.0, 0.07), (2.4, 2.1, 0.895), material=top_m, bevel=0.025)
    for k in range(3):
        box((0.7, 0.03, 0.6), (1.55 + k * 0.85, 1.63, 0.45), material=wood("#4a918d", "#336e6a", "drawer", 3.0), bevel=0.02)
        cylinder(0.03, 0.03, (1.55 + k * 0.85, 1.6, 0.62), (90, 0, 0), metal("#c9a24a", 0.25, "brass"), verts=16)
    mm = bpy.data.materials["scope"]; mk = bpy.data.materials["scope_k"]
    for sx in (1.6, 3.3):
        box((0.3, 0.26, 0.05), (sx, 2.2, 0.955), material=mk, bevel=0.015)
        box((0.07, 0.07, 0.45), (sx + 0.08, 2.27, 1.18), (-12, 0, 0), mm, bevel=0.02)
        cylinder(0.05, 0.28, (sx, 2.17, 1.36), (35, 0, 0), mk, verts=24)
    for k in range(4):
        for j in range(3):
            petri(2.1 + k * 0.3, 1.95, 0.93 + j * 0.032, 0.9, ("#f2d48a", "#e8a39a", "#f6dd9a")[j], k * 3 + j, f"stk{k}{j}")
    for k in range(4):
        beaker(2.2 + k * 0.22, 2.4, 0.93, 0.9, f"ib{k}")
    # coat rack with two white coats (left wall)
    cm = metal("#3b3f46", 0.4, "rack_m")
    cylinder(0.035, 2.0, (-5.2, 1.0, 1.0), material=cm, verts=12)
    cylinder(0.3, 0.04, (-5.2, 1.0, 0.02), material=cm, verts=24)
    coat = mat("coat", "#f6efe2", rough=0.7)
    for dx in (-0.18, 0.18):
        lathe([(0, 1.95), (0.18, 1.9), (0.28, 1.6), (0.3, 1.0), (0.0, 1.0)], 24, (-5.2 + dx, 1.0, 0), coat, 1, "coat")
    # a steel trolley with bottles (right front)
    st = metal("#c9ced6", 0.3, "trolley")
    for z in (0.35, 0.85):
        box((0.9, 0.55, 0.04), (4.9, 0.4, z), material=st, bevel=0.01)
    for dx in (-0.4, 0.4):
        for dy in (-0.24, 0.24):
            cylinder(0.02, 0.85, (4.9 + dx, 0.4 + dy, 0.45), material=st, verts=8)
    for k in range(3):
        lathe([(0, 0), (0.07, 0), (0.08, 0.03), (0.08, 0.28), (0.035, 0.34), (0, 0.34)], 24, (4.65 + k * 0.25, 0.4, 0.87),
              mat(f"tb{k}", ("#d9534f", "#6fc3c0", "#f2b04a")[k], rough=0.15, coat=0.6), 1, "tbot")


def lab_angles():
    build_lab()
    for name, loc, tgt, lens, fs in (("lab_wide", (0.0, -8.0, 1.7), (0.0, 2.5, 2.0), 26, 6.0),
                                     ("lab_mid", (-0.8, -4.4, 1.45), (-0.4, 2.5, 1.6), 30, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)


# ---------------------------------------------------------------- the stomach interior
def build_stomach():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15)
    world_color(hexrgb("#7a2a3a"), 0.6)
    lin_a = mat("lining_a", "#e8848c", rough=0.22, coat=0.8, sss=0.35, noise_bump=0.2)
    lin_b = mat("lining_b", "#d9646f", rough=0.22, coat=0.8, sss=0.35, noise_bump=0.2)
    lin_c = mat("lining_c", "#f2a5a0", rough=0.22, coat=0.8, sss=0.35, noise_bump=0.2)
    plane(200, 200, (0, 0, -0.02), material=lin_b, name="base")
    random.seed(7)
    # floor folds (rugae): long wavy ridges running away from camera, leaving a central walkway
    for k in range(-6, 7):
        if k == 0:
            continue
        x0 = k * 0.9 + (0.35 if k > 0 else -0.35)
        pts = [(x0 + math.sin(j * 0.9 + k) * 0.25, -4 + j * 1.6, 0.05) for j in range(14)]
        tube(pts, 0.22 + abs(k) * 0.02, random.choice((lin_a, lin_c)), f"ruga{k}", 16)
    # walls: an arch of big folds curving over, like a tunnel
    for row in range(14):
        for side in (-1, 1):
            for k in range(8):
                a = 0.25 + k * 0.17
                rad = 7.5 + random.uniform(-0.3, 0.3)
                x = side * math.cos(a) * rad
                z = math.sin(a) * rad * 1.15
                y = -3 + row * 2.4 + random.uniform(-0.4, 0.4)
                sphere(1.0, (x, y, z), (0.7, 1.6, 0.7), random.choice((lin_a, lin_b, lin_c)), seg=24)
    # roof folds
    for row in range(14):
        for k in range(-3, 4):
            sphere(1.1, (k * 1.6 + random.uniform(-0.2, 0.2), -3 + row * 2.4, 8.6 + random.uniform(-0.3, 0.3)), (0.9, 1.5, 0.6),
                   random.choice((lin_a, lin_b)), seg=24)
    # the acid lake far down the tunnel, with bubbles rising
    acid = mat("acid", "#c9e04a", rough=0.04, coat=1.0, emit="#d8f06a", emit_strength=0.5)
    cylinder(4.2, 0.06, (0, 24.0, 0.18), material=acid, verts=64, bevel=0.03).scale = (1.0, 2.0, 1.0)
    bub = mat("bubble", "#f2fbc0", rough=0.05, coat=1.0, emit="#e8f79a", emit_strength=0.5, alpha=0.6)
    for k in range(26):
        sphere(random.uniform(0.06, 0.2), (random.uniform(-3, 3), random.uniform(18, 28), random.uniform(0.3, 2.5)), 1, bub, seg=16)
    # mucus: soft translucent blobs on the folds
    muc = mat("mucus", "#fbe3e0", rough=0.05, coat=1.0, alpha=0.45, sss=0.3)
    for k in range(24):
        sphere(random.uniform(0.15, 0.35), (random.choice((-1, 1)) * random.uniform(1.4, 5), random.uniform(0, 16), random.uniform(0.2, 2.5)), 1, muc, seg=16)
    # spiral bacteria clinging to the lining (big hero ones near camera, more down the tunnel)
    for k, (x, y, z, L, rz) in enumerate([(-0.3, 3.2, 0.75, 2.0, 20), (1.6, 6.0, 0.9, 1.8, -30), (-2.4, 8.5, 2.6, 1.8, 60),
                                          (2.8, 10.5, 3.0, 1.8, -50), (-0.8, 13.0, 0.8, 1.6, 10), (1.0, 16.0, 1.2, 1.6, -15),
                                          (-4.2, 5.0, 3.6, 1.6, 80), (4.3, 7.0, 4.0, 1.6, -80)]):
        spiral_bug((x, y, z), L, L * 0.075, 2.2, (random.uniform(-15, 15), random.uniform(-15, 15), rz), f"sb{k}")
    area_light((-5, -6, 7), (0, 6, 1), 2400, 6, "#fff0dc", "key")
    area_light((5, 12, 5), (0, 4, 1), 1500, 6, "#9fd8ff", "rim")
    area_light((0, -8, 3), (0, 3, 1.5), 500, 8, "#ffd7c2", "fill")


def stomach_angles():
    build_stomach()
    drop_cams(); camera((0.0, -6.5, 1.9), (0, 8, 2.2), lens=24, fstop=0)
    still("plate_stomach_wide", 1080, 1920, 40)
    drop_cams(); camera((0.9, 0.2, 1.3), (-0.3, 3.2, 0.75), lens=34, fstop=2.8)
    still("plate_stomach_close", 1080, 1920, 40)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#e9f0ea"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def medal():
    gm = metal("#e0b040", 0.22, "medal_gold")
    rib = mat("ribbon", "#34425c", rough=0.5)
    parts = [cylinder(0.4, 0.06, (0, 0, 0.4), (90, 0, 0), gm, verts=64, bevel=0.015),
             torus(0.36, 0.025, (0, -0.035, 0.4), (90, 0, 0), metal("#c9962e", 0.3, "medal_rim"))]
    # a raised five-point star (fictional design)
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = 0.22 if k % 2 == 0 else 0.09
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    for (x0, z0), (x1, z1) in zip(pts, pts[1:] + pts[:1]):
        seg((x0, -0.045, 0.4 + z0), (x1, -0.045, 0.4 + z1), 0.018, metal("#f2c75a", 0.2, "medal_star"))
    parts.append(box((0.2, 0.02, 0.5), (-0.12, 0.0, 0.95), (0, 18, 0), rib, bevel=0.005))
    parts.append(box((0.2, 0.02, 0.5), (0.12, 0.0, 0.95), (0, -18, 0), mat("ribbon2", "#d9534f", rough=0.5), bevel=0.005))
    return parts


if not os.environ.get("BK_PROPS_ONLY"):
    lab_angles()
    stomach_angles()
prop_scene(500, 800); beaker(0, 0, 0, 2.0); camera((0, -2.3, 0.75), (0, 0, 0.32), lens=50, fstop=0)
still("beaker", 500, 800, 28, transparent=True, crop=True)
prop_scene(); spiral_bug((0, 0, 0.4), 1.0, 0.09, 2.2, (0, -10, 10), "hero_bug"); sprite_camera((0.3, 0, 0.4), 3.6, 0.9, 50, azimuth=0)
still("bug", 900, 600, 32, transparent=True, crop=True)
prop_scene(); medal(); camera((0, -2.6, 0.75), (0, 0, 0.6), lens=50, fstop=0)
still("medal", 600, 800, 32, transparent=True, crop=True)
prop_scene(); petri(0, 0, 0, 2.5, "#f2d48a", 5); sprite_camera((0, 0, 0.03), 2.2, 1.4, 50, azimuth=0)
still("petri", 700, 500, 28, transparent=True, crop=True)
