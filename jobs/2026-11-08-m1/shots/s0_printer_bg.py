# Hook background: the money printer mid-print, out of focus behind Ved (a single still frame).
import random
random.seed(2)
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.35)
world_color(hexrgb("#0d161c"), 1.0)
floor("#16232b", rough=0.55)
studio(target=(0, 0.6, 0.8), scale=1.1)
pr, slot = printer((0, 0.6, 0), scale=1.0)
for k in range(14):
    banknote(loc=(random.uniform(-1.4, 1.4), random.uniform(-1.2, 0.2), random.uniform(0.2, 1.9)),
             rot=(random.uniform(-60, 60), random.uniform(-60, 60), random.uniform(0, 180)), w=0.6, name=f"fly{k}")
for k in range(30):
    banknote(loc=(random.uniform(-0.9, 0.9), random.uniform(-0.9, -0.2), 0.004 + k * 0.004),
             rot=(0, 0, random.uniform(0, 360)), w=0.6, name=f"pile{k}")
cam, tgt = camera((0, -5.0, 1.4), (0, 0.4, 0.9), lens=38, fstop=1.2, focus=2.2)
