---
name: "shorts-autopilot"
description: "Run Sujal's automated YouTube Shorts channel: channel setup, making and posting a code-drawn Short (research, script, render, post via Zapier), or the weekly review. The channel's docs live in Google Docs. Use for any scheduled Shorts run."
---

# Shorts Autopilot

You run a YouTube Shorts channel on your own. Every video is made **entirely in code by you**:
script, original 2D SVG characters, motion graphics, captions, Kokoro TTS voice, procedural music
and SFX. No stock footage and no outside AI video or image services (the owner asked for this).

How it fits together:
- **Tool**: the public GitHub repo `shorts-autopilot`. Inside it, `python -m autopilot` renders videos from `job.json`,
  and `scripts/push_media.sh` publishes a finished video to the repo's `media` branch, which gives it a public download URL.
- **Posting**: the **Zapier** connector, using the action *YouTube: Upload Video* with that URL as the video file.
  Zapier is an approved YouTube app, so videos can go public right away.
- **Memory**: **Google Docs**. There are four docs: Channel Bible, Shorts Log, Insights and Idea Backlog. Their links are in
  `channel/docs.json`. Read and edit them with the claude.ai Google Docs connector (Google Drive connector to create them).
  **Never use Zapier's Google Docs actions**: they would eat the free task budget. If no Google Docs connector is available,
  write the log line and notes to `channel/pending_docs.md` in the repo, push, and tell the owner. If a `google-workspace` skill is listed, load it before the first doc edit.
- **Zapier budget**: the owner is on Zapier's **free plan, 100 tasks/month**. Each successful Zapier call costs 2 tasks (failed calls cost 0).
  `python -m autopilot budget` counts calls in `channel/zapier_ledger.json`. With `zapier.cycle_day` set in style.json (the day of
  the month Zapier's usage resets), it counts from the last reset and plans to use **every** task by the next reset (bonus Shorts,
  section 3c). Without it, it falls back to a rolling 31 days capped at 48 calls, with no bonus Shorts.
  **Trial:** while `zapier.trial_until` is in the future, the budget uses `trial_tasks` (1,000) and treats the trial's end as the
  reset, so the bonus slots run every day and the channel posts 3 Shorts a day. Trial calls never count against the free plan.
  Never suggest adding a payment method: the owner wants the trial to drop to Free on its own.
  Always pass the slot id as `--ref` for uploads: the budget tells the regular slot (`-a`) from bonus slots (`-b`, `-c`).
  Before any Zapier execute call, run `python -m autopilot budget --need <upload|stats>`. Exit code 3 means no budget: don't call Zapier.
  After every **successful** Zapier execute call, run `python -m autopilot budget --add <upload|stats|other> --ref <id>` and commit the ledger.
  Inspect/discover/enable calls are free and are not recorded.
- The workspace can reach GitHub and PyPI only. Everything that touches YouTube or Google goes through those connectors.

There are four modes. Work out which one applies:
- **Setup**: `channel/docs.json` is empty, or the owner asks to set up or change the channel. This mode is interactive.
- **Produce**: a scheduled run, or "make/post a Short". This mode runs unattended.
- **Review**: every 7 days (scheduled), or "analyse the channel". This mode runs unattended.
- **Manual**: the owner triggers a new video themselves, often with their own changes ("make one on X, slower voice, more 3D").
  Run Produce mode for an extra slot, and follow section 3b.

**This skill is the fixed backbone.** No run ever edits SKILL.md, `channel/style.json`, `characters/`, `jobs/_templates/`,
the renderer, or the Bible's 🔒 sections because of one video's request. The only things that change the backbone are:
- the weekly review, in 🔄 Bible sections only;
- the owner saying plainly that a change is permanent ("make this permanent", "from now on", "always").

If it's unclear whether a change is one-off or permanent, treat it as one-off and ask once in the report.

## 0. Start of every run
1. **Repo**: `list_repos` with query `shorts-autopilot`, then `add_repo(owner, repo, access="push")`, then run the clone command
   it returns, then `register_repo_root`. Then `pip install -q -r requirements.txt --break-system-packages`
   and `bash scripts/fetch_models.sh` (~350 MB, about 1 minute). If the repo isn't there, stop and tell the owner.
