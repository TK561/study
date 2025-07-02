# 📝 textlint AI執筆チェッカー使用ガイド

## 概要
このプロジェクトでは、AI生成文章の特徴を検出し、より自然な日本語表現を促進する`textlint-rule-preset-ai-writing`を導入しています。

## 🚀 セットアップ

### 1. 依存関係のインストール
```bash
npm install
```

### 2. インストールされるツール
- **textlint**: 文章校正ツール本体
- **@textlint-ja/textlint-rule-preset-ai-writing**: AI文章検出ルール
- **textlint-rule-preset-ja-technical-writing**: 技術文書向けルール
- **textlint-filter-rule-comments**: コメント除外フィルター
- **textlint-filter-rule-allowlist**: 許可リストフィルター

## 📋 使用方法

### 基本的なチェック
```bash
# すべてのマークダウンファイルをチェック
npm run lint

# 自動修正を適用
npm run lint:fix

# セッションファイルのみチェック
npm run lint:sessions

# ドキュメントのみチェック
npm run lint:docs
```

### 高度な使用方法
```bash
# カスタムチェックスクリプト
npm run check-writing

# ヘルプを表示
node scripts/check-writing.js --help

# 特定のファイルをチェック
node scripts/check-writing.js README.md

# セッションファイルを自動修正
node scripts/check-writing.js --sessions --fix
```

## 🔍 検出されるパターン

### 1. AI特有のリストフォーマット (no-ai-list-formatting)
機械的に見えるリスト項目のパターンを検出:
- 過度に整形されたリスト
- 機械的な番号付け

### 2. 誇張表現 (no-ai-hype-expressions)
過度に誇張された言語を検出:
- 絶対的・完全性を示す表現
- 抽象的・感覚的な効果の言語
- 権威的・予測的な声明

### 3. 機械的な強調パターン (no-ai-emphasis-patterns)
AIが生成しがちな強調パターンを特定

### 4. 技術文書ガイドライン (ai-tech-writing-guideline)
技術文書のベストプラクティスに基づく改善提案:
- 簡潔性
- 能動態の使用
- 具体的な表現
- 一貫した用語使用
- 文書構造

## ⚙️ 設定ファイル

### .textlintrc.json
```json
{
  "rules": {
    "@textlint-ja/preset-ai-writing": true,
    "preset-ja-technical-writing": {
      "sentence-length": {
        "max": 100
      },
      "no-exclamation-question-mark": false,
      "ja-no-weak-phrase": false,
      "ja-no-successive-word": {
        "allowOnomatopee": true
      }
    }
  },
  "filters": {
    "comments": true,
    "allowlist": {
      "allow": [
        "/\\bAI\\b/",
        "/\\bClaude\\b/",
        "/\\bVercel\\b/",
        "/\\bColab\\b/",
        "/\\bGoogle\\b/",
        "/\\bGitHub\\b/"
      ]
    }
  }
}
```

### .textlintignore
チェック対象外のファイルを指定:
- node_modules/
- public/
- dist/
- *.ipynb
- 画像ファイル
- バイナリファイル

## 💡 活用のヒント

### 1. 定期的なチェック
コミット前に文章チェックを実行することで、品質を保つことができます。

### 2. CI/CD統合
```yaml
# GitHub Actions例
- name: Run textlint
  run: npm run lint
```

### 3. VS Code統合
textlint拡張機能をインストールすることで、リアルタイムでチェックできます。

### 4. カスタムルール追加
プロジェクト固有のルールを追加する場合は、`.textlintrc.json`を編集します。

## 🎯 目的

1. **品質向上**: より自然で読みやすい文章へ
2. **一貫性**: プロジェクト全体で統一された文体
3. **効率化**: 自動修正による作業時間短縮
4. **学習**: AIが生成しがちなパターンの理解

## 📚 参考リンク

- [textlint公式ドキュメント](https://textlint.github.io/)
- [textlint-rule-preset-ai-writing](https://github.com/textlint-ja/textlint-rule-preset-ai-writing)
- [textlint-rule-preset-ja-technical-writing](https://github.com/textlint-ja/textlint-rule-preset-ja-technical-writing)