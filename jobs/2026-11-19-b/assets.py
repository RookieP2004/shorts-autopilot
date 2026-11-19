# 2026-11-19-b: "Cracking your knuckles = arthritis? One doctor tested it for 60 years" (myth-bust).
# Sets: a sunny California doctor's clinic (the 2026-11-14-b lab re-dressed: peach walls, teal wainscot, a glowing X-ray
# lightbox on the wall showing two hand X-rays marked L and R, a 1998 wall calendar, a "CLINIC" sign, palm in the window),
# 2 new angles (wide from the right, mid on the lightbox); inside a knuckle: a glossy teal studio with a finger joint
# (rounded bone head + cartilage cap meeting the next bone, inside a translucent capsule of joint fluid), once closed and
# once pulled apart with a bright gas bubble popping open in the gap (same camera).
# Cut-outs: a gold trophy cup (fictional design), a glass of fizzy water (the bubble analogy).
import math, os, random

# build_lab(), island(), petri(), beaker(), tube(), drop_cams() + 2026-11-08-c helpers (frozen)
_src = open(os.path.join(ROOT, "jobs/2026-11-14-b/assets.py")).read().split("\n# ---------------------------------------------------------------- the stomach interior")[0]
exec(compile(_src, "b14_helpers", "exec"), globals())


def recolor(name, hexc):
    m = bpy.data.materials.get(name)
    if m:
        m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*hexrgb(hexc), 1)


