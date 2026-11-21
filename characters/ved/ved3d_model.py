"""3D Professor Ved: a real modelled character in Blender (front, side and back), built from code so it can be rebuilt,
posed and re-lit by the autopilot. Same identity as the 2D Ved: warm skin, black swept quiff with short sides, full dark
beard and moustache, almond eyes with dark upper lids, white fitted shirt with rolled sleeves, gold spark pin and gold
pencil in the breast pocket, dark trousers and belt with a silver buckle, black shoes, gold watch on his left wrist.

Build method: every body part is a skin-modifier skeleton (clean, organic tubes) or a shaped sphere, smoothed with
subdivision. Stylised proportions (big head, long torso) match the 2D sheet: 1.75 m tall.

    python characters/ved/ved3d_model.py --views front,three_q,side,back,head --out /tmp/ved3dm
    python characters/ved/ved3d_model.py --pose explain --views three_q --out /tmp/ved3dm
    python characters/ved/ved3d_model.py --save characters/ved/ved3d.blend     # keep the model as a .blend
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import bpy                                         # noqa: E402
import bmesh                                       # noqa: E402
from mathutils import Vector                      # noqa: E402
from autopilot import blendkit as bk              # noqa: E402

# ---------------------------------------------------------------- palette (same as make.py)
SKIN, HAIR, BEARD, LIPS = "#d6976b", "#141418", "#1b1717", "#b8705f"
IRIS, SHIRT, TROUSER, GOLD = "#4a2e1c", "#f3f2ee", "#23262d", "#d4a64a"
BELT, SHOE, SILVER, BADGE = "#121214", "#0f0f11", "#c9ccd3", "#16232b"

HEAD_C = Vector((0, 0, 1.605))      # head centre
HA, HB, HC = 0.102, 0.114, 0.134    # head half-width, half-depth, half-height
M = {}                              # materials


def mats():
    M["skin"] = bk.mat("skin", SKIN, rough=0.55, sss=0.12)
    M["hair"] = bk.mat("hair", HAIR, rough=0.45, coat=0.08, noise_bump=0.06)
    M["beard"] = bk.mat("beard", BEARD, rough=0.7, noise_bump=0.25)
    M["shirt"] = bk.mat("shirt", SHIRT, rough=0.82, noise_bump=0.04)
    M["shirt_line"] = bk.mat("shirt_line", "#d9dbe2", rough=0.8)
    M["trouser"] = bk.mat("trouser", TROUSER, rough=0.7)
    M["belt"] = bk.mat("belt", BELT, rough=0.35, coat=0.3)
    M["shoe"] = bk.mat("shoe", SHOE, rough=0.25, coat=0.6)
    M["silver"] = bk.metal(SILVER, rough=0.25, name="silver")
    M["gold"] = bk.metal(GOLD, rough=0.28, name="gold")
    M["badge"] = bk.mat("badge", BADGE, rough=0.3, coat=0.5)
    M["sclera"] = bk.mat("sclera", "#f5efe6", rough=0.25)
    M["iris"] = bk.mat("iris", IRIS, rough=0.2, coat=0.8)
    M["pupil"] = bk.mat("pupil", "#0b0706", rough=0.15, coat=1.0)
    M["lid"] = bk.mat("lid", "#1a1517", rough=0.6)
    M["lips"] = bk.mat("lips", LIPS, rough=0.45, sss=0.1)
    M["mouth"] = bk.mat("mouth", "#3a1714", rough=0.6)
    M["strap"] = bk.mat("strap", "#3b2a20", rough=0.5)
    M["face_dial"] = bk.mat("dial", "#f4ead2", rough=0.3)
    M["pencil_cap"] = bk.mat("pcap", "#2b2b30", rough=0.3)


# ---------------------------------------------------------------- skin-modifier skeletons
def skel(name, verts, edges, radii, material, subd=2, root=0, smooth=True):
    """verts: points; edges: index pairs; radii: (rx, ry) per vertex. Returns the object (modifiers live)."""
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], edges, [])
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    sk = ob.modifiers.new("skin", "SKIN")
    sk.use_smooth_shade = smooth
    sk.branch_smoothing = 0.6
    for i, r in enumerate(radii):
        d = me.skin_vertices[0].data[i]
        d.radius = r if isinstance(r, (tuple, list)) else (r, r)
        d.use_root = i == root
    sd = ob.modifiers.new("smooth", "SUBSURF")
    sd.levels = subd
    sd.render_levels = subd
    ob.data.materials.append(material)
    return ob


def chain(name, pts, radii, material, subd=2):
    return skel(name, pts, [(i, i + 1) for i in range(len(pts) - 1)], radii, material, subd)


def sphere(name, loc, scale, material, seg=48, rings=32, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=1, location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.shade_smooth()
    ob.data.materials.append(material)
    return ob


def cyl(name, loc, r, depth, material, rot=(0, 0, 0), verts=48, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.shade_smooth()
    ob.data.materials.append(material)
    bv = ob.modifiers.new("bevel", "BEVEL")
    bv.width = min(r, depth) * 0.25
    bv.segments = 3
    return ob


def apply_all(ob):
    bpy.context.view_layer.objects.active = ob
    for m in list(ob.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)


# ---------------------------------------------------------------- head
def head_surface(u, v):
    """Shaped head: ellipsoid with a narrower jaw, flatter cheeks and a fuller cranium. u lon, v lat (rad)."""
    x = math.cos(v) * math.sin(u)
    y = -math.cos(v) * math.cos(u)
    z = math.sin(v)
    sx, sy, sz = HA, HB, HC
    if z < 0:                                   # jaw tapers toward the chin
        t = -z
        sx *= 1 - 0.32 * t ** 1.6
        sy *= 1 - 0.10 * t ** 2
    else:
        sx *= 1 + 0.04 * z                      # fuller cranium
    if y > 0:                                   # back of the head
        sy *= 1.04
    return Vector((x * sx, y * sy, z * sz))


def head():
    me = bpy.data.meshes.new("head")
    bm = bmesh.new()
    nu, nv = 64, 40
    grid = []
    for j in range(nv + 1):
        v = -math.pi / 2 + math.pi * j / nv
        row = []
        for i in range(nu):
            u = 2 * math.pi * i / nu
            row.append(bm.verts.new(HEAD_C + head_surface(u, v)))
        grid.append(row)
    for j in range(nv):
        for i in range(nu):
            a, b = grid[j][i], grid[j][(i + 1) % nu]
            c, d = grid[j + 1][(i + 1) % nu], grid[j + 1][i]
            try:
                bm.faces.new((a, b, c, d))
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("head", me)
    bpy.context.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    ob.data.materials.append(M["skin"])
    return ob


def on_face(x, z, push=0.0):
    """Point on the head's front surface at local x (left-right) and z (up-down), pushed out by `push`."""
    v = math.asin(max(-1, min(1, z / HC)))
    cz = math.cos(v)
    best = None
    for k in range(400):
        u = -math.pi / 2 + math.pi * k / 399
        q = head_surface(u, v)
        if best is None or abs(q.x - x) < abs(best.x - x):
            best = q
    n = Vector((best.x / HA ** 2, best.y / HB ** 2, best.z / HC ** 2)).normalized()
    return HEAD_C + best + n * push


