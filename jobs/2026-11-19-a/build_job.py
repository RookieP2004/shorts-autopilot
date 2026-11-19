"""2026-11-19-a: "A year isn't 365 days" (big-question, "you've been told X" hook): why leap years exist.
2D Ved + two townspeople (Rosa the baker, Theo in a bowler) staged in the sunny clock-tower square in front of a giant
wall calendar (February, 29 circled), and in space: Earth stopped just short of the START line of its orbit.
2D on top: WRONG stamp + headline, ticking hud chips (365 d + 6 h, 11 min, 10 days), an eqbar (6 h x 4 = 1 day),
calendar cards (FEB 29; OCT 4 -> OCT 15), optcards (1900 cross / 2000 tick), the comic beat, a season-drift card.
Facts (OpenStax Astronomy 2e 4.4; Britannica "The Gregorian calendar"; Time; Atlas Obscura):
tropical year ~365.2422 days (365 d 5 h 48 min); Julian calendar (Julius Caesar, 45 BC) added a day every 4 years
(365.25 d), ~11 min a year too long; by 1582 the equinox had drifted ~10 days; Pope Gregory XIII's reform: Thursday
4 October 1582 was followed by Friday 15 October; century years are leap years only if divisible by 400 (1900 no, 2000 yes).
Without leap days a 365-day calendar slips ~0.24 day a year: half a year (seasons flipped) in ~750 years.
Run after the assets exist: python jobs/2026-11-19-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-19-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("plaza_wide", "plaza_mid", "clock_up", "orbit_wide", "orbit_close")}

OUT = {   # recurring townspeople: same outfit in every shot
    "rosa": {"skin": "#c68a5e", "build": "round", "hair": ["#1a1410", "bun"], "hat": ["headscarf", "#d9534f"],
             "top": ["#f2b04a", "dress"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "apron": "#f6efe2", "earrings": "#f2b04a"},
    "theo": {"skin": "#8d5a3b", "build": "slim", "hair": ["#1a1410", "short"], "hat": ["bowler", "#1a1410"],
             "top": ["#34425c", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "tie": "#7c2533", "bag": "#8a5a3c"},
}
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 330 84'><rect x='4' y='4' width='322' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='188' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.26, "enter": "pop", "at": at, "sfx": "click"}


def cal(month, day, top="#d9534f", ring=False, cross=False):
    """A cream tear-off calendar page: coloured month band, a big day number."""
    extra = ""
    if ring:
        extra += "<ellipse cx='200' cy='300' rx='150' ry='120' fill='none' stroke='#d9534f' stroke-width='14'/>"
    if cross:
        extra += ("<path d='M70,170 L330,430 M330,170 L70,430' stroke='#d9534f' stroke-width='22' stroke-linecap='round'/>")
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 470'>"
            "<rect x='6' y='14' width='388' height='450' rx='30' fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>"
            f"<path d='M6,44 Q6,14 36,14 L364,14 Q394,14 394,44 L394,120 L6,120 Z' fill='{top}' stroke='#1a1410' stroke-width='7'/>"
            f"<text x='200' y='98' text-anchor='middle' font-size='70' fill='#f6efe2' {AN}>{month}</text>"
            f"<text x='200' y='380' text-anchor='middle' font-size='230' fill='#1a1410' {AN}>{day}</text>"
            "<circle cx='120' cy='14' r='14' fill='#c9a24a' stroke='#1a1410' stroke-width='5'/>"
            "<circle cx='280' cy='14' r='14' fill='#c9a24a' stroke='#1a1410' stroke-width='5'/>" + extra + "</svg>")


SEASONS = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 300'>"
           "<rect x='6' y='6' width='588' height='288' rx='30' fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>"
           f"<text x='150' y='68' text-anchor='middle' font-size='44' fill='#1a1410' {AN}>DECEMBER</text>"
           "<circle cx='150' cy='175' r='62' fill='#ffd23a' stroke='#1a1410' stroke-width='6'/>"
           + "".join(f"<path d='M{150 + 80 * c},{175 + 80 * s} L{150 + 100 * c},{175 + 100 * s}' stroke='#f2b04a' stroke-width='10' stroke-linecap='round'/>"
                     for c, s in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)))
           + f"<text x='435' y='125' text-anchor='middle' font-size='70' fill='#d9534f' {AN}>SUMMER?</text>"
           f"<text x='420' y='225' text-anchor='middle' font-size='46' fill='#3f7fbf' {AN}>IN ~750 YEARS</text></svg>")

S = []
# 0. hook: the square by the giant calendar; WRONG stamp + headline at frame 0; Ved points at February
S.append({"say": "You've been told a year is *365 days*. Wrong.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.08, "focus": [0.55, 0.45]}]},
          "layers": [plate("plaza_mid"),
                     ved("plaza_mid", 0.2, -2.6, [["point", 0], ["explain", 1.6], ["smirk", 2.6]]),
                     txt("A YEAR = *365 DAYS?*", 0.13, 92, enter="none"),
                     {"type": "stamp", "text": "WRONG", "tone": "red", "angle": -7, "size": 84, "x": 0.5, "y": 0.25, "at": 1.9, "sfx": "thud"}]})
# 1. space, wide: the Sun, the orbit ring, Earth stopped just short of the gold line
S.append({"say": "Earth needs *6 more hours* to lap the Sun.",
          "transition": "zoom", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.1, "focus": [0.45, 0.6]}]},
          "layers": [plate("orbit_wide"),
                     hud("one lap of the sun", y=0.13, text="365 DAYS", at=0.1, tone="blue", width_of="365 D + 6 H",
                         until=1.3),
                     hud("one lap of the sun", y=0.13, text="365 D + 6 H", at=1.3, enter="none", tone="gold",
                         width_of="365 D + 6 H"),
                     txt("START", 0.72, 46, x=0.56, enter="pop", at=0.6, sfx="pop", color="#ffd23a"),
                     tag_layer(0.5, 0.24, 2.2)]})
# 2. space, close on Earth and the gold gap: the maths builds
S.append({"say": "Skip them, and every *4 years* you lose a *day*.",
          "transition": "cut", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.05, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.15, "focus": [0.5, 0.55]}]},
          "layers": [plate("orbit_close"),
                     {"type": "tracker", "n": 4, "done": [0.4, 0.9, 1.4, 1.9], "x": 0.5, "y": 0.14, "at": 0.1, "enter": "fade"},
                     {"type": "eqbar", "x": 0.5, "y": 0.24, "at": 0.3, "tone": "gold",
                      "keys": [[0.0, "6 h x 4 years"], [1.6, "24 h = *1 day*"]]},
                     txt("1 DAY BEHIND", 0.7, 70, enter="pop", at=2.6, sfx="pop", color="#ff6b5e")]})
# 3. the square wide: Rosa and Theo by the calendar; FEB 29 page drops in; Rosa cheers
S.append({"say": "So we add one: *February 29*.",
          "transition": "slide_left", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.55, 0.55]}]},
          "layers": [plate("plaza_wide"),
                     person("plaza_wide", "rosa", 0.4, 0.2, [["idle", 0], ["cheer", 1.6], ["happy", 2.6]], hops=[[1.7, 0.03, 0.45]]),
                     person("plaza_wide", "theo", 2.8, -0.4, [["idle", 0], ["shrug", 1.0], ["happy", 2.2]],
                            walk=[(0, 5.0, -0.8), (1.2, 2.8, -0.4)]),
                     ved("plaza_wide", -1.6, -2.2, [["explain", 0], ["point", 1.3]]),
                     {"type": "image", "svg": cal("FEB", "29", ring=True), "x": 0.5, "y": 0.2, "w": 0.3, "rotate": -4, "at": 1.2, "sfx": "pop",
                      "enter": "none", "keys": [{"t": 0, "y": -0.2}, {"t": 0.5, "y": 0.2, "ease": "bounce"}]},
                     txt("LEAP *DAY*", 0.08, 70, enter="pop", at=1.8, sfx="pop")]})
# 4. up at the clock tower: Caesar's rule is 11 minutes too generous
S.append({"say": "But Caesar's rule overshoots: *11 minutes* a year.",
          "transition": "slide_up", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.12, "focus": [0.5, 0.42]}]},
          "layers": [plate("clock_up"),
                     {"type": "dateline", "date": "45 BC", "place": "ROME", "x": 0.5, "y": 0.1, "at": 0.1, "enter": "fade", "sfx": "type"},
                     hud("too long, per year", y=0.76, to=11, suffix=" MIN", count_dur=1.2, at=1.8, tone="red", width_of="11 MIN"),
                     {"type": "clock", "time": "00:11", "from": "00:00", "dur": 1.4, "label": "EXTRA", "r": 0.08, "x": 0.8, "y": 0.62,
                      "at": 1.9, "enter": "pop"}]})
# 5. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("plaza_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "Caesar: *close enough*", "text_y": 0.2}})
# 6. the square mid: by 1582 the seasons are 10 days off
S.append({"say": "By *1582*, the seasons were *10 days* off.",
          "transition": "cut", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.08, "focus": [0.55, 0.5]}]},
          "layers": [plate("plaza_mid"),
                     person("plaza_mid", "theo", 1.0, 0.6, [["idle", 0], ["sad", 1.4]]),
                     {"type": "dateline", "date": "1582", "place": "EUROPE", "x": 0.5, "y": 0.1, "at": 0.0, "enter": "fade", "sfx": "type"},
                     hud("calendar vs sky", y=0.22, to=10, suffix=" DAYS OFF", count_dur=1.4, at=0.6, tone="red", width_of="10 DAYS OFF")]})
# 7. blurred square + two calendar pages: October 4th, then October 15th
S.append({"say": "So the Pope *deleted them*. October 4th, then *15th*.",
          "transition": "slide_left", "caption_y": 0.62,
          "layers": [plate("plaza_wide", blur=12, keys=[{"t": 0, "scale": 1.2}, {"t": 4, "scale": 1.26}]),
                     {"type": "image", "svg": cal("OCT", "4", top="#3f7fbf"), "x": 0.28, "y": 0.27, "w": 0.36, "rotate": -4,
                      "enter": "slide_up", "at": 0.6, "sfx": "whoosh"},
                     {"type": "image", "svg": cal("OCT", "15", top="#3f7fbf"), "x": 0.72, "y": 0.27, "w": 0.36, "rotate": 4,
                      "enter": "pop", "at": 2.6, "sfx": "pop"},
                     {"type": "stamp", "text": "10 DAYS DELETED", "tone": "red", "angle": -6, "size": 62, "x": 0.5, "y": 0.47,
                      "at": 1.4, "sfx": "thud"},
                     dict(close_ved([["explain", 0], ["point", 1.4], ["smirk", 3.0]]), y=0.95, h=0.42, x=0.5)]})
# 8. close Ved: the century rule
S.append({"say": "That's why *1900* had no leap day. *2000* did.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("clock_up", blur=10, keys=[{"t": 0, "scale": 1.3}, {"t": 3.6, "scale": 1.36}]),
                     close_ved([["explain", 0], ["point", 1.2], ["warm", 2.6]]),
                     {"type": "optcard", "label": "leap year?", "text": "1900", "tone": "red", "x": 0.27, "y": 0.14,
                      "w": 0.37, "rotate": -3, "enter": "pop", "at": 0.3, "sfx": "pop", "verdict": "cross", "verdict_at": 0.5},
                     {"type": "optcard", "label": "leap year?", "text": "2000", "tone": "green", "x": 0.71, "y": 0.14,
                      "w": 0.37, "rotate": 3, "enter": "pop", "at": 1.6, "sfx": "pop", "verdict": "tick", "verdict_at": 0.4},
                     txt("CENTURY: ONLY IF / 400", 0.255, 44, enter="pop", at=2.4, sfx="pop")]})
# 9. payoff: back to space: without Feb 29, summer lands in December
S.append({"say": "Without it, in *750 years*, summer lands in *December*.",
          "transition": "zoom", "caption_y": 0.62, "sfx": "ding",
          "camera": {"keys": [{"t": 0, "zoom": 1.12, "focus": [0.5, 0.55]}, {"t": 4.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("orbit_wide"),
                     {"type": "image", "svg": SEASONS, "x": 0.5, "y": 0.17, "w": 0.7, "enter": "pop", "at": 1.6, "sfx": "pop"},
                     {"type": "image", "svg": cal("FEB", "29", ring=True), "x": 0.2, "y": 0.75, "w": 0.2, "rotate": -6,
                      "enter": "pop", "at": 0.2, "sfx": "pop"},
                     tag_layer(0.78, 0.75, 2.8, "MATHS", "#f2b04a")]})

job = {"id": ID, "title": "A year isn't 365 days. That's why Feb 29 exists 📅",
       "description": "Why do we have leap years? A year isn't 365 days: Earth takes about 365 days and 6 hours (365.2422 days) "
                      "to go round the Sun. Ignore the extra hours and the calendar slips a day every 4 years, so Julius "
                      "Caesar's calendar (45 BC) added February 29 every 4 years. But that's about 11 minutes a year too much, "
                      "and by 1582 the seasons had drifted 10 days. Pope Gregory XIII's reform deleted them: Thursday 4 October "
                      "1582 was followed by Friday 15 October, and century years became leap years only if divisible by 400 "
                      "(1900 wasn't, 2000 was). Without leap days, the seasons would flip in about 750 years.\n\n"
                      "Sources: OpenStax Astronomy 2e, 4.4 The Calendar; Britannica, The Gregorian calendar; "
                      "Atlas Obscura, When the Pope made 10 days disappear.",
       "tags": ["leap year", "why do we have leap years", "february 29", "gregorian calendar", "julian calendar",
                "calendar history", "astronomy", "science facts", "explained"],
       "hashtags": ["#science", "#space"],
       "instagram": {"hashtags": ["#science", "#leapyear", "#calendar", "#astronomy", "#explained"]},
       "meta": {"format": "big-question", "topic": "why leap years exist: a year is ~365.2422 days (365 d + ~6 h); without the extra "
                                                   "day the calendar slips 1 day every 4 years; Julian calendar (Caesar, 45 BC) "
                                                   "adds Feb 29 every 4 years but is ~11 min/yr too long; by 1582 seasons drifted "
                                                   "10 days; Gregory XIII: 4 Oct 1582 -> 15 Oct; century rule (1900 no, 2000 yes); "
                                                   "no leap days = seasons flip in ~750 years",
                "hook": "you've been told X",
                "idea_source": "viral-shaped + unique: everyone knows Feb 29 but almost nobody knows the 6-hours / 11-minutes / "
                               "deleted-10-days story; a physical, picturable big-question (Earth's lap); backlog idea; second "
                               "test of the 'you've been told X' hook (this week's experiment)",
                "characters": ["ved", "extra"],
                "sources": ["https://openstax.org/books/astronomy/pages/4-4-the-calendar",
                            "https://www.britannica.com/science/calendar/The-Gregorian-calendar",
                            "https://atlasobscura.com/articles/when-the-pope-made-10-days-disappear",
                            "https://time.com/4237292/leap-year-leap-day-history/",
                            "https://lighthouse.mq.edu.au/article/please-explain/may-2021/Please-explain-Why-do-we-have-leap-years"],
                "humour": {"trend": "timeless dry aside (no fresh rising meme fits; this week's cards already used): side-eye + "
                                    "'Caesar: close enough' on the 11-minute error",
                           "beat": "side_eye", "scene": 5},
                "claims": [
                    {"claim": "a tropical year is about 365.2422 days, roughly 365 days and 6 hours", "tag": "PROVEN",
                     "source": "https://openstax.org/books/astronomy/pages/4-4-the-calendar"},
                    {"claim": "the Julian calendar (Julius Caesar, 45 BC) added a leap day every 4 years (365.25 days), about 11 minutes a year too long", "tag": "PROVEN",
                     "source": "https://openstax.org/books/astronomy/pages/4-4-the-calendar"},
                    {"claim": "by 1582 the equinox had drifted about 10 days", "tag": "PROVEN",
                     "source": "https://www.britannica.com/science/calendar/The-Gregorian-calendar"},
                    {"claim": "Gregory XIII's reform: 4 October 1582 was followed by 15 October 1582", "tag": "PROVEN",
                     "source": "https://atlasobscura.com/articles/when-the-pope-made-10-days-disappear"},
                    {"claim": "century years are leap years only if divisible by 400: 1900 was not, 2000 was", "tag": "PROVEN",
                     "source": "https://openstax.org/books/astronomy/pages/4-4-the-calendar"},
                    {"claim": "without leap days a 365-day calendar slips ~0.24 day a year, half a year (~183 days) in ~750 years", "tag": "PROVEN",
                     "source": "arithmetic from 365.2422 days"}]},
       "thumbnail": {"title": "365 DAYS? *NOPE*", "title_y": 0.2, "title_size": 150, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.3,
                     "tint": ["#2f8fe0", "#f08a24"], "tint_amount": 0.25,
                     "bg": [plate("plaza_mid")],
                     "fg": [{"type": "image", "svg": cal("FEB", "29", ring=True), "x": 0.2, "y": 0.45, "w": 0.3, "rotate": -8, "enter": "none"},
                            sprite("earth", 0.82, 0.43, 0.26),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
