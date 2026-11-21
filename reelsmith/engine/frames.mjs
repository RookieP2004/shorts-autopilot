// node engine/frames.mjs <look> <job.json> <out_dir>
//   job.json: { w, h, fps, dur, props, workers?, format? ("png" transparent, default | "jpg" opaque) }
// Captures every frame of a look to out_dir/f_00000.png for the compositor (autopilot/looks.py), splitting the frames
// across worker pages in one browser. Writes out_dir/cues.json (the look's sound cues) and texts.json (reading boxes
// sampled every 0.1 s). Exits non-zero on any page error or a lost WebGL context.
import fs from 'fs'; import path from 'path';
import { launch, openLook, glLost, closeServer } from './open.mjs';
const [look, jobFile, outDir] = process.argv.slice(2);
if (!look || !jobFile || !outDir) { console.error('usage: node engine/frames.mjs <look> <job.json> <out_dir>'); process.exit(2); }
const J = JSON.parse(fs.readFileSync(jobFile, 'utf8'));
const W = J.w | 0, H = J.h | 0, FPS = J.fps || 30, fmt = J.format || 'png';
fs.mkdirSync(outDir, { recursive: true });
const t0 = Date.now();
const browser = await launch();
let code = 0;
try {
  const probe = await openLook(browser, look, { w: W, h: H, props: J.props || {}, dur: J.dur });
  const DUR = await probe.evaluate(() => window.DUR);
  const cues = await probe.evaluate(() => window.EV || []);
  const texts = [];
  for (let t = 0; t <= DUR + 1e-6; t += 0.1) texts.push({ t: +t.toFixed(2), boxes: await probe.evaluate(t => { window.render(t); return window.TEXTS(t); }, t) });
  fs.writeFileSync(path.join(outDir, 'cues.json'), JSON.stringify(cues));
  fs.writeFileSync(path.join(outDir, 'texts.json'), JSON.stringify(texts));
  await probe.close();
  const N = Math.max(1, Math.round(DUR * FPS)), WK = Math.max(1, Math.min(J.workers || 2, N));
  const per = Math.ceil(N / WK);
  await Promise.all([...Array(WK)].map(async (_, w) => {
    const a = w * per, b = Math.min(N, a + per); if (a >= b) return;
    const page = await openLook(browser, look, { w: W, h: H, props: J.props || {}, dur: J.dur });
    for (let f = a; f < b; f++) {
      await page.evaluate(t => window.render(t), f / FPS);
      const file = path.join(outDir, `f_${String(f).padStart(5, '0')}.${fmt}`);
      await page.screenshot(fmt === 'png' ? { path: file, type: 'png', omitBackground: true } : { path: file, type: 'jpeg', quality: 94 });
      if (page.__err()) throw new Error(`look ${look} failed at t=${(f / FPS).toFixed(2)}: ${page.__err().message}`);
      if (f % 30 === 29 && await glLost(page)) throw new Error(`look ${look}: WebGL context lost at frame ${f}`);
    }
    await page.close();
  }));
  console.log(`look ${look}: ${N} frames ${W}x${H} in ${((Date.now() - t0) / 1000).toFixed(1)}s -> ${outDir}`);
} catch (e) { console.error(String(e.message || e)); code = 1; }
await browser.close(); closeServer(); process.exit(code);
