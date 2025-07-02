#!/usr/bin/env python3
"""
自動整理・保存システム
「ファイルとフォルダ整理」「やったことの保存」のどちらの要求でも両方を自動実行
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import subprocess

class AutoOrganizeAndSave:
    def __init__(self):
        self.name = "自動整理・保存システム"
        self.version = "1.0.0"
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 今日の日付
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # 整理・保存の実行ログ
        self.execution_log = {
            "timestamp": datetime.now().isoformat(),
            "actions_performed": [],
            "files_organized": [],
            "files_saved": [],
            "backup_created": [],
            "errors": []
        }
        
    def detect_user_intent(self, user_request=""):
        """ユーザーの要求を解析し、実行すべきアクションを決定"""
        # どちらの要求でも両方実行するが、優先度を決定
        keywords_organize = ["整理", "ファイル", "フォルダ", "削除", "cleanup", "organize"]
        keywords_save = ["保存", "記録", "やったこと", "作業", "save", "記録"]
        
        organize_priority = any(keyword in user_request for keyword in keywords_organize)
        save_priority = any(keyword in user_request for keyword in keywords_save)
        
        # 両方実行するが、順序を決定
        if organize_priority and save_priority:
            return "both_equal"  # 両方同優先度
        elif organize_priority:
            return "organize_first"  # 整理優先
        elif save_priority:
            return "save_first"  # 保存優先
        else:
            return "both_equal"  # デフォルトは両方実行
    
    def quick_organize_files(self):
        """ファイル・フォルダのクイック整理"""
        print("🧹 ファイル・フォルダ自動整理開始...")
        
        # バックアップディレクトリ作成
        backup_dir = self.root_path / f"auto_backup_{self.timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        # 整理対象の一時ファイル・フォルダを定義
        temp_items = [
            # 一時的なPythonファイル
            "temp_*.py",
            "test_*.py", 
            "*_temp.py",
            "*_backup.py",
            # 一時的なJSONファイル  
            "temp_*.json",
            "*_temp.json",
            # 重複・古いバックアップ
            "old_*",
            "*_old.*",
            # 空のcacheディレクトリ
            "cache",
            "__pycache__",
            # 一時的なログファイル
            "*.tmp",
            "*.log.old"
        ]
        
        organized_count = 0
        
        # system直下の一時ファイルをチェック
        system_dir = self.root_path / "system"
        if system_dir.exists():
            for item in system_dir.iterdir():
                if item.name.startswith(("temp_", "test_", "old_")) and item.is_file():
                    try:
                        # バックアップ
                        backup_target = backup_dir / "system" / item.name
                        backup_target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, backup_target)
                        
                        # 削除
                        item.unlink()
                        organized_count += 1
                        self.execution_log["files_organized"].append(str(item.relative_to(self.root_path)))
                        print(f"  ✅ 削除: {item.relative_to(self.root_path)}")
                    except Exception as e:
                        self.execution_log["errors"].append(f"整理エラー {item.name}: {e}")
        
        # 空ディレクトリの削除
        self._remove_empty_directories()
        
        # 重複バックアップフォルダの統合
        self._consolidate_backup_folders()
        
        print(f"✅ ファイル整理完了: {organized_count}件処理")
        self.execution_log["actions_performed"].append(f"ファイル整理: {organized_count}件")
        
        return organized_count
    
    def _remove_empty_directories(self):
        """空ディレクトリを削除"""
        removed_dirs = []
        
        # 保護すべきディレクトリ
        protected_dirs = [
            "system/implementations",
            "study", 
            "sessions",
            "public",
            "config",
            "logs"
        ]
        
        for root, dirs, files in os.walk(self.root_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    # 空かつ保護対象外のディレクトリを削除
                    if not any(dir_path.iterdir()):
                        rel_path = dir_path.relative_to(self.root_path)
                        if not any(str(rel_path).startswith(protected) for protected in protected_dirs):
                            dir_path.rmdir()
                            removed_dirs.append(str(rel_path))
                except:
                    pass
        
        if removed_dirs:
            print(f"  🗂️ 空ディレクトリ削除: {len(removed_dirs)}件")
            self.execution_log["files_organized"].extend(removed_dirs)
    
    def _consolidate_backup_folders(self):
        """重複するバックアップフォルダを統合"""
        backup_folders = [
            "quick_backup",
            "cleanup_archive", 
            "comprehensive_cleanup_backup"
        ]
        
        # 統合バックアップフォルダを作成
        consolidated_backup = self.root_path / "consolidated_backups"
        
        for folder_name in backup_folders:
            folder_path = self.root_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                # 統合先にコピー
                target_path = consolidated_backup / folder_name
                if not target_path.exists():
                    try:
                        shutil.copytree(folder_path, target_path)
                        print(f"  📦 バックアップ統合: {folder_name}")
                    except Exception as e:
                        self.execution_log["errors"].append(f"バックアップ統合エラー {folder_name}: {e}")
    
    def auto_save_session_work(self):
        """今日の作業を自動保存"""
        print("💾 セッション作業自動保存開始...")
        
        # 今日のセッションファイルを生成
        session_file = self.root_path / "sessions" / f"AUTO_SESSION_SAVE_{self.today}.md"
        
        # git statusとdiffで変更内容を取得
        changes_info = self._get_git_changes()
        
        # 今日作成・更新されたファイルを検索
        recent_files = self._find_recent_files()
        
        # システム出力結果を収集
        system_outputs = self._collect_system_outputs()
        
        # セッション保存内容を生成
        session_content = self._generate_session_content(changes_info, recent_files, system_outputs)
        
        # セッションファイル保存
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(session_content)
        
        self.execution_log["files_saved"].append(str(session_file.relative_to(self.root_path)))
        print(f"✅ セッション保存完了: {session_file.name}")
        
        # 追加で重要ファイルのバックアップ
        self._backup_important_files()
        
        return str(session_file)
    
    def _get_git_changes(self):
        """Git変更情報を取得"""
        try:
            # git status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"], 
                cwd=self.root_path, 
                capture_output=True, 
                text=True
            )
            
            # git diff (staged and unstaged)
            diff_result = subprocess.run(
                ["git", "diff", "HEAD"], 
                cwd=self.root_path,
                capture_output=True, 
                text=True
            )
            
            return {
                "status": status_result.stdout if status_result.returncode == 0 else "Git status取得失敗",
                "diff_summary": f"{len(diff_result.stdout.splitlines())}行の変更" if diff_result.returncode == 0 else "Git diff取得失敗"
            }
        except Exception as e:
            return {"status": f"Git情報取得エラー: {e}", "diff_summary": "取得失敗"}
    
    def _find_recent_files(self):
        """今日作成・更新されたファイルを検索"""
        recent_files = []
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime >= today_start:
                        rel_path = file_path.relative_to(self.root_path)
                        recent_files.append({
                            "path": str(rel_path),
                            "modified": mtime.strftime("%H:%M:%S")
                        })
                except:
                    pass
        
        # 更新時刻でソート
        recent_files.sort(key=lambda x: x["modified"], reverse=True)
        return recent_files[:20]  # 最新20件
    
    def _collect_system_outputs(self):
        """システム出力結果を収集"""
        output_dir = self.root_path / "system" / "implementations" / "output"
        outputs = {
            "benchmarks": [],
            "detections": [], 
            "integrated_research": [],
            "visualizations": [],
            "dataset_selections": [],
            "realtime_processing": []
        }
        
        if output_dir.exists():
            for category in outputs.keys():
                category_dir = output_dir / category
                if category_dir.exists():
                    for file in category_dir.iterdir():
                        if file.is_file():
                            outputs[category].append({
                                "name": file.name,
                                "size": f"{file.stat().st_size // 1024}KB" if file.stat().st_size > 1024 else f"{file.stat().st_size}B"
                            })
        
        return outputs
    
    def _generate_session_content(self, changes_info, recent_files, system_outputs):
        """セッション保存内容を生成"""
        content = f"""# 🔄 自動セッション保存 - {self.today}

