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
        
        # セッション全体の統合サマリーを生成
        self.update_consolidated_summary(summary)
        
        # まとめ表示
        self.display_summary(summary)
        
        # 次回のための更新
        self.last_summary = now
    
    def update_consolidated_summary(self, new_summary: Dict[str, Any]):
        """統合サマリーファイルを更新（記録をまとめる形式）"""
        # 統合サマリーファイルパス
        consolidated_file = self.session_log / "consolidated_work_summary.md"
        
        # セッション情報を読み込み
        with open(self.current_session, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        # 全サマリーを統合
        session_data["summaries"].append(new_summary)
        
        # セッションファイルも更新
        with open(self.current_session, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        # Markdownで統合レポートを生成
        self.generate_consolidated_report(session_data, consolidated_file)
    
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
    
    def send_notification(self, summary: Dict[str, Any]):
        """ターミナル通知を送信"""
        try:
            # Terminal notification with detailed summary
            self.print_terminal_notification(summary)
            
            # Sound notification (if available)
            try:
                if os.name == 'nt':
                    import winsound
                    winsound.Beep(800, 200)  # frequency, duration
            except ImportError:
                pass
                
        except Exception as e:
            print(f"通知送信エラー: {e}")
    
    def print_terminal_notification(self, summary: Dict[str, Any]):
        """ターミナル上に詳細な通知を表示"""
        print("\n" + "🔔" * 60)
        print("                    1時間毎作業まとめ通知")
        print("🔔" * 60)
        
        # 基本情報
        print(f"⏰ 時刻: {summary['summary_time'][:19]}")
        print(f"⌛ 作業時間: {summary['duration_hours']:.1f}時間")
        print(f"🎯 主な活動: {', '.join(summary['activities'])}")
        
        # Git情報
        git_info = summary['git_status']
        if 'recent_commits' in git_info and git_info['recent_commits'] and git_info['recent_commits'][0]:
            print(f"📝 最新コミット: {git_info['recent_commits'][0][:60]}...")
        
        # ファイル状況
        file_count = summary['file_count']
        print(f"📁 ファイル状況:")
        print(f"   • Python: {file_count['python_files']}個")
        print(f"   • Markdown: {file_count['markdown_files']}個") 
        print(f"   • 合計: {file_count['total_files']}個")
        
        # 変更状況
        if git_info.get('status'):
            changed_files = len(git_info['status'].strip().split('\n')) if git_info['status'].strip() else 0
            print(f"🔄 変更中のファイル: {changed_files}個")
        else:
            print("✅ 作業ディレクトリ: クリーン")
        
        # 簡単な進捗サマリー
        self.print_progress_summary(summary)
        
        print("📄 詳細は session_logs/consolidated_work_summary.md を確認")
        print("🔔" * 60)
        print("                  次の1時間も頑張りましょう！")
        print("🔔" * 60 + "\n")
    
    def print_progress_summary(self, summary: Dict[str, Any]):
        """進捗の簡単なサマリーを表示"""
        activities = summary['activities']
        duration = summary['duration_hours']
        
        print("\n📊 この1時間のまとめ:")
        
        # 活動の分析
        if "セキュリティ強化" in activities:
            print("   🔒 セキュリティ対策を実施")
        if "ファイル整理" in activities:
            print("   🧹 プロジェクト整理を実行")
        if "新機能追加" in activities:
            print("   ✨ 新機能の開発を実施")
        if "バグ修正" in activities:
            print("   🐛 バグ修正を実行")
        if "アップデート" in activities:
            print("   ⬆️ システムアップデートを実施")
        if "ファイル変更中" in activities:
            print("   📝 ファイルの編集作業中")
        
        # 作業効率の評価
        if duration >= 0.8:
            print("   ⚡ 高い作業効率を維持")
        elif duration >= 0.5:
            print("   📈 順調な作業ペース")
        else:
            print("   🔧 準備・設定作業中心")
        
        # 次のアクションの提案
        git_info = summary['git_status']
        if git_info.get('status'):
            print("   💡 推奨: 変更をコミットして進捗を保存")
        else:
            print("   💡 推奨: 新しいタスクの開始準備完了")
    
    def generate_consolidated_report(self, session_data: Dict[str, Any], output_file: Path):
        """統合レポートを生成（全記録をまとめる）"""
        session_start = datetime.datetime.fromisoformat(session_data['session_start'])
        now = datetime.datetime.now()
        total_duration = now - session_start
        
        # 全活動を集計
        all_activities = []
        total_commits = 0
        file_changes = []
        
        for summary in session_data['summaries']:
            all_activities.extend(summary['activities'])
            if 'recent_commits' in summary['git_status']:
                total_commits += len([c for c in summary['git_status']['recent_commits'] if c.strip()])
        
        # 活動集計
        activity_counts = {}
        for activity in all_activities:
            activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        # 最新状態
        latest_summary = session_data['summaries'][-1] if session_data['summaries'] else {}
        latest_files = latest_summary.get('file_count', {})
        initial_files = session_data.get('initial_file_count', {})
        
        # Markdownレポート生成
        report = f"""# 作業統合レポート

**生成日時**: {now.strftime('%Y-%m-%d %H:%M:%S')}  
**セッション開始**: {session_start.strftime('%Y-%m-%d %H:%M:%S')}  
**総作業時間**: {total_duration.total_seconds()/3600:.1f}時間

## 全体サマリー

### 主要活動
"""
        
        for activity, count in sorted(activity_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{activity}**: {count}回\n"
        
        report += f"""
### ファイル変更状況
- **Python**: {initial_files.get('python_files', 0)} → {latest_files.get('python_files', 0)}
- **Markdown**: {initial_files.get('markdown_files', 0)} → {latest_files.get('markdown_files', 0)}
- **総ファイル数**: {initial_files.get('total_files', 0)} → {latest_files.get('total_files', 0)}

### Git活動
- **コミット数**: 約{total_commits}回
- **現在ブランチ**: {latest_summary.get('git_status', {}).get('branch', 'unknown')}

## 時系列記録

"""
        
        for i, summary in enumerate(session_data['summaries'], 1):
            summary_time = datetime.datetime.fromisoformat(summary['summary_time'])
            report += f"""### {i}. {summary_time.strftime('%H:%M')} の記録
- **活動**: {', '.join(summary['activities'])}
- **作業時間**: {summary['duration_hours']:.1f}時間
- **ファイル数**: {summary['file_count']['total_files']}個

"""
        
        # 最新のGit状況
        if latest_summary.get('git_status'):
            git_status = latest_summary['git_status']
            if git_status.get('recent_commits') and git_status['recent_commits'][0]:
                report += f"""## 最新Git状況

**最新コミット**:
```
{git_status['recent_commits'][0]}
```

"""
        
        report += f"""## セッション完了

**合計作業時間**: {total_duration.total_seconds()/3600:.1f}時間  
**まとめ回数**: {len(session_data['summaries'])}回  
**記録ファイル**: `{self.current_session.name}`

---
*自動生成: {now.strftime('%Y-%m-%d %H:%M:%S')} | 1時間毎作業整理システム*
"""
        
        # ファイルに保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"統合レポート更新: {output_file.name}")
    
    def display_summary(self, summary: Dict[str, Any]):
        """まとめを表示"""
        print("\n" + "="*50)
        print(f"1時間毎のまとめ - {summary['summary_time'][:19]}")
        print("="*50)
        
        print(f"作業時間: {summary['duration_hours']:.1f}時間")
        print(f"主な活動: {', '.join(summary['activities'])}")
        
        git_info = summary['git_status']
        if 'recent_commits' in git_info and git_info['recent_commits'][0]:
            print(f"最新コミット: {git_info['recent_commits'][0]}")
        
        file_count = summary['file_count']
        print(f"ファイル数: Python({file_count['python_files']}) / "
              f"Markdown({file_count['markdown_files']}) / "
              f"合計({file_count['total_files']})")
        
        if git_info.get('status'):
            print(f"変更中のファイル: {len(git_info['status'].split())}")
        else:
            print("作業ディレクトリ: クリーン")
        
        print("="*50)
        print("次の1時間も継続します\n")
        
        # Send notification
        self.send_notification(summary)
    
    def start_hourly_timer(self):
        """1時間タイマーを開始"""
        def timer_loop():
            while True:
                time.sleep(3600)  # 1時間待機
                self.generate_hourly_summary()
        
        timer_thread = threading.Thread(target=timer_loop, daemon=True)
        timer_thread.start()
        print("1時間毎の整理タイマーを開始しました")
    
    def manual_summary(self):
        """手動でまとめを生成"""
        print("手動まとめを生成中...")
        self.generate_hourly_summary()
    
    def get_session_report(self) -> str:
        """セッション全体のレポートを取得"""
        try:
            with open(self.current_session, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            total_duration = (datetime.datetime.now() - 
                            datetime.datetime.fromisoformat(session_data['session_start']))
            
            report = f"""
セッションレポート
{'='*40}
開始時刻: {session_data['session_start'][:19]}
経過時間: {total_duration.total_seconds()/3600:.1f}時間
まとめ回数: {len(session_data['summaries'])}回

プロジェクト状況:
- 初期ファイル数: {session_data['initial_file_count']['total_files']}
- 現在ファイル数: {self.count_files()['total_files']}

主な活動:
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
    print("1時間毎作業整理システムを開始します")
    
    # システム初期化
    summary_system = HourlySummarySystem()
    
    # 使用方法を表示
    print("""
使用方法:
- 自動: 1時間毎に自動でまとめが表示されます
- 手動: summary_system.manual_summary() で即座にまとめ生成
- レポート: summary_system.get_session_report() でセッション全体を確認

このシステムはバックグラウンドで動作し続けます
""")
    
    return summary_system

if __name__ == "__main__":
    system = main()
    
    # 対話モード
    try:
        while True:
            cmd = input("\nコマンド (m:手動まとめ / r:レポート / q:終了): ").strip().lower()
            
            if cmd == 'm':
                system.manual_summary()
            elif cmd == 'r':
                print(system.get_session_report())
            elif cmd == 'q':
                print("セッションを終了します")
                break
            else:
                print("無効なコマンドです")
                
    except KeyboardInterrupt:
        print("\nセッションを終了します")