# 2026-11-13-b: "What if you could SEE Wi-Fi?" (what-if). Sets: a cosy living room (wood floor, cream walls, a window,
# a teal sofa, a TV console with the Wi-Fi router, plant, floor lamp, rug), 2 angles + the "radio eyes" version of the wide
# angle (router glowing like a lamp, glowing wave rings, walls turned see-through onto the garden and a neighbour's house);
# a green karst valley from above, once with a giant eyeball sitting in it (with tiny houses for scale) and once with a
# FAST-style 500 m radio dish, same camera. Cut-outs: the router, the eyeball.
import math, os, random

# checker_mat(), seg(), tree(), bush(), house(), sunny() ... from earlier jobs (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-11-b/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "b_helpers", "exec"), globals())


# ---------------------------------------------------------------- props
def router(x, y, z, s=1.0, glow_on=False):
    body = mat("router_body", "#2b2f36", rough=0.3, coat=0.6)
    box((0.62 * s, 0.38 * s, 0.11 * s), (x, y, z + 0.055 * s), material=body, bevel=0.035 * s)
    led = mat("router_led", "#7dffb0", emit="#5dff9a", emit_strength=8.0)
    for k in range(4):
        sphere(0.014 * s, (x - 0.15 * s + k * 0.1 * s, y - 0.19 * s, z + 0.07 * s), 1, led, seg=10)
    ant = mat("router_ant", "#24272d", rough=0.35, coat=0.4)
    for k, ang in enumerate((-18, 0, 18)):
        a = cylinder(0.022 * s, 0.42 * s, (x - 0.2 * s + k * 0.2 * s, y + 0.14 * s, z + 0.3 * s), (0, ang, 0), ant, verts=16, bevel=0.01)
    if glow_on:
        g = mat("router_glow", "#7fe8ff", emit="#6fe0ff", emit_strength=40.0)
        sphere(0.3 * s, (x, y, z + 0.25 * s), 1, g, seg=24)
        L = bpy.data.lights.new("router_light", "POINT"); L.energy = 900; L.color = hexrgb("#7fe8ff"); L.shadow_soft_size = 0.4
        o = bpy.data.objects.new("router_light", L); bpy.context.scene.collection.objects.link(o); o.location = (x, y - 0.4, z + 0.4)


def eyeball(x, y, z, r=1.0, iris="#2f7fb8", name="eye"):
    white = mat(name + "_white", "#f7f2ea", rough=0.18, coat=0.8, sss=0.15)
    sphere(r, (x, y, z), 1, white, seg=64, name=name)
    vein = mat(name + "_vein", "#e07b72", rough=0.4)
    random.seed(3)
    for k in range(7):                                                   # a few soft veins toward the iris
        a = random.uniform(0, 2 * math.pi)
        p0 = (x + 0.98 * r * math.cos(a) * 0.9, y - 0.25 * r, z + 0.98 * r * math.sin(a) * 0.9)
        p1 = (x + 0.55 * r * math.cos(a + 0.2), y - 0.8 * r, z + 0.55 * r * math.sin(a + 0.2))
        seg(p0, p1, 0.012 * r, vein)
    ir = mat(name + "_iris", iris, rough=0.3, coat=0.5)
    cylinder(0.42 * r, 0.06 * r, (x, y - 0.995 * r, z), (90, 0, 0), ir, verts=64, bevel=0.01 * r)
    ring = mat(name + "_ring", "#1d3d5c", rough=0.3)
    torus(0.42 * r, 0.03 * r, (x, y - 1.0 * r, z), (90, 0, 0), ring)
    cylinder(0.19 * r, 0.07 * r, (x, y - 1.02 * r, z), (90, 0, 0), mat(name + "_pupil", "#0b0d10", rough=0.15, coat=1.0), verts=48, bevel=0.005 * r)
    sphere(0.07 * r, (x - 0.16 * r, y - 1.05 * r, z + 0.16 * r), 1, mat(name + "_spec", "#ffffff", emit="#ffffff", emit_strength=4.0), seg=16)


