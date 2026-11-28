# Round one: from above, a tight mob of emus bursts apart into small groups running every way (moving 3D).
import os, math, random
exec(open(os.path.join(ROOT, "jobs/2026-11-28-b/shots/emukit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
wheat_field(seed=5, stalk_area=(-6, 6, -6, 7), n_stalks=5000, fence_y=16.0)
rnd = random.Random(3)
dirs = [(-1, 1), (1, 1), (-1, -0.6), (1, -0.6)]
birds = flock(12, (-2.0, 2.0, -1.6, 2.2), seed=9)
for i, (r, t, l, ph) in enumerate(birds):
    dx, dy = dirs[i % 4]
    x0, y0 = r.location.x, r.location.y
    ang = math.degrees(math.atan2(dy, dx))
    go = 0.5 + 0.1 * (i % 3)
    d = rnd.uniform(4.5, 5.5)
    n = math.hypot(dx, dy)
    key(r, 0, loc=(x0, y0, 0), rot=(0, 0, ang + rnd.uniform(-20, 20)), ease="LINEAR")
    key(r, go, loc=(x0, y0, 0), rot=(0, 0, ang), ease="EASE_OUT")
    key(r, DUR, loc=(x0 + dx / n * d, y0 + dy / n * d, 0), rot=(0, 0, ang + rnd.uniform(-8, 8)), ease="EASE_IN")
    run_cycle(t, l, 0, DUR, period=0.38, phase=ph)
cam, tgt = camera((0, -6.0, 6.5), (0, 0.4, 0.6), lens=30, fstop=8.0)
key(cam, 0, loc=(0, -5.5, 6.0)); key(cam, DUR, loc=(0.3, -7.0, 7.8))
key(tgt, 0, loc=(0, 0.4, 0.6)); key(tgt, DUR, loc=(0, 0.8, 0.4))
