#!/usr/bin/env python3
"""
Vercelデプロイメニューシステム - 対話式デプロイ選択
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """ヘッダー表示"""
    print("=" * 60)
    print("🚀 Vercel デプロイメニューシステム")
    print("=" * 60)

def print_menu():
    """メニュー表示"""
    print("\n📋 デプロイオプションを選択してください:")
    print("1. 🚀 ワンコマンドデプロイ（最速）")
    print("2. 🛠️ 完全デプロイ（詳細設定付き）")
    print("3. 🤖 統合システムデプロイ（AI付き）") 
    print("4. 📊 デプロイ履歴表示")
    print("5. ⚙️ 設定確認")
    print("6. 🆘 ヘルプ")
    print("0. 終了")
    print("-" * 40)

def get_user_choice():
    """ユーザー選択を取得"""
    try:
        choice = input("選択してください (0-6): ").strip()
        return choice
    except KeyboardInterrupt:
        print("\n👋 終了します")
        sys.exit(0)

def run_one_command_deploy():
    """ワンコマンドデプロイ実行"""
    print("\n🚀 ワンコマンドデプロイを実行します...")
    try:
        result = subprocess.run([sys.executable, "vercel_one_command.py"], 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def run_complete_deploy():
    """完全デプロイ実行"""
    print("\n🛠️ 完全デプロイシステムを実行します...")
    try:
        result = subprocess.run([sys.executable, "vercel_complete_deploy.py", "deploy"], 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def run_unified_deploy():
    """統合システムデプロイ実行"""
    print("\n🤖 統合システムデプロイを実行します...")
    try:
        result = subprocess.run([sys.executable, "vercel_unified_system.py", "deploy"], 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def show_deployment_history():
    """デプロイ履歴表示"""
    print("\n📊 デプロイ履歴:")
    
    # 統合システムの履歴
    history_files = [
        "VERCEL_DEPLOYMENT_HISTORY.json",
        "VERCEL_UPDATE_HISTORY.json"
    ]
    
    for history_file in history_files:
        if Path(history_file).exists():
            print(f"\n📁 {history_file}:")
            try:
                result = subprocess.run([sys.executable, "vercel_complete_deploy.py", "history"],
                                      capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                else:
                    print("履歴が見つかりません")
            except:
                print("履歴の読み込みに失敗")

def show_config():
    """設定確認"""
    print("\n⚙️ 現在の設定:")
    
    # 環境変数確認
    print("\n🔑 環境変数:")
    vercel_token = os.getenv('VERCEL_TOKEN')
    if vercel_token:
        print(f"VERCEL_TOKEN: 設定済み ({vercel_token[:10]}...)")
    else:
        print("VERCEL_TOKEN: 未設定")
    
    # ファイル確認
    print("\n📁 プロジェクトファイル:")
    files_to_check = [
        "vercel.json",
        "public/index.html",
        "index.html",
        ".env"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    # Git確認
    print("\n📝 Git状態:")
    if Path(".git").exists():
        print("✅ Gitリポジトリ")
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("⚠️ 未コミットの変更があります")
            else:
                print("✅ 全て最新")
        except:
            print("⚠️ Git状態確認失敗")
    else:
        print("❌ Gitリポジトリではありません")

def show_help():
    """ヘルプ表示"""
    print("\n🆘 ヘルプ:")
    print("""
📋 各デプロイオプションの説明:

1. ワンコマンドデプロイ:
   - 最も簡単で高速
   - 基本的なファイル確認とデプロイのみ
   - Git操作も自動実行

2. 完全デプロイ:
   - 詳細な前提条件チェック
   - 自動修復機能
   - 監視とクリーンアップ

3. 統合システムデプロイ:
   - AI分析機能付き
   - 成功パターン学習
   - 包括的なレポート

📋 必要なファイル:
   - vercel.json (自動作成)
   - public/index.html または index.html
   - VERCEL_TOKEN環境変数

📋 使用方法:
   python3 vercel_deploy_menu.py

📋 直接実行:
   python3 vercel_one_command.py        # ワンコマンド
   python3 vercel_complete_deploy.py    # 完全デプロイ
   bash vercel_quick_deploy.sh          # シェルスクリプト
""")

def main():
    """メイン処理"""
    print_header()
    
    while True:
        print_menu()
        choice = get_user_choice()
        
        if choice == "0":
            print("👋 終了します")
            break
        elif choice == "1":
            success = run_one_command_deploy()
            if success:
                print("\n✅ ワンコマンドデプロイ完了!")
            else:
                print("\n❌ ワンコマンドデプロイ失敗")
        elif choice == "2":
            success = run_complete_deploy()
            if success:
                print("\n✅ 完全デプロイ完了!")
            else:
                print("\n❌ 完全デプロイ失敗")
        elif choice == "3":
            success = run_unified_deploy()
            if success:
                print("\n✅ 統合システムデプロイ完了!")
            else:
                print("\n❌ 統合システムデプロイ失敗")
        elif choice == "4":
            show_deployment_history()
        elif choice == "5":
            show_config()
        elif choice == "6":
            show_help()
        else:
            print("❌ 無効な選択です")
        
        # 継続確認
        if choice in ["1", "2", "3"]:
            input("\nEnterキーを押して続行...")

if __name__ == "__main__":
    main()