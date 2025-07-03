# プロジェクト構造 (整理後)

## ルートディレクトリ
- `CLAUDE.md` - Claude Code設定ファイル
- `README.md` - プロジェクト説明
- `SECURITY.md` - セキュリティガイドライン
- `requirements.txt` - Python依存関係
- `vercel.json` - Vercel設定

## 自動化システム
- `hourly_summary_system.py` - 1時間毎作業整理システム
- `start_hourly_system.py` - システム起動スクリプト
- `research_git_automation.py` - Git自動化システム
- `secure_config.py` - セキュア設定管理
- `notification_test.py` - 通知機能テスト

## Vercel API
- `api/index.py` - メインWebページ
- `api/status.py` - ステータスAPI

## 研究資料
- `study/` - 研究プロジェクトフォルダ
  - `README.md` - 研究プロジェクト説明
  - `requirements.txt` - 研究用依存関係
  - `Meaning category-based classification system centered on WordNet.pdf` - 研究論文
  - `references/` - 参考資料・プレゼンテーション
  - `analysis/results/` - 分析結果

## 削除したファイル・フォルダ
- `semantic_classification/` (重複)
- `config.example.py` (古い設定)
- `study/lecture_materials/` (大容量学習ファイル)
- `study/models/` (大容量モデルファイル)
- `study/output/` (出力ファイル群)
- `study/images/` `study/images_test/` (テスト画像)
- `study/analysis/` 内の一時ファイル群
- 各種 `.bat` ファイル群

## プロジェクトサイズ削減効果
- 大容量ファイル削除により軽量化
- 重複フォルダ削除により構造簡素化
- Vercelデプロイ対象を最小化