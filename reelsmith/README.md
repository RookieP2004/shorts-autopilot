# Reelsmith

The Explainer's code-film engine. A **look** is a small web page that can draw any moment `t` of an animated piece; the
engine captures it frame by frame in headless Chrome (transparent PNGs) and the compositor plays it as a `look` layer
inside a scene, next to Ved, plates, captions and the rest of the house style. Looks are deterministic (same props +
same t = same picture), so any frame renders alone, in any order, on any worker.

| No. | Look | For | Placement |
|---|---|---|---|
| RS-01 | Receipt | Monthly costs, bills, "where it all goes", hidden fees. | overlay (paper on any set) |
| RS-02 | Dot Map | Routes, supply chains, where money or goods travel. | full frame |
| RS-03 | Balance | A vs B: interest vs inflation, cost vs benefit, which is bigger. | overlay; use backdrop: dim on bright sets |
| RS-04 | Flipboard | Hook numbers, prices then vs now, countdowns to a reveal. | overlay; backdrop: dim on bright sets |
| RS-05 | Blueprint | How a thing works, what's inside, parts of a system. | full frame |
| RS-06 | Bubbles | Shares, budgets, who has how much. | overlay; backdrop: dim on bright sets |
| RS-07 | Chalk | Formulas, rules of thumb, step-by-step maths. | full frame |
| RS-08 | Sweep | Investigations, hidden networks, "spot the pattern" (dark-files). | full frame |
| RS-09 | Word Beat | 2-4 s hooks, chapter punches. | full frame |
| RS-11 | Riso | One big number or rule as a self-printing three-ink poster (Lemo riso engine) | full frame |
| RS-12 | Terminal | Logs, leaks, audits on a CRT (Lemo CRT post) | full frame |
| RS-13 | Whiteboard | Processes and chains, drawn in marker (Lemo whiteboard engine) | full frame |
| RS-14 | Silent Card | 1920s intertitle on scratched film (Lemo silent-film engine) | full frame |
| RS-15 | Ink Brush | One weighty word in a brushed circle (Lemo ink-wash engine) | full frame |
| RS-10 | Bite | Tax, fees, middlemen, "what you actually keep". | overlay; backdrop: dim on bright sets |

Use in a job: `{"type": "look", "look": "RS-03" | "balance" | "RS-03-balance", "props": {...}, "x", "y", "w", "h", "at", "dur"}`.
`props.backdrop: "dim"` lays a night scrim behind light-on-dark looks over bright sets; `props.fit: false` stops a look
from speeding up to fit a short slot (by default it lands by 85% of the slot and holds).

## Writing a new look
`looks/RS-NN-name/look.js` exports default `{ dur, setup(A), draw(t, A), texts?(t, A), cues?(A) }`. `A` has `ctx`
(2D canvas), `W`, `H`, `S` (scale vs a 1080-wide Short), `P` (props), `kit` (kit/core.js: easing, seeded random,
monotone keys, rrect, wrap, fitText, inkLine, grain, roll, box) and the house fonts by name (display, body, semi, serif,
hand, marker, cond, bebas, mono, type, dot, anton...). Rules: draw from `t` only (no Date, no unseeded random, no state
carried between frames); report every readable text in `texts(t)` (`pass: true` for labels not meant to be read in
full); give every visible action a cue with a name from our sound library. Add `LOOK.md`, then check it:

    node engine/stills.mjs RS-NN-name /tmp/st --props '{...}'            # review stills (portrait; --size 1920x1080 too)
    node engine/frames.mjs RS-NN-name job.json out/ && node engine/textcheck.mjs out/

## Lemo-Opuscar engines
`vendor/lemo/` holds Lemo-Opuscar style engines we build looks on, unchanged and credited (MIT): `riso.js` (risograph
print, RS-11), `crt.js` (CRT post, RS-12), `whiteboard/wb.js` (marker strokes, RS-13), `silent-film/` (film post,
damage, intertitles, RS-14), `ink-wash-ink.js` (brush strokes, RS-15) and `core/lib.js` (their helpers). Where a file was
changed, its header says how (only import paths). `engine/lemo.mjs` renders any Lemo style's own demo page from a library
clone (`scripts/lemo_bank.py` prepares and checks all of them) so an engine can be studied before it becomes a look.

## Credits
`engine/serve.mjs`, `engine/open.mjs`, the timing rule in `engine/textcheck.mjs` and the first block of `kit/core.js`
are adapted from Lemo-Opuscar (MIT; see `NOTICE`). The looks, their guides and the host are our own work.
