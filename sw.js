const CACHE_NAME = 'calcCity-v2';
const CORE_ASSETS = [
  '/calculatorcity/',
  '/calculatorcity/index.html',
  '/calculatorcity/assets/css/base.css',
  '/calculatorcity/assets/css/layout.css',
  '/calculatorcity/assets/css/components.css',
  '/calculatorcity/assets/css/calculator.css',
  '/calculatorcity/assets/js/main.js',
  '/calculatorcity/assets/js/charts.js',
  '/calculatorcity/assets/icons/favicon.svg',
  '/calculatorcity/assets/og-image.svg',
];

self.addEventListener('install', e =>
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(CORE_ASSETS)).then(() => self.skipWaiting()))
);

self.addEventListener('activate', e =>
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  )
);

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        if (!response || response.status !== 200 || response.type !== 'basic') return response;
        const clone = response.clone();
        caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
        return response;
      }).catch(() => caches.match('/calculatorcity/'));
    })
  );
});
