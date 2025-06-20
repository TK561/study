#!/usr/bin/env python3
"""
1時間毎の作業整理システム
Claude Codeセッション中の活動を追跡・整理
"""

import os
import json
import datetime
import threading
import time
from pathlib import Path
from typing import Dict, List, Any
import subprocess

class HourlySummarySystem:
    """1時間毎に作業を自動整理するシステム"""
    
    def __init__(self, project_root: str = "/mnt/c/Desktop/Research"):
        self.project_root = Path(project_root)
        self.session_log = self.project_root / "session_logs"
        self.session_log.mkdir(exist_ok=True)
        
        # セッション開始時刻
        self.session_start = datetime.datetime.now()
        self.last_summary = self.session_start
        
        # 作業ログファイル
        self.current_session = self.session_log / f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 初期化
        self.init_session()
        
        # 1時間タイマー開始
        self.start_hourly_timer()
    
    def init_session(self):
        """セッション初期化"""
        session_data = {
            "session_start": self.session_start.isoformat(),
            "project_root": str(self.project_root),
            "git_status": self.get_git_status(),
            "initial_file_count": self.count_files(),
            "summaries": []
        }
        
        with open(self.current_session, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 セッション開始: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 ログファイル: {self.current_session.name}")
    
    def get_git_status(self) -> Dict[str, Any]:
        """Git状態を取得"""
        try:
            os.chdir(self.project_root)
            
            # Git status
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True)
            
            # Recent commits
            log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                      capture_output=True, text=True)
            
            # Branch info
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True)
            
            return {
                "branch": branch_result.stdout.strip(),
                "status": status_result.stdout.strip(),
                "recent_commits": log_result.stdout.strip().split('\n'),
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def count_files(self) -> Dict[str, int]:
        """ファイル数をカウント"""
        file_counts = {
            "python_files": 0,
            "markdown_files": 0,
            "config_files": 0,
            "total_files": 0
        }
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                file_counts["total_files"] += 1
                
                if file_path.suffix == '.py':
                    file_counts["python_files"] += 1
                elif file_path.suffix == '.md':
                    file_counts["markdown_files"] += 1
                elif file_path.name in ['config.py', '.env', 'requirements.txt']:
                    file_counts["config_files"] += 1
        
        return file_counts
    
    def generate_hourly_summary(self):
        """1時間毎の作業まとめを生成"""
        now = datetime.datetime.now()
        duration = now - self.last_summary
        
        # 現在の状態を取得
        current_git_status = self.get_git_status()
        current_file_count = self.count_files()
        
        summary = {
            "summary_time": now.isoformat(),
            "duration_hours": duration.total_seconds() / 3600,
            "git_status": current_git_status,
            "file_count": current_file_count,
            "activities": self.detect_activities(current_git_status)
        }
        
        # セッションログに追加
        with open(self.current_session, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        session_data["summaries"].append(summary)
        
        with open(self.current_session, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        # まとめ表示
        self.display_summary(summary)
        
        # 次回のための更新
        self.last_summary = now
    
    def detect_activities(self, git_status: Dict[str, Any]) -> List[str]:
        """活動を検出"""
        activities = []
        
        if "recent_commits" in git_status:
            recent_commits = git_status["recent_commits"]
            if recent_commits and recent_commits[0]:
                # 最新コミットから活動を推測
                latest_commit = recent_commits[0].lower()
                
                if "security" in latest_commit or "🔒" in latest_commit:
                    activities.append("セキュリティ強化")
                if "clean" in latest_commit or "🧹" in latest_commit:
                    activities.append("ファイル整理")
                if "add" in latest_commit or "✨" in latest_commit:
                    activities.append("新機能追加")
                if "fix" in latest_commit or "🐛" in latest_commit:
                    activities.append("バグ修正")
                if "update" in latest_commit or "⬆️" in latest_commit:
                    activities.append("アップデート")
        
        if git_status.get("status"):
            activities.append("ファイル変更中")
        
        return activities if activities else ["通常作業"]
    
    def display_summary(self, summary: Dict[str, Any]):
        """まとめを表示"""
        print("\n" + "="*50)
        print(f"⏰ 1時間毎のまとめ - {summary['summary_time'][:19]}")
        print("="*50)
        
        print(f"📊 作業時間: {summary['duration_hours']:.1f}時間")
        print(f"🎯 主な活動: {', '.join(summary['activities'])}")
        
        git_info = summary['git_status']
        if 'recent_commits' in git_info and git_info['recent_commits'][0]:
            print(f"📝 最新コミット: {git_info['recent_commits'][0]}")
        
        file_count = summary['file_count']
        print(f"📁 ファイル数: Python({file_count['python_files']}) / "
              f"Markdown({file_count['markdown_files']}) / "
              f"合計({file_count['total_files']})")
        
        if git_info.get('status'):
            print(f"🔄 変更中のファイル: {len(git_info['status'].split())}")
        else:
            print("✅ 作業ディレクトリ: クリーン")
        
        print("="*50)
        print("💡 次の1時間も頑張りましょう！\n")
    
    def start_hourly_timer(self):
        """1時間タイマーを開始"""
        def timer_loop():
            while True:
                time.sleep(3600)  # 1時間待機
                self.generate_hourly_summary()
        
        timer_thread = threading.Thread(target=timer_loop, daemon=True)
        timer_thread.start()
        print("⏰ 1時間毎の整理タイマーを開始しました")
    
    def manual_summary(self):
        """手動でまとめを生成"""
        print("📋 手動まとめを生成中...")
        self.generate_hourly_summary()
    
    def get_session_report(self) -> str:
        """セッション全体のレポートを取得"""
        try:
            with open(self.current_session, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            total_duration = (datetime.datetime.now() - 
                            datetime.datetime.fromisoformat(session_data['session_start']))
            
            report = f"""
📊 セッションレポート
{'='*40}
🕐 開始時刻: {session_data['session_start'][:19]}
⏱️ 経過時間: {total_duration.total_seconds()/3600:.1f}時間
📝 まとめ回数: {len(session_data['summaries'])}回

📁 プロジェクト状況:
- 初期ファイル数: {session_data['initial_file_count']['total_files']}
- 現在ファイル数: {self.count_files()['total_files']}

🎯 主な活動:
"""
            
            all_activities = []
            for summary in session_data['summaries']:
                all_activities.extend(summary['activities'])
            
            activity_counts = {}
            for activity in all_activities:
                activity_counts[activity] = activity_counts.get(activity, 0) + 1
            
            for activity, count in sorted(activity_counts.items(), 
                                        key=lambda x: x[1], reverse=True):
                report += f"- {activity}: {count}回\n"
            
            return report
            
        except Exception as e:
            return f"レポート生成エラー: {e}"

def main():
    """メイン関数"""
    print("🚀 1時間毎作業整理システムを開始します")
    
    # システム初期化
    summary_system = HourlySummarySystem()
    
    # 使用方法を表示
    print("""
🎯 使用方法:
- 自動: 1時間毎に自動でまとめが表示されます
- 手動: summary_system.manual_summary() で即座にまとめ生成
- レポート: summary_system.get_session_report() でセッション全体を確認

💡 このシステムはバックグラウンドで動作し続けます
""")
    
    return summary_system

if __name__ == "__main__":
    system = main()
    
    # 対話モード
    try:
        while True:
            cmd = input("\n📋 コマンド (m:手動まとめ / r:レポート / q:終了): ").strip().lower()
            
            if cmd == 'm':
                system.manual_summary()
            elif cmd == 'r':
                print(system.get_session_report())
            elif cmd == 'q':
                print("👋 セッションを終了します")
                break
            else:
                print("❓ 無効なコマンドです")
                
    except KeyboardInterrupt:
        print("\n👋 セッションを終了します")