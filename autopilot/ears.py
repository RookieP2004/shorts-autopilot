"""Ears for the pipeline (owner, 2026-11-21: use earshot + the Real SFX checks). Claude cannot hear a render, so every
render is MEASURED and the numbers go into out/ears.json and the run log:

- loudness of the final mix (integrated LUFS, true peak, loudness range) against style.loudness_lufs, via `earshot measure`
- sync: for every sound-effect cue, where its peak actually lands in the effects stem vs the frame it was meant for
- clutter: effects closer than 0.25 s to each other; holes: stretches over 6 s with no effect at all (dead air in a Short)
- balance: effects against the voice (stems), so effects never bury Ved and never vanish under the music

A finding is a warning, never a failure: the run posts anyway; the weekly review reads the numbers.
"""
import json
import os
import shutil
import subprocess

import numpy as np

from . import audio


def measure(path):
    """earshot's model-free measurements (LUFS, true peak, LRA, onsets...). None if earshot is not installed."""
    if not shutil.which("earshot"):
        return None
    r = subprocess.run(["earshot", "measure", path, "--json"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def _db(x):
    return 20 * np.log10(max(1e-9, float(x)))


def check(ctx, final_mp4, out_dir, log=print):
    st = ctx.style
    rep = {"target_lufs": st["loudness_lufs"]}
    m = measure(final_mp4)
    if m:
        rep.update({k: m.get(k) for k in ("lufs", "true_peak_dbtp", "lra", "duration") if k in m})
    warn = []
    if m and m.get("lufs") is not None and abs(m["lufs"] - st["loudness_lufs"]) > 1.5:
        warn.append(f"loudness {m['lufs']:.1f} LUFS vs target {st['loudness_lufs']}")
    if m and m.get("true_peak_dbtp") is not None and m["true_peak_dbtp"] > -1.0:
        warn.append(f"true peak {m['true_peak_dbtp']:.1f} dBTP (over -1)")
    fx = getattr(ctx, "fx_stem", None)
    cues = getattr(ctx, "sfx_cues", [])
    sync = []
    if fx is not None and cues:
        k = max(1, int(0.008 * audio.SR))
        env = np.convolve(np.abs(fx), np.ones(k) / k, mode="same")
        for t, nm, at, pk in cues:
            if nm not in audio.PEAK_SYNC:               # runs and beds (typing, steps, whooshes) have no single peak to sync
                continue
            a, b = int(max(0, t - 0.08) * audio.SR), int(min(len(env), (t + 0.12) * audio.SR))
            if b <= a:
                continue
            real = (a + int(np.argmax(env[a:b]))) / audio.SR
            sync.append({"t": round(t, 3), "sfx": nm, "drift_ms": round((real - t) * 1000)})
        drifts = [abs(s["drift_ms"]) for s in sync]
        if drifts:
            rep["sync_median_ms"] = int(np.median(drifts))
            rep["sync_worst"] = max(sync, key=lambda s: abs(s["drift_ms"]))
            late = [s for s in sync if abs(s["drift_ms"]) > 60]
            if late:
                warn.append(f"{len(late)} effects land more than 60 ms off their frame (worst {rep['sync_worst']})")
        times = [c[0] for c in cues]
        rep["sfx_count"] = len(cues)
        rep["clutter"] = sum(1 for a_, b_ in zip(times, times[1:]) if b_ - a_ < 0.25)
        rep["sfx_dropped"] = getattr(ctx, "sfx_dropped", [])      # removed by the one-at-a-time rule (overlap / busy)
        vo = getattr(ctx, "vo_stem", None)
        if vo is not None and len(vo) == len(fx):                   # how far the voice stands over the effects while he speaks
            w = int(0.4 * audio.SR)
            ev = np.sqrt(np.convolve(vo ** 2, np.ones(w) / w, mode="same"))
            ef = np.sqrt(np.convolve(fx ** 2, np.ones(w) / w, mode="same"))
            sp = (ev > np.percentile(ev, 40)) & (ef > ev * 10 ** (-40 / 20))   # moments when he speaks AND an effect plays
            if sp.any():
                rep["voice_over_sfx_db"] = round(float(np.median(20 * np.log10((ev[sp] + 1e-9) / (ef[sp] + 1e-9)))), 1)
                if rep["voice_over_sfx_db"] < 14:
                    warn.append(f"effects crowd the voice (only {rep['voice_over_sfx_db']} dB under it while he speaks)")
        gaps = [(round(a_, 1), round(b_ - a_, 1)) for a_, b_ in zip([0.0] + times, times + [ctx.total]) if b_ - a_ > 6.0]
        rep["holes"] = gaps
        if gaps and ctx.total < 70:                     # a Short with a dead stretch loses people
            warn.append(f"no effect for over 6 s at {gaps}")
        if rep["clutter"] > max(2, len(cues) // 6):
            warn.append(f"{rep['clutter']} effects crowd within 0.25 s of another")
        vo = np.zeros(int(round(ctx.total * audio.SR)), dtype=np.float32)
        for i in range(len(ctx.vo)):
            audio.add(vo, ctx.vo[i], ctx.start[i] + ctx.lead_of(i))
        v_rms = np.sqrt(np.mean(vo[np.abs(vo) > 1e-4] ** 2)) if np.any(np.abs(vo) > 1e-4) else 0
        f_rms = np.sqrt(np.mean(fx[np.abs(fx) > 1e-4] ** 2)) if np.any(np.abs(fx) > 1e-4) else 0
        if v_rms and f_rms:
            rep["sfx_vs_voice_db"] = round(_db(f_rms) - _db(v_rms), 1)
            if rep["sfx_vs_voice_db"] > 0:
                warn.append(f"effects are {rep['sfx_vs_voice_db']} dB louder than the voice on average")
            elif rep["sfx_vs_voice_db"] < -24:
                warn.append(f"effects are {rep['sfx_vs_voice_db']} dB under the voice: barely audible")
    rep["sync"] = sync
    rep["warnings"] = warn
    json.dump(rep, open(os.path.join(out_dir, "ears.json"), "w"), indent=1)
    summ = (f"ears: {rep.get('lufs', '?')} LUFS, true peak {rep.get('true_peak_dbtp', '?')} dBTP, {rep.get('sfx_count', 0)} effects, "
            f"sync median {rep.get('sync_median_ms', '?')} ms, sfx vs voice {rep.get('sfx_vs_voice_db', '?')} dB")
    log(summ)
    for w in warn:
        log("  ears warning: " + w)
    return rep
