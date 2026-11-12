# 2026-11-12-a: "Do bulls hate red?" (myth-bust). Set: a sunny ranch arena (round sandy ring, wooden post-and-rail fence,
# hay bales, bunting, a little red barn, round trees, green hills behind), 3 angles (wide / mid / low close).
# Cut-outs: a cartoon-rounded bull (side, charging), the same bull standing calm, flags on poles (red, blue, white).
import math, os, random

# tree(), bush(), seg(), checker_mat() + sunny() from earlier town jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


RING_C = (0.0, 5.0)
RING_R = 6.5


def sand_mat():
    m = bpy.data.materials.new("sand"); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.95
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 1.6; n.inputs["Detail"].default_value = 6
    r = nt.nodes.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].position = 0.4; r.color_ramp.elements[0].color = (*hexrgb("#e3c58f"), 1)
    r.color_ramp.elements[1].position = 0.65; r.color_ramp.elements[1].color = (*hexrgb("#d4ad72"), 1)
    nt.links.new(n.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], pr.inputs["Base Color"])
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.25
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 30
    nt.links.new(n2.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], pr.inputs["Normal"])
    return m


def fence():
    post = wood("#9a6a43", "#6e4729", "fence_post", 3.0)
    rail = wood("#b07a4c", "#7d5432", "fence_rail", 4.0)
    cx, cy = RING_C
    n = 36
    pts = []
    for k in range(n):
        a = k / n * 2 * math.pi
        x, y = cx + RING_R * math.cos(a), cy + RING_R * math.sin(a)
        pts.append((x, y))
        if y < -0.6 and abs(x) < 1.6:      # gap in the front of the ring for the camera
            continue
        cylinder(0.09, 1.5, (x, y, 0.75), material=post, verts=14)
        sphere(0.1, (x, y, 1.5), 1, post, seg=12)
    for k in range(n):
        (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % n]
        if (y0 < -0.6 and abs(x0) < 1.6) or (y1 < -0.6 and abs(x1) < 1.6):
            continue
        for z in (0.55, 1.05, 1.42):
            seg((x0, y0, z), (x1, y1, z), 0.045, rail)


def hay(x, y, rot=0):
    straw = mat(f"hay{x}{y}", "#e8c25a", rough=0.9, noise_bump=0.6)
    c = cylinder(0.55, 0.9, (x, y, 0.55), (90, 0, rot), straw, verts=40, bevel=0.08)
    band = mat("hay_band", "#b5533c", rough=0.6)
    for d in (-0.22, 0.22):
        torus(0.555, 0.025, (x + d * math.sin(math.radians(rot)) * 0, y + d, 0.55), (90, 0, rot), band)
    return c


def bunting(p0, p1, n=11, sag=0.5):
    cols = ["#d9534f", "#f2b04a", "#2f6fd6", "#6fc3c0", "#f6efe2"]
    rope = mat("rope", "#5e3f2a", rough=0.7)
    prev = None
    for k in range(n + 1):
        t = k / n
        x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
        z = p0[2] + (p1[2] - p0[2]) * t - sag * 4 * t * (1 - t)
        if prev:
            seg(prev, (x, y, z), 0.015, rope)
        if 0 < k < n + 1 and k < n:
            m = bpy.data.materials.get("flag" + cols[k % 5]) or mat("flag" + cols[k % 5], cols[k % 5], rough=0.6)
            ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
            o = cone(0.17, 0.3, (x + (p1[0] - p0[0]) / n / 2, y + (p1[1] - p0[1]) / n / 2, z - 0.2), (180, 0, ang), m)
            o.scale = (1, 0.2, 1)
        prev = (x, y, z)


def barn(x, y):
    red = mat("barn_red", "#b5433c", rough=0.7, noise_bump=0.2)
    white = mat("barn_trim", "#f6efe2", rough=0.6)
    box((3.4, 2.6, 2.4), (x, y, 1.2), material=red, bevel=0.05)
    roof = mat("barn_roof", "#5a5f6b", rough=0.6)
    for s in (-1, 1):
        box((3.7, 1.6, 0.12), (x, y + s * 0.68, 2.85), (s * -38, 0, 0), roof, bevel=0.03)
    box((1.3, 0.06, 1.6), (x, y - 1.31, 0.8), material=mat("barn_door", "#8f3530", rough=0.7), bevel=0.02)
    seg((x - 0.65, y - 1.35, 1.55), (x + 0.65, y - 1.35, 0.05), 0.04, white)
    seg((x - 0.65, y - 1.35, 0.05), (x + 0.65, y - 1.35, 1.55), 0.04, white)


