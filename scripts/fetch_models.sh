#!/usr/bin/env bash
# Downloads the open-source Kokoro voice model (Apache-2.0) into models/ if missing.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p models
base=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  if [ ! -s "models/$f" ]; then
    echo "downloading $f"
    curl -fsSL --retry 3 -o "models/$f.part" "$base/$f"
    mv "models/$f.part" "models/$f"
  fi
done
ls -la models
