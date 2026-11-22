"""shorts-autopilot CLI

  python -m autopilot validate jobs/<id>/job.json
  python -m autopilot frames   jobs/<id>/job.json [--at 0.5,3.2] [--out preview/]
  python -m autopilot render   jobs/<id>/job.json [--out jobs/<id>/out]
  python -m autopilot zapier   jobs/<id>/job.json   (fields for Zapier's YouTube "Upload Video")
  python -m autopilot logline  jobs/<id>/job.json --youtube-id ID   (row for the Google Docs log)
  python -m autopilot thumbnail jobs/<id>/job.json   (long videos: 1280x720 thumbnail -> out/thumbnail.jpg)
  python -m autopilot characters
  python -m autopilot budget [--need upload|stats|docs|thumb [--ref ID]] [--add upload|stats|other --ref ID] [--bonus] [--sync TASKS]
      (Zapier task budget; --need exits 3 if the call would go over the free-plan cap;
       --bonus prints how many extra Shorts to post today from tasks that would expire at the reset;
       --spare prints calls free for optional extras (e.g. rewriting the Bible doc) before the reset;
       --sync sets the ledger to the "tasks used" number shown on Zapier's billing page)
"""
import argparse
import json
import os
import sys

from .spec import ROOT, job_style, load_characters, load_json, load_style, validate_job


def main(argv=None):
    ap = argparse.ArgumentParser(prog="autopilot")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("job")
    f = sub.add_parser("frames"); f.add_argument("job"); f.add_argument("--at"); f.add_argument("--out"); f.add_argument("--no-guides", action="store_true")
    r = sub.add_parser("render"); r.add_argument("job"); r.add_argument("--out"); r.add_argument("--workers", type=int)
    z = sub.add_parser("zapier"); z.add_argument("job")
    rp = sub.add_parser("refphoto"); rp.add_argument("action", choices=["get"]); rp.add_argument("name")
    rp.add_argument("--license", required=True); rp.add_argument("--author", required=True)
    rp.add_argument("--frame", default="polaroid"); rp.add_argument("--caption", default=""); rp.add_argument("--out", required=True)
    rp.add_argument("--job", default=None); rp.add_argument("--seed", type=int, default=0)
    vr = sub.add_parser("variety"); vr.add_argument("--seed", type=int, default=None)
    lg = sub.add_parser("logline"); lg.add_argument("job"); lg.add_argument("--youtube-id", default="")
    th = sub.add_parser("thumbnail"); th.add_argument("job"); th.add_argument("--out")
    ig = sub.add_parser("instagram"); ig.add_argument("job"); ig.add_argument("--video-url"); ig.add_argument("--cover-url")
    ig.add_argument("--caption-only", action="store_true")
    ig.add_argument("--manual-window", type=float, default=0, help="minutes the owner gets to post it by hand first")
    ig.add_argument("--since", type=float, help="epoch seconds when the owner was notified (default: now)")
    sub.add_parser("characters")
    b = sub.add_parser("budget"); b.add_argument("--need"); b.add_argument("--add"); b.add_argument("--ref", default="")
    b.add_argument("--n", type=int, default=1)
    b.add_argument("--bonus", action="store_true"); b.add_argument("--spare", action="store_true"); b.add_argument("--sync", type=int)
    args = ap.parse_args(argv)

    if args.cmd == "validate":
        job = load_json(args.job)
        errs = validate_job(job, job_style(job), load_characters())
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
        job = load_json(args.job)
        print(json.dumps(zapier_fields(job, job_style(job), args.job), indent=2, ensure_ascii=False))
    elif args.cmd == "refphoto":
        from .refphoto import get
        print(get(args.name, args.license, args.author, args.frame, args.caption, args.out, args.job, args.seed))
    elif args.cmd == "variety":
        from .variety import report
        print(report(args.seed))
    elif args.cmd == "logline":
        from .publish import log_line
        print(log_line(args.job, args.youtube_id))
    elif args.cmd == "thumbnail":
        from .render import thumbnail
        print(thumbnail(args.job, args.out))
    elif args.cmd == "instagram":
        from .instagram import caption, manual_window, post_reel
        if args.caption_only:
            print(caption(load_json(args.job)))
        elif args.manual_window:
            manual_window(args.job, args.video_url, args.cover_url, args.manual_window, args.since)
        else:
            print(post_reel(args.job, args.video_url, args.cover_url))
    elif args.cmd == "characters":
        for cid, c in load_characters().items():
            print(f"{cid}: poses={c['poses']} voice={c['meta'].get('voice')} - {c['meta'].get('description','')}")

    elif args.cmd == "budget":
        from . import budget
        if args.add:
            budget.record(args.add, args.ref, args.n)
        if args.sync is not None:
            print(f"synced: added {budget.sync(args.sync)} calls from outside this channel")
        st = budget.status()
        span = (f"the Zapier trial (ends {st['reset']}, {st['days_left']} day(s) left)" if st["cycle_day"] == "trial"
                else f"this cycle (resets {st['reset']}, {st['days_left']} day(s) left)" if st["cycle_day"]
                else f"the last {st['window_days']} days (set zapier.cycle_day in style.json to enable bonus Shorts)")
        print(f"Zapier: {st['calls_used']} calls ({st['tasks_used']} tasks) in {span}; "
              f"cap {st['cap_calls']} calls of the {st['plan_tasks']}-task plan; {st['calls_left']} left")
        if args.bonus:
            print(f"BONUS {budget.bonus_today(st)}")
        if args.spare:
            print(f"SPARE {budget.spare(st)}")
        if args.need == "upload" and budget.replaced_by_long(args.ref, st):
            print("SKIP: today's long video replaces the regular Short on the free plan")
            sys.exit(4)
        if args.need:
            ok = budget.allowed(args.need, st)
            print(("OK: " if ok else "NO BUDGET: ") + args.need)
            if not ok:
                sys.exit(3)


if __name__ == "__main__":
    main()
