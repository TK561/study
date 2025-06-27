#!/usr/bin/env python3
"""
Google Colab → Vercel 完全自動デプロイスクリプト
ワンクリックでColab環境からVercelへデプロイ
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from google_drive_utils import get_base_path, safe_save, timer

class ColabToVercelDeployer:
    def __init__(self):
        self.base_path = get_base_path()
        self.public_dir = self.base_path / 'public'
        self.deploy_url = "https://study-research-final.vercel.app"
        
    def check_colab_environment(self):
        """Colab環境確認"""
        try:
            import google.colab
            print("✅ Google Colab環境を検出")
            return True
        except ImportError:
            print("⚠️ Colab環境外で実行中")
            return False
    
    def install_vercel_cli(self):
        """Vercel CLI のインストール"""
        print("📦 Vercel CLI インストール中...")
        
        try:
            # Node.js/npm のインストール確認
            node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if node_result.returncode != 0:
                print("📥 Node.js インストール中...")
                os.system('curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -')
                os.system('sudo apt-get install -y nodejs')
            
            # Vercel CLI インストール
            npm_result = subprocess.run(['npm', 'install', '-g', 'vercel'], capture_output=True, text=True)
            
            if npm_result.returncode == 0:
                print("✅ Vercel CLI インストール完了")
                return True
            else:
                print(f"❌ Vercel CLI インストール失敗: {npm_result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ インストールエラー: {e}")
            return False
    
    def setup_vercel_auth(self):
        """Vercel認証セットアップ（手動認証ガイド）"""
        print("🔐 Vercel認証設定")
        print("=" * 50)
        print("以下の手順で認証してください：")
        print("1. 下記のコマンドをコピーして新しいセルで実行")
        print("!vercel login")
        print("2. 表示されるURLにアクセス")
        print("3. Vercelアカウントでログイン")
        print("4. 認証完了後、次の手順に進む")
        print("=" * 50)
        
        # 認証状態チェック用のスクリプト
        auth_check_script = '''
# Vercel認証確認スクリプト
import subprocess

def check_vercel_auth():
    try:
        result = subprocess.run(['vercel', 'whoami'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 認証済み: {result.stdout.strip()}")
            return True
        else:
            print("❌ 認証が必要です")
            return False
    except:
        print("❌ Vercel CLI が見つかりません")
        return False

# 実行
check_vercel_auth()
'''
        
        auth_script_path = self.base_path / 'check_vercel_auth.py'
        safe_save(auth_check_script, auth_script_path)
        
        print(f"📝 認証確認スクリプト作成: {auth_script_path}")
        return auth_script_path
    
    def prepare_deployment(self):
        """デプロイ前準備"""
        print("🔧 デプロイ前準備中...")
        
        # 1. publicディレクトリ確認
        if not self.public_dir.exists():
            print("❌ publicディレクトリが見つかりません")
            return False
        
        # 2. 必須ファイル確認
        required_files = [
            'index.html',
            'main-system/index.html',
            'confidence_feedback/index.html',
            'pptx_systems/index.html'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.public_dir / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ 必須ファイル不足: {missing_files}")
            return False
        
        # 3. vercel.json確認
        vercel_config_path = self.base_path / 'vercel.json'
        if vercel_config_path.exists():
            print("✅ vercel.json 設定済み")
        else:
            print("📝 vercel.json 作成中...")
            self.create_vercel_config()
        
        # 4. バックアップ作成
        self.create_backup()
        
        print("✅ デプロイ前準備完了")
        return True
    
    def create_vercel_config(self):
        """Vercel設定ファイル作成"""
        vercel_config = {
            "version": 2,
            "buildCommand": "echo 'Building static site'",
            "outputDirectory": "public",
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "/public/$1"
                }
            ],
            "rewrites": [
                {
                    "source": "/",
                    "destination": "/public/index.html"
                },
                {
                    "source": "/main-system",
                    "destination": "/public/main-system/index.html"
                },
                {
                    "source": "/confidence_feedback",
                    "destination": "/public/confidence_feedback/index.html"
                },
                {
                    "source": "/pptx_systems",
                    "destination": "/public/pptx_systems/index.html"
                },
                {
                    "source": "/enhanced_features",
                    "destination": "/public/enhanced_features/index.html"
                }
            ],
            "headers": [
                {
                    "source": "/(.*)",
                    "headers": [
                        {
                            "key": "Cache-Control",
                            "value": "public, max-age=3600"
                        }
                    ]
                }
            ]
        }
        
        vercel_path = self.base_path / 'vercel.json'
        safe_save(json.dumps(vercel_config, indent=2), vercel_path)
        print(f"✅ vercel.json 作成完了: {vercel_path}")
    
    def create_backup(self):
        """デプロイ前バックアップ"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.base_path / 'backups' / f'pre_deploy_{timestamp}'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        import shutil
        shutil.copytree(self.public_dir, backup_dir / 'public')
        
        backup_info = {
            'timestamp': datetime.now().isoformat(),
            'backup_location': str(backup_dir),
            'files_count': len(list(self.public_dir.rglob('*')))
        }
        
        safe_save(json.dumps(backup_info, indent=2), backup_dir / 'backup_info.json')
        print(f"💾 バックアップ作成: {backup_dir}")
        
        return backup_dir
    
    def deploy_to_vercel(self):
        """Vercelデプロイ実行"""
        print("🚀 Vercelデプロイ開始...")
        
        # 作業ディレクトリ変更
        os.chdir(self.base_path)
        
        try:
            # プロダクションデプロイ実行
            deploy_command = ['vercel', '--prod', '--yes']
            result = subprocess.run(deploy_command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Vercelデプロイ成功！")
                print(f"🌐 URL: {self.deploy_url}")
                
                # デプロイログ保存
                deploy_log = {
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success',
                    'command': ' '.join(deploy_command),
                    'output': result.stdout,
                    'url': self.deploy_url
                }
                
                log_file = self.base_path / 'logs' / f'deploy_success_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                log_file.parent.mkdir(exist_ok=True)
                safe_save(json.dumps(deploy_log, indent=2), log_file)
                
                return True
            else:
                print("❌ デプロイ失敗")
                print(f"エラー: {result.stderr}")
                
                # エラーログ保存
                error_log = {
                    'timestamp': datetime.now().isoformat(),
                    'status': 'failed',
                    'command': ' '.join(deploy_command),
                    'error': result.stderr,
                    'stdout': result.stdout
                }
                
                error_file = self.base_path / 'logs' / f'deploy_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                error_file.parent.mkdir(exist_ok=True)
                safe_save(json.dumps(error_log, indent=2), error_file)
                
                return False
                
        except Exception as e:
            print(f"❌ デプロイ実行エラー: {e}")
            return False
    
    def verify_deployment(self):
        """デプロイ結果確認"""
        print("🔍 デプロイ結果確認中...")
        
        import requests
        
        urls_to_check = [
            f"{self.deploy_url}/",
            f"{self.deploy_url}/main-system/",
            f"{self.deploy_url}/confidence_feedback/",
            f"{self.deploy_url}/pptx_systems/"
        ]
        
        results = {}
        
        for url in urls_to_check:
            try:
                response = requests.get(url, timeout=10)
                results[url] = {
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'success': response.status_code == 200
                }
                
                if response.status_code == 200:
                    print(f"✅ {url} - OK ({response.elapsed.total_seconds():.2f}s)")
                else:
                    print(f"❌ {url} - Error {response.status_code}")
                    
            except Exception as e:
                results[url] = {'error': str(e), 'success': False}
                print(f"❌ {url} - Error: {e}")
        
        # 確認結果保存
        verification_log = {
            'timestamp': datetime.now().isoformat(),
            'verification_results': results,
            'overall_success': all(r.get('success', False) for r in results.values())
        }
        
        verification_file = self.base_path / 'logs' / f'deployment_verification_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        verification_file.parent.mkdir(exist_ok=True)
        safe_save(json.dumps(verification_log, indent=2), verification_file)
        
        if verification_log['overall_success']:
            print("✅ 全URLで正常動作確認")
        else:
            print("⚠️ 一部URLでエラーが発生")
        
        return verification_log['overall_success']
    
    def create_deploy_script(self):
        """ワンクリックデプロイスクリプト作成"""
        deploy_script = '''
# === Google Colab → Vercel ワンクリックデプロイ ===

from vercel_deploy_from_colab import ColabToVercelDeployer

def quick_deploy():
    """クイックデプロイ実行"""
    deployer = ColabToVercelDeployer()
    
    print("🚀 Google Colab → Vercel デプロイ開始")
    print("=" * 50)
    
    # 1. 環境確認
    if not deployer.check_colab_environment():
        print("⚠️ Colab環境外での実行")
    
    # 2. デプロイ前準備
    if not deployer.prepare_deployment():
        print("❌ デプロイ前準備失敗")
        return False
    
    # 3. デプロイ実行
    if not deployer.deploy_to_vercel():
        print("❌ デプロイ失敗")
        return False
    
    # 4. 結果確認
    if deployer.verify_deployment():
        print("✅ デプロイ完全成功！")
        print(f"🌐 サイトURL: {deployer.deploy_url}")
        return True
    else:
        print("⚠️ デプロイは成功したが、一部URLでエラー")
        return False

# 実行
quick_deploy()
'''
        
        script_path = self.base_path / 'quick_deploy.py'
        safe_save(deploy_script, script_path)
        
        print(f"📝 ワンクリックデプロイスクリプト作成: {script_path}")
        return script_path
    
    def run_complete_setup(self):
        """完全セットアップ実行"""
        print("🌐 Google Colab → Vercel 完全セットアップ")
        print("=" * 60)
        
        # 1. 環境確認
        self.check_colab_environment()
        
        # 2. Vercel CLI インストール
        if not self.install_vercel_cli():
            print("❌ Vercel CLI セットアップ失敗")
            return False
        
        # 3. 認証設定ガイド
        auth_script = self.setup_vercel_auth()
        
        # 4. デプロイ準備
        if not self.prepare_deployment():
            print("❌ デプロイ準備失敗")
            return False
        
        # 5. クイックデプロイスクリプト作成
        deploy_script = self.create_deploy_script()
        
        print("=" * 60)
        print("✅ セットアップ完了！")
        print("\n📋 次の手順:")
        print("1. 認証確認:")
        print("   exec(open('check_vercel_auth.py').read())")
        print("2. 認証が済んでいない場合:")
        print("   !vercel login")
        print("3. デプロイ実行:")
        print("   exec(open('quick_deploy.py').read())")
        print(f"\n🌐 デプロイ先URL: {self.deploy_url}")
        
        return True

def main():
    """メイン実行関数"""
    deployer = ColabToVercelDeployer()
    return deployer.run_complete_setup()

if __name__ == "__main__":
    main()