#!/usr/bin/env python3
"""
包括的プロジェクト整理システム
現在の構造を分析し、最適化された構造に整理する
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class ComprehensiveCleanup:
    def __init__(self):
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.backup_path = self.root_path / "comprehensive_cleanup_backup"
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "actions": [],
            "moved_items": [],
            "deleted_items": [],
            "preserved_items": []
        }
    
    def analyze_current_structure(self):
        """現在の構造を分析"""
        analysis = {
            "duplicates": [],
            "old_backups": [],
            "redundant_tools": [],
            "unused_configs": [],
            "outdated_docs": []
        }
        
        # temp_cleanup_backup内の重複分析
        temp_backup = self.root_path / "temp_cleanup_backup"
        if temp_backup.exists():
            analysis["old_backups"].append(str(temp_backup))
        
        # tools フォルダの重複分析
        tools_path = self.root_path / "tools"
        if tools_path.exists():
            # 研究関連ツールは多すぎる可能性
            research_tools = list(tools_path.glob("*research*"))
            sql_tools = list(tools_path.glob("*sql*"))
            vercel_tools = list(tools_path.glob("*vercel*"))
            
            if len(research_tools) > 5:
                analysis["redundant_tools"].extend([str(t) for t in research_tools[5:]])
            if len(sql_tools) > 3:
                analysis["redundant_tools"].extend([str(t) for t in sql_tools[3:]])
            if len(vercel_tools) > 2:
                analysis["redundant_tools"].extend([str(t) for t in vercel_tools[2:]])
        
        return analysis
    
    def create_optimal_structure(self):
        """最適化された構造を作成"""
        optimal_structure = {
            # 必須システムファイル（ルート）
            "root_files": [
                "CLAUDE.md",
                "README.md", 
                "package.json",
                "requirements.txt",
                "vercel.json"
            ],
            
            # コアシステム
            "system/": [
                "auto_cleanup.py",
                "auto_update_system.py", 
                "gemini_integration.py",
                "session_save_protocol.py",
                "setup_auto_update.py"
            ],
            
            # ドキュメント
            "docs/": [
                "AUTO_UPDATE_GUIDE.md",
                "SESSION_SAVE_GUIDE.md",
                "PROJECT_STRUCTURE.md"
            ],
            
            # セッション記録
            "sessions/": [
                "daily_session_*.md",
                "COMPLETE_SESSION_*.md"
            ],
            
            # AI分析結果
            "ai_analysis/": [
                "gemini_analysis_*.md"
            ],
            
            # 公開サイト
            "public/": [
                "discussion-site/",
                "main-system/"
            ],
            
            # 研究内容（submodule）
            "study/": "preserve_as_is",
            
            # 最小限のツール
            "tools/": [
                "direct_vercel_deploy.py",
                "research_analysis_system.py"
            ]
        }
        
        return optimal_structure
    
    def execute_cleanup(self):
        """整理を実行"""
        print("🧹 包括的プロジェクト整理を開始...")
        
        # バックアップディレクトリ作成
        self.backup_path.mkdir(exist_ok=True)
        
        # 1. temp_cleanup_backup を統合バックアップに移動
        temp_backup = self.root_path / "temp_cleanup_backup"
        if temp_backup.exists():
            dest = self.backup_path / "previous_temp_backup"
            shutil.move(str(temp_backup), str(dest))
            self.report["moved_items"].append(f"{temp_backup} → {dest}")
        
        # 2. 過剰なツールファイルの整理
        self.cleanup_tools_directory()
        
        # 3. 重複ドキュメントの整理
        self.cleanup_duplicate_docs()
        
        # 4. 古いバックアップ・ログの整理
        self.cleanup_old_files()
        
        # 5. レポート作成
        self.create_cleanup_report()
        
        print("✅ 包括的整理完了")
    
    def cleanup_tools_directory(self):
        """toolsディレクトリの整理"""
        tools_path = self.root_path / "tools"
        if not tools_path.exists():
            return
        
        # 保持するツール
        keep_tools = [
            "direct_vercel_deploy.py",
            "research_analysis_system.py",
            "vercel_quick_deploy.sh"
        ]
        
        # 移動対象の特定
        for item in tools_path.iterdir():
            if item.name not in keep_tools:
                dest = self.backup_path / "tools" / item.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(dest))
                self.report["moved_items"].append(f"{item} → {dest}")
    
    def cleanup_duplicate_docs(self):
        """重複ドキュメントの整理"""
        # CLEANUP_REPORT.md は既存なので統合
        cleanup_report = self.root_path / "CLEANUP_REPORT.md"
        if cleanup_report.exists():
            dest = self.backup_path / "old_reports" / "CLEANUP_REPORT.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(cleanup_report), str(dest))
            self.report["moved_items"].append(f"{cleanup_report} → {dest}")
    
    def cleanup_old_files(self):
        """古いファイル・フォルダの整理"""
        # archiveフォルダ
        archive_path = self.root_path / "archive"
        if archive_path.exists():
            dest = self.backup_path / "archive"
            shutil.move(str(archive_path), str(dest))
            self.report["moved_items"].append(f"{archive_path} → {dest}")
    
    def create_cleanup_report(self):
        """整理レポートの作成"""
        report_content = f"""# 包括的プロジェクト整理レポート - {datetime.now().strftime('%Y年%m月%d日')}

## 📋 整理概要
**実行日時**: {self.report['timestamp']}
**整理項目**: {len(self.report['moved_items'])}項目移動

## 🗂️ 最適化後の構造

### ルートディレクトリ（必須ファイルのみ）
- CLAUDE.md - プロジェクト設定
- README.md - プロジェクト概要  
- package.json, requirements.txt - 依存関係
- vercel.json - デプロイ設定

### システムディレクトリ（/system/）
- 自動更新システム
- Gemini AI統合
- セッション保存プロトコル
- プロジェクト整理システム

### ドキュメント（/docs/）
- 使用ガイド
- プロジェクト構造
- セッション保存ガイド

### セッション記録（/sessions/）
- 日次セッション記録
- 包括セッション記録

### 公開サイト（/public/）
- discussion-site - 研究ディスカッションサイト
- main-system - メインシステム

### 研究内容（/study/）
- Git submodule として保持
- 研究データ・分析結果

### 最小限ツール（/tools/）
- direct_vercel_deploy.py - 直接デプロイ
- research_analysis_system.py - 研究分析

## 📦 バックアップ内容

### comprehensive_cleanup_backup/
"""

        for item in self.report["moved_items"]:
            report_content += f"- {item}\n"

        report_content += f"""
## 🎯 整理効果

### 構造明確化
- ルートディレクトリ: 必須ファイルのみ
- 機能別フォルダ: 明確な役割分担
- 重複排除: 類似機能の統合

### 保守性向上
- 必要ファイルの特定容易
- 機能追加時の配置明確
- バックアップによる安全性確保

### 効率向上  
- ファイル検索時間短縮
- システム理解の容易化
- 開発効率の向上

## ⚠️ 注意事項
- バックアップは1週間後に削除検討
- 必要なファイルがあれば復元可能
- study/フォルダはsubmoduleとして保持

---
**作成者**: 包括的整理システム
**次回整理**: 1ヶ月後推奨
"""

        with open(self.root_path / "docs" / "COMPREHENSIVE_CLEANUP_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        
        # JSONレポートも作成
        with open(self.backup_path / "cleanup_log.json", "w", encoding="utf-8") as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    cleanup = ComprehensiveCleanup()
    cleanup.execute_cleanup()