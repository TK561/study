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