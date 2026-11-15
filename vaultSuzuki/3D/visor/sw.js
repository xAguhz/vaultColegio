// Service worker del visor del Swift: permite usarlo sin internet.
// Archivos propios (visor, fichas, capas): primero la red, así siempre se ve la última versión; sin conexión, lo guardado.
// Librería 3D y fuentes (CDN, no cambian): primero lo guardado.
const CACHE = 'swift3d-v2';
const BASE = ['./', './index.html', './fichas.json', './capas.json', './circuitos.json', './tecnica.json', './manifest.webmanifest', './icono-192.png'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BASE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  const propio = u.origin === location.origin;
  const cdn = /(^|\.)jsdelivr\.net$|fonts\.(googleapis|gstatic)\.com$/.test(u.hostname);
  if (!propio && !cdn) return;
  if (propio && /\.pdf$/i.test(u.pathname)) return;            // el manual en PDF no se guarda
  e.respondWith(caches.open(CACHE).then(async (c) => {
    if (cdn) {
      const g = await c.match(e.request);
      if (g) return g;
      const r = await fetch(e.request);
      if (r && (r.ok || r.type === 'opaque')) c.put(e.request, r.clone());
      return r;
    }
    try {
      const r = await fetch(e.request, { cache: 'no-cache' });
      if (r && r.ok) c.put(e.request, r.clone());
      return r;
    } catch (err) {
      return (await c.match(e.request, { ignoreSearch: true })) || Response.error();
    }
  }));
});
