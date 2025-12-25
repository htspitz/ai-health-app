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

# 7. Streamlit用のポート（8501）を開放
EXPOSE 8501

# 8. コンテナ起動時にStreamlitを実行する設定
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]