def sofa(x, y):
    fab = mat("sofa_fab", "#3c8f8c", rough=0.85, noise_bump=0.15)
    fab2 = mat("sofa_cush", "#4aa3a0", rough=0.85, noise_bump=0.15)
    box((2.4, 0.95, 0.42), (x, y, 0.32), material=fab, bevel=0.08)
    box((2.4, 0.28, 0.7), (x, y + 0.4, 0.75), material=fab, bevel=0.1)
    for sx in (-1, 1):
        box((0.26, 0.95, 0.62), (x + sx * 1.22, y, 0.42), material=fab, bevel=0.1)
    for k in (-0.55, 0.55):
        box((1.05, 0.78, 0.16), (x + k, y - 0.06, 0.6), material=fab2, bevel=0.07)
    box((0.42, 0.14, 0.36), (x - 0.75, y + 0.2, 0.86), (12, 0, 8), mat("pillow", "#f2b04a", rough=0.8), bevel=0.08)
    leg = wood("#6a4630", "#4a3020", "sofa_leg", 3.0)
    for sx in (-1.1, 1.1):
        for sy in (-0.38, 0.38):
            cylinder(0.04, 0.12, (x + sx, y + sy, 0.06), material=leg, verts=12)


def plant(x, y, s=1.0):
    pot = mat("pot", "#d9744a", rough=0.6, coat=0.2)
    lathe([(0.0, 0.0), (0.18 * s, 0.0), (0.24 * s, 0.4 * s), (0.27 * s, 0.45 * s), (0.0, 0.45 * s)], 40, (x, y, 0), pot, subdiv=1)
    leaf = mat("leaf", "#3f8a3e", rough=0.6, coat=0.3, noise_bump=0.1)
    random.seed(9)
    for k in range(9):
        a = k / 9 * 2 * math.pi
        o = sphere(0.22 * s, (x + math.cos(a) * 0.2 * s, y + math.sin(a) * 0.12 * s, 0.75 * s + random.uniform(-0.1, 0.35) * s),
                   (0.5, 0.5, 1.4), leaf, seg=20)
        o.rotation_euler = (math.cos(a) * 0.5, math.sin(a) * 0.5, a)


def lamp(x, y):
    m = metal("#c9a46a", 0.3, "lamp_m")
    cylinder(0.2, 0.04, (x, y, 0.02), material=m, verts=32)
    cylinder(0.02, 1.6, (x, y, 0.82), material=m, verts=12)
    sh = mat("shade", "#f6efe2", rough=0.7, emit="#ffd9a0", emit_strength=1.2, sss=0.3)
    lathe([(0.32, 0.0), (0.2, 0.32)], 40, (x, y, 1.45), sh, subdiv=0)
    L = bpy.data.lights.new("lamp_l", "POINT"); L.energy = 120; L.color = hexrgb("#ffcf8a"); L.shadow_soft_size = 0.2
    o = bpy.data.objects.new("lamp_l", L); bpy.context.scene.collection.objects.link(o); o.location = (x, y, 1.55)


ROUTER_AT = (-2.0, 3.35, 0.62)


