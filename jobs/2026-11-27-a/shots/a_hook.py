# Hook: the camera rises from one returned box on the floor up and back over a mountain of returned boxes in a huge
# warehouse (moving 3D, scale reveal).
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-27-a/shots/returnskit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2, exposure=0.1)
warehouse()
heap((0, 4.0, 0), radius=4.2, n=150, seed=9, height=3.0)
rack(-6.5, 8.5, seed=2); rack(6.5, 8.5, seed=4); rack(-6.5, 11.5, seed=6); rack(6.5, 11.5, seed=8)
hero = cbox((0.5, 0.42, 0.36), (0, -1.2, 0.18), (0, 0, 12), name="hero")
cam, tgt = camera((0.2, -2.4, 0.45), (0, -1.2, 0.25), lens=30, fstop=5.0)
key(cam, 0, loc=(0.2, -2.4, 0.45)); key(cam, DUR, loc=(0.6, -7.5, 5.2))
key(tgt, 0, loc=(0, -1.2, 0.25)); key(tgt, DUR, loc=(0, 3.5, 1.8))
