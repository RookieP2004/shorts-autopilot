"""Build the channel's sound-effect library (owner, 2026-11-21: use Openverse, Real SFX and earshot).

assets/sfx/lib/<name>/<source>_<k>.flac, 48 kHz mono, loudness set per role; assets/sfx/lib/manifest.json says where every
file came from. Sources, best first (the real-sfx rule: real recordings beat code-made ones):
  ov_*   real recordings from Openverse (CC0 / public domain only), added by scripts/openverse_fetch.py
  ui_*   uisfx interface sounds shipped with Clipwing's Real SFX skill (CC0)
  es_*   earshot renders (MIT tool; "every sound it makes is yours"): realistic designs rebuilt in code, 3 takes each
autopilot.audio.sfx() picks a take per use (seeded), so repeats never sound identical; synth is the last fallback.
Run: python scripts/build_sfx_lib.py [--uisfx PATH_TO_uisfx/sounds] [--only name,name]
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "assets", "sfx", "lib")

# name -> (earshot design ids or words, loudness in LUFS, max seconds)
EARSHOT = {
    "whoosh": (["whoosh/fast", "whoosh/soft", "swoosh/in"], -18, 0.8),
    "swoosh_soft": (["whoosh/soft", "swoosh/out", "whoosh/airy"], -21, 0.7),
    "riser": (["a rising cinematic tension riser that swells and stops"], -20, 2.0),
    "boom": (["boom/deep", "boom/heavy", "boom/short"], -14, 1.8),
    "hit": (["slam/title", "impact/suck", "hit/crit"], -14, 1.4),
    "thud": (["hit/drop", "boom/short", "boom/door"], -15, 0.8),
    "stomp": (["hit/crit", "slam/title", "hit/drop"], -14, 0.9),
    "braam": (["braam/brass"], -15, 3.0),
    "paper": (["slide/paper", "paper/page", "paper/card"], -20, 0.8),
    "tape": (["tape/peel"], -20, 0.9),
    "marker": (["marker/whiteboard"], -22, 1.2),
    "shutter": (["camera/shutter"], -18, 0.5),
    "type": (["type/run", "keyboard/mechanical", "typewriter/key"], -21, 1.5),
    "stamp": (["stamp/press"], -15, 0.6),
    "splash": (["splash/small", "splash/plunge", "splash/big"], -17, 1.3),
    "bubbles": (["bubble/rise", "water/plop"], -20, 1.2),
    "footsteps": (["step/tile", "step/concrete", "step/wood"], -19, 1.6),
    "heartbeat": (["heartbeat/pulse"], -16, 1.0),
    "tick": (["clock/tick", "tick/wood", "tick/metal"], -20, 0.3),
    "slide": (["slide/panel", "slide/paper"], -20, 0.6),
    "cash": (["coins/handful", "coin/drop", "cash_register/open"], -17, 1.6),
    "coin": (["coin/drop", "coin/flip", "tick/metal"], -18, 1.0),
    "register": (["cash_register/open"], -16, 2.4),
    "glitch": (["glitch/short"], -19, 0.4),
    "door": (["door/close", "door/slam", "door/knock"], -17, 1.0),
    "vibrate": (["phone/vibrate"], -18, 1.6),
    "click": (["tick/switch", "pen/click", "tick/key"], -22, 0.3),
    "ding": (["coin/bright", "success/done"], -19, 1.0),
    "projector": (["an old film projector running, a mechanical clatter"], -24, 2.0),
}
# name -> uisfx files (CC0) relative to uisfx/sounds
UISFX = {
    "pop": ["soft/select.mp3", "glass/select.mp3", "minimal/press.mp3"],
    "click": ["minimal/select.mp3", "mechanical/press.mp3"],
    "ding": ["glass/success.mp3", "minimal/complete.mp3"],
    "notify": ["minimal/notification.mp3", "glass/notification.mp3", "soft/notification.mp3"],
    "error": ["minimal/error.mp3", "glass/error.mp3"],
    "success": ["glass/success.mp3", "soft/success.mp3"],
    "lock": ["minimal/lock.mp3", "mechanical/lock.mp3"],
}
TAKES = 3


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(" ".join(cmd) + "\n" + r.stderr[-800:])
    return r.stdout


def trim_norm(src, dst, max_s, lufs):
    # trim to max_s with a short fade, mono 48 kHz, loudness-normalised (single-pass loudnorm is fine for short cues)
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-t", str(max_s), "-ac", "1", "-ar", "48000",
         "-af", f"afade=t=out:st={max(0.0, max_s - 0.08)}:d=0.08,loudnorm=I={lufs}:TP=-1.5:LRA=11", dst])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uisfx", default="")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = set(filter(None, a.only.split(",")))
    os.makedirs(LIB, exist_ok=True)
    mpath = os.path.join(LIB, "manifest.json")
    man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    tmp = tempfile.mkdtemp()
    for name, (designs, lufs, max_s) in EARSHOT.items():
        if only and name not in only:
            continue
        d = os.path.join(LIB, name)
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f.startswith("es_"):
                os.remove(os.path.join(d, f))
        k = 0
        for di, des in enumerate(designs):
            for seed in range(1, (TAKES if len(designs) == 1 else 2) + 1):
                raw = os.path.join(tmp, f"{name}_{di}_{seed}.wav")
                arg = ["--sound", des] if "/" in des and " " not in des else [des]
                run(["earshot", "make", *arg, "-o", raw, "--seed", str(seed), "--mono"])
                out = f"es_{k}.flac"
                trim_norm(raw, os.path.join(d, out), max_s, lufs)
                man[f"{name}/{out}"] = {"source": "earshot", "design": des, "seed": seed, "licence": "made with earshot (MIT); output is ours"}
                k += 1
        print(f"{name}: {k} earshot takes")
    if a.uisfx:
        for name, files in UISFX.items():
            if only and name not in only:
                continue
            d = os.path.join(LIB, name)
            os.makedirs(d, exist_ok=True)
            for k, f in enumerate(files):
                out = f"ui_{k}.flac"
                lufs = EARSHOT.get(name, (None, -20, 1.0))[1]
                trim_norm(os.path.join(a.uisfx, f), os.path.join(d, out), 1.5, lufs)
                man[f"{name}/{out}"] = {"source": "uisfx (via Clipwing real-sfx)", "file": f, "licence": "CC0 1.0"}
            print(f"{name}: {len(files)} uisfx")
    json.dump(dict(sorted(man.items())), open(mpath, "w"), indent=1)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
