#!/usr/bin/env python3
"""
Claude Code起動時統合スクリプト
自動復元とセッション管理を統合

使用方法:
1. Claude Code起動時に実行:
   exec(open('claude_startup_integration.py').read())

2. 手動実行:
   python3 claude_startup_integration.py
"""

import os
import sys

# 現在のディレクトリをパスに追加
sys.path.insert(0, '/mnt/c/Desktop/Research')

def claude_code_startup():
    """Claude Code起動時の統合処理"""
    print("🚀 Claude Code起動時統合処理開始")
    print("=" * 50)
    
    try:
        # 1. 自動復元システム起動
        print("1️⃣ 自動復元システムチェック...")
        from claude_auto_restore import claude_startup
        claude_startup()
        
        # 2. セッション自動保存システムチェック
        print("\n2️⃣ セッション自動保存システムチェック...")
        if os.path.exists('/mnt/c/Desktop/Research/auto_organize_and_save.py'):
            print("✅ 自動保存システム利用可能")
        else:
            print("⚠️ 自動保存システムが見つかりません")
        
        # 3. 開発環境チェック
        print("\n3️⃣ 開発環境チェック...")
        
        # package.json確認
        if os.path.exists('/mnt/c/Desktop/Research/package.json'):
            print("✅ Node.js環境設定済み")
        else:
            print("⚠️ Node.js環境未設定")
        
        # VS Code設定確認
        vscode_dir = '/mnt/c/Desktop/Research/.vscode'
        if os.path.exists(vscode_dir):
            print("✅ VS Code設定済み")
        else:
            print("⚠️ VS Code設定未完了")
        
        # 4. 研究環境チェック
        print("\n4️⃣ 研究環境チェック...")
        notebooks = [
            'Research_Colab_Simple.ipynb',
            'Auto_Research_Colab.ipynb'
        ]
        
        for notebook in notebooks:
            if os.path.exists(f'/mnt/c/Desktop/Research/{notebook}'):
                print(f"✅ {notebook} 利用可能")
            else:
                print(f"⚠️ {notebook} が見つかりません")
        
        # 5. 推奨次ステップ表示
        print("\n" + "=" * 50)
        print("🎯 推奨次ステップ:")
        print("1. 前回の続きを確認:")
        print("   📄 sessions/AUTO_SESSION_SAVE_2025-07-02.md")
        print("   📄 SESSION_COMPLETION_SUMMARY.md")
        print("")
        print("2. 開発サーバー起動:")
        print("   npm run dev")
        print("")
        print("3. 研究ノートブック起動:")
        print("   jupyter lab Research_Colab_Simple.ipynb")
        print("")
        print("4. システム状態確認:")
        print("   ./research-commands.sh status")
        print("")
        print("5. ファイル整理・保存:")
        print("   python3 auto_organize_and_save.py")
        
        return True
        
    except Exception as e:
        print(f"❌ 起動処理でエラーが発生しました: {e}")
        print("手動でシステムを確認してください")
        return False

# 直接実行された場合
if __name__ == "__main__":
    claude_code_startup()

# インポートされた場合の便利な関数
def quick_status():
    """クイック状態確認"""
    print("📊 Claude Code環境状態:")
    
    # 復元システム状態
    try:
        from claude_auto_restore import get_restore_system
        system = get_restore_system()
        print(f"復元システム: {'✅ 有効' if system.config['enabled'] else '❌ 無効'}")
    except Exception:
        print("復元システム: ❌ エラー")
    
    # セッションファイル
    session_file = '/mnt/c/Desktop/Research/sessions/AUTO_SESSION_SAVE_2025-07-02.md'
    if os.path.exists(session_file):
        print("✅ 最新セッション記録あり")
    else:
        print("⚠️ セッション記録なし")
    
    # 重要ファイル
    important_files = [
        'CLAUDE.md',
        'package.json',
        'Research_Colab_Simple.ipynb'
    ]
    
    for file in important_files:
        if os.path.exists(f'/mnt/c/Desktop/Research/{file}'):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")

def enable_auto_restore():
    """自動復元を有効化"""
    try:
        from claude_auto_restore import get_restore_system
        system = get_restore_system()
        system.enable()
    except Exception as e:
        print(f"自動復元有効化エラー: {e}")

def quick_restore():
    """クイック復元"""
    try:
        from claude_auto_restore import get_restore_system
        system = get_restore_system()
        options = system.get_recovery_options()
        if options:
            print("最新セッションを復元しています...")
            system.restore_session(options[0]["data"])
        else:
            print("復元可能なセッションがありません")
    except Exception as e:
        print(f"復元エラー: {e}")