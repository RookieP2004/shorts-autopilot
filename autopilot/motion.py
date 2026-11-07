"""Keyframed motion for any layer, plus walking and hopping for characters.

Layer fields (job.json):
  "keys": [{"t": 0, "x": 1.15}, {"t": 1.2, "x": 0.72, "walk": true, "ease": "out"}, ...]
      Animatable: x, y (0-1 of frame), scale, rot (deg), opacity, sx (horizontal scale: -1..1, use it for card flips).
      Each property interpolates between the keys that set it. "ease" on the arriving key: in_out (default), linear,
      in, out, back (overshoot), bounce (lands and bounces). Before the first key / after the last, values hold.
  "walk": true on a key  -> the character walks (legs step, body bobs, arms swing) while travelling to that key.
  "hops": [[t, height, dur], ...]  -> jumps: height as a fraction of the frame height, dur in seconds.
  "ground": true -> draw a soft floor shadow under the character that stays on the floor during hops (default when keys
      or hops are used).
"""
import math

PROPS = ("x", "y", "scale", "rot", "opacity", "sx")
DEFAULTS = {"scale": 1.0, "rot": 0.0, "opacity": 1.0, "sx": 1.0}
STEP_RATE = 2.2            # steps per second while walking


def _ease(p, kind):
    p = max(0.0, min(1.0, p))
    if kind == "linear":
        return p
    if kind == "in":
        return p * p * p
    if kind == "out":
        return 1 - (1 - p) ** 3
    if kind == "back":
        c1, c3 = 1.70158, 2.70158
        return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2
    if kind == "bounce":
        n, d = 7.5625, 2.75
        if p < 1 / d:
            return n * p * p
        if p < 2 / d:
            p -= 1.5 / d
            return n * p * p + 0.75
        if p < 2.5 / d:
            p -= 2.25 / d
            return n * p * p + 0.9375
        p -= 2.625 / d
        return n * p * p + 0.984375
    return p * p * (3 - 2 * p)          # in_out (smoothstep)


def keyed(L, t):
    """Interpolated props at time t (only the props the keys mention; others absent)."""
    keys = L.get("keys")
    if not keys:
        return {}
    out = {}
    for prop in PROPS:
        ks = [k for k in keys if prop in k]
        if not ks:
            continue
        if t <= ks[0]["t"]:
            out[prop] = ks[0][prop]
            continue
        if t >= ks[-1]["t"]:
            out[prop] = ks[-1][prop]
            continue
        for a, b in zip(ks, ks[1:]):
            if a["t"] <= t <= b["t"]:
                p = (t - a["t"]) / max(1e-6, b["t"] - a["t"])
                e = _ease(p, b.get("ease", "linear" if b.get("walk") else "in_out"))
                out[prop] = a[prop] + (b[prop] - a[prop]) * e
                break
    return out


def walking(L, t):
    """(is_walking, phase) - phase counts steps since the walk began (one step = 1.0)."""
    keys = L.get("keys") or []
    for a, b in zip(keys, keys[1:]):
        if b.get("walk") and a["t"] <= t < b["t"]:
            return True, (t - a["t"]) * STEP_RATE
    return False, 0.0


def hop(L, t):
    """Height (fraction of frame) above the ground at time t, and 0..1 progress through the hop (or None)."""
    for h in L.get("hops", []):
        t0, height = h[0], h[1]
        dur = h[2] if len(h) > 2 else 0.5
        if t0 <= t <= t0 + dur:
            p = (t - t0) / dur
            return height * 4 * p * (1 - p), p
    return 0.0, None


def legs_and_bob(L, t):
    """Leg lifts (px in the character's own 600x1500 drawing) and body bob (fraction of frame height)."""
    w, phase = walking(L, t)
    hh, hp = hop(L, t)
    if hp is not None:
        tuck = 70 * math.sin(math.pi * hp)
        return (tuck, tuck), 0.0, True
    if w:
        s = math.sin(phase * math.pi)
        lift_l, lift_r = max(0.0, s) * 115, max(0.0, -s) * 115
        bob = abs(s) * 0.006
        return (lift_l, lift_r), bob, True
    return (0.0, 0.0), 0.0, False


def arm_swing(arms_down, t, L):
    """Walking arms: the down pose with wrists/elbows swinging opposite to the legs."""
    w, phase = walking(L, t)
    if not w:
        return None
    s = math.sin(phase * math.pi)
    out = []
    for (sh, el, wr, kind, front) in arms_down:
        side = -1 if sh[0] < 300 else 1
        k = s * side
        out.append((sh, (el[0] - 6 * side, el[1] - 8 * abs(k)), (wr[0] - 34 * k * side, wr[1] - 60 * max(0, k) - 12), kind, front))
    return out
