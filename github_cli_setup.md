# GitHub CLI 連携ガイド

## 🚀 GitHub CLI (gh) のセットアップ

### 1. GitHub CLI のインストール

#### Windows
```bash
# winget を使用
winget install --id GitHub.cli

# または Scoop を使用
scoop install gh

# または Chocolatey を使用
choco install gh
```

#### macOS
```bash
# Homebrew を使用
brew install gh
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. GitHub CLI の認証

```bash
# 対話的に認証
gh auth login

# 以下の質問に答えます：
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations? HTTPS
# ? Authenticate Git with your GitHub credentials? Yes
# ? How would you like to authenticate GitHub CLI? Login with a web browser
```

### 3. Personal Access Token を使用した認証

```bash
# トークンを使用して認証
gh auth login --with-token < token.txt

# または環境変数で設定
export GH_TOKEN="ghp_your_personal_access_token"
gh auth login
```

## 📝 研究プロジェクト用 CLI スクリプト

### 基本的な GitHub CLI コマンド

```bash
# リポジトリ作成
gh repo create TK561/study --public --description "研究プロジェクト"

# リポジトリクローン
gh repo clone TK561/study

# Issue 作成
gh issue create --title "実験結果の分析" --body "新しい手法の検証が必要"

# Pull Request 作成
gh pr create --title "新機能追加" --body "意味カテゴリ分析の改善"

# ワークフロー実行
gh workflow run claude-review.yml

# リポジトリ情報表示
gh repo view TK561/study --web
```

## 🔧 研究プロジェクト用カスタムスクリプト