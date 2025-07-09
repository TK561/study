# 02_ウェブサイト

## 概要
このディレクトリには、研究プロジェクトのWebサイト関連ファイルが含まれています。

## 構造
```
02_ウェブサイト/
├── public/                    # 公開ファイル
│   ├── index.html            # メインページ
│   ├── main-system/          # 分類システム
│   ├── discussion-site/      # ディスカッションサイト
│   └── experiment_timeline/  # 実験タイムライン
├── assets/                   # アセットファイル
│   └── styles/              # CSS ファイル
│       └── unified_design_system.css
└── README.md                # このファイル
```

## デプロイ
- Vercel: https://study-research.vercel.app/
- 設定ファイル: `/vercel.json`
- 自動デプロイ: GitHubプッシュ時

## 開発
```bash
# ローカル開発サーバー
cd 02_ウェブサイト
python -m http.server 8000

# Vercelプレビュー
vercel dev
```