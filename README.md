# shorts-autopilot

Code-made YouTube Shorts: Claude writes a `job.json`, GitHub Actions renders it
(2D characters, motion graphics, captions, AI voice, procedural music) and uploads it to YouTube.
Daily stats land in `data/stats/`. Everything visual and audio is generated in code; there is no stock footage and no paid AI video service.

```
channel/bible.md       what the channel is (identity, cast, formats, rules)
channel/style.json     locked look + sound (palette, fonts, captions, voice, music)
characters/<id>/       SVG poses + character.json (voice, default size)
jobs/<id>/job.json     one video  ->  push to main  ->  rendered + uploaded
data/videos.jsonl      log of everything posted (written by the workflow)
data/stats/latest.json channel + per-video stats (daily workflow)
data/insights.md       weekly review notes
docs/job-spec.md       job.json reference
```

## Local use
```bash
pip install -r requirements.txt && bash scripts/fetch_models.sh   # needs ffmpeg + libcairo
python -m autopilot validate jobs/example/job.json
python -m autopilot frames   jobs/example/job.json      # stills with the Shorts UI area shaded
python -m autopilot render   jobs/example/job.json      # -> jobs/example/out/final.mp4
```

## One-time setup (about 20 minutes)
1. **Repo**: push this folder to a new **private** GitHub repo.
2. **Google Cloud**: create a project → enable *YouTube Data API v3* and *YouTube Analytics API*.
3. **OAuth consent screen**: External, add your Google account as a test user, then press
   **Publish app → In production**. (In "Testing" mode the refresh token dies after 7 days.)
   An unverified app is fine for your own channel; you'll click through a warning once.
4. **Credentials** → Create OAuth client ID → *Desktop app* → download `client_secret.json`.
5. On your computer, in this folder:
   ```bash
   pip install google-auth-oauthlib google-api-python-client
   python -m autopilot auth client_secret.json
   ```
   Sign in with the Google account that owns the channel. It prints three values.
6. GitHub repo → Settings → Secrets and variables → Actions → add
   `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
7. Test: Actions → *publish* → Run workflow → job `jobs/example/job.json` (it uploads as **private**).
8. **Compliance audit** (needed for public auto-posting): YouTube keeps every API upload
   from an un-audited project **private**. Submit the *YouTube API Services Audit and Quota
   Extension* form for this project. Until it's approved, videos upload private and the run tells
   you; you make them public in YouTube Studio (or turn on the Chrome fallback in the skill).

Fonts: Anton, Poppins and Bebas Neue (SIL OFL, see fonts/OFL.txt). Voice: Kokoro-82M (Apache-2.0).