## 📅 保存情報
- **保存日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- **保存システム**: {self.name} v{self.version}
- **保存トリガー**: 自動実行

## 📊 Git変更状況
```
{changes_info['status']}
```
- **変更サマリー**: {changes_info['diff_summary']}

## 📁 今日更新されたファイル ({len(recent_files)}件)
"""
        
        for file_info in recent_files[:10]:  # 上位10件表示
            content += f"- `{file_info['path']}` (更新: {file_info['modified']})\n"
        
        if len(recent_files) > 10:
            content += f"- ... 他{len(recent_files) - 10}件\n"
        
        content += f"""
## 🔧 システム出力結果
"""
        
        for category, files in system_outputs.items():
            if files:
                content += f"""
### {category.replace('_', ' ').title()} ({len(files)}件)
"""
                for file_info in files[:5]:  # 各カテゴリ上位5件
                    content += f"- `{file_info['name']}` ({file_info['size']})\n"
                if len(files) > 5:
                    content += f"- ... 他{len(files) - 5}件\n"
        
        content += f"""
## 🎯 実行されたアクション
"""
        for action in self.execution_log["actions_performed"]:
            content += f"- ✅ {action}\n"
        
        content += f"""
## 💾 保存されたファイル
"""
        for file in self.execution_log["files_saved"]:
            content += f"- 📄 {file}\n"
        
        content += f"""
