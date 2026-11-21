// node engine/textcheck.mjs <frames_dir> [--rate 18 --base 0.8]
// Reading check on a captured look (texts.json from frames.mjs): every piece of text must stay fully on screen at least
// letters/rate + base seconds from when it first appears. The rule follows Lemo-Opuscar's readcheck (MIT, ../NOTICE);
// Shorts default to our faster 18 letters/s + 0.8 s, long videos pass --rate 15 --base 1.5.
import fs from 'fs'; import path from 'path';
const a = process.argv.slice(2), opt = (k, d) => { const i = a.indexOf(k); return i >= 0 ? +a[i + 1] : d; };
const dir = a[0], RATE = opt('--rate', 18), BASE = opt('--base', 0.8);
const T = JSON.parse(fs.readFileSync(path.join(dir, 'texts.json'), 'utf8'));
const seen = {};
for (const { t, boxes } of T) {
  const vis = new Set();
  for (const b of boxes || []) {
    if (b.pass) continue;
    const k = b.id + '\u0000' + b.text; vis.add(k);
    const s = seen[k] ??= { id: b.id, text: b.text, t0: t, run: 0, done: false };
    if (!s.done) s.run = t - s.t0 + 0.1;
  }
  for (const k in seen) if (!vis.has(k)) seen[k].done = true;
}
let bad = 0;
for (const s of Object.values(seen)) {
  const need = [...s.text].filter(c => !/\s/.test(c)).length / RATE + BASE, ok = s.run >= need - 0.05;
  if (!ok) bad++;
  console.log(`${ok ? 'OK ' : 'BAD'} ${String(s.id).padEnd(12)} at ${s.t0.toFixed(1)}s need ${need.toFixed(2)}s got ${s.run.toFixed(2)}s ${JSON.stringify(s.text.slice(0, 30))}`);
}
process.exit(bad ? 1 : 0);
