#!/usr/bin/env python3
"""
Vercel エラー予防システム
デプロイ前の自動チェックとエラー予防
"""

import os
import ast
import json
import re
from datetime import datetime

class VercelErrorPrevention:
    """Vercelエラー予防・チェックシステム"""
    
    def __init__(self):
        self.error_patterns = self._load_known_errors()
        self.check_results = []
    
    def _load_known_errors(self):
        """既知のエラーパターンを読み込み"""
        return {
            "vercel_functions_format": {
                "pattern": r"def handler\(request\):",
                "error": "Vercel Functions は class handler(BaseHTTPRequestHandler) 形式が必要",
                "solution": "クラス形式に変更してください"
            },
            "html_string_issue": {
                "pattern": r"html = '''.*\+.*'''",
                "error": "HTML文字列の連結でVercel Functionsエラーが発生",
                "solution": "f-string形式を使用し、CSS波括弧を{{}}でエスケープ"
            },
            "missing_basehttp": {
                "pattern": r"class handler.*:",
                "import_check": "from http.server import BaseHTTPRequestHandler",
                "error": "BaseHTTPRequestHandler のインポートが必要",
                "solution": "from http.server import BaseHTTPRequestHandler を追加"
            },
            "wrong_response_format": {
                "pattern": r"return\s*{[^}]*'statusCode'",
                "error": "Vercel Functions の戻り値形式が古い",
                "solution": "self.send_response() 形式に変更"
            },
            "token_exposure": {
                "pattern": r"ghp_[a-zA-Z0-9]{36}",
                "error": "GitHubトークンが検出されました",
                "solution": "トークンを削除し .env ファイルを使用"
            }
        }
    
    def check_api_file(self, file_path="api/index.py"):
        """APIファイルの検証"""
        print(f"🔍 {file_path} を検証中...")
        
        if not os.path.exists(file_path):
            self._add_result("error", f"{file_path} が見つかりません")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 構文チェック
            try:
                ast.parse(content)
                self._add_result("success", "Python構文: OK")
            except SyntaxError as e:
                self._add_result("error", f"構文エラー: {e}")
                return False
            
            # Vercel Functions形式チェック
            self._check_vercel_functions_format(content)
            
            # インポートチェック
            self._check_required_imports(content)
            
            # レスポンス形式チェック
            self._check_response_format(content)
            
            # トークン露出チェック
            self._check_token_exposure(content)
            
            return True
            
        except Exception as e:
            self._add_result("error", f"ファイル読み込みエラー: {e}")
            return False
    
    def _check_vercel_functions_format(self, content):
        """Vercel Functions形式チェック"""
        if re.search(self.error_patterns["vercel_functions_format"]["pattern"], content):
            self._add_result("error", self.error_patterns["vercel_functions_format"]["error"])
            self._add_result("solution", self.error_patterns["vercel_functions_format"]["solution"])
        elif "class handler(BaseHTTPRequestHandler)" in content:
            self._add_result("success", "Vercel Functions形式: OK")
        else:
            self._add_result("warning", "Vercel Functions形式が不明確")
    
    def _check_required_imports(self, content):
        """必要なインポートをチェック"""
        required_imports = [
            "from http.server import BaseHTTPRequestHandler",
            "import datetime",
            "import os"
        ]
        
        for import_stmt in required_imports:
            if import_stmt in content:
                self._add_result("success", f"インポート OK: {import_stmt}")
            else:
                self._add_result("warning", f"推奨インポート不足: {import_stmt}")
    
    def _check_response_format(self, content):
        """レスポンス形式チェック"""
        if re.search(self.error_patterns["wrong_response_format"]["pattern"], content):
            self._add_result("error", self.error_patterns["wrong_response_format"]["error"])
            self._add_result("solution", self.error_patterns["wrong_response_format"]["solution"])
        elif "self.send_response(" in content:
            self._add_result("success", "レスポンス形式: OK")
        else:
            self._add_result("warning", "レスポンス形式が不明確")
    
    def _check_token_exposure(self, content):
        """トークン露出チェック"""
        if re.search(self.error_patterns["token_exposure"]["pattern"], content):
            self._add_result("critical", self.error_patterns["token_exposure"]["error"])
            self._add_result("solution", self.error_patterns["token_exposure"]["solution"])
        else:
            self._add_result("success", "トークン露出: なし")
    
    def check_project_structure(self):
        """プロジェクト構造チェック"""
        print("🔍 プロジェクト構造を検証中...")
        
        required_files = {
            "api/index.py": "Vercel Functions本体",
            "vercel.json": "Vercel設定ファイル",
            ".env": "環境変数ファイル"
        }
        
        for file_path, description in required_files.items():
            if os.path.exists(file_path):
                self._add_result("success", f"{description}: 存在")
            else:
                self._add_result("warning", f"{description}: 不足 ({file_path})")
    
    def check_env_variables(self):
        """環境変数チェック"""
        print("🔍 環境変数を検証中...")
        
        required_vars = ["VERCEL_TOKEN", "VERCEL_PROJECT_ID"]
        
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                env_content = f.read()
            
            for var in required_vars:
                if f"{var}=" in env_content:
                    self._add_result("success", f"環境変数 {var}: 設定済み")
                else:
                    self._add_result("error", f"環境変数 {var}: 未設定")
                    
        except FileNotFoundError:
            self._add_result("error", ".env ファイルが見つかりません")
    
    def _add_result(self, level, message):
        """チェック結果を追加"""
        icons = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨",
            "solution": "💡"
        }
        
        result = {
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        self.check_results.append(result)
        print(f"{icons.get(level, '📋')} {message}")
    
    def generate_report(self):
        """チェック結果レポート生成"""
        report = {
            "check_time": datetime.now().isoformat(),
            "results": self.check_results,
            "summary": self._generate_summary()
        }
        
        # レポートファイル保存
        report_file = f"vercel_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 チェックレポート保存: {report_file}")
        return report
    
    def _generate_summary(self):
        """チェック結果サマリー"""
        levels = {}
        for result in self.check_results:
            level = result["level"]
            levels[level] = levels.get(level, 0) + 1
        
        total_issues = levels.get("error", 0) + levels.get("critical", 0)
        
        return {
            "total_checks": len(self.check_results),
            "errors": levels.get("error", 0),
            "warnings": levels.get("warning", 0),
            "critical": levels.get("critical", 0),
            "success": levels.get("success", 0),
            "deployment_ready": total_issues == 0
        }
    
    def full_check(self):
        """完全チェック実行"""
        print("🛡️ Vercel エラー予防システム開始")
        print("=" * 60)
        
        # 各チェック実行
        self.check_project_structure()
        self.check_env_variables()
        self.check_api_file()
        
        # レポート生成
        report = self.generate_report()
        
        print("\n" + "=" * 60)
        print("📊 チェック完了サマリー")
        print("=" * 60)
        
        summary = report["summary"]
        print(f"✅ 成功: {summary['success']}")
        print(f"⚠️ 警告: {summary['warnings']}")
        print(f"❌ エラー: {summary['errors']}")
        print(f"🚨 重大: {summary['critical']}")
        
        if summary["deployment_ready"]:
            print("\n🎉 デプロイ準備完了!")
            print("💡 python3 quick_vercel_fix.py でデプロイ実行可能")
        else:
            print("\n⚠️ エラーを修正してからデプロイしてください")
        
        return summary["deployment_ready"]

