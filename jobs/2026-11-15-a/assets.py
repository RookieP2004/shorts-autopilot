# 2026-11-15-a: "You've been told DNA is tiny" (scale-shock, "you've been told X" hook). Sets: a warm genetics lab (the
# 2026-11-08-b lab rebuilt with peach walls, the brain swapped for a giant glossy double-helix sculpture on the pedestal),
# 3 angles (wide / mid / close on the helix); a deep-space plate with the Sun on the left and a small blue Neptune far right.
# Cut-outs: a cell nucleus, a protein spool wound with DNA thread (histone), a tennis ball, a thread bobbin.
import math, os, random

_src = open(os.path.join(ROOT, "jobs/2026-11-08-b/assets.py")).read().split("\ndef town(")[0]
exec(compile(_src, "b_helpers", "exec"), globals())
_c = open(os.path.join(ROOT, "jobs/2026-11-08-c/assets.py")).read()
exec(compile(_c[_c.index("def seg("):_c.index("def tree(")], "seg", "exec"), globals())


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def recolor(name, hexc):
    m = bpy.data.materials.get(name)
    if m:
        m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*hexrgb(hexc), 1)


def helix(loc=(0, 0, 0), s=1.0, name="helix", turns=1.6, height=1.6):
    """A glossy double helix: two backbones of beads (amber / teal) with coloured rungs between them."""
    x, y, z = loc
    a_m = plastic("#f2b04a", 0.2, name + "_a"); b_m = plastic("#3d7fd1", 0.2, name + "_b")
    rung = [plastic(c, 0.3, f"{name}_r{k}") for k, c in enumerate(("#d9534f", "#46965a", "#f6efe2", "#6fc3c0"))]
    n = int(turns * 14)
    R = 0.32 * s
    prev = None
    for k in range(n + 1):
        t = k / n
        ang = t * turns * 2 * math.pi
        zz = z + t * height * s
        p1 = (x + R * math.cos(ang), y + R * math.sin(ang), zz)
        p2 = (x + R * math.cos(ang + math.pi), y + R * math.sin(ang + math.pi), zz)
        sphere(0.07 * s, p1, 1, a_m, seg=20); sphere(0.07 * s, p2, 1, b_m, seg=20)
        if prev:
            seg(prev[0], p1, 0.035 * s, a_m); seg(prev[1], p2, 0.035 * s, b_m)
        mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, zz)
        seg(p1, mid, 0.025 * s, rung[k % 4]); seg(mid, p2, 0.025 * s, rung[(k + 2) % 4])
        prev = (p1, p2)


def brain(loc=(0, 0, 0), s=1.0, lit=False, name="brain"):     # lab() puts this on the pedestal
    helix(loc, s * 0.95, "bighelix")
    return []


def lab_dna():
    lab(False)
    recolor("wallb", "#f4b183"); recolor("walls", "#f7c9a0"); recolor("rug", "#2a5d7a"); recolor("bed", "#f2b04a")
    angles = (("lab_wide", (0.2, -9.5, 2.6), (0.0, 0.5, 1.5), 30, 0),
              ("lab_mid", (-0.4, -5.0, 1.8), (0.4, 0.5, 1.3), 34, 0),
              ("lab_close", (0.4, -2.9, 2.0), (1.0, 0.6, 1.85), 40, 3.2))
    for name, loc, tgt, lens, fs in angles:
        drop_cams()
        camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)


def space():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.35)
    world_color(hexrgb("#070b1c"), 0.3)
    random.seed(7)
    st = glow("#f6efe2", 6.0, "star")
    for k in range(260):
        sphere(random.uniform(0.02, 0.06), (random.uniform(-30, 30), 40, random.uniform(-40, 40)), 1, st, seg=8)
    sun = sphere(3.2, (-5.0, 18, 7.5), 1, glow("#ffcf5a", 9.0, "sun"), seg=64)
    sphere(4.2, (-5.0, 18.5, 7.5), 1, mat("corona", "#ff9a3c", emit="#ff9a3c", emit_strength=1.5, alpha=0.25), seg=48)
    nep = sphere(0.6, (2.6, 10, -5.8), 1, mat("nep", "#4f86f7", rough=0.4, coat=0.3, emit="#3d7fd1", emit_strength=0.8), seg=48)
    torus(0.95, 0.02, (2.6, 10, -5.8), (75, 0, 20), mat("ring", "#9fb4c8", rough=0.6))
    d = bpy.data.lights.new("sunl", "POINT"); d.energy = 60000; d.color = hexrgb("#ffe2b0")
    o = bpy.data.objects.new("sunl", d); bpy.context.scene.collection.objects.link(o); o.location = (-5.0, 14, 7.5)
    camera((0, -6, 0), (0, 10, 0), lens=24, fstop=0)
    still("plate_space", 1080, 1920, 40)


