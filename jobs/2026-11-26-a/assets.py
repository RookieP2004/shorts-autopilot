# 2026-11-26-a: "Turkeys can't fly? Wild ones hit 55 mph" (myth-bust, Ved as a coach at half-time on Thanksgiving).
# Set: Coach Ved's locker room. Teal lockers, a wooden bench with a football and towels, an orange water cooler, and a
# green tactics board covered in X's, O's and arrows (our own drawing) where the coach settles the debate. Plates:
# locker_wide (Ved by the board, two players by the bench), locker_board (closer on the board), locker_low (low hero angle).
# Cut-outs: the wild turkey (wings up), the farm turkey (standing), a coach's whistle.
import math, os, random
from PIL import Image as PI, ImageDraw as PD

A = ASSETS
exec(open(os.path.join(ROOT, "jobs/2026-11-26-a/shots/turkeykit.py")).read())


def board_tex(path):
    W_, H_ = 1400, 900
    im = PI.new("RGB", (W_, H_), (38, 74, 58))
    d = PD.Draw(im)
    rnd = random.Random(3)
    for k in range(40):                                          # chalk dust smears
        x, y = rnd.randint(0, W_), rnd.randint(0, H_)
        d.ellipse([x, y, x + rnd.randint(80, 260), y + rnd.randint(20, 60)], fill=(48, 86, 68))
    ch = (236, 238, 228)
    for (x, y) in ((260, 300), (420, 520), (300, 700), (620, 380)):
        d.ellipse([x - 40, y - 40, x + 40, y + 40], outline=ch, width=9)
    for (x, y) in ((900, 260), (1080, 450), (950, 660), (1180, 720)):
        d.line([(x - 38, y - 38), (x + 38, y + 38)], fill=ch, width=10)
        d.line([(x - 38, y + 38), (x + 38, y - 38)], fill=ch, width=10)
    for (a, b) in (((300, 300), (840, 250)), ((460, 520), (1020, 470)), ((340, 700), (900, 660))):
        d.line([a, b], fill=(242, 200, 90), width=8)
        bx, by = b
        d.polygon([(bx, by), (bx - 34, by - 18), (bx - 30, by + 22)], fill=(242, 200, 90))
    d.rectangle([20, 20, W_ - 20, H_ - 20], outline=(170, 120, 70), width=26)
    im.save(path)
    return path


BOARD = board_tex(os.path.join(A, "tex_board.png"))


def locker_room():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15, exposure=-0.2)
    world_hdri("lounge", 0.3, backdrop=(0.85, 0.85, 0.82))
    tiles = mat("floor_t", "#9aa6b2", rough=0.35, coat=0.3)
    plane(30, 30, (0, 0, 0), material=tiles, name="floor")
    for k in range(-14, 15):                                     # tile grout lines
        plane(0.015, 30, (k * 0.6, 0, 0.002), material=mat("grout", "#7d8894", rough=0.6), name=f"g{k}")
    box((14, 0.2, 8), (0, 3.1, 4.0), material=mat("wall_c", "#f2e6cf", rough=0.85), bevel=0)
    box((14, 0.06, 1.0), (0, 2.98, 0.5), material=mat("wall_stripe", "#d6483e", rough=0.7), bevel=0)
    box((0.2, 8, 8), (-4.8, -1.0, 4.0), material=mat("wall_side", "#e9dcc2", rough=0.85), bevel=0)
    # tactics board
    o = plane(2.0, 1.3, (-1.35, 2.97, 1.85), (90, 0, 0), material=mat("board", "#ffffff", rough=0.8, image=BOARD), name="board")
    if not o.data.uv_layers:
        o.data.uv_layers.new()
    box((2.1, 0.08, 0.06), (-1.35, 2.93, 1.17), material=wood("#a8743f", "#7a4e2a", "ledge", 6.0, 0.5), bevel=0.01)
    # lockers
    teal = mat("locker", "#3f8f8a", rough=0.35, metal=0.4)
    vent = mat("vent", "#2a5f5b", rough=0.5)
    handle = mat("handle", "#d9d9d9", rough=0.2, metal=1.0)
    for k in range(6):
        x = 0.45 + k * 0.62
        box((0.58, 0.5, 2.0), (x, 2.75, 1.0), material=teal, bevel=0.01, name=f"lk{k}")
        for v in range(4):
            box((0.32, 0.02, 0.025), (x, 2.495, 1.72 - v * 0.06), material=vent, bevel=0)
        box((0.03, 0.03, 0.14), (x + 0.2, 2.49, 1.05), material=handle, bevel=0.005)
        box((0.18, 0.015, 0.1), (x, 2.495, 1.45), material=mat("numplate", "#f6efe2", rough=0.6), bevel=0)
    # jerseys hanging in two lockers
    for k, c in ((1, "#d6483e"), (4, "#f2b04a")):
        box((0.42, 0.06, 0.55), (0.45 + k * 0.62, 2.46, 1.25), material=mat(f"jer{k}", c, rough=0.9), bevel=0.04)
    # bench
    bw = wood("#c9945c", "#a0703f", "bench", 6.0, 0.5)
    box((3.0, 0.42, 0.06), (1.95, 1.75, 0.46), material=bw, bevel=0.01, name="bench")
    for sx in (0.6, 3.3):
        box((0.06, 0.36, 0.44), (sx, 1.75, 0.22), material=mat("bleg", "#3a3d45", rough=0.4), bevel=0.005)
    # football + towels + helmet-free props
    fb = sphere(0.14, (1.2, 1.72, 0.58), (1.6, 1.0, 1.0), mat("ball", "#7a3e22", rough=0.55), seg=32, name="football")
    fb.rotation_euler = (0, 0, math.radians(20))
    box((0.1, 0.01, 0.01), (1.2, 1.6, 0.715), (0, 0, 20), mat("lace", "#f6efe2", rough=0.6), bevel=0)
    for k, c in ((0, "#f6efe2"), (1, "#8fbce0")):
        box((0.45, 0.32, 0.07), (2.3 + k * 0.55, 1.72, 0.53), material=mat(f"towel{k}", c, rough=0.95), bevel=0.03)
    # water cooler
    cylinder(0.22, 0.55, (3.6, 2.3, 0.6), material=mat("cooler", "#f28c28", rough=0.4), verts=32, bevel=0.02)
    cylinder(0.23, 0.08, (3.6, 2.3, 0.92), material=mat("cooler_lid", "#f6efe2", rough=0.4), verts=32, bevel=0.02)
    box((0.5, 0.4, 0.33), (3.6, 2.3, 0.165), material=mat("crate", "#3a3d45", rough=0.6), bevel=0.01)
    # ceiling lights glow strip feel
    area_light((-3.0, -3.0, 4.0), (0, 2, 1), 900, 5, "#fff0dc", "key")
    area_light((3.5, -2.5, 2.5), (0, 2, 1), 300, 5, "#dbe8ff", "fill")
    area_light((-1.35, 1.6, 3.2), (-1.35, 2.9, 1.8), 160, 1.2, "#ffe9c2", "board_spot")


