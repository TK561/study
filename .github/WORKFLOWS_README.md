# GitHub Actions Workflows for Claude Code Integration

このディレクトリには、Claude Code で作成されたプロジェクトを自動化するためのGitHub Actionsワークフローが含まれています。

##  ワークフローファイル

### 1. `claude.yml` - メインワークフロー
**目的**: Claude Code で生成されたコードの包括的な品質管理

**トリガー**:
- `main`/`master` ブランチへのプッシュ
- プルリクエスト
- 手動実行

**機能**:
- 🎨 **コード品質チェック**: Black, isort, Flake8, MyPy
-  **テスト実行**: PyTest (Python 3.8-3.11)
- 🔒 **セキュリティスキャン**: Bandit, Safety
- 📚 **ドキュメント生成**: Sphinx, MkDocs
-  **プロジェクト分析**: 統計レポート生成
-  **Claude Code検出**: AI生成コードの自動識別

### 2. `auto-commit.yml` - 自動コミット
**目的**: 定期的な自動コミット・プッシュ

**トリガー**:
- 毎日午前9時（UTC）のスケジュール実行
- 手動実行

**機能**:
-  **変更検出**: 未コミットファイルの自動検出
-  **自動コミット**: Claude Code署名付きコミット
-  **自動プッシュ**: リモートリポジトリへの自動同期

### 3. `sync-cursor.yml` - Cursor IDE連携
**目的**: Cursor IDE開発環境の最適化

**トリガー**:
- `main`/`master` ブランチへのプッシュ
- プルリクエスト
- 手動実行

**機能**:
-  **VS Code/Cursor設定生成**: settings.json, tasks.json, launch.json
-  **開発環境構築**: Python環境とツール設定
- 📖 **セットアップガイド生成**: CURSOR_SETUP.md
-  **AI統合設定**: Cursor AI機能の有効化

##  セットアップ手順

### 1. リポジトリ準備

```bash
# ワークフローファイルをリポジトリに追加
git add .github/
git commit -m "Add GitHub Actions workflows for Claude Code integration"
git push
```

### 2. シークレット設定（必要に応じて）

GitHub リポジトリの Settings → Secrets and variables → Actions で以下を設定:

- `PERSONAL_ACCESS_TOKEN`: Personal Access Token（プライベートリポジトリの場合）

### 3. 権限設定

Settings → Actions → General で以下を有効化:
-  "Allow GitHub Actions to create and approve pull requests"
-  "Allow GitHub Actions to approve pull requests"

##  ワークフロー実行パターン

### 自動実行
1. **コード変更時**: `claude.yml` が自動実行
2. **毎日定時**: `auto-commit.yml` が自動実行
3. **プルリクエスト**: コード品質チェックが自動実行

### 手動実行
1. GitHub → Actions タブ
2. ワークフローを選択
3. "Run workflow" ボタンクリック

##  生成されるアーティファクト

### コード品質レポート
- `code-quality-report`: Lint、フォーマット結果
- `security-reports`: セキュリティスキャン結果
- `failure-analysis`: 失敗時の詳細分析

### ドキュメント
- `documentation`: 生成されたAPI文書
- `project-analytics`: プロジェクト統計レポート

### Cursor設定
- `cursor-ide-config`: VS Code/Cursor設定ファイル
- セットアップガイド

##  Claude Code 特別機能

### 1. AI生成コード検出
コミットメッセージや ファイル内容から Claude Code で生成されたコードを自動検出:

```yaml
# 検出パターン例
- "Generated with [Claude Code]"
- "Co-Authored-By: Claude"
```

### 2. 自動署名追加
すべての自動コミットに Claude Code 署名を追加:

```
 Generated with [Claude Code](https://claude.ai/code)
 Auto-committed: 2024-01-15 14:30:25

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 3. インテリジェント分析
- ファイル種別に応じた適切な品質チェック
- Python プロジェクト特化の最適化
- AI生成コード特有のパターン検出

##  使用統計とモニタリング

### ワークフロー実行状況
- Actions タブで実行履歴確認
- 成功/失敗率の追跡
- 実行時間の監視

### コード品質トレンド
- 品質メトリクスの時系列変化
- セキュリティ問題の検出履歴
- テストカバレッジの推移

##  カスタマイズ方法

### 1. Python バージョン変更
```yaml
# claude.yml 内
env:
  PYTHON_VERSION: '3.10'  # 変更
```

### 2. 実行スケジュール変更
```yaml
# auto-commit.yml 内
schedule:
  - cron: '0 12 * * *'  # 毎日正午に変更
```

### 3. 品質チェック設定
```yaml
# ツール設定ファイルを追加
- setup.cfg (flake8設定)
- pyproject.toml (black, isort設定)
- mypy.ini (mypy設定)
```

## 🤝 Cursor IDE との連携

### 自動生成される設定
1. **`.vscode/settings.json`**: エディタ設定
2. **`.vscode/tasks.json`**: 開発タスク
3. **`.vscode/launch.json`**: デバッグ設定
4. **`CURSOR_SETUP.md`**: セットアップガイド

### 推奨ワークフロー
1. Cursor で開発 → 2. 自動フォーマット → 3. Git Auto Manager → 4. GitHub Actions

## 📞 トラブルシューティング

### よくある問題

#### 1. ワークフロー実行権限エラー
**解決**: Settings → Actions → General で権限を確認

#### 2. Python依存関係エラー
**解決**: requirements.txt の内容を確認

#### 3. Git 認証エラー
**解決**: Personal Access Token の権限を確認

### ログ確認方法
1. Actions タブ → 失敗したワークフロー選択
2. 各ジョブのログを展開して詳細確認
3. アーティファクトから詳細レポートダウンロード

##  成功事例

このワークフローシステムにより:
-  **コード品質**: 自動的に高品質なコードを維持
-  **開発効率**: Cursor IDE との完璧な統合
-  **自動化**: 手動作業の大幅削減
-  **AI活用**: Claude Code の能力を最大限活用

---

** Claude Code + GitHub Actions + Cursor IDE = 最強の開発環境**