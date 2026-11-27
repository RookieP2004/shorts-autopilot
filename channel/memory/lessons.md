# Lessons: mistakes that must never repeat

Every run reads this file at the start (skill section 0). Each entry: what went wrong, the real cause, and the rule now in
force. When a run hits a new problem, it adds an entry here in the same shape, fixes the tooling so it can't recur, and
tells the owner what it learned. The owner's words (2026-11-26): "learn from problems like this, they should not repeat".

## 2026-11-13: Shorts lost their thumbnails
- **What:** three Shorts showed YouTube's auto frame instead of our thumbnail.
- **Cause:** the thumbnail was set while YouTube was still processing the new video, so YouTube replaced it.
- **Rule:** set the thumbnail at least 10 minutes after the upload, in the same session (skill 3h step 4).

## 2026-11-21: "no video last night"
- **What:** the Saturday evening Short didn't post.
- **Cause:** by design: on the free plan the weekly long video replaces Saturday's Short. Nobody told the owner.
- **Rule:** when a slot is skipped on purpose, the report or the next message says so in one line.

## 2026-11-23: the daily Short was a step back from the hand-made one
- **What:** the 11-23 Short used the old flat style while the 11-22 Wi-Fi Short had set a far higher bar.
- **Cause:** new owner rules were written down as words, but the daily pipeline had no time and no check to deliver them,
  so a run could tick them off on paper.
- **Rule:** every owner rule gets a tool or an automatic check, not only a sentence. The render gate (`gate: PASS/FAIL`)
  checks the bar; never post on a FAIL.

## 2026-11-24 and 2026-11-26: YouTube upload blocked ("429", then "throttled without retry")
- **What:** the Short was made but not posted; the owner had to ask.
- **Cause (ours, not the Zapier account, which was at 32/100):** every upload used a `raw.githubusercontent.com` link.
  The first upload with it failed (429), and the run kept retrying the exact same request, so Zapier started blocking
  that identical failing request. The same file from a second link (`github.com/.../raw/...`) uploaded at once.
- **Rule:** never repeat a failing Zapier request unchanged. On 429 / "throttled", switch at once to the second link that
  `push_media.sh` prints as `ALT`; if that fails too, wait 5 minutes and try once more, then message the owner with the
  video link and the ready-to-paste title and description. A Zapier error is never a reason to end a run quietly.

## 2026-11-25: the Short was rendered at 08:16 but never posted
- **What:** the run finished the video, then ended without uploading.
- **Cause:** the run had been told to wait until 13:25 before uploading. A run can't idle for hours; it just ended.
- **Rule:** upload in the same run as soon as the gate passes. Never schedule a later step inside a run.

## 2026-11-26: the posted Short had no thumbnail for hours
- **What:** after a by-hand upload at 18:06, the thumbnail was only set at 22:06, once the owner asked.
- **Cause:** the 10-minute thumbnail wait was skipped when posting outside the normal run, then forgotten.
- **Rule:** any upload (scheduled, manual or a rescue) is not finished until the thumbnail is set 10-15 minutes later and
  the Reel is handled. `python -m autopilot postcheck <id>` must print `POSTCHECK OK` before the final report.

## 2026-11-27: the RS-01 receipt showed "₹NaN" in the first render (caught before posting)
- **What:** the receipt look printed ₹NaN for every amount.
- **Cause:** amounts were passed as strings ("$8") and the currency prop was left at its ₹ default.
- **Rule:** RS-01 `items` amounts are plain numbers and `currency` is set explicitly ("$" for US-facing Shorts); always pull
  a frame from the look scene before posting.

## 2026-11-22 to 11-27: posting time set from the wrong data
- **What:** Shorts were moved to ~13:30 IST, which the audience heatmap shows is one of the quietest times for our viewers.
- **Cause:** the time was chosen from "views by posting hour", which mixed the first week's strongest topics with the hour.
- **Rule:** choose posting times from YouTube Studio's "When your viewers are on YouTube" heatmap (audience activity), not
  from a few videos' view counts; re-check it in the weekly review.
