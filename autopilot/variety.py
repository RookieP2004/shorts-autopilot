"""Versatility (owner, permanent 2026-11-22): the channel is for restless (ADHD) viewers, so every Short changes Ved's
ROLE, the WAY it explains and the ART STYLES it mixes. The only constant is Ved himself (same drawing, white shirt, same
voice). A role is played through the set, a prop in his hand or on the set, the words he uses and the framing, never by
redrawing him.

`python -m autopilot variety` reads the log and suggests a role, an explain mode and a style mix that were not used
recently. Put the choices in the job's meta (`role`, `explain`, `styles`) so the log records them for the next run.
"""
import datetime as dt
import json
import os
import random
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# role: (who he is in this video, the set, props, how he talks)
ROLES = {
    "teacher": ("a teacher in front of a class", "classroom, chalkboard (RS-07 Chalk)", "chalk, pointer stick", "patient, asks the class a question, then answers it"),
    "project lead": ("a project lead running a stand-up", "office whiteboard (RS-13 Whiteboard), sticky notes", "marker, coffee mug", "brisk, 'here's the plan', assigns the parts of the idea like tasks"),
    "fellow friend": ("a friend on the sofa", "living room, phone in hand", "phone, snacks", "casual, 'bro, you won't believe this'"),
    "enthusiast": ("a fan who can't contain himself", "his room full of models and posters", "model of the subject", "fast, delighted, 'this is the coolest thing ever'"),
    "hacker": ("a hacker in a dark room (documentary, never a how-to)", "night set, screens (RS-12 Terminal)", "laptop, glowing screens", "quiet, 'let me show you what's really running underneath'"),
    "tour guide": ("a guide leading a tour", "the town or a museum hall", "small flag, ticket", "'on your left you'll see...', walks while talking"),
    "mayor": ("the mayor of the town", "town hall podium, townspeople as the crowd", "sash, gavel", "announces it like a city decision, the crowd reacts"),
    "project planner": ("a planner laying out the steps", "planning table, timeline board", "clipboard, Gantt chart", "step 1, step 2, ticks them off (tracker)"),
    "city planner": ("a city planner over a scale model of the town", "model town on a table (no country outlines)", "rolled map of the town, ruler", "zooms in on streets, moves little buildings"),
    "detective": ("a detective cracking a case", "case-file desk, blind-stripe light", "magnifying glass, evidence cards", "clues first, then the reveal"),
    "news anchor": ("a news anchor with breaking news", "news desk, lower-third banner (fictional channel)", "papers, earpiece", "'breaking tonight...', cuts to field shots"),
    "scientist": ("a scientist running an experiment", "lab bench", "beaker, goggles on his forehead", "hypothesis, test, result"),
    "chef": ("a chef cooking up the idea", "kitchen counter", "pan, tasting spoon", "a recipe: ingredients, steps, taste"),
    "sports commentator": ("a commentator calling the action live", "stadium booth", "headset mic", "fast play-by-play, replays the key moment"),
    "museum curator": ("a curator showing an exhibit", "gallery with spotlit plinths", "white gloves", "slow, reverent, one object at a time"),
    "game-show host": ("a quiz host", "game-show stage, option cards (optcard)", "cue cards, buzzer", "asks the viewer to guess, reveals the answer"),
    "coach": ("a coach at half-time", "locker room, tactics board", "whistle, clipboard", "pep talk, draws the play"),
    "ship captain": ("a captain on deck", "ship deck at sea", "spyglass, captain's hat in hand", "orders, weather, the journey"),
    "pilot": ("a pilot talking from the cockpit", "cockpit with dials", "headset", "calm announcements, 'we are now passing...'"),
    "mission control": ("a flight director at mission control", "consoles, countdown clock", "headset, checklist", "go/no-go calls, countdown"),
    "historian": ("a historian with old records", "archive room, dusty shelves", "old book, dateline cards", "'in 1846...', then and now"),
    "explorer": ("an explorer on an expedition", "jungle, cave or desert set", "map of the trail, lantern", "discovers it step by step"),
    "inventor": ("an inventor in his workshop", "workbench, blueprints (RS-05 Blueprint)", "wrench, prototype", "builds the idea piece by piece"),
    "shopkeeper": ("a shopkeeper at the counter", "town market stall", "receipt (RS-01 Receipt), scale", "prices, deals, customers"),
    "banker": ("a banker at the vault", "bank hall, vault door", "ledger, fictional notes (NOT REAL MONEY)", "interest, risk, who wins"),
    "judge": ("a judge hearing a case", "courtroom bench", "gavel", "both sides argue, the evidence decides (verdict stamp)"),
    "weather presenter": ("a weather presenter", "studio with a big map of the town", "clicker", "forecast style, arrows and fronts"),
    "radio host": ("a late-night radio host", "radio booth, ON AIR light", "big microphone", "intimate, takes a 'caller' question"),
    "magician": ("a street magician revealing the trick", "street corner, small crowd", "cards, top hat on the table", "the trick first, then how it really works"),
    "time traveller": ("a time traveller visiting another era", "the town in another century", "pocket watch", "'where I come from...', then vs now"),
    "doctor": ("a doctor explaining how the body works (never advice)", "clinic with an anatomy chart", "stethoscope", "calm, 'here's what happens inside'"),
    "engineer": ("an engineer on site", "construction site, cutaway machine", "hard hat in hand, tablet", "loads, forces, why it doesn't break"),
    "podcast host": ("a podcast host mid-episode", "podcast studio, two mics", "headphones", "conversational, a guest question"),
    "farmer": ("a farmer in his field", "farm, barn, crops", "basket, pitchfork", "seasons, growth, simple maths with crops"),
    "astronaut": ("an astronaut floating in the station", "space station window, Earth glow (no outlines)", "tablet strapped to arm", "weightless demo, wonder"),
    "librarian": ("a librarian pulling the right book", "library aisle", "stack of books, stamp", "hushed, 'the answer is on this shelf'"),
    "documentary narrator": ("the narrator of a nature or history documentary", "wide 3D world, slow camera", "none: voice-led", "calm, serif titles, cinematic"),
}

