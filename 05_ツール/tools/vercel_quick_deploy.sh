#!/bin/bash
# Vercel クイックデプロイスクリプト
# 使用方法: ./vercel_quick_deploy.sh または bash vercel_quick_deploy.sh

echo "🚀 Vercel クイックデプロイ開始"
echo "================================"

# Python環境確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません"
    exit 1
fi

# 必要なPythonパッケージをインストール
echo "📦 必要なパッケージをインストール中..."
pip3 install requests --quiet

# ワンコマンドデプロイを実行
echo "🚀 デプロイ実行中..."
python3 vercel_one_command.py

echo "✅ クイックデプロイ完了"