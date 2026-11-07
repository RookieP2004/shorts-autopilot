"""Zapier task budget.

Every successful Zapier MCP call costs `tasks_per_call` tasks (2). The free plan has 100 tasks per
billing cycle. Successful calls are kept in channel/zapier_ledger.json (committed to the repo, so
every fresh scheduled run sees it). Failed calls cost 0 tasks: only record a call after it succeeded.

Trial: while today is before `trial_until`, the plan is `trial_tasks` (Zapier's 14-day Pro trial,
1,000 tasks) and the "reset" is the trial's end, so the bonus logic posts the full `max_per_day`.
Calls made during the trial never count against the free plan afterwards.

Two modes after the trial:
- `cycle_day` unknown (null): count calls over a rolling 31 days. Safe whatever day the cycle
  resets, but no end-of-cycle bonus, because we can't know when the leftovers would expire.
- `cycle_day` set (day of month Zapier's usage resets, from the Zapier billing page): count calls
  since the last reset, and in the last `bonus_days` days spend whatever is left on bonus Shorts,
  so no tasks are wasted.
"""
import datetime as dt
import json
import math
import os

from .spec import ROOT, load_style

LEDGER = os.path.join(ROOT, "channel", "zapier_ledger.json")
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
DEFAULTS = {"plan_tasks": 100, "tasks_per_call": 2, "reserve_tasks": 4, "window_days": 31,
            "keep_for_review": 3, "cycle_day": None, "bonus_days": 7, "max_per_day": 3,
            "trial_until": None, "trial_tasks": 1000}
NEED = {"upload": 1, "stats": 1, "docs": 1, "other": 1}


def settings(style=None):
    s = dict(DEFAULTS)
    s.update((style or load_style()).get("zapier", {}))
    return s


def load(path=LEDGER):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save(entries, path=LEDGER):
    with open(path, "w") as f:
        json.dump(entries, f, indent=1)
        f.write("\n")


def _now():
    return dt.datetime.now(dt.timezone.utc)


def _on_day(y, m, day):
    """The cycle day in month (y, m), clamped to the month's length (a 31st in February -> the 28th/29th)."""
    import calendar
    return dt.date(y, m, min(day, calendar.monthrange(y, m)[1]))


def cycle(day, today):
    """(start, next_reset) dates of the billing cycle containing `today`."""
    start = _on_day(today.year, today.month, day)
    if start > today:
        py, pm = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
        start = _on_day(py, pm, day)
    ny, nm = (start.year, start.month + 1) if start.month < 12 else (start.year + 1, 1)
    return start, _on_day(ny, nm, day)


