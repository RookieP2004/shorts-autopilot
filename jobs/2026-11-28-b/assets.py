# 2026-11-28-b: "Australia lost a war to emus" (wild-story; Librarian Ved pulls the 1932 file). Set: Ved's library aisle with
# tall shelves of books, warm hanging lamps, a red rug and a reading desk (ledger "FILE 1932", stack of books, rubber stamp,
# green banker's lamp). Plates: lib_wide (down the aisle), lib_desk (close on the desk), lib_low (low hero angle).
# Cut-outs: one emu (thumbnail / props), the ledger.
import math, os
exec(open(os.path.join(ROOT, "jobs/2026-11-28-b/shots/emukit.py")).read())


def drop_cams():
    for o in list(bpy.data.objects):
        if o.type == "CAMERA" or o.name.startswith("cam_target"):
            bpy.data.objects.remove(o)


reset(1080, 1920, 30, 0.1, samples=40, bloom=0.2, exposure=0.0)
library_set()
camera((0.0, -3.2, 1.55), (0.0, 4.0, 1.35), lens=22, fstop=8.0)
still("plate_lib_wide", 1080, 1920, 40)
drop_cams(); camera((0.6, -0.9, 1.55), (1.3, 0.45, 0.9), lens=30, fstop=4.0)
still("plate_lib_desk", 1080, 1920, 40)
drop_cams(); cam, _ = camera((-0.9, -2.2, 0.5), (0.2, 3.0, 1.9), lens=22, fstop=6.0)
dutch(cam, 4)
still("plate_lib_low", 1080, 1920, 40)

# cut-outs
reset(800, 800, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.3, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0.9), 450, 3, "#fff0dc", "k")
area_light((2.5, 2.5, 2), (0, 0, 0.9), 350, 2, "#dbe8ff", "r")
r, t, l = emu(1.0, "hero", seed=4)
r.rotation_euler = (0, 0, math.radians(-30))
for pv, ph in l:
    pv.rotation_euler = (0, math.radians(18 if ph == 0 else -14), 0)
sprite_camera((0, 0, 0.95), dist=4.2, height=1.1, lens=50, azimuth=-15)
still("emu", 800, 800, 40, transparent=True, crop=True)

reset(800, 800, samples=40, transparent=True, bloom=0.2)
world_hdri("studio", 0.6, backdrop=None)
area_light((-2, -3, 3), (0, 0, 0), 600, 3, "#fff0dc", "k")
plane(0.62, 0.4, (0, 0, 0.028), (0, 0, 0), material=paper(ledger_tex()), name="ledger")
box((0.66, 0.44, 0.03), (0, 0, 0.01), (0, 0, 0), material=M("ledgercover", "#3a1f14", rough=0.6), bevel=0.003)
sprite_camera((0, 0, 0.02), dist=1.4, height=1.0, lens=50, azimuth=-10)
still("ledger", 800, 800, 40, transparent=True, crop=True)
