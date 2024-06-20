# ベースイメージの指定
FROM ruby:3.2.3

# 必要なパッケージをインストール
RUN apt-get update -qq && apt-get install -y \
    nodejs \
    npm \
    postgresql-client

# 作業ディレクトリの設定
WORKDIR /app

# GemfileとGemfile.lockをコピー
COPY ./Gemfile ./Gemfile.lock ./

# bundlerのインストール
RUN gem install bundler -v 2.5.6 && bundle install

# アプリケーションのコードをコピー
COPY . /app

# Webpackをインストール
# RUN npm install

# サーバー起動コマンド
CMD ["bin/rails", "server", "-b", "0.0.0.0"]