# optional role pieces from Ved's wardrobe (characters/ved/make.py WEAR_ITEMS): for one or two scenes only, never the
# whole video, at most two at once; most videos need none. Layer: "rig_args": {"wear": "jacket,goggles"}
ROLE_WEAR = {"hacker": "jacket", "detective": "jacket", "explorer": "goggles", "inventor": "goggles", "time traveller": "goggles",
             "engineer": "hardhat", "city planner": "hardhat", "project lead": "badge", "project planner": "badge",
             "mayor": "sash", "ship captain": "cap", "pilot": "headset,sunglasses", "mission control": "headset",
             "radio host": "headset", "podcast host": "headset", "sports commentator": "headset", "news anchor": "blazer",
             "judge": "blazer", "banker": "blazer", "magician": "blazer", "tour guide": "scarf", "enthusiast": "badge",
             "fellow friend": "sunglasses"}

# topic lanes (owner, permanent 2026-11-22: an ADHD viewer's channel jumps between very different worlds). The next Short
# comes from a lane not used in the last 4 videos.
LANES = {
    "everyday mechanisms": "how a scale, a lock, a zip, a fridge, a toilet flush, a lift really works",
    "cosmos and physics": "why galaxies are flying apart, black holes, time, light, quantum weirdness",
    "the body": "what your organs, cells, brain and senses are really doing",
    "human upgrades": "how to build the perfect soldier, fighter, athlete, sprinter, diver: training, genetics, tech, limits",
    "bio-engineering what-ifs": "a human with four arms, gills, night vision, a tail, photosynthesis skin: what would it take",
    "fiction made real": "could a Narnia-style wardrobe portal, dragons, invisibility, a flying carpet, a hollow Earth work",
    "philosophy and God": "is God real, free will, what is consciousness, is the universe a simulation, what is time",
    "mind and psychology": "why you procrastinate, why crowds panic, memory tricks, why we believe things",
    "money and power": "why prices rise, how banks make money, why empires fall, who really owns things",
    "history's wild stories": "true crazy stories, inventions by accident, strange experiments, lost cities",
    "engineering and megaprojects": "how to build a city on Mars, why bridges don't fall, the deepest hole, an unsinkable ship",
    "animals and nature": "animal superpowers, weird ecosystems, why trees talk, how volcanoes work",
    "tech and the internet": "how the internet reaches you, how AI learns, how GPS knows where you are",
    "dark side of the real world": "hidden economies and crime worlds as a documentary (Bible dark-files guardrails)",
}

EXPLAIN = {
    "analogy demo": "one everyday object stands in for the idea and is shown doing it",
    "experiment": "set up, run, measure, surprising result",
    "myth vs fact": "the belief on screen, then stamped FALSE / TRUE with the evidence",
    "story": "one person or moment, told as a mini-film with a twist",
    "step-by-step build": "the thing is assembled piece by piece, each piece named",
    "scale zoom": "macro to whole (or whole to atom), one cut per change of scale",
    "versus": "A vs B on a balance or split screen, the winner explained",
    "what-if simulation": "change one rule and run the world forward",
    "quiz": "ask the viewer, give options, reveal",
    "countdown list": "3 (or 5) reasons, counted down to the biggest",
    "timeline": "then -> now along a dated line",
    "inside the machine": "travel inside the object and watch it work",
    "numbers do the maths": "a crowd or hud chip does the arithmetic on screen",
    "debate": "two townspeople argue, Ved settles it with evidence",
    "case file": "clues, suspects, the reveal",
}

