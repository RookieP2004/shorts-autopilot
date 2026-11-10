# 2026-11-10-b sets and cut-outs: a bright little blood lab (bench with a test-tube rack as the foreground layer,
# shelves of jars, a heart-shaped wall sign, plants), a giant cut-away skin model in a museum-like studio (epidermis,
# dermis, fat, one big dark-red vein and a small bright artery seen in cross-section, a bluish line on top over the vein),
# and props: bright-red vial, dark-red vial, blue vial, horseshoe crab.
import math, os, random


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def blood_mat(kind):
    cols = {"bright": ("#c4121c", "#ff2a2a"), "dark": ("#5a0610", "#7a0a14"), "blue": ("#2f6fd6", "#4f9cff")}
    c, e = cols[kind]
    return bpy.data.materials.get("blood_" + kind) or mat("blood_" + kind, c, rough=0.08, coat=0.8, sss=0.15,
                                                          emit=e, emit_strength=0.12)


def vial(x, y, z, kind="bright", s=1.0, cap="#f6efe2", name="vial"):
    """A rounded test tube (z = bottom) with liquid and a cap. Height ~0.3*s."""
    g = bpy.data.materials.get("tube_glass") or mat("tube_glass", "#eef8ff", rough=0.08, coat=0.6, alpha=0.22)
    r = 0.04 * s
    prof = [(0, 0), (r * 0.7, r * 0.15), (r, r * 0.7), (r, 0.30 * s), (r * 1.08, 0.305 * s), (0, 0.305 * s)]
    tube = lathe(prof, 32, (x, y, z), g, 1, name)
    lp = [(0, r * 0.05), (r * 0.74, r * 0.17), (r * 1.02, r * 0.72), (r * 1.02, 0.2 * s), (r * 0.6, 0.201 * s), (0, 0.202 * s)]
    liq = lathe(lp, 48, (x, y, z), blood_mat(kind), 0, name + "_liq")
    capm = bpy.data.materials.get("cap" + cap) or mat("cap" + cap, cap, rough=0.35, coat=0.4)
    c = cylinder(r * 1.15, 0.05 * s, (x, y, z + 0.32 * s), material=capm, verts=32, bevel=0.006)
    return [tube, liq, c]


def rack(x, y, z, kinds):
    m = bpy.data.materials.get("rack") or mat("rack", "#6fc3c0", rough=0.35, coat=0.4)
    out = [box((0.16 * len(kinds) + 0.1, 0.16, 0.03), (x, y, z + 0.015), material=m, bevel=0.01),
           box((0.16 * len(kinds) + 0.1, 0.16, 0.03), (x, y, z + 0.16), material=m, bevel=0.01)]
    for sx in (-1, 1):
        out.append(box((0.03, 0.16, 0.19), (x + sx * (0.08 * len(kinds) + 0.035), y, z + 0.095), material=m, bevel=0.008))
    for k, kd in enumerate(kinds):
        out += vial(x - 0.08 * (len(kinds) - 1) + k * 0.16, y, z + 0.035, kd, 1.0, name=f"rv{k}")
    return out


