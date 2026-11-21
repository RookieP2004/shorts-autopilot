// RS-07 Chalk — a green chalkboard in a wooden frame; lines write themselves in chalk (rough edges, dust puffs at
// each stroke start), the answer gets a double underline and a box. Maths, science, "here's the formula".
// Props: lines ["E = mc²", ...] (up to 5), answer (index to box), title (top-left, smaller), color per line via "@y:" prefix (yellow)
const L = {
  dur: 6,
  setup(A) {
    A.lines = (A.P.lines || ['2 + 2 = 4', 'x² = 16', 'x = 4']).slice(0, 5);
    A.tLine = i => .4 + i * 1.0;
    A.speed = 16;   // letters per second
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A;
    // frame + slate
    ctx.fillStyle = '#6b4a2b'; ctx.fillRect(0, 0, W, H);
    const m = 34 * S, g = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * .7);
    g.addColorStop(0, '#2f5a48'); g.addColorStop(1, '#1d3a2e'); ctx.fillStyle = g; ctx.fillRect(m, m, W - 2 * m, H - 2 * m);
    // ghosts of old erased writing
    ctx.save(); ctx.globalAlpha = .06; ctx.fillStyle = '#fff'; ctx.font = K.font('hand', 120 * S); const r = K.rng(4);
    for (let i = 0; i < 7; i++) { ctx.save(); ctx.translate(r() * W, r() * H); ctx.rotate((r() - .5) * .3); ctx.fillText(['∑', 'π r²', 'a+b', '∫ dx', '√2', 'F=ma', '%'][i], 0, 0); ctx.restore(); }
    ctx.restore(); K.grain(ctx, W, H, .12, 21, 2 * S);
    if (P.title) { ctx.fillStyle = 'rgba(240,240,230,.75)'; ctx.font = K.font('hand', 64 * S); ctx.textAlign = 'left'; ctx.fillText(P.title, m + 50 * S, m + 100 * S); }
    const lh = Math.min(170 * S, (H * .62) / A.lines.length), y0 = H * .5 - (A.lines.length - 1) * lh / 2;
    A.lines.forEach((raw, i) => {
      const yel = raw.startsWith('@y:'), txt = yel ? raw.slice(3) : raw, t0 = A.tLine(i);
      const n = Math.floor((t - t0) * A.speed); if (n <= 0) return;
      const shown = txt.slice(0, n), y = y0 + i * lh;
      ctx.font = K.font('hand', 112 * S); const px = K.fitText(ctx, txt, 'hand', W * .8, 112 * S); ctx.textAlign = 'center';
      const fullW = ctx.measureText(txt).width, x = W / 2 - fullW / 2;
      ctx.textAlign = 'left'; ctx.fillStyle = yel ? '#f4e27a' : '#f2f2ea';
      // chalk: the same letters drawn 3 times with small jitter = a dry, broken edge
      for (let k = 0; k < 3; k++) { ctx.globalAlpha = .55; ctx.fillText(shown, x + (k - 1) * 1.4 * S, y + (k % 2) * 1.4 * S); }
      ctx.globalAlpha = 1;
      // dust puff where the chalk is now
      if (n < txt.length) { const dx = x + ctx.measureText(shown).width; ctx.fillStyle = 'rgba(240,240,230,.35)';
        const rr = K.rng(n + i * 99); for (let d = 0; d < 7; d++) { ctx.beginPath(); ctx.arc(dx + (rr() - .3) * 30 * S, y - px * .3 + (rr() - .5) * 40 * S, rr() * 4 * S, 0, K.TAU); ctx.fill(); } }
      if (i === (P.answer ?? A.lines.length - 1) && n >= txt.length + 6) {
        const k = K.seg(t, t0 + (txt.length + 6) / A.speed, t0 + (txt.length + 6) / A.speed + .5);
        ctx.strokeStyle = '#f4e27a'; ctx.lineWidth = 6 * S; ctx.lineCap = 'round'; ctx.globalAlpha = .85;
        const bx = x - 30 * S, by = y - px * .85, bw = fullW + 60 * S, bh = px * 1.15;
        K.inkLine(ctx, [[bx, by], [bx + bw, by], [bx + bw, by + bh], [bx, by + bh], [bx, by - 6 * S]], k, 8, 4 * S);
        ctx.globalAlpha = 1;
      }
    });
  },
  texts(t, A) {
    return A.lines.map((raw, i) => ({ raw, i })).filter(o => t > A.tLine(o.i) + (o.raw.length) / A.speed)
      .map(o => A.kit.box('l' + o.i, o.raw.replace('@y:', ''), A.W * .1, A.H * .2 + o.i * 120 * A.S, A.W * .8, 110 * A.S));
  },
  cues(A) { return A.lines.map((_, i) => ({ t: A.tLine(i), sfx: 'marker', gain: .5 })); },
};
export default L;
