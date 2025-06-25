#!/usr/bin/env python3
"""
クイックVercel修正スクリプト
APIエラーを修正してナビゲーションを有効化
"""

import requests
import json
import base64
from datetime import datetime

def quick_deploy():
    """クイックデプロイメント"""
    
    # 環境変数
    VERCEL_TOKEN = "A0FAzBEt0OgzeI7zaqs1J0MD"
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("🔧 クイックVercel修正デプロイ...")
    
    try:
        # api/index.py を読み込み（修正済み）
        with open('api/index.py', 'r', encoding='utf-8') as f:
            api_content = f.read()
        
        # vercel.json を読み込み
        with open('vercel.json', 'r', encoding='utf-8') as f:
            vercel_config = f.read()
        
        # デプロイメントデータ
        files = [
            {
                "file": "api/index.py",
                "data": base64.b64encode(api_content.encode('utf-8')).decode('utf-8')
            },
            {
                "file": "vercel.json",
                "data": base64.b64encode(vercel_config.encode('utf-8')).decode('utf-8')
            }
        ]
        
        deployment_data = {
            "name": "study-research-final",
            "files": files,
            "target": "production"
        }
        
        # デプロイ実行
        response = requests.post("https://api.vercel.com/v13/deployments", 
                               headers=headers, json=deployment_data)
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ デプロイ成功!")
            print(f"🌐 URL: https://study-research-final.vercel.app")
            print(f"⏰ 時刻: {datetime.now().strftime('%H:%M:%S')}")
            return True
        else:
            print(f"❌ エラー: {response.status_code}")
            print(f"詳細: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == "__main__":
    success = quick_deploy()
    if success:
        print("🎉 修正完了! 2-3分で反映されます")
    else:
        print("❌ 修正失敗")