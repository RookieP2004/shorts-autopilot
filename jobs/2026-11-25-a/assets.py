# 2026-11-25-a: "Skyscrapers stand still? This one hides a 660-ton ball" (myth-bust, Ved as an enthusiast).
# Set: Ved's model room. A big work table with his pride and joy, a 1.6 m model of a tiered tower whose top sections are
# clear so a little gold damper ball shows inside; other skyscraper models; blueprint posters (fictional drawings) on a
# blue wall; a shelf of more models; a window with sky; a desk lamp. Plates: room_wide (Ved stands left of the table),
# room_model (close on the model's clear top + ball), room_low (low hero angle across the table).
# Cut-outs: the gold damper ball (hero prop), a small model tower.
import math, os, random
from PIL import Image as PI, ImageDraw as PD, ImageFont as PF

A = ASSETS
exec(open(os.path.join(ROOT, "jobs/2026-11-25-a/shots/towerkit.py")).read())


def blueprint_tex(path, seed=1, kind="tower"):
    W_, H_ = 900, 1300
    im = PI.new("RGB", (W_, H_), (28, 74, 140))
    d = PD.Draw(im)
    for x in range(0, W_, 45):
        d.line([(x, 0), (x, H_)], fill=(52, 100, 170), width=1)
    for y in range(0, H_, 45):
        d.line([(0, y), (W_, y)], fill=(52, 100, 170), width=1)
    wl = (225, 238, 255)
    cx = W_ // 2
    if kind == "tower":
        y = 1180
        d.rectangle([cx - 170, y - 60, cx + 170, y], outline=wl, width=5)
        y -= 60
        d.polygon([(cx - 120, y), (cx + 120, y), (cx + 90, y - 230), (cx - 90, y - 230)], outline=wl, width=5)
        y -= 230
        for k in range(8):
            d.polygon([(cx - 80, y), (cx + 80, y), (cx + 105, y - 88), (cx - 105, y - 88)], outline=wl, width=4)
            y -= 92
        d.polygon([(cx - 60, y), (cx + 60, y), (cx + 40, y - 60), (cx - 40, y - 60)], outline=wl, width=4)
        d.line([(cx, y - 60), (cx, y - 160)], fill=wl, width=4)
        d.ellipse([cx - 34, 270, cx + 34, 338], outline=(255, 210, 90), width=5)
        d.line([(cx + 40, 304), (cx + 260, 250)], fill=wl, width=3)
        d.text((cx + 200, 220), "TMD", fill=wl)
    else:
        rnd = random.Random(seed)
        for k in range(9):
            x0 = rnd.randint(60, 700); y0 = rnd.randint(80, 1100)
            d.rectangle([x0, y0, x0 + rnd.randint(80, 200), y0 + rnd.randint(60, 180)], outline=wl, width=3)
        d.ellipse([cx - 160, 400, cx + 160, 720], outline=wl, width=5)
        d.line([(cx, 120), (cx, 560)], fill=wl, width=4)
    d.rectangle([W_ - 330, H_ - 120, W_ - 30, H_ - 30], outline=wl, width=4)
    d.text((W_ - 310, H_ - 100), "DRAWN BY: VED", fill=wl)
    im.save(path)
    return path


BP1 = blueprint_tex(os.path.join(A, "tex_bp1.png"), 1, "tower")
BP2 = blueprint_tex(os.path.join(A, "tex_bp2.png"), 2, "parts")


def poster(img, loc, w, h, rot_z=0, name="poster"):
    o = plane(w, h, loc, (90, 0, rot_z), material=mat(name + "_m", "#ffffff", rough=0.7, image=img), name=name)
    me = o.data
    if not me.uv_layers:
        me.uv_layers.new()
    return o


