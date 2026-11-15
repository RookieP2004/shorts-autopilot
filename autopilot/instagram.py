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
EXTRA_TAGS = ["#explained", "#didyouknow", "#sciencefacts", "#learnsomethingnew", "#reels"]


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


def caption(job):
    title = job.get("title", "").strip()
    desc = (job.get("description") or "").split("\n\nSources:")[0].strip()
    tags = []
    for t in list(job.get("hashtags") or []) + EXTRA_TAGS:
        t = t if t.startswith("#") else "#" + t
        if t.lower() not in [x.lower() for x in tags] and t.lower() != "#shorts":
            tags.append(t)
    text = (f"{title}\n\n{desc}\n\nFollow for a new \"wait, what?\" explainer every day 🧠\n"
            f"Longer videos on YouTube: The Explainer\n\n{' '.join(tags[:10])}")
    return text[:2200]


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