def save_error_knowledge(error_type, error_message, solution):
    """新しいエラー情報をナレッジベースに保存"""
    knowledge_file = "vercel_error_history.json"
    
    new_error = {
        "timestamp": datetime.now().isoformat(),
        "type": error_type,
        "message": error_message,
        "solution": solution,
        "auto_detected": True
    }
    
    # 既存ナレッジ読み込み
    if os.path.exists(knowledge_file):
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            knowledge = json.load(f)
    else:
        knowledge = {"errors": []}
    
    # 新しいエラー追加
    knowledge["errors"].append(new_error)
    
    # 最新50件のみ保持
    if len(knowledge["errors"]) > 50:
        knowledge["errors"] = knowledge["errors"][-50:]
    
    # 保存
    with open(knowledge_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)
    
    print(f"📚 エラーナレッジを保存: {error_type}")

if __name__ == "__main__":
    checker = VercelErrorPrevention()
    deployment_ready = checker.full_check()
    
    if deployment_ready:
        print("\n🚀 自動デプロイを実行しますか? (y/n)")
        # 実際の運用では自動実行も可能
        # import subprocess
        # subprocess.run(["python3", "quick_vercel_fix.py"])
    else:
        print("\n🔧 修正が必要なエラーがあります")
        print("📖 詳細は VERCEL_ERROR_KNOWLEDGE_BASE.md を参照")