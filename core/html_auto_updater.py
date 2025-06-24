#!/usr/bin/env python3
"""
HTML自動更新システム - Gemini AI統合
デプロイ時に最終更新日時とステータスバッジを自動更新
"""

import os
import re
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLAutoUpdater:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backup_dir = self.project_root / ".html_backups"
        self.log_file = self.project_root / "logs" / "html_updates.json"
        self.ensure_directories()
        
        # 更新対象HTMLファイル
        self.target_files = [
            self.project_root / "index.html",
            self.project_root / "public" / "index.html"
        ]
        
        # 日本時間用のタイムゾーン情報
        self.jst_offset = 9  # UTC+9
        
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        (self.project_root / "logs").mkdir(exist_ok=True)
        
    def get_japanese_datetime(self) -> str:
        """日本時間の現在日時を取得 (YYYY年MM月DD日 HH:MM形式)"""
        now = datetime.utcnow()
        # UTC+9時間を加算して日本時間に変換
        jst_time = now.replace(hour=(now.hour + self.jst_offset) % 24)
        return jst_time.strftime('%Y年%m月%d日 %H:%M')
    
    def get_git_commit_info(self) -> Dict[str, str]:
        """最新のGitコミット情報を取得"""
        try:
            # 最新コミットメッセージ
            commit_msg = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%s"],
                capture_output=True, text=True, check=True
            ).stdout.strip()
            
            # 最新コミットハッシュ
            commit_hash = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%h"],
                capture_output=True, text=True, check=True
            ).stdout.strip()
            
            return {
                "message": commit_msg,
                "hash": commit_hash,
                "timestamp": self.get_japanese_datetime()
            }
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git情報取得エラー: {e}")
            return {
                "message": "Git情報取得失敗",
                "hash": "unknown",
                "timestamp": self.get_japanese_datetime()
            }
    
    def generate_status_badge(self, commit_message: str) -> str:
        """コミットメッセージから適切なステータスバッジを生成"""
        commit_lower = commit_message.lower()
        
        # AI推奨バッジマッピング
        badge_patterns = {
            "ディスカッション": "ディスカッションサイト統合完了",
            "discussion": "ディスカッションサイト統合完了", 
            "ui": "UI改善完了",
            "design": "デザイン更新完了",
            "feature": "新機能追加完了",
            "fix": "バグ修正完了",
            "deploy": "自動デプロイ完了",
            "auto": "自動システム稼働中",
            "test": "テスト実行完了",
            "doc": "ドキュメント更新完了",
            "security": "セキュリティ強化完了",
            "performance": "パフォーマンス向上完了",
            "api": "API統合完了",
            "database": "データベース更新完了",
            "mobile": "モバイル対応完了"
        }
        
        # パターンマッチング
        for keyword, badge in badge_patterns.items():
            if keyword in commit_lower:
                return badge
        
        # デフォルトバッジ（コミットの種類を推測）
        if "merge" in commit_lower:
            return "統合作業完了"
        elif "update" in commit_lower:
            return "システム更新完了"
        elif "add" in commit_lower:
            return "コンテンツ追加完了"
        elif "improve" in commit_lower:
            return "システム改善完了"
        else:
            return "最新版リリース完了"
    
    def create_backup(self, file_path: Path) -> Path:
        """HTMLファイルのバックアップを作成"""
        if not file_path.exists():
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_{timestamp}.html"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copy2(file_path, backup_path)
            logger.info(f"バックアップ作成: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"バックアップ作成失敗: {e}")
            return None
    
    def update_html_content(self, html_content: str, update_info: Dict) -> str:
        """HTMLコンテンツを更新"""
        updated_content = html_content
        changes = []
        
        # 1. 最終更新日時の更新 (行166)
        last_update_pattern = r'(<span id="lastUpdate">)[^<]+(</span>)'
        new_last_update = f'\\g<1>{update_info["datetime"]}\\g<2>'
        
        if re.search(last_update_pattern, updated_content):
            updated_content = re.sub(last_update_pattern, new_last_update, updated_content)
            changes.append(f"最終更新日時: {update_info['datetime']}")
        
        # 2. ステータスバッジの更新 (行164)
        badge_pattern = r'(<span class="badge">)[^<]+(</span>)'
        new_badge = f'\\g<1>{update_info["status_badge"]}\\g<2>'
        
        if re.search(badge_pattern, updated_content):
            updated_content = re.sub(badge_pattern, new_badge, updated_content)
            changes.append(f"ステータスバッジ: {update_info['status_badge']}")
        
        # 3. JavaScript固定日時の更新 (行392)
        js_datetime_pattern = r"(const LAST_UPDATE = ')[^']+(';)"
        new_js_datetime = f"\\g<1>{update_info['datetime']}\\g<2>"
        
        if re.search(js_datetime_pattern, updated_content):
            updated_content = re.sub(js_datetime_pattern, new_js_datetime, updated_content)
            changes.append(f"JavaScript日時: {update_info['datetime']}")
        
        # 4. Build Time コメントの更新 (行3)
        build_time_pattern = r'(<!-- Build Time: )[^-]+(-->)'
        current_month = datetime.now().strftime('%Y年%m月')
        new_build_time = f'\\g<1>{current_month} \\g<2>'
        
        if re.search(build_time_pattern, updated_content):
            updated_content = re.sub(build_time_pattern, new_build_time, updated_content)
            changes.append(f"ビルド時間: {current_month}")
        
        # 5. Deploy ID の更新 (行4)
        deploy_id_pattern = r'(<!-- Deploy ID: )[^-]+(-->)'
        deploy_id = datetime.now().strftime('%Y%m%d_%H%M')
        new_deploy_id = f'\\g<1>{deploy_id} \\g<2>'
        
        if re.search(deploy_id_pattern, updated_content):
            updated_content = re.sub(deploy_id_pattern, new_deploy_id, updated_content)
            changes.append(f"デプロイID: {deploy_id}")
        
        return updated_content, changes
    
    def validate_html_integrity(self, html_content: str) -> Tuple[bool, List[str]]:
        """HTMLの整合性をチェック"""
        issues = []
        
        # 基本構造チェック
        required_elements = [
            r'<!DOCTYPE html>',
            r'<html[^>]*>',
            r'<head>',
            r'</head>',
            r'<body>',
            r'</body>',
            r'</html>'
        ]
        
        for element in required_elements:
            if not re.search(element, html_content, re.IGNORECASE):
                issues.append(f"必須要素が見つかりません: {element}")
        
        # 危険なコードパターンチェック
        dangerous_patterns = [
            r'<script[^>]*src=["\'][^"\']*[<>]',  # XSS対策
            r'javascript:',  # JavaScript URL
            r'on\w+\s*=\s*["\'][^"\']*<',  # インラインイベントハンドラーの不正使用
            r'eval\s*\(',  # eval関数
            r'document\.write\s*\('  # document.write
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                issues.append(f"セキュリティリスク検出: {pattern}")
        
        # タグの対応チェック（簡易版）
        tag_pairs = ['html', 'head', 'body', 'div', 'span', 'script', 'style']
        for tag in tag_pairs:
            open_count = len(re.findall(f'<{tag}[^>]*>', html_content, re.IGNORECASE))
            close_count = len(re.findall(f'</{tag}>', html_content, re.IGNORECASE))
            if open_count != close_count:
                issues.append(f"タグの対応不一致: {tag} (開始:{open_count}, 終了:{close_count})")
        
        return len(issues) == 0, issues
    
    def log_update(self, update_info: Dict, changes: List[str], file_path: Path):
        """更新ログを記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file": str(file_path),
            "git_info": update_info.get("git_info", {}),
            "changes": changes,
            "update_datetime": update_info["datetime"],
            "status_badge": update_info["status_badge"]
        }
        
        # 既存ログを読み込み
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        # 最新100件のみ保持
        if len(logs) > 100:
            logs = logs[-100:]
        
        # ログ保存
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"ログ保存エラー: {e}")
    
    def rollback_from_backup(self, file_path: Path, backup_timestamp: str = None) -> bool:
        """バックアップからロールバック"""
        if not backup_timestamp:
            # 最新のバックアップを使用
            backup_files = list(self.backup_dir.glob(f"{file_path.stem}_*.html"))
            if not backup_files:
                logger.error("利用可能なバックアップがありません")
                return False
            backup_file = max(backup_files, key=lambda p: p.stat().st_mtime)
        else:
            backup_file = self.backup_dir / f"{file_path.stem}_{backup_timestamp}.html"
            if not backup_file.exists():
                logger.error(f"指定されたバックアップが見つかりません: {backup_file}")
                return False
        
        try:
            shutil.copy2(backup_file, file_path)
            logger.info(f"ロールバック完了: {backup_file} -> {file_path}")
            return True
        except Exception as e:
            logger.error(f"ロールバック失敗: {e}")
            return False
    
    def update_all_html_files(self) -> Dict:
        """全てのHTMLファイルを更新"""
        results = {
            "success": True,
            "updated_files": [],
            "errors": [],
            "backups_created": []
        }
        
        # Git情報を取得
        git_info = self.get_git_commit_info()
        
        # 更新情報を準備
        update_info = {
            "datetime": self.get_japanese_datetime(),
            "status_badge": self.generate_status_badge(git_info["message"]),
            "git_info": git_info
        }
        
        logger.info(f"更新開始: {update_info['datetime']}")
        logger.info(f"ステータス: {update_info['status_badge']}")
        
        for file_path in self.target_files:
            if not file_path.exists():
                logger.warning(f"ファイルが存在しません: {file_path}")
                continue
            
            try:
                # バックアップ作成
                backup_path = self.create_backup(file_path)
                if backup_path:
                    results["backups_created"].append(str(backup_path))
                
                # HTMLファイルを読み込み
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # 内容を更新
                updated_content, changes = self.update_html_content(original_content, update_info)
                
                # 整合性チェック
                is_valid, issues = self.validate_html_integrity(updated_content)
                if not is_valid:
                    logger.error(f"HTMLの整合性エラー: {file_path}")
                    for issue in issues:
                        logger.error(f"  - {issue}")
                    results["errors"].append(f"{file_path}: 整合性チェック失敗")
                    
                    # バックアップからロールバック
                    if backup_path:
                        self.rollback_from_backup(file_path)
                    continue
                
                # ファイルを更新
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                # ログ記録
                self.log_update(update_info, changes, file_path)
                
                results["updated_files"].append({
                    "file": str(file_path),
                    "changes": changes
                })
                
                logger.info(f"更新完了: {file_path}")
                for change in changes:
                    logger.info(f"  - {change}")
                
            except Exception as e:
                error_msg = f"{file_path}: {str(e)}"
                results["errors"].append(error_msg)
                results["success"] = False
                logger.error(f"更新エラー: {error_msg}")
                
                # エラー時のロールバック
                if backup_path:
                    self.rollback_from_backup(file_path)
        
        return results

def main():
    """メインエントリーポイント"""
    print("🔄 HTML自動更新システム - Gemini AI統合")
    print("=" * 50)
    
    updater = HTMLAutoUpdater()
    results = updater.update_all_html_files()
    
    if results["success"] and results["updated_files"]:
        print("✅ 更新完了")
        for file_info in results["updated_files"]:
            print(f"📄 {file_info['file']}")
            for change in file_info["changes"]:
                print(f"  - {change}")
        
        if results["backups_created"]:
            print(f"\n💾 バックアップ作成: {len(results['backups_created'])}件")
    
    elif results["errors"]:
        print("❌ エラーが発生しました")
        for error in results["errors"]:
            print(f"  - {error}")
        return 1
    
    else:
        print("ℹ️ 更新対象ファイルが見つかりませんでした")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())