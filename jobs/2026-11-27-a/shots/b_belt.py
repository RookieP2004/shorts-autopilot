# One returned box rides the roller conveyor through the warehouse; the camera tracks alongside it (moving 3D).
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-27-a/shots/returnskit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
warehouse()
rollers = conveyor(-8, 8, 0, z=0.8)
for r in rollers:
    spin(r, 400, axis=1)
rack(-3, 3.2, seed=11); rack(2.5, 3.2, seed=12); rack(7.5, 3.2, seed=13)
pallet_stack((-2.0, -2.2, 0), seed=5)
b = cbox((0.55, 0.5, 0.4), (-4.5, 0, 1.05), (0, 0, 4), name="hero")
b2 = cbox((0.45, 0.42, 0.3), (-6.2, 0, 1.0), (0, 0, -6), name="b2", labelled=False)
b3 = cbox((0.6, 0.5, 0.35), (-2.6, 0, 1.02), (0, 0, 8), name="b3")
for o, d in ((b, 4.5), (b2, 4.5), (b3, 4.5)):
    x, y, z = o.location
    key(o, 0, loc=(x, y, z), ease="LINEAR"); key(o, DUR, loc=(x + d, y, z), ease="LINEAR")
cam, tgt = camera((-5.6, -2.0, 1.5), (-4.5, 0, 1.0), lens=32, fstop=3.5)
key(cam, 0, loc=(-5.6, -2.0, 1.5), ease="LINEAR"); key(cam, DUR, loc=(-0.6, -1.6, 1.3), ease="LINEAR")
key(tgt, 0, loc=(-4.5, 0, 1.0), ease="LINEAR"); key(tgt, DUR, loc=(0.0, 0, 1.0), ease="LINEAR")
