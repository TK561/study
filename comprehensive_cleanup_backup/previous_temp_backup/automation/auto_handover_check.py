#!/usr/bin/env python3
"""
Claude Code起動時の自動引き継ぎチェック
前回のセッション情報を自動表示
"""

import os
from datetime import datetime, timedelta
from session_recovery_system import get_recovery_system

def auto_check_handover():
    """起動時に自動的に引き継ぎ情報をチェック・表示"""
    
    # 引き継ぎファイルの存在確認
    handover_file = "/mnt/c/Desktop/Research/TODAY_WORK_HANDOVER.md"
    
    if os.path.exists(handover_file):
        # ファイルの更新日時をチェック
        mod_time = datetime.fromtimestamp(os.path.getmtime(handover_file))
        time_diff = datetime.now() - mod_time
        
        # 24時間以内の引き継ぎファイルがある場合
        if time_diff < timedelta(hours=24):
            print("📋 前回の作業引き継ぎがあります")
            print(f"作成日時: {mod_time.strftime('%Y年%m月%d日 %H:%M')}")
            print("\n主な作業内容:")
            print("- Vercelデプロイシステム修正 ✅")
            print("- Gemini API統合システム構築 ✅") 
            print("- セッション復元システム実装 ✅")
            print("- プロジェクト整理完了 ✅")
            print("\n詳細は TODAY_WORK_HANDOVER.md を確認してください")
            return True
    
    # セッション復元の確認
    system = get_recovery_system()
    session = system._load_current_session()
    
    if session.get('actions'):
        last_updated = session.get('last_updated')
        if last_updated:
            last_time = datetime.fromisoformat(last_updated)
            time_diff = datetime.now() - last_time
            
            # 5分以上前の作業がある場合
            if time_diff > timedelta(minutes=5):
                print(f"\n🔄 前回の作業セッション（{int(time_diff.total_seconds() / 60)}分前）")
                print("復元したい場合は「復元して」と言ってください")
                return True
    
    return False

if __name__ == "__main__":
    # 起動時チェックのテスト
    auto_check_handover()