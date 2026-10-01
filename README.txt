月読（PWA一式）
================================

■ 入っているもの

  index.html      アプリ本体（画面、カードのデータ、動作のすべて）
  manifest.json   アプリ名、アイコン、起動方法の設定
  sw.js           Service Worker（オフラインで動かすための保存係）
  icons/          ホーム画面用のアイコン
  cards/          自作のカード画像を置く場所（任意）


■ パソコンで試す

  index.html をダブルクリックすると、ブラウザで動きます。
  この開き方ではオフライン保存（Service Worker）は働きませんが、占いはそのまま使えます。

  同じWi-FiにつないだiPhoneから試す場合は、このフォルダで次を実行し、
  iPhoneのSafariで http://(パソコンのIPアドレス):8000 を開きます。

      python3 -m http.server 8000

  この方法は確認用です。ホーム画面に追加してオフラインで使うには、
  下の手順でHTTPSのURLに公開してください。


■ Webに公開する（GitHub Pages、無料）

  1. https://github.com でアカウントを作る
  2. 右上の「+」から New repository を選び、名前（例: tarot）を入れ、Public で作成する
  3. 「uploading an existing file」を開き、このフォルダの中身をすべてドラッグして Commit する
     （icons と cards のフォルダも一緒に入れます）
  4. Settings → Pages を開き、Branch を「main」「/(root)」にして Save する
  5. 1〜2分後、https://(ユーザー名).github.io/(リポジトリ名)/ で開けるようになる

  画面の表記は変わることがあります。GitHub以外では、Cloudflare Pages や Netlify でも
  フォルダをアップロードするだけで公開できます。


■ 配布する

  公開したURLを相手に送ります。

  iPhone   Safariで開く → 共有ボタン →「ホーム画面に追加」
  Android  Chromeで開く → メニュー →「ホーム画面に追加」または「アプリをインストール」

  一度開いておけば、次からは通信がなくても起動します。


■ 内容を変える

  カードの文章    index.html の「大アルカナ22枚」の部分を書き換えます
  カードの絵      cards/README.txt の手順で画像を置きます
  アプリ名        index.html の <title> と見出し、manifest.json の name / short_name を変えます

  変更をアップロードすると、利用者の端末には次々回の起動から反映されます。
  すぐに確実に切り替えたいときは、sw.js の VERSION を "v2" のように上げてください。
