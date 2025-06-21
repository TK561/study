#!/usr/bin/env python3
"""
Simple Hourly System - Essential Functions Only

Generated with Claude Code
Date: 2025-06-20
Purpose: 必要最小限の1時間毎システム
Verified: 実装済み
"""

import os
import sys
import json
import time
import signal
import datetime
import subprocess
from pathlib import Path
import shutil

class SimpleHourlySystem:
    """シンプルな1時間毎システム（安全停止機能付き）"""
    
    def __init__(self, project_root: str = "/mnt/c/Desktop/Research"):
        self.project_root = Path(project_root)
        self.session_logs = self.project_root / "session_logs"
        self.session_logs.mkdir(exist_ok=True)
        
        # ログファイル
        self.system_log = self.session_logs / "simple_system.log"
        self.reports_archive = self.session_logs / "consolidated_reports.json"
        
        # セッション管理
        self.session_start = datetime.datetime.now()
        self.session_id = f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}"
        
        # 安全停止用ファイル
        self.heartbeat_file = self.session_logs / "system_heartbeat.json"
        self.session_state_file = self.session_logs / "session_state.json"
        self.current_session_file = self.session_logs / f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        self.running = True
        
        # セッション状態を記録
        self.save_session_state("started")
        
        # 終了時処理の設定（全シグナル対応）
        signal.signal(signal.SIGTERM, self.exit_handler)
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGHUP, self.exit_handler)
        signal.signal(signal.SIGQUIT, self.exit_handler)
        signal.signal(signal.SIGABRT, self.exit_handler)
        
        # 起動時に前回の異常終了をチェック
        self.check_previous_session()
        
        self.log_message(" Simple Hourly System started (Safe Shutdown Enabled)")
        self.log_message(f"🆔 Session ID: {self.session_id}")
    
    def save_session_state(self, status: str, extra_data: dict = None):
        """セッション状態を保存"""
        state_data = {
            "session_id": self.session_id,
            "status": status,
            "start_time": self.session_start.isoformat(),
            "last_update": datetime.datetime.now().isoformat(),
            "pid": os.getpid()
        }
        
        if extra_data:
            state_data.update(extra_data)
        
        try:
            with open(self.session_state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log_message(f" Could not save session state: {e}")
    
    def update_heartbeat(self):
        """ハートビート更新"""
        heartbeat_data = {
            "session_id": self.session_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "pid": os.getpid(),
            "status": "running"
        }
        
        try:
            with open(self.heartbeat_file, 'w', encoding='utf-8') as f:
                json.dump(heartbeat_data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # ハートビートエラーは無視
    
    def check_previous_session(self):
        """前回セッションの異常終了チェック"""
        if self.session_state_file.exists():
            try:
                with open(self.session_state_file, 'r', encoding='utf-8') as f:
                    prev_state = json.load(f)
                
                # 異常終了の判定を改善
                prev_status = prev_state.get("status")
                prev_session_id = prev_state.get("session_id", "")
                
                # 自分自身のセッションは除外
                if prev_session_id == self.session_id:
                    return
                
                if prev_status in ["started", "running", "shutting_down"]:
                    # 実際に異常終了かどうかをより詳しく確認
                    prev_pid = prev_state.get("pid")
                    if prev_pid and prev_pid != os.getpid():
                        try:
                            # プロセスがまだ生きているかチェック
                            os.kill(prev_pid, 0)
                            self.log_message(f" Previous session (PID: {prev_pid}) is still running")
                            return  # まだ動いているので復旧処理は不要
                        except ProcessLookupError:
                            # プロセスが見つからない = 異常終了
                            pass
                    
                    self.log_message(" Previous session ended unexpectedly")
                    self.log_message(f" Previous status: {prev_status}")
                    self.log_message(" Performing recovery cleanup...")
                    
                    # 復旧処理実行
                    self.perform_recovery_cleanup(prev_state)
                    
                    self.log_message(" Recovery cleanup completed")
                else:
                    self.log_message(f" Previous session ended normally: {prev_status}")
            
            except Exception as e:
                self.log_message(f" Could not check previous session: {e}")
    
    def perform_recovery_cleanup(self, prev_state: dict):
        """復旧時のクリーンアップ"""
        try:
            prev_start = datetime.datetime.fromisoformat(prev_state.get("start_time", ""))
            prev_duration = datetime.datetime.now() - prev_start
            
            self.log_message(f" Previous session duration: {str(prev_duration)}")
            
            # 復旧処理として基本的なクリーンアップを実行
            file_org = self.organize_files()
            github_status = self.check_github_status()
            reports_info = self.consolidate_reports()
            
            # 復旧レポート作成
            recovery_report = {
                "recovery_timestamp": datetime.datetime.now().isoformat(),
                "previous_session": prev_state,
                "previous_duration": str(prev_duration),
                "recovery_actions": {
                    "file_organization": file_org,
                    "github_status": github_status,
                    "reports_consolidation": reports_info
                }
            }
            
            # 復旧レポート保存
            recovery_file = self.session_logs / f"recovery_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(recovery_file, 'w', encoding='utf-8') as f:
                json.dump(recovery_report, f, indent=2, ensure_ascii=False)
            
            self.log_message(f" Recovery report saved: {recovery_file.name}")
        
        except Exception as e:
            self.log_message(f" Recovery cleanup error: {e}")
    
    def exit_handler(self, signum, frame):
        """終了時処理（シグナル対応）"""
        signal_names = {
            signal.SIGTERM: "SIGTERM (正常終了要求)",
            signal.SIGINT: "SIGINT (Ctrl+C)",
            signal.SIGHUP: "SIGHUP (ターミナル切断)",
            signal.SIGQUIT: "SIGQUIT (強制終了)",
            signal.SIGABRT: "SIGABRT (異常終了)"
        }
        
        signal_name = signal_names.get(signum, f"Signal {signum}")
        self.log_message(f"📡 Exit signal received: {signal_name}")
        self.log_message(" Performing safe shutdown...")
        
        # 安全な終了処理
        self.perform_safe_shutdown()
        
        self.log_message(" Safe shutdown completed")
        self.log_message("🛑 Simple Hourly System stopped")
        sys.exit(0)
    
    def log_message(self, message: str):
        """ログメッセージ出力"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        print(log_entry)
        
        try:
            with open(self.system_log, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception:
            pass
    
    def organize_files(self):
        """ファイル整理"""
        self.log_message(" Starting file organization...")
        
        organization_result = {
            "timestamp": datetime.datetime.now().isoformat(),
            "actions_performed": 0,
            "files_cleaned": 0
        }
        
        try:
            # 古いログファイルのアーカイブ（7日以上前）
            archive_dir = self.session_logs / "archive"
            archive_dir.mkdir(exist_ok=True)
            
            archived_count = 0
            for log_file in self.session_logs.glob("session_*.json"):
                if log_file.stat().st_mtime < time.time() - (7 * 24 * 3600):
                    target = archive_dir / log_file.name
                    shutil.move(str(log_file), str(target))
                    archived_count += 1
            
            # 一時ファイルの削除
            temp_files = list(self.project_root.rglob("*.tmp")) + \
                        list(self.session_logs.glob("temp_*.py"))
            
            cleaned_count = 0
            for temp_file in temp_files:
                if temp_file.is_file():
                    temp_file.unlink()
                    cleaned_count += 1
            
            # __pycache__ディレクトリの削除
            for pycache in self.project_root.rglob("__pycache__"):
                if pycache.is_dir():
                    shutil.rmtree(pycache)
                    cleaned_count += 1
            
            organization_result["actions_performed"] = archived_count + cleaned_count
            organization_result["files_cleaned"] = cleaned_count
            organization_result["archived_logs"] = archived_count
            
            self.log_message(f" File organization: {archived_count} archived, {cleaned_count} cleaned")
            return organization_result
            
        except Exception as e:
            self.log_message(f" File organization error: {e}")
            return {"error": str(e), "timestamp": datetime.datetime.now().isoformat()}
    
    def check_github_status(self):
        """GitHub状態確認"""
        self.log_message("🐙 Checking GitHub status...")
        
        github_result = {
            "timestamp": datetime.datetime.now().isoformat(),
            "branch": "",
            "total_changes": 0,
            "status_clean": False
        }
        
        try:
            os.chdir(self.project_root)
            
            # 現在のブランチ
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True)
            github_result["branch"] = branch_result.stdout.strip()
            
            # ステータス確認
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True)
            status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            
            github_result["total_changes"] = len(status_lines)
            github_result["status_clean"] = len(status_lines) == 0
            
            # 変更種別の詳細
            if status_lines:
                modified = len([l for l in status_lines if l.startswith(' M')])
                untracked = len([l for l in status_lines if l.startswith('??')])
                staged = len([l for l in status_lines if l.startswith('M ')])
                
                github_result.update({
                    "modified_files": modified,
                    "untracked_files": untracked,
                    "staged_files": staged
                })
            
            status_emoji = "" if github_result["status_clean"] else ""
            self.log_message(f" GitHub check: {status_emoji} {github_result['total_changes']} changes")
            return github_result
            
        except Exception as e:
            self.log_message(f" GitHub check error: {e}")
            return {"error": str(e), "timestamp": datetime.datetime.now().isoformat()}
    
    def consolidate_reports(self):
        """レポート統合・保存"""
        self.log_message(" Consolidating reports...")
        
        try:
            # 既存の統合レポート読み込み
            if self.reports_archive.exists():
                with open(self.reports_archive, 'r', encoding='utf-8') as f:
                    consolidated = json.load(f)
            else:
                consolidated = {
                    "created": datetime.datetime.now().isoformat(),
                    "sessions": []
                }
            
            # 新しいセッションデータ収集
            session_files = list(self.session_logs.glob("session_*.json"))
            new_sessions = 0
            
            for session_file in session_files:
                if session_file != self.reports_archive:
                    try:
                        with open(session_file, 'r', encoding='utf-8') as f:
                            session_data = json.load(f)
                            session_data["source_file"] = session_file.name
                            
                            # 重複チェック
                            existing = any(s.get("source_file") == session_file.name 
                                         for s in consolidated["sessions"])
                            if not existing:
                                consolidated["sessions"].append(session_data)
                                new_sessions += 1
                    except Exception as e:
                        self.log_message(f" Could not read {session_file.name}: {e}")
            
            # 統計情報更新
            total_sessions = len(consolidated["sessions"])
            consolidated["last_updated"] = datetime.datetime.now().isoformat()
            consolidated["total_sessions"] = total_sessions
            
            # 保存
            with open(self.reports_archive, 'w', encoding='utf-8') as f:
                json.dump(consolidated, f, indent=2, ensure_ascii=False)
            
            self.log_message(f" Reports consolidated: {total_sessions} total sessions")
            return {"total_sessions": total_sessions, "new_sessions": new_sessions}
            
        except Exception as e:
            self.log_message(f" Report consolidation error: {e}")
            return {"error": str(e)}
    
    def display_simple_report(self, file_org, github_status, reports_info, session_duration):
        """簡易レポート表示"""
        print("\n" + "="*50)
        print(" HOURLY REPORT")
        print("="*50)
        
        # 基本情報
        current_time = datetime.datetime.now()
        print(f" Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱  Session Duration: {session_duration}")
        
        # ファイル整理結果
        if "actions_performed" in file_org:
            print(f" Files: {file_org['actions_performed']} actions, {file_org.get('files_cleaned', 0)} cleaned")
        
        # GitHub状態
        if "total_changes" in github_status:
            status_emoji = "" if github_status.get("status_clean", False) else ""
            print(f"🐙 Git: {status_emoji} {github_status['total_changes']} changes")
            
            if not github_status.get("status_clean", True):
                print(" Recommendation: Consider committing pending changes")
        
        # レポート情報
        if "total_sessions" in reports_info:
            print(f" Reports: {reports_info['total_sessions']} sessions archived")
        
        print("="*50)
        next_hour = current_time + datetime.timedelta(hours=1)
        print(f" Next report: {next_hour.strftime('%H:%M')}")
        print("="*50 + "\n")
    
    def perform_hourly_tasks(self):
        """1時間毎タスク実行"""
        self.log_message(" Performing hourly tasks...")
        
        # 各タスク実行
        file_org = self.organize_files()
        github_status = self.check_github_status()
        reports_info = self.consolidate_reports()
        
        # セッション継続時間計算
        session_duration = str(datetime.datetime.now() - self.session_start)
        
        # 簡易レポート表示
        self.display_simple_report(file_org, github_status, reports_info, session_duration)
        
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "file_organization": file_org,
            "github_status": github_status,
            "reports_consolidation": reports_info,
            "session_duration": session_duration
        }
    
    def perform_safe_shutdown(self):
        """安全なシャットダウン処理"""
        try:
            self.log_message(" Performing safe shutdown tasks...")
            
            # セッション状態を終了中に更新
            self.save_session_state("shutting_down")
            
            # 最終タスク実行
            file_org = self.organize_files()
            github_status = self.check_github_status()
            reports_info = self.consolidate_reports()
            
            # 総セッション時間
            total_duration = datetime.datetime.now() - self.session_start
            
            # 最終レポート表示
            print("\n" + "="*60)
            print("🏁 SAFE SHUTDOWN REPORT")
            print("="*60)
            print(f" Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏱  Total duration: {str(total_duration)}")
            print(f" Final cleanup: {file_org.get('actions_performed', 0)} actions")
            print(f"🐙 Git status: {github_status.get('total_changes', 0)} changes")
            print(f" Total sessions: {reports_info.get('total_sessions', 0)}")
            print("="*60)
            print(" System safely stopped")
            print("="*60 + "\n")
            
            # セッション状態を正常終了に更新
            self.save_session_state("completed", {
                "end_time": datetime.datetime.now().isoformat(),
                "total_duration": str(total_duration),
                "final_cleanup": {
                    "file_organization": file_org,
                    "github_status": github_status,
                    "reports_consolidation": reports_info
                }
            })
            
            # ハートビートファイル削除
            if self.heartbeat_file.exists():
                self.heartbeat_file.unlink()
        
        except Exception as e:
            self.log_message(f" Error during safe shutdown: {e}")
            # エラーでも状態は記録
            self.save_session_state("error_shutdown", {"error": str(e)})
    
    def run(self):
        """メインループ実行"""
        self.log_message(" Starting hourly monitoring...")
        
        # 初回実行
        self.perform_hourly_tasks()
        
        # セッション状態を実行中に更新
        self.save_session_state("running")
        
        while self.running:
            try:
                # ハートビート更新
                self.update_heartbeat()
                
                # 1時間待機（10分ごとにハートビート更新）
                for i in range(6):  # 6回 × 10分 = 1時間
                    if not self.running:
                        break
                    time.sleep(600)  # 10分
                    if self.running:
                        self.update_heartbeat()
                
                if self.running:
                    self.perform_hourly_tasks()
            
            except KeyboardInterrupt:
                self.log_message(" Interrupted by user")
                break
            except Exception as e:
                self.log_message(f" Error in main loop: {e}")
                # エラー時もハートビート更新
                self.update_heartbeat()
                time.sleep(60)

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Hourly System')
    parser.add_argument('--project-root', default='/mnt/c/Desktop/Research',
                       help='Project root directory')
    parser.add_argument('--once', action='store_true', 
                       help='Run once and exit')
    
    args = parser.parse_args()
    
    try:
        system = SimpleHourlySystem(args.project_root)
        
        if args.once:
            system.perform_hourly_tasks()
            # --onceモードでは正常終了として記録
            system.save_session_state("completed", {
                "end_time": datetime.datetime.now().isoformat(),
                "total_duration": str(datetime.datetime.now() - system.session_start),
                "exit_mode": "once_flag"
            })
            print(" Single run completed")
        else:
            system.run()
    
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
        # Ctrl+C終了時も正常終了として記録
        if 'system' in locals():
            system.save_session_state("completed", {
                "end_time": datetime.datetime.now().isoformat(),
                "total_duration": str(datetime.datetime.now() - system.session_start),
                "exit_mode": "keyboard_interrupt"
            })
    except Exception as e:
        print(f" System error: {e}")
        # エラー終了時の記録
        if 'system' in locals():
            system.save_session_state("error", {
                "end_time": datetime.datetime.now().isoformat(),
                "error": str(e),
                "exit_mode": "exception"
            })

if __name__ == "__main__":
    main()