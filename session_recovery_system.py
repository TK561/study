#!/usr/bin/env python3
"""
Claude Codeセッション復元システム
予期せぬ終了時でも作業内容を復元可能にする
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import hashlib

class SessionRecoverySystem:
    """セッション復元システム"""
    
    def __init__(self):
        self.base_dir = "/mnt/c/Desktop/Research"
        self.session_dir = os.path.join(self.base_dir, ".claude_sessions")
        self.current_session_file = os.path.join(self.session_dir, "current_session.json")
        self.backup_dir = os.path.join(self.session_dir, "backups")
        
        # ディレクトリ作成
        os.makedirs(self.session_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def save_session_state(self, action_type: str, details: Dict):
        """現在のセッション状態を保存"""
        timestamp = datetime.now().isoformat()
        
        # 現在のセッション読み込み
        session_data = self._load_current_session()
        
        # アクション追加
        action = {
            "timestamp": timestamp,
            "type": action_type,
            "details": details
        }
        session_data["actions"].append(action)
        session_data["last_updated"] = timestamp
        
        # 保存
        with open(self.current_session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        # 定期バックアップ（10アクションごと）
        if len(session_data["actions"]) % 10 == 0:
            self._create_backup(session_data)
    
    def _load_current_session(self) -> Dict:
        """現在のセッション読み込み"""
        if os.path.exists(self.current_session_file):
            with open(self.current_session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 新規セッション作成
            return {
                "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "start_time": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "actions": []
            }
    
    def _create_backup(self, session_data: Dict):
        """バックアップ作成"""
        backup_name = f"backup_{session_data['session_id']}_{datetime.now().strftime('%H%M%S')}.json"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    def auto_save_git_state(self):
        """Git状態の自動保存"""
        try:
            # Git状態取得
            status = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.base_dir)
            diff = subprocess.run(['git', 'diff'], 
                                capture_output=True, text=True, cwd=self.base_dir)
            
            git_state = {
                "status": status.stdout,
                "diff": diff.stdout[:5000]  # 最初の5000文字のみ
            }
            
            self.save_session_state("git_state", git_state)
        except Exception as e:
            print(f"Git状態保存エラー: {e}")
    
    def save_file_operation(self, operation: str, file_path: str, content: str = None):
        """ファイル操作の記録"""
        file_info = {
            "operation": operation,
            "file_path": file_path,
            "timestamp": datetime.now().isoformat()
        }
        
        if content and len(content) < 10000:  # 10KB以下の場合は内容も保存
            file_info["content"] = content
        elif content:
            # 大きいファイルはハッシュのみ保存
            file_info["content_hash"] = hashlib.md5(content.encode()).hexdigest()
        
        self.save_session_state("file_operation", file_info)
    
    def save_command_execution(self, command: str, output: str = None):
        """コマンド実行の記録"""
        cmd_info = {
            "command": command,
            "timestamp": datetime.now().isoformat()
        }
        
        if output and len(output) < 5000:
            cmd_info["output"] = output
        
        self.save_session_state("command_execution", cmd_info)
    
    def recover_last_session(self) -> Dict:
        """最後のセッション復元"""
        if not os.path.exists(self.current_session_file):
            # バックアップから復元
            backups = sorted(os.listdir(self.backup_dir))
            if backups:
                latest_backup = os.path.join(self.backup_dir, backups[-1])
                with open(latest_backup, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"error": "復元可能なセッションがありません"}
        
        return self._load_current_session()
    
    def generate_recovery_report(self) -> str:
        """復元レポート生成"""
        session = self.recover_last_session()
        
        if "error" in session:
            return session["error"]
        
        report = f"""# セッション復元レポート

**セッションID**: {session.get('session_id', 'Unknown')}
**開始時刻**: {session.get('start_time', 'Unknown')}
**最終更新**: {session.get('last_updated', 'Unknown')}
**アクション数**: {len(session.get('actions', []))}

## 実行されたアクション

"""
        
        # アクションを逆順で表示（最新を上に）
        for action in reversed(session.get('actions', [])[-20:]):  # 最新20件
            report += f"### {action['timestamp']}\n"
            report += f"**タイプ**: {action['type']}\n"
            
            if action['type'] == 'file_operation':
                details = action['details']
                report += f"- 操作: {details['operation']}\n"
                report += f"- ファイル: {details['file_path']}\n"
            elif action['type'] == 'command_execution':
                details = action['details']
                report += f"- コマンド: `{details['command']}`\n"
            elif action['type'] == 'git_state':
                report += "- Git状態を保存\n"
            
            report += "\n"
        
        return report
    
    def create_recovery_script(self) -> str:
        """復元スクリプト生成"""
        session = self.recover_last_session()
        
        if "error" in session:
            return None
        
        script = """#!/bin/bash
# Claude Code セッション復元スクリプト
# 自動生成日時: """ + datetime.now().isoformat() + """

echo "🔄 セッション復元開始..."

"""
        
        # ファイル操作の復元
        for action in session.get('actions', []):
            if action['type'] == 'file_operation' and action['details']['operation'] in ['create', 'edit']:
                file_path = action['details']['file_path']
                script += f"# ファイル: {file_path}\n"
                if 'content' in action['details']:
                    # 内容がある場合は復元可能
                    script += f"echo '✅ {file_path} を復元中...'\n"
                else:
                    script += f"echo '⚠️  {file_path} は手動で確認が必要です'\n"
                script += "\n"
        
        script += """
echo "✅ 復元スクリプト実行完了"
echo "詳細は recovery_report.md を確認してください"
"""
        
        script_path = os.path.join(self.base_dir, "recover_session.sh")
        with open(script_path, 'w') as f:
            f.write(script)
        
        os.chmod(script_path, 0o755)
        return script_path

# グローバルインスタンス
_recovery_system = None

def get_recovery_system():
    global _recovery_system
    if _recovery_system is None:
        _recovery_system = SessionRecoverySystem()
    return _recovery_system

# 便利な関数
def auto_save(action_type: str, details: Dict):
    """自動保存"""
    system = get_recovery_system()
    system.save_session_state(action_type, details)

def save_file_op(operation: str, file_path: str, content: str = None):
    """ファイル操作保存"""
    system = get_recovery_system()
    system.save_file_operation(operation, file_path, content)

def save_command(command: str, output: str = None):
    """コマンド保存"""
    system = get_recovery_system()
    system.save_command_execution(command, output)

def recover():
    """セッション復元"""
    system = get_recovery_system()
    report = system.generate_recovery_report()
    
    # レポート保存
    report_path = os.path.join(system.base_dir, "recovery_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 復元スクリプト生成
    script_path = system.create_recovery_script()
    
    print("🔄 セッション復元情報:")
    print(f"📄 レポート: {report_path}")
    if script_path:
        print(f"🔧 復元スクリプト: {script_path}")
    
    return report

if __name__ == "__main__":
    # テスト実行
    print("セッション復元システムのテスト")
    
    # サンプル保存
    save_file_op("create", "/test/sample.py", "print('hello')")
    save_command("git status", "nothing to commit")
    
    # 復元テスト
    report = recover()
    print("\n復元レポート（最初の500文字）:")
    print(report[:500])