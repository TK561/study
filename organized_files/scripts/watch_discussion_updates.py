#!/usr/bin/env python3
"""
ディスカッション記録変更監視システム
- discussion-site/index.htmlの変更を監視
- 新しいディスカッション記録追加を検出
- 自動的に次回セッション内容を更新
"""

import time
import os
import hashlib
from pathlib import Path
from discussion_auto_updater import DiscussionAutoUpdater

class DiscussionWatcher:
    def __init__(self):
        self.base_dir = Path("/mnt/c/Desktop/Research")
        self.discussion_file = self.base_dir / "public/discussion-site/index.html"
        self.updater = DiscussionAutoUpdater()
        self.last_hash = None
        
    def get_file_hash(self):
        """ファイルのハッシュ値を取得"""
        if not self.discussion_file.exists():
            return None
            
        with open(self.discussion_file, 'rb') as f:
            content = f.read()
            return hashlib.md5(content).hexdigest()
    
    def detect_changes(self):
        """ファイル変更を検出"""
        current_hash = self.get_file_hash()
        
        if self.last_hash is None:
            self.last_hash = current_hash
            print(f"📂 監視開始: {self.discussion_file}")
            return False
            
        if current_hash != self.last_hash:
            print("🔄 ディスカッションファイルの変更を検出")
            self.last_hash = current_hash
            return True
            
        return False
    
    def start_monitoring(self, check_interval=30):
        """監視開始"""
        print("👁️ ディスカッション記録監視システム開始")
        print(f"📁 監視ファイル: {self.discussion_file}")
        print(f"⏱️ チェック間隔: {check_interval}秒")
        print("🛑 停止するにはCtrl+Cを押してください\\n")
        
        try:
            while True:
                if self.detect_changes():
                    print("🔔 変更検出 - 自動更新実行中...")
                    
                    # 少し待ってから処理（ファイル書き込み完了を待つ）
                    time.sleep(2)
                    
                    # 自動更新実行
                    success = self.updater.run_auto_update()
                    
                    if success:
                        print("✅ 次回ディスカッション自動生成完了")
                        
                        # Vercelデプロイも実行
                        print("🚀 Vercelデプロイ実行中...")
                        try:
                            os.chdir(self.base_dir)
                            import subprocess
                            result = subprocess.run(["npx", "vercel", "--prod"], 
                                                  capture_output=True, text=True)
                            if result.returncode == 0:
                                print("✅ Vercelデプロイ完了")
                            else:
                                print(f"❌ Vercelデプロイ失敗: {result.stderr}")
                        except Exception as e:
                            print(f"❌ Vercelデプロイエラー: {e}")
                    else:
                        print("⚠️ 自動更新をスキップしました")
                    
                    print("\\n👁️ 監視を継続中...\\n")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\\n🛑 監視システムを停止しました")

def main():
    """メイン実行"""
    import sys
    
    watcher = DiscussionWatcher()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            watcher.start_monitoring(interval)
            
        elif command == "check":
            if watcher.detect_changes():
                print("🔄 変更が検出されました")
            else:
                print("📋 変更はありません")
                
        elif command == "hash":
            hash_value = watcher.get_file_hash()
            print(f"📁 現在のファイルハッシュ: {hash_value}")
            
        else:
            print("❌ 不明なコマンド:", command)
            print("使用可能コマンド:")
            print("  start [間隔] - 監視開始（デフォルト30秒間隔）")
            print("  check - 一回だけ変更チェック")
            print("  hash - 現在のファイルハッシュ表示")
    else:
        # デフォルトは監視開始
        watcher.start_monitoring()

if __name__ == "__main__":
    main()