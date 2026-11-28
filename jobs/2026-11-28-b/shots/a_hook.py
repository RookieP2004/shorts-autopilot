# Hook: a mob of emus sprints straight at a low camera through golden Western Australian wheat (moving 3D).
import os, math, random
exec(open(os.path.join(ROOT, "jobs/2026-11-28-b/shots/emukit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
wheat_field(seed=3, stalk_area=(-8, 8, -7.5, 16), n_stalks=10000, fence_y=26.0)
rnd = random.Random(8)
birds = flock(11, (-2.2, 2.2, 2.8, 8.0), seed=6)
for i, (r, t, l, ph) in enumerate(birds):
    x0, y0 = r.location.x, r.location.y
    sp = rnd.uniform(1.2, 1.5)
    x1 = x0 * 0.6 + rnd.uniform(-0.6, 0.6)
    y1 = y0 - sp * DUR
    key(r, 0, loc=(x0, y0, 0), rot=(0, 0, -90 + rnd.uniform(-6, 6)), ease="LINEAR")
    key(r, DUR, loc=(x1, y1, 0), rot=(0, 0, -90 + rnd.uniform(-6, 6)), ease="LINEAR")
    run_cycle(t, l, 0, DUR, period=rnd.uniform(0.36, 0.42), phase=ph)
cam, tgt = camera((0.5, -3.4, 1.0), (0, 6, 1.4), lens=30, fstop=5.6)
key(cam, 0, loc=(0.5, -3.4, 1.0)); key(cam, DUR, loc=(0.8, -5.8, 1.15))
key(tgt, 0, loc=(0, 6, 1.4)); key(tgt, DUR, loc=(0.2, 1.0, 1.3))
