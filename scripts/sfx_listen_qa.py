"""Listen to every real recording in the sound library with YAMNet (AudioSet labels; via Clipwing Real SFX's listen.py,
model from huggingface.co/audiomagic/yamnet-onnx, Apache-2.0) and drop takes that don't sound like their name.
Run: python scripts/sfx_listen_qa.py [--realsfx /tmp/snd/clipwing/skills/real-sfx] [--apply]
"""
import argparse, json, os, re, subprocess, sys
LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sfx", "lib")
# a take passes when any of these AudioSet words appears in its tags (case-insensitive)
EXPECT = {
    "coin": "coin|cash|jingle|clink|glass|metal|chink|tick|ding", "door": "door|slam|knock|wood|thump|cupboard",
    "heartbeat": "heart|thump|drum|bass", "marker": "writing|scrap|rub|squeak|paper|pencil|sniff|hiss",
    "paper": "paper|rustl|crumpl|scrap|page|tear|hiss|noise", "projector": "mechan|projector|engine|clicking|tick|whir|sewing|motor|vehicle",
    "register": "cash|register|ding|bell|mechan|print|clink|typewriter|tick|click", "shutter": "camera|click|shutter|tick|mechan|rattle",
    "splash": "splash|water|slosh|drip|liquid|pour|bath|plop", "stamp": "knock|thump|tap|wood|slam|stamp|chop|clap",
    "tape": "tear|rip|tape|scrap|zipper|rustl|crack", "thud": "thump|thud|bang|slam|knock|drum|bass|boom|wood",
    "tick": "tick|click|clock|tap|knock|wood|metronome", "type": "typ|keyboard|click|tap|clack|tick",
    "vibrate": "buzz|vibrat|hum|mains|insect|rattle|bee|mosquito|fly", "whoosh": "whoosh|swoosh|swish|wind|air|rustl|noise|hiss|jet|flap",
    "bubbles": "bubbl|water|liquid|pop|gurgl|drip|boing|plop", "footsteps": "walk|footstep|step|run|shuffl|stomp",
}
REALSFX = os.environ.get("REAL_SFX_DIR", "/tmp/snd/clipwing/skills/real-sfx")


def heard(path, realsfx=REALSFX):
    r = subprocess.run([sys.executable, os.path.join(realsfx, "scripts", "listen.py"), "describe", path], capture_output=True, text=True)
    return (re.search(r"tags\s*:\s*(.*)", r.stdout) or [None, ""])[1]


def heard_ok(name, path, realsfx=REALSFX):
    """(passes, tags): does the recording sound like `name`? Names without expectations pass."""
    tags = heard(path, realsfx)
    return (bool(re.search(EXPECT[name], tags, re.I)) if name in EXPECT else True), tags


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--realsfx", default="/tmp/snd/clipwing/skills/real-sfx"); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    man_p = os.path.join(LIB, "manifest.json"); man = json.load(open(man_p))
    drop = []
    for name in sorted(os.listdir(LIB)):
        d = os.path.join(LIB, name)
        if not os.path.isdir(d) or name not in EXPECT:
            continue
        for f in sorted(os.listdir(d)):
            if not f.startswith("ov_"):
                continue
            ok, tags = heard_ok(name, os.path.join(d, f), a.realsfx)
            print(f"{'OK  ' if ok else 'DROP'} {name}/{f:10s} {tags[:90]}")
            if not ok:
                drop.append(f"{name}/{f}")
            else:
                man.setdefault(f"{name}/{f}", {})["heard"] = tags[:120]
    if a.apply:
        for k in drop:
            os.remove(os.path.join(LIB, k)); man.pop(k, None)
        json.dump(dict(sorted(man.items())), open(man_p, "w"), indent=1)
        cr = os.path.join(os.path.dirname(LIB), "CREDITS.md")
        lines = open(cr).read().splitlines()
        open(cr, "w").write("\n".join(l for l in lines if not any(l.startswith(f"- {k}:") for k in drop)) + "\n")
    print(f"{len(drop)} takes {'dropped' if a.apply else 'would be dropped'}")


if __name__ == "__main__":
    main()
