"""Cutaway connector: 3D "how it works" shots (three.js cutaways: macro / cut-open / whole, labels pinned to parts, 3D word
stamps, honesty plates) made with the owner's purchased Cutaway skill, played inside our videos as a `video` layer.

Licence (owner bought Cutaway, 2026-11-21): use and change it for the channel, publish the videos anywhere; never put
its code, text or guides in this PUBLIC repo. So:
  - the skill is read from the owner's private account skill/plugin (or CUTAWAY_DIR), never copied here;
  - reel folders (copies of its template plus our scene code) live outside the repo, in /tmp/cutaway-reels/;
  - only the rendered clip (our output) and its sound cues (our data) land in jobs/<id>/assets/.
Its 55 sounds are CC0 and are in our library (cw_ takes).

  python -m autopilot.cutaway where                                  where the skill is (or why not)
  python -m autopilot.cutaway new <name>                             copy the reel template to /tmp/cutaway-reels/<name>, npm setup
  python -m autopilot.cutaway render <reel_dir> <out.mp4> [--from S --to S --samples 1 --workers 2]
Rendering has no GPU here: about 5 s a frame at 1080x1920 with one sample, so plan 3-6 s of cutaway per Short (5-12 min).
"""
import glob
import json
import os
import shutil
import subprocess
import sys

REELS = os.environ.get("CUTAWAY_REELS", "/tmp/cutaway-reels")
# Cutaway cue-sheet roles -> our sound-library names
ROLE = {"swoosh": "whoosh", "sweep": "sweep", "press": "press", "click": "latch", "latch": "latch", "ratchet": "ratchet",
        "ping": "ding", "chime": "chime", "bubble": "bubbles", "pop": "pop", "tick": "tick", "slide": "slide", "hum": "hum"}


def skill_dir():
    """The Cutaway skill folder (the one holding SKILL.md and reel-template/), from the owner's private install."""
    home = os.path.expanduser("~")
    cands = [os.environ.get("CUTAWAY_DIR", "")]
    cands += [os.path.join(home, ".claude", "skills", "cutaway")]
    cands += glob.glob(os.path.join(home, ".claude", "skills", "synced", "*", "cutaway"))
    cands += glob.glob(os.path.join(home, ".claude", "plugins", "**", "skills", "cutaway"), recursive=True)
    cands += glob.glob("/tmp/skillzip/*/cutaway/skills/cutaway")
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "SKILL.md")) and os.path.isdir(os.path.join(c, "reel-template")):
            return c
    return None


def need_skill():
    d = skill_dir()
    if not d:
        raise SystemExit("cutaway: the Cutaway skill is not installed in this session. The owner adds it once to their Claude "
                         "account (Customize > Plugins > Upload plugin, the Cutaway ZIP), or set CUTAWAY_DIR. Skip the "
                         "cutaway shot rather than copying Cutaway into the repo (its licence forbids a public copy).")
    return d


def new(name):
    sd = need_skill()
    dst = os.path.join(REELS, name)
    if os.path.exists(dst):
        return dst
    os.makedirs(REELS, exist_ok=True)
    shutil.copytree(os.path.join(sd, "reel-template"), dst)
    r = subprocess.run(["npm", "run", "setup"], cwd=dst, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("cutaway: npm run setup failed:\n" + (r.stdout + r.stderr)[-2000:])
    print(f"cutaway: reel folder {dst} (template from {sd}). Write scene/reel.js + the subject module there with the "
          f"Cutaway skill's guidance; keep it out of the repo.")
    return dst


def cues_from_sheet(reel_dir, frm=0.0, to=None):
    """The reel's sound cues (its cue-sheet.json) as our sfx cues, relative to `frm`: [{t, sfx, gain}]."""
    p = os.path.join(reel_dir, "cue-sheet.json")
    if not os.path.exists(p):
        return []
    c = json.load(open(p))
    to = c.get("seconds", 1e9) if to is None else to
    out = []
    for e in c.get("events", []):
        nm = ROLE.get(e.get("role"))
        if nm and frm <= e["t"] < to:
            out.append({"t": round(e["t"] - frm, 3), "sfx": nm, "gain": e.get("gain", 0.8)})
    for t in c.get("ticks", []):
        if frm <= t < to:
            out.append({"t": round(t - frm, 3), "sfx": "tick", "gain": 0.45})
    return sorted(out, key=lambda x: x["t"])


def render(reel_dir, out_mp4, frm=None, to=None, samples=1, workers=2, log=print):
    """Export the reel (or a stretch of it) silent, copy it to out_mp4, and write out_mp4 + '.cues.json' (its sounds)."""
    reel_dir = os.path.abspath(reel_dir)
    tmp_out = os.path.join(reel_dir, "renders", "for_autopilot.mp4")
    cmd = ["node", "studio.mjs", "export", "--samples", str(samples), "--workers", str(workers), "--audio", "none",
           "--out", tmp_out]
    if frm is not None:
        cmd += ["--from", str(frm)]
    if to is not None:
        cmd += ["--to", str(to)]
    log("cutaway: " + " ".join(cmd[1:]))
    r = subprocess.run(cmd, cwd=reel_dir, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("cutaway: export failed:\n" + (r.stdout + r.stderr)[-2000:])
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)), exist_ok=True)
    shutil.copyfile(tmp_out, out_mp4)
    cues = cues_from_sheet(reel_dir, frm or 0.0, to)
    json.dump({"source": "Cutaway reel (owner's licence); clip and cues are our output", "from": frm, "to": to,
               "cues": cues}, open(out_mp4 + ".cues.json", "w"), indent=1)
    log(f"cutaway: {out_mp4} ({len(cues)} sound cues)")
    return out_mp4


def main(argv):
    if not argv or argv[0] == "where":
        d = skill_dir()
        print(d or "not installed (see need_skill)")
        return
    if argv[0] == "new":
        new(argv[1])
    elif argv[0] == "render":
        a = argv[1:]
        opt = lambda k, d=None: (a[a.index(k) + 1] if k in a else d)  # noqa: E731
        render(a[0], a[1], frm=float(opt("--from")) if opt("--from") else None, to=float(opt("--to")) if opt("--to") else None,
               samples=int(opt("--samples", 1)), workers=int(opt("--workers", 2)))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
