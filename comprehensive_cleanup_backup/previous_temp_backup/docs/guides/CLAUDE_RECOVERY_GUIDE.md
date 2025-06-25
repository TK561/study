# Claude Code セッション復元ガイド

## 概要
Claude Codeが予期せず終了した場合でも、作業内容を復元できるシステムです。

## 復元方法

### 1. 簡単な復元（推奨）
```bash
python3 recover_claude_session.py
```

### 2. 状態確認
```bash
# 現在のセッション状態
python3 recover_claude_session.py status

# 詳細レポート表示
python3 recover_claude_session.py report

# バックアップ一覧
python3 recover_claude_session.py list
```

### 3. Python内から復元
```python
from session_recovery_system import recover
report = recover()
```

## 自動保存される内容

1. **ファイル操作**
   - 作成・編集したファイルのパス
   - 小さいファイルは内容も保存
   - 大きいファイルはハッシュ値を記録

2. **コマンド実行**
   - 実行したコマンド
   - 出力結果（5000文字まで）

3. **Git状態**
   - 変更ファイル一覧
   - 差分情報

## 保存場所
- セッションデータ: `/mnt/c/Desktop/Research/.claude_sessions/`
- 現在のセッション: `current_session.json`
- バックアップ: `backups/` フォルダ内

## 自動バックアップ
- 10アクションごとに自動バックアップ
- 手動バックアップ: `python3 recover_claude_session.py backup`

## 復元後の確認
1. `recovery_report.md` - 復元レポート
2. `recover_session.sh` - 復元用スクリプト（必要に応じて）

## 注意事項
- 大きなファイル（10KB以上）の内容は保存されません
- コマンド出力は5000文字まで
- センシティブな情報（パスワード等）は記録しないよう注意

## トラブルシューティング

### セッションが見つからない場合
```bash
# バックアップから復元
ls /mnt/c/Desktop/Research/.claude_sessions/backups/
```

### 手動で特定のバックアップを復元
```python
import json
with open('/path/to/backup.json', 'r') as f:
    session = json.load(f)
# sessionの内容を確認
```