def build_room(wifi=False):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3 if wifi else 0.15)
    sunny(sky_top="#4aa3e6", sky_horizon="#d6eef9", sun=3.2)
    # outside: garden, a neighbour's house, trees (only seen through the window, or through the walls in the wifi view)
    plane(80, 80, (0, 20, -0.01), material=mat("grass", "#6da84e", rough=0.95, noise_bump=0.3), name="grass")
    house(2.5, 9.5, 4.0, 3.2, "#e9c46a", "#b5533c")
    house(-4.8, 11.5, 3.6, 4.0, "#d9e3ea", "#34425c")
    tree(-1.5, 7.5, 3.4, 1.3, 2, "#4f9a45"); tree(6.5, 8.0, 3.8, 1.4, 3, "#5aa64a"); tree(-8.0, 8.5, 3.2, 1.2, 4, "#4a8f45")
    # the room
    planks = wood("#c08a55", "#9a6a3e", "floor_wood", 5.0, 0.45)
    plane(9.0, 12.5, (0, -2.1, 0), material=planks, name="floor")
    wa = 0.18 if wifi else 1.0
    wall = mat("wall", "#efe3c8", rough=0.85, alpha=wa)
    wall2 = mat("wall2", "#e6d6b6", rough=0.85, alpha=wa)
    box((9.0, 0.16, 3.3), (0, 4.1, 1.65), material=wall, bevel=0.0, name="back_wall")
    box((0.16, 7.5, 3.3), (-4.5, 0.4, 1.65), material=wall2, bevel=0.0, name="left_wall")
    box((9.0, 0.06, 0.14), (0, 4.0, 0.07), material=mat("skirt", "#f6efe2", rough=0.5, alpha=wa), bevel=0.01)
    # window in the back wall: frame + a clear pane (the opaque wall behind is cut by a darker inset)
    fr = mat("frame", "#f6efe2", rough=0.4, alpha=max(wa, 0.5))
    if not wifi:
        box((1.9, 0.18, 1.5), (1.4, 4.1, 1.85), material=mat("win_hole", "#bfe4fb", rough=0.05, transmission=1.0, alpha=0.08), bevel=0.0, name="win_glass")
        bpy.data.objects["back_wall"].modifiers.new("hole", "BOOLEAN").object = bpy.data.objects["win_glass"]
        bpy.data.objects["back_wall"].modifiers["hole"].operation = "DIFFERENCE"
    for (sx, sy, w, h) in ((1.4, 2.6, 2.0, 0.08), (1.4, 1.1, 2.0, 0.08), (0.42, 1.85, 0.08, 1.5), (2.38, 1.85, 0.08, 1.5), (1.4, 1.85, 0.06, 1.5)):
        box((w, 0.2, h), (sx, 4.0, sy), material=fr, bevel=0.01)
    # a picture on the wall: a little landscape, framed
    box((0.9, 0.05, 0.7), (-2.0, 4.0, 2.05), material=wood("#7a4e2a", "#5e3f2a", "pic_frame", 3.0), bevel=0.02)
    box((0.76, 0.03, 0.56), (-2.0, 3.98, 2.05), material=mat("pic", "#6fc3c0", rough=0.6, alpha=wa), bevel=0.0)
    sphere(0.09, (-1.8, 3.96, 2.18), 1, mat("pic_sun", "#f2b04a", rough=0.5), seg=12)
    # TV console with the router + books
    cw = wood("#8a5a3c", "#6a4630", "console", 4.0)
    box((1.8, 0.5, 0.55), (-2.0, 3.55, 0.3), material=cw, bevel=0.04)
    for k, c in enumerate(("#d9534f", "#34425c", "#f2b04a", "#46965a")):
        box((0.08, 0.3, 0.32 - k * 0.02), (-1.25 + k * 0.1, 3.6, 0.73 - k * 0.01), material=mat(f"book{k}", c, rough=0.7), bevel=0.01)
    router(*ROUTER_AT, s=0.9, glow_on=wifi)
    rug = mat("rug", "#c97a3a", rough=0.95, noise_bump=0.2)
    cylinder(1.7, 0.02, (0.4, 1.2, 0.01), material=rug, verts=64, bevel=0.005).scale = (1.25, 0.8, 1)
    sofa(1.5, 2.9)
    plant(3.6, 3.4, 1.2)
    lamp(-3.6, 2.8)
    # a low coffee table
    tw = wood("#b07a48", "#8a5a3c", "table", 4.0)
    box((1.2, 0.6, 0.06), (0.6, 1.0, 0.42), material=tw, bevel=0.02)
    for sx in (-0.5, 0.5):
        for sy in (-0.22, 0.22):
            cylinder(0.03, 0.4, (0.6 + sx, 1.0 + sy, 0.2), material=tw, verts=10)
    cylinder(0.08, 0.12, (0.4, 1.0, 0.51), material=mat("mug", "#f6efe2", rough=0.3, coat=0.4), verts=24)
    if wifi:
        # the waves made visible: glowing rings spreading from the router, each one fainter
        for k, r in enumerate((0.6, 1.2, 1.9, 2.7, 3.6, 4.6)):
            g = mat(f"wave{k}", "#7fe8ff", emit="#6fe0ff", emit_strength=6.0 - k * 0.8, alpha=0.75 - k * 0.1)
            torus(r, 0.025 + 0.004 * k, (ROUTER_AT[0], ROUTER_AT[1], ROUTER_AT[2] + 0.25), (90, 0, 0), g)
            torus(r * 0.98, 0.02, (ROUTER_AT[0], ROUTER_AT[1], ROUTER_AT[2] + 0.25), (0, 0, 0), g)
    # light: soft daylight through the window side + a warm interior key from front-left
    area_light((-3.5, -3.0, 3.4), (0, 2.5, 0.8), 650 if not wifi else 380, 4, "#ffe2c2", "key")
    area_light((3.5, -2.5, 2.8), (0, 2.5, 0.8), 220 if not wifi else 120, 4, "#bcd2ff", "fill")
    drop_cams()


