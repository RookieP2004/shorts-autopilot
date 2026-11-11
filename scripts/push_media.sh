#!/usr/bin/env bash
# Publish a rendered video to the repo's public `media` branch and print its download URL
# (Zapier's YouTube "Upload Video" fetches the file from that URL).
#   usage: scripts/push_media.sh <file.mp4|.jpg> <name>      e.g. jobs/2026-11-07-a/out/final.mp4 2026-11-07-a
#   BRANCH=media-long KEEP=6 for long videos and their thumbnails (own branch, so a Short's push never removes them)
# The branch is rewritten as a single commit holding only the newest $KEEP videos,
# so the repo never grows. The repo must be PUBLIC for Zapier to download the file.
set -euo pipefail
src=$(realpath "$1"); name="$2"; keep=${KEEP:-6}; branch=${BRANCH:-media}; ext="${src##*.}"
cd "$(dirname "$0")/.."
remote=$(git remote get-url origin)
slug=${REPO_SLUG:-$(echo "$remote" | sed -E 's#\.git$##' | awk -F'[/:]' '{print $(NF-1)"/"$NF}')}
tmp=$(mktemp -d)
if git clone -q --depth 1 --branch "$branch" "$remote" "$tmp" 2>/dev/null; then :; else
  git init -q -b "$branch" "$tmp"; git -C "$tmp" remote add origin "$remote"; fi
cp "$src" "$tmp/$name.$ext"
cd "$tmp"
{ ls -t -- *.mp4 *.jpg 2>/dev/null || true; } | tail -n +$((keep + 1)) | xargs -r rm -f --
git checkout -q --orphan fresh
git add -A
git -c user.name=shorts-autopilot -c user.email=noreply@anthropic.com commit -q -m "media: latest $keep files"
git push -q -f origin "fresh:$branch"
url="https://raw.githubusercontent.com/$slug/$branch/$name.$ext"
# wait until the public URL serves the file
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -I -w "%{http_code}" "$url" || true)
  [ "$code" = "200" ] && break; sleep 6
done
echo "$url"
[ "$code" = "200" ] || { echo "WARNING: URL not reachable yet (HTTP $code). Is the repo public?" >&2; exit 2; }
