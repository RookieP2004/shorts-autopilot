# shorts-autopilot

Code-made YouTube Shorts. Claude writes a `job.json`, renders it here (2D SVG characters, motion
graphics, captions, Kokoro AI voice, procedural music and SFX), publishes the file to this repo's
public `media` branch, and posts it to YouTube through **Zapier**. The channel bible, video log,
insights and idea backlog live in **Google Docs**.

```
channel/style.json     locked look + sound (palette, fonts, captions, voice, music)
channel/docs.json      links to the 4 Google Docs (bible, log, insights, ideas)
characters/ved/        Professor Ved: make.py (one base drawing -> every pose) + character.json
assets/bg/             The Vast World sets: study, world, cosmos (make_backgrounds.py)
docs/sheets/           character model sheet, look & lighting bible, 3D guide (scripts/build_sheets.py)
autopilot/three.py     simple 3D layer: low-poly scenes, faceless people, camera moves (no GPU)
jobs/<id>/job.json     one video (kept as a record)
jobs/_templates/       one skeleton per format
docs/job-spec.md       job.json reference
docs/google-docs-templates.md   what goes in each Google Doc
scripts/push_media.sh  publish a video to the media branch -> public URL for Zapier
scripts/analyze.py     weekly stats summary
```

## Commands
```bash
pip install -r requirements.txt && bash scripts/fetch_models.sh      # needs ffmpeg + libcairo
python -m autopilot validate jobs/<id>/job.json
python -m autopilot frames   jobs/<id>/job.json        # stills, YouTube UI area shaded red
python -m autopilot render   jobs/<id>/job.json        # -> jobs/<id>/out/final.mp4
scripts/push_media.sh jobs/<id>/out/final.mp4 <id>     # -> https://raw.githubusercontent.com/<you>/<repo>/media/<id>.mp4
python -m autopilot zapier   jobs/<id>/job.json        # fields for Zapier: YouTube > Upload Video
python -m autopilot logline  jobs/<id>/job.json --youtube-id <id>   # line for the Shorts Log doc
```

## One-time setup
1. **GitHub**: push this folder to a **public** repo (Zapier downloads each video from its `media` branch).
   There are no secrets in it. The branch only ever holds the newest 6 videos as a single commit.
2. **Zapier**: in claude.ai, go to Settings → Connectors → add **Zapier** and sign in. In Zapier, connect your
   YouTube channel's Google account and enable these actions: **YouTube: Upload Video**, plus any YouTube
   "Find Video"/"API Request" action for stats. Set them to run without asking each time, or scheduled runs will stall.
   The channel is tuned for Zapier's **free plan (100 tasks/month)**. Each successful Zapier call costs 2 tasks, so:
   1 Short a day (≤31 uploads = 62 tasks) + 1 stats call a week (≤5 = 10 tasks) = **≤72 tasks**, leaving ~28 for
   retries, the pilot and a few manual videos. `python -m autopilot budget` counts calls in
   `channel/zapier_ledger.json` over a rolling 31 days and refuses to go past 48 calls (96 tasks).
   Google Docs go through the claude.ai Google Docs/Drive connectors, never Zapier, so they cost no tasks.
   **No wasted tasks:** set `zapier.cycle_day` in style.json to the day of the month your Zapier usage resets
   (Zapier → Settings → Billing). Then `budget --bonus` works out the spare tasks before the reset, and the
   bonus slots (12:50 and 15:50 IST) post up to 2 extra Shorts a day in the last week or so, landing on exactly 100.
   If you use Zapier for anything else, run `budget --sync <tasks used on Zapier's billing page>` to keep the ledger honest.
   **Trial:** while `zapier.trial_until` is in the future, the budget uses `trial_tasks` (1,000) and posts the full
   3 Shorts a day; trial uploads don't count against the free plan afterwards. Don't add a card during the trial,
   and Zapier drops the account to Free automatically when it ends.
   On a paid plan, raise `zapier.plan_tasks` in style.json.
3. **Google Docs**: add the **Google Docs** and **Google Drive** connectors in claude.ai (not Zapier's Google Docs
   actions, which would use up the free task budget). Setup creates the 4 docs and writes their links to `channel/docs.json`.

Fonts: Anton, Poppins and Bebas Neue (SIL OFL, fonts/OFL.txt). Voice: Kokoro-82M (Apache-2.0).
