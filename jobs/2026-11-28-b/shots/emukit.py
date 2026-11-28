# Shared builder for 2026-11-28-b ("The Great Emu War"): our own stylised emus (shaggy brown body, long blue-grey neck,
# long running legs on hip pivots), a Western Australian wheat field with red dirt, gum trees and a wire fence, a 1930s
# army truck, and Librarian Ved's library (tall shelves, warm lamps, reading desk, an open ledger, a rubber stamp).
# Exec'd by the shot scripts and assets.py (blendkit helpers already loaded). Built from primitives; original designs.
import math, random
import bpy


def par(child, parent):
    if parent.get("_fresh", True):                               # make sure the parent's world matrix is current
        bpy.context.view_layer.update()
        parent["_fresh"] = False
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()
    return child


_M = {}


def M(name, color, **k):
    m = _M.get(name)
    try:
        if m is not None:
            m.name
            return m
    except ReferenceError:
        pass
    m = mat(name, color, **k)
    _M[name] = m
    return m


def emu(s=1.0, name="emu", seed=1):
    """Returns (root, torso, legs). Faces +X; root at the feet; ~1.7*s m tall. legs = [(pivot, phase)]."""
    rnd = random.Random(seed)
    tone = rnd.choice(["#6b5643", "#5e4b3a", "#76604a"])
    body_m = M("emu_body" + tone, tone, rough=0.9, noise_bump=0.6)
    tuft_m = M("emu_tuft", "#3f3328", rough=0.95, noise_bump=0.5)
    tip_m = M("emu_tip", "#8c7458", rough=0.95)
    neck_m = M("emu_neck", "#7f93a8", rough=0.7)
    head_m = M("emu_head", "#46505c", rough=0.7)
    beak_m = M("emu_beak", "#2c2a28", rough=0.5)
    leg_m = M("emu_leg", "#8e8f8c", rough=0.6, noise_bump=0.3)
    eye_m = M("emu_eye", "#c98a3a", rough=0.15)
    root = empty((0, 0, 0), name)
    torso = empty((0, 0, 0), name + "_torso")
    par(torso, root)
    hz = 1.0 * s
    parts = []
    parts.append(sphere(0.46 * s, (0, 0, hz), (1.0, 0.62, 0.6), body_m, seg=40, name=name + "_b"))
    parts.append(sphere(0.3 * s, (-0.3 * s, 0, hz + 0.02 * s), (1.0, 0.8, 0.75), body_m, seg=32, name=name + "_r"))
    for k in range(16):                                          # shaggy drooping feather tufts
        a = rnd.uniform(-0.9, 0.9)
        x = rnd.uniform(-0.45, 0.3) * s
        t = sphere(1.0, (x, math.sin(a) * 0.26 * s, hz - 0.08 * s + math.cos(a) * 0.12 * s),
                   (0.09 * s, 0.05 * s, 0.2 * s), tuft_m if k % 3 else tip_m, seg=12, name=name + f"_tf{k}")
        t.rotation_euler = (a * 0.6, math.radians(rnd.uniform(-35, -10)), 0)
        parts.append(t)
    # neck: one smooth tapered tube (a bevelled curve) from the chest up to the head, with a fluffy collar
    cd = bpy.data.curves.new(name + "_neckc", "CURVE")
    cd.dimensions = "3D"
    cd.bevel_depth = 1.0
    cd.bevel_resolution = 4
    cd.resolution_u = 12
    sp = cd.splines.new("BEZIER")
    pts = [(0.3, 1.08, 0.1), (0.42, 1.32, 0.075), (0.47, 1.52, 0.06), (0.52, 1.68, 0.052)]
    sp.bezier_points.add(len(pts) - 1)
    for bp, (x, z, r) in zip(sp.bezier_points, pts):
        bp.co = (x * s, 0, z * s)
        bp.handle_left_type = bp.handle_right_type = "AUTO"
        bp.radius = r * s
    nk = bpy.data.objects.new(name + "_neck", cd)
    bpy.context.scene.collection.objects.link(nk)
    cd.materials.append(neck_m)
    parts.append(nk)
    parts.append(sphere(0.16 * s, (0.3 * s, 0, 1.12 * s), (1.0, 0.9, 1.0), body_m, seg=24, name=name + "_collar"))
    hx, hzz = 0.56 * s, 1.72 * s
    parts.append(sphere(0.085 * s, (hx, 0, hzz), (1.25, 0.85, 0.9), head_m, seg=24, name=name + "_h"))
    bk = cone(0.035 * s, 0.13 * s, (hx + 0.13 * s, 0, hzz - 0.015 * s), (0, 95, 0), beak_m, name=name + "_bk")
    bk.scale = (1.0, 1.0, 1.0)
    parts.append(bk)
    for sd in (1, -1):
        parts.append(sphere(0.018 * s, (hx + 0.045 * s, sd * 0.06 * s, hzz + 0.02 * s), 1, eye_m, seg=12, name=name + f"_e{sd}"))
    for p in parts:
        par(p, torso)
    legs = []
    for sd, ph in ((1, 0.0), (-1, 0.5)):
        pv = empty((0.02 * s, sd * 0.13 * s, hz - 0.1 * s), name + f"_hip{sd}")
        par(pv, torso)
        th = sphere(1.0, (0.02 * s, sd * 0.13 * s, hz - 0.22 * s), (0.1 * s, 0.08 * s, 0.17 * s), body_m, seg=16, name=name + f"_th{sd}")
        par(th, pv)
        up = cylinder(0.035 * s, 0.42 * s, (0.07 * s, sd * 0.13 * s, hz - 0.5 * s), (0, -12, 0), leg_m, verts=10, bevel=0, name=name + f"_ul{sd}")
        par(up, pv)
        kn = sphere(0.045 * s, (0.11 * s, sd * 0.13 * s, hz - 0.7 * s), 1, leg_m, seg=12, name=name + f"_kn{sd}")
        par(kn, pv)
        lo = cylinder(0.028 * s, 0.32 * s, (0.06 * s, sd * 0.13 * s, hz - 0.86 * s), (0, 18, 0), leg_m, verts=10, bevel=0, name=name + f"_ll{sd}")
        par(lo, pv)
        for a in (-28, 0, 28):
            toe = cylinder(0.016 * s, 0.14 * s, (0.06 * s + 0.06 * s * math.cos(math.radians(a)), sd * 0.13 * s + 0.06 * s * math.sin(math.radians(a)), 0.015 * s),
                           (0, 90, a), leg_m, verts=8, bevel=0, name=name + f"_t{sd}{a}")
            par(toe, pv)
        legs.append((pv, ph))
    return root, torso, legs


