# job.json reference

One file per video at `jobs/<id>/job.json`. `<id>` = `YYYY-MM-DD-a` (a = first slot, b = second).
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
Mouth uses `<pose>_talk.svg` while this character speaks; blinks with `<pose>_blink.svg` / `blink.svg`.

### type: text
`text` (`*word*` highlighted), `size` px, `font` (`display` `body` `light` from style.json),
`color`, `highlight`, `stroke`, `stroke_width`, `max_w` (0–1), `align`, `uppercase`, `shadow`.

### type: counter
`to`, `from`, `count_dur`, `decimals`, `prefix`, `suffix`, `size`, `color`.

### type: shape
`shape`: `circle` `ring` `rect` `arrow` (points right; use `rotate`) `line` `burst`;
`w`, `h` (0–1 of width), `color`, `stroke_width`, `radius`, `outline`.

### type: image
`svg` (inline SVG string, preferred: draw props yourself) or `path` (repo file), `w` (0–1 of width).

Colours anywhere: a palette name from style.json (`primary`, `accent`, `accent2`, `danger`, `ink`, `bg1`, `bg2`) or `#hex`.

## Rules the validator enforces
Known types/enters/loops/shapes/transitions/sfx; characters and poses exist; `y` ≤ safe-zone bottom (0.78);
total length ≤ `max_duration` (58 s).
