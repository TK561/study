# 🚀 GitHub CLI クイックコマンド集

## 📋 基本操作

### リポジトリ操作
```bash
# 現在のディレクトリをGitHubリポジトリとして作成
gh repo create study --source=. --public --push

# リポジトリ情報表示
gh repo view

# ブラウザでリポジトリを開く
gh repo view --web

# リポジトリクローン
gh repo clone TK561/study

# フォークの同期
gh repo sync
```

### Issue 操作
```bash
# Issue 作成
gh issue create --title "実験結果の検証" --body "新手法の性能評価が必要"

# Issue 一覧
gh issue list

# 自分に割り当てられたIssue
gh issue list --assignee @me

# Issue にコメント
gh issue comment 123 --body "実験完了しました"

# Issue を閉じる
gh issue close 123
```

### Pull Request 操作
```bash
# PR 作成（インタラクティブ）
gh pr create

# PR 作成（ワンライナー）
gh pr create --title "新機能: 意味カテゴリ分析" --body "WordNet統合完了"

# ドラフトPR作成
gh pr create --draft --title "WIP: 実験中"

# PR 一覧
gh pr list

# PR の状態確認
gh pr status

# PR をマージ
gh pr merge

# PR レビュー
gh pr review --approve --body "LGTM!"
```

### GitHub Actions 操作
```bash
# ワークフロー一覧
gh workflow list

# ワークフロー実行
gh workflow run claude-review.yml

# 実行履歴確認
gh run list

# 特定のワークフローの実行履歴
gh run list --workflow=claude-review.yml

# 実行ログ表示
gh run view

# 失敗した実行の再実行
gh run rerun
```

## 🔬 研究プロジェクト専用コマンド

### 実験ブランチワークフロー
```bash
# 1. 実験ブランチ作成
git checkout -b experiment/semantic-analysis

# 2. 実験実施・コミット
python semantic_classification_system.py
git add .
git commit -m "🧪 実験: 意味カテゴリ分析の改善"

# 3. プッシュとPR作成
git push -u origin experiment/semantic-analysis
gh pr create --title "実験: 意味カテゴリ分析の改善" --body "## 実験概要
- 新しいカテゴリ判定アルゴリズム
- 性能改善: 15%向上
- 詳細は results/ を参照"

# 4. レビュー後マージ
gh pr merge --squash
```

### 研究進捗管理
```bash
# 週次進捗Issue作成
gh issue create --title "週次進捗 $(date +%Y-%m-%d)" --body "## 今週の成果
- [ ] 実験1: データ前処理
- [ ] 実験2: モデル改善
- [ ] 論文執筆: 手法セクション"

# マイルストーン設定
gh issue create --milestone "v1.0" --title "最終評価実験"

# ラベル付きIssue
gh issue create --label "experiment,priority" --title "ベースライン実験"
```

### リリース管理
```bash
# 研究成果のリリース
gh release create v1.0 --title "研究成果 v1.0" --notes "## 主な成果
- 意味カテゴリ分類システム完成
- 実験結果: 85%精度達成
- 論文採択"

# ファイル添付
gh release create v1.0 results.zip paper.pdf --title "最終成果物"
```

## 🎯 効率化エイリアス

### エイリアス設定
```bash
# PR作成（ドラフト）
gh alias set prc 'pr create --draft --title'

# 自分のIssue一覧
gh alias set my-issues 'issue list --assignee @me'

# 最近の実行
gh alias set runs 'run list --limit 10'

# 実験PR作成
gh alias set experiment 'pr create --title "実験:" --body "## 実験概要"'

# 週次レポート
gh alias set weekly 'issue create --title "週次進捗 $(date +%Y-%m-%d)"'
```

### 使用例
```bash
# ドラフトPR作成
gh prc "新しい分類手法の実装"

# 自分のIssue確認
gh my-issues

# 実験PR作成
gh experiment "WordNet階層の活用"
```

## 📊 統計情報取得

```bash
# リポジトリの統計
gh api repos/:owner/:repo --jq '{
  stars: .stargazers_count,
  forks: .forks_count,
  issues: .open_issues_count,
  language: .language,
  size: .size
}'

# コントリビューター一覧
gh api repos/:owner/:repo/contributors --jq '.[].login'

# 最近のコミット
gh api repos/:owner/:repo/commits --jq '.[0:5] | .[] | {
  date: .commit.author.date,
  message: .commit.message,
  author: .commit.author.name
}'
```

## 🔐 シークレット管理

```bash
# シークレット一覧
gh secret list

# シークレット設定
gh secret set ANTHROPIC_API_KEY

# 環境変数から設定
echo $GITHUB_TOKEN | gh secret set GITHUB_TOKEN

# ファイルから設定
gh secret set LARGE_SECRET < secret.txt
```

## 🚨 トラブルシューティング

### 認証関連
```bash
# 認証状態確認
gh auth status

# 再認証
gh auth login

# トークンでの認証
echo "ghp_xxxxxxxxxxxx" | gh auth login --with-token

# 認証情報リフレッシュ
gh auth refresh
```

### デバッグ
```bash
# デバッグモード
GH_DEBUG=1 gh issue create

# API レート制限確認
gh api rate_limit

# 設定確認
gh config list
```

## 📚 研究プロジェクト テンプレート

### 実験Issue テンプレート
```bash
gh issue create --title "実験: [実験名]" --body "## 目的
[実験の目的]

## 手法
[使用する手法]

## 期待される結果
[期待される成果]

## タスク
- [ ] データ準備
- [ ] 実装
- [ ] 実験実行
- [ ] 結果分析
- [ ] レポート作成"
```

### 論文PR テンプレート
```bash
gh pr create --title "論文: [セクション名]" --body "## 追加内容
[追加した内容の概要]

## 変更点
- 

## レビューポイント
- 

## チェックリスト
- [ ] 文法チェック
- [ ] 参考文献確認
- [ ] 図表の確認"
```

---

**💡 Tips**: 
- `gh browse` で現在のリポジトリをブラウザで開く
- `gh gist create file.py` でコードスニペットを共有
- `gh extension browse` で拡張機能を探す

*Generated with Claude Code - GitHub CLI Guide*