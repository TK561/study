#!/bin/bash
# textlint Git hooks セットアップスクリプト

echo "🔧 textlint Git hooksをセットアップします..."

# pre-commitフック
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# textlint pre-commit hook

echo "🔍 textlintでコミット前チェックを実行中..."

# ステージングされたマークダウンファイルを取得
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|txt)$')

if [ -z "$STAGED_FILES" ]; then
    echo "✅ チェック対象のファイルがありません"
    exit 0
fi

# textlintを実行
echo "対象ファイル:"
echo "$STAGED_FILES" | sed 's/^/  - /'
echo ""

npx textlint $STAGED_FILES

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ textlintエラーが検出されました"
    echo "修正方法:"
    echo "  1. 手動で修正する"
    echo "  2. npm run lint:fix で自動修正"
    echo ""
    echo "修正後、再度 git add してコミットしてください"
    exit 1
fi

echo "✅ textlintチェック完了！"
EOF

# pre-pushフック
cat > .git/hooks/pre-push << 'EOF'
#!/bin/sh
# textlint pre-push hook

echo "🚀 プッシュ前の最終チェック..."

# すべてのマークダウンファイルをチェック
npx textlint '**/*.md' '**/*.txt' --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️ 警告: textlintで問題が検出されました"
    echo "プッシュは続行されますが、修正を検討してください"
    echo ""
fi

exit 0
EOF

# commit-msgフック（コミットメッセージもチェック）
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/sh
# textlint commit-msg hook

COMMIT_MSG_FILE=$1
TEMP_FILE=$(mktemp)

# コミットメッセージを一時ファイルにコピー
cp "$COMMIT_MSG_FILE" "$TEMP_FILE.md"

# textlintでコミットメッセージをチェック
npx textlint "$TEMP_FILE.md" --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "💡 ヒント: コミットメッセージにも改善できる点があります"
fi

# 一時ファイルを削除
rm -f "$TEMP_FILE.md"

exit 0
EOF

# 実行権限を付与
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
chmod +x .git/hooks/commit-msg

echo "✅ Git hooksのセットアップが完了しました！"
echo ""
echo "設定されたフック:"
echo "  - pre-commit: コミット前に変更ファイルをチェック"
echo "  - pre-push: プッシュ前に全ファイルをチェック"
echo "  - commit-msg: コミットメッセージをチェック"
echo ""
echo "無効化する場合:"
echo "  rm .git/hooks/pre-commit"
echo "  rm .git/hooks/pre-push"
echo "  rm .git/hooks/commit-msg"