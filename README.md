# AI健康診断要約アプリ

このプロジェクトは、健康診断の結果テキストから個人情報を匿名化し、LLMを用いて分かりやすく要約するアプリケーションのプロトタイプです。

## 🚀 主な機能
- **個人情報の匿名化**: `GiNZA (spaCy)` を使用し、氏名や生年月日を自動でマスキング。
- **健康診断の要約**: 複雑な診断結果をAIが噛み砕いて要約。
- **データベース保存**: `SQLite` を使用し、処理結果を永続化。
- **コンテナ化**: `Docker` / `Docker Compose` により、環境を問わず1コマンドで起動可能。

## 🛠 使用技術
- **Language**: Python 3.12
- **NLP**: GiNZA / spaCy
- **Database**: SQLite3
- **Infrastructure**: Docker / Docker Compose

## 📦 起動方法
```bash
docker-compose up --build