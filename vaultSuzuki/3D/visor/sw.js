// Service worker del visor del Swift: guarda el visor, los modelos y la librería 3D para usarlo sin internet.
// Estrategia: responde con lo guardado y actualiza en segundo plano (stale-while-revalidate).
const CACHE = 'swift3d-v1';
const BASE = ['./', './index.html', './fichas.json', './capas.json', './circuitos.json', './manifest.webmanifest', './icono-192.png'];
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
  e.respondWith(caches.open(CACHE).then(async (c) => {
    const guardado = await c.match(e.request, { ignoreSearch: propio });
    const red = fetch(e.request).then((r) => { if (r && (r.ok || r.type === 'opaque')) c.put(e.request, r.clone()); return r; }).catch(() => guardado);
    return guardado || red;
  }));
});
