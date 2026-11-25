# Shared builder for 2026-11-25-a: a stylised tiered skyscraper (eight flared "bamboo" sections on a tapered trunk, our own
# simplified design), a bright sky set with a sun, low city blocks and soft clouds, and the golden tuned-mass-damper ball
# hanging from cables inside a steel frame. Exec'd by the shot scripts and assets.py (blendkit helpers are already loaded).
import math, random
import bpy

GOLD = "#e0a82e"
GLASS = "#3f8f8a"


def sky_set(ground="#9fb3a0", sky=(0.32, 0.58, 0.98), sun_power=4.0, blocks=True, seed=3):
    world_color(sky, 0.9)
    plane(400, 400, (0, 0, 0), material=mat("ground", ground, rough=0.9), name="ground")
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = sun_power
    sun.color = (1.0, 0.93, 0.82)
    sun.angle = math.radians(3)
    so = bpy.data.objects.new("sun", sun)
    bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(48), math.radians(-18), math.radians(-35))
    if blocks:
        rnd = random.Random(seed)
        cols = ["#f2c88a", "#d9cbb4", "#bfe3d6", "#e8a87c", "#c9d2e3", "#f6efe2"]
        for k in range(70):
            a = rnd.uniform(0, 2 * math.pi)
            r = rnd.uniform(9, 60)
            x, y = math.cos(a) * r, math.sin(a) * r + 10
            if y < 5 and abs(x) < 16:
                continue
            h = rnd.uniform(1.0, 5.5)
            box((rnd.uniform(2, 4.5), rnd.uniform(2, 4.5), h), (x, y, h / 2), (0, 0, rnd.uniform(0, 90)),
                mat(f"blk{k % 6}", cols[k % 6], rough=0.7), bevel=0.08, name=f"blk{k}")
    return so


def cloud(loc, s=1.0, name="cloud", seed=1):
    rnd = random.Random(seed)
    m = bpy.data.materials.get("cloud_m") or mat("cloud_m", "#ffffff", rough=0.95, sss=0.3)
    root = empty(loc, name)
    for k in range(7):
        o = sphere(s * rnd.uniform(0.7, 1.2), (loc[0] + rnd.uniform(-1.8, 1.8) * s, loc[1] + rnd.uniform(-0.5, 0.5) * s,
                                              loc[2] + rnd.uniform(-0.3, 0.4) * s), (1.3, 1.0, 0.75), m, seg=24,
                   name=f"{name}_{k}")
        o.parent = root
        o.matrix_parent_inverse = root.matrix_world.inverted()
    return root


def _frustum(r0, r1, z0, h, material, name, segs=4):
    # square-section frustum (4 segments, turned 45 degrees so its faces point at the camera)
    o = lathe([(0.0, 0.0), (r0, 0.0), (r1, h), (r1 * 0.92, h + 0.04), (0.0, h + 0.04)], segs, (0, 0, z0), material, subdiv=0,
              name=name)
    o.rotation_euler = (0, 0, math.radians(45))
    for p in o.data.polygons:
        p.use_smooth = False
    return o


