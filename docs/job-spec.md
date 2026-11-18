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

## Long videos (Deep Dives, 16:9)
Set `"kind": "long"`. The channel style then merges `longform` from style.json: 1920x1080 canvas, `max_duration` 720 s,
`target_mb` 90 (the final encode is sized to fit, for Zapier and GitHub), no burned captions, no progress bar,
small watermark bottom-right, no `#shorts`, and the documentary toolkit (next section). Everything else (layers, stage, beats, motion) works the same; x/y/w are still fractions
of the frame, so a layer `w` of 0.4 is 768 px wide here.
- `chapters`: `[{"scene": 0, "title": "A piece of paper"}, ...]`, at least 3, first at scene 0, each >= 10 s long.
  `python -m autopilot zapier` adds them to the description as `0:00 Title` lines (from out/render.json).
- `thumbnail` (the bold explainer look; see the Bible): `{"title": "JUST *PAPER?*", "title_y": 0.14, "title_size": 220,
  "bg": [layers: a plate + townspeople + props, all blurred], "fg": [layers: Ved big (h ~1.7, y ~1.2, x ~0.43, a strong pose
  such as "surprised", `acting: "none"`, `talk: false`) + 1-2 key props], "blur": 16, "tint": ["#2a5bd7", "#f08a24"],
  "tint_amount": 0.45, "glow": "#f2b04a", "glow_x": 0.45, "glow_y": 0.58, "glow_strength": 1.6, "bg_saturation": 1.8}`.
  `python -m autopilot thumbnail jobs/<id>/job.json` writes out/thumbnail.jpg (1280x720, < 2 MB); Read it and iterate.
  Shorts use the same spec: the output is 1080x1920 (the canvas is vertical); put Ved at about `h` 0.95, `y` 0.93, `x` 0.5 and
  use a clean plate (no text, no Ved) as `bg`. YouTube accepts it through *Update Video Thumbnail* (tested 2026-11-13).
  (Old form, still supported: `{"at": seconds, "text": ...}` = one caption-free video frame with the title on top.)
- Sets: render plates at 1920x1080 (`still(name, 1920, 1080, ...)`); landscape shows more of the world, so dress the sides.
- Talking to camera: Ved big on one side (x 0.27 or 0.73, y 0.86, h 1.2, `ground: false`) over the blurred set, with a
  headline or panel on the other side. Beat cards: pass `text_w` 0.4 so they stay on one side.
- Publish: `BRANCH=media-long KEEP=6 scripts/push_media.sh <file> <name>` for both the video and the thumbnail
  (its own branch, so the daily Shorts' pushes never remove it).
- Reference: `jobs/2026-11-14-L/assets.py` + `build_doc.py` (documentary cut); the 3D sets and people as in
  `jobs/2026-11-11-longpilot/build_job.py`.

## Documentary toolkit (long videos; `doc` in the long-form profile, autopilot/doc.py)
Owner's rule (2026-11-15): long videos look like a hand-made documentary, not a long Short. The profile turns on a vignette (no film grain: at YouTube bitrates it
compresses into blocky "mosaic"; set a scene's `grain` only if you must), a slow organic camera float on every shot (`doc.drift`) and an automatic slow push or pull on scenes without a
`camera`; burned captions are off; the default transition is a cut; music is the `doc` underscore. Reference build:
`jobs/2026-11-14-L/build_doc.py` (helpers `dtxt`, `hand`, `lower`, `source`, `card_paper`, `sticky`, `mark`, `chapter_card`).
- Type: `"font": "serif"` / `"serif_i"` (Libre Baskerville), `"cond"` (Oswald caps), `"hand"` (Caveat), `"marker"`,
  `"type"` (typewriter). Use `enter: "rise"`, a thin dark `stroke` (3 px) over busy plates, no Anton headlines, no pop-ins.
- Scene keys: `look: "archival"` (sepia film with scratches, flicker and gate weave, labelled RECONSTRUCTION; for history),
  `letterbox: 0.11` (+ `letterbox_in` seconds), `leak: [start, dur, strength]` (warm light leak), `jcut: 0.3` (voice starts
  before the cut), transitions `whip` | `paper` (torn-paper wipe, into boards) | `dip` (through black) | `burn` (film splice flash).
- Layer keys (any layer): `pan: [dx, dy, dscale]` drift over the layer's life (move foreground more than background =
  parallax); `blur_keys: [[t, px], ...]` rack focus on image layers; entrances `rise` and `slam` (a card dropped on a board).
