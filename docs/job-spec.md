# job.json reference

One file per video at `jobs/<id>/job.json`. `<id>` = `YYYY-MM-DD-a` (the daily slot; `-b`, `-c` only if more slots are added on a paid plan; manual runs use `-m1`, `-m2`).
Render it with `python -m autopilot render`, then publish with `scripts/push_media.sh` + Zapier.

```jsonc
{
  "id": "2026-11-07-a",
  "title": "≤100 chars (aim ≤60)",
  "description": "1–2 sentences + source line",
  "tags": ["5-10 plain tags"],
  "hashtags": ["#niche1", "#niche2"],          // #shorts is added from style.json
  "meta": {                                      // used by the weekly review, keep it honest
    "format": "fact-drop",                       // a format name from the bible
    "topic": "octopus hearts",
    "hook": "number-shock",                      // a hook type from the bible
    "idea_source": "trend: <url> | backlog | insight 2026-11-03",
    "characters": ["host"],
    "sources": ["https://..."]
  },
  "privacy": "public",                           // optional; default from style.json
  "publish_at": "2026-11-07T13:30:00Z",          // optional scheduled publish (forces private until then)
  "speaker": "host",                             // default speaker for scenes
  "music": {"style": "lofi"},                    // optional per-video override (avoid: consistency)
  "style_override": {"captions": {"y": 0.38}},   // ONE-OFF changes for this video only (deep-merged over style.json)
                                                 // also record them in meta.overrides (plain words) for the log
  "scenes": [ /* see below */ ]
}
```

## Scene
| key | meaning |
|-----|---------|
| `say` | narration (TTS). `*word*` = highlighted in captions/text. Scene length follows the speech. |
| `caption` | optional different caption text (default = `say`) |
| `speaker` | character id whose voice + mouth is used |
| `voice` | `{voice, speed, lang}` override (rare) |
| `dur` / `min_dur` | seconds, for silent scenes or to hold longer |
| `pad`, `lead` | silence after / before the line (defaults 0.28 / 0.12) |
| `transition` | into this scene: `cut` `fade` `slide_left` `slide_up` `zoom` `flash` |
| `sfx` | at scene start: `pop` `whoosh` `ding` `click` `boom` `riser` `none` (slide/zoom transitions add a whoosh by default) |
| `bg` | override background `{type: gradient|radial|solid, colors:[...], angle, pattern: dots|grid|rays|none}` |
| `camera` | `{zoom:[from,to], punch:[t,...], shake:[t,dur], focus:[x,y]}` |
| `captions` | `false` to hide captions for this scene |
| `caption_y` | move captions for this scene (0–1) |
| `layers` | list, drawn in order (later = on top) |

## Layer (all types)
`x`, `y` (0–1, centre), `scale`, `rotate` (deg), `opacity`, `flip`,
`at` (s from scene start), `until` (s; then `exit`: fade|pop), 
`enter`: `none` `pop` `fade` `zoom` `slide_up` `slide_down` `slide_left` `slide_right` `drop` `typewriter` (text),
`enter_dur`, `loop`: `none` `bob` `float` `pulse` `shake` `spin` `wiggle`, `loop_speed`, `loop_amp`,
`sfx` (plays at `at`).

### type: character
`id`, `pose` (an SVG in `characters/<id>/`), `h` (height, 0–1 of frame), `talk` (default true).
Lip-sync is automatic: while this character speaks, each frame picks one of 5 mouth shapes from the voice audio
(loudness = how open, brightness = round "oo" vs wide "ee"): `<pose>_m1`, `_talk`, `_m3`, `_oo`, `_ee`, held for at
least 2 frames so it never flickers. He changes gesture at natural pauses (see Acting); no nodding or swaying.
Blinks use `<pose>_blink.svg`. Base poses: idle, warm, serious, explain, point, think, welcome, surprised, crossed.

**Acting** (rigged characters like Ved are drawn fresh every frame): `pose` is the starting gesture, then
- `"acting": "auto"` (default): while he speaks he changes gesture at natural pauses every ~1.6–2.8 s,
  moving smoothly (0.4 s) between poses. Between changes he stands still. No wobble.
- `"acting": "none"`: hold one pose.
- `"acting": [["explain", 0], ["point", 1.4], ["crossed", 3.2]]`: exact gestures at scene times (use this when a
  gesture must land on a specific word, e.g. point when the visual appears).
Never put `loop` animations (bob, float, wiggle, shake) on characters; that reads as shaking. Loops are for props and text.

### type: text
`text` (`*word*` highlighted), `size` px, `font` (`display` `body` `light` from style.json),
`color`, `highlight`, `stroke`, `stroke_width`, `max_w` (0–1), `align`, `uppercase`, `shadow`.

### type: counter
`to`, `from`, `count_dur`, `decimals`, `prefix`, `suffix`, `size`, `color`.

### type: shape
`shape`: `circle` `ring` `rect` `arrow` (points right; use `rotate`) `line` `burst`;
`w`, `h` (0–1 of width), `color`, `stroke_width`, `radius`, `outline`.

