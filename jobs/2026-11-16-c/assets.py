# 2026-11-16-c: "Money laundering isn't named after Capone's laundromats" (dark-files, myth-bust hook).
# Sets: a 1920s city street at dusk (brick shopfronts in palette colours, a glowing LAUNDRY shop with a striped awning and
# washers in the window, gas lamps, crates, potted shrubs), 2 angles (wide, mid on the shop); the 1910 Treasury basement
# (cream tiles, a big brass-and-wood money-washing machine with rollers, trays and stacks of banknotes, hanging lamps),
# 2 angles (wide, close on the rollers); a tax agent's desk (green lamp, an open ledger, papers), 1 angle.
# Cut-outs: a banknote, the ledger.
import math, os, random

# dusk_sky(), bush(), tree(), drop_cams(), seg() ... (frozen helpers)
_src = open(os.path.join(ROOT, "jobs/2026-11-13-c/assets.py")).read().split("\nif not os.environ.get")[0]
exec(compile(_src, "c13_helpers", "exec"), globals())

NOTE = os.path.join(TEX, "note_1.png")


def drop_cams():
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(o)


def pt(loc, power=60, color="#ffcf8a", radius=0.1, name="pt"):
    d = bpy.data.lights.new(name, "POINT"); d.energy = power; d.color = hexrgb(color); d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    return o


def washer(x, y, glow=False, name="washer"):
    body = box((0.7, 0.65, 0.88), (x, y, 0.44), material=mat("washer_white", "#e9e6df", rough=0.3, coat=0.4), bevel=0.04, name=name)
    torus(0.24, 0.035, (x, y - 0.36, 0.47), (90, 0, 0), metal("#c8ccd0", 0.25, "chrome"))
    drum_m = mat("drum_glow" if glow else "drum", "#2a3a44", rough=0.4, metal=0.6,
                 emit="#7fd3ff" if glow else None, emit_strength=5.0 if glow else 0)
    cylinder(0.205, 0.02, (x, y - 0.33, 0.47), (90, 0, 0), drum_m, verts=48)
    box((0.6, 0.02, 0.1), (x, y - 0.33, 0.8), material=mat("wpanel", "#bfc3c6", rough=0.4), bevel=0.01)
    return body


def gas_lamp(x, y):
    iron = metal("#2b2f36", 0.45, "iron")
    cylinder(0.06, 3.2, (x, y, 1.6), material=iron, verts=20)
    cylinder(0.14, 0.2, (x, y, 0.1), material=iron, verts=24)
    box((0.3, 0.3, 0.42), (x, y, 3.42), material=mat("lampglass", "#ffe2a0", emit="#ffc35a", emit_strength=12.0), bevel=0.03)
    cone(0.26, 0.2, (x, y, 3.72), material=iron)
    pt((x, y - 0.1, 3.4), 160, "#ffb35a", 0.2, "gaslamp")


def crate(x, y, rot=0, h=0.4):
    box((0.6, 0.45, h), (x, y, h / 2), (0, 0, rot), wood("#b8864e", "#8a6036", "crate", 4.0), bevel=0.025)


