// RS-12 Terminal — an old green-phosphor monitor powers on and types out lines like a log, then the key line flashes;
// scanlines, glow, chroma bleed and corner falloff come from Lemo-Opuscar's CRT post (crt.js, MIT, vendored).
// For hacks, leaks, "the system said...", data trails. Props: title, lines ["> ...", ...], key (index), color ("green"|"amber")
import { makePost } from '/reelsmith/vendor/lemo/crt.js';
const L = {
  dur: 5,
  gl: true,
  setup(A) {
    const mk = () => { const c = document.createElement('canvas'); c.width = A.W; c.height = A.H; return c; };
    A.scene = mk(); A.glow = mk(); A.s = A.scene.getContext('2d'); A.gw = A.glow.getContext('2d');
    A.post = makePost(A.canvas);
    A.lines = A.P.lines || ['> connect bank-core-03', '> list transfers --over 10000', '  2,091 results', '> flag suspicious', '  0 flagged'];
    A.key = A.P.key ?? A.lines.length - 1;
    A.cps = 22; let t = .9; A.tL = A.lines.map(l => { const s = t; t += l.length / A.cps + .25; return s; });
    L.dur = t + 1.4;                                      // natural length follows the text
    A.maxLen = Math.max(...A.lines.map(l => l.length), 10);
  },
  draw(t, A) {
    const { s, gw, W, H, S, P, kit: K } = A;
    const col = P.color === 'amber' ? '#ffb000' : '#5cff9a';
    for (const c of [s, gw]) { c.setTransform(1, 0, 0, 1, 0, 0); c.fillStyle = '#000'; c.fillRect(0, 0, W, H); }
    s.fillStyle = '#05100a'; s.fillRect(0, 0, W, H);
    const px = Math.min(64 * S, W * .86 / (A.maxLen * .62)), lh = px * 1.45, x0 = W * .07;
    let y = H * .2;
    const draw = (txt, yy, a = 1, big = false) => {
      for (const c of [s, gw]) { c.font = K.font(big ? 'dotg' : 'mono_b', big ? px * 1.5 : px); c.fillStyle = col; c.globalAlpha = a; c.textAlign = 'left'; c.fillText(txt, x0, yy); c.globalAlpha = 1; }
    };
    if (P.title) draw(String(P.title).toUpperCase(), H * .12, K.seg(t, .6, .8), true);
    A.lines.forEach((l, i) => {
      const n = Math.floor((t - A.tL[i]) * A.cps); if (n <= 0) return;
      const shown = l.slice(0, n), isK = i === A.key && n >= l.length;
      const blink = isK ? (Math.floor((t - A.tL[i] - l.length / A.cps) * 4) % 2 === 0 ? 1 : .35) : 1;
      if (isK) { s.fillStyle = col; s.globalAlpha = .18 * blink; s.fillRect(x0 - 12 * S, y - px * 1.05, W * .86, lh); s.globalAlpha = 1; }
      draw(shown, y, blink);
      if (n < l.length && Math.floor(t * 3) % 2 === 0) { const w = s.measureText(shown).width; s.fillStyle = col; s.fillRect(x0 + w + 4 * S, y - px * .85, px * .55, px); }
      y += lh;
    });
    // CRT: power-on squeeze in the first 0.6 s, gentle tracking wobble
    const power = K.seg(t, 0, .6);
    A.post.render(A.scene, A.glow, Math.floor(t * 30), null, { power, scan: .22, grille: .08, glow: .5, bloom: 1.0 });
  },
  texts(t, A) {
    return A.lines.map((l, i) => ({ l, i })).filter(o => t > A.tL[o.i] + o.l.length / A.cps)
      .map(o => A.kit.box('l' + o.i, o.l, A.W * .07, A.H * .2 + o.i * 80, A.W * .86, 70, o.i !== A.key));
  },
  cues(A) { return [{ t: .05, sfx: 'glitch', gain: .4 }, ...A.lines.map((_, i) => ({ t: A.tL[i], sfx: 'type', gain: .4 })),
    { t: A.tL[A.key] + A.lines[A.key].length / A.cps, sfx: 'error', gain: .6 }]; },
};
export default L;
