# Hook: a wild turkey bursts across an autumn field mown in stripes (with yard lines, a nod to Thanksgiving football),
# wings beating, the camera racing alongside it (moving 3D).
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-26-a/shots/turkeykit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
field_set(side_trees=False)
tk, pv = turkey(1.0, True, "wt", legs_tucked=True, tail_open=False)
x0, x1 = -22.0, 22.0
key(tk, 0, loc=(x0, 6.0, 1.2), rot=(0, 14, 0), ease="LINEAR")
key(tk, DUR * 0.5, loc=((x0 + x1) / 2, 6.0, 2.3), rot=(4, 10, 0), ease="LINEAR")
key(tk, DUR, loc=(x1, 6.0, 3.0), rot=(0, 8, 0), ease="LINEAR")
flap(pv, DUR, period=0.2, up=60, down=-40)
cam, tgt = camera((x0 - 0.6, 2.7, 0.9), (x0 + 0.3, 6.0, 1.25), lens=30, fstop=4.0)
key(cam, 0, loc=(x0 - 0.6, 2.7, 0.9), ease="LINEAR"); key(cam, DUR * 0.5, loc=((x0 + x1) / 2 - 0.9, 2.6, 1.9), ease="LINEAR")
key(cam, DUR, loc=(x1 - 1.4, 2.9, 2.5), ease="LINEAR")
key(tgt, 0, loc=(x0 + 0.3, 6.0, 1.25), ease="LINEAR"); key(tgt, DUR * 0.5, loc=((x0 + x1) / 2 + 0.2, 6.0, 2.25), ease="LINEAR")
key(tgt, DUR, loc=(x1 + 0.2, 6.0, 2.95), ease="LINEAR")
