# Shared builder for 2026-11-27-a ("Where do your returns go?"): our own returns warehouse. Cardboard boxes with tape and a
# fictional RETURN label, a roller conveyor, steel racks, pallets, a big skip/landfill heap, concrete floor, high windows.
# Exec'd by the shot scripts and assets.py (blendkit helpers already loaded). Built from primitives; all designs fictional.
import math, os, random
import bpy
from PIL import Image as _PI, ImageDraw as _PD, ImageFont as _PF

_TEX = {}


def _label_tex():
    p = os.path.join(ROOT, "jobs/2026-11-27-a/assets/tex_label.png")
    if os.path.exists(p):
        return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    im = _PI.new("RGB", (512, 512), (176, 128, 78))               # kraft cardboard
    d = _PD.Draw(im)
    rnd = random.Random(5)
    for k in range(300):                                          # fibres
        x, y = rnd.randint(0, 511), rnd.randint(0, 511)
        c = rnd.choice([(166, 118, 70), (186, 138, 88), (160, 112, 66)])
        d.line([(x, y), (x + rnd.randint(-14, 14), y + rnd.randint(-3, 3))], fill=c, width=1)
    d.rectangle([0, 226, 511, 286], fill=(200, 170, 120))         # tape strip
    d.rectangle([300, 330, 480, 460], fill=(246, 239, 226))       # label
    f = _PF.truetype(os.path.join(ROOT, "fonts", "Anton-Regular.ttf"), 44) if os.path.exists(os.path.join(ROOT, "fonts", "Anton-Regular.ttf")) else None
    d.text((314, 336), "RETURN", fill=(214, 72, 62), font=f)
    for k in range(5):
        d.line([(314, 400 + k * 10), (314 + rnd.randint(60, 150), 400 + k * 10)], fill=(40, 40, 40), width=4)
    im.save(p)
    return p


def _alive(name):
    m = _TEX.get(name)
    if m is None:
        return False
    try:
        m.name
        return True
    except ReferenceError:
        return False


def card_mat(name="cardboard"):
    if _alive(name):
        return _TEX[name]
    m = mat(name, "#ffffff", rough=0.85, image=_label_tex())
    _TEX[name] = m
    return m


def plain_card(name="card_plain", color="#b0804e"):
    if _alive(name):
        return _TEX[name]
    m = mat(name, color, rough=0.9)
    _TEX[name] = m
    return m


def _uv_box(o):
    if not o.data.uv_layers:
        o.data.uv_layers.new()
    try:
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.reset()
        bpy.ops.object.mode_set(mode="OBJECT")
        o.select_set(False)
    except Exception:
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except Exception:
            pass


def cbox(size, loc, rot=(0, 0, 0), name="cb", labelled=True, tint=None):
    m = card_mat() if labelled else plain_card(tint or "card_plain", tint or "#b0804e")
    o = box(size, loc, rot, m, bevel=0.012, name=name)
    if labelled:
        _uv_box(o)
    return o


def warehouse(floor_c="#8e9096", wall_c="#d9d2c4", lights=True, hdri=0.35):
    world_hdri("lounge", hdri, backdrop=(0.78, 0.8, 0.84))
    plane(60, 60, (0, 0, 0), material=mat("concrete", floor_c, rough=0.6, coat=0.15), name="floor")
    for k in range(-6, 7):                                       # yellow floor lane lines
        pass
    plane(0.12, 40, (-1.7, 0, 0.003), material=mat("lane", "#f2c230", rough=0.5), name="lane1")
    plane(0.12, 40, (1.7, 0, 0.003), material=mat("lane", "#f2c230", rough=0.5), name="lane2")
    box((90, 0.3, 24), (0, 14, 12), material=mat("wall", wall_c, rough=0.9), bevel=0, name="backwall")
    for k in range(-4, 5):                                       # high windows (glow)
        plane(2.2, 1.0, (k * 3.6, 13.84, 7.5), (90, 0, 0), material=glow("#fff3d6", 2.5, "win"), name=f"win{k}")
    if lights:
        area_light((-4, -4, 7), (0, 2, 0), 2600, 8, "#fff0dc", "key")
        area_light((5, -2, 5), (0, 2, 1), 900, 6, "#dbe8ff", "fill")


