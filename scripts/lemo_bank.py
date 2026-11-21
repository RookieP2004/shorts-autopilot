"""Lemo-Opuscar style bank: prepare every style's demo page (fonts + generated textures, from its own build.sh guards),
render a few stills through Reelsmith's bridge (reelsmith/engine/lemo.mjs), and record each style's status and licence.
Output: /tmp/lemo_bank/status.json and a contact sheet. The demo code is MIT (Lemomo / LemoLab); their STYLE.md guides
are CC BY-NC and are never copied into our repo.
Run: python scripts/lemo_bank.py [--only slug,slug] [--workers 2]
"""
import argparse, concurrent.futures as cf, json, os, re, subprocess, sys
LEMO = os.environ.get("LEMO_DIR", "/tmp/lemo")
RS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reelsmith")
OUT = "/tmp/lemo_bank"


def prep(slug):
    """Run only the asset lines of the demo's build.sh: font fetchers and `[ -f x ] || make x` guards."""
    d = os.path.join(LEMO, "styles", slug, "demo")
    bs = os.path.join(d, "build.sh")
    if not os.path.exists(bs):
        return "no build.sh"
    lines = [l.split("  #")[0].strip() for l in open(bs) if not l.strip().startswith("#")]
    keep = [l for l in lines if re.search(r"fonts?\.sh|fetch_fonts|fonts\.mjs", l) or re.match(r"\[ -[fs] .*\] \|\|", l)]
    keep = [l for l in keep if not re.search(r"video|mux|tts|asr|music|mix\.py|score", l)]
    keep = [l.replace('$(dirname "$0")', d).replace("$(dirname $0)", d) for l in keep]
    for f, runner in (("tools/fetch_fonts.py", sys.executable), ("tools/fetch_fonts.mjs", "node"), ("fetch_fonts.mjs", "node"),
                      ("tools/fonts.sh", "sh"), ("fetch_fonts.py", sys.executable)):
        if os.path.exists(os.path.join(d, f)):              # every font fetcher the demo ships, whatever build.sh calls it
            subprocess.run([runner, f], cwd=d, capture_output=True, text=True, timeout=300)
    env = dict(os.environ, LIB=LEMO, HERE=d, PY=sys.executable, D=f"styles/{slug}/demo")
    script = "\n".join([f'HERE="{d}"; LIB="{LEMO}"; PY="{sys.executable}"; D=styles/{slug}/demo; cd "{LEMO}"'] + keep)
    r = subprocess.run(["sh", "-c", script], env=env, capture_output=True, text=True, timeout=600)
    return "ok" if r.returncode == 0 else ("prep failed: " + (r.stderr or r.stdout)[-200:])


def probe(slug, cls):
    p = prep(slug)
    r = subprocess.run(["node", os.path.join(RS, "engine", "lemo.mjs"), slug, os.path.join(OUT, "stills"), "--size", "960x540"],
                       capture_output=True, text=True, timeout=400, cwd=RS)
    try:
        res = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        res = {"slug": slug, "ok": False, "err": (r.stderr or r.stdout)[-200:]}
    res.update(prep=p, **cls.get(slug, {}))
    print(f"{'OK ' if res.get('ok') else 'BAD'} {slug}: {res.get('err') or ''} {'' if p == 'ok' else p[:80]}", flush=True)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    os.makedirs(os.path.join(OUT, "stills"), exist_ok=True)
    cls = json.load(open("/tmp/lemo_class.json")) if os.path.exists("/tmp/lemo_class.json") else {}
    slugs = [s for s in sorted(os.listdir(os.path.join(LEMO, "styles"))) if os.path.isdir(os.path.join(LEMO, "styles", s, "demo"))]
    if a.only:
        slugs = [s for s in slugs if s in a.only.split(",")]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        res = list(ex.map(lambda s: probe(s, cls), slugs))
    sp = os.path.join(OUT, "status.json")
    old = json.load(open(sp)) if os.path.exists(sp) else {}
    old.update({r["slug"]: r for r in res})
    json.dump(old, open(sp, "w"), indent=1)
    print(sum(r.get("ok", False) for r in res), "of", len(res), "render")


if __name__ == "__main__":
    main()
