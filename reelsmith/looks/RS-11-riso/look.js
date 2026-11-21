// RS-11 Riso — a three-ink risograph poster that prints itself: blue plate, then yellow, then pink roll across the
// sheet; misregistered plates, halftone dots, pinholes and ink streaks (print engine: Lemo-Opuscar's riso.js, MIT,
// vendored in ../../vendor/lemo). Our layout: kicker, a huge number or word, a caption, sun and bars that overprint.
// Props: kicker, big (number/word), caption, footer, bars [values] (optional mini chart), inks ("classic"|"teal")
import { makeRiso, INK } from '/reelsmith/vendor/lemo/riso.js';
const L = {
  dur: 4.5, gl: true,
  setup(A) {
    A.plate = document.createElement('canvas'); A.plate.width = A.W; A.plate.height = A.H;
    A.g = A.plate.getContext('2d', { willReadFrequently: true });
    A.print = makeRiso(A.canvas, A.W, A.H);
    A.tPlate = [0.15, 0.85, 1.55];
  },
  draw(t, A) {
    const { g, W, H, S, P, kit: K } = A;
    g.globalCompositeOperation = 'source-over'; g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
    // plate colours: R = blue, G = yellow, B = pink density. 'lighter' adds to one plate only = overprint.
    const ink = (r, gg, b) => `rgb(${r},${gg},${b})`;
    g.globalCompositeOperation = 'lighter';
    // sun (pink) behind everything, overprints the blue to purple
    const sun = K.out3(K.seg(t, .2, 1.2));
    g.fillStyle = ink(0, 0, 255); g.beginPath(); g.arc(W * .7, H * .27, Math.min(W, H) * .24 * (.6 + .4 * sun), 0, K.TAU); g.fill();
    // ground stripes (yellow)
    g.fillStyle = ink(0, 210, 0); for (let i = 0; i < 5; i++) g.fillRect(0, H * (.7 + i * .03), W, H * .013);
    // optional bars (blue), growing
    if (P.bars && P.bars.length) {
      const mx = Math.max(...P.bars), bw = W * .7 / P.bars.length;
      P.bars.forEach((v, i) => { const k = K.out3(K.seg(t, .4 + i * .12, .9 + i * .12)), h = H * .22 * v / mx * k;
        g.fillStyle = ink(230, 0, 0); g.fillRect(W * .15 + i * bw + bw * .12, H * .84 - h, bw * .76, h); });
    }
    // type: big word in blue + pink shadow (overprint), kicker in pink, caption in blue
    g.textAlign = 'center'; g.textBaseline = 'alphabetic';
    const big = String(P.big ?? '72'), px = K.fitText(g, big, 'anton', W * .86, 560 * S);
    g.font = K.font('anton', px);
    g.fillStyle = ink(0, 0, 200); g.fillText(big, W / 2 + 14 * S, H * .47 + 12 * S);
    g.fillStyle = ink(255, 0, 0); g.fillText(big, W / 2, H * .47);
    if (P.kicker) { g.font = K.font('bebas', 120 * S); g.fillStyle = ink(255, 0, 0); g.textAlign = 'left'; g.fillText(String(P.kicker).toUpperCase(), W * .08, H * .14); g.textAlign = 'center'; }
    if (P.caption) { g.font = K.font('body', 60 * S); g.fillStyle = ink(255, 0, 0);
      K.wrap(g, P.caption, W * .84).forEach((l, j) => g.fillText(l, W / 2, H * .55 + j * 72 * S)); }
    if (P.footer) { g.font = K.font('mono_b', 34 * S); g.fillStyle = ink(200, 0, 0); g.fillText(P.footer, W / 2, H * .9); }
    // print: each plate gates on and its ink rolls across; ink grain boils at 12 fps like a real print run
    const step = Math.floor(t * 12), seed = step % 7;
    const gate = A.tPlate.map(tp => K.seg(t, tp, tp + .05));
    const sweep = A.tPlate.map(tp => K.lerp(-200, W + 400, K.inOut(K.seg(t, tp, tp + .6))));
    const r = K.rng(seed + 1), j = () => (r() - .5) * 2 * S;
    const inks = P.inks === 'teal' ? [[0, 131, 138], INK.yellow, [255, 102, 94]] : [INK.blue, INK.yellow, INK.pink];
    A.print(A.plate, { seed, sheet: 1, gate, sweep, inks, off: [[j(), j()], [6 * S + j(), -4 * S + j()], [-6 * S + j(), 5 * S + j()]], rot: [0, .002, -.002] });
  },
  texts(t, A) {
    const o = [];
    if (t > A.tPlate[0] + .6) o.push(A.kit.box('big', String(A.P.big ?? '72'), A.W * .07, A.H * .26, A.W * .86, A.H * .22));
    if (A.P.caption && t > A.tPlate[2] + .6) o.push(A.kit.box('cap', A.P.caption, A.W * .08, A.H * .5, A.W * .84, A.H * .12));
    return o;
  },
  cues(A) { return [...A.tPlate.map(tp => ({ t: tp, sfx: 'slide', gain: .5 })), { t: A.tPlate[2] + .3, sfx: 'stamp', gain: .7 }]; },
};
export default L;