2. **Connectors**: load the Zapier tools with ToolSearch, searching for "zapier youtube".
   If *YouTube: Upload Video* isn't enabled, use Zapier's discover/enable action tools to add it.
   Load the claude.ai Google Docs/Drive connector tools with ToolSearch ("google docs"). If Zapier isn't connected at all, stop and tell the owner it needs connecting in claude.ai.
3. **Read the channel**: open the Bible, the top entry of Insights, the Idea Backlog, and the last 30 lines of the Shorts Log.
   Then read `channel/style.json` and `docs/job-spec.md`, and run `python -m autopilot characters`.

## 1. Consistency rules (never break these)
- **Look**: use only the palette, fonts, background and caption style in `style.json`. Don't override them per video unless the Bible's format allows it.
- **Cast**: characters are made only by `characters/<id>/make.py`, from one base drawing. To add a pose, add an entry to `POSES`
  and re-run it. Never hand-draw a new version of a character. A character's colours, proportions, voice and personality never change.
- **Sound**: the voice comes from `style.json` or `character.json`. The music settings (`style`, `key`, `bpm`, `progression`, `seed`)
  are the channel's signature sound, so don't change them per video.
- **Acting**: Professor Ved is rigged (`characters/ved/make.py`) and drawn fresh every frame. While he talks he changes
  gesture at natural pauses and moves smoothly between poses (`"acting": "auto"`, the default). When a gesture must land
  on a word, script it with `"acting": [["point", 1.4], ...]`. Never put loop animations (bob, float, wiggle, shake) on a
  character, because they read as shaking. Use loops only for props and text. Lip-sync is automatic: 5 mouth shapes chosen from the voice.
- **Props**: draw them as inline SVG in the channel's flat style. Use only palette colours and the cast's stroke weight.
- **Layout**: visuals and the headline go at y 0.10–0.34, captions at y≈0.41, Professor Ved at y≈0.68 with h≈0.40. His feet may sit in the
  bottom UI zone, because that's only ground. Nothing that matters goes below y 0.78 or right of x 0.86, because YouTube's UI covers those areas.
- **World**: "The Vast World". The home base is `assets/bg/study.svg`. Cut to `world.svg` (landscapes, nature, history outdoors) or `cosmos.svg`
  (space, physics) when the topic travels. New sets are written into `assets/bg/make_backgrounds.py` and follow its depth rules:
  foreground 4.5 px line, midground 2 px at 60%, background no line and bluer with distance. Warm key light from the left, cool shadows.
- **3D**: mix in simple code-made 3D (`scene3d` layers, see `docs/job-spec.md` and `docs/sheets/vast_world_3d_guide.png`)
  for crowds, scale, places and demonstrations. People are faceless low-poly mannequins, and locations are built from
  terrain, planes, buildings, trees and primitives. Professor Ved is always 2D and in front. 3D uses the same upper-left
  warm light and fog = sky colour, the camera moves slowly (orbit ≤ 8°/s), and there are one or two 3D shots per video at most.
- **Look references**: `docs/sheets/professor_ved_character_sheet.png`, `vast_world_style_guide.png` and `vast_world_3d_guide.png`.
  Check new props and sets against them, and rebuild them with `scripts/build_sheets.py` whenever the cast changes.
- **Formats**: each video uses exactly one format from the Bible, with its structure and length.
- **Humour**: every video gets **one** comic beat (two only past 40 s), built with a scene `beat` (see `docs/job-spec.md` "Beats"):
  `deadpan`, `side_eye`, `smirk`, `freeze`, `zoom_punch` or `silence`, with an optional meme-caption card (`text`, ≤ 60 chars).
  It must be **current, sneaky and on-topic**: a trend from the last 2–3 weeks (meme format, phrase or slang), bent to fit this
  video's subject so it lands as an unexpected aside, never a detour. Place it right after a line (`"at": "after_say"`), usually
  between 35% and 80% of the video; never in the first 1.5 s, never over speech, never in the final payoff line. Keep it dry and
  quick: the joke is the reaction or the caption, never a long setup. Ved stays Ved: a wise, cool young professor with a dry
  sense of humour, not a clown. No "boomer" humour (dad jokes, "when you…" captions on dead formats, forced slang, excess emoji).
  Recreate meme formats in the channel's own art: no meme images, screenshots, real people's faces, trending songs or copied audio.
  No punching down, politics, religion, tragedy or crude jokes. If nothing current fits naturally, use a timeless dry reaction instead
  of forcing one.
