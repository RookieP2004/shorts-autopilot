// Reelsmith kit: deterministic helpers every look shares. The first block (clamp ... env) is adapted from
// Lemo-Opuscar core/lib.js (MIT, ../NOTICE); the drawing helpers below it are ours.
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const smooth = t => { t = clamp(t); return t * t * (3 - 2 * t); };
export const inOut = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const out3 = t => 1 - Math.pow(1 - clamp(t), 3);
export const in3 = t => Math.pow(clamp(t), 3);
export const overshoot = (t, s = 1.8) => { t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s); };
export const spring = (t, k = 7, z = .35) => { t = Math.max(0, t); return 1 - Math.exp(-z * k * t) * Math.cos(k * Math.sqrt(1 - z * z) * t * 1.6); };
export function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
export const noise1 = x => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(hash(i), hash(i + 1), u); };
export const TAU = Math.PI * 2;
export const env = (t, a, b, fi = .3, fo = .3) => Math.min(seg(t, a, a + fi), 1 - seg(t, b - fo, b));
export function monotone(keys) {   // [[t, v], ...] -> smooth curve without overshoot (Fritsch-Carlson)
  const n = keys.length, xs = keys.map(k => k[0]), ys = keys.map(k => k[1]);
  if (n === 1) return () => ys[0];
  const d = [], m = new Array(n).fill(0);
  for (let i = 0; i < n - 1; i++) d.push((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]));
  m[0] = d[0]; m[n - 1] = d[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
  for (let i = 0; i < n - 1; i++) {
    if (d[i] === 0) { m[i] = m[i + 1] = 0; continue; }
    const a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b;
    if (s > 9) { const k = 3 / Math.sqrt(s); m[i] = k * a * d[i]; m[i + 1] = k * b * d[i]; }
  }
  return t => {
    if (t <= xs[0]) return ys[0]; if (t >= xs[n - 1]) return ys[n - 1];
    let i = 0; while (t > xs[i + 1]) i++;
    const h = xs[i + 1] - xs[i], u = (t - xs[i]) / h, u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * ys[i] + (u3 - 2 * u2 + u) * h * m[i] + (-2 * u3 + 3 * u2) * ys[i + 1] + (u3 - u2) * h * m[i + 1];
  };
}

// ---- ours: house palette, type and drawing helpers ----
export const C = { night: '#16232b', night2: '#24343d', cream: '#f6efe2', paper: '#efe3c8', ink: '#1a1410', gold: '#f2b04a',
  teal: '#6fc3c0', red: '#d9534f', navy: '#34425c', green: '#35e08a', alarm: '#ff3b4a', coin: '#f4c04e', data: '#4aa3ff' };
export const font = (fam, px) => `${Math.round(px)}px ${fam}`;
export function fitText(ctx, text, fam, maxW, maxPx, minPx = 10) {   // the biggest size that fits maxW
  let px = maxPx; ctx.font = font(fam, px);
  while (px > minPx && ctx.measureText(text).width > maxW) { px *= 0.94; ctx.font = font(fam, px); }
  return px;
}
export function wrap(ctx, text, maxW) {
  const words = String(text).split(/\s+/), lines = []; let cur = '';
  for (const w of words) { const n = cur ? cur + ' ' + w : w; if (ctx.measureText(n).width > maxW && cur) { lines.push(cur); cur = w; } else cur = n; }
  if (cur) lines.push(cur); return lines;
}
export function rrect(ctx, x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2); ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
}
// a hand-drawn line: the same wobble every frame (seeded), drawn up to fraction k of its length
export function inkLine(ctx, pts, k = 1, seed = 1, wob = 2) {
  const r = rng(seed), P = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i], [x1, y1] = pts[i + 1], n = Math.max(2, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / 18));
    for (let j = 0; j < n; j++) { const u = j / n; P.push([lerp(x0, x1, u) + (r() - .5) * wob, lerp(y0, y1, u) + (r() - .5) * wob]); }
  }
  P.push(pts[pts.length - 1]);
  const m = Math.max(1, Math.floor((P.length - 1) * clamp(k)) + 1);
  ctx.beginPath(); ctx.moveTo(P[0][0], P[0][1]); for (let i = 1; i < m; i++) ctx.lineTo(P[i][0], P[i][1]); ctx.stroke();
  return P[m - 1];
}
// paper / film grain baked from a seed, so it holds still between frames unless `boil` asks it to move
export function grain(ctx, W, H, amt = .06, seed = 7, cell = 3) {
  const r = rng(seed); ctx.save();
  for (let y = 0; y < H; y += cell * 7) for (let x = 0; x < W; x += cell * 7) {
    const v = r(); if (v < .5) continue; ctx.fillStyle = `rgba(0,0,0,${amt * (v - .5)})`; ctx.fillRect(x + r() * 6 * cell, y + r() * 6 * cell, cell, cell);
  }
  ctx.restore();
}
export const fmtNum = (v, dp = 0) => Number(v).toLocaleString('en-IN', { minimumFractionDigits: dp, maximumFractionDigits: dp });
// a number that rolls from a to b between t0 and t1 (eased), for counters
export const roll = (t, t0, t1, a, b) => lerp(a, b, out3(seg(t, t0, t1)));
// a text box for the reading check (TEXTS)
export const box = (id, text, x, y, w, h, pass = false) => ({ id, text, x0: x, y0: y, x1: x + w, y1: y + h, pass });