def run_cycle(torso, legs, t0, t1, period=0.42, swing=34, bob=0.06, s=1.0, phase=0.0):
    """Running gait between t0 and t1: legs swing in opposite phase, the body bobs twice per stride."""
    n = max(4, int((t1 - t0) / period * 8))
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        u = (t - t0) / period + phase
        for pv, ph in legs:
            key(pv, t, rot=(0, swing * math.sin(2 * math.pi * (u + ph)), 0), ease="LINEAR")
        key(torso, t, loc=(0, 0, bob * s * abs(math.sin(2 * math.pi * u))), rot=(0, 6 + 3 * math.sin(4 * math.pi * u), 0), ease="LINEAR")


def gum_tree(loc, h=6.0, seed=1, name="gum"):
    rnd = random.Random(seed)
    x, y, z = loc
    bark = M("gum_bark", "#e9e2d4", rough=0.8, noise_bump=0.3)
    cylinder(0.16 * h / 6, h * 0.65, (x, y, z + h * 0.32), (rnd.uniform(-6, 6), rnd.uniform(-6, 6), 0), bark, verts=12, bevel=0, name=name + "_t")
    for k in range(4):
        c = rnd.choice(["#7d8f55", "#6a7d4a", "#8fa066"])
        sphere(h * 0.18 * rnd.uniform(0.8, 1.2), (x + rnd.uniform(-1.2, 1.2), y + rnd.uniform(-0.8, 0.8), z + h * 0.72 + rnd.uniform(-0.3, 0.6)),
               (1.3, 1.1, 0.7), M("gum_leaf" + c, c, rough=0.85), seg=20, name=name + f"_c{k}")