- Only the owner can change 🔒 Bible sections. The review may change 🔄 sections, and must log each change in the Bible's change log.

## 2. Setup mode (with the owner)
Ask, don't assume. Use AskUserQuestion for choices, and send previews as files.
1. **Identity**: niche, promise, audience, language (Kokoro has en-us, en-gb, hi, es, fr, it, ja, pt and zh voices), and
   whether the style should resemble reference channels or be fully original. For references, research them on the web
   (titles, structure, pacing, visual devices) and write down what to borrow. Never copy their characters, branding or catchphrases.
2. **Look**: edit `style.json` (palette, fonts from `fonts/` or another OFL font from google/fonts, background, caption
   style, watermark = handle). Run `python -m autopilot frames jobs/example/job.json` and send the owner the stills.
3. **Cast**: Professor Ved (`characters/ved/`, aged 25–35) is the main explainer. Any new character gets its own
   `characters/<id>/make.py` (copy `characters/ved/make.py` as the pattern) and `character.json` (name, description, `default_h`, voice).
   Required poses: idle, talk, blink, and each acting pose needs `_talk` and `_blink` versions. For the voice, make 20-second samples of
   3–4 candidate voices with `autopilot.audio.tts`, send them, and let the owner pick.
4. **Sound**: choose the music style (lofi, ambient, upbeat or suspense), key, bpm and seed. Send a sample.
5. **Formats**: define 2–4 formats. For each one, save a skeleton at `jobs/_templates/<format>.json`.
6. **Docs**: create the four Google Docs, following `docs/google-docs-templates.md`, filled with everything decided above.
   Put their links in `channel/docs.json`, then commit and push.
7. **Pilot**: make one full video, publish it with `push_media.sh`, and upload it through Zapier as **private**. Send the owner the
   link and iterate until they're happy. This also proves the Zapier connection works.
8. **Schedule**: create the scheduled tasks (section 5). Remind the owner to set the Zapier and Google Docs tools to run
   without asking, otherwise unattended runs will stall waiting for approval.

## 3. Produce mode (unattended, one video)
There is 1 regular Short a day (Zapier free plan), slot `a`. Bonus slots `b` and `c` post only near the end of the Zapier
billing cycle (section 3c). The slot id is `YYYY-MM-DD-<slot>`, using the IST date. Never post the same format
three days in a row. If the Shorts Log already has that id, or `jobs/<id>/` exists in the repo, the slot is done. Stop.
**Budget first:** run `python -m autopilot budget --need upload` before researching. If it exits 3, don't make the video;
send the owner one SendUserMessage saying today's Short was skipped because the Zapier free-plan budget is used up, and stop.

**a. Research (4–8 searches, send them in parallel).** Look at what is trending in the niche this week, news hooks, evergreen
questions people ask, and what's working for similar Shorts. If the vidIQ connector is available, use its trending and
outlier tools. Collect 5 candidates, and add the Idea Backlog as candidates too.
Also run 2–3 searches for **humour that is current right now**: meme formats, catchphrases and slang trending this week on
YouTube Shorts, Instagram Reels and X (e.g. "trending meme format this week", "viral phrase <month year>", Know Your Meme's recent
entries). Note 2–3 that are still rising (not peaked or dead), what each means, and where the Bible's Humour list says it flopped before.

**b. Pick.** Score each candidate 1–5 on: hook strength · fit with the channel promise · format fit · novelty (no topic
repeated within 30 days of the Log) · evidence from Insights (formats and hooks that win) · can be drawn with the current cast
and simple props. Take the top score.

**c. Verify.** Check every factual claim with a search. Drop anything you can't confirm, and put the URLs in `meta.sources`.

**d. Script.** The hook lands in the first 1.5 s and frame 0 must already show it (`enter: none`, or `at: 0` with a fast pop).
Use one idea per scene and about 2.6 spoken words per second (30 s ≈ 75 words). End on a payoff, or a line that loops back to the start.
Write it in the channel's voice. Clickbait must still be true.
Plan the comic beat now: which line sets it up, which trend it borrows, which `beat` kind and caption pay it off. Read it back:
if it needs explaining, or a 20-year-old would cringe, cut it or swap it for a plain dry reaction.

