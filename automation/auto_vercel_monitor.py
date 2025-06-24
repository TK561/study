#!/usr/bin/env python3
"""
自動Vercelモニターシステム - ファイル変更を検知して自動デプロイ
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️ watchdogが利用できません。ポーリングモードで動作します。")

class AutoVercelHandler:
    if WATCHDOG_AVAILABLE:
        # watchdogが利用可能な場合のみ継承
        __bases__ = (FileSystemEventHandler,)
    """ファイル変更監視ハンドラー"""
    
    def __init__(self):
        self.last_deploy = 0
        self.deploy_cooldown = 30  # 30秒のクールダウン
        self.watched_extensions = {'.html', '.css', '.js', '.json', '.md', '.py'}
        self.ignore_paths = {'.git', '__pycache__', '.vscode', 'node_modules'}
        
    def should_trigger_deploy(self, file_path: str) -> bool:
        """デプロイをトリガーするかチェック"""
        path = Path(file_path)
        
        # 無視するパスをチェック
        for ignore in self.ignore_paths:
            if ignore in str(path):
                return False
        
        # 拡張子をチェック
        if path.suffix.lower() in self.watched_extensions:
            return True
            
        # 特定のファイル名をチェック
        if path.name in ['vercel.json', 'index.html']:
            return True
            
        return False
    
    def on_modified(self, event):
        """ファイル変更時の処理"""
        if event.is_directory:
            return
            
        if not self.should_trigger_deploy(event.src_path):
            return
            
        # クールダウンチェック
        current_time = time.time()
        if current_time - self.last_deploy < self.deploy_cooldown:
            print(f"⏳ クールダウン中... 残り{int(self.deploy_cooldown - (current_time - self.last_deploy))}秒")
            return
            
        print(f"📝 ファイル変更検知: {event.src_path}")
        self.trigger_auto_deploy(event.src_path)
        self.last_deploy = current_time
    
    def trigger_auto_deploy(self, changed_file: str):
        """自動デプロイを実行"""
        print("🚀 自動デプロイを開始...")
        
        try:
            # 最もシンプルなデプロイを実行
            result = subprocess.run([
                sys.executable, "vdeploy.py"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ 自動デプロイ成功!")
                print(result.stdout)
                self.log_auto_deploy(changed_file, "success", result.stdout)
            else:
                print("❌ 自動デプロイ失敗")
                print(result.stderr)
                self.log_auto_deploy(changed_file, "failed", result.stderr)
                
        except subprocess.TimeoutExpired:
            print("⏰ デプロイタイムアウト")
            self.log_auto_deploy(changed_file, "timeout", "Deploy timeout")
        except Exception as e:
            print(f"❌ デプロイエラー: {e}")
            self.log_auto_deploy(changed_file, "error", str(e))
    
    def log_auto_deploy(self, changed_file: str, status: str, message: str):
        """自動デプロイログを記録"""
        log_file = Path("AUTO_DEPLOY_LOG.json")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "changed_file": changed_file,
            "status": status,
            "message": message
        }
        
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                pass
        
        logs.append(log_entry)
        logs = logs[-100:]  # 最新100件のみ保持
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

class AutoVercelMonitor:
    """自動Vercelモニターメインクラス"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.observer = None
        self.handler = AutoVercelHandler()
        
    def start_monitoring(self):
        """監視を開始"""
        print("🎯 自動Vercelモニター開始")
        print(f"📁 監視ディレクトリ: {self.project_root}")
        print("📝 監視対象: .html, .css, .js, .json, .md, .py ファイル")
        print("⏱️ クールダウン: 30秒")
        print("🔄 変更検知時に自動デプロイを実行します")
        print("-" * 50)
        
        if WATCHDOG_AVAILABLE:
            # watchdog使用
            self.observer = Observer()
            self.observer.schedule(
                self.handler,
                str(self.project_root),
                recursive=True
            )
            
            self.observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 監視を停止します...")
                self.observer.stop()
            
            self.observer.join()
        else:
            # ポーリングモード
            print("📊 ポーリングモードで監視中...")
            self.start_polling_mode()
        
        print("✅ 監視停止完了")
    
    def start_polling_mode(self):
        """ポーリングモードでファイル監視"""
        file_times = {}
        
        try:
            while True:
                # 監視対象ファイルをチェック
                for ext in self.handler.watched_extensions:
                    for file_path in self.project_root.rglob(f"*{ext}"):
                        if not self.handler.should_trigger_deploy(str(file_path)):
                            continue
                        
                        try:
                            mtime = file_path.stat().st_mtime
                            last_mtime = file_times.get(str(file_path), 0)
                            
                            if mtime > last_mtime:
                                file_times[str(file_path)] = mtime
                                if last_mtime > 0:  # 初回は除外
                                    print(f"📝 ファイル変更検知: {file_path}")
                                    self.handler.trigger_auto_deploy(str(file_path))
                        except:
                            continue
                
                time.sleep(5)  # 5秒毎にチェック
                
        except KeyboardInterrupt:
            print("\n👋 ポーリング監視を停止します...")

def main():
    """メイン関数"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            monitor = AutoVercelMonitor()
            monitor.start_monitoring()
        elif command == "log":
            # ログ表示
            log_file = Path("AUTO_DEPLOY_LOG.json")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    for log in logs[-10:]:  # 最新10件
                        print(f"📅 {log['timestamp']}: {log['status']} - {log['changed_file']}")
            else:
                print("📝 ログファイルが見つかりません")
        elif command == "test":
            # テストデプロイ
            handler = AutoVercelHandler()
            handler.trigger_auto_deploy("test_file.html")
        else:
            print("使用方法:")
            print("  python3 auto_vercel_monitor.py start  - 監視開始")
            print("  python3 auto_vercel_monitor.py log    - ログ表示")
            print("  python3 auto_vercel_monitor.py test   - テスト実行")
    else:
        # デフォルトは監視開始
        monitor = AutoVercelMonitor()
        monitor.start_monitoring()

if __name__ == "__main__":
    main()