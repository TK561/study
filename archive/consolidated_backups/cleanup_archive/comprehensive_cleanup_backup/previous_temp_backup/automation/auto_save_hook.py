#!/usr/bin/env python3
"""
Claude Code自動保存フック
すべての操作を自動的に記録
"""

import functools
from session_recovery_system import save_file_op, save_command, auto_save

# ファイル操作の自動記録デコレータ
def track_file_operation(operation_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(file_path, *args, **kwargs):
            try:
                result = func(file_path, *args, **kwargs)
                
                # 内容を取得
                content = None
                if operation_type in ['write', 'create'] and args:
                    content = args[0] if isinstance(args[0], str) else str(args[0])
                
                # 保存
                save_file_op(operation_type, file_path, content)
                
                return result
            except Exception as e:
                save_file_op(f"{operation_type}_error", file_path, str(e))
                raise
        return wrapper
    return decorator

# コマンド実行の自動記録デコレータ
def track_command():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(command, *args, **kwargs):
            try:
                result = func(command, *args, **kwargs)
                
                # 出力を文字列化
                output = str(result) if result else None
                save_command(command, output)
                
                return result
            except Exception as e:
                save_command(command, f"Error: {str(e)}")
                raise
        return wrapper
    return decorator

# Claude Code用の統合フック
class AutoSaveHook:
    """自動保存を有効化するフック"""
    
    @staticmethod
    def enable():
        """自動保存を有効化"""
        print("✅ 自動保存フックを有効化しました")
        print("📁 セッションデータ: /mnt/c/Desktop/Research/.claude_sessions/")
        print("🔄 復元コマンド: python3 -c 'from session_recovery_system import recover; recover()'")
        
        # 初期状態を保存
        auto_save("session_start", {
            "message": "Claude Code自動保存開始",
            "auto_save_enabled": True
        })
    
    @staticmethod
    def status():
        """現在の保存状態を表示"""
        from session_recovery_system import get_recovery_system
        system = get_recovery_system()
        session = system._load_current_session()
        
        print(f"📊 セッション状態:")
        print(f"  - ID: {session.get('session_id', 'Unknown')}")
        print(f"  - アクション数: {len(session.get('actions', []))}")
        print(f"  - 最終更新: {session.get('last_updated', 'Unknown')}")

# 使用例
if __name__ == "__main__":
    # 自動保存有効化
    AutoSaveHook.enable()
    
    # テスト
    @track_file_operation('write')
    def test_write(path, content):
        print(f"Writing to {path}")
        return True
    
    @track_command()
    def test_command(cmd):
        print(f"Executing: {cmd}")
        return "Success"
    
    # テスト実行
    test_write("/test/file.txt", "Hello World")
    test_command("ls -la")
    
    # ステータス確認
    AutoSaveHook.status()