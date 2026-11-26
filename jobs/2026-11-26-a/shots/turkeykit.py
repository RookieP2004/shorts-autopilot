# Shared builder for 2026-11-26-a: our own stylised turkeys (a bronze wild turkey with a fanned tail and flapping wings, and a
# fat white farm turkey), an autumn field with mown stripes and yard lines, an autumn oak, a barn, and Coach Ved's locker room.
# Exec'd by the shot scripts and assets.py (blendkit helpers are already loaded). Built from primitives; original designs.
import math, random
import bpy


def par(child, parent):
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()
    return child


def flap(pivots, dur, period=0.24, up=55, down=-35, t0=0.0, t1=None, rest=None):
    """Wing beats: pivots = [(empty, side)], side +1 / -1. Between t0 and t1 the wings beat; outside they rest folded."""
    t1 = dur if t1 is None else t1
    steps = max(4, int((t1 - t0) / period * 6))
    for pv, side in pivots:
        if rest is not None and t0 > 0:
            key(pv, 0, rot=(rest * side, 0, 0), ease="LINEAR")
            key(pv, max(0, t0 - 0.02), rot=(rest * side, 0, 0), ease="LINEAR")
        for i in range(steps + 1):
            t = t0 + (t1 - t0) * i / steps
            s = math.sin(2 * math.pi * (t - t0) / period)
            ang = (up + down) / 2 + (up - down) / 2 * s
            key(pv, t, rot=(ang * side, 0, 0), ease="LINEAR")
        if rest is not None and t1 < dur:
            key(pv, t1 + 0.15, rot=(rest * side, 0, 0), ease="LINEAR")
            key(pv, dur, rot=(rest * side, 0, 0), ease="LINEAR")


