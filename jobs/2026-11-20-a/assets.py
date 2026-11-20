# 2026-11-20-a: "A drug lord bought 4 hippos. Now there are 200" (dark-files, number-shock).
# Sets: the ranch (a sunny private-zoo ranch: white fences, a round pond with 4 hippos, palms, a ranch house, a gate arch);
# 2 angles (wide, mid on the pond). The river (a wide brown-green tropical river, jungle banks, a little wooden fishing
# boat, a big herd of hippos in the water and on a sandbank); 2 angles (high wide on the herd, low close by the boat).
# Cut-out: a hippo (3/4 view).
import math, os, random

# sunny(), house(), tree(), bunting(), drop_cams() ... (frozen 2026-11-09-b helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-09-b/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "b09_helpers", "exec"), globals())


def palm(x, y, h=4.2, seed=1):
    random.seed(seed)
    trunk_m = wood("#a07a52", "#7d5a3a", "trunk", 2.0, 0.8)
    leaf_m = plastic("#3f9a4a", 0.5, "palm_leaf")
    for i in range(9):
        t = i / 9
        cylinder(0.17 - 0.06 * t, h / 9 * 1.06, (x + 0.35 * t * t, y, h / 9 * (i + 0.5)), (0, 6 * t, 0), trunk_m, verts=16, bevel=0)
    top = (x + 0.35, y, h)
    for k in range(9):
        a = k / 9 * 2 * math.pi + random.uniform(-0.2, 0.2); L = random.uniform(1.4, 2.0)
        leaf = sphere(0.5, (top[0] + math.cos(a) * L * 0.5, top[1] + math.sin(a) * L * 0.5, top[2] - 0.25), (L * 0.55, 0.24, 0.04), leaf_m)
        leaf.rotation_euler = (0, math.radians(25), a)


def hippo_mats():
    skin = bpy.data.materials.get("hippo_skin") or mat("hippo_skin", "#8b7d93", rough=0.42, sss=0.05, noise_bump=0.06)
    pink = bpy.data.materials.get("hippo_pink") or mat("hippo_pink", "#d99a9a", rough=0.5)
    eye = bpy.data.materials.get("hippo_eye") or mat("hippo_eye", "#15110f", rough=0.15, coat=0.8)
    tooth = bpy.data.materials.get("hippo_tooth") or mat("hippo_tooth", "#f3ead6", rough=0.35)
    return skin, pink, eye, tooth


def hippo(x, y, z=0.0, yaw=0.0, s=1.0, mouth=False, name="hippo"):
    """A rounded cartoon-real hippo, ~1.5 m tall at s=1, facing -y before yaw. Built around (0,0,0) then moved."""
    skin, pink, eye, tooth = hippo_mats()
    parts = []
    parts.append(sphere(1.0, (0, 0.35, 0.95), (0.95, 1.55, 0.78), skin, seg=48))           # barrel body
    parts.append(sphere(0.7, (0, -1.2, 1.15), (0.78, 0.7, 0.66), skin, seg=40))             # head
    parts.append(sphere(0.6, (0, -1.75, 0.98), (0.9, 0.62, 0.55), skin, seg=40))            # broad muzzle
    parts.append(sphere(0.3, (0, -1.92, 0.78), (1.35, 0.9, 0.5), pink, seg=32))             # pink lower lip
    for sx in (-1, 1):
        parts.append(sphere(0.13, (sx * 0.28, -2.02, 1.18), (1, 0.7, 0.8), skin, seg=20))   # nostril bumps
        parts.append(sphere(0.05, (sx * 0.28, -2.12, 1.22), 1, eye, seg=12))
        parts.append(sphere(0.17, (sx * 0.36, -1.1, 1.62), 1, skin, seg=20))                # eye bumps
        parts.append(sphere(0.075, (sx * 0.38, -1.24, 1.66), 1, eye, seg=16))
        parts.append(sphere(0.11, (sx * 0.4, -0.85, 1.78), (0.8, 0.5, 1.2), pink, seg=16))  # ears
        for sy in (-1, 1):
            parts.append(cylinder(0.24, 0.62, (sx * 0.55, 0.35 + sy * 0.95, 0.3), material=skin, verts=24, bevel=0.08))
    if mouth:
        parts.append(sphere(0.45, (0, -1.85, 0.7), (0.95, 0.75, 0.25), pink, seg=24))
        for sx in (-1, 1):
            parts.append(cone(0.06, 0.28, (sx * 0.38, -2.05, 0.95), material=tooth))
    parts.append(sphere(0.12, (0, 1.92, 1.05), (0.6, 1.4, 0.6), skin, seg=16))              # little tail
    root = empty((0, 0, 0), name)
    for p in parts:
        p.parent = root
    root.scale = (s, s, s)
    root.rotation_euler = (0, 0, math.radians(yaw))
    root.location = (x, y, z)
    return root


