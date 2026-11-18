# 2026-11-18-b: "Your foot never falls asleep" (big-question, why a foot 'falls asleep').
# Sets: movie night in a cosy living room at dusk (the 2026-11-13-b room re-dressed: mustard sofa, a TV on the console
# glowing with a film, a bowl of popcorn and two mugs on the coffee table, warm lamp light, orange evening sky outside),
# 2 new angles (wide from the right, mid by the sofa); inside the leg: a glossy plum studio where a fat yellow nerve cable
# (a bundle of fibres in a translucent sheath) runs over a pale bone, once free and once squashed flat under a big
# rounded "other knee" (same camera). Cut-outs: the phone (live chat screen), a popcorn bowl.
import math, os, random

# sofa(), plant(), lamp(), router(), build_room() + checker_mat(), seg(), tree(), house(), sunny(), drop_cams() (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-13-b/assets.py")).read().split("\n# ---------------------------------------------------------------- the karst valley")[0]
_src = _src.split("\ndef room_angles(")[0]
exec(compile(_src, "b13_helpers", "exec"), globals())


def recolor(name, hexc):
    m = bpy.data.materials.get(name)
    if m:
        m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*hexrgb(hexc), 1)


def popcorn_bowl(x, y, z, s=1.0):
    bowl = mat("bowl", "#d6483e", rough=0.35, coat=0.5)
    lathe([(0.0, 0.0), (0.12 * s, 0.0), (0.2 * s, 0.13 * s), (0.21 * s, 0.14 * s), (0.0, 0.14 * s)], 40, (x, y, z), bowl, subdiv=1)
    pc = mat("popcorn", "#fff3d6", rough=0.8, noise_bump=0.6)
    pc2 = mat("popcorn2", "#f2d38a", rough=0.8, noise_bump=0.6)
    random.seed(4)
    for k in range(38):
        a = random.uniform(0, 2 * math.pi); d = math.sqrt(random.uniform(0, 1)) * 0.17 * s
        sphere(random.uniform(0.026, 0.04) * s, (x + math.cos(a) * d, y + math.sin(a) * d, z + 0.14 * s + random.uniform(0, 0.07) * s * (1 - d / (0.18 * s))),
               (1.1, 1.0, 0.85), pc if k % 4 else pc2, seg=10)


def tv(x, y, z):
    frame = mat("tv_frame", "#1d2026", rough=0.3, coat=0.6)
    box((1.5, 0.08, 0.86), (x, y, z + 0.5), material=frame, bevel=0.03)
    box((0.06, 0.2, 0.08), (x, y, z + 0.04), material=frame, bevel=0.01)
    # the film on screen: dusk sky + a hill + a big moon (emissive, so it glows)
    scr = mat("tv_screen", "#ff9d5c", emit="#ff8f50", emit_strength=1.6)
    box((1.38, 0.02, 0.74), (x, y - 0.045, z + 0.5), material=scr, bevel=0.0)
    box((1.38, 0.025, 0.26), (x, y - 0.05, z + 0.26), material=mat("tv_hill", "#5a3d7a", emit="#4a3a8a", emit_strength=1.2), bevel=0.0)
    cylinder(0.11, 0.02, (x + 0.35, y - 0.06, z + 0.66), (90, 0, 0), mat("tv_moon", "#fff3c4", emit="#fff0c0", emit_strength=3.0), verts=32)


