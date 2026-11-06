"""Summarise channel stats for the weekly review.

  python scripts/analyze.py stats/latest.json [--min-age-hours 48] [--days 28]

Input JSON (built in the review run from Zapier/YouTube numbers + the Google Docs log):
  {"pulled_at": "...", "channel": {"title":..,"subscriberCount":..},
   "videos": [{"youtube_id","title","published" (ISO),"views","likes","comments",
               "duration" ("PT34S") or "secs", "format","hook","topic",
               optional "avg_view_pct","subs_gained","privacy"}]}

Prints: channel totals, per-format / per-hook tables (median views, retention, likes per 1k views,
subs gained), top and bottom videos, and length vs retention. Only public videos older than
--min-age-hours count, so new uploads don't drag numbers down.
"""
import argparse
import datetime as dt
import json
import os
import re
import statistics as stx
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def iso_dur(s):
    m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", s or "")
    return (int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else None


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(stx.median(xs), 1) if xs else None


def table(rows, key, title):
    g = defaultdict(list)
    for r in rows:
        g[r.get(key) or "?"].append(r)
    print(f"\n## by {title}")
    print(f"{'group':<22}{'n':>4}{'med views':>11}{'med ret%':>10}{'likes/1k':>10}{'subs':>6}")
    out = []
    for k, rs in g.items():
        likes = sum(r.get("likes", 0) for r in rs)
        views = sum(r.get("views", 0) for r in rs)
        out.append((k, len(rs), med([r.get("views") for r in rs]), med([r.get("avg_view_pct") for r in rs]),
                    round(1000 * likes / views, 1) if views else None,
                    sum(r.get("subs_gained") or 0 for r in rs)))
    for k, n, mv, mr, lk, sg in sorted(out, key=lambda x: -(x[2] or 0)):
        print(f"{str(k)[:21]:<22}{n:>4}{mv if mv is not None else '-':>11}{mr if mr is not None else '-':>10}"
              f"{lk if lk is not None else '-':>10}{sg:>6}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stats", nargs="?", default=os.path.join(ROOT, "stats", "latest.json"))
    ap.add_argument("--min-age-hours", type=float, default=48)
    ap.add_argument("--days", type=int, default=28)
    a = ap.parse_args()
    p = a.stats
    if not os.path.exists(p):
        raise SystemExit(f"no stats file at {p}")
    data = json.load(open(p, encoding="utf-8"))
    now = dt.datetime.now(dt.timezone.utc)
    rows = []
    for v in data["videos"]:
        if v.get("privacy", "public") != "public" or not v.get("published"):
            continue
        pub = dt.datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
        age_h = (now - pub).total_seconds() / 3600
        if age_h < a.min_age_hours or age_h > a.days * 24:
            continue
        v["age_h"] = round(age_h)
        v["secs"] = v.get("secs") or iso_dur(v.get("duration"))
        rows.append(v)
    ch = data.get("channel", {})
    print(f"# {ch.get('title')}  subs={ch.get('subscriberCount')} views={ch.get('viewCount')} "
          f"videos={ch.get('videoCount')}  (stats pulled {data.get('pulled_at', '?')})")
    print(f"{len(rows)} public videos aged {a.min_age_hours:.0f}h-{a.days}d in this analysis")
    if not rows:
        return
    print(f"channel median views: {med([r['views'] for r in rows])}, "
          f"median retention: {med([r.get('avg_view_pct') for r in rows])}%")
    table(rows, "format", "format")
    table(rows, "hook", "hook")
    rs = sorted(rows, key=lambda r: -r["views"])
    print("\n## top 5")
    for r in rs[:5]:
        print(f"{r['views']:>8} views  ret {r.get('avg_view_pct','-')}%  {r.get('secs')}s  "
              f"[{r.get('format')}/{r.get('hook')}] {r['title']}")
    print("\n## bottom 5")
    for r in rs[-5:]:
        print(f"{r['views']:>8} views  ret {r.get('avg_view_pct','-')}%  {r.get('secs')}s  "
              f"[{r.get('format')}/{r.get('hook')}] {r['title']}")
    print("\n## length vs retention")
    for lo, hi in ((0, 20), (20, 30), (30, 40), (40, 61)):
        b = [r for r in rows if r.get("secs") is not None and lo <= r["secs"] < hi]
        if b:
            print(f"{lo:>2}-{hi:<2}s  n={len(b):<3} med views {med([r['views'] for r in b])}  "
                  f"med ret {med([r.get('avg_view_pct') for r in b])}%")
    untagged = [r for r in rows if not r.get("format")]
    if untagged:
        print(f"\nnote: {len(untagged)} videos have no format tag (posted outside the pipeline?)")


if __name__ == "__main__":
    main()
