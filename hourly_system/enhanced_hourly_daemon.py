#!/usr/bin/env python3
"""
Enhanced Hourly Daemon - True Background Service

Generated with Claude Code
Date: 2025-06-20
Purpose: デーモンとして動作する改良版1時間毎システム
Verified: 実装済み
"""

import os
import sys
import json
import time
import signal
import argparse
import datetime
import threading
from pathlib import Path
from typing import Dict, List, Any
import subprocess

class EnhancedHourlyDaemon:
    """真のバックグラウンドデーモンとしての1時間システム"""
    
    def __init__(self, project_root: str = "/mnt/c/Desktop/Research", daemon_mode: bool = False):
        self.project_root = Path(project_root)
        self.daemon_mode = daemon_mode
        self.running = True
        
        # ログとセッション管理
        self.session_log = self.project_root / "session_logs"
        self.session_log.mkdir(exist_ok=True)
        
        self.daemon_log = self.session_log / "daemon.log"
        self.pid_file = self.session_log / "hourly_daemon.pid"
        
        # セッション開始
        self.session_start = datetime.datetime.now()
        self.last_summary = self.session_start
        
        # 現在のセッションファイル
        self.current_session = self.session_log / f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        
        # デーモン初期化
        if daemon_mode:
            self.daemonize()
        
        # シグナルハンドラー設定
        self.setup_signal_handlers()
        
        # セッション初期化
        self.init_session()
        
        # メインループ開始
        self.start_main_loop()
    
    def daemonize(self):
        """プロセスをデーモン化"""
        try:
            # 二重フォーク
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # 最初の親プロセス終了
        except OSError as e:
            sys.stderr.write(f"Fork #1 failed: {e}\n")
            sys.exit(1)
        
        # セッションリーダーになる
        os.setsid()
        os.umask(0)
        
        try:
            # 二回目のフォーク
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # 二番目の親プロセス終了
        except OSError as e:
            sys.stderr.write(f"Fork #2 failed: {e}\n")
            sys.exit(1)
        
        # 標準入出力をリダイレクト
        sys.stdout.flush()
        sys.stderr.flush()
        
        with open('/dev/null', 'r') as stdin:
            os.dup2(stdin.fileno(), sys.stdin.fileno())
        
        with open(self.daemon_log, 'a') as stdout:
            os.dup2(stdout.fileno(), sys.stdout.fileno())
        
        with open(self.daemon_log, 'a') as stderr:
            os.dup2(stderr.fileno(), sys.stderr.fileno())
        
        # PIDファイル作成
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        self.log_daemon_message("Daemon started successfully")
    
    def setup_signal_handlers(self):
        """シグナルハンドラーの設定"""
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGHUP, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """シグナル受信時の処理"""
        self.log_daemon_message(f"Received signal {signum}, shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def log_daemon_message(self, message: str):
        """デーモンログへの記録"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.daemon_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            # フォールバック
            print(f"[{timestamp}] {message}")
    
    def init_session(self):
        """セッション初期化"""
        session_data = {
            "session_start": self.session_start.isoformat(),
            "daemon_mode": self.daemon_mode,
            "project_root": str(self.project_root),
            "git_status": self.get_git_status(),
            "initial_file_count": self.count_files(),
            "summaries": []
        }
        
        with open(self.current_session, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        self.log_daemon_message(f"Session initialized: {self.current_session}")
    
    def get_git_status(self):
        """Git状態の取得"""
        try:
            os.chdir(self.project_root)
            
            # ブランチ取得
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True)
            branch = branch_result.stdout.strip()
            
            # ステータス取得
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True)
            status = status_result.stdout.strip()
            
            # 最近のコミット
            log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                      capture_output=True, text=True)
            recent_commits = log_result.stdout.strip().split('\n') if log_result.stdout else []
            
            return {
                "branch": branch,
                "status": status,
                "recent_commits": recent_commits,
                "timestamp": datetime.datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.datetime.now().isoformat()}
    
    def count_files(self):
        """ファイル数カウント"""
        try:
            python_files = len(list(self.project_root.rglob("*.py")))
            markdown_files = len(list(self.project_root.rglob("*.md")))
            config_files = len(list(self.project_root.rglob("*.json"))) + \
                          len(list(self.project_root.rglob("*.yaml"))) + \
                          len(list(self.project_root.rglob("*.yml")))
            total_files = len([f for f in self.project_root.rglob("*") if f.is_file()])
            
            return {
                "python_files": python_files,
                "markdown_files": markdown_files,
                "config_files": config_files,
                "total_files": total_files
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_hourly_summary(self):
        """1時間毎まとめの生成"""
        current_time = datetime.datetime.now()
        
        summary_data = {
            "timestamp": current_time.isoformat(),
            "time_since_start": str(current_time - self.session_start),
            "time_since_last": str(current_time - self.last_summary),
            "git_status": self.get_git_status(),
            "file_count": self.count_files(),
            "system_status": "active"
        }
        
        # セッションファイルに追加
        try:
            with open(self.current_session, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            session_data["summaries"].append(summary_data)
            
            with open(self.current_session, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            self.log_daemon_message(f"Error saving summary: {e}")
        
        # ログ出力
        self.log_daemon_message(" Hourly summary generated")
        self.log_daemon_message(f" Session file: {self.current_session}")
        self.log_daemon_message(f" Next summary at: {(current_time + datetime.timedelta(hours=1)).strftime('%H:%M')}")
        
        self.last_summary = current_time
        
        return summary_data
    
    def start_main_loop(self):
        """メインループ開始"""
        self.log_daemon_message("Starting main daemon loop")
        
        while self.running:
            try:
                # 1時間待機
                time.sleep(3600)  # 3600秒 = 1時間
                
                if self.running:  # 停止シグナル確認
                    self.generate_hourly_summary()
            
            except Exception as e:
                self.log_daemon_message(f"Error in main loop: {e}")
                time.sleep(60)  # エラー時は1分待機
    
    def cleanup(self):
        """クリーンアップ処理"""
        try:
            # 最終サマリー生成
            final_summary = self.generate_hourly_summary()
            final_summary["final_summary"] = True
            
            # PIDファイル削除
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            self.log_daemon_message("Daemon cleanup completed")
        
        except Exception as e:
            self.log_daemon_message(f"Cleanup error: {e}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Enhanced Hourly Daemon')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--project-root', default='/mnt/c/Desktop/Research', 
                       help='Project root directory')
    parser.add_argument('--stop', action='store_true', help='Stop running daemon')
    
    args = parser.parse_args()
    
    if args.stop:
        # デーモン停止
        pid_file = Path(args.project_root) / "session_logs" / "hourly_daemon.pid"
        if pid_file.exists():
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"Daemon stopped (PID: {pid})")
            except ProcessLookupError:
                print("Daemon not running")
                pid_file.unlink()
        else:
            print("No daemon PID file found")
        return
    
    # デーモン起動
    try:
        daemon = EnhancedHourlyDaemon(
            project_root=args.project_root,
            daemon_mode=args.daemon
        )
    except KeyboardInterrupt:
        print("Daemon interrupted")
    except Exception as e:
        print(f"Daemon error: {e}")

if __name__ == "__main__":
    main()