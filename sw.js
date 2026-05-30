const CACHE = 'calcCity-v1';
const ASSETS = [
  '/calculatorcity/',
  '/calculatorcity/index.html',
  '/calculatorcity/assets/css/base.css',
  '/calculatorcity/assets/css/layout.css',
  '/calculatorcity/assets/css/components.css',
  '/calculatorcity/assets/css/calculator.css',
  '/calculatorcity/assets/js/main.js',
  '/calculatorcity/assets/js/charts.js',
];

self.addEventListener('install', e =>
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)))
);

self.addEventListener('activate', e =>
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ))
);

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).catch(() => caches.match('/calculatorcity/')))
  );
});
