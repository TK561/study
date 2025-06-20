# プロジェクト構造（整理後）

## ディレクトリ構成

```
Research/
├── index.py                 # Vercel用Webインターフェース（メイン）
├── README.md                # プロジェクト概要
├── PROJECT_STRUCTURE.md    # このファイル（プロジェクト構造説明）
│
├── shared_resources/        # 共有リソース（両システム共通）
│   ├── CLAUDE.md            # Claude Code開発ガイドライン
│   ├── requirements.txt     # Python依存関係
│   └── vercel.json          # Vercelデプロイ設定
│
├── study/                   # 研究システム
│   ├── README.md            # 研究システム説明
│   ├── requirements.txt     # 研究用依存関係
│   ├── Meaning category-based classification system centered on WordNet.pdf
│   │
│   ├── analysis_reports/    # 分析レポート
│   │   ├── COHENS_POWER_ANALYSIS_REPORT.md
│   │   ├── DAILY_RESEARCH_SUMMARY_20250620.md
│   │   ├── DATASET_EXPANSION_PLAN.md
│   │   ├── DATASET_SELECTION_RATIONALE.md
│   │   ├── IMAGENET_BASED_RATIONALE.md
│   │   ├── IMAGENET_OPTIMAL_CATEGORY_ANALYSIS.md
│   │   ├── MAXIMUM_SPECIALIZATION_SCALING.md
│   │   ├── RESEARCH_VERIFICATION_ANALYSIS.md
│   │   ├── SPECIALIZATION_ADVANTAGE_ANALYSIS.md
│   │   ├── SPECIALIZED_DATASET_EFFECT_STUDY.md
│   │   ├── SPECIALIZED_DATASET_VALIDATION.md
│   │   ├── STATISTICAL_ANALYSIS_REPORT.md
│   │   └── STRONG_DATASET_RATIONALE.md
│   │
│   ├── research_content/    # 研究実装コード
│   │   ├── automated_dataset_collector.py
│   │   ├── cohens_power_analysis.py
│   │   ├── dataset_expansion_plan.py
│   │   ├── dataset_selection_rationale.py
│   │   ├── imagenet_optimal_category_analysis.py
│   │   ├── maximum_specialization_scaling.py
│   │   ├── single_clear_rationale.py
│   │   ├── specialization_advantage_analysis.py
│   │   ├── specialized_dataset_effect_study.py
│   │   └── strong_dataset_rationale.py
│   │
│   ├── reports/             # 生成されたレポート類
│   │   ├── PROJECT_REPORT.md
│   │   ├── PROJECT_REPORT.rtf
│   │   ├── PROJECT_REPORT.txt
│   │   ├── PROJECT_SUMMARY.md
│   │   └── PROJECT_SUMMARY_SIMPLE.html
│   │
│   ├── docs/                # ドキュメント
│   │   ├── SECURITY.md
│   │   └── project_structure.md
│   │
│   ├── tools/               # 開発・生成ツール
│   │   ├── cleanup_test.py
│   │   ├── create_pdf_report.py
│   │   ├── notification_test.py
│   │   └── simple_html_generator.py
│   │
│   ├── analysis/            # 分析結果
│   │   └── results/
│   │       ├── dataset_analysis_report.md
│   │       └── enhanced_analysis_results.json
│   │
│   └── references/          # 研究資料・論文
│       ├── M1 Naoya Inoue Complete Edition.pdf
│       ├── M1 Naoya Inoue Presentation Slides.pptx
│       ├── semantic_classification_system_midterm_presentation.pdf
│       ├── summary.pdf
│       └── summary.pptx
│
├── hourly_system/           # 1時間毎自動レポートシステム
│   ├── README.md            # システム説明
│   ├── session_logs/        # セッションログ（自動生成）
│   │   ├── archive/
│   │   ├── comprehensive_daily_report.json
│   │   ├── consolidated_reports.json
│   │   ├── current_session.json
│   │   ├── daemon_status.json
│   │   ├── session_*.json
│   │   └── recovery_report_*.json
│   │
│   ├── simple_hourly_system.py      # メインシステム
│   ├── claude_code_startup.py       # 自動起動
│   ├── enhanced_hourly_daemon.py    # 拡張デーモン
│   ├── start_hourly_system.py       # システム起動
│   ├── HOURLY_SYSTEM_MANUAL.md      # 詳細マニュアル
│   ├── QUICK_START_GUIDE.md         # クイックガイド
│   └── test_*.py                    # テストファイル
│
├── api/                     # Vercel API
│   └── index.py
│
├── .github/                 # GitHub Actions
│   └── workflows/
│       └── vercel-deploy.yml
│
├── temp/                    # 一時ファイル（空）
└── archive/                 # アーカイブ（空）
```

## ファイル分類

### 実行ファイル（ルート）
- **index.py** - Vercelデプロイメインファイル
- **README.md** - プロジェクト全体概要
- **PROJECT_STRUCTURE.md** - このファイル（構造説明）

### 共有リソース（shared_resources/）
- **CLAUDE.md** - Claude Code使用ガイドライン
- **requirements.txt** - 依存関係定義
- **vercel.json** - デプロイ設定

### 研究システム（study/）
- メインの研究実装
- 分析結果・レポート
- 参考文献・資料
- 開発ツール

### 1時間毎システム（hourly_system/）
- 自動監視・レポート
- セッション管理
- 作業追跡ログ

## 使用方法

### Webアプリケーション表示
```bash
# ローカル開発
python index.py
# または Vercel URL でアクセス
```

### 研究システム実行
```bash
cd study
python semantic_classification_system.py
```

### 1時間毎システム起動
```bash
cd hourly_system
python start_hourly_system.py
```

## 自動化機能
- **GitHub Actions** - プッシュ時自動デプロイ
- **Claude Code** - エラー自動修正
- **監視システム** - 30分毎ヘルスチェック
- **セッション管理** - 1時間毎作業整理

---
*Generated with Claude Code - 2025-06-20*