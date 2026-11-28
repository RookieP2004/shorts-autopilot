# Round two: a 1930s army truck bounces through the wheat after the emus, and the emus pull away (moving 3D, tracking).
import os, math, random
exec(open(os.path.join(ROOT, "jobs/2026-11-28-b/shots/emukit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
wheat_field(seed=7, stalk_area=(-8, 26, -5.0, 7), n_stalks=12000, fence_y=12.0)
rnd = random.Random(4)
tr, body, wheels = truck()
v_truck = 3.6
key(tr, 0, loc=(-1.8, 3.0, 0), rot=(0, 0, 0), ease="LINEAR"); key(tr, DUR, loc=(-1.8 + v_truck * DUR, 3.0, 0), ease="LINEAR")
n = int(DUR / 0.12)
for i in range(n + 1):
    t = DUR * i / n
    key(body, t, loc=(0, 0, 0.06 * abs(math.sin(t * 11)) + rnd.uniform(0, 0.05)), rot=(rnd.uniform(-3, 3), rnd.uniform(-3, 3), 0), ease="LINEAR")
for w in wheels:
    key(w, 0, rot=(90, 0, 0), ease="LINEAR"); key(w, DUR, rot=(90, -math.degrees(v_truck * DUR / 0.45), 0), ease="LINEAR")
birds = flock(6, (1.4, 3.6, 2.3, 4.2), seed=12)
for i, (r, t, l, ph) in enumerate(birds):
    x0, y0 = r.location.x, r.location.y
    sp = rnd.uniform(4.3, 4.7)
    key(r, 0, loc=(x0, y0, 0), rot=(0, 0, rnd.uniform(-5, 5)), ease="LINEAR")
    key(r, DUR, loc=(x0 + sp * DUR, y0 + rnd.uniform(-0.6, 0.6), 0), rot=(0, 0, rnd.uniform(-5, 5)), ease="LINEAR")
    run_cycle(t, l, 0, DUR, period=0.34, phase=ph)
cam, tgt = camera((0.7, -5.6, 1.7), (0.7, 3.0, 1.25), lens=19, fstop=11.0)
key(cam, 0, loc=(0.7, -5.6, 1.7), ease="LINEAR"); key(cam, DUR, loc=(0.7 + 4.0 * DUR, -5.8, 1.8), ease="LINEAR")
key(tgt, 0, loc=(0.7, 3.0, 1.25), ease="LINEAR"); key(tgt, DUR, loc=(0.7 + 4.0 * DUR, 3.0, 1.25), ease="LINEAR")