def rack(x, y, levels=4, length=4.0, depth=1.0, height=4.0, seed=1, fill=0.8, rot=0):
    """Steel pallet rack (orange beams, blue uprights) filled with boxes."""
    rnd = random.Random(seed)
    up = mat("rack_up", "#2f5f9a", rough=0.4, metal=0.5)
    beam = mat("rack_beam", "#e0702e", rough=0.4, metal=0.4)
    objs = []
    for sx in (-length / 2, length / 2):
        for sy in (-depth / 2, depth / 2):
            objs.append(box((0.08, 0.08, height), (x + sx, y + sy, height / 2), material=up, bevel=0.005))
    for lv in range(levels):
        z = 0.15 + lv * height / levels
        for sy in (-depth / 2, depth / 2):
            objs.append(box((length, 0.08, 0.12), (x, y + sy, z), material=beam, bevel=0.005))
        n = 0
        cx = x - length / 2 + 0.35
        while cx < x + length / 2 - 0.3:
            if rnd.random() < fill:
                s = rnd.uniform(0.45, 0.7)
                hh = rnd.uniform(0.35, 0.6)
                objs.append(cbox((s, depth * 0.8, hh), (cx, y, z + 0.06 + hh / 2), (0, 0, rnd.uniform(-6, 6)),
                                 name=f"rb{seed}_{lv}_{n}", labelled=rnd.random() < 0.5))
            cx += rnd.uniform(0.55, 0.8)
            n += 1
    return objs


def pallet(loc, name="pallet"):
    x, y, z = loc
    w = wood("#c9a06a", "#9a7444", name + "_w", 5.0, 0.6)
    objs = []
    for k in range(5):
        objs.append(box((1.2, 0.14, 0.03), (x, y - 0.5 + k * 0.25, z + 0.13), material=w, bevel=0.004))
    for k in range(3):
        objs.append(box((0.12, 1.1, 0.1), (x - 0.5 + k * 0.5, y, z + 0.06), material=w, bevel=0.004))
    return objs


def pallet_stack(loc, seed=3, layers=3, wrap=True, name="ps"):
    rnd = random.Random(seed)
    x, y, z = loc
    objs = pallet(loc, name + "_p")
    for L in range(layers):
        for i in range(2):
            for j in range(2):
                hh = 0.38
                objs.append(cbox((0.56, 0.52, hh), (x - 0.29 + i * 0.58, y - 0.27 + j * 0.54, z + 0.16 + hh / 2 + L * 0.4),
                                 (0, 0, rnd.uniform(-4, 4)), name=f"{name}_{L}{i}{j}", labelled=rnd.random() < 0.6))
    if wrap:
        objs.append(box((1.22, 1.14, layers * 0.4 + 0.04), (x, y, z + 0.16 + layers * 0.2), material=mat("wrap", "#e8f2ff", rough=0.15, alpha=0.18),
                        bevel=0.05, name=name + "_wrap"))
    return objs


