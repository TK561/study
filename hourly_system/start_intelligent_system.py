#!/usr/bin/env python3
"""
Start Intelligent Hourly System

Generated with Claude Code
Date: 2025-06-20
Purpose: 賢い1時間毎システムの簡単起動スクリプト
Usage: python3 start_intelligent_system.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    """メイン起動関数"""
    
    print(" Starting Intelligent Hourly System...")
    print("=" * 50)
    print(" Features:")
    print("  - 1時間毎のファイル整理")
    print("  - GitHub状態監視")
    print("  - レポート統合・保存")
    print("  - ターミナル簡易表示")
    print("  - ターミナル終了時自動停止")
    print("=" * 50)
    
    # スクリプトパス
    script_path = Path(__file__).parent / "scripts" / "intelligent_hourly_system.py"
    
    if not script_path.exists():
        print(f" Script not found: {script_path}")
        return 1
    
    try:
        # システム起動
        print(" Starting monitoring...")
        result = subprocess.run([
            sys.executable, 
            str(script_path),
            "--project-root", str(Path(__file__).parent)
        ])
        
        return result.returncode
    
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
        return 0
    except Exception as e:
        print(f" Error starting system: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())