def turkey(s=1.0, wild=True, name="tk", legs_tucked=False, tail_open=True):
    """Returns (root, [(left_wing_pivot, +1), (right_wing_pivot, -1)]). Faces +X; root at the feet. Height ~1.0*s m."""
    root = empty((0, 0, 0), name)
    if wild:
        body_c, dark, tip, wingc = "#6e4a30", "#3a2618", "#c98a4a", "#8a6440"
        sheen = 0.35
    else:
        body_c, dark, tip, wingc = "#f4f0e6", "#cfc4ae", "#ffffff", "#e2d6bf"
        sheen = 0.0
    feather = mat(name + "_body", body_c, rough=0.45, metal=sheen * 0.4, coat=sheen)
    fdark = mat(name + "_dark", dark, rough=0.5)
    ftip = mat(name + "_tip", tip, rough=0.6)
    skin_head = mat(name + "_head", "#8fb3e0" if wild else "#c9d7ea", rough=0.5)
    red = mat(name + "_red", "#c8322b", rough=0.4, sss=0.2)
    beak = mat(name + "_beak", "#e0c48c", rough=0.4)
    legm = mat(name + "_leg", "#c99a86", rough=0.5)
    eye = mat(name + "_eye", "#0b0b0e", rough=0.1)
    fat = 1.0 if wild else 1.35
    hz = 0.52 * s                                                # body centre height
    parts = []
    body = sphere(0.34 * s, (0, 0, hz), (1.25 * fat, 0.95 * fat, 0.85 * fat), feather, seg=48, name=name + "_bodym")
    breast = sphere(0.26 * s, (0.2 * s, 0, hz - 0.05 * s), (1.0 * fat, 0.95 * fat, 1.0 * fat), feather, seg=40, name=name + "_breast")
    parts += [body, breast]
    if wild:                                                     # the beard (a tuft of hair-like feathers on the chest)
        bd = cone(0.035 * s, 0.22 * s, (0.42 * s, 0, hz + 0.02 * s), (0, 160, 0), fdark, name=name + "_beard")
        parts.append(bd)
        # bronze "scale" bands on the body: thin darker rings
        for k in range(0):
            r = torus(0.27 * s, 0.012 * s, (-0.05 * s - k * 0.09 * s, 0, hz + 0.02 * s), (0, 90, 0), fdark, name=name + f"_band{k}")
            r.scale = (1.0, 0.95, 0.85)
            parts.append(r)
    # neck + head
    nx, nz = 0.34 * s * fat, hz + 0.28 * s
    neck = cylinder(0.06 * s, 0.32 * s, (nx, 0, nz), (0, -25, 0), skin_head, verts=20, bevel=0, name=name + "_neck")
    head = sphere(0.085 * s, (nx + 0.08 * s, 0, nz + 0.17 * s), (1.15, 0.9, 1.0), skin_head, seg=32, name=name + "_headm")
    bk = cone(0.035 * s, 0.09 * s, (nx + 0.19 * s, 0, nz + 0.16 * s), (0, 100, 0), beak, name=name + "_beak")
    snood = cylinder(0.018 * s, 0.13 * s, (nx + 0.17 * s, 0, nz + 0.13 * s), (0, 15, 0), red, verts=12, bevel=0, name=name + "_snood")
    wat = sphere(0.045 * s, (nx + 0.1 * s, 0, nz + 0.06 * s), (0.8, 0.7, 1.4), red, seg=24, name=name + "_wattle")
    parts += [neck, head, bk, snood, wat]
    for side in (1, -1):
        e = sphere(0.016 * s, (nx + 0.13 * s, side * 0.07 * s, nz + 0.2 * s), 1, eye, seg=16, name=name + f"_eye{side}")
        parts.append(e)
    # legs
    for side in (1, -1):
        if legs_tucked:
            lg = cylinder(0.025 * s, 0.32 * s, (-0.2 * s, side * 0.1 * s, hz - 0.22 * s), (0, 75, 0), legm, verts=12, bevel=0, name=name + f"_leg{side}")
            parts.append(lg)
        else:
            lg = cylinder(0.028 * s, 0.34 * s, (0.02 * s, side * 0.11 * s, 0.17 * s), (0, 0, 0), legm, verts=12, bevel=0, name=name + f"_leg{side}")
            parts.append(lg)
            for a in (-35, 0, 35):
                toe = cylinder(0.014 * s, 0.13 * s, (0.02 * s + 0.06 * s * math.cos(math.radians(a)), side * 0.11 * s + 0.06 * s * math.sin(math.radians(a)), 0.012 * s),
                               (0, 90, a), legm, verts=8, bevel=0, name=name + f"_toe{side}{a}")
                parts.append(toe)
    # tail fan
    n = 13 if wild else 9
    tl = (0.48 if wild else 0.3) * s
    for i in range(n):
        a = -80 + 160 * i / (n - 1) if tail_open else -25 + 50 * i / (n - 1)
        ra = math.radians(a)
        bx, bz = -0.36 * s * fat, hz + 0.08 * s
        dx, dy = -math.sin(math.radians(20)) * 0.0, math.sin(ra)
        cx = bx - 0.06 * s
        cy = math.sin(ra) * tl * 0.55
        cz = bz + math.cos(ra) * tl * 0.55 * (1.0 if tail_open else 0.4)
        f = sphere(1.0, (cx, cy, cz), (0.035 * s, 0.11 * s, tl * 0.55), feather if i % 2 else fdark, seg=20, name=name + f"_tf{i}")
        f.rotation_euler = (-ra, math.radians(-18 if tail_open else -60), 0)
        parts.append(f)
        tp = sphere(1.0, (cx - 0.01 * s, math.sin(ra) * tl * 1.02, bz + math.cos(ra) * tl * 1.02 * (1.0 if tail_open else 0.4)),
                    (0.03 * s, 0.1 * s, 0.07 * s), ftip, seg=16, name=name + f"_tt{i}")
        tp.rotation_euler = (-ra, 0, 0)
        parts.append(tp)
    for p in parts:
        par(p, root)
    # wings on pivots (rotate the pivot about X to flap)
    pivots = []
    wl = (0.62 if wild else 0.38) * s
    wm = mat(name + "_wing", wingc, rough=0.5, metal=sheen * 0.3, coat=sheen)
    bar = mat(name + "_bar", "#efe7d6" if wild else "#ffffff", rough=0.6)
    for side in (1, -1):
        pv = empty((0.05 * s, side * 0.22 * s * fat, hz + 0.12 * s), name + f"_wpv{side}")
        par(pv, root)
        cov = sphere(1.0, (0.02 * s, side * (0.22 * s * fat + wl * 0.35), hz + 0.12 * s), (0.36 * s, wl * 0.72, 0.05 * s), wm, seg=24, name=name + f"_wcov{side}")
        par(cov, pv)
        for k in range(6):
            yy = side * (0.22 * s * fat + wl * (0.45 + 0.1 * k))
            pr = sphere(1.0, (-0.12 * s - 0.02 * k * s, yy, hz + 0.11 * s), (0.42 * s, 0.07 * s, 0.03 * s), wm if k % 2 else fdark, seg=16, name=name + f"_pr{side}{k}")
            pr.rotation_euler = (0, 0, math.radians(side * (8 + 6 * k)))
            par(pr, pv)
            if wild:                                             # white bars on the primaries
                for b in range(3):
                    bb = box((0.03 * s, 0.075 * s, 0.035 * s), (-0.02 * s - 0.12 * s * b - 0.02 * k * s, yy, hz + 0.11 * s), (0, 0, side * (8 + 6 * k)), bar, bevel=0, name=name + f"_bb{side}{k}{b}")
                    par(bb, pv)
        pivots.append((pv, side))
    folds = []
    for side in (1, -1):                                         # folded wings for standing poses (hidden by default)
        fo = sphere(1.0, (-0.05 * s, side * 0.27 * s * fat, hz + 0.06 * s), (0.36 * s * fat, 0.07 * s, 0.17 * s * fat), wm, seg=32, name=name + f"_fold{side}")
        fo.rotation_euler = (0, math.radians(-12), 0)
        par(fo, root)
        fo["sc"] = list(fo.scale)
        fo.scale = (0.001, 0.001, 0.001)
        folds.append(fo)
    root["folds"] = [f.name for f in folds]
    return root, pivots


