# プロジェクト構造 - 最適化後

最終更新: 2025年6月25日（包括的整理後）

## 📂 ディレクトリ構造（最適化後）

```
/mnt/c/Desktop/Research/
├── CLAUDE.md                          # Claude Code設定・指示
├── README.md                          # プロジェクト概要
├── package.json                       # Node.js依存関係
├── requirements.txt                   # Python依存関係
├── vercel.json                        # Vercelデプロイ設定
│
├── 📁 system/                         # コアシステム（7ファイル）
│   ├── auto_cleanup.py               # 自動整理システム
│   ├── auto_update_system.py         # 自動更新システム
│   ├── cleanup_plan.py               # 整理計画システム
│   ├── comprehensive_cleanup.py      # 包括的整理システム
│   ├── gemini_integration.py         # Gemini AI統合
│   ├── session_save_protocol.py      # セッション保存プロトコル
│   └── setup_auto_update.py          # 自動更新セットアップ
│
├── 📁 docs/                           # ドキュメント（4ファイル）
│   ├── AUTO_UPDATE_GUIDE.md          # 自動更新ガイド
│   ├── COMPREHENSIVE_CLEANUP_REPORT.md # 包括整理レポート
│   ├── PROJECT_STRUCTURE.md          # プロジェクト構造（このファイル）
│   └── SESSION_SAVE_GUIDE.md         # セッション保存ガイド
│
├── 📁 sessions/                       # セッション記録（2ファイル）
│   ├── daily_session_2025-06-25.md   # 日次セッション記録
│   └── COMPLETE_SESSION_SUMMARY_2025-06-25.md # 包括セッション記録
│
├── 📁 ai_analysis/                    # AI分析結果（2ファイル）
│   ├── gemini_analysis_chat_*.md     # Gemini対話結果
│   └── gemini_analysis_progress_*.md # Gemini進捗分析
│
├── 📁 public/                         # Web公開ファイル
│   ├── discussion-site/              # 研究ディスカッションサイト
│   │   ├── index.html               # メインHTML（3タブシステム）
│   │   └── index_old.html           # 旧バージョン
│   ├── main-system/                  # メインシステム
│   │   └── index.html               # システムHTML
│   └── index.html                    # ルートHTML
│
├── 📁 tools/                          # 最小限ツール（3ファイル）
│   ├── direct_vercel_deploy.py       # 直接Vercelデプロイ
│   ├── research_analysis_system.py   # 研究分析システム
│   └── vercel_quick_deploy.sh        # クイックデプロイスクリプト
│
├── 📁 study/                          # 研究内容（Git submodule）
│   ├── early_development/            # 第0-2回初期開発
│   ├── research_discussions/         # 研究ディスカッション記録
│   ├── analysis_reports/             # 分析レポート
│   └── research_content/             # 研究実装コード
│
└── 📁 comprehensive_cleanup_backup/   # 整理済みファイル保管
    ├── previous_temp_backup/         # 前回整理分
    ├── tools/                        # 移動済みツール（14ファイル）
    ├── old_reports/                  # 古いレポート
    └── archive/                      # アーカイブ
```

## 🎯 各ディレクトリの役割

### ルートファイル
- **CLAUDE.md**: プロジェクト全体の設定・指示
- **README.md**: プロジェクト概要・使用方法
- **設定ファイル**: package.json, requirements.txt, vercel.json

### system/
研究プロジェクトのコアシステム
- **自動更新・整理システム**: auto_update_system.py, comprehensive_cleanup.py
- **AI統合・分析システム**: gemini_integration.py
- **セッション管理システム**: session_save_protocol.py

### docs/
プロジェクト関連ドキュメント
- **システム使用ガイド**: AUTO_UPDATE_GUIDE.md, SESSION_SAVE_GUIDE.md
- **プロジェクト構造説明**: PROJECT_STRUCTURE.md
- **整理・保存プロトコル**: COMPREHENSIVE_CLEANUP_REPORT.md

### sessions/
セッション記録・作業履歴
- **日次作業記録**: daily_session_*.md
- **包括的セッション記録**: COMPLETE_SESSION_SUMMARY_*.md

### public/
Web公開サイト
- **研究ディスカッションサイト**: discussion-site/（3タブシステム）
- **メインシステム**: main-system/

### tools/
最小限の実用ツール
- **Vercelデプロイ**: direct_vercel_deploy.py, vercel_quick_deploy.sh
- **研究分析**: research_analysis_system.py

### study/
研究内容（Git submodule）
- **初期開発**: early_development/（第0-2回ファイル）
- **研究実装・分析**: research_content/, analysis_reports/
- **ディスカッション記録**: research_discussions/

## 🚀 使い方

### 自動更新システム
```bash
# 研究記録更新時の自動同期
python3 system/auto_update_system.py monitor

# VS Code: Ctrl+Shift+P > Tasks: Run Task > Discussion: Check Updates
```

### Gemini AI統合
```bash
# 研究進捗分析
python3 system/gemini_integration.py progress

# 対話形式質問
python3 system/gemini_integration.py chat "質問内容"
```

### セッション保存
```bash
# 包括的セッション保存（トリガー: "今日の内容を保存"）
python3 system/session_save_protocol.py
```

### プロジェクト整理
```bash
# 包括的プロジェクト整理
python3 system/comprehensive_cleanup.py
```

## 🔄 整理履歴

### 2025年6月25日 - 包括的整理
- **17項目移動**: tools/, archive/, 重複ファイル
- **構造最適化**: 機能別フォルダ分類
- **バックアップ**: comprehensive_cleanup_backup/に安全保管

### 効果
- **構造明確化**: 機能別の明確な役割分担
- **保守性向上**: 必要ファイルの特定容易
- **効率向上**: ファイル検索時間短縮

## ⚠️ 注意事項

### バックアップ管理
- **comprehensive_cleanup_backup/**: 1週間後削除検討
- **復元可能**: 必要時は手動復元
- **Git管理**: .gitignore でバックアップ除外

### 継続保守
- **定期整理**: 1ヶ月後に再整理推奨
- **自動システム**: system/ 内のツールで自動化
- **Git管理**: 重要変更は適切にコミット