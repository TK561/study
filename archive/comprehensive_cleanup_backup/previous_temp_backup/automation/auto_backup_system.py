#!/usr/bin/env python3
"""
自動バックアップシステム - 重要ファイルの自動バックアップ
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

class AutoBackupSystem:
    """自動バックアップシステム"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.backup_root = self.project_root / "backups"
        self.config_file = self.project_root / "AUTO_BACKUP_CONFIG.json"
        self.log_file = self.project_root / "AUTO_BACKUP_LOG.json"
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """設定を読み込み"""
        default_config = {
            "backup_files": [
                "public/index.html",
                "vercel.json",
                "*.py",
                "*.md",
                "*.json",
                "*.sh"
            ],
            "exclude_patterns": [
                "__pycache__",
                ".git",
                "node_modules",
                "*.log",
                "backups"
            ],
            "retention_days": 7,
            "max_backups": 50,
            "compress": True,
            "auto_cleanup": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
            except:
                pass
        
        return default_config
    
    def save_config(self):
        """設定を保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def log_event(self, event_type: str, message: str, status: str = "info"):
        """イベントをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
            "status": status
        }
        
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                pass
        
        logs.append(log_entry)
        logs = logs[-200:]  # 最新200件のみ保持
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {event_type}: {message}")
    
    def get_files_to_backup(self) -> List[Path]:
        """バックアップ対象ファイルを取得"""
        files_to_backup = []
        
        for pattern in self.config['backup_files']:
            if '*' in pattern:
                # globパターン
                files = list(self.project_root.glob(pattern))
                if '**' not in pattern:
                    files.extend(list(self.project_root.glob(f"**/{pattern}")))
            else:
                # 単一ファイル
                file_path = self.project_root / pattern
                if file_path.exists():
                    files = [file_path]
                else:
                    files = []
            
            for file_path in files:
                if self.should_include_file(file_path):
                    files_to_backup.append(file_path)
        
        return list(set(files_to_backup))  # 重複を除去
    
    def should_include_file(self, file_path: Path) -> bool:
        """ファイルを含めるかチェック"""
        # 除外パターンをチェック
        for exclude in self.config['exclude_patterns']:
            if exclude in str(file_path):
                return False
        
        # ディレクトリは除外
        if file_path.is_dir():
            return False
        
        return True
    
    def create_backup(self) -> bool:
        """バックアップを作成"""
        try:
            # バックアップディレクトリを作成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.backup_root / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.log_event("BACKUP", f"バックアップ開始: {backup_dir}", "info")
            
            # バックアップ対象ファイルを取得
            files_to_backup = self.get_files_to_backup()
            
            if not files_to_backup:
                self.log_event("BACKUP", "バックアップ対象ファイルなし", "warning")
                return False
            
            # ファイルをコピー
            copied_files = []
            for file_path in files_to_backup:
                try:
                    # 相対パスを保持してコピー
                    rel_path = file_path.relative_to(self.project_root)
                    dest_path = backup_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    shutil.copy2(file_path, dest_path)
                    copied_files.append(str(rel_path))
                    
                except Exception as e:
                    self.log_event("BACKUP", f"ファイルコピーエラー {file_path}: {e}", "error")
            
            # 圧縮（設定されている場合）
            if self.config['compress']:
                zip_path = backup_dir.with_suffix('.zip')
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in copied_files:
                        source_path = backup_dir / file_path
                        if source_path.exists():
                            zipf.write(source_path, file_path)
                
                # 元のディレクトリを削除
                shutil.rmtree(backup_dir)
                backup_path = zip_path
            else:
                backup_path = backup_dir
            
            # バックアップ情報を記録
            backup_info = {
                "timestamp": timestamp,
                "path": str(backup_path),
                "files_count": len(copied_files),
                "files": copied_files,
                "compressed": self.config['compress']
            }
            
            info_file = backup_path.parent / f"{timestamp}_info.json"
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            self.log_event("BACKUP", f"完了: {len(copied_files)}ファイル -> {backup_path}", "success")
            return True
            
        except Exception as e:
            self.log_event("BACKUP", f"エラー: {e}", "error")
            return False
    
    def cleanup_old_backups(self):
        """古いバックアップを削除"""
        if not self.config['auto_cleanup']:
            return
        
        try:
            self.log_event("CLEANUP", "古いバックアップの削除開始", "info")
            
            # 保持期間を計算
            cutoff_date = datetime.now() - timedelta(days=self.config['retention_days'])
            
            # バックアップファイル/ディレクトリを取得
            backup_items = []
            if self.backup_root.exists():
                for item in self.backup_root.iterdir():
                    if item.is_file() and item.suffix == '.zip':
                        backup_items.append(item)
                    elif item.is_dir():
                        backup_items.append(item)
            
            # 日付でソート
            backup_items.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # 古いバックアップを削除
            deleted_count = 0
            for i, item in enumerate(backup_items):
                item_date = datetime.fromtimestamp(item.stat().st_mtime)
                
                # 保持期間を超えている、または最大数を超えている
                if (item_date < cutoff_date or i >= self.config['max_backups']):
                    try:
                        if item.is_file():
                            item.unlink()
                            # 対応するinfoファイルも削除
                            info_file = item.with_name(f"{item.stem}_info.json")
                            if info_file.exists():
                                info_file.unlink()
                        else:
                            shutil.rmtree(item)
                        
                        deleted_count += 1
                        self.log_event("CLEANUP", f"削除: {item.name}", "info")
                        
                    except Exception as e:
                        self.log_event("CLEANUP", f"削除エラー {item.name}: {e}", "error")
            
            if deleted_count > 0:
                self.log_event("CLEANUP", f"{deleted_count}個のバックアップを削除", "success")
            else:
                self.log_event("CLEANUP", "削除対象なし", "info")
                
        except Exception as e:
            self.log_event("CLEANUP", f"エラー: {e}", "error")
    
    def list_backups(self):
        """バックアップ一覧を表示"""
        if not self.backup_root.exists():
            print("📁 バックアップが見つかりません")
            return
        
        print("📁 バックアップ一覧:")
        print("-" * 60)
        
        backup_items = []
        for item in self.backup_root.iterdir():
            if item.is_file() and item.suffix == '.zip':
                backup_items.append(item)
            elif item.is_dir():
                backup_items.append(item)
        
        backup_items.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for item in backup_items:
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if item.is_file():
                size = f"{item.stat().st_size / 1024:.1f}KB"
                type_icon = "📦"
            else:
                size = f"{sum(f.stat().st_size for f in item.rglob('*') if f.is_file()) / 1024:.1f}KB"
                type_icon = "📁"
            
            print(f"{type_icon} {item.name}")
            print(f"   📅 {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   📊 {size}")
            
            # info.jsonがあれば内容表示
            info_file = item.parent / f"{item.stem}_info.json"
            if info_file.exists():
                try:
                    with open(info_file, 'r', encoding='utf-8') as f:
                        info = json.load(f)
                        print(f"   📝 {info['files_count']}ファイル")
                except:
                    pass
            
            print()
    
    def restore_backup(self, backup_name: str):
        """バックアップから復元"""
        backup_path = self.backup_root / backup_name
        
        if not backup_path.exists():
            self.log_event("RESTORE", f"バックアップが見つかりません: {backup_name}", "error")
            return False
        
        try:
            self.log_event("RESTORE", f"復元開始: {backup_name}", "info")
            
            if backup_path.suffix == '.zip':
                # ZIPファイルから復元
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(self.project_root)
            else:
                # ディレクトリから復元
                for item in backup_path.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(backup_path)
                        dest_path = self.project_root / rel_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_path)
            
            self.log_event("RESTORE", f"復元完了: {backup_name}", "success")
            return True
            
        except Exception as e:
            self.log_event("RESTORE", f"復元エラー: {e}", "error")
            return False
    
    def run_backup_cycle(self):
        """バックアップサイクルを実行"""
        print("🔄 自動バックアップサイクル開始")
        
        # バックアップ作成
        success = self.create_backup()
        
        # 古いバックアップ削除
        if success:
            self.cleanup_old_backups()
        
        return success

