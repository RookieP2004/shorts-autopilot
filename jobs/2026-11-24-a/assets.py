# 2026-11-24-a: "Scientists hacked eyes to see infrared" (build-it, Ved as a hacker).
# Set: a hacker's den on the night set: a dark desk with a laptop and two glowing monitors running a fictional
# "EYE.PATCH" terminal (green code, an eye wireframe, a spectrum bar), a desk lamp off, cables, a mug.
# Plates: den_wide (Ved stands at the desk), den_low (low hero angle, Dutch tilt), den_screen (close on the monitor).
# Cut-outs: a nanoparticle contact lens, a lab mouse figurine (tiny white clay mouse).
import math, os, random
from PIL import Image as PI, ImageDraw as PD, ImageFont as PF

A = ASSETS
FONT = os.path.join(ROOT, "assets/fonts")


def _font(sz):
    for f in ("JetBrainsMono-Regular.ttf", "DejaVuSansMono.ttf"):
        for d in (FONT, "/usr/share/fonts/truetype/dejavu"):
            p = os.path.join(d, f)
            if os.path.exists(p):
                return PF.truetype(p, sz)
    return PF.load_default()


def screen_tex(path, kind):
    W_, H_ = 1600, 1000
    im = PI.new("RGB", (W_, H_), (3, 12, 9))
    d = PD.Draw(im)
    f = _font(34)
    rnd = random.Random(11 if kind == "code" else 5)
    if kind == "code":
        d.text((40, 30), "EYE.PATCH v1.0  //  retina_scan", fill=(80, 255, 160), font=_font(44))
        for i in range(19):
            n = rnd.randint(14, 34)
            s = "".join(rnd.choice("abcdef0123456789 _=()") for _ in range(n))
            col = (40, 200, 120) if i % 5 else (255, 210, 90)
            d.text((40 + (i % 3) * 30, 110 + i * 46), f"{i:02d}  {s}", fill=col, font=f)
    else:
        # an eye wireframe + a spectrum bar with the visible window marked
        cx, cy = 560, 430
        for k in range(9):
            r = 60 + k * 32
            d.ellipse([cx - r * 1.5, cy - r, cx + r * 1.5, cy + r], outline=(30, 150 + k * 10, 110), width=3)
        d.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], outline=(80, 255, 160), width=6)
        d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(80, 255, 160))
        x0 = 1050
        for i in range(400):
            t = i / 400
            col = (int(120 + 135 * t), int(60 * (1 - t)), int(255 * (1 - t))) if t < 0.6 else (90, 10, 18)
            d.line([(x0 + 0, 150 + i * 1.6), (x0 + 120, 150 + i * 1.6)], fill=col)
        d.text((x0 - 10, 90), "SPECTRUM", fill=(80, 255, 160), font=f)
        d.text((x0 + 140, 300), "SEEN", fill=(220, 220, 220), font=f)
        d.text((x0 + 140, 700), "IR ??", fill=(255, 80, 90), font=f)
    im.save(path)
    return path


CODE = screen_tex(os.path.join(A, "tex_code.png"), "code")
EYE = screen_tex(os.path.join(A, "tex_eye.png"), "eye")


def monitor(loc, rot_z, img, w=1.05, name="mon"):
    x, y, z = loc
    h = w * 0.625
    frame = box((w + 0.05, 0.05, h + 0.05), (x, y, z), (0, 0, rot_z), glossy_black(), bevel=0.012, name=name)
    scr = plane(w, h, (0, 0, 0), (90, 0, 0), name=name + "_scr")
    m = mat(name + "_sm", "#000000", rough=0.3)
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(img)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 2.2
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    assign(scr, m)
    scr.parent = frame
    scr.location = (0, -0.03, 0)
    scr.rotation_euler = (math.radians(90), 0, 0)
    cylinder(0.025, z - 0.78, (x, y + 0.08, (z + 0.78) / 2), material=glossy_black(), verts=16, bevel=0, name=name + "_st")
    return frame


