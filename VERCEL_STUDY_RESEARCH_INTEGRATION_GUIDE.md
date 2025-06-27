# 🌐 Vercel study-research統合デプロイ手順

## 📋 統合概要
- **統合前**: study-research-final.vercel.app (独立プロジェクト)
- **統合後**: study-research.vercel.app/research/ (サブディレクトリ統合)

## 🚀 デプロイ手順

### 1. 事前準備
```bash
# Google Drive/Colab環境で実行
cd /content/drive/MyDrive/research
```

### 2. 統合設定の適用
```bash
# 統合後のpublic/構造を使用
cp -r public_integrated/* public/

# 統合vercel.json設定を適用
cp web_deployment/vercel.json ./vercel.json
```

### 3. Vercelプロジェクト設定更新
```bash
# Vercel CLI経由でプロジェクト名変更
vercel --name study-research

# または新規プロジェクトとして作成
vercel --name study-research --force
```

### 4. ドメイン設定
```bash
# 既存ドメインの更新
vercel domains add study-research.vercel.app

# 古いドメインからのリダイレクト設定
vercel alias study-research-final.vercel.app study-research.vercel.app
```

### 5. デプロイ実行
```bash
# 本番デプロイ
vercel --prod --yes
```

### 6. 動作確認
```bash
# 主要URLの確認
curl -I https://study-research.vercel.app/
curl -I https://study-research.vercel.app/research/
curl -I https://study-research.vercel.app/research/main-system/
```

## 🔧 トラブルシューティング

### ドメイン競合の場合
```bash
# 一意なプロジェクト名を使用
vercel --name study-research-unified

# カスタムドメインの設定
vercel domains add your-custom-domain.com
```

### ルーティングエラーの場合
```bash
# vercel.json設定確認
cat vercel.json

# キャッシュクリア後再デプロイ
vercel --force --prod
```

## 📊 統合後のURL構造

### メインサイト
- `https://study-research.vercel.app/` - 統合ランディングページ

### 研究セクション
- `https://study-research.vercel.app/research/` - WordNet研究メイン
- `https://study-research.vercel.app/research/main-system/` - 分類システム
- `https://study-research.vercel.app/research/confidence-feedback/` - 信頼度システム
- `https://study-research.vercel.app/research/pptx-systems/` - プレゼンシステム
- `https://study-research.vercel.app/research/enhanced-features/` - 拡張機能

### レガシーURL（自動リダイレクト）
- `/main-system/` → `/research/main-system/`
- `/confidence_feedback/` → `/research/confidence-feedback/`
- `/pptx_systems/` → `/research/pptx-systems/`

## 🎯 統合後の利点

1. **統一ブランディング**: 単一study-researchブランド
2. **SEO最適化**: 統合ドメインでの権威性向上  
3. **管理効率化**: プロジェクト統合による運用簡素化
4. **拡張性**: 将来の研究プロジェクト追加容易

---
生成日時: 2025年06月27日 10:33:55
