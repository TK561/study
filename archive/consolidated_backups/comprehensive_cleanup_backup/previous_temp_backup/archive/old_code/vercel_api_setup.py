#!/usr/bin/env python3
"""
Vercel API 連携スクリプト
Claude Code により生成
目的: Vercel APIを使用した自動デプロイ・管理
"""

import os
import json
import requests
import base64
from pathlib import Path

class VercelAPIManager:
    def __init__(self):
        """Vercel API管理クラス初期化"""
        self.load_env()
        self.base_url = "https://api.vercel.com"
        self.headers = {
            "Authorization": f"Bearer {self.vercel_token}",
            "Content-Type": "application/json"
        }
    
    def load_env(self):
        """環境変数読み込み"""
        env_path = Path(__file__).parent / ".env"
        if not env_path.exists():
            raise FileNotFoundError("❌ .envファイルが見つかりません")
        
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
        
        self.vercel_token = os.getenv('VERCEL_TOKEN')
        self.project_id = os.getenv('VERCEL_PROJECT_ID')
        self.org_id = os.getenv('VERCEL_ORG_ID')
        
        if not self.vercel_token or self.vercel_token == "[新しいトークンを設定してください]":
            print("⚠️ VERCEL_TOKENを設定してください")
            print("https://vercel.com/account/tokens で新しいトークンを作成")
            return False
        return True
    
    def test_connection(self):
        """Vercel API接続テスト"""
        try:
            response = requests.get(f"{self.base_url}/v2/user", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Vercel API接続成功: {user_data.get('name', 'Unknown')}")
                return True
            else:
                print(f"❌ API接続失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 接続エラー: {e}")
            return False
    
    def get_project_info(self):
        """プロジェクト情報取得"""
        try:
            url = f"{self.base_url}/v9/projects/{self.project_id}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                project = response.json()
                print(f"📂 プロジェクト: {project.get('name')}")
                print(f"🌐 URL: https://{project.get('name')}.vercel.app")
                return project
            else:
                print(f"❌ プロジェクト取得失敗: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ エラー: {e}")
            return None
    
    def deploy_project(self, files_content=None):
        """プロジェクトデプロイ"""
        try:
            # api/index.py の内容を読み込み
            api_file = Path(__file__).parent / "api" / "index.py"
            if not api_file.exists():
                print("❌ api/index.py が見つかりません")
                return False
            
            with open(api_file, 'r', encoding='utf-8') as f:
                api_content = f.read()
            
            # Base64エンコード
            api_encoded = base64.b64encode(api_content.encode('utf-8')).decode('utf-8')
            
            # vercel.json の内容読み込み
            vercel_json_file = Path(__file__).parent / "vercel.json"
            with open(vercel_json_file, 'r', encoding='utf-8') as f:
                vercel_config = json.load(f)
            
            vercel_encoded = base64.b64encode(json.dumps(vercel_config).encode('utf-8')).decode('utf-8')
            
            # デプロイメント作成
            deploy_data = {
                "name": "research-update",
                "files": [
                    {
                        "file": "api/index.py",
                        "data": api_encoded
                    },
                    {
                        "file": "vercel.json", 
                        "data": vercel_encoded
                    }
                ],
                "projectSettings": {
                    "framework": None
                }
            }
            
            url = f"{self.base_url}/v13/deployments"
            # 既存プロジェクトを指定
            if self.project_id:
                deploy_data["target"] = "production"
            response = requests.post(url, headers=self.headers, json=deploy_data)
            
            if response.status_code in [200, 201]:
                deployment = response.json()
                deploy_url = deployment.get('url', '')
                print(f"✅ デプロイ成功: https://{deploy_url}")
                return True
            else:
                print(f"❌ デプロイ失敗: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ デプロイエラー: {e}")
            return False
    
    def list_deployments(self):
        """デプロイメント一覧取得"""
        try:
            url = f"{self.base_url}/v6/deployments"
            params = {"projectId": self.project_id, "limit": 5}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                deployments = response.json().get('deployments', [])
                print("📋 最新デプロイメント:")
                for deploy in deployments[:3]:
                    status = "✅" if deploy.get('state') == 'READY' else "⏳"
                    print(f"  {status} {deploy.get('url')} - {deploy.get('state')}")
                return deployments
            else:
                print(f"❌ デプロイメント取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ エラー: {e}")
            return []

def main():
    """メイン実行関数"""
    print("🚀 Vercel API 管理システム")
    print("=" * 50)
    
    # API管理クラス初期化
    api = VercelAPIManager()
    
    # 接続テスト
    if not api.test_connection():
        return
    
    # プロジェクト情報表示
    api.get_project_info()
    
    # デプロイメント一覧表示
    api.list_deployments()
    
    print("\n📋 使用可能なコマンド:")
    print("  python vercel_api_setup.py deploy  # デプロイ実行")
    print("  python vercel_api_setup.py status  # ステータス確認")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        api = VercelAPIManager()
        
        if command == "deploy":
            print("🚀 デプロイ開始...")
            api.deploy_project()
        elif command == "status":
            api.test_connection()
            api.get_project_info()
            api.list_deployments()
    else:
        main()