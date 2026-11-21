// RS-08 Sweep — a dark scope: a sweep line turns, and each target lights up only when the beam passes it, then fades
// to an afterglow; a readout logs each contact. For "hidden in plain sight", investigations, spotting the pattern.
// Props: blips [{label, angle (deg, 0 = up), dist (0-1), tone?}], title, readout (true)
const L = {
  dur: 6,
  setup(A) {
    A.blips = (A.P.blips || [{ label: 'Shell co. A', angle: 40, dist: .6 }, { label: 'Shell co. B', angle: 150, dist: .4 }, { label: 'The bank', angle: 260, dist: .75, tone: 'red' }]).slice(0, 8);
    A.rpm = A.P.rpm || 18;   // degrees per... revolutions per minute
    A.order = null;
    A.hit = b => { const a = ((b.angle % 360) + 360) % 360; return a / (A.rpm * 6) + .3; };   // first time the beam passes
  },
  draw(t, A) {
    if (!A.order) A.order = A.blips.map((b, i) => i).sort((a, b) => A.hit(A.blips[a]) - A.hit(A.blips[b]));
    const { ctx, kit: K, W, H, S, P } = A, cx = W / 2, cy = H * (W < H ? .44 : .52), R = Math.min(W, H) * .42;
    ctx.fillStyle = '#071012'; ctx.fillRect(0, 0, W, H);
    const on = K.seg(t, 0, .3), grn = (a) => `rgba(80,255,170,${a})`;
    ctx.globalAlpha = on; ctx.strokeStyle = grn(.25); ctx.lineWidth = 2 * S;
    for (let k = 1; k <= 4; k++) { ctx.beginPath(); ctx.arc(cx, cy, R * k / 4, 0, K.TAU); ctx.stroke(); }
    for (let a = 0; a < 12; a++) { ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.sin(a / 12 * K.TAU) * R, cy - Math.cos(a / 12 * K.TAU) * R); ctx.stroke(); }
    const sweep = Math.max(0, t - .3) * A.rpm * 6;                     // degrees turned
    const ang = d => (d - 90) * Math.PI / 180;
    // the beam: a wedge with a fading tail
    for (let k = 0; k < 40; k++) {
      const a0 = sweep - k * 1.5; ctx.fillStyle = grn(.22 * (1 - k / 40));
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, R, ang(a0 - 1.5), ang(a0)); ctx.closePath(); ctx.fill();
    }
    ctx.strokeStyle = grn(.9); ctx.lineWidth = 3 * S; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(ang(sweep)) * R, cy + Math.sin(ang(sweep)) * R); ctx.stroke();
    // blips: bright when the beam passes, then an afterglow; once found, the label stays
    let logY = 0;
    A.blips.forEach((b, i) => {
      const th = A.hit(b); if (t < th) return;
      const since = ((sweep - b.angle) % 360 + 360) % 360 / (A.rpm * 6);   // seconds since the beam last passed it
      const glow = Math.exp(-since * 1.6), x = cx + Math.sin(b.angle * Math.PI / 180) * R * b.dist, y = cy - Math.cos(b.angle * Math.PI / 180) * R * b.dist;
      const col = b.tone === 'red' ? [255, 70, 80] : b.tone === 'gold' ? [242, 176, 74] : [80, 255, 170];
      const rg = ctx.createRadialGradient(x, y, 0, x, y, 40 * S); rg.addColorStop(0, `rgba(${col},${.5 + .5 * glow})`); rg.addColorStop(1, `rgba(${col},0)`);
      ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(x, y, 40 * S, 0, K.TAU); ctx.fill();
      ctx.fillStyle = `rgb(${col})`; ctx.beginPath(); ctx.arc(x, y, 9 * S, 0, K.TAU); ctx.fill();
      const ka = K.seg(t, th, th + .3); ctx.globalAlpha = ka; ctx.font = K.font('mono_b', 46 * S); ctx.textAlign = x > cx ? 'right' : 'left';
      ctx.fillStyle = `rgb(${col})`; ctx.fillText(b.label, x + (x > cx ? -26 : 26) * S, y - 22 * S); ctx.globalAlpha = 1;
      if (P.readout !== false) {                                        // contact log under the scope
        ctx.font = K.font('mono_b', 40 * S); ctx.textAlign = 'left'; ctx.fillStyle = grn(.85 * ka);
        const ly = cy + R + 100 * S + A.order.indexOf(i) * 58 * S;
        ctx.fillText(`> CONTACT ${String(i + 1).padStart(2, '0')}  ${b.label.toUpperCase()}`, cx - R, ly);
      }
    });
    if (P.title) { ctx.fillStyle = grn(.95); ctx.font = K.font('dotg', 64 * S); ctx.textAlign = 'center'; ctx.fillText(P.title.toUpperCase(), cx, H * .09); }
    // scanlines
    ctx.fillStyle = 'rgba(0,0,0,.18)'; for (let y = 0; y < H; y += 4 * S) ctx.fillRect(0, y, W, 1.5 * S);
    ctx.globalAlpha = 1;
  },
  texts(t, A) {
    const o = A.P.title ? [A.kit.box('title', A.P.title, 0, A.H * .04, A.W, A.H * .07)] : [];
    A.blips.forEach((b, i) => { if (t > A.hit(b)) o.push(A.kit.box('b' + i, b.label, 0, 0, 10, 10, true)); });
    return o;
  },
  cues(A) { return [{ t: .3, sfx: 'riser', gain: .25 }, ...A.blips.map(b => ({ t: A.hit(b), sfx: b.tone === 'red' ? 'error' : 'ding', gain: .5 }))]; },
};
export default L;