def wheat_field(seed=3, stalk_area=(-8, 8, -2, 6), n_stalks=500, sun_rot=(48, -10, -35), fence_y=14.0):
    """Golden wheat under a big blue sky; red dirt road, gum trees, a wire fence on the horizon line."""
    world_color((0.45, 0.66, 0.95), 0.95)
    plane(400, 400, (0, 0, 0), material=M("wheat_ground", "#cf9f45", rough=0.95, noise_bump=0.8), name="ground")
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 4.4
    sun.color = (1.0, 0.9, 0.76)
    sun.angle = math.radians(3)
    so = bpy.data.objects.new("sun", sun)
    bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = tuple(math.radians(a) for a in sun_rot)
    rnd = random.Random(seed)
    x0, x1, y0, y1 = stalk_area
    hair_wheat(stalk_area, n_stalks)
    for k in range(14):
        gum_tree((rnd.uniform(-40, 40), rnd.uniform(fence_y + 8, fence_y + 40), 0), rnd.uniform(5, 9), seed=k, name=f"gum{k}")
    post_m = M("post", "#6b5038", rough=0.9)
    wire_m = M("wire", "#9a9ea4", rough=0.4, metal=0.8)
    for k in range(-20, 21):
        cylinder(0.05, 1.3, (k * 2.5, fence_y, 0.65), (0, 0, 0), post_m, verts=8, bevel=0, name=f"post{k}")
    for zz in (0.45, 0.8, 1.15):
        cylinder(0.008, 102, (0, fence_y, zz), (0, 90, 0), wire_m, verts=4, bevel=0, name=f"wire{zz}")
    for k in range(6):
        sphere(30, (rnd.uniform(-120, 120), rnd.uniform(160, 200), -22), (2.0, 1.0, 0.8), M("far_hill", "#b98a5a", rough=0.95), seg=24, name=f"hill{k}")
    return so


