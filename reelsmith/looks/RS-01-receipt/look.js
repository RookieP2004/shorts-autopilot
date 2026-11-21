// RS-01 Receipt — a till receipt prints down the frame line by line; the total is circled in red marker.
// Props: title, items [[label, amount], ...], total_label, currency ("₹"), note (handwritten, optional), x, y (0-1 centre)
const L = {
  dur: 6,
  setup(A) {
    const { P, W, H, S } = A;
    A.items = P.items || [['Rent', 18000], ['Food', 9000], ['Travel', 3500], ['Phone', 699]];
    A.cur = P.currency ?? '₹';
    A.total = P.total ?? A.items.reduce((s, r) => s + Number(r[1]), 0);
    A.pw = Math.min(W * 0.72, 760 * S); A.lh = 74 * S; A.pad = 46 * S;
    A.ph = A.pad * 2 + 150 * S + A.items.length * A.lh + 190 * S;
    A.cx = W * (P.x ?? 0.5); A.top = H * (P.y ?? 0.5) - A.ph / 2;
    A.tLine = i => 0.55 + i * 0.42;                       // when each line prints
    A.tTot = A.tLine(A.items.length) + 0.25; A.tCirc = A.tTot + 0.5;
  },
  draw(t, A) {
    const { ctx, kit: K, S, P } = A, x0 = A.cx - A.pw / 2;
    const fed = K.out3(K.seg(t, 0, A.tTot + 0.2));        // paper feeds out as lines print
    const shown = A.ph * (0.22 + 0.78 * fed);
    ctx.save();
    ctx.translate(0, K.lerp(-40 * S, 0, K.out3(K.seg(t, 0, .5))));
    ctx.globalAlpha = K.seg(t, 0, .2);
    // shadow + paper with a torn bottom edge
    ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.fillRect(x0 + 14 * S, A.top + 18 * S, A.pw, shown);
    ctx.beginPath(); ctx.moveTo(x0, A.top); ctx.lineTo(x0 + A.pw, A.top); ctx.lineTo(x0 + A.pw, A.top + shown);
    const r = K.rng(5);
    for (let x = x0 + A.pw; x > x0; x -= 22 * S) ctx.lineTo(x - 11 * S, A.top + shown + (r() * 10 - 5) * S);
    ctx.lineTo(x0, A.top + shown); ctx.closePath(); ctx.fillStyle = '#fbf8f1'; ctx.fill();
    ctx.save(); ctx.clip(); K.grain(ctx, A.W, A.H, .05, 11, 2 * S);
    // header
    ctx.fillStyle = K.C.ink; ctx.textAlign = 'center';
    ctx.font = K.font('mono_b', 44 * S); ctx.fillText((P.title || 'MONTHLY BILL').toUpperCase(), A.cx, A.top + A.pad + 40 * S);
    ctx.font = K.font('mono', 26 * S); ctx.fillText(P.subtitle || '— thank you, come again —', A.cx, A.top + A.pad + 84 * S);
    dashed(ctx, x0 + A.pad, x0 + A.pw - A.pad, A.top + A.pad + 118 * S, S);
    // lines: typed left to right
    A.items.forEach(([lab, amt], i) => {
      const k = K.seg(t, A.tLine(i), A.tLine(i) + 0.3); if (k <= 0) return;
      const y = A.top + A.pad + 180 * S + i * A.lh;
      ctx.font = K.font('mono', 38 * S); ctx.textAlign = 'left';
      const s = String(lab); ctx.fillText(s.slice(0, Math.ceil(s.length * k)), x0 + A.pad, y);
      ctx.textAlign = 'right';
      if (k >= 1) ctx.fillText(A.cur + K.fmtNum(amt), x0 + A.pw - A.pad, y);
    });
    const yT = A.top + A.pad + 180 * S + A.items.length * A.lh + 30 * S;
    if (t >= A.tTot) {
      dashed(ctx, x0 + A.pad, x0 + A.pw - A.pad, yT - 34 * S, S);
      ctx.font = K.font('mono_b', 50 * S); ctx.textAlign = 'left'; ctx.fillText(P.total_label || 'TOTAL', x0 + A.pad, yT + 34 * S);
      ctx.textAlign = 'right';
      const v = K.roll(t, A.tTot, A.tTot + 0.45, 0, A.total);
      ctx.fillText(A.cur + K.fmtNum(Math.round(v)), x0 + A.pw - A.pad, yT + 34 * S);
    }
    ctx.restore();
    // red marker circle around the total, drawn once
    if (t >= A.tCirc) {
      ctx.strokeStyle = '#d23a2c'; ctx.lineWidth = 9 * S; ctx.lineCap = 'round';
      const cx = x0 + A.pw - A.pad - 120 * S, cy = yT + 18 * S, rx = 190 * S, ry = 62 * S, k = K.out3(K.seg(t, A.tCirc, A.tCirc + .45));
      const pts = []; for (let a = 0; a <= 1.08; a += .03) pts.push([cx + Math.cos(-2.6 + a * K.TAU) * rx * (1 + .05 * Math.sin(a * 9)), cy + Math.sin(-2.6 + a * K.TAU) * ry]);
      K.inkLine(ctx, pts, k, 3, 3 * S);
      if (P.note && t > A.tCirc + .5) {
        ctx.fillStyle = '#d23a2c'; ctx.font = K.font('hand', 64 * S); ctx.textAlign = 'center';
        ctx.globalAlpha = K.seg(t, A.tCirc + .5, A.tCirc + .8);
        ctx.fillText(P.note, cx - 40 * S, cy + 130 * S);
      }
    }
    ctx.restore();
  },
  texts(t, A) {
    const o = [], x0 = A.cx - A.pw / 2;
    if (t > .3) o.push(A.kit.box('title', A.P.title || 'MONTHLY BILL', x0, A.top, A.pw, 120 * A.S, true));
    if (t >= A.tTot) o.push(A.kit.box('total', (A.P.total_label || 'TOTAL') + ' ' + A.cur + A.total, x0, A.top + A.ph - 200 * A.S, A.pw, 80 * A.S));
    if (A.P.note && t > A.tCirc + .5) o.push(A.kit.box('note', A.P.note, x0, A.top + A.ph - 80 * A.S, A.pw, 80 * A.S));
    return o;
  },
  cues(A) {
    return [{ t: 0.05, sfx: 'slide', gain: .5 }, ...A.items.map((_, i) => ({ t: A.tLine(i), sfx: 'type', gain: .45 })),
      { t: A.tTot, sfx: 'register', gain: .8 }, { t: A.tCirc, sfx: 'marker', gain: .6 }];
  },
};
function dashed(ctx, a, b, y, S) { ctx.save(); ctx.setLineDash([10 * S, 9 * S]); ctx.lineWidth = 3 * S; ctx.strokeStyle = '#1a1410'; ctx.beginPath(); ctx.moveTo(a, y); ctx.lineTo(b, y); ctx.stroke(); ctx.restore(); }
export default L;
