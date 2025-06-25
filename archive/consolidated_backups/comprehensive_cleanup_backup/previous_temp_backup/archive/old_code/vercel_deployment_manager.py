#!/usr/bin/env python3
"""
Vercelデプロイメント管理システム
成功パターンの記録、失敗時の修正、ロールバック機能
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess

class VercelDeploymentManager:
    def __init__(self):
        self.success_patterns_file = "VERCEL_SUCCESS_PATTERNS.json"
        self.deployment_backup_dir = ".vercel_backups"
        self.current_deployment_file = "CURRENT_DEPLOYMENT.json"
        
        # ディレクトリ作成
        os.makedirs(self.deployment_backup_dir, exist_ok=True)
        
        # 成功パターンを読み込み
        self.success_patterns = self._load_success_patterns()
        
    def _load_success_patterns(self) -> Dict:
        """成功パターンを読み込む"""
        if os.path.exists(self.success_patterns_file):
            with open(self.success_patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "patterns": [],
            "metadata": {
                "last_success": None,
                "total_successes": 0,
                "common_issues": []
            }
        }
    
    def _save_success_patterns(self):
        """成功パターンを保存"""
        with open(self.success_patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.success_patterns, f, ensure_ascii=False, indent=2)
    
    def backup_current_deployment(self) -> str:
        """現在のデプロイメントをバックアップ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.deployment_backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_path, exist_ok=True)
        
        # 重要ファイルをバックアップ
        files_to_backup = [
            "public/index.html",
            "index.html",
            "vercel.json",
            "package.json",
            ".env"
        ]
        
        backed_up_files = []
        for file in files_to_backup:
            if os.path.exists(file):
                dest = os.path.join(backup_path, file)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(file, dest)
                backed_up_files.append(file)
        
        # バックアップ情報を記録
        backup_info = {
            "timestamp": timestamp,
            "files": backed_up_files,
            "path": backup_path
        }
        
        with open(os.path.join(backup_path, "backup_info.json"), 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, ensure_ascii=False, indent=2)
        
        return backup_path
    
    def record_success_pattern(self, 
                             deployment_type: str,
                             files_changed: List[str],
                             config_used: Dict,
                             success_reason: str,
                             deploy_id: str,
                             url: str) -> Dict:
        """成功パターンを記録"""
        
        success_pattern = {
            "id": f"pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "deployment_type": deployment_type,
            "files_changed": files_changed,
            "config": config_used,
            "success_reason": success_reason,
            "deploy_id": deploy_id,
            "url": url,
            "reproduction_steps": self._generate_reproduction_steps(deployment_type, files_changed, config_used)
        }
        
        # パターンを追加
        self.success_patterns["patterns"].append(success_pattern)
        
        # メタデータ更新
        self.success_patterns["metadata"]["last_success"] = datetime.now().isoformat()
        self.success_patterns["metadata"]["total_successes"] += 1
        
        # 保存
        self._save_success_patterns()
        
        return success_pattern
    
    def _generate_reproduction_steps(self, deployment_type: str, files: List[str], config: Dict) -> List[str]:
        """再現手順を生成"""
        steps = []
        
        if deployment_type == "static_html":
            steps.append("1. 静的HTMLファイルを準備 (public/index.html)")
            steps.append("2. vercel.jsonを最小構成に設定")
            steps.append("3. python3 direct_vercel_deploy.py を実行")
        elif deployment_type == "api_function":
            steps.append("1. api/ディレクトリにPythonファイルを配置")
            steps.append("2. vercel.jsonでビルド設定を定義")
            steps.append("3. デプロイ実行")
        
        if files:
            steps.append(f"4. 変更ファイル: {', '.join(files)}")
        
        return steps
    
    def find_similar_success_pattern(self, current_config: Dict) -> Optional[Dict]:
        """類似の成功パターンを検索"""
        for pattern in self.success_patterns["patterns"]:
            if pattern["deployment_type"] == current_config.get("type"):
                return pattern
        return None
    
    def rollback_to_backup(self, backup_timestamp: str) -> bool:
        """指定のバックアップにロールバック"""
        backup_path = os.path.join(self.deployment_backup_dir, f"backup_{backup_timestamp}")
        
        if not os.path.exists(backup_path):
            print(f"❌ バックアップが見つかりません: {backup_timestamp}")
            return False
        
        # バックアップ情報を読み込み
        with open(os.path.join(backup_path, "backup_info.json"), 'r', encoding='utf-8') as f:
            backup_info = json.load(f)
        
        print(f"🔄 バックアップ {backup_timestamp} にロールバック中...")
        
        # ファイルを復元
        for file in backup_info["files"]:
            src = os.path.join(backup_path, file)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(file), exist_ok=True)
                shutil.copy2(src, file)
                print(f"✅ 復元: {file}")
        
        return True
    
    def analyze_deployment_issue(self, error_msg: str) -> Dict:
        """デプロイエラーを分析して解決策を提案"""
        solutions = {
            "suggestions": [],
            "similar_successes": [],
            "rollback_available": False
        }
        
        # エラーパターンマッチング
        if "BaseHTTPRequestHandler" in error_msg or "issubclass" in error_msg:
            solutions["suggestions"].append({
                "issue": "Python Runtime互換性エラー",
                "solution": "静的HTMLサイトに移行することを推奨",
                "steps": [
                    "rm -rf api/",
                    "mkdir -p public",
                    "mv index.html public/",
                    "echo '{\"version\": 2}' > vercel.json"
                ]
            })
        
        # 類似の成功パターンを検索
        for pattern in self.success_patterns["patterns"]:
            if pattern["deployment_type"] == "static_html":
                solutions["similar_successes"].append(pattern)
        
        # バックアップ確認
        backups = os.listdir(self.deployment_backup_dir)
        if backups:
            solutions["rollback_available"] = True
            solutions["latest_backup"] = sorted(backups)[-1].replace("backup_", "")
        
        return solutions
    
    def create_fix_script(self, issue_type: str) -> str:
        """問題修正用のスクリプトを生成"""
        script_name = f"fix_{issue_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        
        if issue_type == "python_runtime_error":
            script_content = '''#!/usr/bin/env python3
"""
Python Runtimeエラー修正スクリプト
静的HTMLサイトに自動変換
"""

import os
import shutil

def fix_python_runtime_error():
    print("🔧 Python Runtimeエラーを修正中...")
    
    # APIディレクトリを削除
    if os.path.exists("api"):
        shutil.rmtree("api")
        print("✅ api/ディレクトリを削除")
    
    # publicディレクトリを作成
    os.makedirs("public", exist_ok=True)
    
    # index.htmlを移動
    if os.path.exists("index.html") and not os.path.exists("public/index.html"):
        shutil.move("index.html", "public/index.html")
        print("✅ index.htmlをpublic/に移動")
    
    # vercel.jsonを簡素化
    with open("vercel.json", "w") as f:
        f.write('{\n  "version": 2\n}')
    print("✅ vercel.jsonを更新")
    
    print("🎉 修正完了！")
    print("📝 次のコマンドでデプロイしてください:")
    print("   python3 direct_vercel_deploy.py")

if __name__ == "__main__":
    fix_python_runtime_error()
'''
        
        with open(script_name, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        os.chmod(script_name, 0o755)
        return script_name
    
    def generate_deployment_report(self) -> str:
        """デプロイメントレポートを生成"""
        report = ["# Vercelデプロイメント分析レポート\n"]
        report.append(f"**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 成功パターン統計
        report.append("## 📊 成功パターン統計\n")
        report.append(f"- **総成功数**: {self.success_patterns['metadata']['total_successes']}")
        report.append(f"- **最終成功**: {self.success_patterns['metadata']['last_success']}")
        
        # 成功パターンリスト
        report.append("\n## ✅ 成功パターン一覧\n")
        for pattern in self.success_patterns["patterns"][-5:]:  # 最新5件
            report.append(f"### {pattern['id']}")
            report.append(f"- **タイプ**: {pattern['deployment_type']}")
            report.append(f"- **理由**: {pattern['success_reason']}")
            report.append(f"- **URL**: {pattern['url']}")
            report.append(f"- **再現手順**:")
            for step in pattern['reproduction_steps']:
                report.append(f"  {step}")
            report.append("")
        
        # バックアップ情報
        report.append("## 💾 利用可能なバックアップ\n")
        backups = sorted(os.listdir(self.deployment_backup_dir))
        for backup in backups[-5:]:  # 最新5件
            report.append(f"- {backup}")
        
        return "\n".join(report)

# 使用例とヘルパー関数
def deploy_with_safety(deployment_config: Dict) -> Tuple[bool, str]:
    """安全なデプロイメント実行"""
    manager = VercelDeploymentManager()
    
    # バックアップ作成
    backup_path = manager.backup_current_deployment()
    print(f"💾 バックアップ作成: {backup_path}")
    
    # デプロイ実行
    try:
        # ここで実際のデプロイを実行
        # success = deploy_to_vercel()
        success = True  # デモ用
        
        if success:
            # 成功パターンを記録
            pattern = manager.record_success_pattern(
                deployment_type=deployment_config.get("type", "static_html"),
                files_changed=deployment_config.get("files", []),
                config_used=deployment_config,
                success_reason=deployment_config.get("reason", "正常にデプロイ完了"),
                deploy_id=deployment_config.get("deploy_id", "unknown"),
                url=deployment_config.get("url", "https://study-research-final.vercel.app")
            )
            return True, f"成功パターン {pattern['id']} として記録されました"
        else:
            return False, "デプロイ失敗"
            
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    manager = VercelDeploymentManager()
    print(manager.generate_deployment_report())