# 2026-11-18-a: "He told doctors to wash their hands" (wild-story: Semmelweis, Vienna 1847).
# Sets: a sunlit 1840s maternity ward (long hall, tall arched windows with sky, cream walls with a teal dado, plank floor,
# two rows of black iron beds with white sheets and blue blankets, a door at the far end), 2 angles (wide down the aisle,
# mid by a bed); the washstand close-up (a wooden stand by a window with a porcelain basin of pale-green chlorine water, a
# jug, a soap bar, a brown glass jar labelled CHLORINE, a folded towel); the dissection hall in the night mood (a stone
# table under a white cloth, a tray of tools, an oil lamp, one hard spot from above). Cut-outs: the jar, a soap bar.
import math, os, random


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def iron_bed(x, y, blanket, rotz=0.0):
    iron = bpy.data.materials.get("iron") or mat("iron", "#2a2d33", rough=0.35, metal=0.6, coat=0.3)
    sheet = bpy.data.materials.get("sheet") or mat("sheet", "#f7f3ea", rough=0.75, sss=0.05)
    L, W = 1.9, 0.9
    # frame posts + head/foot rails (bed runs along x, head against the wall side)
    for dx in (-L / 2, L / 2):
        for dy in (-W / 2, W / 2):
            hgt = 1.05 if dx < 0 else 0.75
            cylinder(0.03, hgt, (x + dx, y + dy, hgt / 2), material=iron, verts=12, bevel=0)
        hgt = 1.0 if dx < 0 else 0.7
        cylinder(0.022, W, (x + dx, y, hgt), (90, 0, 0), iron, verts=12, bevel=0)
        cylinder(0.018, W, (x + dx, y, hgt - 0.22), (90, 0, 0), iron, verts=12, bevel=0)
        for k in range(4):
            cylinder(0.012, 0.22, (x + dx, y - W / 2 + (k + 1) * W / 5, hgt - 0.11), material=iron, verts=8, bevel=0)
    box((L, W - 0.02, 0.18), (x, y, 0.52), material=sheet, bevel=0.06)
    box((0.36, W - 0.2, 0.12), (x - L / 2 + 0.28, y, 0.66), material=sheet, bevel=0.05)
    box((L * 0.62, W + 0.04, 0.06), (x + L * 0.17, y, 0.63), material=blanket, bevel=0.03)


def ward():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15)
    world_color(hexrgb("#dfe8f2"), 0.45)
    plane(40, 60, (0, 8, 0), material=wood("#a8805a", "#7d5a3a", "planks", 9.0, 0.75), name="floor")
    wallm = mat("ward_wall", "#f6e6c8", rough=0.8)
    dado = mat("ward_dado", "#5e9e98", rough=0.6, coat=0.2)
    for sx in (-1, 1):
        box((0.3, 40, 7), (sx * 3.6, 8, 3.5), material=wallm, bevel=0)
        box((0.06, 40, 1.0), (sx * 3.44, 8, 0.5), material=dado, bevel=0)
        # tall arched windows with sky light
        sky = bpy.data.materials.get("win_sky") or mat("win_sky", "#9fd4f2", rough=0.5, emit="#cdeaff", emit_strength=2.2)
        fr = bpy.data.materials.get("win_fr") or mat("win_fr", "#f6efe2", rough=0.4, coat=0.3)
        for k in range(7):
            yy = 0.4 + k * 2.6
            box((0.05, 1.1, 2.0), (sx * 3.43, yy, 2.6), material=sky, bevel=0)
            cylinder(0.55, 0.05, (sx * 3.43, yy, 3.6), (0, 90, 0), sky, verts=32, bevel=0)
            box((0.1, 1.24, 0.1), (sx * 3.4, yy, 1.58), material=fr, bevel=0.02)
            box((0.1, 0.07, 2.5), (sx * 3.4, yy, 2.8), material=fr, bevel=0.01)
            box((0.1, 1.15, 0.06), (sx * 3.4, yy, 2.6), material=fr, bevel=0.01)
    box((8, 0.3, 7), (0, 19, 3.5), material=wallm, bevel=0)
    door = wood("#6e4426", "#4f2f18", "door", 3.0)
    box((1.6, 0.12, 2.6), (0, 18.84, 1.3), material=door, bevel=0.03)
    cylinder(0.8, 0.14, (0, 18.8, 2.6), (90, 0, 0), door, verts=32, bevel=0)
    box((2.0, 0.1, 0.2), (0, 18.78, 3.5), material=wood("#6e4426", "#4f2f18", "lintel", 3.0), bevel=0.02)
    box((8, 40, 0.2), (0, 8, 6.2), material=mat("ceil", "#f4ead6", rough=0.9), bevel=0)
    for k in range(6):
        box((7.2, 0.25, 0.3), (0, k * 3.4, 5.95), material=wood("#8a5a30", "#6a4020", f"beam{k}", 4.0), bevel=0.02)
    blues = [mat("blanket_a", "#3f6fa8", rough=0.85), mat("blanket_b", "#5b86b8", rough=0.85)]
    for k in range(7):
        yy = 0.4 + k * 2.6
        iron_bed(-2.35, yy, blues[k % 2])
        iron_bed(2.35, yy, blues[(k + 1) % 2])
        # bedside stool
        cylinder(0.18, 0.04, (-1.2, yy + 0.75, 0.48), material=door, verts=24)
        cylinder(0.18, 0.04, (1.2, yy - 0.75, 0.48), material=door, verts=24)
    # a hanging lamp row
    lampm = mat("lamp", "#fff3d6", emit="#ffe6b0", emit_strength=4.0)
    for k in range(4):
        sphere(0.14, (0, 1.0 + k * 4.5, 4.6), 1, lampm, seg=16)
        cylinder(0.008, 1.3, (0, 1.0 + k * 4.5, 5.3), material=mat("chain", "#2a2d33"), verts=6, bevel=0)
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 3.2; sun.color = hexrgb("#ffe2b8"); sun.angle = math.radians(4)
    so = bpy.data.objects.new("sun", sun); bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(55), math.radians(-35), math.radians(-60))
    area_light((-2.5, -3, 4.5), (0, 3, 1.2), 900, 4, "#fff0dc", "key")
    area_light((2.5, 4, 4.5), (0, 5, 1.0), 500, 5, "#dbe8ff", "fill")


