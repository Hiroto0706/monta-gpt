FROM python:3.11-slim

WORKDIR /migration

COPY . .

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# 環境変数をデフォルト設定（必要に応じて上書き可能）
ENV DATABASE_URL="postgresql://postgres:password@postgres:5432/monta-gpt"

CMD ["alembic", "upgrade", "head"]
