#!/bin/bash
# Shift+Enter改行設定スクリプト

echo "⌨️ Shift+Enter改行設定スクリプト"
echo "================================"

case "$1" in
    "vscode")
        echo "🔧 VS Code用設定を適用します..."
        
        # .vscode ディレクトリ作成
        mkdir -p .vscode
        
        # settings.json 設定
        cat > .vscode/settings.json << 'EOF'
{
    "terminal.integrated.commandsToSkipShell": [
        "workbench.action.terminal.sendSequence"
    ],
    "terminal.integrated.allowChords": false,
    "terminal.integrated.enableMultiLinePasteWarning": false,
    "terminal.integrated.rightClickBehavior": "paste",
    "claude.terminal.multilineInput": true,
    "claude.terminal.submitOnEnter": true,
    "claude.terminal.newlineOnShiftEnter": true
}
EOF
        
        # keybindings.json 設定
        cat > .vscode/keybindings.json << 'EOF'
[
    {
        "key": "shift+enter",
        "command": "workbench.action.terminal.sendSequence",
        "args": {"text": "\n"},
        "when": "terminalFocus"
    },
    {
        "key": "enter",
        "command": "workbench.action.terminal.sendSequence", 
        "args": {"text": "\r"},
        "when": "terminalFocus && !suggestWidgetVisible"
    }
]
EOF
        
        echo "✅ VS Code設定ファイルを作成しました:"
        echo "  - .vscode/settings.json"
        echo "  - .vscode/keybindings.json"
        echo ""
        echo "📋 VS Codeを再起動して設定を反映してください"
        ;;
        
    "generic")
        echo "🔧 汎用ターミナル設定を適用します..."
        
        # .inputrc 設定
        if [ ! -f ~/.inputrc ]; then
            touch ~/.inputrc
        fi
        
        # Shift+Enter設定を追加（重複チェック）
        if ! grep -q "27;2;13" ~/.inputrc; then
            echo '"\e[27;2;13~": "\n"  # Shift+Enter for newline' >> ~/.inputrc
            echo "✅ ~/.inputrc に Shift+Enter設定を追加しました"
        else
            echo "ℹ️ ~/.inputrc に既に設定があります"
        fi
        
        # .bashrc設定
        if [ -f ~/.bashrc ]; then
            if ! grep -q "bind.*27;2;13" ~/.bashrc; then
                echo 'bind '"'"'"\e[27;2;13~": "\n"'"'"' # Shift+Enter' >> ~/.bashrc
                echo "✅ ~/.bashrc にbind設定を追加しました"
            else
                echo "ℹ️ ~/.bashrc に既に設定があります"
            fi
        fi
        
        echo ""
        echo "📋 設定を反映するには:"
        echo "  source ~/.bashrc"
        echo "  または新しいターミナルセッションを開始"
        ;;
        
    "test")
        echo "🧪 Shift+Enter設定テストを実行します..."
        echo ""
        echo "以下をテストしてください:"
        echo "1. 'echo \"line1\"' と入力"
        echo "2. Shift+Enter を押す（改行のみ）"
        echo "3. 'echo \"line2\"' と入力" 
        echo "4. Enter を押す（実行）"
        echo ""
        echo "期待される結果:"
        echo "line1"
        echo "line2"
        echo ""
        echo "実際にテストを実行しますか？ [y/N]"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo ""
            echo "📝 以下のコマンドを入力してテストしてください:"
            echo "echo \"Test line 1\""
            echo "（ここでShift+Enterを押してください）"
            echo "echo \"Test line 2\""
            echo "（ここでEnterを押してください）"
        fi
        ;;
        
    "claude")
        echo "🤖 Claude Code用設定を適用します..."
        
        # Claude Code用設定
        mkdir -p .vscode
        
        # 既存の設定を読み込んで追加
        if [ -f .vscode/settings.json ]; then
            # バックアップ作成
            cp .vscode/settings.json .vscode/settings.json.backup
            echo "📄 既存設定のバックアップを作成しました"
        fi
        
        cat > .vscode/settings.json << 'EOF'
{
    "claude.terminal.multilineInput": true,
    "claude.terminal.submitOnEnter": true,
    "claude.terminal.newlineOnShiftEnter": true,
    "claude.terminal.enableSmartNewlines": true,
    "terminal.integrated.commandsToSkipShell": [
        "workbench.action.terminal.sendSequence"
    ],
    "terminal.integrated.allowChords": false,
    "terminal.integrated.enableMultiLinePasteWarning": false
}
EOF
        
        echo "✅ Claude Code用設定を適用しました"
        echo "📋 Claude Code拡張機能を再読み込みしてください"
        ;;
        
    "status")
        echo "📊 現在のShift+Enter設定状況:"
        echo ""
        
        # VS Code設定チェック
        if [ -f .vscode/settings.json ]; then
            echo "✅ VS Code設定ファイル存在"
            if grep -q "shift+enter" .vscode/keybindings.json 2>/dev/null; then
                echo "✅ VS Code キーバインド設定済み"
            else
                echo "⚠️ VS Code キーバインド未設定"
            fi
        else
            echo "❌ VS Code設定ファイル未作成"
        fi
        
        # システム設定チェック
        if grep -q "27;2;13" ~/.inputrc 2>/dev/null; then
            echo "✅ システム inputrc設定済み"
        else
            echo "⚠️ システム inputrc設定未完了"
        fi
        
        if grep -q "bind.*27;2;13" ~/.bashrc 2>/dev/null; then
            echo "✅ Bash bind設定済み"
        else
            echo "⚠️ Bash bind設定未完了"
        fi
        ;;
        
    *)
        echo "使用方法:"
        echo "  $0 vscode   - VS Code用設定"
        echo "  $0 generic  - 汎用ターミナル設定"
        echo "  $0 claude   - Claude Code用設定"
        echo "  $0 test     - 設定テスト"
        echo "  $0 status   - 設定状況確認"
        echo ""
        echo "推奨: まず 'status' で現在の状況を確認してください"
        ;;
esac