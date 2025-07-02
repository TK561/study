#!/usr/bin/env python3
"""
textlint自動実行システム
ファイル変更を監視し、自動的に文章チェックを実行
"""
import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
import threading
import argparse

class TextlintAutoRunner:
    def __init__(self):
        self.config_file = 'textlint_auto_config.json'
        self.log_file = 'textlint_auto_log.json'
        self.last_check_file = '.last_textlint_check'
        self.load_config()
        
    def load_config(self):
        """設定ファイルを読み込み"""
        default_config = {
            "auto_check_enabled": True,
            "check_on_save": True,
            "check_interval_minutes": 30,
            "auto_fix": False,
            "target_patterns": [
                "*.md",
                "sessions/*.md",
                "docs/*.md"
            ],
            "exclude_patterns": [
                "node_modules/**",
                ".git/**",
                "public/**"
            ],
            "notification": {
                "enabled": True,
                "threshold_errors": 5,
                "threshold_warnings": 10
            },
            "git_hook_enabled": True,
            "schedule_enabled": True,
            "schedule_times": ["09:00", "15:00", "21:00"]
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """設定ファイルを保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def log_event(self, event_type, details):
        """イベントをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # 直近100件のみ保持
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def run_textlint(self, fix=False, specific_files=None):
        """textlintを実行"""
        cmd = ['npx', 'textlint']
        
        if fix or self.config.get('auto_fix', False):
            cmd.append('--fix')
        
        if specific_files:
            cmd.extend(specific_files)
        else:
            # デフォルトのパターンを使用
            for pattern in self.config['target_patterns']:
                cmd.append(pattern)
        
        try:
            # textlintを実行
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # 結果を解析
            output = result.stdout + result.stderr
            errors = output.count('error')
            warnings = output.count('warning')
            
            # ログに記録
            self.log_event('textlint_check', {
                'files_checked': len(specific_files) if specific_files else 'all',
                'errors': errors,
                'warnings': warnings,
                'auto_fix': fix or self.config.get('auto_fix', False),
                'exit_code': result.returncode
            })
            
            # 最終チェック時刻を更新
            with open(self.last_check_file, 'w') as f:
                f.write(datetime.now().isoformat())
            
            return {
                'success': result.returncode == 0,
                'errors': errors,
                'warnings': warnings,
                'output': output
            }
            
        except Exception as e:
            self.log_event('textlint_error', {'error': str(e)})
            return {
                'success': False,
                'errors': 0,
                'warnings': 0,
                'output': f"Error: {str(e)}"
            }
    
    def get_modified_files(self, since_minutes=30):
        """指定時間内に変更されたファイルを取得"""
        modified_files = []
        current_time = time.time()
        threshold_time = current_time - (since_minutes * 60)
        
        for pattern in self.config['target_patterns']:
            for file_path in Path('.').glob(pattern):
                if file_path.stat().st_mtime > threshold_time:
                    # 除外パターンチェック
                    excluded = False
                    for exclude in self.config['exclude_patterns']:
                        if file_path.match(exclude):
                            excluded = True
                            break
                    
                    if not excluded:
                        modified_files.append(str(file_path))
        
        return modified_files
    
    def check_notification_threshold(self, result):
        """通知閾値をチェック"""
        if not self.config['notification']['enabled']:
            return False
        
        errors = result['errors']
        warnings = result['warnings']
        threshold_errors = self.config['notification']['threshold_errors']
        threshold_warnings = self.config['notification']['threshold_warnings']
        
        return errors >= threshold_errors or warnings >= threshold_warnings
    
    def send_notification(self, result):
        """通知を送信（実際の実装では適切な通知方法を使用）"""
        print(f"\n🔔 textlint通知:")
        print(f"  エラー: {result['errors']}件")
        print(f"  警告: {result['warnings']}件")
        
        if result['errors'] > 0:
            print("  ⚠️ エラーが検出されました。修正をお勧めします。")
    
    def auto_check_loop(self):
        """自動チェックループ"""
        print("🔍 textlint自動チェックを開始しました")
        print(f"  チェック間隔: {self.config['check_interval_minutes']}分")
        print(f"  自動修正: {'有効' if self.config.get('auto_fix', False) else '無効'}")
        print("  停止するには Ctrl+C を押してください\n")
        
        while True:
            try:
                # 変更されたファイルを取得
                modified_files = self.get_modified_files(self.config['check_interval_minutes'])
                
                if modified_files:
                    print(f"\n📝 {len(modified_files)}個のファイルが変更されました")
                    result = self.run_textlint(specific_files=modified_files)
                    
                    if self.check_notification_threshold(result):
                        self.send_notification(result)
                    
                    if result['success']:
                        print("✅ 問題は見つかりませんでした")
                    else:
                        print(f"❌ {result['errors']}個のエラー、{result['warnings']}個の警告")
                
                # 指定間隔待機
                time.sleep(self.config['check_interval_minutes'] * 60)
                
            except KeyboardInterrupt:
                print("\n⏹️ 自動チェックを停止しました")
                break
            except Exception as e:
                print(f"\n❌ エラー: {e}")
                time.sleep(60)  # エラー時は1分待機
    
    def setup_git_hook(self):
        """Git pre-commitフックをセットアップ"""
        hook_path = Path('.git/hooks/pre-commit')
        hook_content = """#!/bin/sh
# textlint pre-commit hook
echo "🔍 textlintでコミット前チェックを実行中..."

# textlintを実行
npx textlint --format compact $(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.md$')

if [ $? -ne 0 ]; then
    echo "❌ textlintエラーが検出されました。修正してから再度コミットしてください。"
    echo "💡 ヒント: npm run lint:fix で自動修正できます"
    exit 1
fi

echo "✅ textlintチェック完了"
"""
        
        # .git/hooksディレクトリが存在することを確認
        if hook_path.parent.exists():
            with open(hook_path, 'w') as f:
                f.write(hook_content)
            
            # 実行権限を付与
            os.chmod(hook_path, 0o755)
            
            print("✅ Git pre-commitフックを設定しました")
            self.log_event('git_hook_setup', {'status': 'success'})
        else:
            print("❌ .gitディレクトリが見つかりません")
            self.log_event('git_hook_setup', {'status': 'failed', 'reason': 'no_git_directory'})
    
    def check_now(self, fix=False):
        """今すぐチェックを実行"""
        print("🔍 textlintチェックを実行中...")
        result = self.run_textlint(fix=fix)
        
        if result['success']:
            print("✅ すべてのチェックが完了しました")
        else:
            print(f"❌ 問題が検出されました:")
            print(f"  エラー: {result['errors']}件")
            print(f"  警告: {result['warnings']}件")
            
            if not fix:
                print("\n💡 ヒント: --fix オプションで自動修正できます")
        
        return result
    
    def show_status(self):
        """現在の状態を表示"""
        print("📊 textlint自動実行システム状態:")
        print(f"  自動チェック: {'有効' if self.config['auto_check_enabled'] else '無効'}")
        print(f"  チェック間隔: {self.config['check_interval_minutes']}分")
        print(f"  自動修正: {'有効' if self.config.get('auto_fix', False) else '無効'}")
        print(f"  Gitフック: {'有効' if self.config['git_hook_enabled'] else '無効'}")
        
        # 最終チェック時刻
        if os.path.exists(self.last_check_file):
            with open(self.last_check_file, 'r') as f:
                last_check = f.read().strip()
            print(f"  最終チェック: {last_check}")
        
        # 最近のログ
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            print(f"\n📝 最近のイベント（直近5件）:")
            for log in logs[-5:]:
                timestamp = log['timestamp'][:19].replace('T', ' ')
                event_type = log['event_type']
                details = log['details']
                
                if event_type == 'textlint_check':
                    print(f"  {timestamp}: チェック実行 - エラー:{details.get('errors', 0)} 警告:{details.get('warnings', 0)}")
                else:
                    print(f"  {timestamp}: {event_type}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='textlint自動実行システム')
    parser.add_argument('command', nargs='?', default='status',
                      choices=['start', 'check', 'fix', 'setup', 'status'],
                      help='実行するコマンド')
    parser.add_argument('--interval', type=int, help='チェック間隔（分）')
    parser.add_argument('--auto-fix', action='store_true', help='自動修正を有効化')
    
    args = parser.parse_args()
    
    runner = TextlintAutoRunner()
    
    if args.interval:
        runner.config['check_interval_minutes'] = args.interval
        runner.save_config()
    
    if args.auto_fix:
        runner.config['auto_fix'] = True
        runner.save_config()
    
    if args.command == 'start':
        runner.auto_check_loop()
    elif args.command == 'check':
        runner.check_now(fix=False)
    elif args.command == 'fix':
        runner.check_now(fix=True)
    elif args.command == 'setup':
        runner.setup_git_hook()
    elif args.command == 'status':
        runner.show_status()

if __name__ == "__main__":
    main()