# shorts-autopilot

Code-made YouTube Shorts. Claude writes a `job.json`, renders it here (2D SVG characters, motion
graphics, captions, Kokoro AI voice, procedural music and SFX), publishes the file to this repo's
public `media` branch, and posts it to YouTube through **Zapier**. The channel bible, video log,
insights and idea backlog live in **Google Docs**.

```
channel/style.json     locked look + sound (palette, fonts, captions, voice, music)
channel/docs.json      links to the 4 Google Docs (bible, log, insights, ideas)
characters/<id>/       make.py (one base drawing -> every pose) + character.json (voice, size)
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
   Each Zapier action uses 2 tasks, so 2 Shorts/day needs a paid Zapier plan (the free plan is 100 tasks/month).
3. **Google Docs**: add the **Google Docs** and **Google Drive** connectors (or enable Zapier's Google Docs
   actions). Setup creates the 4 docs and writes their links to `channel/docs.json`.

Fonts: Anton, Poppins and Bebas Neue (SIL OFL, fonts/OFL.txt). Voice: Kokoro-82M (Apache-2.0).
