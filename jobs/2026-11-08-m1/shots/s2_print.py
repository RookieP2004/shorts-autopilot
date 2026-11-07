# The government prints 10 more dollars: the printer spits bills that tumble onto the pile; the apples stay ten.
import random
random.seed(4)
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.25)
world_color(hexrgb("#0d161c"), 1.0)
floor("#16232b", rough=0.6)
studio(target=(0, -0.6, 0.6), scale=1.0)

pr, slot = printer((0, 0.9, 0), scale=0.95)
# the ten apples, untouched, on a plinth at the left
plinth = cylinder(0.58, 0.16, (-0.72, -0.45, 0.08), material=mat("plinth", "#7a4b2e", rough=0.45, coat=0.5), bevel=0.02, verts=64)
for i in range(10):
    row, col = divmod(i, 4) if i < 8 else (2, i - 8)
    ax = -0.72 - 0.33 + col * 0.22 + (0.33 if row == 2 else 0)
    ay = -0.66 + row * 0.2
    apple((ax, ay, 0.16), r=0.09, name=f"apple{i}")

# the original stack of ten notes, then ten new ones shoot out and land on it
base = (0.42, -0.85, 0.0)
for k in range(10):
    banknote(loc=(base[0], base[1], 0.004 + k * 0.006), rot=(0, 0, 3 * math.sin(k)), w=0.62, name=f"old{k}")
for k in range(10):
    n = banknote(loc=slot, rot=(0, 0, 0), w=0.62, name=f"new{k}")
    t0 = 0.6 + k * 0.32
    land = (base[0] + random.uniform(-0.12, 0.12), base[1] + random.uniform(-0.1, 0.1), 0.07 + k * 0.012)
    spin_z = random.uniform(-70, 70)
    key(n, 0, loc=(slot[0], slot[1] + 0.25, slot[2]), rot=(0, 0, 0), scale=0.001)
    key(n, t0, loc=(slot[0], slot[1] + 0.25, slot[2]), rot=(0, 0, 0), scale=0.001)
    key(n, t0 + 0.12, loc=(slot[0], slot[1] - 0.2, slot[2] + 0.05), rot=(-10, 0, 0), scale=1)
    mid = ((slot[0] + land[0]) / 2, (slot[1] + land[1]) / 2 - 0.1, slot[2] + 0.45)
    key(n, t0 + 0.42, loc=mid, rot=(random.uniform(-40, 40), random.uniform(-30, 30), spin_z * 0.6))
    key(n, t0 + 0.8, loc=land, rot=(0, 0, spin_z))

cam, tgt = camera((0.2, -3.6, 2.3), (-0.05, -0.15, 0.5), lens=32, fstop=4.0)
key(cam, 0, loc=(0.35, -3.7, 2.4))
key(cam, DUR, loc=(-0.05, -3.2, 2.15))
