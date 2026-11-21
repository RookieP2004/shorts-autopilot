// RS-09 Word Beat — one word per beat, full frame, colour field flipping on every cut; the key word holds longer and
// lands bigger. A 2-4 s hook or a chapter punch, locked to the score's tempo.
// Props: words ["Money", "never", "sleeps"], bpm (90), key (index of the word that holds), palette ("house" | "night")
const L = {
  dur: 3,
  setup(A) {
    const { P } = A;
    A.words = P.words || ['Every', 'rupee', 'has', 'a', 'story'];
    A.beat = 60 / (P.bpm || 96) / (P.half ? 1 : 2);   // eighth notes by default
    A.key = P.key ?? A.words.length - 1;
    A.starts = []; let s = .1; A.words.forEach((_, i) => { A.starts.push(s); s += A.beat * (i === A.key ? 3 : 1); });
    A.end = s; A.DURw = s + .6;
  },
  draw(t, A) {
    const { ctx, kit: K, W, H, S, P } = A;
    const pals = { house: [['#f6efe2', '#16232b'], ['#16232b', '#f6efe2'], ['#f2b04a', '#16232b'], ['#6fc3c0', '#16232b']],
      night: [['#0b0f12', '#f6efe2'], ['#ff3b4a', '#0b0f12'], ['#0b0f12', '#35e08a'], ['#f6efe2', '#0b0f12']] }[P.palette || 'house'];
    let i = A.starts.findIndex((s, j) => t >= s && (j === A.words.length - 1 || t < A.starts[j + 1]));
    if (i < 0) { if (t < A.starts[0]) return; i = A.words.length - 1; }
    const [bg, fg] = i === A.key ? ['#f2b04a', '#16232b'] : pals[i % pals.length];
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    const w = A.words[i], u = t - A.starts[i], isK = i === A.key;
    const px = K.fitText(ctx, w.toUpperCase(), 'anton', W * .88, (isK ? 380 : 300) * S);
    const sc = isK ? 1 + .25 * (1 - K.out3(K.seg(u, 0, .25))) : 1 + .08 * (1 - K.out3(K.seg(u, 0, .12)));
    ctx.save(); ctx.translate(W / 2, H * .5); ctx.scale(sc, sc); ctx.rotate(isK ? 0 : ((i % 2) - .5) * .05);
    ctx.fillStyle = fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = K.font('anton', px);
    ctx.fillText(w.toUpperCase(), 0, 0); ctx.restore();
  },
  texts(t, A) { return t > A.starts[A.key] ? [A.kit.box('key', A.words[A.key], A.W * .06, A.H * .4, A.W * .88, A.H * .2)] : []; },
  cues(A) { return A.starts.map((s, i) => ({ t: s, sfx: i === A.key ? 'hit' : 'click', gain: i === A.key ? .9 : .55 })); },
};
export default L;
