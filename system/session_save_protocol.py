#!/usr/bin/env python3
"""
セッション保存プロトコル
「今日の内容を保存」等の指示時の包括的保存手順
"""

SESSION_SAVE_TRIGGERS = [
    "今日の内容を保存",
    "今日の作業を記録", 
    "セッションを保存",
    "今日のまとめ",
    "作業内容を保存",
    "今日やったことを保存",
    "セッション記録",
    "今日の記録",
    "作業記録を保存"
]

COMPREHENSIVE_SAVE_PROTOCOL = """
## 包括的セッション保存プロトコル

### 1. セッション全体の分析
- 開始時刻から現在までの全作業内容
- 実施したタスクの完全リスト
- 作成・修正・削除したファイル
- Git操作履歴
- 技術的成果と課題

### 2. 詳細記録の作成・更新
- daily_session_YYYY-MM-DD.md の包括的更新
- 時系列での作業内容記録
- 定量的成果（行数・ファイル数・時間）
- 技術的価値と長期的影響

### 3. ファイル整理・保存
- 関連ファイルの適切な配置
- バックアップの確認
- Git add, commit, push の実行
- 必要に応じたタグ付け

### 4. 次回への継続事項整理
- 未完了タスクの明確化
- 次回優先事項の設定
- システム状態の確認
- 設定ファイルの更新

### 5. 保存完了確認
- すべての変更のコミット確認
- 重要ファイルの存在確認
- 次回アクセス時の情報整理
"""

def detect_save_request(user_input):
    """保存要求の検出"""
    user_input_lower = user_input.lower()
    for trigger in SESSION_SAVE_TRIGGERS:
        if trigger in user_input_lower:
            return True
    return False

if __name__ == "__main__":
    print("📋 セッション保存プロトコル")
    print("=" * 40)
    print("検出キーワード:")
    for trigger in SESSION_SAVE_TRIGGERS:
        print(f"  - {trigger}")
    print("\n包括的保存プロトコル:")
    print(COMPREHENSIVE_SAVE_PROTOCOL)