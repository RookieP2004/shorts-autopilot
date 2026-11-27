# The tossed quarter: boxes tumble off the end of the conveyor into a big skip in front of a landfill heap of returns;
# the camera pushes in and drops low (moving 3D).
import os, math
exec(open(os.path.join(ROOT, "jobs/2026-11-27-a/shots/returnskit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
warehouse(floor_c="#7d7f85")
rollers = conveyor(-6, 0.0, 0, z=1.6)
for r in rollers:
    spin(r, 400, axis=1)
skip_bin((1.6, 0, 0))
heap((1.6, 0, 0.4), radius=1.3, n=30, seed=31, height=0.9, name="in")
heap((1.5, 6.5, 0), radius=5.0, n=150, seed=32, height=3.4, name="far")
import random
rnd = random.Random(4)
for i in range(6):
    o = cbox((0.5, 0.45, 0.36), (-4.0 - i * 0.9, 0, 1.85), (0, 0, rnd.uniform(-8, 8)), name=f"f{i}", labelled=i % 2 == 0)
    t_edge = 0.3 + i * 0.6                                       # time it reaches the end of the belt
    x0 = -4.0 - i * 0.9
    speed = 2.2
    tx = (0.0 - x0) / speed
    key(o, 0, loc=(x0, 0, 1.85), rot=(0, 0, 0), ease="LINEAR")
    if tx < DUR:
        key(o, tx, loc=(0.0, 0, 1.85), rot=(0, 0, 0), ease="LINEAR")
        tl = min(DUR, tx + 0.55)
        key(o, tl, loc=(1.3 + rnd.uniform(-0.3, 0.4), rnd.uniform(-0.4, 0.4), 1.15), rot=(rnd.uniform(40, 110), rnd.uniform(-40, 40), 0), ease="EASE_IN")
    else:
        key(o, DUR, loc=(x0 + speed * DUR, 0, 1.85), ease="LINEAR")
cam, tgt = camera((-2.2, -5.5, 2.6), (0.6, 0, 1.4), lens=28, fstop=4.5)
key(cam, 0, loc=(-2.2, -5.5, 2.6)); key(cam, DUR, loc=(-0.4, -3.4, 1.2))
key(tgt, 0, loc=(0.6, 0, 1.4)); key(tgt, DUR, loc=(1.4, 1.5, 1.4))
