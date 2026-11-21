"""Add REAL recordings (Openverse, CC0 / public domain only) to the sound library: assets/sfx/lib/<name>/ov_<k>.flac.
They outrank the earshot renders and the UI pack (autopilot.audio.SOURCE_RANK), so these names start sounding like a
person with a good library cut them. Every file is logged in assets/sfx/lib/manifest.json and assets/sfx/CREDITS.md.
Run: python scripts/openverse_fetch.py [--only cash,paper] [--per 3]
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import openverse
from build_sfx_lib import EARSHOT, LIB  # noqa: E402

QUERIES = {   # name -> what to ask Openverse for (real foley first; the code-made layer stays as fallback)
    "cash": "counting banknotes", "coin": "coin drop table", "paper": "paper sheet slide", "tape": "tape rip",
    "stamp": "rubber stamp", "shutter": "camera shutter", "type": "typewriter typing", "footsteps": "footsteps hallway",
    "splash": "water splash", "bubbles": "underwater bubbles", "door": "door close", "register": "cash register",
    "heartbeat": "heartbeat", "tick": "clock tick", "vibrate": "phone vibrate", "marker": "marker pen writing",
    "thud": "heavy thud", "whoosh": "whoosh", "projector": "film projector",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--per", type=int, default=3)
    a = ap.parse_args()
    only = set(filter(None, a.only.split(",")))
    mpath = os.path.join(LIB, "manifest.json")
    man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    credits = []
    for name, q in QUERIES.items():
        if only and name not in only:
            continue
        lufs, max_s = EARSHOT.get(name, (None, -19, 1.5))[1:]
        res = openverse.search_audio(q, max_s=max(4.0, max_s * 3))
        d = os.path.join(LIB, name)
        os.makedirs(d, exist_ok=True)
        got = 0
        for r in res:
            if got >= a.per:
                break
            out = f"ov_{got}.flac"
            try:
                openverse.download(r, os.path.join(d, out), max_s=max_s, lufs=lufs)
            except Exception as e:
                print(f"  skip {r['id']}: {e}")
                continue
            man[f"{name}/{out}"] = {"source": f"openverse/{r['source']}", "id": r["id"], "title": r["title"], "creator": r["creator"],
                                    "licence": f"{r['license']} {r.get('license_version') or ''}".strip(), "landing": r["landing"]}
            credits.append(f"- {name}/{out}: \"{r['title']}\" by {r['creator']} ({r['source']}, {r['license'].upper()}) {r['landing']}")
            got += 1
        print(f"{name}: {got} real recordings")
    json.dump(dict(sorted(man.items())), open(mpath, "w"), indent=1)
    with open(os.path.join(os.path.dirname(LIB), "CREDITS.md"), "a") as f:
        f.write("\n".join(credits) + ("\n" if credits else ""))


if __name__ == "__main__":
    main()