def washstand(x, y, s=1.0):
    st = wood("#9a6634", "#7a4e2a", "stand", 4.0)
    box((0.9 * s, 0.55 * s, 0.06 * s), (x, y, 0.92 * s), material=st, bevel=0.02)
    for dx in (-0.4, 0.4):
        for dy in (-0.22, 0.22):
            cylinder(0.03 * s, 0.9 * s, (x + dx * s, y + dy * s, 0.45 * s), material=st, verts=12)
    box((0.86 * s, 0.5 * s, 0.03 * s), (x, y, 0.25 * s), material=st, bevel=0.01)
    por = mat("porcelain", "#fbf8f1", rough=0.12, coat=0.8)
    lathe([(0, 0), (0.1 * s, 0), (0.28 * s, 0.1 * s), (0.31 * s, 0.13 * s), (0.30 * s, 0.135 * s), (0.0, 0.03 * s)], 48,
          (x - 0.1 * s, y, 0.95 * s), por, 1, "basin")
    water = mat("chlorine_water", "#bfe8c0", rough=0.03, transmission=0.6, coat=0.6)
    cylinder(0.27 * s, 0.01 * s, (x - 0.1 * s, y, 1.06 * s), material=water, verts=48, bevel=0)
    # jug
    lathe([(0, 0), (0.07 * s, 0), (0.1 * s, 0.12 * s), (0.08 * s, 0.26 * s), (0.06 * s, 0.32 * s), (0.08 * s, 0.36 * s), (0, 0.36 * s)],
          32, (x + 0.33 * s, y + 0.1 * s, 0.95 * s), por, 1, "jug")
    # soap bar + towel
    box((0.12 * s, 0.07 * s, 0.04 * s), (x + 0.26 * s, y - 0.17 * s, 0.97 * s), material=mat("soap", "#f2e3b0", rough=0.4, coat=0.3), bevel=0.015)
    box((0.3 * s, 0.05 * s, 0.4 * s), (x + 0.47 * s, y - 0.1 * s, 0.75 * s), material=mat("towel", "#f6efe2", rough=0.9), bevel=0.02)
    chlorine_jar(x + 0.2 * s, y + 0.18 * s, 0.95 * s, 0.9 * s)


def chlorine_jar(x, y, z, s=1.0):
    jar = mat("jar_glass", "#7a4a1e", rough=0.1, coat=0.8, transmission=0.3)
    lathe([(0, 0), (0.08 * s, 0), (0.09 * s, 0.02 * s), (0.09 * s, 0.22 * s), (0.05 * s, 0.27 * s), (0.04 * s, 0.31 * s), (0, 0.31 * s)],
          32, (x, y, z), jar, 1, "jar")
    cylinder(0.045 * s, 0.04 * s, (x, y, z + 0.32 * s), material=mat("cork", "#c49a62", rough=0.8), verts=16)
    lab = mat("jar_label", "#f6efe2", rough=0.6)
    box((0.12 * s, 0.01 * s, 0.09 * s), (x, y - 0.088 * s, z + 0.12 * s), material=lab, bevel=0.0)
    text3d("Cl", 0.06 * s, (x, y - 0.096 * s, z + 0.1 * s), (90, 0, 0), mat("jar_ink", "#1a1410", rough=0.5), font="display", extrude=0.002)


