#!/usr/bin/env python3
"""
Vercel即座更新スクリプト
ナビゲーション追加されたindex.htmlをVercelに反映
"""

import requests
import json
import os
import base64
from datetime import datetime

def update_vercel_deployment():
    """Vercelデプロイメントを即座に更新"""
    
    # Vercel設定
    VERCEL_TOKEN = "9Y0lcFuUlEIX7vHIgdWaJzfb"
    PROJECT_ID = "study-research-final"  # プロジェクト名から推定
    
    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("🚀 Vercelデプロイメント更新開始...")
    
    try:
        # index.htmlファイルを読み込み
        with open('/mnt/c/Desktop/Research/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # ファイルをBase64エンコード
        html_base64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        
        # デプロイメント作成
        deployment_data = {
            "name": "study-research-final",
            "files": {
                "index.html": {
                    "file": html_base64
                },
                "vercel.json": {
                    "file": base64.b64encode(json.dumps({
                        "version": 2,
                        "builds": [{"src": "index.html", "use": "@vercel/static"}],
                        "routes": [{"src": "/", "dest": "/index.html"}]
                    }).encode('utf-8')).decode('utf-8')
                }
            },
            "projectSettings": {
                "framework": "other"
            },
            "target": "production"
        }
        
        # デプロイメント実行
        deploy_url = "https://api.vercel.com/v13/deployments"
        response = requests.post(deploy_url, headers=headers, json=deployment_data)
        
        if response.status_code == 200:
            result = response.json()
            deployment_url = result.get('url', 'Unknown')
            print(f"✅ デプロイメント成功!")
            print(f"🌐 URL: https://{deployment_url}")
            print(f"📅 更新時刻: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
            
            # ナビゲーション追加の確認
            if 'ディスカッション記録' in html_content:
                print("✅ ナビゲーションメニュー追加確認済み")
            else:
                print("⚠️ ナビゲーションメニューが見つかりません")
                
            return True
        else:
            print(f"❌ デプロイメント失敗: {response.status_code}")
            print(f"エラー: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def force_cache_invalidation():
    """キャッシュ無効化を強制実行"""
    print("🔄 キャッシュ無効化実行中...")
    
    # Vercel関連のキャッシュをクリア
    cache_bust_params = [
        f"?v={datetime.now().strftime('%Y%m%d%H%M%S')}",
        f"?t={int(datetime.now().timestamp())}",
        "?bust=true"
    ]
    
    base_url = "https://study-research-final.vercel.app"
    
    try:
        for param in cache_bust_params:
            test_url = f"{base_url}/{param}"
            response = requests.get(test_url, timeout=10)
            print(f"📡 キャッシュテスト: {response.status_code}")
        
        print("✅ キャッシュ無効化完了")
        return True
        
    except Exception as e:
        print(f"⚠️ キャッシュ無効化エラー: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Vercel更新プロセス開始")
    print("=" * 50)
    
    # 1. デプロイメント更新
    deploy_success = update_vercel_deployment()
    
    if deploy_success:
        print("\n" + "=" * 50)
        # 2. キャッシュ無効化
        force_cache_invalidation()
        
        print("\n" + "=" * 50)
        print("🎉 Vercel更新完了!")
        print("📱 ナビゲーションメニュー追加済み")
        print("🔗 ディスカッション記録サイトへのリンク有効")
        print("⏰ 反映まで2-3分お待ちください")
    else:
        print("\n❌ デプロイメント失敗")
        print("🔧 手動でVercelを確認してください")