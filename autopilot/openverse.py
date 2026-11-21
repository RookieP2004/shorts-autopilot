"""Openverse: openly licensed real recordings and photos (owner, 2026-11-21).

Openverse (api.openverse.org, run by WordPress; platform code MIT) indexes CC-licensed audio (Freesound, Wikimedia,
Jamendo, ccMixter...) and images. We take only what we may use on a monetised channel without strings:
  - sound effects: CC0 or Public Domain Mark only (no attribution needed; we still log the creator and link)
  - photos: CC0 / PDM by default; CC BY allowed only with `allow_by=True`, and then the credit line is added to the video
    description automatically (job meta.credits). Never NC (non-commercial) or ND (no derivatives).
Anonymous access works with rate limits. The workspace must be allowed to reach: api.openverse.org and the file hosts
(cdn.freesound.org, upload.wikimedia.org, ...). Without them every call raises OpenverseBlocked with that message.
"""
import json
import os
import subprocess
import urllib.parse
import urllib.request

API = "https://api.openverse.org/v1"
OK_AUDIO = "cc0,pdm"
OK_IMAGE = "cc0,pdm"
UA = "TheExplainer-autopilot/1.0 (+https://github.com/RookieP2004/shorts-autopilot)"


class OpenverseBlocked(RuntimeError):
    pass


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:                                  # proxy refusal shows up as a URLError / 403
        raise OpenverseBlocked(f"cannot reach {urllib.parse.urlparse(url).netloc}: {e}. Allow api.openverse.org and the file "
                               f"hosts (cdn.freesound.org, upload.wikimedia.org) for this workspace.") from e


def search_audio(q, max_s=6.0, n=12, licence=OK_AUDIO, category="sound_effect", fetch=None):
    """Short openly licensed sound effects for a query, best first. fetch = injectable getter (tests)."""
    params = {"q": q, "license": licence, "page_size": n, "category": category, "mature": "false"}
    raw = (fetch or _get)(f"{API}/audio/?{urllib.parse.urlencode(params)}")
    out = []
    for r in json.loads(raw).get("results", []):
        dur = (r.get("duration") or 0) / 1000.0
        if dur and dur > max_s:
            continue
        if r.get("license", "").lower() not in licence.split(","):
            continue
        out.append({"id": r["id"], "title": r.get("title"), "url": r.get("url"), "creator": r.get("creator"),
                    "license": r.get("license"), "license_version": r.get("license_version"),
                    "landing": r.get("foreign_landing_url"), "source": r.get("source") or r.get("provider"),
                    "duration": dur, "filetype": r.get("filetype")})
    return out


def search_images(q, n=12, allow_by=False, fetch=None, aspect=None):
    lic = OK_IMAGE + (",by" if allow_by else "")
    params = {"q": q, "license": lic, "page_size": n, "mature": "false"}
    if aspect:
        params["aspect_ratio"] = aspect                        # tall | wide | square
    raw = (fetch or _get)(f"{API}/images/?{urllib.parse.urlencode(params)}")
    out = []
    for r in json.loads(raw).get("results", []):
        if r.get("license", "").lower() not in lic.split(","):
            continue
        out.append({"id": r["id"], "title": r.get("title"), "url": r.get("url"), "creator": r.get("creator"),
                    "license": r.get("license"), "license_version": r.get("license_version"),
                    "landing": r.get("foreign_landing_url"), "source": r.get("source") or r.get("provider"),
                    "w": r.get("width"), "h": r.get("height"), "credit": credit_line(r)})
    return out


def credit_line(r):
    lic = (r.get("license") or "").upper()
    ver = r.get("license_version") or ""
    if lic in ("CC0", "PDM"):
        return None
    return f"\"{r.get('title') or 'Untitled'}\" by {r.get('creator') or 'unknown'} ({r.get('source')}), CC {lic} {ver}: {r.get('foreign_landing_url')}"


def download(item, dst, max_s=None, lufs=None, fetch=None):
    """Download a result; audio is trimmed and loudness-normalised to a 48 kHz mono FLAC (or kept as is for images)."""
    data = (fetch or _get)(item["url"], timeout=60)
    tmp = dst + ".src"
    with open(tmp, "wb") as f:
        f.write(data)
    if dst.endswith(".flac"):
        af = []
        if max_s:
            af.append(f"afade=t=out:st={max(0.0, max_s - 0.08)}:d=0.08")
        if lufs:
            af.append(f"loudnorm=I={lufs}:TP=-1.5:LRA=11")
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-ac", "1", "-ar", "48000"]
        if max_s:
            cmd += ["-t", str(max_s)]
        if af:
            cmd += ["-af", ",".join(af)]
        subprocess.run(cmd + [dst], check=True)
        os.remove(tmp)
    else:
        os.replace(tmp, dst)
    return dst
