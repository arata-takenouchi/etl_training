FROM python:3.11-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust

# Pythonパッケージの依存関係をコピー
COPY requirements.txt .

# Pythonパッケージをインストール
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# アプリケーションのファイルをコピー
COPY . .

# 出力ディレクトリを作成
RUN mkdir -p output

# コンテナ起動時のコマンドを設定
CMD ["python", "simple_etl.py"]
