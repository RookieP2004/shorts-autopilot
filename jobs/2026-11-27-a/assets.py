# 2026-11-27-a: "Where do your returns go?" (scale-shock; Detective Ved tails one returned box through a returns warehouse).
# Set: the returns warehouse. Racks of boxes, a roller conveyor, pallets, and Ved's inspection table with an open box, a
# case-file folder and a gold magnifier. Plates: wh_wide, wh_table (closer on the table), wh_low (low hero angle).
# Cut-outs: magnifier, returned box, case folder.
import math, os
A = ASSETS
exec(open(os.path.join(ROOT, "jobs/2026-11-27-a/shots/returnskit.py")).read())


def table_set():
    reset(1080, 1920, 30, 0.1, samples=40, bloom=0.15, exposure=-0.1)
    warehouse()
    rack(-3.2, 4.2, seed=41); rack(1.6, 4.2, seed=42); rack(6.4, 4.2, seed=43)
    conveyor(-6, 6, 2.2, z=0.8)
    for i, x in enumerate((-4.2, -1.8, 1.0, 3.6)):
        cbox((0.5, 0.45, 0.36), (x, 2.2, 1.03), (0, 0, 5 * i), name=f"cvb{i}", labelled=i % 2 == 0)
    pallet_stack((4.2, 0.6, 0), seed=44, wrap=False)
    # inspection table (steel top, blue legs)
    top = box((2.0, 0.9, 0.06), (-1.3, 0.6, 0.86), material=metal("#c9ced6", 0.35, "tbl"), bevel=0.01, name="tabletop")
    for sx in (-2.2, -0.4):
        for sy in (0.25, 0.95):
            box((0.06, 0.06, 0.86), (sx, sy, 0.43), material=mat("tleg", "#2f5f9a", rough=0.4, metal=0.4), bevel=0.004)
    # open returned box (flaps up)
    cbox((0.56, 0.46, 0.34), (-1.6, 0.6, 1.06), (0, 0, 8), name="openbox")
    for k, (dx, ry) in enumerate(((-0.28, -55), (0.28, 55))):
        box((0.02, 0.44, 0.24), (-1.6 + dx * 1.05, 0.6, 1.3), (0, ry, 8), material=plain_card("flap", "#b8885a"), bevel=0.003)
    # case-file folder + magnifier
    box((0.42, 0.3, 0.02), (-0.75, 0.55, 0.9), (0, 0, -12), material=mat("folder", "#e8c98a", rough=0.8), bevel=0.004, name="folder")
    box((0.3, 0.04, 0.005), (-0.78, 0.48, 0.913), (0, 0, -12), material=mat("folder_tab", "#d6483e", rough=0.6), bevel=0)
    mg = magnifier((-0.6, 0.75, 0.93))
    for o in mg:
        o.rotation_euler = (math.radians(0), 0, math.radians(30))
        o.location.z = 0.92
    mg[0].rotation_euler = (0, 0, math.radians(30)); mg[1].rotation_euler = (0, 0, math.radians(30))
    spot_light((-1.3, 0.2, 3.4), (-1.3, 0.6, 0.9), 900, 40, 0.3, 0.1, "#ffe9c2", "tspot")
    return top


def drop_cams():
    for o in list(bpy.data.objects):
        if o.type == "CAMERA" or o.name.startswith("cam_target"):
            bpy.data.objects.remove(o)


table_set()
camera((0.0, -4.6, 1.6), (0.0, 1.5, 1.2), lens=24, fstop=8.0)
still("plate_wh_wide", 1080, 1920, 40)
drop_cams(); camera((-1.0, -1.4, 1.75), (-1.3, 0.8, 1.0), lens=30, fstop=4.0)
still("plate_wh_table", 1080, 1920, 40)
drop_cams(); cam, _ = camera((2.0, -2.6, 0.45), (-0.3, 1.5, 1.3), lens=24, fstop=5.0)
dutch(cam, 4)
still("plate_wh_low", 1080, 1920, 40)

# cut-outs
reset(700, 700, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.6, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0), 600, 3, "#fff0dc", "k")
area_light((2.5, 2.5, 2), (0, 0, 0), 300, 2, "#dbe8ff", "r")
mg = magnifier((0, 0, 0))
camera((0.3, -3.0, 0.2), (0.1, 0, -0.15), lens=50, fstop=0)
still("magnifier", 700, 700, 40, transparent=True, crop=True)

reset(700, 700, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.6, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0.3), 600, 3, "#fff0dc", "k")
area_light((2.5, 2.5, 2), (0, 0, 0.3), 300, 2, "#dbe8ff", "r")
cbox((0.56, 0.46, 0.4), (0, 0, 0.2), (0, 0, 20), name="rbox")
sprite_camera((0, 0, 0.2), dist=2.4, height=1.2, lens=50, azimuth=-25)
still("returnbox", 700, 700, 40, transparent=True, crop=True)
