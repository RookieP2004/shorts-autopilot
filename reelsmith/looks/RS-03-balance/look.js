// RS-03 Balance — a brass scale weighs two things: each pan fills with labelled weights, the beam tips with a damped
// swing to the heavier side, and the winner's number slams in. For "which is bigger / costs more / matters more".
// Props: left {label, value, unit?}, right {label, value, unit?}, verdict (optional text under the heavier pan), title
const L = {
  dur: 5.5,
  setup(A) {
    const { P } = A;
    A.l = P.left || { label: 'Savings', value: 2 }; A.r = P.right || { label: 'Inflation', value: 6 };
    const lv = +A.l.value, rv = +A.r.value, tot = Math.max(1e-9, lv + rv);
    A.target = Math.max(-1, Math.min(1, (rv - lv) / tot * 1.6)) * 0.32;   // radians, + = right side down
    A.tL = .6; A.tR = 1.5; A.tTip = 2.4;
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A;
    const cx = W / 2, top = H * .3, beam = Math.min(W * .29, 600 * S);
    // beam angle: level until weighed, then a damped swing into place
    let ang = 0; if (t > A.tTip) { const u = t - A.tTip; ang = A.target * (1 - Math.exp(-3.2 * u) * Math.cos(7 * u)); }
    else if (t > A.tL) ang = -0.06 * K.seg(t, A.tL, A.tL + .3) * (1 - K.seg(t, A.tR, A.tR + .3)) + 0.04 * K.seg(t, A.tR, A.tR + .3) * (1 - K.seg(t, A.tTip - .2, A.tTip));
    const brass = (y0, y1) => { const g = ctx.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, '#f7d58a'); g.addColorStop(.5, '#c9962f'); g.addColorStop(1, '#8a5f14'); return g; };
    ctx.save(); ctx.globalAlpha = K.seg(t, 0, .3);
    // stand
    const base = W < H ? H * .66 : H * .8;
    ctx.fillStyle = brass(top, base); ctx.fillRect(cx - 12 * S, top, 24 * S, base - top);
    ctx.beginPath(); ctx.ellipse(cx, base, 190 * S, 34 * S, 0, 0, K.TAU); ctx.fill();
    // beam + hangers + pans
    const ends = [-1, 1].map(s => [cx + Math.cos(ang) * beam * s, top + Math.sin(ang) * beam * s]);
    ctx.save(); ctx.translate(cx, top); ctx.rotate(ang); ctx.fillStyle = brass(-14 * S, 14 * S);
    K.rrect(ctx, -beam - 10 * S, -12 * S, beam * 2 + 20 * S, 24 * S, 12 * S); ctx.fill(); ctx.restore();
    ctx.fillStyle = brass(top - 40 * S, top + 40 * S); ctx.beginPath(); ctx.arc(cx, top, 30 * S, 0, K.TAU); ctx.fill();
    const drop = 280 * S, panW = Math.min(W * .17, 230 * S);
    [[A.l, ends[0], A.tL, -1], [A.r, ends[1], A.tR, 1]].forEach(([side, [ex, ey], t0, sg]) => {
      const py = ey + drop;
      ctx.strokeStyle = '#8a5f14'; ctx.lineWidth = 4 * S;
      ctx.beginPath(); ctx.moveTo(ex, ey); ctx.lineTo(ex - panW * .9, py); ctx.moveTo(ex, ey); ctx.lineTo(ex + panW * .9, py); ctx.stroke();
      // weights stacked in the pan (count grows with value, max 6)
      const n = Math.max(1, Math.min(6, Math.round(+side.value / Math.max(+A.l.value, +A.r.value) * 6)));
      for (let k = 0; k < n; k++) {
        const kk = K.seg(t, t0 + k * .08, t0 + k * .08 + .25); if (kk <= 0) continue;
        const bx = ex - panW * .7 + (k % 3) * panW * .48, by = py - 52 * S - Math.floor(k / 3) * 60 * S - (1 - K.overshoot(kk, 2)) * 200 * S;
        ctx.fillStyle = sg < 0 ? '#6fc3c0' : '#d9534f'; K.rrect(ctx, bx, by, panW * .44, 54 * S, 10 * S); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(bx + 8 * S, by + 8 * S, panW * .44 - 16 * S, 8 * S);
      }
      ctx.fillStyle = brass(py - 10 * S, py + 30 * S); ctx.beginPath(); ctx.ellipse(ex, py, panW, 26 * S, 0, 0, Math.PI); ctx.fill();
      // label + number under the pan
      const la = K.seg(t, t0 + .2, t0 + .5);
      ctx.globalAlpha = la; ctx.textAlign = 'center'; ctx.fillStyle = '#f6efe2';
      ctx.font = K.font('body', 46 * S); ctx.fillText(side.label, ex, py + 96 * S);
      ctx.font = K.font('display', 92 * S); const heavy = (sg > 0) === (A.target > 0);
      const sc = t > A.tTip + .3 && heavy ? 1 + .15 * (1 - K.out3(K.seg(t, A.tTip + .3, A.tTip + .7))) : 1;
      ctx.save(); ctx.translate(ex, py + 196 * S); ctx.scale(sc, sc);
      ctx.fillStyle = t > A.tTip + .3 && heavy ? '#f2b04a' : '#f6efe2'; ctx.fillText(`${side.value}${side.unit || ''}`, 0, 0); ctx.restore();
      ctx.globalAlpha = 1;
    });
    if (P.title) { ctx.globalAlpha = K.seg(t, .1, .4); ctx.font = K.font('display', 72 * S); ctx.fillStyle = '#f6efe2'; ctx.textAlign = 'center'; ctx.fillText(P.title, cx, H * .15); }
    if (P.verdict && t > A.tTip + .8) {
      const k = K.out3(K.seg(t, A.tTip + .8, A.tTip + 1.1)); ctx.globalAlpha = k;
      ctx.font = K.font('marker', 64 * S); ctx.fillStyle = '#f2b04a'; ctx.textAlign = 'center'; ctx.fillText(P.verdict, cx, W < H ? H * .75 : H * .93);
    }
    ctx.restore();
  },
  texts(t, A) {
    const K = A.kit, o = [];
    if (A.P.title && t > .2) o.push(K.box('title', A.P.title, 0, A.H * .1, A.W, A.H * .07));
    if (t > A.tL + .3) o.push(K.box('l', `${A.l.label} ${A.l.value}`, 0, 0, 10, 10, true));
    if (t > A.tR + .3) o.push(K.box('r', `${A.r.label} ${A.r.value}`, 0, 0, 10, 10, true));
    if (A.P.verdict && t > A.tTip + .9) o.push(K.box('verdict', A.P.verdict, 0, A.H * .7, A.W, A.H * .07));
    return o;
  },
  cues(A) { return [{ t: A.tL, sfx: 'thud', gain: .5 }, { t: A.tR, sfx: 'thud', gain: .5 }, { t: A.tTip, sfx: 'slide', gain: .5 }, { t: A.tTip + .3, sfx: 'hit', gain: .8 }]; },
};
export default L;
