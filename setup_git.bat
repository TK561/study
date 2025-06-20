@echo off
chcp 65001 > nul
echo 🚀 Auto Git Manager - Setup
echo ================================
echo.
echo このスクリプトでGitHub Personal Access Tokenを使用した
echo 自動Git管理環境をセットアップします。
echo.
echo 必要な情報:
echo - GitHubユーザー名
echo - メールアドレス  
echo - Personal Access Token (repo権限が必要)
echo - リポジトリURL
echo.
pause

python auto_git_manager.py --setup

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ セットアップが完了しました！
    echo.
    echo VS Codeで以下のタスクが利用可能です:
    echo - Ctrl+Shift+P → "Tasks: Run Task" → "Git Auto Commit & Push"
    echo - ショートカット: Ctrl+Shift+G Ctrl+Shift+P
    echo.
    echo 今すぐ自動コミット・プッシュを実行しますか？ (Y/N)
    set /p choice="選択: "
    if /i "%choice%"=="Y" (
        echo.
        echo 🚀 自動コミット・プッシュを実行中...
        python auto_git_manager.py --auto-commit
    )
) else (
    echo.
    echo ❌ セットアップに失敗しました。
    echo ログファイル git_auto_manager.log を確認してください。
)

echo.
pause