def build_movie_room():
    build_room(False)
    recolor("sofa_fab", "#d9a23a"); recolor("sofa_cush", "#e8b54a"); recolor("pillow", "#3f7fbf"); recolor("rug", "#3c8f8c")
    recolor("wall", "#f0dcc0")
    # remove the router (it was the Wi-Fi video's star) and put a TV on the console
    for o in [o for o in bpy.data.objects if o.data and getattr(o.data, "materials", None)
              and any(m and m.name.startswith("router") for m in o.data.materials)]:
        bpy.data.objects.remove(o)
    tv(-2.0, 3.6, 0.58)
    # a ceiling with a soft round light, so the wide angle reads as a room (not open to the sky)
    box((9.4, 13.0, 0.14), (0, -2.1, 3.37), material=mat("ceiling", "#f6eadb", rough=0.9), bevel=0.0, name="ceiling")
    cylinder(0.35, 0.06, (0.4, 1.0, 3.28), material=mat("ceil_lamp", "#fff3d6", emit="#ffe2b0", emit_strength=3.0), verts=48)
    box((0.16, 7.5, 3.3), (4.5, 0.4, 1.65), material=mat("wall3", "#ead9bd", rough=0.85), bevel=0.0, name="right_wall")
    pt = bpy.data.lights.new("room_l", "AREA"); pt.energy = 420; pt.color = hexrgb("#ffd9a8"); pt.size = 2.0
    po = bpy.data.objects.new("room_l", pt); bpy.context.scene.collection.objects.link(po); po.location = (0.4, 0.5, 3.15)
    popcorn_bowl(0.85, 1.0, 0.45)
    cylinder(0.08, 0.12, (0.15, 0.95, 0.51), material=mat("mug2", "#3f7fbf", rough=0.3, coat=0.4), verts=24)
    # evening: orange sky, low warm sun, the TV and lamp glow
    w = bpy.context.scene.world
    sun = bpy.data.objects.get("sun")
    if sun:
        sun.data.color = hexrgb("#ffb070"); sun.data.energy = 2.2
    L = bpy.data.lights.new("tv_l", "AREA"); L.energy = 160; L.color = hexrgb("#ff9a60"); L.size = 1.2
    o = bpy.data.objects.new("tv_l", L); bpy.context.scene.collection.objects.link(o); o.location = (-2.0, 3.0, 1.1)
    o.rotation_euler = (math.radians(90), 0, 0)


def room_angles():
    build_movie_room()
    drop_cams(); camera((2.2, -4.6, 1.55), (-0.6, 2.6, 1.0), lens=22, fstop=8.0)
    still("plate_movie_wide", 1080, 1920, 40)
    drop_cams(); camera((0.4, -2.2, 1.35), (1.2, 3.0, 0.8), lens=26, fstop=4.0)
    still("plate_movie_mid", 1080, 1920, 40)