def den():
    reset(1080, 1920, samples=28, bloom=0.4, exposure=0.25)
    night_set(target=(0, 1.2, 0.8), rim=NIGHT["rim"], spot_power=9000, spot_height=8, spot_angle=38, grid=True,
              back_wall=CODE, wall_glow=0.18)
    desk = mat("desk", "#2a3140", rough=0.35, coat=0.4)
    box((2.6, 0.9, 0.06), (0, 1.5, 0.76), material=desk, bevel=0.01, name="desk_top")
    for sx in (-1.2, 1.2):
        box((0.06, 0.8, 0.74), (sx, 1.5, 0.38), material=desk, bevel=0.005, name="desk_leg")
    monitor((-0.6, 1.75, 1.3), math.radians(10), CODE, name="monL")
    monitor((0.6, 1.75, 1.3), math.radians(-10), EYE, name="monR")
    # laptop
    box((0.5, 0.34, 0.02), (0.15, 1.25, 0.8), (0, 0, 0), mat("lap", "#3a4250", rough=0.3, metal=0.5), bevel=0.004, name="lap")
    lid = plane(0.5, 0.32, (0.15, 1.42, 0.96), (75, 0, 0), name="lap_scr")
    lm = mat("lap_sm", "#000000", rough=0.3)
    nt = lm.node_tree
    tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(CODE)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.4
    nt.links.new(tx.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0].inputs["Surface"])
    assign(lid, lm)
    # mug and cable coils
    lathe([(0, 0), (0.05, 0), (0.055, 0.11), (0.0, 0.11)], 32, (-0.85, 1.25, 0.79), mat("mug", "#d6483e", rough=0.3, coat=0.5), name="mug")
    for k in range(3):
        torus(0.12 + k * 0.03, 0.008, (0.95, 1.6, 0.8), (0, 0, 0), glossy_black(), name=f"cable{k}")
    area_light((0, 0.9, 1.5), (0, 2.0, 1.2), 120, 1.6, NIGHT["green"], "screen_spill")


den()
camera((0.45, -2.5, 1.3), (0, 1.3, 1.15), lens=26, fstop=4.0)
still("plate_den_wide", samples=28)

den()
cam, _ = camera((-1.1, -2.2, 0.75), (0.1, 1.4, 1.15), lens=28, fstop=2.4, focus=3.6)
dutch(cam, 5)
still("plate_den_low", samples=28)

den()
camera((0.75, 0.2, 1.3), (0.6, 1.75, 1.28), lens=36, fstop=2.0)
still("plate_den_screen", samples=28)

# cut-outs
reset(800, 800, samples=40, transparent=True, bloom=0.3, exposure=0.3)
world_color(NIGHT["bg"], 0.05)
spot_light((0.0, -2.0, 4.0), (0, 0, 0), 900, 40, color=NIGHT["spot"], name="k")
area_light((2.0, 2.0, 1.2), (0, 0, 0), 300, 2.0, NIGHT["rim"], "rim")
area_light((-2, -3, 1), (0, 0, 0), 120, 5.0, "#bcc8ff", "fill")
exec(open(os.path.join(ROOT, "jobs/2026-11-24-a/shots/eyekit.py")).read())
cap, dots = contact_lens((0, 0, 0), 0.27, "hero_lens")
camera((0.18, -1.0, 0.25), (0, 0, 0), lens=60, fstop=0)
still("lens", 800, 800, 40, transparent=True, crop=True)
for o in list(bpy.data.objects):
    if o.type == "MESH":
        bpy.data.objects.remove(o)
mw = mat("mouse", "#f1ece6", rough=0.55, sss=0.2)
pink = mat("mouse_pink", "#f0a3a8", rough=0.5, sss=0.2)
sphere(0.16, (0, 0, 0.12), (1.0, 1.5, 0.85), mw, name="m_body")
sphere(0.09, (0, -0.24, 0.16), (1, 1.25, 0.95), mw, name="m_head")
for sx in (-1, 1):
    sphere(0.045, (sx * 0.065, -0.22, 0.26), (1, 0.35, 1), pink, name="m_ear")
    sphere(0.014, (sx * 0.04, -0.33, 0.19), 1, glow(NIGHT["green"], 6.0, "m_eye"), seg=12, name="m_eye")
sphere(0.012, (0, -0.355, 0.15), 1, pink, seg=12, name="m_nose")
torus(0.16, 0.012, (0.0, 0.3, 0.05), (90, 0, 90), pink, name="m_tail")
camera((-0.9, -1.1, 0.6), (0, -0.05, 0.13), lens=55, fstop=0)
still("mouse", 800, 800, 40, transparent=True, crop=True)
