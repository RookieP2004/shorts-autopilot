"""Zapier task budget.

Every successful Zapier MCP call costs `tasks_per_call` tasks (2). The free plan has 100 tasks a
month. We keep a ledger of successful calls in channel/zapier_ledger.json (committed to the repo,
so every fresh scheduled run sees it) and count calls in a rolling window that is at least as long
as any billing cycle (31 days). Staying under the cap in every rolling window means every Zapier
billing cycle stays under it too, whatever day the cycle resets.

Failed calls cost 0 tasks, so only record a call after it succeeded.
"""
import datetime as dt
import json
import os

from .spec import ROOT, load_style

LEDGER = os.path.join(ROOT, "channel", "zapier_ledger.json")
DEFAULTS = {"plan_tasks": 100, "tasks_per_call": 2, "reserve_tasks": 4, "window_days": 31,
            "keep_for_review": 1}
# calls each kind of run needs; an upload must leave `keep_for_review` calls for the weekly review
NEED = {"upload": 1, "stats": 1, "other": 1}


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


def status(now=None, path=LEDGER, style=None):
    s = settings(style)
    now = now or _now()
    since = now - dt.timedelta(days=s["window_days"])
    used = [e for e in load(path) if dt.datetime.fromisoformat(e["ts"]) > since]
    cap = (s["plan_tasks"] - s["reserve_tasks"]) // s["tasks_per_call"]
    return {"calls_used": len(used), "tasks_used": len(used) * s["tasks_per_call"], "cap_calls": cap,
            "calls_left": cap - len(used), "window_days": s["window_days"],
            "plan_tasks": s["plan_tasks"], "keep_for_review": s["keep_for_review"]}


def allowed(kind, st):
    need = NEED.get(kind, 1)
    if kind == "upload":
        need += st["keep_for_review"]
    return st["calls_left"] >= need


def record(kind, ref="", n=1, path=LEDGER):
    entries = load(path)
    ts = _now().isoformat(timespec="seconds")
    entries += [{"ts": ts, "kind": kind, "ref": ref} for _ in range(n)]
    cutoff = _now() - dt.timedelta(days=90)          # keep the file small
    entries = [e for e in entries if dt.datetime.fromisoformat(e["ts"]) > cutoff]
    save(entries, path)
    return entries
