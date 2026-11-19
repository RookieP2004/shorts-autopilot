# 2026-11-19-a: "A year isn't 365 days" (big-question: why do we have leap years?).
# Sets: the sunny clock-tower town square (2026-11-14-c helpers) re-dressed: no coin jar; instead a giant wooden wall
# calendar on two posts showing FEBRUARY with the 29th circled in red; 3 angles (wide, mid on the calendar, up at the clock).
# Space: a glowing Sun, Earth's orbit as a thin glowing ring, a gold START line, Earth stopped just short of it
# (365 days done, ~6 hours of orbit still to go); 2 angles (high wide, low close on Earth and the gap).
# Cut-out: a small Earth.
import math, os, random

# small_earth_mat(), prop_space(), drop_cams() ... (frozen 2026-11-15-c helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-15-c/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "c15_helpers", "exec"), globals())
# sunny(), house(), tree(), bunting(), clock_tower() ... (frozen 2026-11-14-c helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-14-c/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "c14_helpers", "exec"), globals())


def calendar_texture(path):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1400, 1100
    im = Image.new("RGB", (W, H), (246, 239, 226))
    d = ImageDraw.Draw(im)
    fa = ImageFont.truetype(os.path.join(ROOT, "fonts/Anton-Regular.ttf"), 170)
    fn = ImageFont.truetype(os.path.join(ROOT, "fonts/Anton-Regular.ttf"), 78)
    d.rectangle((0, 0, W, 250), fill=(217, 83, 79))
    d.text((W / 2, 125), "FEBRUARY", fill=(246, 239, 226), font=fa, anchor="mm")
    x0, y0, cw, ch = 60, 290, (W - 120) / 7, 155
    for k in range(29):
        c, r = k % 7, k // 7
        cx, cy = x0 + c * cw + cw / 2, y0 + r * ch + ch / 2
        d.rectangle((x0 + c * cw + 6, y0 + r * ch + 6, x0 + (c + 1) * cw - 6, y0 + (r + 1) * ch - 6), outline=(200, 186, 160), width=4)
        d.text((cx, cy), str(k + 1), fill=(26, 20, 16) if k < 28 else (217, 83, 79), font=fn, anchor="mm")
        if k == 28:
            for w in range(10):
                d.ellipse((cx - 78 - w, cy - 66 - w, cx + 78 + w, cy + 66 + w), outline=(217, 83, 79))
    im.save(path)
    return path


def wall_calendar(x, y):
    tex = calendar_texture(os.path.join(ASSETS, "_cal_tex.png"))
    wd = wood("#8a4f2c", "#5e321a", "cal_wood", 3.0)
    for sx in (-1.75, 1.75):
        cylinder(0.12, 4.6, (x + sx, y + 0.05, 2.3), material=wd, verts=20)
    box((3.9, 0.18, 3.1), (x, y, 3.0), material=wd, bevel=0.05)
    face = mat("cal_face", "#ffffff", rough=0.5, image=tex)
    plane(3.6, 2.83, (x, y - 0.1, 3.0), (90, 0, 0), material=face, name="cal_face")
    box((4.2, 0.5, 0.18), (x, y, 4.62), material=mat("cal_roof", "#34425c", rough=0.5), bevel=0.04)
    # two rings at the top, like a flip calendar
    for sx in (-0.9, 0.9):
        torus(0.16, 0.04, (x + sx, y - 0.12, 4.5), (0, 90, 0), metal("#c9a24a", 0.25, "cal_ring"))


def build_plaza():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0)
    sunny("#2f8fe0", "#cfe8fb", 4.6)
    plane(400, 400, (0, 0, 0), material=mat("cobbles", "#d8c19a", rough=0.9, noise_bump=0.3), name="cobbles")
    cylinder(2.4, 0.04, (0.6, 0.2, 0.02), material=mat("plaza_ring", "#c9b08a", rough=0.85), verts=64, bevel=0)
    wall_calendar(1.4, 1.6)
    clock_tower(-2.2, 5.5, 1.0)
    house(3.6, 6.2, 4.0, 4.6, "#f2c88a", "#b5533c", 1)
    house(-7.6, 7.2, 4.4, 5.6, "#e8a39a", "#7c2533", 2)
    house(8.4, 8.0, 4.0, 4.2, "#a8d5d1", "#34425c", 3)
    house(-12, 10, 4.2, 5.0, "#d9c6ea", "#6b4c8a", 4)
    house(12.5, 11, 4.5, 5.0, "#f6e3a8", "#b5533c", 5)
    tree(-5.0, 3.2, 3.4, 1); tree(5.4, 3.6, 3.0, 2); tree(-9.6, 4.6, 3.6, 3); tree(9.8, 5.0, 3.4, 4)
    bunting(-4.6, 2.0, 2.8, 4.2)
    area_light((-5, -6, 7), (0, 1, 1.5), 900, 6, "#fff0dc", "key")
    area_light((5, -4, 3), (0, 1, 1.5), 300, 5, "#dbe8ff", "fill")


