#!/bin/bash

echo "🚀 Auto Git Manager - Setup"
echo "================================"
echo ""
echo "このスクリプトでGitHub Personal Access Tokenを使用した"
echo "自動Git管理環境をセットアップします。"
echo ""
echo "必要な情報:"
echo "- GitHubユーザー名"
echo "- メールアドレス"
echo "- Personal Access Token (repo権限が必要)"
echo "- リポジトリURL"
echo ""
read -p "続行しますか？ (Y/n): " choice

if [[ "$choice" =~ ^[Yy]$ ]] || [[ "$choice" == "" ]]; then
    python3 auto_git_manager.py --setup
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ セットアップが完了しました！"
        echo ""
        echo "VS Codeで以下のタスクが利用可能です:"
        echo "- Ctrl+Shift+P → 'Tasks: Run Task' → 'Git Auto Commit & Push'"
        echo "- ショートカット: Ctrl+Shift+G Ctrl+Shift+P"
        echo ""
        read -p "今すぐ自動コミット・プッシュを実行しますか？ (Y/n): " commit_choice
        
        if [[ "$commit_choice" =~ ^[Yy]$ ]] || [[ "$commit_choice" == "" ]]; then
            echo ""
            echo "🚀 自動コミット・プッシュを実行中..."
            python3 auto_git_manager.py --auto-commit
        fi
    else
        echo ""
        echo "❌ セットアップに失敗しました。"
        echo "ログファイル git_auto_manager.log を確認してください。"
    fi
else
    echo "セットアップがキャンセルされました。"
fi

echo ""
read -p "Press Enter to continue..."