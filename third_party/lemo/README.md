# Lemo-Opuscar audio engine (vendored)

From [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), MIT licence (`LICENSE-MIT.txt`).
Only the MIT code is copied here, unchanged: `core/audio/sampler.py`, `core/audio/sfx.py`,
`tools/fetch.sh`, `tools/assets.json`. Their guides (CC BY-NC) are not copied; our own rules are in
`docs/job-spec.md` ("Score") and `skill/SKILL.md`.

The sample packs are not in git. Fetch the two we use (both CC0, ~670 MB unpacked):

    cd third_party/lemo && sh tools/fetch.sh instruments vsco2ce && sh tools/fetch.sh instruments vcsl

`autopilot/orchestra.py` uses only VSCO 2 CE and VCSL (CC0), so the channel's music needs no attribution;
`CREDITS` still names them. When the packs are missing, the music falls back to the old synth.
