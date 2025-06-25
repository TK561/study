#!/bin/bash
# 自動システム起動スクリプト (Linux/Mac用)

echo "🚀 自動システム起動中..."
cd "$(dirname "$0")"

# 依存関係をインストール
echo "📦 依存関係をインストール中..."
python3 -m pip install watchdog requests --quiet

# マスターコントローラーを開始
echo "🎛️ マスターコントローラー開始..."
python3 auto_master_controller.py start