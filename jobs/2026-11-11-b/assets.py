# 2026-11-11-b: "Can you see the Great Wall from space?" (myth-bust). Sets: a sunny Great-Wall viewpoint (stone terrace
# in front, olive-and-tan hills with a stone wall snaking along the ridge, watchtowers, pines, far blue mountains), 3 angles;
# a cosy space-station module (white panels, handrails, a big round window looking down on a fictional blue-green Earth),
# 1 angle + a day view and a night view of Earth from the window. Cut-outs: a single spaghetti strand, a pair of binoculars.
import math, os, random

# tree(), bush(), seg() + sunny() from earlier town jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read().split("\npark_angles()\n")[0]
exec(compile(_src, "c_helpers", "exec"), globals())


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


# ---------------------------------------------------------------- the Great Wall viewpoint
def H(x, y):
    """Terrain height: flat terrace near the camera, a ridge around y=7, far mountains."""
    if y < 2.0:
        base = 0.0
    else:
        t = min(1.0, (y - 2.0) / 2.0)
        base = t * t * (3 - 2 * t)
    ridge = 1.7 * math.exp(-((y - 7.5) / 2.6) ** 2) * (0.75 + 0.3 * math.sin(x * 0.45 + 0.6))
    far = 5.5 * math.exp(-((y - 22) / 5.0) ** 2) * (0.65 + 0.35 * math.sin(x * 0.22 + 1.3))
    return base * (ridge + far + 0.25 * math.sin(x * 0.9 + y * 0.6) * min(1, (y - 2) / 4 if y > 2 else 0))


def terrain(x0, x1, y0, y1, n, m, material, name="terrain"):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = []
    for j in range(m + 1):
        row = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            y = y0 + (y1 - y0) * j / m
            row.append(bm.verts.new((x, y, H(x, y))))
        vs.append(row)
    for j in range(m):
        for i in range(n):
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(material)
    return o


def hill_mat():
    """Olive grass blended with tan earth (noise) - close to the wall's own colour on purpose."""
    m = bpy.data.materials.new("hills"); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.9
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 0.12; n.inputs["Detail"].default_value = 6
    r = nt.nodes.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].position = 0.38; r.color_ramp.elements[0].color = (*hexrgb("#99985e"), 1)
    r.color_ramp.elements[1].position = 0.62; r.color_ramp.elements[1].color = (*hexrgb("#b9a57a"), 1)
    nt.links.new(n.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], pr.inputs["Base Color"])
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.3
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 18
    nt.links.new(n2.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], pr.inputs["Normal"])
    return m


def wall_path(x):
    return 7.2 + 0.9 * math.sin(0.42 * x + 0.3)


def great_wall():
    stone = mat("wall_stone", "#ad9d7a", rough=0.85, noise_bump=0.45)
    top = mat("wall_top", "#b8a684", rough=0.9, noise_bump=0.3)
    import bmesh
    step = 0.16
    xs = [-16 + k * step for k in range(int(32 / step) + 1)]
    me = bpy.data.meshes.new("wall"); bm = bmesh.new(); rows = []
    for x in xs:
        y = wall_path(x); dy = (wall_path(x + 0.01) - wall_path(x - 0.01)) / 0.02
        L = math.hypot(1, dy); nx, ny = -dy / L * 0.31, 1 / L * 0.31        # half-width along the normal
        zb = H(x, y) - 0.4; zt = H(x, y) + 0.72
        rows.append([bm.verts.new((x + nx, y + ny, zb)), bm.verts.new((x - nx, y - ny, zb)),
                     bm.verts.new((x - nx, y - ny, zt)), bm.verts.new((x + nx, y + ny, zt))])
    for a, b in zip(rows, rows[1:]):
        for i in range(4):
            j = (i + 1) % 4
            f = bm.faces.new((a[i], b[i], b[j], a[j]))
            if i == 2:
                f.material_index = 1
    bm.faces.new(list(reversed(rows[0]))); bm.faces.new(rows[-1])
    bm.normal_update(); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("wall", me); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(stone); o.data.materials.append(top)
    bv = o.modifiers.new("bev", "BEVEL"); bv.width = 0.03; bv.segments = 2; bv.limit_method = "ANGLE"
    for k, x in enumerate(xs[:-1]):
        if k % 2 == 0:                                       # crenels on the outer (camera) side
            y = wall_path(x + step / 2); dy = (wall_path(x + 0.01) - wall_path(x - 0.01)) / 0.02
            ang = math.degrees(math.atan2(dy, 1)); L = math.hypot(1, dy)
            box((step * 1.1, 0.1, 0.2), (x + step / 2 + dy / L * 0.26, y - 0.26 / L, H(x, y) + 0.82), (0, 0, ang), stone, bevel=0.01)
    for tx in (-6.5, 2.2, 10.5):                           # watchtowers
        ty = wall_path(tx); tz = H(tx, ty)
        box((1.25, 1.25, 1.9), (tx, ty, tz + 0.55), (0, 0, 0), stone, bevel=0.04)
        for k in range(4):
            box((0.24, 0.14, 0.22), (tx - 0.45 + k * 0.3, ty - 0.62, tz + 1.6), (0, 0, 0), stone, bevel=0.01)
        box((0.26, 0.05, 0.45), (tx, ty - 0.64, tz + 0.95), (0, 0, 0), mat("door_dark", "#3a3428", rough=0.9), bevel=0.01)


