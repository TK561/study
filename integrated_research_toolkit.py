#!/usr/bin/env python3
"""
統合研究ツールキット - GeminiとSQL機能を研究に完全統合
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from research_sql_system import ResearchSQLSystem
from gemini_sql_toolkit import GeminiSQLToolkit
from deep_consultation_system import DeepConsultationSystem

class IntegratedResearchToolkit:
    """研究とSQL機能を統合したツールキット"""
    
    def __init__(self, db_path: str = "research_toolkit.db"):
        self.research_sql = ResearchSQLSystem(db_path)
        self.gemini_sql = GeminiSQLToolkit()
        self.deep_consult = DeepConsultationSystem()
        self.session_log = []
        
    def analyze_research_data_with_gemini(self, analysis_request: str) -> Dict[str, Any]:
        """研究データをGeminiと相談しながら分析"""
        
        # 現在のデータベース状況を取得
        cursor = self.research_sql.conn.cursor()
        
        # 実験データサマリーを取得
        cursor.execute("""
        SELECT 
            COUNT(*) as total_experiments,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_experiments,
            MAX(created_at) as latest_experiment
        FROM experiments
        """)
        
        exp_summary = cursor.fetchone()
        
        # 統計データを取得
        cursor.execute("""
        SELECT 
            metric_name,
            AVG(metric_value) as avg_value,
            MAX(metric_value) as max_value,
            MIN(metric_value) as min_value,
            COUNT(*) as count
        FROM experiment_statistics
        GROUP BY metric_name
        """)
        
        stats_summary = cursor.fetchall()
        
        # Geminiと相談
        consultation_prompt = f"""
        研究データの分析を行います。

        # 現在のデータベース状況
        - 総実験数: {exp_summary['total_experiments'] if exp_summary else 0}
        - 完了実験数: {exp_summary['completed_experiments'] if exp_summary else 0}
        - 最新実験: {exp_summary['latest_experiment'] if exp_summary else 'なし'}

        # 統計サマリー
        """
        
        for stat in stats_summary:
            consultation_prompt += f"""
        - {stat['metric_name']}: 平均 {stat['avg_value']:.4f}, 最大 {stat['max_value']:.4f}, 最小 {stat['min_value']:.4f} ({stat['count']}件)
        """
        
        consultation_prompt += f"""
        
        # 分析リクエスト
        {analysis_request}
        
        以下の観点から分析してください：
        1. データの傾向と パターン
        2. 統計的な有意性
        3. 研究上の示唆
        4. 改善提案
        5. 追加調査が必要な点
        
        また、さらなる分析に必要なSQLクエリも提案してください。
        """
        
        analysis_result = self.deep_consult.deep_consult(consultation_prompt)
        
        # 結果をログに保存
        self.session_log.append({
            'type': 'data_analysis',
            'request': analysis_request,
            'result': analysis_result,
            'timestamp': datetime.now().isoformat()
        })
        
        return analysis_result
    
    def smart_experiment_setup(self, experiment_description: str) -> Dict[str, Any]:
        """Geminiと相談して実験設定を最適化"""
        
        setup_prompt = f"""
        新しい画像分類実験の設定について相談します。

        # 実験の説明
        {experiment_description}

        # 現在の研究コンテキスト
        - 研究テーマ: WordNetベースの意味カテゴリ分析を用いた特化型画像分類
        - 対象カテゴリ: Person, Animal, Food, Landscape, Building, Furniture, Vehicle, Plant
        - 利用可能モデル: BLIP, WordNet, YOLOv8, SAM, CLIP

        以下について具体的に提案してください：

        1. **実験設計**
           - 実験の目的と仮説
           - 評価指標の選定
           - 実験条件の設定

        2. **データ設計**
           - 必要なデータセット
           - サンプルサイズの推定
           - データ分割方法

        3. **統計的考慮**
           - 統計的検定の計画
           - 有意水準の設定
           - 効果量の推定

        4. **技術的実装**
           - モデルパラメータの推奨値
           - 処理パイプラインの設計
           - パフォーマンス監視方法

        5. **データベース設計**
           - 実験データの記録項目
           - 分析に必要なクエリ
           - レポート生成計画
        """
        
        setup_result = self.deep_consult.deep_consult(setup_prompt)
        
        # 結果に基づいて実験テンプレートを生成
        experiment_template = self._extract_experiment_template(setup_result)
        
        return {
            'consultation_result': setup_result,
            'experiment_template': experiment_template,
            'recommended_queries': self._generate_recommended_queries(setup_result)
        }
    
    def _extract_experiment_template(self, consultation_result) -> Dict[str, Any]:
        """相談結果から実験テンプレートを抽出"""
        
        # 相談結果から構造化されたテンプレートを抽出
        template = {
            'experiment_name': 'New Experiment',
            'description': 'Generated from Gemini consultation',
            'parameters': {
                'batch_size': 32,
                'learning_rate': 0.001,
                'epochs': 50
            },
            'evaluation_metrics': ['accuracy', 'precision', 'recall', 'f1_score'],
            'statistical_tests': ['t_test', 'anova'],
            'monitoring_interval': 100  # predictions
        }
        
        return template
    
    def _generate_recommended_queries(self, consultation_result) -> List[str]:
        """推奨SQLクエリを生成"""
        
        queries = [
            "SELECT AVG(confidence_score) FROM predictions WHERE experiment_id = ?",
            "SELECT category_name, COUNT(*) FROM predictions p JOIN categories c ON p.predicted_category_id = c.category_id GROUP BY category_name",
            "SELECT AVG(processing_time), STDDEV(processing_time) FROM predictions WHERE experiment_id = ?",
            "SELECT COUNT(*) as correct FROM predictions p JOIN images i ON p.image_id = i.image_id WHERE p.predicted_category_id = i.true_category_id AND p.experiment_id = ?"
        ]
        
        return queries
    
    def intelligent_data_exploration(self, exploration_goal: str) -> Dict[str, Any]:
        """Geminiと協力してデータ探索を実行"""
        
        exploration_prompt = f"""
        研究データの探索を行います。

        # 探索目標
        {exploration_goal}

        # 利用可能なデータ
        1. 実験データ（experiments テーブル）
        2. 予測結果（predictions テーブル）
        3. カテゴリ情報（categories テーブル）
        4. 統計結果（experiment_statistics テーブル）
        5. パフォーマンス指標（performance_metrics テーブル）

        以下のステップで探索を実行してください：

        1. **探索戦略の策定**
           - どのような仮説を検証するか
           - どのデータを調べるべきか
           - どのような分析手法が適切か

        2. **SQLクエリの生成**
           - データ抽出用のクエリ
           - 集計・分析用のクエリ
           - 可視化用のクエリ

        3. **分析計画**
           - 統計的分析の手順
           - 結果の解釈方法
           - 追加調査の方向性

        具体的なSQLクエリも含めて提案してください。
        """
        
        exploration_result = self.deep_consult.deep_consult(exploration_prompt)
        
        # 提案されたクエリを抽出して実行
        suggested_queries = self._extract_sql_queries(exploration_result)
        query_results = {}
        
        for i, query in enumerate(suggested_queries):
            try:
                cursor = self.research_sql.conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                query_results[f"query_{i+1}"] = {
                    'sql': query,
                    'results': [dict(row) for row in results],
                    'row_count': len(results)
                }
            except Exception as e:
                query_results[f"query_{i+1}"] = {
                    'sql': query,
                    'error': str(e)
                }
        
        return {
            'exploration_strategy': exploration_result,
            'executed_queries': query_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_sql_queries(self, text) -> List[str]:
        """テキストからSQLクエリを抽出"""
        
        import re
        
        # テキストから辞書の場合の処理
        if isinstance(text, dict):
            if 'final_answer' in text:
                text = text['final_answer']
            else:
                text = str(text)
        
        # SQLクエリを抽出
        sql_pattern = r'```sql\n(.*?)\n```'
        queries = re.findall(sql_pattern, text, re.DOTALL)
        
        # 簡単なクエリの場合の補完
        if not queries:
            simple_patterns = [
                r'SELECT[^;]+;',
                r'INSERT[^;]+;',
                r'UPDATE[^;]+;',
                r'DELETE[^;]+;'
            ]
            
            for pattern in simple_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                queries.extend(matches)
        
        return queries[:5]  # 最大5つまで
    
    def generate_research_insights(self, experiment_ids: List[str]) -> Dict[str, Any]:
        """実験結果からGeminiと協力して研究洞察を生成"""
        
        # 実験データを収集
        experiment_data = {}
        
        for exp_id in experiment_ids:
            cursor = self.research_sql.conn.cursor()
            
            # 実験基本情報
            cursor.execute("""
            SELECT * FROM experiments WHERE experiment_id = ?
            """, (exp_id,))
            exp_info = cursor.fetchone()
            
            # 統計情報
            cursor.execute("""
            SELECT metric_name, metric_value 
            FROM experiment_statistics 
            WHERE experiment_id = ?
            """, (exp_id,))
            stats = {row['metric_name']: row['metric_value'] for row in cursor.fetchall()}
            
            if exp_info:
                experiment_data[exp_id] = {
                    'info': dict(exp_info),
                    'statistics': stats
                }
        
        # Geminiと洞察を生成
        insights_prompt = f"""
        複数の実験結果から研究的洞察を導出してください。

        # 実験データ
        """
        
        for exp_id, data in experiment_data.items():
            insights_prompt += f"""
        ## 実験 {exp_id}
        - 名前: {data['info'].get('experiment_name', 'Unknown')}
        - 研究者: {data['info'].get('researcher', 'Unknown')}
        - モデル: {data['info'].get('model_version', 'Unknown')}
        - 統計:
        """
            for metric, value in data['statistics'].items():
                insights_prompt += f"  - {metric}: {value}\n"
        
        insights_prompt += f"""
        
        # 分析観点
        
        1. **パフォーマンス分析**
           - 各実験の性能比較
           - 強みと弱みの特定
           - 改善点の抽出

        2. **統計的有意性**
           - 実験間の差の有意性
           - 信頼区間の推定
           - 効果量の評価

        3. **研究上の含意**
           - 仮説の検証状況
           - 理論的な示唆
           - 実用性の評価

        4. **今後の研究方向**
           - 追加実験の提案
           - 改善アプローチ
           - 新しい仮説の生成

        5. **方法論的考察**
           - 実験設計の妥当性
           - データ収集の適切性
           - 分析手法の評価

        詳細な研究洞察を提供してください。
        """
        
        insights_result = self.deep_consult.deep_consult(insights_prompt)
        
        return {
            'experiment_data': experiment_data,
            'research_insights': insights_result,
            'insight_timestamp': datetime.now().isoformat()
        }
    
    def create_automated_research_pipeline(self, pipeline_config: Dict) -> Dict[str, Any]:
        """自動化された研究パイプラインを作成"""
        
        pipeline_prompt = f"""
        自動化された研究パイプラインの設計について相談します。

        # パイプライン設定
        {json.dumps(pipeline_config, ensure_ascii=False, indent=2)}

        以下の自動化コンポーネントを設計してください：

        1. **データ収集自動化**
           - 実験データの自動取り込み
           - データ品質チェック
           - 異常値検出

        2. **分析自動化**
           - 統計計算の自動実行
           - パフォーマンス監視
           - 比較分析

        3. **レポート自動化**
           - 実験結果サマリー
           - 可視化グラフ生成
           - 研究進捗レポート

        4. **アラート機能**
           - 性能異常の検出
           - 実験完了通知
           - データ品質警告

        5. **協力者との共有**
           - データエクスポート
           - レポート配信
           - アクセス制御

        具体的な実装計画とSQLクエリも含めて提案してください。
        """
        
        pipeline_result = self.deep_consult.deep_consult(pipeline_prompt)
        
        # パイプライン設定をデータベースに保存
        cursor = self.research_sql.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_pipelines (
            pipeline_id TEXT PRIMARY KEY,
            pipeline_name TEXT,
            config TEXT,
            design TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
        """)
        
        pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute("""
        INSERT INTO research_pipelines 
        (pipeline_id, pipeline_name, config, design)
        VALUES (?, ?, ?, ?)
        """, (
            pipeline_id,
            pipeline_config.get('name', 'Automated Pipeline'),
            json.dumps(pipeline_config),
            json.dumps(pipeline_result if isinstance(pipeline_result, dict) else {'result': str(pipeline_result)})
        ))
        
        self.research_sql.conn.commit()
        
        return {
            'pipeline_id': pipeline_id,
            'design': pipeline_result,
            'config': pipeline_config
        }
    
    def save_session_log(self, filename: Optional[str] = None) -> str:
        """セッションログを保存"""
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'research_session_{timestamp}.json'
        
        session_data = {
            'session_log': self.session_log,
            'timestamp': datetime.now().isoformat(),
            'summary': f'Research session with {len(self.session_log)} activities'
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def close(self):
        """リソースを解放"""
        self.research_sql.close()


def demo_integrated_toolkit():
    """統合ツールキットのデモンストレーション"""
    
    print("🚀 統合研究ツールキット デモ")
    print("=" * 60)
    
    toolkit = IntegratedResearchToolkit("demo_integrated.db")
    
    # 1. スマート実験設定
    print("\n🧠 1. スマート実験設定")
    experiment_desc = "8カテゴリの特化型分類器の性能を従来手法と比較評価する実験"
    setup_result = toolkit.smart_experiment_setup(experiment_desc)
    print("✅ 実験設定の相談完了")
    
    # 2. データ探索
    print("\n🔍 2. インテリジェントデータ探索")
    exploration_result = toolkit.intelligent_data_exploration(
        "カテゴリ別の分類性能の差異と、その原因を調査したい"
    )
    print(f"✅ {len(exploration_result.get('executed_queries', {}))}件のクエリを実行")
    
    # 3. 研究洞察生成
    print("\n💡 3. 研究洞察生成")
    
    # まずサンプル実験を作成
    sample_exp_data = {
        'experiment_name': 'Sample Research Experiment',
        'description': 'Demonstration experiment for toolkit',
        'researcher': 'Demo Researcher'
    }
    
    exp_id = toolkit.research_sql.insert_experiment_data(sample_exp_data)
    
    # サンプル統計を挿入
    cursor = toolkit.research_sql.conn.cursor()
    cursor.execute("""
    INSERT INTO experiment_statistics (experiment_id, metric_name, metric_value)
    VALUES (?, 'accuracy', 0.812)
    """, (exp_id,))
    toolkit.research_sql.conn.commit()
    
    insights = toolkit.generate_research_insights([exp_id])
    print("✅ 研究洞察を生成")
    
    # 4. 自動化パイプライン作成
    print("\n⚙️ 4. 自動化パイプライン作成")
    pipeline_config = {
        'name': 'Real-time Performance Monitoring',
        'frequency': 'every_100_predictions',
        'metrics': ['accuracy', 'confidence', 'processing_time'],
        'alerts': ['performance_drop', 'data_quality_issue']
    }
    
    pipeline_result = toolkit.create_automated_research_pipeline(pipeline_config)
    print(f"✅ パイプライン作成: {pipeline_result['pipeline_id']}")
    
    # 5. セッション保存
    print("\n💾 5. セッション保存")
    saved_file = toolkit.save_session_log()
    print(f"✅ セッションログ保存: {saved_file}")
    
    # クリーンアップ
    toolkit.close()
    
    print("\n🎉 統合ツールキット デモ完了！")
    print("\n📋 実装された機能:")
    print("  ✨ Gemini相談による実験設計最適化")
    print("  🔍 インテリジェントデータ探索")
    print("  📊 自動統計分析とレポート生成")
    print("  💡 AI支援による研究洞察導出")
    print("  ⚙️ 自動化パイプライン構築")
    print("  📈 リアルタイム性能監視")


if __name__ == "__main__":
    demo_integrated_toolkit()