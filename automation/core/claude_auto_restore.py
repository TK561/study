#!/usr/bin/env python3
"""
Claude Code 自動復元システム
CLAUDE.mdの仕様に基づいた自動復元機能

使用方法:
- python3 claude_auto_restore.py enable    # 有効化
- python3 claude_auto_restore.py disable   # 無効化
- python3 claude_auto_restore.py status    # 状態確認
- python3 claude_auto_restore.py restore   # 手動復元

起動時自動実行:
- from claude_auto_restore import claude_startup
- claude_startup()
"""

import os
import json
import time
import hashlib
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import subprocess

# psutilの代替実装
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class ClaudeAutoRestore:
    """Claude Code自動復元システム"""
    
    def __init__(self):
        self.base_dir = "/mnt/c/Desktop/Research"
        self.sessions_dir = os.path.join(self.base_dir, ".claude_sessions")
        self.config_file = os.path.join(self.sessions_dir, "auto_restore_config.json")
        self.current_session_file = os.path.join(self.sessions_dir, "current_session.json")
        self.backups_dir = os.path.join(self.sessions_dir, "backups")
        
        # ディレクトリ作成
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.backups_dir, exist_ok=True)
        
        # 設定読み込み
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """設定ファイル読み込み"""
        default_config = {
            "enabled": False,
            "auto_backup_interval": 10,  # 10アクションごと
            "max_session_age_minutes": 5,  # 5分以上更新がないと異常終了と判定
            "max_backups": 50,
            "auto_detect_claude": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                default_config.update(loaded_config)
            except Exception as e:
                print(f"設定ファイル読み込みエラー: {e}")
        
        return default_config
    
    def _save_config(self):
        """設定ファイル保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def enable(self):
        """自動復元機能を有効化"""
        self.config["enabled"] = True
        self._save_config()
        print("✅ Claude Code自動復元機能が有効になりました")
        print("起動時に以下を実行してください:")
        print("```python")
        print("from claude_auto_restore import claude_startup")
        print("claude_startup()")
        print("```")
    
    def disable(self):
        """自動復元機能を無効化"""
        self.config["enabled"] = False
        self._save_config()
        print("❌ Claude Code自動復元機能が無効になりました")
    
    def status(self):
        """現在の状態を表示"""
        print("🔄 Claude Code自動復元システム状態")
        print("=" * 40)
        print(f"有効状態: {'✅ 有効' if self.config['enabled'] else '❌ 無効'}")
        print(f"自動バックアップ: {self.config['auto_backup_interval']}アクションごと")
        print(f"異常終了検出: {self.config['max_session_age_minutes']}分")
        
        # セッション情報
        if os.path.exists(self.current_session_file):
            session = self._load_current_session()
            print(f"現在のセッション: {session['session_id']}")
            print(f"開始時刻: {session['start_time']}")
            print(f"アクション数: {len(session['actions'])}")
            
            # 最終更新からの経過時間
            last_updated = datetime.fromisoformat(session['last_updated'])
            elapsed = datetime.now() - last_updated
            print(f"最終更新: {elapsed.total_seconds():.1f}秒前")
        else:
            print("現在のセッション: なし")
        
        # バックアップ情報
        backups = self._get_backup_files()
        print(f"バックアップ数: {len(backups)}")
        
        # Claude Code プロセス検出
        claude_running = self._is_claude_code_running()
        print(f"Claude Code実行中: {'✅ はい' if claude_running else '❌ いいえ'}")
    
    def _is_claude_code_running(self) -> bool:
        """Claude Codeが実行中かチェック"""
        if PSUTIL_AVAILABLE:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'claude' in cmdline.lower() and 'code' in cmdline.lower():
                            return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                return False
            except Exception:
                return False
        else:
            # psutil未インストールの場合は簡易チェック
            try:
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                return 'claude' in result.stdout.lower() and 'code' in result.stdout.lower()
            except Exception:
                return False
    
    def _load_current_session(self) -> Dict:
        """現在のセッション読み込み"""
        if os.path.exists(self.current_session_file):
            with open(self.current_session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._create_new_session()
    
    def _create_new_session(self) -> Dict:
        """新しいセッション作成"""
        session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "actions": [],
            "files_created": [],
            "files_modified": [],
            "commands_executed": []
        }
        self._save_session(session)
        return session
    
    def _save_session(self, session: Dict):
        """セッション保存"""
        session["last_updated"] = datetime.now().isoformat()
        with open(self.current_session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        
        # 自動バックアップ
        if len(session["actions"]) % self.config["auto_backup_interval"] == 0:
            self._create_backup(session)
    
    def _create_backup(self, session: Dict):
        """バックアップ作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backups_dir, f"session_backup_{timestamp}.json")
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        
        # 古いバックアップ削除
        self._cleanup_old_backups()
    
    def _cleanup_old_backups(self):
        """古いバックアップファイル削除"""
        backups = self._get_backup_files()
        if len(backups) > self.config["max_backups"]:
            # 古いものから削除
            for backup in backups[self.config["max_backups"]:]:
                os.remove(backup)
    
    def _get_backup_files(self) -> List[str]:
        """バックアップファイル一覧取得（新しい順）"""
        if not os.path.exists(self.backups_dir):
            return []
        
        backups = []
        for file in os.listdir(self.backups_dir):
            if file.startswith("session_backup_") and file.endswith(".json"):
                full_path = os.path.join(self.backups_dir, file)
                backups.append(full_path)
        
        # 更新時刻でソート（新しい順）
        backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return backups
    
    def save_action(self, action_type: str, details: Dict):
        """アクション保存"""
        if not self.config["enabled"]:
            return
        
        session = self._load_current_session()
        
        action = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "details": details
        }
        
        session["actions"].append(action)
        
        # ファイル操作の場合はリストに追加
        if action_type == "file_create":
            session["files_created"].append(details.get("file_path"))
        elif action_type == "file_modify":
            session["files_modified"].append(details.get("file_path"))
        elif action_type == "command":
            session["commands_executed"].append(details.get("command"))
        
        self._save_session(session)
    
    def detect_abnormal_termination(self) -> bool:
        """異常終了検出"""
        if not os.path.exists(self.current_session_file):
            return False
        
        session = self._load_current_session()
        last_updated = datetime.fromisoformat(session["last_updated"])
        
        # 最終更新から指定時間以上経過している場合は異常終了と判定
        elapsed = datetime.now() - last_updated
        max_age = timedelta(minutes=self.config["max_session_age_minutes"])
        
        return elapsed > max_age
    
    def get_recovery_options(self) -> List[Dict]:
        """復元オプション取得"""
        options = []
        
        # 現在のセッション
        if os.path.exists(self.current_session_file):
            session = self._load_current_session()
            options.append({
                "type": "current",
                "session_id": session["session_id"],
                "description": f"現在のセッション ({len(session['actions'])}アクション)",
                "timestamp": session["last_updated"],
                "data": session
            })
        
        # バックアップ
        backups = self._get_backup_files()
        for i, backup_file in enumerate(backups[:10]):  # 最新10件
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_session = json.load(f)
                
                options.append({
                    "type": "backup",
                    "session_id": backup_session["session_id"],
                    "description": f"バックアップ#{i+1} ({len(backup_session['actions'])}アクション)",
                    "timestamp": backup_session["last_updated"],
                    "data": backup_session
                })
            except Exception:
                continue
        
        return options
    
    def generate_recovery_report(self, session_data: Dict) -> str:
        """復元レポート生成"""
        report = f"""# 🔄 自動復元レポート

## セッション情報
- **セッションID**: {session_data['session_id']}
- **開始時刻**: {session_data['start_time']}
- **最終更新**: {session_data['last_updated']}
- **総アクション数**: {len(session_data['actions'])}

## ファイル操作
- **作成**: {len(session_data.get('files_created', []))}件
- **変更**: {len(session_data.get('files_modified', []))}件

## コマンド実行
- **実行回数**: {len(session_data.get('commands_executed', []))}回

## 最近のアクション（最新10件）
"""
        
        recent_actions = session_data['actions'][-10:]
        for action in reversed(recent_actions):
            report += f"\n### {action['timestamp']}\n"
            report += f"**タイプ**: {action['type']}\n"
            
            details = action['details']
            if action['type'] == 'file_create':
                report += f"- 作成: `{details.get('file_path', 'Unknown')}`\n"
            elif action['type'] == 'file_modify':
                report += f"- 変更: `{details.get('file_path', 'Unknown')}`\n"
            elif action['type'] == 'command':
                report += f"- コマンド: `{details.get('command', 'Unknown')}`\n"
            else:
                report += f"- 詳細: {details}\n"
        
        return report
    
    def auto_restore_prompt(self) -> Optional[Dict]:
        """自動復元プロンプト"""
        if not self.config["enabled"]:
            return None
        
        abnormal = self.detect_abnormal_termination()
        if not abnormal:
            return None
        
        print("🚨 異常終了を検出しました")
        print("前回のセッションを復元しますか？")
        
        options = self.get_recovery_options()
        if not options:
            print("復元可能なセッションがありません")
            return None
        
        print("\n復元オプション:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option['description']} - {option['timestamp']}")
        
        print("0. 復元しない")
        
        # 5秒後に自動選択
        print("\n5秒後に最新セッションを自動復元します...")
        for i in range(5, 0, -1):
            print(f"\r{i}秒後に自動復元... (何かキーを押してキャンセル)", end="", flush=True)
            time.sleep(1)
        
        print("\n自動復元を実行します")
        return options[0]
    
    def restore_session(self, session_data: Dict):
        """セッション復元実行"""
        # 復元レポート生成
        report = self.generate_recovery_report(session_data)
        report_file = os.path.join(self.base_dir, "auto_recovery_report.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 復元レポートを生成しました: {report_file}")
        
        # セッションを新規開始
        new_session = self._create_new_session()
        print(f"新しいセッションを開始しました: {new_session['session_id']}")
        
        return report_file

