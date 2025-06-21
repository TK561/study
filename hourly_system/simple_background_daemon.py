#!/usr/bin/env python3
"""
Simple Background Daemon - Terminal Independent

Generated with Claude Code
Date: 2025-06-20
Purpose: シンプルなバックグラウンドデーモン（ターミナル終了後も継続）
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

def start_background_daemon(project_root="/mnt/c/Desktop/Research"):
    """バックグラウンドデーモンの開始"""
    
    project_path = Path(project_root)
    session_logs = project_path / "session_logs"
    session_logs.mkdir(exist_ok=True)
    
    pid_file = session_logs / "bg_daemon.pid"
    log_file = session_logs / "bg_daemon.log"
    
    # 既存デーモンチェック
    if pid_file.exists():
        try:
            with open(pid_file, 'r') as f:
                existing_pid = int(f.read().strip())
            
            # プロセス存在確認
            os.kill(existing_pid, 0)
            print(f" Daemon already running (PID: {existing_pid})")
            return existing_pid
        
        except (ProcessLookupError, ValueError):
            pid_file.unlink()
    
    # バックグラウンドで起動
    daemon_script = f'''
import os
import sys
import json
import time
import signal
import datetime
from pathlib import Path

class BackgroundDaemon:
    def __init__(self):
        self.project_root = Path("{project_root}")
        self.session_logs = self.project_root / "session_logs"
        self.log_file = self.session_logs / "bg_daemon.log"
        self.status_file = self.session_logs / "daemon_status.json"
        self.running = True
        self.start_time = datetime.datetime.now()
        
        # シグナルハンドラー
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        
    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"[{{timestamp}}] {{message}}\\n")
    
    def update_status(self, status):
        data = {{
            "status": status,
            "pid": os.getpid(),
            "start_time": self.start_time.isoformat(),
            "last_update": datetime.datetime.now().isoformat()
        }}
        with open(self.status_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def stop(self, signum=None, frame=None):
        self.log("Daemon stopping...")
        self.running = False
        self.update_status("stopped")
    
    def generate_summary(self):
        current_time = datetime.datetime.now()
        summary = {{
            "timestamp": current_time.isoformat(),
            "daemon_pid": os.getpid(),
            "uptime": str(current_time - self.start_time),
            "status": "active"
        }}
        
        summary_file = self.session_logs / f"summary_{{current_time.strftime('%Y%m%d_%H%M%S')}}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.log(f" Summary generated: {{summary_file.name}}")
    
    def run(self):
        self.log("Background daemon started")
        self.update_status("running")
        
        while self.running:
            try:
                time.sleep(3600)  # 1時間待機
                if self.running:
                    self.generate_summary()
            except Exception as e:
                self.log(f"Error: {{e}}")
                time.sleep(60)
        
        self.log("Daemon stopped")

if __name__ == "__main__":
    daemon = BackgroundDaemon()
    daemon.run()
'''
    
    # スクリプトファイル作成
    daemon_file = session_logs / "temp_daemon.py"
    with open(daemon_file, 'w') as f:
        f.write(daemon_script)
    
    try:
        # nohup で完全バックグラウンド実行
        cmd = [
            'nohup', 
            'python3', 
            str(daemon_file),
            '&'
        ]
        
        # シェル経由で実行（リダイレクト付き）
        shell_cmd = f"nohup python3 '{daemon_file}' > /dev/null 2>&1 & echo $!"
        
        result = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True, 
                               cwd=project_path)
        
        if result.stdout.strip():
            pid = int(result.stdout.strip())
            
            # PIDファイル保存
            with open(pid_file, 'w') as f:
                f.write(str(pid))
            
            print(f" Background daemon started successfully")
            print(f"🔢 PID: {pid}")
            print(f" Log: {log_file}")
            print(f" Will continue after terminal closes")
            
            return pid
        else:
            print(f" Failed to start daemon: {result.stderr}")
            return None
    
    except Exception as e:
        print(f" Daemon start error: {e}")
        return None

def stop_background_daemon(project_root="/mnt/c/Desktop/Research"):
    """バックグラウンドデーモンの停止"""
    
    project_path = Path(project_root)
    pid_file = project_path / "session_logs" / "bg_daemon.pid"
    
    if not pid_file.exists():
        print(" No daemon PID file found")
        return False
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        os.kill(pid, signal.SIGTERM)
        pid_file.unlink()
        
        print(f" Daemon stopped (PID: {pid})")
        return True
    
    except ProcessLookupError:
        print(" Daemon process not found")
        pid_file.unlink()
        return False
    except Exception as e:
        print(f" Error stopping daemon: {e}")
        return False

def check_daemon_status(project_root="/mnt/c/Desktop/Research"):
    """デーモン状態確認"""
    
    project_path = Path(project_root)
    pid_file = project_path / "session_logs" / "bg_daemon.pid"
    status_file = project_path / "session_logs" / "daemon_status.json"
    
    if not pid_file.exists():
        print(" No daemon running")
        return False
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # プロセス存在確認
        os.kill(pid, 0)
        
        # ステータス読み込み
        if status_file.exists():
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            print(f" Daemon running")
            print(f"🔢 PID: {pid}")
            print(f" Started: {status.get('start_time', 'Unknown')}")
            print(f" Status: {status.get('status', 'Unknown')}")
            print(f" Last update: {status.get('last_update', 'Unknown')}")
        else:
            print(f" Daemon running (PID: {pid})")
        
        return True
    
    except ProcessLookupError:
        print(" Daemon process not running")
        pid_file.unlink()
        return False
    except Exception as e:
        print(f" Error checking status: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Background Daemon')
    parser.add_argument('--start', action='store_true', help='Start daemon')
    parser.add_argument('--stop', action='store_true', help='Stop daemon')
    parser.add_argument('--status', action='store_true', help='Check status')
    parser.add_argument('--project-root', default='/mnt/c/Desktop/Research', 
                       help='Project root directory')
    
    args = parser.parse_args()
    
    if args.stop:
        stop_background_daemon(args.project_root)
    elif args.status:
        check_daemon_status(args.project_root)
    else:
        # デフォルトで起動
        start_background_daemon(args.project_root)