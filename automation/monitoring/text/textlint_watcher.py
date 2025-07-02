#!/usr/bin/env python3
"""
textlintファイル監視システム
ファイルの変更をリアルタイムで検出し、即座にtextlintを実行
"""
import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

class TextlintWatcher:
    def __init__(self):
        self.watched_files = {}
        self.config_file = 'textlint_watcher_config.json'
        self.load_config()
        
    def load_config(self):
        """設定を読み込み"""
        default_config = {
            "watch_patterns": [
                "*.md",
                "sessions/*.md",
                "docs/*.md",
                "*.txt"
            ],
            "ignore_patterns": [
                "*_backup*",
                "*.tmp",
                "node_modules/**",
                ".git/**"
            ],
            "debounce_seconds": 2,
            "auto_fix_on_save": False,
            "show_inline_hints": True
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_file_hash(self, filepath):
        """ファイルのハッシュ値を取得"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def is_ignored(self, filepath):
        """ファイルが無視パターンに一致するかチェック"""
        path = Path(filepath)
        for pattern in self.config['ignore_patterns']:
            if path.match(pattern):
                return True
        return False
    
    def scan_files(self):
        """監視対象ファイルをスキャン"""
        files = {}
        for pattern in self.config['watch_patterns']:
            for filepath in Path('.').glob(pattern):
                if not self.is_ignored(filepath):
                    file_hash = self.get_file_hash(filepath)
                    if file_hash:
                        files[str(filepath)] = {
                            'hash': file_hash,
                            'mtime': filepath.stat().st_mtime
                        }
        return files
    
    def check_file(self, filepath, fix=False):
        """特定のファイルをチェック"""
        cmd = ['npx', 'textlint']
        if fix or self.config.get('auto_fix_on_save', False):
            cmd.append('--fix')
        cmd.append(filepath)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout + result.stderr,
            'fixed': fix or self.config.get('auto_fix_on_save', False)
        }
    
    def format_output(self, filepath, result):
        """出力を整形"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if result['success']:
            status = "✅ OK"
            color = '\033[32m'  # 緑
        else:
            status = "❌ 問題あり"
            color = '\033[31m'  # 赤
        
        reset_color = '\033[0m'
        
        print(f"\n[{timestamp}] {color}{status}{reset_color} - {filepath}")
        
        if not result['success'] and self.config.get('show_inline_hints', True):
            # エラーメッセージから主要な部分を抽出
            lines = result['output'].split('\n')
            for line in lines:
                if 'error' in line.lower() or 'warning' in line.lower():
                    print(f"  → {line.strip()}")
        
        if result['fixed']:
            print(f"  🔧 自動修正を適用しました")
    
    def watch(self):
        """ファイル監視を開始"""
        print("👁️ textlintファイル監視を開始しました")
        print(f"監視対象: {', '.join(self.config['watch_patterns'])}")
        print(f"自動修正: {'有効' if self.config.get('auto_fix_on_save', False) else '無効'}")
        print("停止するには Ctrl+C を押してください\n")
        
        # 初期スキャン
        self.watched_files = self.scan_files()
        print(f"📁 {len(self.watched_files)}個のファイルを監視中...")
        
        last_check_time = {}
        
        try:
            while True:
                current_files = self.scan_files()
                current_time = time.time()
                
                # 新規・変更ファイルをチェック
                for filepath, info in current_files.items():
                    if filepath not in self.watched_files:
                        # 新規ファイル
                        print(f"\n🆕 新規ファイル検出: {filepath}")
                        self.watched_files[filepath] = info
                        result = self.check_file(filepath)
                        self.format_output(filepath, result)
                        last_check_time[filepath] = current_time
                        
                    elif info['hash'] != self.watched_files[filepath]['hash']:
                        # 変更されたファイル（デバウンス適用）
                        if filepath not in last_check_time or \
                           current_time - last_check_time[filepath] >= self.config['debounce_seconds']:
                            
                            print(f"\n📝 変更検出: {filepath}")
                            self.watched_files[filepath] = info
                            result = self.check_file(filepath)
                            self.format_output(filepath, result)
                            last_check_time[filepath] = current_time
                
                # 削除されたファイルを処理
                deleted_files = set(self.watched_files.keys()) - set(current_files.keys())
                for filepath in deleted_files:
                    print(f"\n🗑️ ファイル削除: {filepath}")
                    del self.watched_files[filepath]
                    if filepath in last_check_time:
                        del last_check_time[filepath]
                
                time.sleep(0.5)  # 0.5秒ごとにチェック
                
        except KeyboardInterrupt:
            print("\n\n⏹️ ファイル監視を停止しました")
            print(f"監視したファイル数: {len(self.watched_files)}")

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='textlintファイル監視システム')
    parser.add_argument('--auto-fix', action='store_true', 
                      help='ファイル保存時に自動修正を適用')
    parser.add_argument('--config', action='store_true',
                      help='設定ファイルを編集')
    
    args = parser.parse_args()
    
    watcher = TextlintWatcher()
    
    if args.config:
        print(f"設定ファイル: {watcher.config_file}")
        print("エディタで設定を編集してください")
        return
    
    if args.auto_fix:
        watcher.config['auto_fix_on_save'] = True
        with open(watcher.config_file, 'w', encoding='utf-8') as f:
            json.dump(watcher.config, f, ensure_ascii=False, indent=2)
        print("✅ 自動修正を有効にしました")
    
    watcher.watch()

if __name__ == "__main__":
    main()