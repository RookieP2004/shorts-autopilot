"""YouTube: one-time auth, upload, and channel stats (Data API v3 + Analytics API v2)."""
import datetime as dt
import json
import os
import time

from .spec import ROOT, load_json, load_style

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]


def creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    miss = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if miss:
        raise SystemExit(f"missing env/secrets: {', '.join(miss)}")
    c = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                    client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"],
                    token_uri="https://oauth2.googleapis.com/token", scopes=SCOPES)
    c.refresh(Request())
    return c


def service(name="youtube", version="v3"):
    from googleapiclient.discovery import build
    return build(name, version, credentials=creds(), cache_discovery=False)


def auth(client_secret_file):
    """Run on your own computer once. Prints the three GitHub secrets."""
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    c = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    print("\nAdd these as GitHub repo secrets (Settings > Secrets and variables > Actions):\n")
    print(f"YT_CLIENT_ID={c.client_id}")
    print(f"YT_CLIENT_SECRET={c.client_secret}")
    print(f"YT_REFRESH_TOKEN={c.refresh_token}")
    print("\nor with the GitHub CLI:")
    print(f"  gh secret set YT_CLIENT_ID --body '{c.client_id}'")
    print(f"  gh secret set YT_CLIENT_SECRET --body '{c.client_secret}'")
    print(f"  gh secret set YT_REFRESH_TOKEN --body '{c.refresh_token}'")


def build_body(job, style):
    yt = {**style.get("youtube", {}), **job.get("youtube", {})}
    desc = job.get("description", "").strip()
    tags = [t.lstrip("#") for t in job.get("tags", [])][:30]
    hashtags = yt.get("hashtags", []) + [h for h in job.get("hashtags", []) if h not in yt.get("hashtags", [])]
    if hashtags:
        desc = (desc + "\n\n" + " ".join(hashtags)).strip()
    snippet = {"title": job["title"][:100], "description": desc[:4900], "tags": tags,
               "categoryId": str(yt.get("categoryId", "24"))}
    if yt.get("default_language"):
        snippet["defaultLanguage"] = yt["default_language"]
        snippet["defaultAudioLanguage"] = yt["default_language"]
    status = {"privacyStatus": job.get("privacy", yt.get("privacy", "public")),
              "selfDeclaredMadeForKids": bool(yt.get("made_for_kids", False)),
              "containsSyntheticMedia": bool(yt.get("synthetic_media", False))}
    if job.get("publish_at"):  # RFC3339, needs privacy private
        status["privacyStatus"] = "private"
        status["publishAt"] = job["publish_at"]
    return {"snippet": snippet, "status": status}


def upload(job_path, video_path, root=ROOT, log=print):
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    job = load_json(job_path)
    style = load_style(root)
    body = build_body(job, style)
    yt = service()
    media = MediaFileUpload(video_path, mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp, tries = None, 0
    while resp is None:
        try:
            st, resp = req.next_chunk()
            if st:
                log(f"  uploaded {int(st.progress()*100)}%")
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and tries < 6:
                tries += 1
                time.sleep(2 ** tries)
                continue
            raise
    vid = resp["id"]
    log(f"uploaded: https://youtube.com/shorts/{vid}")
    time.sleep(5)
    got = yt.videos().list(part="status", id=vid).execute().get("items", [{}])
    actual = got[0].get("status", {}).get("privacyStatus") if got else None
    wanted = body["status"]["privacyStatus"]
    result = {"youtube_id": vid, "url": f"https://youtube.com/shorts/{vid}",
              "posted_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "privacy_requested": wanted, "privacy_actual": actual,
              "locked_private": wanted == "public" and actual == "private"}
    if result["locked_private"]:
        log("WARNING: YouTube kept this video private. The Google Cloud project has not passed the "
            "YouTube API compliance audit yet, so API uploads stay private.")
    job_dir = os.path.dirname(os.path.abspath(job_path))
    with open(os.path.join(job_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    meta = job.get("meta", {})
    rinfo = {}
    rp = os.path.join(job_dir, "out", "render.json")
    if os.path.exists(rp):
        rinfo = load_json(rp)
    line = {"id": job["id"], "title": job["title"], **result,
            "format": meta.get("format"), "topic": meta.get("topic"), "hook": meta.get("hook"),
            "idea_source": meta.get("idea_source"), "characters": meta.get("characters"),
            "duration": rinfo.get("duration")}
    os.makedirs(os.path.join(root, "data"), exist_ok=True)
    with open(os.path.join(root, "data", "videos.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return result


def _chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def stats(root=ROOT, log=print):
    yt = service()
    ya = service("youtubeAnalytics", "v2")
    ch = yt.channels().list(part="contentDetails,statistics,snippet", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while len(ids) < 500:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50,
                                    pageToken=tok).execute()
        ids += [it["contentDetails"]["videoId"] for it in r.get("items", [])]
        tok = r.get("nextPageToken")
        if not tok:
            break
    vids = {}
    for part in _chunks(ids, 50):
        r = yt.videos().list(part="snippet,statistics,contentDetails,status", id=",".join(part)).execute()
        for v in r.get("items", []):
            s = v.get("statistics", {})
            vids[v["id"]] = {"youtube_id": v["id"], "title": v["snippet"]["title"],
                             "published": v["snippet"]["publishedAt"],
                             "privacy": v["status"]["privacyStatus"],
                             "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                             "comments": int(s.get("commentCount", 0)),
                             "duration": v["contentDetails"]["duration"]}
    today = dt.date.today()
    start = (today - dt.timedelta(days=365)).isoformat()
    try:
        rep = ya.reports().query(ids="channel==MINE", startDate=start, endDate=today.isoformat(),
                                 metrics="views,estimatedMinutesWatched,averageViewDuration,"
                                         "averageViewPercentage,likes,shares,subscribersGained",
                                 dimensions="video", sort="-views", maxResults=200).execute()
        cols = [c["name"] for c in rep.get("columnHeaders", [])]
        for row in rep.get("rows", []):
            d = dict(zip(cols, row))
            v = vids.setdefault(d["video"], {"youtube_id": d["video"]})
            v.update({"a_views": d.get("views"), "avg_view_sec": d.get("averageViewDuration"),
                      "avg_view_pct": d.get("averageViewPercentage"), "shares": d.get("shares"),
                      "subs_gained": d.get("subscribersGained"),
                      "watch_min": d.get("estimatedMinutesWatched")})
    except Exception as e:  # analytics lags ~2 days and needs some data first
        log(f"analytics not available yet: {e}")
    # join with our own log: format / topic / hook per video
    logp = os.path.join(root, "data", "videos.jsonl")
    if os.path.exists(logp):
        for ln in open(logp, encoding="utf-8"):
            if ln.strip():
                L = json.loads(ln)
                v = vids.get(L.get("youtube_id"))
                if v:
                    for k in ("id", "format", "topic", "hook", "idea_source", "characters"):
                        v[k] = L.get(k)
    out = {"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "channel": {"title": ch["snippet"]["title"], **{k: int(v) for k, v in ch["statistics"].items()
                                                           if v.isdigit()}},
           "videos": sorted(vids.values(), key=lambda v: v.get("published", ""), reverse=True)}
    d = os.path.join(root, "data", "stats")
    os.makedirs(d, exist_ok=True)
    for name in ("latest.json", f"{today.isoformat()}.json"):
        with open(os.path.join(d, name), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
    log(f"stats: {len(vids)} videos, {out['channel'].get('subscriberCount', '?')} subscribers")
    return out
