#!/usr/bin/env python3
"""
毎時0分自動実行セットアップスクリプト
Cronジョブを設定して毎分チェック
"""

import subprocess
import sys
from pathlib import Path
import os

class AutoHourlySetup:
    def __init__(self):
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.monitor_script = self.root_path / "simple_auto_monitor.py"
        
    def setup_cron(self):
        """Cronジョブを設定"""
        try:
            # 現在のcrontabを取得
            try:
                result = subprocess.run(
                    ["crontab", "-l"],
                    capture_output=True,
                    text=True
                )
                current_cron = result.stdout if result.returncode == 0 else ""
            except:
                current_cron = ""
            
            # 自動実行ジョブ
            cron_job = f"* * * * * cd {self.root_path} && python3 simple_auto_monitor.py check >> /tmp/auto_monitor.log 2>&1"
            
            # 既に設定済みかチェック
            if "simple_auto_monitor.py" in current_cron:
                print("✅ Cronジョブは既に設定済みです")
                return True
            
            # 新しいcrontabを作成
            new_cron = current_cron.strip()
            if new_cron:
                new_cron += "\n"
            new_cron += cron_job + "\n"
            
            # crontabを設定
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(input=new_cron)
            
            if process.returncode == 0:
                print("✅ Cronジョブ設定完了")
                print(f"📋 設定内容: 毎分チェック、毎時0分に自動実行")
                print(f"📄 ログファイル: /tmp/auto_monitor.log")
                return True
            else:
                print("❌ Cronジョブ設定失敗")
                return False
                
        except Exception as e:
            print(f"❌ Cronセットアップエラー: {e}")
            return False
    
    def remove_cron(self):
        """Cronジョブを削除"""
        try:
            # 現在のcrontabを取得
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("❌ 現在のcrontabを取得できません")
                return False
            
            current_cron = result.stdout
            
            # 自動実行ジョブを除外
            lines = current_cron.split('\n')
            new_lines = [line for line in lines if "simple_auto_monitor.py" not in line]
            new_cron = '\n'.join(new_lines)
            
            # crontabを更新
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(input=new_cron)
            
            if process.returncode == 0:
                print("✅ Cronジョブ削除完了")
                return True
            else:
                print("❌ Cronジョブ削除失敗")
                return False
                
        except Exception as e:
            print(f"❌ Cron削除エラー: {e}")
            return False
    
    def show_cron(self):
        """現在のCronジョブを表示"""
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("📋 現在のCronジョブ:")
                print(result.stdout)
            else:
                print("❌ Cronジョブが設定されていません")
                
        except Exception as e:
            print(f"❌ Cron表示エラー: {e}")
    
    def test_monitor(self):
        """監視システムをテスト"""
        try:
            print("🧪 監視システムテスト中...")
            
            result = subprocess.run(
                ["python3", "simple_auto_monitor.py", "status"],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            
            if result.returncode == 0:
                print("✅ 監視システム正常")
                return True
            else:
                print("❌ 監視システムエラー")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ テストエラー: {e}")
            return False

def main():
    """メイン実行"""
    setup = AutoHourlySetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "setup":
            print("🚀 毎時0分自動実行システムセットアップ中...")
            success = setup.setup_cron()
            if success:
                print("\n🎉 セットアップ完了！")
                print("📝 使用方法:")
                print("  - 毎分自動チェック（バックグラウンド）")
                print("  - 毎時0分かつClaude Code実行中に自動整理・保存実行")
                print("  - ログ確認: tail -f /tmp/auto_monitor.log")
            else:
                print("❌ セットアップ失敗")
                
        elif command == "remove":
            setup.remove_cron()
            
        elif command == "show":
            setup.show_cron()
            
        elif command == "test":
            setup.test_monitor()
            
        else:
            print("使用方法:")
            print("  python3 setup_auto_hourly.py setup   - セットアップ")
            print("  python3 setup_auto_hourly.py remove  - 削除")
            print("  python3 setup_auto_hourly.py show    - 表示")
            print("  python3 setup_auto_hourly.py test    - テスト")
    else:
        print("🔧 毎時0分自動実行システム")
        print("使用方法:")
        print("  python3 setup_auto_hourly.py setup   - セットアップ")
        print("  python3 setup_auto_hourly.py test    - テスト")

if __name__ == "__main__":
    main()