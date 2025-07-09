#!/bin/bash

echo "WSL環境でClaude Codeデータディレクトリを検索中..."

# 可能なパスを探す
paths=(
    "$HOME/.config/claude"
    "$HOME/.claude"
    "/home/*/.config/claude"
    "/home/*/.claude"
)

found=false

for path in "${paths[@]}"; do
    # ワイルドカードを展開
    for expanded_path in $path; do
        if [ -d "$expanded_path/projects" ]; then
            echo "✓ 見つかりました: $expanded_path"
            echo ""
            echo "Windows側から使用する場合のパス:"
            # WSLパスをWindowsパスに変換
            windows_path=$(echo "$expanded_path" | sed 's|/home/|\\\\wsl$\\Ubuntu\\home\\|g' | sed 's|/|\\|g')
            echo "  $windows_path"
            echo ""
            echo "PowerShellで以下のコマンドを実行してください:"
            echo "  \$env:CLAUDE_CONFIG_DIR = \"$windows_path\""
            echo ""
            echo "または、VSCode拡張機能の設定で claudeConfigPath に以下を設定:"
            echo "  $expanded_path"
            found=true
            break 2
        fi
    done
done

if [ "$found" = false ]; then
    echo "Claude Codeのデータディレクトリが見つかりませんでした。"
    echo "Claude Codeを実行したことがあるか確認してください。"
fi