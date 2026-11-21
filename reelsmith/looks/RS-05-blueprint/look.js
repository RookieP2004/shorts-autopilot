// RS-05 Blueprint — how a thing works, drawn as a technical sheet that draws itself: cyan grid paper, parts in an
// exploded column, dimension lines, numbered callouts with leader lines, a title block in the corner.
// Props: title, parts [{label, shape: "box"|"circle"|"gear"|"cyl"|"bolt", note?}], sheet ("A-01")
const L = {
  dur: 6,
  setup(A) {
    const { P } = A;
    A.parts = (P.parts || [{ label: 'Lid', shape: 'cyl' }, { label: 'Gear train', shape: 'gear' }, { label: 'Battery', shape: 'box' }]).slice(0, 5);
    A.tPart = i => .5 + i * .8;
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A;
    ctx.fillStyle = '#123a5c'; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = 'rgba(160,210,255,.10)'; ctx.lineWidth = 1;
    const g = 40 * S; for (let x = 0; x < W; x += g) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
    for (let y = 0; y < H; y += g) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
    ctx.strokeStyle = 'rgba(200,230,255,.5)'; ctx.lineWidth = 3 * S; ctx.strokeRect(30 * S, 30 * S, W - 60 * S, H - 60 * S);
    const ink = '#dff1ff'; ctx.strokeStyle = ink; ctx.fillStyle = ink; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    if (P.title) { ctx.globalAlpha = K.seg(t, .1, .4); ctx.font = K.font('cond', 78 * S); ctx.textAlign = 'left'; ctx.fillText(P.title.toUpperCase(), 70 * S, 140 * S); ctx.globalAlpha = 1; }
    const n = A.parts.length, cx = W * (W < H ? .3 : .36), top = H * .2, step = (H * .66) / n, sz = Math.min(step * .8, W * (W < H ? .4 : .26));
    A.parts.forEach((p, i) => {
      const k = K.seg(t, A.tPart(i), A.tPart(i) + .6); if (k <= 0) return;
      const y = top + step * (i + .5) + (1 - K.out3(k)) * 30 * S;
      ctx.lineWidth = 4 * S; shape(ctx, K, p.shape, cx, y, sz, k, S, i);
      // centre line through the stack (dash-dot), drawn with the first part
      if (i === 0) { ctx.save(); ctx.setLineDash([24 * S, 8 * S, 4 * S, 8 * S]); ctx.lineWidth = 2 * S; ctx.globalAlpha = .6;
        ctx.beginPath(); ctx.moveTo(cx, top); ctx.lineTo(cx, top + (H * .66) * K.out3(K.seg(t, .4, 2.5))); ctx.stroke(); ctx.restore(); }
      // callout: numbered circle + leader + label
      const kl = K.seg(t, A.tPart(i) + .35, A.tPart(i) + .75); if (kl <= 0) return;
      const lx = cx + sz * .62, bx = W * (W < H ? .58 : .62);
      ctx.lineWidth = 2.5 * S; ctx.beginPath(); ctx.moveTo(lx, y); ctx.lineTo(K.lerp(lx, bx, kl), y); ctx.stroke();
      if (kl >= 1) {
        ctx.beginPath(); ctx.arc(bx + 26 * S, y, 26 * S, 0, K.TAU); ctx.stroke();
        ctx.font = K.font('mono_b', 30 * S); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(String(i + 1), bx + 26 * S, y + 2 * S);
        ctx.textAlign = 'left'; ctx.font = K.font('cond', 54 * S); ctx.fillText(p.label.toUpperCase(), bx + 68 * S, y - (p.note ? 16 * S : 0));
        if (p.note) { ctx.font = K.font('mono', 32 * S); ctx.globalAlpha = .85; ctx.fillText(p.note, bx + 68 * S, y + 34 * S); ctx.globalAlpha = 1; }
        ctx.textBaseline = 'alphabetic';
      }
    });
    // title block
    const kb = K.seg(t, .2, .6); ctx.globalAlpha = kb; ctx.lineWidth = 2 * S;
    const bw = 360 * S, bh = 110 * S, bx = W - 60 * S - bw, by = H - 60 * S - bh;
    ctx.strokeRect(bx, by, bw, bh); ctx.beginPath(); ctx.moveTo(bx, by + bh / 2); ctx.lineTo(bx + bw, by + bh / 2); ctx.moveTo(bx + bw * .6, by); ctx.lineTo(bx + bw * .6, by + bh); ctx.stroke();
    ctx.font = K.font('mono', 24 * S); ctx.textAlign = 'left'; ctx.fillText('THE EXPLAINER', bx + 14 * S, by + 36 * S); ctx.fillText('DRAWN: VED', bx + 14 * S, by + 90 * S);
    ctx.fillText('SHEET', bx + bw * .6 + 14 * S, by + 36 * S); ctx.fillText(P.sheet || 'A-01', bx + bw * .6 + 14 * S, by + 90 * S); ctx.globalAlpha = 1;
  },
  texts(t, A) {
    const o = A.P.title && t > .3 ? [A.kit.box('title', A.P.title, 0, 60 * A.S, A.W, 100 * A.S)] : [];
    A.parts.forEach((p, i) => { if (t > A.tPart(i) + .75) o.push(A.kit.box('p' + i, p.label + (p.note ? ' ' + p.note : ''), A.W * .6, 0, A.W * .38, 60)); });
    return o;
  },
  cues(A) { return [{ t: .1, sfx: 'paper', gain: .5 }, ...A.parts.map((_, i) => ({ t: A.tPart(i), sfx: 'marker', gain: .45 })), ...A.parts.map((_, i) => ({ t: A.tPart(i) + .75, sfx: 'pop', gain: .4 }))]; },
};
function shape(ctx, K, kind, x, y, s, k, S, seed) {
  const pts = [];
  if (kind === 'circle') { for (let a = 0; a <= 1; a += .02) pts.push([x + Math.cos(a * K.TAU) * s * .45, y + Math.sin(a * K.TAU) * s * .45]); K.inkLine(ctx, pts, k, seed, 1.5 * S); return; }
  if (kind === 'gear') {
    const r0 = s * .36, r1 = s * .46, teeth = 12;
    for (let a = 0; a <= 1.0001; a += 1 / (teeth * 4)) { const q = Math.floor(a * teeth * 4) % 4, r = q < 2 ? r1 : r0; pts.push([x + Math.cos(a * K.TAU) * r, y + Math.sin(a * K.TAU) * r * .55]); }
    K.inkLine(ctx, pts, k, seed, 1 * S);
    if (k > .6) { ctx.beginPath(); ctx.ellipse(x, y, s * .12, s * .066, 0, 0, K.TAU); ctx.stroke(); }
    return;
  }
  if (kind === 'cyl' || kind === 'bolt') {
    const w = kind === 'bolt' ? s * .2 : s * .45, h = kind === 'bolt' ? s * .5 : s * .28;
    for (let a = 0; a <= 1; a += .03) pts.push([x + Math.cos(a * K.TAU) * w, y - h / 2 + Math.sin(a * K.TAU) * w * .3]);
    pts.push([x + w, y + h / 2]); for (let a = 0; a <= .5; a += .03) pts.push([x + Math.cos(a * K.TAU) * w, y + h / 2 + Math.sin(a * K.TAU) * w * .3]);
    pts.push([x - w, y - h / 2]); K.inkLine(ctx, pts, k, seed, 1.2 * S); return;
  }
  // box: an isometric block
  const w = s * .5, h = s * .22, d = s * .2;
  const P = [[x - w, y - h / 2], [x + w, y - h / 2], [x + w, y + h / 2], [x - w, y + h / 2], [x - w, y - h / 2], [x - w + d, y - h / 2 - d * .6], [x + w + d, y - h / 2 - d * .6], [x + w, y - h / 2], [x + w + d, y - h / 2 - d * .6], [x + w + d, y + h / 2 - d * .6], [x + w, y + h / 2]];
  K.inkLine(ctx, P, k, seed, 1.2 * S);
}
export default L;
