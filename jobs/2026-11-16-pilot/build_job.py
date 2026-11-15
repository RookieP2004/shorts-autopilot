"""Pilot 2026-11-16-pilot: the reference-reel style (owner, 2026-11-15) on a Dark Files story.
Learned from @ayushpediaa: moody single-light 3D, one red accent, a mono label + condensed headline on every shot that stays
while the picture changes, camera that travels (push transitions, rack focus), stats as objects, real foley under every
action, a deep expressive narrator, and a share prompt at the end. Facts: US DOJ (Dec 2012), US Senate PSI report (Jul 2012).
Run: python jobs/2026-11-16-pilot/build_job.py
"""
import json, os

J = "jobs/2026-11-16-pilot/"
A = J + "assets/"
S = []


def plate(name, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def head(label, text, at=0.15, y=0.15, **k):
    return {"type": "headline", "label": label, "text": text, "y": y, "at": at, **k}


def scene(say, layers, **k):
    S.append({"say": say, "layers": layers, "look": "moody", **k})


# 1. hook: the boxes
scene("Drug cartels built boxes... made to fit a bank's teller window.",
      [plate("teller_close", blur_keys=[[0, 10], [1.2, 0]]),
       head("HSBC Mexico · 2006-2010", "BOXES MADE TO FIT\nTHE *TELLER WINDOW*", at=0.0)],
      sfx="slide", sfx_at=0.4, camera={"zoom": [1.0, 1.08], "focus": [0.48, 0.52]})
# 2. the cash
scene("Packed with cash. Hundreds of thousands of dollars... in a single day.",
      [plate("cash_close"), head("US Justice Department", "*CASH.* EVERY DAY.", at=0.2),
       sprite("bundle", 0.5, 0.36, 0.36, enter="drop", at=2.2, sfx="thud")],
      transition="push", transition_frames=12, sfx="cash", sfx_at=0.3, camera={"zoom": [1.04, 1.12], "focus": [0.55, 0.55]})
# 3. washing: in, around, out
scene("Dirty money has to be washed. In... around... and back out, clean.",
      [plate("laundry_wide"),
       plate("laundry_door", iris={"x": 0.5, "y": 0.5, "r0": 0.0, "r1": 0.75, "at": 1.4, "dur": 1.0}),
       head("Money laundering", "DIRTY CASH IN.\n*CLEAN* MONEY OUT.", at=0.2)],
      transition="push", transition_frames=12, sfx="drone", camera={"zoom": [1.0, 1.1], "focus": [0.52, 0.42]})
# 4. the $7 billion
scene("HSBC Mexico shipped seven billion dollars in cash to the US... in two years.",
      [plate("cash_table"), head("US Senate report · 2012", "*$7 BILLION*\nIN PHYSICAL DOLLARS", at=0.2),
       {"type": "counter", "from": 0, "to": 7000000000, "count_dur": 2.2, "at": 1.0, "x": 0.5, "y": 0.66, "size": 104,
        "font": "fonts/Anton-Regular.ttf", "prefix": "$", "color": "primary", "enter": "fade", "sfx": "tick"},
       {"type": "tag", "text": "2007-2008", "x": 0.5, "y": 0.73, "at": 2.4, "font": "mono_b", "size": 30}],
      transition="cut", camera={"zoom": [1.1, 1.0], "focus": [0.5, 0.55]})
# 5. traced to cartels
scene("Prosecutors said at least eight hundred and eighty-one million came from two cartels.",
      [plate("cash_close", blur=6),
       head("Sinaloa · Norte del Valle", "*$881 MILLION*\nFROM TWO CARTELS", at=0.2),
       sprite("bundle", 0.3, 0.55, 0.3, enter="drop", at=1.6, sfx="thud", rotate=-8),
       sprite("bundle", 0.68, 0.6, 0.3, enter="drop", at=2.0, sfx="thud", rotate=6),
       sprite("bundle", 0.5, 0.5, 0.32, enter="drop", at=2.4, sfx="thud", rotate=-3)],
      transition="cut", camera={"zoom": [1.0, 1.06], "focus": [0.5, 0.55]})
# 6. the punishment
scene("The bank paid one point nine billion. Not one banker went to prison.",
      [plate("courthouse"),
       {"type": "character", "id": "ved", "pose": "crossed", "acting": [["serious", 0], ["crossed", 2.4]], "x": 0.74, "y": 0.83,
        "h": 0.3, "enter": "fade", "allow_outside_safe": True, "ground": True},
       head("December 2012", "$1.9 BILLION PAID.\n*0* JAILED.", at=0.2)],
      transition="push", transition_frames=12, sfx="stomp", sfx_at=2.6, camera={"zoom": [1.0, 1.07], "focus": [0.5, 0.45]})
# 7. why it matters to you
scene("It's why your bank asks... where your money comes from.",
      [plate("desk"),
       {"type": "paper", "kind": "doc", "title": "SOURCE OF FUNDS", "text": "Where does this money come from? ____________", "w": 0.5,
        "x": 0.52, "y": 0.58, "rotate": -6, "at": 0.6, "enter": "slam", "sfx": "paper", "tape": []},
       head("Know your customer", "“SOURCE OF *FUNDS?*”", at=0.2)],
      transition="cut", camera={"zoom": [1.0, 1.08], "focus": [0.5, 0.58]})
# 8. share prompt
scene("Send this to someone who thinks banks are boring.",
      [plate("teller_wide", blur=10),
       {"type": "character", "id": "ved", "pose": "point", "acting": [["point", 0]], "x": 0.5, "y": 0.86, "h": 0.62,
        "enter": "fade", "ground": False, "allow_outside_safe": True},
       head("Send this", "TO SOMEONE WHO THINKS\nBANKS ARE *BORING*", at=0.1, sub="Follow for more")],
      transition="dip", transition_frames=10, min_dur=3.4, camera={"zoom": [1.0, 1.05], "focus": [0.5, 0.45]})

job = {
    "id": "2026-11-16-pilot",
    "title": "Cartels built boxes to fit a bank's window \U0001f4e6",
    "description": "Mexican drug cartels used boxes designed to fit HSBC Mexico's teller windows. What happened next, and why your "
                   "bank now asks where your money comes from.\n\nSources: US Department of Justice, HSBC deferred prosecution "
                   "announcement (Dec 2012); US Senate Permanent Subcommittee on Investigations, HSBC case history (Jul 2012).",
    "tags": ["money laundering", "hsbc", "cartels", "dark files", "true crime", "banking", "explained"],
    "hashtags": ["#truecrime", "#moneylaundering"],
    "instagram": {"hashtags": ["#truecrime", "#moneylaundering", "#hsbc", "#cartel", "#explained"]},
    "meta": {"format": "dark-files", "topic": "HSBC and the cartel cash boxes (money laundering explained)", "hook": "story",
             "idea_source": "owner request: reference-reel style pilot; dark-files backlog",
             "characters": ["ved"], "overrides": "pilot of the reference-reel style (moody 3D, headline system, deeper narrator)",
             "sources": ["https://www.justice.gov/opa/speech/assistant-attorney-general-lanny-breuer-speaks-hsbc-press-conference",
                         "https://www.hsgac.senate.gov/subcommittees/investigations/rep/hsbc-exposed-u-s-financial-system-to-money-laundering-drug-terrorist-financing-risks/",
                         "https://www.foxbusiness.com/markets/hsbc-became-bank-to-drug-cartels-pays-big-for-lapses"],
             "claims": [{"claim": "traffickers used boxes designed to fit HSBC Mexico teller windows", "tag": "PROVEN", "source": "DOJ 2012"},
                        {"claim": "hundreds of thousands of dollars in cash in a single day, into a single account", "tag": "PROVEN", "source": "DOJ 2012"},
                        {"claim": "HSBC Mexico shipped $7B in physical US dollars to HSBC US in 2007-2008", "tag": "PROVEN", "source": "Senate PSI 2012"},
                        {"claim": "at least $881M laundered by the Sinaloa and Norte del Valle cartels (2006-2010)", "tag": "PROVEN", "source": "DOJ 2012"},
                        {"claim": "$1.92B total ($1.256B forfeiture + $665M civil); no bank or executive indicted", "tag": "PROVEN", "source": "DOJ/Reuters 2012"}],
             "humour": {"trend": "none (dark-files pilot)", "beat": "none", "scene": -1}},
    "privacy": "private", "speaker": "ved",
    "voice": {"pitch": -1.6, "warmth": 0.5},
    "music": {"cues": [{"scene": 0, "style": "tension", "key": "D", "scale": "minor", "bpm": 70}, {"scene": 6, "style": "doc", "key": "D", "scale": "minor"}],
              "volume": 0.12},
    "captions": False,
    "style_override": {"doc": {"enabled": True, "grain": 0, "vignette": 0.3, "drift": 1.0, "auto_camera": True},
                       "progress_bar": {"enabled": False}},
    "assets_script": J + "assets.py",
    "scenes": S,
}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "words", sum(len(s["say"].split()) for s in S))
