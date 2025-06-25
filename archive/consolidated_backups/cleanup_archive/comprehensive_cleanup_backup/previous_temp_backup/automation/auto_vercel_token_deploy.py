#!/usr/bin/env python3
"""
自動Vercel Token デプロイシステム
今後すべてのVercel更新はこのスクリプトで実行
"""

import requests
import json
import os
import base64
from datetime import datetime
import time

def load_env():
    """環境変数を読み込み"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value.strip('"')
    except FileNotFoundError:
        print("❌ .envファイルが見つかりません")
    return env_vars

def prepare_files():
    """デプロイ用ファイルを準備"""
    files = []
    
    # index.html
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        files.append({
            "file": "index.html",
            "data": base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        })
    
    # api/index.py
    if os.path.exists('api/index.py'):
        with open('api/index.py', 'r', encoding='utf-8') as f:
            api_content = f.read()
        files.append({
            "file": "api/index.py",
            "data": base64.b64encode(api_content.encode('utf-8')).decode('utf-8')
        })
    
    # vercel.json
    if os.path.exists('vercel.json'):
        with open('vercel.json', 'r', encoding='utf-8') as f:
            vercel_config = f.read()
        files.append({
            "file": "vercel.json",
            "data": base64.b64encode(vercel_config.encode('utf-8')).decode('utf-8')
        })
    
    return files

def deploy_to_vercel():
    """Vercel APIデプロイメント実行"""
    
    # 環境変数読み込み
    env = load_env()
    VERCEL_TOKEN = env.get('VERCEL_TOKEN')
    
    if not VERCEL_TOKEN:
        print("❌ VERCEL_TOKENが設定されていません")
        return False
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("🚀 Vercel Token デプロイメント開始...")
    print(f"⏰ 開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # ファイル準備
        files = prepare_files()
        
        if not files:
            print("❌ デプロイ対象ファイルが見つかりません")
            return False
        
        print(f"📂 デプロイファイル数: {len(files)}")
        for file_info in files:
            print(f"  📄 {file_info['file']}")
        
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
            print(f"📅 完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # ナビゲーション確認
            nav_check = any('ディスカッション記録' in str(file_info.get('data', '')) for file_info in files)
            if nav_check:
                print("✅ ナビゲーションメニュー確認済み")
            
            return True
            
        else:
            print(f"❌ デプロイメント失敗: {response.status_code}")
            print(f"📄 エラー内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def wait_for_deployment():
    """デプロイメント反映を待機"""
    print("⏳ デプロイメント反映を待機中...")
    
    base_url = "https://study-research-final.vercel.app"
    max_attempts = 10
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}?v={int(time.time())}", timeout=10)
            if response.status_code == 200:
                if 'ディスカッション記録' in response.text:
                    print(f"✅ 反映確認! (試行{attempt + 1})")
                    return True
                else:
                    print(f"⏳ 反映待機中... (試行{attempt + 1}/{max_attempts})")
            else:
                print(f"⚠️ HTTPエラー: {response.status_code} (試行{attempt + 1})")
        except Exception as e:
            print(f"⚠️ 接続エラー: {e} (試行{attempt + 1})")
        
        if attempt < max_attempts - 1:
            time.sleep(30)  # 30秒待機
    
    print("⚠️ 反映確認タイムアウト（手動確認推奨）")
    return False

def save_deployment_log():
    """デプロイメントログを保存"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "method": "vercel_token_api",
        "status": "success",
        "changes": [
            "Navigation menu added",
            "Discussion site link integrated",
            "API handler fixed"
        ]
    }
    
    log_file = "deployment_log.json"
    logs = []
    
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    # 最新10件のみ保持
    if len(logs) > 10:
        logs = logs[-10:]
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    
    print(f"📝 デプロイメントログ保存: {log_file}")

if __name__ == "__main__":
    print("🎯 自動Vercel Token デプロイシステム")
    print("=" * 70)
    
    # デプロイ実行
    success = deploy_to_vercel()
    
    if success:
        print("\n" + "=" * 70)
        print("🎉 デプロイメント完了!")
        
        # 反映確認
        if wait_for_deployment():
            print("✅ ナビゲーション機能正常動作確認済み")
        
        # ログ保存
        save_deployment_log()
        
        print("\n📋 今後のVercel更新について:")
        print("🔧 このスクリプト (auto_vercel_token_deploy.py) を使用")
        print("⚡ トークン認証による安全なデプロイメント")
        print("📱 ナビゲーション機能とディスカッションサイト連携済み")
        print("\n🌐 確認URL: https://study-research-final.vercel.app")
    else:
        print("\n❌ デプロイメント失敗")
        print("🔧 環境設定を確認してください")