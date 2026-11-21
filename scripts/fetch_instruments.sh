#!/bin/sh
# The real-instrument sample packs for the score (CC0: VSCO 2 CE, VCSL, FreePats; ~1.1 GB unpacked, ~10 s on a fast link).
# Uses the vendored Lemo-Opuscar fetch tool (MIT), from that library's GitHub release. Safe to run twice (skips what is there).
set -e
cd "$(dirname "$0")/../third_party/lemo"
for lib in vsco2ce vcsl freepats; do
  if [ -d "core/audio/instruments/$lib" ]; then echo "✓ $lib"; continue; fi
  n=0; until sh tools/fetch.sh instruments "$lib" >/dev/null 2>&1; do      # resumes after a dropped connection
    n=$((n + 1)); [ $n -ge 4 ] && { echo "✗ $lib: download failed; the music falls back to the synth"; exit 0; }
  done
  echo "✓ $lib"
done
