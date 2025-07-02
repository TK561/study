#!/usr/bin/env python3
"""
ディスカッション記録自動更新システム
- 毎週木曜18時のディスカッション開催に対応
- 新しいディスカッション記録追加時に次回タブを自動更新
- GitHubへの自動コミット・プッシュ機能
"""

import os
import re
import json
import datetime
from pathlib import Path
import subprocess

class DiscussionAutoUpdater:
    def __init__(self):
        self.base_dir = Path("/mnt/c/Desktop/Research")
        self.discussion_file = self.base_dir / "public/discussion-site/index.html"
        self.config_file = self.base_dir / "discussion_auto_config.json"
        
    def load_config(self):
        """設定ファイル読み込み"""
        default_config = {
            "last_session_number": 13,
            "meeting_time": "18:00",
            "meeting_day": "thursday",
            "auto_update_enabled": True,
            "auto_commit": True
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # デフォルト値で不足項目を補完
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config):
        """設定ファイル保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def get_next_thursday_date(self, base_date=None):
        """次の木曜日の日付を取得"""
        if base_date is None:
            base_date = datetime.datetime.now()
        
        # 今日が木曜日かチェック
        days_until_thursday = (3 - base_date.weekday()) % 7  # 3 = Thursday
        if days_until_thursday == 0:  # 今日が木曜日
            days_until_thursday = 7  # 来週の木曜日
            
        next_thursday = base_date + datetime.timedelta(days=days_until_thursday)
        return next_thursday
    
    def extract_session_numbers(self, html_content):
        """HTMLから現在のセッション番号を抽出"""
        pattern = r'第(\d+)回.*?ディスカッション'
        matches = re.findall(pattern, html_content)
        if matches:
            return [int(match) for match in matches]
        return []
    
    def detect_new_session_added(self):
        """新しいセッションが追加されたかチェック"""
        config = self.load_config()
        
        if not self.discussion_file.exists():
            print("❌ ディスカッションファイルが見つかりません")
            return False
            
        with open(self.discussion_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        session_numbers = self.extract_session_numbers(content)
        current_max = max(session_numbers) if session_numbers else 0
        last_recorded = config.get("last_session_number", 0)
        
        print(f"📊 現在の最大セッション番号: {current_max}")
        print(f"📊 前回記録したセッション番号: {last_recorded}")
        
        if current_max > last_recorded:
            print(f"🆕 新しいセッション第{current_max}回が検出されました")
            return True, current_max
        
        return False, current_max
    
    def generate_next_session_content(self, current_session_num):
        """次回セッションの内容を生成"""
        next_session = current_session_num + 1
        next_date = self.get_next_thursday_date()
        
        # 前回の内容に基づいて次回の議題を設定
        agenda_templates = {
            14: {
                "title": "実用化システム構築・学術論文執筆・産業応用展開",
                "badge": "論文化",
                "topics": [
                    "<strong>Cohen's Power Analysis成果</strong>: カテゴリ数12飽和現象の学術論文化",
                    "<strong>実用化システム</strong>: Webアプリケーション版とAPI開発", 
                    "<strong>産業応用展開</strong>: 商用化パートナーとの連携検討",
                    "<strong>次世代研究</strong>: マルチモーダル統合とLLM連携",
                    "<strong>学術発表</strong>: 国際会議投稿と特許出願準備"
                ]
            },
            15: {
                "title": "学術論文完成・システム商用化・次世代研究開始",
                "badge": "商用化", 
                "topics": [
                    "<strong>論文投稿完了</strong>: 国際会議への投稿とレビュー対応",
                    "<strong>システム商用化</strong>: 正式サービスローンチ準備",
                    "<strong>パートナー連携</strong>: 企業との本格的協業開始",
                    "<strong>次世代研究</strong>: マルチモーダル統合システムの本格開発",
                    "<strong>知財保護</strong>: 特許出願と技術ライセンス戦略"
                ]
            }
        }
        
        # デフォルトテンプレート
        default_template = {
            "title": "研究発展・システム拡張・産業応用推進",
            "badge": "発展",
            "topics": [
                "<strong>前回成果の発展</strong>: 前回ディスカッションの成果を基にした次段階実装",
                "<strong>システム拡張</strong>: 新機能追加と性能向上",
                "<strong>産業応用</strong>: 実用化システムの適用範囲拡大",
                "<strong>学術発表</strong>: 研究成果の学会発表と論文執筆",
                "<strong>次期計画</strong>: 中長期的な研究開発ロードマップ"
            ]
        }
        
        template = agenda_templates.get(next_session, default_template)
        
        return {
            "session_number": next_session,
            "date": next_date.strftime("%Y/%m/%d"),
            "iso_date": next_date.strftime("%Y-%m-%d"),
            "title": template["title"],
            "badge": template["badge"],
            "topics": template["topics"]
        }
    
    def update_next_session_tab(self, session_info):
        """次回セッションタブを更新"""
        if not self.discussion_file.exists():
            print("❌ ディスカッションファイルが見つかりません")
            return False
            
        with open(self.discussion_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 次回タブの内容を新しい内容に置換
        topics_html = "\\n".join([f"                                <li>{topic}</li>" for topic in session_info["topics"]])
        
        new_next_tab = f'''                <!-- 次回タブ -->
                <div id="next-meeting" class="tab-content">
                    <h2>📅 第{session_info["session_number"]}回ディスカッション: {session_info["iso_date"]} 18:00</h2>
                    
                    <div class="discussion-item">
                        <div class="discussion-header">
                            <div class="discussion-title">第{session_info["session_number"]}回 - {session_info["title"]}<span class="achievement-badge">{session_info["badge"]}</span></div>
                            <div class="discussion-date">{session_info["date"]} 18:00</div>
                        </div>
                        <div class="discussion-content">
                            <ul>
{topics_html}
                            </ul>
                        </div>
                    </div>'''
        
        # 既存の次回タブ部分を置換
        pattern = r'(\s*<!-- 次回タブ -->\s*<div id="next-meeting" class="tab-content">.*?)</div>\s*<div class="section">'
        replacement = new_next_tab + '\\n                    \\n                    <div class="section">'
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if updated_content != content:
            with open(self.discussion_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✅ 第{session_info['session_number']}回ディスカッション内容を更新しました")
            return True
        else:
            print("⚠️ 更新対象が見つかりませんでした")
            return False
    
    def commit_and_push_changes(self, session_number):
        """変更をGitにコミット・プッシュ"""
        try:
            os.chdir(self.base_dir)
            
            # Git add
            subprocess.run(["git", "add", "public/discussion-site/index.html", "discussion_auto_config.json"], check=True)
            
            # Git commit
            commit_message = f"""📅 第{session_number}回ディスカッション自動生成