def room():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15, exposure=-0.3)
    world_hdri("lounge", 0.35, backdrop=(0.9, 0.86, 0.78))
    plane(30, 30, (0, 0, 0), material=wood("#c9945c", "#a0703f", "floor_wood", 10.0, 0.55), name="floor")
    box((14, 0.2, 8), (0, 3.0, 4.0), material=mat("wall_blue", "#8fbce0", rough=0.85), bevel=0)
    box((14, 0.08, 0.18), (0, 2.88, 0.09), material=mat("skirting", "#f6efe2", rough=0.5), bevel=0.01)
    lathe([(0, 0), (1.6, 0), (1.6, 0.012), (0, 0.012)], 64, (0.0, 0.6, 0.0), mat("rug", "#d6483e", rough=0.95), subdiv=0, name="rug")
    lathe([(0, 0), (1.25, 0), (1.25, 0.016), (0, 0.016)], 64, (0.0, 0.6, 0.0), mat("rug2", "#f2b04a", rough=0.95), subdiv=0, name="rug2")
    box((0.2, 8, 8), (-4.6, -1.0, 4.0), material=mat("wall_side", "#7fb0d6", rough=0.85), bevel=0)
    # posters (blueprints) and a window
    poster(BP1, (-1.9, 2.88, 2.25), 0.9, 1.3, name="bp1")
    poster(BP2, (2.3, 2.88, 2.3), 0.8, 1.15, name="bp2")
    box((1.2, 0.06, 1.5), (0.35, 2.92, 2.55), material=mat("win_frame", "#f6efe2", rough=0.5), bevel=0.02)
    plane(1.05, 1.35, (0.35, 2.88, 2.55), (90, 0, 0), material=glow("#bfe2fb", 2.0, "sky_win"))
    # work table
    top = wood("#a8743f", "#7a4e2a", "table_top", 6.0, 0.4)
    box((2.8, 1.1, 0.07), (0.3, 1.9, 0.82), material=top, bevel=0.012, name="table")
    for sx in (-1.0, 1.6):
        for sy in (1.45, 2.35):
            box((0.07, 0.07, 0.8), (sx, sy, 0.4), material=mat("leg", "#3a3d45", rough=0.4), bevel=0.005)
    # the star model: tiered tower with a clear top and a tiny gold ball inside
    pv, ztop = tower(0.15, xray_top=True, name="mdl")
    pv.location = (0.35, 1.95, 0.855)
    sp, ball = damper((0.35, 1.95, 0.855 + 7.7 * 0.15), 0.42 * 0.15, 0.5 * 0.15, "mtmd")
    # other models
    glassB = mat("mglass2", "#5b8fc9", rough=0.15, metal=0.3, coat=0.6)
    box((0.22, 0.22, 0.95), (1.25, 2.05, 0.855 + 0.475), material=glassB, bevel=0.01, name="m2")
    box((0.16, 0.16, 0.6), (1.5, 1.75, 0.855 + 0.3), material=mat("mglass3", "#e8a87c", rough=0.3), bevel=0.01, name="m3")
    lathe([(0.0, 0.0), (0.12, 0.0), (0.1, 0.7), (0.05, 0.85), (0.0, 0.88)], 32, (-0.55, 2.05, 0.855),
          mat("mglass4", "#bfe3d6", rough=0.15, metal=0.3, coat=0.5), name="m4")
    box((0.5, 0.35, 0.04), (-0.35, 1.6, 0.875), material=mat("cutmat", "#46965a", rough=0.6), bevel=0.004)
    # a desk lamp
    cylinder(0.08, 0.02, (-0.9, 1.65, 0.865), material=mat("lampb", "#d6483e", rough=0.3), verts=24)
    cylinder(0.012, 0.5, (-0.9, 1.65, 1.1), material=mat("lampb", "#d6483e", rough=0.3), verts=12, bevel=0)
    lathe([(0.0, 0.0), (0.11, 0.0), (0.06, 0.1), (0.0, 0.11)], 32, (-0.9, 1.65, 1.3), mat("lamps", "#d6483e", rough=0.3), name="lamph")
    # shelf with mini models
    shelf = wood("#a8743f", "#7a4e2a", "shelf", 6.0, 0.4)
    box((1.6, 0.3, 0.04), (-2.9, 2.75, 1.55), material=shelf, bevel=0.01)
    rnd = random.Random(5)
    for k in range(6):
        h = rnd.uniform(0.18, 0.42)
        box((0.1, 0.1, h), (-3.5 + k * 0.24, 2.75, 1.57 + h / 2), material=mat(f"mini{k % 3}", ["#5b8fc9", "#e8a87c", "#3f8f8a"][k % 3], rough=0.3), bevel=0.006)
    # a plant
    lathe([(0, 0), (0.12, 0), (0.15, 0.25), (0.0, 0.25)], 32, (3.0, 2.4, 0.0), mat("pot", "#b5533c", rough=0.6), name="pot")
    for k in range(9):
        a = k / 9 * 2 * math.pi
        lf = sphere(0.2, (3.0 + math.cos(a) * 0.12, 2.4 + math.sin(a) * 0.12, 0.45 + rnd.uniform(0, 0.25)), (0.45, 0.16, 1.0),
                    plastic("#3f9a4a", 0.5, "leaf"))
        lf.rotation_euler = (math.radians(rnd.uniform(-25, 25)), math.radians(rnd.uniform(-30, 30)), a)
    area_light((-3.5, -3.5, 4.0), (0.3, 2, 1.2), 900, 5, "#fff0dc", "key")
    area_light((3.5, -3.0, 2.2), (0.3, 2, 1.2), 280, 5, "#dbe8ff", "fill")
    area_light((0.35, 1.4, 2.6), (0.35, 1.95, 1.8), 120, 1.0, "#ffe9c2", "model_spot")


def drop_cams():
    for o in list(bpy.data.objects):
        if o.type == "CAMERA" or o.name.startswith("cam_target"):
            bpy.data.objects.remove(o)


room()
camera((0.1, -2.7, 1.5), (0.1, 2.2, 1.4), lens=24, fstop=8.0)
still("plate_room_wide", 1080, 1920, 40)
drop_cams(); camera((0.62, 1.05, 2.05), (0.35, 1.95, 1.95), lens=40, fstop=2.6)
still("plate_room_model", 1080, 1920, 40)
drop_cams(); cam, _ = camera((-1.4, -1.3, 0.55), (0.3, 1.9, 1.35), lens=26, fstop=4.0)
dutch(cam, 4)
still("plate_room_low", 1080, 1920, 40)

# cut-outs
reset(800, 800, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.5, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0), 600, 3, "#fff0dc", "k")
area_light((2.5, 1.5, 1.5), (0, 0, 0), 300, 2, "#dbe8ff", "r")
sp, ball = damper((0, 0, 0), 0.5, 0.7, "hero")
for o in list(bpy.data.objects):
    if o.name.startswith("hero_deck"):
        bpy.data.objects.remove(o)
camera((0.4, -3.2, 0.3), (0, 0, 0.35), lens=50, fstop=0)
still("ball", 800, 800, 40, transparent=True, crop=True)
