#!/usr/bin/env python3
"""
簡単な自動時間監視システム - psutil不要版
毎時0分に自動整理・保存を実行
"""

import time
import subprocess
import os
from datetime import datetime
from pathlib import Path

class SimpleAutoMonitor:
    def __init__(self):
        self.name = "簡単自動時間監視システム"
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.last_execution_hour = -1
        self.log_file = self.root_path / "simple_auto_monitor.log"
        
    def is_claude_code_running(self):
        """Claude Codeが実行中かを簡単にチェック"""
        try:
            # ps コマンドでプロセスを確認
            result = subprocess.run(
                ["ps", "aux"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            if result.returncode == 0:
                processes = result.stdout.lower()
                # Claude Code関連のキーワードをチェック
                keywords = ['claude', 'anthropic', 'research', 'node']
                return any(keyword in processes for keyword in keywords)
            
            return False
            
        except Exception as e:
            self.log_message(f"プロセス確認エラー: {e}")
            # エラー時は実行中とみなす（安全側）
            return True
    
    def should_execute_now(self):
        """現在実行すべきかを判定"""
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        
        # 条件：毎時0分 かつ 今時間にまだ実行していない
        is_zero_minute = current_minute == 0
        not_executed_this_hour = current_hour != self.last_execution_hour
        claude_running = self.is_claude_code_running()
        
        conditions = {
            "claude_running": claude_running,
            "minute_is_zero": is_zero_minute,
            "not_executed_this_hour": not_executed_this_hour
        }
        
        self.log_message(f"実行条件チェック {now.strftime('%H:%M:%S')}: {conditions}")
        
        return all(conditions.values())
    
    def execute_auto_organize_save(self):
        """自動整理・保存システムを実行"""
        try:
            self.log_message("自動整理・保存システム実行開始")
            
            result = subprocess.run(
                ["python3", "auto_organize_and_save.py", "自動実行（毎時0分）"],
                cwd=self.root_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.log_message("自動整理・保存実行成功")
                self.log_message(f"出力: {result.stdout[:300]}...")
            else:
                self.log_message(f"自動整理・保存実行失敗: {result.stderr}")
            
            # 実行時間を記録
            self.last_execution_hour = datetime.now().hour
            return result.returncode == 0
            
        except Exception as e:
            self.log_message(f"自動整理・保存実行エラー: {e}")
            return False
    
    def run_once(self):
        """一度だけチェックして実行"""
        if self.should_execute_now():
            self.log_message("実行条件満たしました - 自動整理・保存を実行")
            success = self.execute_auto_organize_save()
            
            if success:
                self.log_message("自動実行完了")
                print("✅ 自動実行完了")
                return True
            else:
                self.log_message("自動実行失敗")
                print("❌ 自動実行失敗")
                return False
        else:
            now = datetime.now()
            self.log_message(f"実行条件未満足 {now.strftime('%H:%M:%S')}")
            return False
    
    def get_status(self):
        """現在の状態を取得"""
        now = datetime.now()
        claude_running = self.is_claude_code_running()
        
        print("📊 簡単自動時間監視システム状態:")
        print(f"  ⏰ 現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  🖥️ Claude Code実行中: {claude_running}")
        print(f"  📅 最後実行時間: {self.last_execution_hour}時")
        print(f"  🎯 実行条件:")
        print(f"    - Claude実行中: {claude_running}")
        print(f"    - 現在の分: {now.minute} (0分で実行)")
        print(f"    - 今時間未実行: {now.hour != self.last_execution_hour}")
        
        return claude_running and now.minute == 0 and now.hour != self.last_execution_hour
    
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
    """メイン実行"""
    import sys
    
    monitor = SimpleAutoMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "check":
            # 一度だけチェックして実行
            monitor.run_once()
            
        elif command == "status":
            # 状態表示
            will_execute = monitor.get_status()
            if will_execute:
                print("🟢 実行条件満たしています")
            else:
                print("🔴 実行条件未満足")
                
        elif command == "test":
            # テスト実行
            print("🧪 テスト実行中...")
            success = monitor.execute_auto_organize_save()
            print(f"✅ テスト結果: {'成功' if success else '失敗'}")
            
        else:
            print("使用方法:")
            print("  python3 simple_auto_monitor.py check   - 条件チェック & 実行")
            print("  python3 simple_auto_monitor.py status  - 状態確認")
            print("  python3 simple_auto_monitor.py test    - テスト実行")
    else:
        # デフォルトはチェック実行
        monitor.run_once()

if __name__ == "__main__":
    main()