# ---------------------------------------------------------------- the blood lab
def build_lab():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    world_color(hexrgb("#f3ece2"), 1.0)
    plane(40, 40, (0, 0, 0), material=mat("floor_tile", "#e9e2d6", rough=0.35, coat=0.2), name="floor")
    box((7.0, 3.4, 0.02), (0.2, -0.8, 0.01), material=mat("rug", "#34425c", rough=0.9), bevel=0.005)
    box((6.6, 3.0, 0.025), (0.2, -0.8, 0.012), material=mat("rug_in", "#e8a39a", rough=0.9), bevel=0.005)
    box((30, 0.3, 9), (0, 4.6, 4.5), material=mat("wall", "#f7dccb", rough=0.7), bevel=0)
    box((30, 0.1, 1.2), (0, 4.42, 0.6), material=mat("wainscot", "#7c2533", rough=0.5, coat=0.3), bevel=0.02)
    box((30, 0.14, 0.06), (0, 4.4, 1.22), material=metal("#c9a24a", 0.3, "trim"), bevel=0.01)
    box((0.3, 20, 9), (-6.5, -2, 4.5), material=mat("wall_l", "#f0cfbd", rough=0.7), bevel=0)
    random.seed(2)
    shelf = wood("#c58b4e", "#9a6634", "shelf", 4.0)
    jar_cols = ["#d9534f", "#f2b04a", "#6fc3c0", "#e8a39a", "#7c2533", "#46965a"]
    for sz in (1.9, 2.9):
        box((3.4, 0.4, 0.05), (-2.0, 4.2, sz), material=shelf, bevel=0.01)
        for k in range(7):
            col = jar_cols[(k + int(sz)) % len(jar_cols)]
            jm = bpy.data.materials.get("jar" + col) or mat("jar" + col, col, rough=0.15, coat=0.6, sss=0.1)
            h = random.uniform(0.22, 0.4)
            lathe([(0, 0), (0.1, 0), (0.12, 0.05), (0.12, h), (0.08, h + 0.04), (0, h + 0.04)], 28, (-3.4 + k * 0.46, 4.15, sz + 0.025), jm, 1, "jar")
    text3d("BLOOD LAB", 0.5, (-2.0, 4.35, 4.0), (90, 0, 0), mat("sign_ink", "#7c2533", rough=0.5), font="display", extrude=0.04)
    # a big red drop sign on the wall (right)
    dm = mat("drop_sign", "#d9534f", rough=0.3, coat=0.5)
    lathe([(0, 0), (0.3, 0.06), (0.42, 0.25), (0.4, 0.45), (0.25, 0.7), (0.08, 0.95), (0, 1.05)], 40, (2.2, 4.3, 2.4), dm, 1, "drop")
    o = bpy.data.objects["drop"]; o.scale = (1, 0.25, 1)
    # a heart-rate monitor screen
    box((1.0, 0.08, 0.65), (3.9, 4.35, 2.0), material=mat("monitor", "#25262b", rough=0.3, coat=0.5), bevel=0.03)
    box((0.86, 0.02, 0.52), (3.9, 4.30, 2.0), material=mat("screen", "#16232b", emit="#2a6f6a", emit_strength=0.8), bevel=0.01)
    pts = [(-0.38, 0), (-0.15, 0), (-0.08, 0.16), (0.0, -0.14), (0.06, 0.06), (0.12, 0), (0.38, 0)]
    gm = mat("ecg", "#9ff7a8", emit="#7dff8a", emit_strength=4.0)
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, z1 - z0)
        c = cylinder(0.012, L, (3.9 + (x0 + x1) / 2, 4.28, 2.0 + (z0 + z1) / 2), (0, math.degrees(math.atan2(x1 - x0, z1 - z0)), 0), gm, verts=8, bevel=0)
    # bench (foreground layer) with the rack, a microscope and a clipboard
    top_m = mat("bench_top", "#f6efe2", rough=0.25, coat=0.5)
    body_m = wood("#3d7f7c", "#2c605d", "bench_body", 3.0)
    bench = [box((2.6, 0.8, 0.86), (-1.0, 0.5, 0.43), material=body_m, bevel=0.04),
             box((2.8, 0.95, 0.07), (-1.0, 0.48, 0.895), material=top_m, bevel=0.025)]
    for k in range(3):
        bench.append(box((0.7, 0.03, 0.6), (-1.85 + k * 0.85, 0.09, 0.45), material=wood("#4a918d", "#336e6a", "drawer", 3.0), bevel=0.02))
        bench.append(cylinder(0.03, 0.03, (-1.85 + k * 0.85, 0.06, 0.62), (90, 0, 0), metal("#c9a24a", 0.25, "brass"), verts=16))
    bench += rack(-1.35, 0.45, 0.93, ["bright", "bright", "dark", "dark", "bright", "dark"])
    # microscope
    mm = mat("scope", "#f6efe2", rough=0.3, coat=0.5); mk = mat("scope_k", "#25262b", rough=0.3)
    bench.append(box((0.3, 0.26, 0.05), (-0.1, 0.55, 0.955), material=mk, bevel=0.015))
    bench.append(box((0.07, 0.07, 0.45), (-0.02, 0.62, 1.18), (-12, 0, 0), mm, bevel=0.02))
    bench.append(cylinder(0.05, 0.28, (-0.1, 0.52, 1.36), (35, 0, 0), mk, verts=24))
    bench.append(box((0.22, 0.2, 0.02), (-0.1, 0.5, 1.08), material=mk, bevel=0.005))
    bench.append(box((0.26, 0.34, 0.015), (0.5, 0.35, 0.94), (0, 0, -10), mat("clip", "#f2b04a", rough=0.6), bevel=0.005))
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
    area_light((-1.3, -0.4, 1.9), (-1.3, 0.45, 1.0), 120, 1.2, "#fff6e8", "rack_spot")
    return bench


