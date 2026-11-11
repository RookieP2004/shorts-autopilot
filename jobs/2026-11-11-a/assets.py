# 2026-11-11-a: "All 8 billion humans fit in a sugar cube" (scale-shock). Sets: a sunny cafe terrace in the town square
# (bistro table with a sugar bowl, cup and one hero sugar cube, striped parasol, chairs, houses, bunting), 3 angles + a
# "crushed" variant (the cube has smashed the table into the cobbles); a football stadium (striped pitch, tiered stands,
# floodlights, a glass marble on the centre spot), 3 angles. Cut-outs: sugar cube, marble, electron, nucleus.
import math, os, random

# tree(), bush(), house(), bench(), seg(), checker_mat() + sunny(), bunting() from earlier town jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def sugar_mat():
    return bpy.data.materials.get("sugar") or mat("sugar", "#fbf8f2", rough=0.85, sss=0.25, noise_bump=0.6)


def sugar_cube(loc, s=0.06, rot=0, name="sugar"):
    o = box((s, s, s), (loc[0], loc[1], loc[2] + s / 2), (0, 0, rot), sugar_mat(), bevel=s * 0.08, name=name)
    return o


def bistro_chair(x, y, rot=0):
    ir = metal("#2f3a40", 0.35, "chair_iron")
    seat = mat("chair_seat", "#6fc3c0", rough=0.5)
    parts = [cylinder(0.22, 0.04, (x, y, 0.46), material=seat, verts=32)]
    for k in range(4):
        a = k / 4 * 2 * math.pi + 0.78
        parts.append(seg((x + math.cos(a) * 0.15, y + math.sin(a) * 0.15, 0.45), (x + math.cos(a) * 0.2, y + math.sin(a) * 0.2, 0.0), 0.015, ir))
    ry = math.radians(rot)
    bx, by = x + math.sin(ry) * 0.2, y + math.cos(ry) * 0.2
    t = torus(0.18, 0.02, (bx, by, 0.75), (90, 0, rot), ir)
    parts += [t, seg((bx - math.cos(ry) * 0.17, by + math.sin(ry) * 0.17, 0.46), (bx - math.cos(ry) * 0.17, by + math.sin(ry) * 0.17, 0.72), 0.015, ir),
              seg((bx + math.cos(ry) * 0.17, by - math.sin(ry) * 0.17, 0.46), (bx + math.cos(ry) * 0.17, by - math.sin(ry) * 0.17, 0.72), 0.015, ir)]
    return parts


def cup(x, y, z):
    china = mat("china", "#f6efe2", rough=0.2, coat=0.5)
    cylinder(0.075, 0.012, (x, y, z + 0.006), material=china, verts=32)
    lathe([(0.0, 0.0), (0.035, 0.0), (0.045, 0.02), (0.05, 0.075), (0.045, 0.075), (0.04, 0.025), (0.0, 0.02)], 32, (x, y, z + 0.012), china, 1, "cup")
    cylinder(0.042, 0.004, (x, y, z + 0.075), material=mat("coffee", "#5a3520", rough=0.1, coat=0.8), verts=32)
    torus(0.018, 0.006, (x + 0.055, y, z + 0.055), (90, 0, 0), china)


def sugar_bowl(x, y, z):
    lathe([(0.0, 0.0), (0.05, 0.0), (0.075, 0.04), (0.08, 0.08), (0.075, 0.085), (0.0, 0.08)], 32, (x, y, z),
          mat("bowl", "#6fc3c0", rough=0.25, coat=0.6), 1, "bowl")
    random.seed(3)
    for k in range(5):
        sugar_cube((x + random.uniform(-0.03, 0.03), y + random.uniform(-0.03, 0.03), z + 0.07), 0.028, random.uniform(0, 60), f"bowl_s{k}")


def parasol(x, y):
    cylinder(0.025, 2.4, (x, y, 1.2), material=metal("#c9ced6", 0.3, "pole"), verts=16)
    aw = paper(os.path.join(TEX, "awning_stripes.png"), 0.6, "parasol_cloth")
    c = cone(1.35, 0.5, (x, y, 2.35), (0, 0, 0), aw)
    sphere(0.05, (x, y, 2.62), 1, metal("#d9a441", 0.3, "finial"))
    return c


