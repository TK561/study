#!/usr/bin/env python3
"""
自動マスターコントローラー - すべての自動システムを統括管理
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class AutoMasterController:
    """自動マスターコントローラー"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "AUTO_MASTER_CONFIG.json"
        self.log_file = self.project_root / "AUTO_MASTER_LOG.json"
        self.status_file = self.project_root / "AUTO_MASTER_STATUS.json"
        self.config = self.load_config()
        self.services = {}
        self.running = False
        
    def load_config(self) -> Dict:
        """設定を読み込み"""
        default_config = {
            "services": {
                "vercel_monitor": {
                    "enabled": True,
                    "script": "auto_vercel_monitor.py",
                    "args": ["start"],
                    "restart_on_crash": True,
                    "health_check_interval": 60
                },
                "git_manager": {
                    "enabled": True,
                    "script": "auto_git_manager.py",
                    "args": ["start"],
                    "restart_on_crash": True,
                    "health_check_interval": 60
                },
                "backup_system": {
                    "enabled": True,
                    "script": "auto_backup_system.py",
                    "args": [],
                    "restart_on_crash": False,
                    "schedule_interval": 3600  # 1時間毎
                },
                "system_startup": {
                    "enabled": False,  # 無限ループを避けるため
                    "script": "auto_system_startup.py",
                    "args": ["start"],
                    "restart_on_crash": False,
                    "health_check_interval": 300
                }
            },
            "master_settings": {
                "startup_delay": 10,
                "health_check_interval": 30,
                "crash_restart_delay": 5,
                "max_restart_attempts": 3,
                "log_retention_days": 7
            },
            "notifications": {
                "service_start": True,
                "service_stop": True,
                "service_crash": True,
                "health_check_fail": True
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
    
    def log_event(self, event_type: str, service: str, message: str, status: str = "info"):
        """イベントをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "service": service,
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
        logs = logs[-1000:]  # 最新1000件のみ保持
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {service}: {message}")
    
    def update_status(self):
        """ステータスファイルを更新"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "master_running": self.running,
            "services": {}
        }
        
        for service_name, service_info in self.services.items():
            status["services"][service_name] = {
                "running": service_info.get("process") is not None,
                "pid": service_info.get("process").pid if service_info.get("process") else None,
                "restart_count": service_info.get("restart_count", 0),
                "last_start": service_info.get("last_start"),
                "last_health_check": service_info.get("last_health_check")
            }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
    
    def install_dependencies(self):
        """必要な依存関係をインストール"""
        dependencies = ["watchdog", "requests"]
        
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                self.log_event("DEPENDENCIES", "master", f"{dep}をインストール中...", "info")
                try:
                    subprocess.run([
                        sys.executable, '-m', 'pip', 'install', dep
                    ], check=True, capture_output=True)
                    self.log_event("DEPENDENCIES", "master", f"{dep}インストール完了", "success")
                except Exception as e:
                    self.log_event("DEPENDENCIES", "master", f"{dep}インストール失敗: {e}", "error")
    
    def start_service(self, service_name: str) -> bool:
        """サービスを開始"""
        service_config = self.config["services"].get(service_name)
        if not service_config or not service_config.get("enabled"):
            return False
        
        try:
            script_path = self.project_root / service_config["script"]
            if not script_path.exists():
                self.log_event("START", service_name, f"スクリプトが見つかりません: {script_path}", "error")
                return False
            
            # プロセスを開始
            command = [sys.executable, str(script_path)] + service_config.get("args", [])
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.project_root
            )
            
            self.services[service_name] = {
                "process": process,
                "config": service_config,
                "start_time": datetime.now(),
                "restart_count": self.services.get(service_name, {}).get("restart_count", 0),
                "last_start": datetime.now().isoformat(),
                "last_health_check": None
            }
            
            self.log_event("START", service_name, f"開始成功 (PID: {process.pid})", "success")
            return True
            
        except Exception as e:
            self.log_event("START", service_name, f"開始失敗: {e}", "error")
            return False
    
    def stop_service(self, service_name: str) -> bool:
        """サービスを停止"""
        if service_name not in self.services:
            return False
        
        service_info = self.services[service_name]
        process = service_info.get("process")
        
        if not process:
            return False
        
        try:
            process.terminate()
            process.wait(timeout=10)
            self.log_event("STOP", service_name, "停止完了", "success")
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            self.log_event("STOP", service_name, "強制停止", "warning")
        except Exception as e:
            self.log_event("STOP", service_name, f"停止エラー: {e}", "error")
            return False
        
        self.services[service_name]["process"] = None
        return True
    
    def restart_service(self, service_name: str) -> bool:
        """サービスを再起動"""
        self.log_event("RESTART", service_name, "再起動中...", "info")
        
        # 停止
        self.stop_service(service_name)
        
        # 少し待機
        time.sleep(self.config["master_settings"]["crash_restart_delay"])
        
        # 再起動カウントを増加
        if service_name in self.services:
            self.services[service_name]["restart_count"] = \
                self.services[service_name].get("restart_count", 0) + 1
        
        # 開始
        return self.start_service(service_name)
    
    def check_service_health(self, service_name: str) -> bool:
        """サービスの健全性をチェック"""
        if service_name not in self.services:
            return False
        
        service_info = self.services[service_name]
        process = service_info.get("process")
        
        if not process:
            return False
        
        # プロセスが生きているかチェック
        if process.poll() is not None:
            self.log_event("HEALTH", service_name, "プロセス停止を検出", "error")
            return False
        
        # 最後のヘルスチェック時刻を記録
        self.services[service_name]["last_health_check"] = datetime.now().isoformat()
        
        return True
    
    def run_scheduled_task(self, service_name: str):
        """スケジュールされたタスクを実行"""
        service_config = self.config["services"].get(service_name)
        if not service_config:
            return
        
        try:
            script_path = self.project_root / service_config["script"]
            command = [sys.executable, str(script_path)] + service_config.get("args", [])
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5分タイムアウト
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                self.log_event("SCHEDULED", service_name, "タスク実行成功", "success")
            else:
                self.log_event("SCHEDULED", service_name, f"タスク実行失敗: {result.stderr}", "error")
                
        except Exception as e:
            self.log_event("SCHEDULED", service_name, f"タスク実行エラー: {e}", "error")
    
    def start_all_services(self):
        """すべてのサービスを開始"""
        self.log_event("MASTER", "master", "マスターコントローラー開始", "info")
        
        # 依存関係インストール
        self.install_dependencies()
        
        # 起動遅延
        startup_delay = self.config["master_settings"]["startup_delay"]
        if startup_delay > 0:
            self.log_event("MASTER", "master", f"{startup_delay}秒待機中...", "info")
            time.sleep(startup_delay)
        
        # サービス開始
        for service_name, service_config in self.config["services"].items():
            if service_config.get("enabled"):
                if "schedule_interval" in service_config:
                    # スケジュールタスクは別途管理
                    self.log_event("MASTER", service_name, "スケジュールタスクとして登録", "info")
                else:
                    # 常駐サービス
                    self.start_service(service_name)
        
        self.running = True
        self.update_status()
        
        # メインループ
        self.run_main_loop()
    
    def run_main_loop(self):
        """メインループ"""
        last_scheduled_run = {}
        
        try:
            while self.running:
                current_time = time.time()
                
                # ヘルスチェック
                for service_name in list(self.services.keys()):
                    service_info = self.services[service_name]
                    service_config = service_info.get("config", {})
                    
                    # 常駐サービスのヘルスチェック
                    if "schedule_interval" not in service_config:
                        if not self.check_service_health(service_name):
                            # 再起動が有効な場合
                            if service_config.get("restart_on_crash"):
                                restart_count = service_info.get("restart_count", 0)
                                max_attempts = self.config["master_settings"]["max_restart_attempts"]
                                
                                if restart_count < max_attempts:
                                    self.restart_service(service_name)
                                else:
                                    self.log_event("HEALTH", service_name, 
                                                  f"最大再起動回数に達しました ({max_attempts})", "error")
                
                # スケジュールタスク実行
                for service_name, service_config in self.config["services"].items():
                    if not service_config.get("enabled"):
                        continue
                        
                    schedule_interval = service_config.get("schedule_interval")
                    if schedule_interval:
                        last_run = last_scheduled_run.get(service_name, 0)
                        if current_time - last_run >= schedule_interval:
                            self.run_scheduled_task(service_name)
                            last_scheduled_run[service_name] = current_time
                
                # ステータス更新
                self.update_status()
                
                # 少し待機
                time.sleep(self.config["master_settings"]["health_check_interval"])
                
        except KeyboardInterrupt:
            self.log_event("MASTER", "master", "停止要求を受信", "info")
        
        self.shutdown()
    
    def shutdown(self):
        """シャットダウン"""
        self.log_event("MASTER", "master", "シャットダウン開始", "info")
        self.running = False
        
        # すべてのサービスを停止
        for service_name in list(self.services.keys()):
            self.stop_service(service_name)
        
        self.update_status()
        self.log_event("MASTER", "master", "シャットダウン完了", "success")
    
    def show_status(self):
        """現在の状態を表示"""
        print("🎛️ マスターコントローラー状態")
        print("=" * 50)
        
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    status = json.load(f)
                
                print(f"📅 最終更新: {status['timestamp']}")
                print(f"🎯 マスター稼働: {'✅' if status['master_running'] else '❌'}")
                print("\n📋 サービス状態:")
                
                for service_name, service_status in status['services'].items():
                    running_icon = "🟢" if service_status['running'] else "🔴"
                    print(f"  {running_icon} {service_name}")
                    if service_status['running']:
                        print(f"    PID: {service_status['pid']}")
                        print(f"    再起動回数: {service_status['restart_count']}")
                    
            except Exception as e:
                print(f"❌ ステータス読み込みエラー: {e}")
        else:
            print("📝 ステータスファイルが見つかりません")