def main():
    """メイン関数"""
    backup_system = AutoBackupSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "run":
            backup_system.run_backup_cycle()
        elif command == "create":
            backup_system.create_backup()
        elif command == "list":
            backup_system.list_backups()
        elif command == "cleanup":
            backup_system.cleanup_old_backups()
        elif command == "restore" and len(sys.argv) > 2:
            backup_name = sys.argv[2]
            backup_system.restore_backup(backup_name)
        elif command == "config":
            print(json.dumps(backup_system.config, indent=2, ensure_ascii=False))
        elif command == "log":
            if backup_system.log_file.exists():
                with open(backup_system.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    for log in logs[-20:]:  # 最新20件
                        print(f"[{log['timestamp']}] {log['event_type']}: {log['message']}")
            else:
                print("📝 ログファイルが見つかりません")
        else:
            print("使用方法:")
            print("  python3 auto_backup_system.py run                 - バックアップサイクル実行")
            print("  python3 auto_backup_system.py create              - バックアップ作成")
            print("  python3 auto_backup_system.py list                - バックアップ一覧")
            print("  python3 auto_backup_system.py cleanup             - 古いバックアップ削除")
            print("  python3 auto_backup_system.py restore <name>      - バックアップから復元")
            print("  python3 auto_backup_system.py config              - 設定表示")
            print("  python3 auto_backup_system.py log                 - ログ表示")
    else:
        backup_system.run_backup_cycle()

if __name__ == "__main__":
    main()