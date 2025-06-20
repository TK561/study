#!/usr/bin/env python3
"""
ファイル整理機能のテスト
"""

import os
import tempfile
from pathlib import Path
from hourly_summary_system import HourlySummarySystem

def test_file_cleanup():
    """ファイル整理機能をテスト"""
    print("🧹 ファイル整理機能テスト開始")
    
    # テスト用一時ファイルを作成
    temp_files = []
    project_root = Path("/mnt/c/Desktop/Research")
    
    try:
        # テスト用ファイル作成
        test_temp = project_root / "test.tmp"
        test_temp.write_text("test temporary file")
        temp_files.append(test_temp)
        
        test_bak = project_root / "test.bak"
        test_bak.write_text("test backup file")
        temp_files.append(test_bak)
        
        print(f"テスト用一時ファイルを作成: {len(temp_files)}個")
        
        # システム初期化
        system = HourlySummarySystem()
        
        # ファイル整理実行
        cleanup_results = system.perform_file_cleanup()
        
        # 結果表示
        print("\n🧹 整理結果:")
        print(f"削除されたファイル: {len(cleanup_results['deleted_files'])}個")
        print(f"エラー: {len(cleanup_results['errors'])}件")
        
        if cleanup_results['deleted_files']:
            print("削除されたファイル:")
            for file in cleanup_results['deleted_files'][:5]:  # 最初の5個だけ表示
                print(f"  - {file}")
        
        if cleanup_results['errors']:
            print("エラー:")
            for error in cleanup_results['errors']:
                print(f"  - {error}")
        
        print("\n✅ ファイル整理テスト完了")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
    
    finally:
        # 残っているテストファイルをクリーンアップ
        for temp_file in temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except:
                pass

if __name__ == "__main__":
    test_file_cleanup()