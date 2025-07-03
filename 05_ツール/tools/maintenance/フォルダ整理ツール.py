#!/usr/bin/env python3
"""
フォルダ構造整理ツール
複雑になったフォルダを見やすく整理
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class FolderOrganizer:
    def __init__(self):
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.archive_path = self.root_path / "organized_archive"
        self.important_folders = {
            "study": "📚 研究メインフォルダ",
            "public": "🌐 Webサイト",
            "system/implementations": "🤖 実装システム",
            "sessions": "📋 セッション記録",
            "docs": "📖 ドキュメント", 
            "config": "⚙️ 設定"
        }
        
        self.cleanup_targets = [
            "cleanup_archive",
            "consolidated_backups", 
            "important_backup_*",
            "quick_backup",
            "auto_execution_log_*.json",
            "comprehensive_cleanup_backup"
        ]
        
    def analyze_structure(self):
        """現在のフォルダ構造を分析"""
        print("📊 フォルダ構造分析中...")
        
        analysis = {
            "total_folders": 0,
            "total_files": 0,
            "important_folders": {},
            "cleanup_targets": {},
            "large_folders": {}
        }
        
        for root, dirs, files in os.walk(self.root_path):
            rel_path = Path(root).relative_to(self.root_path)
            
            # 重要フォルダチェック
            for important_folder in self.important_folders:
                if str(rel_path).startswith(important_folder):
                    analysis["important_folders"][str(rel_path)] = len(files)
            
            # 大きなフォルダチェック  
            if len(files) > 10:
                analysis["large_folders"][str(rel_path)] = len(files)
                
            analysis["total_folders"] += len(dirs)
            analysis["total_files"] += len(files)
        
        return analysis
    
    def create_summary_report(self):
        """フォルダ構造サマリーレポート作成"""
        analysis = self.analyze_structure()
        
        report = f"""# 📁 フォルダ構造分析レポート
生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 基本統計
- 総フォルダ数: {analysis['total_folders']}
- 総ファイル数: {analysis['total_files']}

## ✅ 重要フォルダ（保持推奨）
"""
        
        for folder, description in self.important_folders.items():
            folder_path = self.root_path / folder
            if folder_path.exists():
                file_count = len(list(folder_path.rglob("*")))
                report += f"- **{folder}** {description}: {file_count}ファイル\n"
        
        report += "\n## 📦 大容量フォルダ（整理検討）\n"
        for folder, file_count in sorted(analysis['large_folders'].items(), 
                                       key=lambda x: x[1], reverse=True)[:10]:
            report += f"- {folder}: {file_count}ファイル\n"
        
        report += f"""
## 🗑️ 整理対象候補
以下のフォルダ・ファイルは整理対象です：
"""
        
        for target in self.cleanup_targets:
            matches = list(self.root_path.glob(target))
            if matches:
                report += f"- {target}: {len(matches)}件\n"
        
        report += f"""
## 🔧 推奨アクション
1. **自動整理実行**: `python3 auto_organize_and_save.py`
2. **手動確認**: 大容量フォルダの内容確認
3. **アーカイブ**: 古いバックアップの削除・移動

詳細は `FOLDER_STRUCTURE_GUIDE.md` を参照してください。
"""
        
        # レポート保存
        report_file = self.root_path / "FOLDER_ANALYSIS_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📋 分析レポート作成: {report_file}")
        return report_file
    
    def show_simple_tree(self, max_depth=2):
        """簡単なフォルダツリー表示"""
        print(f"📁 フォルダ構造（階層{max_depth}まで）:")
        print("=" * 50)
        
        def print_tree(path, prefix="", depth=0):
            if depth > max_depth:
                return
                
            items = sorted([p for p in path.iterdir() if p.is_dir()])
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                
                # 重要フォルダかチェック
                rel_path = item.relative_to(self.root_path)
                icon = ""
                for important_folder in self.important_folders:
                    if str(rel_path).startswith(important_folder):
                        icon = "⭐ "
                        break
                
                # ファイル数カウント
                try:
                    file_count = len([f for f in item.rglob("*") if f.is_file()])
                    if file_count > 20:
                        icon += "📦 "
                    elif file_count > 5:
                        icon += "📁 "
                except:
                    file_count = 0
                
                print(f"{prefix}{current_prefix}{icon}{item.name} ({file_count})")
                
                # 再帰
                if depth < max_depth:
                    extension = "    " if is_last else "│   "
                    print_tree(item, prefix + extension, depth + 1)
        
        print_tree(self.root_path)
        print("=" * 50)
        print("⭐ = 重要フォルダ, 📦 = 大容量(20+), 📁 = 中容量(5+)")
    
    def quick_cleanup_suggestions(self):
        """クイック整理提案"""
        print("\n🧹 クイック整理提案:")
        
        suggestions = []
        
        # バックアップフォルダチェック
        backup_folders = list(self.root_path.glob("*backup*"))
        if len(backup_folders) > 3:
            suggestions.append(f"💾 バックアップフォルダが{len(backup_folders)}個あります - 統合推奨")
        
        # 実行ログチェック
        log_files = list(self.root_path.glob("auto_execution_log_*.json"))
        if len(log_files) > 5:
            suggestions.append(f"📄 実行ログが{len(log_files)}個あります - 古いログ削除推奨")
        
        # アーカイブフォルダチェック
        archive_folders = list(self.root_path.glob("*archive*"))
        if len(archive_folders) > 2:
            suggestions.append(f"📦 アーカイブフォルダが{len(archive_folders)}個あります - 統合推奨")
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
            print(f"\n✨ 実行: python3 auto_organize_and_save.py")
        else:
            print("  ✅ フォルダ構造は比較的整理されています")

def main():
    """メイン実行"""
    import sys
    
    organizer = FolderOrganizer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "analyze":
            organizer.create_summary_report()
            
        elif command == "tree":
            depth = int(sys.argv[2]) if len(sys.argv) > 2 else 2
            organizer.show_simple_tree(depth)
            
        elif command == "suggest":
            organizer.quick_cleanup_suggestions()
            
        elif command == "full":
            print("🔍 完全分析実行中...")
            organizer.show_simple_tree(2)
            organizer.quick_cleanup_suggestions()
            organizer.create_summary_report()
            
        else:
            print("使用方法:")
            print("  python3 folder_organizer.py analyze  - 分析レポート作成")
            print("  python3 folder_organizer.py tree [depth] - ツリー表示")
            print("  python3 folder_organizer.py suggest - 整理提案")
            print("  python3 folder_organizer.py full    - 完全分析")
    else:
        # デフォルトは簡単な表示
        organizer.show_simple_tree(2)
        organizer.quick_cleanup_suggestions()

if __name__ == "__main__":
    main()