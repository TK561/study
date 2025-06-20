# 📁 プロジェクト構造（整理後）

## ディレクトリ構成

```
Research/
├── 📄 index.py                 # Vercel用Webインターフェース（メイン）
├── 📄 requirements.txt         # Python依存関係
├── 📄 vercel.json             # Vercelデプロイ設定
├── 📄 PROJECT_STRUCTURE.md    # このファイル（プロジェクト構造説明）
│
├── 📂 docs/                   # ドキュメント類
│   ├── CLAUDE.md             # Claude Code開発ガイドライン
│   ├── README.md             # プロジェクト概要
│   ├── SECURITY.md           # セキュリティ情報
│   └── project_structure.md  # 旧構造ファイル
│
├── 📂 reports/               # 生成されたレポート類
│   ├── PROJECT_REPORT.md     # 拡張Markdownレポート
│   ├── PROJECT_REPORT.rtf    # Word用リッチテキスト
│   ├── PROJECT_REPORT.txt    # プレーンテキストレポート
│   ├── PROJECT_SUMMARY.md    # プロジェクトサマリー
│   └── PROJECT_SUMMARY_SIMPLE.html # PDF化用HTML
│
├── 📂 scripts/               # 自動化スクリプト
│   ├── hourly_summary_system.py    # 1時間毎作業整理
│   ├── research_git_automation.py  # Git自動化
│   ├── secure_config.py            # セキュア設定管理
│   └── start_hourly_system.py      # システム起動
│
├── 📂 tools/                 # 開発・生成ツール
│   ├── cleanup_test.py             # テストクリーンアップ
│   ├── create_pdf_report.py        # PDF/レポート生成
│   ├── notification_test.py        # 通知テスト
│   └── simple_html_generator.py    # HTML生成ツール
│
├── 📂 session_logs/          # セッションログ（自動生成）
│   └── session_20250620_153158.json
│
├── 📂 study/                 # メイン研究コード
│   ├── README.md            # 研究システム説明
│   ├── requirements.txt     # 研究用依存関係
│   ├── 📄 Meaning category-based classification system centered on WordNet.pdf
│   │
│   ├── 📂 analysis/         # 分析結果
│   │   └── results/
│   │       ├── dataset_analysis_report.md
│   │       └── enhanced_analysis_results.json
│   │
│   └── 📂 references/       # 研究資料・論文
│       ├── M1 Naoya Inoue Complete Edition.pdf
│       ├── M1 Naoya Inoue Presentation Slides.pptx
│       ├── semantic_classification_system_midterm_presentation.pdf
│       ├── summary.pdf
│       └── summary.pptx
│
├── 📂 temp/                 # 一時ファイル（空）
└── 📂 archive/              # アーカイブ（空）
```

## 📋 ファイル分類

### 🚀 実行ファイル（ルート）
- **index.py** - Vercelデプロイメインファイル
- **requirements.txt** - 依存関係定義
- **vercel.json** - デプロイ設定

### 📚 ドキュメント（docs/）
- **CLAUDE.md** - Claude Code使用ガイドライン
- **README.md** - プロジェクト全体概要
- **SECURITY.md** - セキュリティポリシー

### 📊 レポート（reports/）
- **PROJECT_SUMMARY.*** - プロジェクトまとめ（各形式）
- **PROJECT_REPORT.*** - 詳細レポート（各形式）

### ⚙️ スクリプト（scripts/）
- 自動化・管理用スクリプト
- セッション管理
- Git自動化

### 🛠️ ツール（tools/）
- 開発支援ツール
- レポート生成
- テスト用ツール

### 🔬 研究コード（study/）
- メインの研究実装
- 分析結果
- 参考文献・資料

## 🎯 使用方法

### Webアプリケーション表示
```bash
# ローカル開発
python index.py
# または Vercel URL でアクセス
```

### レポート表示・PDF化
```bash
# HTMLレポートをブラウザで開く
open reports/PROJECT_SUMMARY_SIMPLE.html
# ブラウザで Ctrl+P → PDF保存
```

### 自動化システム起動
```bash
python scripts/start_hourly_system.py
```

## 🤖 自動化機能
- **GitHub Actions** - プッシュ時自動デプロイ
- **Claude Code** - エラー自動修正
- **監視システム** - 30分毎ヘルスチェック
- **セッション管理** - 1時間毎作業整理

---
*Generated with Claude Code - 2025-06-20*