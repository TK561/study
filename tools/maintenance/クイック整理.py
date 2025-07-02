#!/usr/bin/env python3
"""
クイック整理システム - 重要でないファイルのみ素早く整理
"""

import shutil
from pathlib import Path
from datetime import datetime

def quick_cleanup():
    """重要でないファイルを素早く整理"""
    root = Path("/mnt/c/Desktop/Research")
    backup = root / "quick_backup"
    backup.mkdir(exist_ok=True)
    
    # 削除対象（実装完了済みの一時ファイル）
    temp_files = [
        "auto_cleanup.py",
        "auto_update_system.py", 
        "cleanup_plan.py",
        "comprehensive_cleanup.py",
        "enhanced_pptx_analyzer.py",
        "gemini_integration.py",
        "pptx_reader.py",
        "session_save_protocol.py",
        "setup_auto_update.py",
        "simple_pptx_analyzer.py"
    ]
    
    # 削除対象ディレクトリ（分析完了済み）
    temp_dirs = [
        "system/pptx_analysis"  # 実装完了済み
    ]
    
    deleted_items = []
    
    print("🧹 クイック整理開始...")
    
    # 一時ファイル削除
    for file_name in temp_files:
        file_path = root / file_name
        if file_path.exists():
            # バックアップ
            shutil.copy2(file_path, backup / file_name)
            # 削除
            file_path.unlink()
            deleted_items.append(file_name)
            print(f"  ✅ 削除: {file_name}")
    
    # 一時ディレクトリ削除
    for dir_name in temp_dirs:
        dir_path = root / dir_name
        if dir_path.exists():
            # バックアップ
            backup_dir = backup / dir_name
            backup_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dir_path, backup_dir)
            # 削除
            shutil.rmtree(dir_path)
            deleted_items.append(dir_name)
            print(f"  ✅ 削除: {dir_name}")
    
    # 重複分析フォルダ削除
    ai_analysis = root / "ai_analysis"
    if ai_analysis.exists():
        shutil.copytree(ai_analysis, backup / "ai_analysis")
        shutil.rmtree(ai_analysis)
        deleted_items.append("ai_analysis")
        print(f"  ✅ 削除: ai_analysis")
    
    print(f"\n✅ クイック整理完了")
    print(f"📦 削除アイテム: {len(deleted_items)}件")
    print(f"💾 バックアップ: {backup}")
    
    # 現在の重要ファイル確認
    important_files = [
        "CLAUDE.md",
        "README.md", 
        "WordNet-Based_Semantic_Image_Classification_Research_Presentation.pptx",
        "system/implementations/integrated_research_system.py",
        "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
    ]
    
    print(f"\n📋 重要ファイル確認:")
    for file_name in important_files:
        file_path = root / file_name
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file_name}")
    
    return deleted_items

if __name__ == "__main__":
    quick_cleanup()