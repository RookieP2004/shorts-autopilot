// Static file server for look pages (ES modules can't load over file://). 127.0.0.1 only, requests must stay inside root.
// Adapted from Lemo-Opuscar core/render/serve.mjs (MIT, see ../NOTICE).
import http from 'http'; import fs from 'fs'; import path from 'path';
const T = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.hdr': 'application/octet-stream',
  '.glb': 'model/gltf-binary', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf' };
export function resolveRequest(root, url) {
  let u; try { u = decodeURIComponent(url.split('?')[0].split('#')[0]); } catch { return { status: 400 }; }
  if (u.includes('\0')) return { status: 400 };
  const p = path.resolve(root, '.' + path.sep + u.replace(/^\/+/, ''));
  if (p !== root && !p.startsWith(root + path.sep)) return { status: 403 };
  return { path: p };
}
export function serve(root, port = 0) {
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      const send = (c, b) => { r.writeHead(c, { 'Content-Type': 'text/plain' }); r.end(b); };
      if (!/^(127\.0\.0\.1|localhost)(:\d+)?$/.test(q.headers.host || '')) return send(403, 'bad host');
      const x = resolveRequest(root, q.url);
      if (x.status) return send(x.status, 'refused');
      fs.readFile(x.path, (e, d) => {
        if (e) return send(404, 'not found');
        r.writeHead(200, { 'Content-Type': T[path.extname(x.path).toLowerCase()] || 'application/octet-stream' }); r.end(d);
      });
    });
    s.listen(port, '127.0.0.1', () => res({ server: s, port: s.address().port }));
  });
}
