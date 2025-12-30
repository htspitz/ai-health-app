# 🏥 AI保健師相談室 (AI Health Advisor)

健康診断の結果や日々の体調の悩みを、個人情報を守りながらAIに相談できるWebアプリケーションです。

## 🌟 主な機能
- **個人情報の匿名化 (Pii Masking)**: GiNZA (spaCy) を使用し、氏名、住所、病院名、日付などを自動でマスキングしてからAIに送信します。
- **AIによる健康アドバイス**: ローカルLLM (Ollama / Qwen2.5:3b) を活用し、ユーザーに寄り添ったポジティブな要約とアドバイスを提供します。
- **相談履歴の保存**: 過去の相談内容をSQLiteデータベースに保存。Streamlitの `st.fragment` を利用し、画面全体をリロードせずに履歴をスムーズに確認できます。
- **タイムゾーン対応**: 日本時間 (JST) で正確に履歴を記録します。

## 🏗️ 技術スタック
- **Frontend**: Streamlit
- **Backend**: FastAPI (Python 3.11)
- **AI Engine**: Ollama (Model: qwen2.5:3b)
- **Natural Language Processing**: GiNZA / spaCy (ja_ginza)
- **Database**: SQLite / SQLAlchemy
- **Container**: Docker / Docker Compose
- **Editor**: GitHub Copilot / Cursor / Cline

## 📂 フォルダ構成
- `app.py`: Streamlit フロントエンド
- `main.py`: FastAPI バックエンド（司令塔）
- `engine.py`: 匿名化ロジック & AIリクエスト処理
- `database.py`: データベース定義 & CRUD操作
- `schemas.py`: Pydanticによるデータ定義
- `docker-compose.yml`: 環境構築設定

## 🚀 セットアップ方法

### 1. Ollamaの準備（ホストPC側）
ローカル環境でOllamaを起動し、モデルをプルしておきます。

`ollama run qwen2.5:3b`

### 2. コンテナの起動
プロジェクトのルートディレクトリで以下のコマンドを実行します。

`docker-compose up -d`

### 3. アプリケーションへのアクセス
- Frontend (Streamlit): http://localhost:8501
- Backend (FastAPI Docs): http://localhost:8000/docs

## 🔒 セキュリティについて
本アプリはAI（外部/ローカルモデル）へデータを送信する前に、必ず engine.py 内の mask_entities 関数を通過させ、個人情報を [Person] や [Location] といったタグに置き換えます。これにより、プライバシーを保護した状態での相談を可能にしています。