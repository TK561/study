# 🤖 textlint自動実行システム使用ガイド

## 📋 概要
textlintを自動的に実行し、AI生成文章の品質を継続的に監視・改善するシステムです。

## 🚀 クイックスタート

### 1. 依存関係のインストール
```bash
npm install
```

### 2. 自動実行システムの起動
```bash
# 統合メニューから選択
./start_textlint_auto.sh

# または直接指定
npm run textlint:auto      # 定期チェック
npm run textlint:watch     # ファイル監視
npm run textlint:schedule  # スケジュール実行
npm run textlint:setup     # Git hooks設定
```

## 🎯 実行モード

### 1. 📊 定期チェックモード
```bash
python3 textlint_auto_runner.py start
```
- **機能**: 指定間隔で自動的にtextlintを実行
- **デフォルト**: 30分ごと
- **用途**: 継続的な品質監視

#### オプション
```bash
# チェック間隔を指定（分）
python3 textlint_auto_runner.py start --interval 60

# 自動修正を有効化
python3 textlint_auto_runner.py start --auto-fix
```

### 2. 👁️ ファイル監視モード
```bash
python3 textlint_watcher.py
```
- **機能**: ファイル変更をリアルタイムで検出し、即座にチェック
- **用途**: 執筆中のリアルタイム品質管理

#### 特徴
- 新規ファイル作成を検出
- ファイル変更時の自動チェック
- デバウンス機能（連続変更の重複実行防止）
- カラー出力で結果表示

### 3. ⏰ スケジュール実行モード
```bash
python3 textlint_scheduler.py start
```
- **機能**: 指定時刻に自動実行
- **デフォルト**: 9:00, 13:00, 18:00
- **用途**: 定時での品質チェック

#### 機能
- 複数時刻での自動実行
- 日次レポート生成
- 統計情報の蓄積
- 通知機能（設定可能）

### 4. 🔧 Git hooks統合
```bash
./setup_textlint_hooks.sh
```
- **機能**: Git操作時の自動チェック
- **設定されるフック**:
  - `pre-commit`: コミット前チェック
  - `pre-push`: プッシュ前チェック
  - `commit-msg`: コミットメッセージチェック

## ⚙️ 設定ファイル

### 定期チェック設定 (`textlint_auto_config.json`)
```json
{
  "auto_check_enabled": true,
  "check_interval_minutes": 30,
  "auto_fix": false,
  "target_patterns": ["*.md", "sessions/*.md"],
  "notification": {
    "enabled": true,
    "threshold_errors": 5
  }
}
```

### ファイル監視設定 (`textlint_watcher_config.json`)
```json
{
  "watch_patterns": ["*.md", "sessions/*.md"],
  "ignore_patterns": ["*_backup*", "node_modules/**"],
  "debounce_seconds": 2,
  "auto_fix_on_save": false
}
```

### スケジュール設定 (`textlint_scheduler_config.json`)
```json
{
  "schedules": [
    {"time": "09:00", "auto_fix": false, "scope": "all"},
    {"time": "18:00", "auto_fix": true, "scope": "all"}
  ],
  "daily_report": true,
  "report_time": "20:00"
}
```

## 📊 レポート機能

### 日次レポート
- 自動生成される品質レポート
- エラー・警告の統計
- 頻出問題の分析
- 時系列での品質推移

### リアルタイム通知
- 閾値を超えたエラー検出時の通知
- 修正提案の表示
- 進捗状況のフィードバック

## 🎮 npmスクリプト

### 基本チェック
```bash
npm run lint              # 全ファイルチェック
npm run lint:fix          # 自動修正付きチェック
npm run lint:sessions     # セッションファイルのみ
npm run lint:docs         # ドキュメントのみ
```

### 自動実行
```bash
npm run textlint:auto     # 定期チェック開始
npm run textlint:watch    # ファイル監視開始
npm run textlint:schedule # スケジュール実行開始
npm run textlint:setup    # Git hooks設定
```

### カスタムチェック
```bash
npm run check-writing                 # 高機能チェック
npm run check-writing -- --fix       # 自動修正付き
npm run check-writing -- --sessions  # セッションのみ
```

## 💡 使用例とワークフロー

### 📝 執筆時のワークフロー
1. **ファイル監視モード**で執筆開始
2. **リアルタイム**でエラー検出・修正
3. **コミット前**に自動チェック実行
4. **定期チェック**で全体品質維持

### 🔄 チーム開発での活用
1. **Git hooks**でコミット品質保証
2. **スケジュール実行**で定時品質レポート
3. **自動修正**で作業効率向上
4. **日次レポート**で品質傾向分析

## 🛠️ トラブルシューティング

### よくある問題

#### 1. textlintが見つからない
```bash
npm install  # 依存関係を再インストール
```

#### 2. Python依存関係エラー
```bash
pip install schedule  # スケジューラー用
```

#### 3. 権限エラー
```bash
chmod +x *.sh *.py  # 実行権限を付与
```

#### 4. Git hooksが動作しない
```bash
ls -la .git/hooks/  # フックファイルの確認
chmod +x .git/hooks/*  # 実行権限付与
```

## 📚 参考情報

### コマンド一覧
- `./start_textlint_auto.sh` - 統合起動メニュー
- `python3 textlint_auto_runner.py status` - システム状態確認
- `python3 textlint_scheduler.py check` - 今すぐチェック実行
- `python3 textlint_watcher.py --config` - 監視設定表示

### ログファイル
- `textlint_auto_log.json` - 定期チェックログ
- `textlint_reports/` - 日次レポート
- `.last_textlint_check` - 最終チェック時刻

### 設定のカスタマイズ
各設定ファイルを編集することで、チェック対象、実行間隔、通知設定等をカスタマイズできます。