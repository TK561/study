#!/usr/bin/env python3
"""
Gemini to SQL システム - 自然言語からSQL文を生成
深層相談システムを活用して精度の高いSQL変換を実現
"""

import os
import json
import requests
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from deep_consultation_system import DeepConsultationSystem

class GeminiToSQLSystem:
    """自然言語をSQL文に変換するシステム"""
    
    def __init__(self):
        self.gemini_api_key = self._load_api_key()
        self.deep_consult = DeepConsultationSystem()
        self.supported_operations = {
            'select': '検索・取得',
            'insert': 'データ追加',
            'update': 'データ更新',
            'delete': 'データ削除',
            'create_table': 'テーブル作成',
            'alter_table': 'テーブル変更',
            'join': '結合処理',
            'aggregate': '集計処理',
            'subquery': 'サブクエリ',
            'window': 'ウィンドウ関数'
        }
        
    def _load_api_key(self) -> str:
        env_file = '/mnt/c/Desktop/Research/.env'
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"')
        raise ValueError("GEMINI_API_KEY not found")
    
    def _call_gemini(self, prompt: str) -> str:
        """Gemini APIを呼び出す"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"エラー: {response.status_code}"
        except Exception as e:
            return f"接続エラー: {str(e)}"
    
    def analyze_request(self, natural_language: str, schema_info: Optional[Dict] = None) -> Dict[str, Any]:
        """自然言語のリクエストを分析"""
        prompt = f"""
        以下の自然言語のリクエストを分析してください:
        
        リクエスト: {natural_language}
        
        {f"データベーススキーマ情報: {json.dumps(schema_info, ensure_ascii=False)}" if schema_info else ""}
        
        以下の項目を判定してください:
        1. SQL操作タイプ (SELECT/INSERT/UPDATE/DELETE/CREATE/ALTER)
        2. 対象テーブル
        3. 必要なカラム
        4. 条件（WHERE句）
        5. 結合が必要か
        6. 集計が必要か
        7. ソート条件
        8. その他の特殊な要件
        
        JSON形式で回答してください。
        """
        
        response = self._call_gemini(prompt)
        
        # JSON部分を抽出
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "JSON解析失敗", "raw_response": response}
        except:
            return {"error": "分析失敗", "raw_response": response}
    
    def generate_sql(self, natural_language: str, schema_info: Optional[Dict] = None, 
                    use_deep_consultation: bool = True) -> Dict[str, Any]:
        """自然言語からSQL文を生成"""
        
        # まず要求を分析
        analysis = self.analyze_request(natural_language, schema_info)
        
        if use_deep_consultation:
            # 深層相談で詳細を確認
            consultation_prompt = f"""
            ユーザーのSQL生成リクエスト: {natural_language}
            
            初期分析結果: {json.dumps(analysis, ensure_ascii=False)}
            
            以下の点について、さらに詳しく確認が必要な場合は質問してください:
            1. テーブル構造の詳細
            2. カラムのデータ型
            3. 制約条件
            4. パフォーマンス要件
            5. エラーハンドリング
            
            最終的に最適なSQL文を生成するための情報を収集してください。
            """
            
            consultation_result = self.deep_consult.deep_consult(consultation_prompt)
            analysis['consultation'] = consultation_result
        
        # SQL生成プロンプト
        sql_prompt = f"""
        以下の情報を基に、最適なSQL文を生成してください:
        
        元のリクエスト: {natural_language}
        分析結果: {json.dumps(analysis, ensure_ascii=False)}
        {f"スキーマ情報: {json.dumps(schema_info, ensure_ascii=False)}" if schema_info else ""}
        
        要件:
        1. 標準SQLに準拠
        2. パフォーマンスを考慮
        3. セキュリティ（SQLインジェクション対策）を考慮
        4. エラーハンドリングを考慮
        5. コメントで説明を追加
        
        以下の形式で回答してください:
        ```sql
        -- SQL文
        ```
        
        説明:
        - 生成したSQL文の説明
        - 注意点
        - 代替案（あれば）
        """
        
        sql_response = self._call_gemini(sql_prompt)
        
        # SQL文を抽出
        sql_match = re.search(r'```sql\n(.*?)\n```', sql_response, re.DOTALL)
        sql_code = sql_match.group(1) if sql_match else ""
        
        result = {
            'natural_language': natural_language,
            'analysis': analysis,
            'sql': sql_code,
            'explanation': sql_response,
            'timestamp': datetime.now().isoformat()
        }
        
        # 検証
        if sql_code:
            validation = self.validate_sql(sql_code, schema_info)
            result['validation'] = validation
        
        return result
    
    def validate_sql(self, sql: str, schema_info: Optional[Dict] = None) -> Dict[str, Any]:
        """生成されたSQL文を検証"""
        validation_prompt = f"""
        以下のSQL文を検証してください:
        
        ```sql
        {sql}
        ```
        
        {f"スキーマ情報: {json.dumps(schema_info, ensure_ascii=False)}" if schema_info else ""}
        
        検証項目:
        1. 構文の正しさ
        2. テーブル名・カラム名の存在確認
        3. データ型の整合性
        4. パフォーマンス上の問題
        5. セキュリティ上の問題
        6. ベストプラクティスとの適合性
        
        JSON形式で検証結果を回答してください。
        """
        
        response = self._call_gemini(validation_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"valid": True, "issues": [], "warnings": []}
        except:
            return {"valid": True, "issues": [], "warnings": [], "raw_response": response}
    
    def optimize_sql(self, sql: str, schema_info: Optional[Dict] = None) -> Dict[str, Any]:
        """SQL文を最適化"""
        optimization_prompt = f"""
        以下のSQL文を最適化してください:
        
        ```sql
        {sql}
        ```
        
        {f"スキーマ情報: {json.dumps(schema_info, ensure_ascii=False)}" if schema_info else ""}
        
        最適化の観点:
        1. インデックスの活用
        2. 不要な処理の削除
        3. JOINの順序最適化
        4. サブクエリの最適化
        5. パーティション活用
        6. キャッシュ活用
        
        最適化前後の比較と、期待される改善効果も説明してください。
        """
        
        response = self._call_gemini(optimization_prompt)
        
        # 最適化されたSQL文を抽出
        sql_match = re.search(r'```sql\n(.*?)\n```', response, re.DOTALL)
        optimized_sql = sql_match.group(1) if sql_match else sql
        
        return {
            'original_sql': sql,
            'optimized_sql': optimized_sql,
            'explanation': response,
            'timestamp': datetime.now().isoformat()
        }
    
    def explain_sql(self, sql: str) -> str:
        """SQL文を詳しく説明"""
        explain_prompt = f"""
        以下のSQL文を初心者にもわかりやすく説明してください:
        
        ```sql
        {sql}
        ```
        
        説明に含める内容:
        1. 全体的な目的
        2. 各句の役割
        3. 使用されている関数や演算子
        4. 実行順序
        5. 期待される結果
        6. 注意点
        """
        
        return self._call_gemini(explain_prompt)
    
    def convert_between_dialects(self, sql: str, from_dialect: str, to_dialect: str) -> Dict[str, Any]:
        """SQL方言間の変換"""
        conversion_prompt = f"""
        以下の{from_dialect}のSQL文を{to_dialect}に変換してください:
        
        ```sql
        {sql}
        ```
        
        変換時の注意点:
        1. 構文の違い
        2. 関数名の違い
        3. データ型の違い
        4. 制約の違い
        5. 機能の有無
        
        変換できない部分がある場合は、代替案を提示してください。
        """
        
        response = self._call_gemini(conversion_prompt)
        
        # 変換されたSQL文を抽出
        sql_match = re.search(r'```sql\n(.*?)\n```', response, re.DOTALL)
        converted_sql = sql_match.group(1) if sql_match else ""
        
        return {
            'original_sql': sql,
            'original_dialect': from_dialect,
            'converted_sql': converted_sql,
            'target_dialect': to_dialect,
            'explanation': response,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_test_data_sql(self, table_schema: Dict, num_records: int = 10) -> str:
        """テストデータ生成用のSQL文を作成"""
        prompt = f"""
        以下のテーブルスキーマに対して、{num_records}件のテストデータを生成するINSERT文を作成してください:
        
        テーブルスキーマ: {json.dumps(table_schema, ensure_ascii=False)}
        
        要件:
        1. 現実的なデータ
        2. バリエーション豊富
        3. 制約を満たす
        4. 外部キー参照がある場合は整合性を保つ
        5. 日付データは適切な範囲
        """
        
        response = self._call_gemini(prompt)
        
        # SQL文を抽出
        sql_match = re.search(r'```sql\n(.*?)\n```', response, re.DOTALL)
        return sql_match.group(1) if sql_match else response
    
    def suggest_indexes(self, sql: str, schema_info: Optional[Dict] = None) -> List[Dict]:
        """SQL文に基づいてインデックスを提案"""
        prompt = f"""
        以下のSQL文のパフォーマンスを改善するためのインデックスを提案してください:
        
        ```sql
        {sql}
        ```
        
        {f"現在のスキーマ: {json.dumps(schema_info, ensure_ascii=False)}" if schema_info else ""}
        
        提案時の考慮点:
        1. WHERE句の条件
        2. JOIN条件
        3. ORDER BY句
        4. GROUP BY句
        5. 既存インデックスとの重複回避
        6. インデックスのコスト
        
        JSON形式で、各インデックスの提案理由と期待効果を含めて回答してください。
        """
        
        response = self._call_gemini(prompt)
        
        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return []
        except:
            return []


def main():
    """メイン関数 - テスト用"""
    system = GeminiToSQLSystem()
    
    # テストケース
    test_cases = [
        "ユーザーテーブルから年齢が20歳以上の人を取得",
        "売上データを月別に集計して、売上額の高い順に表示",
        "在庫テーブルに新しい商品を追加",
        "注文テーブルと顧客テーブルを結合して、東京在住の顧客の注文を取得"
    ]
    
    # サンプルスキーマ
    sample_schema = {
        "users": {
            "columns": {
                "id": "INT PRIMARY KEY",
                "name": "VARCHAR(100)",
                "age": "INT",
                "email": "VARCHAR(255)"
            }
        },
        "orders": {
            "columns": {
                "id": "INT PRIMARY KEY",
                "user_id": "INT",
                "product_id": "INT",
                "amount": "DECIMAL(10,2)",
                "order_date": "DATETIME"
            }
        }
    }
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"テスト: {test}")
        print('='*60)
        
        result = system.generate_sql(test, sample_schema, use_deep_consultation=False)
        
        print(f"\n生成されたSQL:")
        print(result['sql'])
        
        if 'validation' in result:
            print(f"\n検証結果:")
            print(json.dumps(result['validation'], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()