// node render.mjs <Composition> <props.json> <out_dir>
// Renders a transparent PNG sequence (frame_0000.png ...) for the Python compositor (autopilot/motion.py).
import {bundle} from '@remotion/bundler';
import {renderFrames, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const [comp, propsFile, outDir] = process.argv.slice(2);
const here = path.dirname(fileURLToPath(import.meta.url));
const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8'));
const browserExecutable = process.env.REMOTION_CHROME || (fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : null);
const chromiumOptions = {gl: 'swangle'};
const cacheDir = path.join(here, '.bundle');
let serveUrl;
const stamp = path.join(cacheDir, '.stamp');
const srcTime = Math.max(...fs.readdirSync(path.join(here, 'src')).map((f) => fs.statSync(path.join(here, 'src', f)).mtimeMs));
if (fs.existsSync(stamp) && Number(fs.readFileSync(stamp, 'utf8')) >= srcTime) {
  serveUrl = cacheDir;
} else {
  fs.rmSync(cacheDir, {recursive: true, force: true});
  serveUrl = await bundle({entryPoint: path.join(here, 'src/index.ts'), outDir: cacheDir, publicDir: path.join(here, 'public')});
  fs.writeFileSync(stamp, String(srcTime));
}
const composition = await selectComposition({serveUrl, id: comp, inputProps, browserExecutable, chromiumOptions});
fs.mkdirSync(outDir, {recursive: true});
const t0 = Date.now();
await renderFrames({
  composition, serveUrl, inputProps, browserExecutable, chromiumOptions, outputDir: outDir, imageFormat: 'png',
  concurrency: Number(process.env.MOTION_CONCURRENCY || 2), onStart: () => {},
  onFrameUpdate: () => {}, frameRange: null,
});
console.log(`motion ${comp}: ${composition.durationInFrames} frames ${composition.width}x${composition.height} in ${((Date.now() - t0) / 1000).toFixed(1)}s -> ${outDir}`);
