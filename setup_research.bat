@echo off
chcp 65001 > nul
title 研究プロジェクト自動化システム セットアップ

echo.
echo 🔬 研究プロジェクト自動化システム セットアップ
echo ================================================
echo.
echo このスクリプトは Claude Code を活用した研究プロジェクトの
echo GitHub自動化システムを一括でセットアップします。
echo.
echo 📋 セットアップ内容:
echo   ✅ 設定ファイルの準備と検証
echo   ✅ Git リポジトリの初期化  
echo   ✅ GitHub Actions ワークフローの設定
echo   ✅ VS Code タスクの設定
echo   ✅ 研究プロジェクト構造の作成
echo   ✅ 初回コミット・プッシュ
echo.
echo 📝 必要な情報:
echo   • GitHub Personal Access Token
echo   • GitHubユーザー名
echo   • リポジトリ名
echo   • メールアドレス
echo   • 研究機関名
echo   • 研究者名
echo.
pause

cls
echo 🚀 セットアップを開始します...
echo.

python setup_research_automation.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ セットアップが完了しました！
    echo.
    echo 🎯 今すぐ使用可能な機能:
    echo   • python research_git_automation.py --auto-commit  ^(自動コミット^)
    echo   • python research_git_automation.py --status       ^(状態確認^)
    echo   • python semantic_classification_system.py        ^(メインシステム^)
    echo.
    echo 📱 VS Code での使用方法:
    echo   • Ctrl+Shift+P → "Tasks: Run Task" → タスク選択
    echo   • 推奨タスク: "🚀 Research Commit: Auto Commit & Push"
    echo.
    echo 🔄 日常的なワークフロー:
    echo   1. Claude Code で研究作業
    echo   2. 自動コミット・プッシュでバックアップ
    echo   3. GitHub Actions で品質管理
    echo   4. Cursor IDE で継続開発
    echo.
    echo 📚 詳細情報:
    echo   • CLAUDE.md          - 研究ガイドライン
    echo   • README.md          - 使用方法
    echo   • config.py          - システム設定
    echo.
    
    set /p open_vscode="VS Code でプロジェクトを開きますか？ (Y/n): "
    if /i not "%open_vscode%"=="n" (
        echo.
        echo 🎯 VS Code を起動中...
        code .
    )
) else (
    echo.
    echo ❌ セットアップに失敗しました。
    echo.
    echo 🔧 トラブルシューティング:
    echo   1. Python 3.8以上がインストールされているか確認
    echo   2. Gitがインストールされているか確認  
    echo   3. config.py に正しい値が設定されているか確認
    echo   4. インターネット接続を確認
    echo.
    echo 📞 サポート:
    echo   - ログファイル: research_automation.log を確認
    echo   - 設定検証: python research_git_automation.py --validate-config
)

echo.
echo 🎉 Claude Code + GitHub + Cursor IDE = 最強の研究環境
echo 効率的で高品質な研究開発をお楽しみください！
echo.
pause