---
name: "shorts-autopilot"
description: "Run Sujal's automated YouTube Shorts channel The Explainer: channel setup, making and posting a code-drawn Short (research, script, render, post via Zapier), the weekly long video, or the weekly review. Use for any scheduled channel run."
---

# Shorts Autopilot: The Explainer

You run the YouTube Shorts channel **The Explainer** (@the_explainer-n3d, host Professor Ved) on your own. Every video is made
**entirely in code by you**: script, cinematic 3D shots rendered in Blender (bpy), original 2D SVG host and infographic text,
captions, Kokoro TTS voice, procedural music and SFX. No stock footage and no outside AI video or image services (the owner asked for this).

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

There are five modes. Work out which one applies:
- **Setup**: the owner asks to set up or change the channel. Interactive.
- **Produce**: a scheduled run, or "make/post a Short". Unattended.
- **Review**: every 7 days (scheduled), or "analyse the channel". Unattended.
- **Deep Dive**: the weekly long video (scheduled, Saturday), or "make a long video". Unattended. Section 3d.
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
   Then `pip install -q -r requirements.txt --break-system-packages`, `bash scripts/fetch_models.sh` (~350 MB, about 1 minute)
   and `bash scripts/fetch_blender.sh` (Blender from the repo's `deps` branch, about 10 s).
2. **Connectors**: load the Zapier tools with ToolSearch ("zapier"). Check *YouTube: Upload Video* is enabled (in a review, also
   *YouTube: Make API GET Request* and the Google Docs actions *Get Document Content* and *Append Text to Document*);
   enable missing ones with Zapier's discover/enable tools. If Zapier isn't connected at all, stop and tell the owner.
3. **Read the channel**: `channel/memory/bible.md`, the top entry of `insights.md`, `ideas.md`, and the last 30 lines of `log.md`.
   Then `channel/style.json` and `docs/job-spec.md`, and run `python -m autopilot characters`.

## 1. Consistency rules (never break these)
- **Look**: use only the palette, fonts, background and caption style in `style.json`. Don't override them per video unless the Bible's format allows it.
- **Topics: complex ideas made simple.** Economics and money, philosophy, quantum physics and big science, the human body and
  medicine, society and psychology, famous experiments, political-economic systems (capitalism, communism, how markets and
  governments work), surprising facts. The skill is making the hard thing feel easy: one concrete analogy (10 apples and 10 dollars
  = inflation), shown, not just said.
- **Even-handed:** political and economic ideas are explained neutrally (what it is, how it's meant to work, the strongest case for
  and the strongest criticism, historical facts). No parties, candidates or current elections; Ved never takes a side. Medical videos
  explain how the body works and never tell viewers what to take or do.
  Fair is not fake balance: when the evidence clearly favours one answer on a factual question (what happened, what the data
  shows, which approach did better at a stated goal), say so plainly with the numbers, the source and why, plus the context
  (better at what, where, when; a different situation can change the result). When evidence is mixed, say how strong each side's
  evidence is. Questions of values get no verdict. Stats, facts and probability, never bias.
  Give real answers, often conditional, not just "both sides": where and when it works, where it fails, and why (e.g. state
  communism failed at country scale, while shared ownership works in small, close-knit or voluntary groups such as kibbutzim,
  Hutterite colonies and co-operatives, because trust, size and choice change the result). Be equally blunt with every side:
  facts over political correctness, said with respect for people.
- **Callbacks:** mention an earlier video only when it is genuinely needed to understand this one (a real follow-up on the same
  idea). Check `log.md`; if the link isn't strong, don't mention past videos at all.
- **The look: 2D characters in a 3D world, plus 2D infographics.** Never all-3D and never all-2D. Inspiration: Rick's Clips
  (2D cartoon characters acting inside a bright 3D world), Zack D Films (clean 3D objects, soft light, depth of field) and The
  Infographics Show (bold, punchy text, panels and pacing). Ved is always 2D:
  - hook and payoff: Ved full-size in front of a blurred 3D still (a `blender` layer with `dur` 0.034) with a big headline;
  - the middle: Ved **lives inside the 3D world**, he is never just pasted over it. He walks in from the side (`keys` with
    `"walk": true`), talks to camera in close-ups ("Hey, ever wondered why..."), jumps when something surprising happens
    (`hops`), points at and reacts to props (`acting`), stands on the set's floor line with his moving shadow. Cut between
    wide / medium / close-up angles every 2–4 s (8–12 cuts in a 25–35 s video), with gentle camera pushes (`camera.keys`);
  - 2D on top: at least one flat infographic panel per video (cream card, icons, before/after numbers, arrows, built as inline
    SVG with plain-ASCII text), bold Anton headlines with `*accent*` words, counters, pop/slide entrances with a sfx each, and the
    comic beat card.
  Every explanation step gets its own shot, panel or label; something new moves on screen at least every 2–3 s; move captions
  (`caption_y`) off any object they would cover. Never childish clip-art diagrams, never a talking head explaining something we could show.
- **The town (supporting cast)**: the world is populated. Faceless townspeople (`"id": "extra"`, outfit per layer in
  `rig_args.outfit`: apron, headscarf, straw hat, fez, suit and bowler, necklace, bag...) play the roles in the story (seller,
  buyers, banker, crowd) and show feelings with body language: `happy`/`cheer` + `hops` when good news lands, `sad` (head and
  shoulders drop) and slow walks away when it backfires, `give`/`take` for trades, `shrug`. Name the recurring people in the
  job builder and keep their outfits identical in every shot. Stage everyone in depth with `autopilot/stage.py` (place by floor
  position in metres from the plate's saved camera; `walk()` paths shrink/grow with distance) and draw each set's foreground layer
  (`fg_<set>`, rendered with `still(..., only=[counter])`) between the people behind it and the people in front. Reference:
  `jobs/2026-11-08-m3/assets.py` + `build_job.py` and `docs/job-spec.md` "The town".
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
- **3D (Blender), the cheap way**: build the world from **stills**, then animate in 2D at 30 fps (smooth, minutes to render).
  The job's `assets_script` (`jobs/<id>/assets.py`, see `docs/job-spec.md` "The 3D world, cheaply" and
  `jobs/2026-11-08-m2/assets.py` + `build_job.py` as the reference) renders 2–3 sets, each from 2–3 camera angles (wide / medium /
  close-up plates, 1080x1920), plus every prop as a transparent cut-out (`still(..., transparent=True, crop=True)`). Props then
  drop, bounce, fly, spin and flip as `image` layers with `keys`. Sets are bright, colourful little worlds (market, lab, street,
  body interior, bank) or a moody studio when the topic needs drama; warm sun/key light, soft shadows. Real objects stand in for
  abstract ideas; reuse and extend the props in blendkit; textures are drawn with PIL in `assets/tex/make_textures.py`, always
  fictional designs. Open every plate and cut-out with Read before using it, and re-render only what's wrong (`BK_SKIP_EXISTING=1`
  after deleting those files). Budget: about 6–10 min of Blender per video. Animated `blender` shots (about 7 s per frame) only for
  a moment that truly needs a moving 3D camera; the low-poly `scene3d` layer only for quick crowds or maps.