def lab_angles():
    bench = build_lab()
    for name, loc, tgt, lens, fs in (("lab_wide", (0.2, -9.0, 2.4), (0.2, 1.5, 1.5), 26, 6.0),
                                     ("lab_mid", (-0.6, -4.0, 1.55), (-0.9, 0.6, 1.15), 34, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 24, only=bench)
    drop_cams(); camera((-1.35, -0.55, 1.2), (-1.35, 0.45, 1.05), lens=40, fstop=2.2)   # macro on the rack
    still("plate_rack_close", 1080, 1920, 40)


# ---------------------------------------------------------------- the giant skin model
def skin_model():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.1)
    world_color(hexrgb("#1c2b33"), 0.6)
    floor("#24343d", 0.5)
    # a low plinth
    box((3.6, 2.0, 0.18), (0, 0, 0.09), material=mat("plinth", "#34425c", rough=0.4, coat=0.3), bevel=0.04)
    W, D = 3.0, 1.6
    z0 = 0.18
    fat = mat("fat", "#f2d48a", rough=0.5, sss=0.2)
    derm = mat("dermis", "#e8a39a", rough=0.5, sss=0.25)
    epi = mat("epidermis", "#d99a78", rough=0.45, sss=0.2, coat=0.2)
    box((W, D, 0.55), (0, 0, z0 + 0.275), material=fat, bevel=0.01)
    box((W, D, 0.5), (0, 0, z0 + 0.55 + 0.25), material=derm, bevel=0.01)
    box((W, D, 0.14), (0, 0, z0 + 1.05 + 0.07), material=epi, bevel=0.03)
    # fat lobules bulging on the front face
    random.seed(5)
    fm = mat("fat_lob", "#f6dd9a", rough=0.45, sss=0.2)
    for k in range(26):
        sphere(random.uniform(0.07, 0.11), (random.uniform(-W / 2 + 0.12, W / 2 - 0.12), -D / 2 + 0.01, z0 + random.uniform(0.08, 0.48)),
               (1, 0.35, 1), fm, seg=20)
    # the vein (big, dark red) and an artery (small, bright red), running front to back
    vx, vz = 0.35, z0 + 0.78
    vw = mat("vein_wall", "#b04a5a", rough=0.4, sss=0.2)
    cylinder(0.22, D + 0.04, (vx, 0, vz), (90, 0, 0), vw, verts=48, bevel=0.01)
    cylinder(0.18, D + 0.06, (vx, 0, vz), (90, 0, 0), blood_mat("dark"), verts=48, bevel=0.0)
    aw = mat("art_wall", "#e0b0a8", rough=0.4, sss=0.2)
    cylinder(0.1, D + 0.04, (-0.75, 0, z0 + 0.62), (90, 0, 0), aw, verts=40, bevel=0.01)
    cylinder(0.06, D + 0.06, (-0.75, 0, z0 + 0.62), (90, 0, 0), blood_mat("bright"), verts=40, bevel=0.0)
    # the bluish line on top over the vein (what we see from outside)
    box((0.34, D - 0.02, 0.01), (vx, 0, z0 + 1.195), material=mat("blue_look", "#6f8fc0", rough=0.5, alpha=0.75), bevel=0.0)
    # little hairs on top
    hm = mat("hair", "#4a3220", rough=0.6)
    for k in range(18):
        hx = random.uniform(-W / 2 + 0.1, W / 2 - 0.1); hy = random.uniform(-D / 2 + 0.1, D / 2 - 0.1)
        cylinder(0.008, 0.18, (hx, hy, z0 + 1.28), (random.uniform(-25, 25), random.uniform(-25, 25), 0), hm, verts=6, bevel=0)
    # labels stand on the plinth
    lab = mat("label", "#f6efe2", rough=0.4)
    for txt_, lx in (("SKIN", -1.2),):
        text3d(txt_, 0.16, (lx, -1.0, 0.28), (90, 0, 0), lab, font="body", extrude=0.02)
    area_light((-3.5, -4, 4.5), (0, 0, 0.8), 1500, 3.5, "#ffe2c2", "key")
    area_light((3.5, 4, 3), (0, 0, 0.8), 700, 2.5, "#8fd3ff", "rim")
    area_light((4, -3, 1.5), (0, 0, 0.8), 260, 4, "#9fb4c8", "fill")


def skin_angles():
    skin_model()
    drop_cams(); camera((1.1, -6.2, 1.75), (0.7, 0, 1.0), lens=27, fstop=6.0)
    still("plate_skin_wide", 1080, 1920, 40)
    drop_cams(); camera((0.2, -4.0, 1.85), (0.2, 0, 0.85), lens=30, fstop=5.0)
    still("plate_skin_close", 1080, 1920, 40)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def horseshoe_crab():
    shell = mat("crab_shell", "#7a5a34", rough=0.3, coat=0.7)
    dark = mat("crab_dark", "#4e3820", rough=0.35, coat=0.6)
    s = sphere(0.3, (0, 0.05, 0.05), (1.0, 0.85, 0.32), shell, seg=48)
    ab = sphere(0.18, (0, -0.28, 0.04), (0.85, 0.7, 0.28), dark, seg=40)
    for k in (-1, 1):
        sphere(0.04, (k * 0.13, 0.12, 0.13), (0.6, 0.9, 0.4), dark, seg=16)       # eyes ridges
        for j in range(4):
            sp = cone(0.012, 0.06, (k * (0.11 + j * 0.01), -0.2 - j * 0.04, 0.06), (0, k * 70, 0), dark)
    cone(0.03, 0.55, (0, -0.68, 0.03), (90, 0, 0), dark)
    sphere(0.05, (0, 0.1, 0.15), (2.5, 0.2, 0.3), dark, seg=16)                  # centre ridge


if not os.environ.get("BK_PROPS_ONLY"):
    lab_angles()
    skin_angles()
for kind in ("bright", "dark", "blue"):
    prop_scene(); vial(0, 0, 0, kind, 2.0, name="hero_" + kind); camera((0, -2.2, 0.55), (0, 0, 0.33), lens=55, fstop=0)
    still("vial_" + kind, 400, 800, 28, transparent=True, crop=True)
prop_scene(); horseshoe_crab(); camera((1.6, -1.9, 2.3), (0, -0.2, 0.05), lens=50, fstop=0)
still("crab", 700, 700, 28, transparent=True, crop=True)
