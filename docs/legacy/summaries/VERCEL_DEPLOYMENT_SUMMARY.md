# 🚀 Vercel Deployment Summary - study-research

## プロジェクト情報
- **プロジェクト名**: `study-research` 
- **デプロイ日時**: 2025-07-02
- **アカウント**: tk561s-projects
- **ステータス**: ✅ 本番環境デプロイ完了

## 公開URL
- **メインURL**: https://study-research.vercel.app
- **代替URL**: 
  - https://study-research-tk561s-projects.vercel.app
  - https://study-research-tk561-tk561s-projects.vercel.app

## デプロイ内容
### メインページ
- `/` - 研究プロジェクトトップページ
- `/main` - メインシステム（main-system/index.html）
- `/timeline` - 実験タイムライン（experiment_timeline/index.html）
- `/discussion` - ディスカッションサイト（discussion-site/index.html）
- `/results` - 実験結果（experiment_results/index.html）

### その他の機能
- `/enhanced_features/` - 拡張機能セクション
- `/confidence_feedback/` - 信頼度フィードバックシステム
- `/pptx_systems/` - PPTXシステムインターフェース

## 設定内容（vercel.json）
```json
{
  "version": 2,
  "buildCommand": "echo 'Building study-research static site'",
  "outputDirectory": "public",
  "framework": null,
  "public": true,
  "cleanUrls": true,
  "trailingSlash": false,
  "rewrites": [
    {
      "source": "/",
      "destination": "/index.html"
    },
    {
      "source": "/main",
      "destination": "/main-system/index.html"
    },
    {
      "source": "/timeline",
      "destination": "/experiment_timeline/index.html"
    },
    {
      "source": "/discussion",
      "destination": "/discussion-site/index.html"
    },
    {
      "source": "/results",
      "destination": "/experiment_results/index.html"
    }
  ]
}
```

## 注意事項
- 静的HTMLサイトとしてデプロイ
- Pythonファイルやバックエンドコードは含まれない
- `.vercelignore`により不要ファイルは除外済み

## 更新方法
```bash
# 更新をデプロイ
npx vercel --prod

# プレビューデプロイ
npx vercel

# プロジェクト情報確認
npx vercel list
```