# グローバルインスタンス
_restore_system = None

def get_restore_system():
    """復元システム取得"""
    global _restore_system
    if _restore_system is None:
        _restore_system = ClaudeAutoRestore()
    return _restore_system

def claude_startup():
    """Claude Code起動時実行関数"""
    print("🔄 Claude Code自動復元システム起動")
    
    system = get_restore_system()
    
    if not system.config["enabled"]:
        print("自動復元機能は無効です")
        print("有効にするには: python3 claude_auto_restore.py enable")
        return
    
    # 異常終了検出
    recovery_option = system.auto_restore_prompt()
    
    if recovery_option:
        system.restore_session(recovery_option["data"])
    else:
        print("新しいセッションを開始します")
        system._create_new_session()

# 便利な関数
def save_file_create(file_path: str, content: str = None):
    """ファイル作成記録"""
    system = get_restore_system()
    details = {"file_path": file_path}
    if content and len(content) < 10000:
        details["content_preview"] = content[:1000]
    system.save_action("file_create", details)

def save_file_modify(file_path: str, content: str = None):
    """ファイル変更記録"""
    system = get_restore_system()
    details = {"file_path": file_path}
    if content and len(content) < 10000:
        details["content_preview"] = content[:1000]
    system.save_action("file_modify", details)

def save_command(command: str, output: str = None):
    """コマンド実行記録"""
    system = get_restore_system()
    details = {"command": command}
    if output and len(output) < 5000:
        details["output"] = output[:2000]
    system.save_action("command", details)

def main():
    """コマンドライン実行"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 claude_auto_restore.py enable   # 有効化")
        print("  python3 claude_auto_restore.py disable  # 無効化")
        print("  python3 claude_auto_restore.py status   # 状態確認")
        print("  python3 claude_auto_restore.py restore  # 手動復元")
        return
    
    command = sys.argv[1]
    system = get_restore_system()
    
    if command == "enable":
        system.enable()
    elif command == "disable":
        system.disable()
    elif command == "status":
        system.status()
    elif command == "restore":
        recovery_option = system.auto_restore_prompt()
        if recovery_option:
            system.restore_session(recovery_option["data"])
        else:
            print("復元をキャンセルしました")
    else:
        print(f"不明なコマンド: {command}")

if __name__ == "__main__":
    main()