#!/usr/bin/env python3
"""
通知機能のテスト
"""

import os
import subprocess
from datetime import datetime

def test_notification():
    """通知機能をテスト"""
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if os.name == 'nt':
            # Windows Toast Notification
            notification_title = "Claude Code 作業更新"
            notification_text = f"1時間毎のまとめが完了しました\\n時刻: {current_time}"
            
            ps_command = f'''
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.MessageBox]::Show("{notification_text}", "{notification_title}", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
            '''
            
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Windows通知テスト成功")
            else:
                print(f"❌ Windows通知エラー: {result.stderr}")
        
        # Console notification
        print("\\n" + "="*50)
        print("🔔 NOTIFICATION TEST")
        print("="*50)
        print(f"⏰ 時刻: {current_time}")
        print("📊 テスト通知が正常に動作しています")
        print("="*50)
        
        # Sound test
        try:
            if os.name == 'nt':
                import winsound
                winsound.Beep(800, 200)
                print("🔊 音声通知テスト完了")
        except ImportError:
            print("ℹ️ winsoundが利用できません")
            
    except Exception as e:
        print(f"❌ 通知テストエラー: {e}")

if __name__ == "__main__":
    test_notification()