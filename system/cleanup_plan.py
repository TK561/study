#!/usr/bin/env python3
"""
ファイルとフォルダ整理計画
研究プロジェクトの構造を最適化し、不要ファイルを整理
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

class ProjectCleaner:
    def __init__(self):
        self.research_root = Path("/mnt/c/Desktop/Research")
        self.cleanup_report = []
        
    def analyze_structure(self):
        """現在の構造を分析"""
        print("📋 プロジェクト構造分析中...")
        
        # 重要な保持すべきファイル・フォルダ
        keep_items = {
            # メインファイル
            "CLAUDE.md", "README.md", "vercel.json", "package.json",
            "auto_update_system.py", "setup_auto_update.py", "gemini_integration.py",
            "AUTO_UPDATE_GUIDE.md", "daily_session_2025-06-25.md",
            
            # 重要フォルダ
            "public/", "study/", "ai_analysis/", ".vscode/",
            
            # 設定ファイル
            ".env", ".gitignore", ".auto_update_config.json"
        }
        
        # 削除対象
        cleanup_targets = {
            # 古いバックアップ
            ".html_backups/": "古いHTMLバックアップ",
            "archive/old_backups/": "古いバックアップファイル",
            "archive/old_code/": "古いコードファイル",
            "archive/old_sessions/": "古いセッション記録",
            "archive/old_summaries/": "古い要約ファイル",
            
            # 重複ファイル
            "discussion-site/": "重複するディスカッションサイト",
            "nodejs/": "未使用のNode.js設定",
            "node_modules/": "ルートのnode_modules",
            
            # 古い開発ファイル
            "daily_session_2025-06-24.md": "前日のセッション記録",
            "PROJECT_STRUCTURE_CLEAN.md": "古い構造ファイル",
            "PROJECT_STRUCTURE_FINAL.md": "古い構造ファイル",
            "AI_INTEGRATION_SUMMARY.md": "統合済みの要約",
            "ITERATIVE_DEVELOPMENT_PROCESS.md": "プロセス文書（統合済み）",
            
            # 古い自動化システム
            "automation/": "旧自動化システム",
            "core/": "旧コアシステム",
            "tools/system/": "旧システムツール",
            "config/": "旧設定ファイル群",
            "data/": "旧データファイル",
            "knowledge/": "旧ナレッジベース",
            "logs/": "旧ログファイル",
            
            # 古いドキュメント
            "docs/archives/": "アーカイブ文書",
            "docs/guides/": "統合されたガイド群",
            "reports/": "旧レポート",
        }
        
        return keep_items, cleanup_targets
    
    def safe_cleanup(self, cleanup_targets):
        """安全な整理実行"""
        print("🧹 ファイル整理を開始...")
        
        # バックアップディレクトリ作成
        backup_dir = self.research_root / "temp_cleanup_backup"
        backup_dir.mkdir(exist_ok=True)
        
        for target, description in cleanup_targets.items():
            target_path = self.research_root / target
            
            if target_path.exists():
                try:
                    # バックアップに移動
                    backup_path = backup_dir / target
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if target_path.is_dir():
                        shutil.move(str(target_path), str(backup_path))
                        print(f"📁 移動: {target} → temp_cleanup_backup/")
                    else:
                        shutil.move(str(target_path), str(backup_path))
                        print(f"📄 移動: {target} → temp_cleanup_backup/")
                    
                    self.cleanup_report.append(f"✅ {target}: {description}")
                    
                except Exception as e:
                    print(f"❌ エラー: {target} - {e}")
                    self.cleanup_report.append(f"❌ {target}: エラー - {e}")
            else:
                print(f"⚠️ 見つからない: {target}")
    
    def organize_remaining_structure(self):
        """残りのファイルを整理"""
        print("📁 フォルダ構造を最適化...")
        
        # 新しい構造の提案
        new_structure = {
            "system/": ["auto_update_system.py", "setup_auto_update.py", "gemini_integration.py"],
            "docs/": ["AUTO_UPDATE_GUIDE.md"],
            "sessions/": ["daily_session_2025-06-25.md"],
        }
        
        for folder, files in new_structure.items():
            folder_path = self.research_root / folder
            folder_path.mkdir(exist_ok=True)
            
            for file in files:
                file_path = self.research_root / file
                if file_path.exists():
                    new_path = folder_path / file
                    try:
                        shutil.move(str(file_path), str(new_path))
                        print(f"📋 移動: {file} → {folder}")
                    except Exception as e:
                        print(f"❌ 移動エラー: {file} - {e}")
    
    def create_cleanup_summary(self):
        """整理結果のサマリー作成"""
        summary = f"""# ファイル・フォルダ整理レポート

**実行日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 📋 整理内容

### ✅ 完了した整理
"""
        
        for item in self.cleanup_report:
            summary += f"- {item}\n"
        
        summary += f"""

### 📁 最終的なプロジェクト構造

```
Research/
├── CLAUDE.md                    # プロジェクト設定
├── README.md                    # プロジェクト概要
├── vercel.json                  # Vercel設定
├── package.json                 # Node.js設定
├── .env                         # 環境変数
├── .gitignore                   # Git除外設定
├── .auto_update_config.json     # 自動更新設定
├── .vscode/                     # VS Code設定
├── system/                      # システムスクリプト
│   ├── auto_update_system.py
│   ├── setup_auto_update.py
│   └── gemini_integration.py
├── docs/                        # ドキュメント
│   └── AUTO_UPDATE_GUIDE.md
├── sessions/                    # セッション記録
│   └── daily_session_2025-06-25.md
├── ai_analysis/                 # AI分析結果
├── public/                      # Webサイト
│   ├── index.html
│   ├── discussion-site/
│   └── main-system/
├── study/                       # 研究コンテンツ
└── temp_cleanup_backup/         # 整理済みファイル（一時保管）
```

### 🗑️ バックアップ保管場所

整理したファイルは `temp_cleanup_backup/` に一時保管されています。
1週間後に問題がなければ完全削除することを推奨します。

### ⚠️ 注意事項

- 重要なファイルは保持されています
- バックアップは一時的に保管されています
- 必要に応じて復元可能です

---

**整理者**: Claude Code システム
**バックアップ期限**: {(datetime.now() + timedelta(days=7)).strftime('%Y年%m月%d日')}
"""
        
        summary_file = self.research_root / "CLEANUP_REPORT.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"📄 整理レポートを作成: {summary_file}")

def main():
    """メイン実行"""
    print("🧹 プロジェクト整理システム")
    print("=" * 40)
    
    cleaner = ProjectCleaner()
    
    # 構造分析
    keep_items, cleanup_targets = cleaner.analyze_structure()
    
    print(f"📊 分析結果:")
    print(f"  保持対象: {len(keep_items)}項目")
    print(f"  整理対象: {len(cleanup_targets)}項目")
    
    # ユーザー確認
    print("\n⚠️ 整理を実行しますか？")
    print("整理されたファイルは temp_cleanup_backup/ に一時保管されます")
    
    response = input("続行 (y/N): ")
    
    if response.lower() == 'y':
        # 整理実行
        cleaner.safe_cleanup(cleanup_targets)
        
        # 構造最適化
        cleaner.organize_remaining_structure()
        
        # レポート作成
        cleaner.create_cleanup_summary()
        
        print("\n✅ 整理完了!")
        print("📋 詳細は CLEANUP_REPORT.md を確認してください")
        
    else:
        print("❌ 整理をキャンセルしました")

if __name__ == "__main__":
    main()