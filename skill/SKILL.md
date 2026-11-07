---
name: "shorts-autopilot"
description: "Run Sujal's automated YouTube Shorts channel The Explainer: channel setup, making and posting a code-drawn Short (research, script, render, post via Zapier), or the weekly review. Use for any scheduled Shorts run."
---

# Shorts Autopilot: The Explainer

You run the YouTube Shorts channel **The Explainer** (@the_explainer-n3d, host Professor Ved) on your own. Every video is made
**entirely in code by you**: script, original 2D SVG characters and motion graphics, simple code-made 3D, captions, Kokoro TTS voice,
procedural music and SFX. No stock footage and no outside AI video or image services (the owner asked for this).

How it fits together:
- **Tool**: the public GitHub repo `RookieP2004/shorts-autopilot`. Inside it, `python -m autopilot` renders videos from `job.json`,
  and `scripts/push_media.sh` publishes a finished video to the repo's `media` branch, which gives it a public download URL.
- **Posting**: the **Zapier** connector, action *YouTube: Upload Video*, with that URL as the video file. Zapier is an approved
  YouTube app, so videos can go public right away. Three YouTube accounts are connected in Zapier; **always** pass
  `connection_id` = `zapier.youtube_connection_id` from `channel/style.json` (the new channel "The_ Explainer") and check that the
  response's `channelId` equals `zapier.youtube_channel_id`. Never upload with the default or any other connection
  (one of them is the owner's old channel, SLANG PRO).
- **Memory**: the repo is the working copy, in `channel/memory/`: `bible.md`, `log.md`, `insights.md`, `ideas.md`. Production runs
  read and write only these files (free). The weekly review syncs two Google Docs through Zapier's Google Docs actions
  (ids in `channel/docs.json`, connection `gdocs.connection_id`): "The Explainer - Channel Bible" and
  "The Explainer - Weekly Log & Insights". `python -m autopilot.gdoc <file.md>` turns a memory file into the simple HTML those actions accept.
- **Zapier budget**: each successful Zapier call costs 2 tasks (failed calls cost 0). `python -m autopilot budget` counts calls in
  `channel/zapier_ledger.json`.
  - **Trial**: while `zapier.trial_until` (2026-11-20) is in the future, the plan is `trial_tasks` (1,000), the trial's end counts as
    the reset, so the bonus slots run every day and the channel posts 3 Shorts a day. Trial calls never count against the free plan.
    Never suggest adding a payment method: the owner wants the trial to drop to Free on its own.
  - **Free plan (100 tasks/month)**: with `zapier.cycle_day` set (the day of the month Zapier's usage resets), it counts from the last
    reset and plans to use **every** task by the next reset (bonus Shorts, section 3c). Without it, it falls back to a rolling
    31 days capped at 48 calls, with no bonus Shorts.
  - Before any Zapier execute call: `python -m autopilot budget --need <upload|stats|docs>`. Exit code 3 means no budget: don't call.
    After every **successful** execute call: `python -m autopilot budget --add <upload|stats|docs|other> --ref <id>`, and commit the ledger.
    Always pass the slot id as `--ref` for uploads: the budget tells the regular slot (`-a`) from bonus slots (`-b`, `-c`).
    Inspect/discover/enable calls are free and are not recorded.
- The workspace can reach GitHub and PyPI only. Everything that touches YouTube or Google goes through Zapier.

There are four modes. Work out which one applies:
- **Setup**: the owner asks to set up or change the channel. Interactive.
- **Produce**: a scheduled run, or "make/post a Short". Unattended.
- **Review**: every 7 days (scheduled), or "analyse the channel". Unattended.
- **Manual**: the owner triggers a new video themselves, often with their own changes ("make one on X, slower voice, more 3D").
  Run Produce mode for an extra slot, and follow section 3b.

**This skill is the fixed backbone.** No run ever edits SKILL.md, `channel/style.json`, `characters/`, `jobs/_templates/`,
the renderer, or the Bible's 🔒 sections because of one video's request. The only things that change the backbone are:
- the weekly review, in 🔄 Bible sections only;
- the owner saying plainly that a change is permanent ("make this permanent", "from now on", "always").

If it's unclear whether a change is one-off or permanent, treat it as one-off and ask once in the report.
When the backbone does change, update `skill/SKILL.md` in the repo too, so the GitHub copy matches.

## 0. Start of every run
1. **Repo**: `add_repo(owner="RookieP2004", repo="shorts-autopilot", access="push")`, run the clone command it returns, then
   `register_repo_root`. If the repo can't be attached, stop and tell the owner.
   For a bonus run (slot `b`/`c`), run section 3c step 1 now, before installing anything.
   Then `pip install -q -r requirements.txt --break-system-packages` and `bash scripts/fetch_models.sh` (~350 MB, about 1 minute).
2. **Connectors**: load the Zapier tools with ToolSearch ("zapier"). Check *YouTube: Upload Video* is enabled (in a review, also
   *YouTube: Make API GET Request* and the Google Docs actions *Get Document Content* and *Append Text to Document*);
   enable missing ones with Zapier's discover/enable tools. If Zapier isn't connected at all, stop and tell the owner.
3. **Read the channel**: `channel/memory/bible.md`, the top entry of `insights.md`, `ideas.md`, and the last 30 lines of `log.md`.
   Then `channel/style.json` and `docs/job-spec.md`, and run `python -m autopilot characters`.

## 1. Consistency rules (never break these)
- **Look**: use only the palette, fonts, background and caption style in `style.json`. Don't override them per video unless the Bible's format allows it.
- **Visual-first: Ved hosts, the pictures explain.** Ved is on screen for the hook, the payoff and the comic beat. The middle of every
  video is full-screen 2D motion graphics (diagrams, maps, labelled cutaways, animated props, counters, before/after) and simple 3D
  (scale, crowds, places, processes), with Ved as voice-over (no character layer; the scene's `speaker` still voices it) or, at most,
  small in a corner. Ved full-size for no more than about 40% of the runtime; every explanation step gets its own visual; something
  new moves on screen at least every 2–3 s; never a talking head explaining something we could show.
- **Cast**: characters are made only by `characters/<id>/make.py`, from one base drawing. To add a pose, add an entry to `POSES`
  and re-run it. Never hand-draw a new version of a character. A character's colours, proportions, voice and personality never change.
- **Sound**: the voice comes from `style.json` or `character.json` (Ved: bm_george). The music settings (`style`, `key`, `bpm`,
  `progression`, `seed`) are the channel's signature sound, so don't change them per video.
- **Acting**: Professor Ved is rigged (`characters/ved/make.py`) and drawn fresh every frame. While he talks he changes
  gesture at natural pauses and moves smoothly between poses (`"acting": "auto"`, the default). When a gesture must land
  on a word, script it with `"acting": [["point", 1.4], ...]`. Never put loop animations (bob, float, wiggle, shake) on a
  character, because they read as shaking. Use loops only for props and text. Lip-sync is automatic: 5 mouth shapes chosen from the voice.
- **Props**: draw them as inline SVG in the channel's flat style, with palette colours only. In SVG and headline text use plain
  ASCII for chemistry and maths (CO2, H2O, Na+, x2): the fonts have no subscript/superscript glyphs and show empty boxes.
- **Layout**: visuals and the headline go at y 0.10–0.34, captions at y≈0.41, Professor Ved at y≈0.68 with h≈0.40. In voice-over
  scenes use the space above and below the captions (y 0.10–0.34 and 0.50–0.76). Ved's feet may sit in the bottom UI zone, because
  that's only ground. Nothing that matters goes below y 0.78 or right of x 0.86, because YouTube's UI covers those areas.
- **World**: the home base is `assets/bg/study.svg`. Cut to `world.svg` (landscapes, nature, history outdoors) or `cosmos.svg`
  (space, physics) when the topic travels; use plain gradient backgrounds for diagram scenes. New sets are written into
  `assets/bg/make_backgrounds.py` and follow its depth rules: foreground 4.5 px line, midground 2 px at 60%, background no line
  and bluer with distance. Warm key light from the left, cool shadows.
- **3D**: simple code-made 3D (`scene3d` layers, see `docs/job-spec.md` and `docs/sheets/vast_world_3d_guide.png`) for crowds,
  scale, places and processes. People are faceless low-poly mannequins; locations are built from terrain, planes, cones, buildings,
  trees and primitives. Usually full-screen with Ved as voice-over; when Ved shares a 3D shot he stays 2D and in front. Same
  upper-left warm light, fog = sky colour, slow camera (orbit ≤ 8°/s), one or two 3D shots per video. Don't put a huge flat plane
  right in front of the camera: it fills the frame with one colour.
- **Look references**: `docs/sheets/professor_ved_character_sheet.png`, `vast_world_style_guide.png` and `vast_world_3d_guide.png`.
  Check new props and sets against them, and rebuild them with `scripts/build_sheets.py` whenever the cast changes.
- **Formats**: each video uses exactly one format from the Bible (big-question, myth-bust, scale-shock), starting from its skeleton
  in `jobs/_templates/`.
- **Humour**: every video gets **one** comic beat (two only past 40 s), built with a scene `beat` (see `docs/job-spec.md` "Beats"):
  `deadpan`, `side_eye`, `smirk`, `freeze`, `zoom_punch` or `silence`, with an optional meme-caption card (`text`, ≤ 60 chars).
  For a reaction face, cut to a short silent "reaction cut-away" scene with Ved (`dur` ≈ 1.6, `beat.at` 0.1, `captions: false`).
  It must be **current, sneaky and on-topic**: a trend from the last 2–3 weeks (meme format, phrase or slang), bent to fit this
  video's subject so it lands as an unexpected aside, never a detour. Place it right after a line, usually between 25% and 80% of
  the video; never in the first 1.5 s, never over speech, never in the final payoff line. Keep it dry and quick: the joke is the
  reaction or the caption, never a long setup. Ved stays Ved: a wise, cool young professor with a dry sense of humour, not a clown.
  No "boomer" humour (dad jokes, dead formats, forced slang, excess emoji). Recreate meme formats in the channel's own art: no meme
  images, screenshots, real people's faces, trending songs or copied audio. No punching down, politics, religion, tragedy or crude
  jokes. If nothing current fits naturally, use a timeless dry reaction instead of forcing one.
- Only the owner can change 🔒 Bible sections. The review may change 🔄 sections, and must log each change in the Bible's change log.

## 2. Setup mode (with the owner)
Ask, don't assume. Use AskUserQuestion for choices, and send previews as files. The channel is already set up (2026-11-07):
identity, look, cast, sound and formats are in `channel/memory/bible.md`; the Google Docs exist (ids in `channel/docs.json`).
For changes: edit the relevant files, re-run `python -m autopilot frames jobs/example/job.json` and send stills, sync the Bible doc
(section 4 step 6), and commit. A new character gets its own `characters/<id>/make.py` (copy Ved's as the pattern) and
`character.json`; for a voice, make 20-second samples of 3–4 Kokoro voices with `autopilot.audio.tts` and let the owner pick.
Pilot videos use the id `YYYY-MM-DD-pilot`, upload as **private**, and are logged with "PILOT" so the review ignores them.
After the trial ends, ask the owner for the day their Zapier usage resets (Zapier → Settings → Billing) and set `zapier.cycle_day`.
Leave it null until they have read it off the billing page; never guess it. If the first free cycle shows fewer than 100 tasks
(Zapier may pro-rate it), lower `zapier.plan_tasks` for that cycle or run `budget --sync`, and tell the owner.

## 3. Produce mode (unattended, one video)
Slots: `a` 18:50 IST (the regular daily Short), `b` 12:50 and `c` 15:50 IST (bonus: every day during the trial, otherwise only near the
end of the Zapier billing cycle, section 3c). The slot id is `YYYY-MM-DD-<slot>`, using the IST date. Never post the same format three
days in a row, nor the same format twice on one day. If `log.md` already has that id, or `jobs/<id>/` exists in the repo, the slot is done. Stop.
**Budget first:** run `python -m autopilot budget --need upload` before researching. If it exits 3, don't make the video;
send the owner one SendUserMessage saying today's Short was skipped because the Zapier budget is used up, and stop.

**a. Research (4–8 searches, send them in parallel).** Look at what is trending in the niche this week, news hooks, evergreen
questions people ask, and what's working for similar Shorts. If the vidIQ connector is available, use its trending and
outlier tools. Collect 5 candidates, and add `ideas.md` as candidates too.
Also run 2–3 searches for **humour that is current right now**: meme formats, catchphrases and slang trending this week on
YouTube Shorts, Instagram Reels and X (e.g. "trending meme format this week", "viral phrase <month year>", Know Your Meme's recent
entries). Note 2–3 that are still rising (not peaked or dead), what each means, and where the Bible's Humour list says it flopped before.

**b. Pick.** Score each candidate 1–5 on: hook strength · fit with the channel promise · format fit · novelty (no topic
repeated within 30 days of the log) · evidence from Insights (formats and hooks that win) · can be **shown** with 2D graphics or
simple 3D (not just talked about). Take the top score.

**c. Verify.** Check every factual claim with a search. Drop anything you can't confirm, and put the URLs in `meta.sources`.

**d. Script.** The hook lands in the first 1.5 s and frame 0 must already show it (`enter: none`, or `at: 0` with a fast pop).
One idea per scene, each with its own visual, about 2.6 spoken words per second (30 s ≈ 75 words). End on a payoff, or a line that
loops back to the start. Write it in the channel's voice. Clickbait must still be true.
Plan the visuals scene by scene (what is on screen while each line is spoken), and the comic beat: which line sets it up, which
trend it borrows, which `beat` kind and caption pay it off. Read it back: if it needs explaining, or a 20-year-old would cringe,
cut it or swap it for a plain dry reaction.

**e. Build `jobs/<id>/job.json`** from the format skeleton (see `docs/job-spec.md`). Fill in `meta` honestly
(format, topic, hook, idea_source, characters, sources, and `humour`: the trend used, the beat kind, its scene), because the review
depends on it. Write the title, description and tags per the Bible.

**f. QA loop (up to 3 rounds).** Run `python -m autopilot validate` and then `python -m autopilot frames jobs/<id>/job.json`.
**Look at every frame** with Read. Check that text is readable (no empty boxes from missing glyphs), nothing sits in the red zone,
nothing overlaps, characters are on-model, frame 0 shows the hook, Ved isn't on screen for most of it, and it doesn't look like
the last 3 videos. Also render a still in the middle of the beat (`frames --at <scene start + beat at + 0.4>`) and check the caption
card is readable and Ved's reaction face reads clearly. Fix and repeat.

**g. Render.** Run `python -m autopilot render jobs/<id>/job.json`. Check `out/render.json`: the length must be ≤ 58 s. Then pull 3–4 frames from
`out/final.mp4` with ffmpeg and look at them.

**h. Publish.**
1. Run `scripts/push_media.sh jobs/<id>/out/final.mp4 <id>`. It prints the public URL and waits until the URL serves the file.
   Exit code 2 means the URL isn't reachable. Retry once; if it still fails, stop and notify the owner.
2. Run `python -m autopilot zapier jobs/<id>/job.json` to get the upload fields.
3. Call Zapier *YouTube: Upload Video* with `connection_id` = `zapier.youtube_connection_id`, video = the URL, title, description,
   tags (list), privacy_status, category_id "27", made_for_kids "false", notify_subscribers "true", default_language and
   default_audio_language "en". Check `channelId` in the response equals `zapier.youtube_channel_id`; if not, tell the owner at once.
   Read the video id, then run `python -m autopilot budget --add upload --ref <slot id>`.
   If the call fails (an error costs 0 tasks), retry once. If it fails again, stop and notify the owner.
   Never upload twice: before a retry, check `log.md`. Use *YouTube: Find Video* (2 tasks) only if the first call timed out with no clear result.
4. Append `python -m autopilot logline jobs/<id>/job.json --youtube-id <video id>` to `channel/memory/log.md`. In `ideas.md`,
   remove the idea you used and add the 2–3 runners-up.
5. `git add jobs/<id>/job.json channel/ && git commit -m "short <id>: <title>" && git push`.

**i. Report.** Send the owner one SendUserMessage: title, link, format and hook, the joke used (one line), and why you picked it (one line).

## 3b. Manual run with the owner's one-off changes
1. Do Produce mode (sections 3a–3i) for an extra slot, with id `YYYY-MM-DD-m1`, `-m2`, and so on, so it never takes a scheduled slot.
   If the owner already gave the topic, skip research and only verify the facts.
2. Turn each of the owner's changes into **job-level** settings only:
   - topic, script or format choice: the job content;
   - look or sound tweaks: `style_override` in job.json (deep-merged over style.json for this video only);
   - voice for one video: scene or job `voice`;
   - new props or sets: inline SVG or `scene3d` inside this job.
   Never edit the backbone files to get the effect.
3. Describe the one-off changes in plain words in `meta.overrides`. They're recorded in the log, and the review
   treats that video as an experiment, not as the normal format.
4. In the report, list what was applied as one-off. Offer in one line to make any of it permanent; it only becomes permanent if the owner says so.

## 3c. Bonus slots (use every Zapier task before the reset)
1. At the very start of a bonus run (slot `b` or `c`), right after cloning and before installing models or researching, run
   `python -m autopilot budget --bonus`. If the last line is `BONUS 0`, stop at once and don't message the owner.
2. Otherwise make **one** Short for this slot with the full Produce flow (sections 3a–3i, same quality bar, different topic and
   format from today's other Shorts), with id `YYYY-MM-DD-b` or `-c`.
3. If the owner uses Zapier for anything else and tells you the "tasks used" figure from Zapier's billing page, run
   `python -m autopilot budget --sync <tasks>` and commit the ledger, so the bonus maths stays honest.

## 4. Review mode (every 7 days): 3 Zapier calls, plus an optional 4th
1. **Collect stats (1 call).** Take every video id from `log.md` for the last 28 days (skip PILOT lines). Get views, likes,
   comments and publish time in **one** call: vidIQ channel stats if that connector is available (no Zapier tasks), otherwise
   Zapier *YouTube: Make API GET Request* with the pinned YouTube connection:
   `GET https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails,status&id=<up to 50 ids>`.
   `budget --need stats` first, `--add stats` after. Never call Find Video once per video.
   Write the results to `stats/latest.json` in the format at the top of `scripts/analyze.py`, joined with format, hook and topic from the log.
2. **Pull in the owner's edits (1 call).** Zapier *Google Docs: Get Document Content* on `gdocs.bible`. Compare its text with
   `channel/memory/.bible_synced.txt` (the text as last synced). If the owner changed anything, apply those changes to
   `bible.md` (the owner's version wins, 🔒 sections included) and add a change-log line "owner edit in Google Doc".
3. Run `python scripts/analyze.py stats/latest.json`. If there are fewer than 6 videos older than 48 h, skip to step 6 with a short note.
4. Find what wins and loses by format, hook, topic cluster, length, 2D-only vs 2D+3D, and comic beat, using median views, likes per
   1k views and comments per 1k views. Manual videos with `one-off` notes are experiments: report them separately, and if one clearly
   wins, suggest it to the owner; don't adopt it yourself. Compare the top 5 with the bottom 5: what do the winners share
   (topic type, hook, first line, length, joke)? Treat any difference under ~1.5× the channel median as noise.
5. Decide changes **only in 🔄 Bible sections** of `bible.md`: shift format weights (minimum 0.1), prefer the winning hook types,
   retarget lengths, adjust title patterns, record what landed and flopped in Humour, and trial at most one new format per week
   (≤ 2 of the week's slots, built from the existing cast and style). Never change 🔒 sections; suggest it to the owner instead.
   Add change-log lines. Write a new entry at the top of `insights.md` (date, data window, findings with numbers, decisions,
   next week's experiment). Steer `ideas.md` toward what works.
6. **Sync the docs.**
   - Always (1 call): Zapier *Google Docs: Append Text to Document* on `gdocs.log_insights` with a "Week of <date>" entry:
     the week's log lines, the stats table in short, and this week's Insights entry (HTML via `python -m autopilot.gdoc`).
   - Only if `bible.md` changed this week **and** `python -m autopilot budget --spare` shows SPARE ≥ 1 (an optional 4th call):
     replace the Bible doc's body with the new text using *Google Docs: Make API Mutating Request*:
     `POST https://docs.googleapis.com/v1/documents/<id>:batchUpdate` with `deleteContentRange` (1 to the end index from step 2,
     minus 1) then `insertText` at index 1. Otherwise note "Bible changes waiting to sync" in the weekly entry and retry next week.
   - After syncing, save the Bible doc's text to `channel/memory/.bible_synced.txt`.
7. Commit and push. Send the owner a summary of 5 lines or fewer, with the two doc links.

## 5. Scheduled tasks
Created in setup with `create_trigger` (time zone Asia/Calcutta, `requires_local_device` false):
- Production slot a, daily 18:50: "Use the shorts-autopilot skill in Produce mode for today's slot `a` (IST date). Post one Short."
- Bonus slots b and c, daily 12:50 and 15:50: "Use the shorts-autopilot skill: bonus slot `<b|c>` (IST date). Check
  `budget --bonus` first and stop quietly if it is 0."
- Review, Sunday 10:20: "Use the shorts-autopilot skill in Review mode."
Each run starts fresh, so the repo (and the Google Docs) carry all the state.

## 6. Platform rules
- Everything is original: no copyrighted characters, logos, music or lyrics.
- YouTube demonetises repetitive, mass-produced content. Every video needs a real, distinct idea and fresh writing, even within a
  format. Never post near-duplicates or reposts.
- Brand-new channels do best at ≤ 3 Shorts a day; never raise `max_per_day` above 3 unless the owner asks.
- Synthetic-media disclosure is for realistic AI content. Cartoon characters don't need it. If a format ever shows realistic people or
  events, set `youtube.synthetic_media` to true in style.json and tick the matching field in Zapier if it offers one.
- Make no extra Zapier calls, and always go through the budget check. Manual runs count too: if `--need upload` says no, tell the owner
  and offer to render the video now and post it when the budget frees up.
- More regular videos a day only if the owner moves to a paid Zapier plan: then raise `zapier.plan_tasks` in style.json.
  The bonus logic scales with it automatically.

## 7. Not built yet
Instagram Reels posting. `final.mp4` is already Reels-ready (9:16), and the same media URL can feed a Zapier
*Instagram for Business: Publish Video/Reel* action once the owner has an Instagram Business account. Tell the owner if they ask.
