"""shorts-autopilot CLI

  python -m autopilot validate jobs/<id>/job.json
  python -m autopilot frames   jobs/<id>/job.json [--at 0.5,3.2] [--out preview/]
  python -m autopilot render   jobs/<id>/job.json [--out jobs/<id>/out]
  python -m autopilot upload   jobs/<id>/job.json jobs/<id>/out/final.mp4
  python -m autopilot stats
  python -m autopilot auth     client_secret.json      (run once on your own computer)
  python -m autopilot recent   [--n 20]                 (what was posted lately)
"""
import argparse
import json
import os
import sys

from .spec import ROOT, load_characters, load_json, load_style, validate_job


def main(argv=None):
    ap = argparse.ArgumentParser(prog="autopilot")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("job")
    f = sub.add_parser("frames"); f.add_argument("job"); f.add_argument("--at"); f.add_argument("--out"); f.add_argument("--no-guides", action="store_true")
    r = sub.add_parser("render"); r.add_argument("job"); r.add_argument("--out"); r.add_argument("--workers", type=int)
    u = sub.add_parser("upload"); u.add_argument("job"); u.add_argument("video")
    sub.add_parser("stats")
    a = sub.add_parser("auth"); a.add_argument("client_secret")
    rc = sub.add_parser("recent"); rc.add_argument("--n", type=int, default=20)
    sub.add_parser("characters")
    args = ap.parse_args(argv)

    if args.cmd == "validate":
        job = load_json(args.job)
        errs = validate_job(job, load_style(), load_characters())
        if errs:
            print("INVALID"); [print("  -", e) for e in errs]; sys.exit(1)
        print("OK")
    elif args.cmd == "frames":
        from .render import frames
        times = [float(x) for x in args.at.split(",")] if args.at else None
        out = args.out or os.path.join(os.path.dirname(args.job), "preview")
        for p in frames(args.job, out, times, guides=not args.no_guides):
            print(p)
    elif args.cmd == "render":
        from .render import render
        out = args.out or os.path.join(os.path.dirname(args.job), "out")
        render(args.job, out, workers=args.workers)
    elif args.cmd == "upload":
        from .youtube import upload
        print(json.dumps(upload(args.job, args.video), indent=2))
    elif args.cmd == "stats":
        from .youtube import stats
        stats()
    elif args.cmd == "auth":
        from .youtube import auth
        auth(args.client_secret)
    elif args.cmd == "recent":
        p = os.path.join(ROOT, "data", "videos.jsonl")
        rows = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []
        for L in rows[-args.n:]:
            print(f"{L.get('posted_at','')[:16]}  {L.get('format','?'):<14} {L.get('topic','?'):<28} {L['title']}")
    elif args.cmd == "characters":
        for cid, c in load_characters().items():
            print(f"{cid}: poses={c['poses']} voice={c['meta'].get('voice')} - {c['meta'].get('description','')}")


if __name__ == "__main__":
    main()
