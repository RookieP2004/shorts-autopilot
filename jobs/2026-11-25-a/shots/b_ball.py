# The damper: the golden 660-tonne ball hanging on its cables inside the top floors (warm interior, cream walls, a viewing
# rail); it swings slowly while the camera orbits and pushes in (moving 3D).
import os, math
exec(open(os.path.join(ROOT, "jobs/2026-11-25-a/shots/towerkit.py")).read())
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.3, exposure=0.2)
world_hdri("lounge", 0.4, backdrop=(0.92, 0.86, 0.74))
plane(40, 40, (0, 0, 0), material=wood("#b88a5a", "#8c6238", "fl", 8.0, 0.5), name="floor")
wall = mat("wall", "#f3e6cf", rough=0.85)
box((14, 0.3, 9), (0, 4.0, 4.5), material=wall, bevel=0)
box((0.3, 14, 9), (-4.2, 0, 4.5), material=mat("wall2", "#e8d6b8", rough=0.85), bevel=0)
# windows with sky on the back wall
for k in range(3):
    plane(1.6, 3.2, (-2.4 + k * 2.4, 3.84, 4.0), (90, 0, 0), material=glow("#cfe9fb", 2.0, "sky_w"), name=f"win{k}")
# steel columns
steel = mat("col", "#3a4250", rough=0.35, metal=0.7)
for x in (-2.6, 2.6):
    box((0.35, 0.35, 8.5), (x, 2.6, 4.25), material=steel, bevel=0.02)
sp, ball = damper((0, 1.2, 2.4), 1.35, 2.6)
swing(sp, 0, 5.0, 3.6, DUR, phase=0.0)
swing(sp, 1, 3.0, 3.6, DUR, phase=1.2)
# the bowl below it and the yellow bumper ring
lathe([(0.0, 0.0), (2.2, 0.0), (2.4, 0.5), (2.2, 0.55), (0.0, 0.55)], 64, (0, 1.2, 0), mat("bowl", "#5a6472", rough=0.4, metal=0.5), name="bowl")
torus(2.1, 0.09, (0, 1.2, 0.62), (0, 0, 0), mat("bumper", "#f2b04a", rough=0.4), name="bumper")
# viewing rail in front
rail = mat("rail", "#d9dbe0", rough=0.2, metal=0.9)
cylinder(0.04, 8, (0, -1.6, 1.05), (0, 90, 0), rail, verts=16, bevel=0)
for x in range(-4, 5):
    cylinder(0.03, 1.05, (x * 0.9, -1.6, 0.52), (0, 0, 0), rail, verts=12, bevel=0)
area_light((-3, -4, 6), (0, 1.2, 2.4), 1500, 5, "#fff0dc", "key")
area_light((3.5, -2, 3), (0, 1.2, 2.4), 500, 4, "#dbe8ff", "fill")
area_light((0, 2.5, 7.5), (0, 1.2, 3), 600, 3, "#ffe0a8", "top")
cam, tgt = camera((-2.6, -5.2, 2.0), (0, 1.2, 2.9), lens=26, fstop=4.0)
key(cam, 0, loc=(-2.6, -5.2, 2.0)); key(cam, DUR, loc=(1.2, -4.3, 2.6))