def folded(root, pivots, t=0.0, on=True):
    """Key the wings folded (on=True) or open (on=False) from time t."""
    for f in root["folds"]:
        fo = bpy.data.objects[f]
        key(fo, t, scale=tuple(fo["sc"]) if on else (0.001, 0.001, 0.001), ease="LINEAR")
    for pv, side in pivots:
        key(pv, t, scale=(0.001, 0.001, 0.001) if on else (1, 1, 1), ease="LINEAR")


def tree(loc, h=4.0, colors=("#e0702e", "#c8322b", "#f2b04a"), seed=1, name="tree", r=1.2):
    rnd = random.Random(seed)
    x, y, z = loc
    trunk = cylinder(0.14 * h / 4, h * 0.6, (x, y, z + h * 0.3), (0, 0, 0), mat("bark", "#5b3e2b", rough=0.9), verts=16, bevel=0, name=name + "_tr")
    for k in range(5):
        c = colors[k % len(colors)]
        sphere(r * rnd.uniform(0.7, 1.05), (x + rnd.uniform(-0.6, 0.6) * r, y + rnd.uniform(-0.5, 0.5) * r, z + h * 0.62 + rnd.uniform(0, 0.6) * r),
               (1.1, 1.0, 0.85), mat(f"leaf_{c}", c, rough=0.8, sss=0.15), seg=24, name=name + f"_c{k}")
    return trunk


def field_set(seed=4, sky=(0.42, 0.66, 0.98), sun_rot=(52, -12, -40), stripes=True, side_trees=True):
    world_color(sky, 0.9)
    plane(400, 400, (0, 0, -0.01), material=mat("grass_far", "#6f9a4a", rough=0.95), name="ground")
    if stripes:
        g1 = mat("grass_a", "#5e9a3e", rough=0.9)
        g2 = mat("grass_b", "#77b04f", rough=0.9)
        line = mat("yard_line", "#f6f3ea", rough=0.7)
        for k in range(-22, 23):
            plane(2.0, 40, (k * 2.0, 6, 0.0), material=g1 if k % 2 else g2, name=f"stripe{k}")
            if k % 2 == 0:
                plane(0.08, 40, (k * 2.0 - 1.0, 6, 0.003), material=line, name=f"yl{k}")
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 4.2
    sun.color = (1.0, 0.92, 0.8)
    sun.angle = math.radians(3)
    so = bpy.data.objects.new("sun", sun)
    bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = tuple(math.radians(a) for a in sun_rot)
    rnd = random.Random(seed)
    for k in range(26):
        x = rnd.uniform(-26, 26)
        y = rnd.uniform(18, 34)
        tree((x, y, 0), rnd.uniform(4, 7), seed=k, name=f"bt{k}", r=rnd.uniform(1.2, 2.0))
    for k in range(8 if side_trees else 0):
        x = rnd.choice([-1, 1]) * rnd.uniform(14, 24)
        tree((x, rnd.uniform(-4, 14), 0), rnd.uniform(4, 6), seed=100 + k, name=f"st{k}", r=1.5)
    for k in range(5):
        sphere(18, (rnd.uniform(-60, 60), rnd.uniform(70, 90), -8), (1.6, 1.0, 0.6), mat("hill", "#8fae6a", rough=0.95), seg=32, name=f"hill{k}")
    return so
