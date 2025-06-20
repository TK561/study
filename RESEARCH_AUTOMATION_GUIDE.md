# 🔬 研究プロジェクト自動化システム - 完全ガイド

Claude Code を活用した研究プロジェクトのGitHub自動化システムの包括的なガイドです。

## 📋 システム概要

このシステムは、Claude Code を使用した研究開発プロジェクトを効率的に管理するための自動化ツールセットです。

### 🎯 主要機能

1. **Git自動化**: Personal Access Token認証によるセキュアな自動コミット・プッシュ
2. **研究ガイドライン**: Claude Code との協働のためのベストプラクティス
3. **GitHub Actions**: 研究コードの品質管理と実験追跡
4. **VS Code統合**: 研究タスクの効率的な実行環境
5. **データ管理**: 研究データの自動バックアップと版数管理
6. **実験ログ**: 研究活動の自動記録と分析

## 🚀 クイックスタート

### 1. システムセットアップ
```bash
# Windows
setup_research.bat

# または Python直接実行
python setup_research_automation.py
```

### 2. 設定ファイル編集
`config.py` を編集して実際の値を設定:
```python
GITHUB_TOKEN = "ghp_your_personal_access_token"
GITHUB_USERNAME = "your_github_username"
REPOSITORY_NAME = "your_repository_name"
GITHUB_EMAIL = "your@email.com"
ANTHROPIC_API_KEY = "sk-ant-your_claude_api_key"  # オプション
RESEARCH_INSTITUTION = "Your University"
RESEARCHER_NAME = "Your Name"
```

### 3. VS Code でタスク実行
- `Ctrl+Shift+P` → `Tasks: Run Task`
- 推奨タスク: `🚀 Research Commit: Auto Commit & Push`

## 📁 ファイル構成

### 核となるファイル

#### 設定ファイル
- **`config.py`** - システム設定（APIキー、トークン等）
- **`config.example.py`** - 設定テンプレート

#### 自動化スクリプト
- **`research_git_automation.py`** - メイン自動化システム（600行以上）
- **`setup_research_automation.py`** - 一括セットアップスクリプト

#### ガイドライン・ドキュメント
- **`CLAUDE.md`** - 研究プロジェクト用Claude Codeガイドライン
- **`RESEARCH_AUTOMATION_GUIDE.md`** - このファイル（完全ガイド）

#### GitHub Actions
- **`.github/workflows/claude-review.yml`** - 研究レビューワークフロー
- **`.github/WORKFLOWS_README.md`** - ワークフロー説明書

#### VS Code統合
- **`.vscode/tasks.json`** - 研究タスク定義

#### 実行用スクリプト
- **`setup_research.bat`** - Windows用セットアップバッチ

## 🔧 詳細機能

### 1. Git自動化システム

#### 基本コマンド
```bash
# 初期セットアップ
python research_git_automation.py --setup

# 自動コミット・プッシュ
python research_git_automation.py --auto-commit

# プロジェクト状態確認
python research_git_automation.py --status

# 手動バックアップ
python research_git_automation.py --backup

# 設定検証
python research_git_automation.py --validate-config
```

#### カスタムメッセージでのコミット
```bash
python research_git_automation.py --auto-commit -m "🧪 新しい実験手法を実装"
```

### 2. 研究進捗に基づくコミットメッセージ

システムは変更内容を自動分析し、研究活動に応じたコミットメッセージを生成します：

#### 自動検出される研究活動
- **実験実施** (`experiment`): Jupyter Notebook の変更
- **コード開発** (`development`): Python ファイルの変更
- **結果分析** (`analysis`): 結果ファイルの変更
- **文書作成** (`documentation`): Markdown/LaTeX ファイルの変更
- **テスト実行** (`testing`): テストファイルの変更

