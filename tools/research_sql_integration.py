#!/usr/bin/env python3
"""
研究とSQL統合システム - Geminiと相談して設計
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from deep_consultation_system import DeepConsultationSystem
from gemini_to_sql_system import GeminiToSQLSystem

class ResearchSQLIntegrationConsultant:
    """研究とSQL統合のためのGemini相談システム"""
    
    def __init__(self):
        self.deep_consult = DeepConsultationSystem()
        self.sql_system = GeminiToSQLSystem()
        self.consultation_history = []
        
    def analyze_research_for_sql_integration(self) -> Dict[str, Any]:
        """現在の研究内容とSQL統合可能性をGeminiと相談して分析"""
        
        consultation_prompt = f"""
        現在の研究プロジェクトについて詳しく分析して、SQL機能をどのように統合できるか提案してください。

        # 現在の研究内容
        
        ## 研究テーマ
        WordNetベースの意味カテゴリ分析を用いた特化型画像分類システム
        
        ## システム構成
        - BLIP（画像キャプション生成）
        - WordNet（意味カテゴリ判定・8カテゴリ）
        - YOLOv8 + SAM（物体検出・セグメンテーション）
        - CLIP（特化型分類）
        
        ## データ構造
        - 8つの専門データセット（Person, Animal, Food, Landscape, Building, Furniture, Vehicle, Plant）
        - 実験結果データ（分類精度81.25%、16テストケース）
        - 統計分析データ（確信度、処理時間、パフォーマンス指標）
        
        ## 研究成果
        - 分類精度: 81.2%
        - 確信度改善率: +15.3%（汎用比）
        - テストケース: 16/16完了
        
        # 質問・相談内容
        
        1. この研究プロジェクトにおいて、SQLデータベースはどのような価値を提供できますか？
        
        2. 実験データ、統計分析、結果管理のためのSQL活用方法を具体的に提案してください。
        
        3. 研究の効率性と再現性を向上させるためのSQL機能はありますか？
        
        4. 機械学習研究に特化したSQL機能として、どのようなユースケースが考えられますか？
        
        5. 現在のPythonベースの研究環境とSQL機能を統合する最適な方法は何ですか？
        
        6. データ分析、可視化、レポート生成におけるSQL活用の具体的な提案をしてください。
        
        以下の観点から詳細に検討してください：
        - データ管理の効率化
        - 実験の再現性向上
        - 結果の分析・可視化
        - 研究プロセスの自動化
        - データの整合性保証
        - 協力者との共有・コラボレーション
        """
        
        print("🤔 Geminiと研究×SQL統合について相談中...")
        
        consultation_result = self.deep_consult.deep_consult(consultation_prompt)
        
        self.consultation_history.append({
            'timestamp': datetime.now().isoformat(),
            'topic': 'Research SQL Integration Analysis',
            'result': consultation_result
        })
        
        return consultation_result
    
    def generate_research_specific_sql_requirements(self) -> List[Dict[str, Any]]:
        """研究特化のSQL要件をGeminiと相談して生成"""
        
        requirements_prompt = f"""
        前回の相談結果を踏まえて、具体的な研究向けSQL機能の要件を定義してください。

        # 要件定義の観点
        
        ## データスキーマ設計
        - 実験データを格納するテーブル構造
        - 統計結果を管理するスキーマ
        - バージョン管理と実験履歴の追跡
        
        ## クエリ機能要件
        - 実験結果の分析・集計クエリ
        - 統計的検定用のクエリ
        - パフォーマンス比較分析
        - データ品質チェック
        
        ## 自動化要件
        - 実験データの自動挿入
        - 結果レポートの自動生成
        - 統計分析の自動実行
        
        ## 研究特化機能
        - 実験条件の管理
        - 結果の再現性確保
        - データ系譜追跡
        - 協力研究者との共有
        
        各要件について以下を明確にしてください：
        1. 機能概要
        2. 技術仕様
        3. 実装優先度
        4. 期待される効果
        5. 具体的なSQL例
        """
        
        print("📋 研究特化SQL要件をGeminiと相談中...")
        
        requirements_result = self.deep_consult.deep_consult(requirements_prompt)
        
        return self._parse_requirements(requirements_result)
    
    def _parse_requirements(self, requirements_result) -> List[Dict[str, Any]]:
        """要件テキストを構造化データに変換"""
        
        # 相談結果が辞書形式の場合、テキストを抽出
        if isinstance(requirements_result, dict):
            if 'final_answer' in requirements_result:
                requirements_text = requirements_result['final_answer']
            else:
                requirements_text = str(requirements_result)
        else:
            requirements_text = str(requirements_result)
        
        # 簡易的な要件抽出（実際の実装では自然言語処理を使用）
        requirements = []
        
        sections = requirements_text.split('##')
        
        for section in sections:
            if section.strip():
                lines = section.split('\n')
                title = lines[0].strip()
                content = '\n'.join(lines[1:]).strip()
                
                if title and content:
                    requirements.append({
                        'title': title,
                        'description': content,
                        'priority': 'medium',  # デフォルト
                        'status': 'proposed'
                    })
        
        return requirements
    
    def design_research_database_schema(self) -> Dict[str, Any]:
        """研究データベーススキーマをGeminiと相談して設計"""
        
        schema_prompt = f"""
        現在の画像分類研究に最適なデータベーススキーマを設計してください。

        # 管理すべきデータ
        
        ## 実験データ
        - 実験ID、実施日時、バージョン
        - 実験条件（モデル、パラメータ、データセット）
        - 入力データ（画像パス、メタデータ）
        - 予測結果（分類結果、確信度）
        - 正解ラベル、評価指標
        
        ## 統計データ
        - 分類精度、確信度統計
        - 処理時間、パフォーマンス指標
        - カテゴリ別性能、混同行列データ
        
        ## メタデータ
        - データセット情報
        - モデル情報
        - 実験設定
        - 研究者情報
        
        ## 分析結果
        - 統計検定結果
        - 比較分析結果
        - 可視化データ
        
        以下の要件を満たすスキーマを設計してください：
        1. 正規化とパフォーマンスのバランス
        2. 実験の再現性確保
        3. データの整合性保証
        4. 分析クエリの効率性
        5. 将来の拡張性
        
        DDL（CREATE TABLE文）とサンプルデータも含めて提案してください。
        """
        
        print("🗄️ 研究データベーススキーマをGeminiと相談中...")
        
        schema_result = self.deep_consult.deep_consult(schema_prompt)
        
        return {
            'consultation_result': schema_result,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_research_sql_queries(self) -> Dict[str, List[str]]:
        """研究分析用SQLクエリをGeminiと相談して生成"""
        
        queries_prompt = f"""
        研究分析に必要な具体的なSQLクエリを生成してください。

        # 必要なクエリカテゴリ
        
        ## 基本分析クエリ
        - 実験結果の基本統計
        - カテゴリ別性能分析
        - 時系列での性能推移
        
        ## 比較分析クエリ
        - 異なる実験条件の比較
        - モデル間の性能比較
        - データセット別の性能分析
        
        ## 統計検定クエリ
        - 有意差検定用データ抽出
        - 信頼区間計算
        - 効果量計算
        
        ## 品質管理クエリ
        - データ品質チェック
        - 異常値検出
        - 実験の完整性確認
        
        ## レポート生成クエリ
        - 研究成果サマリー
        - 実験プロセス追跡
        - 結果可視化用データ
        
        各クエリについて：
        1. 目的の説明
        2. 具体的なSQL文
        3. 期待される結果
        4. 使用場面
        を明確にしてください。
        """
        
        print("📊 研究分析SQLクエリをGeminiと相談中...")
        
        queries_result = self.deep_consult.deep_consult(queries_prompt)
        
        return self._parse_sql_queries(queries_result)
    
    def _parse_sql_queries(self, queries_text: str) -> Dict[str, List[str]]:
        """SQLクエリテキストを分類して抽出"""
        
        import re
        
        categories = {
            'basic_analysis': [],
            'comparison': [],
            'statistical_tests': [],
            'quality_management': [],
            'reporting': []
        }
        
        # SQL文を抽出
        sql_pattern = r'```sql\n(.*?)\n```'
        sql_matches = re.findall(sql_pattern, queries_text, re.DOTALL)
        
        # 簡易的にカテゴリに分類
        for sql in sql_matches:
            if any(word in sql.upper() for word in ['AVG', 'COUNT', 'SUM']):
                categories['basic_analysis'].append(sql)
            elif 'COMPARE' in sql.upper() or 'BETWEEN' in sql.upper():
                categories['comparison'].append(sql)
            elif 'STDDEV' in sql.upper() or 'VARIANCE' in sql.upper():
                categories['statistical_tests'].append(sql)
            elif 'CHECK' in sql.upper() or 'VALIDATE' in sql.upper():
                categories['quality_management'].append(sql)
            else:
                categories['reporting'].append(sql)
        
        return categories
    
    def create_integration_plan(self) -> Dict[str, Any]:
        """統合実装計画をGeminiと相談して作成"""
        
        plan_prompt = f"""
        これまでの相談結果を踏まえて、研究環境にSQL機能を統合する具体的な実装計画を作成してください。

        # 実装計画の要素
        
        ## フェーズ1: 基盤構築
        - データベース設計・構築
        - 基本的なデータ挿入機能
        - 簡単な分析クエリ
        
        ## フェーズ2: 分析機能
        - 統計分析SQL機能
        - 比較分析機能
        - 可視化連携
        
        ## フェーズ3: 自動化
        - 実験データ自動収集
        - レポート自動生成
        - アラート機能
        
        ## フェーズ4: 高度機能
        - 機械学習モデル性能監視
        - 予測分析
        - 協力者との共有機能
        
        各フェーズについて：
        1. 実装内容の詳細
        2. 必要な技術・ツール
        3. 想定期間
        4. 成功指標
        5. リスクと対策
        
        また、現在のPython研究環境との統合方法も具体的に提案してください。
        """
        
        print("🚀 統合実装計画をGeminiと相談中...")
        
        plan_result = self.deep_consult.deep_consult(plan_prompt)
        
        return {
            'integration_plan': plan_result,
            'consultation_history': self.consultation_history,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_consultation_results(self, filename: Optional[str] = None) -> str:
        """相談結果を保存"""
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'research_sql_consultation_{timestamp}.json'
        
        results = {
            'consultation_history': self.consultation_history,
            'timestamp': datetime.now().isoformat(),
            'summary': 'Research SQL integration consultation results'
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return filename


def main():
    """メイン実行関数"""
    
    print("🔬 研究×SQL統合相談システム")
    print("=" * 60)
    
    consultant = ResearchSQLIntegrationConsultant()
    
    # ステップ1: 統合可能性分析
    print("\n📋 ステップ1: 研究×SQL統合可能性の分析")
    integration_analysis = consultant.analyze_research_for_sql_integration()
    print("✅ 分析完了")
    
    # ステップ2: 要件定義
    print("\n📋 ステップ2: 研究特化SQL要件の定義")
    requirements = consultant.generate_research_specific_sql_requirements()
    print(f"✅ {len(requirements)}個の要件を定義")
    
    # ステップ3: スキーマ設計
    print("\n📋 ステップ3: データベーススキーマの設計")
    schema_design = consultant.design_research_database_schema()
    print("✅ スキーマ設計完了")
    
    # ステップ4: クエリ生成
    print("\n📋 ステップ4: 研究分析SQLクエリの生成")
    sql_queries = consultant.generate_research_sql_queries()
    print("✅ クエリ生成完了")
    
    # ステップ5: 統合計画
    print("\n📋 ステップ5: 統合実装計画の作成")
    integration_plan = consultant.create_integration_plan()
    print("✅ 実装計画完了")
    
    # 結果保存
    print("\n💾 相談結果を保存中...")
    saved_file = consultant.save_consultation_results()
    print(f"✅ 相談結果を {saved_file} に保存")
    
    print("\n🎉 研究×SQL統合相談が完了しました！")
    print(f"📄 詳細な相談結果は {saved_file} をご確認ください。")


if __name__ == "__main__":
    main()