def table(x, y):
    top_m = wood("#8a5a30", "#5e3a1c", "cafe_top", 5.0, 0.35)
    ir = metal("#2f3a40", 0.35, "table_iron")
    return [cylinder(0.42, 0.04, (x, y, 0.74), material=top_m, verts=48, bevel=0.012),
            cylinder(0.035, 0.72, (x, y, 0.37), material=ir, verts=20),
            cylinder(0.24, 0.03, (x, y, 0.015), material=ir, verts=32)]


TX, TY = 0.55, 0.4          # the cafe table (the hero sugar cube sits on it)


def build_cafe(crushed=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sun=4.0)
    plane(300, 300, (0, 0, 0), material=checker_mat("cobbles", "#e6d3b0", "#d2bb92", 0.9), name="cobbles")
    cols = ["#f2b04a", "#6fc3c0", "#e8a598", "#f6efe2", "#c9b7e3", "#9fd39a", "#e3c99a"]
    for k in range(8):
        house(-10.5 + k * 3.0, 9.5 + (k % 2) * 0.8, 2.7, 4 + (k * 53 % 4), cols[k % 7], ["#b5533c", "#34425c", "#7c2533"][k % 3])
    bunting(-5.5, 5.5, 6.0, 4.4)
    tree(-4.6, 4.0, 4.0, 1.4, 7); tree(5.0, 5.0, 4.2, 1.5, 8, "#5aa64a")
    bush(-2.6, 2.2, 0.5, seed=4); bush(3.4, 2.6, 0.5, "#46965a", "#d9534f", 5)
    for x in (-3.4, 3.8):
        cylinder(0.05, 3.4, (x, 2.6, 1.7), material=metal("#3b3f46", 0.4, "lamp"), verts=12)
        sphere(0.18, (x, 2.6, 3.45), 1, mat("globe", "#f6efe2", rough=0.2, emit="#ffe2a8", emit_strength=1.0))
    # a second table behind, for life
    table(-1.9, 3.2); bistro_chair(-2.4, 3.3, 90); bistro_chair(-1.4, 3.5, -90); parasol(-1.9, 3.2)
    bistro_chair(TX + 0.55, TY + 0.25, -100)
    fg = []
    if not crushed:
        fg = table(TX, TY)
        cup(TX + 0.2, TY + 0.12, 0.76); sugar_bowl(TX - 0.2, TY + 0.15, 0.76)
        cylinder(0.07, 0.01, (TX, TY - 0.12, 0.765), material=mat("china", "#f6efe2", rough=0.2, coat=0.5), verts=32)
        sugar_cube((TX, TY - 0.12, 0.77), 0.06, 20, "hero_cube")
    else:
        top_m = wood("#8a5a30", "#5e3a1c", "cafe_top", 5.0, 0.35)
        ir = metal("#2f3a40", 0.35, "table_iron")
        # table top snapped and flat on the cobbles, pedestal knocked over, cup and bowl spilled
        a = cylinder(0.42, 0.04, (TX - 0.45, TY - 0.1, 0.05), (14, -18, 0), top_m, verts=48, bevel=0.012)
        cylinder(0.035, 0.72, (TX + 0.55, TY + 0.25, 0.04), (90, 0, 35), ir, verts=20)
        cylinder(0.24, 0.03, (TX + 0.3, TY + 0.55, 0.1), (60, 0, 20), ir, verts=32)
        cup(TX + 0.8, TY - 0.35, 0.0)
        random.seed(9)
        for k in range(6):
            sugar_cube((TX + random.uniform(-0.9, 0.9), TY + random.uniform(-0.7, 0.4), 0.0), 0.028, random.uniform(0, 80), f"spill{k}")
        # the crater: dark ring, cracks, the cube sunk into it
        cylinder(0.32, 0.02, (TX, TY - 0.12, 0.003), material=mat("crater", "#6e5a44", rough=0.9), verts=48, bevel=0)
        torus(0.34, 0.05, (TX, TY - 0.12, 0.0), material=mat("crater_rim", "#b39a76", rough=0.9))
        crack = mat("crack", "#3a2e24", rough=0.9)
        for k in range(9):
            ang = k / 9 * 360 + random.uniform(-15, 15)
            L = random.uniform(0.25, 0.6)
            r0 = math.radians(ang)
            box((L, 0.02, 0.01), (TX + math.cos(r0) * (0.3 + L / 2), TY - 0.12 + math.sin(r0) * (0.3 + L / 2), 0.004), (0, 0, ang), crack, bevel=0)
        sugar_cube((TX, TY - 0.12, -0.02), 0.06, 32, "hero_cube")
    area_light((-4, -5, 4), (TX, TY, 0.8), 500, 3, "#fff0dc", "fill_key")
    return fg


