# The patch: the nanoparticle contact lens drops onto the eye; the infrared beam (dark red, invisible) turns into green
# light inside the lens and the iris lights up. Camera orbits from the side to the front.
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-24-a/shots/eyekit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.45, exposure=0.3)
eye_set()
E = (0, 0, 1.0)
sc, ir, pu, co = eyeball(E, 0.5)
LZ = (0, -0.5 * 0.80 - 0.1, 1.0)
lens, dots = contact_lens((LZ[0], LZ[1] - 0.25, LZ[2] + 1.1), 0.27)
t_land = min(1.2, DUR * 0.38)
key(lens, 0, loc=(LZ[0], LZ[1] - 0.25, LZ[2] + 1.1), rot=(0, 25, 0))
key(lens, t_land, loc=LZ, rot=(0, 0, 0))
body, bulb = led((1.5, -1.6, 1.25), (0, -0.45, 1.0))
red = beam((1.45, -1.55, 1.24), (0.05, -0.5, 1.02), IR_DIM, 1.2, 0.022, "irbeam")
t_on = t_land + 0.35
grn = beam((0.03, -0.53, 1.01), (0.0, -0.42, 1.0), GREEN, 8.0, 0.05, "gbeam")
show_at(grn, t_on)
iris_glow(t_on, t_on + 0.5, 5.0, GREEN)
cam, tgt = camera((-2.6, -2.4, 1.6), (0, -0.3, 1.05), lens=45, fstop=2.2)
key(cam, 0, loc=(-2.6, -2.4, 1.6)); key(cam, DUR, loc=(-0.7, -2.9, 1.2))
