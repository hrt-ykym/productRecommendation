ARG PYTHON_BASE_IMAGE='python'

FROM ${PYTHON_BASE_IMAGE}:3.11 AS rye

# Pythonがpycファイルを書き込まないようにします。
ENV PYTHONDONTWRITEBYTECODE=1

# Pythonがstdoutとstderrをバッファリングしないようにします。
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH="/workspace/src:$PYTHONPATH"

# 仮想環境はryeが実行されるワーキングディレクトリで作成されるため、
# 開発環境と本番環境はそれぞれ同一のディレクトリにする必要があります。
WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

# RYE_INSTALL_OPTIONはビルドに必要です。
RUN curl -sSf https://rye.astral.sh/get |  RYE_INSTALL_OPTION="--yes" bash

# 依存関係のダウンロードを別のステップとして行います。
COPY pyproject.toml requirements.lock requirements-dev.lock .python-version README.md ./
RUN rye sync --no-dev --no-lock

RUN . .venv/bin/activate

# 開発のためのステージ。
FROM rye AS dev

# ファイルをコンテナにコピーします。
COPY pyproject.toml requirements.lock requirements-dev.lock .python-version README.md ./
RUN rye sync --no-lock

# 本番用のステージ
FROM rye AS run

# アプリケーションが実行する非特権ユーザーを作成します。
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY . .

# 仮想環境ディレクトリと必要なディレクトリの作成と権限を変更
RUN mkdir -p /workspace /nonexistent /workspace/.venv && \
    chown -R appuser:appuser /workspace /nonexistent /workspace/.venv

# アプリケーションを実行するために非特権ユーザーに切り替えます。
USER appuser

CMD ["rye", "run", "recommendationengine"]
