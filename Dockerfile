# 1. ベースとなるOSとPython環境を選択
FROM python:3.11-slim

# 2. 作業ディレクトリを作成
WORKDIR /app

# 3. OSの依存パッケージをインストール（GiNZAのビルド等に必要な最小限のもの）
RUN apt-get update && apt-get install -y \
    sqlite3 \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. 必要なファイルをコピー
COPY requirements.txt .

# 5. ライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# 6. アプリケーションコードをコピー
COPY app.py .

# 7. FastAPI用のポート（8000）を開放
EXPOSE 8000

# 8. コンテナ起動時にFastAPIを実行する設定
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]