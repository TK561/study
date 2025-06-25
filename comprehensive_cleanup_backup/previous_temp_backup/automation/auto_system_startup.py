#!/usr/bin/env python3
"""
自動システム起動スクリプト - PC起動時に自動実行
"""

import os
import sys
import time
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime

class AutoSystemStartup:
    """自動システム起動管理"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "AUTO_STARTUP_CONFIG.json"
        self.log_file = self.project_root / "AUTO_STARTUP_LOG.json"
        self.config = self.load_config()
        self.running_processes = {}
        
    def load_config(self) -> dict:
        """設定を読み込み"""
        default_config = {
            "auto_monitor": True,
            "auto_git_sync": True,
            "auto_backup": True,
            "startup_delay": 5,
            "services": {
                "vercel_monitor": {
                    "enabled": True,
                    "command": "python3 auto_vercel_monitor.py start",
                    "restart_on_crash": True
                },
                "git_sync": {
                    "enabled": True,
                    "interval": 300,  # 5分毎
                    "command": "git pull origin main"
                },
                "backup_system": {
                    "enabled": True,
                    "interval": 3600,  # 1時間毎
                    "command": "python3 auto_backup_system.py run"
                }
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
            except:
                pass
        
        return default_config
    
    def save_config(self):
        """設定を保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def log_event(self, event_type: str, message: str, status: str = "info"):
        """イベントをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
            "status": status
        }
        
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                pass
        
        logs.append(log_entry)
        logs = logs[-500:]  # 最新500件のみ保持
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {event_type}: {message}")
    
    def start_vercel_monitor(self):
        """Vercelモニターを開始"""
        if not self.config['services']['vercel_monitor']['enabled']:
            return
        
        try:
            self.log_event("VERCEL_MONITOR", "開始中...", "info")
            
            process = subprocess.Popen([
                sys.executable, "auto_vercel_monitor.py", "start"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.running_processes['vercel_monitor'] = process
            self.log_event("VERCEL_MONITOR", "開始完了", "success")
            
        except Exception as e:
            self.log_event("VERCEL_MONITOR", f"開始失敗: {e}", "error")
    
    def start_git_sync(self):
        """Git同期を開始"""
        if not self.config['services']['git_sync']['enabled']:
            return
        
        def git_sync_loop():
            interval = self.config['services']['git_sync']['interval']
            while True:
                try:
                    self.log_event("GIT_SYNC", "同期中...", "info")
                    
                    result = subprocess.run([
                        'git', 'pull', 'origin', 'main'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        if "Already up to date" in result.stdout:
                            self.log_event("GIT_SYNC", "最新の状態", "info")
                        else:
                            self.log_event("GIT_SYNC", "更新を取得", "success")
                    else:
                        self.log_event("GIT_SYNC", f"エラー: {result.stderr}", "error")
                        
                except Exception as e:
                    self.log_event("GIT_SYNC", f"同期エラー: {e}", "error")
                
                time.sleep(interval)
        
        thread = threading.Thread(target=git_sync_loop, daemon=True)
        thread.start()
        self.log_event("GIT_SYNC", "自動同期開始", "success")
    
    def start_backup_system(self):
        """バックアップシステムを開始"""
        if not self.config['services']['backup_system']['enabled']:
            return
        
        def backup_loop():
            interval = self.config['services']['backup_system']['interval']
            while True:
                try:
                    self.log_event("BACKUP", "バックアップ中...", "info")
                    
                    # 重要なファイルをバックアップ
                    backup_files = [
                        "public/index.html",
                        "vercel.json",
                        "AUTO_STARTUP_CONFIG.json",
                        "VERCEL_UPDATE_HISTORY.json"
                    ]
                    
                    backup_dir = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_dir.mkdir(parents=True, exist_ok=True)
                    
                    import shutil
                    for file_path in backup_files:
                        if Path(file_path).exists():
                            shutil.copy2(file_path, backup_dir / Path(file_path).name)
                    
                    self.log_event("BACKUP", f"完了: {backup_dir}", "success")
                    
                except Exception as e:
                    self.log_event("BACKUP", f"エラー: {e}", "error")
                
                time.sleep(interval)
        
        thread = threading.Thread(target=backup_loop, daemon=True)
        thread.start()
        self.log_event("BACKUP", "自動バックアップ開始", "success")
    
    def install_dependencies(self):
        """必要な依存関係をインストール"""
        try:
            self.log_event("DEPENDENCIES", "依存関係チェック中...", "info")
            
            # watchdogが必要
            try:
                import watchdog
            except ImportError:
                self.log_event("DEPENDENCIES", "watchdogをインストール中...", "info")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'watchdog'], 
                             check=True, capture_output=True)
                self.log_event("DEPENDENCIES", "watchdogインストール完了", "success")
            
            # requestsが必要
            try:
                import requests
            except ImportError:
                self.log_event("DEPENDENCIES", "requestsをインストール中...", "info")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests'], 
                             check=True, capture_output=True)
                self.log_event("DEPENDENCIES", "requestsインストール完了", "success")
            
            self.log_event("DEPENDENCIES", "依存関係チェック完了", "success")
            
        except Exception as e:
            self.log_event("DEPENDENCIES", f"インストールエラー: {e}", "error")
    
    def create_windows_startup_script(self):
        """Windows起動スクリプトを作成"""
        try:
            # PowerShellスクリプトを作成
            ps_script = f"""