- 毎週木曜18時のディスカッション予定を自動更新
- 前回セッション完了に基づく次回議題の自動設定
- discussion_auto_updater.pyによる自動生成

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Git push
            subprocess.run(["git", "push", "origin", "main"], check=True)
            
            print("✅ Gitコミット・プッシュ完了")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git操作失敗: {e}")
            return False
    
    def run_auto_update(self):
        """自動更新実行"""
        print("🔄 ディスカッション記録自動更新開始")
        
        config = self.load_config()
        
        if not config.get("auto_update_enabled", True):
            print("⚠️ 自動更新が無効化されています")
            return False
        
        # 新しいセッションが追加されたかチェック
        new_session_detected, current_max = self.detect_new_session_added()
        
        if not new_session_detected:
            print("📋 新しいセッションは検出されませんでした")
            return False
        
        # 次回セッション情報生成
        next_session_info = self.generate_next_session_content(current_max)
        
        # 次回タブ更新
        if self.update_next_session_tab(next_session_info):
            # 設定更新
            config["last_session_number"] = current_max
            config["last_update"] = datetime.datetime.now().isoformat()
            self.save_config(config)
            
            # Git操作
            if config.get("auto_commit", True):
                self.commit_and_push_changes(next_session_info["session_number"])
            
            print(f"🎉 第{next_session_info['session_number']}回ディスカッション自動生成完了!")
            print(f"📅 次回日時: {next_session_info['iso_date']} 18:00")
            return True
        
        return False

def main():
    """メイン実行関数"""
    updater = DiscussionAutoUpdater()
    
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            # 手動チェック
            detected, session_num = updater.detect_new_session_added()
            if detected:
                print(f"🆕 新しいセッション第{session_num}回が検出されました")
            else:
                print("📋 新しいセッションはありません")
                
        elif command == "force":
            # 強制実行
            config = updater.load_config()
            current_max = config.get("last_session_number", 13)
            next_info = updater.generate_next_session_content(current_max)
            updater.update_next_session_tab(next_info)
            print(f"🔧 強制的に第{next_info['session_number']}回を生成しました")
            
        elif command == "config":
            # 設定表示
            config = updater.load_config()
            print("⚙️ 現在の設定:")
            for key, value in config.items():
                print(f"  {key}: {value}")
                
        else:
            print("❌ 不明なコマンド:", command)
            print("使用可能コマンド: check, force, config")
    else:
        # 通常の自動更新実行
        updater.run_auto_update()

if __name__ == "__main__":
    main()