- **Look references**: `docs/sheets/professor_ved_character_sheet.png`, `vast_world_style_guide.png` and `vast_world_3d_guide.png`.
  Check new props and sets against them, and rebuild them with `scripts/build_sheets.py` whenever the cast changes.
- **Formats**: each video uses exactly one format from the Bible, starting from its skeleton in `jobs/_templates/`:
  big-question, myth-bust, scale-shock, and (added by the owner 2026-11-13, in addition, nothing removed) what-if thought
  experiments, frontier "how could it really work" explainers (teleportation, star travel, CERN), wild true stories behind
  discoveries and thinkers, and occasional deep-question philosophy. Follow the Bible's weights (about 1 in 3 Shorts uses the new
  ones; deep-question at most about weekly). In these formats every claim carries an on-screen honesty tag (PROVEN / THEORY /
  R&D / SPECULATION), Ved says out loud where known science ends, and speculation is never presented as fact. Fill
  `meta.claims` with each claim, its tag and its source.
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
Slots (live times, chosen for the US-majority audience and >= 5 h apart; each run starts ~55 min earlier, at 22:36 / 16:36 /
04:06, because making a Short takes 40-50 min): `a` ~23:30 IST (the regular daily Short), `b` ~17:30 and `c` ~05:00 IST (bonus: every day during the trial, otherwise only near the
end of the Zapier billing cycle, section 3c). The slot id is `YYYY-MM-DD-<slot>`, using the IST date. Never post the same format three
days in a row, nor the same format twice on one day. If `log.md` already has that id, or `jobs/<id>/` exists in the repo, the slot is done. Stop.
**Budget first:** run `python -m autopilot budget --need upload` before researching. If it exits 3, don't make the video;
send the owner one SendUserMessage saying today's Short was skipped because the Zapier budget is used up, and stop.
For slot `a`, pass `--ref <slot id>`: exit code 4 means today's long video already took this slot (free plan). Stop quietly.

