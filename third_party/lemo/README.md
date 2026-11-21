# Lemo-Opuscar audio engine (vendored)

From [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), MIT licence (`LICENSE-MIT.txt`).
Only the MIT code is copied here, unchanged: `core/audio/sampler.py`, `core/audio/sfx.py`, `core/audio/pluck.py`
(physically modelled strings, needs numba),
`tools/fetch.sh`, `tools/assets.json`. Their guides (CC BY-NC) are not copied; our own rules are in
`docs/job-spec.md` ("Score") and `skill/SKILL.md`.

The sample packs and HDRIs are not in git: `sh scripts/fetch_instruments.sh` fetches VSCO 2 CE, VCSL, FreePats,
Karoryfer (CC0), the Salamander grand piano (CC BY 3.0, credited automatically) and two Poly Haven HDRIs (CC0).

`autopilot/orchestra.py` records which libraries a render used; CC BY ones (the piano) go into the description. When the packs are missing, the music falls back to the old synth.
