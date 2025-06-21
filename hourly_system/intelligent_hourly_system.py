#!/usr/bin/env python3
"""
Intelligent Hourly System - File Organization & GitHub Monitoring

Generated with Claude Code
Date: 2025-06-20
Purpose: 1時間毎のファイル整理・GitHub確認・レポート統合システム
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
from typing import Dict, List, Any, Optional
import shutil

class IntelligentHourlySystem:
    """賢い1時間毎システム（ターミナル依存型）"""
    
    def __init__(self, project_root: str = "/mnt/c/Desktop/Research"):
        self.project_root = Path(project_root)
        self.session_logs = self.project_root / "session_logs"
        self.session_logs.mkdir(exist_ok=True)
        
        # ログファイル
        self.system_log = self.session_logs / "intelligent_system.log"
        self.reports_archive = self.session_logs / "consolidated_reports.json"
        
        # システム状態
        self.running = True
        self.session_start = datetime.datetime.now()
        self.last_summary = self.session_start
        
        # 現在のセッション
        self.current_session = self.session_logs / f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        
        # シグナルハンドラー（ターミナル終了時に停止）
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGHUP, self.shutdown_handler)  # ターミナル終了時
        
        self.log_message(" Intelligent Hourly System started")
        self.log_message(f" Project: {self.project_root}")
        self.log_message(" Will stop when terminal/Claude Code exits")
    
    def shutdown_handler(self, signum, frame):
        """シャットダウンハンドラー"""
        self.log_message(f"📡 Shutdown signal received: {signum}")
        self.log_message("🛑 System stopping due to terminal/Claude Code exit")
        self.running = False
        self.generate_final_summary()
        sys.exit(0)
    
    def log_message(self, message: str):
        """ログメッセージ出力"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        # ターミナル表示
        print(log_entry)
        
        # ファイル保存
        try:
            with open(self.system_log, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception:
            pass
    
    def organize_files(self):
        """ファイル整理機能"""
        self.log_message(" Starting file organization...")
        
        organization_report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "actions": [],
            "statistics": {}
        }
        
        try:
            # 1. 古いログファイルを整理
            old_logs = []
            for log_file in self.session_logs.glob("session_*.json"):
                if log_file.stat().st_mtime < time.time() - (7 * 24 * 3600):  # 7日以上古い
                    old_logs.append(log_file.name)
            
            if old_logs:
                archive_dir = self.session_logs / "archive"
                archive_dir.mkdir(exist_ok=True)
                
                for log_name in old_logs:
                    source = self.session_logs / log_name
                    target = archive_dir / log_name
                    shutil.move(str(source), str(target))
                    organization_report["actions"].append(f"Archived: {log_name}")
            
            # 2. 一時ファイルクリーンアップ
            temp_files = list(self.project_root.rglob("*.tmp")) + \
                        list(self.project_root.rglob("__pycache__")) + \
                        list(self.session_logs.glob("temp_*.py"))
            
            for temp_file in temp_files:
                if temp_file.is_file():
                    temp_file.unlink()
                    organization_report["actions"].append(f"Deleted temp: {temp_file.name}")
                elif temp_file.is_dir():
                    shutil.rmtree(temp_file)
                    organization_report["actions"].append(f"Deleted temp dir: {temp_file.name}")
            
            # 3. ファイル統計
            organization_report["statistics"] = {
                "python_files": len(list(self.project_root.rglob("*.py"))),
                "markdown_files": len(list(self.project_root.rglob("*.md"))),
                "json_files": len(list(self.project_root.rglob("*.json"))),
                "total_files": len([f for f in self.project_root.rglob("*") if f.is_file()]),
                "archived_logs": len(old_logs),
                "cleaned_temp": len(temp_files)
            }
            
            self.log_message(f" File organization completed: {len(organization_report['actions'])} actions")
            return organization_report
            
        except Exception as e:
            self.log_message(f" File organization error: {e}")
            return {"error": str(e), "timestamp": datetime.datetime.now().isoformat()}
    
    def check_github_status(self):
        """GitHub状態確認"""
        self.log_message("🐙 Checking GitHub status...")
        
        github_report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "branch_info": {},
            "status": {},
            "recent_activity": {},
            "recommendations": []
        }
        
        try:
            os.chdir(self.project_root)
            
            # ブランチ情報
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True)
            github_report["branch_info"]["current"] = branch_result.stdout.strip()
            
            # ステータス
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True)
            status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            
            github_report["status"] = {
                "clean": len(status_lines) == 0,
                "modified_files": len([l for l in status_lines if l.startswith(' M')]),
                "untracked_files": len([l for l in status_lines if l.startswith('??')]),
                "staged_files": len([l for l in status_lines if l.startswith('M ')]),
                "total_changes": len(status_lines)
            }
            
            # 最近のコミット
            log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                      capture_output=True, text=True)
            github_report["recent_activity"]["recent_commits"] = log_result.stdout.strip().split('\n') if log_result.stdout else []
            
            # リモート同期状態
            try:
                fetch_result = subprocess.run(['git', 'fetch', '--dry-run'], 
                                            capture_output=True, text=True)
                github_report["recent_activity"]["sync_status"] = "up_to_date" if not fetch_result.stderr else "behind"
            except:
                github_report["recent_activity"]["sync_status"] = "unknown"
            
            # 推奨事項
            if github_report["status"]["total_changes"] > 0:
                github_report["recommendations"].append(" Consider committing pending changes")
            
            if github_report["status"]["untracked_files"] > 3:
                github_report["recommendations"].append(" Many untracked files - review and add to .gitignore")
            
            if len(github_report["recent_activity"]["recent_commits"]) == 0:
                github_report["recommendations"].append(" No recent commits - consider regular commits")
            
            self.log_message(f" GitHub check completed: {github_report['status']['total_changes']} changes detected")
            return github_report
            
        except Exception as e:
            self.log_message(f" GitHub check error: {e}")
            return {"error": str(e), "timestamp": datetime.datetime.now().isoformat()}
    
    def consolidate_reports(self):
        """レポート統合・整理"""
        self.log_message(" Consolidating reports...")
        
        try:
            # 既存の統合レポート読み込み
            if self.reports_archive.exists():
                with open(self.reports_archive, 'r', encoding='utf-8') as f:
                    consolidated = json.load(f)
            else:
                consolidated = {
                    "created": datetime.datetime.now().isoformat(),
                    "sessions": [],
                    "summary_statistics": {}
                }
            
            # 新しいセッションレポートを収集
            new_sessions = []
            for session_file in self.session_logs.glob("session_*.json"):
                if session_file != self.reports_archive:
                    try:
                        with open(session_file, 'r', encoding='utf-8') as f:
                            session_data = json.load(f)
                            session_data["file_name"] = session_file.name
                            new_sessions.append(session_data)
                    except Exception as e:
                        self.log_message(f" Could not read session file {session_file.name}: {e}")
            
            # 統計計算
            total_sessions = len(consolidated.get("sessions", [])) + len(new_sessions)
            total_summaries = sum(len(s.get("summaries", [])) for s in consolidated.get("sessions", []))
            total_summaries += sum(len(s.get("summaries", [])) for s in new_sessions)
            
            # 新しいセッション追加
            consolidated["sessions"].extend(new_sessions)
            consolidated["last_updated"] = datetime.datetime.now().isoformat()
            consolidated["summary_statistics"] = {
                "total_sessions": total_sessions,
                "total_summaries": total_summaries,
                "last_consolidation": datetime.datetime.now().isoformat()
            }
            
            # 保存
            with open(self.reports_archive, 'w', encoding='utf-8') as f:
                json.dump(consolidated, f, indent=2, ensure_ascii=False)
            
            self.log_message(f" Reports consolidated: {total_sessions} sessions, {total_summaries} summaries")
            return consolidated["summary_statistics"]
            
        except Exception as e:
            self.log_message(f" Report consolidation error: {e}")
            return {"error": str(e)}
    
    def generate_hourly_summary(self):
        """1時間毎総合サマリー生成"""
        current_time = datetime.datetime.now()
        self.log_message(" Generating hourly summary...")
        
        # 各機能実行
        file_org = self.organize_files()
        github_status = self.check_github_status()
        report_stats = self.consolidate_reports()
        
        # 総合サマリー
        summary = {
            "timestamp": current_time.isoformat(),
            "session_duration": str(current_time - self.session_start),
            "time_since_last": str(current_time - self.last_summary),
            "file_organization": file_org,
            "github_status": github_status,
            "report_consolidation": report_stats,
            "system_status": "active"
        }
        
        # セッションファイルに保存
        try:
            if self.current_session.exists():
                with open(self.current_session, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
            else:
                session_data = {
                    "session_start": self.session_start.isoformat(),
                    "project_root": str(self.project_root),
                    "summaries": []
                }
            
            session_data["summaries"].append(summary)
            
            with open(self.current_session, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            self.log_message(f" Error saving summary: {e}")
        
        # ターミナル用簡易表示
        self.display_simple_report(summary)
        
        self.last_summary = current_time
        return summary
    
    def display_simple_report(self, summary: dict):
        """ユーザー向け簡易レポート表示"""
        print("\n" + "="*60)
        print(" HOURLY SYSTEM REPORT")
        print("="*60)
        
        # 時刻情報
        timestamp = datetime.datetime.fromisoformat(summary["timestamp"])
        print(f" Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱  Duration: {summary['session_duration']}")
        
        # ファイル整理
        if "statistics" in summary.get("file_organization", {}):
            stats = summary["file_organization"]["statistics"]
            print(f" Files: {stats.get('total_files', 0)} total, {stats.get('cleaned_temp', 0)} cleaned")
        
        # GitHub状態
        if "status" in summary.get("github_status", {}):
            git_status = summary["github_status"]["status"]
            status_emoji = "" if git_status.get("clean", False) else ""
            print(f"🐙 Git: {status_emoji} {git_status.get('total_changes', 0)} changes")
        
        # 推奨事項
        recommendations = summary.get("github_status", {}).get("recommendations", [])
        if recommendations:
            print(" Recommendations:")
            for rec in recommendations[:3]:  # 最大3つまで表示
                print(f"   {rec}")
        
        print("="*60)
        print(f" Next report at: {(timestamp + datetime.timedelta(hours=1)).strftime('%H:%M')}")
        print("="*60 + "\n")
    
    def generate_final_summary(self):
        """最終サマリー生成"""
        self.log_message(" Generating final summary...")
        final_summary = self.generate_hourly_summary()
        final_summary["final_summary"] = True
        final_summary["total_runtime"] = str(datetime.datetime.now() - self.session_start)
        
        self.log_message(" Final summary completed")
        self.log_message("🛑 Intelligent Hourly System stopped")
    
    def run(self):
        """メインループ実行"""
        self.log_message(" Starting hourly monitoring loop...")
        
        # 初回サマリー
        self.generate_hourly_summary()
        
        while self.running:
            try:
                # 1時間待機
                time.sleep(3600)
                
                if self.running:
                    self.generate_hourly_summary()
            
            except KeyboardInterrupt:
                self.log_message(" Interrupted by user")
                break
            except Exception as e:
                self.log_message(f" Error in main loop: {e}")
                time.sleep(60)  # エラー時は1分待機

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Intelligent Hourly System')
    parser.add_argument('--project-root', default='/mnt/c/Desktop/Research',
                       help='Project root directory')
    parser.add_argument('--once', action='store_true', 
                       help='Run once and exit (for testing)')
    
    args = parser.parse_args()
    
    try:
        system = IntelligentHourlySystem(args.project_root)
        
        if args.once:
            # テスト用：一回だけ実行
            system.generate_hourly_summary()
        else:
            # 通常モード：継続実行
            system.run()
    
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
    except Exception as e:
        print(f" System error: {e}")

if __name__ == "__main__":
    main()