def conveyor(x0, x1, y, z=0.8, width=0.9, name="cv"):
    """Roller conveyor along X at height z. Returns roller objects (spin them)."""
    steel = metal("#b9bec6", 0.3, "cv_steel")
    frame = mat("cv_frame", "#2f5f9a", rough=0.4, metal=0.4)
    L = x1 - x0
    box((L, 0.08, 0.14), ((x0 + x1) / 2, y - width / 2, z - 0.05), material=frame, bevel=0.005, name=name + "_f1")
    box((L, 0.08, 0.14), ((x0 + x1) / 2, y + width / 2, z - 0.05), material=frame, bevel=0.005, name=name + "_f2")
    k = 0
    while x0 + k * 1.5 < x1:
        for sy in (-width / 2, width / 2):
            box((0.07, 0.07, z), (x0 + k * 1.5, y + sy, z / 2), material=frame, bevel=0.004)
        k += 1
    rollers = []
    n = int(L / 0.16)
    for i in range(n):
        r = cylinder(0.045, width - 0.06, (x0 + 0.08 + i * 0.16, y, z), (90, 0, 0), steel, verts=16, bevel=0, name=f"{name}_r{i}")
        rollers.append(r)
    return rollers


def heap(center, radius=4.0, n=140, seed=9, height=2.6, name="heap"):
    """A mountain of returned boxes and bags."""
    rnd = random.Random(seed)
    cx, cy, cz = center
    objs = []
    core = cone(radius * 0.92, height * 1.05, (cx, cy, cz + height * 0.5), (0, 0, 0), plain_card("core_c", "#a87a4a"), name=name + "_core")
    core.scale = (1.0, 1.0, 1.0)
    cols = ["#b0804e", "#c4925a", "#a37344", "#d6483e", "#3f8f8a", "#f2b04a", "#f6efe2"]
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        r = radius * math.sqrt(rnd.random())
        hz = height * max(0.0, 1 - r / radius) * 1.0 + rnd.uniform(-0.2, 0.0)
        s = rnd.uniform(0.35, 0.8)
        lab = rnd.random() < 0.45
        if not lab and rnd.random() < 0.3:
            c = rnd.choice(cols[3:])
            o = box((s, s * rnd.uniform(0.6, 1.0), s * 0.5), (cx + r * math.cos(a), cy + r * math.sin(a), cz + hz + s * 0.25),
                    (rnd.uniform(-30, 30), rnd.uniform(-30, 30), rnd.uniform(0, 360)), mat("bag" + c, c, rough=0.5), bevel=0.05)
        else:
            o = cbox((s, s * rnd.uniform(0.7, 1.0), s * rnd.uniform(0.5, 0.9)),
                     (cx + r * math.cos(a), cy + r * math.sin(a), cz + hz + s * 0.3),
                     (rnd.uniform(-35, 35), rnd.uniform(-35, 35), rnd.uniform(0, 360)), name=f"{name}{i}", labelled=lab)
        objs.append(o)
    return objs


def skip_bin(loc, name="skip"):
    """A big open green dumpster (skip)."""
    x, y, z = loc
    g = mat("skip_g", "#2e6b45", rough=0.45, metal=0.3)
    box((3.0, 0.1, 1.3), (x, y - 0.8, z + 0.65), material=g, bevel=0.01)
    box((3.0, 0.1, 1.3), (x, y + 0.8, z + 0.65), material=g, bevel=0.01)
    box((0.1, 1.7, 1.3), (x - 1.5, y, z + 0.65), material=g, bevel=0.01)
    box((0.1, 1.7, 1.3), (x + 1.5, y, z + 0.65), material=g, bevel=0.01)
    box((3.0, 1.7, 0.1), (x, y, z + 0.05), material=g, bevel=0.01)
    return g


def magnifier(loc=(0, 0, 0), name="mag"):
    x, y, z = loc
    ring = torus(0.3, 0.04, (x, y, z), (90, 0, 0), metal("#d9a441", 0.25, "mag_gold"), name=name + "_ring")
    lens = cylinder(0.29, 0.02, (x, y, z), (90, 0, 0), glass("#eaf4ff", 0.02, "mag_glass"), verts=48, bevel=0, name=name + "_lens")
    h = cylinder(0.05, 0.5, (x + 0.26, y, z - 0.42), (0, 32, 0), wood("#5a3a22", "#3a2414", "mag_h", 5, 0.4), verts=20, bevel=0.01, name=name + "_h")
    return [ring, lens, h]