def xray_texture(path):
    """Two hand X-rays side by side (L and R) on blue-black film, drawn with PIL (fictional, simplified)."""
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 1200, 800
    im = Image.new("RGB", (W, H), (18, 34, 58))
    d = ImageDraw.Draw(im)
    for hx, lab in ((300, "L"), (900, "R")):
        mirror = -1 if lab == "L" else 1
        # palm glow
        d.ellipse((hx - 170, 420, hx + 170, 760), fill=(40, 70, 104))
        # four fingers: metacarpal + 3 phalanges, small gaps = joints
        for k, fx in enumerate((-105, -35, 35, 105)):
            x = hx + fx
            top = 120 + (abs(fx) // 3) + (k == 0) * 30
            segs = [(560, 720, 22), (420, 548, 19), (320, 410, 16), (top, 312, 13)]
            for y0, y1, r in segs:
                d.rounded_rectangle((x - r, y0, x + r, y1), r, fill=(214, 228, 240))
            for y in (550, 414, 315):
                d.ellipse((x - 12, y - 6, x + 12, y + 6), fill=(110, 150, 190))
        # thumb
        tx = hx + mirror * 190
        d.rounded_rectangle((tx - 20, 540, tx + 20, 690), 20, fill=(214, 228, 240))
        d.rounded_rectangle((tx + mirror * 30 - 17, 420, tx + mirror * 30 + 17, 530), 17, fill=(214, 228, 240))
        d.rounded_rectangle((tx + mirror * 50 - 14, 330, tx + mirror * 50 + 14, 412), 14, fill=(214, 228, 240))
        d.rectangle((hx - 6, 30, hx + 6, 30), fill=(0, 0, 0))
        d.text((hx - 12, 30), lab, fill=(246, 239, 226))
    im = im.filter(ImageFilter.GaussianBlur(2.2))
    d = ImageDraw.Draw(im)
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(os.path.join(ROOT, "fonts/Anton-Regular.ttf"), 90)
        for hx, lab in ((300, "L"), (900, "R")):
            d.text((hx - 24, 20), lab, fill=(246, 239, 226), font=f)
    except Exception:
        pass
    im.save(path)
    return path


def build_clinic():
    build_lab()
    recolor("lab_wall", "#f3cfa8"); recolor("lab_wall_l", "#e9bf94"); recolor("lab_wains", "#3d7f7c")
    recolor("bench_top", "#f6efe2"); recolor("cal_top", "#3f7fbf"); recolor("island_body", "#d9534f"); recolor("drawer", "#e2665f")
    for o in list(bpy.data.objects):
        if o.type == "FONT":
            if o.data.body == "1984":
                o.data.body = "1998"
            elif o.data.body == "RESEARCH":
                o.data.body = "CLINIC"
        if o.data and getattr(o.data, "materials", None) and any(m and m.name.startswith("poster") for m in o.data.materials):
            bpy.data.objects.remove(o)
    # the X-ray lightbox where the poster was: a cream frame + a glowing film
    tex = xray_texture(os.path.join(ASSETS, "_xray_tex.png"))
    box((2.5, 0.08, 1.62), (-1.45, 4.44, 2.65), material=mat("lb_frame", "#f6efe2", rough=0.35, coat=0.4), bevel=0.03)
    film = mat("lb_film", "#ffffff", rough=0.4, image=tex)
    nt = film.node_tree; p = nt.nodes.get("Principled BSDF")
    t = [n for n in nt.nodes if n.type == "TEX_IMAGE"][0]
    nt.links.new(t.outputs["Color"], p.inputs["Emission Color"]); p.inputs["Emission Strength"].default_value = 1.6
    pl = plane(2.36, 1.5, (-1.45, 4.39, 2.65), (90, 0, 0), material=film, name="xray_film")
    box((14, 12, 0.14), (0, -1.5, 4.85), material=mat("ceiling", "#f6eadb", rough=0.9), bevel=0.0, name="ceiling")
    area_light((-1.45, 3.4, 2.75), (-1.45, 0, 2.6), 60, 1.5, "#cfe6ff", "lb_glow")


def clinic_angles():
    build_clinic()
    for name, loc, tgt, lens, fs in (("clinic_wide", (2.4, -6.4, 1.6), (-0.9, 2.5, 1.8), 22, 6.0),
                                     ("clinic_mid", (-0.9, -3.6, 1.5), (-1.45, 3.0, 2.2), 28, 3.5)):
        drop_cams(); camera(loc, tgt, lens=lens, fstop=fs)
        still("plate_" + name, 1080, 1920, 40)


# ---------------------------------------------------------------- inside the knuckle
def joint_set(pulled=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    world_color(hexrgb("#123c44"), 0.8)
    floor("#174a52", rough=0.4, size=40)
    box((30, 0.3, 14), (0, 6.5, 6.5), material=mat("backdrop", "#1f6670", rough=0.6, emit="#2a7f88", emit_strength=0.35), bevel=0)
    bone = mat("bone", "#efe4cf", rough=0.35, coat=0.4, sss=0.1)
    cart = mat("cartilage", "#dff2f6", rough=0.12, coat=0.9, sss=0.25)
    zc = 1.25
    gap = 0.9 if pulled else 0.0
    # the hand bone (metacarpal) from the left: shaft + a big rounded head capped with cartilage
    cylinder(0.42, 4.6, (-3.1, 0, zc), (0, 90, 0), bone, verts=48, bevel=0.05)
    sphere(0.66, (-0.62, 0, zc), (1.0, 1.0, 1.0), cart, seg=64)
    sphere(0.6, (-0.78, 0, zc), (1.0, 1.0, 1.0), bone, seg=48)
    # the finger bone (phalanx) from the right: a flared, slightly cupped base with a cartilage rim
    x0 = 0.12 + gap
    lathe([(0.0, 0.0), (0.5, 0.0), (0.62, 0.06), (0.64, 0.22), (0.5, 0.42), (0.38, 0.62), (0.36, 4.4), (0.0, 4.4)], 48,
          (x0, 0, zc), bone, 1, "phalanx").rotation_euler = (0, math.radians(90), 0)
    o = cylinder(0.6, 0.1, (x0 + 0.03, 0, zc), (0, 90, 0), cart, verts=48, bevel=0.04)
    o.scale = (1, 1, 1)
    # the joint capsule (a translucent sleeve) and the joint fluid inside
    span = 2.6 + gap
    cx = -0.25 + gap / 2
    fluid = mat("fluid", "#fbf3cc", rough=0.05, coat=1.0, alpha=0.14, sss=0.1)
    caps = mat("capsule", "#bfe8ee", rough=0.1, coat=0.9, alpha=0.13)
    o = cylinder(0.92, span * 0.82, (cx, 0, zc), (0, 90, 0), fluid, verts=48, bevel=0.2)
    o = cylinder(1.02, span, (cx, 0, zc), (0, 90, 0), caps, verts=48, bevel=0.25)
    if pulled:
        # the cavity: a bright gas bubble that opened in the gap, with a few tiny satellite bubbles
        bub = mat("gas", "#e9fbff", rough=0.02, coat=1.0, emit="#bff4ff", emit_strength=3.5, alpha=0.95)
        sphere(0.44, (0.07 + gap / 2, -0.05, zc + 0.02), (0.9, 1.0, 1.15), bub, seg=48)
        for (dx, dz, r) in ((-0.3, 0.42, 0.07), (0.35, -0.38, 0.06), (0.25, 0.5, 0.05), (-0.22, -0.45, 0.05)):
            sphere(r, (0.07 + gap / 2 + dx, -0.15, zc + dz), 1, bub, seg=16)
    # tendons above (glossy cream bands) and soft tissue behind
    ten = mat("tendon", "#f6efe2", rough=0.25, coat=0.6, sss=0.2)
    mus = mat("tissue", "#d9707a", rough=0.35, coat=0.5, sss=0.25)
    mus2 = mat("tissue2", "#e8949a", rough=0.35, coat=0.5, sss=0.25)
    random.seed(19)
    for k in range(9):
        yy = 3.6 + (k % 3) * 0.8; zz = 0.4 + (k // 3) * 1.25 + random.uniform(-0.15, 0.15)
        cylinder(0.5, 12.0, (random.uniform(-0.5, 0.5), yy, zz), (0, 90, random.uniform(-4, 4)), mus if k % 2 else mus2, verts=32, bevel=0.0)
    cylinder(0.11, 12.0, (0, 1.4, 0.3), (0, 90, 0), mat("artery", "#e0303a", rough=0.25, coat=0.7), verts=24, bevel=0.0)
    cylinder(0.1, 12.0, (0, 1.7, 0.28), (0, 90, 0), mat("vein", "#4a6fd0", rough=0.25, coat=0.7), verts=24, bevel=0.0)
    area_light((-3.0, -3.0, 4.0), (0, 0.2, 1.2), 700, 3, "#ffe2c2", "key")
    area_light((3.2, 2.5, 3.0), (0, 0.2, 1.2), 420, 2.5, "#8fd3ff", "rim")
    area_light((0.5, -4.0, 1.0), (0, 0.2, 1.2), 160, 3, "#ffd0c0", "fill")
    camera((2.9, -3.9, 2.6), (0.1, 0.3, 1.25), lens=24, fstop=4.0)


if not os.environ.get("BK_PROPS_ONLY"):
    clinic_angles()
    joint_set(False); still("plate_joint_closed", 1080, 1920, 40)
    joint_set(True); still("plate_joint_pulled", 1080, 1920, 40)


# cut-outs
def prop_scene2(w=800, h=800):
    reset(w, h, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#e9eef2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


prop_scene2(600, 800)
gold = metal("#e0b040", 0.2, "cup_gold")
lathe([(0, 0), (0.32, 0), (0.33, 0.06), (0.12, 0.12), (0.07, 0.2), (0.06, 0.42), (0.12, 0.48), (0.36, 0.62), (0.44, 0.95),
       (0.46, 1.08), (0.42, 1.08), (0.0, 0.9)], 48, (0, 0, 0), gold, 1, "cup")
for sgn in (-1, 1):
    torus(0.17, 0.03, (sgn * 0.5, 0, 0.82), (90, 0, 0), gold)
box((0.5, 0.42, 0.14), (0, 0, -0.07), material=mat("cup_base", "#34425c", rough=0.3, coat=0.5), bevel=0.02)
camera((0, -3.2, 1.0), (0, 0, 0.5), lens=50, fstop=0)
still("trophy", 600, 800, 32, transparent=True, crop=True)

prop_scene2(500, 800)
gm = mat("glass_g", "#eef8ff", rough=0.04, coat=0.8, alpha=0.25)
lathe([(0, 0), (0.24, 0), (0.27, 0.9), (0.25, 0.9), (0.22, 0.04), (0, 0.04)], 48, (0, 0, 0), gm, 1, "glass")
lathe([(0, 0.04), (0.22, 0.04), (0.245, 0.72), (0, 0.72)], 48, (0, 0, 0), mat("soda", "#d8f0ff", rough=0.05, coat=0.9, alpha=0.4), 1, "soda")
bm = mat("fizz", "#ffffff", rough=0.05, coat=1.0, emit="#e8fbff", emit_strength=0.6, alpha=0.8)
random.seed(5)
for k in range(30):
    a = random.uniform(0, 6.28); r = random.uniform(0, 0.17)
    sphere(random.uniform(0.012, 0.03), (math.cos(a) * r, math.sin(a) * r - 0.05, random.uniform(0.08, 0.7)), 1, bm, seg=10)
camera((0, -2.6, 0.75), (0, 0, 0.42), lens=50, fstop=0)
still("fizz_glass", 500, 800, 28, transparent=True, crop=True)
