"""2026-11-17-a: How hawala moves money without moving money (dark-files, night look, documentary view, no how-to).
Set: two broker kiosks in the night arena, NEW YORK (left) and LAHORE (right), a fictional dotted route on the far wall.
Cast (fixed outfits): Amir (sender, NY), Mohammad (NY broker), Shirin (Lahore broker), Iqbal (Amir's cousin, Lahore).
New + old pieces mixed: Ved and the townspeople, a cream ledger card, hud chips, optcards with tick/cross, stamps,
a live fictional phone chat with the code word, note bursts (NOT REAL MONEY), comic beat.
Facts: CFI hawala explainer (password, broker pays from own funds, debt between brokers, settled in cash/goods/services);
ClearTax (illegal in India under FEMA; brokers settle later by offsetting); UNODC 2023 ('we don't ask questions');
FATF Sept 2026 report (nearly 90% of jurisdictions reported underground banking/HOSSPs; commissions 0.5-5%).
Run: python jobs/2026-11-17-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-17-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("wide", "ny", "lh", "hero")}
NOTES = [A + "note1.png", A + "note2.png", A + "coin.png"]
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"

OUT = {
    "amir": {"skin": "#c68a5e", "build": "regular", "hair": ["#1a1410", "short"], "hat": ["cap", "#d9534f"],
             "top": ["#3f7fbf", "jacket"], "bottom": ["#34383f", "trousers"], "shoes": "#151515", "bag": "#8a5a3c"},
    "mohammad": {"skin": "#b07850", "build": "round", "hair": ["#2a2320", "short"], "hat": ["fez", "#7c2533"],
                 "top": ["#f6efe2", "vest"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "tie": "#7c2533"},
    "shirin": {"skin": "#c98e62", "build": "slim", "hair": ["#1a1410", "bun"], "hat": ["headscarf", "#46965a"],
               "top": ["#f2b04a", "kurta"], "bottom": ["#2f3a52", "trousers"], "shoes": "#25262b", "earrings": "#f2b04a"},
    "iqbal": {"skin": "#a86f48", "build": "slim", "hair": ["#1a1410", "curly"], "top": ["#6fc3c0", "kurta"],
              "bottom": ["#e9e6df", "trousers"], "shoes": "#2b2b30"},
}
# floor spots (metres): brokers behind their counters, customers in front
SPOT = {"mohammad": (-2.39, 1.27), "amir": (-1.45, 0.15), "shirin": (2.39, 1.27), "iqbal": (1.45, 0.15)}


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def person(set_, who, acting, pos=None, walk=None, **k):
    st = ST[set_]
    wx, wy = pos or SPOT[who]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    L.update(k)
    return L


def ved(set_, wx, wy, acting, walk=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    L.update(k)
    return L


def close_ved(acting, x=0.5, y=0.8, h=1.06, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def txt(t, y, size=110, **k):
    return {"type": "text", "text": t, "font": "display", "x": k.pop("x", 0.5), "y": y, "size": size, "max_w": k.pop("max_w", 0.88),
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def hud(label, y, **k):
    return {"type": "hud", "label": label, "x": k.pop("x", 0.5), "y": y, "enter": "pop", "sfx": "click", **k}


def label_svg(word, color, w):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 96'><rect x='4' y='4' width='{w-8}' height='88' rx='20' "
            f"fill='#0b1424' fill-opacity='0.85' stroke='{color}' stroke-width='5'/><text x='{w/2}' y='68' text-anchor='middle' "
            f"font-size='56' fill='{color}' {AN}>{word}</text></svg>")


def honesty(word, x, y, at=0.0, color="#35e08a"):
    return {"type": "image", "svg": label_svg(word, color, 300), "x": x, "y": y, "w": 0.2, "enter": "pop", "at": at, "rotate": -4}


def card(body, w=900, h=300):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{body}</svg>")


# the cream ledger card: the only thing that 'travels' is a line in a book
LEDGER = card(f"<text x='450' y='70' text-anchor='middle' font-size='44' fill='#7c2533' {AN}>THE LEDGER</text>"
              "<line x1='60' y1='92' x2='840' y2='92' stroke='#1a1410' stroke-width='4'/>"
              f"<text x='70' y='170' font-size='58' fill='#2a6fbf' {AN}>NEW YORK</text>"
              f"<text x='450' y='170' text-anchor='middle' font-size='40' fill='#34425c' {F}>owes</text>"
              f"<text x='830' y='170' text-anchor='end' font-size='58' fill='#2a8a5a' {AN}>LAHORE</text>"
              f"<text x='450' y='256' text-anchor='middle' font-size='76' fill='#b8860b' {AN}>$1,000</text>", 900, 290)

CHAT_NY = {"kind": "chat", "name": "Amir", "sub": "to: cousin Iqbal",
           "msgs": [{"text": "Sent $1,000 for you", "side": "out", "time": "9:40", "at": 0.3},
                    {"text": "Code word: MANGO-7", "side": "out", "time": "9:41", "at": 1.0}]}
CHAT_LH = {"kind": "chat", "name": "Broker, Lahore", "sub": "counter 2",
           "msgs": [{"text": "Code word?", "side": "in", "time": "9:52", "at": 0.2},
                    {"text": "MANGO-7", "side": "out", "time": "9:52", "at": 0.8, "badge": "MATCH"}]}

S = []
# 0. hook: frame 0 already shows the claim; Ved walks into the spotlight between the two kiosks
S.append({"say": "A thousand dollars just crossed a border. Not one note moved.",
          "caption": "$1,000 just crossed a border. Not one note moved.",
          "layers": [plate("hero"),
                     ved("hero", 0.15, -1.3, [["welcome", 0], ["point", 1.8], ["crossed", 3.2]],
                         walk=[(0, 1.6, -1.8), (1.0, 0.15, -1.3)]),
                     txt("$1,000 SENT.\n*ZERO* NOTES MOVED.", 0.17, 116, enter="none"),
                     hud("new york  >  lahore", 0.31, prefix="$", value=1000, tone="gold", at=0.0, enter="none"),
                     {"type": "stamp", "text": "NO CASH TRAVELLED", "tone": "red", "angle": -7, "size": 62, "x": 0.5,
                      "y": 0.52, "at": 2.4, "sfx": "thud"}],
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.07, "focus": [0.5, 0.5]}]},
          "caption_y": 0.72, "sfx": "footsteps", "sfx_at": 0.0})
# 1. New York: Amir hands Mohammad the cash; the code word goes to his cousin by phone
S.append({"say": "In New York, Amir hands a broker cash and a password.",
          "transition": "push", "transition_frames": 10, "caption_y": 0.74,
          "layers": [plate("ny"),
                     person("ny", "mohammad", [["idle", 0], ["take", 1.0], ["hold", 2.2]]),
                     fg("ny"),
                     person("ny", "amir", [["give", 0], ["idle", 1.6], ["hold", 2.4]]),
                     {"type": "image", "path": A + "note1.png", "x": 0.52, "y": 0.66, "w": 0.2, "enter": "pop", "at": 0.3,
                      "sfx": "cash", "keys": [{"t": 0, "x": 0.56, "y": 0.66, "rot": -8}, {"t": 0.9, "x": 0.36, "y": 0.6, "rot": 6}],
                      "until": 1.4, "exit": "fade"},
                     {"type": "phone", "sprite": A + "phone.png", "screen": CHAT_NY, "x": 0.72, "y": 0.27, "w": 0.27,
                      "tilt": [[0, -18, 4], [3.0, 8, 2]], "enter": "rise", "at": 1.2, "sfx": "swoosh_soft"},
                     {"type": "hud", "label": "new york", "text": "BROKER 1", "tone": "blue", "x": 0.26, "y": 0.13,
                      "enter": "pop", "at": 0.1, "sfx": "click"}],
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.06, "focus": [0.46, 0.52]}]}})
# 2. Lahore: Shirin pays Iqbal from her own drawer once the code word matches
S.append({"say": "In Lahore, another broker pays his cousin from her own drawer.",
          "transition": "push", "transition_frames": 10, "caption_y": 0.74,
          "layers": [plate("lh"),
                     person("lh", "shirin", [["idle", 0], ["give", 1.2], ["happy", 2.6]]),
                     fg("lh"),
                     person("lh", "iqbal", [["idle", 0], ["take", 1.4], ["cheer", 2.6]], hops=[[2.7, 0.05, 0.4]]),
                     {"type": "image", "path": A + "note2.png", "x": 0.5, "y": 0.6, "w": 0.2, "enter": "pop", "at": 1.2,
                      "sfx": "cash", "keys": [{"t": 0, "x": 0.5, "y": 0.6, "rot": 6}, {"t": 0.9, "x": 0.66, "y": 0.68, "rot": -10}],
                      "until": 2.4, "exit": "fade"},
                     {"type": "phone", "sprite": A + "phone.png", "screen": CHAT_LH, "x": 0.28, "y": 0.27, "w": 0.27,
                      "tilt": [[0, 18, 4], [3.0, -8, 2]], "enter": "rise", "at": 0.1, "sfx": "swoosh_soft"},
                     {"type": "hud", "label": "paid from her own cash", "prefix": "$", "to": 1000, "count_dur": 0.8,
                      "tone": "green", "x": 0.7, "y": 0.13, "enter": "pop", "at": 1.4, "sfx": "ding"},
                     honesty("PROVEN", 0.8, 0.64, at=2.2)],
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.06, "focus": [0.54, 0.52]}]}})
# 3. wide: nothing flew, only a line in a ledger
S.append({"say": "No money flew. Just a debt: New York owes Lahore.",
          "transition": "cut",
          "layers": [plate("wide"),
                     person("wide", "mohammad", [["idle", 0], ["shrug", 1.4]]),
                     person("wide", "shirin", [["idle", 0], ["point", 1.4]]),
                     fg("wide"),
                     person("wide", "amir", [["idle", 0]]),
                     person("wide", "iqbal", [["happy", 0]]),
                     ved("wide", 0.0, -2.2, [["explain", 0], ["point", 1.6]]),
                     {"type": "optcard", "label": "cash in the air", "text": "$0", "tone": "red", "x": 0.5, "y": 0.25,
                      "w": 0.36, "enter": "pop", "at": 0.2, "sfx": "pop", "verdict": "cross", "verdict_at": 0.8},
                     {"type": "image", "svg": LEDGER, "x": 0.5, "y": 0.7, "w": 0.66, "enter": "pop", "at": 1.4, "sfx": "paper",
                      "rotate": -2}],
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.0, "focus": [0.5, 0.5]}]}})
# 4. how the brokers square up later
S.append({"say": "They settle later, with goods or payments going the other way.",
          "transition": "cut",
          "layers": [plate("wide", blur=6),
                     {"type": "image", "svg": LEDGER, "x": 0.5, "y": 0.2, "w": 0.6, "enter": "none", "rotate": -2},
                     {"type": "optcard", "label": "settle by", "text": "GOODS\n(TRADE)", "tone": "gold", "x": 0.28, "y": 0.6,
                      "w": 0.38, "enter": "pop", "at": 1.0, "sfx": "pop", "rotate": -3, "verdict": "tick", "verdict_at": 1.5},
                     {"type": "optcard", "label": "settle by", "text": "A TRANSFER\nTHE OTHER WAY", "tone": "blue", "x": 0.68,
                      "y": 0.6, "w": 0.38, "enter": "pop", "at": 2.0, "sfx": "pop", "rotate": 3, "verdict": "tick",
                      "verdict_at": 2.5},
                     {"type": "eqbar", "keys": [[0.4, "NY owes LHR $1,000"], [2.6, "$1,000 - $1,000 = *$0*"]],
                      "tone": "gold", "x": 0.5, "y": 0.34, "enter": "fade"}],
          "caption_y": 0.45})
# 5. why people use it: hero, Ved, three ticks
S.append({"say": "Cheap, fast, built on trust.",
          "transition": "push", "transition_frames": 10, "min_dur": 2.4, "caption_y": 0.72,
          "layers": [plate("hero"),
                     ved("hero", 0.15, -1.3, [["explain", 0], ["point", 1.2]]),
                     {"type": "tracker", "n": 3, "done": [0.2, 0.7, 1.3], "x": 0.5, "y": 0.13, "enter": "fade"},
                     hud("typical fee", 0.25, text="0.5-5%", tone="green", at=0.4, sub="FATF report, Sept 2026")]})
# 6. legality: licensed vs illegal
S.append({"say": "Licensed in some countries. Illegal in others, like India.",
          "transition": "cut", "caption_y": 0.72,
          "layers": [plate("hero", blur=4),
                     ved("hero", 0.15, -1.3, [["explain", 0], ["crossed", 2.0]]),
                     {"type": "optcard", "label": "some countries", "text": "LICENSED\nBROKERS", "tone": "green", "x": 0.29,
                      "y": 0.2, "w": 0.38, "enter": "pop", "at": 0.1, "sfx": "pop", "rotate": -3, "verdict": "tick",
                      "verdict_at": 0.7},
                     {"type": "optcard", "label": "india (FEMA)", "text": "HAWALA\nIS ILLEGAL", "tone": "red", "x": 0.68,
                      "y": 0.2, "w": 0.38, "enter": "pop", "at": 1.5, "sfx": "pop", "rotate": 3, "verdict": "cross",
                      "verdict_at": 2.1},
                     honesty("PROVEN", 0.5, 0.33, at=2.4)]})
# 7. the dark side: the UN quote
S.append({"say": "And criminals love it. One broker told the UN: we don't ask questions.",
          "caption": "And criminals love it. One broker told the UN: \"we don't ask questions.\"",
          "transition": "dip", "transition_frames": 8, "caption_y": 0.72,
          "layers": [plate("ny"),
                     person("ny", "mohammad", [["idle", 0], ["shrug", 2.4]]),
                     fg("ny"),
                     hud("countries that reported it", 0.17, text="9 in 10", tone="red", at=0.3,
                         sub="FATF survey, 2026"),
                     {"type": "stamp", "text": "\"WE DON'T ASK QUESTIONS\"", "tone": "red", "angle": -6, "size": 58,
                      "x": 0.5, "y": 0.27, "at": 2.6, "sfx": "thud"},
                     {"type": "image", "svg": label_svg("UNODC, 2023", "#f6efe2", 420), "x": 0.5, "y": 0.35,
                      "w": 0.3, "enter": "pop", "at": 3.0}],
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.5]}]}})
# 8. comic beat: reaction cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("hero", blur=12, keys=[{"t": 0, "scale": 1.3}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved",
                   "text": "my type quiz result:\n*doesn't ask questions*", "text_y": 0.2}})
# 9. payoff, loops back to the hook
S.append({"say": "The money never moved. The trust did.",
          "transition": "push", "transition_frames": 10, "min_dur": 3.0,
          "layers": [plate("wide"),
                     person("wide", "mohammad", [["idle", 0], ["wave", 1.0]]),
                     person("wide", "shirin", [["idle", 0], ["wave", 1.0]]),
                     fg("wide"),
                     ved("wide", 0.0, -2.2, [["point", 0], ["smirk", 1.8]]),
                     {"type": "burst", "sprites": NOTES, "n": 18, "origin": [0.5, 0.56], "at": 0.2, "dur": 1.8, "spread": 0.9,
                      "sfx": "cash", "sizes": [1.0, 1.0, 0.45]},
                     txt("MONEY *STAYED*\nTRUST *MOVED*", 0.25, 110, enter="pop", at=1.2, sfx="ding")]})

job = {
    "id": ID,
    "title": "$1,000 crossed a border. No money moved 🤝",
    "description": "Hawala, explained: a sender in New York gives a broker cash and a code word, a second broker in Lahore pays "
                   "the cousin from her own cash, and only a debt is left between the brokers, settled later with goods or "
                   "transfers the other way. Cheap, fast and built on trust: licensed in some countries, illegal in others "
                   "(including India), and, as a UN study found, also used by criminals. A documentary explainer, not advice.\n\n"
                   "Sources: Corporate Finance Institute (Hawala); ClearTax (Hawala in India, FEMA); UNODC (2023) on hawala and "
                   "organised crime; FATF report on underground banking and hawala (Sept 2026).",
    "tags": ["hawala", "hawala explained", "how hawala works", "underground banking", "money laundering", "fatf",
             "remittance", "dark files", "explained"],
    "hashtags": ["#hawala", "#money"],
    "instagram": {"hashtags": ["#money", "#hawala", "#moneylaundering", "#truecrime", "#explained"]},
    "look": "night",
    "meta": {"format": "dark-files", "topic": "how hawala moves money across borders without moving money: code word, broker "
                                              "pays from own cash, debt between brokers settled later (goods / reverse "
                                              "transfers), cheap/fast/trust, licensed vs illegal (India, FEMA), criminal use "
                                              "(UNODC 'we don't ask questions'), FATF 2026: ~9 in 10 jurisdictions report it",
             "hook": "number-shock",
             "idea_source": "unique + trending: backlog runner-up twice (owner's dark-files examples); FATF's Sept 2026 report "
                            "on underground banking and 'digital hawala' is in the news; strong India-audience topic; rarely "
                            "explained visually in Shorts",
             "characters": ["ved", "extra"],
             "sources": ["https://corporatefinanceinstitute.com/resources/wealth-management/hawala/",
                         "https://cleartax.in/s/hawala-money",
                         "https://unodc.org/unodc/frontpage/2023/September/we-dont-ask-questions_-hawala-payment-system-vulnerable-to-use-by-organized-crime-groups--including-opiate-traffickers-and-migrant-smugglers.html",
                         "https://www.zigram.tech/?p=41971",
                         "https://www.drishtiias.com/daily-updates/daily-news-analysis/fatf-report-on-underground-banking-and-digital-hawala"],
             "claims": [{"claim": "sender gives a broker cash + a password; a broker in the other city pays the recipient from own funds once the password matches", "tag": "PROVEN", "source": "CFI; ClearTax"},
                        {"claim": "no physical money moves; the brokers owe each other and settle later via cash, goods, services or offsetting transfers", "tag": "PROVEN", "source": "CFI; ClearTax"},
                        {"claim": "typical commissions 0.5-5%", "tag": "PROVEN", "source": "FATF Sept 2026 report via Zigram"},
                        {"claim": "licensing frameworks exist in many countries; hawala is illegal in India under FEMA", "tag": "PROVEN", "source": "UNODC 2023; ClearTax"},
                        {"claim": "a Somali hawaladar told UNODC researchers 'we don't ask questions'", "tag": "PROVEN", "source": "UNODC 2023"},
                        {"claim": "nearly 90% of jurisdictions in the FATF survey reported underground banking / hawala-type providers", "tag": "PROVEN", "source": "FATF Sept 2026 via Drishti IAS / Zigram"}],
             "humour": {"trend": "'My Type Quiz' (mytype.fyi, viral on X early-mid Nov 2026, Know Your Meme 13 Nov): 'my type quiz result: doesn't ask questions'",
                        "beat": "side_eye", "scene": 8}},
    "thumbnail": {"title": "NO MONEY *MOVED?*", "title_y": 0.14, "title_size": 170, "max_w": 0.95, "blur": 10,
                  "glow": "#f4c04e", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.2, "bg_saturation": 1.2,
                  "bg": [plate("wide")],
                  "fg": [{"type": "image", "path": A + "note1.png", "x": 0.26, "y": 0.5, "w": 0.38, "rotate": -12, "enter": "none"},
                         {"type": "character", "id": "ved", "pose": "surprised", "x": 0.66, "y": 0.93, "h": 0.85, "enter": "none",
                          "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
    "music": {"cues": [{"scene": 0, "style": "tension", "key": "E", "scale": "minor", "bpm": 92}], "volume": 0.12},
    "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
for sc in S:
    if "say" in sc:
        sc.setdefault("pad", 0.14); sc.setdefault("lead", 0.06)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "words", sum(len(s.get("say", "").split()) for s in S))