def water(w=200, d=200, z=0.0, col="#4f8f8a", name="water"):
    m = mat(name + "_m", col, rough=0.06, coat=0.4, noise_bump=0.12)
    return plane(w, d, (0, 0, z), material=m, name=name)


def fence(x0, x1, y, h=1.0):
    wm = mat("fence_w", "#f6efe2", rough=0.6)
    n = int(abs(x1 - x0) / 1.4) + 1
    for k in range(n):
        xx = x0 + (x1 - x0) * k / max(1, n - 1)
        box((0.14, 0.14, h), (xx, y, h / 2), material=wm, bevel=0.02)
    for zz in (h * 0.45, h * 0.85):
        box((abs(x1 - x0), 0.08, 0.12), ((x0 + x1) / 2, y, zz), material=wm, bevel=0.02)


# ---------------------------------------------------------------- the ranch
def build_ranch():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny("#2f7fd8", "#a9d8f5", 4.4)
    plane(400, 400, (0, 0, 0), material=mat("grass", "#7cbf55", rough=0.9, noise_bump=0.25), name="grass")
    cylinder(4.6, 0.06, (0.6, 3.0, 0.0), material=mat("pond_mud", "#a88a5a", rough=0.9), verts=72, bevel=0.03)
    cylinder(4.3, 0.04, (0.6, 3.0, 0.06), material=mat("pond_w", "#4f9fa8", rough=0.05, coat=0.5, noise_bump=0.1), verts=72, bevel=0)
    # the four hippos, two wading low in the pond, one half out, one on the bank
    hippo(-1.4, 2.4, -0.55, -30, 0.95, name="h1")
    hippo(1.4, 3.6, -0.7, 25, 1.0, mouth=True, name="h2")
    hippo(2.8, 1.6, -0.5, -60, 0.8, name="h3")
    hippo(-3.6, 5.6, 0.0, 40, 0.9, name="h4")
    fence(-9, -2.2, -1.8, 1.0)
    fence(3.4, 9, -1.8, 1.0)
    fence(-9, 9, 9.5, 1.0)
    house(6.8, 11.5, 5.0, 3.6, "#f6efe2", "#b5533c", 1)
    house(-7.5, 12.5, 4.4, 3.4, "#f2c88a", "#7c2533", 2)
    palm(-6.0, 4.0, 5.0, 1); palm(7.0, 5.0, 4.6, 2); palm(-9.5, 8.0, 5.4, 3); palm(10.5, 9.0, 5.0, 4); palm(4.6, 9.5, 4.2, 5)
    tree(-12, 14, 4.2, 1); tree(12, 15, 4.0, 2); tree(0, 16, 4.6, 3)
    # gate arch with the ranch sign
    wd = wood("#8a4f2c", "#5e321a", "gate_wood", 3.0)
    for sx in (-2.6, 2.6):
        cylinder(0.16, 4.2, (0.6 + sx, -1.8, 2.1), material=wd, verts=20)
    box((6.0, 0.3, 0.9), (0.6, -1.8, 4.0), material=mat("gate_board", "#f6efe2", rough=0.6), bevel=0.06)
    text3d("HACIENDA NAPOLES", 0.42, (0.6, -1.98, 3.82), (90, 0, 0), mat("gate_ink", "#7c2533", rough=0.5), font="display", extrude=0.02)
    area_light((-6, -7, 8), (0, 2, 1), 900, 6, "#fff0dc", "key")
    area_light((6, -5, 3), (0, 2, 1), 300, 5, "#dbe8ff", "fill")


def ranch_angles():
    build_ranch()
    drop_cams(); camera((0.6, -11.5, 2.6), (0.6, 3.0, 2.4), lens=24, fstop=6.0)
    still("plate_ranch_wide", 1080, 1920, 40)
    drop_cams(); camera((0.6, -4.2, 3.0), (0.6, 3.0, 0.6), lens=32, fstop=4.0)
    still("plate_ranch_mid", 1080, 1920, 40)