STYLES = {
    "3D town (Ved + townspeople)": "town",
    "Cutaway 3D mechanism": "cutaway",
    "Blender hero props / plates": "blender",
    "cream infographic card": "card",
    "hud chip + equation bar": "hud",
    "crowd as data": "crowd",
    "night set": "night",
    "case-file pieces": "casefile",
    "motion clip: KineticTitle / NumberSlam": "motion-type",
    "motion clip: FlowDiagram / Stack3D / Hero3D": "motion-3d",
    "phone / fictional app screen": "phone",
    "comic beat card": "comic",
    "RS-01 Receipt": "RS-01", "RS-02 Pinboard map": "RS-02", "RS-03 Balance": "RS-03", "RS-04 Flipboard": "RS-04",
    "RS-05 Blueprint": "RS-05", "RS-06 Bubbles": "RS-06", "RS-07 Chalk": "RS-07", "RS-08 Radar": "RS-08",
    "RS-09 Word Beat": "RS-09", "RS-10 Bite": "RS-10", "RS-11 Riso": "RS-11", "RS-12 Terminal": "RS-12",
    "RS-13 Whiteboard": "RS-13", "RS-14 Silent card": "RS-14", "RS-15 Ink brush": "RS-15",
}


def recent(n=12):
    """(role, explain, styles) of the last n videos, read from the log's 'role:' / 'explain:' / 'styles:' cells."""
    p = os.path.join(ROOT, "channel", "memory", "log.md")
    rows = [l for l in open(p, encoding="utf-8").read().splitlines() if re.match(r"^\d{4}-\d\d-\d\d-\w+ \|", l)][-n:]
    out = []
    for l in rows:
        cell = lambda k: (re.search(rf"\| {k}: ([^|]+)", l) or [None, ""])[1].strip()
        out.append((cell("role"), cell("explain"), [s.strip() for s in cell("styles").split("+") if s.strip()], cell("lane")))
    return out


def suggest(seed=None, k_styles=4):
    rec = recent()
    used_roles = {x[0] for x in rec[-10:] if x[0]}
    used_explain = {x[1] for x in rec[-4:] if x[1]}
    used_lanes = {x[3] for x in rec[-4:] if x[3]}
    last_styles = set(rec[-1][2]) if rec else set()
    rng = random.Random(seed if seed is not None else dt.date.today().toordinal())
    roles = [r for r in ROLES if r not in used_roles] or list(ROLES)
    modes = [m for m in EXPLAIN if m not in used_explain] or list(EXPLAIN)
    lanes = [l for l in LANES if l not in used_lanes] or list(LANES)
    role, mode, lane = rng.choice(roles), rng.choice(modes), rng.choice(lanes)
    pool = [s for s in STYLES.values() if s not in last_styles]
    styles = ["town"] if "town" not in last_styles else []           # Ved's world appears in most videos, but not by rote
    styles += rng.sample([s for s in pool if s not in styles], k_styles - len(styles))
    return role, mode, styles, lane


def report(seed=None):
    role, mode, styles, lane = suggest(seed)
    who, where, props, talk = ROLES[role]
    names = {v: k for k, v in STYLES.items()}
    lines = [
        f"LANE     {lane}: {LANES[lane]}  (pick the topic from this lane; see ideas.md)",
        f"ROLE     {role}: Ved as {who}",
        f"         set: {where} | props: {props}",
        f"         talks: {talk}",
        f"         wear (optional, one or two scenes only): {ROLE_WEAR.get(role, 'none needed')}",
        f"EXPLAIN  {mode}: {EXPLAIN[mode]}",
        "STYLES   " + " + ".join(names.get(s, s) for s in styles),
        "         (cut between them every 2-4 s; Ved, his white shirt and his voice never change)",
        f'meta:    "lane": "{lane}", "role": "{role}", "explain": "{mode}", "styles": {json.dumps(styles)}',
        "Suggestions, not orders: swap any of them when the topic clearly fits another role, mode or style better",
        "(but never repeat a role used in the last 10 videos, nor a lane used in the last 4).",
    ]
    return "\n".join(lines)
