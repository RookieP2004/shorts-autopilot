# 2026-11-21-L Deep Dive (16:9): "Why Doctors Refused to Wash Their Hands".
# Sets at 1920x1080, re-shot from the Semmelweis Short (jobs/2026-11-18-a): the 1840s maternity ward of the First Clinic
# (wide down the aisle, mid by a bed, a low close on one bed), the Second Clinic (same hall, green blankets, warmer light),
# the washstand with the chlorine bowl, the dissection hall in the night mood (wide + a tight hero angle).
# The 1860s lab (Pasteur / Lister / Koch reconstructions) and the present-day town cafe are reused from jobs/2026-11-14-L.
import math, os, random

_src = open(os.path.join(ROOT, "jobs/2026-11-18-a/assets.py")).read().split('\nif not os.environ.get("BK_PROPS_ONLY"):')[0]
exec(compile(_src, "ward_helpers", "exec"), globals())

W, H = 1920, 1080


def landscape(samples=40):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = W, H


def ward16(second=False):
    ward()
    landscape()
    if second:
        # the midwives' clinic: green blankets, a warmer afternoon sun
        for nm, col in (("blanket_a", "#4f8f5a"), ("blanket_b", "#6fae78")):
            m = bpy.data.materials.get(nm)
            if m and m.node_tree:
                for n in m.node_tree.nodes:
                    if n.type == "BSDF_PRINCIPLED":
                        n.inputs["Base Color"].default_value = (*hexrgb(col), 1.0)
        s = bpy.data.objects.get("sun")
        if s:
            s.data.color = hexrgb("#ffd49a"); s.data.energy = 3.8
        drop_cams(); camera((0.9, -3.2, 1.6), (-0.4, 8.0, 1.15), lens=26, fstop=8.0)
        still("plate_ward2_wide", W, H, 40)
        return
    drop_cams(); camera((0.0, -3.4, 1.65), (0, 8.0, 1.2), lens=24, fstop=8.0)
    still("plate_ward_wide", W, H, 40)
    drop_cams(); camera((-0.2, 0.6, 1.45), (-2.4, 5.6, 0.85), lens=28, fstop=4.0)
    still("plate_ward_mid", W, H, 40)
    drop_cams(); camera((0.9, 4.6, 0.95), (-2.35, 5.6, 0.7), lens=32, fstop=2.6)
    still("plate_ward_bed", W, H, 40)


def wash16():
    wash_set()
    landscape()
    drop_cams(); camera((0.2, -2.1, 1.5), (-0.05, 0.35, 1.0), lens=36, fstop=3.2)
    still("plate_wash", W, H, 40)
    drop_cams(); camera((-0.35, -0.75, 1.32), (-0.1, 0.35, 1.0), lens=40, fstop=2.2)
    still("plate_wash_close", W, H, 44)


def dissect16():
    dissection()
    landscape()
    # a stand under the oil lamp (it floated in the landscape frame) and a back wall of tiles far behind
    cylinder(0.2, 0.86, (-1.55, -0.2, 0.43), material=wood("#5a3a22", "#3a2414", "lstand", 3.0), verts=24)
    drop_cams()
    cam, _ = camera((1.2, -5.2, 2.1), (0, 0.1, 0.95), lens=30, fstop=2.4)
    dutch(cam, 4)
    still("plate_dissect", W, H, 40)
    drop_cams()
    cam, _ = camera((-2.3, -2.2, 1.75), (-0.5, 0.0, 0.98), lens=34, fstop=2.0)
    dutch(cam, 6)
    still("plate_dissect_close", W, H, 40)


only = os.environ.get("BK_ONLY", "")
for name, fn in (("ward", ward16), ("ward2", lambda: ward16(True)), ("wash", wash16), ("dissect", dissect16)):
    if not only or name in only.split(","):
        fn()