# ---------------------------------------------------------------- the river and the herd
def boat(x, y, yaw=0):
    wd = wood("#9a6a3c", "#6e4626", "boat_wood", 3.0)
    b = box((1.1, 3.4, 0.5), (0, 0, 0.18), material=wd, bevel=0.22)
    seat = box((1.0, 0.25, 0.08), (0, 0.4, 0.45), material=wd, bevel=0.02)
    oar = cylinder(0.04, 2.4, (0.65, -0.2, 0.55), (60, 0, 15), mat("oar", "#c9a46a", rough=0.6), verts=10)
    root = empty((0, 0, 0), "boat")
    for p in (b, seat, oar):
        p.parent = root
    root.rotation_euler = (0, 0, math.radians(yaw)); root.location = (x, y, 0.0)


def bank(x0, x1, y0, y1, seed=0, trees=10):
    random.seed(seed)
    box((x1 - x0, y1 - y0, 1.2), ((x0 + x1) / 2, (y0 + y1) / 2, 0.0), material=mat("bank_mud", "#7cae4f", rough=0.9, noise_bump=0.3), bevel=0.6)
    for k in range(trees):
        xx = random.uniform(x0 + 0.5, x1 - 0.5); yy = random.uniform(y0 + 0.5, y1 - 0.5)
        if random.random() < 0.5:
            palm(xx, yy, random.uniform(4.0, 6.0), seed * 50 + k)
        else:
            tree(xx, yy, random.uniform(3.6, 5.2), seed * 50 + k)


def build_river():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny("#2f7fd8", "#a9d8f5", 4.4)
    water(400, 400, 0.0, "#5b8f7c")
    # sandbank in the middle, jungle banks on both sides and far away
    sphere(1.0, (3.2, 6.0, -0.35), (5.0, 2.6, 0.6), mat("sand", "#d8c08a", rough=0.9, noise_bump=0.2), seg=48)
    bank(-40, -9, -10, 60, 1, 22)
    bank(10, 40, -10, 60, 2, 22)
    bank(-40, 40, 40, 70, 3, 40)
    bm = [mat(f"bush{k}", c, rough=0.75, noise_bump=0.25) for k, c in enumerate(("#3f8f45", "#4f9e4a", "#2f7a3c"))]
    random.seed(5)
    for k in range(70):
        yy = random.uniform(-6, 40); 
        for sx in (-9.3, 10.3):
            if k % 2 == 0:
                sphere(random.uniform(1.0, 1.9), (sx + random.uniform(-0.6, 0.6), yy, 0.4), (1, 1, 0.8), bm[k % 3], seg=20)
    for k in range(60):
        sphere(random.uniform(1.4, 2.4), (random.uniform(-30, 30), 40.5 + random.uniform(-0.8, 0.8), 0.6), (1, 1, 0.8), bm[k % 3], seg=20)
    random.seed(11)
    spots = []
    while len(spots) < 30:
        xx = random.uniform(-7.5, 8.5); yy = random.uniform(1.0, 30.0)
        if all((xx - a) ** 2 + (yy - b) ** 2 > 5.0 for a, b in spots) and not (abs(xx + 2.6) < 1.8 and yy < 4):
            spots.append((xx, yy))
    for k, (xx, yy) in enumerate(spots):
        on_sand = (xx - 3.2) ** 2 / 20 + (yy - 6.0) ** 2 / 5 < 1
        hippo(xx, yy, 0.0 if on_sand else random.uniform(-0.95, -0.6), random.uniform(-180, 180),
              random.uniform(0.75, 1.0), mouth=(k % 9 == 3), name=f"rh{k}")
    boat(-2.6, 1.5, 20)
    area_light((-6, -7, 8), (0, 6, 0), 900, 8, "#fff0dc", "key")
    area_light((6, -5, 3), (0, 6, 0), 300, 6, "#dbe8ff", "fill")


def river_angles():
    build_river()
    drop_cams(); camera((0.0, -9.5, 7.0), (0.6, 12.0, 0.6), lens=24, fstop=8.0)
    still("plate_river_wide", 1080, 1920, 40)
    drop_cams(); camera((-3.6, -3.2, 1.3), (-0.4, 4.0, 0.4), lens=28, fstop=3.0)
    still("plate_river_close", 1080, 1920, 40)


if not os.environ.get("BK_PROPS_ONLY"):
    ranch_angles()
    river_angles()
reset(600, 600, 30, 0.1, samples=32, transparent=True, bloom=0)
sunny()
area_light((-4, -5, 6), (0, 0, 1), 700, 4, "#fff0dc", "key")
hippo(0, 0, 0, -35, 1.0, name="hp")
camera((0.0, -8.0, 2.6), (0.0, 0.0, 0.95), lens=50, fstop=0)
still("hippo", 700, 600, 32, transparent=True, crop=True)
