#!/usr/bin/env python3
"""
Vercel完全デプロイシステム - ワンコマンドで完全デプロイ
"""

import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class VercelCompleteDeployment:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "VERCEL_COMPLETE_CONFIG.json"
        self.history_file = self.project_root / "VERCEL_DEPLOYMENT_HISTORY.json"
        self.env_file = self.project_root / ".env"
        self.vercel_token = self.get_vercel_token()
        self.config = self.load_config()
        
    def get_vercel_token(self) -> Optional[str]:
        """Vercelトークンを取得"""
        # 環境変数から取得
        token = os.getenv('VERCEL_TOKEN')
        if token:
            return token
            
        # .envファイルから取得
        if self.env_file.exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if line.startswith('VERCEL_TOKEN='):
                            return line.split('=', 1)[1].strip()
            except:
                pass
                
        # デフォルトトークン（既存設定から）
        return "WkO3OyNzgZDXHpRwRgA5GDnL"
    
    def load_config(self) -> Dict:
        """設定を読み込み"""
        default_config = {
            "project_name": "study-research-final",
            "project_id": "prj_yt8CeSOyuRcskyogkyA9KTfV6L1C",
            "auto_git_commit": True,
            "auto_git_push": True,
            "auto_cleanup": True,
            "build_settings": {
                "build_command": None,
                "output_directory": "public",
                "install_command": None
            },
            "deployment_settings": {
                "target": "production",
                "alias": ["study-research-final.vercel.app"],
                "env_vars": {}
            },
            "monitoring": {
                "check_status": True,
                "timeout_seconds": 300,
                "retry_attempts": 3
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
            except:
                pass
                
        return default_config
    
    def save_config(self):
        """設定を保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def log_deployment(self, deployment_data: Dict):
        """デプロイメント履歴を記録"""
        history = []
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                pass
        
        history.append({
            **deployment_data,
            "timestamp": datetime.now().isoformat(),
            "config_snapshot": self.config.copy()
        })
        
        # 最新50件のみ保持
        history = history[-50:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def check_prerequisites(self) -> Dict[str, bool]:
        """前提条件をチェック"""
        checks = {}
        
        # Vercelトークンの確認
        checks['vercel_token'] = bool(self.vercel_token)
        
        # プロジェクトファイルの確認
        checks['vercel_json'] = (self.project_root / "vercel.json").exists()
        checks['index_html'] = (self.project_root / "public" / "index.html").exists()
        
        # Gitリポジトリの確認
        checks['git_repo'] = (self.project_root / ".git").exists()
        
        # インターネット接続の確認
        try:
            response = requests.get("https://api.vercel.com/v2/user", 
                                  headers={"Authorization": f"Bearer {self.vercel_token}"},
                                  timeout=10)
            checks['vercel_api'] = response.status_code == 200
        except:
            checks['vercel_api'] = False
        
        return checks
    
    def auto_fix_issues(self, checks: Dict[str, bool]) -> Dict[str, bool]:
        """問題を自動修正"""
        print("🔧 問題を自動修正中...")
        
        # vercel.jsonが存在しない場合は作成
        if not checks['vercel_json']:
            vercel_json_path = self.project_root / "vercel.json"
            with open(vercel_json_path, 'w') as f:
                json.dump({"version": 2}, f, indent=2)
            print("✅ vercel.json を作成しました")
            checks['vercel_json'] = True
        
        # public/index.htmlが存在しない場合は確認
        if not checks['index_html']:
            # 他の場所にindex.htmlがあるかチェック
            root_index = self.project_root / "index.html"
            if root_index.exists():
                # publicディレクトリを作成してファイルを移動
                public_dir = self.project_root / "public"
                public_dir.mkdir(exist_ok=True)
                import shutil
                shutil.copy2(root_index, public_dir / "index.html")
                print("✅ index.html を public/ に移動しました")
                checks['index_html'] = True
        
        return checks
    
    def git_operations(self) -> bool:
        """Git操作を実行"""
        if not self.config['auto_git_commit']:
            return True
            
        try:
            print("📝 Git操作を実行中...")
            
            # git add
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            
            # git commit
            commit_message = f"🚀 Complete Vercel deployment - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         check=True, capture_output=True)
            
            # git push（設定されている場合）
            if self.config['auto_git_push']:
                subprocess.run(['git', 'push'], check=True, capture_output=True)
                print("✅ Git push完了")
            
            print("✅ Git操作完了")
            return True
            
        except subprocess.CalledProcessError as e:
            # コミットするものがない場合は正常とみなす
            if "nothing to commit" in str(e.stderr):
                print("📝 変更なし - Git操作スキップ")
                return True
            print(f"⚠️ Git操作でエラー: {e}")
            return False
    
    def deploy_to_vercel(self) -> Dict:
        """Vercelにデプロイ"""
        print("🚀 Vercelデプロイを開始...")
        
        # デプロイメント作成
        deploy_data = {
            "name": self.config['project_name'],
            "target": self.config['deployment_settings']['target'],
            "projectSettings": {
                "buildCommand": self.config['build_settings']['build_command'],
                "outputDirectory": self.config['build_settings']['output_directory'],
                "installCommand": self.config['build_settings']['install_command']
            }
        }
        
        # ファイルをアップロード
        files = []
        
        # public/index.htmlを含める
        index_path = self.project_root / "public" / "index.html"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                files.append({
                    "file": "index.html",
                    "data": f.read()
                })
        
        # vercel.jsonを含める
        vercel_json_path = self.project_root / "vercel.json"
        if vercel_json_path.exists():
            with open(vercel_json_path, 'r', encoding='utf-8') as f:
                files.append({
                    "file": "vercel.json",
                    "data": f.read()
                })
        
        deploy_data["files"] = files
        
        # API呼び出し
        headers = {
            "Authorization": f"Bearer {self.vercel_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"https://api.vercel.com/v13/deployments",
                json=deploy_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ デプロイメント作成成功")
                print(f"🆔 デプロイID: {result.get('id', 'N/A')}")
                print(f"🌐 URL: {result.get('url', 'N/A')}")
                return result
            else:
                print(f"❌ デプロイメント失敗: {response.status_code}")
                print(f"エラー: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"❌ デプロイメントエラー: {e}")
            return {"error": str(e)}
    
    def monitor_deployment(self, deployment_id: str) -> bool:
        """デプロイメント状況を監視"""
        print("📊 デプロイメント状況を監視中...")
        
        headers = {"Authorization": f"Bearer {self.vercel_token}"}
        timeout = self.config['monitoring']['timeout_seconds']
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    f"https://api.vercel.com/v13/deployments/{deployment_id}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    state = data.get('readyState', 'UNKNOWN')
                    
                    if state == 'READY':
                        print("✅ デプロイメント完了!")
                        return True
                    elif state == 'ERROR':
                        print("❌ デプロイメントエラー")
                        return False
                    else:
                        print(f"⏳ 状態: {state}")
                        time.sleep(5)
                else:
                    print(f"⚠️ 状態確認エラー: {response.status_code}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"⚠️ 監視エラー: {e}")
                time.sleep(5)
        
        print("⏰ タイムアウト - 状態確認を終了")
        return False
    
    def cleanup(self):
        """デプロイ後のクリーンアップ"""
        if not self.config['auto_cleanup']:
            return
            
        print("🧹 クリーンアップ中...")
        
        # 一時ファイルの削除
        temp_files = [
            self.project_root / "deployment.log",
            self.project_root / ".vercel_temp"
        ]
        
        for temp_file in temp_files:
            if temp_file.exists():
                temp_file.unlink()
        
        print("✅ クリーンアップ完了")
    
    def run_complete_deployment(self) -> bool:
        """完全デプロイメントを実行"""
        print("=" * 60)
        print("🚀 Vercel完全デプロイメントシステム")
        print("=" * 60)
        
        # 1. 前提条件チェック
        print("\n📋 Step 1: 前提条件チェック")
        checks = self.check_prerequisites()
        
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check_name}: {result}")
        
        # 2. 問題の自動修正
        if not all(checks.values()):
            print("\n🔧 Step 2: 問題の自動修正")
            checks = self.auto_fix_issues(checks)
        
        # 3. Git操作
        print("\n📝 Step 3: Git操作")
        git_success = self.git_operations()
        
        # 4. Vercelデプロイ
        print("\n🚀 Step 4: Vercelデプロイ")
        deployment_result = self.deploy_to_vercel()
        
        if "error" in deployment_result:
            print("❌ デプロイメント失敗")
            self.log_deployment({
                "status": "failed",
                "error": deployment_result["error"],
                "checks": checks,
                "git_success": git_success
            })
            return False
        
        # 5. デプロイメント監視
        deployment_id = deployment_result.get('id')
        if deployment_id and self.config['monitoring']['check_status']:
            print("\n📊 Step 5: デプロイメント監視")
            deploy_success = self.monitor_deployment(deployment_id)
        else:
            deploy_success = True
        
        # 6. クリーンアップ
        print("\n🧹 Step 6: クリーンアップ")
        self.cleanup()
        
        # 7. 結果記録
        self.log_deployment({
            "status": "success" if deploy_success else "failed",
            "deployment_id": deployment_id,
            "url": deployment_result.get('url'),
            "checks": checks,
            "git_success": git_success,
            "deploy_success": deploy_success
        })
        
        print("\n" + "=" * 60)
        if deploy_success:
            print("🎉 完全デプロイメント成功!")
            print(f"🌐 URL: https://{deployment_result.get('url', 'N/A')}")
            if 'study-research-final.vercel.app' not in str(deployment_result.get('url', '')):
                print(f"🌐 本番URL: https://study-research-final.vercel.app")
        else:
            print("❌ デプロイメント失敗")
        print("=" * 60)
        
        return deploy_success

def main():
    """メイン関数"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        deployer = VercelCompleteDeployment()
        
        if command == "deploy":
            deployer.run_complete_deployment()
        elif command == "config":
            print(json.dumps(deployer.config, indent=2, ensure_ascii=False))
        elif command == "history":
            if deployer.history_file.exists():
                with open(deployer.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    for entry in history[-5:]:  # 最新5件表示
                        print(f"📅 {entry['timestamp']}: {entry['status']}")
        elif command == "setup":
            print("🔧 セットアップ中...")
            deployer.save_config()
            print("✅ セットアップ完了")
        else:
            print("使用方法:")
            print("  python3 vercel_complete_deploy.py deploy   - 完全デプロイ実行")
            print("  python3 vercel_complete_deploy.py config   - 設定表示")
            print("  python3 vercel_complete_deploy.py history  - 履歴表示")
            print("  python3 vercel_complete_deploy.py setup    - 初期セットアップ")
    else:
        # 引数なしの場合はデプロイ実行
        deployer = VercelCompleteDeployment()
        deployer.run_complete_deployment()

if __name__ == "__main__":
    main()