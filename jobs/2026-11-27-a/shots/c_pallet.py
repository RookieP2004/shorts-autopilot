# Liquidation: boxes drop onto a pallet stack, which gets a red SOLD tag; the camera orbits (moving 3D).
import os, math
exec(open(os.path.join(ROOT, "jobs/2026-11-27-a/shots/returnskit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
warehouse()
pallet_stack((0, 0, 0), seed=21, layers=2, wrap=False)
pallet_stack((-1.6, 1.6, 0), seed=22, layers=3)
pallet_stack((1.7, 1.4, 0), seed=23, layers=3)
rack(-4, 5, seed=24); rack(4, 5, seed=25)
drops = []
for i, (dx, dy) in enumerate(((-0.29, -0.27), (0.29, -0.27), (-0.29, 0.27), (0.29, 0.27))):
    o = cbox((0.56, 0.52, 0.38), (dx, dy, 3.5), (0, 0, 3 * i), name=f"d{i}", labelled=i % 2 == 0)
    t0 = 0.25 + i * 0.45
    key(o, 0, loc=(dx, dy, 3.5)); key(o, t0, loc=(dx, dy, 3.5), ease="LINEAR")
    key(o, t0 + 0.38, loc=(dx, dy, 0.16 + 0.19 + 0.8), ease="EASE_IN")
tag = box((0.5, 0.02, 0.3), (0, -0.56, 0.9), (0, 0, 0), mat("sold", "#d6483e", rough=0.5), bevel=0.01, name="tag")
pop_in(tag, 2.4)
cam, tgt = camera((-2.6, -3.4, 1.9), (0, 0, 0.9), lens=32, fstop=4.0)
for i in range(7):
    a = math.radians(-38 + 50 * i / 6)
    key(cam, DUR * i / 6, loc=(3.6 * math.sin(a), -3.6 * math.cos(a), 1.9 - 0.3 * i / 6), ease="LINEAR")
