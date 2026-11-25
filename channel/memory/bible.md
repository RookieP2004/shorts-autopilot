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
- **Facts over balance (owner, 2026-11-13):** fair is not the same as pretending everything is equal. When the evidence clearly
  favours one answer on a factual question (what happened, what the data shows, which approach did better at a stated goal), Ved
  says so plainly, with the numbers, the source and why. He always adds the context: better *at what*, *where* and *when*, because
  a different situation can change the result. Where the evidence is mixed, he says how strong each side's evidence is. Questions
  of values (what is fair, what people should want) get no verdict; the viewer decides. Stats, facts and probability, never
  bias, and still no current parties, candidates or elections.
- **Give real answers, often conditional (owner, 2026-11-13):** don't stop at "this side vs that side". Say where and when
  something works, and where it doesn't, and why. Example: state communism failed at country scale (the evidence is clear), but
  shared ownership does work in small, close-knit or voluntary groups (kibbutzim, Hutterite colonies, co-operatives like Amul or
  Mondragon, group buying), because trust, size and choice change the result. The answer is the conditions, backed by data.
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
- **Night set: the second mood 🔒 owner-approved 2026-11-16 ("I think this one is good"; reference: `jobs/2026-11-16-n`).** The bright town
  stays the default. Dark-files, scams, money traps and big reveals may use `"look": "night"`: near-black navy set, ONE hard
  spotlight from above, a coloured rim light, shallow focus, slight Dutch tilt on hero shots (`blendkit.night_set`, `dutch`).
  Ved and the townspeople are still there and get the same rim light. Graphics in this mood: hud number chips that tick, a
  running equation bar ending in the reveal, step trackers, rubber-stamp verdicts, option cards that get a red cross or green
  tick, a glossy phone with a fictional live screen (chat, tips list, pay-now countdown, lock screen), crowds as data (a big number
  as thousands of tiny figures on the floor, split/tinted/faded to do the maths), 3D node trees, cash bursts. Captions switch to
  the highlight mode (sentence case, the spoken words in a thin selection box). Colour meaning is fixed inside a video:
  green = survives/true, red = scam/danger, gold = money, blue = neutral data. Money is always fictional ("NOT REAL MONEY"),
  apps are always fictional (no real logo or layout). Scam topics may end on the viewer's lock screen + "Comment YES or NO".
  Learned from a reference Short (2026-11-16): techniques only, never that creator's layouts, wording or assets.
- **🔒 Mix, never replace (owner, repeated 2026-11-15/16: "integrate, mix, match, modify, not replace").** Every new style
  reference or toolkit is ADDED to what the channel already has, adapted to fit it. Ved, the townspeople, the bright town, the
  cream infographic cards, the house captions, his voice and the comic beat always stay. Each video mixes old and new pieces
  that suit its topic (e.g. a cream card in one beat, a ticking hud chip in the next); a new piece never wipes out an old one.
- **🔒 Mix styles inside every Short (owner, 2026-11-22: "Permanent rule that you mix the styles").** No Short uses one
  style only: each cuts between at least three visual styles that fit its beats (Ved + townspeople in the 3D town, a 3D
  mechanism shot from Cutaway or Blender, cream cards / hud chips, Reelsmith looks, motion clips, night set, case-file
  pieces). Ved comes and goes between them. New shot every 2-4 s; one continuous move only where travel is the point.
- **🔒 Versatility (owner, 2026-11-22: "this is a ADHD person yt, make it change styles... the only constant is me the person in
  white dress... versatility").** Every Short changes Ved's role (teacher, project lead, friend, enthusiast, hacker, guide,
  mayor, planner, city planner, detective, anchor, scientist, chef, commentator, host, captain, historian, inventor, judge,
  magician, time traveller and more; no role twice within 10 videos), the way it explains (analogy, experiment, myth vs fact,
  story, build, scale zoom, versus, what-if, quiz, countdown, timeline, inside the machine, debate, case file) and the art
  styles it mixes. The role lives in the set, the props, his words and the framing; Ved's drawing, white shirt and voice
  never change. `python -m autopilot variety` suggests a fresh combination; the log records role / explain / styles.
  Wardrobe accents (owner, 2026-11-22: "he can sometimes change his look also, like leather jacket, goggles... only when
  needed, not always and not in full videos"): one or two pieces (jacket, blazer, goggles, sunglasses, hard hat, headset,
  cap, sash, scarf, badge) for a scene or two when the role calls for it; he always still reads as Ved.