def pine(x, y, h=2.2, col="#3f7a43"):
    z = H(x, y)
    cylinder(0.07, h * 0.3, (x, y, z + h * 0.15), material=wood("#7a5a3a", "#5e3f2a", "pine_bark", 2.0, 0.8), verts=12)
    m = bpy.data.materials.get("pine" + col) or mat("pine" + col, col, rough=0.8, noise_bump=0.2)
    for k in range(3):
        cone(h * (0.32 - k * 0.07), h * 0.45, (x, y, z + h * (0.42 + k * 0.2)), material=m)


def build_wall():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny(sky_top="#4aa3e6", sky_horizon="#d6eef9", sun=4.0)
    terrain(-40, 40, -12, 45, 160, 120, hill_mat())
    # far haze mountains (bluer with distance)
    for k in range(7):
        mx = -36 + k * 12
        sphere(9, (mx, 52 + (k % 2) * 6, -1.5), (1.6, 0.6, 0.55 + 0.1 * (k % 3)), mat(f"far{k}", "#9cbfd6", rough=1.0), seg=32)
    great_wall()
    # the terrace: flagstones, a stone parapet low at the left, a sign, pines and bushes
    flag = checker_mat("flags", "#d8c7a2", "#cdb994", 2.2)
    plane(18, 12, (0.5, -4.0, 0.006), material=flag, name="terrace")
    box((5.0, 0.35, 0.55), (-4.6, 1.6, 0.27), (0, 0, 8), mat("parapet", "#c2b08a", rough=0.85, noise_bump=0.4), bevel=0.05)
    post = wood("#8a6142", "#5e3f2a", "post", 3.0)
    cylinder(0.05, 1.3, (3.6, 1.2, 0.65), material=post, verts=12)
    box((1.15, 0.06, 0.5), (3.6, 1.18, 1.35), (0, 0, -6), mat("signboard", "#7c2533", rough=0.6), bevel=0.02)
    text3d("VIEWPOINT", 0.15, (3.6, 1.13, 1.3), (90, 0, -6), mat("sign_ink", "#f6efe2", rough=0.5), font="body", extrude=0.01)
    random.seed(11)
    for (px, py, ph) in ((-6.0, 4.0, 2.6), (6.2, 3.5, 2.4), (-9.0, 6.0, 2.8), (8.5, 9.5, 2.5), (-2.5, 10.5, 2.2),
                         (4.8, 11.0, 2.0), (-12, 9, 3.0), (12.5, 6.5, 2.7), (0.8, 4.2, 1.6)):
        pine(px, py, ph, random.choice(["#3f7a43", "#4a8a48", "#36703d"]))
    bush(-2.6, 2.4, 0.45, "#5a8f45", "#f2b04a", 7); bush(5.2, 2.0, 0.5, "#4f8a3e", "#d9534f", 8)
    area_light((-6, -6, 6), (0, 3, 1), 900, 6, "#fff0dc", "key")
    drop_cams()


