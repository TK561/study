#!/usr/bin/env python3
"""
Start Simple Hourly System

Generated with Claude Code
Date: 2025-06-20
Purpose: シンプル1時間毎システムの起動スクリプト
"""

import subprocess
import sys
from pathlib import Path

def main():
    """シンプルシステム起動"""
    
    print(" Starting Simple Hourly System...")
    print("=" * 40)
    print(" Essential features only:")
    print("   1時間毎ファイル整理")
    print("   GitHub状態確認")
    print("   レポート統合・保存")
    print("   簡易ターミナル表示")
    print("   Claude Code終了時最終処理")
    print("=" * 40)
    
    script_path = Path(__file__).parent / "scripts" / "simple_hourly_system.py"
    
    if not script_path.exists():
        print(f" Script not found: {script_path}")
        return 1
    
    try:
        print(" Starting monitoring (Press Ctrl+C to stop)...")
        result = subprocess.run([
            sys.executable, 
            str(script_path),
            "--project-root", str(Path(__file__).parent)
        ])
        
        return result.returncode
    
    except KeyboardInterrupt:
        print("\n🛑 System stopped")
        return 0
    except Exception as e:
        print(f" Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())