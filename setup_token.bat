@echo off
chcp 65001 > nul
title GitHub Personal Access Token 簡単セットアップ

echo.
echo 🔑 GitHub Personal Access Token 簡単セットアップ
echo ================================================
echo.
echo このスクリプトは、お持ちのGitHub APIキー（Personal Access Token）を
echo 使用して、すぐにGitHub連携を開始できます。
echo.
pause

python quick_setup_with_token.py --setup

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ セットアップ完了！
    echo.
    echo 🎯 今すぐ使えるコマンド:
    echo.
    echo 📝 変更をコミット・プッシュ:
    echo    python quick_setup_with_token.py --commit -m "変更内容"
    echo.
    echo 🚀 または研究用自動化:
    echo    python research_git_automation.py --auto-commit
    echo.
    echo 📊 状態確認:
    echo    git status
    echo    gh repo view  ^(GitHub CLI使用時^)
    echo.
    
    set /p first_commit="今すぐ初回コミットを実行しますか？ (Y/n): "
    if /i not "%first_commit%"=="n" (
        git add .
        git commit -m "🎉 Initial commit with GitHub integration"
        git push -u origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo ✅ 初回コミット完了！
            echo 🌐 GitHubで確認: https://github.com/YOUR_USERNAME/YOUR_REPO
        )
    )
) else (
    echo.
    echo ❌ セットアップに失敗しました
)

echo.
pause