def cafe_plates():
    fg = build_cafe()
    for name, loc, tgt, lens, fs in (("cafe_wide", (0.3, -8.5, 2.0), (0.1, 1.5, 1.6), 26, 0),
                                     ("cafe_mid", (-0.3, -3.8, 1.45), (0.35, 0.6, 1.0), 32, 0)):
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
        still("fg_" + name, 1080, 1920, 32, only=fg)
    drop_cams()
    camera((TX + 0.12, TY - 0.72, 0.9), (TX, TY - 0.12, 0.8), lens=50, fstop=2.2)
    still("plate_cafe_table", 1080, 1920, 48)
    build_cafe(crushed=True)
    drop_cams()
    camera((-0.3, -3.8, 1.45), (0.35, 0.6, 1.0), lens=32, fstop=0)
    still("plate_cafe_crushed", 1080, 1920, 40)


def stadium():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sky_top="#2f86d6", sky_horizon="#cfe9fb", sun=4.2)
    plane(600, 600, (0, 0, -0.01), material=mat("ground", "#8fb36a", rough=0.9), name="ground")
    track = mat("track", "#c8664a", rough=0.85)
    plane(150, 100, (0, 0, 0.0), material=track, name="track")
    g1, g2 = mat("grass1", "#4fa84a", rough=0.85, noise_bump=0.15), mat("grass2", "#5dbb55", rough=0.85, noise_bump=0.15)
    for k in range(12):
        plane(105 / 12, 68, (-52.5 + 105 / 24 + k * 105 / 12, 0, 0.005), material=g1 if k % 2 else g2, name=f"stripe{k}")
    line = mat("line", "#f6efe2", rough=0.6)
    torus(9.15, 0.08, (0, 0, 0.01), material=line).scale = (1, 1, 0.1)
    plane(0.12, 68, (0, 0, 0.012), material=line, name="halfway")
    for sx in (-1, 1):
        plane(105, 0.12, (0, sx * 34, 0.012), material=line)
        plane(0.12, 68, (sx * 52.5, 0, 0.012), material=line)
        plane(16.5, 0.12, (sx * (52.5 - 8.25), 20.16, 0.012), material=line)
        plane(16.5, 0.12, (sx * (52.5 - 8.25), -20.16, 0.012), material=line)
        plane(0.12, 40.3, (sx * 36, 0, 0.012), material=line)
        # goals
        gm = mat("goal", "#f6efe2", rough=0.4)
        for gy in (-3.66, 3.66):
            cylinder(0.06, 2.44, (sx * 52.5, gy, 1.22), material=gm, verts=12)
        cylinder(0.06, 7.32, (sx * 52.5, 0, 2.44), (90, 0, 0), gm, verts=12)
    # tiered stands: bands of colour (seats), elongated into an oval bowl
    bands = [("#6fc3c0", 62, 70, 1.0, 9), ("#f2b04a", 70, 78, 9, 17), ("#d9534f", 78, 86, 17, 25), ("#34425c", 86, 92, 25, 31)]
    for k, (c, r0, r1, z0, z1) in enumerate(bands):
        prof = [(r0, z0 - 0.6)]
        n = int(r1 - r0)
        for i in range(n):          # stepped seat rows: each row throws a thin shadow line
            ra, za = r0 + i * (r1 - r0) / n, z0 + i * (z1 - z0) / n
            prof += [(ra, za), (ra + (r1 - r0) / n, za)]
        prof += [(r1, z1), (r1 + 0.6, z1), (r1 + 0.6, z0 - 0.6)]
        o = lathe(prof, 128, (0, 0, 0),
                  mat(f"seats{k}", c, rough=0.6, noise_bump=0.5), 0, f"band{k}")
        o.scale = (1.0, 0.68, 1.0)
    o = lathe([(60, 0), (62, 0.4), (62, 1.0), (60, 1.0)], 96, (0, 0, 0), mat("wall", "#efe3c8", rough=0.6), 0, "wall")
    o.scale = (1.0, 0.68, 1.0)
    roof = lathe([(80, 34), (95, 36), (95, 37), (80, 35)], 96, (0, 0, 0), metal("#d8dde3", 0.3, "roof"), 0, "roof")
    roof.scale = (1.0, 0.68, 1.0)
    for k in range(8):
        a = k / 8 * 2 * math.pi + 0.39
        x, y = math.cos(a) * 93, math.sin(a) * 93 * 0.68
        cylinder(0.6, 34, (x, y, 17), material=metal("#c9ced6", 0.3, "pillar"), verts=16)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * 98, sy * 62
            cylinder(0.5, 48, (x, y, 24), material=metal("#9aa0a8", 0.3, "mast"), verts=16)
            b = box((7, 1.0, 3.5), (x, y, 49), (0, 0, 0), mat("flood", "#fff6e0", rough=0.3, emit="#fff1c8", emit_strength=4.0), bevel=0.1)
            b.rotation_euler = (math.radians(-55 * sy), 0, math.atan2(-y, -x) + math.pi / 2)
    # the marble on the centre spot
    cylinder(0.11, 0.004, (0, 0, 0.013), material=line, verts=24)
    marble((0, 0, 0.12), 0.12)


