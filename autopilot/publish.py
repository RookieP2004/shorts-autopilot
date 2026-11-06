"""Metadata for Zapier's YouTube "Upload Video" action and the Google Docs log line."""
import datetime as dt
import json
import os

from .spec import load_json

CATEGORY_NAMES = {"1": "Film & Animation", "10": "Music", "15": "Pets & Animals", "17": "Sports",
                  "19": "Travel & Events", "20": "Gaming", "22": "People & Blogs", "23": "Comedy",
                  "24": "Entertainment", "25": "News & Politics", "26": "Howto & Style",
                  "27": "Education", "28": "Science & Technology"}


def zapier_fields(job, style):
    yt = {**style.get("youtube", {}), **job.get("youtube", {})}
    desc = job.get("description", "").strip()
    tags = [t.lstrip("#") for t in job.get("tags", [])][:30]
    hashtags = list(yt.get("hashtags", []))
    hashtags += [h for h in job.get("hashtags", []) if h not in hashtags]
    if hashtags:
        desc = (desc + "\n\n" + " ".join(hashtags)).strip()
    cat = str(yt.get("categoryId", "24"))
    f = {"title": job["title"][:100], "description": desc[:4900], "tags": ",".join(tags),
         "privacy_status": job.get("privacy", yt.get("privacy", "public")),
         "category": f"{cat} ({CATEGORY_NAMES.get(cat, '?')})",
         "made_for_kids": bool(yt.get("made_for_kids", False)),
         "notify_subscribers": True,
         "default_language": yt.get("default_language", "en"),
         "contains_synthetic_media": bool(yt.get("synthetic_media", False))}
    if job.get("publish_at"):
        f["privacy_status"] = "private"
        f["publish_at"] = job["publish_at"]
    return f


def log_line(job_path, youtube_id=""):
    """One row for the 'Shorts log' Google Doc table (pipe-separated)."""
    job = load_json(job_path)
    m = job.get("meta", {})
    rp = os.path.join(os.path.dirname(os.path.abspath(job_path)), "out", "render.json")
    dur = load_json(rp).get("duration") if os.path.exists(rp) else ""
    url = f"https://youtube.com/shorts/{youtube_id}" if youtube_id else ""
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M IST")
    cells = [job["id"], now, job["title"], m.get("format", ""), m.get("hook", ""), m.get("topic", ""),
             f"{dur}s" if dur else "", url, youtube_id]
    if m.get("overrides"):
        cells.append("one-off: " + m["overrides"])
    return " | ".join(str(c).replace("|", "/") for c in cells)
