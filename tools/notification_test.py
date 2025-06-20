#!/usr/bin/env python3
"""
通知機能のテスト
"""

import os
import subprocess
from datetime import datetime

def test_notification():
    """通知機能をテスト"""
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Mock summary data for testing
        test_summary = {
            "summary_time": current_time,
            "duration_hours": 1.2,
            "activities": ["新機能追加", "ファイル整理"],
            "git_status": {
                "recent_commits": ["Add hourly notification system - implement terminal notifications"],
                "status": "M hourly_summary_system.py\\nM notification_test.py"
            },
            "file_count": {
                "python_files": 8,
                "markdown_files": 3,
                "total_files": 25
            }
        }
        
        # Test terminal notification
        print_test_terminal_notification(test_summary)
        
        # Sound test
        try:
            if os.name == 'nt':
                import winsound
                winsound.Beep(800, 200)
                print("🔊 音声通知テスト完了")
        except ImportError:
            print("ℹ winsoundが利用できません")
            
    except Exception as e:
        print(f" 通知テストエラー: {e}")

def print_test_terminal_notification(summary):
    """テスト用ターミナル通知"""
    print("\\n" + "🔔" * 60)
    print("                    1時間毎作業まとめ通知 (TEST)")
    print("🔔" * 60)
    
    # 基本情報
    print(f" 時刻: {summary['summary_time'][:19]}")
    print(f"⌛ 作業時間: {summary['duration_hours']:.1f}時間")
    print(f" 主な活動: {', '.join(summary['activities'])}")
    
    # Git情報
    git_info = summary['git_status']
    if git_info.get('recent_commits') and git_info['recent_commits'][0]:
        print(f" 最新コミット: {git_info['recent_commits'][0][:60]}...")
    
    # ファイル状況
    file_count = summary['file_count']
    print(f" ファイル状況:")
    print(f"   • Python: {file_count['python_files']}個")
    print(f"   • Markdown: {file_count['markdown_files']}個") 
    print(f"   • 合計: {file_count['total_files']}個")
    
    # 変更状況
    if git_info.get('status'):
        changed_files = len(git_info['status'].strip().split('\\n')) if git_info['status'].strip() else 0
        print(f" 変更中のファイル: {changed_files}個")
    else:
        print(" 作業ディレクトリ: クリーン")
    
    # 進捗サマリー
    print("\\n この1時間のまとめ:")
    activities = summary['activities']
    if "新機能追加" in activities:
        print("    新機能の開発を実施")
    if "ファイル整理" in activities:
        print("   🧹 プロジェクト整理を実行")
    
    duration = summary['duration_hours']
    if duration >= 0.8:
        print("    高い作業効率を維持")
    
    if git_info.get('status'):
        print("    推奨: 変更をコミットして進捗を保存")
    
    print(" 詳細は session_logs/consolidated_work_summary.md を確認")
    print("🔔" * 60)
    print("                  次の1時間も頑張りましょう！")
    print("🔔" * 60 + "\\n")

if __name__ == "__main__":
    test_notification()