def build_arena():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sky_top="#2f86d6", sky_horizon="#a8d8f2", sun=4.2)
    grass = mat("grass", "#7fb552", rough=0.9, noise_bump=0.3)
    plane(140, 140, (0, 30, -0.01), material=grass, name="grass")
    sand = cylinder(RING_R + 0.3, 0.04, (RING_C[0], RING_C[1], 0.0), material=sand_mat(), verts=96, bevel=0.01, name="sand")
    plane(4.2, 6, (0, -2.5, 0.005), material=sand_mat(), name="sand_path")
    fence()
    # dressing: hay bales, bunting, barn, trees, bushes, a water trough, hills far away (bluer with distance)
    hay(-5.2, 0.6, 20); hay(-4.4, -0.6, -10); hay(5.6, 1.2, 70)
    hay(3.2, 10.0, 15); hay(1.9, 10.6, -25); hay(-3.8, 9.6, 40)
    bunting((-3.5, -0.4, 2.6), (3.5, -0.4, 2.6), 13, 0.45)
    for x in (-3.5, 3.5):
        cylinder(0.06, 2.7, (x, -0.4, 1.35), material=wood("#9a6a43", "#6e4729", "pole", 3.0), verts=12)
    barn(-6.5, 15.0)
    trough = metal("#8f9aa6", 0.35, "trough")
    box((1.4, 0.5, 0.45), (5.8, -1.4, 0.23), material=trough, bevel=0.06)
    box((1.3, 0.42, 0.04), (5.8, -1.4, 0.43), material=mat("water", "#5aa9d6", rough=0.05, coat=0.8), bevel=0.01)
    for (tx, ty, s) in ((-10, 9, 3), (9.5, 10, 5), (4, 17, 7), (-2, 20, 9), (13, 16, 11), (-13, 14, 13)):
        tree(tx, ty, 3.8, 1.4, s, random.choice(["#4f9a45", "#5aa84b", "#468c3e"]))
    bush(-6.8, -2.2, 0.5, "#4f8a3e", "#d9534f", 4); bush(7.4, 3.0, 0.55, "#5a8f45", "#f2b04a", 5)
    for k in range(7):
        sphere(14, (-48 + k * 16, 62 + (k % 2) * 8, -6), (1.4, 0.7, 0.6 + 0.1 * (k % 3)),
               mat(f"hill{k}", ["#7fae7a", "#8cb9a0", "#9cc2c4"][k % 3], rough=1.0), seg=32)
    area_light((-6, -6, 6), (0, 4, 1), 900, 6, "#fff0dc", "key")
    drop_cams()


def arena_angles():
    build_arena()
    for name, loc, tgt, lens, fs in (("arena_wide", (0.0, -7.5, 3.4), (0.0, 6.0, 0.8), 22, 8.0),
                                     ("arena_mid", (1.0, -3.2, 1.55), (0.3, 4.0, 1.0), 28, 5.0),
                                     ("arena_low", (-0.8, 2.2, 0.6), (1.5, 10.0, 1.4), 22, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)


# ---------------------------------------------------------------- props
def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.6), 420, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.6), 260, 2, "#cfe6ff", "rim")


