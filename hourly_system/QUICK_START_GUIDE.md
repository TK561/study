#  **1時間毎システム クイックスタートガイド**

##  **すぐに始める（3ステップ）**

### **ステップ1: 起動**
```bash
# プロジェクトルートで実行
python3 start_simple_system.py
```

### **ステップ2: 確認**
```
 Starting Simple Hourly System...
========================================
 Essential features only:
   1時間毎ファイル整理
   GitHub状態確認  
   レポート統合・保存
   簡易ターミナル表示
   Claude Code終了時最終処理
========================================
 Starting monitoring (Press Ctrl+C to stop)...
```

### **ステップ3: 動作確認**
初回実行後、以下が表示されます：
```
==================================================
 HOURLY REPORT
==================================================
 Time: 2025-06-20 21:22:49
⏱  Session Duration: 0:00:06.297151
 Files: 0 actions, 0 cleaned
🐙 Git:  56 changes
 Recommendation: Consider committing pending changes
 Reports: 10 sessions archived
==================================================
 Next report: 22:22
==================================================
```

## 🛑 **停止方法**
- **Ctrl+C**: 安全停止（推奨）
- **VSCode終了**: 自動安全停止
- **ターミナル終了**: 自動安全停止

##  **ログ確認**
```bash
# リアルタイムログ
tail -f session_logs/simple_system.log

# セッション状態
cat session_logs/session_state.json

# 統合レポート
cat session_logs/consolidated_reports.json
```

##  **テスト実行**
```bash
# 一回だけ実行（テスト用）
python3 scripts/simple_hourly_system.py --once
```

##  **トラブル時**
```bash
# 権限エラー時
chmod +x start_simple_system.py
chmod +x scripts/simple_hourly_system.py

# ディレクトリ作成
mkdir -p session_logs

# 状態リセット
rm session_logs/session_state.json
```

##  **何をするシステム？**
1. **ファイル整理**: 不要ファイル削除・古いログアーカイブ
2. **Git監視**: ブランチ・変更状況の確認
3. **レポート作成**: 作業記録の自動生成・統合
4. **状況表示**: 進捗・推奨事項をターミナル表示
5. **安全停止**: 予期しない終了時の復旧対応

##  **いつ使う？**
- 長時間の研究作業中
- 定期的な進捗確認が必要な時
- ファイルやGitの状況を自動管理したい時
- 作業記録を残したい時

---
*詳細は HOURLY_SYSTEM_MANUAL.md を参照*