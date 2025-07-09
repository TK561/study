# 包括的セットアップガイド

## 🚀 クイックスタート

### 1. 基本環境セットアップ

```bash
# Node.js依存関係のインストール
npm install

# Vercel CLIのインストール
npm install -g vercel

# MCPサーバーの起動
npm run mcp-server
```

### 2. Claude MCP設定

```json
{
  "mcpServers": {
    "research-automation": {
      "command": "node",
      "args": ["scripts/mcp-research-master.js"]
    },
    "vercel-integration": {
      "command": "node", 
      "args": ["scripts/mcp-vercel-master.js"]
    }
  }
}
```

### 3. Vercel設定

```bash
# Vercelログイン
vercel login

# プロジェクトリンク
vercel link

# 本番デプロイ
vercel --prod
```

## 📋 利用可能なコマンド

### 研究自動化
- `npm run research-collect` - データ収集
- `npm run research-experiment` - 実験実行
- `npm run research-report` - レポート生成
- `npm run research-master` - 統合実行

### Vercel統合
- `npm run mcp-deploy` - 自動デプロイ
- `npm run mcp-monitor` - リアルタイム監視
- `npm run mcp-test` - テスト実行
- `npm run mcp-debug` - デバッグ
- `npm run mcp-master` - 統合管理

### システム管理
- `npm run project-organize` - プロジェクト整理
- `npm run maintenance` - メンテナンス実行

## 🔧 設定ファイル

### vercel.json
```json
{
  "version": 2,
  "public": true,
  "builds": [{"src": "**/*", "use": "@vercel/static"}],
  "routes": [
    {"src": "/", "dest": "/index.html"},
    {"src": "/main-system", "dest": "/public/main-system/index.html"},
    {"src": "/discussion-site", "dest": "/public/discussion-site/index.html"},
    {"src": "/experiment_timeline", "dest": "/public/experiment_timeline/index.html"}
  ]
}
```

### .mcp.json
```json
{
  "server": {
    "host": "localhost",
    "port": 3000
  },
  "features": {
    "research_automation": true,
    "vercel_integration": true,
    "real_time_monitoring": true
  }
}
```

## 📊 利用可能なツール

### 研究ツール
- **研究分析システム**: `python 05_ツール/tools/research_analysis_system.py`
- **データ収集**: MCPスクリプト統合
- **実験実行**: 自動化パイプライン

### デプロイツール
- **Vercel統合**: 完全自動化
- **リアルタイム監視**: ダッシュボード
- **テスト自動化**: 品質保証

### メンテナンスツール
- **プロジェクト整理**: 自動整理システム
- **ファイル統合**: 重複排除
- **フォルダ構造最適化**: 構造改善

## 🎯 主要機能

### 1. MCP統合自動化システム
- Model Context Protocol完全対応
- リアルタイム研究支援
- 自動レポート生成

### 2. Vercel統合管理
- 自動デプロイパイプライン
- リアルタイム監視
- 品質保証テスト

### 3. 研究支援システム
- データ収集自動化
- 実験実行管理
- 結果分析支援

## 🔍 トラブルシューティング

### よくある問題
1. **MCP接続エラー**: サーバー再起動 `npm run mcp-server`
2. **Vercelデプロイ失敗**: 認証確認 `vercel login`
3. **依存関係エラー**: 再インストール `npm install`

### ログ確認
```bash
# MCPログ
tail -f logs/mcp-server.log

# Vercelログ
vercel logs

# システムログ
npm run logs
```

## 📈 パフォーマンス最適化

### 推奨設定
- Node.js: v18以上
- NPM: v9以上
- Memory: 8GB以上
- Storage: 5GB以上

### 最適化コマンド
```bash
# キャッシュクリア
npm cache clean --force

# 不要ファイル削除
npm run cleanup

# パフォーマンス測定
npm run performance-test
```

## 🛡️ セキュリティ

### 環境変数設定
```bash
# .env.local
VERCEL_TOKEN=your_token_here
MCP_SECRET=your_secret_here
```

### アクセス制御
- Vercelプロジェクト: 認証必須
- MCPサーバー: ローカルアクセスのみ
- 研究データ: 暗号化保存

## 📞 サポート

### 問題報告
- GitHub Issues: プロジェクトリポジトリ
- MCP統合: `npm run mcp-support`
- Vercel問題: `vercel help`

### ドキュメント
- MCP使用方法: `MCP_RESEARCH_AUTOMATION_GUIDE.md`
- Vercel統合: `MCP_VERCEL_USAGE.md`
- 研究方法論: `03_研究資料/実験方針/`

---

*このガイドは統合された包括的なセットアップガイドです。*