### type: scene3d  (simple 3D, drawn in code)
Usually a full-frame backdrop or a cutaway: `x` 0.5, `y` 0.5, `w` 1, `h` 1 (fractions of the frame).
`sky`: 2–3 colours top→bottom (omit for transparent), `fog`: `{color, near, far, max}` (distance fades to it),
`camera`: `{pos:[x,y,z], target:[x,y,z], fov, orbit: deg/s, dolly:[from,to], move:{to, target_to, dur}}`,
`objects`: list of `{shape, pos, rot, scale, color, ...}`:
- `person` faceless mannequin: `color` (clothes), `legs`, `skin`, `walk` (steps/s), `travel` (m/s forward),
  `action`: `idle` `wave` `point` `cheer`, `height`, `phase` (desync crowds)
- `building` (`w`,`d`,`h`,`roof`,`windows`), `tree` (`seed`), `terrain` (`w`,`d`,`n`,`height`,`seed`,`flat_center`),
  `plane` (`w`,`d`), `box` (`size`), `sphere` (`r`), `cylinder`/`cone` (`r`,`h`)
- animation on any object: `spin:[dx,dy,dz]` deg/s, `bob`, `move:{to, dur, at}`
Units are metres; y is up; a person is 1.75 tall. Light comes from the upper-left like the 2D sets.

