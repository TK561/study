#!/usr/bin/env python3
"""
自動監視システム起動スクリプト
Claude Code起動時に自動時間監視システムをバックグラウンドで開始
"""

import subprocess
import sys
import threading
import time
from pathlib import Path
import atexit
import signal
import os

class AutoMonitorStarter:
    def __init__(self):
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.monitor_process = None
        self.is_running = False
        
    def start_background_monitor(self):
        """バックグラウンドで監視システムを開始"""
        try:
            # 既存のプロセスをチェック
            if self.is_monitor_running():
                print("🔄 自動時間監視システムは既に実行中です")
                return True
            
            print("🚀 自動時間監視システムをバックグラウンドで開始...")
            
            # バックグラウンドプロセスとして実行
            self.monitor_process = subprocess.Popen(
                [sys.executable, "auto_hourly_monitor.py", "start"],
                cwd=self.root_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            self.is_running = True
            
            # 終了時の処理を登録
            atexit.register(self.cleanup)
            signal.signal(signal.SIGTERM, self.signal_handler)
            signal.signal(signal.SIGINT, self.signal_handler)
            
            print("✅ 自動時間監視システム開始完了")
            print("📋 条件: Claude Code実行中 かつ 毎時0分に自動整理・保存実行")
            print("🔍 監視間隔: 30秒")
            
            return True
            
        except Exception as e:
            print(f"❌ 自動時間監視システム開始失敗: {e}")
            return False
    
    def is_monitor_running(self):
        """監視システムが実行中かチェック"""
        try:
            result = subprocess.run(
                [sys.executable, "auto_hourly_monitor.py", "status"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return "監視中: True" in result.stdout
        except:
            return False
    
    def stop_monitor(self):
        """監視システムを停止"""
        try:
            if self.monitor_process and self.monitor_process.poll() is None:
                self.monitor_process.terminate()
                self.monitor_process.wait(timeout=5)
                print("⏹️ 自動時間監視システム停止")
            
            # 明示的に停止コマンドも実行
            subprocess.run(
                [sys.executable, "auto_hourly_monitor.py", "stop"],
                cwd=self.root_path,
                timeout=5
            )
            
            self.is_running = False
            
        except Exception as e:
            print(f"⚠️ 監視システム停止エラー: {e}")
    
    def cleanup(self):
        """終了時のクリーンアップ"""
        if self.is_running:
            self.stop_monitor()
    
    def signal_handler(self, signum, frame):
        """シグナルハンドラ"""
        print(f"\n📡 シグナル {signum} 受信 - 自動監視システム終了")
        self.cleanup()
        sys.exit(0)
    
    def get_status(self):
        """監視システムの状態を取得"""
        try:
            result = subprocess.run(
                [sys.executable, "auto_hourly_monitor.py", "status"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout
        except Exception as e:
            return f"状態取得エラー: {e}"

def main():
    """メイン実行"""
    starter = AutoMonitorStarter()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            starter.start_background_monitor()
            
        elif command == "stop":
            starter.stop_monitor()
            
        elif command == "status":
            status = starter.get_status()
            print(status)
            
        elif command == "restart":
            print("🔄 自動監視システム再起動中...")
            starter.stop_monitor()
            time.sleep(2)
            starter.start_background_monitor()
            
        else:
            print("使用方法: python3 start_auto_monitor.py [start|stop|status|restart]")
    else:
        # デフォルトは開始
        starter.start_background_monitor()

if __name__ == "__main__":
    main()