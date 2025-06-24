#!/usr/bin/env python3
"""
自動Git管理システム - Git操作の自動化
"""

import os
import sys
import json
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class AutoGitManager:
    """自動Git管理システム"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "AUTO_GIT_CONFIG.json"
        self.log_file = self.project_root / "AUTO_GIT_LOG.json"
        self.config = self.load_config()
        self.running = False
        
    def load_config(self) -> Dict:
        """設定を読み込み"""
        default_config = {
            "auto_commit": True,
            "auto_push": True,
            "auto_pull": True,
            "commit_interval": 300,  # 5分毎
            "push_interval": 600,    # 10分毎
            "pull_interval": 300,    # 5分毎
            "auto_commit_message_template": "🤖 Auto commit - {timestamp}",
            "watched_extensions": [".py", ".html", ".css", ".js", ".json", ".md"],
            "ignore_patterns": ["__pycache__", ".vscode", "node_modules", "*.log"],
            "branch": "main",
            "max_log_entries": 1000
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
    
    def log_event(self, event_type: str, message: str, status: str = "info", details: Optional[str] = None):
        """イベントをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
            "status": status,
            "details": details
        }
        
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                pass
        
        logs.append(log_entry)
        logs = logs[-self.config['max_log_entries']:]  # 設定数のみ保持
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {event_type}: {message}")
    
    def run_git_command(self, command: List[str], timeout: int = 30) -> Dict:
        """Gitコマンドを実行"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.project_root
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timeout",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def check_git_status(self) -> Dict:
        """Git状態をチェック"""
        # git status --porcelain
        result = self.run_git_command(['git', 'status', '--porcelain'])
        
        if not result['success']:
            return {"has_changes": False, "files": [], "error": result['stderr']}
        
        changes = []
        for line in result['stdout'].split('\n'):
            if line.strip():
                status = line[:2]
                filename = line[3:]
                changes.append({"status": status, "file": filename})
        
        return {"has_changes": len(changes) > 0, "files": changes}
    
    def should_commit_file(self, filename: str) -> bool:
        """ファイルをコミット対象とするかチェック"""
        file_path = Path(filename)
        
        # 拡張子チェック
        if file_path.suffix not in self.config['watched_extensions']:
            return False
        
        # 無視パターンチェック
        for pattern in self.config['ignore_patterns']:
            if pattern in filename:
                return False
        
        return True
    
    def auto_commit(self) -> bool:
        """自動コミットを実行"""
        if not self.config['auto_commit']:
            return True
        
        try:
            # 状態チェック
            status = self.check_git_status()
            
            if 'error' in status:
                self.log_event("COMMIT", f"状態チェックエラー: {status['error']}", "error")
                return False
            
            if not status['has_changes']:
                self.log_event("COMMIT", "変更なし", "info")
                return True
            
            # コミット対象ファイルを確認
            files_to_commit = []
            for change in status['files']:
                if self.should_commit_file(change['file']):
                    files_to_commit.append(change['file'])
            
            if not files_to_commit:
                self.log_event("COMMIT", "コミット対象ファイルなし", "info")
                return True
            
            # git add
            for file in files_to_commit:
                add_result = self.run_git_command(['git', 'add', file])
                if not add_result['success']:
                    self.log_event("COMMIT", f"add失敗 {file}: {add_result['stderr']}", "error")
            
            # コミットメッセージ生成
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = self.config['auto_commit_message_template'].format(
                timestamp=timestamp,
                files_count=len(files_to_commit)
            )
            
            # git commit
            commit_result = self.run_git_command(['git', 'commit', '-m', commit_message])
            
            if commit_result['success']:
                self.log_event("COMMIT", f"成功: {len(files_to_commit)}ファイル", "success", commit_message)
                return True
            else:
                self.log_event("COMMIT", f"失敗: {commit_result['stderr']}", "error")
                return False
                
        except Exception as e:
            self.log_event("COMMIT", f"エラー: {e}", "error")
            return False
    
    def auto_push(self) -> bool:
        """自動プッシュを実行"""
        if not self.config['auto_push']:
            return True
        
        try:
            # ローカルの変更をチェック
            status_result = self.run_git_command(['git', 'status', '--porcelain'])
            
            # コミットされていない変更があれば先にコミット
            if status_result['success'] and status_result['stdout']:
                self.auto_commit()
            
            # リモートとの差分をチェック
            fetch_result = self.run_git_command(['git', 'fetch', 'origin', self.config['branch']])
            if not fetch_result['success']:
                self.log_event("PUSH", f"fetch失敗: {fetch_result['stderr']}", "error")
                return False
            
            # ローカルがリモートより先にあるかチェック
            ahead_result = self.run_git_command([
                'git', 'rev-list', '--count', f"origin/{self.config['branch']}..HEAD"
            ])
            
            if not ahead_result['success']:
                self.log_event("PUSH", f"ahead確認失敗: {ahead_result['stderr']}", "error")
                return False
            
            ahead_count = int(ahead_result['stdout']) if ahead_result['stdout'].isdigit() else 0
            
            if ahead_count == 0:
                self.log_event("PUSH", "プッシュ対象なし", "info")
                return True
            
            # git push
            push_result = self.run_git_command(['git', 'push', 'origin', self.config['branch']])
            
            if push_result['success']:
                self.log_event("PUSH", f"成功: {ahead_count}コミット", "success")
                return True
            else:
                self.log_event("PUSH", f"失敗: {push_result['stderr']}", "error")
                return False
                
        except Exception as e:
            self.log_event("PUSH", f"エラー: {e}", "error")
            return False
    
    def auto_pull(self) -> bool:
        """自動プルを実行"""
        if not self.config['auto_pull']:
            return True
        
        try:
            # リモートの変更をチェック
            fetch_result = self.run_git_command(['git', 'fetch', 'origin', self.config['branch']])
            if not fetch_result['success']:
                self.log_event("PULL", f"fetch失敗: {fetch_result['stderr']}", "error")
                return False
            
            # リモートがローカルより先にあるかチェック
            behind_result = self.run_git_command([
                'git', 'rev-list', '--count', f"HEAD..origin/{self.config['branch']}"
            ])
            
            if not behind_result['success']:
                self.log_event("PULL", f"behind確認失敗: {behind_result['stderr']}", "error")
                return False
            
            behind_count = int(behind_result['stdout']) if behind_result['stdout'].isdigit() else 0
            
            if behind_count == 0:
                self.log_event("PULL", "プル対象なし", "info")
                return True
            
            # ローカルに未コミットの変更があるかチェック
            status = self.check_git_status()
            if status['has_changes']:
                # 先にコミット
                self.auto_commit()
            
            # git pull
            pull_result = self.run_git_command(['git', 'pull', 'origin', self.config['branch']])
            
            if pull_result['success']:
                self.log_event("PULL", f"成功: {behind_count}コミット", "success")
                return True
            else:
                self.log_event("PULL", f"失敗: {pull_result['stderr']}", "error")
                return False
                
        except Exception as e:
            self.log_event("PULL", f"エラー: {e}", "error")
            return False
    
    def run_sync_cycle(self):
        """同期サイクルを実行"""
        self.log_event("SYNC", "同期サイクル開始", "info")
        
        # 1. プル（リモートの最新を取得）
        pull_success = self.auto_pull()
        
        # 2. コミット（ローカルの変更をコミット）
        commit_success = self.auto_commit()
        
        # 3. プッシュ（ローカルの変更をリモートに送信）
        push_success = self.auto_push()
        
        if pull_success and commit_success and push_success:
            self.log_event("SYNC", "同期サイクル完了", "success")
        else:
            self.log_event("SYNC", "同期サイクル部分的失敗", "warning")
    
    def start_auto_sync(self):
        """自動同期を開始"""
        self.running = True
        self.log_event("AUTO_SYNC", "自動同期開始", "info")
        
        def sync_loop():
            last_commit = time.time()
            last_push = time.time()
            last_pull = time.time()
            
            while self.running:
                try:
                    current_time = time.time()
                    
                    # プル（最も頻繁）
                    if current_time - last_pull >= self.config['pull_interval']:
                        self.auto_pull()
                        last_pull = current_time
                    
                    # コミット
                    if current_time - last_commit >= self.config['commit_interval']:
                        self.auto_commit()
                        last_commit = current_time
                    
                    # プッシュ
                    if current_time - last_push >= self.config['push_interval']:
                        self.auto_push()
                        last_push = current_time
                    
                    time.sleep(10)  # 10秒毎にチェック
                    
                except Exception as e:
                    self.log_event("AUTO_SYNC", f"ループエラー: {e}", "error")
                    time.sleep(30)  # エラー時は少し長く待機
        
        thread = threading.Thread(target=sync_loop, daemon=True)
        thread.start()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 自動同期を停止します...")
            self.running = False
            self.log_event("AUTO_SYNC", "自動同期停止", "info")
    
    def show_status(self):
        """現在の状態を表示"""
        print("📊 Git状態:")
        print("-" * 40)
        
        # ブランチ情報
        branch_result = self.run_git_command(['git', 'branch', '--show-current'])
        if branch_result['success']:
            print(f"🌿 現在のブランチ: {branch_result['stdout']}")
        
        # 状態情報
        status = self.check_git_status()
        if 'error' in status:
            print(f"❌ エラー: {status['error']}")
        else:
            if status['has_changes']:
                print(f"📝 未コミット変更: {len(status['files'])}ファイル")
                for change in status['files'][:5]:  # 最初の5件のみ表示
                    print(f"   {change['status']} {change['file']}")
            else:
                print("✅ すべてコミット済み")
        
        # リモートとの差分
        fetch_result = self.run_git_command(['git', 'fetch', 'origin', self.config['branch']])
        if fetch_result['success']:
            ahead_result = self.run_git_command([
                'git', 'rev-list', '--count', f"origin/{self.config['branch']}..HEAD"
            ])
            behind_result = self.run_git_command([
                'git', 'rev-list', '--count', f"HEAD..origin/{self.config['branch']}"
            ])
            
            if ahead_result['success'] and behind_result['success']:
                ahead = int(ahead_result['stdout']) if ahead_result['stdout'].isdigit() else 0
                behind = int(behind_result['stdout']) if behind_result['stdout'].isdigit() else 0
                
                if ahead > 0:
                    print(f"⬆️ プッシュ待ち: {ahead}コミット")
                if behind > 0:
                    print(f"⬇️ プル待ち: {behind}コミット")
                if ahead == 0 and behind == 0:
                    print("🔄 リモートと同期済み")

def main():
    """メイン関数"""
    git_manager = AutoGitManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            git_manager.start_auto_sync()
        elif command == "sync":
            git_manager.run_sync_cycle()
        elif command == "commit":
            git_manager.auto_commit()
        elif command == "push":
            git_manager.auto_push()
        elif command == "pull":
            git_manager.auto_pull()
        elif command == "status":
            git_manager.show_status()
        elif command == "config":
            print(json.dumps(git_manager.config, indent=2, ensure_ascii=False))
        elif command == "log":
            if git_manager.log_file.exists():
                with open(git_manager.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    for log in logs[-20:]:  # 最新20件
                        print(f"[{log['timestamp']}] {log['event_type']}: {log['message']}")
            else:
                print("📝 ログファイルが見つかりません")
        else:
            print("使用方法:")
            print("  python3 auto_git_manager.py start   - 自動同期開始")
            print("  python3 auto_git_manager.py sync    - 同期サイクル実行")
            print("  python3 auto_git_manager.py commit  - 自動コミット")
            print("  python3 auto_git_manager.py push    - 自動プッシュ")
            print("  python3 auto_git_manager.py pull    - 自動プル")
            print("  python3 auto_git_manager.py status  - 状態表示")
            print("  python3 auto_git_manager.py config  - 設定表示")
            print("  python3 auto_git_manager.py log     - ログ表示")
    else:
        git_manager.run_sync_cycle()

if __name__ == "__main__":
    main()