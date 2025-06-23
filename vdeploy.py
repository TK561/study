#!/usr/bin/env python3
"""
vdeploy - 超シンプルVercelデプロイコマンド
使用方法: python3 vdeploy.py
"""

import json
import requests
from pathlib import Path
from datetime import datetime

def deploy():
    """シンプルデプロイ"""
    print("🚀 Vercel デプロイ中...")
    
    # 基本設定
    token = "WkO3OyNzgZDXHpRwRgA5GDnL"
    
    # vercel.json確認・作成
    if not Path("vercel.json").exists():
        with open("vercel.json", 'w') as f:
            json.dump({"version": 2}, f, indent=2)
        print("✅ vercel.json 作成")
    
    # index.html確認
    index_path = Path("public/index.html")
    if not index_path.exists():
        index_path = Path("index.html")
        if index_path.exists():
            Path("public").mkdir(exist_ok=True)
            import shutil
            shutil.copy2(index_path, "public/index.html")
            index_path = Path("public/index.html")
    
    if not index_path.exists():
        print("❌ index.html が見つかりません")
        return False
    
    # ファイル読み込み
    files = []
    with open(index_path, 'r', encoding='utf-8') as f:
        files.append({"file": "index.html", "data": f.read()})
    
    with open("vercel.json", 'r') as f:
        files.append({"file": "vercel.json", "data": f.read()})
    
    # デプロイ
    try:
        response = requests.post(
            "https://api.vercel.com/v13/deployments",
            json={"name": "study-research-final", "files": files, "target": "production"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ デプロイ成功!")
            print(f"🌐 URL: https://study-research-final.vercel.app")
            print(f"🆔 ID: {result.get('id', 'N/A')}")
            return True
        else:
            print(f"❌ 失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == "__main__":
    deploy()