def wash_set():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15)
    world_color(hexrgb("#dfe8f2"), 0.5)
    plane(20, 20, (0, 0, 0), material=wood("#b07a46", "#86562e", "planks2", 9.0, 0.55), name="floor")
    box((10, 0.3, 6), (0, 1.0, 3), material=mat("w_wall", "#efe1c6", rough=0.8), bevel=0)
    box((10, 0.06, 1.0), (0, 0.84, 0.5), material=mat("w_dado", "#5e9e98", rough=0.6, coat=0.2), bevel=0)
    sky = mat("win_sky2", "#9fd4f2", rough=0.5, emit="#cdeaff", emit_strength=2.2)
    fr = mat("win_fr2", "#f6efe2", rough=0.4, coat=0.3)
    box((1.1, 0.05, 1.6), (1.1, 0.84, 2.2), material=sky, bevel=0)
    cylinder(0.55, 0.05, (1.1, 0.84, 3.0), (90, 0, 0), sky, verts=32, bevel=0)
    box((1.24, 0.1, 0.08), (1.1, 0.8, 1.38), material=fr, bevel=0.02)
    box((0.06, 0.1, 2.2), (1.1, 0.8, 2.45), material=fr, bevel=0.01)
    washstand(0, 0.35, 1.0)
    area_light((-2.0, -2.5, 3.0), (0, 0.3, 1.0), 450, 3, "#fff0dc", "key")
    area_light((1.4, 0.2, 2.6), (0, 0.3, 1.0), 220, 1.5, "#cfe6ff", "window")
    area_light((2.5, -2.0, 1.6), (0, 0.3, 1.0), 120, 2, "#ffe6c8", "fill")
    camera((0.15, -1.7, 1.55), (-0.02, 0.35, 1.0), lens=34, fstop=3.2)


def dissection():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2)
    night_set((0, 0, 0.9), rim="#3fa9ff", spot_power=9000, spot_height=7.0, spot_angle=34, grid=False, floor_color="#1c2230")
    stone = mat("stone", "#8d8a84", rough=0.6, noise_bump=0.4)
    box((2.2, 0.9, 0.12), (0, 0, 0.9), material=stone, bevel=0.03)
    for dx in (-0.8, 0.8):
        box((0.22, 0.6, 0.84), (dx, 0, 0.42), material=stone, bevel=0.02)
    cloth = mat("cloth", "#f2eee4", rough=0.85, sss=0.05)
    box((2.0, 1.0, 0.03), (0, 0, 0.975), material=cloth, bevel=0.01)
    for sx in (-1, 1):
        box((2.0, 0.03, 0.3), (0, sx * 0.5, 0.84), material=cloth, bevel=0.01)
    # tool tray with metal tools, an oil lamp, a ledger
    tray = mat("tray", "#c9ccd1", rough=0.2, metal=0.9)
    box((0.6, 0.35, 0.03), (1.6, -0.3, 0.9), material=tray, bevel=0.01)
    cylinder(0.25, 0.86, (1.6, -0.3, 0.44), material=wood("#5a3a22", "#3a2414", "tstand", 3.0), verts=24)
    for k in range(4):
        box((0.42, 0.02, 0.012), (1.6, -0.42 + k * 0.08, 0.925), (0, 0, 4 - k * 3), tray, bevel=0.003)
    lamp_glass = mat("lamp_glass", "#ffd690", emit="#ffbe5c", emit_strength=6.0)
    lathe([(0, 0), (0.1, 0), (0.12, 0.08), (0.07, 0.12), (0, 0.12)], 24, (-1.55, -0.2, 0.92), metal("#b8862f", 0.3, "lampbase"), 1)
    lathe([(0, 0), (0.06, 0), (0.08, 0.1), (0.05, 0.24), (0.04, 0.3), (0, 0.3)], 24, (-1.55, -0.2, 1.04), lamp_glass, 1)
    L = bpy.data.lights.new("oil", "POINT"); L.energy = 60; L.color = hexrgb("#ffb35c"); L.shadow_soft_size = 0.05
    o = bpy.data.objects.new("oil", L); bpy.context.scene.collection.objects.link(o); o.location = (-1.55, -0.2, 1.2)
    cam, _ = camera((1.6, -4.4, 2.2), (0, 0.1, 0.95), lens=30, fstop=2.4)
    dutch(cam, 5)


if not os.environ.get("BK_PROPS_ONLY"):
    ward()
    drop_cams(); camera((0.0, -3.4, 1.65), (0, 8.0, 1.2), lens=22, fstop=8.0)
    still("plate_ward_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.6, 1.0, 1.4), (-2.6, 5.4, 0.8), lens=26, fstop=4.0)
    still("plate_ward_mid", 1080, 1920, 40)
    wash_set(); still("plate_wash", 1080, 1920, 40)
    dissection(); still("plate_dissect", 1080, 1920, 40)

# cut-outs
reset(800, 800, 30, 0.1, samples=24, bloom=0)
world_color(hexrgb("#dfe8f2"), 0.6)
area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")
chlorine_jar(0, 0, 0, 3.0)
camera((0, -3.0, 0.9), (0, 0, 0.45), lens=55, fstop=0)
still("jar", 500, 800, 32, transparent=True, crop=True)
reset(800, 800, 30, 0.1, samples=24, bloom=0)
world_color(hexrgb("#dfe8f2"), 0.6)
area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")
box((0.6, 0.35, 0.2), (0, 0, 0.1), material=mat("soap_c", "#f2e3b0", rough=0.4, coat=0.3), bevel=0.07)
camera((0.6, -1.8, 1.2), (0, 0, 0.1), lens=55, fstop=0)
still("soap", 600, 500, 28, transparent=True, crop=True)
