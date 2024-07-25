# CMoD
Circle Manager on Discord

![GitHub Release](https://img.shields.io/github/v/release/CASru-IT/CMoD)
![GitHub Tag](https://img.shields.io/github/v/tag/CASru-IT/CMoD)
![GitHub repo size](https://img.shields.io/github/repo-size/CASru-IT/CMoD)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/CASru-IT/CMoD)


## 概要
Discordを使用して、サークルの管理を行うためのbotです。

# クイックスタート

## 前提条件
- botを動作させることが出来るサーバーが用意されていること
- 動作させる環境にDockerがインストールされていること
- Discord botを作成し、トークンを取得していること

## 手順
1. 任意のサーバーにこのリポジトリをクローンする
2. このリポジトリのルートディレクトリ（botディレクトリの一個上の階層）に.envファイルを作成し、以下の内容を記述する
```
DISCORD_BOT_TOKEN="作成したDiscord botのトークン" 
GUILDS="このbotを使用するサーバーのID(指定できるのは一つのみ)" 
```
3. 以下のコマンドをターミナル上で実行する。(作業ディレクトリはdocker-compose.yamlのあるディレクトリ)
```
docker-compose up --build -d
```
