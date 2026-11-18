# motion/ — Remotion + GSAP + three.js clips for The Explainer

Owner request (2026-11-18): learn the Remotion, GSAP and three.js skills and use them in our own pipeline, mixed with the
house style. This folder is a small Remotion project; `autopilot/remotion.py` renders a composition to a transparent PNG
sequence and the Python compositor plays it as a `motion` layer inside a scene (with Ved, plates, captions, cards...).

Skill packs studied (fetch them again with `git clone --depth 1 https://github.com/<repo>` when you need the full docs):
`remotion-dev/skills`, `greensock/gsap-skills` (MIT), `cloudAI-X/threejs-skills` (MIT). Remotion is free for individuals and
companies of up to 3 people (remotion.dev/license); the channel is a one-person project.

## Rules we follow (learned from those skills)
- **Everything is a function of the frame.** Remotion renders frames in parallel tabs, so nothing may animate on its own:
  no CSS transitions/animations, no `useFrame()` in three.js, no GSAP ticker. GSAP timelines are built once, paused, and
  seeked to `frame / fps` on every render (`src/gsapClock.ts`).
- Seconds-to-frames always via `fps` from `useVideoConfig()`; `interpolate()` with clamps; `spring()` for physical pops;
  `Easing.bezier()` for custom curves; animate `scale` / `translate` / `rotate`, not layout.
- GSAP: `back.out` for pops, `power2.inOut` for draws, `stagger` for letters and lists; all plugins are free
  (DrawSVG for self-drawing lines, MotionPath for pulses along arrows, SplitText-style per-letter reveals).
- three.js: wrap in `<ThreeCanvas>` with width/height; real lighting (environment map from `RoomEnvironment` + key and rim
  lights); physical materials (clearcoat, metalness/roughness); step the camera back to fit narrow portrait frames;
  transparent background so the clip sits on our plates.
- Fonts are our own (`public/fonts` -> repo `fonts/`), loaded with `delayRender` before any frame is captured.

## Compositions (props in brackets; size/fps/length come from the layer)
- `KineticTitle` — house title text (white + dark stroke, yellow accent) that rises / pops / waves in letter by letter, the
  accent word gets a hand-drawn underline. [lines, size, color, accent, stroke, font, style: rise|pop|wave, sub, y, out]
- `FlowDiagram` — house cream cards pop in one by one, curved arrows draw themselves, a pulse travels along each.
  [nodes: [{id, label, x, y, color, w}], edges: [[a, b]], step, theme: cream|night]
- `Hero3D` — real-time 3D: `coin` (gold, spins), `bars` (3D bar chart that springs up), `globe` (dot globe, no map outline,
  gold arcs that draw between lat/lon points). [object, values, colors, arcs, tone, spin, zoom]

## Render by hand
`node render.mjs KineticTitle props.json out_dir` (props include w, h, fps, dur). Needs Chrome (`/usr/bin/google-chrome`
or `REMOTION_CHROME`); WebGL runs in software (`gl: swangle`): ~0.1 s a frame for 2D, ~0.3 s for 3D at 1080x1920.
First use in a fresh checkout: `npm ci` (autopilot/remotion.py does it automatically).
