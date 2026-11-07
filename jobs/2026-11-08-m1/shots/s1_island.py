# A tiny economy: 10 apples and 10 dollars on a round plinth. Apples pop in one by one, then the cash stack lands.
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2)
world_color(hexrgb("#0d161c"), 1.0)
floor("#16232b", rough=0.6)
studio(target=(0, 0, 0.3), scale=0.8)

plinth = cylinder(1.25, 0.24, (0, 0, 0.12), material=mat("plinth", "#7a4b2e", rough=0.45, coat=0.5, noise_bump=0.05),
                  bevel=0.03, verts=96)

# 10 apples, two rows of five, at the back of the plinth
for i in range(10):
    row, col = divmod(i, 5)
    x = -0.72 + col * 0.36 + (0.18 if row else 0)
    y = 0.28 + row * 0.33
    a = apple((x, y, 0.24), r=0.15, name=f"apple{i}")
    a.rotation_euler = (0, 0, math.radians(37 * i))
    pop_in(a, 0.15 + i * 0.11, 0.3)

# the money: a neat stack of ten $1 notes at the front, dropping in after the apples
notes = []
for k in range(10):
    n = banknote(loc=(0, -0.45, 0.245 + k * 0.006), rot=(0, 0, 4 * math.sin(k * 1.7)), w=0.72, name=f"note{k}")
    t0 = 1.9 + k * 0.07
    key(n, 0, loc=(n.location[0], n.location[1], 2.6 + k * 0.1))
    key(n, t0, loc=(n.location[0], n.location[1], 2.6 + k * 0.1))
    key(n, t0 + 0.35, loc=(0, -0.45, 0.245 + k * 0.006))
    notes.append(n)

cam, tgt = camera((0, -4.3, 3.0), (0, 0.0, 0.32), lens=42, fstop=3.2)
key(cam, 0, loc=(0.35, -4.4, 3.1))
key(cam, DUR, loc=(-0.2, -3.7, 2.55))
