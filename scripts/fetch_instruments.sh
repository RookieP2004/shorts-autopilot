#!/bin/sh
# The real-instrument sample packs for the score (CC0: VSCO 2 CE, VCSL, FreePats, Karoryfer; CC BY 3.0: the Salamander grand
# piano, credited automatically in descriptions) and two Poly Haven CC0 HDRIs for Blender light. ~1.4 GB, ~20 s on a fast link.
# Uses the vendored Lemo-Opuscar fetch tool (MIT), from that library's GitHub release. Safe to run twice (skips what is there).
set -e
cd "$(dirname "$0")/../third_party/lemo"
for lib in vsco2ce vcsl freepats karoryfer salamander; do
  if [ -d "core/audio/instruments/$lib" ]; then echo "✓ $lib"; continue; fi
  n=0; until sh tools/fetch.sh instruments "$lib" >/dev/null 2>&1; do      # resumes after a dropped connection
    n=$((n + 1)); [ $n -ge 4 ] && { echo "✗ $lib: download failed; the music falls back to the synth"; exit 0; }
  done
  echo "✓ $lib"
done
[ -d core/assets/polyhaven ] && echo "✓ hdri" || { sh tools/fetch.sh hdri >/dev/null 2>&1 && echo "✓ hdri" || echo "✗ hdri (Blender falls back to flat world light)"; }
