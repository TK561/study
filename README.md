# 研究プロジェクト管理システム

WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価研究

## デプロイ

### Vercelでのデプロイ

1. GitHubリポジトリをVercelに接続
2. 自動的にStreamlitアプリがデプロイされます

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/TK561/study)

### ローカル実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# Streamlitアプリの起動
streamlit run streamlit_app.py
```

## 機能

- **セッション管理**: 1時間毎の作業整理システム
- **プロジェクト概要**: ファイル構造と主要ファイルの表示
- **Git状況**: リアルタイムでのGit状態確認
- **セキュリティ**: API キーの安全な管理

## 主要ファイル

- `streamlit_app.py`: Webアプリケーション
- `hourly_summary_system.py`: 作業整理システム
- `semantic_classification_system.py`: メイン分類システム
- `secure_config.py`: セキュア設定管理

## セキュリティ

- API キーは `.env` ファイルで管理
- `.gitignore` で機密ファイルを保護
- 詳細は `SECURITY.md` を参照

## 自動化機能

- 1時間毎の作業まとめ自動生成
- Git活動の自動追跡
- セッションログの自動保存