- **🔒 Real reference photos (owner, 2026-11-22: "use the real photo of that incident... just to give reference, like a stamp in
  some shot, a click photograph, a sticky note").** For real incidents, places, objects and documents: a real photo as a
  small accent (polaroid, stamp, sticky note, clipping) in the shot that talks about it, one to three per Short. Only public
  domain / CC0 / CC BY files from Wikimedia Commons, credited in the description (`autopilot refphoto`). Never people's faces
  (a name card, their date, invention or place instead), never graphic or victim images, never logos.
- **Motion & graphics standard for EVERY Short (owner, 2026-11-16: "take notes from these for your normal shorts also").**
  The night pilot's graphics are now house graphics in the bright town too (only the night lighting, rim light and highlight
  captions stay night-only; town captions are unchanged). In every Short:
  - numbers never just appear: a `hud` chip or a cream card ticks to the value (eased count; mix both across a video), a running `eqbar` builds the maths step by step
    and ends on the answer in the accent colour; a number of people is shown as a `crowd` on the set floor that splits, tints,
    fades or glows to do the maths (with contact shadows and outlines in daylight);
  - steps and lists build one at a time with the narration (`tracker` circles tick green, `nodes` trees grow, `optcard` choices
    get a green tick or red cross); verdicts land as a `stamp` with a thud;
  - every entrance is eased with a little overshoot (pop / rise / slam) and has its own sfx; nothing important is static for
    more than 1-2 s; the camera keeps moving (slow push or pull, `push` cuts between beats of the same idea);
  - phones, apps and screens are live (`phone` layer: messages pop in, timers tick, it turns in 3D with a light sheen);
    money moments get a `burst`; all money and apps fictional;
  - fixed colour meaning inside a video: green = true / survives, red = wrong / danger, gold = money, blue = neutral data.
  These sit with (never replace) Ved, the townspeople, the cream infographic cards and the comic beat.
- **Case-file pieces (2026-11-18, DEMO `jobs/2026-11-18-dossier`, awaiting owner OK before public use).** Learned (not copied)
  from a reference documentary: a noir desk cut by warm venetian-blind light (`blendkit.noir_desk`, `blinds`), real-looking
  evidence props (SIM card, fictional papers with red rows, gold envelope, glass cloche), dot-matrix labels that decode or type
  in (`dottext`), big serif numbers with lining figures (`bignum`), date + place stamps (`dateline`), numbered takeaways
  (`tipnum`), day tiles (`tiles`), a sweeping clock (`clock`), gold route arcs between city dots (`flows`, never a country
  outline: Indian map rules), and a `blinds` light overlay that gives any shot the look. Mixed in, never replacing: Ved is in
  the case-file shots (close, under the same stripes), bright town beats stay, house captions and the comic beat stay. Best
  homes: the weekly long documentary and Dark Files / scam Shorts; single beats (a dateline, a bignum) can appear in any video.
- **Long documentary recipe (sample `jobs/2026-11-18-doc`, 2026-11-18, awaiting owner OK).** Fast pace: a new shot every
  3-5 s, every shot moving (push-in, drift, a clip, a counter); a cold open that starts mid-story with a dateline, a kinetic
  title slam, then Ved introduces the case on his town set; chapters with chapter cards; each chapter mixes: Blender sets
  (town or night, Ved and townspeople walking in), case-file desk shots under blind light (dateline, dottext, tiles, quotes
  with a source tag), motion clips (FlowDiagram of cream cards for mechanisms, NumberSlam for the big figures, Stack3D /
  Hero3D globe for scale and routes), night verdicts (optcards with crosses, stamps), the comic beat, a numbered takeaway
  (tipnum) and a "Next:" kinetic title to pull into the next chapter. Whip / push / dip transitions; music cues per chapter.
- **Reference video (owner-approved, 2026-11-08):** `jobs/2026-11-08-m3` ("Why can't countries just print more money?",
  youtu.be/QFhXI3hT9Ik). This is the quality bar and the house style: every new video should look at least this alive, in its own
  new world and story.

- **🔒 The bar (owner, 2026-11-23).** The Wi-Fi Short (`jobs/2026-11-22-m1`) is the minimum, not a one-off: real moving 3D
  (>= 8 s), a new shot every 2-4 s, Ved coming and going, at most 2 text pieces on screen besides 2-word captions, the role
  visible on screen, voice-first sound. The render gate (`gate: PASS/FAIL`) checks it; never post on a FAIL. Runs start
  ~6 h before posting to make room for the 3D. The bar is quality, not a template: all the owner's other rules (style mix,
  versatility, lanes, wardrobe, reference photos, sound, humour) still apply and the gate checks the style mix and the
  variety choices too. Match the Wi-Fi Short's polish; never copy its look.

