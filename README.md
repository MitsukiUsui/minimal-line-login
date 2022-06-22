## About

これは、[LINEログイン](https://developers.line.biz/ja/docs/line-login/)
の公式サンプル（[line-api-use-case-line-login](https://github.com/line/line-api-use-case-line-login)
）を最小限のスタックで再実装したものです。それぞれ以下のように対応します。

| スタック | 公式サンプル     | 本レポジトリ   |
|---------|------------|----------|
| バックエンド | AWS lambda | Flask    |
| フロントエンド | Nuxt       | 生のHTML   |
| データベース | DynamoDB   | インメモリ    |
| LINE連携 | LINE Front-end Framework | 生のAPI |

公式サンプルはAWSのサーバーレスアプリケーションモデルに従っているのに対し、本レポジトリはFlaskの入ったローカルPython環境があれば実行することができます。

## Getting Started

### Lineチャネル

1. Line Developersコンソールからプロバイダーとチャネルを作成する
    *
    詳しい説明は[LINEログイン](https://developers.line.biz/ja/docs/line-login/getting-started/#line-login-starter-app-prerequisites)
    の公式ドキュメントにあります。
2. チャネルのLINEログイン設定のコールバックURLを `http://127.0.0.1:5000/callback` に設定する
3. チャネルIDとシークレットを環境変数に登録する

### Python環境

```
poetry install
poetry shell
```

* poetryがない場合は、pipで必要なライブラリを入れてください

## Usage

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

`http://127.0.0.1:5000`にアプリが立ち上がります。 各ページの役割は以下の通りです。

| パス        | 役割                            |
|-----------|-------------------------------|
| /         | ログインボタンを表示する                  |
| /login    | LINEログインにリダイレクトする　            |
| /callback | LINEログインから戻り、トークンとプロフィールを取得する |
| /mypage | プロフィールとログアウトボタンを表示する          | 

詳しいロジックは `app.py` を見てください。
