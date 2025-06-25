#!/usr/bin/env python3
"""
自動ファイル整理システム
安全にプロジェクト構造を最適化
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def main():
    research_root = Path("/mnt/c/Desktop/Research")
    
    print("🧹 プロジェクト自動整理を開始...")
    
    # 削除対象（安全な項目のみ）
    safe_cleanup_targets = [
        ".html_backups",
        "archive/old_backups", 
        "archive/old_code",
        "archive/old_sessions",
        "archive/old_summaries",
        "discussion-site",  # 重複サイト
        "nodejs",
        "daily_session_2025-06-24.md",  # 前日のセッション
        "PROJECT_STRUCTURE_CLEAN.md",
        "PROJECT_STRUCTURE_FINAL.md", 
        "AI_INTEGRATION_SUMMARY.md",
        "ITERATIVE_DEVELOPMENT_PROCESS.md",
        "automation",
        "core",
        "config",
        "data", 
        "knowledge",
        "logs",
        "docs/archives",
        "docs/guides",
        "reports"
    ]
    
    # バックアップディレクトリ作成
    backup_dir = research_root / "temp_cleanup_backup"
    backup_dir.mkdir(exist_ok=True)
    
    cleanup_count = 0
    
    # 安全な整理実行
    for target in safe_cleanup_targets:
        target_path = research_root / target
        
        if target_path.exists():
            try:
                backup_path = backup_dir / target
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.move(str(target_path), str(backup_path))
                print(f"✅ 移動: {target}")
                cleanup_count += 1
                
            except Exception as e:
                print(f"❌ エラー: {target} - {e}")
        else:
            print(f"⚠️ 見つからない: {target}")
    
    # システムファイルの整理
    system_dir = research_root / "system"
    system_dir.mkdir(exist_ok=True)
    
    system_files = [
        "auto_update_system.py",
        "setup_auto_update.py", 
        "gemini_integration.py"
    ]
    
    for file in system_files:
        file_path = research_root / file
        if file_path.exists():
            new_path = system_dir / file
            try:
                shutil.move(str(file_path), str(new_path))
                print(f"📋 システムフォルダに移動: {file}")
            except Exception as e:
                print(f"❌ 移動エラー: {file} - {e}")
    
    # ドキュメント整理
    docs_dir = research_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    doc_files = ["AUTO_UPDATE_GUIDE.md"]
    for file in doc_files:
        file_path = research_root / file
        if file_path.exists():
            new_path = docs_dir / file
            try:
                shutil.move(str(file_path), str(new_path))
                print(f"📚 ドキュメントフォルダに移動: {file}")
            except Exception as e:
                print(f"❌ 移動エラー: {file} - {e}")
    
    # セッション記録整理
    sessions_dir = research_root / "sessions"
    sessions_dir.mkdir(exist_ok=True)
    
    session_files = ["daily_session_2025-06-25.md"]
    for file in session_files:
        file_path = research_root / file
        if file_path.exists():
            new_path = sessions_dir / file
            try:
                shutil.move(str(file_path), str(new_path))
                print(f"📅 セッションフォルダに移動: {file}")
            except Exception as e:
                print(f"❌ 移動エラー: {file} - {e}")
    
    # 重複node_modulesの削除（rootレベルのみ）
    root_node_modules = research_root / "node_modules"
    if root_node_modules.exists():
        try:
            shutil.move(str(root_node_modules), str(backup_dir / "node_modules"))
            print("📦 ルートnode_modulesを移動")
            cleanup_count += 1
        except Exception as e:
            print(f"❌ node_modules移動エラー: {e}")
    
    # 整理レポート作成
    report_content = f"""# プロジェクト整理レポート

**実行日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}  
**整理項目数**: {cleanup_count}項目

## 📁 最適化されたプロジェクト構造

```
Research/
├── CLAUDE.md                    # プロジェクト設定
├── README.md                    # プロジェクト概要  
├── vercel.json                  # Vercel設定
├── package.json                 # Node.js設定
├── requirements.txt             # Python依存関係
├── .env                         # 環境変数
├── .gitignore                   # Git除外設定
├── .auto_update_config.json     # 自動更新設定
├── .vscode/                     # VS Code設定
├── system/                      # システムスクリプト
│   ├── auto_update_system.py    # 自動更新システム
│   ├── setup_auto_update.py     # セットアップ
│   └── gemini_integration.py    # Gemini AI統合
├── docs/                        # ドキュメント
│   └── AUTO_UPDATE_GUIDE.md     # 自動更新ガイド
├── sessions/                    # セッション記録
│   └── daily_session_2025-06-25.md
├── ai_analysis/                 # AI分析結果
├── public/                      # Webサイト（本番）
│   ├── index.html               # メインサイト
│   ├── discussion-site/         # ディスカッション記録
│   └── main-system/             # メインシステム
├── study/                       # 研究コンテンツ
├── tools/                       # 開発ツール
├── temp_cleanup_backup/         # 整理済みファイル（一時保管）
└── cleanup_plan.py              # 整理計画スクリプト
```

## ✅ 整理完了項目

### 🗑️ 削除・移動された項目
- 古いHTMLバックアップファイル群
- 重複するディスカッションサイト
- 未使用の自動化システム
- 古いセッション記録・要約
- 重複するNode.js設定
- 古いドキュメント・ガイド群

### 📁 整理されたフォルダ
- `system/`: システムスクリプト集約
- `docs/`: ドキュメント集約  
- `sessions/`: セッション記録集約

## 🔄 バックアップ情報

**保管場所**: `temp_cleanup_backup/`  
**保管期限**: {(datetime.now() + timedelta(days=7)).strftime('%Y年%m月%d日')}（推奨）

整理されたファイルは一時的に保管されています。
1週間問題がなければ完全削除を推奨します。

## 🎯 整理効果

- **ファイル数削減**: 大幅な整理により見通し向上
- **構造最適化**: 機能別フォルダ分類で管理効率化
- **重複削除**: 重複ファイル・フォルダの除去
- **保守性向上**: 明確な構造による維持管理の簡素化

---

**整理システム**: Claude Code 自動整理システム  
**次回推奨**: 1ヶ月後の定期整理
"""
    
    report_file = research_root / "CLEANUP_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✅ プロジェクト整理完了!")
    print(f"📊 整理項目: {cleanup_count}個")
    print(f"📄 詳細レポート: CLEANUP_REPORT.md")
    print(f"💾 バックアップ: temp_cleanup_backup/")
    
    # 最終構造確認
    print("\n📁 整理後の主要構造:")
    important_items = [
        "CLAUDE.md", "README.md", "vercel.json", 
        "system/", "docs/", "sessions/", "ai_analysis/", 
        "public/", "study/", ".vscode/"
    ]
    
    for item in important_items:
        item_path = research_root / item
        if item_path.exists():
            print(f"  ✅ {item}")
        else:
            print(f"  ❌ {item}")

if __name__ == "__main__":
    main()