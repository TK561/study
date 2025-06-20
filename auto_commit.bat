@echo off
chcp 65001 > nul
echo 🚀 Auto Git Manager - Quick Commit
echo ==================================

python auto_git_manager.py --status
echo.
echo 自動コミット・プッシュを実行しますか？ (Y/N)
set /p choice="選択: "

if /i "%choice%"=="Y" (
    echo.
    echo 🚀 自動コミット・プッシュを実行中...
    python auto_git_manager.py --auto-commit
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ 自動コミット・プッシュが完了しました！
    ) else (
        echo.
        echo ❌ 自動コミット・プッシュに失敗しました。
        echo ログファイル git_auto_manager.log を確認してください。
    )
) else (
    echo キャンセルされました。
)

echo.
pause