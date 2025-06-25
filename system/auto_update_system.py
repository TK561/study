#!/usr/bin/env python3
"""
研究ディスカッション記録 自動更新システム
記録タブ更新時に次回・目標タブを自動的に同期更新

機能:
1. WEEKLY_DISCUSSION_SUMMARY.md の変更監視
2. 最新回数に基づく次回タブの自動更新
3. 目標タブのスケジュール自動調整
4. index.html の自動書き換え
"""

import os
import re
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class DiscussionAutoUpdater:
    def __init__(self):
        self.research_root = Path(__file__).parent
        self.summary_file = self.research_root / "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        self.index_file = self.research_root / "public/discussion-site/index.html"
        self.config_file = self.research_root / ".auto_update_config.json"
        self.last_hash = None
        
        # 設定読み込み
        self.load_config()
        
    def load_config(self):
        """設定ファイルの読み込み"""
        default_config = {
            "last_hash": "",
            "last_session_number": 12,
            "next_session_date": "2025-06-26",
            "monitoring_enabled": True,
            "auto_deploy": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = {**default_config, **json.load(f)}
            except:
                self.config = default_config
        else:
            self.config = default_config
            
        self.save_config()
    
    def save_config(self):
        """設定ファイルの保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_file_hash(self, filepath):
        """ファイルのハッシュ値を取得"""
        if not filepath.exists():
            return ""
        
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def parse_summary_file(self):
        """WEEKLY_DISCUSSION_SUMMARY.md を解析して最新情報を取得"""
        if not self.summary_file.exists():
            return None
            
        with open(self.summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 最新の回数を取得
        session_pattern = r'### 第(\d+)回'
        sessions = re.findall(session_pattern, content)
        
        if not sessions:
            return None
            
        latest_session = max([int(s) for s in sessions])
        
        # 最新セッションの詳細を取得
        latest_pattern = f'### 第{latest_session}回.*?(?=### 第|---|\Z)'
        latest_match = re.search(latest_pattern, content, re.DOTALL)
        
        if not latest_match:
            return None
            
        latest_content = latest_match.group(0)
        
        # 日付パターンを探す
        date_pattern = r'\((\d{4}/\d{1,2}/\d{1,2})\)'
        date_match = re.search(date_pattern, latest_content)
        latest_date = date_match.group(1) if date_match else None
        
        return {
            'session_number': latest_session,
            'date': latest_date,
            'content': latest_content
        }
    
    def calculate_next_session(self, latest_session_info):
        """次回セッション情報を計算"""
        if not latest_session_info or not latest_session_info['date']:
            # デフォルト値
            return {
                'number': self.config['last_session_number'] + 1,
                'date': self.config['next_session_date']
            }
        
        # 次回の回数
        next_number = latest_session_info['session_number'] + 1
        
        # 次回の日付（毎週木曜日想定）
        try:
            latest_date_str = latest_session_info['date']
            latest_date = datetime.strptime(latest_date_str, '%Y/%m/%d')
            next_date = latest_date + timedelta(days=7)  # 1週間後
            next_date_str = next_date.strftime('%Y年%m月%d日')
        except:
            # 日付解析に失敗した場合のフォールバック
            next_date_str = "未定"
        
        return {
            'number': next_number,
            'date': next_date_str
        }
    
    def update_next_tab(self, next_session_info):
        """次回タブの内容を更新"""
        if not self.index_file.exists():
            return False
            
        with open(self.index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 次回タブのタイトルを更新
        old_title_pattern = r'<h2>📅 第\d+回ディスカッション: [^<]+</h2>'
        new_title = f'<h2>📅 第{next_session_info["number"]}回ディスカッション: {next_session_info["date"]}（木）</h2>'
        
        content = re.sub(old_title_pattern, new_title, content)
        
        # サブタイトルも更新（もしあれば）
        subtitle_pattern = r'(第\d+回ディスカッション: )([^<]+)'
        def replace_subtitle(match):
            return f'第{next_session_info["number"]}回ディスカッション: {next_session_info["date"]}'
        
        content = re.sub(subtitle_pattern, replace_subtitle, content)
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    
    def update_goals_tab_schedule(self, next_session_info):
        """目標タブのスケジュールを更新"""
        if not self.index_file.exists():
            return False
            
        with open(self.index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 現在の日付に基づいてスケジュールを調整
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # 中間発表の日付を調整（8月下旬 = 8月第4週）
        if current_month <= 6:
            # まだ6月以前なら、今年の8月
            interim_date = f"{current_year}年8月下旬"
        else:
            # 7月以降なら来年の8月
            interim_date = f"{current_year + 1}年8月下旬"
        
        # 卒業発表の日付を調整（2月下旬）
        if current_month <= 10:
            # 10月以前なら翌年の2月
            graduation_date = f"{current_year + 1}年2月下旬"
        else:
            # 11月以降なら翌々年の2月
            graduation_date = f"{current_year + 2}年2月下旬"
        
        # 目標タブ内の日付を更新
        content = re.sub(
            r'中間発表（\d{4}年8月下旬）',
            f'中間発表（{interim_date}）',
            content
        )
        
        content = re.sub(
            r'卒業発表（\d{4}年2月下旬）',
            f'卒業発表（{graduation_date}）',
            content
        )
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    
    def auto_deploy(self):
        """自動デプロイ実行"""
        if not self.config.get('auto_deploy', False):
            return False
            
        try:
            # Git コミット
            os.system('cd /mnt/c/Desktop/Research && git add .')
            commit_message = f"🤖 自動更新: 第{self.config['last_session_number']}回記録反映に基づく次回・目標タブ同期更新"
            os.system(f'cd /mnt/c/Desktop/Research && git commit -m "{commit_message}"')
            
            # プッシュ
            os.system('cd /mnt/c/Desktop/Research && git push origin main')
            
            return True
        except:
            return False
    
    def check_and_update(self):
        """記録ファイルをチェックして必要に応じて更新"""
        current_hash = self.get_file_hash(self.summary_file)
        
        # ハッシュが変わっていない場合は何もしない
        if current_hash == self.config.get('last_hash'):
            return False
        
        print(f"📋 記録ファイルの変更を検出: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 最新のセッション情報を解析
        latest_session_info = self.parse_summary_file()
        if not latest_session_info:
            print("❌ セッション情報の解析に失敗")
            return False
        
        print(f"📊 最新セッション: 第{latest_session_info['session_number']}回")
        
        # 次回セッション情報を計算
        next_session_info = self.calculate_next_session(latest_session_info)
        print(f"📅 次回セッション: 第{next_session_info['number']}回 ({next_session_info['date']})")
        
        # 次回タブを更新
        if self.update_next_tab(next_session_info):
            print("✅ 次回タブを更新しました")
        else:
            print("❌ 次回タブの更新に失敗")
        
        # 目標タブのスケジュールを更新
        if self.update_goals_tab_schedule(next_session_info):
            print("✅ 目標タブのスケジュールを更新しました")
        else:
            print("❌ 目標タブの更新に失敗")
        
        # 設定を更新
        self.config['last_hash'] = current_hash
        self.config['last_session_number'] = latest_session_info['session_number']
        self.config['next_session_date'] = next_session_info['date']
        self.save_config()
        
        # 自動デプロイ
        if self.auto_deploy():
            print("🚀 自動デプロイを実行しました")
        else:
            print("⚠️ 自動デプロイをスキップしました")
        
        return True
    
    def start_monitoring(self, interval=30):
        """監視開始（指定間隔で継続監視）"""
        print(f"🔍 記録ファイル監視を開始 (間隔: {interval}秒)")
        print(f"📁 監視対象: {self.summary_file}")
        print(f"🎯 更新対象: {self.index_file}")
        print("Ctrl+C で停止")
        
        try:
            while True:
                if self.check_and_update():
                    print("🔄 更新完了")
                else:
                    print("📝 変更なし")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n⭐ 監視を停止しました")

def main():
    """メイン関数"""
    import sys
    
    updater = DiscussionAutoUpdater()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            # 1回だけチェック
            if updater.check_and_update():
                print("✅ 更新完了")
            else:
                print("📝 更新なし")
                
        elif command == "monitor":
            # 継続監視
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            updater.start_monitoring(interval)
            
        elif command == "config":
            # 設定表示
            print("📋 現在の設定:")
            for key, value in updater.config.items():
                print(f"  {key}: {value}")
                
        else:
            print("❌ 不明なコマンド")
            print("使用法:")
            print("  python auto_update_system.py check     # 1回チェック")
            print("  python auto_update_system.py monitor   # 継続監視")
            print("  python auto_update_system.py config    # 設定表示")
    else:
        # デフォルトは1回チェック
        if updater.check_and_update():
            print("✅ 更新完了")
        else:
            print("📝 更新なし")

if __name__ == "__main__":
    main()