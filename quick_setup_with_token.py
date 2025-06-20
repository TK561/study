#!/usr/bin/env python3
"""
GitHub Personal Access Token を使用したクイックセットアップ
========================================================

既にお持ちのGitHub APIキー（Personal Access Token）を使用して
研究プロジェクトのGit/GitHub連携を即座にセットアップします。
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_with_token():
    """Personal Access Token を使用したセットアップ"""
    
    print("🚀 GitHub Personal Access Token セットアップ")
    print("=" * 50)
    print()
    
    # トークン入力
    print("📝 GitHub Personal Access Token を入力してください")
    print("   (ghp_ で始まる文字列)")
    print()
    token = input("Token: ").strip()
    
    if not token or not token.startswith('ghp_'):
        print("❌ 無効なトークン形式です")
        return False
    
    # ユーザー情報入力
    print("\n📋 GitHub ユーザー情報を入力してください")
    username = input("GitHub ユーザー名: ").strip()
    email = input("GitHub メールアドレス: ").strip()
    
    # リポジトリ情報
    repo_name = input("リポジトリ名 (例: study): ").strip() or "study"
    
    print("\n🔧 設定を適用中...")
    
    # 1. Git グローバル設定
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', username], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
        print("✅ Git グローバル設定完了")
    except:
        print("❌ Git 設定エラー")
        return False
    
    # 2. GitHub CLI 認証（トークン使用）
    try:
        process = subprocess.Popen(
            ['gh', 'auth', 'login', '--with-token'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=token)
        
        if process.returncode == 0:
            print("✅ GitHub CLI 認証完了")
        else:
            print(f"❌ GitHub CLI 認証エラー: {stderr}")
            return False
    except FileNotFoundError:
        print("⚠️ GitHub CLI がインストールされていません")
        print("   トークンを環境変数に設定します...")
        
        # 環境変数設定（GitHub CLI なしの場合）
        os.environ['GITHUB_TOKEN'] = token
        print("✅ 環境変数 GITHUB_TOKEN 設定完了")
    
    # 3. 現在のディレクトリでGit初期化
    if not Path('.git').exists():
        try:
            subprocess.run(['git', 'init'], check=True)
            print("✅ Git リポジトリ初期化完了")
        except:
            print("❌ Git 初期化エラー")
            return False
    
    # 4. リモートリポジトリ設定
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    
    try:
        # 既存のリモート確認
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            # 既存のリモートを更新
            subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
            print("✅ リモートリポジトリ URL 更新完了")
        else:
            # 新規リモート追加
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
            print("✅ リモートリポジトリ追加完了")
    except:
        print("❌ リモート設定エラー")
        return False
    
    # 5. config.py の更新（存在する場合）
    config_file = Path('config.py')
    if config_file.exists():
        print("\n📝 config.py を更新中...")
        
        # config.py を読み込んで更新
        content = config_file.read_text(encoding='utf-8')
        
        # 値を更新
        replacements = {
            'GITHUB_TOKEN = ""': f'GITHUB_TOKEN = "{token}"',
            'GITHUB_USERNAME = ""': f'GITHUB_USERNAME = "{username}"',
            'REPOSITORY_NAME = ""': f'REPOSITORY_NAME = "{repo_name}"',
            'GITHUB_EMAIL = ""': f'GITHUB_EMAIL = "{email}"'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # 保存
        config_file.write_text(content, encoding='utf-8')
        print("✅ config.py 更新完了")
    
    # 6. 初回コミット準備
    print("\n📦 初回コミットの準備")
    
    # .gitignore 作成（存在しない場合）
    gitignore = Path('.gitignore')
    if not gitignore.exists():
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/

# IDE
.vscode/
.idea/

# Project specific
config.py
*.log
.env
*.tmp

# Data files
*.csv
*.pkl
*.npz
*.npy

# Large files
models/
data/raw/
"""
        gitignore.write_text(gitignore_content)
        print("✅ .gitignore 作成完了")
    
    print("\n🎉 セットアップ完了！")
    print("\n📋 設定内容:")
    print(f"   ユーザー名: {username}")
    print(f"   リポジトリ: {username}/{repo_name}")
    print(f"   認証方式: Personal Access Token")
    
    # 次のステップ
    print("\n🚀 次のステップ:")
    print("1. ファイルを追加してコミット:")
    print(f"   git add .")
    print(f'   git commit -m "Initial commit"')
    print(f"   git push -u origin main")
    print()
    print("2. または自動化スクリプトを使用:")
    print("   python research_git_automation.py --auto-commit")
    print()
    print("3. GitHub でリポジトリを確認:")
    print(f"   https://github.com/{username}/{repo_name}")
    
    return True

def quick_commit_push(message=None):
    """クイックコミット・プッシュ"""
    
    if not message:
        message = input("コミットメッセージ: ") or "Update"
    
    try:
        # ステータス確認
        result = subprocess.run(['git', 'status', '--porcelain'], 
                               capture_output=True, text=True)
        
        if not result.stdout:
            print("ℹ️ 変更がありません")
            return
        
        print("📝 変更ファイル:")
        print(result.stdout)
        
        # 追加・コミット・プッシュ
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        print("✅ コミット・プッシュ完了!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {e}")

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub Token クイックセットアップ")
    parser.add_argument('--setup', action='store_true', help='初期セットアップ実行')
    parser.add_argument('--commit', action='store_true', help='クイックコミット・プッシュ')
    parser.add_argument('-m', '--message', help='コミットメッセージ')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_with_token()
    elif args.commit:
        quick_commit_push(args.message)
    else:
        print("🚀 GitHub Personal Access Token クイックセットアップ")
        print()
        print("使用方法:")
        print("  初期セットアップ: python quick_setup_with_token.py --setup")
        print("  クイックコミット: python quick_setup_with_token.py --commit -m 'メッセージ'")
        print()
        print("既にトークンをお持ちの場合は --setup を実行してください")

if __name__ == "__main__":
    main()