- `paper` layers: `kind` "photo" (`path`, `tone` sepia/bw, handwritten `caption`), "doc" (typed `title` + `text`), "clip"
  (newspaper: `masthead`, `title`, grey column lines), "note" (`title` in marker + `text` in handwriting, `lined`,
  `paper` colour, e.g. "#f6e27f" sticky); `tape` corners, `stamp` ("1911"), `w`, `rotate`.
- Drawn overlays: `marker` (`shape` circle | underline | arrow | box | cross | check | scribble | highlight, `box`
  [x0, y0, x1, y1] or `from`/`to`, `color`, draws itself on and boils at 12 fps), `string` (red string, `points`),
  `timeline` (`x0`, `x1`, `y`, `events` [{pos, year, label}], `active`), `lower_third` (`title`, `sub`), `chapter`
  (`num`, `title`; a chapter title card over a blurred, dimmed shot), `tag` (small typewriter label: sources, VISUALISATION).
- Sound: foley `paper`, `tape`, `marker`, `shutter`, `type`, `thud`, `hit` (chapter cards), `swoosh_soft`, `projector`.
  `music.cues: [{"scene": i, "style": "doc" | "tension" | "wonder" | "none", "key": ..., "scale": ...}]` scores the film in
  sections that crossfade (use "none" for one held silence on the big reveal).

## Night set (second mood, `"look": "night"`; autopilot/night.py, devices.py, blendkit night helpers)
Opt-in per job for dark-files, scams, money traps and big reveals; the bright town stays the default. Owner-approved
2026-11-16 (reference video: `jobs/2026-11-16-n`). Use it for at most the videos that fit; most Shorts stay in the town.
**The layers below are for every Short, town look included** (owner, 2026-11-16); only the night lighting, character rim light
and highlight captions come with `"look": "night"`. In daylight the `crowd` draws contact shadows and outlined figures
(`"shadow": 0..0.4`); place it on an empty patch of the plate's floor (check corners with `Stage(plate).point(x, y)`).
`"look": "night"` merges `style.looks.night`: highlight captions, push transitions, a night grade (deeper blacks, vignette) and a
rim light on every `character` layer (`"rim": false` turns it off on one layer, `"rim": [left, right]` recolours it).

