@echo off
echo 🚀 自動システム起動中...
cd /d "%~dp0"

REM 依存関係をインストール
echo 📦 依存関係をインストール中...
python3 -m pip install watchdog requests --quiet

REM マスターコントローラーを開始
echo 🎛️ マスターコントローラー開始...
python3 auto_master_controller.py start

pause