# ---------------------------------------------------------------- inside the leg: the nerve cable
def nerve_set(squeezed=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.25)
    world_color(hexrgb("#4a2448"), 0.8)
    floor("#5a2e57", rough=0.4, size=40)
    bone = mat("bone", "#efe4cf", rough=0.35, coat=0.4, sss=0.1)
    # the bone the nerve wraps over (a rounded head on a shaft), lying across the frame
    cylinder(0.42, 6.0, (0, 0.55, 0.42), (0, 90, 0), bone, verts=48, bevel=0.05)
    sphere(0.62, (0.0, 0.55, 0.5), (1.1, 1.0, 0.9), bone, seg=48)
    # the nerve: 7 fibres in a hex bundle + a translucent sheath, along x, resting on the bone head
    fib = mat("fibre", "#f6c443", rough=0.3, coat=0.6, sss=0.2)
    fib2 = mat("fibre2", "#f2a93a", rough=0.3, coat=0.6, sss=0.2)
    sheath = mat("sheath", "#ffe9a8", rough=0.1, alpha=0.35, coat=0.8)
    z0, y0, r = 1.3, 0.1, 0.34
    offs = [(0, 0)] + [(math.cos(a) * r * 0.62, math.sin(a) * r * 0.62) for a in [k * math.pi / 3 for k in range(6)]]
    segs = [(-4.0, -0.75), (-0.75, 0.75), (0.75, 4.0)] if squeezed else [(-4.0, 4.0)]
    for (xa, xb) in segs:
        mid = (xa + xb) / 2; ln = xb - xa
        sq = squeezed and abs(mid) < 0.5
        zs = 0.42 if sq else 1.0; ys = 1.45 if sq else 1.0
        zc = z0 - (0.2 if sq else 0)
        for k, (dy, dz) in enumerate(offs):
            cylinder(r * 0.3, ln, (mid, y0 + dy * ys, zc + dz * zs), (0, 90, 0), fib if k % 2 else fib2, verts=24, bevel=0.0)
        o = cylinder(r * 1.05, ln, (mid, y0, zc), (0, 90, 0), sheath, verts=32, bevel=0.0)
        o.scale = (zs, ys, 1.0) if sq else (1, 1, 1)
    if squeezed:
        # the other knee pressing down: a big soft rounded pad of skin
        skin = mat("knee", "#e3a27f", rough=0.5, sss=0.3, coat=0.2)
        sphere(1.0, (0.0, 0.1, 2.0), (1.05, 0.95, 0.85), skin, seg=64)
        # pressure arrows (glossy red cones) pushing down on it
        red = mat("press", "#d6483e", rough=0.3, coat=0.6)
        for dx in (-0.7, 0.7):
            cone(0.16, 0.32, (dx, 0.1, 3.15), (180, 0, 0), red)
            cylinder(0.05, 0.4, (dx, 0.1, 3.5), material=red, verts=16)
    # muscle bundles + a red and a blue vessel behind (soft tissue backdrop)
    mus = mat("muscle", "#c4505a", rough=0.35, coat=0.5, sss=0.25)
    mus2 = mat("muscle2", "#d8707a", rough=0.35, coat=0.5, sss=0.25)
    random.seed(12)
    for k in range(9):
        yy = 2.6 + (k % 3) * 0.7; zz = 0.5 + (k // 3) * 1.05 + random.uniform(-0.15, 0.15)
        o = cylinder(0.5, 12.0, (random.uniform(-0.5, 0.5), yy, zz), (0, 90, random.uniform(-4, 4)), mus if k % 2 else mus2, verts=32, bevel=0.0)
    cylinder(0.13, 12.0, (0, 1.4, 0.35), (0, 90, 0), mat("artery", "#e0303a", rough=0.25, coat=0.7), verts=24, bevel=0.0)
    cylinder(0.12, 12.0, (0, 1.75, 0.3), (0, 90, 0), mat("vein", "#4a6fd0", rough=0.25, coat=0.7), verts=24, bevel=0.0)
    area_light((-3.0, -3.0, 4.0), (0, 0.2, 1.0), 700, 3, "#ffe2c2", "key")
    area_light((3.2, 2.5, 3.0), (0, 0.2, 1.0), 420, 2.5, "#8fd3ff", "rim")
    area_light((0.5, -4.0, 1.0), (0, 0.2, 1.0), 160, 3, "#ffc0e0", "fill")
    camera((5.6, -2.3, 2.3), (0.0, 0.3, 1.2), lens=30, fstop=4.0)


if not os.environ.get("BK_PROPS_ONLY"):
    room_angles()
    nerve_set(False); still("plate_nerve_open", 1080, 1920, 40)
    nerve_set(True); still("plate_nerve_squeeze", 1080, 1920, 40)

# cut-outs
reset(800, 800, 30, 0.1, samples=24, bloom=0)
world_color(hexrgb("#dfe8f2"), 0.6)
area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")
body, scr = phone((0, 0, 0), (0, 0, 0), w=0.8)
camera((0, -3.4, 0.1), (0, 0, 0), lens=60, fstop=0)
phone_sprite("phone", scr, samples=40)
reset(800, 800, 30, 0.1, samples=24, bloom=0)
world_color(hexrgb("#dfe8f2"), 0.6)
area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")
popcorn_bowl(0, 0, 0, 2.5)
camera((0.3, -2.4, 1.6), (0, 0, 0.3), lens=50, fstop=0)
still("popcorn_bowl", 700, 600, 32, transparent=True, crop=True)