def nucleus(c=(0, 0, 0.4), s=1.0):
    x, y, z = c
    sphere(0.42 * s, c, 1, mat("nuc", "#8a5ad1", rough=0.35, sss=0.3, coat=0.5), seg=56)
    pore = mat("pore", "#5b3796", rough=0.4)
    random.seed(3)
    for k in range(26):
        th = random.uniform(0, 2 * math.pi); ph = random.uniform(0.3, 2.8)
        sphere(0.035 * s, (x + 0.42 * s * math.sin(ph) * math.cos(th), y + 0.42 * s * math.sin(ph) * math.sin(th),
                           z + 0.42 * s * math.cos(ph)), 1, pore, seg=12)
    sphere(0.13 * s, (x - 0.12 * s, y - 0.34 * s, z + 0.1 * s), 1, mat("nucleolus", "#d97ab0", rough=0.3, sss=0.3), seg=24)


def spool(c=(0, 0, 0.3), s=1.0):
    """A histone: a round protein bead with DNA thread wound ~1.7 times around it, the thread trailing off both sides."""
    x, y, z = c
    sphere(0.3 * s, c, (1, 1, 0.8), mat("histone", "#6fc3c0", rough=0.35, sss=0.2, coat=0.4), seg=48)
    th = plastic("#f2b04a", 0.25, "dna_thread")
    pts = []
    for k in range(80):
        t = k / 79
        a = t * 1.7 * 2 * math.pi
        pts.append((x + 0.33 * s * math.cos(a), y + 0.33 * s * math.sin(a), z + (t - 0.5) * 0.32 * s))
    pts = [(x - 0.9 * s, y - 0.3 * s, z - 0.3 * s)] + pts + [(x + 0.9 * s, y - 0.3 * s, z + 0.3 * s)]
    for p0, p1 in zip(pts, pts[1:]):
        seg(p0, p1, 0.04 * s, th)


def tennis(c=(0, 0, 0.3), r=0.3):
    sphere(r, c, 1, mat("felt", "#d4e157", rough=0.9, noise_bump=0.5), seg=56)
    x, y, z = c
    wm = mat("seam", "#f6efe2", rough=0.6)
    pts = []
    for k in range(121):
        t = k / 120 * 2 * math.pi
        v = (math.cos(t) + 0.35 * math.cos(3 * t), math.sin(t) - 0.35 * math.sin(3 * t), 0.75 * math.sin(2 * t))
        L = math.sqrt(sum(q * q for q in v))
        pts.append(tuple(cc + r * 1.005 * q / L for cc, q in zip(c, v)))
    for p0, p1 in zip(pts, pts[1:]):
        seg(p0, p1, 0.012 * r / 0.3, wm)


def bobbin(c=(0, 0, 0.3), s=1.0):
    x, y, z = c
    w = wood("#c58b4e", "#9a6634", "bob_wood", 3.0)
    cylinder(0.26 * s, 0.06 * s, (x, y, z - 0.25 * s), material=w, verts=40)
    cylinder(0.26 * s, 0.06 * s, (x, y, z + 0.25 * s), material=w, verts=40)
    cylinder(0.2 * s, 0.44 * s, (x, y, z), material=mat("thread_roll", "#d9534f", rough=0.8, noise_bump=0.6), verts=48)


if not os.environ.get("BK_PROPS_ONLY"):
    lab_dna()
    space()
prop_scene(); nucleus((0, 0, 0.42), 1.0); sprite_camera((0, 0, 0.42), 2.6, 0.5, 50, azimuth=-15)
still("nucleus", 560, 560, 28, transparent=True, crop=True)
prop_scene(); spool((0, 0, 0.35), 1.0); sprite_camera((0, 0, 0.35), 3.2, 0.9, 50, azimuth=-10)
still("spool", 760, 560, 28, transparent=True, crop=True)
prop_scene(); tennis((0, 0, 0.3), 0.3); sprite_camera((0, 0, 0.3), 2.2, 0.4, 50, azimuth=-20)
still("tennis", 500, 500, 28, transparent=True, crop=True)
prop_scene(); bobbin((0, 0, 0.32), 1.0); sprite_camera((0, 0, 0.32), 2.4, 0.6, 50, azimuth=-20)
still("bobbin", 500, 560, 28, transparent=True, crop=True)
