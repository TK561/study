#!/usr/bin/env python3
"""
ワンコマンドVercelデプロイ - 最も簡単なデプロイ方法
使用方法: python3 vercel_one_command.py
"""

import os
import sys
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path

def print_status(message, status="info"):
    """ステータス表示"""
    icons = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}
    print(f"{icons.get(status, 'ℹ️')} {message}")

def get_vercel_token():
    """Vercelトークンを取得"""
    # 環境変数から取得
    token = os.getenv('VERCEL_TOKEN')
    if token:
        return token
    
    # .envファイルから取得
    env_file = Path('.env')
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('VERCEL_TOKEN='):
                        return line.split('=', 1)[1].strip()
        except:
            pass
    
    # デフォルトトークン
    return "WkO3OyNzgZDXHpRwRgA5GDnL"

def ensure_files():
    """必要なファイルを確認・作成"""
    print_status("必要なファイルを確認中...")
    
    # vercel.json
    vercel_json = Path("vercel.json")
    if not vercel_json.exists():
        with open(vercel_json, 'w') as f:
            json.dump({"version": 2}, f, indent=2)
        print_status("vercel.json を作成しました", "success")
    
    # index.html の場所を確認
    public_index = Path("public/index.html")
    root_index = Path("index.html")
    
    if not public_index.exists():
        if root_index.exists():
            # publicディレクトリを作成してファイルを移動
            Path("public").mkdir(exist_ok=True)
            import shutil
            shutil.copy2(root_index, public_index)
            print_status("index.html を public/ にコピーしました", "success")
        else:
            print_status("index.html が見つかりません", "error")
            return False
    
    return True

def git_commit_and_push():
    """Git操作を実行"""
    try:
        print_status("Git操作を実行中...")
        
        # git add
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        
        # git commit
        commit_message = f"🚀 Auto deploy - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        result = subprocess.run(['git', 'commit', '-m', commit_message], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("Git commit完了", "success")
            
            # git push
            push_result = subprocess.run(['git', 'push'], 
                                       capture_output=True, text=True)
            if push_result.returncode == 0:
                print_status("Git push完了", "success")
            else:
                print_status("Git push失敗（デプロイは継続します）", "warning")
        else:
            if "nothing to commit" in result.stderr:
                print_status("変更なし - Git操作スキップ", "info")
            else:
                print_status("Git commit失敗（デプロイは継続します）", "warning")
                
    except Exception as e:
        print_status(f"Git操作エラー: {e}", "warning")

def deploy_to_vercel():
    """Vercelにデプロイ"""
    print_status("Vercelにデプロイ中...")
    
    token = get_vercel_token()
    
    # ファイルを読み込み
    files = []
    
    # index.html
    index_path = Path("public/index.html")
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            files.append({
                "file": "index.html",
                "data": f.read()
            })
    
    # vercel.json
    vercel_json_path = Path("vercel.json")
    if vercel_json_path.exists():
        with open(vercel_json_path, 'r', encoding='utf-8') as f:
            files.append({
                "file": "vercel.json",
                "data": f.read()
            })
    
    # デプロイメントデータ
    deploy_data = {
        "name": "study-research-final",
        "files": files,
        "target": "production"
    }
    
    # API呼び出し
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "https://api.vercel.com/v13/deployments",
            json=deploy_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print_status("デプロイ成功!", "success")
            
            # URL表示
            url = result.get('url', '')
            if url:
                print_status(f"プレビューURL: https://{url}", "success")
            print_status("本番URL: https://study-research-final.vercel.app", "success")
            
            # デプロイIDも表示
            deploy_id = result.get('id', '')
            if deploy_id:
                print_status(f"デプロイID: {deploy_id}", "info")
            
            return True
        else:
            print_status(f"デプロイ失敗: {response.status_code}", "error")
            print_status(f"エラー詳細: {response.text}", "error")
            return False
            
    except Exception as e:
        print_status(f"デプロイエラー: {e}", "error")
        return False

def main():
    """メイン処理"""
    print("=" * 50)
    print("🚀 ワンコマンドVercelデプロイ")
    print("=" * 50)
    
    # 1. ファイル確認
    if not ensure_files():
        print_status("ファイル確認に失敗しました", "error")
        return False
    
    # 2. Git操作
    git_commit_and_push()
    
    # 3. Vercelデプロイ
    success = deploy_to_vercel()
    
    print("=" * 50)
    if success:
        print_status("🎉 デプロイ完了!", "success")
        print_status("サイトは数分で利用可能になります", "info")
    else:
        print_status("❌ デプロイ失敗", "error")
    print("=" * 50)
    
    return success

if __name__ == "__main__":
    main()