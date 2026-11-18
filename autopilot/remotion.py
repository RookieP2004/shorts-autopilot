"""Remotion / GSAP / three.js motion clips (the `motion` layer; not to be confused with motion.py = keyframes) for the compositor (owner, 2026-11-18: learn and use the Remotion, GSAP and
three.js skills, mixed into the house style).

A `motion` layer names a composition in motion/src (KineticTitle, FlowDiagram, Hero3D, ...) plus its props. Before
frames are drawn, render_clip() renders it ONCE with Remotion in headless Chrome to a transparent PNG sequence (cached by
a hash of the composition, props, size and code); the layer then plays it like a `blender` shot, so it sits inside the
scene with Ved, the plates, captions and everything else. three.js renders here in ~0.3 s a frame (Blender: ~7 s).
"""
import hashlib
import json
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTION = os.path.join(ROOT, "motion")
COMPS = {"KineticTitle", "FlowDiagram", "Hero3D", "NumberSlam", "Stack3D"}


def _src_stamp():
    h = hashlib.sha1()
    for d in ("src",):
        for f in sorted(os.listdir(os.path.join(MOTION, d))):
            p = os.path.join(MOTION, d, f)
            h.update(f.encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()[:10]


def ensure_installed(log=print):
    """node_modules is not in git: install from package-lock.json the first time a run needs it (~1 min)."""
    if os.path.isdir(os.path.join(MOTION, "node_modules", "remotion")):
        return
    if not shutil.which("npm"):
        raise RuntimeError("motion layers need Node.js + npm")
    log("  motion: installing Remotion / GSAP / three.js (npm ci)")
    r = subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=MOTION, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("npm ci failed in motion/:\n" + r.stderr[-2000:])


def render_clip(comp, props, out_dir, w, h, fps, dur, log=print):
    """Render `comp` with `props` to out_dir/*.png (transparent). Cached: re-renders only if anything changed."""
    ensure_installed(log)
    full = dict(props, w=int(w), h=int(h), fps=int(fps), dur=float(dur))
    key = hashlib.sha1((comp + json.dumps(full, sort_keys=True) + _src_stamp()).encode()).hexdigest()[:16]
    done = os.path.join(out_dir, ".done")
    if os.path.exists(done) and open(done).read().strip() == key:
        return out_dir
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)
    pf = os.path.join(out_dir, "_props.json")
    json.dump(full, open(pf, "w"))
    r = subprocess.run(["node", os.path.join(MOTION, "render.mjs"), comp, pf, out_dir], cwd=MOTION, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"motion clip {comp} failed:\n" + r.stdout[-1500:] + r.stderr[-3000:])
    log("   " + [ln for ln in r.stdout.splitlines() if ln.startswith("motion ")][-1])
    open(done, "w").write(key)
    return out_dir
