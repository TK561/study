#!/bin/bash

# Dev Container起動スクリプト
# VS Code Dev Containers拡張機能の代替

echo "Starting Dev Container..."

# Docker Composeを使用してdev containerを起動
docker run -it --rm \
  -v "$(pwd):/workspace" \
  -v "$(pwd)/.claude:/home/vscode/.claude" \
  -w /workspace \
  -p 9222:9222 \
  -p 9223:9223 \
  --name claude-mcp-dev \
  mcr.microsoft.com/devcontainers/base:ubuntu \
  /bin/bash -c "
    # Node.jsをインストール
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
    
    # Python 3.11をインストール
    sudo apt-get update
    sudo apt-get install -y python3.11 python3-pip
    
    # MCPツールをインストール
    npm install -g @playwright/mcp figma-developer-mcp
    
    # シェルを起動
    /bin/bash
  "