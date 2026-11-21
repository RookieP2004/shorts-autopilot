#!/bin/sh
# Fetch (or update) the Lemo-Opuscar style library into /tmp/lemo for reading only, and print the styles that suit
# The Explainer. Their STYLE.md files are CC BY-NC: read them to learn a technique, never copy their text, demo code,
# films or designs into ours (skill/SKILL.md, "Style donors").
set -e
D=${LEMO_DIR:-/tmp/lemo}
if [ -d "$D/.git" ]; then git -C "$D" pull -q --ff-only || true; else git clone -q --depth 1 https://github.com/lemomo-ai/lemo-opuscar.git "$D"; fi
echo "library: $D ($(ls "$D/styles" | grep -vc '^_\|README') styles)"
echo "donors that fit the channel (read $D/styles/<slug>/STYLE.md, sections on native moves, transitions and sound):"
for s in dark-documentary halftone-dossier visual-investigation news-package map-explainer satellite-briefing \
         briefing-board telestrator text-flash-cuts countdown kino-montage spy-titles archive-lighttable newsreel \
         iso-infographic data-physical dataviz pictogram-motion stick-explainer whiteboard sketchnote game-show; do
  [ -f "$D/styles/$s/STYLE.md" ] && printf '  %-22s %s\n' "$s" "$(sed -n 's/^# //p' "$D/styles/$s/STYLE.md" | head -1 | cut -c1-70)"
done
