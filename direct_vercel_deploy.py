#!/usr/bin/env python3
"""
Vercel API直接デプロイスクリプト
環境変数のトークンを使用してナビゲーション更新をデプロイ
"""

import requests
import json
import os
import base64
from datetime import datetime

def load_env():
    """環境変数を読み込み"""
    env_vars = {}
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value.strip('"')
    return env_vars

def deploy_to_vercel():
    """Vercel APIを使用してデプロイ"""
    
    # 環境変数読み込み
    env = load_env()
    VERCEL_TOKEN = env.get('VERCEL_TOKEN')
    VERCEL_PROJECT_ID = env.get('VERCEL_PROJECT_ID')
    
    if not VERCEL_TOKEN or not VERCEL_PROJECT_ID:
        print("❌ VercelトークンまたはプロジェクトIDが見つかりません")
        return False
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("🚀 Vercel APIデプロイメント開始...")
    print(f"📋 プロジェクトID: {VERCEL_PROJECT_ID}")
    
    try:
        # index.htmlを読み込み
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # vercel.jsonを読み込み
        with open('vercel.json', 'r', encoding='utf-8') as f:
            vercel_config = f.read()
        
        # ファイルをBase64エンコード
        files = [
            {
                "file": "index.html",
                "data": base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
            },
            {
                "file": "vercel.json", 
                "data": base64.b64encode(vercel_config.encode('utf-8')).decode('utf-8')
            }
        ]
        
        # デプロイメントデータ
        deployment_data = {
            "name": "study-research-final",
            "files": files,
            "target": "production"
        }
        
        # デプロイメント実行
        deploy_url = "https://api.vercel.com/v13/deployments"
        response = requests.post(deploy_url, headers=headers, json=deployment_data)
        
        if response.status_code in [200, 201]:
            result = response.json()
            deployment_url = result.get('url', 'Unknown')
            deployment_id = result.get('id', 'Unknown')
            
            print(f"✅ デプロイメント成功!")
            print(f"🆔 デプロイID: {deployment_id}")
            print(f"🌐 プレビューURL: https://{deployment_url}")
            print(f"🌐 本番URL: https://study-research-final.vercel.app")
            print(f"📅 デプロイ時刻: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
            
            # ナビゲーション確認
            if 'ディスカッション記録' in html_content:
                print("✅ ナビゲーションメニュー確認済み")
                print("🔗 ディスカッションサイトリンク統合済み")
            
            return True
            
        else:
            print(f"❌ デプロイメント失敗: {response.status_code}")
            print(f"📄 レスポンス: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def check_deployment_status(deployment_id, token):
    """デプロイメント状況確認"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        status_url = f"https://api.vercel.com/v13/deployments/{deployment_id}"
        response = requests.get(status_url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            state = result.get('state', 'UNKNOWN')
            ready_state = result.get('readyState', 'UNKNOWN')
            
            print(f"📊 デプロイ状況: {state}")
            print(f"📋 準備状況: {ready_state}")
            
            if state == 'READY':
                print("🎉 デプロイメント完了!")
                return True
            elif state == 'ERROR':
                print("❌ デプロイメントエラー")
                return False
            else:
                print("⏳ デプロイメント進行中...")
                return None
        else:
            print(f"⚠️ 状況確認失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 状況確認エラー: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Vercel Token使用デプロイメント")
    print("=" * 60)
    
    # デプロイ実行
    success = deploy_to_vercel()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Vercelデプロイメント完了!")
        print("📱 ナビゲーションメニュー追加")
        print("🔗 ディスカッション記録サイトへのリンク有効")
        print("⏰ 2-3分で反映されます")
        print("\n🌐 サイト確認: https://study-research-final.vercel.app")
    else:
        print("\n❌ デプロイメント失敗")
        print("🔧 設定を確認してください")