def hair_wheat(area, count, seed=2):
    """A dense wheat carpet: particle hair on a patch (fast in Cycles), golden strands with paler tips."""
    x0, x1, y0, y1 = area
    bpy.ops.mesh.primitive_plane_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, 0.002))
    pl = bpy.context.object
    pl.scale = (x1 - x0, y1 - y0, 1)
    bpy.ops.object.transform_apply(scale=True)
    pl.name = "wheatpatch"
    pl.data.materials.append(M("wheat_ground", "#cf9f45", rough=0.95, noise_bump=0.8))
    wm = bpy.data.materials.new("wheat_hair")
    wm.use_nodes = True
    nt = wm.node_tree
    bs = nt.nodes.get("Principled BSDF")
    hi = nt.nodes.new("ShaderNodeHairInfo")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.55, 0.36, 0.1, 1)
    ramp.color_ramp.elements[1].color = (0.98, 0.8, 0.42, 1)
    nt.links.new(hi.outputs["Intercept"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bs.inputs["Base Color"])
    bs.inputs["Roughness"].default_value = 0.6
    pl.data.materials.append(wm)
    mod = pl.modifiers.new("wheat", "PARTICLE_SYSTEM")
    ps = mod.particle_system.settings
    ps.type = "HAIR"
    ps.count = int(count)
    ps.hair_length = 0.72
    ps.material = 2
    ps.use_advanced_hair = True
    ps.factor_random = 0.06
    ps.brownian_factor = 0.0
    ps.root_radius = 0.012 if hasattr(ps, "root_radius") else 0
    try:
        ps.radius_scale = 0.012
        ps.root_radius = 1.0
        ps.tip_radius = 0.5
    except Exception:
        pass
    ps.rendered_child_count = 0
    ps.child_type = "NONE"
    mod.particle_system.seed = seed
    return pl


def flock(n, area, seed=5, s=1.0, prefix="em"):
    rnd = random.Random(seed)
    out = []
    x0, x1, y0, y1 = area
    for i in range(n):
        r, t, l = emu(s * rnd.uniform(0.9, 1.08), f"{prefix}{i}", seed=seed * 100 + i)
        r.location = (rnd.uniform(x0, x1), rnd.uniform(y0, y1), 0)
        out.append((r, t, l, rnd.uniform(0, 1)))
    return out


def truck(name="truck"):
    """A 1930s flatbed army truck (our own design). Faces +X. Returns (root, body, wheels)."""
    root = empty((0, 0, 0), name)
    body = empty((0, 0, 0), name + "_body")
    par(body, root)
    green = M("truck_green", "#4c5e3a", rough=0.55, coat=0.2)
    dark = M("truck_dark", "#24261f", rough=0.6)
    chrome = M("truck_chrome", "#c9ccc8", rough=0.2, metal=1.0)
    plank = wood("#8a6a44", "#5e4528", "bed", 3.0, 0.7)
    glass_m = M("truck_glass", "#a9c6d8", rough=0.05, metal=0.2)
    p = []
    p.append(box((1.3, 1.5, 0.9), (1.4, 0, 1.2), material=green, bevel=0.12, name=name + "_hood"))
    p.append(box((1.1, 1.7, 1.4), (0.3, 0, 1.45), material=green, bevel=0.1, name=name + "_cab"))
    p.append(box((0.04, 1.3, 0.5), (0.86, 0, 1.85), material=glass_m, bevel=0.01, name=name + "_ws"))
    p.append(box((0.06, 1.2, 0.7), (2.07, 0, 1.15), material=chrome, bevel=0.03, name=name + "_grill"))
    for sd in (1, -1):
        p.append(sphere(0.12, (2.0, sd * 0.6, 1.55), 1, M("lamp", "#fff3cf", emit="#fff3cf", emit_strength=2.0), seg=16, name=name + f"_lamp{sd}"))
        p.append(sphere(0.55, (1.55, sd * 0.78, 0.6), (1.2, 0.5, 0.7), green, seg=24, name=name + f"_fend{sd}"))
    p.append(box((2.4, 1.9, 0.18), (-1.3, 0, 0.95), material=plank, bevel=0.02, name=name + "_bed"))
    for sd in (1, -1):
        p.append(box((2.4, 0.08, 0.4), (-1.3, sd * 0.92, 1.22), material=plank, bevel=0.02, name=name + f"_side{sd}"))
    # a tripod-mounted gun shape on the bed (simple, not detailed)
    for a in (0, 120, 240):
        p.append(cylinder(0.025, 0.8, (-1.4 + 0.2 * math.cos(math.radians(a)), 0.2 * math.sin(math.radians(a)), 1.35), (0, 18, a), dark, verts=8, bevel=0, name=name + f"_leg{a}"))
    p.append(cylinder(0.07, 1.1, (-1.1, 0, 1.78), (0, 82, 0), dark, verts=16, bevel=0.01, name=name + "_barrel"))
    for b in p:
        par(b, body)
    wheels = []
    for wx in (1.45, -1.6):
        for sd in (1, -1):
            w = cylinder(0.45, 0.28, (wx, sd * 0.85, 0.45), (90, 0, 0), dark, verts=32, bevel=0.04, name=name + f"_w{wx}{sd}")
            hub = cylinder(0.18, 0.3, (wx, sd * 0.86, 0.45), (90, 0, 0), chrome, verts=20, bevel=0.02, name=name + f"_hub{wx}{sd}")
            par(w, root); par(hub, w)
            wheels.append(w)
    return root, body, wheels


# ---------------- library (Librarian Ved's set) ----------------
def shelf_unit(x, y, rot_z=0, seed=1, w=2.2, h=3.4, name="shelf"):
    rnd = random.Random(seed)
    wd = wood("#7a4b2a", "#52301a", "shelfwood", 5.0, 0.55)
    grp = empty((x, y, 0), name)
    parts = [box((w, 0.45, 0.08), (0, 0, h), material=wd, bevel=0.02),
             box((0.08, 0.45, h), (-w / 2, 0, h / 2), material=wd, bevel=0.01),
             box((0.08, 0.45, h), (w / 2, 0, h / 2), material=wd, bevel=0.01),
             box((w, 0.04, h), (0, 0.22, h / 2), material=M("shelfback", "#3b2416", rough=0.8), bevel=0)]
    cols = ["#8f2f2a", "#2f5a7a", "#2f6b4a", "#c08a2e", "#5a3d6e", "#d9cdb2", "#a4552f", "#1f3a52", "#6e7d3a"]
    for r in range(5):
        z0 = 0.1 + r * (h / 5)
        parts.append(box((w - 0.1, 0.42, 0.05), (0, 0, z0), material=wd, bevel=0.01))
        xx = -w / 2 + 0.1
        while xx < w / 2 - 0.15:
            bw = rnd.uniform(0.05, 0.11)
            bh = rnd.uniform(0.38, 0.55)
            c = rnd.choice(cols)
            tilt = rnd.uniform(-12, 0) if rnd.random() < 0.08 else 0
            parts.append(box((bw, 0.3, bh), (xx + bw / 2, -0.03, z0 + 0.025 + bh / 2), (0, tilt, 0),
                             material=M("book" + c, c, rough=0.6), bevel=0.006))
            if rnd.random() < 0.5:
                parts.append(box((bw * 0.9, 0.005, 0.02), (xx + bw / 2, -0.181, z0 + 0.1 + bh * 0.6), material=M("gilt", "#d9a441", rough=0.3, metal=1.0), bevel=0))
            xx += bw + 0.006
    for p_ in parts:
        p_.location = (p_.location.x + x, p_.location.y + y, p_.location.z)
    for p_ in parts:
        par(p_, grp)
    grp.rotation_euler = (0, 0, math.radians(rot_z))
    return grp


def lamp(x, y, z, name="lamp", power=180):
    shade = cylinder(0.22, 0.25, (x, y, z), (0, 0, 0), M("lampshade", "#f2b04a", rough=0.5, emit="#ffcf7a", emit_strength=1.4), verts=24, bevel=0.01, name=name)
    cylinder(0.012, 0.8, (x, y, z + 0.5), (0, 0, 0), M("lampcord", "#2a2420"), verts=6, bevel=0)
    lt = bpy.data.lights.new(name + "_l", "POINT")
    lt.energy = power
    lt.color = (1.0, 0.8, 0.55)
    lt.shadow_soft_size = 0.3
    lo = bpy.data.objects.new(name + "_l", lt)
    bpy.context.scene.collection.objects.link(lo)
    lo.location = (x, y, z - 0.15)
    return shade


def ledger_tex():
    import os
    from PIL import Image as _PI, ImageDraw as _PD, ImageFont as _PF
    p = os.path.join(ROOT, "jobs/2026-11-28-b/assets/tex_ledger.png")
    if os.path.exists(p):
        return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    im = _PI.new("RGB", (1024, 640), (238, 226, 198))
    d = _PD.Draw(im)
    fp = os.path.join(ROOT, "fonts", "Anton-Regular.ttf")
    f1 = _PF.truetype(fp, 70) if os.path.exists(fp) else None
    d.line([(512, 0), (512, 640)], fill=(190, 170, 140), width=6)
    d.text((80, 60), "FILE 1932", fill=(120, 40, 30), font=f1)
    rnd = random.Random(3)
    for k in range(9):
        y = 190 + k * 44
        d.line([(80, y), (80 + rnd.randint(200, 360), y)], fill=(60, 50, 40), width=5)
    # right page: emu tally sketch (our own doodle)
    d.ellipse([640, 150, 860, 290], outline=(60, 50, 40), width=6)
    d.line([(840, 180), (900, 90)], fill=(60, 50, 40), width=6)
    d.ellipse([890, 70, 930, 100], outline=(60, 50, 40), width=5)
    d.line([(720, 285), (700, 400)], fill=(60, 50, 40), width=6)
    d.line([(780, 285), (800, 400)], fill=(60, 50, 40), width=6)
    for k in range(4):
        x = 640 + k * 70
        for j in range(4):
            d.line([(x + j * 12, 450), (x + j * 12, 520)], fill=(170, 40, 30), width=5)
        d.line([(x - 6, 510), (x + 46, 460)], fill=(170, 40, 30), width=5)
    im.save(p)
    return p


def stamp(loc, name="stamp"):
    x, y, z = loc
    cylinder(0.07, 0.04, (x, y, z + 0.02), (0, 0, 0), M("stamp_rubber", "#c8322b", rough=0.6), verts=24, bevel=0.005, name=name + "_r")
    cylinder(0.05, 0.08, (x, y, z + 0.08), (0, 0, 0), M("stamp_metal", "#d9a441", rough=0.3, metal=1.0), verts=24, bevel=0.005)
    sphere(0.06, (x, y, z + 0.17), (1.0, 1.0, 1.2), wood("#8a5a34", "#5e3a1e", "stampwood", 4.0, 0.4), seg=24, name=name + "_k")


def library_set():
    floorw = wood("#9a6a40", "#6e4526", "floorw", 8.0, 0.45)
    plane(40, 40, (0, 0, 0), material=floorw, name="floor")
    world_color((0.12, 0.09, 0.07), 0.3)
    # back wall + two rows of shelves forming an aisle that runs away from camera
    box((20, 0.3, 6), (0, 9, 3), material=M("libwall", "#5a3a28", rough=0.9), bevel=0)
    plane(20, 20, (0, 4, 4.3), (180, 0, 0), material=M("ceiling", "#8a6448", rough=0.9), name="ceiling")
    beam = wood("#6a4024", "#4a2a14", "beamw", 4.0, 0.5)
    for k in range(6):
        box((6, 0.22, 0.25), (0, -1.5 + k * 1.9, 4.15), material=beam, bevel=0.02, name=f"beam{k}")
    # an arched window glow above the back shelf
    plane(1.6, 1.1, (0, 8.84, 4.0), (90, 0, 0), material=glow("#ffe7b8", 2.5, "libwin"))
    for k in range(4):
        shelf_unit(-2.2, 1.6 + k * 1.9, rot_z=90, seed=10 + k, name=f"shL{k}")
        shelf_unit(2.2, 1.6 + k * 1.9, rot_z=-90, seed=20 + k, name=f"shR{k}")
    shelf_unit(0, 8.6, seed=31, w=3.4, name="shBack")
    # rug down the aisle
    plane(1.6, 9, (0, 4.5, 0.004), material=M("rug", "#8f2f2a", rough=0.95, noise_bump=0.3), name="rug")
    plane(1.3, 8.7, (0, 4.5, 0.006), material=M("rug_in", "#a8433a", rough=0.95, noise_bump=0.3), name="rug2")
    for k in range(4):
        lamp(0, 1.8 + k * 2.0, 3.2, name=f"lamp{k}", power=120)
    # reading desk at the front right of the aisle with the ledger, a stack of books and the stamp
    dx = 1.0
    deskw = wood("#6e4024", "#4a2a14", "deskw", 5.0, 0.4)
    box((1.6, 0.8, 0.06), (0.4 + dx, 0.4, 0.82), material=deskw, bevel=0.02, name="desk")
    for sx in (-0.3, 1.1):
        for sy in (0.1, 0.7):
            box((0.07, 0.07, 0.8), (sx + dx, sy, 0.4), material=deskw, bevel=0.01)
    led = plane(0.62, 0.4, (0.3 + dx, 0.35, 0.868), (0, 0, -6), material=paper(ledger_tex()), name="ledger")
    box((0.66, 0.44, 0.015), (0.3 + dx, 0.35, 0.848), (0, 0, -6), material=M("ledgercover", "#3a1f14", rough=0.6), bevel=0.003)
    for k, c in enumerate(["#2f5a7a", "#8f2f2a", "#c08a2e"]):
        box((0.36, 0.26, 0.06), (0.95 + dx, 0.5, 0.88 + k * 0.062), (0, 0, k * 9 - 6), material=M("book" + c, c, rough=0.6), bevel=0.008)
    stamp((0.85 + dx, 0.2, 0.85))
    # green banker's lamp on the desk
    cylinder(0.08, 0.02, (-0.15 + dx, 0.6, 0.86), (0, 0, 0), M("brass", "#d9a441", rough=0.3, metal=1.0), verts=20)
    cylinder(0.012, 0.3, (-0.15 + dx, 0.6, 1.0), (0, 0, 0), M("brass", "#d9a441"), verts=8, bevel=0)
    cylinder(0.09, 0.32, (-0.05 + dx, 0.6, 1.17), (0, 90, 0), M("banker", "#2f6b4a", rough=0.3, emit="#5fa57a", emit_strength=0.3), verts=20, bevel=0.01)
    spot_light((-0.05 + dx, 0.6, 1.12), (0.3 + dx, 0.35, 0.85), 60, 70, 0.4, 0.05, "#ffe2a8", "deskspot")
    area_light((-3, -4, 4), (0, 3, 1), 700, 4, "#ffdcb0", "key")
    area_light((3, -3, 2.5), (0, 3, 1), 200, 4, "#c9d8ff", "fill")
    area_light((0, 8, 5), (0, 3, 0), 300, 3, "#ffcf8a", "back")
    return led
