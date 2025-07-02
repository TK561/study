#!/usr/bin/env python3
"""
ディスカッション自動化システムセットアップ
- 必要なファイルとスクリプトの配置
- 自動実行の設定とテスト
- 使い方ガイドの表示
"""

import os
import stat
from pathlib import Path

def setup_discussion_automation():
    """ディスカッション自動化システムのセットアップ"""
    base_dir = Path("/mnt/c/Desktop/Research")
    
    print("🔧 ディスカッション自動化システムセットアップ開始")
    
    # 実行権限の付与
    scripts = [
        "discussion_auto_updater.py",
        "watch_discussion_updates.py",
        "setup_discussion_automation.py"
    ]
    
    for script in scripts:
        script_path = base_dir / script
        if script_path.exists():
            # 実行権限を付与
            current_permissions = script_path.stat().st_mode
            script_path.chmod(current_permissions | stat.S_IEXEC)
            print(f"✅ {script} に実行権限を付与")
        else:
            print(f"⚠️ {script} が見つかりません")
    
    print("\\n📋 セットアップ完了!")
    print_usage_guide()

def print_usage_guide():
    """使用方法ガイド表示"""
    print("""
📘 ディスカッション自動化システム使用ガイド

🎯 基本的な使い方:

1️⃣ 自動更新の実行:
   python3 discussion_auto_updater.py
   
2️⃣ 新しいセッション検出チェック:
   python3 discussion_auto_updater.py check
   
3️⃣ 次回セッション強制生成:
   python3 discussion_auto_updater.py force
   
4️⃣ 設定確認:
   python3 discussion_auto_updater.py config

🔄 監視システム:

1️⃣ ファイル変更監視開始:
   python3 watch_discussion_updates.py start
   
2️⃣ 30秒間隔で監視:
   python3 watch_discussion_updates.py start 30
   
3️⃣ 変更チェック（一回のみ）:
   python3 watch_discussion_updates.py check

⚙️ 自動化の流れ:

1. 毎週木曜18時のディスカッション開催
2. 新しいセッション記録をdiscussion-site/index.htmlに追加
3. 自動検出システムが変更を感知
4. 次回セッション（翌週木曜18時）の内容を自動生成
5. GitHubへ自動コミット・プッシュ
6. Vercelへ自動デプロイ

🎨 カスタマイズ:

- discussion_auto_config.json で設定変更可能
- 議題テンプレートは discussion_auto_updater.py 内で編集
- 監視間隔や自動コミットの有効/無効も設定可能

⚡ 簡単な使い方:

新しいディスカッション記録を追加したら:
python3 discussion_auto_updater.py

これだけで次回の準備が完了します！

🔧 トラブルシューティング:

エラーが発生した場合:
1. discussion_auto_config.json の設定を確認
2. GitHubアクセス権限を確認  
3. Vercel CLIの設定を確認

💡 CLAUDE.mdに統合する場合:

以下をCLAUDE.mdに追加:
```bash
# ディスカッション記録更新時の自動実行
python3 discussion_auto_updater.py
```
""")

def test_system():
    """システムテスト実行"""
    print("🧪 システムテスト実行中...")
    
    from discussion_auto_updater import DiscussionAutoUpdater
    
    updater = DiscussionAutoUpdater()
    
    # 設定読み込みテスト
    config = updater.load_config()
    print(f"✅ 設定読み込み: {config.get('last_session_number', 'N/A')}回まで記録")
    
    # ファイル存在チェック
    if updater.discussion_file.exists():
        print("✅ ディスカッションファイル存在確認")
    else:
        print("❌ ディスカッションファイルが見つかりません")
        
    # セッション検出テスト
    detected, session_num = updater.detect_new_session_added()
    if detected:
        print(f"🆕 新しいセッション第{session_num}回を検出")
    else:
        print(f"📋 最新セッション: 第{session_num}回")
    
    print("🧪 テスト完了")

def main():
    """メイン実行"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            setup_discussion_automation()
        elif command == "test":
            test_system()
        elif command == "guide":
            print_usage_guide()
        else:
            print("❌ 不明なコマンド:", command)
            print("使用可能コマンド: setup, test, guide")
    else:
        setup_discussion_automation()

if __name__ == "__main__":
    main()