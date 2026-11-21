"""Find the Kokoro voice (or blend of voices) that sounds nearest to a reference recording, fully offline.
Speaker likeness is measured with a WeSpeaker ResNet34 speaker-embedding model (Apache-2.0, via sherpa-onnx), and pitch
with pYIN. Search: every male voice reading the same words, then blends of the best four, speed and pitch shift.
Run: python scripts/voice_match.py <recording> [--text "what the recording says"] [--out /tmp/voice_match]
Writes best.json (the voice spec for channel/style.json or character.json) and sample WAVs to compare by ear.
The model downloads from huggingface.co/csukuangfj/speaker-embedding-models the first time.
"""
import argparse, json, os, sys, urllib.request
import numpy as np, soundfile as sf, soxr
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autopilot import audio  # noqa: E402

MODEL_URL = "https://huggingface.co/csukuangfj/speaker-embedding-models/resolve/main/wespeaker_en_voxceleb_resnet34_LM.onnx"
MODEL = os.path.expanduser("~/.cache/autopilot/wespeaker_resnet34_LM.onnx")
_EX = None


def extractor():
    global _EX
    if _EX is None:
        import sherpa_onnx
        if not os.path.exists(MODEL):
            os.makedirs(os.path.dirname(MODEL), exist_ok=True)
            urllib.request.urlretrieve(MODEL_URL, MODEL + ".part"); os.replace(MODEL + ".part", MODEL)
        _EX = sherpa_onnx.SpeakerEmbeddingExtractor(sherpa_onnx.SpeakerEmbeddingExtractorConfig(model=MODEL, num_threads=2))
    return _EX


def embed(x, sr):
    x = soxr.resample(np.asarray(x, np.float64), sr, 16000).astype(np.float32)
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    ex = extractor(); st = ex.create_stream(); st.accept_waveform(16000, x); st.input_finished()
    e = np.array(ex.compute(st)); return e / (np.linalg.norm(e) + 1e-9)


def f0(x, sr):
    import librosa
    y = soxr.resample(np.asarray(x, np.float64), sr, 16000)
    f, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=16000, frame_length=1024)
    f = f[~np.isnan(f)]; return float(np.median(f)) if len(f) else 0.0


def say(text, voice, speed=1.0, pitch=0.0, lang="en-us"):
    return audio.narrator(text, voice, speed=speed, lang=lang, pitch=pitch) if pitch else audio.tts(text, voice, speed, lang)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("ref"); ap.add_argument("--text", default=None)
    ap.add_argument("--out", default="/tmp/voice_match"); ap.add_argument("--tries", type=int, default=48)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    ref, sr = sf.read(a.ref)
    if ref.ndim > 1: ref = ref.mean(axis=1)
    E, F = embed(ref, sr), f0(ref, sr)
    text = a.text or "Hello, this is how I sound. Every video on this channel should sound like this."
    print(f"reference: {len(ref) / sr:.1f} s, median pitch {F:.0f} Hz")
    k = audio.kokoro()
    males = [v for v in k.get_voices() if v[1] == "m" and v[0] in "abhipe"]       # English, Hindi, Italian, Portuguese, Spanish male
    score = lambda x: (float(np.dot(embed(x, audio.SR), E)))  # noqa: E731
    rank = []
    for v in males:
        for lang in (["en-us", "en-gb"] if v[0] in "bh" else ["en-us"]):
            try:
                x = say(text, v, lang=lang)
            except Exception:
                continue
            rank.append((score(x), v, lang, f0(x, audio.SR)))
    rank.sort(reverse=True)
    for s, v, l, p in rank[:8]:
        print(f"  {v:10s} {l}  likeness {s:.3f}  pitch {p:.0f} Hz")
    top = rank[:4]
    best = {"score": top[0][0], "voice": top[0][1], "lang": top[0][2], "speed": 1.0, "pitch": 0.0}
    rng = np.random.default_rng(7)
    for i in range(a.tries):                                                     # blends of the best four + speed + pitch
        w = rng.dirichlet(np.ones(len(top)) * 0.8)
        spec = ",".join(f"{v}:{wi:.2f}" for (_, v, _, _), wi in zip(top, w) if wi >= 0.05)
        lang = top[int(np.argmax(w))][2]
        sp = float(rng.choice([0.92, 0.96, 1.0, 1.04]))
        x0 = say(text, spec, sp, 0.0, lang)
        st = 12 * np.log2(max(F, 1) / max(f0(x0, audio.SR), 1))                  # pitch shift toward the reference
        pt = float(np.clip(round(st * 2) / 2, -3, 3))
        x = say(text, spec, sp, pt, lang) if pt else x0
        s = score(x)
        if s > best["score"]:
            best = {"score": s, "voice": spec, "lang": lang, "speed": sp, "pitch": pt}
            print(f"  better {s:.3f}: {spec} speed {sp} pitch {pt:+.1f} st")
    cur = say(text, "bm_george", 1.0, 0.0, "en-gb")
    best["ved_now_score"] = score(cur)
    sf.write(os.path.join(a.out, "reference.wav"), ref / (np.abs(ref).max() + 1e-9) * 0.9, sr)
    sf.write(os.path.join(a.out, "nearest_single.wav"), say(text, top[0][1], 1.0, 0.0, top[0][2]), audio.SR)
    sf.write(os.path.join(a.out, "nearest_blend.wav"), say(text, best["voice"], best["speed"], best["pitch"], best["lang"]), audio.SR)
    sf.write(os.path.join(a.out, "ved_now_bm_george.wav"), cur, audio.SR)
    best["reference_pitch_hz"] = round(F, 1); best["ranking"] = [(round(s, 3), v, l) for s, v, l, _ in rank[:8]]
    json.dump(best, open(os.path.join(a.out, "best.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in best.items() if k != "ranking"}, indent=1))


if __name__ == "__main__":
    main()
