# 1時間毎自動レポートシステム

Claude Code起動時に自動開始される研究活動追跡システムです。

## システム概要

### 自動実行機能
- **トリガー**: Claude Code起動時
- **実行間隔**: 1時間毎
- **動作方式**: バックグラウンドデーモン
- **ログ保存**: `session_logs/session_YYYYMMDD_HHMMSS.json`

### レポート内容
- ファイル変更追跡: 新規作成・更新ファイル一覧
- Git活動記録: コミット・ブランチ状況
- 作業時間計測: セッション開始からの経過時間
- 進捗サマリー: 完了タスクと次のステップ

## システム構成

```
hourly_system/
├── session_logs/          # セッションログ（自動生成）
├── simple_hourly_system.py    # メインシステム
├── claude_code_startup.py     # 自動起動スクリプト
├── enhanced_hourly_daemon.py  # 拡張デーモン
├── start_hourly_system.py     # システム起動
├── HOURLY_SYSTEM_MANUAL.md    # 詳細マニュアル
└── QUICK_START_GUIDE.md       # クイックスタートガイド
```

## 動作確認

### システム状態確認
```bash
cat session_logs/current_session.json
```

### デーモン制御
```bash
python enhanced_hourly_daemon.py --daemon  # 起動
python enhanced_hourly_daemon.py --stop    # 停止
```

## 自動初期化

Claude Code起動時に以下が自動実行されます：

- 1時間毎レポートシステム自動起動
- プロジェクト検出・環境設定  
- セッション管理開始
- Git活動追跡開始

## 機能詳細

### 安全停止機能
- VSCode/ターミナル終了検知
- 予期しない終了時の安全停止
- セッション状態の自動保存

### 復旧機能
- セッション中断からの自動復旧
- 復旧レポートの自動生成
- 作業継続性の確保

## 設定・カスタマイズ

システムの設定は各スクリプト内で行えます。主な設定項目：

- レポート生成間隔
- ログ保存期間
- 監視対象ディレクトリ
- Git追跡設定

## トラブルシューティング

### よくある問題
1. システムが起動しない
   - Python環境の確認
   - 権限設定の確認

2. ログが生成されない
   - ディスク容量の確認
   - ログディレクトリの権限確認

3. 自動停止しない
   - プロセス手動終了: `pkill -f simple_hourly_system`

## 使用上の注意

- 研究専用システムのため、機密情報は自動記録対象外
- システムは研究活動のみを追跡
- 手動停止も可能

---

Generated with Claude Code - Hourly System Documentation