# 06_設定

## 概要
このディレクトリには、プロジェクトの各種設定ファイルが含まれています。

## 構造
```
06_設定/
├── mcp/                     # MCP設定
│   └── .mcp.json           # MCP サーバー設定
├── devcontainer/           # 開発コンテナ設定
│   └── devcontainer.json  # VS Code Dev Container設定
├── deployment/             # デプロイ設定
└── README.md              # このファイル
```

## 設定ファイルの説明

### MCP設定
- `.mcp.json`: Model Context Protocol サーバー設定
- 研究自動化とVercel統合のためのMCP設定

### 開発コンテナ設定
- `devcontainer.json`: VS Code Dev Container設定
- 開発環境の統一化とポータビリティの確保

### デプロイ設定
- Vercel, GitHub Actions等のデプロイ関連設定
- 本番環境とステージング環境の設定

## 使用方法
各設定ファイルはプロジェクトルートからシンボリックリンクで参照されるか、各ツールが直接参照します。