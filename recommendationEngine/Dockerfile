# pythonのベースイメージを定義
ARG PYTHON_BASE_IMAGE='python'

# python3.11のイメージを取得 (DockerHubにあるpythonイメージ)
FROM ${PYTHON_BASE_IMAGE}:3.11 AS rye

# Pythonがpycファイルを書き込まないように。
# Pythonはスクリプトが実行されると、対応する.pycファイルを__pycache__ディレクトリに生成するのでそれを防ぐ。(一貫性のため)
ENV PYTHONDONTWRITEBYTECODE=1

# Pythonがstdout(標準出力)とstderr(標準エラー)をバッファリング(データを一定量まとめてから出力)しないように。
# バッファリングを無効にすることで、ログがリアルタイムで出力されるようになる。
ENV PYTHONUNBUFFERED=1

# pythonのパスにワークスペースである、srcディレクトリを追加
ENV PYTHONPATH="/workspace/src:$PYTHONPATH"

# 仮想環境はryeが実行されるワーキングディレクトリを指定。
WORKDIR /workspace

# buildに必要なパッケージをインストール
# build-essential: ソフトウェア開発に必要な基本的なコンパイルツールとライブラリが一括で揃う。例えば、gccやmakeなど。
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ryeのインストール
ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSf https://rye.astral.sh/get |  RYE_INSTALL_OPTION="--yes" bash

# 必要なファイルをコンテナにコピーし、Ryeを使って依存関係をインストール。

COPY pyproject.toml requirements.lock requirements-dev.lock .python-version README.md ./
RUN rye sync --no-dev --no-lock

# 開発環境を有効に
RUN . .venv/bin/activate

# activateスクリプトをソース（sourceまたは.）することで、仮想環境内のPython環境をアクティブにし、その環境内でPythonパッケージが利用できるように。
FROM rye AS dev

# 開発用のイメージを作成し、再度依存関係をインストール。
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

# 多段ビルド：開発環境と本番環境を分けてイメージを作成しているため、不要なファイルを本番イメージに含めない。
# 非特権ユーザー：セキュリティのためにアプリケーションを非特権ユーザーで実行。
# Ryeの利用：Ryeを使ってPython環境と依存関係を管理。
# 環境変数の設定：パフォーマンスやデバッグのための環境変数を適切に設定。