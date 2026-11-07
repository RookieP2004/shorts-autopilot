# The Explainer - Channel Bible

Only the owner (Sujal) changes sections marked 🔒. The weekly review may tune sections marked 🔄 and logs every change in §12.
The repo copy (`channel/memory/bible.md`) is the working copy; the Google Doc "The Explainer - Channel Bible" is synced from it
every week, and edits the owner makes in the Google Doc are pulled back in by the weekly review.

## 1. Identity 🔒
- Channel: **The Explainer** · @the_explainer-n3d · YouTube Shorts (Instagram Reels later)
- Niche: **complex ideas made simple.** Economics and money, philosophy, quantum physics and big science, the human body and
  medicine, society and psychology, famous experiments, and political-economic systems (capitalism, communism, how governments
  and markets work), plus surprising facts. Topics people find hard, explained so anyone gets them in under a minute.
- Promise: "The complicated stuff, made simple, in under a minute."
- Audience: curious people 16-34, English-speaking worldwide, strong India share.
- Language: English (Professor Ved speaks with a British voice).
- Style: fully original and cinematic. Clean 3D shots rendered in Blender (soft studio light, depth of field, gentle camera moves,
  like Zack D Films) carry the explanation, with bold infographic text and diagrams on top (like The Infographics Show), and
  Professor Ved as the 2D host. Every idea is turned into a concrete picture or analogy (10 apples and 10 dollars = inflation).

## 2. Tone 🔒
- Three words: wise, cool, dry-witted.
- Ved talks like a smart friend who happens to know everything: short sentences, no jargon without a picture, never preachy.
- One quick, current, on-topic joke per video (§11). Never a clown, never "boomer" humour.
- Never: clickbait that isn't true, fear-mongering, punching down, personal medical or financial advice, partisan politics
  (no parties, candidates or current elections), or mocking religion.
- Political and economic ideas (capitalism, communism, socialism, taxes...) are explained even-handedly: what the idea is, how it
  is meant to work, the strongest case for it and the strongest criticism, with historical facts. Ved never takes a side.
- Medical topics explain how the body works; they never tell a viewer what to take or do. Philosophy presents the idea, not a verdict.
- **Callbacks:** refer to an earlier video only when it is genuinely needed to understand this one (e.g. a follow-up on the same
  idea), never as filler or promotion. Check the log; if there's no strong link, don't mention past videos.

## 3. Look 🔒
- Palette, fonts, background and captions live in `channel/style.json`. Characters are flat vector, no outlines,
  two-tone shading; sets keep lines; warm key light from the upper left, cool shadows, teal/amber grade.
- Layout: visuals and headline y 0.10-0.34, captions y≈0.41, Ved y≈0.68 with h≈0.40, nothing important below y 0.78 or right of x 0.86.
- Sets: `study.svg` (home), `world.svg` (nature, history outdoors), `cosmos.svg` (space, physics).
- **Cinematic 3D (main explainer visuals):** Blender shots (`blender` layers, `autopilot/blendkit.py`): dark studio cyclorama,
  warm key + cool rim light, glossy/clay/metal/paper materials, shallow depth of field, slow dolly/orbit, things popping in,
  flying and flipping. Real objects stand in for abstract ideas (apples for goods, banknotes for money). 2-4 shots per video,
  full-screen with Ved as voice-over. Big bold infographic text on top (y 0.10-0.30). Avoid childish clip-art diagrams.
- Simple low-poly 3D (`scene3d`) only for quick crowds or maps.
- References: `docs/sheets/professor_ved_character_sheet.png`, `vast_world_style_guide.png`, `vast_world_3d_guide.png`.
- **Visual-first: Ved hosts, the pictures explain.** Ved is on screen for the hook, the payoff and the comic beat. The middle of
  every video is full-screen cinematic 3D shots (Blender) with bold infographic text, counters and simple labelled graphics on top,
  with Ved as voice-over or, at most, small in a corner.
  Ved full-size for no more than about 40% of the runtime; every explanation step gets its own visual; something new moves on
  screen at least every 2-3 seconds; never a talking head explaining something we could show.

## 4. Cast 🔒
| id | name | role | personality | voice | poses |
|---|---|---|---|---|---|
| ved | Professor Ved | host and explainer | about 25, sharp, calm, quietly funny; white shirt, top button open, sleeves rolled | Kokoro bm_george, speed 0.95, en-gb | idle, warm, serious, explain, point, think, welcome, surprised, crossed + reaction faces deadpan, side_eye, smirk |

Rule: characters are made only by `characters/<id>/make.py`. Colours, proportions and voice never change.

## 5. Sound 🔒
- Voice: bm_george (style.json / character.json).
- Music signature: ambient, D dorian, 78 bpm, seed 21, ducked under the voice, loudness -14 LUFS.
- SFX meanings: pop = new item, whoosh = scene change, ding = payoff/CTA, boom = big reveal, scratch/crickets/wah = comedy beats only.

## 6. Formats 🔄
| format | weight | length | structure | hooks |
|---|---|---|---|---|
| big-question | 0.45 | 25-45 s | Ved asks, question on screen at frame 0 → the mechanism as full-screen 2D/3D visuals (voice-over) → Ved reaction beat → payoff that answers it | question |
| myth-bust | 0.30 | 20-30 s | "MYTH:" headline + Ved deadpan → the truth shown as visuals/evidence (voice-over) → why the myth exists | myth-bust |
| scale-shock | 0.25 | 20-30 s | huge number counting up at frame 0 → make it visible in full-screen 3D (voice-over) → a comparison the viewer feels | number-shock |

Skeletons: `jobs/_templates/<format>.json`. Never the same format three days in a row.

## 7. Hooks 🔄
question · myth-bust · number-shock · "you've been told X" · countdown. The hook is on screen at frame 0 and spoken in the first 1.5 s.

## 8. Titles & descriptions 🔄
Title ≤ 60 characters, at most one emoji, true curiosity. Description: one-line summary, then "Sources:" with links.
5-10 tags, plus #shorts and 2 niche hashtags.

## 9. Accuracy 🔒
Every factual claim is checked with a search in the same run, with sources in `meta.sources`. Anything unverified is dropped.

## 10. Schedule 🔄
- Zapier Pro trial until 2026-11-20: 3 Shorts a day, slot b 12:50, slot c 15:50, slot a 18:50 IST.
- After the trial (free plan, 100 tasks/month): slot a 18:50 IST daily; bonus slots b/c only near the end of the billing cycle.
- Weekly review: Sunday 10:20 IST (stats + sync with the Google Docs: 3 Zapier calls).

## 11. Humour 🔄
One comic beat per video (job-spec "Beats"): deadpan, side_eye, smirk, freeze, zoom_punch or silence, with an optional
meme-caption card. Current (last 2-3 weeks), sneaky, on-topic, dry and quick. Banned: dead memes, punching down, politics,
tragedy, crude jokes, real people's photos, copied meme images or audio.
- Landed: (filled in by the weekly review)
- Flopped: (filled in by the weekly review)

## 12. Change log
| date | section | change | evidence |
|---|---|---|---|
| 2026-11-07 | all | channel set up | owner decisions in setup |
| 2026-11-08 | 1, 2, 3 | niche = complex topics made simple; cinematic Blender 3D + infographic text; even-handed politics/economics; callbacks only when essential | owner request |
