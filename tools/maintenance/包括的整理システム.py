#!/usr/bin/env python3
"""
包括的ファイル・フォルダ整理システム
名前の統一、統合、最終整理を実行
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import re

class ComprehensiveOrganizer:
    def __init__(self):
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.backup_path = self.root_path / "final_backup"
        
        # 統合対象フォルダのマッピング
        self.consolidation_plan = {
            # バックアップフォルダの統合
            "archive": {
                "target": "archive",
                "sources": [
                    "cleanup_archive",
                    "comprehensive_cleanup_backup", 
                    "consolidated_backups",
                    "quick_backup"
                ],
                "description": "全バックアップを統合"
            },
            
            # 自動バックアップの統合
            "auto_backups": {
                "target": "auto_backups",
                "sources": [
                    "important_backup_20250626_002550",
                    "important_backup_20250626_003055", 
                    "important_backup_20250626_003407"
                ],
                "description": "自動バックアップを統合"
            }
        }
        
        # ファイル名の改善マッピング
        self.rename_plan = {
            "AUTO_ORGANIZE_SAVE_USAGE_GUIDE.md": "docs/自動整理保存システム使用ガイド.md",
            "FOLDER_STRUCTURE_GUIDE.md": "docs/フォルダ構造ガイド.md",
            "PROJECT_CLEANUP_REPORT.md": "docs/プロジェクト整理レポート.md",
            "folder_organizer.py": "tools/フォルダ整理ツール.py",
            "comprehensive_organizer.py": "tools/包括的整理システム.py",
            "auto_hourly_monitor.py": "automation/毎時監視システム.py",
            "simple_auto_monitor.py": "automation/簡単監視システム.py",
            "setup_auto_hourly.py": "automation/自動実行セットアップ.py",
            "start_auto_monitor.py": "automation/監視システム起動.py",
            "project_cleanup_organizer.py": "tools/プロジェクト整理.py",
            "quick_cleanup.py": "tools/クイック整理.py"
        }
        
    def analyze_current_structure(self):
        """現在の構造を分析"""
        print("🔍 現在のファイル・フォルダ構造分析中...")
        
        analysis = {
            "backup_folders": [],
            "duplicate_files": [],
            "long_names": [],
            "consolidatable": {},
            "total_size": 0
        }
        
        # バックアップフォルダ検出
        for item in self.root_path.iterdir():
            if item.is_dir():
                name = item.name.lower()
                if any(keyword in name for keyword in ['backup', 'archive', 'cleanup']):
                    analysis["backup_folders"].append(str(item.name))
                    
                # 長い名前のフォルダ
                if len(item.name) > 30:
                    analysis["long_names"].append(str(item.name))
        
        # 類似ファイル検出
        similar_patterns = {
            "auto_execution_log": r"auto_execution_log_\d+_\d+\.json",
            "monitor_scripts": r".*monitor.*\.py",
            "cleanup_scripts": r".*cleanup.*\.py"
        }
        
        for pattern_name, pattern in similar_patterns.items():
            matches = []
            for file_path in self.root_path.rglob("*"):
                if file_path.is_file() and re.match(pattern, file_path.name):
                    matches.append(str(file_path.relative_to(self.root_path)))
            if len(matches) > 1:
                analysis["consolidatable"][pattern_name] = matches
        
        return analysis
    
    def create_organization_plan(self):
        """整理プランを作成"""
        analysis = self.analyze_current_structure()
        
        plan = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "actions": []
        }
        
        # フォルダ統合プラン
        for group_name, group_info in self.consolidation_plan.items():
            existing_sources = [s for s in group_info["sources"] 
                             if (self.root_path / s).exists()]
            if len(existing_sources) > 1:
                plan["actions"].append({
                    "type": "consolidate_folders",
                    "group": group_name,
                    "target": group_info["target"],
                    "sources": existing_sources,
                    "description": group_info["description"]
                })
        
        # ファイル移動・リネームプラン
        for old_name, new_path in self.rename_plan.items():
            old_file = self.root_path / old_name
            if old_file.exists():
                plan["actions"].append({
                    "type": "move_rename",
                    "source": old_name,
                    "target": new_path,
                    "description": f"{old_name} を {new_path} に移動・リネーム"
                })
        
        # ログファイル整理プラン
        log_files = list(self.root_path.glob("auto_execution_log_*.json"))
        if len(log_files) > 3:
            # 最新3つを残して古いものを logs/ に移動
            log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for log_file in log_files[3:]:
                plan["actions"].append({
                    "type": "archive_log",
                    "source": log_file.name,
                    "target": f"logs/{log_file.name}",
                    "description": f"古いログファイル {log_file.name} をアーカイブ"
                })
        
        return plan
    
    def execute_consolidation(self, plan):
        """統合プランを実行"""
        print("🔄 フォルダ・ファイル統合実行中...")
        
        results = []
        
        for action in plan["actions"]:
            try:
                if action["type"] == "consolidate_folders":
                    result = self._consolidate_folders(action)
                elif action["type"] == "move_rename":
                    result = self._move_rename_file(action)
                elif action["type"] == "archive_log":
                    result = self._archive_log_file(action)
                else:
                    result = {"success": False, "error": f"Unknown action type: {action['type']}"}
                
                results.append({
                    "action": action,
                    "result": result
                })
                
                if result["success"]:
                    print(f"✅ {action['description']}")
                else:
                    print(f"❌ {action['description']}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ {action['description']}: {str(e)}")
                results.append({
                    "action": action,
                    "result": {"success": False, "error": str(e)}
                })
        
        return results
    
    def _consolidate_folders(self, action):
        """フォルダ統合実行"""
        target_path = self.root_path / action["target"]
        target_path.mkdir(exist_ok=True)
        
        consolidated_count = 0
        
        for source_name in action["sources"]:
            source_path = self.root_path / source_name
            if source_path.exists() and source_path != target_path:
                try:
                    # 内容を移動
                    target_subdir = target_path / source_name
                    shutil.move(str(source_path), str(target_subdir))
                    consolidated_count += 1
                except Exception as e:
                    return {"success": False, "error": f"Failed to move {source_name}: {str(e)}"}
        
        return {"success": True, "consolidated_folders": consolidated_count}
    
    def _move_rename_file(self, action):
        """ファイル移動・リネーム実行"""
        source_path = self.root_path / action["source"]
        target_path = self.root_path / action["target"]
        
        # ターゲットディレクトリを作成
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(source_path), str(target_path))
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _archive_log_file(self, action):
        """ログファイルアーカイブ実行"""
        source_path = self.root_path / action["source"]
        target_path = self.root_path / action["target"]
        
        # ログディレクトリを作成
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(source_path), str(target_path))
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_new_structure_guide(self):
        """新しい構造ガイドを作成"""
        guide_content = f"""# 📁 整理済みプロジェクト構造ガイド
