#!/usr/bin/env python3
"""
ユニバーサル意図記録システム
どのプロジェクト・ディレクトリでもバックグラウンドで自動動作
プロジェクトを自動判別し、それぞれに適した意図記録を行う
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class UniversalIntentSystem:
    """プロジェクト横断的な意図記録システム"""
    
    def __init__(self, auto_detect=True):
        # ホームディレクトリに全体設定を保存
        self.global_config_dir = os.path.expanduser("~/.claude_intent_system")
        os.makedirs(self.global_config_dir, exist_ok=True)
        
        # 現在のプロジェクトを自動検出
        if auto_detect:
            self.current_project = self._detect_current_project()
        else:
            self.current_project = self._get_default_project()
        
        # プロジェクト固有の設定
        self.project_config_dir = os.path.join(os.getcwd(), ".claude_project")
        os.makedirs(self.project_config_dir, exist_ok=True)
        
        # データファイルパス
        self.global_projects_file = os.path.join(self.global_config_dir, "all_projects.json")
        self.project_intents_file = os.path.join(self.project_config_dir, "intents.json")
        self.project_timeline_file = os.path.join(self.project_config_dir, "timeline.json")
        
        # データ読み込み
        self.global_projects = self._load_global_projects()
        self.current_intents = self._load_current_intents()
        self.current_timeline = self._load_current_timeline()
        
        # プロジェクト登録
        self._register_current_project()
    
    def _detect_current_project(self) -> Dict:
        """現在のプロジェクトを自動検出"""
        cwd = os.getcwd()
        project_name = os.path.basename(cwd)
        
        # プロジェクトタイプを推測
        project_type = self._guess_project_type(cwd)
        
        # Git情報取得
        git_info = self._get_git_info(cwd)
        
        return {
            "name": project_name,
            "path": cwd,
            "type": project_type,
            "git_info": git_info,
            "detected_at": datetime.now().isoformat(),
            "project_id": hashlib.md5(cwd.encode()).hexdigest()[:8]
        }
    
    def _guess_project_type(self, path: str) -> str:
        """プロジェクトタイプを推測"""
        files_in_dir = os.listdir(path)
        
        # ファイル・フォルダの存在でタイプ判定
        if "package.json" in files_in_dir:
            return "node.js"
        elif "requirements.txt" in files_in_dir or "setup.py" in files_in_dir:
            return "python"
        elif "Cargo.toml" in files_in_dir:
            return "rust"
        elif "pom.xml" in files_in_dir:
            return "java"
        elif "go.mod" in files_in_dir:
            return "go"
        elif "vercel.json" in files_in_dir:
            return "web_app"
        elif "study" in files_in_dir and "research" in path.lower():
            return "research"
        elif ".git" in files_in_dir:
            return "git_project"
        else:
            return "general"
    
    def _get_git_info(self, path: str) -> Dict:
        """Git情報を取得"""
        try:
            import subprocess
            
            # ブランチ名
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'], 
                cwd=path, capture_output=True, text=True
            )
            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
            
            # リモートURL
            remote_result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'], 
                cwd=path, capture_output=True, text=True
            )
            remote = remote_result.stdout.strip() if remote_result.returncode == 0 else "no_remote"
            
            return {
                "branch": branch,
                "remote": remote,
                "has_git": True
            }
        except:
            return {"has_git": False}
    
    def auto_record_intent(self, file_path: str, operation: str, content_sample: str = ""):
        """ファイル操作から自動的に意図を推測・記録"""
        
        filename = os.path.basename(file_path)
        
        # 既に記録済みの場合はスキップ
        if filename in self.current_intents:
            return
        
        # 意図を推測
        intent = self._infer_intent(filename, operation, content_sample)
        
        if intent:
            category = self._categorize_by_project_type(filename, self.current_project["type"])
            
            self.record_intent(
                filename,
                intent,
                f"自動検出: {operation}操作から推測",
                category
            )
    
    def _infer_intent(self, filename: str, operation: str, content_sample: str) -> Optional[str]:
        """ファイル名・操作・内容から意図を推測"""
        
        filename_lower = filename.lower()
        content_lower = content_sample.lower()
        
        # プロジェクトタイプ別の推測パターン
        project_type = self.current_project["type"]
        
        if project_type == "research":
            return self._infer_research_intent(filename_lower, operation, content_lower)
        elif project_type == "web_app":
            return self._infer_webapp_intent(filename_lower, operation, content_lower)
        elif project_type == "python":
            return self._infer_python_intent(filename_lower, operation, content_lower)
        elif project_type == "node.js":
            return self._infer_nodejs_intent(filename_lower, operation, content_lower)
        else:
            return self._infer_general_intent(filename_lower, operation, content_lower)
    
    def _infer_research_intent(self, filename: str, operation: str, content: str) -> str:
        """研究プロジェクトの意図推測"""
        patterns = {
            "analysis": "データ分析・統計処理",
            "experiment": "実験実施・データ収集",
            "model": "機械学習モデル・アルゴリズム実装",
            "visualization": "結果可視化・グラフ生成",
            "report": "研究レポート・論文作成",
            "dataset": "データセット管理・前処理",
            "api": "外部API連携・データ取得",
            "test": "実験検証・テスト実装"
        }
        
        for pattern, intent in patterns.items():
            if pattern in filename:
                return intent
        
        if "import" in content and ("pandas" in content or "numpy" in content):
            return "データ分析・統計処理"
        elif "class" in content and ("model" in content or "classifier" in content):
            return "機械学習モデル実装"
        
        return "研究支援機能"
    
    def _infer_webapp_intent(self, filename: str, operation: str, content: str) -> str:
        """Webアプリの意図推測"""
        patterns = {
            "component": "UIコンポーネント実装",
            "page": "ページ・画面実装",
            "api": "API・バックエンド機能",
            "style": "スタイリング・デザイン",
            "config": "設定・環境構築",
            "auth": "認証・セキュリティ",
            "db": "データベース・永続化",
            "deploy": "デプロイ・公開設定"
        }
        
        for pattern, intent in patterns.items():
            if pattern in filename:
                return intent
        
        if filename.endswith(('.css', '.scss', '.less')):
            return "スタイリング・デザイン"
        elif filename.endswith(('.html', '.jsx', '.vue')):
            return "UIコンポーネント・画面実装"
        
        return "Webアプリ機能実装"
    
    def _infer_python_intent(self, filename: str, operation: str, content: str) -> str:
        """Pythonプロジェクトの意図推測"""
        patterns = {
            "main": "メインプログラム・エントリーポイント",
            "utils": "ユーティリティ・共通機能",
            "config": "設定管理・環境構築",
            "test": "テスト・品質保証",
            "cli": "コマンドライン・UI",
            "scraper": "データ収集・スクレイピング",
            "parser": "データ解析・パース処理",
            "client": "外部API・サービス連携"
        }
        
        for pattern, intent in patterns.items():
            if pattern in filename:
                return intent
        
        if "def main(" in content:
            return "メインプログラム実装"
        elif "class" in content:
            return "クラス・オブジェクト実装"
        elif "import requests" in content:
            return "外部API連携・HTTP通信"
        
        return "Python機能実装"
    
    def _infer_nodejs_intent(self, filename: str, operation: str, content: str) -> str:
        """Node.jsプロジェクトの意図推測"""
        patterns = {
            "server": "サーバー・バックエンド実装",
            "router": "ルーティング・エンドポイント",
            "middleware": "ミドルウェア・共通処理",
            "controller": "コントローラー・ビジネスロジック",
            "model": "データモデル・DB操作",
            "service": "サービス・外部連携",
            "util": "ユーティリティ・ヘルパー"
        }
        
        for pattern, intent in patterns.items():
            if pattern in filename:
                return intent
        
        if "express" in content:
            return "Express.js Webサーバー実装"
        elif "mongoose" in content:
            return "MongoDB・データベース操作"
        
        return "Node.js機能実装"
    
    def _infer_general_intent(self, filename: str, operation: str, content: str) -> str:
        """一般的なプロジェクトの意図推測"""
        if operation == "create":
            return "新機能・新要素の実装"
        elif operation == "edit":
            return "既存機能の改善・修正"
        elif filename.endswith('.md'):
            return "ドキュメント・説明書作成"
        elif filename.endswith(('.json', '.yaml', '.toml')):
            return "設定・構成管理"
        else:
            return "プロジェクト機能実装"
    
    def _categorize_by_project_type(self, filename: str, project_type: str) -> str:
        """プロジェクトタイプに応じたカテゴリ分類"""
        type_categories = {
            "research": {
                "analysis": "データ分析",
                "model": "AI・機械学習", 
                "experiment": "実験・検証",
                "report": "レポート・論文"
            },
            "web_app": {
                "component": "フロントエンド",
                "api": "バックエンド",
                "style": "デザイン・UI",
                "deploy": "インフラ・デプロイ"
            },
            "python": {
                "main": "コアロジック",
                "utils": "ユーティリティ",
                "test": "テスト・品質",
                "cli": "ユーザーインターフェース"
            }
        }
        
        if project_type in type_categories:
            for pattern, category in type_categories[project_type].items():
                if pattern in filename.lower():
                    return category
        
        return "その他"
    
    def record_intent(self, name: str, intent: str, context: str = "", category: str = "general"):
        """意図を記録"""
        intent_record = {
            "name": name,
            "intent": intent,
            "context": context,
            "category": category,
            "project_id": self.current_project["project_id"],
            "project_name": self.current_project["name"],
            "project_type": self.current_project["type"],
            "created_date": datetime.now().isoformat(),
            "tags": self._extract_tags(intent + " " + context),
            "related_files": self._find_related_files(name)
        }
        
        self.current_intents[name] = intent_record
        
        # タイムラインに追加
        timeline_entry = {
            "date": datetime.now().isoformat(),
            "action": "intent_recorded",
            "item": name,
            "intent_summary": intent[:100] + "..." if len(intent) > 100 else intent,
            "project": self.current_project["name"]
        }
        self.current_timeline.append(timeline_entry)
        
        self._save_current_data()
    
    def get_project_summary(self) -> str:
        """プロジェクト全体のサマリー生成"""
        summary = f"""# {self.current_project['name']} プロジェクトサマリー