def tower(scale=1.0, xray_top=False, name="tw"):
    """Returns (pivot, top_z). Everything is parented to `pivot` at the base so a rotation = the whole tower sways.
    Units: scale 1.0 -> 10.2 high. xray_top: the top two sections in see-through glass (to show the damper ball)."""
    pv = empty((0, 0, 0), name + "_pivot")
    glass = mat(name + "_glass", GLASS, rough=0.12, metal=0.35, coat=0.8)
    trim = mat(name + "_trim", "#e9eef0", rough=0.3, metal=0.5)
    ghost = mat(name + "_ghost", "#9fe0d8", rough=0.05, alpha=0.25, coat=0.3)
    parts = []
    s = scale
    parts.append(box((2.2 * s, 2.2 * s, 0.5 * s), (0, 0, 0.25 * s), material=mat(name + "_podium", "#d9cbb4", rough=0.6),
                     bevel=0.04, name=name + "_podium"))
    parts.append(_frustum(0.95 * s, 0.72 * s, 0.5 * s, 2.0 * s, glass, name + "_trunk"))
    z = 2.5 * s
    for k in range(8):
        m = ghost if (xray_top and k >= 6) else glass
        parts.append(_frustum(0.62 * s, 0.8 * s, z, 0.78 * s, m, f"{name}_sec{k}"))
        parts.append(box((1.18 * s, 1.18 * s, 0.05 * s), (0, 0, z + 0.03 * s), (0, 0, 0), trim, bevel=0.01, name=f"{name}_band{k}"))
        z += 0.82 * s
    parts.append(_frustum(0.5 * s, 0.32 * s, z, 0.6 * s, glass, name + "_crown"))
    z += 0.6 * s
    parts.append(cylinder(0.05 * s, 1.1 * s, (0, 0, z + 0.55 * s), material=trim, verts=16, bevel=0, name=name + "_spire"))
    for o in parts:
        o.parent = pv
    return pv, z


def damper(loc, r=1.0, cable_len=2.2, name="tmd"):
    """The golden ball on cables. Returns (swing_pivot, ball). Rotate swing_pivot (at the cable tops) to swing it."""
    x, y, z = loc
    top = z + r + cable_len
    sp = empty((x, y, top), name + "_swing")
    gold = metal(GOLD, 0.22, name + "_gold")
    ball = sphere(r, (x, y, z), 1, gold, seg=64, name=name + "_ball")
    # the steel plates: thin darker rings around the ball's waist
    for k in range(-4, 5):
        zz = z + k * r * 0.2
        rr = math.sqrt(max(r * r - (k * r * 0.2) ** 2, 0.01)) * 1.003
        o = torus(rr, 0.008 * r, (x, y, zz), (0, 0, 0), metal("#b27f1c", 0.3, name + f"_ring{k}"), name=name + f"_r{k}")
        o.parent = sp
        o.matrix_parent_inverse = sp.matrix_world.inverted()
    ball.parent = sp
    ball.matrix_parent_inverse = sp.matrix_world.inverted()
    steel = mat(name + "_steel", "#2c333d", rough=0.35, metal=0.8)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        cx, cy = x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55
        zb = z + r * 0.8
        c = cylinder(0.025 * r, top - zb, (cx, cy, (top + zb) / 2), material=steel, verts=10, bevel=0, name=name + f"_cab{k}")
        c.parent = sp
        c.matrix_parent_inverse = sp.matrix_world.inverted()
    # the frame it hangs from
    box((r * 3.2, r * 3.2, 0.12 * r), (x, y, top + 0.06 * r), material=steel, bevel=0.01, name=name + "_deck")
    return sp, ball


def swing(obj, axis, amp, period, dur, phase=0.0, steps=None):
    """Smooth sinusoidal rotation keys (degrees) about axis 0/1/2."""
    steps = steps or max(6, int(dur / period * 8))
    for i in range(steps + 1):
        t = dur * i / steps
        ang = amp * math.sin(2 * math.pi * (t / period) + phase)
        r = [0, 0, 0]
        r[axis] = ang
        key(obj, t, rot=tuple(r), ease="LINEAR")


def wind(n, area, z, dur, speed=6.0, seed=2, name="wind"):
    """Thin white streaks sliding across the frame (+x)."""
    rnd = random.Random(seed)
    m = glow("#ffffff", 1.6, name + "_m")
    for k in range(n):
        y = rnd.uniform(area[0], area[1])
        zz = rnd.uniform(z[0], z[1])
        L = rnd.uniform(1.2, 2.6)
        x0 = rnd.uniform(-14, -4)
        c = cylinder(0.018, L, (x0, y, zz), (0, 90, 0), m, verts=8, bevel=0, name=f"{name}{k}")
        key(c, 0, loc=(x0, y, zz), ease="LINEAR")
        key(c, dur, loc=(x0 + speed * dur * rnd.uniform(0.8, 1.3), y, zz), ease="LINEAR")
