# Hook: the hacked eye. A big glossy eyeball glows green in the dark, nanoparticle lens on, an infrared LED's faint beam
# hits it; the camera pushes in and drifts (moving 3D).
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-24-a/shots/eyekit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.45, exposure=0.3)
eye_set()
E = (0, 0, 1.0)
sc, ir, pu, co = eyeball(E, 0.5)
lens, dots = contact_lens((0, -0.5 * 0.80 - 0.1, 1.0), 0.27)
iris_glow(0.0, 0.6, 5.0, GREEN)
body, bulb = led((1.5, -1.6, 1.25), (0, -0.45, 1.0))
beam((1.45, -1.55, 1.24), (0.05, -0.5, 1.02), IR_DIM, 1.2, 0.022, "irbeam")
for o in (sc, ir, pu, co):
    key(o, 0, rot=(0, 0, 0)); key(o, DUR * 0.5, rot=(0, 0, -6)); key(o, DUR, rot=(0, 0, 4))
cam, tgt = camera((0.9, -4.4, 1.55), (0, -0.2, 1.0), lens=50, fstop=2.0)
key(cam, 0, loc=(0.9, -4.4, 1.55)); key(cam, DUR, loc=(0.3, -2.3, 1.12))
