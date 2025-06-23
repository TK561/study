#!/usr/bin/env python3
"""
Vercel自動トリガーシステム
Vercel関連の操作を検出して自動実行
"""

import os
import time
import json
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Set
from pathlib import Path
import hashlib

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("📝 Note: ファイル監視機能を使用するには 'pip install watchdog' を実行してください")

class VercelAutoTrigger:
    """
    Vercel関連の変更を自動検出して統合システムを実行
    """
    
    def __init__(self):
        self.trigger_config_file = "VERCEL_AUTO_TRIGGER_CONFIG.json"
        self.last_trigger_file = "VERCEL_LAST_TRIGGER.json"
        self.config = self._load_config()
        self.last_trigger = self._load_last_trigger()
        
        # 監視対象ファイル
        self.watch_files = {
            "public/index.html",
            "index.html", 
            "vercel.json",
            "package.json",
            ".env"
        }
        
        # 監視対象ディレクトリ
        self.watch_dirs = {
            "public",
            "api",
            "pages"
        }
        
        # Vercel関連コマンド
        self.vercel_commands = {
            "vercel",
            "vercel deploy",
            "vercel --prod",
            "npm run build",
            "npm run dev",
            "python3 direct_vercel_deploy.py",
            "python3 vercel_unified_system.py"
        }
        
        # ファイルハッシュキャッシュ
        self.file_hashes = {}
        self._update_file_hashes()
        
        # 実行ロック
        self.execution_lock = threading.Lock()
        self.last_execution = None
        
    def _load_config(self) -> Dict:
        """設定を読み込む"""
        if os.path.exists(self.trigger_config_file):
            with open(self.trigger_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        default_config = {
            "enabled": True,
            "auto_deploy_on_file_change": True,
            "auto_deploy_on_command": True,
            "cooldown_seconds": 30,  # 連続実行防止
            "watch_patterns": [
                "*.html",
                "*.js", 
                "*.css",
                "*.json",
                "*.py"
            ],
            "ignore_patterns": [
                "node_modules/*",
                ".git/*",
                "*.log",
                "*.tmp"
            ],
            "trigger_actions": {
                "file_change": "smart_deploy",
                "command_detected": "smart_deploy",
                "error_detected": "auto_fix"
            }
        }
        
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict = None):
        """設定を保存"""
        if config:
            self.config = config
        with open(self.trigger_config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _load_last_trigger(self) -> Dict:
        """最後のトリガー情報を読み込む"""
        if os.path.exists(self.last_trigger_file):
            with open(self.last_trigger_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"last_execution": None, "trigger_count": 0}
    
    def _save_last_trigger(self):
        """最後のトリガー情報を保存"""
        with open(self.last_trigger_file, 'w', encoding='utf-8') as f:
            json.dump(self.last_trigger, f, ensure_ascii=False, indent=2)
    
    def _update_file_hashes(self):
        """監視ファイルのハッシュを更新"""
        for file_path in self.watch_files:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                    self.file_hashes[file_path] = hashlib.md5(content).hexdigest()
    
    def _check_file_changes(self) -> List[str]:
        """ファイル変更を検出"""
        changed_files = []
        
        for file_path in self.watch_files:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                    current_hash = hashlib.md5(content).hexdigest()
                    
                    if file_path not in self.file_hashes or self.file_hashes[file_path] != current_hash:
                        changed_files.append(file_path)
                        self.file_hashes[file_path] = current_hash
        
        return changed_files
    
    def _should_trigger(self, trigger_type: str) -> bool:
        """トリガー実行の可否を判定"""
        if not self.config.get("enabled", True):
            return False
        
        # クールダウン期間チェック
        if self.last_execution:
            cooldown = self.config.get("cooldown_seconds", 30)
            if (datetime.now() - self.last_execution).total_seconds() < cooldown:
                print(f"⏳ クールダウン中 ({cooldown}秒)")
                return False
        
        return True
    
    async def _execute_smart_deploy(self, trigger_reason: str):
        """スマートデプロイを実行"""
        with self.execution_lock:
            if not self._should_trigger("smart_deploy"):
                return
            
            print(f"\n🚀 自動トリガー実行: {trigger_reason}")
            print("=" * 60)
            
            try:
                # 統合システムを使用
                from vercel_unified_system import VercelUnifiedSystem
                system = VercelUnifiedSystem()
                
                # スマートデプロイ実行
                result = await system.smart_deploy_workflow()
                
                # 実行記録
                self.last_execution = datetime.now()
                self.last_trigger["last_execution"] = self.last_execution.isoformat()
                self.last_trigger["trigger_count"] += 1
                self.last_trigger["last_reason"] = trigger_reason
                self.last_trigger["last_result"] = result["success"]
                self._save_last_trigger()
                
                if result["success"]:
                    print("✅ 自動デプロイ成功")
                else:
                    print("❌ 自動デプロイ失敗")
                    # エラー時は自動修復を試行
                    await self._execute_auto_fix("deployment_failure")
                    
            except Exception as e:
                print(f"❌ 自動実行エラー: {e}")
    
    async def _execute_auto_fix(self, error_type: str):
        """自動修復を実行"""
        print(f"\n🔧 自動修復実行: {error_type}")
        
        try:
            from vercel_fix_assistant import VercelFixAssistant
            assistant = VercelFixAssistant()
            
            # 静的HTML変換で修復
            result = assistant.apply_fix("static_html")
            
            if result:
                print("✅ 自動修復成功")
                # 修復後に再デプロイ
                await self._execute_smart_deploy("auto_fix_retry")
            else:
                print("❌ 自動修復失敗")
                
        except Exception as e:
            print(f"❌ 自動修復エラー: {e}")
    
    def start_file_monitoring(self):
        """ファイル監視を開始"""
        if not WATCHDOG_AVAILABLE:
            print("📝 ファイル監視機能が利用できません")
            return self._start_polling_monitor()
        
        print("👁️ Vercelファイル監視を開始...")
        
        class VercelFileHandler(FileSystemEventHandler):
            def __init__(self, trigger_system):
                self.trigger_system = trigger_system
                
            def on_modified(self, event):
                if event.is_directory:
                    return
                
                file_path = event.src_path
                file_name = os.path.basename(file_path)
                
                # Vercel関連ファイルの変更を検出
                if any(pattern in file_path for pattern in 
                      ["public/", "vercel.json", "index.html", "package.json"]):
                    print(f"📝 変更検出: {file_path}")
                    
                    # 自動デプロイ実行
                    import asyncio
                    asyncio.create_task(
                        self.trigger_system._execute_smart_deploy(f"ファイル変更: {file_name}")
                    )
        
        # 監視開始
        event_handler = VercelFileHandler(self)
        observer = Observer()
        observer.schedule(event_handler, ".", recursive=True)
        observer.start()
        
        return observer
    
    def _start_polling_monitor(self):
        """ポーリング方式でファイル監視"""
        print("📊 ポーリング方式でファイル監視を開始...")
        
        def polling_check():
            while True:
                try:
                    changed_files = self._check_file_changes()
                    if changed_files:
                        print(f"📝 変更検出: {', '.join(changed_files)}")
                        import asyncio
                        asyncio.create_task(
                            self._execute_smart_deploy(f"ファイル変更: {', '.join(changed_files)}")
                        )
                    
                    time.sleep(5)  # 5秒間隔でチェック
                    
                except Exception as e:
                    print(f"⚠️ 監視エラー: {e}")
                    time.sleep(10)
        
        # バックグラウンドで実行
        monitor_thread = threading.Thread(target=polling_check, daemon=True)
        monitor_thread.start()
        return monitor_thread
    
    def start_command_monitoring(self):
        """コマンド監視を開始（プロセス監視）"""
        print("🖥️ Vercelコマンド監視を開始...")
        
        def monitor_commands():
            import psutil
            
            while True:
                try:
                    # 現在実行中のプロセスをチェック
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            cmdline = ' '.join(proc.info['cmdline'] or [])
                            
                            # Vercel関連コマンドを検出
                            for vercel_cmd in self.vercel_commands:
                                if vercel_cmd in cmdline and proc.info['name'] not in ['python3', 'python']:
                                    print(f"🖥️ Vercelコマンド検出: {cmdline}")
                                    
                                    # 自動実行
                                    import asyncio
                                    asyncio.create_task(
                                        self._execute_smart_deploy(f"コマンド実行: {vercel_cmd}")
                                    )
                                    
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    time.sleep(10)  # 10秒間隔でチェック
                    
                except Exception as e:
                    print(f"⚠️ コマンド監視エラー: {e}")
                    time.sleep(30)
        
        # バックグラウンドで実行
        try:
            import psutil
            command_thread = threading.Thread(target=monitor_commands, daemon=True)
            command_thread.start()
            return command_thread
        except ImportError:
            print("📝 Note: コマンド監視機能を使用するには 'pip install psutil' を実行してください")
            return None
    
    def setup_git_hooks(self):
        """Git フックを設定してpush時に自動実行"""
        git_hooks_dir = ".git/hooks"
        
        if not os.path.exists(git_hooks_dir):
            print("📝 Gitリポジトリが見つかりません")
            return
        
        # pre-push フック
        pre_push_hook = os.path.join(git_hooks_dir, "pre-push")
        hook_content = """#!/bin/bash
# Vercel自動トリガー - Git push時

echo "🚀 Git push検出 - Vercel自動デプロイを実行中..."
python3 vercel_auto_trigger.py --trigger git_push
"""
        
        with open(pre_push_hook, 'w') as f:
            f.write(hook_content)
        
        # 実行権限を付与
        os.chmod(pre_push_hook, 0o755)
        print("✅ Git pre-pushフックを設定しました")
    
    def start_comprehensive_monitoring(self):
        """包括的な監視を開始"""
        print("🎯 Vercel包括的自動監視システムを開始")
        print("=" * 60)
        
        # 各種監視を開始
        file_observer = self.start_file_monitoring()
        command_monitor = self.start_command_monitoring()
        
        # Git フック設定
        self.setup_git_hooks()
        
        # 状態表示
        print("\n📊 監視システム状態:")
        print(f"  - ファイル監視: {'✅ 有効' if file_observer else '❌ 無効'}")
        print(f"  - コマンド監視: {'✅ 有効' if command_monitor else '❌ 無効'}")
        print(f"  - Git フック: ✅ 設定済み")
        print(f"  - 自動実行: {'✅ 有効' if self.config['enabled'] else '❌ 無効'}")
        
        # 設定情報
        print(f"\n⚙️ 設定:")
        print(f"  - クールダウン: {self.config['cooldown_seconds']}秒")
        print(f"  - 監視ファイル: {len(self.watch_files)}個")
        print(f"  - 最終実行: {self.last_trigger.get('last_execution', 'なし')}")
        
        print("\n🔄 監視中... (Ctrl+C で停止)")
        
        try:
            # メインループ
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 監視システムを停止します")
            if hasattr(file_observer, 'stop'):
                file_observer.stop()
                file_observer.join()
    
    def status(self):
        """現在のステータスを表示"""
        print("📊 Vercel自動トリガーシステム状態")
        print("=" * 50)
        
        # 基本情報
        print(f"状態: {'✅ 有効' if self.config['enabled'] else '❌ 無効'}")
        print(f"最終実行: {self.last_trigger.get('last_execution', 'なし')}")
        print(f"実行回数: {self.last_trigger.get('trigger_count', 0)}回")
        print(f"最終結果: {self.last_trigger.get('last_result', 'なし')}")
        
        # 監視対象
        print(f"\n監視ファイル: {len(self.watch_files)}個")
        for file in self.watch_files:
            exists = "✅" if os.path.exists(file) else "❌"
            print(f"  {exists} {file}")
        
        # 設定
        print(f"\n設定:")
        print(f"  - ファイル変更監視: {'✅' if self.config['auto_deploy_on_file_change'] else '❌'}")
        print(f"  - コマンド監視: {'✅' if self.config['auto_deploy_on_command'] else '❌'}")
        print(f"  - クールダウン: {self.config['cooldown_seconds']}秒")

async def trigger_smart_deploy(reason: str):
    """外部から呼び出し可能なトリガー関数"""
    trigger = VercelAutoTrigger()
    await trigger._execute_smart_deploy(reason)

def main():
    import sys
    import asyncio
    
    trigger = VercelAutoTrigger()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            # 監視開始
            trigger.start_comprehensive_monitoring()
            
        elif command == "status":
            # ステータス表示
            trigger.status()
            
        elif command == "--trigger":
            # 手動トリガー
            reason = sys.argv[2] if len(sys.argv) > 2 else "manual_trigger"
            asyncio.run(trigger_smart_deploy(reason))
            
        elif command == "setup":
            # 初期設定
            trigger.setup_git_hooks()
            print("✅ 自動トリガーシステムのセットアップが完了しました")
            
        elif command == "enable":
            # 有効化
            trigger.config["enabled"] = True
            trigger._save_config()
            print("✅ 自動トリガーを有効にしました")
            
        elif command == "disable":
            # 無効化
            trigger.config["enabled"] = False
            trigger._save_config()
            print("❌ 自動トリガーを無効にしました")
            
        else:
            print(f"不明なコマンド: {command}")
            print("使用方法:")
            print("  python3 vercel_auto_trigger.py start    # 監視開始")
            print("  python3 vercel_auto_trigger.py status   # 状態確認")
            print("  python3 vercel_auto_trigger.py setup    # 初期設定")
            print("  python3 vercel_auto_trigger.py enable   # 有効化")
            print("  python3 vercel_auto_trigger.py disable  # 無効化")
    else:
        # デフォルトは状態表示
        trigger.status()

if __name__ == "__main__":
    main()