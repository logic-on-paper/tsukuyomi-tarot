/* 月読 Service Worker
   ファイルを端末に保存し、通信がなくてもアプリを起動できるようにします。
   アプリを更新したら VERSION の数字を上げてください（例: "v2"）。古い保存分が消えます。 */
const VERSION = "v15";
const PREFIX = "tsukiakari-tarot-";
const CACHE = PREFIX + VERSION;

// 初回に保存しておくファイル
const CORE = [
  "./",
  "index.html",
  "manifest.json",
  "readings/love.js",
  "readings/friend.js",
  "readings/study.js",
  "readings/oshi.js",
  "readings/self.js",
  "readings/extra.js",
  "readings/blunt.js",
  "icons/icon-180.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "cards/00.jpg",
  "cards/01.jpg",
  "cards/02.jpg",
  "cards/03.jpg",
  "cards/04.jpg",
  "cards/05.jpg",
  "cards/06.jpg",
  "cards/07.jpg",
  "cards/08.jpg",
  "cards/09.jpg",
  "cards/10.jpg",
  "cards/11.jpg",
  "cards/12.jpg",
  "cards/13.jpg",
  "cards/14.jpg",
  "cards/15.jpg",
  "cards/16.jpg",
  "cards/17.jpg",
  "cards/18.jpg",
  "cards/19.jpg",
  "cards/20.jpg",
  "cards/21.jpg",
  "cards/22.jpg",
  "cards/23.jpg",
  "cards/24.jpg",
  "cards/25.jpg",
  "cards/26.jpg",
  "cards/27.jpg",
  "cards/28.jpg",
  "cards/29.jpg",
  "cards/30.jpg",
  "cards/31.jpg",
  "cards/32.jpg",
  "cards/33.jpg",
  "cards/34.jpg",
  "cards/35.jpg",
  "cards/36.jpg",
  "cards/37.jpg",
  "cards/38.jpg",
  "cards/39.jpg",
  "cards/40.jpg",
  "cards/41.jpg",
  "cards/42.jpg",
  "cards/43.jpg",
  "cards/44.jpg",
  "cards/45.jpg",
  "cards/46.jpg",
  "cards/47.jpg",
  "cards/48.jpg",
  "cards/49.jpg",
  "cards/50.jpg",
  "cards/51.jpg",
  "cards/52.jpg",
  "cards/53.jpg",
  "cards/54.jpg",
  "cards/55.jpg",
  "cards/56.jpg",
  "cards/57.jpg",
  "cards/58.jpg",
  "cards/59.jpg",
  "cards/60.jpg",
  "cards/61.jpg",
  "cards/62.jpg",
  "cards/63.jpg",
  "cards/64.jpg",
  "cards/65.jpg",
  "cards/66.jpg",
  "cards/67.jpg",
  "cards/68.jpg",
  "cards/69.jpg",
  "cards/70.jpg",
  "cards/71.jpg",
  "cards/72.jpg",
  "cards/73.jpg",
  "cards/74.jpg",
  "cards/75.jpg",
  "cards/76.jpg",
  "cards/77.jpg",
  "cards/back.jpg"
];

// インストール時：必要なファイルをまとめて保存する
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(CORE)).then(() => self.skipWaiting())
  );
});

// 有効化時：前のバージョンの保存分を消す
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k.startsWith(PREFIX) && k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// 通信の中継：保存分があればすぐ返し、裏で新しい版を取りに行って次回に備える
self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(req, { ignoreSearch: true });
    const fresh = fetch(req)
      .then(res => {
        if (res.ok) cache.put(req, res.clone());
        return res;
      })
      .catch(() => null);

    if (cached) {
      event.waitUntil(fresh);
      return cached;
    }
    const res = await fresh;
    if (res) return res;
    if (req.mode === "navigate") {
      const home = await cache.match("index.html");
      if (home) return home;
    }
    return Response.error();
  })());
});