def drop_cams():
    for o in list(bpy.data.objects):
        if o.type == "CAMERA" or o.name.startswith("cam_target"):
            bpy.data.objects.remove(o)


locker_room()
camera((0.3, -3.0, 1.5), (0.3, 2.2, 1.3), lens=24, fstop=8.0)
still("plate_locker_wide", 1080, 1920, 40)
drop_cams(); camera((-0.6, -0.9, 1.55), (-1.25, 2.9, 1.6), lens=30, fstop=5.0)
still("plate_locker_board", 1080, 1920, 40)
drop_cams(); cam, _ = camera((1.8, -1.6, 0.5), (0.2, 2.2, 1.35), lens=24, fstop=5.0)
dutch(cam, -4)
still("plate_locker_low", 1080, 1920, 40)

# cut-outs
reset(800, 800, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.5, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0.5), 600, 3, "#fff0dc", "k")
area_light((2.5, 2.5, 2), (0, 0, 0.5), 300, 2, "#dbe8ff", "r")
r, pv = turkey(1.0, True, "wild", legs_tucked=True)
for p, sd in pv:
    p.rotation_euler = (math.radians(45 * sd), 0, 0)
r.rotation_euler = (0, math.radians(-12), 0)
camera((1.2, -3.4, 1.4), (0.0, 0, 0.6), lens=40, fstop=0)
still("wild_turkey", 800, 800, 40, transparent=True, crop=True)

reset(800, 800, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.5, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0.5), 600, 3, "#fff0dc", "k")
area_light((2.5, 2.5, 2), (0, 0, 0.5), 300, 2, "#dbe8ff", "r")
r, pv = turkey(1.0, False, "farm")
folded(r, pv, 0)
bpy.context.scene.frame_set(1)
camera((1.4, -3.4, 1.0), (0.0, 0, 0.5), lens=40, fstop=0)
still("farm_turkey", 800, 800, 40, transparent=True, crop=True)

reset(600, 600, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.6, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0), 500, 3, "#fff0dc", "k")
sil = metal("#d9dde3", 0.15, "whistle_m")
cylinder(0.22, 0.3, (0, 0, 0), (90, 0, 0), sil, verts=48, bevel=0.02, name="w1")
box((0.42, 0.3, 0.16), (0.3, 0, 0.1), material=sil, bevel=0.04, name="w2")
torus(0.12, 0.025, (-0.28, 0, 0.12), (90, 0, 0), sil, name="ring")
cord = torus(0.45, 0.02, (-0.75, 0, -0.15), (90, 0, 20), mat("cord", "#d6483e", rough=0.6), name="cord")
camera((0.3, -2.6, 1.0), (0, 0, 0), lens=50, fstop=0)
still("whistle", 600, 600, 40, transparent=True, crop=True)