def face_features(expr="warm"):
    obs = []
    # ears
    for s in (-1, 1):
        e = sphere(f"ear{s}", HEAD_C + Vector((s * (HA * 0.96), 0.012, 0.0)), (0.018, 0.03, 0.034), M["skin"],
                   rot=(0, 0, math.radians(-12 * s)))
        obs.append(e)
    # nose: a soft wedge
    tip = on_face(0, -0.016, 0.017)
    root = on_face(0, 0.026, 0.002)
    obs.append(chain("nose", [root, (root + tip) / 2 + Vector((0, -0.006, 0)), tip, tip + Vector((0, 0.006, -0.012))],
                     [(0.007, 0.0055), (0.008, 0.0065), (0.0115, 0.0095), (0.0085, 0.007)], M["skin"]))
    for s in (-1, 1):                           # nostril wings
        obs.append(sphere(f"ala{s}", tip + Vector((s * 0.0105, 0.008, -0.006)), (0.0065, 0.007, 0.006), M["skin"]))
    # eyes: sclera, iris, pupil, upper lid with lash line
    open_ = {"surprised": 1.0, "smile": 0.55, "warm": 0.65, "think": 0.7, "serious": 0.62, "neutral": 0.75}.get(expr, 0.7)
    for s in (-1, 1):
        c = on_face(s * 0.036, 0.012, -0.004)
        sc = sphere(f"eye{s}", c, (0.0165, 0.012, 0.011 * (0.55 + 0.45 * open_)), M["sclera"])
        front = c + Vector((0, -0.0115, 0))
        ir = sphere(f"iris{s}", front + Vector((0, 0.001, 0)), (0.0072, 0.002, 0.0072), M["iris"])
        pu = sphere(f"pupil{s}", front + Vector((0, -0.0007, 0)), (0.0034, 0.0012, 0.0034), M["pupil"])
        hl = sphere(f"glint{s}", front + Vector((-0.0025, -0.0016, 0.003)), (0.0013, 0.0006, 0.0013),
                    bk.mat("glint", "#ffffff", emit="#ffffff", emit_strength=2.0))
        lid_pts = [c + Vector((x * 0.0175, -0.010 - 0.004 * (1 - abs(x)), 0.0075 * (0.55 + 0.45 * open_) * (1 - x * x) + 0.003))
                   for x in (-1.0, -0.5, 0.0, 0.5, 1.0)]
        lid = chain(f"lid{s}", lid_pts, [(0.0026, 0.0018)] * 5, M["lid"])
        obs += [sc, ir, pu, hl, lid]
    # brows: thick, straight-ish, slight arch
    for s in (-1, 1):
        pts = [on_face(s * x, 0.040 + 0.006 * math.sin(math.pi * (x - 0.018) / 0.05), 0.007) for x in (0.016, 0.03, 0.046, 0.058)]
        obs.append(chain(f"brow{s}", pts, [(0.0075, 0.005), (0.0085, 0.0055), (0.008, 0.005), (0.005, 0.004)], M["hair"]))
    # mouth: dark line and lower lip, under the moustache
    mz = -0.062
    obs.append(chain("mouth", [on_face(x, mz + 0.002 * abs(x) / 0.02, 0.001) for x in (-0.02, -0.01, 0, 0.01, 0.02)],
                     [(0.0018, 0.0015)] * 5, M["mouth"]))
    obs.append(chain("lip", [on_face(x, mz - 0.007, 0.002) for x in (-0.014, 0, 0.014)],
                     [(0.004, 0.003), (0.0055, 0.0045), (0.004, 0.003)], M["lips"]))
    return obs


