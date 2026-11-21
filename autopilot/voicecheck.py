"""The voice check: every line Ved speaks is transcribed back (faster-whisper, offline once the model is cached) and
compared with the script, so a mispronounced, swallowed or garbled word is caught before posting (learned from
Lemo-Opuscar's speech-to-text check; our own code). Measured, never blocking: out/voice.json and a `voice:` log line.
The model (~145 MB, base.en) downloads from huggingface.co the first time.
"""
import difflib
import json
import os
import re

import numpy as np

MODEL = os.environ.get("VOICE_CHECK_MODEL", "base.en")
_M = None


def model():
    global _M
    if _M is None:
        from faster_whisper import WhisperModel
        _M = WhisperModel(MODEL, device="cpu", compute_type="int8")
    return _M


def _num(tok):
    from num2words import num2words
    t = tok.replace(",", "")
    try:
        if re.fullmatch(r"(1[0-9]|20)\d\d", t):                    # 2012 -> twenty twelve (how years are read)
            return num2words(int(t), to="year")
        if re.fullmatch(r"\d+(\.\d+)?", t):
            return num2words(float(t) if "." in t else int(t))
    except Exception:
        pass
    return tok


def words(text):
    """Normalised word list: lowercase, numbers spelled out, %/₹/$ as words, punctuation gone."""
    t = text.replace("*", "").replace("%", " percent").replace("₹", " rupees ").replace("$", " dollars ")
    t = re.sub(r"(\d),(\d)", r"\1\2", t)
    out = []
    for tok in re.findall(r"[A-Za-z']+|\d+(?:\.\d+)?", t):
        tok = _num(tok) if tok[0].isdigit() else tok
        out += re.findall(r"[a-z']+", tok.lower().replace("-", " "))
    return [w.strip("'") for w in out if w.strip("'")]


def score(said, heard):
    """Word accuracy 0-1 and the words of the script that were not heard."""
    a, b = words(said), words(heard)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    hit = sum(m.size for m in sm.get_matching_blocks())
    missing = [a[i] for tag, i1, i2, _, _ in sm.get_opcodes() if tag in ("replace", "delete") for i in range(i1, i2)]
    return (hit / len(a) if a else 1.0), missing


def check(ctx, out_dir, log=print, sr=None):
    from . import audio
    sr = sr or audio.SR
    m = model()
    rep, bad = [], 0
    for i, s in enumerate(ctx.job["scenes"]):
        say = s.get("say", "")
        if not say.strip():
            continue
        x = np.asarray(ctx.vo[i], dtype=np.float32)
        if sr != 16000:
            x = audio.resample(x, sr, 16000)
        segs, _ = m.transcribe(x, language="en", beam_size=3, vad_filter=False, condition_on_previous_text=False)
        heard = " ".join(g.text for g in segs).strip()
        acc, miss = score(say, heard)
        ok = acc >= 0.85 and len(miss) <= 1
        bad += not ok
        rep.append({"scene": i, "said": audio.clean_for_tts(say), "heard": heard, "accuracy": round(acc, 2),
                    "missing": miss, "ok": ok})
    with open(os.path.join(out_dir, "voice.json"), "w") as f:
        json.dump(rep, f, indent=1, ensure_ascii=False)
    worst = min(rep, key=lambda r: r["accuracy"]) if rep else None
    log(f"voice: {len(rep) - bad}/{len(rep)} lines heard back clearly"
        + (f"; check scene {worst['scene']}: heard \"{worst['heard'][:60]}\"" if bad else ""))
    return rep
