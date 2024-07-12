# CMoD
Circle Manager on Discord

## 概要
Discordのbotを使用して、サークルの管理を行うためのbotです。

## 機能

## 前提条件
- Dockerがインストールされていること
- Discord botを作成し、トークンを取得していること

## 使い方
1. このリポジトリをクローンする
2. このリポジトリのルートディレクトリ（botディレクトリの一個上の階層）に.envファイルを作成し、以下の内容を記述する
```
DISCORD_BOT_TOKEN="作成したDiscord botのトークン" 
GUILDS="このbotを使用するサーバーのID(カンマ区切りで複数指定可)" 
```
3. 以下のコマンドをターミナル上で実行する。
```
docker-compose up --build　-d
```
