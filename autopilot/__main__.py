"""shorts-autopilot CLI

  python -m autopilot validate jobs/<id>/job.json
  python -m autopilot frames   jobs/<id>/job.json [--at 0.5,3.2] [--out preview/]
  python -m autopilot render   jobs/<id>/job.json [--out jobs/<id>/out]
  python -m autopilot zapier   jobs/<id>/job.json   (fields for Zapier's YouTube "Upload Video")
  python -m autopilot logline  jobs/<id>/job.json --youtube-id ID   (row for the Google Docs log)
  python -m autopilot characters
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
    z = sub.add_parser("zapier"); z.add_argument("job")
    lg = sub.add_parser("logline"); lg.add_argument("job"); lg.add_argument("--youtube-id", default="")
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
    elif args.cmd == "zapier":
        from .publish import zapier_fields
        print(json.dumps(zapier_fields(load_json(args.job), load_style()), indent=2, ensure_ascii=False))
    elif args.cmd == "logline":
        from .publish import log_line
        print(log_line(args.job, args.youtube_id))
    elif args.cmd == "characters":
        for cid, c in load_characters().items():
            print(f"{cid}: poses={c['poses']} voice={c['meta'].get('voice')} - {c['meta'].get('description','')}")


if __name__ == "__main__":
    main()