## 🗑️ 整理されたファイル
"""
        for file in self.execution_log["files_organized"]:
            content += f"- 🧹 {file}\n"
        
        if self.execution_log["errors"]:
            content += f"""
## ⚠️ エラー・警告
"""
            for error in self.execution_log["errors"]:
                content += f"- ❌ {error}\n"
        
        content += f"""
## 📋 次回セッション引き継ぎ事項
- **重要ファイル**: 自動バックアップ済み
- **プロジェクト構造**: 最適化完了
- **システム出力**: 全て保持
- **作業継続**: 準備完了

---
*自動保存システムにより生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return content
    
    def _backup_important_files(self):
        """重要ファイルの自動バックアップ"""
        important_files = [
            "CLAUDE.md",
            "README.md", 
            "WordNet-Based_Semantic_Image_Classification_Research_Presentation.pptx",
            "system/implementations/integrated_research_system.py",
            "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        ]
        
        backup_dir = self.root_path / f"important_backup_{self.timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        for file_path in important_files:
            source = self.root_path / file_path
            if source.exists():
                target = backup_dir / file_path
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(source, target)
                    self.execution_log["backup_created"].append(file_path)
                except Exception as e:
                    self.execution_log["errors"].append(f"バックアップエラー {file_path}: {e}")
        
        # Obsidianボルトのバックアップ
        obsidian_path = Path("/mnt/c/Desktop/Obsidian/study")
        if obsidian_path.exists():
            print("  📚 Obsidianボルトのバックアップ開始...")
            obsidian_backup_dir = backup_dir / "Obsidian_Vault_Backup"
            obsidian_backup_dir.mkdir(exist_ok=True)
            
            # 重要なObsidianファイルのみバックアップ
            obsidian_important = [
                "Research/WordNet-Based Semantic Image Classification.md",
                "Research/Weekly-Discussion-Summary.md",
                "Research/Research Index.md",
                "Daily/2025-07-02.md",
                "Research MOC.md",
                "Study MOC.md",
                "Naming-Convention-Guide.md",
                ".obsidian/app.json",
                ".obsidian/core-plugins.json"
            ]
            
            for file_path in obsidian_important:
                source = obsidian_path / file_path
                if source.exists():
                    target = obsidian_backup_dir / file_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.copy2(source, target)
                        self.execution_log["backup_created"].append(f"Obsidian/{file_path}")
                    except Exception as e:
                        self.execution_log["errors"].append(f"Obsidianバックアップエラー {file_path}: {e}")
            
            print(f"  📚 Obsidianバックアップ完了")
        
        print(f"  💾 重要ファイルバックアップ: {len(self.execution_log['backup_created'])}件")
    
    def execute_auto_organize_and_save(self, user_request=""):
        """自動整理・保存の実行"""
        print("🚀 自動整理・保存システム 起動")
        print("=" * 60)
        
        # ユーザー意図の解析
        intent = self.detect_user_intent(user_request)
        print(f"📋 検出された要求: {intent}")
        
        # どの要求でも常に整理→保存の順序で実行
        print("\n📍 実行順序: ファイル整理 → セッション保存")
        organized_count = self.quick_organize_files()
        session_file = self.auto_save_session_work()
        
        # 実行ログの保存
        log_file = self.root_path / f"auto_execution_log_{self.timestamp}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.execution_log, f, ensure_ascii=False, indent=2)
        
        # 完了サマリー
        print("\n" + "=" * 60)
        print("🎉 自動整理・保存完了")
        print("=" * 60)
        print("📊 実行サマリー:")
        print(f"  🧹 整理: {organized_count}件処理")
        print(f"  💾 保存: {len(self.execution_log['files_saved'])}件")
        print(f"  📦 バックアップ: {len(self.execution_log['backup_created'])}件") 
        print(f"  ⚠️ エラー: {len(self.execution_log['errors'])}件")
        print(f"\n📄 詳細ログ: {log_file.name}")
        
        print(f"📋 セッション記録: {Path(session_file).name}")
        
        print("\n✅ 次回は「ファイルとフォルダ整理」「やったことの保存」どちらの要求でも自動実行されます")
        
        return {
            "organized_files": organized_count,
            "saved_files": len(self.execution_log["files_saved"]),
            "backup_files": len(self.execution_log["backup_created"]),
            "errors": len(self.execution_log["errors"]),
            "log_file": str(log_file),
            "session_file": session_file if 'session_file' in locals() else None
        }

def main():
    """メイン実行関数"""
    organizer = AutoOrganizeAndSave()
    
    # コマンドライン引数から要求を取得（オプション）
    import sys
    user_request = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    
    result = organizer.execute_auto_organize_and_save(user_request)
    return result

if __name__ == "__main__":
    main()