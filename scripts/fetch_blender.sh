#!/usr/bin/env bash
# Install Blender as a Python module (bpy) for the 3D shots.
# Fast path: the repo's `deps` branch holds the wheel in <100 MB parts (GitHub downloads are quick here).
# Slow path: PyPI (about 400 MB; can take 20+ minutes on a slow link).
set -euo pipefail
python3 -c "import bpy" 2>/dev/null && { echo "bpy already installed"; exit 0; }
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
URL="$(git -C "$ROOT" remote get-url origin 2>/dev/null || echo https://github.com/RookieP2004/shorts-autopilot)"
TMP="$(mktemp -d)"
if git clone -q --depth 1 --branch deps --single-branch "$URL" "$TMP/deps"; then
  WHL="$(ls "$TMP/deps" | grep '\.part00$' | sed 's/\.part00$//')"
  cat "$TMP/deps/$WHL".part* > "$TMP/$WHL"
  (cd "$TMP" && sha256sum -c deps/SHA256SUMS >/dev/null) || { echo "checksum mismatch"; exit 1; }
  pip install -q --break-system-packages "$TMP/$WHL"
else
  echo "deps branch not reachable, installing from PyPI (slow)"
  pip install -q --break-system-packages bpy==5.2.3
fi
rm -rf "$TMP"
python3 -c "import bpy; print('bpy', bpy.app.version_string)"
