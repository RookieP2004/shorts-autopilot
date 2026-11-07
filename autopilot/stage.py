"""Place 2D characters and props into a rendered 3D plate by floor position (metres), with correct perspective.

  from autopilot.stage import Stage
  st = Stage("jobs/<id>/assets/plate_market_mid.json")
  st.place(1.2, -0.8)                 -> {"x": .., "y": .., "h": ..}  for a 1.75 m character standing at (1.2, -0.8, 0)
  st.place(0.3, 0.9, who="extra")     -> a townsperson (1.68 m by default; pass height=)
  st.point(0.0, 0.0, 0.97)            -> (x, y) screen fractions of a 3D point (e.g. where the counter top is)
  st.walk([(t, wx, wy), ...], base)   -> keys with x, y, scale for a walk across the set (scale vs. the base placement)

Characters are drawn feet-at-the-bottom on a 600x1500 canvas; FIG describes where head-top and feet sit on it.
"""
import json

import numpy as np

FIG = {"ved": (20, 1456), "extra": (82, 1450)}       # (top of head, soles) in the 1500 px tall drawing
HEIGHT = {"ved": 1.78, "extra": 1.68}


class Stage:
    def __init__(self, path):
        d = json.load(open(path))
        self.M = np.array(d["matrix_world"])
        self.Minv = np.linalg.inv(self.M)
        self.w, self.h = d["w"], d["h"]
        self.f = d["lens"] / d["sensor"] * (max(self.w, self.h) if d.get("fit", "AUTO") == "AUTO"
                                            else (self.w if d["fit"] == "HORIZONTAL" else self.h))

    def point(self, x, y, z=0.0):
        p = self.Minv @ np.array([x, y, z, 1.0])
        depth = -p[2]
        sx = self.w / 2 + self.f * p[0] / depth
        sy = self.h / 2 - self.f * p[1] / depth
        return sx / self.w, sy / self.h

    def place(self, x, y, who="ved", height=None, z=0.0):
        height = height or HEIGHT[who]
        fx, fy = self.point(x, y, z)
        _, hy = self.point(x, y, z + height)
        top, sole = FIG[who]
        px_per_canvas = (fy - hy) * self.h / (sole - top)        # frame px per drawing px
        h = 1500 * px_per_canvas / self.h                        # layer height (fraction of frame)
        cy = fy - (sole / 1500 - 0.5) * h
        return {"x": round(fx, 4), "y": round(cy, 4), "h": round(h, 4)}

    def walk(self, pts, base, who="ved", height=None, ease_last="out"):
        """pts: [(t, wx, wy), ...]. Returns keys (x, y, scale) relative to `base` (a place() result); walking between points."""
        keys = []
        for i, (t, wx, wy) in enumerate(pts):
            p = self.place(wx, wy, who, height)
            k = {"t": t, "x": p["x"], "y": p["y"], "scale": round(p["h"] / base["h"], 4)}
            if i > 0:
                k["walk"] = True
            keys.append(k)
        return keys