def shopfront(x, y, w, h, color, trim="#f6efe2", sign=None, sign_col="#7c2533", awning=None, inside=None, glow="#ffd27a"):
    brick = mat(f"bld_{color}", color, rough=0.85, noise_bump=0.12)
    box((w, 3.0, h), (x, y + 2.7, h / 2), material=brick, bevel=0.04)                     # body, set back
    ww = w - 1.4; wc = x - 0.3; zl, zh = 0.5, 2.3                                           # shop window opening
    box((w, 0.24, h - zh), (x, y + 0.12, (h + zh) / 2), material=brick, bevel=0.03)         # facade above the window
    box((w, 0.24, zl), (x, y + 0.12, zl / 2), material=brick, bevel=0.03)                   # sill wall
    lx = wc - ww / 2
    box((lx - (x - w / 2), 0.24, zh - zl), ((x - w / 2 + lx) / 2, y + 0.12, (zl + zh) / 2), material=brick, bevel=0.02)
    rx = wc + ww / 2
    box((x + w / 2 - rx, 0.24, zh - zl), ((x + w / 2 + rx) / 2, y + 0.12, (zl + zh) / 2), material=brick, bevel=0.02)
    for sx in (-1, 1):                                                                      # side walls of the shop
        box((0.1, 1.2, h), (x + sx * (w / 2 - 0.05), y + 0.6, h / 2), material=brick, bevel=0)
    trim_m = mat(f"trim_{trim}", trim, rough=0.6)
    box((w + 0.16, 3.2, 0.22), (x, y + 1.6, h + 0.05), material=trim_m, bevel=0.05)          # cornice
    box((w + 0.06, 0.12, 0.16), (x, y - 0.02, 2.75), material=trim_m, bevel=0.03)            # sign band edge
    # shop window: frame bars, glass, a lit interior behind
    fr = mat("wframe", "#3a2a22", rough=0.5)
    box((ww + 0.12, 0.1, 0.08), (wc, y - 0.02, zh), material=fr, bevel=0.01); box((ww + 0.12, 0.1, 0.08), (wc, y - 0.02, zl), material=fr, bevel=0.01)
    for bx in (lx, wc, rx):
        box((0.07, 0.1, zh - zl), (bx, y - 0.02, (zl + zh) / 2), material=fr, bevel=0.01)
    box((w - 0.2, 0.05, h), (x, y + 1.18, h / 2), material=mat(f"interior_{glow}", "#f3dfb8", emit=glow, emit_strength=0.55), bevel=0)
    box((w - 0.2, 1.2, 0.05), (x, y + 0.6, 0.02), material=mat("shopfloor", "#c9b7a0", rough=0.6), bevel=0)
    pt((wc, y + 0.5, 2.1), 60, "#ffe2b0", 0.6, "shop_in")
    # door
    box((0.8, 0.12, 2.1), (x + w / 2 - 0.55, y - 0.02, 1.05), material=wood("#6b4529", "#4a2e1a", "door", 3.0), bevel=0.03)
    sphere(0.04, (x + w / 2 - 0.85, y - 0.1, 1.05), 1, metal("#d9a441", 0.3, "knob"), seg=12)
    # upper windows
    win = mat("upwin", "#ffd27a", emit="#ffb64a", emit_strength=2.5)
    for k in range(max(1, int(w // 1.4))):
        wx = x - w / 2 + 0.8 + k * 1.4
        for wz in (3.6, 4.9):
            if wz + 0.5 < h:
                box((0.7, 0.08, 0.9), (wx, y - 0.02, wz), material=trim_m, bevel=0.02)
                box((0.55, 0.1, 0.75), (wx, y - 0.03, wz), material=win if (k + int(wz)) % 2 else mat("darkwin", "#34425c", rough=0.2, coat=0.6), bevel=0.01)
    if awning:
        aw = paper(os.path.join(TEX, awning), 0.6, f"aw_{awning}")
        box((w - 0.3, 1.3, 0.05), (x, y - 0.6, 2.45), (22, 0, 0), material=aw, bevel=0.015)
    if sign:
        box((w - 0.5, 0.1, 0.62), (x, y - 0.07, 3.08), material=mat(f"signb_{sign_col}", sign_col, rough=0.5), bevel=0.03)
        text3d(sign, 0.5, (x, y - 0.14, 3.08), (90, 0, 0), mat("signink", "#f6efe2", emit="#fff3d8", emit_strength=3.0), font="display", extrude=0.02)
    if inside == "washers":
        for i in range(3):
            washer(x - 0.25 - 0.85 + i * 0.85, y + 0.75, glow=(i == 1), name=f"sw{i}")
        pt((x - 0.25, y + 0.4, 2.0), 120, "#ffe2b0", 0.4, "shoplight")


def build_street():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    dusk_sky(top="#2a3a7a", mid="#c27a8a", horizon="#ffbf78")
    plane(200, 200, (0, 20, 0), material=mat("cobble", "#6b625c", rough=0.8, noise_bump=0.35), name="road")
    box((40, 2.2, 0.16), (0, -0.6, 0.08), material=mat("pavement", "#b9ab98", rough=0.8, noise_bump=0.1), bevel=0.02)
    shopfront(-5.6, 0.6, 3.4, 6.2, "#46965a", sign="BAKERY", sign_col="#f2b04a", awning="awning_green.png", glow="#ffd9a0")
    shopfront(-1.6, 0.6, 4.4, 5.6, "#b5533c", sign="LAUNDRY", sign_col="#34425c", awning="awning_blue.png", inside="washers", glow="#d8f0ff")
    shopfront(2.6, 0.6, 3.6, 6.8, "#c9a24a", sign="BARBER", sign_col="#7c2533", awning="awning_stripes.png", glow="#ffd9a0")
    shopfront(6.6, 0.6, 3.8, 5.8, "#6fc3c0", glow="#ffe0b0")
    for gx in (-3.6, 0.9, 4.6):
        gas_lamp(gx, -1.25)
    crate(-3.0, -0.5, 0.2); crate(-3.0, -0.5, -0.1, 0.8)
    bush(1.6, -0.6, 0.45, "#2f6b45", "#e8857c", 41)
    bush(-6.8, -0.6, 0.5, "#2c6340", "#f6efe2", 42)
    for k, (bx, by, h) in enumerate(((-12, 18, 14), (-5, 22, 18), (3, 20, 15), (11, 19, 17), (18, 23, 13))):
        box((5, 4, h), (bx, by, h / 2), material=mat(f"far{k}", "#7f86b8", rough=1.0), bevel=0.1)
    area_light((-8, -9, 9), (0, 1, 1.5), 1300, 8, "#ffd2a0", "key")
    area_light((8, -6, 4), (0, 1, 1.5), 380, 6, "#a9c4ff", "fill")


def street_angles():
    build_street()
    drop_cams(); camera((0.4, -11.5, 1.7), (0.0, 1.0, 2.6), lens=26, fstop=8.0)
    still("plate_street_wide", 1080, 1920, 40)
    drop_cams(); camera((-1.0, -6.4, 1.45), (-1.4, 0.6, 1.9), lens=30, fstop=4.0)
    still("plate_street_mid", 1080, 1920, 40)


# ------------------------------------------------------------------ the 1910 Treasury basement and its money washer
def note_mat():
    return paper(NOTE, 0.6, "note_paper")


def money_machine(x, y):
    brass = metal("#d9a441", 0.28, "mbrass"); iron = mat("miron", "#34425c", rough=0.35, metal=0.6, coat=0.3)
    oak = wood("#9a6a44", "#6b4529", "moak", 4.0, 0.55)
    box((2.6, 1.2, 0.9), (x, y, 0.45), material=oak, bevel=0.05)                       # wooden base cabinet
    box((2.7, 1.3, 0.08), (x, y, 0.92), material=brass, bevel=0.02)
    for sx in (-1.15, 1.15):                                                           # iron side frames
        box((0.14, 1.0, 1.4), (x + sx, y, 1.6), material=iron, bevel=0.04)
    for k, z in enumerate((1.25, 1.55, 1.85, 2.15)):                                  # wash + press rollers
        cylinder(0.13 if k % 2 else 0.16, 2.2, (x, y - 0.05 + (0.06 if k % 2 else 0), z), (0, 90, 0),
                 mat(f"roll{k}", "#f6efe2" if k % 2 else "#c8ccd0", rough=0.3, metal=0.0 if k % 2 else 0.6), verts=40, bevel=0.01)
    cylinder(0.5, 0.14, (x + 1.35, y - 0.1, 1.7), (0, 90, 0), brass, verts=48)          # flywheel
    torus(0.42, 0.04, (x + 1.43, y - 0.1, 1.7), (0, 90, 0), brass)
    box((1.9, 0.8, 0.16), (x, y - 0.75, 1.02), (0, 0, 0), mat("tray_water", "#7fc6d8", rough=0.05, coat=0.8), bevel=0.03)  # soap tray
    box((2.0, 0.9, 0.12), (x, y - 0.75, 0.96), material=brass, bevel=0.02)
    for k in range(5):                                                                 # bubbles
        sphere(0.07 + 0.03 * (k % 3), (x - 0.7 + k * 0.35, y - 0.78, 1.13), 1, glass("#dff6ff", 0.02, "bubble"), seg=16)
    nm = note_mat()
    for k in range(4):                                                                 # notes going through the rollers
        banknote(NOTE, (x - 0.75 + k * 0.5, y - 0.28, 1.42), (60, 0, 0), 0.34, f"mnote{k}")
    text3d("U.S. TREASURY", 0.16, (x, y - 0.62, 0.55), (90, 0, 0), brass, font="serif", extrude=0.01)
    return nm


def note_stack(x, y, n=12, rot=0, name="stk"):
    for k in range(n):
        banknote(NOTE, (x, y, 0.95 + k * 0.006), (0, 0, rot + random.uniform(-3, 3)), 0.32, f"{name}{k}")


def hanging_lamp(x, y, z, shade="#46965a", power=300, color="#ffd6a0"):
    lathe([(0, 0.0), (0.32, 0.0), (0.12, 0.22), (0.03, 0.26), (0, 0.26)], 40, (x, y, z), mat(f"shade_{shade}", shade, rough=0.35, metal=0.3), 1, "shade")
    cylinder(0.006, 2.0, (x, y, z + 1.25), material=mat("cord", "#111111"), verts=8, bevel=0)
    sphere(0.07, (x, y, z + 0.02), 1, mat("bulb", "#fff1d0", emit="#ffd9a0", emit_strength=20.0), seg=16)
    pt((x, y, z - 0.15), power, color, 0.15, "lamp")


def build_treasury():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.25)
    world_color(hexrgb("#e9dcc4"), 0.25)
    plane(30, 30, (0, 0, 0), material=wood("#8a5a30", "#5e3a1c", "tfloor", 2.0), name="floor")
    box((30, 0.3, 7), (0, 2.6, 3.5), material=mat("tilewall", "#e3cfa6", rough=0.5, coat=0.3), bevel=0)
    box((30, 0.32, 2.0), (0, 2.58, 1.0), material=mat("wainscot", "#46965a", rough=0.45, coat=0.4), bevel=0)
    for px in (-4.2, 4.2):
        box((0.5, 0.5, 7), (px, 2.3, 3.5), material=mat("pillar", "#d9c99a", rough=0.6), bevel=0.04)
    money_machine(0.0, 1.0)
    oak = wood("#a8743f", "#7a4e2a", "toak", 5.0)
    box((1.8, 0.9, 0.9), (-2.7, 0.2, 0.45), material=oak, bevel=0.04)                  # sorting table
    random.seed(4)
    note_stack(-3.1, 0.1, 12, 10, "dirty"); note_stack(-2.4, 0.3, 9, -8, "dirty2")
    box((1.6, 0.9, 0.9), (2.9, 0.1, 0.45), material=oak, bevel=0.04)                   # clean pile
    note_stack(2.6, 0.0, 16, 2, "clean"); note_stack(3.2, 0.2, 14, -4, "clean2")
    box((0.62, 0.42, 0.3), (3.0, -0.8, 0.15), material=wood("#c99a5b", "#9c7040", "basket", 20.0, 0.7), bevel=0.05)
    for hx in (-2.6, 0.0, 2.6):
        hanging_lamp(hx, 0.4, 3.6)
    text3d("BUREAU OF ENGRAVING", 0.34, (0, 2.42, 4.6), (90, 0, 0), metal("#c9a24a", 0.3, "wallsign"), font="serif", extrude=0.03)
    area_light((-4, -6, 6), (0, 1, 1.2), 800, 6, "#ffe2c2", "key")
    area_light((5, -3, 3), (0, 1, 1.2), 450, 4, "#bcd6ff", "fill")


def treasury_angles():
    build_treasury()
    drop_cams(); camera((0.5, -5.4, 1.7), (0.0, 1.0, 1.75), lens=30, fstop=6.0)
    still("plate_treasury_wide", 1080, 1920, 40)
    drop_cams(); camera((-0.5, -2.6, 1.75), (0.0, 0.8, 1.35), lens=32, fstop=2.8, focus=3.45)
    still("plate_treasury_close", 1080, 1920, 40)


# ------------------------------------------------------------------ the tax agent's desk
def ledger(x, y, z, rot=0, name="ledger"):
    cover = mat("ledger_cover", "#7c2533", rough=0.5)
    box((0.9, 0.62, 0.04), (x, y, z + 0.02), (0, 0, rot), cover, bevel=0.01, name=name)
    pg = paper(os.path.join(ROOT, "jobs/2026-11-16-c/ledger_page.png"), 0.7, "ledger_page")
    for sx, rr in ((-0.215, 4), (0.215, -4)):
        box((0.42, 0.58, 0.035), (x + sx * math.cos(math.radians(rot)), y + sx * math.sin(math.radians(rot)), z + 0.055),
            (0, rr, rot), pg, bevel=0.004)
    cylinder(0.02, 0.6, (x, y, z + 0.07), (90, 0, rot), cover, verts=12)


def desk_angles():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.3)
    world_color(hexrgb("#2b2440"), 0.5)
    plane(30, 30, (0, 0, 0), material=wood("#6b4529", "#4a2e1a", "floorboards", 2.0), name="floor")
    box((30, 0.3, 7), (0, 2.4, 3.5), material=mat("officewall", "#34425c", rough=0.7), bevel=0)
    box((3.4, 1.6, 0.08), (0, 0.3, 0.86), material=wood("#9a6a44", "#6b4529", "desktop", 4.0), bevel=0.03)
    box((3.2, 1.4, 0.82), (0, 0.35, 0.41), material=wood("#7a4e2a", "#5a3a20", "deskbody", 3.0), bevel=0.04)
    ledger(0.0, 0.1, 0.9, 0)
    for k in range(5):
        box((0.42, 0.3, 0.006), (-1.1 + k * 0.05, 0.45 + k * 0.03, 0.905 + k * 0.006), (0, 0, k * 6 - 12),
            paper(os.path.join(ROOT, "jobs/2026-11-16-c/ledger_page.png"), 0.7, "slip"), bevel=0.001)
    # banker's lamp
    brass = metal("#d9a441", 0.28, "lbrass")
    cylinder(0.14, 0.04, (1.1, 0.5, 0.92), material=brass, verts=32)
    cylinder(0.02, 0.45, (1.1, 0.5, 1.15), material=brass, verts=12)
    cylinder(0.12, 0.6, (1.0, 0.45, 1.38), (0, 90, 15), mat("lampgreen", "#46965a", rough=0.15, coat=0.8), verts=32)
    pt((1.0, 0.3, 1.25), 90, "#ffd6a0", 0.1, "desklamp")
    cylinder(0.04, 0.12, (-0.9, -0.15, 0.96), material=metal("#2b2f36", 0.3, "inkpot"), verts=24)
    cylinder(0.012, 0.3, (0.55, -0.1, 0.93), (0, 90, 30), mat("pen", "#1a1410", rough=0.3), verts=12)
    box((1.4, 0.06, 1.0), (-0.6, 2.22, 2.6), material=mat("frame", "#c9a24a", rough=0.4, metal=0.5), bevel=0.02)
    box((1.2, 0.07, 0.8), (-0.6, 2.2, 2.6), material=mat("picture", "#efe3cf", rough=0.7), bevel=0.01)
    text3d("WANTED: RECEIPTS", 0.13, (-0.6, 2.15, 2.6), (90, 0, 0), mat("pink", "#7c2533"), font="display", extrude=0.005)
    area_light((-3, -4, 5), (0, 0.2, 0.9), 900, 4, "#ffe2c2", "key")
    area_light((3, -2, 2.5), (0, 0.2, 0.9), 220, 3, "#9fb4ff", "fill")
    drop_cams(); camera((0.0, -2.9, 2.2), (0.0, 0.3, 0.95), lens=30, fstop=3.2, focus=3.3)
    still("plate_desk", 1080, 1920, 40)


def prop_scene():
    reset(800, 800, 30, 0.1, samples=24, bloom=0)
    world_color(hexrgb("#dfeaf2"), 0.6)
    area_light((-2.5, -3, 3.5), (0, 0, 0.3), 380, 2.5, "#ffe0bc", "key"); area_light((2.5, 2.5, 2.5), (0, 0, 0.3), 220, 2, "#9fc0e8", "rim")


if not os.environ.get("BK_PROPS_ONLY"):
    street_angles()
    treasury_angles()
    desk_angles()
prop_scene(); banknote(NOTE, (0, 0, 0.1), (70, 0, 0), 0.6, "hero_note", bend=12); sprite_camera((0, 0, 0.1), 1.6, 0.3, 50, azimuth=-15)
still("note", 600, 400, 24, transparent=True, crop=True)
prop_scene(); ledger(0, 0, 0, 0, "hero_ledger"); sprite_camera((0, 0, 0.05), 1.8, 1.0, 50, azimuth=-15)
still("ledger", 600, 500, 24, transparent=True, crop=True)
