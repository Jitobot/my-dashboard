# My Dashboard

ブラウザで開いてフルスクリーン（F11）にするだけで使える、個人用ダッシュボードWebアプリケーションです。

## 機能

- **時計** - 日付・曜日・時刻をリアルタイム表示
- **天気** - 47都道府県対応。現在の天気・気温・湿度に加え、翌日までの時間帯別降水確率を棒グラフで表示（Open-Meteo API）
- **今日の予定** - Googleカレンダーから今日のイベントを取得。終了時刻を過ぎた予定は自動で非表示
- **ToDo** - Google Tasksから今日のタスクを取得。チェックボックスで完了切替（Google側にも反映）
- **メモ** - 自由記述。入力後1秒で自動保存（SQLite）
- **ブックマーク** - よく使うサイトへのショートカット。追加・削除可能
- **ニュース** - NHKニュースの最新ヘッドラインを自動取得（15分更新）

## 使用技術

- **バックエンド**: Python 3.10+ / FastAPI
- **フロントエンド**: Jinja2 + JavaScript + CSS Grid
- **データベース**: SQLite + SQLAlchemy
- **外部API**: Open-Meteo（天気）、Google Calendar API、Google Tasks API、NHK RSS（ニュース）

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/<ユーザー名>/my-dashboard.git
cd my-dashboard
```

### 2. Python仮想環境を作成

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Mac/Linux
source .venv/bin/activate
```

### 3. パッケージインストール

```bash
pip install -r requirements.txt
```

### 4. Google API認証の設定

Googleカレンダー・ToDoの連携に必要です。

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. 「APIとサービス」→「ライブラリ」から以下を有効化:
   - Google Calendar API
   - Google Tasks API
3. 「OAuth同意画面」を設定（外部 / テストユーザーに自分のGmailを追加）
4. 「認証情報」→「OAuthクライアントID」を作成（デスクトップアプリ）
5. JSONをダウンロードし、プロジェクトルートに `credentials.json` として配置

### 5. サーバー起動

```bash
uvicorn app.main:app --reload
```

ブラウザで http://localhost:8000 を開きます。

初回アクセス時にGoogleの認証画面が開くので、許可してください。認証後 `token.json` が自動保存され、2回目以降は不要です。

## 注意事項

- `credentials.json` と `token.json` は `.gitignore` に含まれています。**絶対にGitにコミットしないでください**
- 天気の都市選択はブラウザの `localStorage` に保存されます
- メモとブックマークは `dashboard.db`（SQLite）に保存されます

## ライセンス

MIT
