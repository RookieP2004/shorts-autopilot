# Channel bible

The single source of truth for what this channel is. Every video follows it.
Sections marked 🔒 are locked: the weekly review may not change them; only the owner can.
Sections marked 🔄 may be tuned by the weekly review (log every change at the bottom).

> STATUS: TEMPLATE. Fill this in during channel setup before the first video goes out.

## 1. Identity 🔒
- Channel name / handle:
- Niche (one line):
- Promise to the viewer (what they get every video):
- Audience (who, age band, country, language):
- Language of narration and on-screen text:
- Style reference (videos/channels to resemble, or "fully original") and what to take from them:

## 2. Tone 🔒
- Personality in three words:
- How the narrator talks (sentence length, slang level, humour):
- Things we never do (clickbait lies, mocking groups, gore, medical advice, etc.):

## 3. Look 🔒
- Palette, fonts, background, captions: defined in `channel/style.json`. Do not override per video
  except where a format below allows it.
- Layout zones (1080x1920): headline/visuals y 0.10–0.34, captions y≈0.45,
  character y≈0.62–0.66 with h ≤ 0.30. Nothing important below y 0.78 or right of x 0.86 (YouTube UI).
- Recurring visual motifs (e.g. burst behind numbers, arrow pointing to the key word):

## 4. Cast 🔒
| id | name | role | personality | voice | poses |
|----|------|------|-------------|-------|-------|
| host | Pip (placeholder) | narrator | curious, upbeat | am_michael @1.05 | idle, talk, blink, happy, shocked, think |

- Catchphrases / recurring lines:
- Rules: a character never changes colours, proportions or voice. New poses are added as new SVG files
  in the same drawing style (copy an existing pose and edit only face/arms).

## 5. Sound 🔒
- Voice: `style.json > voice` (per-character override in `characters/<id>/character.json`).
- Music: `style.json > music` (style, key, bpm, progression, seed). Same settings = same signature sound.
- SFX language: pop = new item appears, whoosh = scene change, ding = payoff/CTA, boom = big reveal.

## 6. Formats 🔄
Recurring templates. Each video uses exactly one. Weights decide how often each is picked.

### fact-drop (weight 1.0)
- 20–35 s, 4–6 scenes.
- S1 hook (0–3 s): the most surprising claim, big number or word on screen from frame 0.
- S2–S4: explain in 2–3 beats, one visual idea per scene.
- S5 payoff/twist. S6 (optional) CTA ≤ 2 s.

### (add 1–3 more formats during setup)

## 7. Hooks 🔄
Hook types we use (tag each video's `meta.hook` with one): number-shock, myth-bust, question,
"you've been doing X wrong", countdown, before/after.

## 8. Titles & descriptions 🔄
- Title ≤ 60 chars, no ALL CAPS sentences, one emoji max, curiosity without lying.
- Description: 1–2 sentence summary + source line if a fact was used.
- Tags: 5–10. Hashtags: `#shorts` + 2 niche tags.

## 9. Accuracy 🔒
- Every factual claim is checked with a web search in the same run; sources noted in `meta.sources`.
- If a claim can't be verified, drop it.

## 10. Schedule 🔄
- 2 videos/day. Slots (IST): 
- Weekly review: every 7 days.

## 11. Change log
| date | section | change | why (evidence) |
|------|---------|--------|----------------|