def status(now=None, path=LEDGER, style=None):
    s = settings(style)
    now = now or _now()
    today = now.astimezone(IST).date()
    trial_end = dt.date.fromisoformat(s["trial_until"]) if s.get("trial_until") else None
    if trial_end and today < trial_end:
        # trial: big allowance until the trial ends; treat the end as the reset
        s = {**s, "plan_tasks": s["trial_tasks"], "cycle_day": "trial"}
        since = dt.datetime.combine(trial_end - dt.timedelta(days=15), dt.time(), IST)
        reset, days_left = trial_end, (trial_end - today).days
    elif s["cycle_day"]:
        start, reset = cycle(int(s["cycle_day"]), today)
        # a day's margin either side of midnight: Zapier may reset on UTC or account time
        since = dt.datetime.combine(start - dt.timedelta(days=1), dt.time(), IST)
        days_left = (reset - today).days            # days until reset, today included
    else:
        since, reset, days_left = now - dt.timedelta(days=s["window_days"]), None, None
    if trial_end and today >= trial_end:     # trial calls never count against the free plan
        since = max(since, dt.datetime.combine(trial_end, dt.time(), IST))
    used = [e for e in load(path) if dt.datetime.fromisoformat(e["ts"]) > since]
    cap = (s["plan_tasks"] - s["reserve_tasks"]) // s["tasks_per_call"]
    if days_left == 1:
        # last day of the cycle: spend the safety margin too. If the ledger was off, the call that
        # goes over simply fails, and failed calls cost nothing.
        cap = s["plan_tasks"] // s["tasks_per_call"]
    reviews_left = None
    if days_left is not None:
        reviewed_today = any(e["kind"] == "stats" and dt.datetime.fromisoformat(e["ts"]).astimezone(IST).date() == today
                             for e in used)
        reviews_left = sum(1 for k in range(days_left) if (today + dt.timedelta(days=k)).weekday() == 6
                           and not (k == 0 and reviewed_today))
    todays = [e for e in used if e["kind"] == "upload"
              and dt.datetime.fromisoformat(e["ts"]).astimezone(IST).date() == today]
    today_uploads = len(todays)
    regular_done = any(e.get("ref", "").endswith("-a") for e in todays)   # slot a = the daily regular Short
    return {"calls_used": len(used), "tasks_used": len(used) * s["tasks_per_call"], "cap_calls": cap,
            "calls_left": cap - len(used), "plan_calls": s["plan_tasks"] // s["tasks_per_call"], "plan_tasks": s["plan_tasks"], "keep_for_review": s["keep_for_review"],
            "window_days": s["window_days"], "cycle_day": s["cycle_day"], "reset": reset, "days_left": days_left,
            "today": today, "today_uploads": today_uploads, "regular_done": regular_done, "reviews_left": reviews_left, "bonus_days": s["bonus_days"],
            "max_per_day": s["max_per_day"]}


def allowed(kind, st):
    need = NEED.get(kind, 1)
    if kind == "upload":   # leave room for the weekly review's calls (in cycle mode: only if one is still due)
        review_due = st["reviews_left"] is None or st["reviews_left"] > 0
        need += st["keep_for_review"] if review_due else 0
    return st["calls_left"] >= need


def bonus_today(st):
    """How many extra Shorts to post today from tasks that would otherwise expire at the reset.

    Plans against the whole plan (safety margin included, since it is released on the last day) and
    starts early enough that the spare fits under max_per_day: never fewer than `bonus_days` days."""
    if not st["cycle_day"] or st["days_left"] is None:
        return 0
    d = st["days_left"]
    # still owed before the reset: today's regular slot (if not posted yet), the regular slot on the
    # other remaining days, and a weekly review on any remaining Sunday
    owed_today = 0 if st["regular_done"] else 1
    regular = owed_today + (d - 1)
    total_left = st["plan_calls"] - st["calls_used"]
    spare = total_left - regular - st["reviews_left"] * st["keep_for_review"]
    extra_per_day = st["max_per_day"] - 1
    if spare <= 0 or d > max(st["bonus_days"], math.ceil(spare / max(1, extra_per_day))):
        return 0
    per_day = math.ceil(spare / d)                   # spread the spare over the days left
    room = st["max_per_day"] - st["today_uploads"] - owed_today    # the daily cap includes the regular Short
    safe = st["calls_left"] - regular - st["reviews_left"] * st["keep_for_review"]
    return max(0, min(per_day, room, spare, safe if d > 1 else spare))


def record(kind, ref="", n=1, path=LEDGER):
    entries = load(path)
    ts = _now().isoformat(timespec="seconds")
    entries += [{"ts": ts, "kind": kind, "ref": ref} for _ in range(n)]
    cutoff = _now() - dt.timedelta(days=90)          # keep the file small
    entries = [e for e in entries if dt.datetime.fromisoformat(e["ts"]) > cutoff]
    save(entries, path)
    return entries


def sync(tasks_used, path=LEDGER, style=None):
    """Match the ledger to the 'tasks used' figure on Zapier's billing page (adds 'other' calls for
    anything spent outside this channel, e.g. other Zaps). Never removes entries."""
    st = status(path=path, style=style)
    s = settings(style)
    missing = math.ceil(tasks_used / s["tasks_per_call"]) - st["calls_used"]
    if missing > 0:
        record("other", "sync", missing, path)
    return max(0, missing)