def bull(charge=True):
    """A rounded cartoon bull facing +x. charge=True: head low, front legs reaching, back legs pushing."""
    hide = mat("bull_hide", "#3d2a22", rough=0.55, sss=0.05, noise_bump=0.15)
    hide2 = mat("bull_belly", "#5a3d2e", rough=0.6)
    muzzle = mat("bull_muzzle", "#c9a08a", rough=0.5)
    horn = mat("bull_horn", "#efe3c8", rough=0.35, coat=0.3)
    hoof = mat("bull_hoof", "#1a1410", rough=0.4)
    eye = mat("bull_eye", "#0b0f12", rough=0.1, coat=0.9)
    gold = metal("#d9a441", 0.25, "ring_gold")
    sphere(0.5, (0, 0, 1.0), (1.3, 0.64, 0.6), hide)                      # body
    sphere(0.42, (0.42, 0, 1.18), (0.85, 0.66, 0.72), hide)               # shoulder hump
    sphere(0.4, (-0.2, 0, 0.9), (1.1, 0.6, 0.55), hide2)                  # belly
    hz = 0.8 if charge else 1.18
    hx = 1.02 if charge else 0.98
    sphere(0.3, (0.74, 0, (hz + 1.1) / 2), (0.95, 0.72, 0.85), hide)       # neck
    sphere(0.26, (hx, 0, hz), (1.05, 0.85, 0.85), hide)                    # head
    sphere(0.17, (hx + 0.22, 0, hz - 0.1), (1.0, 0.9, 0.8), muzzle)        # muzzle
    for s in (-1, 1):
        sphere(0.025, (hx + 0.36, s * 0.07, hz - 0.08), 1, hoof, seg=12)  # nostrils
        sphere(0.04, (hx + 0.1, s * 0.19, hz + 0.08), 1, eye, seg=16)
        seg((hx - 0.04, s * 0.18, hz + 0.16), (hx + 0.02, s * 0.44, hz + 0.2), 0.055, horn)
        seg((hx + 0.02, s * 0.44, hz + 0.2), (hx + 0.2, s * 0.5, hz + 0.36), 0.04, horn)
        sphere(0.022, (hx + 0.2, s * 0.5, hz + 0.36), 1, horn, seg=12)
        o = sphere(0.09, (hx - 0.1, s * 0.27, hz + 0.08), (0.5, 1.4, 0.6), hide2)
    torus(0.06, 0.012, (hx + 0.38, 0, hz - 0.17), (0, 90, 0), gold)
    # legs: (hip, knee, hoof) for front/back, left/right
    if charge:
        legs = [((0.5, 0.85), (0.8, 0.5), (1.0, 0.16)), ((0.42, 0.85), (0.55, 0.45), (0.5, 0.06)),
                ((-0.45, 0.85), (-0.68, 0.45), (-0.95, 0.14)), ((-0.38, 0.85), (-0.42, 0.45), (-0.55, 0.05))]
    else:
        legs = [((0.5, 0.85), (0.52, 0.45), (0.52, 0.06)), ((0.34, 0.85), (0.35, 0.45), (0.35, 0.06)),
                ((-0.46, 0.85), (-0.5, 0.45), (-0.48, 0.06)), ((-0.3, 0.85), (-0.32, 0.45), (-0.31, 0.06))]
    for i, ((x0, z0), (x1, z1), (x2, z2)) in enumerate(legs):
        y = 0.17 if i % 2 == 0 else -0.17
        seg((x0, y, z0), (x1, y, z1), 0.12, hide)
        seg((x1, y, z1), (x2, y, z2 + 0.06), 0.085, hide)
        cylinder(0.095, 0.12, (x2, y, z2), material=hoof, verts=16)
    # tail
    t0 = (-0.6, 0, 1.15); t1 = (-0.9, 0, 1.3) if charge else (-0.72, 0, 0.85)
    t2 = (-1.1, 0, 1.48) if charge else (-0.74, 0, 0.55)
    seg(t0, t1, 0.03, hide); seg(t1, t2, 0.025, hide)
    sphere(0.07, t2, (1.0, 1.0, 1.5), hoof, seg=16)


def cloth_flag(color, name):
    """A flag on a pole: a cloth plane bent in waves."""
    import bmesh
    pole = wood("#9a6a43", "#6e4729", "flagpole", 3.0)
    cylinder(0.025, 1.9, (0, 0, 0.95), material=pole, verts=12)
    sphere(0.045, (0, 0, 1.92), 1, metal("#d9a441", 0.25, "pole_top"), seg=16)
    me = bpy.data.meshes.new(name); bm = bmesh.new(); rows = []
    nx, nz = 24, 12
    for j in range(nz + 1):
        row = []
        for i in range(nx + 1):
            u, v = i / nx, j / nz
            x = 0.03 + u * 0.95
            y = 0.09 * math.sin(u * 7.5 + v * 0.8) * u
            z = 1.85 - v * 0.65 - 0.06 * u * math.sin(u * 3.0)
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for j in range(nz):
        for i in range(nx):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.01
    o.data.materials.append(mat(name + "_m", color, rough=0.7, sss=0.05))
    return o


if not os.environ.get("BK_PROPS_ONLY"):
    arena_angles()
prop_scene(); bull(True); camera((1.0, -4.6, 1.6), (0.05, 0, 0.8), lens=50, fstop=0)
still("bull_charge", 900, 700, 32, transparent=True, crop=True)
prop_scene(); bull(False); camera((1.0, -4.6, 1.6), (0.05, 0, 0.8), lens=50, fstop=0)
still("bull_stand", 900, 700, 32, transparent=True, crop=True)
for col, nm in (("#c41e1a", "flag_red"), ("#2f6fd6", "flag_blue"), ("#f6efe2", "flag_white")):
    prop_scene(); cloth_flag(col, nm); camera((0.5, -4.0, 1.2), (0.5, 0, 1.1), lens=50, fstop=0)
    still(nm, 500, 700, 24, transparent=True, crop=True)
