#!/usr/bin/env python3
"""
自動時間監視システム - 毎時0分に自動整理・保存を実行
Claude Code起動中かつ時刻の分が0の時に自動実行
"""

import time
import threading
import subprocess
import psutil
from datetime import datetime
from pathlib import Path
import json
import os

class AutoHourlyMonitor:
    def __init__(self):
        self.name = "自動時間監視システム"
        self.version = "1.0.0"
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.is_running = False
        self.monitoring_thread = None
        
        # 監視設定
        self.check_interval = 30  # 30秒間隔でチェック
        self.last_execution_hour = -1  # 最後に実行した時間
        
        # Claude Code関連プロセス名
        self.claude_processes = [
            "claude",
            "claude-code", 
            "claude_code",
            "node",  # Claude Codeがnodeプロセスとして実行される場合
            "python3"  # Python環境でClaude Codeが実行される場合
        ]
        
        # ログファイル
        self.log_file = self.root_path / "auto_hourly_monitor.log"
        
    def is_claude_code_running(self):
        """Claude Codeが実行中かを確認"""
        try:
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    process_info = process.info
                    process_name = process_info['name'].lower()
                    cmdline = ' '.join(process_info['cmdline'] or []).lower()
                    
                    # Claude Code関連プロセスをチェック
                    if any(claude_proc in process_name for claude_proc in self.claude_processes):
                        # コマンドラインでClaude Code関連を確認
                        if any(keyword in cmdline for keyword in ['claude', 'anthropic', 'research']):
                            return True
                    
                    # Python環境でのClaude Code実行をチェック
                    if 'python' in process_name and 'claude' in cmdline:
                        return True
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return False
            
        except Exception as e:
            self.log_message(f"プロセス確認エラー: {e}")
            return False
    
    def should_execute_now(self):
        """現在実行すべきかを判定"""
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        
        # 条件チェック
        conditions = {
            "claude_running": self.is_claude_code_running(),
            "minute_is_zero": current_minute == 0,
            "not_executed_this_hour": current_hour != self.last_execution_hour
        }
        
        self.log_message(f"実行条件チェック {now.strftime('%H:%M:%S')}: {conditions}")
        
        return all(conditions.values())
    
    def execute_auto_organize_save(self):
        """自動整理・保存システムを実行"""
        try:
            self.log_message("自動整理・保存システム実行開始")
            
            # auto_organize_and_save.pyを実行
            result = subprocess.run(
                ["python3", "auto_organize_and_save.py", "自動実行（毎時0分）"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                timeout=300  # 5分タイムアウト
            )
            
            if result.returncode == 0:
                self.log_message("自動整理・保存実行成功")
                self.log_message(f"出力: {result.stdout[:500]}...")  # 最初の500文字
            else:
                self.log_message(f"自動整理・保存実行失敗: {result.stderr}")
                
            # 実行時間を記録
            self.last_execution_hour = datetime.now().hour
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.log_message("自動整理・保存実行タイムアウト")
            return False
        except Exception as e:
            self.log_message(f"自動整理・保存実行エラー: {e}")
            return False
    
    def monitoring_loop(self):
        """監視ループ"""
        self.log_message("自動時間監視開始")
        
        while self.is_running:
            try:
                if self.should_execute_now():
                    self.log_message("実行条件満たしました - 自動整理・保存を実行")
                    success = self.execute_auto_organize_save()
                    
                    if success:
                        self.log_message("自動実行完了")
                    else:
                        self.log_message("自動実行失敗")
                
                # 指定間隔で待機
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log_message("監視システム停止要求受信")
                break
            except Exception as e:
                self.log_message(f"監視ループエラー: {e}")
                time.sleep(60)  # エラー時は1分待機
        
        self.log_message("自動時間監視終了")
    
    def start_monitoring(self):
        """監視開始"""
        if self.is_running:
            self.log_message("既に監視中です")
            return False
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(
            target=self.monitoring_loop,
            name="AutoHourlyMonitor",
            daemon=True
        )
        self.monitoring_thread.start()
        
        self.log_message("自動時間監視システム開始")
        print("🕐 自動時間監視システム開始")
        print(f"📋 監視条件: Claude Code実行中 かつ 毎時0分")
        print(f"🔍 チェック間隔: {self.check_interval}秒")
        print(f"📄 ログファイル: {self.log_file}")
        
        return True
    
    def stop_monitoring(self):
        """監視停止"""
        if not self.is_running:
            self.log_message("監視は実行されていません")
            return False
        
        self.is_running = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)
        
        self.log_message("自動時間監視システム停止")
        print("⏹️ 自動時間監視システム停止")
        
        return True
    
    def get_status(self):
        """現在の状態を取得"""
        now = datetime.now()
        claude_running = self.is_claude_code_running()
        
        status = {
            "monitoring_active": self.is_running,
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "claude_code_running": claude_running,
            "last_execution_hour": self.last_execution_hour,
            "next_check_in": self.check_interval - (now.second % self.check_interval),
            "conditions": {
                "claude_running": claude_running,
                "minute_is_zero": now.minute == 0,
                "not_executed_this_hour": now.hour != self.last_execution_hour
            }
        }
        
        return status
    
    def log_message(self, message):
        """ログメッセージを記録"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"ログ書き込みエラー: {e}")

def main():
    """メイン実行関数"""
    import sys
    
    monitor = AutoHourlyMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            monitor.start_monitoring()
            try:
                # フォアグラウンドで実行継続
                while monitor.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                
        elif command == "stop":
            monitor.stop_monitoring()
            
        elif command == "status":
            status = monitor.get_status()
            print("📊 自動時間監視システム状態:")
            print(f"  🔄 監視中: {status['monitoring_active']}")
            print(f"  ⏰ 現在時刻: {status['current_time']}")
            print(f"  🖥️ Claude Code実行中: {status['claude_code_running']}")
            print(f"  📅 最後実行時間: {status['last_execution_hour']}時")
            print(f"  ⏭️ 次回チェック: {status['next_check_in']}秒後")
            print(f"  ✅ 実行条件:")
            for condition, value in status['conditions'].items():
                print(f"    - {condition}: {value}")
                
        elif command == "test":
            # テスト実行
            print("🧪 テスト実行中...")
            success = monitor.execute_auto_organize_save()
            print(f"✅ テスト結果: {'成功' if success else '失敗'}")
            
        else:
            print(f"❌ 不明なコマンド: {command}")
            print("使用方法: python3 auto_hourly_monitor.py [start|stop|status|test]")
    else:
        # デフォルトは監視開始
        monitor.start_monitoring()
        try:
            while monitor.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()

if __name__ == "__main__":
    main()