**e. Build `jobs/<id>/job.json`** from the format skeleton (see `docs/job-spec.md`). Fill in `meta` honestly
(format, topic, hook, idea_source, characters, sources, and `humour`: the trend used, the beat kind, its time), because the review
depends on it. Write the title, description and tags per the Bible.

**f. QA loop (up to 3 rounds).** Run `python -m autopilot validate` and then `python -m autopilot frames jobs/<id>/job.json`.
**Look at every frame** with Read. Check that text is readable, nothing sits in the red zone, nothing overlaps, characters are on-model,
frame 0 shows the hook, and it doesn't look like the last 3 videos. Fix and repeat.
Also render a still in the middle of the beat (`frames --at <scene start + beat at + 0.4>`) and check the caption card is
readable and Ved's reaction face reads clearly.

**g. Render.** Run `python -m autopilot render jobs/<id>/job.json`. Check `out/render.json`: the length must be ≤ 58 s. Then pull 3–4 frames from
`out/final.mp4` with ffmpeg and look at them.

**h. Publish.**
1. Run `scripts/push_media.sh jobs/<id>/out/final.mp4 <id>`. It prints the public URL and waits until the URL serves the file.
   Exit code 2 means the URL isn't reachable. Retry once; if it still fails, stop and notify the owner (the repo may not be public).
2. Run `python -m autopilot zapier jobs/<id>/job.json` to get the upload fields.
3. Call Zapier *YouTube: Upload Video* with video/file = the URL, plus title, description, tags, privacy status, category and
   made-for-kids = no. Read the video id from the response, then run `python -m autopilot budget --add upload --ref <id>`.
   If the call fails (an error costs 0 tasks), retry once. If it fails again, stop and notify the owner.
   Never upload twice: before a retry, check the Log. Use *YouTube: Find Video* (2 tasks) only if the first call timed out with no clear result.
4. Run `git add jobs/<id>/job.json channel/zapier_ledger.json && git commit -m "short <id>: <title>" && git push`.
5. Append `python -m autopilot logline jobs/<id>/job.json --youtube-id <id>` to the end of the Shorts Log doc. In the Idea Backlog,
   remove the idea you used and add the 2–3 runners-up.

**i. Report.** Send the owner one SendUserMessage: title, link, format and hook, the joke used (one line), and why you picked it (one line).

## 3c. Bonus slots (use every Zapier task before the reset)
Tasks left at the reset are lost, so near the end of the billing cycle spend them on extra Shorts.
1. At the very start of a bonus run (slot `b` or `c`), before installing models or researching, clone the repo and run
   `python -m autopilot budget --bonus`. If the last line is `BONUS 0`, stop at once and don't message the owner.
   It is 0 whenever `zapier.cycle_day` isn't set, or the reset is too far off for spare tasks to exist.
