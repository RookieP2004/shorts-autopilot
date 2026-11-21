// RS-15 Ink Brush — rice paper, one loaded brush: an open circle (ensō) sweeps around the key word with dry-brush streaks
// where the ink runs out, a heavy stroke underlines it, and a red seal stamps the corner. Brush engine: Lemo-Opuscar's
// ink-wash ink.js (MIT, vendored): bristles, pressure profiles, flying-white streaks. Composition and props are ours.
// Props: word (big, 1-2 words), sub (a line under it), seal ("E" by default: 1-2 letters), tone ("ink" | "sepia")
import { mk, draw, TONE } from '/reelsmith/vendor/lemo/ink-wash-ink.js';
const L = {
  dur: 4.5,
  setup(A) {
    const { W, H, S } = A, cx = W / 2, cy = H * (H > W ? .42 : .4), R = Math.min(W, H) * (H > W ? .36 : .28);
    const pts = []; for (let i = 0; i <= 28; i++) { const a = -2.0 + i / 28 * (Math.PI * 2 * .9); pts.push([cx + Math.cos(a) * R * (1 + .03 * Math.sin(i)), cy + Math.sin(a) * R * .96, 1]); }
    A.enso = mk(pts, { w: 64 * S, tone: TONE.jiao, dry: .45, prof: 'brush', seed: 7 });
    const y = cy + R * 1.16;
    A.under = mk([[cx - R * .9, y + 8 * S, .6], [cx - R * .1, y - 6 * S, 1], [cx + R * .85, y + 4 * S, .5]], { w: 34 * S, tone: TONE.nong, dry: .55, prof: 'nail', seed: 11 });
    A.cx = cx; A.cy = cy; A.R = R;
  },
  draw(t, A) {
    const { ctx, W, H, S, P, kit: K } = A;
    // rice paper: warm, fibrous, uneven
    ctx.fillStyle = P.tone === 'sepia' ? '#efe3c8' : '#f3eee2'; ctx.fillRect(0, 0, W, H);
    const r = K.rng(5); ctx.strokeStyle = 'rgba(120,100,70,.07)'; ctx.lineWidth = 1.2 * S;
    for (let i = 0; i < 260; i++) { const x = r() * W, y = r() * H, a = r() * 6.28, l = (8 + r() * 30) * S; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); ctx.stroke(); }
    K.grain(ctx, W, H, .05, 9, 2 * S);
    const ink = { wet: ctx, dry: ctx };
    draw(ink, A.enso, K.inOut(K.seg(t, .25, 1.35)), 1);
    // the word lands with the brush's last pass: big serif, ink-black, slight bleed shadow
    const kw = K.seg(t, 1.1, 1.5);
    if (kw > 0) {
      const word = String(P.word ?? 'Patience'); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      const px = K.fitText(ctx, word, 'display', A.R * 1.55, 200 * S); ctx.font = K.font('display', px);
      ctx.globalAlpha = kw * .25; ctx.fillStyle = '#1a1410'; ctx.fillText(word, A.cx + 3 * S, A.cy + 4 * S);
      ctx.globalAlpha = kw; ctx.fillText(word, A.cx, A.cy); ctx.globalAlpha = 1; ctx.textBaseline = 'alphabetic';
    }
    draw(ink, A.under, K.out3(K.seg(t, 1.6, 2.1)), 1);
    if (P.sub) { const k = K.seg(t, 2.0, 2.4); ctx.globalAlpha = k; ctx.fillStyle = '#3a2f25'; ctx.font = K.font('serif_i', (H > W ? 62 : 54) * S); ctx.textAlign = 'center';
      K.wrap(ctx, P.sub, W * .8).forEach((l, i) => ctx.fillText(l, A.cx, A.cy + A.R * 1.16 + 110 * S + i * 66 * S)); ctx.globalAlpha = 1; }
    // red seal, stamped
    const ks = K.seg(t, 2.5, 2.62);
    if (ks > 0) {
      const s = 110 * S, x = W * .84 - s / 2, y = H * (H > W ? .2 : .2) - s / 2, sc = 1 + .25 * (1 - ks);
      ctx.save(); ctx.translate(x + s / 2, y + s / 2); ctx.scale(sc, sc); ctx.rotate(-.05); ctx.globalAlpha = .9 * ks;
      ctx.fillStyle = '#b8322a'; K.rrect(ctx, -s / 2, -s / 2, s, s, 10 * S); ctx.fill();
      ctx.fillStyle = '#f3eee2'; ctx.font = K.font('display', s * .62); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(String(P.seal ?? 'E').slice(0, 2), 0, 4 * S);
      ctx.restore(); ctx.textBaseline = 'alphabetic';
    }
  },
  texts(t, A) {
    const o = t > 1.5 ? [A.kit.box('word', String(A.P.word ?? 'Patience'), A.cx - A.R, A.cy - 120 * A.S, A.R * 2, 240 * A.S)] : [];
    if (A.P.sub && t > 2.4) o.push(A.kit.box('sub', A.P.sub, A.W * .1, A.cy + A.R * 1.1, A.W * .8, 160 * A.S));
    return o;
  },
  cues() { return [{ t: .25, sfx: 'swoosh_soft', gain: .5 }, { t: 1.6, sfx: 'paper', gain: .45 }, { t: 2.5, sfx: 'stamp', gain: .7 }]; },
};
export default L;
