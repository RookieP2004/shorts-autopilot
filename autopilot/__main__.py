"""shorts-autopilot CLI

  python -m autopilot validate jobs/<id>/job.json
  python -m autopilot frames   jobs/<id>/job.json [--at 0.5,3.2] [--out preview/]
  python -m autopilot render   jobs/<id>/job.json [--out jobs/<id>/out]
  python -m autopilot zapier   jobs/<id>/job.json   (fields for Zapier's YouTube "Upload Video")
  python -m autopilot logline  jobs/<id>/job.json --youtube-id ID   (row for the Google Docs log)
  python -m autopilot characters
  python -m autopilot budget [--need upload|stats] [--add upload|stats|other --ref ID]
      (Zapier task budget; --need exits 3 if the call would go over the free-plan cap)
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
    b = sub.add_parser("budget"); b.add_argument("--need"); b.add_argument("--add"); b.add_argument("--ref", default="")
    b.add_argument("--n", type=int, default=1)
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

    elif args.cmd == "budget":
        from . import budget
        if args.add:
            budget.record(args.add, args.ref, args.n)
        st = budget.status()
        print(f"Zapier: {st['calls_used']} calls ({st['tasks_used']} tasks) in the last {st['window_days']} days; "
              f"cap {st['cap_calls']} calls of the {st['plan_tasks']}-task plan; {st['calls_left']} left")
        if args.need:
            ok = budget.allowed(args.need, st)
            print(("OK: " if ok else "NO BUDGET: ") + args.need)
            if not ok:
                sys.exit(3)


if __name__ == "__main__":
    main()
