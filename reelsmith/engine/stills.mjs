// node engine/stills.mjs <look> <out_dir> [--size 1080x1920] [--props '{"title":"..."}' | --props-file f.json] [--bg '#16232b'] t1 t2 ...
// Review stills of a look (JPEG, on a background colour so transparent looks are visible). Adapted from Lemo-Opuscar
// core/render/still.mjs (MIT, ../NOTICE).
import fs from 'fs'; import path from 'path';
import { launch, openLook, closeServer } from './open.mjs';
const a = process.argv.slice(2), take = k => { const i = a.indexOf(k); return i >= 0 ? a.splice(i, 2)[1] : null; };
const size = take('--size') || '1080x1920', [W, H] = size.split('x').map(Number);
const pf = take('--props-file'), props = pf ? JSON.parse(fs.readFileSync(pf, 'utf8')) : JSON.parse(take('--props') || '{}');
const bg = take('--bg') || '#16232b';
const [look, outDir, ...times] = a;
fs.mkdirSync(outDir, { recursive: true });
const browser = await launch();
const page = await openLook(browser, look, { w: W, h: H, props });
await page.evaluate(c => { document.body.style.background = c; }, bg);
const DUR = await page.evaluate(() => window.DUR);
const ts = times.length ? times.map(Number) : [0.2, 0.35, 0.5, 0.7, 0.95].map(k => +(k * DUR).toFixed(2));
for (const t of ts) {
  await page.evaluate(t => window.render(t), t);
  const f = path.join(outDir, `${look}_${t.toFixed(2)}.jpg`);
  await page.screenshot({ path: f, type: 'jpeg', quality: 90 }); console.log(f);
}
await browser.close(); closeServer();
