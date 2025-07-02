#!/usr/bin/env python3
"""
自動システム統合コーディネーター
複数の自動実行システムが競合しないよう管理する

主要機能:
1. 排他制御 - 同時実行の防止
2. 優先度管理 - 重要なシステムの優先実行
3. リソース監視 - CPU/メモリ使用量チェック
4. スケジューリング - 効率的な実行順序
5. ログ統合 - 全システムの動作ログ

使用方法:
from auto_system_coordinator import AutoCoordinator
coordinator = AutoCoordinator()
coordinator.register_system("textlint", "textlint_auto_runner.py", priority=2)
coordinator.start_coordination()
"""

import os
import json
import time
import fcntl
import signal
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable
import subprocess
import hashlib
from enum import Enum

class SystemPriority(Enum):
    """システム優先度"""
    CRITICAL = 1    # 最高優先度（復元、緊急処理）
    HIGH = 2        # 高優先度（保存、バックアップ）
    NORMAL = 3      # 通常優先度（textlint、監視）
    LOW = 4         # 低優先度（整理、最適化）

class SystemStatus(Enum):
    """システム状態"""
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    ERROR = "error"
    DISABLED = "disabled"

class AutoCoordinator:
    """自動システム統合コーディネーター"""
    
    def __init__(self):
        self.base_dir = "/mnt/c/Desktop/Research"
        self.coordination_dir = os.path.join(self.base_dir, ".auto_coordination")
        self.lock_dir = os.path.join(self.coordination_dir, "locks")
        self.log_file = os.path.join(self.coordination_dir, "coordination.log")
        self.config_file = os.path.join(self.coordination_dir, "coordinator_config.json")
        self.status_file = os.path.join(self.coordination_dir, "system_status.json")
        
        # ディレクトリ作成
        os.makedirs(self.coordination_dir, exist_ok=True)
        os.makedirs(self.lock_dir, exist_ok=True)
        
        # 登録システム
        self.registered_systems = {}
        self.system_processes = {}
        self.system_status = {}
        
        # 制御設定
        self.config = self._load_config()
        self.coordination_active = False
        self.coordination_thread = None
        
        # シグナルハンドラー設定
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _load_config(self) -> Dict:
        """設定読み込み"""
        default_config = {
            "max_concurrent_systems": 3,
            "resource_check_interval": 30,  # 秒
            "max_cpu_usage": 80,  # %
            "max_memory_usage": 80,  # %
            "timeout_seconds": 300,  # 5分
            "retry_attempts": 3,
            "enable_resource_monitoring": True,
            "enable_conflict_detection": True,
            "log_level": "INFO"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                default_config.update(loaded_config)
            except Exception as e:
                self._log(f"設定ファイル読み込みエラー: {e}")
        
        return default_config
    
    def _save_config(self):
        """設定保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _log(self, message: str, level: str = "INFO"):
        """ログ出力"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # ファイルに書き込み
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # コンソールにも出力（DEBUGレベル以外）
        if level != "DEBUG":
            print(f"🤖 Coordinator {level}: {message}")
    
    def register_system(self, 
                       system_id: str,
                       script_path: str,
                       priority: SystemPriority = SystemPriority.NORMAL,
                       max_execution_time: int = 300,
                       resource_requirements: Dict = None,
                       dependencies: List[str] = None,
                       conflict_systems: List[str] = None):
        """システム登録"""
        
        if resource_requirements is None:
            resource_requirements = {"cpu": 20, "memory": 100}  # MB
        
        if dependencies is None:
            dependencies = []
            
        if conflict_systems is None:
            conflict_systems = []
        
        system_info = {
            "system_id": system_id,
            "script_path": script_path,
            "priority": priority,
            "max_execution_time": max_execution_time,
            "resource_requirements": resource_requirements,
            "dependencies": dependencies,
            "conflict_systems": conflict_systems,
            "registered_at": datetime.now().isoformat(),
            "execution_count": 0,
            "last_execution": None,
            "last_success": None,
            "error_count": 0
        }
        
        self.registered_systems[system_id] = system_info
        self.system_status[system_id] = SystemStatus.IDLE
        
        self._log(f"システム登録: {system_id} (優先度: {priority.name})")
        self._save_status()
    
    def _save_status(self):
        """システム状態保存"""
        status_data = {
            "coordination_active": self.coordination_active,
            "last_updated": datetime.now().isoformat(),
            "systems": {}
        }
        
        for system_id, info in self.registered_systems.items():
            status_data["systems"][system_id] = {
                "status": self.system_status[system_id].value,
                "priority": info["priority"].name,
                "execution_count": info["execution_count"],
                "last_execution": info["last_execution"],
                "error_count": info["error_count"]
            }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, ensure_ascii=False, indent=2)
    
    def acquire_lock(self, system_id: str, operation: str = "default") -> bool:
        """ロック取得"""
        lock_file = os.path.join(self.lock_dir, f"{system_id}_{operation}.lock")
        
        try:
            # ロックファイル作成
            fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            
            # ロック情報書き込み
            lock_info = {
                "system_id": system_id,
                "operation": operation,
                "acquired_at": datetime.now().isoformat(),
                "pid": os.getpid()
            }
            
            os.write(fd, json.dumps(lock_info).encode())
            os.close(fd)
            
            self._log(f"ロック取得: {system_id} ({operation})", "DEBUG")
            return True
            
        except OSError:
            # ロック取得失敗
            return False
    
    def release_lock(self, system_id: str, operation: str = "default"):
        """ロック解放"""
        lock_file = os.path.join(self.lock_dir, f"{system_id}_{operation}.lock")
        
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                self._log(f"ロック解放: {system_id} ({operation})", "DEBUG")
        except Exception as e:
            self._log(f"ロック解放エラー: {system_id} - {e}")
    
    def _check_conflicts(self, system_id: str) -> List[str]:
        """競合チェック"""
        conflicts = []
        system_info = self.registered_systems[system_id]
        
        for conflict_system in system_info["conflict_systems"]:
            if (conflict_system in self.system_status and 
                self.system_status[conflict_system] == SystemStatus.RUNNING):
                conflicts.append(conflict_system)
        
        return conflicts
    
    def _check_dependencies(self, system_id: str) -> bool:
        """依存関係チェック"""
        system_info = self.registered_systems[system_id]
        
        for dependency in system_info["dependencies"]:
            if dependency not in self.registered_systems:
                self._log(f"依存システム未登録: {dependency}")
                return False
            
            # 依存システムが正常終了していない場合は待機
            dep_info = self.registered_systems[dependency]
            if (dep_info["last_execution"] and 
                not dep_info["last_success"]):
                return False
        
        return True
    
    def _check_resources(self) -> bool:
        """リソースチェック"""
        if not self.config["enable_resource_monitoring"]:
            return True
        
        try:
            # CPU使用率チェック（簡易版）
            loadavg = os.getloadavg()[0] * 100  # 1分平均
            if loadavg > self.config["max_cpu_usage"]:
                self._log(f"CPU使用率が高い: {loadavg:.1f}%")
                return False
            
            # メモリチェック（利用可能な場合）
            try:
                import psutil
                memory = psutil.virtual_memory()
                if memory.percent > self.config["max_memory_usage"]:
                    self._log(f"メモリ使用率が高い: {memory.percent:.1f}%")
                    return False
            except ImportError:
                pass  # psutilが利用できない場合はスキップ
            
            return True
            
        except Exception as e:
            self._log(f"リソースチェックエラー: {e}")
            return True  # エラー時は実行を許可
    
    def can_execute(self, system_id: str) -> Tuple[bool, str]:
        """実行可能性チェック"""
        if system_id not in self.registered_systems:
            return False, "システム未登録"
        
        if self.system_status[system_id] == SystemStatus.RUNNING:
            return False, "既に実行中"
        
        if self.system_status[system_id] == SystemStatus.DISABLED:
            return False, "システム無効"
        
        # 競合チェック
        conflicts = self._check_conflicts(system_id)
        if conflicts:
            return False, f"競合システム実行中: {', '.join(conflicts)}"
        
        # 依存関係チェック
        if not self._check_dependencies(system_id):
            return False, "依存関係未満たし"
        
        # リソースチェック
        if not self._check_resources():
            return False, "リソース不足"
        
        # 同時実行数チェック
        running_count = sum(1 for status in self.system_status.values() 
                          if status == SystemStatus.RUNNING)
        if running_count >= self.config["max_concurrent_systems"]:
            return False, "最大同時実行数に到達"
        
        return True, "実行可能"
    
    def execute_system(self, system_id: str, args: List[str] = None) -> bool:
        """システム実行"""
        can_exec, reason = self.can_execute(system_id)
        if not can_exec:
            self._log(f"実行不可: {system_id} - {reason}")
            return False
        
        # ロック取得
        if not self.acquire_lock(system_id, "execution"):
            self._log(f"ロック取得失敗: {system_id}")
            return False
        
        try:
            system_info = self.registered_systems[system_id]
            script_path = os.path.join(self.base_dir, system_info["script_path"])
            
            if not os.path.exists(script_path):
                self._log(f"スクリプトファイル未発見: {script_path}")
                return False
            
            # 実行コマンド構築
            cmd = ["python3", script_path]
            if args:
                cmd.extend(args)
            
            self._log(f"システム実行開始: {system_id}")
            self.system_status[system_id] = SystemStatus.RUNNING
            system_info["last_execution"] = datetime.now().isoformat()
            system_info["execution_count"] += 1
            
            # 実行
            start_time = time.time()
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True,
                    timeout=system_info["max_execution_time"]
                )
                
                execution_time = time.time() - start_time
                
                if result.returncode == 0:
                    self._log(f"システム実行成功: {system_id} ({execution_time:.1f}秒)")
                    system_info["last_success"] = datetime.now().isoformat()
                    self.system_status[system_id] = SystemStatus.IDLE
                    return True
                else:
                    self._log(f"システム実行失敗: {system_id} - {result.stderr}")
                    system_info["error_count"] += 1
                    self.system_status[system_id] = SystemStatus.ERROR
                    return False
                    
            except subprocess.TimeoutExpired:
                self._log(f"システム実行タイムアウト: {system_id}")
                system_info["error_count"] += 1
                self.system_status[system_id] = SystemStatus.ERROR
                return False
                
        except Exception as e:
            self._log(f"システム実行エラー: {system_id} - {e}")
            system_info["error_count"] += 1
            self.system_status[system_id] = SystemStatus.ERROR
            return False
            
        finally:
            self.release_lock(system_id, "execution")
            self._save_status()
    
    def get_execution_queue(self) -> List[str]:
        """実行キュー取得（優先度順）"""
        executable_systems = []
        
        for system_id in self.registered_systems:
            can_exec, _ = self.can_execute(system_id)
            if can_exec:
                executable_systems.append(system_id)
        
        # 優先度でソート
        executable_systems.sort(
            key=lambda x: self.registered_systems[x]["priority"].value
        )
        
        return executable_systems
    
    def start_coordination(self):
        """コーディネーション開始"""
        if self.coordination_active:
            self._log("コーディネーション既に実行中")
            return
        
        self.coordination_active = True
        self.coordination_thread = threading.Thread(target=self._coordination_loop)
        self.coordination_thread.daemon = True
        self.coordination_thread.start()
        
        self._log("自動システムコーディネーション開始")
    
    def stop_coordination(self):
        """コーディネーション停止"""
        self.coordination_active = False
        if self.coordination_thread:
            self.coordination_thread.join(timeout=5)
        
        self._log("自動システムコーディネーション停止")
    
    def _coordination_loop(self):
        """コーディネーションメインループ"""
        while self.coordination_active:
            try:
                # 実行可能なシステムを取得
                queue = self.get_execution_queue()
                
                for system_id in queue:
                    if not self.coordination_active:
                        break
                    
                    # リソースチェック
                    if not self._check_resources():
                        self._log("リソース不足のため実行スキップ")
                        time.sleep(self.config["resource_check_interval"])
                        continue
                    
                    # システム実行
                    self.execute_system(system_id)
                    
                    # 少し待機
                    time.sleep(1)
                
                # 次のチェックまで待機
                time.sleep(self.config["resource_check_interval"])
                
            except Exception as e:
                self._log(f"コーディネーションループエラー: {e}")
                time.sleep(5)
    
    def _signal_handler(self, signum, frame):
        """シグナルハンドラー"""
        self._log(f"シグナル受信: {signum}")
        self.stop_coordination()
    
    def get_status_report(self) -> str:
        """状態レポート生成"""
        report = f"""# 🤖 自動システムコーディネーター状態レポート

**生成時刻**: {datetime.now().isoformat()}
**コーディネーション状態**: {'✅ 実行中' if self.coordination_active else '❌ 停止中'}

## 📊 システム状態

"""
        
        for system_id, info in self.registered_systems.items():
            status = self.system_status[system_id]
            status_icon = {
                SystemStatus.IDLE: "⚪",
                SystemStatus.RUNNING: "🟢",
                SystemStatus.WAITING: "🟡",
                SystemStatus.ERROR: "🔴",
                SystemStatus.DISABLED: "⚫"
            }.get(status, "❓")
            
            report += f"### {status_icon} {system_id}\n"
            report += f"- **状態**: {status.value}\n"
            report += f"- **優先度**: {info['priority'].name}\n"
            report += f"- **実行回数**: {info['execution_count']}\n"
            report += f"- **エラー回数**: {info['error_count']}\n"
            
            if info['last_execution']:
                report += f"- **最終実行**: {info['last_execution']}\n"
            
            report += "\n"
        
        return report

