# 📋 研究ディスカッション記録 自動更新システム

## 🎯 概要
研究ディスカッション記録が更新されると、自動的に「次回」タブと「目標」タブを同期更新するシステムです。

---

## 🚀 主要機能

### 1. 自動検出・更新
- **監視対象**: `study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md`
- **更新対象**: `public/discussion-site/index.html` の次回・目標タブ

### 2. 自動更新内容
- **次回タブ**: 回数・日付の自動更新（毎週木曜日想定）
- **目標タブ**: 中間発表・卒業発表の日程自動調整
- **Git操作**: 自動コミット・プッシュでVercelデプロイ

### 3. 柔軟な実行方式
- **即座チェック**: 1回だけ確認・更新
- **継続監視**: 指定間隔での自動監視
- **VS Code統合**: タスクパネルから直接実行

---

## 📋 使用方法

### 基本コマンド
```bash
# 1回だけチェック・更新
python3 auto_update_system.py check

# 継続監視（30秒間隔）
python3 auto_update_system.py monitor

# 60秒間隔で監視
python3 auto_update_system.py monitor 60

# 現在の設定確認
python3 auto_update_system.py config
```

### VS Code タスク（推奨）
1. `Ctrl+Shift+P` でコマンドパレット
2. `Tasks: Run Task` を選択
3. 以下から選択:
   - `Discussion: Check Updates` - 1回チェック
   - `Discussion: Start Monitoring` - 継続監視開始
   - `Discussion: Show Config` - 設定表示

---

## 🔧 セットアップ

### 完全セットアップ（推奨）
```bash
python3 setup_auto_update.py all
```

### 個別セットアップ
```bash
# システムテスト
python3 setup_auto_update.py test

# VS Code タスク設定
python3 setup_auto_update.py vscode

# エイリアス作成
python3 setup_auto_update.py aliases
```

---

## ⚙️ 設定ファイル

### 設定場所
`.auto_update_config.json`

### 設定項目
```json
{
  "last_hash": "ファイルハッシュ値",
  "last_session_number": 12,
  "next_session_date": "2025-06-26",
  "monitoring_enabled": true,
  "auto_deploy": true
}
```

---

## 📊 動作例

### 記録更新時の自動処理
1. **検出**: `WEEKLY_DISCUSSION_SUMMARY.md` の変更検出
2. **解析**: 最新セッション情報の抽出
3. **計算**: 次回セッション（番号・日付）の自動計算
4. **更新**: 次回タブの内容書き換え
5. **調整**: 目標タブのスケジュール調整
6. **デプロイ**: Git操作でVercel自動デプロイ

### 実行ログ例
```
📋 記録ファイルの変更を検出: 2025-06-25 20:52:45
📊 最新セッション: 第12回
📅 次回セッション: 第13回 (2025年6月26日)
✅ 次回タブを更新しました
✅ 目標タブのスケジュールを更新しました
🚀 自動デプロイを実行しました
```

---

## 🎯 具体的更新内容

### 次回タブの更新
- **タイトル**: `第13回ディスカッション: 2025年6月26日（木）`
- **日付計算**: 前回から1週間後（木曜日）
- **回数増加**: 自動的に +1

### 目標タブの更新
- **中間発表**: 現在の年・月に基づく8月下旬の調整
- **卒業発表**: 適切な年の2月下旬に調整
- **スケジュール**: 現在日付基準の自動調整

---

## 🔄 継続監視

### バックグラウンド実行
```bash
# ターミナルで継続監視開始
python3 auto_update_system.py monitor &

# プロセス確認
ps aux | grep auto_update

# 停止
kill <プロセスID>
```

### cron ジョブ設定
```bash
# 5分ごとの自動チェック
crontab -e
# 以下を追加:
*/5 * * * * cd /mnt/c/Desktop/Research && python3 auto_update_system.py check
```

---

## ⚠️ 注意事項

### 必要な権限
- ファイル読み書き権限
- Git操作権限
- インターネット接続（Vercelデプロイ用）

### 対象ファイル
- 監視: `study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md`
- 更新: `public/discussion-site/index.html`
- 設定: `.auto_update_config.json`

### エラー処理
- ファイルが見つからない場合：警告表示・処理継続
- Git操作失敗：エラー表示・手動対応必要
- 日付解析失敗：デフォルト値使用

---

## 📈 利点

### 効率性
- **手動作業削減**: 記録更新時の次回・目標タブ手動修正が不要
- **一貫性確保**: 自動計算による日付・回数の正確性
- **即時反映**: デプロイまで自動化

### 信頼性
- **ハッシュベース**: ファイル変更の確実な検出
- **エラーハンドリング**: 例外状況への適切な対応
- **ログ出力**: 動作状況の可視化

### 拡張性
- **設定可能**: 監視間隔・自動デプロイのON/OFF
- **柔軟実行**: 即座チェック・継続監視の選択
- **統合対応**: VS Code・cron・systemd対応

---

## 🔗 関連ファイル

### 実行ファイル
- `auto_update_system.py` - メインシステム
- `setup_auto_update.py` - セットアップスクリプト

### 設定ファイル
- `.auto_update_config.json` - システム設定
- `.vscode/tasks.json` - VS Code タスク定義

### 対象ファイル
- `study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md` - 監視対象
- `public/discussion-site/index.html` - 更新対象

---

**作成日**: 2025年6月25日  
**作成者**: Claude Code システム  
**更新対象**: 研究ディスカッション記録サイト