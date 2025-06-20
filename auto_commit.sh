#!/bin/bash

echo "🚀 Auto Git Manager - Quick Commit"
echo "=================================="

python3 auto_git_manager.py --status
echo ""
read -p "自動コミット・プッシュを実行しますか？ (Y/n): " choice

if [[ "$choice" =~ ^[Yy]$ ]] || [[ "$choice" == "" ]]; then
    echo ""
    echo "🚀 自動コミット・プッシュを実行中..."
    python3 auto_git_manager.py --auto-commit
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 自動コミット・プッシュが完了しました！"
    else
        echo ""
        echo "❌ 自動コミット・プッシュに失敗しました。"
        echo "ログファイル git_auto_manager.log を確認してください。"
    fi
else
    echo "キャンセルされました。"
fi

echo ""
read -p "Press Enter to continue..."