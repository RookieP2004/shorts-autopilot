# 2026-11-17-a: "How hawala moves money without moving money" (dark-files, night look).
# One night set: two little broker kiosks on a dark glossy floor, NEW YORK on the left, LAHORE on the right, each with a
# wooden counter, a lit back panel with shelves (jars, boxes, ledgers), a glowing sign and a hanging bulb; a far wall with a
# fictional dotted "route" arc between two glowing pins. Four plates (wide, mid on each kiosk, low hero with a Dutch tilt),
# foreground counters for depth staging, cut-outs: phone (live screen later), two fictional notes ("NOT REAL MONEY"),
# an open ledger, a coin.
import math, os, random
from PIL import Image as PI, ImageDraw as PD
from autopilot import devices

A = ASSETS


def route_wall(path):
    """Fictional night 'map': a field of faint dots, two glowing pins and a dashed arc between them (no real map)."""
    W_, H_ = 1600, 900
    im = PI.new("RGB", (W_, H_), (4, 7, 14))
    d = PD.Draw(im)
    rnd = random.Random(11)
    for _ in range(1400):
        x, y = rnd.uniform(0, W_), rnd.uniform(60, H_ - 60)
        r = rnd.choice((1.5, 2, 2.5))
        c = rnd.choice(((18, 34, 62), (22, 44, 80), (14, 26, 48)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    p0, p1 = (330, 560), (1270, 560)
    pts = []
    for i in range(61):
        t = i / 60
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] - math.sin(math.pi * t) * 300
        pts.append((x, y))
    for i in range(0, 60, 2):
        d.line([pts[i], pts[i + 1]], fill=(244, 192, 78), width=6)
    for (x, y), col in ((p0, (74, 163, 255)), (p1, (53, 224, 138))):
        for r, a in ((46, 40), (30, 90), (16, 255)):
            cc = tuple(int(v * a / 255) for v in col)
            d.ellipse([x - r, y - r, x + r, y + r], fill=cc)
    im.save(path)
    return path


WALL = route_wall(os.path.join(A, "route_wall.png"))
NOTE = os.path.join(A, "note_fake.png")


def note_texture(value, path, w=1200, h=560, tint=(102, 196, 168)):
    """Fictional dollar-style note (our own design, NOT REAL MONEY), same layout as devices.note_texture."""
    font = devices.font
    img = PI.new("RGB", (w, h), tint)
    d = PD.Draw(img)
    dark = tuple(int(c * 0.55) for c in tint)
    pale = tuple(min(255, int(c * 1.25)) for c in tint)
    for i in range(0, w + h, 14):
        d.line([(i, 0), (i - h, h)], fill=pale, width=1)
    for r in range(40, 260, 18):
        d.ellipse([w * 0.72 - r, h / 2 - r, w * 0.72 + r, h / 2 + r], outline=dark, width=2)
    d.rectangle([14, 14, w - 15, h - 15], outline=dark, width=8)
    d.text((60, 40), "$" + value, font=font("b", 150), fill=dark)
    d.text((60, h - 140), "NOT REAL MONEY", font=font("b", 64), fill=dark)
    d.text((62, h - 64), "THE EXPLAINER - FOR ILLUSTRATION ONLY", font=font("s", 28), fill=dark)
    d.text((w * 0.72, h / 2), value, font=font("b", 120), fill=(250, 250, 245), anchor="mm")
    img.save(path)


note_texture("100", NOTE)
LEDGER_TEX = os.path.join(A, "ledger_tex.png")


def ledger_texture(path):
    W_, H_ = 1200, 800
    im = PI.new("RGB", (W_, H_), (240, 228, 200))
    d = PD.Draw(im)
    d.line([(W_ // 2, 0), (W_ // 2, H_)], fill=(170, 150, 120), width=6)
    for y in range(90, H_ - 40, 52):
        d.line([(40, y), (W_ // 2 - 30, y)], fill=(160, 190, 210), width=3)
        d.line([(W_ // 2 + 30, y), (W_ - 40, y)], fill=(160, 190, 210), width=3)
    rnd = random.Random(3)
    for y in range(90, H_ - 90, 52):
        for x0 in (60, W_ // 2 + 50):
            x = x0
            for _ in range(rnd.randint(2, 4)):
                w = rnd.randint(40, 120)
                d.line([(x, y - 14), (x + w, y - 14)], fill=(40, 50, 80), width=5)
                x += w + 18
    im.save(path)
    return path


ledger_texture(LEDGER_TEX)

NY = (-2.3, 0.9)
LH = (2.3, 0.9)
COUNTERS = []


def bulb(x, y, z):
    cylinder(0.005, 1.2, (x, y, z + 0.65), material=mat("cord", "#111111"), verts=8)
    sphere(0.07, (x, y, z), 1, mat("bulb_glow", "#fff1c9", emit="#ffcf7a", emit_strength=18.0), seg=20)
    d = bpy.data.lights.new("bulb", "POINT"); d.energy = 90; d.color = hexrgb("#ffc77a"); d.shadow_soft_size = 0.05
    o = bpy.data.objects.new("bulb", d); bpy.context.scene.collection.objects.link(o); o.location = (x, y, z - 0.1)


def kiosk(cx, cy, rot, label, sign_col, name):
    r = math.radians(rot)

    def P(dx, dy, z):
        return (cx + dx * math.cos(r) - dy * math.sin(r), cy + dx * math.sin(r) + dy * math.cos(r), z)

    rr = (0, 0, rot)
    woodm = wood("#a8743f", "#7a4e2a", f"wood_{name}", 5.0)
    dark = mat(f"panel_{name}", "#1d2a3d", rough=0.6)
    # back panel + shelves
    box((2.0, 0.12, 2.5), P(0, 0.9, 1.25), rr, dark, bevel=0.03)
    for z in (1.15, 1.6):
        box((1.8, 0.32, 0.05), P(0, 0.76, z), rr, woodm, bevel=0.01)
    rnd = random.Random(len(label))
    cols = ["#d9534f", "#f2b04a", "#46965a", "#3f7fbf", "#e9e6df", "#6fc3c0"]
    for z in (1.18, 1.63):
        x = -0.8
        while x < 0.75:
            kind = rnd.random()
            c = rnd.choice(cols)
            if kind < 0.45:
                h = rnd.uniform(0.16, 0.26)
                cylinder(0.06, h, P(x + 0.06, 0.74, z + h / 2), rr, mat(f"jar_{c}", c, rough=0.3, coat=0.5), verts=20)
                x += 0.16
            elif kind < 0.75:
                h = rnd.uniform(0.22, 0.3)
                box((0.06, 0.22, h), P(x + 0.03, 0.74, z + h / 2), rr, mat(f"book_{c}", c, rough=0.6), bevel=0.008)
                x += 0.08
            else:
                box((0.22, 0.2, 0.14), P(x + 0.11, 0.74, z + 0.07), rr, wood("#c79a5b", "#9a6f3d", "boxw", 4.0), bevel=0.01)
                x += 0.26
    # sign
    box((1.8, 0.08, 0.46), P(0, 0.82, 2.25), rr, mat(f"sign_{name}", "#0b1424", rough=0.5), bevel=0.02)
    box((1.86, 0.06, 0.52), P(0, 0.84, 2.25), rr, mat(f"signedge_{name}", sign_col, emit=sign_col, emit_strength=3.0), bevel=0.01)
    text3d(label, 0.34, P(0, 0.75, 2.25), (90, 0, rot), mat(f"sign_text_{name}", sign_col, emit=sign_col, emit_strength=1.6),
           extrude=0.02, name=f"label_{name}")
    # side posts and a little roof
    for sx in (-0.98, 0.98):
        box((0.08, 0.08, 2.6), P(sx, 0.85, 1.3), rr, woodm, bevel=0.01)
    box((2.2, 1.1, 0.08), P(0, 0.4, 2.62), rr, mat(f"roof_{name}", "#7c2533" if name == "ny" else "#2a6b4a", rough=0.5), bevel=0.02)
    # counter (foreground object)
    parts = [box((1.8, 0.6, 1.0), P(0, -0.15, 0.5), rr, woodm, bevel=0.03),
             box((1.95, 0.72, 0.07), P(0, -0.15, 1.03), rr, mat("countertop", "#3a2a22", rough=0.35, coat=0.6), bevel=0.02),
             box((1.6, 0.03, 0.12), P(0, -0.46, 0.8), rr, metal("#d9a441", 0.3, "brass"), bevel=0.01)]
    # ledger + a lamp on the counter
    book = box((0.42, 0.3, 0.03), P(-0.35, -0.1, 1.08), (0, 0, rot - 8), paper(LEDGER_TEX), bevel=0.004)
    lamp_base = cylinder(0.07, 0.03, P(0.6, 0.0, 1.08), rr, metal("#d9a441", 0.3, "brass"), verts=24)
    lamp_shade = cone(0.13, 0.12, P(0.6, 0.0, 1.38), rr, mat("lampshade", "#46965a", rough=0.4, emit="#ffe2a0", emit_strength=0.4))
    lamp_stem = cylinder(0.012, 0.3, P(0.6, 0.0, 1.22), rr, metal("#d9a441", 0.3, "brass"), verts=10)
    parts += [book, lamp_base, lamp_shade, lamp_stem]
    COUNTERS.extend(parts)
    bulb(*P(0, 0.2, 2.3))


def build(grid=True):
    COUNTERS.clear()
    reset(1080, 1920, samples=28, bloom=0.35, exposure=0.25)
    night_set(target=(0, 0.6, 0), rim=NIGHT["rim"], spot_power=26000, spot_height=10, spot_angle=60, grid=grid,
              back_wall=WALL, wall_glow=0.5)
    area_light((0, -6, 4), (0, 0.6, 1), 500, 6.0, "#9fb4ff", "front_fill")
    kiosk(NY[0], NY[1], 14, "NEW YORK", "#4aa3ff", "ny")
    kiosk(LH[0], LH[1], -14, "LAHORE", "#35e08a", "lh")


# 1. wide: both kiosks
build()
camera((0, -10.2, 3.6), (0, 0.6, 1.1), lens=27, fstop=0)
still("plate_wide", samples=28)
still("fg_wide", only=list(COUNTERS), samples=28)

# 2. mid on New York
build()
cam, _ = camera((-1.0, -4.9, 1.75), (-2.3, 0.7, 1.15), lens=30, fstop=2.8, focus=5.6)
dutch(cam, 3)
still("plate_ny", samples=28)
still("fg_ny", only=list(COUNTERS), samples=28)

# 3. mid on Lahore
build()
cam, _ = camera((1.0, -4.9, 1.75), (2.3, 0.7, 1.15), lens=30, fstop=2.8, focus=5.6)
dutch(cam, -3)
still("plate_lh", samples=28)
still("fg_lh", only=list(COUNTERS), samples=28)

# 4. low hero between the kiosks (Ved's stage), Dutch tilt
build()
cam, _ = camera((0.5, -6.6, 1.15), (0, 0.4, 1.15), lens=34, fstop=2.0, focus=6.4)
dutch(cam, 5)
still("plate_hero", samples=28)

# 5. cut-outs under the night light
def cut_light():
    world_color(NIGHT["bg"], 0.05)
    spot_light((0.0, -3.0, 6.0), (0, 0, 0), 1500, 40, color=NIGHT["spot"], name="k")
    area_light((2.5, 2.5, 1.5), (0, 0, 0), 600, 2.0, NIGHT["rim"], "rim")
    area_light((-2.5, 2.0, 1.0), (0, 0, 0), 300, 2.0, "#7a5cff", "rim2")
    area_light((-3, -4, 1), (0, 0, 0), 200, 6.0, "#ffffff", "fill")


reset(1080, 1920, samples=48, bloom=0.3, exposure=0.3)
cut_light()
body, scr = phone((0, 0, 0), (0, 0, 0), w=0.8)
camera((0, -3.4, 0.1), (0, 0, 0), lens=60, fstop=0)
phone_sprite("phone", scr, samples=48)

for i, (rot, bend) in enumerate((((80, 8, 20), 18), ((65, -20, -35), -24))):
    reset(1080, 1080, samples=40, bloom=0.25, exposure=0.3)
    cut_light()
    banknote(NOTE, (0, 0, 0), rot, w=1.0, name="note", bend=bend)
    camera((0, -3.4, 0.4), (0, 0, 0), lens=55, fstop=0)
    still(f"note{i + 1}", 1080, 1080, samples=40, transparent=True, crop=True)

reset(1080, 1080, samples=48, bloom=0.3, exposure=0.3)
cut_light()
area_light((0.5, -4, 1.5), (0, 0, 0), 900, 8.0, "#ffe2b8", "coinfill")
coin((0, 0, 0), (90, 0, 18), r=0.5, symbol="$")
camera((0.4, -3.2, 0.6), (0, 0, 0), lens=60, fstop=0)
still("coin", 1080, 1080, samples=48, transparent=True, crop=True)

