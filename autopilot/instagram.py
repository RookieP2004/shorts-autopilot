"""Post a finished Short to Instagram as a Reel (Instagram Graph API, system-user token).

Needs env IG_TOKEN (never-expiring system-user token of the "Explainer Poster" Meta app) and
IG_USER_ID (17841428825494803 = @explainerthe_). The token is a secret: it lives only in the
scheduled tasks' prompts, never in this (public) repo. Uses no Zapier tasks.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from .spec import load_json

API = "https://graph.facebook.com/v27.0"
RAW = "https://raw.githubusercontent.com/RookieP2004/shorts-autopilot"
GENERIC = {"explained", "education", "science story", "facts", "shorts", "learning", "science explained"}
MAX_TAGS = 5  # Instagram's hard limit per Reel since Dec 2025; more than 5 can block the post


def _call(method, path, **params):
    params["access_token"] = os.environ["IG_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"Instagram API error {e.code} on {path}: {body}")


def _tag(t):
    t = "".join(ch for ch in t.lower() if ch.isalnum())
    return "#" + t if t else ""


def hashtags(job):
    """5 hashtags for this video: job["instagram"]["hashtags"] if the run researched them, else derived from the job.
    Mix: 1 broad niche tag, 3 topic-specific tags, then #explained (the channel's own)."""
    own = (job.get("instagram") or {}).get("hashtags")
    if own:
        tags = [_tag(t) for t in own]
    else:
        broad = [_tag(t) for t in (job.get("hashtags") or []) if _tag(t) not in ("#shorts", "")][:1]
        topic = [_tag(t) for t in (job.get("tags") or []) if t.lower() not in GENERIC and len(_tag(t)) <= 25][:3]
        tags = broad + topic + ["#explained"]
    out = []
    for t in tags:
        if t and t not in out and t != "#shorts":
            out.append(t)
    return out[:MAX_TAGS]


def caption(job):
    title = job.get("title", "").strip()
    desc = (job.get("description") or "").split("\n\nSources:")[0].strip()
    text = (f"{title}\n\n{desc}\n\nFollow for a new \"wait, what?\" explainer every day 🧠\n"
            f"Longer videos on YouTube: The Explainer\n\n{' '.join(hashtags(job))}")
    return text[:2200]


def recent_reels(since_epoch):
    """Reels on the account published at or after since_epoch (the owner posting by hand counts)."""
    import datetime as dt
    ig = os.environ.get("IG_USER_ID", "17841428825494803")
    got = _call("GET", f"{ig}/media", fields="id,caption,timestamp,media_product_type,permalink", limit="10")
    out = []
    for m in got.get("data", []):
        ts = dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z").timestamp()
        if ts >= since_epoch - 60 and m.get("media_product_type") == "REELS":
            out.append(m)
    return out


def manual_window(job_path, video_url=None, cover_url=None, minutes=30, since=None, poll_s=120):
    """Give the owner `minutes` to post the Reel by hand (with Meta AI translation on). If a new Reel shows up on the
    account in that time, stop: prints MANUAL <link>. Otherwise post it automatically: prints AUTO <link>."""
    since = since or time.time()
    end = since + minutes * 60
    while time.time() < end:
        found = recent_reels(since)
        if found:
            print("MANUAL", found[0].get("permalink", found[0]["id"]), flush=True)
            return "MANUAL", found[0].get("permalink")
        print(f"waiting: {int((end - time.time()) / 60)} min left", flush=True)
        time.sleep(min(poll_s, max(1, end - time.time())))
    found = recent_reels(since)
    if found:
        print("MANUAL", found[0].get("permalink", found[0]["id"]), flush=True)
        return "MANUAL", found[0].get("permalink")
    link = post_reel(job_path, video_url, cover_url)
    print("AUTO", link, flush=True)
    return "AUTO", link


def post_reel(job_path, video_url=None, cover_url=None, wait_s=300):
    job = load_json(job_path)
    jid = job["id"]
    video_url = video_url or f"{RAW}/media/{jid}.mp4"
    ig = os.environ.get("IG_USER_ID", "17841428825494803")
    params = dict(media_type="REELS", video_url=video_url, share_to_feed="true", caption=caption(job))
    if cover_url:
        params["cover_url"] = cover_url
    cid = _call("POST", f"{ig}/media", **params)["id"]
    t0 = time.time()
    while True:
        st = _call("GET", cid, fields="status_code,status")
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") in ("ERROR", "EXPIRED") or time.time() - t0 > wait_s:
            raise SystemExit(f"Reel container {cid} not ready: {st}")
        time.sleep(15)
    mid = _call("POST", f"{ig}/media_publish", creation_id=cid)["id"]
    info = _call("GET", mid, fields="permalink")
    return info.get("permalink", mid)
