#!/usr/bin/env python3
"""
統合Vercelデプロイメントシステム
全てのVercel関連機能を統合した単一エントリーポイント
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

class VercelDeploymentSystem:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "config" / "system_config.json"
        self.log_dir = self.project_root / "logs" / "deployment"
        self.ensure_directories()
        
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        (self.project_root / "config").mkdir(exist_ok=True)
        
    def deploy(self, mode="auto"):
        """
        Vercelにデプロイ
        mode: "auto", "manual", "api"
        """
        print("🚀 Vercel統合デプロイメントシステム")
        print("="*50)
        
        # デプロイ前チェック
        if not self.pre_deploy_check():
            print("❌ デプロイ前チェックに失敗しました")
            return False
            
        # デプロイ実行
        if mode == "auto":
            return self.auto_deploy()
        elif mode == "api":
            return self.api_deploy()
        else:
            return self.manual_deploy()
            
    def pre_deploy_check(self):
        """デプロイ前の環境チェック"""
        checks = {
            "index.html": os.path.exists("index.html") or os.path.exists("public/index.html"),
            "vercel.json": os.path.exists("vercel.json"),
            "git_status": self.check_git_status()
        }
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check}: {'OK' if result else 'NG'}")
            
        return all(checks.values())
        
    def check_git_status(self):
        """Gitの状態をチェック"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except:
            return False
            
    def auto_deploy(self):
        """自動デプロイ（Git push経由）"""
        print("\n📦 Git経由での自動デプロイを実行...")
        
        try:
            # Git add
            subprocess.run(["git", "add", "-A"], check=True)
            
            # Git commit
            commit_msg = f"Auto deploy - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            
            # Git push
            subprocess.run(["git", "push", "origin", "main"], check=True)
            
            print("✅ デプロイが開始されました")
            print("🌐 https://vercel.com でデプロイ状況を確認してください")
            
            self.log_deployment("auto", True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ エラー: {e}")
            self.log_deployment("auto", False, str(e))
            return False
            
    def api_deploy(self):
        """Vercel API経由でのデプロイ"""
        print("\n🔧 API経由でのデプロイを実行...")
        
        # 既存のdirect_vercel_deploy.pyの機能を統合
        from direct_vercel_deploy import deploy_to_vercel
        
        try:
            result = deploy_to_vercel()
            self.log_deployment("api", result)
            return result
        except Exception as e:
            print(f"❌ APIデプロイエラー: {e}")
            self.log_deployment("api", False, str(e))
            return False
            
    def manual_deploy(self):
        """手動デプロイガイド"""
        print("\n📋 手動デプロイ手順:")
        print("1. vercel コマンドを実行")
        print("2. プロンプトに従って設定")
        print("3. デプロイ完了を待つ")
        
        try:
            subprocess.run(["vercel"], check=True)
            self.log_deployment("manual", True)
            return True
        except:
            print("\n❌ vercel CLIがインストールされていません")
            print("npm install -g vercel でインストールしてください")
            self.log_deployment("manual", False, "CLI not found")
            return False
            
    def log_deployment(self, mode, success, error=None):
        """デプロイメントログを記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "success": success,
            "error": error
        }
        
        log_file = self.log_dir / f"deploy_{datetime.now().strftime('%Y%m%d')}.json"
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

def main():
    """メインエントリーポイント"""
    system = VercelDeploymentSystem()
    
    # コマンドライン引数でモードを指定
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    
    if mode not in ["auto", "api", "manual"]:
        print("使用方法: python vercel_deploy.py [auto|api|manual]")
        sys.exit(1)
        
    success = system.deploy(mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()