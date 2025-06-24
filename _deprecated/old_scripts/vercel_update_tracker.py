#!/usr/bin/env python3
"""
Vercel更新履歴トラッカー
アップデート内容を自動保存し、履歴を管理
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class VercelUpdateTracker:
    def __init__(self, history_file: str = "VERCEL_UPDATE_HISTORY.json"):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """履歴ファイルを読み込む"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "updates": [],
            "metadata": {
                "projectId": "",
                "projectName": "",
                "currentVersion": "",
                "lastUpdate": ""
            }
        }
    
    def _save_history(self):
        """履歴をファイルに保存"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_update(self, 
                   version: str,
                   deploy_id: str,
                   url: str,
                   changes: List[str],
                   files: List[str],
                   status: str = "success",
                   project_id: Optional[str] = None,
                   project_name: Optional[str] = None) -> Dict:
        """新しい更新を追加"""
        
        timestamp = datetime.now().isoformat()
        
        update = {
            "date": timestamp,
            "version": version,
            "deployId": deploy_id,
            "url": url,
            "changes": changes,
            "files": files,
            "status": status
        }
        
        # 履歴に追加
        self.history["updates"].append(update)
        
        # メタデータ更新
        self.history["metadata"]["lastUpdate"] = timestamp
        self.history["metadata"]["currentVersion"] = version
        
        if project_id:
            self.history["metadata"]["projectId"] = project_id
        if project_name:
            self.history["metadata"]["projectName"] = project_name
        
        # 保存
        self._save_history()
        
        return update
    
    def get_latest_update(self) -> Optional[Dict]:
        """最新の更新情報を取得"""
        if self.history["updates"]:
            return self.history["updates"][-1]
        return None
    
    def get_update_by_version(self, version: str) -> Optional[Dict]:
        """バージョンで更新を検索"""
        for update in self.history["updates"]:
            if update["version"] == version:
                return update
        return None
    
    def get_all_updates(self) -> List[Dict]:
        """全ての更新履歴を取得"""
        return self.history["updates"]
    
    def rollback_info(self, version: str) -> Optional[Dict]:
        """指定バージョンへのロールバック情報を取得"""
        update = self.get_update_by_version(version)
        if update:
            return {
                "version": update["version"],
                "deployId": update["deployId"],
                "date": update["date"],
                "files": update["files"]
            }
        return None
    
    def generate_report(self) -> str:
        """更新履歴レポートを生成"""
        report = ["# Vercel更新履歴レポート\n"]
        report.append(f"**最終更新**: {self.history['metadata']['lastUpdate']}")
        report.append(f"**現在のバージョン**: {self.history['metadata']['currentVersion']}")
        report.append(f"**プロジェクト**: {self.history['metadata']['projectName']}\n")
        
        report.append("## 更新履歴\n")
        
        for update in reversed(self.history["updates"]):
            report.append(f"### {update['version']} - {update['date']}")
            report.append(f"- **デプロイID**: {update['deployId']}")
            report.append(f"- **URL**: {update['url']}")
            report.append(f"- **ステータス**: {update['status']}")
            report.append("- **変更内容**:")
            for change in update['changes']:
                report.append(f"  - {change}")
            report.append("- **更新ファイル**:")
            for file in update['files']:
                report.append(f"  - {file}")
            report.append("")
        
        return "\n".join(report)

# 使用例
if __name__ == "__main__":
    tracker = VercelUpdateTracker()
    
    # 最新の更新情報を表示
    latest = tracker.get_latest_update()
    if latest:
        print(f"最新バージョン: {latest['version']}")
        print(f"デプロイ日時: {latest['date']}")
        print(f"URL: {latest['url']}")
    
    # レポート生成
    print("\n" + tracker.generate_report())