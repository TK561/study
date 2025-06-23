#!/usr/bin/env python3
"""
高度なGemini SQL機能 - より複雑なSQL操作をサポート
"""

import os
import json
import sqlite3
from typing import Dict, List, Tuple, Optional, Any, Union
from gemini_to_sql_system import GeminiToSQLSystem
from datetime import datetime, timedelta

class AdvancedGeminiSQLFeatures:
    """高度なSQL機能を提供するクラス"""
    
    def __init__(self):
        self.base_system = GeminiToSQLSystem()
        self.query_history = []
        self.performance_stats = {}
        
    def generate_complex_query(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """複雑なクエリを生成"""
        
        prompt = f"""
        以下の要件に基づいて、複雑なSQL文を生成してください:
        
        要件:
        - メインテーブル: {requirements.get('main_table')}
        - 結合テーブル: {requirements.get('join_tables', [])}
        - 集計関数: {requirements.get('aggregations', [])}
        - ウィンドウ関数: {requirements.get('window_functions', [])}
        - CTE（共通テーブル式）: {requirements.get('use_cte', False)}
        - 条件: {requirements.get('conditions', [])}
        - グループ化: {requirements.get('group_by', [])}
        - 並び順: {requirements.get('order_by', [])}
        - 制限: {requirements.get('limit')}
        
        高度な機能を積極的に使用してください:
        1. WITH句を使った可読性の向上
        2. ウィンドウ関数による高度な分析
        3. CASE文による条件分岐
        4. サブクエリの最適な配置
        5. 効率的なインデックス活用
        """
        
        response = self.base_system._call_gemini(prompt)
        
        # SQL文を抽出
        import re
        sql_match = re.search(r'```sql\n(.*?)\n```', response, re.DOTALL)
        sql_code = sql_match.group(1) if sql_match else ""
        
        result = {
            'requirements': requirements,
            'sql': sql_code,
            'explanation': response,
            'complexity_score': self._calculate_complexity(sql_code),
            'estimated_performance': self._estimate_performance(sql_code),
            'timestamp': datetime.now().isoformat()
        }
        
        self.query_history.append(result)
        return result
    
    def _calculate_complexity(self, sql: str) -> int:
        """SQLの複雑度を計算"""
        complexity = 0
        
        # 各要素の複雑度を加算
        complexity_factors = {
            'JOIN': 2,
            'LEFT JOIN': 3,
            'RIGHT JOIN': 3,
            'FULL JOIN': 4,
            'UNION': 3,
            'WITH': 3,
            'OVER': 4,
            'PARTITION BY': 3,
            'CASE': 2,
            'EXISTS': 3,
            'IN (SELECT': 3,
            'GROUP BY': 2,
            'HAVING': 2
        }
        
        sql_upper = sql.upper()
        for factor, score in complexity_factors.items():
            complexity += sql_upper.count(factor) * score
        
        return complexity
    
    def _estimate_performance(self, sql: str) -> Dict[str, Any]:
        """パフォーマンスを推定"""
        performance = {
            'estimated_rows': 'unknown',
            'index_usage': [],
            'potential_issues': [],
            'optimization_suggestions': []
        }
        
        # 簡易的な分析
        sql_upper = sql.upper()
        
        if 'SELECT *' in sql_upper:
            performance['potential_issues'].append('SELECT * は避けるべき')
            performance['optimization_suggestions'].append('必要なカラムのみを選択')
        
        if sql_upper.count('JOIN') > 3:
            performance['potential_issues'].append('多数のJOINがパフォーマンスに影響する可能性')
            performance['optimization_suggestions'].append('CTEやサブクエリでの段階的な処理を検討')
        
        if 'LIKE \'%' in sql_upper:
            performance['potential_issues'].append('前方一致でないLIKEはインデックスを使用できない')
            performance['optimization_suggestions'].append('全文検索インデックスの使用を検討')
        
        return performance
    
    def generate_migration_sql(self, from_schema: Dict, to_schema: Dict) -> List[str]:
        """スキーマ移行用のSQL文を生成"""
        
        prompt = f"""
        以下のスキーマ変更に必要なSQL文を生成してください:
        
        現在のスキーマ:
        {json.dumps(from_schema, ensure_ascii=False, indent=2)}
        
        目標スキーマ:
        {json.dumps(to_schema, ensure_ascii=False, indent=2)}
        
        以下を考慮してください:
        1. データの保持
        2. 外部キー制約の一時的な無効化と再有効化
        3. インデックスの再作成
        4. トリガーの再作成
        5. ロールバック可能な構造
        
        各ステップを個別のSQL文として、順序を考慮して出力してください。
        """
        
        response = self.base_system._call_gemini(prompt)
        
        # 複数のSQL文を抽出
        import re
        sql_statements = re.findall(r'```sql\n(.*?)\n```', response, re.DOTALL)
        
        return sql_statements if sql_statements else [response]
    
    def generate_stored_procedure(self, procedure_name: str, 
                                description: str, 
                                parameters: List[Dict],
                                logic: str) -> str:
        """ストアドプロシージャを生成"""
        
        prompt = f"""
        以下の仕様でストアドプロシージャを生成してください:
        
        プロシージャ名: {procedure_name}
        説明: {description}
        
        パラメータ:
        {json.dumps(parameters, ensure_ascii=False, indent=2)}
        
        処理内容:
        {logic}
        
        要件:
        1. エラーハンドリング
        2. トランザクション管理
        3. ログ出力
        4. パラメータ検証
        5. 戻り値の適切な設定
        
        MySQL、PostgreSQL、SQL Serverの3つの方言で生成してください。
        """
        
        return self.base_system._call_gemini(prompt)
    
    def analyze_query_plan(self, sql: str, actual_data: Optional[Dict] = None) -> Dict[str, Any]:
        """クエリ実行計画を分析"""
        
        prompt = f"""
        以下のSQL文の実行計画を分析してください:
        
        ```sql
        {sql}
        ```
        
        分析項目:
        1. 予想される実行順序
        2. インデックス使用状況
        3. テーブルスキャン vs インデックススキャン
        4. 結合アルゴリズム（Nested Loop/Hash/Merge）
        5. メモリ使用量の推定
        6. 最適化の提案
        
        {f"実データサンプルも考慮してください" if actual_data is not None else ""}
        """
        
        analysis = self.base_system._call_gemini(prompt)
        
        return {
            'sql': sql,
            'analysis': analysis,
            'optimization_suggestions': self._extract_optimizations(analysis),
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_optimizations(self, analysis: str) -> List[str]:
        """分析結果から最適化提案を抽出"""
        suggestions = []
        
        lines = analysis.split('\n')
        in_suggestions = False
        
        for line in lines:
            if '最適化' in line or '提案' in line or 'suggest' in line.lower():
                in_suggestions = True
                continue
            
            if in_suggestions and line.strip() and line.strip()[0].isdigit():
                suggestions.append(line.strip())
        
        return suggestions
    
    def generate_data_warehouse_etl(self, source_tables: List[str], 
                                  target_schema: str,
                                  transformations: List[Dict]) -> Dict[str, Any]:
        """データウェアハウス用のETL処理を生成"""
        
        prompt = f"""
        以下の要件でETL（Extract, Transform, Load）処理を生成してください:
        
        ソーステーブル: {source_tables}
        ターゲットスキーマ: {target_schema}
        
        変換処理:
        {json.dumps(transformations, ensure_ascii=False, indent=2)}
        
        要件:
        1. 増分更新対応（CDC - Change Data Capture）
        2. エラーレコードの隔離
        3. 監査ログ
        4. パフォーマンス最適化
        5. 冪等性の保証
        
        以下を生成してください:
        - 抽出クエリ
        - 変換処理
        - ロード処理
        - エラーハンドリング
        - メタデータ更新
        """
        
        response = self.base_system._call_gemini(prompt)
        
        return {
            'source_tables': source_tables,
            'target_schema': target_schema,
            'transformations': transformations,
            'etl_sql': response,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_time_series_analysis(self, table_name: str,
                                    date_column: str,
                                    value_column: str,
                                    analysis_type: str) -> str:
        """時系列分析用のSQL文を生成"""
        
        analysis_types = {
            'moving_average': '移動平均',
            'year_over_year': '前年同期比',
            'cumulative': '累積',
            'lag_lead': '前後期間比較',
            'seasonality': '季節性分析',
            'trend': 'トレンド分析'
        }
        
        prompt = f"""
        以下の時系列分析を行うSQL文を生成してください:
        
        テーブル: {table_name}
        日付カラム: {date_column}
        値カラム: {value_column}
        分析タイプ: {analysis_types.get(analysis_type, analysis_type)}
        
        高度なウィンドウ関数を使用して、以下を含めてください:
        1. 基本的な集計
        2. 期間比較
        3. ランキング
        4. パーセンタイル
        5. 外れ値検出
        
        可視化しやすい形式で結果を出力してください。
        """
        
        return self.base_system._call_gemini(prompt)
    
    def generate_data_quality_checks(self, table_name: str, 
                                   columns: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """データ品質チェック用のSQL文を生成"""
        
        prompt = f"""
        以下のテーブルに対するデータ品質チェックSQL文を生成してください:
        
        テーブル: {table_name}
        カラム情報:
        {json.dumps(columns, ensure_ascii=False, indent=2)}
        
        チェック項目:
        1. NULL値の検出
        2. 重複レコードの検出
        3. 外れ値の検出
        4. データ型の不整合
        5. 参照整合性
        6. ビジネスルール違反
        7. 文字列パターンの異常
        8. 日付の論理的整合性
        
        各チェックを個別のクエリとして、問題のあるレコードを特定できる形で出力してください。
        """
        
        response = self.base_system._call_gemini(prompt)
        
        # 複数のチェッククエリを抽出
        import re
        checks = []
        
        # SQL文とその説明を抽出
        sql_blocks = re.findall(r'-- (.*?)\n```sql\n(.*?)\n```', response, re.DOTALL)
        
        for description, sql in sql_blocks:
            checks.append({
                'description': description.strip(),
                'sql': sql.strip(),
                'severity': 'warning'  # デフォルト
            })
        
        return checks
    
    def generate_permission_management(self, database: str, 
                                     roles: List[Dict[str, Any]]) -> List[str]:
        """権限管理用のSQL文を生成"""
        
        prompt = f"""
        以下の要件で権限管理SQL文を生成してください:
        
        データベース: {database}
        ロール定義:
        {json.dumps(roles, ensure_ascii=False, indent=2)}
        
        生成内容:
        1. ロールの作成
        2. 権限の付与
        3. ユーザーへのロール割り当て
        4. 権限の継承設定
        5. 監査設定
        
        セキュリティベストプラクティス:
        - 最小権限の原則
        - ロールベースアクセス制御（RBAC）
        - 監査ログの有効化
        - 定期的な権限レビュー用のクエリ
        """
        
        response = self.base_system._call_gemini(prompt)
        
        # SQL文を抽出
        import re
        sql_statements = re.findall(r'```sql\n(.*?)\n```', response, re.DOTALL)
        
        return sql_statements
    
    def generate_backup_restore_strategy(self, database_info: Dict) -> Dict[str, Any]:
        """バックアップ・リストア戦略を生成"""
        
        prompt = f"""
        以下のデータベースに対するバックアップ・リストア戦略を生成してください:
        
        データベース情報:
        {json.dumps(database_info, ensure_ascii=False, indent=2)}
        
        戦略に含める内容:
        1. フルバックアップSQL
        2. 増分バックアップSQL
        3. ポイントインタイムリカバリ
        4. バックアップ検証
        5. リストア手順
        6. 災害復旧計画
        
        RPO（Recovery Point Objective）とRTO（Recovery Time Objective）を考慮してください。
        """
        
        response = self.base_system._call_gemini(prompt)
        
        return {
            'database_info': database_info,
            'strategy': response,
            'scripts': self._extract_backup_scripts(response),
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_backup_scripts(self, strategy: str) -> Dict[str, str]:
        """バックアップスクリプトを抽出"""
        scripts = {}
        
        import re
        
        # 各種スクリプトを抽出
        script_patterns = {
            'full_backup': r'-- フルバックアップ.*?```(?:sql|bash)\n(.*?)```',
            'incremental_backup': r'-- 増分バックアップ.*?```(?:sql|bash)\n(.*?)```',
            'restore': r'-- リストア.*?```(?:sql|bash)\n(.*?)```',
            'verify': r'-- 検証.*?```(?:sql|bash)\n(.*?)```'
        }
        
        for script_type, pattern in script_patterns.items():
            match = re.search(pattern, strategy, re.DOTALL | re.IGNORECASE)
            if match:
                scripts[script_type] = match.group(1).strip()
        
        return scripts


def demonstrate_advanced_features():
    """高度な機能のデモンストレーション"""
    
    system = AdvancedGeminiSQLFeatures()
    
    print("=== 高度なGemini SQL機能デモ ===\n")
    
    # 1. 複雑なクエリ生成
    print("1. 複雑なクエリ生成")
    complex_requirements = {
        'main_table': 'sales',
        'join_tables': ['products', 'customers', 'regions'],
        'aggregations': ['SUM(amount)', 'AVG(amount)', 'COUNT(*)'],
        'window_functions': ['ROW_NUMBER()', 'RANK()', 'LAG()'],
        'use_cte': True,
        'conditions': ['sales_date >= 2024-01-01', 'region = "Asia"'],
        'group_by': ['product_category', 'customer_segment'],
        'order_by': ['total_sales DESC'],
        'limit': 100
    }
    
    result = system.generate_complex_query(complex_requirements)
    print(f"複雑度スコア: {result['complexity_score']}")
    print(f"生成されたSQL:\n{result['sql'][:200]}...")
    
    # 2. 時系列分析
    print("\n2. 時系列分析SQL生成")
    time_series_sql = system.generate_time_series_analysis(
        'daily_sales',
        'sale_date',
        'revenue',
        'moving_average'
    )
    print(f"時系列分析SQL:\n{time_series_sql[:200]}...")
    
    # 3. データ品質チェック
    print("\n3. データ品質チェック")
    quality_checks = system.generate_data_quality_checks(
        'customers',
        [
            {'name': 'email', 'type': 'VARCHAR', 'constraints': 'UNIQUE'},
            {'name': 'age', 'type': 'INT', 'constraints': 'CHECK (age >= 0)'},
            {'name': 'created_date', 'type': 'DATETIME', 'constraints': 'NOT NULL'}
        ]
    )
    print(f"生成されたチェック数: {len(quality_checks)}")
    
    print("\n=== デモ完了 ===")


if __name__ == "__main__":
    demonstrate_advanced_features()