**プロジェクトタイプ**: {self.current_project['type']}  
**場所**: {self.current_project['path']}  
**登録日**: {self.current_project['detected_at'][:10]}

## 意図記録済みファイル ({len(self.current_intents)}件)

"""
        
        # カテゴリ別に整理
        categories = {}
        for name, record in self.current_intents.items():
            cat = record.get("category", "その他")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(record)
        
        for category, items in categories.items():
            summary += f"### {category}\n"
            for item in items:
                summary += f"- **{item['name']}**: {item['intent']}\n"
            summary += "\n"
        
        return summary
    
    def _register_current_project(self):
        """現在のプロジェクトを全体リストに登録"""
        project_id = self.current_project["project_id"]
        self.global_projects[project_id] = self.current_project
        self._save_global_projects()
    
    def _extract_tags(self, text: str) -> List[str]:
        """テキストからタグを抽出"""
        # プロジェクトタイプ別のキーワード
        all_keywords = {
            "research": ["分析", "実験", "モデル", "データ", "統計", "可視化"],
            "web_app": ["UI", "API", "デプロイ", "認証", "データベース", "フロント"],
            "python": ["クラス", "関数", "ライブラリ", "CLI", "スクリプト"],
            "general": ["実装", "機能", "設定", "テスト", "ドキュメント"]
        }
        
        project_type = self.current_project["type"]
        keywords = all_keywords.get(project_type, all_keywords["general"])
        
        tags = []
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                tags.append(keyword)
        
        return tags
    
    def _find_related_files(self, filename: str) -> List[str]:
        """関連ファイルを検索"""
        related = []
        search_term = filename.lower().replace(".py", "").replace("_", "")
        
        for root, dirs, files in os.walk("."):
            if len(related) >= 5:  # 最大5件
                break
            for file in files:
                if search_term in file.lower() and file != filename:
                    related.append(os.path.join(root, file))
        
        return related
    
    # データ保存・読み込みメソッド
    def _load_global_projects(self) -> Dict:
        if os.path.exists(self.global_projects_file):
            with open(self.global_projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_current_intents(self) -> Dict:
        if os.path.exists(self.project_intents_file):
            with open(self.project_intents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_current_timeline(self) -> List:
        if os.path.exists(self.project_timeline_file):
            with open(self.project_timeline_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_global_projects(self):
        with open(self.global_projects_file, 'w', encoding='utf-8') as f:
            json.dump(self.global_projects, f, ensure_ascii=False, indent=2)
    
    def _save_current_data(self):
        with open(self.project_intents_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_intents, f, ensure_ascii=False, indent=2)
        
        with open(self.project_timeline_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_timeline, f, ensure_ascii=False, indent=2)
    
    def _get_default_project(self) -> Dict:
        """デフォルトプロジェクト情報"""
        cwd = os.getcwd()
        return {
            "name": os.path.basename(cwd),
            "path": cwd,
            "type": "general",
            "git_info": {"has_git": False},
            "detected_at": datetime.now().isoformat(),
            "project_id": hashlib.md5(cwd.encode()).hexdigest()[:8]
        }

# グローバル関数
def auto_intent_record(file_path: str, operation: str, content_sample: str = ""):
    """バックグラウンド自動記録"""
    try:
        system = UniversalIntentSystem()
        system.auto_record_intent(file_path, operation, content_sample)
    except:
        pass  # エラーでも他の処理を止めない

def get_project_info():
    """現在のプロジェクト情報取得"""
    system = UniversalIntentSystem()
    return system.get_project_summary()

def why_this_file_universal(filename: str) -> str:
    """ユニバーサル版ファイル意図検索"""
    system = UniversalIntentSystem()
    if filename in system.current_intents:
        record = system.current_intents[filename]
        return f"""
📄 **{filename}** ({system.current_project['name']}プロジェクト)

**なぜ作った？**: {record['intent']}

**背景・経緯**: {record.get('context', '記録なし')}

**カテゴリ**: {record.get('category', 'その他')}

**作成日**: {record['created_date'][:10]}
"""
    else:
        return f"❓ {filename} の作成意図は記録されていません"

if __name__ == "__main__":
    # システム初期化・テスト
    system = UniversalIntentSystem()
    
    print("🌍 ユニバーサル意図記録システム初期化完了")
    print(f"📁 現在のプロジェクト: {system.current_project['name']}")
    print(f"🏷️ プロジェクトタイプ: {system.current_project['type']}")
    print(f"📊 記録済み意図: {len(system.current_intents)}件")
    
    # プロジェクトサマリー表示
    print("\n" + system.get_project_summary())