#!/usr/bin/env python3
"""
コーディネーター対応起動スクリプト
すべての自動実行システムを干渉なく管理

使用方法:
1. Claude Code起動時に実行:
   exec(open('coordinated_startup.py').read())

2. 手動実行:
   python3 coordinated_startup.py
"""

import os
import sys
import time

# パス設定
sys.path.insert(0, '/mnt/c/Desktop/Research')

def coordinated_claude_startup():
    """コーディネーター統合起動"""
    print("🤖 コーディネーター統合起動システム")
    print("=" * 60)
    
    try:
        # 1. コーディネーター初期化
        print("1️⃣ 自動システムコーディネーター初期化...")
        from auto_system_coordinator import get_coordinator, SystemPriority
        
        coordinator = get_coordinator()
        
        # 2. システム登録
        print("2️⃣ 自動実行システム登録...")
        
        # 復元システム（最高優先度）
        coordinator.register_system(
            system_id="auto_restore",
            script_path="claude_auto_restore.py",
            priority=SystemPriority.CRITICAL,
            max_execution_time=60,
            conflict_systems=["auto_save", "textlint_watcher"],
            resource_requirements={"cpu": 10, "memory": 50}
        )
        
        # 自動保存システム（高優先度）
        coordinator.register_system(
            system_id="auto_save",
            script_path="auto_organize_and_save.py", 
            priority=SystemPriority.HIGH,
            max_execution_time=300,
            conflict_systems=["auto_restore"],
            resource_requirements={"cpu": 20, "memory": 100}
        )
        
        # textlint自動実行（通常優先度）
        coordinator.register_system(
            system_id="textlint_runner",
            script_path="textlint_auto_runner.py",
            priority=SystemPriority.NORMAL,
            max_execution_time=120,
            resource_requirements={"cpu": 15, "memory": 80}
        )
        
        # textlint監視（通常優先度）
        coordinator.register_system(
            system_id="textlint_watcher",
            script_path="textlint_watcher.py",
            priority=SystemPriority.NORMAL,
            max_execution_time=86400,  # 24時間（常駐）
            conflict_systems=["auto_restore"],
            resource_requirements={"cpu": 5, "memory": 30}
        )
        
        # 開発ワークフロー（通常優先度）
        coordinator.register_system(
            system_id="dev_workflow",
            script_path="auto_dev_workflow.py",
            priority=SystemPriority.NORMAL,
            max_execution_time=600,
            resource_requirements={"cpu": 30, "memory": 150}
        )
        
        # 研究自動実行（低優先度）
        coordinator.register_system(
            system_id="research_trigger",
            script_path="auto_research_trigger.py",
            priority=SystemPriority.LOW,
            max_execution_time=1800,
            resource_requirements={"cpu": 40, "memory": 200}
        )
        
        print("✅ 6つのシステムを登録しました")
        
        # 3. 初期実行（復元のみ）
        print("3️⃣ 初期復元処理...")
        
        # 復元システムを最初に実行
        can_exec, reason = coordinator.can_execute("auto_restore")
        if can_exec:
            print("🔄 自動復元システム実行中...")
            success = coordinator.execute_system("auto_restore", ["startup"])
            if success:
                print("✅ 復元処理完了")
            else:
                print("⚠️ 復元処理で問題発生（継続）")
        else:
            print(f"⚠️ 復元実行不可: {reason}")
        
        # 4. コーディネーション開始
        print("4️⃣ 自動コーディネーション開始...")
        coordinator.start_coordination()
        print("✅ バックグラウンドでシステム管理開始")
        
        # 5. 状態表示
        print("\n" + "=" * 60)
        print("🎯 コーディネーター統合完了")
        print("\n📊 システム状態:")
        
        status_report = coordinator.get_status_report()
        # レポートの重要部分のみ表示
        lines = status_report.split('\n')
        for line in lines:
            if line.startswith('###') or line.startswith('- **状態**'):
                print(line)
        
        print("\n🔧 管理コマンド:")
        print("  python3 auto_system_coordinator.py status     # 詳細状態")
        print("  python3 auto_system_coordinator.py stop       # 停止")
        print("  python3 coordinated_startup.py check          # システムチェック")
        
        print("\n💡 各システムは優先度と干渉回避で自動実行されます")
        
        return True
        
    except Exception as e:
        print(f"❌ 統合起動でエラーが発生: {e}")
        print("個別のシステムを手動で確認してください")
        return False

def check_system_health():
    """システム健全性チェック"""
    print("🏥 システム健全性チェック")
    print("=" * 40)
    
    try:
        from auto_system_coordinator import get_coordinator
        coordinator = get_coordinator()
        
        # 状態レポート表示
        print(coordinator.get_status_report())
        
        # 実行可能システムチェック
        queue = coordinator.get_execution_queue()
        if queue:
            print(f"⚡ 実行可能システム: {len(queue)}個")
            for system_id in queue:
                print(f"  - {system_id}")
        else:
            print("⚪ 実行待機中のシステムなし")
        
        # リソース状況
        if coordinator._check_resources():
            print("✅ リソース状況: 正常")
        else:
            print("⚠️ リソース状況: 高負荷")
        
    except Exception as e:
        print(f"❌ ヘルスチェック失敗: {e}")

def emergency_stop():
    """緊急停止"""
    print("🚨 緊急停止実行")
    
    try:
        from auto_system_coordinator import get_coordinator
        coordinator = get_coordinator()
        coordinator.stop_coordination()
        print("✅ 全自動システムを停止しました")
    except Exception as e:
        print(f"❌ 停止失敗: {e}")

# 直接実行された場合
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "check":
            check_system_health()
        elif command == "stop":
            emergency_stop()
        elif command == "startup":
            coordinated_claude_startup()
        else:
            print(f"不明なコマンド: {command}")
            print("使用可能: startup, check, stop")
    else:
        coordinated_claude_startup()

# インポートされた場合の便利な関数
def quick_status():
    """クイック状態確認"""
    try:
        from auto_system_coordinator import get_coordinator
        coordinator = get_coordinator()
        
        print("🤖 コーディネーター状態:")
        print(f"実行中: {'✅' if coordinator.coordination_active else '❌'}")
        
        running_systems = [
            system_id for system_id, status in coordinator.system_status.items()
            if status.value == "running"
        ]
        
        if running_systems:
            print(f"実行中システム: {', '.join(running_systems)}")
        else:
            print("実行中システム: なし")
            
    except Exception as e:
        print(f"状態確認エラー: {e}")

def safe_execute(system_id: str):
    """安全なシステム実行"""
    try:
        from auto_system_coordinator import get_coordinator
        coordinator = get_coordinator()
        
        can_exec, reason = coordinator.can_execute(system_id)
        if can_exec:
            print(f"🚀 {system_id} 実行中...")
            success = coordinator.execute_system(system_id)
            if success:
                print(f"✅ {system_id} 完了")
            else:
                print(f"❌ {system_id} 失敗")
            return success
        else:
            print(f"⚠️ {system_id} 実行不可: {reason}")
            return False
    except Exception as e:
        print(f"実行エラー: {e}")
        return False