# Why it works: side view of the tower, top two sections in see-through glass with the gold ball inside; the tower leans one
# way while the ball swings the other way (half a cycle behind), then both settle smaller. Camera drifts (moving 3D).
import os, math
exec(open(os.path.join(ROOT, "jobs/2026-11-25-a/shots/towerkit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.25, exposure=0.15)
sky_set(blocks=True, seed=9)
pv, top = tower(1.0, xray_top=True)
# ball inside the see-through sections (sections 6-7 sit at z ~7.4-9.0)
sp, ball = damper((0, 0, 7.7), 0.42, 0.5, "tmd")
deck = bpy.data.objects["tmd_deck"]
for o in (sp, deck):
    o.parent = pv
# tower leans along x (rotation about y), the ball's pivot counter-swings relative to the tower
P = 2.4
steps = 24
for i in range(steps + 1):
    t = DUR * i / steps
    damp = 1.0 - 0.45 * (t / DUR)
    a = 3.4 * damp * math.sin(2 * math.pi * t / P)
    key(pv, t, rot=(0, a, 0), ease="LINEAR")
    key(sp, t, rot=(0, -a * 4.5, 0), ease="LINEAR")
wind(10, (-3, 2), (3, 10), DUR, speed=6.0, seed=5)
for k, (lx, ly, lz, s) in enumerate(((-5, 20, 12, 1.8), (6, 26, 15, 2.2))):
    c = cloud((lx, ly, lz), s, f"cl{k}", seed=k + 7)
    key(c, 0, loc=(lx, ly, lz), ease="LINEAR"); key(c, DUR, loc=(lx + 1.0, ly, lz), ease="LINEAR")
cam, tgt = camera((0.0, -11.0, 6.4), (0, 0, 7.0), lens=34, fstop=0)
key(cam, 0, loc=(-0.8, -11.0, 6.2)); key(cam, DUR, loc=(0.6, -9.6, 6.9))
