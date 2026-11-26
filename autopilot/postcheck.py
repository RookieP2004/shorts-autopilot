"""End-of-run check (owner, 2026-11-26: "learn from problems like this, they should not repeat"). A Short is only done
when it is on YouTube, has its thumbnail, and its Reel is handled. Prints what's missing, or POSTCHECK OK.
  python -m autopilot postcheck 2026-11-26-a"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(sid):
    miss = []
    log = open(os.path.join(ROOT, "channel", "memory", "log.md"), encoding="utf-8").read().splitlines()
    line = next((l for l in log if l.startswith(sid + " |")), None)
    if not line:
        miss.append(f"no log.md line for {sid}")
    else:
        if not re.search(r"youtube\.com/shorts/[\w-]{11}|youtu\.be/[\w-]{11}|watch\?v=[\w-]{11}", line):
            miss.append("no YouTube link in the log line: the video is not posted (see lessons.md, 11-24/11-26)")
        if not sid.endswith("-L") and " | IG " not in line:
            miss.append("no Instagram Reel in the log line")
    led = json.load(open(os.path.join(ROOT, "channel", "zapier_ledger.json")))
    calls = led["calls"] if isinstance(led, dict) and "calls" in led else led
    kinds = {c.get("kind") for c in calls if c.get("ref") == sid}
    if "upload" not in kinds:
        miss.append("no upload recorded in the Zapier ledger")
    if "thumb" not in kinds:
        miss.append("no thumbnail set yet: set it 10-15 min after the upload (lessons.md, 11-13/11-26)")
    return miss


def main(argv):
    sid = argv[0]
    miss = check(sid)
    if miss:
        print("POSTCHECK MISSING for " + sid + ":\n- " + "\n- ".join(miss))
        return 1
    print("POSTCHECK OK " + sid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
