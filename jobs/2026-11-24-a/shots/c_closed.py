# Eyes closed: the eyelid comes down over the lensed eye, the infrared beam still goes through it, and the closed lid
# glows green from inside (the lens still converts the light). Front three-quarter camera, slow push.
import os
exec(open(os.path.join(ROOT, "jobs/2026-11-24-a/shots/eyekit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.5, exposure=0.3)
eye_set()
E = (0, 0, 1.0)
sc, ir, pu, co = eyeball(E, 0.5)
lens, dots = contact_lens((0, -0.5 * 0.80 - 0.1, 1.0), 0.27)
iris_glow(0.0, 0.3, 4.0, GREEN)
lid = eyelid(E, 0.64)
m = lid.active_material
p = m.node_tree.nodes.get("Principled BSDF")
p.inputs["Emission Color"].default_value = (*hexrgb(GREEN), 1)
s = p.inputs["Emission Strength"]
for t, v in ((0, 0.0), (1.0, 0.0), (1.6, 0.35)):
    s.default_value = v
    s.keyframe_insert("default_value", frame=int(t * FPS) + 1)
key(lid, 0, rot=(-150, 0, 0)); key(lid, 0.2, rot=(-150, 0, 0)); key(lid, 0.95, rot=(0, 0, 0))
body, bulb = led((1.5, -1.6, 1.25), (0, -0.6, 1.0))
beam((1.45, -1.55, 1.24), (0.12, -0.66, 1.03), IR_DIM, 1.4, 0.022, "irbeam")
cam, tgt = camera((-1.3, -3.0, 1.6), (0.1, -0.2, 1.0), lens=40, fstop=2.6)
key(cam, 0, loc=(-1.3, -3.0, 1.6)); key(cam, DUR, loc=(-0.9, -2.4, 1.4))