def main():
    """メイン関数"""
    controller = AutoMasterController()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            controller.start_all_services()
        elif command == "stop":
            controller.shutdown()
        elif command == "status":
            controller.show_status()
        elif command == "restart" and len(sys.argv) > 2:
            service_name = sys.argv[2]
            controller.restart_service(service_name)
        elif command == "config":
            print(json.dumps(controller.config, indent=2, ensure_ascii=False))
        elif command == "log":
            if controller.log_file.exists():
                with open(controller.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    for log in logs[-30:]:  # 最新30件
                        print(f"[{log['timestamp']}] {log['service']}: {log['message']}")
            else:
                print("📝 ログファイルが見つかりません")
        elif command == "install":
            controller.install_dependencies()
            controller.save_config()
            print("✅ インストール完了")
        else:
            print("使用方法:")
            print("  python3 auto_master_controller.py start           - 全システム開始")
            print("  python3 auto_master_controller.py stop            - 全システム停止")
            print("  python3 auto_master_controller.py status          - 状態表示")
            print("  python3 auto_master_controller.py restart <name>  - サービス再起動")
            print("  python3 auto_master_controller.py config          - 設定表示")
            print("  python3 auto_master_controller.py log             - ログ表示")
            print("  python3 auto_master_controller.py install         - 初期セットアップ")
    else:
        controller.start_all_services()

if __name__ == "__main__":
    main()