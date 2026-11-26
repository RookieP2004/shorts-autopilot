# Sundown: a wild turkey stands under a big autumn oak, then flaps straight up to a high branch to sleep; the camera tilts up
# with it (moving 3D). Warm sunset light, never dark.
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-26-a/shots/turkeykit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.25, exposure=0.25)
sun = field_set(sky=(0.98, 0.62, 0.42), sun_rot=(78, -8, -60), stripes=False)
sun.data.color = (1.0, 0.72, 0.45)
sun.data.energy = 4.6
bark = mat("bark2", "#5b3e2b", rough=0.9)
cylinder(0.45, 8.0, (1.2, 5.0, 4.0), (0, 0, 0), bark, verts=24, bevel=0, name="oak")
br = cylinder(0.14, 3.2, (-0.2, 5.0, 4.6), (0, 72, 0), bark, verts=16, bevel=0, name="branch")
cylinder(0.12, 2.6, (2.6, 5.0, 5.4), (0, -65, 0), bark, verts=16, bevel=0, name="branch2")
rnd = random.Random(9)
for k in range(9):
    c = ("#e0702e", "#c8322b", "#f2b04a")[k % 3]
    sphere(rnd.uniform(1.0, 1.6), (rnd.uniform(-0.2, 3.8), 5.4 + rnd.uniform(-0.4, 0.8), rnd.uniform(7.0, 8.4)), (1.2, 1.0, 0.8),
           mat(f"oakleaf{c}", c, rough=0.8, sss=0.15), seg=24, name=f"ol{k}")
area_light((-3, 0, 4), (0, 5, 3), 900, 4, "#ffd2a0", "warmfill")
tk, pv = turkey(1.15, True, "rt", legs_tucked=False, tail_open=True)
folded(tk, pv, 0, True)
key(tk, 0, loc=(-2.2, 4.2, 0), rot=(0, 0, 10), ease="LINEAR")
key(tk, 0.45, loc=(-2.2, 4.2, 0), rot=(0, 0, 10))
folded(tk, pv, 0.5, False)
flap(pv, DUR, period=0.22, up=65, down=-45, t0=0.5, t1=DUR * 0.78)
key(tk, 1.2, loc=(-1.9, 4.4, 1.6), rot=(0, -20, 10))
key(tk, DUR * 0.78, loc=(-0.9, 5.0, 4.7), rot=(0, -6, 0))
folded(tk, pv, DUR * 0.8, True)
key(tk, DUR, loc=(-0.9, 5.0, 4.72), rot=(0, 0, -8))
cam, tgt = camera((-3.6, -2.6, 0.9), (-2.1, 4.2, 0.6), lens=28, fstop=5.6)
key(cam, 0, loc=(-3.6, -2.6, 0.9)); key(cam, DUR, loc=(-2.4, 0.2, 3.7))
key(tgt, 0, loc=(-2.1, 4.2, 0.6)); key(tgt, 1.2, loc=(-1.9, 4.4, 1.7)); key(tgt, DUR * 0.8, loc=(-0.9, 5.0, 4.6)); key(tgt, DUR, loc=(-0.8, 5.0, 4.8))
