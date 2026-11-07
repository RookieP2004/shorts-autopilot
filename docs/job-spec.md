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
least 2 frames so it never flickers. He also nods on stressed words and sways slightly while talking.
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

### type: image
`svg` (inline SVG string, preferred: draw props yourself) or `path` (repo file), `w` (0–1 of width).

Colours anywhere: a palette name from style.json (`primary`, `accent`, `accent2`, `danger`, `ink`, `bg1`, `bg2`) or `#hex`.

## Rules the validator enforces
Known types/enters/loops/shapes/transitions/sfx; characters and poses exist; `y` ≤ safe-zone bottom (0.78);
total length ≤ `max_duration` (58 s).
