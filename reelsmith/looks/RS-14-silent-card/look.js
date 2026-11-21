// RS-14 Silent Card — a 1920s picture house moment: an optional still irises in on scratched, weaving, flickering film,
// then an art-deco intertitle card holds the line. Film post, dust/hair damage, deco border and iris: Lemo-Opuscar's
// silent-film engine (film.js, cards.js, ink.js; MIT, vendored). Composition, props and timing are ours.
// Props: lines ["In 1929,", "the market fell."] (1-3; the first is the big one), level (0 shout, 1 deco, 2 ornate),
//        image (optional repo path to a still, e.g. a plate), image_dur (s, default 1.6), strength (film wear 0-1, .6)
import { FilmPost, damage } from '/reelsmith/vendor/lemo/silent-film/film.js';
import { intertitle, iris } from '/reelsmith/vendor/lemo/silent-film/cards.js';
const L = {
  dur: 4.5,
  async setup(A) {
    const { P, W, H } = A;
    A.src = document.createElement('canvas'); A.src.width = W; A.src.height = H; A.g = A.src.getContext('2d');
    A.post = new FilmPost(W, H);
    A.lines = (P.lines || ['In 1929,', 'the market fell.']).slice(0, 3);
    if (P.image) { A.img = new Image(); A.img.src = '/' + String(P.image).replace(/^\/+/, ''); await A.img.decode(); }
    A.tCard = A.img ? (P.image_dur ?? 1.6) : 0;
  },
  draw(t, A) {
    const { ctx, g, W, H, S, P, kit: K } = A, frame = Math.floor(t * 18);    // hand-cranked: 18 frames a second
    const str = P.strength ?? .6;
    if (A.img && t < A.tCard) {                                               // the still, sepia, irising in
      g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
      const s = Math.max(W / A.img.width, H / A.img.height) * (1.04 + .04 * t / A.tCard);
      g.filter = 'grayscale(1) contrast(1.15)'; g.drawImage(A.img, W / 2 - A.img.width * s / 2, H / 2 - A.img.height * s / 2, A.img.width * s, A.img.height * s); g.filter = 'none';
      iris(g, W, H, W / 2, H * .45, Math.hypot(W, H) * K.out3(K.seg(t, 0, .7)) * .6 + 1, 40 * S);
    } else {
      if (!A.card) {                                                          // size each line to the card once
        const port = H > W, out = [];
        A.lines.forEach((tx, i) => {
          const big = i === 0, fam = big ? 'Playfair Display SC' : 'Old Standard TT', want = (big ? 150 : 96) * S * (port ? 1 : .9);
          g.font = `${big ? '' : 'italic '}${Math.round(want)}px "${fam}"`;
          const parts = big ? [big ? tx.toUpperCase() : tx] : K.wrap(g, tx, W * .8);
          parts.forEach(pt => { let px = want; g.font = `${big ? '' : 'italic '}${Math.round(px)}px "${fam}"`;
            while (g.measureText(pt).width > W * .8 && px > 20) { px *= .94; g.font = `${big ? '' : 'italic '}${Math.round(px)}px "${fam}"`; }
            out.push({ text: pt, font: fam, size: Math.round(px), italic: !big, caps: false, spacing: big ? 4 : 0, rule: big && A.lines.length > 1 }); });
        });
        A.card = out;
      }
      const lines = A.card;
      intertitle(g, W, H, { lines, level: P.level ?? 1, seed: 3, shake: .25 }, t - A.tCard);
    }
    const out = A.post.render(A.src, { frame, strength: str, sepia: .18, exposure: A.img && t < A.tCard ? .8 : 1 });
    ctx.drawImage(out, 0, 0, W, H);
    damage(ctx, 0, 0, W, H, frame, str);
    if (t < .12 || Math.abs(t - A.tCard) < .06) { ctx.fillStyle = 'rgba(255,248,230,.5)'; ctx.fillRect(0, 0, W, H); }   // splice flash
  },
  texts(t, A) { return t >= A.tCard ? [A.kit.box('card', A.lines.join(' '), A.W * .1, A.H * .3, A.W * .8, A.H * .4)] : []; },
  cues(A) { return [{ t: 0, sfx: 'projector', gain: .5 }, ...(A.img ? [{ t: A.tCard, sfx: 'shutter', gain: .5 }] : [])]; },
};
export default L;
