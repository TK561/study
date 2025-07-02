#\!/bin/bash
echo "🔍 Claude Code復旧テスト"
echo "========================"

echo "📊 1. ファイル存在確認:"
test -f sessions/AUTO_SESSION_SAVE_2025-07-02.md && echo "✅ セッション記録" || echo "❌ セッション記録"
test -f .vscode/settings.json && echo "✅ VS Code設定" || echo "❌ VS Code設定"
test -f auto_dev_workflow.py && echo "✅ 自動化システム" || echo "❌ 自動化システム"
test -f Research_Colab_Simple.ipynb && echo "✅ 研究ノートブック" || echo "❌ 研究ノートブック"

echo ""
echo "🔧 2. コマンド動作確認:"
test -x ./research-commands.sh && echo "✅ 研究コマンド実行可能" || echo "❌ 研究コマンド問題"
test -x ./setup-shift-enter.sh && echo "✅ Shift+Enter設定実行可能" || echo "❌ Shift+Enter設定問題"

echo ""
echo "📋 3. 推奨復旧手順:"
echo "  1. ./research-commands.sh status"
echo "  2. ./setup-shift-enter.sh status"
echo "  3. npm install (必要時)"
echo "  4. npm run dev (開発サーバー起動)"

echo ""
echo "📚 4. 詳細情報:"
echo "  - セッション記録: sessions/AUTO_SESSION_SAVE_2025-07-02.md"
echo "  - 完了サマリー: SESSION_COMPLETION_SUMMARY.md"
echo "  - 研究メイン: Research_Colab_Simple.ipynb"
EOF < /dev/null
