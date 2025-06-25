#!/usr/bin/env python3
"""
HTML自動更新システム - Gemini AI推奨実装
最終更新日時とステータスバッジの自動更新を安全に実行
"""

import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import hashlib

class HTMLAutoUpdater:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backup_dir = self.project_root / ".html_backups"
        self.log_file = self.project_root / "logs" / "html_updates.json"
        self.ensure_directories()
        
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        self.backup_dir.mkdir(exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
    def get_current_timestamp(self):
        """現在の日本時間を取得"""
        now = datetime.now()
        return now.strftime("%Y年%m月%d日 %H:%M")
        
    def get_git_commit_info(self):
        """最新のGitコミット情報を取得"""
        try:
            # 最新コミットメッセージ
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=%s"],
                capture_output=True,
                text=True,
                check=True
            )
            commit_msg = result.stdout.strip()
            
            # コミット日時
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=%ci"],
                capture_output=True,
                text=True,
                check=True
            )
            commit_date = result.stdout.strip()
            
            return {
                "message": commit_msg,
                "date": commit_date,
                "success": True
            }
        except Exception as e:
            return {
                "message": "Manual update",
                "date": str(datetime.now()),
                "success": False,
                "error": str(e)
            }
            
    def generate_status_badge(self, commit_info):
        """コミット情報からステータスバッジを生成"""
        commit_msg = commit_info.get("message", "").lower()
        
        # パターンマッチングでバッジを生成
        if any(word in commit_msg for word in ["discussion", "ディスカッション"]):
            return "ディスカッションサイト統合完了"
        elif any(word in commit_msg for word in ["deploy", "デプロイ"]):
            return "自動デプロイ完了"
        elif any(word in commit_msg for word in ["fix", "修正", "bug"]):
            return "バグ修正完了"
        elif any(word in commit_msg for word in ["update", "更新", "improve"]):
            return "システム更新完了"
        elif any(word in commit_msg for word in ["add", "追加", "new"]):
            return "新機能追加完了"
        elif any(word in commit_msg for word in ["ui", "design", "デザイン"]):
            return "UI改善完了"
        elif any(word in commit_msg for word in ["auto", "自動"]):
            return "自動化システム完了"
        else:
            return "最新更新完了"
            
    def create_backup(self, file_path):
        """ファイルのバックアップを作成"""
        if not os.path.exists(file_path):
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = Path(file_path).name
        backup_path = self.backup_dir / f"{file_name}.{timestamp}.bak"
        
        try:
            shutil.copy2(file_path, backup_path)
            return str(backup_path)
        except Exception as e:
            print(f"❌ バックアップ作成エラー: {e}")
            return None
            
    def validate_html_content(self, content):
        """HTMLコンテンツの安全性を検証"""
        # 基本的なHTML構造チェック
        if not content.strip().startswith('<!DOCTYPE html>'):
            return False, "無効なHTML構造"
            
        # 悪意のあるスクリプトタグチェック
        dangerous_patterns = [
            r'<script[^>]*src\s*=\s*["\']https?://[^"\']*["\'][^>]*>',
            r'javascript:',
            r'eval\s*\(',
            r'document\.write\s*\('
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return False, f"危険なパターンを検出: {pattern}"
                
        return True, "安全"
        
    def update_html_file(self, file_path, timestamp, badge_text):
        """HTMLファイルを更新"""
        if not os.path.exists(file_path):
            print(f"⚠️ ファイルが見つかりません: {file_path}")
            return False
            
        # バックアップ作成
        backup_path = self.create_backup(file_path)
        if not backup_path:
            print(f"❌ バックアップ作成に失敗: {file_path}")
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 安全性検証
            is_safe, message = self.validate_html_content(content)
            if not is_safe:
                print(f"❌ セキュリティエラー: {message}")
                return False
                
            # 最終更新日時の更新（HTML内）
            content = re.sub(
                r'(<span id="lastUpdate">)[^<]*(</span>)',
                f'\\g<1>{timestamp}\\g<2>',
                content
            )
            
            # 最終更新日時の更新（JavaScript内）
            content = re.sub(
                r"(const LAST_UPDATE = ')[^']*(';)",
                f"\\g<1>{timestamp}\\g<2>",
                content
            )
            
            # ステータスバッジの更新
            content = re.sub(
                r'(<span class="badge">)[^<]*(</span>)',
                f'\\g<1>{badge_text}\\g<2>',
                content
            )
            
            # ファイル書き込み
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✅ {file_path} を更新しました")
            return True
            
        except Exception as e:
            print(f"❌ ファイル更新エラー: {e}")
            # エラー時はバックアップから復元
            if backup_path and os.path.exists(backup_path):
                shutil.copy2(backup_path, file_path)
                print(f"🔄 バックアップから復元しました: {file_path}")
            return False
            
    def log_update(self, updates):
        """更新ログを記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "updates": updates,
            "success": all(u.get("success", False) for u in updates)
        }
        
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
                
        logs.append(log_entry)
        
        # 最新50件のログのみ保持
        if len(logs) > 50:
            logs = logs[-50:]
            
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ ログ記録エラー: {e}")
            
    def update_all_html_files(self):
        """全HTMLファイルを更新"""
        print("🚀 HTML自動更新システム開始")
        print("="*50)
        
        # 現在の情報を取得
        timestamp = self.get_current_timestamp()
        commit_info = self.get_git_commit_info()
        badge_text = self.generate_status_badge(commit_info)
        
        print(f"📅 更新日時: {timestamp}")
        print(f"🏷️ ステータス: {badge_text}")
        print(f"📝 コミット: {commit_info.get('message', 'N/A')}")
        
        # 更新対象ファイル
        html_files = [
            "index.html",
            "public/index.html"
        ]
        
        updates = []
        
        for file_path in html_files:
            success = self.update_html_file(file_path, timestamp, badge_text)
            updates.append({
                "file": file_path,
                "success": success,
                "timestamp": timestamp,
                "badge": badge_text
            })
            
        # ログ記録
        self.log_update(updates)
        
        success_count = sum(1 for u in updates if u["success"])
        print(f"\n📊 結果: {success_count}/{len(updates)} ファイルが正常に更新されました")
        
        if success_count == len(updates):
            print("✅ 全ファイルの更新が完了しました")
            return True
        else:
            print("⚠️ 一部のファイル更新に失敗しました")
            return False

def main():
    """メインエントリーポイント"""
    updater = HTMLAutoUpdater()
    success = updater.update_all_html_files()
    
    if success:
        print("\n🎉 HTML自動更新システムが正常に完了しました")
    else:
        print("\n❌ HTML自動更新システムでエラーが発生しました")
        
    return success

if __name__ == "__main__":
    main()