def room_angles():
    build_room(False)
    camera((0.3, -5.2, 1.6), (0.0, 2.8, 1.25), lens=22, fstop=8.0)
    still("plate_room_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.2, -2.6, 1.45), (-1.2, 3.3, 0.95), lens=28, fstop=4.0)
    still("plate_room_mid", 1080, 1920, 40)
    build_room(True)
    camera((0.3, -5.2, 1.6), (0.0, 2.8, 1.25), lens=22, fstop=8.0)
    still("plate_room_wifi", 1080, 1920, 40)


# ---------------------------------------------------------------- the karst valley (FAST)
def H(x, y):
    """A round valley floor (r ~ 16) ringed by steep green cone hills."""
    r = math.hypot(x, y - 30)
    bowl = -2.0 * math.exp(-(r / 14) ** 2)
    hills = 0.0
    for (hx, hy, hh, hr) in KARST:
        hills += hh * math.exp(-((x - hx) ** 2 + (y - hy) ** 2) / (hr * hr))
    return bowl + hills


random.seed(21)
KARST = []
for k in range(26):
    a = k / 26 * 2 * math.pi + random.uniform(-0.1, 0.1)
    d = random.uniform(20, 30)
    KARST.append((d * math.cos(a), 30 + d * math.sin(a), random.uniform(7, 13), random.uniform(4.5, 6.5)))
for k in range(14):
    a = random.uniform(0, 2 * math.pi); d = random.uniform(34, 52)
    KARST.append((d * math.cos(a), 30 + d * math.sin(a), random.uniform(9, 16), random.uniform(5, 8)))


def karst_mat():
    m = bpy.data.materials.new("karst"); m.use_nodes = True; nt = m.node_tree
    pr = nt.nodes.get("Principled BSDF"); pr.inputs["Roughness"].default_value = 0.9
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 0.25; n.inputs["Detail"].default_value = 6
    r = nt.nodes.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].position = 0.4; r.color_ramp.elements[0].color = (*hexrgb("#3f7a3a"), 1)
    r.color_ramp.elements[1].position = 0.62; r.color_ramp.elements[1].color = (*hexrgb("#6fa04a"), 1)
    nt.links.new(n.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], pr.inputs["Base Color"])
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.4
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 6
    nt.links.new(n2.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], pr.inputs["Normal"])
    return m


