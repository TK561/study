#!/usr/bin/env python3
"""
Gemini SQL Toolkit - 統合ツールキット
すべてのGemini to SQL機能を簡単に使用可能
"""

from gemini_to_sql_system import GeminiToSQLSystem
from advanced_gemini_sql_features import AdvancedGeminiSQLFeatures
from interactive_sql_assistant import InteractiveSQLAssistant, quick_sql
import json
from typing import Dict, List, Optional, Any

class GeminiSQLToolkit:
    """Gemini SQL機能の統合ツールキット"""
    
    def __init__(self):
        self.base = GeminiToSQLSystem()
        self.advanced = AdvancedGeminiSQLFeatures()
        self.assistant = InteractiveSQLAssistant()
    
    def quick_convert(self, natural_language: str, schema: Optional[Dict] = None) -> str:
        """クイック変換 - 自然言語を即座にSQLに変換"""
        result = self.base.generate_sql(natural_language, schema, use_deep_consultation=False)
        return result.get('sql', '')
    
    def deep_convert(self, natural_language: str, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """深層変換 - Geminiと相談しながら高精度なSQL生成"""
        return self.base.generate_sql(natural_language, schema, use_deep_consultation=True)
    
    def interactive_mode(self):
        """インタラクティブモードを起動"""
        self.assistant.start_session()
    
    def batch_convert(self, requests: List[str], schema: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """バッチ変換 - 複数のリクエストを一度に処理"""
        results = []
        for request in requests:
            print(f"\n処理中: {request}")
            result = self.base.generate_sql(request, schema, use_deep_consultation=False)
            results.append({
                'request': request,
                'sql': result.get('sql', ''),
                'validation': result.get('validation', {}),
                'error': result.get('error')
            })
        return results
    
    def analyze_and_optimize(self, sql: str, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """分析と最適化 - 既存SQLを分析して最適化"""
        analysis = self.advanced.analyze_query_plan(sql)
        optimization = self.base.optimize_sql(sql, schema)
        
        return {
            'original_sql': sql,
            'analysis': analysis,
            'optimized_sql': optimization.get('optimized_sql', sql),
            'improvements': optimization.get('explanation', '')
        }
    
    def generate_schema_from_description(self, description: str) -> Dict[str, Any]:
        """説明からスキーマを生成"""
        prompt = f"""
        以下の説明から、データベーススキーマを生成してください:
        
        {description}
        
        以下の形式でJSON出力してください:
        {{
            "table_name": {{
                "columns": {{
                    "column_name": "data_type constraints",
                    ...
                }},
                "indexes": [...],
                "foreign_keys": [...]
            }}
        }}
        """
        
        response = self.base._call_gemini(prompt)
        
        # JSONを抽出
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                return {"error": "スキーマ生成失敗", "raw": response}
        return {"error": "スキーマ生成失敗"}
    
    def sql_to_natural_language(self, sql: str) -> str:
        """SQLを自然言語に変換"""
        return self.base.explain_sql(sql)
    
    def generate_crud_operations(self, table_name: str, schema: Dict) -> Dict[str, str]:
        """CRUD操作を自動生成"""
        operations = {}
        
        # Create
        operations['create'] = self.quick_convert(
            f"{table_name}テーブルに新しいレコードを挿入",
            {table_name: schema}
        )
        
        # Read
        operations['read_all'] = self.quick_convert(
            f"{table_name}テーブルのすべてのレコードを取得",
            {table_name: schema}
        )
        
        operations['read_one'] = self.quick_convert(
            f"{table_name}テーブルからIDで1件取得",
            {table_name: schema}
        )
        
        # Update
        operations['update'] = self.quick_convert(
            f"{table_name}テーブルのレコードをIDで更新",
            {table_name: schema}
        )
        
        # Delete
        operations['delete'] = self.quick_convert(
            f"{table_name}テーブルからIDでレコードを削除",
            {table_name: schema}
        )
        
        return operations
    
    def create_sql_documentation(self, sql_queries: List[Dict[str, str]]) -> str:
        """SQLクエリのドキュメントを生成"""
        doc_lines = ["# SQL Documentation\n"]
        
        for query_info in sql_queries:
            name = query_info.get('name', 'Unnamed Query')
            sql = query_info.get('sql', '')
            description = query_info.get('description', '')
            
            doc_lines.append(f"\n## {name}")
            if description:
                doc_lines.append(f"\n{description}")
            
            doc_lines.append("\n```sql")
            doc_lines.append(sql)
            doc_lines.append("```")
            
            # 説明を生成
            explanation = self.sql_to_natural_language(sql)
            doc_lines.append(f"\n### 説明\n{explanation}")
        
        return '\n'.join(doc_lines)


# 便利な関数
def sql(text: str) -> str:
    """ショートカット関数 - 自然言語を即座にSQLに変換"""
    return quick_sql(text)

def sql_help():
    """使い方を表示"""
    print("""
🚀 Gemini SQL Toolkit - クイックヘルプ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

基本的な使い方:
    from gemini_sql_toolkit import sql
    
    # 簡単なSQL生成
    query = sql("ユーザーテーブルから年齢が20歳以上の人を取得")
    print(query)

高度な使い方:
    from gemini_sql_toolkit import GeminiSQLToolkit
    
    toolkit = GeminiSQLToolkit()
    
    # 深層相談を使った生成
    result = toolkit.deep_convert("複雑なクエリの説明")
    
    # インタラクティブモード
    toolkit.interactive_mode()
    
    # バッチ処理
    queries = toolkit.batch_convert([
        "売上データを月別に集計",
        "在庫が少ない商品を取得",
        "顧客の購買履歴を分析"
    ])
    
    # 最適化
    optimized = toolkit.analyze_and_optimize("SELECT * FROM users")

利用可能な機能:
    ✨ 自然言語からSQL生成
    🔍 SQL分析・最適化
    📊 スキーマ生成
    📝 ドキュメント生成
    🔄 SQL方言変換
    🧪 テストデータ生成
    🎯 インデックス提案
    🛡️ セキュリティチェック
    """)

# 使用例とデモ
def demo():
    """デモンストレーション"""
    print("=== Gemini SQL Toolkit デモ ===\n")
    
    toolkit = GeminiSQLToolkit()
    
    # 1. 簡単な変換
    print("1. 簡単な変換:")
    simple_sql = toolkit.quick_convert("商品テーブルから価格が1000円以上の商品を取得")
    print(simple_sql)
    
    # 2. スキーマ生成
    print("\n2. スキーマ生成:")
    schema = toolkit.generate_schema_from_description(
        "ECサイトの注文管理システム。顧客、商品、注文の情報を管理"
    )
    print(json.dumps(schema, ensure_ascii=False, indent=2))
    
    # 3. CRUD操作生成
    if isinstance(schema, dict) and not schema.get('error'):
        print("\n3. CRUD操作生成:")
        first_table = list(schema.keys())[0]
        crud = toolkit.generate_crud_operations(first_table, schema[first_table])
        for operation, sql in crud.items():
            print(f"\n{operation}:")
            print(sql)
    
    print("\n=== デモ完了 ===")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "help":
            sql_help()
        elif sys.argv[1] == "demo":
            demo()
        elif sys.argv[1] == "interactive":
            toolkit = GeminiSQLToolkit()
            toolkit.interactive_mode()
        else:
            # クイック変換
            request = ' '.join(sys.argv[1:])
            print(sql(request))
    else:
        # ヘルプを表示
        sql_help()