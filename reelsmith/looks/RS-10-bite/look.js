// RS-10 Bite — a round plate of shares (a chart you can eat): slices settle in one by one with their labels, then
// the "taker" slice is bitten out with a crunch and slides away, leaving what is left. Tax, fees, middlemen.
// Props: slices [[label, value, tone?], ...], take (index bitten out), title, prefix/suffix, left_label ("what you keep")
const L = {
  dur: 5.5,
  setup(A) {
    const { P } = A;
    A.sl = (P.slices || [['You keep', 70], ['Tax', 20], ['Fees', 10]]).map((r, i) => ({ label: r[0], v: +r[1], tone: r[2], i }));
    A.sum = A.sl.reduce((s, o) => s + o.v, 0); A.take = P.take ?? 1;
    let a = -Math.PI / 2; A.sl.forEach(o => { o.a0 = a; a += o.v / A.sum * Math.PI * 2; o.a1 = a; });
    A.tIn = i => .3 + i * .35; A.tBite = .3 + A.sl.length * .35 + .7;
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A, cx = W / 2, cy = H * (W < H ? .47 : .53), R = Math.min(W, H) * .32;
    const pal = ['#f2b04a', '#d9534f', '#6fc3c0', '#4aa3ff', '#35e08a', '#b98ce0'];
    if (P.title) { ctx.globalAlpha = K.seg(t, .05, .35); ctx.fillStyle = '#f6efe2'; ctx.font = K.font('display', 72 * S); ctx.textAlign = 'center'; ctx.fillText(P.title, cx, H * .12); ctx.globalAlpha = 1; }
    // plate
    ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.beginPath(); ctx.ellipse(cx + 12 * S, cy + 22 * S, R * 1.12, R * 1.12, 0, 0, K.TAU); ctx.fill();
    ctx.fillStyle = '#f6efe2'; ctx.beginPath(); ctx.arc(cx, cy, R * 1.12, 0, K.TAU); ctx.fill();
    ctx.strokeStyle = '#d9cdb4'; ctx.lineWidth = 4 * S; ctx.beginPath(); ctx.arc(cx, cy, R * 1.04, 0, K.TAU); ctx.stroke();
    const kb = K.seg(t, A.tBite, A.tBite + .6);
    A.sl.forEach(o => {
      const k = K.seg(t, A.tIn(o.i), A.tIn(o.i) + .35); if (k <= 0) return;
      const isT = o.i === A.take, mid = (o.a0 + o.a1) / 2;
      const off = (1 - K.overshoot(k, 2)) * 40 * S + (isT ? K.in3(kb) * R * 1.6 : 0);
      const ox = Math.cos(mid) * off, oy = Math.sin(mid) * off;
      ctx.save(); ctx.translate(ox, oy); if (isT) ctx.globalAlpha = 1 - K.seg(t, A.tBite + .35, A.tBite + .6);
      ctx.fillStyle = o.tone || pal[o.i % pal.length];
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, R, o.a0 + .012, o.a1 - .012); ctx.closePath(); ctx.fill();
      if (isT && kb > 0) {                                           // the bite marks on the taken slice
        ctx.globalCompositeOperation = 'destination-out';
        for (let b = 0; b < 3; b++) { const ba = K.lerp(o.a0, o.a1, .25 + b * .25); ctx.beginPath(); ctx.arc(cx + Math.cos(ba) * R, cy + Math.sin(ba) * R, R * .16, 0, K.TAU); ctx.fill(); }
        ctx.globalCompositeOperation = 'source-over';
      }
      // label on the slice
      const lr = R * .62, lx = cx + Math.cos(mid) * lr, ly = cy + Math.sin(mid) * lr, frac = o.v / A.sum;
      if (k >= 1 && frac > .06) {
        ctx.fillStyle = '#16232b'; ctx.textAlign = 'center'; ctx.font = K.font('body', Math.max(28, Math.min(54, 300 * frac)) * S);
        ctx.fillText(o.label, lx, ly); ctx.font = K.font('semi', 40 * S); ctx.fillText(`${P.prefix || ''}${K.fmtNum(o.v)}${P.suffix ?? '%'}`, lx, ly + 46 * S);
      }
      ctx.restore();
    });
    if (P.left_label && t > A.tBite + .7) {
      const k = K.out3(K.seg(t, A.tBite + .7, A.tBite + 1)); ctx.globalAlpha = k; ctx.fillStyle = '#f2b04a';
      ctx.font = K.font('marker', 66 * S); ctx.textAlign = 'center'; ctx.fillText(P.left_label, cx, cy + R * 1.12 + 120 * S); ctx.globalAlpha = 1;
    }
  },
  texts(t, A) {
    const o = A.P.title && t > .3 ? [A.kit.box('title', A.P.title, 0, A.H * .07, A.W, A.H * .07)] : [];
    if (A.P.left_label && t > A.tBite + .8) o.push(A.kit.box('left', A.P.left_label, 0, A.H * .8, A.W, A.H * .07));
    return o;
  },
  cues(A) { return [...A.sl.map(o => ({ t: A.tIn(o.i), sfx: 'pop', gain: .45 })), { t: A.tBite, sfx: 'stomp', gain: .7 }, { t: A.tBite + .3, sfx: 'whoosh', gain: .5 }]; },
};
export default L;
