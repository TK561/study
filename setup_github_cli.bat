@echo off
chcp 65001 > nul
title GitHub CLI セットアップ

echo.
echo 🚀 GitHub CLI セットアップ & 研究プロジェクト連携
echo ================================================
echo.

:: GitHub CLI インストールチェック
where gh >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ GitHub CLI がインストールされていません
    echo.
    echo 📥 インストール方法:
    echo.
    echo 1. Windows Package Manager (推奨):
    echo    winget install --id GitHub.cli
    echo.
    echo 2. Scoop:
    echo    scoop install gh
    echo.
    echo 3. Chocolatey:
    echo    choco install gh
    echo.
    echo 4. 手動ダウンロード:
    echo    https://cli.github.com/
    echo.
    echo インストール後、このスクリプトを再実行してください。
    pause
    exit /b 1
)

echo ✅ GitHub CLI がインストールされています
gh --version
echo.

:: 認証チェック
echo 🔐 認証状態をチェック中...
gh auth status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ GitHub CLI が認証されていません
    echo.
    echo 認証を開始します...
    echo.
    
    set /p auth_method="認証方法を選択してください (1: ブラウザ, 2: トークン): "
    
    if "%auth_method%"=="2" (
        echo.
        echo Personal Access Token を使用した認証を行います。
        echo.
        echo 📝 必要な権限:
        echo   • repo (Full control of private repositories)
        echo   • workflow (Update GitHub Action workflows)
        echo   • read:org (Read org and team membership)
        echo.
        echo トークンは以下から作成できます:
        echo https://github.com/settings/tokens/new
        echo.
        set /p token="Personal Access Token を入力してください: "
        echo %token% | gh auth login --with-token
    ) else (
        echo.
        echo ブラウザ認証を開始します...
        gh auth login
    )
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ 認証に失敗しました
        pause
        exit /b 1
    )
)

echo.
echo ✅ GitHub CLI 認証済み
gh auth status
echo.

:: 研究プロジェクト用設定
echo 🔬 研究プロジェクト用設定
echo =========================
echo.

:: 現在のディレクトリをリポジトリとして初期化するか確認
if exist .git (
    echo 📁 既存のGitリポジトリが検出されました
    
    :: リモートリポジトリの確認
    git remote get-url origin >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ リモートリポジトリ設定済み:
        git remote get-url origin
    ) else (
        echo ⚠️ リモートリポジトリが設定されていません
        set /p create_remote="GitHubにリポジトリを作成しますか？ (Y/n): "
        if /i not "%create_remote%"=="n" (
            set /p repo_name="リポジトリ名を入力してください: "
            set /p repo_desc="リポジトリの説明を入力してください: "
            
            echo.
            echo 🚀 GitHubリポジトリを作成中...
            gh repo create "%repo_name%" --source=. --description "%repo_desc%" --public --push
            
            if %ERRORLEVEL% EQU 0 (
                echo ✅ リポジトリ作成完了
            ) else (
                echo ❌ リポジトリ作成に失敗しました
            )
        )
    )
) else (
    echo ❌ Gitリポジトリが初期化されていません
    set /p init_git="Gitリポジトリを初期化しますか？ (Y/n): "
    if /i not "%init_git%"=="n" (
        git init
        echo ✅ Gitリポジトリを初期化しました
        
        set /p create_remote="GitHubにリポジトリを作成しますか？ (Y/n): "
        if /i not "%create_remote%"=="n" (
            set /p repo_name="リポジトリ名を入力してください: "
            set /p repo_desc="リポジトリの説明を入力してください: "
            
            echo.
            echo 🚀 GitHubリポジトリを作成中...
            gh repo create "%repo_name%" --source=. --description "%repo_desc%" --public --push
            
            if %ERRORLEVEL% EQU 0 (
                echo ✅ リポジトリ作成完了
            ) else (
                echo ❌ リポジトリ作成に失敗しました
            )
        )
    )
)

echo.
echo 📚 利用可能なコマンド
echo =====================
echo.
echo 🔧 基本的なGitHub CLIコマンド:
echo   gh repo view                    - リポジトリ情報表示
echo   gh issue create                 - Issue作成
echo   gh pr create                    - Pull Request作成
echo   gh workflow list                - ワークフロー一覧
echo   gh workflow run workflow.yml    - ワークフロー実行
echo.
echo 🔬 研究プロジェクト用コマンド:
echo   python github_cli_research.py repo-create [name]    - リポジトリ作成
echo   python github_cli_research.py issue [title]         - Issue作成
echo   python github_cli_research.py pr [title]            - PR作成
echo   python github_cli_research.py workflow list         - ワークフロー一覧
echo   python github_cli_research.py info                  - リポジトリ情報
echo.
echo 📋 研究ワークフロー例:
echo   1. 実験ブランチ作成: git checkout -b experiment/new-method
echo   2. 実験実施・コミット: git add . && git commit -m "実験: 新手法"
echo   3. プッシュ: git push -u origin experiment/new-method
echo   4. PR作成: gh pr create --title "実験: 新手法の検証"
echo   5. レビュー・マージ: gh pr merge
echo.

:: エイリアス設定
echo 🎯 便利なエイリアス設定
echo ======================
echo.
set /p setup_alias="GitHub CLI エイリアスを設定しますか？ (Y/n): "
if /i not "%setup_alias%"=="n" (
    echo.
    echo エイリアスを設定中...
    
    :: 研究用エイリアス
    gh alias set prc "pr create --draft --title"
    gh alias set issues "issue list --assignee @me"
    gh alias set runs "run list --limit 10"
    gh alias set wf "workflow"
    gh alias set rv "repo view"
    
    echo.
    echo ✅ エイリアス設定完了:
    echo   gh prc "タイトル"    - ドラフトPR作成
    echo   gh issues           - 自分のIssue一覧
    echo   gh runs             - 最近の実行履歴
    echo   gh wf               - ワークフロー
    echo   gh rv               - リポジトリ情報
)

echo.
echo ✅ GitHub CLI セットアップ完了！
echo.
echo 🚀 次のステップ:
echo   1. gh pr create で Pull Request を作成
echo   2. gh issue create で Issue を作成
echo   3. gh workflow run でワークフローを実行
echo.
echo 詳細なヘルプ: gh --help
echo.
pause