## 4. Cast 🔒
| id | name | role | personality | voice | poses |
|---|---|---|---|---|---|
| ved | Professor Ved | host and explainer | about 25, sharp, calm, quietly funny; white shirt, top button open, sleeves rolled | Kokoro bm_lewis, speed 1.0, en-us (owner's nearest voice, since 2026-11-21; was bm_george) | idle, warm, serious, explain, point, think, welcome, surprised, crossed + reaction faces deadpan, side_eye, smirk |

Rule: characters are made only by `characters/<id>/make.py`. Colours, proportions and voice never change. Exception: Ved's
occasional wardrobe accents (section 3, Versatility), drawn by make.py on top of him, for a scene or two only.

## 5. Sound 🔒
- **🔒 Dynamic, story-first sound (owner, 2026-11-22: "explaining is the main thing... the sound effect doesn't pile up too much
  and become noise... volume up, volume lower the voice and sound effect as you like but according to need of video").**
  The listener must always follow the explanation. Levels move with the moment: the score dips under the voice and rises in
  pauses; small texture sounds nearly vanish under speech; story hits keep their punch, ideally in a pause. One effect at a
  time, at most 3 in any 2 s, fewer is better. Any level can go up or down per video when the story needs it.
- Voice: bm_lewis, en-us, speed 1.0 (style.json / character.json). Owner, 2026-11-21: "use my audio... similar sound of my audio to create my videos". Chosen offline as the nearest of the 54 Kokoro voices to the owner's own recording (speaker likeness 0.876 vs 0.815 for the old bm_george; `scripts/voice_match.py`). Ved speaks in this voice in every video from now on.
- Music signature: ambient, D dorian, 78 bpm, seed 21, ducked under the voice, loudness -14 LUFS.
- SFX meanings: pop = new item, whoosh = scene change, ding = payoff/CTA, boom = big reveal, scratch/crickets/wah = comedy beats only.

## 6. Formats 🔄
| format | weight | length | structure | hooks |
|---|---|---|---|---|
| big-question | 0.14 | 25-35 s | Ved asks, question on screen at frame 0 → the mechanism as full-screen 2D/3D visuals (voice-over) → Ved reaction beat → payoff that answers it | question |
| myth-bust | 0.19 | 20-30 s | "MYTH:" headline + Ved deadpan → the truth shown as visuals/evidence (voice-over) → why the myth exists | myth-bust |
| scale-shock | 0.13 | 20-30 s | huge number counting up at frame 0 → make it visible in full-screen 3D (voice-over) → a comparison the viewer feels | number-shock |
| what-if | 0.08 | 30-40 s | "WHAT IF...?" at frame 0 → the real science it starts from (PROVEN tag) → play it out step by step in the town, each leap tagged THEORY or SPECULATION → the surprising consequence → what it means for us today | what-if |
| frontier | 0.08 | 30-40 s | "HOW COULD WE REALLY...?" (teleportation, interstellar travel, fusion, CERN) → what already works today (PROVEN) → what the best current research is trying (R&D, with the lab or experiment named) → what is still missing → how far away it really is | question |
| wild-story | 0.07 | 30-45 s | a true, crazy story behind a discovery, experiment or thinker, told as a mini-drama with the townspeople as the cast → the twist → what it taught us | story |
| deep-question | 0.05 | 35-45 s | occasional philosophy ("Are humans a kind of AI?", "Can communism actually work?", "Are your facts real or propaganda?") → the strongest answers on each side, fairly → a thinking tool the viewer can use → Ved leaves the final call to the viewer | question |
| dark-files | 0.08 | 30-45 s (and Deep Dives) | a hidden economy or crime world (drug markets, cartels, mafias and the underworld, hawala, money laundering, gambling, smuggling, illegal trades) → one true case as a mini-drama → how the system really works, at the level of a news documentary → where it touches your everyday world (prices, banks, sport, phones, elections) → what it costs people and how it ends for those involved → what actually works against it (the evidence) | story / number-shock |
| build-it | 0.12 | 30-40 s | "HOW TO BUILD THE PERFECT...?" (soldier, fighter, athlete, a human with four arms, a city on Mars, an unsinkable ship) → the design brief → one upgrade per shot from real science (training, genetics, biology, tech), each with its cost and an honesty tag → the trade-off nobody escapes → the closest real thing today | build-it / what-if |
| fiction-made-real | 0.06 | 30-40 s | "COULD <A FAMOUS FICTIONAL WORLD OR POWER> BE REAL?" (a wardrobe portal to another world, dragons, invisibility, flying carpets, a hollow Earth) → what the story asks of physics or biology → the real science that comes closest (PROVEN / THEORY / R&D) → where it breaks → the coolest real thing that does part of it | what-if |

**Added 2026-11-13 by the owner (additions only; nothing above changes):** what-if thought experiments, frontier
"how could it really work" explainers, wild true stories from science and philosophy, and occasional philosophy questions.
They keep the channel promise (complex ideas made simple) and the same look, cast and town.
The owner's topics (IQ 500, the perfect athlete, teleportation, CERN, "are humans AI?", communism, propaganda, spectrum) are
examples of the kind of video, not a to-do list: find new topics of these kinds every day.
- **Honesty tags:** these formats mix fact and imagination, so every claim gets a small on-screen tag: PROVEN (established,
  sourced), THEORY (serious science, not settled), R&D (being worked on now; name the lab or project), SPECULATION (our own
  what-if step). Ved says out loud where known science ends ("From here on, we're guessing."). Never present speculation as fact.
- **Grounded what-ifs:** start from the real thing (e.g. IQ is a ranking scale with mean 100 and SD 15, so "IQ 500" isn't a
  real score, then explore what a far smarter brain would need: energy, size, wiring). No medical or training advice.
- **Philosophy and politics:** the even-handed rule applies in full: each side's strongest case, the main criticism, historical
  facts, no verdict on contested questions, no current parties or candidates. "Propaganda" videos teach how to check a claim
  (sources, incentives, evidence), never who to distrust.
- **Topic rule (owner, 2026-11-13), all formats:** a new topic every video, and each must be unique (fresh topic or angle),
  trending (people are talking about or searching it this week) or viral-shaped (a famous "impossible" subject made shockingly
  easy, like rocket science in 40 seconds), ideally two or three at once.
- Mix: about 1 in 3 Shorts uses the new formats; deep-question at most about once a week. The review tunes the weights.
- **🔒 Topic spread (owner, 2026-11-22: "this is an ADHD person's channel... from how a scale works to how galaxies are
  moving apart to is God real to how Narnia could be... wide spread of explainers").** The channel jumps between very
  different worlds, video to video. Every Short belongs to one **topic lane** and the next Short must come from a different
  lane (no lane twice within 4 videos); `python -m autopilot variety` picks it and the log records `lane:`. Lanes:
  everyday mechanisms (how a scale, a lock, a zip works) · cosmos and physics · the body and biology · human upgrades and
  performance (the perfect soldier, fighter, athlete; training, genetics, enhancement) · bio-engineering what-ifs (four
  arms, gills, night vision) · fiction made real (Narnia-style portals, dragons, superpowers) · big philosophy and God
  questions · mind and psychology · money and power · history's wild stories · engineering and megaprojects · animals and
  nature · tech and the internet · the dark side of the real world. The review may tune format weights but never narrows
  this spread.
  **Guardrails for the wild lanes:** human upgrades and bio-engineering are told as science and thought experiments with
  honesty tags, never as instructions: no drug or doping doses, no weapons how-to, no self-surgery, no gore; real
  enhancement history (e.g. doping scandals) as documentary only. God and religion: the strongest arguments on each side,
  what science can and cannot test, respect for every faith and for none, no verdict. Fiction: name the work in words only;
  every picture is our own original art, never its characters, maps or designs.
- **Dark files (owner, 2026-11-15): the hidden side of the real world**, from fiction to fact. Drug markets and cartels, mafias
  and the underworld (D-Company, Yakuza, 'Ndrangheta...), hawala and money laundering, gambling and match-fixing, smuggling and
  illegal trades, and how they link to the normal world (the banks that laundered cartel money, the dirty money in property and
  sport, why your phone's minerals can fund wars). Mix the forms: true stories behind famous cases, myth vs reality (movies vs
  court records), thought experiments on policy (Portugal's decriminalisation, prohibition then and now) and what the evidence says.
  Guardrails, always: a documentary journalist's view, never a manual. Explain how a system works and why, never steps someone
  could copy (no recipes, quantities, prices to buy at, contacts, routes, ways to dodge police or banks, or to hide money). Real
  sources only (court records, UNODC, FATF, Interpol, government reports, major journalism) and every claim tagged. Show the cost:
  victims, violence, prison and how most of them ended. Never glamorise crime or make a criminal a hero; no gore. Living people:
  only what courts or major outlets have established, worded as such ("convicted of", "accused of"). Advertiser-friendly wording
  (YouTube may limit ads on drug or crime topics): no graphic images, no drug use shown, calm titles.
**Retention rule (owner's Studio data, 2026-11-13):** viewers watched only 10-19 s of our 40-55 s Shorts (20-36% on average).
Shorts are 25-35 s (hard cap 45 s, enforced by style.json); 65-90 spoken words; the hook and the most surprising fact land in the
first 2 s; no warm-up lines; every 2-3 s something new on screen; end on a line that loops back to the opening.
Abstract economics ("opportunity cost", "tragedy of the commons") got 94-164 views, while concrete, personal ones ("Why does the bank
pay YOU interest?") got more and won the most subscribers: frame money topics around the viewer's own wallet, with a "you" hook.
**Review 2026-11-15 (28-day stats, 20 public Shorts):** the 36-39 s Shorts reached 994-1,141 views within 6-30 h, as many as the
40-57 s ones got in a week, so keep 25-35 s. Myth-busts are the steadiest (7 of 7 at 994-1,462 views); every big-question below
850 views was abstract economics (commons 94, opportunity cost 380, bank interest 836), so big-questions should be concrete and
physical (gold, goosebumps, prisoner's dilemma all 1,100+), and economics stays wallet-first.
**Review 2026-11-22 (28-day stats, 36 public videos older than 48 h):** channel median 1,042 views; still a ceiling at
~1,000-1,470, no breakout. Myth-bust stays the steadiest (10 Shorts, median 1,112, floor 989). Dark-files is the weakest Short
format (Capone laundering 202, hawala 911, Escobar hippos 2 views after 35 h, likes 13.5 per 1k vs ~20 for the others), so its
weight drops to the 0.10 minimum and its titles stay calm and literal (no "drug lord", "cartel", "crime" words in the title).
Big-questions earn the fewest likes (14.9 per 1k; foot-asleep 1,141 views but 6 per 1k): concrete and physical only.
Skeletons: `jobs/_templates/<format>.json`. Never the same format three days in a row. Deep Dives can use any format too
(a what-if or frontier topic makes a great long video).

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
- **Documentary style** 🔒 owner-approved 2026-11-15 ("documentary type editing ... so it looks human-created"). Long videos are
  edited like a documentary, not like a long Short: a letterboxed cold open with no headlines, then a title card; a chapter
  title card for every chapter; history told as archival "reconstruction" shots of the 3D sets plus an evidence board (photos,
  clippings, typed notes, red string, marker circles and arrows drawing themselves on); timelines for dates; lower-third supers
  for people and places; small source tags ("SOURCE: NASA") on facts; quotes as full-screen quote cards; serif / handwritten
  type instead of Shorts headlines; no burned captions; mostly straight cuts, with whip pans, paper wipes and dips to black for
  scene changes; slow camera drift on every shot (no film grain: it turns into blocky mosaic after YouTube's compression; only archival shots get a fine, light grain); a score that changes with the story (wonder, doc, tension,
  one held silence). Ved is the host: to camera at the start of chapters and for the big lines, the world carries the rest.
  Humour stays dry: handwritten sticky notes, never meme caption cards. Tools: docs/job-spec.md "Documentary toolkit".
- Thumbnail, for long videos and (since 2026-11-13) Shorts too, in 9:16 (owner-approved look, 2026-11-11, The Infographics Show as reference): the world blurred and colour-graded
  behind (a two-colour gradient tint + a warm glow behind Ved), Ved big and sharp with a strong face (surprised, shocked,
  side-eye) right under the title, one or two key props sharp beside him, and a huge 1-3 word title in heavy white sans with
  one *accent* word ("JUST *PAPER?*"). No watermark, no small text. `python -m autopilot thumbnail` (spec in docs/job-spec.md);
  set via Zapier (*Update Video Thumbnail*; the channel is phone-verified and has advanced features since 2026-11-13) when the
  budget allows, otherwise the owner sets it in YouTube Studio.
- Reference: `jobs/2026-11-11-longpilot` ("How Money Actually Works").

## 7. Hooks 🔄
question · myth-bust · number-shock · "you've been told X" · countdown. The hook is on screen at frame 0 and spoken in the first 1.5 s.
- Preferred (2026-11-15): myth-bust (median 1,129 views, never below 994) and number-shock (median 1,142 when posted >= 5 h apart).
  "Question" hooks work when the question is about a physical thing the viewer can picture; avoid textbook-term questions.
- "You've been told X" tested 2026-11-15 to 11-19 (4 Shorts: 990, 434, 989, 977 views; 15.6 likes per 1k): no better than the
  median (1,042), so it is an occasional hook only, not preferred. Myth-bust (median 1,089 as a hook) and number-shock (1,042,
  21 likes per 1k) stay preferred.
- Untested: countdown (next week's experiment, at most 2 slots).

## 8. Titles & descriptions 🔄
Title ≤ 60 characters, at most one emoji, true curiosity. Description: one-line summary, then "Sources:" with links.
5-10 tags, plus #shorts and 2 niche hashtags.
- **Long videos (owner's analytics 2026-11-22: CTR 1.4-3.1%, average view 45 s of 5:18 = 14%).** Titles are one short
  curiosity question or promise (<= 50 characters, e.g. "Where Does Money Actually Come From?"), never "How X Works (From A
  to B)". The first 15 s show the payoff promise and the single strongest visual (no slow letterbox build-up before it); a
  new beat every 3-5 s; target 4-6 min (not 8). After each long video goes public, the report names the 1-2 best-performing
  Shorts on the same theme so the owner can set it as their **Related video** in YouTube Studio (the API can't set that).

## 9. Accuracy 🔒
Every factual claim is checked with a search in the same run, with sources in `meta.sources`. Anything unverified is dropped.

## 10. Schedule 🔄
- Audience (YouTube Analytics, 2026-11-08 to 11-12): ~78% United States, then India, Indonesia, Philippines; ~97% of views
  come from the Shorts feed. So posting times target US Eastern hours (IST = ET + 10:30 until US daylight saving starts on
  2027-03-14, then ET + 9:30: re-check the times then).
- Spacing rule (owner, 2026-11-12): at least ~5 hours between Shorts. Our first week showed it: the first Short after an
  18-hour gap always got 800-1,400 views, while Shorts posted 1-3 hours after the previous one got 4, 86, 164 and 565.
- Runs start early enough for real moving 3D (slot a 11:06 IST) and **post as soon as the gate passes**, in the same run; never wait
  for a later time (2026-11-25: a run told to wait ended without posting).
- **Times moved (owner, 2026-11-22, from his YouTube Studio view by posting hour: ~1,300 views for 13:00-14:30 IST posts,
  ~1,200-1,360 for 18:30-20:00, ~1,000-1,150 for 22:30-23:30).** Shorts now go live at about **13:30 IST** (slot a = the
  regular daily Short; run starts 12:36), **19:00 IST** (bonus slot b; starts 18:06) and **23:30 IST** (bonus slot c; starts
  22:36). Caveat: the midday numbers come mostly from the first week's strongest myth-busts, so topic and time are mixed up;
  the review compares slot a's new midday posts with the old 23:30 ones after 2 weeks (~14 Shorts) and reports to the owner.
- Free plan (100 tasks/month): slot a daily; bonus slots b/c only near the end of the billing cycle.
- Deep Dive (long video): Saturday, live ~21:30 IST (11 AM ET Saturday; run starts 19:56), weekly (1 upload + 1 thumbnail call). On the free plan it replaces that
  Saturday's regular Short (`budget --need upload --ref <id>-a` exits 4 on Saturdays, since slot a now runs before it).
- Weekly review: Sunday 10:20 IST (stats + sync with the Google Docs: 3 Zapier calls).

## 11. Humour 🔄
One comic beat per video (job-spec "Beats"): deadpan, side_eye, smirk, freeze, zoom_punch or silence, with an optional
meme-caption card. Current (last 2-3 weeks), sneaky, on-topic, dry and quick.
- **🔒 American internet first (owner, 2026-11-22: "the majority of the audience is from America, so the jokes and punches in
  between should mostly be the latest trends going up in the American space").** Most of the audience is in the US (~78%), so
  the joke borrows a meme format, phrase or slang that is rising right now in US internet culture (US TikTok, Reels, X, Reddit,
  late-night and sports moments, US school/office/food life), checked in that week's research (Know Your Meme recent entries,
  "trending meme this week", US TikTok trend round-ups). Still on-topic, dry, quick and in our own art; never politics,
  elections or culture-war fights, never tragedy, never real people's photos or copied meme images/audio. A timeless dry
  card is the fallback when nothing rising fits. Banned: dead memes, punching down, politics,
tragedy, crude jokes, real people's photos, copied meme images or audio.
- Landed (provisional, likes per 1k views; views alone can't separate the joke from the topic): 'Is This a Pigeon?' card (Great
  Wall, 34/1k, the channel's best), 'Remember November 2026' card (cells, 29.5/1k), 'W chews / L nibbles' card (prisoner's
  dilemma, 26.4/1k), '___ arc' slang (trillion, fine views).
- Flopped (provisional): 'Me when / me trying to' caption (goosebumps, 12.2/1k); 'Always Has Been' is mixed (sugar cube 25/1k,
  brain 10/1k), so rest it for a while; timeless cards do as well as trends when the topic is strong (gold 1,141 views).
- Don't reuse one meme more than twice a week ('What's up brah?' ran 3 times).
- Review 2026-11-22 (provisional): timeless dry cards did as well as trends ('Caesar: close enough' leap year 20/1k, Semmelweis
  hand-wash card 22/1k, Jupiter 'glow-up' 20/1k); 'I Got So Mad' landed (Voyager 23/1k); 'My Type Quiz' (hawala 8.8/1k) and the
  Tony Stark head-turn (senses 8/1k) flopped; 'foot.exe has stopped responding' 6/1k. When no rising trend fits, a timeless
  card is fine.

## 12. Change log
| date | section | change | evidence |
|---|---|---|---|
| 2026-11-23 | 3, 10 | The bar = the Wi-Fi Short: render gate (shots every <=3.5 s, >= 8 s moving 3D, <= 2 text pieces, role visible, 2-word captions); caption default 2 words at y 0.70; runs start ~6 h early | owner on the 11-23 sugar Short: "is it really the improved version?" |
| 2026-11-22 | 10 | Slot times: a ~13:30 IST (run 12:36), b ~19:00 (18:06), c ~23:30 (22:36); Saturday's slot a skips by date on the free plan; review re-checks times after 2 weeks | owner's YouTube Studio data by posting hour |
| 2026-11-22 | 11 | Humour: American internet trends first (US meme formats, phrases, slang rising this week); timeless card as fallback | owner: "majority of audience is from America" |
| 2026-11-22 | 8 | Long videos: curiosity-question titles (<= 50 chars), payoff promise + strongest visual in the first 15 s, 4-6 min, Related-video links from the best Shorts | owner's analytics: long CTR 1.4-3.1%, 45 s average view of 5:18 |
| 2026-11-22 | 6 | Topic spread: 14 topic lanes, a different lane every video (none twice in 4); new formats build-it (0.12) and fiction-made-real (0.06); weights rebalanced (big-question 0.14, myth-bust 0.19, scale-shock 0.13, what-if 0.08, deep-question 0.05, dark-files 0.08); guardrails for the wild lanes | owner: "ADHD person yt... wide spread of explainers" |
| 2026-11-22 | 3 | Real reference photos as accents (polaroid, stamp, sticky note, clipping) for real incidents, places, objects, documents; PD / CC0 / CC BY from Wikimedia Commons, auto-credited; never faces, graphic images or logos | owner: "use the real photo... just to give reference" |
| 2026-11-22 | 3, 4 | Ved wardrobe accents: jacket, blazer, goggles, sunglasses, hard hat, headset, cap, sash, scarf, badge; max 2 at once, a scene or two only, when the role needs it | owner: "only when needed, not always and not in full videos" |
| 2026-11-22 | 3 | Versatility: every Short changes Ved's role, the explain mode and the art-style mix (no role twice in 10 videos); only Ved stays constant; `autopilot variety` + log cells role/explain/styles | owner: "ADHD person yt... the only constant is me... versatility" |
| 2026-11-22 | 6 | weights: dark-files 0.20 -> 0.10, myth-bust 0.23 -> 0.28, scale-shock 0.12 -> 0.17; dark-files titles calm and literal | review: dark-files 202 / 911 / 2 views vs channel median 1,042; myth-bust median 1,112 |
| 2026-11-22 | 7 | "you've been told X" tested: occasional only; countdown is next week's experiment | review: 4 Shorts, median 983 views, 15.6 likes per 1k |
| 2026-11-22 | 11 | humour notes: timeless cards hold up; 'I Got So Mad' landed; 'My Type Quiz', Tony Stark head-turn flopped | review: likes per 1k |
| 2026-11-22 | 5 | Dynamic, story-first sound: voice always easy to follow, levels move with the moment, effects one at a time (max 3 per 2 s), small sounds vanish under speech, hits keep punch; renderer enforces it and ears reports dropped effects | owner: "explaining is the main thing... doesn't pile up too much and become noise" |
| 2026-11-22 | 3 | Mix styles inside every Short: at least three visual styles cut together per Short, Ved comes and goes, new shot every 2-4 s (reference jobs/2026-11-22-m1) | owner: "Permanent rule that you mix the styles" |
| 2026-11-21 | 3 | Professor Ved v9 (same Ved, cleaner): eyes and pocket redrawn, stray lines and overlaps removed; signature = gold pencil in pocket + gold spark pin (owner picked A + B); Ved drawn in every look (marker, chalk, riso, film, ink; night rim); mascot badge + gold watermark; 3D Ved = the layered paper standee (owner kept it over a fully modelled 3D Ved). v9.1 cleanup: no lines across the eyes, no stray folds or sleeve corners. Sheet: docs/sheets/professor_ved_model_sheet_v9.png. Owner approved 2026-11-21 ("keep the old one in 3d and move ahead") | owner request (character redesign) |
| 2026-11-21 | 3 | sound library (earshot renders + CC0 UI pack; Openverse real recordings once allowed), peak-on-frame sync, no doubling, voice-safe ducking, ears measurements on every render | owner request (Openverse, Real SFX, earshot) |
| 2026-11-21 | 3 | score on real sampled instruments (Lemo-Opuscar sampler, CC0 packs; same key/tempo/progression), orchestral stings on slams, chapters and stamps, director's checks on every render (hook, reading time, pace, camera variety, sound-carried cuts, silences, blank frames), treatment step for Deep Dives, Lemo styles as technique donors | owner request (lemo-opuscar) |
| 2026-11-21 | 3 | Reelsmith: our own code-film engine (look layers captured in headless Chrome) with 10 original looks RS-01..RS-10, grand piano (credited automatically), folk palette with modelled guitar, HDRI room light in Blender; DEMO jobs/2026-11-21-looks, awaiting owner OK | owner request (lemo-opuscar, "same or better, our own names") |
| 2026-11-21 | 3 | Cutaway (owner-purchased) connected: 3D cutaway shots as `video` layers from the private install (never in the public repo); its CC0 sounds in the library; freeze check; DEMO jobs/2026-11-21-cutaway | owner request |
| 2026-11-21 | 2 | Ved's voice changed to bm_lewis (en-us, 1.0): the nearest built-in voice to the owner's own recording | owner request (voice recording) |
| 2026-11-18 | 3 | motion clips made more dynamic (NumberSlam, Stack3D, slam titles); long documentary recipe + sample 2026-11-18-doc | owner request |
| 2026-11-18 | 3 | motion clips added (Remotion + GSAP + three.js: kinetic titles, self-drawing cream-card flows, real-time 3D coin/bars/globe), mixed into the house style; DEMO 2026-11-18-motion | owner request (learn remotion, gsap, three.js skills) |
| 2026-11-18 | 3 | case-file pieces added (noir desk + blinds light, dottext, bignum, dateline, tipnum, tiles, clock, flows, evidence props); DEMO awaiting owner OK | owner request (reference documentary study) |
| 2026-11-16 | 3 | night-pilot graphics + motion rules become the standard for all Shorts (town too): ticking hud chips, eqbar, crowd-as-data, trackers, node trees, option cards, stamps, live phones, bursts, fixed colour meaning | owner request |
| 2026-11-16 | 3 | night set APPROVED by the owner (pilot 2026-11-16-n); usable in public dark-files / scam / money-trap / big-reveal Shorts | owner: "I think this one is good" |
| 2026-11-16 | 3 | night set added as an opt-in second mood (PILOT 2026-11-16-n, awaiting approval): hud, eqbar, tracker, stamp, optcard, phone, crowd, nodes, burst, highlight captions, rim light | owner request (reference Short study) |
| 2026-11-15 | 6 | dark-files 0.08 -> 0.20 (about 1 Short in 5); big-question 0.23 -> 0.18, scale-shock 0.14 -> 0.12, what-if 0.12 -> 0.09, frontier 0.10 -> 0.08; myth-bust stays 0.23 | owner: dark content attracts viewers |
| 2026-11-15 | 6 | new format dark-files 0.08 (hidden economies, crime worlds, how they touch the normal world; documentary guardrails); big-question 0.27 -> 0.23, scale-shock 0.15 -> 0.14, what-if 0.15 -> 0.12 | owner request |
| 2026-11-15 | 6 | Deep Dive documentary style (chapter cards, archival reconstructions, evidence board, supers, source tags, grain, scored cues, no burned captions) | owner request |
| 2026-11-15 | 6 | weights: myth-bust 0.20 -> 0.23, big-question 0.30 -> 0.27; big-questions concrete/physical, not textbook terms | review: myth-bust 7/7 >= 994 views; big-question lows all abstract econ (94, 380, 836) |
| 2026-11-15 | 7 | preferred hooks myth-bust + number-shock; 'you've been told X' / countdown queued as next week's test | review 2026-11-15 |
| 2026-11-15 | 11 | first Landed / Flopped notes (provisional); max 2 uses of one meme per week | review 2026-11-15, likes per 1k |
| 2026-11-07 | all | channel set up | owner decisions in setup |
| 2026-11-13 | 6 | custom thumbnails on Shorts too (9:16, same look), when the budget allows | owner: "thumbnail impressions are low" |
| 2026-11-13 | 6 | Shorts 25-35 s (cap 45 s); hook + best fact in 2 s; econ topics framed around the viewer | owner's Studio data |
| 2026-11-13 | 1 | give real, conditional answers (works where/when/why), e.g. communism at country vs small-group scale | owner |
| 2026-11-13 | 1 | facts over balance: say which side the evidence favours, with numbers and context; no verdict on values | owner |
| 2026-11-13 | 6 | topic rule: unique / trending / viral-shaped, ideally a mix | owner |
| 2026-11-13 | 6 | new formats added: what-if, frontier, wild-story, deep-question; honesty tags | owner idea (additions only) |
| 2026-11-11 | 6, 10 | weekly long video (Deep Dive, 16:9) added | owner: "make it a video a week" |
| 2026-11-08 | 3 | v3 (2026-11-08-m3) approved as the final house style and reference video; removed the old "Ved small in a corner" rule | owner: "final this" |
| 2026-11-08 | 3 | living town: faceless townspeople with outfits, body-language emotions, depth staging (perspective + foreground layers), smoother stall/apples | owner request |
| 2026-11-08 | 3 | 3D world from stills + cut-outs animated in 2D (smooth, fast); Ved walks/jumps/talks to camera; multi-angle cuts | owner request |
| 2026-11-08 | 1, 3 | style = 2D characters in a 3D world (Rick's Clips) + 2D infographic panels + clean 3D objects | owner request |
| 2026-11-08 | 1, 2, 3 | niche = complex topics made simple; cinematic Blender 3D + infographic text; even-handed politics/economics; callbacks only when essential | owner request |
