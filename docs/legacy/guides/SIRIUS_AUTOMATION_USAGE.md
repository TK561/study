# 🚀 Sirius Template式自動化システム使用ガイド

## 📋 概要
Sirius TemplateのCLAUDE.mdから抽出したAI駆動の完全自動化開発フローを実装しました。

## 🎯 主要機能

### 1. **全自動TDD開発フロー**
AI主導による体系的な開発サイクル:
- Issue作成 → ブランチ生成 → テスト実装 → コード実装 → 継続的テスト・レビュー

### 2. **多段階AI自動レビュー**
複数のAIモデルによる包括的なコードレビュー:
- Claude, Gemini, OpenAI による多角的な品質チェック
- 問題が見つからなくなるまで継続的レビュー

### 3. **包括的自動テスト**
- UI Unit Testing
- API Unit Testing  
- Integration Testing
- E2E Black Box Testing

### 4. **自動デプロイメント準備**
- Lint & 型チェック解決
- 包括的テストカバレッジ検証
- 自動環境設定

## 🚀 使用方法

### クイックスタート
```bash
# 依存関係インストール
npm install

# GitHub Actions自動化設定
npm run auto:setup

# 自動開発ワークフロー状態確認
npm run auto:status

# フィーチャー開発の自動実行
npm run auto:dev -- --feature="新機能名" --description="機能説明"
```

### 手動実行
```bash
# 自動開発ワークフロー実行
python3 auto_dev_workflow.py run --feature="authentication" --description="ユーザー認証機能"

# ワークフロー状態確認
python3 auto_dev_workflow.py status

# 設定確認
python3 auto_dev_workflow.py config
```

## 🔧 自動化フロー詳細

### 1. フィーチャーブランチ自動作成
```bash
# main/developブランチから自動分岐
feature/[機能名]
```

### 2. 自動テストサイクル
```bash
# UIユニットテスト
npm test || npm run test:unit

# APIユニットテスト  
python -m pytest tests/ || npm run test:api

# 統合テスト
npm run test:integration

# E2Eテスト
npx playwright test || npx cypress run
```

### 3. 自動品質チェック
```bash
# Lintチェック + 自動修正
npm run lint && npm run lint:fix

# 型チェック
npm run type-check || npx tsc --noEmit

# textlintチェック
npm run lint
```

### 4. カバレッジ検証
```bash
# テストカバレッジチェック（閾値: 80%）
npm run test:coverage
```

### 5. 自動ドキュメント更新
```bash
# API文書生成
npm run docs:generate

# README更新（最終更新日自動追加）
# 自動的に実行
```

### 6. プルリクエスト自動作成
```bash
# GitHub CLI使用
gh pr create --title "feat: [機能名]" --body "[説明]"
```

## 🤖 GitHub Actions統合

### 作成されるワークフロー

#### 1. **auto-tdd.yml** - 自動TDD開発サイクル
- **トリガー**: `develop`, `feature/*` ブランチへのpush
- **実行内容**:
  - 依存関係インストール
  - textlintチェック
  - 全テストスイート実行
  - 型チェック・ビルドチェック
  - 自動ドキュメント更新
  - Vercelデプロイ（mainブランチ）

#### 2. **ai-review.yml** - AI自動レビュー
- **トリガー**: プルリクエスト作成・更新
- **実行内容**:
  - 多段階AIレビュー
  - コード品質チェック
  - テストカバレッジ確認
  - ドキュメントチェック
  - レビューレポート生成

#### 3. **deployment.yml** - デプロイ自動化
- **トリガー**: mainブランチへのpush
- **実行内容**:
  - デプロイ前総合チェック
  - Vercelデプロイ
  - 環境設定更新
  - デプロイ後ドキュメント更新

#### 4. **monitoring.yml** - 定期監視・レポート
- **トリガー**: 9:00, 15:00, 21:00の定期実行
- **実行内容**:
  - ファイル自動整理
  - textlint定期チェック
  - 日次レポート生成
  - システムヘルスチェック
  - 自動的な変更コミット

## ⚙️ 設定ファイル

### auto_dev_config.json
```json
{
  "workflow_enabled": true,
  "auto_testing": {
    "ui_unit_tests": true,
    "api_unit_tests": true,
    "integration_tests": true,
    "e2e_tests": true
  },
  "auto_review": {
    "enabled": true,
    "ai_models": ["claude", "gemini", "openai"],
    "review_cycles": 3
  },
  "auto_deployment": {
    "lint_check": true,
    "type_check": true,
    "test_coverage_threshold": 80
  },
  "github_integration": {
    "auto_issue_creation": true,
    "auto_branch_creation": true,
    "auto_pr_creation": true
  }
}
```

## 🔑 必要な設定

### GitHub Secrets
```bash
# Vercelトークンを追加
VERCEL_TOKEN=your_vercel_token_here
```

### Repository設定
1. **Actions有効化**: Settings → Actions → Allow all actions
2. **Branch protection**: mainブランチの保護ルール設定
3. **Auto-merge**: プルリクエストの自動マージ設定（オプション）

## 💡 使用例とワークフロー

### 新機能開発の完全自動化
```bash
# 1. 新機能開発開始
npm run auto:dev -- --feature="user-dashboard" --description="ユーザーダッシュボード機能"

# 2. 以下が自動実行される:
#    - feature/user-dashboard ブランチ作成
#    - 各種テスト実行
#    - コード品質チェック
#    - ドキュメント更新
#    - プルリクエスト作成

# 3. GitHub Actionsで自動レビュー・デプロイ
```

### チーム開発での活用
1. **開発者**がフィーチャー開発開始
2. **AI**が自動でテスト・レビュー実行  
3. **GitHub Actions**が品質保証
4. **自動デプロイ**で本番反映
5. **定期監視**で継続的品質管理

## 📊 ログ・レポート

### 生成されるログ
- `workflow_log.json` - ワークフロー実行ログ
- `auto_dev.log` - 詳細実行ログ
- `review_report.json` - AIレビュー結果

### 監視ダッシュボード
- ワークフロー実行状況
- テストカバレッジ推移
- 品質指標トレンド
- 自動修正統計

## 🛠️ トラブルシューティング

### よくある問題

#### GitHub Actions失敗
```bash
# ローカルで事前チェック
npm run lint
npm test
npm run build
```

#### 権限エラー
```bash
# 実行権限付与
chmod +x *.py *.sh
```

#### Python依存関係エラー
```bash
# 必要パッケージインストール
pip install pyyaml schedule
```

## 📚 参考情報

### コマンド一覧
- `npm run auto:dev` - 自動開発ワークフロー実行
- `npm run auto:status` - システム状態確認
- `npm run auto:setup` - GitHub Actions設定
- `python3 auto_dev_workflow.py status` - 詳細状態表示

### 拡張カスタマイズ
- 設定ファイル編集で動作カスタマイズ
- GitHub Actions YAMLファイル編集で CI/CD カスタマイズ
- 新しいテストフレームワークの追加対応

この自動化システムにより、Sirius Template方式の AI駆動完全自動開発フローが実現されます。