def plaza_angles():
    build_plaza()
    for name, loc, tgt, lens, fs in (("plaza_wide", (0.0, -10.5, 2.4), (-0.2, 2.0, 3.4), 24, 6.0),
                                     ("plaza_mid", (0.2, -5.6, 1.8), (1.2, 1.6, 2.6), 28, 4.0)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)
    drop_cams(); camera((-1.2, -2.2, 1.4), (-2.2, 4.25, 7.4), lens=26, fstop=0)
    still("plate_clock_up", 1080, 1920, 40)


# ---------------------------------------------------------------- space: the orbit and the gap
R = 7.0
GAP = 14.0   # degrees short of the line (exaggerated so the gap reads)


def build_orbit():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.55)
    world_color(hexrgb("#03050c"), 1.0)
    random.seed(31)
    sm = mat("sstar", "#ffffff", emit="#ffffff", emit_strength=8.0)
    for k in range(700):
        a = random.uniform(0, 2 * math.pi); b = random.uniform(-1.4, 1.4); Rs = 420
        sphere(random.uniform(0.3, 0.9), (Rs * math.cos(a) * math.cos(b), Rs * math.sin(a) * math.cos(b), Rs * math.sin(b)), 1, sm, seg=6)
    sun = sphere(1.6, (0, 0, 0), 1, mat("sunm", "#ffd27a", emit="#ff9a2a", emit_strength=3.0), seg=96, name="sun")
    sun.visible_shadow = False
    P = bpy.data.lights.new("sunlight", "POINT"); P.energy = 26000; P.color = hexrgb("#fff1dc"); P.shadow_soft_size = 1.6
    o = bpy.data.objects.new("sunlight", P); bpy.context.scene.collection.objects.link(o)
    # the orbit ring
    torus(R, 0.035, (0, 0, 0), (0, 0, 0), mat("orbit", "#8fd3ff", emit="#6fc3ff", emit_strength=1.5))
    # START / 1 YEAR line: a gold bar across the ring at angle -90 (towards the camera)
    a0 = math.radians(-90)
    box((0.06, 1.3, 0.06), (R * math.cos(a0), R * math.sin(a0), 0), (0, 0, 0),
        mat("startline", "#ffd23a", emit="#ffb020", emit_strength=1.8), bevel=0.01)
    # Earth stopped short of the line (it moves anticlockwise seen from above)
    ae = a0 - math.radians(GAP)
    e = sphere(0.42, (R * math.cos(ae), R * math.sin(ae), 0), 1, small_earth_mat("searth_o"), seg=96, name="earth")
    e.rotation_euler = (math.radians(-23), 0, 0)
    # the leftover arc in gold (the missing ~6 hours)
    for k in range(12):
        a = ae + (a0 - ae) * (k + 0.5) / 12
        sphere(0.06, (R * math.cos(a), R * math.sin(a), 0), 1, mat("gapdot", "#ffd23a", emit="#ffb020", emit_strength=1.5), seg=12)
    area_light((-6, -12, 6), (0, -6, 0), 300, 6, "#8fb9ff", "fill")


def orbit_angles():
    build_orbit()
    drop_cams(); camera((0.0, -15.0, 11.5), (0.0, -1.8, 0.0), lens=26, fstop=0)
    still("plate_orbit_wide", 1080, 1920, 40)
    a0 = math.radians(-90); ae = a0 - math.radians(GAP / 2)
    tx, ty = R * math.cos(ae), R * math.sin(ae)
    drop_cams(); camera((tx - 0.6, ty - 4.2, 1.5), (tx, ty, 0.0), lens=30, fstop=0)
    still("plate_orbit_close", 1080, 1920, 40)


if not os.environ.get("BK_PROPS_ONLY"):
    plaza_angles()
    orbit_angles()
prop_space(); s = sphere(0.5, (0, 0, 0.5), 1, small_earth_mat("searth_p"), seg=96); s.rotation_euler = (math.radians(-23), 0, 0)
camera((0.0, -3.4, 0.5), (0, 0, 0.5), lens=55, fstop=0)
still("earth", 600, 600, 32, transparent=True, crop=True)
