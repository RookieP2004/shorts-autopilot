# Zimbabwe, 2009: a giant 100-trillion-dollar note floats in the dark while worthless notes drift down behind it.
import random
random.seed(9)
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.35)
world_color(hexrgb("#120c16"), 1.0)
studio(target=(0, 0, 1.5), scale=1.2, key="#ffe2c2", rim="#c58bff")

hero = banknote(os.path.join(TEX, "note_100t.png"), loc=(0, 0, 1.55), rot=(90, 0, 0), w=1.35, name="hero", bend=14)
key(hero, 0, rot=(84, 0, -14), loc=(0, 0, 1.5))
key(hero, DUR, rot=(92, 0, 10), loc=(0, 0, 1.6))

# background: notes falling like leaves (out of focus)
for k in range(26):
    x, y = random.uniform(-3.5, 3.5), random.uniform(2.5, 6.0)
    n = banknote(os.path.join(TEX, "note_100t.png"), loc=(x, y, 4.5), w=0.7, name=f"bg{k}")
    z0 = random.uniform(1.5, 6.0)
    fall = random.uniform(1.6, 3.0)
    key(n, 0, loc=(x, y, z0), rot=(random.uniform(0, 90), random.uniform(0, 90), random.uniform(0, 180)), ease="LINEAR")
    key(n, DUR, loc=(x + random.uniform(-0.5, 0.5), y, z0 - fall),
        rot=(random.uniform(90, 300), random.uniform(60, 200), random.uniform(0, 360)), ease="LINEAR")

cam, tgt = camera((-1.2, -2.2, 1.7), (-0.5, 0, 1.55), lens=45, fstop=2.2)
key(cam, 0, loc=(-0.25, -2.25, 1.6))
key(cam, DUR, loc=(0.15, -3.6, 1.72))
key(tgt, 0, loc=(-0.12, 0, 1.55))
key(tgt, DUR, loc=(0, 0, 1.55))
