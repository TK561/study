#!/usr/bin/env python3
"""
Vercel自動デプロイシステム
独立したVercelデプロイ自動化システム
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import json

class VercelAutoDeploySystem:
    def __init__(self):
        self.name = "Vercel自動デプロイシステム"
        self.version = "1.0.0"
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 実行ログ
        self.execution_log = {
            "timestamp": datetime.now().isoformat(),
            "actions_performed": [],
            "git_operations": [],
            "vercel_operations": [],
            "errors": []
        }
        
    def detect_project_directory(self):
        """Vercelプロジェクトディレクトリの自動検出"""
        print("🔍 Vercelプロジェクトディレクトリを検出中...")
        
        # 検索対象ディレクトリの優先順位
        candidate_dirs = [
            self.root_path / "discussion-site",
            self.root_path / "vercel-project",
            self.root_path / "public",
            self.root_path,
            self.root_path / "web" / "public"
        ]
        
        for dir_path in candidate_dirs:
            if dir_path.exists():
                # vercel.jsonまたはindex.htmlの存在確認
                if (dir_path / "vercel.json").exists() or (dir_path / "index.html").exists():
                    print(f"  ✅ プロジェクトディレクトリ検出: {dir_path.relative_to(self.root_path)}")
                    return dir_path
        
        print("  ⚠️ Vercelプロジェクトディレクトリが見つかりません")
        return None
    
    def execute_git_operations(self):
        """Git操作の実行"""
        print("📤 Git操作実行中...")
        
        try:
            # git add .
            add_result = subprocess.run(
                ['git', 'add', '.'], 
                cwd=str(self.root_path), 
                capture_output=True, 
                text=True
            )
            
            if add_result.returncode == 0:
                print("  ✅ git add 完了")
                self.execution_log["git_operations"].append("git add successful")
            else:
                print(f"  ⚠️ git add エラー: {add_result.stderr}")
                self.execution_log["errors"].append(f"git add error: {add_result.stderr}")
            
            # git commit
            commit_msg = f"🚀 Vercel自動デプロイ - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_msg], 
                cwd=str(self.root_path),
                capture_output=True, 
                text=True
            )
            
            if commit_result.returncode == 0:
                print("  ✅ git commit 完了")
                self.execution_log["git_operations"].append("git commit successful")
            else:
                print(f"  ⚠️ git commit: {commit_result.stderr}")
                # コミットするものがない場合は警告レベル
                if "nothing to commit" in commit_result.stdout:
                    print("    📋 変更なし - コミットスキップ")
                    self.execution_log["git_operations"].append("no changes to commit")
                else:
                    self.execution_log["errors"].append(f"git commit error: {commit_result.stderr}")
            
            # git push
            push_result = subprocess.run(
                ['git', 'push'], 
                cwd=str(self.root_path),
                capture_output=True, 
                text=True,
                timeout=60
            )
            
            if push_result.returncode == 0:
                print("  ✅ git push 完了")
                self.execution_log["git_operations"].append("git push successful")
                return True
            else:
                print(f"  ⚠️ git push エラー: {push_result.stderr}")
                self.execution_log["errors"].append(f"git push error: {push_result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("  ⚠️ git push タイムアウト")
            self.execution_log["errors"].append("git push timeout")
            return False
        except Exception as e:
            print(f"  ❌ Git操作エラー: {e}")
            self.execution_log["errors"].append(f"git operations error: {e}")
            return False
    
    def execute_vercel_deploy(self, project_dir):
        """Vercelデプロイの実行"""
        print("🚀 Vercelデプロイ実行中...")
        
        try:
            # vercel --prod --yes の実行
            deploy_result = subprocess.run(
                ['vercel', '--prod', '--yes'], 
                cwd=str(project_dir),
                capture_output=True, 
                text=True,
                timeout=120
            )
            
            if deploy_result.returncode == 0:
                print("  ✅ Vercelデプロイ完了")
                self.execution_log["vercel_operations"].append("vercel deploy successful")
                
                # デプロイURLの抽出（オプション）
                output_lines = deploy_result.stdout.splitlines()
                for line in output_lines:
                    if "https://" in line and "vercel.app" in line:
                        print(f"  🌐 デプロイURL: {line.strip()}")
                        self.execution_log["vercel_operations"].append(f"deploy URL: {line.strip()}")
                        break
                
                return True
            else:
                print(f"  ❌ Vercelデプロイエラー: {deploy_result.stderr}")
                self.execution_log["errors"].append(f"vercel deploy error: {deploy_result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("  ⚠️ Vercelデプロイタイムアウト（2分）")
            self.execution_log["errors"].append("vercel deploy timeout")
            return False
        except FileNotFoundError:
            print("  ❌ vercel コマンドが見つかりません")
            print("    💡 Vercel CLIをインストールしてください: npm i -g vercel")
            self.execution_log["errors"].append("vercel command not found")
            return False
        except Exception as e:
            print(f"  ❌ Vercelデプロイエラー: {e}")
            self.execution_log["errors"].append(f"vercel deploy error: {e}")
            return False
    
    def execute_auto_deploy(self):
        """自動デプロイの実行"""
        print("🚀 Vercel自動デプロイシステム 起動")
        print("=" * 60)
        
        # プロジェクトディレクトリの検出
        project_dir = self.detect_project_directory()
        if not project_dir:
            print("❌ プロジェクトディレクトリが見つからないため、デプロイを中止します")
            return False
        
        # Git操作の実行
        print("\\n📍 ステップ1: Git操作")
        git_success = self.execute_git_operations()
        
        # Vercelデプロイの実行
        print("\\n📍 ステップ2: Vercelデプロイ")
        if git_success:
            deploy_success = self.execute_vercel_deploy(project_dir)
        else:
            print("  ⚠️ Git操作が失敗したため、Vercelデプロイをスキップします")
            deploy_success = False
        
        # 実行ログの保存
        log_file = self.root_path / f"vercel_deploy_log_{self.timestamp}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.execution_log, f, ensure_ascii=False, indent=2)
        
        # 完了サマリー
        print("\\n" + "=" * 60)
        if git_success and deploy_success:
            print("🎉 Vercel自動デプロイ完了")
            print("✅ Git push とVercelデプロイの両方が成功しました")
        elif git_success:
            print("⚠️ Git操作は成功、Vercelデプロイに問題があります")
        else:
            print("❌ Git操作でエラーが発生しました")
        
        print("=" * 60)
        print("📊 実行サマリー:")
        print(f"  📤 Git操作: {len(self.execution_log['git_operations'])}件")
        print(f"  🚀 Vercel操作: {len(self.execution_log['vercel_operations'])}件")
        print(f"  ⚠️ エラー: {len(self.execution_log['errors'])}件")
        print(f"\\n📄 詳細ログ: {log_file.name}")
        
        return git_success and deploy_success

def main():
    """メイン実行関数"""
    deployer = VercelAutoDeploySystem()
    
    # コマンドライン引数の確認
    if len(sys.argv) > 1 and sys.argv[1] in ["deploy", "デプロイ", "vercel"]:
        print("📋 Vercelデプロイが要求されました")
    
    success = deployer.execute_auto_deploy()
    
    if success:
        print("\\n✅ 次回は「vercelに反映」で自動デプロイが実行されます")
    else:
        print("\\n⚠️ エラーが発生しました。ログを確認してください")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())