// RS-02 Dot Map — a field of dots (no coastlines, no borders: our map rule), pins drop on named places and dashed
// routes arc between them while the camera drifts toward the last pin. Positions are 0-1 of the frame, so any region works.
// Props: title, points [{name, x, y, tone?}], routes [[i, j, label?], ...], tone ("night" | "paper")
const L = {
  dur: 6,
  setup(A) {
    const { P } = A;
    A.pts = P.points || [{ name: 'Port', x: .25, y: .62 }, { name: 'Hub', x: .55, y: .4 }, { name: 'Market', x: .78, y: .7 }];
    A.routes = P.routes || [[0, 1], [1, 2]];
    A.dark = (P.tone || 'night') === 'night';
    A.tPin = i => .5 + i * .45; A.tRoute = j => A.tPin(A.pts.length - 1) + .4 + j * .6;
    A.field = []; const r = A.kit.rng(P.seed || 9);
    // dot field with soft "land" blobs: density from a few seeded noise centres, never an outline
    const blobs = [...A.pts.map(p => [p.x + (r() - .5) * .1, p.y + (r() - .5) * .08, .22 + r() * .12]), ...[...Array(4)].map(() => [r(), .15 + r() * .8, .14 + r() * .2])];
    for (let y = 0; y < 1; y += .018) for (let x = 0; x < 1; x += .018 * A.H / A.W) {
      let d = 0; for (const [bx, by, br] of blobs) d = Math.max(d, 1 - Math.hypot(x - bx, (y - by) * A.H / A.W) / br);
      if (d > 0.02 || r() < .1) A.field.push([x, y, Math.min(1, d * 1.4)]);
    }
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A, last = A.pts[A.pts.length - 1];
    ctx.fillStyle = A.dark ? '#121c22' : '#efe3c8'; ctx.fillRect(0, 0, W, H);
    // camera: slow push toward the last pin
    const z = 1 + .12 * K.inOut(K.seg(t, 0, A.dur || 6)), fx = K.lerp(.5, last.x, .35 * K.inOut(K.seg(t, 0, 6))), fy = K.lerp(.5, last.y, .35 * K.inOut(K.seg(t, 0, 6)));
    ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-fx * W, -fy * H);
    for (const [x, y, d] of A.field) {
      const a = K.seg(t, Math.hypot(x - .5, y - .5) * .6, Math.hypot(x - .5, y - .5) * .6 + .4);
      ctx.fillStyle = A.dark ? `rgba(111,195,192,${(.16 + .6 * d) * a})` : `rgba(52,66,92,${(.1 + .45 * d) * a})`;
      ctx.beginPath(); ctx.arc(x * W, y * H, (2 + 3.2 * d) * S, 0, K.TAU); ctx.fill();
    }
    // routes: dashed arcs that draw themselves, a dot runs along each
    A.routes.forEach(([i, j, lab], k) => {
      const a = A.pts[i], b = A.pts[j], t0 = A.tRoute(k), p = K.inOut(K.seg(t, t0, t0 + .7)); if (p <= 0) return;
      const ax = a.x * W, ay = a.y * H, bx = b.x * W, by = b.y * H, mx = (ax + bx) / 2, my = (ay + by) / 2 - Math.hypot(bx - ax, by - ay) * .3;
      const q = u => [(1 - u) ** 2 * ax + 2 * (1 - u) * u * mx + u * u * bx, (1 - u) ** 2 * ay + 2 * (1 - u) * u * my + u * u * by];
      ctx.save(); ctx.setLineDash([14 * S, 12 * S]); ctx.lineDashOffset = -t * 40 * S; ctx.lineWidth = 5 * S;
      ctx.strokeStyle = A.dark ? '#f2b04a' : '#d23a2c'; ctx.beginPath(); ctx.moveTo(ax, ay);
      for (let u = 0; u <= p; u += .02) { const [x, y] = q(u); ctx.lineTo(x, y); } ctx.stroke(); ctx.restore();
      const [hx, hy] = q(p); ctx.fillStyle = A.dark ? '#f2b04a' : '#d23a2c'; ctx.beginPath(); ctx.arc(hx, hy, 9 * S, 0, K.TAU); ctx.fill();
      if (lab && p >= 1) { ctx.font = K.font('body', 44 * S); ctx.textAlign = 'center'; ctx.globalAlpha = K.seg(t, t0 + .7, t0 + 1);
        ctx.fillText(lab, mx, my + 40 * S); ctx.globalAlpha = 1; }
    });
    // pins: drop with a bounce, label tag beside
    A.pts.forEach((p, i) => {
      const t0 = A.tPin(i), k = K.seg(t, t0, t0 + .35); if (k <= 0) return;
      const S = A.S * 1.5;
      const x = p.x * W, y = p.y * H - (1 - K.overshoot(k, 2.6)) * 120 * S;
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(p.x * W, p.y * H + 6 * S, 18 * S * k, 6 * S * k, 0, 0, K.TAU); ctx.fill();
      const col = p.tone === 'gold' ? '#f2b04a' : p.tone === 'green' ? '#35e08a' : '#ff3b4a';
      ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y - 44 * S, 22 * S, Math.PI * .85, Math.PI * .15); ctx.lineTo(x, y); ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y - 46 * S, 8 * S, 0, K.TAU); ctx.fill();
      const ka = K.seg(t, t0 + .25, t0 + .5); if (ka <= 0) return;
      ctx.globalAlpha = ka; ctx.font = K.font('body', 34 * S); const tw = ctx.measureText(p.name).width;
      const tx = x + (p.x > .7 ? -tw - 70 * S : 36 * S), ty = y - 84 * S;
      ctx.fillStyle = A.dark ? 'rgba(246,239,226,.95)' : '#1a1410'; K.rrect(ctx, tx, ty, tw + 32 * S, 54 * S, 10 * S); ctx.fill();
      ctx.fillStyle = A.dark ? '#16232b' : '#f6efe2'; ctx.textAlign = 'left'; ctx.fillText(p.name, tx + 16 * S, ty + 39 * S); ctx.globalAlpha = 1;
    });
    ctx.restore();
    if (P.title) {                                          // title strip, outside the camera
      ctx.globalAlpha = K.seg(t, .1, .4); ctx.font = K.font('display', 70 * S); ctx.textAlign = 'center';
      ctx.fillStyle = A.dark ? '#f6efe2' : '#1a1410'; ctx.fillText(P.title, W / 2, H * .12); ctx.globalAlpha = 1;
    }
  },
  texts(t, A) {
    const o = A.P.title ? [A.kit.box('title', A.P.title, 0, A.H * .06, A.W, A.H * .08)] : [];
    A.pts.forEach((p, i) => { if (t > A.tPin(i) + .3) o.push(A.kit.box('pin' + i, p.name, 0, 0, 10, 10, true)); });
    return o;
  },
  cues(A) { return [...A.pts.map((_, i) => ({ t: A.tPin(i) + .3, sfx: 'thud', gain: .5 })), ...A.routes.map((_, j) => ({ t: A.tRoute(j), sfx: 'swoosh_soft', gain: .5 }))]; },
};
export default L;
