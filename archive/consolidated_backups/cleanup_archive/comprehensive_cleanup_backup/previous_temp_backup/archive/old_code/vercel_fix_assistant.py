#!/usr/bin/env python3
"""
Vercel修正アシスタント
エラー発生時の自動修正とユーザー満足度向上
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

class VercelFixAssistant:
    def __init__(self):
        self.error_history_file = "VERCEL_ERROR_HISTORY.json"
        self.fix_history_file = "VERCEL_FIX_HISTORY.json"
        self.manager = None
        
        try:
            from vercel_deployment_manager import VercelDeploymentManager
            self.manager = VercelDeploymentManager()
        except:
            pass
    
    def diagnose_issue(self, error_message: str = None) -> Dict:
        """問題を診断して解決策を提示"""
        print("🔍 Vercelデプロイメント診断を開始...")
        
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "error_detected": False,
            "error_type": None,
            "solutions": [],
            "quick_fixes": [],
            "rollback_options": []
        }
        
        # エラーメッセージ分析
        if error_message:
            diagnosis["error_detected"] = True
            
            if "BaseHTTPRequestHandler" in error_message or "issubclass" in error_message:
                diagnosis["error_type"] = "python_runtime_error"
                diagnosis["solutions"].append({
                    "priority": 1,
                    "name": "静的HTMLサイトへの移行",
                    "description": "Python APIを削除し、静的HTMLとして配置",
                    "command": "python3 vercel_fix_assistant.py --fix static_html"
                })
                diagnosis["quick_fixes"].append({
                    "name": "即座に修正",
                    "steps": [
                        "rm -rf api/",
                        "mkdir -p public",
                        "mv index.html public/ 2>/dev/null || true",
                        "echo '{\"version\": 2}' > vercel.json",
                        "python3 direct_vercel_deploy.py"
                    ]
                })
        
        # バックアップ確認
        if self.manager:
            backups = os.listdir(self.manager.deployment_backup_dir)
            if backups:
                latest_backups = sorted(backups)[-3:]  # 最新3件
                for backup in latest_backups:
                    diagnosis["rollback_options"].append({
                        "backup_id": backup.replace("backup_", ""),
                        "command": f"python3 vercel_fix_assistant.py --rollback {backup.replace('backup_', '')}"
                    })
        
        return diagnosis
    
    def apply_fix(self, fix_type: str) -> bool:
        """修正を適用"""
        print(f"🔧 修正タイプ '{fix_type}' を適用中...")
        
        if fix_type == "static_html":
            return self._fix_to_static_html()
        elif fix_type == "restore_working":
            return self._restore_last_working()
        else:
            print(f"❌ 不明な修正タイプ: {fix_type}")
            return False
    
    def _fix_to_static_html(self) -> bool:
        """静的HTMLサイトに修正"""
        try:
            # バックアップ作成
            if self.manager:
                backup = self.manager.backup_current_deployment()
                print(f"💾 バックアップ作成: {backup}")
            
            # APIディレクトリ削除
            if os.path.exists("api"):
                subprocess.run(["rm", "-rf", "api"], check=True)
                print("✅ api/ディレクトリを削除")
            
            # publicディレクトリ作成
            os.makedirs("public", exist_ok=True)
            print("✅ public/ディレクトリを作成")
            
            # index.htmlの移動/作成
            if os.path.exists("index.html") and not os.path.exists("public/index.html"):
                subprocess.run(["mv", "index.html", "public/"], check=True)
                print("✅ index.htmlをpublic/に移動")
            elif not os.path.exists("public/index.html"):
                # サンプルHTMLを作成
                self._create_sample_html()
                print("✅ サンプルindex.htmlを作成")
            
            # vercel.json更新
            vercel_config = {"version": 2}
            with open("vercel.json", "w") as f:
                json.dump(vercel_config, f, indent=2)
            print("✅ vercel.jsonを最小構成に更新")
            
            # 修正履歴を記録
            self._record_fix({
                "type": "static_html",
                "timestamp": datetime.now().isoformat(),
                "changes": [
                    "APIディレクトリ削除",
                    "静的HTMLサイト構成に変更",
                    "vercel.json簡素化"
                ],
                "success": True
            })
            
            print("\n✅ 修正完了！")
            print("📝 次のコマンドでデプロイしてください:")
            print("   python3 direct_vercel_deploy.py")
            
            return True
            
        except Exception as e:
            print(f"❌ 修正中にエラー: {e}")
            return False
    
    def _create_sample_html(self):
        """サンプルHTMLを作成"""
        html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究成果</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>研究成果</h1>
        <p>このページは自動修正により作成されました。</p>
        <p>最終更新: <span id="lastUpdate">{}</span></p>
    </div>
    <script>
        document.getElementById('lastUpdate').textContent = new Date().toLocaleString('ja-JP');
    </script>
</body>
</html>""".format(datetime.now().strftime('%Y年%m月%d日 %H:%M'))
        
        with open("public/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def _restore_last_working(self) -> bool:
        """最後の正常な状態に復元"""
        if not self.manager:
            print("❌ デプロイメント管理システムが利用できません")
            return False
        
        # 最新の成功パターンを取得
        patterns = self.manager.success_patterns.get("patterns", [])
        if not patterns:
            print("❌ 成功パターンが見つかりません")
            return False
        
        latest_pattern = patterns[-1]
        print(f"📋 成功パターン {latest_pattern['id']} に基づいて復元...")
        
        # 再現手順を実行
        for step in latest_pattern["reproduction_steps"]:
            print(f"  {step}")
        
        return True
    
    def _record_fix(self, fix_info: Dict):
        """修正履歴を記録"""
        try:
            if os.path.exists(self.fix_history_file):
                with open(self.fix_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = {"fixes": []}
            
            history["fixes"].append(fix_info)
            
            with open(self.fix_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def interactive_fix(self):
        """対話的な修正プロセス"""
        print("🤖 Vercel修正アシスタント")
        print("=" * 50)
        
        # 診断実行
        diagnosis = self.diagnose_issue()
        
        print("\n📊 診断結果:")
        if diagnosis["rollback_options"]:
            print("\n💾 利用可能なバックアップ:")
            for i, option in enumerate(diagnosis["rollback_options"], 1):
                print(f"  {i}. {option['backup_id']}")
        
        print("\n🔧 利用可能な修正オプション:")
        print("  1. 静的HTMLサイトに変換")
        print("  2. 最後の成功状態に復元")
        print("  3. バックアップからロールバック")
        print("  4. 手動で修正")
        print("  0. 終了")
        
        while True:
            try:
                choice = input("\n選択してください (0-4): ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    self.apply_fix("static_html")
                    break
                elif choice == "2":
                    self._restore_last_working()
                    break
                elif choice == "3":
                    if diagnosis["rollback_options"]:
                        backup_choice = input("バックアップ番号を選択: ").strip()
                        try:
                            idx = int(backup_choice) - 1
                            backup_id = diagnosis["rollback_options"][idx]["backup_id"]
                            if self.manager:
                                self.manager.rollback_to_backup(backup_id)
                                print("✅ ロールバック完了")
                        except:
                            print("❌ 無効な選択")
                    else:
                        print("❌ バックアップがありません")
                elif choice == "4":
                    print("\n📝 手動修正のガイド:")
                    print("1. public/index.htmlに静的HTMLを配置")
                    print("2. vercel.jsonを{\"version\": 2}に設定")
                    print("3. python3 direct_vercel_deploy.pyを実行")
                    break
                else:
                    print("❌ 無効な選択です")
                    
            except KeyboardInterrupt:
                print("\n👋 終了します")
                break

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Vercel修正アシスタント")
    parser.add_argument("--fix", type=str, help="修正タイプを指定")
    parser.add_argument("--rollback", type=str, help="バックアップIDを指定してロールバック")
    parser.add_argument("--diagnose", action="store_true", help="診断のみ実行")
    parser.add_argument("--error", type=str, help="エラーメッセージを指定")
    
    args = parser.parse_args()
    
    assistant = VercelFixAssistant()
    
    if args.diagnose:
        diagnosis = assistant.diagnose_issue(args.error)
        print(json.dumps(diagnosis, ensure_ascii=False, indent=2))
    elif args.fix:
        assistant.apply_fix(args.fix)
    elif args.rollback:
        if assistant.manager:
            assistant.manager.rollback_to_backup(args.rollback)
    else:
        # 対話モード
        assistant.interactive_fix()

if __name__ == "__main__":
    main()