# グローバルインスタンス
_coordinator = None

def get_coordinator():
    """コーディネーター取得"""
    global _coordinator
    if _coordinator is None:
        _coordinator = AutoCoordinator()
    return _coordinator

def register_system(system_id: str, script_path: str, priority: SystemPriority = SystemPriority.NORMAL, **kwargs):
    """システム登録（便利関数）"""
    coordinator = get_coordinator()
    coordinator.register_system(system_id, script_path, priority, **kwargs)

def execute_system(system_id: str, args: List[str] = None) -> bool:
    """システム実行（便利関数）"""
    coordinator = get_coordinator()
    return coordinator.execute_system(system_id, args)

def start_coordination():
    """コーディネーション開始（便利関数）"""
    coordinator = get_coordinator()
    coordinator.start_coordination()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 auto_system_coordinator.py status    # 状態表示")
        print("  python3 auto_system_coordinator.py start     # コーディネーション開始")
        print("  python3 auto_system_coordinator.py stop      # コーディネーション停止")
        print("  python3 auto_system_coordinator.py register  # デフォルトシステム登録")
        sys.exit(1)
    
    command = sys.argv[1]
    coordinator = get_coordinator()
    
    if command == "status":
        print(coordinator.get_status_report())
    elif command == "start":
        coordinator.start_coordination()
        print("コーディネーション開始しました")
        try:
            while coordinator.coordination_active:
                time.sleep(1)
        except KeyboardInterrupt:
            coordinator.stop_coordination()
    elif command == "stop":
        coordinator.stop_coordination()
        print("コーディネーション停止しました")
    elif command == "register":
        # デフォルトシステム登録
        coordinator.register_system(
            "auto_restore", "claude_auto_restore.py", 
            SystemPriority.CRITICAL,
            conflict_systems=["auto_save"]
        )
        coordinator.register_system(
            "auto_save", "auto_organize_and_save.py", 
            SystemPriority.HIGH,
            conflict_systems=["auto_restore"]
        )
        coordinator.register_system(
            "textlint_runner", "textlint_auto_runner.py", 
            SystemPriority.NORMAL
        )
        coordinator.register_system(
            "textlint_watcher", "textlint_watcher.py", 
            SystemPriority.NORMAL
        )
        coordinator.register_system(
            "dev_workflow", "auto_dev_workflow.py", 
            SystemPriority.NORMAL
        )
        print("デフォルトシステムを登録しました")
    else:
        print(f"不明なコマンド: {command}")