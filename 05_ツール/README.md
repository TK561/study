# 05_ツール

## 概要
このディレクトリには、開発・保守・自動化に使用するツールが含まれています。

## 構造
```
05_ツール/
├── tools/                   # 開発ツール
│   ├── maintenance/         # 保守ツール
│   ├── analysis/           # 分析ツール
│   └── automation/         # 自動化ツール
├── scripts/                # 自動化スクリプト
│   ├── mcp-*.js           # MCP統合スクリプト
│   ├── vercel-*.js        # Vercel関連スクリプト
│   └── research-*.js      # 研究自動化スクリプト
├── vscode-extensions/      # VS Code拡張機能
└── README.md              # このファイル
```

## 主要ツール

### 開発ツール
- **研究分析システム**: `tools/research_analysis_system.py`
- **Vercel直接デプロイ**: `tools/direct_vercel_deploy.py`
- **データ収集自動化**: 各種データ収集ツール

### 自動化スクリプト
- **MCP統合**: Model Context Protocol統合
- **Vercel統合**: デプロイ・監視・テスト自動化
- **研究支援**: 実験実行・データ分析自動化

### VS Code拡張機能
- **Claude使用量表示**: リアルタイムトークン監視
- **開発支援**: 効率的な開発環境

## 主要コマンド

### 研究自動化
```bash
# データ収集
npm run research-collect

# 実験実行
npm run research-experiment

# レポート生成
npm run research-report

# 統合実行
npm run research-master
```

### Vercel統合
```bash
# 自動デプロイ
npm run mcp-deploy

# リアルタイム監視
npm run mcp-monitor

# テスト実行
npm run mcp-test

# デバッグ
npm run mcp-debug

# 統合管理
npm run mcp-master
```

### 保守ツール
```bash
# プロジェクト整理
npm run project-organize

# ファイル整理
python tools/maintenance/包括的整理システム.py

# 直接デプロイ
python tools/direct_vercel_deploy.py
```

## 技術仕様

### 言語・環境
- **JavaScript/Node.js**: MCP・Vercel統合
- **Python**: 分析・保守ツール
- **TypeScript**: VS Code拡張機能
- **Bash**: システム管理スクリプト

### 外部サービス統合
- **Vercel API**: デプロイ・監視
- **GitHub API**: リポジトリ管理
- **MCP**: 研究自動化プロトコル

## 設定・環境変数

### 必要な環境変数
```bash
VERCEL_TOKEN=your_token_here
GITHUB_TOKEN=your_token_here
MCP_SECRET=your_secret_here
```

### 設定ファイル
- `06_設定/`内の各種設定ファイル
- `package.json`のスクリプト設定

## 使用方法

### 初期設定
```bash
# 依存関係インストール
npm install

# 環境変数設定
cp .env.example .env

# 各種ツールの設定
cd tools && python setup.py
```

### 定期実行
- 自動化スクリプトはcronジョブで定期実行可能
- CI/CDパイプラインとの統合も対応

## 注意事項
- APIキーの適切な管理
- 自動化スクリプトの監視
- ログファイルの定期的な確認