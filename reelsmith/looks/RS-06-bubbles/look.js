// RS-06 Bubbles — values as circles whose AREA is the value (honest sizes), packed without overlap, popping in from
// small to big; then the focus bubble grows and the rest dim. "Who has how much", "where the money goes".
// Props: items [[label, value, tone?], ...] (up to 9), focus (index), unit ("₹" prefix or "%" suffix via prefix/suffix), title
const L = {
  dur: 5.5,
  setup(A) {
    const { P, W, H, S } = A;
    const it = (P.items || [['Food', 40], ['Rent', 30], ['Travel', 12], ['Fun', 10], ['Other', 8]]).slice(0, 9).map((r, i) => ({ label: r[0], v: +r[1], tone: r[2], i }));
    const max = Math.max(...it.map(o => o.v)), R = Math.min(W, H) * .24;
    it.forEach(o => { o.r = Math.max(34 * S, R * Math.sqrt(o.v / max)); });
    // pack: biggest at the centre, each next one placed at the closest free spot on a spiral
    const order = [...it].sort((a, b) => b.v - a.v), cx = W / 2, cy = H * .5, placed = [];
    for (const o of order) {
      if (!placed.length) { o.x = cx; o.y = cy; placed.push(o); continue; }
      for (let a = 0, d = 0; ; a += .21, d += .9 * S) {
        const x = cx + Math.cos(a) * d, y = cy + Math.sin(a) * d * (H > W ? 1.25 : .8);
        if (placed.every(p => Math.hypot(p.x - x, p.y - y) > p.r + o.r + 10 * S)) { o.x = x; o.y = y; placed.push(o); break; }
      }
    }
    // fit the packed cluster into the free area (under the title, above the Shorts UI)
    const bx0 = Math.min(...it.map(o => o.x - o.r)), bx1 = Math.max(...it.map(o => o.x + o.r));
    const by0 = Math.min(...it.map(o => o.y - o.r)), by1 = Math.max(...it.map(o => o.y + o.r));
    const fx0 = W * .05, fx1 = W * .95, fy0 = H * (P.title ? .19 : .1), fy1 = H * .8;
    const f = Math.min(1, (fx1 - fx0) / (bx1 - bx0), (fy1 - fy0) / (by1 - by0));
    it.forEach(o => { o.x = (fx0 + fx1) / 2 + (o.x - (bx0 + bx1) / 2) * f; o.y = (fy0 + fy1) / 2 + (o.y - (by0 + by1) / 2) * f; o.r *= f; });
    A.it = it; A.order = order;
    A.tIn = o => .3 + A.order.indexOf(o) * .22; A.tFocus = .3 + it.length * .22 + .6;
    A.focus = P.focus ?? order[0].i;
  },
  draw(t, A) {
    const { ctx, kit: K, S, P, W, H } = A, pal = ['#f2b04a', '#6fc3c0', '#d9534f', '#4aa3ff', '#35e08a', '#b98ce0', '#f6efe2', '#e0874a', '#8fb35a'];
    const kf = K.inOut(K.seg(t, A.tFocus, A.tFocus + .6));
    if (P.title) { ctx.globalAlpha = K.seg(t, .05, .35); ctx.fillStyle = '#f6efe2'; ctx.font = K.font('display', 70 * S); ctx.textAlign = 'center'; ctx.fillText(P.title, W / 2, H * .13); ctx.globalAlpha = 1; }
    for (const o of A.order.slice().reverse()) {
      const k = K.seg(t, A.tIn(o), A.tIn(o) + .35); if (k <= 0) continue;
      const isF = o.i === A.focus, grow = isF ? 1 + .18 * kf : 1 - .08 * kf, r = o.r * K.overshoot(k, 2.2) * grow;
      const col = o.tone || pal[o.i % pal.length];
      ctx.globalAlpha = isF ? 1 : 1 - .6 * kf;
      const g = ctx.createRadialGradient(o.x - r * .35, o.y - r * .4, r * .1, o.x, o.y, r);
      g.addColorStop(0, '#ffffff'); g.addColorStop(.18, col); g.addColorStop(1, shade(col, -.35));
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(o.x, o.y, r, 0, K.TAU); ctx.fill();
      if (k > .7) {
        ctx.fillStyle = '#16232b'; ctx.textAlign = 'center';
        const px = Math.max(22 * S, Math.min(64 * S, r * .38)); ctx.font = K.font('body', px);
        const lab = String(o.label); K.fitText(ctx, lab, 'body', r * 1.6, px);
        ctx.fillText(lab, o.x, o.y - px * .1);
        ctx.font = K.font('semi', px * .78); ctx.fillText(`${P.prefix || ''}${K.fmtNum(o.v)}${P.suffix || ''}`, o.x, o.y + px * .85);
      }
    }
    ctx.globalAlpha = 1;
  },
  texts(t, A) {
    const o = A.P.title && t > .3 ? [A.kit.box('title', A.P.title, 0, A.H * .08, A.W, A.H * .07)] : [];
    for (const b of A.it) if (t > A.tIn(b) + .3) o.push(A.kit.box('b' + b.i, b.label, 0, 0, 10, 10, b.i !== A.focus));
    return o;
  },
  cues(A) { return [...A.order.map(o => ({ t: A.tIn(o), sfx: 'pop', gain: .5 })), { t: A.tFocus, sfx: 'swoosh_soft', gain: .5 }]; },
};
function shade(hex, f) { const n = parseInt(hex.slice(1), 16), c = [n >> 16, n >> 8 & 255, n & 255].map(v => Math.max(0, Math.min(255, Math.round(v * (1 + f))))); return `rgb(${c})`; }
export default L;