def smooth(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def pshell(name, u0, u1, vlo, vhi, height, material, nu=120, nv=40, wrap=False, inner=0.004):
    """A smooth shell over the head between two latitude curves vlo(u)..vhi(u) (radians), lifted off the skin by
    height(u, v, t) metres along the normal. Boundaries follow the curves exactly, so edges are clean, not stepped."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    cols = nu if wrap else nu + 1
    grid = []
    for i in range(cols):
        u = u0 + (u1 - u0) * i / nu
        lo, hi = vlo(u), vhi(u)
        col = []
        for j in range(nv + 1):
            t = j / nv
            v = lo + (hi - lo) * t
            p = head_surface(u, v)
            n = Vector((p.x / HA ** 2, p.y / HB ** 2, p.z / HC ** 2)).normalized()
            col.append(bm.verts.new(HEAD_C + p + n * height(u, v, t)))
        grid.append(col)
    for i in range(nu if wrap else nu):
        a, b = grid[i], grid[(i + 1) % cols]
        for j in range(nv):
            try:
                bm.faces.new((a[j], b[j], b[j + 1], a[j + 1]))
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    so = ob.modifiers.new("thick", "SOLIDIFY")
    so.thickness = inner
    so.offset = -1
    sd = ob.modifiers.new("smooth", "SUBSURF")
    sd.levels = 1
    sd.render_levels = 2
    ob.data.materials.append(material)
    return ob


def beard_and_hair():
    obs = []
    asin = lambda z: math.asin(max(-1.0, min(1.0, z)))

    def beard_top(u):                     # cheek line: under the lower lip at the front, up to the sideburn by the ear
        a = abs(u)
        z = -0.72 + 0.30 * smooth(0.14, 0.36, a) + 0.52 * smooth(0.36, 1.45, a) ** 1.15
        return asin(z)
    beard_h = lambda u, v, t: 0.003 + 0.009 * (1 - t ** 2) * (1 - 0.5 * smooth(1.0, 1.5, abs(u)))
    obs.append(pshell("beard", -1.5, 1.5, lambda u: -1.32, beard_top, beard_h, M["beard"], nu=140, nv=36))
    # moustache: one full mass from under the nose, drooping into the beard at the mouth corners
    xs = [-0.036, -0.026, -0.014, 0.0, 0.014, 0.026, 0.036]
    pts = [on_face(x, -0.05 - 0.02 * (abs(x) / 0.036) ** 1.3, 0.005 - 0.004 * (abs(x) / 0.036) ** 2) for x in xs]
    obs.append(chain("moustache", pts, [(0.0105, 0.008), (0.011, 0.0085), (0.012, 0.009), (0.0115, 0.009),
                                        (0.012, 0.009), (0.011, 0.0085), (0.0105, 0.008)], M["beard"]))

    def hair_lo(u):                       # hairline: forehead at the front, above the ears, nape at the back
        c = math.cos(u)
        z = 0.16 + 0.42 * smooth(0.3, 1.0, c) - 0.75 * smooth(0.1, 1.0, -c)
        return asin(z)

    def hair_h(u, v, t):
        z = math.sin(v)
        c = math.cos(u)
        top = 0.006 + 0.012 * smooth(0.35, 0.9, z)
        # the pompadour: volume swept up off the front hairline, highest at the front top, leaning to his left (+x)
        du = math.atan2(math.sin(u - 0.28), math.cos(u - 0.28))
        quiff = 0.05 * math.exp(-du * du / 1.6) * smooth(0.42, 0.72, z) * smooth(-0.7, 0.5, c)
        h = top + quiff
        pole = 0.018 + 0.012                        # all longitudes meet at the crown: blend to one height there
        h = h + (pole - h) * smooth(0.82, 1.0, t)
        return 0.002 + h * smooth(0.0, 0.25, t)
    obs.append(pshell("hair", 0.0, 2 * math.pi, hair_lo, lambda u: math.pi / 2, hair_h, M["hair"], nu=160, nv=44, wrap=True))
    return obs


# ---------------------------------------------------------------- body
POSES = {   # shoulder -> elbow -> wrist for (right arm = -x, left arm = +x); hand: relaxed | open
    "idle": {"R": [(-0.225, 0.0, 1.385), (-0.25, 0.01, 1.11), (-0.255, -0.015, 0.85)],
             "L": [(0.225, 0.0, 1.385), (0.25, 0.01, 1.11), (0.255, -0.015, 0.85)], "hands": ("relaxed", "relaxed")},
    "explain": {"R": [(-0.225, 0.0, 1.385), (-0.3, -0.04, 1.14), (-0.27, -0.16, 1.33)],
                "L": [(0.225, 0.0, 1.385), (0.25, 0.01, 1.11), (0.255, -0.015, 0.85)], "hands": ("open", "relaxed")},
}


def torso_and_shirt(pose):
    obs = []
    # shirt body: pelvis -> waist -> chest -> shoulder line, with the arms branching from the shoulders
    P = POSES[pose]
    v = [(0, 0.0, 0.84), (0, 0.0, 1.0), (0, -0.004, 1.2), (0, 0.004, 1.34), (0, 0.006, 1.405)]
    r = [(0.162, 0.13), (0.158, 0.124), (0.185, 0.142), (0.178, 0.13), (0.085, 0.075)]
    e = [(0, 1), (1, 2), (2, 3), (3, 4)]
    for side in ("R", "L"):
        sh, el, wr = [Vector(p) for p in P[side]]
        cuff = el + (wr - el) * 0.32                # sleeves rolled to just below the elbow
        base = len(v)
        v += [tuple(sh), tuple(el), tuple(cuff)]
        r += [(0.062, 0.058), (0.05, 0.048), (0.049, 0.047)]
        e += [(3, base), (base, base + 1), (base + 1, base + 2)]
    shirt = skel("shirt", v, e, r, M["shirt"], subd=2)
    obs.append(shirt)
    # rolled cuffs, forearms, hands, watch
    for side in ("R", "L"):
        sh, el, wr = [Vector(p) for p in P[side]]
        cuff = el + (wr - el) * 0.32
        d = (wr - el).normalized()
        ring = cyl(f"cuff{side}", cuff, 0.052, 0.05, M["shirt"], rot=d.to_track_quat("Z", "Y").to_euler())
        obs.append(ring)
        obs.append(chain(f"forearm{side}", [cuff - d * 0.02, (cuff + wr) / 2, wr], [(0.038, 0.034), (0.034, 0.03), (0.027, 0.022)],
                         M["skin"]))
        obs += hand(side, wr, d, POSES[pose]["hands"][0 if side == "R" else 1])
        if side == "L":                             # gold watch on his left wrist
            q = d.to_track_quat("Z", "Y").to_euler()
            obs.append(cyl("watch_strap", wr - d * 0.03, 0.03, 0.018, M["strap"], rot=q))
            face = wr - d * 0.03 + Vector((0.0, -0.03, 0))
            obs.append(cyl("watch_case", face, 0.014, 0.008, M["gold"], rot=(math.radians(90), 0, 0)))
            obs.append(cyl("watch_dial", face + Vector((0, -0.0045, 0)), 0.011, 0.002, M["face_dial"], rot=(math.radians(90), 0, 0)))
    # neck
    obs.append(chain("neck", [(0, 0.012, 1.38), (0, 0.008, 1.47), (0, 0.004, 1.52)], [(0.052, 0.05), (0.05, 0.048), (0.05, 0.048)],
                     M["skin"]))
    # collar: open band collar with a V, two flaps
    for s in (-1, 1):
        pts = [(s * 0.004, -0.06, 1.37), (s * 0.04, -0.052, 1.42), (s * 0.06, -0.01, 1.455), (s * 0.04, 0.04, 1.46),
               (0, 0.055, 1.46)]
        obs.append(chain(f"collar{s}", pts, [(0.005, 0.012), (0.006, 0.014), (0.006, 0.015), (0.006, 0.014), (0.006, 0.014)],
                         M["shirt"]))
    # V of skin at the open collar
    dg = bpy.context.evaluated_depsgraph_get()

    def front(x, z):                            # y of the shirt's front surface at (x, z)
        ok, loc, _, _ = shirt.ray_cast((x, -1.0, z), (0, 1, 0), depsgraph=dg)
        return loc.y if ok else -0.13
    # placket and buttons follow the chest
    obs.append(chain("placket", [(0.0, front(0, z) - 0.001, z) for z in (0.87, 1.0, 1.12, 1.24, 1.36)],
                     [(0.007, 0.0016)] * 5, M["shirt_line"], subd=1))
    for z in (1.3, 1.2, 1.1, 1.0, 0.9):
        obs.append(cyl("button", (0.0, front(0, z) - 0.003, z), 0.0055, 0.003, M["shirt_line"], rot=(math.radians(90), 0, 0)))
    # breast pocket (his right = -x) with the gold pencil
    py = front(-0.085, 1.235)
    obs.append(bk.box((0.075, 0.008, 0.07), loc=(-0.085, py - 0.001, 1.235), material=M["shirt"], bevel=0.002))
    obs.append(bk.box((0.077, 0.009, 0.005), loc=(-0.085, py - 0.002, 1.268), material=M["shirt_line"], bevel=0.001))
    obs.append(cyl("pencil", (-0.072, py + 0.002, 1.278), 0.0055, 0.07, M["gold"]))
    obs.append(cyl("pencil_cap", (-0.072, py + 0.002, 1.315), 0.0058, 0.008, M["pencil_cap"]))
    # spark pin by the collar
    pin = (-0.075, front(-0.075, 1.36) - 0.003, 1.36)
    obs.append(cyl("pin", pin, 0.016, 0.004, M["badge"], rot=(math.radians(80), 0, 0)))
    obs.append(bk.torus(r=0.016, thick=0.0018, loc=pin, rot=(80, 0, 0), material=M["gold"]))
    star = bpy.data.curves.new("spark", "CURVE")
    star.dimensions = "2D"
    sp = star.splines.new("POLY")
    pts = []
    for k in range(8):
        a = math.pi / 2 + k * math.pi / 4
        rr = 0.012 if k % 2 == 0 else 0.0035
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    star.fill_mode = "BOTH"
    star.extrude = 0.0012
    so = bpy.data.objects.new("spark", star)
    bpy.context.collection.objects.link(so)
    so.location = (pin[0], pin[1] - 0.0028, pin[2])
    so.rotation_euler = (math.radians(80), 0, 0)
    so.data.materials.append(M["gold"])
    obs.append(so)
    return obs


def hand(side, wr, d, kind):
    """A simple, clean hand: palm block + four fingers + thumb as tubes."""
    s = -1 if side == "R" else 1
    obs = []
    if kind == "open":                              # raised, palm to camera, fingers up
        up, across, out = Vector((0, -0.02, 1)).normalized(), Vector((1, 0, 0)), Vector((0, -1, 0))
        palm_c = wr + up * 0.05
    else:                                           # hanging, palm facing the thigh
        up, across, out = d, Vector((0, -1, 0)), Vector((s, 0, 0))
        palm_c = wr + d * 0.045
    obs.append(sphere(f"palm{side}", palm_c, (0.04, 0.021, 0.048), M["skin"],
                      rot=up.to_track_quat("Z", "Y").to_euler()))
    for k, (off, ln) in enumerate(((-0.025, 0.068), (-0.0085, 0.078), (0.0085, 0.074), (0.024, 0.06))):
        b = palm_c + up * 0.04 + across * off
        curl = out * (0.008 if kind == "relaxed" else 0.0)
        pts = [b, b + up * ln * 0.5 + curl, b + up * ln + curl * 2.2]
        obs.append(chain(f"finger{side}{k}", pts, [0.0112, 0.01, 0.0088], M["skin"]))
    tb = palm_c - across * 0.03 * (1 if kind == "open" else -s) - up * 0.01
    tdir = (up * 0.6 - across * 0.8 * (1 if kind == "open" else -s) + out * 0.3).normalized()
    obs.append(chain(f"thumb{side}", [tb, tb + tdir * 0.03, tb + tdir * 0.055], [0.012, 0.0105, 0.009], M["skin"]))
    return obs


def girth(ob, z, band=0.012):
    """Half-width and half-depth of an object's evaluated (smoothed) mesh at height z, to fit belts and cuffs."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = ob.evaluated_get(dg).to_mesh()
    xs = [abs(v.co.x) for v in me.vertices if abs(v.co.z - z) < band]
    ys = [abs(v.co.y) for v in me.vertices if abs(v.co.z - z) < band]
    ob.evaluated_get(dg).to_mesh_clear()
    return (max(xs), max(ys)) if xs else (0.15, 0.1)


def legs_and_shoes():
    obs = []
    v = [(0, 0.0, 0.9), (0, 0.0, 0.8)]
    r = [(0.15, 0.124), (0.158, 0.126)]
    e = []
    for s in (-1, 1):
        b = len(v)
        v += [(s * 0.084, 0.0, 0.7), (s * 0.09, -0.005, 0.45), (s * 0.094, 0.0, 0.1), (s * 0.094, 0.0, 0.075)]
        r += [(0.09, 0.095), (0.074, 0.076), (0.062, 0.062), (0.063, 0.062)]
        e += [(1, b), (b, b + 1), (b + 1, b + 2), (b + 2, b + 3)]
    e = [(0, 1)] + e
    obs.append(skel("trousers", v, e, r, M["trouser"], subd=2))
    for s in (-1, 1):
        obs.append(chain(f"shoe{s}", [(s * 0.097, 0.04, 0.045), (s * 0.099, -0.05, 0.04), (s * 0.102, -0.15, 0.032)],
                         [(0.052, 0.042), (0.054, 0.038), (0.046, 0.03)], M["shoe"]))
    # belt + buckle
    rx, ry = girth(obs[0], 0.845)
    obs.append(cyl("belt", (0, 0, 0.845), 1.0, 0.04, M["belt"], scale=(rx * 1.035, ry * 1.05, 1)))
    obs.append(bk.box((0.05, 0.008, 0.034), loc=(0, -ry * 1.05 - 0.003, 0.845), material=M["silver"], bevel=0.003))
    obs.append(bk.box((0.036, 0.01, 0.022), loc=(0, -ry * 1.05 - 0.005, 0.845), material=M["belt"], bevel=0.002))
    return obs


# ---------------------------------------------------------------- scene, cameras, render
VIEWS = {   # azimuth (deg, 0 = front), camera height, target z, distance, lens
    "front": (0, 1.05, 0.93, 4.6, 50), "three_q": (-35, 1.15, 0.93, 4.6, 50), "side": (-90, 1.05, 0.93, 4.6, 50),
    "back": (180, 1.05, 0.93, 4.6, 50), "head": (-25, 1.62, 1.6, 1.3, 70), "head_front": (0, 1.62, 1.6, 1.3, 70), "head_side": (-90, 1.62, 1.6, 1.3, 70),
}


def stage():
    bk.world_hdri("studio", strength=0.3, backdrop=(0.93, 0.89, 0.8))
    sc = bpy.context.scene
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = -0.95
    bk.floor("#e8d9b8", rough=0.8, size=30)
    bk.area_light((0, 1.0, 4.0), (0, 9, 2.0), power=320, size=8.0, color="#fff1dc")       # soft wash on the back wall
    bk.area_light((-2.4, -3.0, 3.2), (0, 0, 1.2), power=520, size=3.0, color="#ffe9d2")    # soft warm key
    bk.area_light((2.6, 1.8, 2.6), (0, 0, 1.4), power=420, size=1.4, color="#bfe6ff")      # cool rim
    bk.area_light((2.4, -3.2, 1.4), (0, 0, 1.0), power=160, size=4.0, color="#fff6ea")     # fill
    bk.area_light((0, -1.2, 2.3), (0, 0, 1.6), power=35, size=0.8, color="#fff1e0")        # face fill


def build(pose="idle", expr="warm"):
    mats()
    parts = [head()] + face_features(expr) + beard_and_hair() + torso_and_shirt(pose) + legs_and_shoes()
    root = bpy.data.objects.new("Ved", None)
    bpy.context.collection.objects.link(root)
    for ob in bpy.context.collection.objects:
        if ob is not root and ob.parent is None and ob.type in ("MESH", "CURVE") and not ob.name.startswith("floor"):
            ob.parent = root
    return root


def render_views(root, views, out, prefix, w, h, samples):
    """The camera stays put and Ved turns, so the set and light read the same in every view (a true turnaround)."""
    sc = bpy.context.scene
    sc.cycles.samples = samples
    sc.render.resolution_x, sc.render.resolution_y = w, h
    for name in views:
        az, hz, tz, dist, lens = VIEWS[name]
        root.rotation_euler = (0, 0, math.radians(-az))
        cam, _ = bk.camera(loc=(0, -dist, hz), target=(0, 0, tz), lens=lens, fstop=None, name=f"cam_{name}")
        sc.camera = cam
        sc.render.filepath = os.path.join(out, f"{prefix}_{name}.png")
        bpy.ops.render.render(write_still=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pose", default="idle", choices=sorted(POSES))
    ap.add_argument("--expr", default="warm")
    ap.add_argument("--views", default="front,three_q,side,back,head")
    ap.add_argument("--size", default="720x1280")
    ap.add_argument("--samples", type=int, default=48)
    ap.add_argument("--out", default="/tmp/ved3dm")
    ap.add_argument("--save", default="")
    a = ap.parse_args()
    w, h = map(int, a.size.split("x"))
    os.makedirs(a.out, exist_ok=True)
    bk.reset(w=w, h=h, samples=a.samples, motion_blur=False, bloom=0.0)
    stage()
    root = build(a.pose, a.expr)
    if a.save:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.save))
    if a.views:
        render_views(root, a.views.split(","), a.out, a.pose, w, h, a.samples)


if __name__ == "__main__":
    main()
