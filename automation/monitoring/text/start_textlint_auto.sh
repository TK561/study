#!/bin/bash
# textlint自動実行システム統合起動スクリプト

echo "🚀 textlint自動実行システムを起動します"
echo ""

# 引数処理
MODE=${1:-"menu"}

show_menu() {
    echo "どのモードで起動しますか？"
    echo ""
    echo "1) 📊 定期チェック (30分ごと)"
    echo "2) 👁️  ファイル監視 (リアルタイム)"
    echo "3) ⏰ スケジュール実行 (指定時刻)"
    echo "4) 🔧 Git hooks セットアップ"
    echo "5) 📈 今すぐチェック"
    echo "6) 🛠️  設定変更"
    echo "0) 終了"
    echo ""
    read -p "選択してください [0-6]: " choice
    
    case $choice in
        1) start_auto_check ;;
        2) start_file_watcher ;;
        3) start_scheduler ;;
        4) setup_git_hooks ;;
        5) run_check_now ;;
        6) configure_system ;;
        0) exit 0 ;;
        *) echo "無効な選択です"; show_menu ;;
    esac
}

start_auto_check() {
    echo ""
    echo "📊 定期チェックモードを起動します"
    echo "デフォルト: 30分ごとにチェック"
    echo ""
    read -p "チェック間隔（分）を指定しますか？ [Enter でデフォルト]: " interval
    
    if [ -n "$interval" ]; then
        python3 textlint_auto_runner.py start --interval $interval
    else
        python3 textlint_auto_runner.py start
    fi
}

start_file_watcher() {
    echo ""
    echo "👁️ ファイル監視モードを起動します"
    echo "ファイルの変更を検出して即座にチェックします"
    echo ""
    read -p "自動修正を有効にしますか？ [y/N]: " auto_fix
    
    if [[ $auto_fix =~ ^[Yy]$ ]]; then
        python3 textlint_watcher.py --auto-fix
    else
        python3 textlint_watcher.py
    fi
}

start_scheduler() {
    echo ""
    echo "⏰ スケジュール実行モードを起動します"
    echo "設定された時刻に自動的にチェックを実行します"
    echo ""
    python3 textlint_scheduler.py start
}

setup_git_hooks() {
    echo ""
    echo "🔧 Git hooksをセットアップします"
    echo "コミット時に自動的にtextlintチェックが実行されます"
    echo ""
    
    if [ -d .git ]; then
        ./setup_textlint_hooks.sh
        echo ""
        read -p "セットアップ完了。メニューに戻りますか？ [Y/n]: " back
        if [[ ! $back =~ ^[Nn]$ ]]; then
            show_menu
        fi
    else
        echo "❌ エラー: Gitリポジトリが見つかりません"
        echo "Gitリポジトリのルートディレクトリで実行してください"
    fi
}

run_check_now() {
    echo ""
    echo "📈 今すぐチェックを実行します"
    echo ""
    echo "1) すべてのファイル"
    echo "2) セッションファイルのみ"
    echo "3) ドキュメントのみ"
    echo "4) 自動修正モード"
    echo ""
    read -p "選択してください [1-4]: " check_mode
    
    case $check_mode in
        1) npm run lint ;;
        2) npm run lint:sessions ;;
        3) npm run lint:docs ;;
        4) npm run lint:fix ;;
        *) echo "無効な選択です" ;;
    esac
    
    echo ""
    read -p "メニューに戻りますか？ [Y/n]: " back
    if [[ ! $back =~ ^[Nn]$ ]]; then
        show_menu
    fi
}

configure_system() {
    echo ""
    echo "🛠️ 設定変更"
    echo ""
    echo "1) 定期チェック設定 (textlint_auto_config.json)"
    echo "2) ファイル監視設定 (textlint_watcher_config.json)"
    echo "3) スケジュール設定 (textlint_scheduler_config.json)"
    echo "4) textlint基本設定 (.textlintrc.json)"
    echo ""
    read -p "選択してください [1-4]: " config_choice
    
    case $config_choice in
        1) ${EDITOR:-nano} textlint_auto_config.json ;;
        2) ${EDITOR:-nano} textlint_watcher_config.json ;;
        3) ${EDITOR:-nano} textlint_scheduler_config.json ;;
        4) ${EDITOR:-nano} .textlintrc.json ;;
        *) echo "無効な選択です" ;;
    esac
    
    echo ""
    read -p "メニューに戻りますか？ [Y/n]: " back
    if [[ ! $back =~ ^[Nn]$ ]]; then
        show_menu
    fi
}

# パッケージチェック
check_dependencies() {
    if ! command -v npm &> /dev/null; then
        echo "❌ npmがインストールされていません"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3がインストールされていません"
        exit 1
    fi
    
    # textlintがインストールされているかチェック
    if ! npm list textlint &> /dev/null; then
        echo "📦 textlintがインストールされていません"
        read -p "今すぐインストールしますか？ [Y/n]: " install
        if [[ ! $install =~ ^[Nn]$ ]]; then
            npm install
        else
            exit 1
        fi
    fi
}

# メイン処理
check_dependencies

case $MODE in
    "auto") start_auto_check ;;
    "watch") start_file_watcher ;;
    "schedule") start_scheduler ;;
    "check") run_check_now ;;
    *) show_menu ;;
esac