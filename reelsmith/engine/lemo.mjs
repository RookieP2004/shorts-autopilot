// node engine/lemo.mjs <slug> <out_dir> [--size 1920x1080] [--q 'k=v'] t1 t2 ...
// Renders stills of a Lemo-Opuscar style's own demo page (MIT code) from the library clone (LEMO_DIR, default
// /tmp/lemo; fetch with scripts/lemo_styles.sh). Used to study an engine before we adapt it into a look of our own.
import fs from 'fs'; import path from 'path';
import { chromium } from 'playwright-core';
import { serve } from './serve.mjs';
import { ARGS } from './open.mjs';
const a = process.argv.slice(2), take = k => { const i = a.indexOf(k); return i >= 0 ? a.splice(i, 2)[1] : null; };
const [W, H] = (take('--size') || '1920x1080').split('x').map(Number), q = take('--q') || '';
const [slug, out, ...ts] = a, LEMO = process.env.LEMO_DIR || '/tmp/lemo';
fs.mkdirSync(out, { recursive: true });
const { server, port } = await serve(LEMO);
const CHROME = process.env.RS_CHROME || '/usr/bin/google-chrome';
const browser = await chromium.launch({ executablePath: CHROME, args: ARGS });
const page = await browser.newPage({ viewport: { width: W, height: H } });
let err = null; page.on('pageerror', e => { err = err || e.message; });
await page.goto(`http://127.0.0.1:${port}/styles/${slug}/demo/index.html${q ? '?' + q : ''}`);
const t0 = Date.now(); let ok = true;
while (!(await page.evaluate(() => window.READY === true).catch(() => false))) {
  if (err || Date.now() - t0 > 90000) { ok = false; break; } await new Promise(r => setTimeout(r, 200));
}
if (!ok) { console.log(JSON.stringify({ slug, ok: false, err: err || 'READY timeout' })); await browser.close(); server.close(); process.exit(1); }
const DUR = await page.evaluate(() => window.DUR);
const times = ts.length ? ts.map(Number) : [0.15, 0.4, 0.7].map(k => +(k * DUR).toFixed(2));
const files = [];
for (const t of times) {
  await page.evaluate(t => window.render(t), t);
  const f = path.join(out, `${slug}_${t.toFixed(1)}.jpg`); await page.screenshot({ path: f, type: 'jpeg', quality: 85 }); files.push(f);
}
console.log(JSON.stringify({ slug, ok: !err, dur: DUR, files, err }));
await browser.close(); server.close();
