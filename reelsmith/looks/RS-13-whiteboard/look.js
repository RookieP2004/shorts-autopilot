// RS-13 Whiteboard — a glossy dry-erase board where boxes, arrows and labels draw themselves in marker, one step at a
// time, and the key step gets a red circle. Stroke engine: Lemo-Opuscar's whiteboard wb.js (MIT, vendored): hand wobble,
// chisel-tip ribbons, overshoot at corners. Layout, steps and timing are ours.
// Props: title, steps ["Cash in", "Shell company", "Clean money"] (2-5), key (index to circle), note (handwritten, bottom)
import { line, arrow, roundRect, circle, ribbon, INK } from '/reelsmith/vendor/lemo/whiteboard/wb.js';
const L = {
  dur: 6,
  setup(A) {
    const { P, W, H, S } = A;
    A.steps = (P.steps || ['Dirty cash', 'Shell company', 'Clean money']).slice(0, 5);
    const n = A.steps.length, port = H > W;
    const bw = port ? W * .78 : Math.min(W * .8 / n - 60 * S, 420 * S), bh = port ? Math.min(200 * S, H * .45 / n) : 150 * S;
    const top = H * (port ? .24 : .36), gap = port ? (H * .5 - n * bh) / Math.max(1, n - 1) : (W * .84 - n * bw) / Math.max(1, n - 1);
    A.box = A.steps.map((_, i) => port ? [W / 2 - bw / 2, top + i * (bh + gap), bw, bh] : [W * .08 + i * (bw + gap), top, bw, bh]);
    // schedule: each step = box (0.45 s) + label writes (0.45 s) + arrow to the next (0.35 s)
    A.items = []; let t = .5;
    const add = (strokes, d, col, w) => { (Array.isArray(strokes) ? strokes : [strokes]).forEach((s, k, arr) => {
      s.t0 = t + d * k / arr.length; s.t1 = t + d * (k + 1) / arr.length; s.col = col; if (w) s.w = w; A.items.push(s); }); t += d; };
    A.tLabel = [];
    A.box.forEach(([x, y, w, h], i) => {
      add(roundRect(x, y, w, h, 22 * S, { w: 9 * S, color: INK.black }), .45, INK.black);
      A.tLabel.push(t); t += .45;
      if (i < n - 1) { const [x2, y2, w2] = A.box[i + 1];
        const a = port ? arrow(x + w / 2, y + h + 14 * S, x2 + w2 / 2, y2 - 14 * S, { w: 8 * S }) : arrow(x + w + 14 * S, y + h / 2, x2 - 14 * S, y2 + h / 2, { w: 8 * S });
        add(a, .35, INK.blue); }
    });
    const k = P.key ?? n - 1, [kx, ky, kw, kh] = A.box[k];
    A.tKey = t + .15; t += .15;
    const c = circle(kx + kw / 2, ky + kh / 2, Math.max(kw, kh) * .62, { w: 10 * S, ry: kh * .95 });
    c.t0 = t; c.t1 = t + .6; c.col = INK.red; A.items.push(c); t += .6;
    if (P.title) { const ul = line(W * .12, H * (port ? .16 : .2), W * .88, H * (port ? .16 : .2) + 6 * S, { w: 7 * S }); ul.t0 = .25; ul.t1 = .6; ul.col = INK.orange; A.items.push(ul); }
    A.tNote = t + .1; L.dur = Math.max(5, t + 1.4);
  },
  draw(t, A) {
    const { ctx, W, H, S, P, kit: K } = A;
    // the board: warm white enamel, a soft window reflection sliding slowly, ghosts of an old diagram
    ctx.fillStyle = '#f7f6f2'; ctx.fillRect(0, 0, W, H);
    const gx = W * (.2 + .05 * Math.sin(t * .3)), g = ctx.createLinearGradient(gx, 0, gx + W * .35, H);
    g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(.5, 'rgba(255,255,255,.55)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    ctx.save(); ctx.globalAlpha = .05; ctx.strokeStyle = '#6a6f78'; ctx.lineWidth = 10 * S; ctx.lineCap = 'round';
    const r = K.rng(31); for (let i = 0; i < 6; i++) { ctx.beginPath(); ctx.moveTo(r() * W, r() * H); ctx.quadraticCurveTo(r() * W, r() * H, r() * W, r() * H); ctx.stroke(); }
    ctx.restore();
    ctx.strokeStyle = '#c9ccd1'; ctx.lineWidth = 18 * S; ctx.strokeRect(0, 0, W, H);          // aluminium frame
    if (P.title) { ctx.fillStyle = INK.black; ctx.font = K.font('marker', 74 * S); ctx.textAlign = 'center'; textWrite(ctx, K, P.title, W / 2, H * (H > W ? .14 : .17), K.seg(t, .05, .45)); }
    // strokes: chisel ribbons filled up to their progress
    for (const s of A.items) { const p = s.prog(t); if (p <= 0) continue; ctx.beginPath(); ribbon(ctx, s, p * s.len, 1); ctx.fillStyle = s.col; ctx.globalAlpha = .93; ctx.fill(); ctx.globalAlpha = 1; }
    // labels written left to right
    A.steps.forEach((txt, i) => { const [x, y, w, h] = A.box[i], k = K.seg(t, A.tLabel[i], A.tLabel[i] + .45); if (k <= 0) return;
      ctx.fillStyle = i === (P.key ?? A.steps.length - 1) && t > A.tKey ? INK.red : INK.black;
      K.fitText(ctx, txt, 'marker', w * .86, 84 * S); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      textWrite(ctx, K, txt, x + w / 2, y + h / 2 + 4 * S, k); ctx.textBaseline = 'alphabetic'; });
    if (P.note && t > A.tNote) { ctx.fillStyle = INK.blue; ctx.font = K.font('hand', 84 * S); ctx.textAlign = 'center';
      textWrite(ctx, K, P.note, W / 2, H * (H > W ? .8 : .88), K.seg(t, A.tNote, A.tNote + .6)); }
  },
  texts(t, A) {
    const K = A.kit, o = [];
    if (A.P.title && t > .5) o.push(K.box('title', A.P.title, A.W * .1, A.H * .08, A.W * .8, A.H * .08));
    A.steps.forEach((s, i) => { if (t > A.tLabel[i] + .45) { const [x, y, w, h] = A.box[i]; o.push(K.box('s' + i, s, x, y, w, h)); } });
    if (A.P.note && t > A.tNote + .6) o.push(K.box('note', A.P.note, A.W * .1, A.H * .75, A.W * .8, A.H * .08));
    return o;
  },
  cues(A) {
    const c = [{ t: .25, sfx: 'marker', gain: .4 }];
    A.tLabel.forEach(tl => c.push({ t: tl - .45, sfx: 'marker', gain: .45 }));
    c.push({ t: A.tKey, sfx: 'marker', gain: .6 }, { t: A.tKey + .6, sfx: 'pop', gain: .5 }); return c;
  },
};
// writing reveal: clip the finished text from left to right
function textWrite(ctx, K, txt, x, y, k) {
  if (k <= 0) return; const w = ctx.measureText(txt).width, x0 = ctx.textAlign === 'center' ? x - w / 2 : x;
  ctx.save(); ctx.beginPath(); ctx.rect(x0 - 20, y - 400, (w + 40) * K.smooth(k), 800); ctx.clip(); ctx.fillText(txt, x, y); ctx.restore();
}
export default L;
