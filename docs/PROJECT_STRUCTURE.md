# プロジェクト構造

最終更新: 2025年6月24日

## 📁 ディレクトリ構造

```
/mnt/c/Desktop/Research/
├── 📁 core/                     # コアシステム
│   ├── vercel_deploy.py         # 統合Vercelデプロイシステム
│   ├── research_manager.py      # 統合研究データ管理（作成予定）
│   ├── session_manager.py       # 統合セッション管理（作成予定）
│   └── auto_master.py           # マスター自動化システム（作成予定）
│
├── 📁 automation/               # 自動化スクリプト
│   ├── git_auto.py             # Git自動管理
│   ├── backup_auto.py          # バックアップ自動化
│   ├── monitor_auto.py         # 監視自動化
│   └── startup scripts         # 起動スクリプト
│
├── 📁 study/                    # 研究本体
│   ├── analysis/               # 分析結果
│   ├── research_content/       # 研究コンテンツ
│   ├── research_discussions/   # ディスカッション記録
│   └── reports/                # レポート
│
├── 📁 discussion-site/          # ディスカッションサイト
│   └── index.html              # ディスカッション記録ページ
│
├── 📁 docs/                     # ドキュメント
│   ├── guides/                 # ガイド文書
│   │   ├── Vercel関連ガイド
│   │   ├── システムガイド
│   │   └── クイックスタート
│   ├── archives/               # アーカイブ済みドキュメント
│   └── PROJECT_STRUCTURE.md    # このファイル
│
├── 📁 config/                   # 設定ファイル
│   ├── vercel.json
│   ├── system_config.json
│   └── 各種設定ファイル
│
├── 📁 logs/                     # ログファイル
│   ├── deployment/             # デプロイメントログ
│   ├── system/                 # システムログ
│   └── archives/               # アーカイブ済みログ
│
├── 📁 backup/                   # バックアップ
│   ├── .claude_sessions/       # Claudeセッション
│   └── .vercel_backups/        # Vercelバックアップ
│
├── 📁 public/                   # 公開ファイル
│   └── index.html              # メインサイト
│
├── 📁 _deprecated/              # 非推奨・削除予定
│   ├── old_scripts/            # 古いスクリプト
│   └── demo_files/             # デモファイル
│
├── index.html                   # ルートのメインページ
├── vercel.json                  # Vercel設定
├── README.md                    # プロジェクト概要
├── CLAUDE.md                    # Claude設定
└── requirements.txt             # Python依存関係
```

## 🔧 主要ファイルの説明

### コアシステム (`core/`)
- **vercel_deploy.py**: 全てのVercelデプロイ機能を統合
  - 自動デプロイ（Git経由）
  - APIデプロイ
  - 手動デプロイガイド

### 自動化システム (`automation/`)
- Git操作、バックアップ、監視の自動化スクリプト
- 起動時の自動実行設定

### 研究コンテンツ (`study/`)
- 研究の本体部分
- 分析結果、実験データ、レポート

### ドキュメント (`docs/`)
- プロジェクトのガイドとドキュメント
- アーカイブされた作業記録

## 🚀 使い方

### Vercelデプロイ
```bash
# 自動デプロイ（推奨）
python core/vercel_deploy.py auto

# APIデプロイ
python core/vercel_deploy.py api

# 手動デプロイ
python core/vercel_deploy.py manual
```

### 研究データ管理
```bash
# 研究データの管理（作成予定）
python core/research_manager.py
```

### セッション管理
```bash
# セッションの保存と復元（作成予定）
python core/session_manager.py
```

## 📝 メンテナンス

### 定期的なクリーンアップ
1. `_deprecated/` フォルダの古いファイルを定期的に削除
2. `logs/archives/` の古いログを圧縮または削除
3. `backup/` の古いバックアップを整理

### 新規ファイルの追加
- 機能別に適切なディレクトリに配置
- 重複機能がないか確認
- ドキュメントを更新

## 🔄 移行状況

### 完了
- ✅ ディレクトリ構造の作成
- ✅ デモファイルの移動
- ✅ 日付付きドキュメントのアーカイブ
- ✅ Vercelスクリプトの統合（一部）
- ✅ ガイド文書の整理

### 進行中
- 🔄 研究データ管理システムの統合
- 🔄 セッション管理システムの統合
- 🔄 自動化システムの整理

### 予定
- ⏳ 重複ファイルの完全削除
- ⏳ 設定ファイルの統合
- ⏳ テストとドキュメントの更新