def marble(loc, r=0.12):
    g = mat("marble_glass", "#dff4ff", rough=0.03, transmission=0.95, ior=1.5, coat=0.6)
    o = sphere(r, loc, 1, g, seg=48, name="marble")
    sw = mat("swirl", "#f2b04a", rough=0.2, emit="#f2b04a", emit_strength=0.4)
    t = torus(r * 0.5, r * 0.16, loc, (35, 20, 0), sw)
    t.scale = (1, 0.45, 1)
    t2 = torus(r * 0.42, r * 0.12, loc, (-40, 60, 0), mat("swirl2", "#d9534f", rough=0.2))
    t2.scale = (1, 0.5, 1)
    return o


def stadium_plates():
    stadium()
    for name, loc, tgt, lens, fs, _f in (("stadium_wide", (-72, -6, 44), (8, 0, 0), 24, 0, None),
                                          ("stadium_pitch", (-7.5, -0.6, 1.6), (3, 0.4, 1.4), 26, 0, None),
                                          ("stadium_marble", (-0.75, -0.22, 0.22), (0, 0, 0.12), 50, 2.0, None)):
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)


def prop_scene(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#f1e4dc"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def nucleus(loc=(0, 0, 0.5), r=0.12):
    random.seed(5)
    p = mat("proton", "#d9534f", rough=0.25, coat=0.6)
    n = mat("neutron", "#9fb4c8", rough=0.25, coat=0.6)
    pts = []
    k = 0
    while len(pts) < 14 and k < 400:
        k += 1
        v = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        d = math.sqrt(sum(c * c for c in v))
        if d > 1 or d < 0.2:
            continue
        q = tuple(c / d * r * 1.25 * d ** 0.4 for c in v)
        if all(math.dist(q, o) > r * 0.9 for o in pts):
            pts.append(q)
    for i, q in enumerate([(0, 0, 0)] + pts):
        sphere(r, (loc[0] + q[0], loc[1] + q[1], loc[2] + q[2]), 1, p if i % 2 else n, seg=32)


cafe_plates()
stadium_plates()
prop_scene(); sugar_cube((0, 0, 0), 0.5, 25); sprite_camera((0, 0, 0.25), 3.0, 1.6, 50, azimuth=-10)
still("sugar_cube", 700, 700, 40, transparent=True, crop=True)
prop_scene(); marble((0, 0, 0.5), 0.5); sprite_camera((0, 0, 0.5), 3.4, 1.0, 50, azimuth=0)
still("marble", 700, 700, 48, transparent=True, crop=True)
prop_scene(); sphere(0.4, (0, 0, 0.5), 1, mat("electron", "#1fa8ff", rough=0.2, coat=0.6, emit="#1fa8ff", emit_strength=0.6), seg=40)
sprite_camera((0, 0, 0.5), 3.0, 0.4, 50, azimuth=0)
still("electron", 500, 500, 24, transparent=True, crop=True)
prop_scene(); nucleus((0, 0, 0.5), 0.14); sprite_camera((0, 0, 0.5), 2.2, 0.6, 50, azimuth=-15)
still("nucleus", 600, 600, 32, transparent=True, crop=True)
