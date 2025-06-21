#!/usr/bin/env python3
"""
Test Safe Shutdown Functionality

Generated with Claude Code
Date: 2025-06-20
Purpose: 安全停止機能のテスト用スクリプト
"""

import subprocess
import time
import signal
import os
from pathlib import Path

def test_normal_shutdown():
    """正常終了のテスト"""
    print(" Testing normal shutdown (SIGTERM)...")
    
    # システム起動
    process = subprocess.Popen([
        'python3', 
        'scripts/simple_hourly_system.py',
        '--project-root', str(Path.cwd())
    ])
    
    # 5秒待機
    time.sleep(5)
    
    # SIGTERM送信
    process.terminate()
    
    # 終了待機
    process.wait()
    
    print(" Normal shutdown test completed")

def test_force_shutdown():
    """強制終了のテスト"""
    print(" Testing force shutdown (SIGKILL simulation)...")
    
    # システム起動
    process = subprocess.Popen([
        'python3', 
        'scripts/simple_hourly_system.py',
        '--project-root', str(Path.cwd())
    ])
    
    # 3秒待機
    time.sleep(3)
    
    # 強制終了（シグナルキャッチ不可）
    process.kill()
    
    # 終了待機
    process.wait()
    
    print(" Force shutdown test completed")
    print(" This should create an unexpected termination")

def check_recovery():
    """復旧機能のテスト"""
    print(" Testing recovery functionality...")
    
    # 次回起動時に復旧処理が動作するかテスト
    result = subprocess.run([
        'python3', 
        'scripts/simple_hourly_system.py',
        '--once',
        '--project-root', str(Path.cwd())
    ], capture_output=True, text=True)
    
    if "Previous session ended unexpectedly" in result.stdout:
        print(" Recovery detection working")
    else:
        print(" Recovery not detected")
    
    if "Recovery cleanup completed" in result.stdout:
        print(" Recovery cleanup working")
    else:
        print(" Recovery cleanup not working")

def main():
    """メインテスト実行"""
    print(" Safe Shutdown Test Suite")
    print("=" * 40)
    
    try:
        # テスト1: 正常終了
        test_normal_shutdown()
        time.sleep(2)
        
        # テスト2: 強制終了
        test_force_shutdown()
        time.sleep(2)
        
        # テスト3: 復旧機能
        check_recovery()
        
        print("=" * 40)
        print(" All tests completed")
        
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
    except Exception as e:
        print(f" Test error: {e}")

if __name__ == "__main__":
    main()