def fast_dish(cx, cy, R=13.0):
    panel = mat("dish_panels", "#dfe5ea", rough=0.35, metal=0.3, noise_bump=0.15)
    prof = [(0.6, 0.0)] + [(R * t, (0.32 * (R * t) ** 2) / R) for t in (0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0)]
    z0 = H(cx, cy) + 0.35
    d = lathe(prof, 96, (cx, cy, z0), panel, subdiv=1, name="dish")
    cylinder(0.8, 0.12, (cx, cy, z0), material=panel, verts=32)
    s = d.modifiers.new("thick", "SOLIDIFY"); s.thickness = 0.12
    rimz = z0 + 0.32 * R
    tower = mat("tower", "#d9dee4", rough=0.4)
    cable = metal("#7d8590", 0.4, "cable")
    cab = (cx, cy, rimz + 5.0)
    for k in range(6):
        a = k / 6 * 2 * math.pi + 0.3
        tx, ty = cx + (R + 2.0) * math.cos(a), cy + (R + 2.0) * math.sin(a)
        tz = H(tx, ty)
        top = (tx, ty, rimz + 8.0)
        cylinder(0.35, top[2] - tz, (tx, ty, (top[2] + tz) / 2), material=tower, verts=16, bevel=0.03)
        seg(top, cab, 0.035, cable)
    box((1.6, 1.6, 0.9), cab, material=mat("cabin", "#f2b04a", rough=0.4, coat=0.3), bevel=0.1)


def tiny_village(cx, cy):
    random.seed(5)
    cols = ("#e9c46a", "#d9e3ea", "#f6efe2", "#d9744a")
    for k in range(7):
        x = cx + k * 1.3 + random.uniform(-0.2, 0.2); y = cy + random.uniform(-0.6, 0.6)
        z = H(x, y)
        box((0.8, 0.7, 0.62), (x, y, z + 0.31), material=mat(f"vh{k}", cols[k % 4], rough=0.8), bevel=0.02)
        r = cylinder(0.52, 0.78, (x, y, z + 0.72), (90, 0, 0), mat("vroof", "#b5533c", rough=0.6), verts=3, bevel=0.01)
        r.rotation_euler = (math.radians(90), math.radians(30), 0)


def build_valley(kind):
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.1)
    sunny(sky_top="#3f9be0", sky_horizon="#e3f1f7", sun=4.0)
    terrain(-70, 70, -10, 95, 170, 150, karst_mat())
    # far haze ridges, bluer with distance
    for k in range(6):
        sphere(18, (-60 + k * 24, 110 + (k % 2) * 8, -4), (1.5, 0.6, 0.7 + 0.1 * (k % 3)), mat(f"haze{k}", "#a9c7d9", rough=1.0), seg=32)
    if kind == "dish":
        fast_dish(0, 30)
    else:
        before = set(bpy.data.objects)
        eyeball(0, 0, 0, 11.0, name="giant_eye")
        e = group([o for o in bpy.data.objects if o not in before and o.parent is None], "eye_grp")
        e.location = (0, 30, H(0, 30) + 10.5)
        e.rotation_euler = (math.radians(-48), 0, 0)
        tiny_village(-14.5, 24)
        tiny_village(9.0, 20)
    random.seed(7)
    for k in range(14):
        x = random.uniform(-26, 26); y = random.uniform(8, 18)
        if math.hypot(x, y - 30) > 15:
            tree(x, y, 1.6, 0.6, 20 + k, random.choice(("#3f7a3a", "#4f8a3e", "#5aa64a")))
    area_light((-30, -10, 30), (0, 30, 0), 9000, 20, "#fff0dc", "key")
    drop_cams()
    camera((0, -2, 48), (0, 33, 0), lens=26, fstop=0)


def valley_angles():
    build_valley("eye")
    still("plate_valley_eye", 1080, 1920, 40)
    build_valley("dish")
    still("plate_valley_dish", 1080, 1920, 40)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#c9d4e2"), 0.7)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#fff0dc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 260, 2, "#cfe6ff", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    room_angles()
    valley_angles()
prop_scene(); router(0, 0, 0, 1.0); camera((0.9, -2.2, 1.2), (0, 0, 0.18), lens=50, fstop=0)
still("router", 800, 700, 24, transparent=True, crop=True)
prop_scene(); eyeball(0, 0, 0.5, 0.5, name="eye_prop"); camera((0.35, -3.0, 0.9), (0, 0, 0.5), lens=50, fstop=0)
still("eye", 700, 700, 24, transparent=True, crop=True)
