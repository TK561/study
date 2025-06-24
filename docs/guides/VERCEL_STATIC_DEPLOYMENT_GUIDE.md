# Vercel 静的サイトデプロイメントガイド

## 🎯 推奨方法：静的HTMLサイトとしてデプロイ

### なぜ静的HTMLが推奨か
- **Python Runtimeの問題を完全回避**
- **高速な配信**（サーバーレス関数のオーバーヘッドなし）
- **100%の稼働率**（ランタイムエラーなし）
- **簡単なメンテナンス**

## 📁 推奨ディレクトリ構造

```
project/
├── public/
│   └── index.html      # メインページ
├── vercel.json         # 最小構成
└── .gitignore
```

## 🚀 デプロイ手順

### 1. HTMLファイルを準備

```bash
# publicディレクトリ作成
mkdir -p public

# HTMLファイルを配置
# public/index.html にコンテンツを作成
```

### 2. vercel.json を最小構成に

```json
{
  "version": 2
}
```

### 3. Gitにコミット＆プッシュ

```bash
git add -A
git commit -m "静的サイトとしてデプロイ"
git push origin main
```

### 4. 直接APIデプロイ（オプション）

```bash
python3 direct_vercel_deploy.py
```

## ⚠️ 注意事項

### Python APIを使わない
- `api/` ディレクトリは作成しない
- `BaseHTTPRequestHandler` は使用しない
- サーバーサイド処理が必要な場合はNext.jsかNode.jsを検討

### HTMLテンプレート例

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タイトル</title>
    <style>
        /* CSSはそのまま記述可能 */
        body {
            font-family: sans-serif;
        }
    </style>
</head>
<body>
    <h1>コンテンツ</h1>
    <script>
        // JavaScriptで動的な要素を追加
        document.addEventListener('DOMContentLoaded', function() {
            // 動的コンテンツ
        });
    </script>
</body>
</html>
```

## 🔧 トラブルシューティング

### デプロイが反映されない場合
1. Vercelダッシュボードで「Redeploy」をクリック
2. ブラウザのキャッシュをクリア
3. 2-3分待つ

### 404エラーが出る場合
- `public/index.html` が存在することを確認
- ファイルパスが正しいか確認
- vercel.jsonに余計な設定がないか確認

## 📝 まとめ

静的HTMLサイトとしてデプロイすることで：
- ✅ Python Runtimeエラーを完全回避
- ✅ 高速で安定した配信
- ✅ シンプルなメンテナンス
- ✅ 100%の稼働率

今後はこの方法でデプロイすることを強く推奨します。

---
**作成日**: 2025年6月23日  
**管理**: Claude Code システム