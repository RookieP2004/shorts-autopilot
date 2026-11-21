"""Reelsmith looks: the `look` layer. A look is a web page (reelsmith/looks/<id>/look.js) that draws any moment t of a
small animated piece (a receipt printing, a scale tipping, a radar sweep...). Before frames are drawn, render_clip()
captures it once in headless Chrome to a transparent PNG sequence (cached by look code + props + size), and the layer
plays it inside the scene like a `motion` clip, with Ved, plates and captions around it. The look's own sound cues
(cues.json) join the mix, and its text boxes (texts.json) feed the director's reading check.
"""
import hashlib
import json
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RS = os.path.join(ROOT, "reelsmith")
LOOKS_DIR = os.path.join(RS, "looks")


def catalogue():
    """{id: short name} for every look in reelsmith/looks (id = folder name, e.g. RS-03-balance)."""
    return {d: d.split("-", 2)[-1] for d in sorted(os.listdir(LOOKS_DIR)) if os.path.isfile(os.path.join(LOOKS_DIR, d, "look.js"))}


def resolve(name):
    """Accept the full id ('RS-03-balance'), the number ('RS-03') or the short name ('balance')."""
    for d in catalogue():
        if name in (d, d[:5], d.split("-", 2)[-1]):
            return d
    raise KeyError(f"unknown look '{name}'; have {sorted(catalogue())}")


def _stamp(look):
    h = hashlib.sha1()
    for p in (os.path.join(LOOKS_DIR, look, "look.js"), os.path.join(RS, "host.html"), os.path.join(RS, "kit", "core.js")):
        h.update(open(p, "rb").read())
    return h.hexdigest()[:10]


def ensure_installed(log=print):
    if os.path.isdir(os.path.join(RS, "node_modules", "playwright-core")):
        return
    log("  looks: installing Reelsmith (npm install, playwright-core + three)")
    r = subprocess.run(["npm", "install", "--no-audit", "--no-fund"], cwd=RS, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("npm install failed in reelsmith/:\n" + r.stderr[-2000:])


def render_clip(name, props, out_dir, w, h, fps, dur, log=print, workers=2):
    look = resolve(name)
    ensure_installed(log)
    job = {"w": int(w), "h": int(h), "fps": int(fps), "dur": float(dur), "props": props or {}, "workers": workers}
    key = hashlib.sha1((look + json.dumps(job, sort_keys=True) + _stamp(look)).encode()).hexdigest()[:16]
    done = os.path.join(out_dir, ".done")
    if os.path.exists(done) and open(done).read().strip() == key:
        return out_dir
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)
    jf = os.path.join(out_dir, "_job.json")
    json.dump(job, open(jf, "w"))
    r = subprocess.run(["node", os.path.join(RS, "engine", "frames.mjs"), look, jf, out_dir], cwd=RS, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"look {look} failed:\n" + r.stdout[-1500:] + r.stderr[-3000:])
    log("   " + (r.stdout.strip().splitlines() or ["look done"])[-1])
    open(done, "w").write(key)
    return out_dir


def cues(out_dir):
    try:
        return json.load(open(os.path.join(out_dir, "cues.json")))
    except (OSError, ValueError):
        return []


def texts(out_dir):
    try:
        return json.load(open(os.path.join(out_dir, "texts.json")))
    except (OSError, ValueError):
        return []