**Sets** (in the job's `assets_script`): `night_set(target, rim, spot_power, grid, back_wall=png)` = navy dark, one hard spot from
above, coloured rim lights, glossy floor + faint grid; `camera(..., fstop=2.0)` then `dutch(cam, 4..6)` for hero shots. Props:
`phone(...)` + `phone_sprite(name, screen)` (saves the screen quad), `coin(...)`, `banknote(devices.note_texture(...))` (fictional,
"NOT REAL MONEY"), `crowd(area, n, color_of=, glow_of=)` for a hero still of thousands of figures. Reference: `jobs/2026-11-16-n/assets.py`.

**Layers** (frame fractions; times inside a layer are seconds after its `at`):
| type | what | keys |
|---|---|---|
| hud | number chip: dark card, glowing border, small-caps label, big number that ticks | `label`, `value` / `to`+`count_dur` / `steps: [[t, v]]` / `text`, `prefix`, `suffix`, `indian` (default true: 9,99,800), `tone`, `sub`, `size`, `width_of` |
| eqbar | running equation under a hud | `keys: [[t, "8,000 \u00f7 2^3 = *1,000*"]]` (`^x` superscript, `*x*` answer colour), `tone` |
| tracker | step circles that tick green one by one | `n`, `done: [t1, t2, ...]`, `size` |
| stamp | slanted rubber-stamp verdict that slams in | `text`, `tone`, `angle`, `size` (add `"sfx": "thud"`) |
| optcard | option card that gets a red cross or green tick | `label`, `text` (\n for 2 lines), `sub`, `tone`, `w`, `verdict: cross/tick`, `verdict_at` |
| phone | glossy 3D phone with a LIVE fictional screen; turns in 3D | `sprite` (phone_sprite png), `screen` (devices spec: lock / chat / tips / pay; elements pop in at `at`), `w`, `tilt: [[t, yaw, pitch]]`, `ui_w` |
| crowd | thousands of tiny figures on a plate's floor doing the maths | `plate` (.json), `area: [x0, x1, y0, y1]` m, `n` (<= 9000), `steps: [{at, split: x/y, colors}, {at, keep: i, lost}, {at, glow}]`, `aisle: [x, half_w]` (a lane for Ved), `in_dur` |
| nodes | decision tree / flow as glowing nodes floating in 3D, built step by step, slowly orbiting | `nodes: [{id, pos: [x, y, z], at, tone, label}]`, `edges: [[a, b, at, tone]]`, `yaw: [d0, d1]`, `x`, `y` |
| burst | cash / coin burst with motion blur | `sprites: [png]`, `sizes`, `n`, `origin`, `dur`, `spread` |
Colours by meaning (`tone`): green = survives/true, red = scam/danger, gold = money, blue = neutral data (+ violet, white, grey).
Crowd maths: each `split` divides the still-standing figures into equal groups by position; `keep` keeps one group (the rest
turn red, then fade grey), so 8,000 -> split/keep x3 -> 1,000 exactly. Ved walks through the crowd along the `aisle`.
Scam payoff: a `phone` with `{"kind": "lock", "notes": [...], "cta": "Comment YES or NO", "cta_at": 1.2}`.
Pilot / reference build: `jobs/2026-11-16-n/build_job.py`. Tests: `python -m pytest -q tests`.

## Case-file pieces (autopilot/dossier.py, devices.doc_texture, blendkit noir_desk; DEMO 2026-11-18, awaiting owner OK)
Mix into any look (town or night); best in the weekly documentary and Dark Files. Reference build: `jobs/2026-11-18-dossier`.
**Set**: `noir_desk(target)` = dark slate desk + wall, warm venetian-blind stripes (`blinds(...)`: a hard spot behind a row of
slats), navy fill. Props: `sim_card()`, `doc_sheet(devices.doc_texture("slips"|"ledger"|"statement"|"form"))`, `envelope()`,
`cloche()`, `phone(screen_image=...)` (lie it screen-up: rot (-90, 0, z)). Masked numbers only, no real bank, logo or person.
| type | what | keys |
|---|---|---|
| dottext | dot-matrix label that decodes (scramble, then locks left to right) or types in | `text` (`*x*` accent, `\n`), `size`, `tone`, `accent`, `anim: decode/type/none`, `cps`, `align`, `plate: true` (dark pill: use on bright sets) |
| bignum | big serif number (lining figures) that counts, with a dot caption | `value`/`to`/`steps`/`text`, `prefix`, `suffix`, `indian`, `label`, `tone: cream/gold`, `size`, `label_side: below/right` |
| dateline | date (types) + place (serif caps rises) stamp | `date`, `place`, `size` |
| tipnum | numbered takeaway: serif numeral + decoding title + small sub | `n`, `title`, `sub` |
| tiles | day / step tiles lying in perspective, filling gold | `n`, `progress: [[t, k]]`, `labels`, `unit`, `end`, `pitch`, `yaw`, `w` |
| clock | thin analog clock, hands sweep to a time, label | `time: "HH:MM"`, `from`, `dur`, `label`, `r` |
| blinds | (world) warm stripe light over the frame, drifting; put it after the plate and characters | `angle`, `count`, `strength`, `shade`, `color`, `drift`, `phase` |
| flows | (world) gold arcs between city dots, travelling pulses | `points: {name: [x, y]}`, `routes: [[a, b, t]]`, `tone`; never draw a country outline (map rules), label dots "illustrative" when positions are approximate |

## Motion clips (`motion` layer: Remotion + GSAP + three.js; autopilot/remotion.py, motion/)
A `motion` layer plays a clip rendered with Remotion in headless Chrome (cached, transparent PNG frames), inside the scene
like any layer: `{"type": "motion", "comp": "KineticTitle"|"FlowDiagram"|"Hero3D", "props": {...}, "x", "y", "w", "h", "at",
"dur"}` (w/h = frame fractions; the clip is rendered at that size; `res` < 1 renders smaller). Props per composition and the
rules (everything frame-driven, GSAP timelines seeked, no useFrame) are in `motion/README.md`. Use it where motion design
beats a still: a kinetic hook title, a cause-and-effect flow of cream cards with self-drawing arrows, a real-time 3D object
(coin, bars, dot globe with arcs). Mix with the house pieces; it never replaces Ved, captions, cards or plates.
Reference demo: `jobs/2026-11-18-motion`.

## Rules the validator enforces
Known types/enters/loops/shapes/transitions/sfx; characters and poses exist; `y` ≤ safe-zone bottom (0.78);
total length ≤ `max_duration` (58 s).
