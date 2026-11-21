// Open a look in headless Chrome and wait until it is ready. The page contract (host.html sets it up for every look):
//   window.DUR (s), window.render(t) draws moment t deterministically, window.READY = true once fonts/images are in,
//   optional window.EV = [{t, sfx, gain}] (sound cues) and window.TEXTS(t) = [{id, text, x0, y0, x1, y1, pass}] (reading check).
// Props reach the page as window.PROPS (injected before any script runs). Any page error stops the render: a broken
// look never becomes a silent broken clip. Adapted from Lemo-Opuscar core/render/page.mjs + browser.mjs (MIT, ../NOTICE).
import { chromium } from 'playwright-core';
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
import { serve } from './serve.mjs';
export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const REPO = path.resolve(ROOT, '..');
const CHROME = process.env.RS_CHROME || ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(p => fs.existsSync(p));
// cloud VMs have no GPU: SwiftShader keeps WebGL alive (slower, but never blank); RS_ANGLE overrides
const ANGLE = process.env.RS_ANGLE || (process.platform === 'darwin' ? 'metal' : 'swiftshader');
export const ARGS = [`--use-angle=${ANGLE}`, '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--font-render-hinting=none',
  '--force-color-profile=srgb', '--disable-dev-shm-usage'];
const GL_WATCH = `addEventListener('webglcontextlost', e => { window.__glLost = (e.target && e.target.id) || 'canvas'; }, true);`;
let srv = null;
async function server() { if (!srv) srv = await serve(REPO); return srv; }   // repo root: looks can reach /fonts and /assets
export function closeServer() { if (srv) { srv.server.close(); srv = null; } }
export async function launch() {
  return chromium.launch({ executablePath: CHROME, args: ARGS });
}
export async function openLook(browser, look, { w = 1080, h = 1920, props = {}, dur = null } = {}) {
  if (!fs.existsSync(path.join(ROOT, 'looks', look, 'look.js'))) throw new Error(`no look "${look}" (reelsmith/looks/${look}/look.js)`);
  const { port } = await server();
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await page.addInitScript(GL_WATCH);
  await page.addInitScript(`window.PROPS = ${JSON.stringify(props)}; window.WANT_DUR = ${dur == null ? 'null' : Number(dur)};`);
  let err = null;
  page.on('pageerror', e => { err = err || e; console.error('[look error]', e.message); });
  page.on('response', r => { if (r.status() >= 400 && /script|document|font|image/.test(r.request().resourceType()))
    console.error(`[look] ${r.status()} ${new URL(r.url()).pathname}`); });
  await page.goto(`http://127.0.0.1:${port}/reelsmith/host.html?look=${encodeURIComponent(look)}`);
  const t0 = Date.now();
  while (!(await page.evaluate(() => window.READY === true))) {
    if (err) throw new Error(`look ${look} failed while loading: ${err.message}`);
    if (Date.now() - t0 > 60000) throw new Error(`look ${look}: window.READY never became true (60 s)`);
    await new Promise(r => setTimeout(r, 50));
  }
  page.__err = () => err;
  return page;
}
export const glLost = page => page.evaluate(() => window.__glLost || null);