## The 3D world, cheaply: stills + cut-outs (default)
Build each video's world the Rick's Clips way: render **stills** in Blender once, then animate everything in 2D at 30 fps.
- Job field `"assets_script": "jobs/<id>/assets.py"`: a blendkit script run once (cached) before any frame is drawn. It calls
  `reset(...)`, builds a set, and `still("plate_market_mid", 1080, 1920, 32)` for a background plate (2-3 camera angles of the
  same set = wide / medium / close-up), and `still("apple", 500, 500, 24, transparent=True, crop=True)` for a prop cut-out
  (use `sprite_camera(center, dist, height, lens)` to frame it at roughly the plate's camera height). Output: `jobs/<id>/assets/*.png`.
  `BK_SKIP_EXISTING=1` re-renders only the files you deleted. A full set of 5 plates + 8 cut-outs takes about 6-9 min.
  See `jobs/2026-11-08-m2/assets.py` (bright island market with a stall and palms, a bank hall, a spotlit vault).
- Use them as `image` layers with `"path": "jobs/<id>/assets/<name>.png"` (`w` = width as a fraction of the frame, `blur` px for
  out-of-focus backgrounds behind close-ups). Props then fall, fly, bounce, spin and flip in 2D (see "Motion").
- Full animated Blender shots (`blender` layers) are expensive (about 7 s per frame); use them only for a moment that really needs
  a moving 3D camera.

## The town: supporting cast and depth staging
**Townspeople** (`"id": "extra"`): faceless figures in the channel's flat style. Each layer brings its own outfit:
`"rig_args": {"outfit": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "bag": "#8a5a3c", ...}}`
(full list in `characters/extra/make.py`: builds, hair, hats, tops, bottoms, apron, tie, necklace, earrings, belt). Feelings are body
language: gestures `idle happy cheer sad give take hold shrug point explain wave surprised` via `acting`; they walk and hop like Ved.
Give the recurring people names and fixed outfits in the job builder, and keep them identical in every shot (continuity).

**Depth staging** (`autopilot/stage.py`): every plate saves its camera (`plate_<set>.json`), so characters are placed by floor
position in metres and come out the right size: `Stage(...).place(wx, wy, "extra"|"ved")` -> x, y, h; `.walk([(t, wx, wy), ...], base)`
-> keys that shrink/grow with distance; `.point(x, y, z)` -> where a 3D point is on screen (for props, printers, counters).
A foreground layer (`still("fg_<set>", only=[counter objects])`) is drawn after the people behind the counter and before the
people in front, so a seller really stands behind his stall. Order: plate, people behind (far to near), fg, people in front
(far to near), then props/text. Reference: `jobs/2026-11-08-m3/assets.py` + `build_job.py`.

## Motion (any layer)
`"keys": [{"t": 0, "x": 1.18}, {"t": 1.15, "x": 0.62, "walk": true}, ...]`: keyframes in seconds from the layer's `at`.
Animatable: `x`, `y`, `scale`, `rot` (deg), `opacity`, `sx` (horizontal scale; 1 -> 0 then a second layer 0 -> 1 = a card flip).
`"ease"` on the arriving key: `in_out` (default), `linear`, `in`, `out`, `back`, `bounce` (lands and bounces: dropped props).
Recipes in `jobs/2026-11-08-m2/build_job.py`: `drop()` (falls into place with a bounce), `fly()` (arcs out of a printer and spins).

**Characters act inside the world:** `"walk": true` on a key makes the character walk to it (legs step, body bobs, arms swing),
`"hops": [[t, height, dur]]` makes them jump (legs tuck; the shadow stays on the floor), and a soft floor shadow follows them
whenever they move (`"ground": false` to turn it off, e.g. in close-ups). Combine with `acting` for gestures and faces.
Shot grammar: a **wide** (Ved small in the set), **medium** (Ved h ≈ 0.42 on the floor line next to the props) and **close-up**
(Ved h ≈ 1.06, x 0.5, y 0.8, `allow_outside_safe`, background plate blurred and scaled 1.35, captions at `caption_y` 0.64).
Cut between them every 3-5 s.

**Camera moves:** scene `"camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3, "zoom": 1.1, "focus": [0.54, 0.5]}]}`.
Text layers are part of the scene, so keep `focus` y ≈ 0.5 when zooming or headlines near the top get cropped.

### type: blender  (animated 3D shot, expensive)
The main explainer visual. `script`: a shot file (path from the repo root, usually `jobs/<id>/shots/<name>.py`),
`x` 0.5, `y` 0.5, `w` 1, `h` 1, `fps` (15 is the default budget; motion blur hides the steps), `res` (0.4 = 432x768 rendered,
upscaled), `samples` (10), `dur` (defaults to the rest of the scene; use 0.034 for a single still frame, e.g. a blurred background
behind Ved). Shots are rendered before any frame is drawn and cached (`out/shots/`), so re-renders after text edits are fast.
Budget: about 7 s per rendered frame on 2 CPU cores, so 25 s of 3D at 15 fps ≈ 45 min. Keep 3D to 2-4 shots per video.

A shot script (see `jobs/2026-11-08-m1/shots/` for examples) gets `DUR`, `FPS`, `W`, `H`, `SAMPLES` and every helper in
`autopilot/blendkit.py`:
```python
reset(W, H, FPS, DUR, samples=SAMPLES, bloom=0.2)      # empty Cycles scene, AgX colour, motion blur
world_color(hexrgb("#0d161c")); floor("#16232b")      # dark studio with a curved cyclorama floor
studio(target=(0, 0, 0.3))                            # warm key, cool rim, soft fill
a = apple((0, 0, 0.2), r=0.15); pop_in(a, 0.4)        # props: apple, banknote(image), printer(), price_tag(front, back)
box/sphere/cylinder/torus/cone/plane/text3d(...)      # primitives (bevelled, smooth) + materials:
plastic/clay/metal/glass/glow/organic/paper(image)    #   organic = wet, translucent (organs, cells, fruit)
cam, tgt = camera((0, -4, 2.5), (0, 0, 0.3), lens=42, fstop=3.2)   # tracks `tgt`; depth of field on it
key(cam, 0, loc=(...)); key(cam, DUR, loc=(...))      # keyframes in seconds; key(obj, t, rot=(deg...), scale=..)
```
Preview single frames before the full render: `BK_FRAMES=1,90 python -m autopilot.blendrun <script> /tmp/pv <dur> 30 432 768 10`,
then Read the PNGs. Vertical frames are narrow: keep wide objects small and centred. Textures (banknotes, tags, labels) are drawn
with PIL in `assets/tex/make_textures.py`; all designs fictional. Install Blender with `bash scripts/fetch_blender.sh`.

### type: image
`svg` (inline SVG string, preferred: draw props yourself) or `path` (repo file), `w` (0–1 of width).

Colours anywhere: a palette name from style.json (`primary`, `accent`, `accent2`, `danger`, `ink`, `bg1`, `bg2`) or `#hex`.

## Beats (the comedy moment)
One short, unexpected funny beat per video, tied to a trend that is current this week. Put it on the scene where it lands:

```json
"beat": {"kind": "deadpan", "at": "after_say", "text": "the air when blue light shows up:", "sfx": "none"}
```

| kind | what happens | default dur / sfx / music |
|---|---|---|
| `deadpan` | Ved crosses his arms and stares flat at camera; camera pushes in on his face | 1.3 s, none, music cuts |
| `side_eye` | Ved slides his eyes sideways, half-lidded; push-in | 1.1 s, none, music cuts |
| `smirk` | one brow up, half smile; small push-in | 0.9 s, none, music keeps |
| `freeze` | freeze-frame, colour drains (the "you're probably wondering how I got here" move) | 1.4 s, `scratch`, music cuts |
| `zoom_punch` | hard snap zoom on the face or `focus` | 0.5 s, `boom`, music keeps |
| `silence` | awkward pause, nothing moves | 1.4 s, `crickets`, music cuts |

- `at`: `"after_say"` (default, right after this scene's line; the scene stretches to fit) or seconds into the scene.
  Never put a beat over speech.
- `text`: optional meme-caption card (cream card, ink text, tilted −3°), ≤ 60 characters, `*word*` for the accent colour.
  Position with `text_y` (default 0.24), `text_x`, `tilt`.
- `sfx`: override (`scratch`, `crickets`, `wah`, `boom`, `ding`, `pop`, `none`). `music`: `"cut"` or `"keep"`.
  `zoom`, `focus` [x, y], `who` (character id) and `dur` override the defaults.
- `"beats": [...]` takes a list, but one beat per video is the rule (two only in a video over 40 s).

## Rules the validator enforces
Known types/enters/loops/shapes/transitions/sfx; characters and poses exist; `y` ≤ safe-zone bottom (0.78);
total length ≤ `max_duration` (58 s).
