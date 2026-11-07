# Google Docs for the channel

Four Google Docs hold everything that isn't code. Setup creates them, and their links go in
`channel/docs.json` so every run can find them.

```json
{"bible": "<doc link or id>", "log": "<doc link or id>", "insights": "<doc link or id>", "ideas": "<doc link or id>"}
```

---------------------------------------------------------------------------------------------------
## Doc 1: "<Channel> - Channel Bible"
Only the owner changes sections marked 🔒. The weekly review may tune sections marked 🔄, and logs each change in §11.

1. **Identity 🔒**: channel name/handle · niche (one line) · promise to the viewer · audience (who, age band,
   country) · language · style reference (channels/videos to resemble, or "fully original") and what we take from them.
2. **Tone 🔒**: personality in three words · how the narrator talks · things we never do.
3. **Look 🔒**: palette, fonts, background and captions live in `channel/style.json` in the repo. Layout zones:
   visuals y 0.10–0.34, captions y≈0.41, Professor Ved y≈0.68 with h≈0.40 (his feet may sit in the UI zone; it's only ground), nothing below y 0.78 or right of x 0.86.
   Recurring visual motifs. 3D: simple low-poly cutaways and backdrops (faceless people, easy locations) behind
   2D Ved, same light and grade; rules in `docs/sheets/vast_world_3d_guide.png`.
4. **Cast 🔒**: table of id · name · role · personality · voice · poses. Catchphrases. The rule: characters are made only by
   `characters/<id>/make.py`, and their colours, proportions and voice never change.
5. **Sound 🔒**: the voice (style.json / character.json), the music signature (style, key, bpm, seed), and what each SFX means:
   pop = new item, whoosh = scene change, ding = payoff/CTA, boom = big reveal.
6. **Formats 🔄**: 2–4 recurring templates, each with a weight, length, scene structure and allowed hook types.
   A skeleton for each lives at `jobs/_templates/<format>.json`.
7. **Hooks 🔄**: the hook types we use (number-shock, myth-bust, question, "you're doing X wrong", countdown...).
8. **Titles & descriptions 🔄**: title ≤ 60 chars, at most one emoji, true curiosity. Description = summary + source line.
   5–10 tags, plus `#shorts` and 2 niche hashtags.
9. **Accuracy 🔒**: every factual claim is checked in the same run, with sources in `meta.sources`. Anything unverified gets dropped.
10. **Schedule 🔄**: 3 Shorts/day: slot a 08:40, slot b 13:20, slot c 18:50 IST. Weekly review Sunday 10:20 IST.
11. **Change log**: date · section · change · evidence.

---------------------------------------------------------------------------------------------------
## Doc 2: "<Channel> - Shorts Log"
One line per posted video, appended by each production run (`python -m autopilot logline ...`):

`id | posted (IST) | title | format | hook | topic | length | url | youtube_id`

Newest goes at the bottom. Never edit old lines. The review adds stats in its own doc, not here.

---------------------------------------------------------------------------------------------------
## Doc 3: "<Channel> - Insights"
The weekly review writes a new entry at the **top**: date · data window · findings with numbers · decisions ·
next week's experiment.

---------------------------------------------------------------------------------------------------
## Doc 4: "<Channel> - Idea Backlog"
`- [format] idea · why it should work · source link`. Production runs append runners-up and delete what they use.