# Auto Vercel System Startup Script
Set-Location "{self.project_root}"
Start-Process python3 -ArgumentList "auto_system_startup.py", "start" -WindowStyle Hidden
"""
            
            ps_file = self.project_root / "auto_startup.ps1"
            with open(ps_file, 'w', encoding='utf-8') as f:
                f.write(ps_script)
            
            # バッチファイルを作成
            bat_script = f"""@echo off
cd /d "{self.project_root}"
python3 auto_system_startup.py start
"""
            
            bat_file = self.project_root / "auto_startup.bat"
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_script)
            
            self.log_event("STARTUP_SCRIPT", "起動スクリプト作成完了", "success")
            
            # スタートアップフォルダーへのショートカット作成方法を表示
            startup_folder = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
            print(f"\n📋 自動起動設定方法:")
            print(f"1. 以下のファイルをスタートアップフォルダーにコピー:")
            print(f"   {bat_file}")
            print(f"2. スタートアップフォルダー:")
            print(f"   {startup_folder}")
            print(f"3. または、以下のコマンドでコピー:")
            print(f'   copy "{bat_file}" "{startup_folder}"')
            
        except Exception as e:
            self.log_event("STARTUP_SCRIPT", f"作成エラー: {e}", "error")
    
    def start_all_services(self):
        """すべてのサービスを開始"""
        print("🚀 自動システム起動中...")
        print("=" * 50)
        
        # 依存関係インストール
        self.install_dependencies()
        
        # 起動遅延
        if self.config['startup_delay'] > 0:
            self.log_event("STARTUP", f"{self.config['startup_delay']}秒待機中...", "info")
            time.sleep(self.config['startup_delay'])
        
        # 各サービスを開始
        self.start_vercel_monitor()
        self.start_git_sync()
        self.start_backup_system()
        
        self.log_event("STARTUP", "すべてのサービス開始完了", "success")
        
        print("=" * 50)
        print("✅ 自動システム起動完了")
        print("📊 監視中のサービス:")
        for service, info in self.config['services'].items():
            if info['enabled']:
                print(f"  - {service}: 実行中")
        print("📝 ログ確認: python3 auto_system_startup.py log")
        print("🛑 停止: Ctrl+C")
        print("=" * 50)
        
        try:
            while True:
                time.sleep(10)
                # プロセスの健全性チェック
                self.check_process_health()
        except KeyboardInterrupt:
            print("\n👋 システムを停止します...")
            self.stop_all_services()
    
    def check_process_health(self):
        """プロセスの健全性をチェック"""
        for name, process in self.running_processes.items():
            if hasattr(process, 'poll') and process.poll() is not None:
                self.log_event("HEALTH_CHECK", f"{name}が停止しています", "warning")
                
                # 自動再起動
                if self.config['services'][name].get('restart_on_crash', False):
                    self.log_event("HEALTH_CHECK", f"{name}を再起動中...", "info")
                    if name == 'vercel_monitor':
                        self.start_vercel_monitor()
    
    def stop_all_services(self):
        """すべてのサービスを停止"""
        for name, process in self.running_processes.items():
            try:
                if hasattr(process, 'terminate'):
                    process.terminate()
                    process.wait(timeout=5)
                    self.log_event("SHUTDOWN", f"{name}停止完了", "success")
            except Exception as e:
                self.log_event("SHUTDOWN", f"{name}停止エラー: {e}", "error")
        
        self.log_event("SHUTDOWN", "システム停止完了", "success")

def main():
    """メイン関数"""
    startup = AutoSystemStartup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            startup.start_all_services()
        elif command == "install":
            startup.install_dependencies()
            startup.create_windows_startup_script()
            startup.save_config()
            print("✅ インストール完了")
        elif command == "config":
            print(json.dumps(startup.config, indent=2, ensure_ascii=False))
        elif command == "log":
            if startup.log_file.exists():
                with open(startup.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    for log in logs[-20:]:  # 最新20件
                        print(f"[{log['timestamp']}] {log['event_type']}: {log['message']}")
            else:
                print("📝 ログファイルが見つかりません")
        else:
            print("使用方法:")
            print("  python3 auto_system_startup.py start    - システム開始")
            print("  python3 auto_system_startup.py install  - 自動起動設定")
            print("  python3 auto_system_startup.py config   - 設定表示")
            print("  python3 auto_system_startup.py log      - ログ表示")
    else:
        startup.start_all_services()

if __name__ == "__main__":
    main()