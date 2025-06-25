#!/usr/bin/env python3
"""
自動意図記録フック
ファイル操作を監視してバックグラウンドで自動的に意図を記録
"""

import functools
import os
from universal_intent_system import auto_intent_record

def auto_intent_hook(operation_type: str):
    """ファイル操作を自動的に記録するデコレータ"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 元の処理を実行
            result = func(*args, **kwargs)
            
            try:
                # ファイルパスを抽出
                file_path = None
                content_sample = ""
                
                if args:
                    # 最初の引数がファイルパスの場合
                    if isinstance(args[0], str) and ('/' in args[0] or '\\' in args[0] or args[0].endswith(('.py', '.js', '.md', '.json'))):
                        file_path = args[0]
                        
                        # 内容のサンプルを取得（書き込み操作の場合）
                        if operation_type in ['write', 'create'] and len(args) > 1:
                            content_sample = str(args[1])[:500]  # 最初の500文字
                
                # ファイルパスが特定できた場合は自動記録
                if file_path and os.path.basename(file_path) not in ['', '.', '..']:
                    auto_intent_record(file_path, operation_type, content_sample)
            
            except Exception as e:
                # エラーが発生しても元の処理は継続
                pass
            
            return result
        return wrapper
    return decorator

# Claude Code標準関数のフック例
def setup_auto_hooks():
    """自動フックのセットアップ"""
    
    # builtinsのopen関数をフック（書き込みモード）
    import builtins
    original_open = builtins.open
    
    @functools.wraps(original_open)
    def hooked_open(file, mode='r', *args, **kwargs):
        result = original_open(file, mode, *args, **kwargs)
        
        # 書き込みモードの場合は記録
        if 'w' in mode or 'a' in mode:
            try:
                auto_intent_record(file, 'write' if 'w' in mode else 'append')
            except:
                pass
        
        return result
    
    # builtins.open を置き換え
    builtins.open = hooked_open
    
    print("✅ 自動意図記録フックを設定しました")

# Claude Code統合用の便利関数
def claude_write_with_intent(file_path: str, content: str, intent: str = None):
    """意図を明示的に指定してファイル書き込み"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 意図が指定されている場合は明示的に記録
    if intent:
        from universal_intent_system import UniversalIntentSystem
        system = UniversalIntentSystem()
        system.record_intent(
            os.path.basename(file_path),
            intent,
            "明示的に指定された意図",
            system._categorize_by_project_type(file_path, system.current_project["type"])
        )

def claude_edit_with_intent(file_path: str, old_content: str, new_content: str, intent: str = None):
    """意図を明示的に指定してファイル編集"""
    # ファイル読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 置換実行
    updated_content = content.replace(old_content, new_content)
    
    # ファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    # 意図記録
    if intent:
        from universal_intent_system import UniversalIntentSystem
        system = UniversalIntentSystem()
        system.record_intent(
            os.path.basename(file_path),
            intent,
            f"編集操作: {old_content[:50]}... → {new_content[:50]}...",
            system._categorize_by_project_type(file_path, system.current_project["type"])
        )
    else:
        auto_intent_record(file_path, 'edit', new_content[:500])

if __name__ == "__main__":
    # フックのテスト
    setup_auto_hooks()
    
    # テスト用ファイル作成
    test_content = """
def test_function():
    '''テスト用の関数'''
    return "Hello, Auto Intent System!"
"""
    
    # 自動記録のテスト
    claude_write_with_intent(
        "test_auto_intent.py", 
        test_content,
        "自動意図記録システムのテスト用関数"
    )
    
    print("📝 テストファイルを作成し、意図を自動記録しました")
    
    # 記録結果確認
    from universal_intent_system import why_this_file_universal
    print(why_this_file_universal("test_auto_intent.py"))