#!/usr/bin/env python3
"""
Claude Code Startup Hook - Automatic Hourly System Launcher

Generated with Claude Code
Date: 2025-06-20
Purpose: Claude Code起動時に自動で1時間毎システムを開始
Verified: 実装済み
"""

import os
import sys
import json
import atexit
import signal
import datetime
import threading
import subprocess
from pathlib import Path

class ClaudeCodeStartupHook:
    """Claude Code起動時の自動実行システム"""
    
    def __init__(self):
        self.project_root = Path("/mnt/c/Desktop/Research")
        self.scripts_dir = self.project_root / "scripts"
        self.startup_log = self.project_root / "session_logs" / "startup.log"
        
        # 起動検出とシステム開始
        self.detect_and_start()
    
    def detect_claude_code_session(self):
        """Claude Codeセッションの検出"""
        
        detection_indicators = {
            'claude_md_exists': (self.project_root / "CLAUDE.md").exists(),
            'research_structure': (self.project_root / "study").exists(),
            'session_logs_dir': (self.project_root / "session_logs").exists(),
            'scripts_dir': self.scripts_dir.exists(),
            'is_git_repo': (self.project_root / ".git").exists()
        }
        
        # Claude Codeプロジェクトの確信度判定
        confidence_score = sum(detection_indicators.values()) / len(detection_indicators)
        
        return {
            'is_claude_code_project': confidence_score >= 0.8,
            'confidence': confidence_score,
            'indicators': detection_indicators
        }
    
    def check_existing_hourly_system(self):
        """既存の1時間システムの確認"""
        
        try:
            # プロセス確認
            result = subprocess.run(['pgrep', '-f', 'hourly_summary_system'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'running': True,
                    'pid': result.stdout.strip(),
                    'action': 'existing_system_detected'
                }
            else:
                return {
                    'running': False,
                    'pid': None,
                    'action': 'need_to_start'
                }
        
        except Exception as e:
            return {
                'running': False,
                'error': str(e),
                'action': 'need_to_start'
            }
    
    def start_hourly_system_daemon(self):
        """デーモンとして1時間システムを起動"""
        
        try:
            # バックグラウンドで起動
            startup_script = self.scripts_dir / "hourly_summary_system.py"
            
            # nohupで完全にバックグラウンド実行
            cmd = [
                'nohup', 
                'python3', 
                str(startup_script),
                '--daemon',  # デーモンモード
                '--project-root', 
                str(self.project_root)
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True  # セッションから独立
            )
            
            return {
                'success': True,
                'pid': process.pid,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_startup_indicator(self):
        """起動インジケーターファイルの作成"""
        
        startup_info = {
            'claude_code_session_start': datetime.datetime.now().isoformat(),
            'auto_hourly_system': True,
            'project_root': str(self.project_root),
            'startup_method': 'claude_code_trigger',
            'system_status': 'active'
        }
        
        # 起動ログに記録
        self.startup_log.parent.mkdir(exist_ok=True)
        
        with open(self.startup_log, 'a', encoding='utf-8') as f:
            f.write(f"\n[{datetime.datetime.now()}] Claude Code Startup Detected\n")
            f.write(f"Project: {self.project_root}\n")
            f.write(f"Hourly System: Auto-started\n")
            f.write("-" * 50 + "\n")
        
        # 状態ファイル作成
        status_file = self.project_root / "session_logs" / "current_session.json"
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(startup_info, f, indent=2, ensure_ascii=False)
    
    def setup_cleanup_hooks(self):
        """終了時のクリーンアップ設定"""
        
        def cleanup():
            """Claude Code終了時のクリーンアップ"""
            try:
                # 終了ログ
                with open(self.startup_log, 'a', encoding='utf-8') as f:
                    f.write(f"\n[{datetime.datetime.now()}] Claude Code Session Ended\n")
                
                # 状態ファイル更新
                status_file = self.project_root / "session_logs" / "current_session.json"
                if status_file.exists():
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                    
                    status['session_end'] = datetime.datetime.now().isoformat()
                    status['system_status'] = 'ended'
                    
                    with open(status_file, 'w', encoding='utf-8') as f:
                        json.dump(status, f, indent=2, ensure_ascii=False)
            
            except Exception as e:
                print(f"Cleanup error: {e}")
        
        # 終了フックの設定
        atexit.register(cleanup)
        signal.signal(signal.SIGTERM, lambda s, f: cleanup())
        signal.signal(signal.SIGINT, lambda s, f: cleanup())
    
    def detect_and_start(self):
        """メイン検出・起動プロセス"""
        
        # 1. Claude Codeプロジェクト検出
        detection = self.detect_claude_code_session()
        
        if not detection['is_claude_code_project']:
            # Claude Codeプロジェクトでない場合は何もしない
            return
        
        print(" Claude Code起動検出!")
        print(f" プロジェクト: {self.project_root}")
        print(f" 確信度: {detection['confidence']:.1%}")
        
        # 2. 既存システムチェック
        existing_system = self.check_existing_hourly_system()
        
        if existing_system['running']:
            print(f" 1時間システム既に動作中 (PID: {existing_system['pid']})")
            return
        
        # 3. 1時間システム自動起動
        print(" 1時間毎レポートシステムを自動起動中...")
        
        startup_result = self.start_hourly_system_daemon()
        
        if startup_result['success']:
            print(f" 自動起動成功! (PID: {startup_result['pid']})")
            print(" 1時間毎に作業まとめが自動生成されます")
        else:
            print(f" 自動起動失敗: {startup_result['error']}")
        
        # 4. 起動記録とクリーンアップ設定
        self.create_startup_indicator()
        self.setup_cleanup_hooks()

def auto_detect_and_start():
    """自動検出・起動の実行"""
    try:
        ClaudeCodeStartupHook()
    except Exception as e:
        print(f"Claude Code startup hook error: {e}")

# Claude Code起動時の自動実行
if __name__ == "__main__":
    auto_detect_and_start()

# モジュールインポート時の自動実行
auto_detect_and_start()