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
- Style: fully original, a **mix of 2D and 3D**: Professor Ved and other 2D characters live inside a 3D world (like Rick's Clips:
  2D cartoon characters in a bright 3D world), standing on the 3D sets, pointing at things and reacting; clean 3D objects with soft
  light and depth of field (like Zack D Films); bold 2D infographic panels, icons and big text on top (like The Infographics Show).
  Ved is always 2D. Every idea is turned into a concrete picture or analogy (10 apples and 10 dollars = inflation).

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
- **3D world + 2D characters:** the world is built from Blender **stills** (sets from 2-3 camera angles + prop cut-outs, made by
  the job's `assets_script`) and animated in 2D at 30 fps, so motion is smooth and renders take minutes. Ved **lives in it**: he
  walks in from the side, talks to camera in close-ups, jumps, points, reacts; props drop, bounce, fly and flip; 8-14 cuts across
  wide / medium / close-up shots. Animated Blender shots only when a moving 3D camera is essential. The sets are: a studio cyclorama or a
  bright, colourful little world (street, lab, market, body interior), warm key + cool rim light, glossy/clay/metal/paper materials,
  shallow depth of field, slow dolly/orbit, things popping in, flying and flipping. Real objects stand in for abstract ideas
  (apples for goods, banknotes for money). Ved stands on the set's floor line with his moving shadow, scaled by perspective
  (`autopilot/stage.py`). Close-ups can be pure 3D.
- **The town:** the world is populated. Faceless townspeople (`extra`, outfits and ornaments show who they are: seller in an apron,
  banker in a suit and bowler, shoppers in headscarves, straw hats, fezzes) react to the idea with body language (cheer and jump when
  money arrives, slump and walk away when prices rise). Same people, same outfits through the whole video. Staged in depth with
  correct perspective; counters and tables sit in front of people behind them.
- **2D layer:** flat infographic panels (cream cards, icons, arrows, before/after numbers), bold headlines, counters and the comic
  beat card, all in the channel palette. Avoid childish clip-art diagrams; every 2D graphic must carry real information.
- Simple low-poly 3D (`scene3d`) only for quick crowds or maps.
- References: `docs/sheets/professor_ved_character_sheet.png`, `vast_world_style_guide.png`, `vast_world_3d_guide.png`.
- **Visual-first: the pictures explain, Ved and the town act it out.** Every explanation step gets its own shot, prop or
  panel; something new moves on screen at least every 2-3 seconds; never a talking head explaining something we could show.
- **Reference video (owner-approved, 2026-11-08):** `jobs/2026-11-08-m3` ("Why can't countries just print more money?",
  youtu.be/QFhXI3hT9Ik). This is the quality bar and the house style: every new video should look at least this alive, in its own
  new world and story.

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

**Deep Dive (long video, weekly)** 🔒 owner-approved 2026-11-11. One a week, Saturday. 16:9 (1920x1080), 5-8 min
(hard cap 12 min and 90 MB), `"kind": "long"` in job.json (the long-form style profile in style.json does the rest).
- Topic: a big idea from the niche that needs more than 60 s; prefer the idea behind this week's best Short (from the log /
  the review's stats), going much deeper. Same Ved, same town and outfits, same look as the Shorts, framed for landscape.
- Shape: cold open (a concrete object or question in the first 5 s, plus a promise of the payoff) -> 5-8 chapters, each a little
  story in the 3D world with the townspeople acting it out -> recap -> "money is trust you can carry"-style one-line payoff ->
  short subscribe outro. A new shot or cut every 3-6 s; Ved talking to camera from one side with a panel or headline on the other.
- Chapters in job.json (`chapters`, >= 3, first at scene 0, each >= 10 s); they go into the description automatically.
- 2-3 comic beats (one per ~2 minutes), same rules as the Shorts.
- Even-handed: where experts disagree, give both views in one or two lines each.
- Thumbnail (owner-approved look, 2026-11-11, The Infographics Show as reference): the world blurred and colour-graded
  behind (a two-colour gradient tint + a warm glow behind Ved), Ved big and sharp with a strong face (surprised, shocked,
  side-eye) right under the title, one or two key props sharp beside him, and a huge 1-3 word title in heavy white sans with
  one *accent* word ("JUST *PAPER?*"). No watermark, no small text. `python -m autopilot thumbnail` (spec in docs/job-spec.md);
  set via Zapier when the budget allows, otherwise the owner sets it in YouTube Studio.
- Reference: `jobs/2026-11-11-longpilot` ("How Money Actually Works").

## 7. Hooks 🔄
question · myth-bust · number-shock · "you've been told X" · countdown. The hook is on screen at frame 0 and spoken in the first 1.5 s.

## 8. Titles & descriptions 🔄
Title ≤ 60 characters, at most one emoji, true curiosity. Description: one-line summary, then "Sources:" with links.
5-10 tags, plus #shorts and 2 niche hashtags.

## 9. Accuracy 🔒
Every factual claim is checked with a search in the same run, with sources in `meta.sources`. Anything unverified is dropped.

## 10. Schedule 🔄
- Zapier Pro trial until 2026-11-20: 3 Shorts a day, live around 12:50 (b), 15:50 (c) and 18:50 (a) IST; the runs start at
  11:56, 14:56 and 17:56 because each Short takes 40-50 minutes to make (owner, 2026-11-12: videos should be up by those times).
- After the trial (free plan, 100 tasks/month): slot a 18:50 IST daily; bonus slots b/c only near the end of the billing cycle.
- Deep Dive (long video): Saturday 16:20 IST, weekly (1 upload + 1 thumbnail call). On the free plan it replaces that
  Saturday's regular Short (`budget --need upload --ref <id>-a` exits 4).
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
| 2026-11-11 | 6, 10 | weekly long video (Deep Dive, 16:9) added | owner: "make it a video a week" |
| 2026-11-08 | 3 | v3 (2026-11-08-m3) approved as the final house style and reference video; removed the old "Ved small in a corner" rule | owner: "final this" |
| 2026-11-08 | 3 | living town: faceless townspeople with outfits, body-language emotions, depth staging (perspective + foreground layers), smoother stall/apples | owner request |
| 2026-11-08 | 3 | 3D world from stills + cut-outs animated in 2D (smooth, fast); Ved walks/jumps/talks to camera; multi-angle cuts | owner request |
| 2026-11-08 | 1, 3 | style = 2D characters in a 3D world (Rick's Clips) + 2D infographic panels + clean 3D objects | owner request |
| 2026-11-08 | 1, 2, 3 | niche = complex topics made simple; cinematic Blender 3D + infographic text; even-handed politics/economics; callbacks only when essential | owner request |
