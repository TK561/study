# Claude Code 設定ファイル

## 🚨 Vercelデプロイメント重要事項
**Python APIハンドラーは使用しないでください。静的HTMLサイトとしてデプロイしてください。**

詳細は以下を参照：
- `VERCEL_STATIC_DEPLOYMENT_GUIDE.md` - 静的サイトデプロイガイド
- `VERCEL_ERROR_KNOWLEDGE_BASE.md` - エラー対策集
- `VERCEL_UPDATE_HISTORY.json` - 更新履歴（自動保存）

### Vercel更新履歴の自動保存
デプロイ時に自動的に以下の情報が保存されます：
- バージョン番号
- デプロイID
- 変更内容
- 更新ファイル
- デプロイ時刻

履歴確認方法：
```bash
python3 vercel_update_tracker.py
```

### Vercelデプロイメント管理
成功パターンの記録と失敗時の修正：

#### 📊 成功パターン記録
- `VERCEL_SUCCESS_PATTERNS.json` - 成功したデプロイの再現情報
- 成功理由と再現手順を自動記録
- 類似パターンの検索機能

#### 🔧 エラー時の自動修正
```bash
# 対話的修正
python3 vercel_fix_assistant.py

# 静的HTMLに即座修正
python3 vercel_fix_assistant.py --fix static_html

# バックアップから復元
python3 vercel_fix_assistant.py --rollback 20241223_171500
```

#### 💾 自動バックアップ
- デプロイ前に自動バックアップ作成
- `.vercel_backups/` に保存
- ロールバック機能搭載

### 🚀 Vercel × Gemini AI統合システム
**最高のユーザー満足度を実現する包括的なデプロイメントシステム**

#### 🎯 スマートデプロイ
```bash
# AI支援付きデプロイ（推奨）
python3 vercel_unified_system.py deploy
```

#### 🧠 AI機能
- Gemini AIによる成功率予測
- 自動最適化提案
- ユーザー満足度追跡
- 学習型エラー修復

#### 📊 統合ダッシュボード
```bash
python3 vercel_unified_system.py dashboard
```

#### 🔧 主要機能
1. **環境診断**: 健全性スコア自動計算
2. **AI分析**: Geminiによる詳細分析
3. **自動最適化**: 構成の自動調整
4. **インテリジェントバックアップ**: 失敗時自動復元
5. **満足度追跡**: フィードバック収集と改善

詳細は `VERCEL_INTEGRATION_GUIDE.md` を参照

## 自動復元機能
Claude Code起動時に前回のセッションを自動的に検出・復元します。

### 有効化方法
```bash
python3 claude_auto_restore.py enable
```

### 起動時の自動実行
Claude Code起動時に以下を実行してください：
```python
from claude_auto_restore import claude_startup
claude_startup()
```

## セッション管理
- 自動保存: すべての操作を記録
- 自動バックアップ: 10アクションごと
- 異常終了検出: 5分以上更新がない場合

## 復元オプション
1. 自動復元（5秒後）
2. 手動で選択
3. レポート確認後に決定

## ファイルの場所
- セッションデータ: `.claude_sessions/`
- 復元レポート: `auto_recovery_report.md`
- バックアップ: `.claude_sessions/backups/`