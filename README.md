# Slide Studio 紹介サイト

[Slide Studio](https://github.com/edoaki/slide-studio) の実画面・スライドの実例・導入手順を紹介する静的サイトです。

## 手元で確認する

このリポジトリのディレクトリで実行します。Python 3 が必要です。

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

ブラウザで <http://127.0.0.1:8000> を開きます。終了は `Ctrl+C`。依存パッケージのインストールやビルドは不要です。埋め込みスライドの操作を確認するため、HTTP サーバーから開いてください。

## GitHub Pages で公開する

1. このリポジトリを GitHub に push します。
2. **Settings → Pages → Build and deployment → Source** で **GitHub Actions** を選びます。
3. **Actions → Deploy to GitHub Pages → Run workflow** から `main` のワークフローを実行します。以後は `main` への push で更新されます。
4. 実行完了後、**Settings → Pages** または **github-pages** 環境に表示される URL を確認します。

[公開用ワークフロー](.github/workflows/pages.yml) は `index.html`、`styles.css`、`script.js`、`.nojekyll`、`assets/` を公開します。新しいフォルダを追加した場合は、コピー対象も更新してください。

設定の詳細は GitHub 公式の [公開元の設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) と [カスタムワークフロー](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) を参照してください。

## 内容を更新する

- `index.html`：紹介文、埋め込み、導入手順。
- `styles.css`：レイアウト、文字サイズ、スマートフォン向けの表示。
- `script.js`：画像拡大、コピー。
- `assets/slides/nco-intro.html`：実際の nco-intro を書き出した単一 HTML。
- `assets/screenshots/`：最新版 nco-intro のアプリ画面。

埋め込みスライドを更新するときは、Slide Studio で nco-intro を検査してから HTML を書き出し、`assets/slides/nco-intro.html` を差し替えます。テーマや HTML 図も現在の保管フォルダの内容を使います。現在は、マルチエージェントの発表で編集した正式版の mist テーマを反映しています。

画面写真の取得元と再撮影コマンドは [画面写真の記録](assets/screenshots/README.md)、埋め込みの記録は [スライドの記録](assets/slides/README.md) を参照してください。

画像・スクリプト・埋め込みは相対パスを使い、GitHub Pages の `/<リポジトリ名>/` でも表示できる構成です。
