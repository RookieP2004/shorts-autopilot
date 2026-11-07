"""Render one blendkit shot script to PNG frames.

  python -m autopilot.blendrun <script.py> <out_dir> <dur_s> <fps> <w> <h> [samples]

The script runs with these names defined: DUR, FPS, W, H, OUT, SAMPLES, plus everything from autopilot.blendkit.
It should call reset(W, H, FPS, DUR, ...) first and build the scene; this runner calls render(OUT) afterwards
unless the script already did. Output is cached: if out_dir/.done matches the script + settings, nothing re-renders.
"""
import hashlib
import json
import os
import sys
import time


def main():
    script, out, dur, fps, w, h = sys.argv[1:7]
    samples = int(sys.argv[7]) if len(sys.argv) > 7 else 24
    dur, fps, w, h = float(dur), int(fps), int(w), int(h)
    src = open(script).read()
    sig = hashlib.sha1(json.dumps([src, dur, fps, w, h, samples]).encode()).hexdigest()
    done = os.path.join(out, ".done")
    if os.environ.get("BK_FRAMES"):
        sig = None                              # previews are never cached
    if sig and os.path.exists(done) and open(done).read() == sig:
        print("cached", out)
        return
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from autopilot import blendkit
    ns = {k: getattr(blendkit, k) for k in dir(blendkit) if not k.startswith("_")}
    ns.update(DUR=dur, FPS=fps, W=w, H=h, OUT=out, SAMPLES=samples, __file__=script, __name__="__shot__")
    t0 = time.time()
    exec(compile(src, script, "exec"), ns)
    if not (os.path.isdir(out) and any(f.endswith(".png") for f in os.listdir(out))):
        blendkit.render(out)
    if sig:
        open(done, "w").write(sig)
    n = len([f for f in os.listdir(out) if f.endswith(".png")])
    print(f"rendered {n} frames in {time.time() - t0:.0f}s -> {out}")


if __name__ == "__main__":
    main()