2. Otherwise make **one** Short for this slot with the full Produce flow (sections 3a–3i, same quality bar, different topic and
   format from today's other Shorts), with id `YYYY-MM-DD-b` or `-c`, and record it with `budget --add upload --ref <id>`.
3. If the owner uses Zapier for anything else and tells you the "tasks used" figure from Zapier's billing page, run
   `python -m autopilot budget --sync <tasks>` and commit the ledger, so the bonus maths stays honest.

## 3b. Manual run with the owner's one-off changes
1. Do Produce mode (sections 3a–3i) for an extra slot, with id `YYYY-MM-DD-m1`, `-m2`, and so on, so it never takes a scheduled slot.
   If the owner already gave the topic, skip research and only verify the facts.
2. Turn each of the owner's changes into **job-level** settings only:
   - topic, script or format choice: the job content;
   - look or sound tweaks: `style_override` in job.json (deep-merged over style.json for this video only);
   - voice for one video: scene or job `voice`;
   - new props or sets: inline SVG or `scene3d` inside this job.
   Never edit the backbone files to get the effect.
3. Describe the one-off changes in plain words in `meta.overrides`. They're recorded in the Shorts Log, and the review
   treats that video as an experiment, not as the normal format.
4. In the report, list what was applied as one-off. Offer in one line to make any of it permanent; it only becomes permanent if the owner says so.

## 4. Review mode (every 7 days)
1. **Collect stats.** Take every video id from the Shorts Log for the last 28 days. Get views, likes, comments and publish time
   for all of them in **one** call:
   - vidIQ channel stats, if that connector is available (costs no Zapier tasks, so prefer it);
   - otherwise one Zapier YouTube "API Request" call: `GET https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails,status&id=<up to 50 ids, comma-separated>`.
     Run `python -m autopilot budget --need stats` first and `--add stats` after. Never call Find Video once per video.

   Write the results to `stats/latest.json` in the format at the top of `scripts/analyze.py`, joined with format, hook and topic from the Log.
   If no stats source works, tell the owner which Zapier action to enable, and stop.
2. Run `python scripts/analyze.py stats/latest.json`. If there are fewer than 6 videos older than 48 h, add a short note to Insights and stop.
3. Find what wins and loses by format, hook, topic cluster, length and 2D-only vs 2D+3D, using median views, likes per 1k views and comments per 1k views.
   Manual videos with `one-off` notes in the Log are experiments: report them separately, and if one clearly wins, suggest it to the owner.
   Don't adopt it yourself.
   Retention is only available if the owner later adds an analytics source. Compare the top 5 with the bottom 5: what do the winners share
   (topic type, hook, first line, length)? Treat any difference under ~1.5× the channel median as noise.
4. Decide changes **only in 🔄 Bible sections**:
   - Shift format weights (minimum 0.1).
   - Prefer the winning hook types.
   - Retarget lengths.
   - Adjust title patterns.
   - Humour: compare videos by the beat kind and trend in `meta.humour` (and the Log). Record what landed and what flopped in
     the Bible's 🔄 Humour section, and steer away from formats that underperform.
   - Trial at most one new format per week, in ≤ 2 of the week's 7 slots, built from the existing cast and style.
   Never change 🔒 sections. If the data says one should change, put it to the owner as a suggestion.
5. Write a new entry at the **top** of the Insights doc: date, data window, findings with numbers, decisions, next week's experiment.
   Edit the 🔄 Bible sections and add the change-log lines. Steer the Idea Backlog toward what works.
6. Send the owner a summary of 5 lines or fewer.

## 5. Scheduled tasks (create these in setup)
Use `create_trigger` with `requires_local_device` false and the owner's time zone (Asia/Calcutta). Create one daily
production task at the Bible's slot time (default 18:50 IST). The prompts:
- Production: "Use the shorts-autopilot skill in Produce mode for today's slot `a` (IST date). Post one Short."
- Bonus (two daily tasks, 12:50 and 15:50 IST): "Use the shorts-autopilot skill: bonus slot `<b|c>` (IST date). Check
  `budget --bonus` first and stop quietly if it is 0."
- Review (weekly, e.g. Sunday 10:20 IST): "Use the shorts-autopilot skill in Review mode."
In setup, ask the owner which day of the month their Zapier usage resets (Zapier → Settings → Billing) and set `zapier.cycle_day`.
Leave it null until the owner has read it off the billing page after the trial ends; never guess it. If the first free cycle shows
fewer than 100 tasks (Zapier may pro-rate it), lower `zapier.plan_tasks` for that cycle or run `budget --sync`, and tell the owner.
Each run starts fresh, so the repo and the Google Docs carry all the state.

## 6. Platform rules
- Everything is original: no copyrighted characters, logos, music or lyrics.
- YouTube demonetises repetitive, mass-produced content. Every video needs a real, distinct idea and fresh writing, even within a
  format. Never post near-duplicates or reposts.
- Synthetic-media disclosure is for realistic AI content. Cartoon characters don't need it. If a format ever shows realistic people or
  events, set `youtube.synthetic_media` to true in style.json and tick the matching field in Zapier if it offers one.
- Each successful Zapier call costs 2 tasks of the owner's 100 a month. Make no extra calls, and always go through the budget check.
  Manual runs count too: if `--need upload` says no, tell the owner and offer to render the video now and post it when the budget frees up.
- More regular videos a day only if the owner moves to a paid Zapier plan: then raise `zapier.plan_tasks` in style.json.
  The bonus logic scales with it automatically.

## 7. Not built yet
Instagram Reels posting. `final.mp4` is already Reels-ready (9:16), and the same media URL can feed a Zapier
*Instagram for Business: Publish Video/Reel* action once the owner has an Instagram Business account. Tell the owner if they ask.