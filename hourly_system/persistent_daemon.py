#!/usr/bin/env python3
"""
Persistent Daemon - True Independent Background Service

Generated with Claude Code
Date: 2025-06-20
Purpose: ターミナル終了に依存しない完全独立デーモン
Verified: 実装済み
"""

import os
import sys
import json
import time
import signal
import datetime
import subprocess
from pathlib import Path

class PersistentDaemon:
    """完全独立型デーモン"""
    
    def __init__(self, project_root: str = "/mnt/c/Desktop/Research"):
        self.project_root = Path(project_root)
        self.session_log = self.project_root / "session_logs"
        self.session_log.mkdir(exist_ok=True)
        
        self.daemon_log = self.session_log / "persistent_daemon.log"
        self.pid_file = self.session_log / "persistent_daemon.pid"
        self.status_file = self.session_log / "daemon_status.json"
        
        self.running = True
        self.session_start = datetime.datetime.now()
        self.last_summary = self.session_start
    
    def is_already_running(self):
        """既存デーモンの確認"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # プロセス存在確認
            os.kill(pid, 0)  # シグナル0で存在確認
            return True
        
        except (ProcessLookupError, ValueError):
            # プロセス不存在、PIDファイル削除
            self.pid_file.unlink()
            return False
    
    def start_as_systemd_service(self):
        """systemd-run による完全独立プロセス起動"""
        
        if self.is_already_running():
            self.log_message("Daemon already running, skipping start")
            return True
        
        try:
            # systemd-run でユーザースコープのサービスとして実行
            cmd = [
                'systemd-run',
                '--user',              # ユーザースコープ
                '--scope',             # スコープ単位
                '--unit=claude-hourly-daemon',  # ユニット名
                'python3',
                str(Path(__file__)),
                '--internal-daemon',
                str(self.project_root)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_message(f"Started as systemd service: {result.stdout.strip()}")
                return True
            else:
                self.log_message(f"systemd-run failed: {result.stderr}")
                return self.fallback_nohup_start()
        
        except FileNotFoundError:
            self.log_message("systemd-run not available, using nohup fallback")
            return self.fallback_nohup_start()
    
    def fallback_nohup_start(self):
        """nohup + disown による代替起動"""
        
        try:
            # 完全にバックグラウンド化されたプロセス起動
            cmd = f"""
            nohup python3 '{Path(__file__)}' --internal-daemon '{self.project_root}' \\
                </dev/null >/dev/null 2>&1 & \\
            echo $! > '{self.pid_file}'
            """
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_message("Started with nohup + background")
                return True
            else:
                self.log_message(f"nohup start failed: {result.stderr}")
                return False
        
        except Exception as e:
            self.log_message(f"Fallback start failed: {e}")
            return False
    
    def run_internal_daemon(self):
        """内部デーモンループ（実際の作業プロセス）"""
        
        # 完全な環境分離
        os.chdir(self.project_root)
        os.umask(0o022)
        
        # シグナルハンドラー設定
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)  # HUPを無視
        
        # PIDファイル作成
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # ステータスファイル作成
        self.update_status("running")
        
        self.log_message(f"Internal daemon started (PID: {os.getpid()})")
        
        # メインループ
        while self.running:
            try:
                # 1時間待機
                time.sleep(3600)
                
                if self.running:
                    self.generate_hourly_summary()
            
            except Exception as e:
                self.log_message(f"Error in daemon loop: {e}")
                time.sleep(60)  # エラー時は1分待機
        
        self.cleanup()
    
    def shutdown_handler(self, signum, frame):
        """シャットダウンハンドラー"""
        self.log_message(f"Shutdown signal received: {signum}")
        self.running = False
    
    def generate_hourly_summary(self):
        """1時間毎サマリー生成"""
        current_time = datetime.datetime.now()
        
        summary_data = {
            "timestamp": current_time.isoformat(),
            "daemon_pid": os.getpid(),
            "time_since_start": str(current_time - self.session_start),
            "time_since_last": str(current_time - self.last_summary),
            "git_status": self.get_git_status(),
            "file_count": self.count_files(),
            "system_status": "persistent_daemon_active"
        }
        
        # サマリーファイル保存
        summary_file = self.session_log / f"hourly_summary_{current_time.strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        self.log_message(f" Hourly summary generated: {summary_file.name}")
        self.update_status("active", {"last_summary": current_time.isoformat()})
        
        self.last_summary = current_time
    
    def get_git_status(self):
        """Git状態取得"""
        try:
            # ブランチ
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         cwd=self.project_root, capture_output=True, text=True)
            branch = branch_result.stdout.strip()
            
            # ステータス
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         cwd=self.project_root, capture_output=True, text=True)
            status = status_result.stdout.strip()
            
            return {"branch": branch, "status": status, "timestamp": datetime.datetime.now().isoformat()}
        
        except Exception as e:
            return {"error": str(e)}
    
    def count_files(self):
        """ファイル数カウント"""
        try:
            python_files = len(list(self.project_root.rglob("*.py")))
            markdown_files = len(list(self.project_root.rglob("*.md")))
            total_files = len([f for f in self.project_root.rglob("*") if f.is_file()])
            
            return {"python_files": python_files, "markdown_files": markdown_files, "total_files": total_files}
        
        except Exception as e:
            return {"error": str(e)}
    
    def update_status(self, status: str, extra_data: dict = None):
        """ステータス更新"""
        status_data = {
            "status": status,
            "pid": os.getpid(),
            "last_update": datetime.datetime.now().isoformat(),
            "project_root": str(self.project_root)
        }
        
        if extra_data:
            status_data.update(extra_data)
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    def log_message(self, message: str):
        """ログ出力"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.daemon_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass  # ログエラーは無視
    
    def cleanup(self):
        """クリーンアップ"""
        try:
            self.update_status("stopped")
            
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            self.log_message("Daemon cleanup completed")
        
        except Exception as e:
            self.log_message(f"Cleanup error: {e}")
    
    def stop_daemon(self):
        """デーモン停止"""
        if not self.pid_file.exists():
            print("No daemon running")
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, signal.SIGTERM)
            print(f"Daemon stopped (PID: {pid})")
            return True
        
        except ProcessLookupError:
            print("Daemon not found")
            self.pid_file.unlink()
            return False
        except Exception as e:
            print(f"Error stopping daemon: {e}")
            return False

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Persistent Daemon')
    parser.add_argument('--start', action='store_true', help='Start daemon')
    parser.add_argument('--stop', action='store_true', help='Stop daemon')
    parser.add_argument('--status', action='store_true', help='Check status')
    parser.add_argument('--internal-daemon', help='Internal daemon mode')
    parser.add_argument('project_root', nargs='?', default='/mnt/c/Desktop/Research')
    
    args = parser.parse_args()
    
    daemon = PersistentDaemon(args.project_root)
    
    if args.internal_daemon:
        # 内部デーモンモード
        daemon.run_internal_daemon()
    
    elif args.stop:
        daemon.stop_daemon()
    
    elif args.status:
        if daemon.status_file.exists():
            with open(daemon.status_file, 'r') as f:
                status = json.load(f)
            print(f"Status: {status}")
        else:
            print("No daemon status file")
    
    else:
        # デーモン起動（デフォルト）
        success = daemon.start_as_systemd_service()
        if success:
            print(" Persistent daemon started successfully")
            print(" Will continue running even after terminal closes")
            print(f" Logs: {daemon.daemon_log}")
            print(f" Status: {daemon.status_file}")
        else:
            print(" Failed to start persistent daemon")

if __name__ == "__main__":
    main()