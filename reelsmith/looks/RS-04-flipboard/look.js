// RS-04 Flipboard — a split-flap board (station departures style, our own drawing) clacks from one number to another,
// digit by digit, the last digit settling late; a caption flips in under it. Hooks and "the number is..." reveals.
// Props: from (number), to (number), prefix ("₹"), suffix, label, tone ("gold" | "red" | "green")
const L = {
  dur: 4,
  setup(A) {
    const { P } = A;
    // digits group in threes with a narrow comma tile; a long number may pass compact: "1.92B" style text instead
    const grp = s => P.group === false ? s : s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    A.to = P.text ?? grp(String(P.to ?? 1000000));
    A.from = P.text ? A.to.replace(/[0-9]/g, '0') : grp(String(P.from ?? 0).padStart(String(P.to ?? 1000000).length, '0'));
    A.chars = (P.prefix || '') + A.to + (P.suffix || '');
    A.fromChars = (P.prefix || '') + A.from + (P.suffix || '');
    A.n = A.chars.length;
    A.wOf = c => (c === ',' || c === '.') ? .38 : 1;
    const units = [...A.chars].reduce((s, c) => s + A.wOf(c), 0);
    A.tile = Math.min(A.W * .9 / (units * 1.08), 170 * A.S);
    A.settle = i => .5 + i * .16 + (i === A.n - 1 ? .35 : 0);
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A, tw = A.tile, th = tw * 1.45, gap = tw * .08;
    const tot = [...A.chars].reduce((s, c) => s + A.wOf(c) * tw + gap, -gap), x0 = W / 2 - tot / 2, y0 = H * .44 - th / 2;
    let xc = x0;
    const col = { gold: '#f2b04a', red: '#ff3b4a', green: '#35e08a' }[P.tone || 'gold'];
    ctx.globalAlpha = K.seg(t, 0, .2);
    for (let i = 0; i < A.n; i++) {
      const target = A.chars[i], start = A.fromChars[i], ts = A.settle(i), x = xc, tw0 = tw; xc += A.wOf(target) * tw + gap;
      if (A.wOf(target) < 1) { ctx.fillStyle = t >= ts ? ({ gold: '#f2b04a', red: '#ff3b4a', green: '#35e08a' }[P.tone || 'gold']) : '#f6efe2';
        ctx.font = K.font('bebas', th * .8); ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillText(target, x + tw * .19, y0 + th * .92); continue; }
      // until it settles, the tile cycles through digits at 14 flips a second
      let ch = target, phase = 1;
      if (/[0-9]/.test(target) && t < ts) {
        const k = Math.max(0, t - .15) * 14 + i * 3; ch = t < .15 ? start : String(Math.floor(k) % 10); phase = k % 1;
      }
      ctx.fillStyle = '#0f1418'; K.rrect(ctx, x, y0, tw, th, 10 * S); ctx.fill();
      const g = ctx.createLinearGradient(0, y0, 0, y0 + th); g.addColorStop(0, '#2a333a'); g.addColorStop(.5, '#1c2328'); g.addColorStop(.5, '#151b1f'); g.addColorStop(1, '#232b31');
      ctx.fillStyle = g; K.rrect(ctx, x + 3 * S, y0 + 3 * S, tw - 6 * S, th - 6 * S, 8 * S); ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.rect(x, y0, tw, th); ctx.clip();
      ctx.fillStyle = t >= ts ? col : '#f6efe2'; ctx.font = K.font('bebas', th * .92); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      // the flap: the top half folds down over the first 40% of each flip
      const fold = phase < .4 ? Math.cos(phase / .4 * Math.PI / 2) : 1;
      ctx.save(); ctx.translate(x + tw / 2, y0 + th / 2); ctx.scale(1, phase < .4 ? Math.max(.05, fold) : 1);
      ctx.fillText(ch, 0, th * .04); ctx.restore(); ctx.restore();
      ctx.fillStyle = 'rgba(0,0,0,.6)'; ctx.fillRect(x, y0 + th / 2 - 2 * S, tw, 4 * S);       // the hinge
      if (t >= ts && t < ts + .25) { ctx.fillStyle = `rgba(255,255,255,${.35 * (1 - (t - ts) / .25)})`; K.rrect(ctx, x, y0, tw, th, 10 * S); ctx.fill(); }
    }
    if (P.label) {
      const tl = A.settle(A.n - 1) + .15, k = K.seg(t, tl, tl + .3);
      ctx.globalAlpha = k; ctx.fillStyle = '#f6efe2'; ctx.font = K.font('body', 62 * S); ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
      const lines = K.wrap(ctx, P.label, W * .84); lines.forEach((l, j) => ctx.fillText(l, W / 2, y0 + th + 110 * S + j * 76 * S));
    }
    ctx.globalAlpha = 1;
  },
  texts(t, A) {
    const o = [], th = A.tile * 1.45;
    if (t > A.settle(A.n - 1)) o.push(A.kit.box('num', A.chars, A.W * .05, A.H * .44 - th / 2, A.W * .9, th));
    if (A.P.label && t > A.settle(A.n - 1) + .3) o.push(A.kit.box('label', A.P.label, A.W * .08, A.H * .44 + th / 2 + 40 * A.S, A.W * .84, 140 * A.S));
    return o;
  },
  cues(A) {
    const c = [{ t: .15, sfx: 'riser', gain: .35 }];
    for (let i = 0; i < A.n; i++) if (/[0-9]/.test(A.chars[i])) c.push({ t: A.settle(i), sfx: 'tick', gain: .6 });
    c.push({ t: A.settle(A.n - 1), sfx: 'hit', gain: .9 }); return c;
  },
};
export default L;
