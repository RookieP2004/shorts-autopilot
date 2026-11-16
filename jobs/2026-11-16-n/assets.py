# 2026-11-16-n (PILOT, night-set style): the Telegram stock-tip split-list trick (survivorship bias).
# One night arena (navy dark, one hard spot from above, blue rim, faint floor grid, a glowing fictional chart wall far
# behind) seen from three cameras; a hero still of the survivor crowd built with crowd(); cut-outs: a generic glossy
# phone (live screen composited later), a gold coin, fictional "NOT REAL MONEY" notes.
import math, os, random
from PIL import Image as PI, ImageDraw as PD
from autopilot import devices

A = ASSETS


def chart_wall(path):
    """A fictional glowing candlestick chart (no ticker, no real data): the 'market' behind the arena."""
    W_, H_ = 1600, 900
    im = PI.new("RGB", (W_, H_), (4, 7, 14))
    d = PD.Draw(im)
    for y in range(0, H_, 90):
        d.line([(0, y), (W_, y)], fill=(16, 28, 50), width=2)
    rnd = random.Random(5)
    p = 620.0
    for i in range(46):
        x = 40 + i * 33
        o = p
        p = max(120, min(820, p + rnd.uniform(-70, 60) - 4))
        c = p
        up = c < o
        col = (53, 224, 138) if up else (255, 59, 74)
        hi, lo = min(o, c) - rnd.uniform(10, 50), max(o, c) + rnd.uniform(10, 50)
        d.line([(x + 10, hi), (x + 10, lo)], fill=col, width=3)
        d.rectangle([x, min(o, c), x + 20, max(o, c) + 2], fill=col)
    im.save(path)
    return path


WALL = chart_wall(os.path.join(A, "chart_wall.png"))
NOTE = os.path.join(A, "note_fake.png")
devices.note_texture("500", NOTE)
CROWD_AREA = (-3.6, 3.6, -2.4, 3.2)


def arena(grid=True):
    reset(1080, 1920, samples=24, bloom=0.35, exposure=0.2)
    night_set(target=(0, 0.4, 0), rim=NIGHT["rim"], spot_power=22000, spot_height=10, spot_angle=44, grid=grid,
              back_wall=WALL)


# 1. wide high angle: the floor where the crowd stands (crowd drawn live by the compositor)
arena()
camera((0, -10.5, 8.2), (0, 0.6, 0), lens=30, fstop=0)
still("plate_arena_wide", samples=24)

# 2. low hero angle with a Dutch tilt: Ved / the reveal
arena()
cam, _ = camera((1.1, -6.2, 1.25), (0, 0.4, 1.05), lens=35, fstop=2.0, focus=6.3)
dutch(cam, 5)
still("plate_arena_hero", samples=24)

# 3. medium angle: Ved walking through the crowd
arena()
cam, _ = camera((2.6, -8.6, 3.4), (0, 0.2, 0.5), lens=32, fstop=2.8, focus=8.6)
dutch(cam, -3)
still("plate_arena_mid", samples=24)

# 4. hero still: the survivor crowd built in 3D (crowd()): one block of survivors glows green, the rest dim grey
arena(grid=False)
camera((0, -10.5, 8.2), (0, 0.6, 0), lens=30, fstop=0)
crowd(CROWD_AREA, n=3200, h=0.32, colors=("#59606e",),
      color_of=lambda i, x, y, u, v: NIGHT["green"] if (0.375 <= u < 0.625 and 0.35 <= v < 0.65) else "#7d8596",
      glow_of=lambda i, x, y, u, v: 0.375 <= u < 0.625 and 0.35 <= v < 0.65, seed=3)
still("plate_crowd_survivors", samples=24)

# 5. cut-outs under the same night light (spot from above + blue rim), transparent
reset(1080, 1920, samples=48, bloom=0.3, exposure=0.3)
world_color(NIGHT["bg"], 0.05)
spot_light((0.0, -3.0, 6.0), (0, 0, 0), 1500, 40, color=NIGHT["spot"], name="k")
area_light((2.5, 2.5, 1.5), (0, 0, 0), 600, 2.0, NIGHT["rim"], "rim")
area_light((-2.5, 2.0, 1.0), (0, 0, 0), 300, 2.0, "#7a5cff", "rim2")
area_light((-3, -4, 1), (0, 0, 0), 120, 6.0, "#bcc8ff", "fill")
body, scr = phone((0, 0, 0), (0, 0, 0), w=0.8)
camera((0, -3.4, 0.1), (0, 0, 0), lens=60, fstop=0)
phone_sprite("phone", scr, samples=48)

reset(1080, 1080, samples=48, bloom=0.3, exposure=0.3)
world_color(NIGHT["bg"], 0.05)
spot_light((0.0, -3.0, 6.0), (0, 0, 0), 1500, 40, color=NIGHT["spot"], name="k")
area_light((2.5, 2.5, 1.5), (0, 0, 0), 700, 2.0, NIGHT["rim"], "rim")
area_light((0.5, -4, 1.5), (0, 0, 0), 900, 8.0, "#ffe2b8", "fill")
coin((0, 0, 0), (90, 0, 18), r=0.5)
camera((0.4, -3.2, 0.6), (0, 0, 0), lens=60, fstop=0)
still("coin", 1080, 1080, samples=48, transparent=True, crop=True)

for i, (rot, bend) in enumerate((((80, 8, 20), 18), ((65, -20, -35), -24))):
    reset(1080, 1080, samples=40, bloom=0.25, exposure=0.3)
    world_color(NIGHT["bg"], 0.05)
    spot_light((0.0, -3.0, 6.0), (0, 0, 0), 1400, 40, color=NIGHT["spot"], name="k")
    area_light((2.5, 2.5, 1.5), (0, 0, 0), 500, 2.0, NIGHT["rim"], "rim")
    area_light((-3, -4, 1), (0, 0, 0), 200, 6.0, "#ffffff", "fill")
    banknote(NOTE, (0, 0, 0), rot, w=1.0, name="note", bend=bend)
    camera((0, -3.4, 0.4), (0, 0, 0), lens=55, fstop=0)
    still(f"note{i + 1}", 1080, 1080, samples=40, transparent=True, crop=True)
