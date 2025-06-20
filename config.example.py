"""
研究プロジェクト用設定ファイル例
=========================

このファイルをコピーして config.py として使用してください。
実際の値は config.py に設定し、このファイルはテンプレートとして保持します。

コピー方法:
cp config.example.py config.py

その後、config.py を編集して実際の値を設定してください。
"""

# ===== GitHub設定 =====
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # GitHub Personal Access Token
# 取得方法: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
# 必要な権限: repo, workflow

GITHUB_USERNAME = "your_github_username"  # あなたのGitHubユーザー名

REPOSITORY_NAME = "semantic-classification-research"  # このプロジェクトのリポジトリ名

GITHUB_EMAIL = "your_email@example.com"  # GitHubアカウントのメールアドレス

# ===== Claude API設定 =====
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Claude APIキー
# 取得方法: https://console.anthropic.com/ → API Keys

# ===== 研究プロジェクト設定 =====
PROJECT_NAME = "意味カテゴリに基づく画像分類システム"
RESEARCH_INSTITUTION = "○○大学 情報学部"  # 所属機関
RESEARCHER_NAME = "山田太郎"  # 研究者名

PROJECT_DESCRIPTION = """
WordNetベースの意味カテゴリ分析を用いた
特化型画像分類手法の性能評価研究
"""

# ===== 自動化設定 =====
AUTO_COMMIT_ENABLED = True
AUTO_BACKUP_ENABLED = True
DAILY_COMMIT_TIME = "09:00"

# その他の設定は config.py の実際のファイルと同じ構造
# (以下省略 - 実際の設定は元のファイルを参照)