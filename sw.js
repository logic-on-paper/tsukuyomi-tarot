/* 月読 Service Worker
   ファイルを端末に保存し、通信がなくてもアプリを起動できるようにします。
   アプリを更新したら VERSION の数字を上げてください（例: "v2"）。古い保存分が消えます。 */
const VERSION = "v2";
const PREFIX = "tsukiakari-tarot-";
const CACHE = PREFIX + VERSION;

// 初回に保存しておくファイル
const CORE = [
  "./",
  "index.html",
  "manifest.json",
  "icons/icon-180.png",
  "icons/icon-192.png",
  "icons/icon-512.png"
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