生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 メインフォルダ

### 📚 研究関連
```
study/                      # 研究メインフォルダ
├── 論文・資料
├── 実験・分析
└── 議論記録
```

### 🌐 Webサイト
```
public/                     # 公開サイト
├── index.html              # 研究プロジェクト
├── main-system/            # 画像分類システム
└── discussion-site/        # ディスカッション記録
```

### 🤖 システム実装
```
system/                     # 研究システム実装
└── implementations/        # 8つの実装システム
```

### 🛠️ 自動化ツール
```
automation/                 # 自動化システム
├── 毎時監視システム.py
├── 簡単監視システム.py
├── 自動実行セットアップ.py
└── 監視システム起動.py
```

### 🔧 開発ツール
```
tools/                      # 開発・整理ツール
├── フォルダ整理ツール.py
├── 包括的整理システム.py
├── プロジェクト整理.py
└── クイック整理.py
```

### 📖 ドキュメント
```
docs/                       # ドキュメント
├── 自動整理保存システム使用ガイド.md
├── フォルダ構造ガイド.md
└── プロジェクト整理レポート.md
```

### 📋 記録・ログ
```
sessions/                   # セッション記録
logs/                       # ログファイル
archive/                    # アーカイブ
auto_backups/              # 自動バックアップ
```

## 🔄 メンテナンス

### 定期実行推奨
```bash
# 自動整理・保存（毎時0分に自動実行済み）
python3 auto_organize_and_save.py

# フォルダ構造分析
python3 tools/フォルダ整理ツール.py analyze
```

### 手動整理
```bash
# 包括的整理
python3 tools/包括的整理システム.py execute

# クイック整理
python3 tools/クイック整理.py
```

整理完了！分かりやすく統合されたプロジェクト構造です。
"""
        
        guide_path = self.root_path / "docs" / "整理済み構造ガイド.md"
        guide_path.parent.mkdir(exist_ok=True)
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return guide_path

def main():
    """メイン実行"""
    import sys
    
    organizer = ComprehensiveOrganizer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "analyze":
            analysis = organizer.analyze_current_structure()
            print("📊 構造分析結果:")
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
            
        elif command == "plan":
            plan = organizer.create_organization_plan()
            print("📋 整理プラン:")
            for action in plan["actions"]:
                print(f"  - {action['description']}")
            
        elif command == "execute":
            print("🚀 包括的整理実行中...")
            plan = organizer.create_organization_plan()
            results = organizer.execute_consolidation(plan)
            
            success_count = sum(1 for r in results if r["result"]["success"])
            total_count = len(results)
            
            print(f"\n📊 実行結果: {success_count}/{total_count} 成功")
            
            # 新しい構造ガイド作成
            guide_path = organizer.create_new_structure_guide()
            print(f"📚 新しい構造ガイド作成: {guide_path}")
            
        else:
            print("使用方法:")
            print("  python3 comprehensive_organizer.py analyze  - 構造分析")
            print("  python3 comprehensive_organizer.py plan     - 整理プラン表示") 
            print("  python3 comprehensive_organizer.py execute  - 整理実行")
    else:
        print("🔧 包括的ファイル・フォルダ整理システム")
        print("使用方法:")
        print("  python3 comprehensive_organizer.py execute  - 整理実行")

if __name__ == "__main__":
    main()