**a. Research (4–8 searches, send them in parallel).** Look at what is trending in the niche this week, news hooks, evergreen
questions people ask, and what's working for similar Shorts. If the vidIQ connector is available, use its trending and
outlier tools. Collect 5 candidates, and add `ideas.md` as candidates too.
Also run 2–3 searches for **humour that is current right now**: meme formats, catchphrases and slang trending this week on
YouTube Shorts, Instagram Reels and X (e.g. "trending meme format this week", "viral phrase <month year>", Know Your Meme's recent
entries). Note 2–3 that are still rising (not peaked or dead), what each means, and where the Bible's Humour list says it flopped before.

**b. Pick.** A new topic every run (owner's rule): it must be at least one of these, and ideally two or three at once:
- **Unique**: a fresh topic or a fresh angle that few Shorts have done (check YouTube search results for it in your research);
- **Trending**: tied to something people are talking about or searching this week (news, a launch, a discovery, a viral debate);
- **Viral-shaped**: a famous "impossible" subject made shockingly easy ("rocket science in 40 seconds", "quantum physics with
  two apples"), the kind people share because they finally got it.
Drop any candidate that is none of the three. Then score the rest 1–5 on: hook strength · how many of the three it hits · fit
with the channel promise · format fit · novelty (no topic repeated within 30 days of the log) · evidence from Insights (formats
and hooks that win) · can be **shown** with 2D graphics or simple 3D (not just talked about). Take the top score, and note in
`meta.idea_source` which of unique / trending / viral it hits. The owner's example topics in `ideas.md` are inspiration for the
kind of video, not a to-do list.

**c. Verify.** Check every factual claim with a search. Drop anything you can't confirm, and put the URLs in `meta.sources`.

**d. Script.** The hook lands in the first 1.5 s and frame 0 must already show it (`enter: none`, or `at: 0` with a fast pop).
One idea per scene, each with its own visual, about 2.6 spoken words per second (30 s ≈ 75 words); Shorts are 25-35 s
(65-90 words), with the most surprising fact in the first 2 s and no warm-up lines. Frame money topics around the viewer's own
wallet ("Why does the bank pay YOU..."), never as an abstract term. End on a payoff, or a line that
loops back to the start. Write it in the channel's voice. Clickbait must still be true.
Plan the visuals scene by scene (which 3D shot and which infographic text is on screen while each line is spoken; the analogy
object for every abstract idea), and the comic beat: which line sets it up, which
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

**g. Render.** Run `python -m autopilot render jobs/<id>/job.json` (assets are cached, so this is 2–3 min; if the job has animated
`blender` shots, run it with `nohup ... > /tmp/render.log 2>&1 &` and poll until it prints `done`). Check `out/render.json`: the
length must be ≤ 45 s (aim for 25-35 s: viewers stay ~10-19 s on average). Then pull 3–4 frames from `out/final.mp4` with ffmpeg and look at them.

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
4. **Thumbnail** (Shorts too: it shows in search, on the channel page and in suggestions, not in the swipe feed). During the trial,
   or if `python -m autopilot budget --spare` shows SPARE >= 1: add a `thumbnail` to job.json in the house look (the long-video
   rules in 3d step 6, vertical): `bg` = a clean plate of the set (no text, no Ved) with the key townspeople and props, `fg` = Ved
   big (about `h` 0.95, `y` 0.93, `x` 0.5, a strong face such as "surprised", `acting: "none"`, `talk: false`, `ground: false`)
   plus one key prop, and a 1-3 word title with one *accent* word. `python -m autopilot thumbnail jobs/<id>/job.json` writes a
   1080x1920 out/thumbnail.jpg; Read it, then `KEEP=8 scripts/push_media.sh jobs/<id>/out/thumbnail.jpg <id>-thumb` and Zapier
   *YouTube: Update Video Thumbnail* (video_id, thumbnail = that URL), then `budget --add thumb --ref <slot id>`. Skip it quietly
   when there's no spare budget.
5. Append `python -m autopilot logline jobs/<id>/job.json --youtube-id <video id>` to `channel/memory/log.md`. In `ideas.md`,
   remove the idea you used and add the 2–3 runners-up.
6. `git add jobs/<id>/job.json channel/ && git commit -m "short <id>: <title>" && git push`.

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

## 3d. Deep Dive mode (weekly long video, 16:9)
Follows the Bible's "Deep Dive" format; `jobs/2026-11-11-longpilot` (the pilot) is the reference build.
Slot id `YYYY-MM-DD-L` (IST date). If `log.md` already has it, stop.
1. Section 0, then `python -m autopilot budget --need upload` (exit 3: tell the owner the long video was skipped, and stop).
2. **Topic.** Prefer the idea behind the best recent Short (log + last review), taken much deeper; otherwise research as in 3a
   (6-10 searches). Verify every claim (3c), put the URLs in `meta.sources` and name the main sources in the description.
   Where experts disagree, give both views briefly.
3. **Script.** 5-8 min (about 750-1100 words), 5-8 chapters. Cold open with a concrete object or question and a promise of the
   payoff; each chapter is a small story acted out by Ved and the townspeople; 2-3 comic beats (one per ~2 min); a one-line payoff;
   a short subscribe outro. Plan a new shot, cut or panel every 3-6 s.
4. **Build** `jobs/<id>/assets.py` (sets at 1920x1080, reuse and extend the props) and `build_job.py` from the pilot's helpers;
   `"kind": "long"`, `chapters`, `thumbnail`. See docs/job-spec.md "Long videos".
5. **QA.** Preview sets (`BK_PREVIEW=1`, look at every plate), then `frames` for every scene (look at all of them: framing, panels
   and text inside the frame, people placed in depth, nothing cut off). Fix and repeat. Then render the full sets with `nohup`
   and poll, then `nohup python -m autopilot render ...` and poll (20-40 min). Check out/render.json: `duration` <= 720 and
   `size_mb` <= 90; pull 5-6 frames from final.mp4 and look at them.
6. **Thumbnail** (owner-approved look, always): the world blurred and colour-graded behind (two-colour gradient tint + a warm glow
   behind Ved), Ved big and sharp right under the title with a strong face (surprised, shocked, side-eye), one or two key props
   sharp beside him, and a huge 1-3 word title in heavy white sans with one *accent* word ("JUST *PAPER?*"); no watermark, no small
   text. Build it as `thumbnail` with `bg`/`fg` layers (docs/job-spec.md, the pilot's job.json is the reference), run
   `python -m autopilot thumbnail jobs/<id>/job.json`, Read out/thumbnail.jpg and iterate until it reads at a glance on a phone.
7. **Publish.** `BRANCH=media-long KEEP=6 scripts/push_media.sh jobs/<id>/out/final.mp4 <id>` and the same for
   `out/thumbnail.jpg` as `<id>-thumb`. `python -m autopilot zapier jobs/<id>/job.json` (description includes the chapters),
   then upload exactly as 3h step 3 (pinned connection, check `channelId`) and `budget --add upload --ref <id>`.
   Thumbnail: during the trial, or if `python -m autopilot budget --spare` shows SPARE >= 1, call Zapier *YouTube: Update Video
   Thumbnail* (video_id, thumbnail = the thumb URL) and `budget --add thumb --ref <id>`. If YouTube refuses because the channel
   isn't phone-verified, or there's no budget, send the owner the thumbnail file to set in YouTube Studio.
8. Log (`logline` marks it LONG), commit, push, and report as 3i with the link and the chapter list.

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
   Long videos (LONG in the log) are judged separately: views, likes and comments per 1k views, and, when the stats call can
   get it, average view duration; compare them only with each other, and note which Short topics they grew from.
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
- Production slot a, daily 22:36 (live ~23:30): "Use the shorts-autopilot skill in Produce mode for today's slot `a` (IST date). Post one Short."
- Bonus slots b and c, daily 16:36 and 04:06 (live ~17:30 and ~05:00): "Use the shorts-autopilot skill: bonus slot `<b|c>` (IST date). Check
  `budget --bonus` first and stop quietly if it is 0."
- Review, Sunday 10:20: "Use the shorts-autopilot skill in Review mode."
- Deep Dive, Saturday 19:56 (live ~21:30): "Use the shorts-autopilot skill in Deep Dive mode (slot `L`, IST date). Post one long video."
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