#### 生成されるコミットメッセージ例
```
🧪 実験実施: ノートブック: semantic_analysis.ipynb, データ: 3ファイル

📂 プロジェクト: 意味カテゴリに基づく画像分類システム
🔬 研究活動: experiment
📅 実行日時: 2024-01-15 14:30:25

変更サマリー:
• Jupyter Notebook: 1ファイル
• データファイル: 3ファイル
• 実験結果: 2ファイル

🚀 Generated with [Claude Code](https://claude.ai/code)
🎓 Research automation system

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 3. データ管理とバックアップ

#### 自動作成されるディレクトリ構造
```
research-project/
├── data/
│   ├── raw/           # 元データ
│   ├── processed/     # 処理済みデータ
│   └── external/      # 外部データ
├── notebooks/         # Jupyter Notebooks
├── results/           # 実験結果
├── figures/           # グラフ・図表
├── scripts/           # スクリプト
├── docs/              # ドキュメント
└── papers/            # 論文関連
```

#### バックアップ設定
- **自動バックアップ**: コミット時に重要ディレクトリを自動バックアップ
- **除外設定**: 大容量ファイルや一時ファイルは自動除外
- **版数管理**: タイムスタンプ付きバックアップディレクトリ

### 4. 実験ログ管理

#### 自動記録される情報
```json
{
  "timestamp": "2024-01-15T14:30:25",
  "commit_hash": "a1b2c3d4",
  "research_activity": "experiment",
  "change_type": "modification",
  "files_modified": {
    "code": 2,
    "notebooks": 1,
    "data": 3,
    "results": 2,
    "docs": 1
  },
  "project_metadata": {
    "dataset_version": "1.0",
    "model_version": "1.0"
  }
}
```

### 5. GitHub Actions ワークフロー

#### claude-review.yml の機能
- **Claude Code 検出**: AI生成コードの自動識別
- **コード品質チェック**: Black, isort, Flake8, MyPy
- **実験検証**: 複数Python版でのテスト実行
- **データ管理**: 機密情報チェック、バックアップ作成
- **進捗レポート**: 包括的な研究進捗レポート生成

#### 実行トリガー
- **プッシュ**: main/master/develop ブランチ
- **プルリクエスト**: main/master ブランチ
- **スケジュール**: 毎日午前6時（UTC）
- **手動実行**: ワークフロー画面から

### 6. VS Code タスク統合

#### 利用可能なタスク
1. **🔧 Research Setup** - 初期設定
2. **🚀 Research Commit** - 自動コミット・プッシュ  
3. **📊 Research Status** - プロジェクト状態表示
4. **💾 Research Backup** - 手動バックアップ
5. **🔍 Config Validation** - 設定検証
6. **🎯 Run Main System** - メインシステム実行
7. **🧪 Research Experiment** - カスタムメッセージでコミット
8. **📝 Code Formatting** - コード整形
9. **🔍 Code Quality** - 品質チェック
10. **🧪 Run Tests** - テスト実行
11. **🔄 Full Workflow** - 完全ワークフロー
12. **🆘 Quick Fix** - 問題解決支援

#### キーボードショートカット
- `Ctrl+Shift+P` → `Tasks: Run Task` → タスク選択

## 🎯 日常的なワークフロー

### 典型的な研究日のフロー

#### 1. 朝の準備
```bash
# プロジェクト状態確認
python research_git_automation.py --status

# または VS Code タスク
# Ctrl+Shift+P → "📊 Research Status: Project Overview"
```

#### 2. 研究作業
- Claude Code で実験コード作成
- Jupyter Notebook で データ分析
- 結果の可視化とレポート作成

#### 3. 作業終了時
```bash
# 自動コミット・プッシュ
python research_git_automation.py --auto-commit

# または VS Code タスク  
# Ctrl+Shift+P → "🚀 Research Commit: Auto Commit & Push"
```

#### 4. 定期的なメンテナンス
```bash
# 完全ワークフロー実行（週1回推奨）
# VS Code: Ctrl+Shift+P → "🔄 Full Research Workflow"

# 手動バックアップ（重要な実験前後）
python research_git_automation.py --backup
```

### 実験特化ワークフロー

#### 重要な実験前
1. **バックアップ作成**: 現在の状態を保存
2. **ブランチ作成**: 実験用ブランチ
3. **設定記録**: 実験パラメータの記録

#### 実験実行中
1. **進捗コミット**: 定期的な中間保存
2. **ログ記録**: 実験ノートの更新
3. **結果保存**: 図表とデータの保存

#### 実験完了後
1. **結果まとめ**: 包括的なコミット
2. **レポート作成**: 実験レポート生成
3. **マージ**: メインブランチへの統合

## 🔍 トラブルシューティング

### よくある問題と解決策

#### 1. 設定エラー
```bash
# 設定検証実行
python research_git_automation.py --validate-config

# config.py の内容確認・修正
```

#### 2. Git認証エラー
```
❌ Authentication failed
```
**解決策**:
- Personal Access Token の有効性確認
- トークンの権限設定確認（repo, workflow権限が必要）
- GitHub ユーザー名・メールアドレスの確認

#### 3. プッシュ権限エラー
```
❌ Permission denied
```
**解決策**:
- リポジトリの所有権確認
- コラボレーター権限の確認
- Personal Access Token の repo 権限確認

#### 4. 依存関係エラー
```
❌ Module not found
```
**解決策**:
```bash
# 依存関係再インストール
pip install -r requirements.txt

# 特定パッケージのインストール
pip install numpy pandas matplotlib
```

#### 5. ワークフロー実行エラー
- GitHub Actions タブでログ確認
- ワークフロー設定ファイルの構文確認
- シークレット設定の確認

### デバッグモード

#### 詳細ログの有効化
`config.py` で以下を設定:
```python
DEBUG_MODE = True
VERBOSE_LOGGING = True
LOG_LEVEL = "DEBUG"
```

#### ログファイルの確認
```bash
# Windows
type research_automation.log

