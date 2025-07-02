# Claude Code 設定ファイル

## 🔄 自動整理・保存システム
**ユーザーが「ファイルとフォルダ整理」「やったことの保存」のどちらを要求しても両方を自動実行**

### 自動実行コマンド
```bash
# 手動実行
python3 auto_organize_and_save.py

# 自動時間監視システム開始（毎時0分に自動実行）
python3 start_auto_monitor.py start
```

### 対応キーワード
- **整理関連**: 「整理」「ファイル」「フォルダ」「削除」「cleanup」「organize」
- **保存関連**: 「保存」「記録」「やったこと」「作業」「save」「記録」

### 実行内容（固定順序）
1. **ファイル・フォルダ整理**（第1ステップ）:
   - 一時ファイル削除 (temp_*, test_*, old_*)
   - 空ディレクトリ削除
   - バックアップ統合
   
2. **セッション作業保存**（第2ステップ）:
   - Git変更状況記録
   - 今日更新されたファイル一覧
   - システム出力結果収集
   - 重要ファイル自動バックアップ

**注意**: どちらの要求でも必ず「整理→保存」の順序で実行されます

### 🕐 自動時間実行機能
**Claude Code実行中かつ毎時0分に自動実行**

#### 自動監視システム
```bash
# 監視開始
python3 start_auto_monitor.py start

# 状態確認  
python3 start_auto_monitor.py status

# 監視停止
python3 start_auto_monitor.py stop
```

#### 実行条件
1. **Claude Code起動中**: プロセス監視により自動検出
2. **毎時0分**: 00:00, 01:00, 02:00... の時刻
3. **重複防止**: 同じ時間帯では1回のみ実行

#### 監視ログ
- `auto_hourly_monitor.log` - 監視システムログ
- 30秒間隔で条件チェック
- 実行結果を自動記録

### 出力ファイル
- `sessions/AUTO_SESSION_SAVE_YYYY-MM-DD.md` - セッション記録
- `auto_execution_log_YYYYMMDD_HHMMSS.json` - 実行ログ
- `important_backup_YYYYMMDD_HHMMSS/` - 重要ファイルバックアップ

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

### 🔄 完全自動化システム
**Vercel関連の操作を検出して自動実行**

#### 🎯 包括的セットアップ
```bash
# ワンコマンドで全機能セットアップ
python3 vercel_smart_integration.py setup
```

#### 👁️ 自動監視機能
```bash
# 自動監視開始
python3 vercel_auto_trigger.py start

# または短縮コマンド（セットアップ後）
vst
```

#### 🔧 自動実行トリガー
- **ファイル変更検出**: HTML, CSS, JS, JSON等の変更
- **コマンド監視**: vercel, git push, npm run等の実行
- **Git hooks**: push時の自動デプロイ
- **エラー検出**: 失敗時の自動修復

#### 🎮 便利なエイリアス（セットアップ後）
```bash
vsd  # スマートデプロイ
vss  # システム状態確認
vsf  # 自動修復
vst  # 自動監視開始
```

#### 💡 VS Code統合
- Ctrl+Shift+V, Ctrl+Shift+D: スマートデプロイ
- Ctrl+Shift+V, Ctrl+Shift+S: システム状態
- タスクパネルから直接実行可能

## 🔄 自動復元機能
Claude Code起動時に前回のセッションを自動的に検出・復元します。

### 📋 基本コマンド
```bash
# 有効化
python3 claude_auto_restore.py enable

# 状態確認
python3 claude_auto_restore.py status

# 手動復元
python3 claude_auto_restore.py restore

# 無効化
python3 claude_auto_restore.py disable
```

### 🚀 起動時の自動実行
Claude Code起動時に以下を実行（**競合回避統合システム**）：

**統合起動（推奨・干渉防止）**
```python
exec(open('coordinated_startup.py').read())
```

**従来方式（競合の可能性あり）**
```python
exec(open('claude_startup_integration.py').read())
```

### ⚡ クイック起動・管理
```bash
# 統合起動（干渉回避）
python3 coordinated_startup.py startup

# システム状態確認
python3 coordinated_startup.py check

# 緊急停止
python3 coordinated_startup.py stop

# コーディネーター詳細状態
python3 auto_system_coordinator.py status
```

### 🔧 セッション管理機能
- **自動保存**: すべての操作を記録
- **自動バックアップ**: 10アクションごと
- **異常終了検出**: 5分以上更新がない場合
- **プロセス監視**: Claude Code実行状況を自動検出

### 📊 復元オプション
1. **自動復元**: 5秒後に最新セッション復元
2. **手動選択**: 復元したいセッションを選択
3. **レポート生成**: 詳細な復元レポート作成
4. **スキップ**: 新しいセッション開始

### 📁 ファイルの場所
- **セッションデータ**: `.claude_sessions/current_session.json`
- **復元レポート**: `auto_recovery_report.md`
- **バックアップ**: `.claude_sessions/backups/`
- **設定ファイル**: `.claude_sessions/auto_restore_config.json`

### 🎯 便利な関数
```python
from claude_auto_restore import save_file_create, save_file_modify, save_command

# ファイル操作記録
save_file_create("new_file.py", "print('hello')")
save_file_modify("existing_file.py", "updated content")

# コマンド記録
save_command("npm run dev", "Server started on port 3000")
```

## 🤖 自動システム競合回避
複数の自動実行コードが干渉しないよう統合管理

### 📋 統合コーディネーター機能
- **排他制御**: 同時実行の防止
- **優先度管理**: 重要システムの優先実行
- **リソース監視**: CPU/メモリ使用量チェック
- **競合検出**: システム間の競合回避
- **統合ログ**: 全システムの動作記録

### 🎯 管理対象システム

#### 🔴 最高優先度（CRITICAL）
- **claude_auto_restore.py** - セッション復元システム

#### 🟠 高優先度（HIGH）  
- **auto_organize_and_save.py** - 自動整理・保存システム

#### 🟡 通常優先度（NORMAL）
- **textlint_auto_runner.py** - textlint自動実行
- **textlint_watcher.py** - textlintファイル監視
- **auto_dev_workflow.py** - 自動開発ワークフロー

#### 🟢 低優先度（LOW）
- **auto_research_trigger.py** - 研究自動実行

### 🔧 コーディネーター制御

```bash
# システム登録（必要時のみ）
python3 auto_system_coordinator.py register

# コーディネーション開始
python3 auto_system_coordinator.py start

# 状態確認
python3 auto_system_coordinator.py status

# 停止
python3 auto_system_coordinator.py stop
```

### 🚨 競合回避ルール
1. **復元 ⚔️ 保存**: 同時実行禁止
2. **復元 ⚔️ 監視**: ファイル競合回避
3. **保存 ⚔️ 復元**: 排他制御
4. **リソース制限**: CPU 80%、メモリ 80%以下
5. **最大同時実行**: 3システムまで