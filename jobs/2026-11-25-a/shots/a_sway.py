# Hook: low angle up the tiered tower in a bright sky; the whole tower sways (exaggerated), wind streaks slide past,
# clouds drift; the camera pushes up the facade towards the top (moving 3D).
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-25-a/shots/towerkit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.15)
sky_set()
pv, top = tower(1.0)
swing(pv, 1, 3.0, 2.6, DUR, phase=0.6)
for k, (lx, ly, lz, s) in enumerate(((-6, 18, 13, 1.6), (5, 22, 15, 2.0), (-2, 30, 17, 2.4), (8, 12, 10, 1.2))):
    c = cloud((lx, ly, lz), s, f"cl{k}", seed=k + 1)
    key(c, 0, loc=(lx, ly, lz), ease="LINEAR"); key(c, DUR, loc=(lx + 1.2, ly, lz), ease="LINEAR")
wind(14, (-2.5, 1.5), (4, 10.5), DUR, speed=7.0)
cam, tgt = camera((2.6, -6.2, 1.0), (0, 0, 6.0), lens=22, fstop=0)
key(cam, 0, loc=(2.6, -6.2, 1.0)); key(cam, DUR, loc=(1.7, -5.4, 2.2))
key(tgt, 0, loc=(0, 0, 5.2)); key(tgt, DUR, loc=(0, 0, 8.0))