# Linux/Mac
cat research_automation.log
```

## 🚀 高度な使用方法

### 1. カスタム研究活動の定義

`research_git_automation.py` の `analyze_changes()` 関数を拡張して、
プロジェクト特有の研究活動を定義できます。

### 2. 通知システムの設定

Slack/Discord Webhook を `config.py` で設定:
```python
ENABLE_NOTIFICATIONS = True
NOTIFICATION_WEBHOOK = "https://hooks.slack.com/services/..."
```

### 3. 実験メタデータのカスタマイズ

`config.py` の `EXPERIMENT_METADATA` を研究内容に応じて調整:
```python
EXPERIMENT_METADATA = {
    'dataset_version': '2.0',
    'model_architecture': 'transformer',
    'evaluation_metrics': ['accuracy', 'f1-score', 'auc'],
    'hardware_specs': 'GPU: RTX 4090'
}
```

### 4. 複数プロジェクトの管理

異なるディレクトリで別々の設定ファイルを使用:
```bash
python research_git_automation.py --path /path/to/project1 --auto-commit
python research_git_automation.py --path /path/to/project2 --auto-commit
```

## 📊 システム監視とメトリクス

### 利用可能なメトリクス

#### 研究活動統計
- コミット頻度
- 研究活動タイプ別分布
- ファイルタイプ別変更頻度
- 実験実行回数

#### コード品質メトリクス
- コード品質スコア
- テストカバレッジ
- セキュリティスキャン結果
- 依存関係の健全性

#### GitHub Actions統計
- ワークフロー実行成功率
- 平均実行時間
- リソース使用量
- エラー発生頻度

### レポート生成

#### 週次レポート
```bash
# GitHub Actions の schedule トリガーで自動生成
# または手動実行
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/USER/REPO/actions/workflows/claude-review.yml/dispatches \
  -d '{"ref":"main","inputs":{"generate_report":"true"}}'
```

#### カスタムレポート
研究固有のメトリクスを追加して独自のレポートを生成可能。

## 🤝 チーム協働

### 複数研究者での使用

#### 設定の共有
- `config.example.py` をテンプレートとして共有
- 個人の `config.py` は `.gitignore` で除外
- 共通設定は別ファイルで管理

#### ブランチ戦略
- `main`: 安定版
- `develop`: 開発版
- `experiment/*`: 実験用ブランチ
- `feature/*`: 機能追加用ブランチ

#### コードレビュー
- プルリクエスト時に自動品質チェック
- Claude Code 生成コードの人間による検証
- 実験結果の相互検証

## 📚 拡張とカスタマイズ

### プラグインシステム

将来的な拡張のための設計パターン:

#### カスタム分析器
```python
def custom_research_analyzer(changed_files):
    """プロジェクト特有の分析ロジック"""
    # 独自の分析実装
    pass
```

#### カスタム通知
```python
def custom_notification_handler(analysis_result):
    """独自の通知システム"""
    # Teams, Email 等への通知実装
    pass
```

### 外部ツール連携

#### MLflow 連携
実験管理ツールとの連携:
```python
import mlflow

def log_experiment_to_mlflow(analysis, results):
    with mlflow.start_run():
        mlflow.log_params(analysis)
        mlflow.log_metrics(results)
```

#### Weights & Biases 連携
```python
import wandb

def sync_with_wandb(experiment_data):
    wandb.log(experiment_data)
```

## 🎓 ベストプラクティス

### 1. 研究データ管理
- 元データは変更不可として保護
- 処理済みデータの版数管理
- 大容量データのGit LFS使用
- 機密データの適切な除外

### 2. コード品質
- Claude Code 生成コードの人間による検証
- 適切なテストカバレッジ維持
- 定期的なコードレビュー
- ドキュメントの継続的更新

### 3. 実験管理
- 再現可能な実験設計
- パラメータの体系的記録
- 結果の統計的検証
- 失敗した実験も含めた完全な記録

### 4. セキュリティ
- APIキーの適切な管理
- 機密情報のコミット防止
- アクセス権限の最小化
- 定期的なセキュリティ監査

## 🔮 今後の発展

### 計画中の機能
- **AI支援レポート生成**: Claude API を使用した自動レポート作成
- **高度な実験管理**: MLOps パイプラインとの統合
- **リアルタイム協働**: 複数研究者のリアルタイム同期
- **インテリジェント推奨**: AI による次の実験提案

### コミュニティ貢献
- GitHub Issues での機能要望
- プルリクエストでの改善提案
- ドキュメントの翻訳・改善
- 使用事例の共有

---

## 📞 サポートとコミュニティ

### 問題報告
- GitHub Issues: 技術的な問題
- ディスカッション: 使用方法の質問
- ドキュメント: このガイドの改善提案

### 学習リソース
- **CLAUDE.md**: Claude Code との協働ガイドライン
- **GitHub Actions ワークフロー**: CI/CD の理解
- **VS Code タスク**: 効率的な開発環境
- **Git 自動化**: バージョン管理のベストプラクティス

---

**🎉 Claude Code + GitHub + VS Code/Cursor = 最強の研究開発環境**

*この自動化システムで、効率的で高品質な研究を実現しましょう！*

---
*Generated with Claude Code - Research Automation System*  
*Last Updated: 2024-01-15*