def wall_angles():
    build_wall()
    for name, loc, tgt, lens, fs in (("wall_wide", (0.2, -9.0, 2.3), (0.4, 6.0, 1.6), 22, 8.0),
                                     ("wall_mid", (1.4, -4.6, 1.55), (0.6, 3.0, 1.3), 30, 5.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
    # close-up on the wall itself, hugging the hillside: same colours as the ground around it
    wx = -3.2; wy = wall_path(wx); wz = H(wx, wy)
    drop_cams(); camera((wx + 1.2, wy - 3.2, wz + 1.5), (wx, wy, wz + 0.5), lens=32, fstop=3.5)
    still("plate_wall_close", 1080, 1920, 40)


# ---------------------------------------------------------------- the space station + Earth
def earth_mat(night=False):
    m = bpy.data.materials.new("earth_night" if night else "earth"); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.55
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 0.022; n.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    land = nt.nodes.new("ShaderNodeValToRGB")          # ocean / land mask
    land.color_ramp.elements[0].position = 0.47; land.color_ramp.elements[0].color = (0, 0, 0, 1)
    land.color_ramp.elements[1].position = 0.5; land.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(n.outputs["Fac"], land.inputs["Fac"])
    if not night:
        col = nt.nodes.new("ShaderNodeMix"); col.data_type = "RGBA"
        col.inputs[6].default_value = (*hexrgb("#1f5f9e"), 1)       # ocean
        n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 0.12
        nt.links.new(tc.outputs["Object"], n2.inputs["Vector"])
        lr = nt.nodes.new("ShaderNodeValToRGB")
        lr.color_ramp.elements[0].color = (*hexrgb("#5f8f45"), 1); lr.color_ramp.elements[1].color = (*hexrgb("#c8ab78"), 1)
        nt.links.new(n2.outputs["Fac"], lr.inputs["Fac"])
        nt.links.new(lr.outputs["Color"], col.inputs[7])
        nt.links.new(land.outputs["Color"], col.inputs[0])
        # clouds
        cn = nt.nodes.new("ShaderNodeTexNoise"); cn.inputs["Scale"].default_value = 0.09; cn.inputs["Detail"].default_value = 6
        nt.links.new(tc.outputs["Object"], cn.inputs["Vector"])
        cr = nt.nodes.new("ShaderNodeValToRGB")
        cr.color_ramp.elements[0].position = 0.6; cr.color_ramp.elements[0].color = (0, 0, 0, 1)
        cr.color_ramp.elements[1].position = 0.72; cr.color_ramp.elements[1].color = (1, 1, 1, 1)
        nt.links.new(cn.outputs["Fac"], cr.inputs["Fac"])
        cm = nt.nodes.new("ShaderNodeMix"); cm.data_type = "RGBA"
        nt.links.new(cr.outputs["Color"], cm.inputs[0]); nt.links.new(col.outputs[2], cm.inputs[6])
        cm.inputs[7].default_value = (0.95, 0.96, 1.0, 1)
        nt.links.new(cm.outputs[2], pr.inputs["Base Color"])
    else:
        col = nt.nodes.new("ShaderNodeMix"); col.data_type = "RGBA"
        col.inputs[6].default_value = (*hexrgb("#06111f"), 1); col.inputs[7].default_value = (*hexrgb("#141a1c"), 1)
        nt.links.new(land.outputs["Color"], col.inputs[0])
        nt.links.new(col.outputs[2], pr.inputs["Base Color"])
        # city lights: fine noise thresholded, only on land
        def thr(scale, a, b, detail=3):
            ln = nt.nodes.new("ShaderNodeTexNoise"); ln.inputs["Scale"].default_value = scale; ln.inputs["Detail"].default_value = detail
            nt.links.new(tc.outputs["Object"], ln.inputs["Vector"])
            lr = nt.nodes.new("ShaderNodeValToRGB")
            lr.color_ramp.elements[0].position = a; lr.color_ramp.elements[0].color = (0, 0, 0, 1)
            lr.color_ramp.elements[1].position = b; lr.color_ramp.elements[1].color = (1, 1, 1, 1)
            nt.links.new(ln.outputs["Fac"], lr.inputs["Fac"])
            return lr
        fine, clus = thr(3.0, 0.6, 0.68, 2), thr(0.15, 0.5, 0.62, 4)
        m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
        nt.links.new(fine.outputs["Color"], m1.inputs[0]); nt.links.new(clus.outputs["Color"], m1.inputs[1])
        m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
        nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(land.outputs["Color"], m2.inputs[1])
        mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"; mm.inputs[1].default_value = 8.0
        nt.links.new(m2.outputs[0], mm.inputs[0])
        pr.inputs["Emission Color"].default_value = (*hexrgb("#ffb35a"), 1)
        nt.links.new(mm.outputs[0], pr.inputs["Emission Strength"])
    return m


def atmosphere():
    m = bpy.data.materials.new("atmo"); m.use_nodes = True; nt = m.node_tree
    for nd in list(nt.nodes):
        if nd.type != "OUTPUT_MATERIAL":
            nt.nodes.remove(nd)
    out = [nd for nd in nt.nodes if nd.type == "OUTPUT_MATERIAL"][0]
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (*hexrgb("#7fc8ff"), 1); em.inputs["Strength"].default_value = 3.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 3.0
    nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    nt.links.new(pw.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m


def stars(n=260, R=300, seed=3):
    random.seed(seed)
    sm = mat("star", "#ffffff", emit="#ffffff", emit_strength=8.0)
    for k in range(n):
        a = random.uniform(0, 2 * math.pi); e = random.uniform(-0.2, 1.2)
        sphere(random.uniform(0.25, 0.6), (R * math.cos(a) * math.cos(e), R * math.sin(a) * math.cos(e) + 80, R * math.sin(e)), 1, sm, seg=6)


EARTH_C = (0, 95, -78)
EARTH_R = 80


def build_station():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15)
    world_color(hexrgb("#020408"), 1.0)
    stars()
    sphere(EARTH_R, EARTH_C, 1, earth_mat(), seg=128, name="earth")
    sphere(EARTH_R * 1.025, EARTH_C, 1, atmosphere(), seg=128, name="atmo")
    d = bpy.data.lights.new("sun", "SUN"); d.energy = 3.5; d.color = hexrgb("#fff3e0")
    o = bpy.data.objects.new("sun", d); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(35), math.radians(-30), math.radians(-20))
    # the module: floor, side walls, ceiling, back wall with a big round window (boolean)
    panel = mat("panel", "#eef1f4", rough=0.4, coat=0.3)
    panel2 = mat("panel2", "#d9dee4", rough=0.45, coat=0.2)
    box((5.2, 8, 0.1), (0, -1.0, -0.05), material=checker_mat("floor_pan", "#e3e7ec", "#d3d9df", 3.0), bevel=0.01)
    for sx in (-1, 1):
        box((0.1, 8, 4.0), (sx * 2.6, -1.0, 2.0), material=panel, bevel=0.02)
        for k in range(5):
            box((0.05, 1.3, 1.2), (sx * 2.53, -4 + k * 1.5, 2.2), material=panel2, bevel=0.03)
        rail = metal("#c9a24a", 0.3, "rail")
        cylinder(0.035, 7.5, (sx * 2.42, -1.0, 1.15), (90, 0, 0), rail, verts=12)
    box((5.2, 8, 0.1), (0, -1.0, 4.0), material=panel, bevel=0.02)
    for k in range(4):
        box((0.9, 0.5, 0.04), (0, -3.5 + k * 1.6, 3.94), material=mat("ceil_light", "#fff6e8", emit="#fff1d6", emit_strength=3.0), bevel=0.01)
    back = box((5.2, 0.25, 4.0), (0, 3.0, 2.0), material=panel, bevel=0.02, name="backwall")
    cut = cylinder(1.55, 1.0, (0, 3.0, 2.1), (90, 0, 0), panel, verts=96, bevel=0, name="cutter")
    mod = back.modifiers.new("hole", "BOOLEAN"); mod.operation = "DIFFERENCE"; mod.object = cut
    bpy.context.view_layer.objects.active = back
    bpy.ops.object.modifier_apply(modifier="hole")
    bpy.data.objects.remove(cut)
    torus(1.6, 0.12, (0, 2.86, 2.1), (90, 0, 0), metal("#9aa3ad", 0.3, "frame"))
    for k in range(8):
        a = k / 8 * 2 * math.pi
        cylinder(0.05, 0.08, (1.6 * math.cos(a), 2.74, 2.1 + 1.6 * math.sin(a)), (90, 0, 0), metal("#c9a24a", 0.3, "bolt"), verts=12)
    # details: a laptop strapped to the wall, a plant box, cables, a mission patch (fictional)
    box((0.7, 0.05, 0.45), (-2.5, -0.6, 1.8), (0, 0, 90), mat("laptop", "#25262b", rough=0.3), bevel=0.02)
    box((0.62, 0.02, 0.38), (-2.47, -0.6, 1.8), (0, 0, 90), mat("lap_screen", "#16232b", emit="#2a6f6a", emit_strength=1.2), bevel=0.005)
    box((0.9, 0.5, 0.35), (2.2, 0.8, 0.6), material=mat("plant_box", "#6fc3c0", rough=0.4, coat=0.3), bevel=0.04)
    leaf = mat("leaf", "#4f9e4a", rough=0.6)
    random.seed(9)
    for k in range(7):
        sphere(0.15, (2.0 + random.uniform(-0.3, 0.3) + 0.05 * k, 0.8 + random.uniform(-0.15, 0.15), 0.9 + random.uniform(0, 0.2)), 1, leaf, seg=16)
    cab = mat("cable", "#d9534f", rough=0.5)
    for k in range(3):
        seg((-2.5, 1.0 + k * 0.4, 3.5), (-2.5, 1.2 + k * 0.4, 0.4), 0.025, cab)
    cylinder(0.3, 0.03, (2.52, -2.0, 2.6), (0, 90, 0), mat("patch", "#f2b04a", rough=0.6), verts=40)
    area_light((-1.5, -3.5, 3.6), (0, 1, 1.2), 380, 3.0, "#fff0dc", "key")
    area_light((1.8, -1.0, 3.0), (0, 1, 1.0), 120, 2.0, "#dbe8ff", "fill")
    drop_cams()


def station_angles():
    build_station()
    drop_cams(); camera((0.4, -3.8, 1.55), (0.0, 3.0, 1.85), lens=22, fstop=5.0)
    still("plate_station_mid", 1080, 1920, 48)
    # straight out of the window: Earth fills the lower frame, curved limb, black sky
    drop_cams(); camera((0, 2.9, 2.1), (0, 40, -12), lens=30, fstop=0)
    for o in bpy.data.objects:
        if o.name in ("backwall",) or o.name.startswith("Torus"):
            o.hide_render = True
    still("plate_earth_day", 1080, 1920, 48)
    bpy.data.objects["earth"].data.materials.clear(); bpy.data.objects["earth"].data.materials.append(earth_mat(night=True))
    bpy.data.objects["sun"].data.energy = 0.0
    still("plate_earth_night", 1080, 1920, 48)


# ---------------------------------------------------------------- props
def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def spaghetti():
    m = mat("pasta", "#f2c75a", rough=0.35, coat=0.3, sss=0.15)
    cv = bpy.data.curves.new("strand", "CURVE"); cv.dimensions = "3D"; cv.bevel_depth = 0.022; cv.bevel_resolution = 4
    sp = cv.splines.new("BEZIER"); n = 7
    sp.bezier_points.add(n - 1)
    for i, bp in enumerate(sp.bezier_points):
        x = -0.9 + 1.8 * i / (n - 1)
        bp.co = (x, 0, 0.06 * math.sin(i * 1.4))
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new("strand", cv); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def binoculars():
    b = mat("bino", "#25262b", rough=0.35, coat=0.4); g = metal("#c9a24a", 0.3, "bino_brass")
    lens_m = mat("bino_lens", "#6fc3c0", rough=0.05, coat=0.9)
    for sx in (-0.16, 0.16):
        cylinder(0.11, 0.42, (sx, 0, 0.12), (90, 0, 0), b, verts=40, bevel=0.02)
        cylinder(0.13, 0.08, (sx, -0.2, 0.12), (90, 0, 0), g, verts=40, bevel=0.01)
        cylinder(0.1, 0.01, (sx, -0.245, 0.12), (90, 0, 0), lens_m, verts=40, bevel=0)
    box((0.22, 0.12, 0.08), (0, 0.02, 0.15), material=g, bevel=0.02)


if not os.environ.get("BK_PROPS_ONLY"):
    wall_angles()
    station_angles()
prop_scene(); spaghetti(); camera((0, -2.6, 0.9), (0, 0, 0.0), lens=50, fstop=0)
still("spaghetti", 900, 400, 24, transparent=True, crop=True)
prop_scene(); binoculars(); camera((0.9, -1.6, 0.9), (0, 0, 0.1), lens=50, fstop=0)
still("binoculars", 600, 600, 24, transparent=True, crop=True)
