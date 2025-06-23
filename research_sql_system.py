#!/usr/bin/env python3
"""
研究特化SQL システム - 画像分類研究に最適化されたSQL機能
Gemini相談結果を基に設計・実装
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from gemini_to_sql_system import GeminiToSQLSystem

class ResearchSQLSystem:
    """研究特化SQLシステム"""
    
    def __init__(self, db_path: str = "research_database.db"):
        self.db_path = db_path
        self.base_sql = GeminiToSQLSystem()
        self.conn = None
        self._init_database()
        
    def _init_database(self):
        """研究データベースを初期化"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能
        
        # 研究用テーブルを作成
        self._create_research_tables()
        
    def _create_research_tables(self):
        """研究用テーブルスキーマを作成"""
        
        cursor = self.conn.cursor()
        
        # 実験テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id TEXT PRIMARY KEY,
            experiment_name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            researcher TEXT,
            model_version TEXT,
            dataset_version TEXT,
            parameters TEXT,  -- JSON形式でパラメータ保存
            status TEXT DEFAULT 'running',
            completion_time DATETIME
        )
        """)
        
        # カテゴリテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL,
            wordnet_synset TEXT,
            specialized_dataset TEXT,
            description TEXT
        )
        """)
        
        # 画像データテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id TEXT PRIMARY KEY,
            image_path TEXT NOT NULL,
            true_category_id INTEGER,
            metadata TEXT,  -- JSON形式でメタデータ
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (true_category_id) REFERENCES categories (category_id)
        )
        """)
        
        # 予測結果テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT,
            image_id TEXT,
            predicted_category_id INTEGER,
            confidence_score REAL,
            processing_time REAL,
            prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_output TEXT,  -- JSON形式で詳細な出力
            FOREIGN KEY (experiment_id) REFERENCES experiments (experiment_id),
            FOREIGN KEY (image_id) REFERENCES images (image_id),
            FOREIGN KEY (predicted_category_id) REFERENCES categories (category_id)
        )
        """)
        
        # 統計結果テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiment_statistics (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT,
            metric_name TEXT,
            metric_value REAL,
            category_id INTEGER,  -- カテゴリ別統計の場合
            calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            calculation_details TEXT,  -- JSON形式で計算詳細
            FOREIGN KEY (experiment_id) REFERENCES experiments (experiment_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
        """)
        
        # パフォーマンス監視テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            accuracy REAL,
            precision_macro REAL,
            recall_macro REAL,
            f1_score_macro REAL,
            processing_speed REAL,  -- images per second
            memory_usage REAL,  -- MB
            FOREIGN KEY (experiment_id) REFERENCES experiments (experiment_id)
        )
        """)
        
        # 比較分析テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiment_comparisons (
            comparison_id INTEGER PRIMARY KEY AUTOINCREMENT,
            comparison_name TEXT,
            experiment_ids TEXT,  -- JSON配列
            comparison_metrics TEXT,  -- JSON形式
            statistical_significance TEXT,  -- JSON形式
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            researcher_notes TEXT
        )
        """)
        
        self.conn.commit()
        
        # 初期カテゴリデータを挿入
        self._insert_default_categories()
        
    def _insert_default_categories(self):
        """デフォルトカテゴリを挿入"""
        
        categories = [
            ('Person', 'person.n.01', 'LFW', '人物・顔認識特化'),
            ('Animal', 'animal.n.01', 'ImageNet', '動物分類・行動認識特化'),
            ('Food', 'food.n.01', 'Food-101', '料理・食材認識特化'),
            ('Landscape', 'landscape.n.01', 'Places365', 'シーン・環境認識特化'),
            ('Building', 'building.n.01', 'OpenBuildings', '建築物・構造物認識特化'),
            ('Furniture', 'furniture.n.01', 'Objects365', '家具・日用品認識特化'),
            ('Vehicle', 'vehicle.n.01', 'Pascal VOC', '車両・交通手段認識特化'),
            ('Plant', 'plant.n.01', 'PlantVillage', '植物・農作物認識特化')
        ]
        
        cursor = self.conn.cursor()
        
        for cat_name, synset, dataset, desc in categories:
            cursor.execute("""
            INSERT OR IGNORE INTO categories 
            (category_name, wordnet_synset, specialized_dataset, description)
            VALUES (?, ?, ?, ?)
            """, (cat_name, synset, dataset, desc))
        
        self.conn.commit()
    
    def generate_research_query(self, natural_request: str) -> Dict[str, Any]:
        """研究向けの自然言語からSQL生成"""
        
        # 研究特化コンテキストを追加
        research_context = {
            "experiments": {
                "columns": {
                    "experiment_id": "TEXT PRIMARY KEY",
                    "experiment_name": "TEXT",
                    "researcher": "TEXT",
                    "model_version": "TEXT",
                    "accuracy": "REAL via experiment_statistics",
                    "created_at": "DATETIME"
                }
            },
            "predictions": {
                "columns": {
                    "prediction_id": "INTEGER PRIMARY KEY",
                    "experiment_id": "TEXT",
                    "image_id": "TEXT",
                    "predicted_category_id": "INTEGER",
                    "confidence_score": "REAL",
                    "processing_time": "REAL"
                }
            },
            "categories": {
                "columns": {
                    "category_id": "INTEGER PRIMARY KEY",
                    "category_name": "TEXT",
                    "specialized_dataset": "TEXT"
                }
            }
        }
        
        # 研究特化プロンプトを追加
        enhanced_request = f"""
        研究データベース用のSQL文を生成してください。
        
        研究コンテキスト:
        - 画像分類研究プロジェクト
        - 8つの専門カテゴリ（Person, Animal, Food, etc.）
        - 実験結果の管理と分析
        - 統計的検定とパフォーマンス評価
        
        ユーザーリクエスト: {natural_request}
        
        利用可能なテーブル:
        - experiments: 実験管理
        - predictions: 予測結果
        - categories: カテゴリ管理
        - experiment_statistics: 統計結果
        - performance_metrics: パフォーマンス指標
        - experiment_comparisons: 実験比較
        
        研究分析に適したSQL文を生成してください。
        """
        
        return self.base_sql.generate_sql(enhanced_request, research_context)
    
    def insert_experiment_data(self, experiment_data: Dict) -> str:
        """実験データを挿入"""
        
        cursor = self.conn.cursor()
        
        experiment_id = experiment_data.get('experiment_id', 
                                          f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        cursor.execute("""
        INSERT INTO experiments 
        (experiment_id, experiment_name, description, researcher, 
         model_version, dataset_version, parameters)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            experiment_id,
            experiment_data.get('experiment_name', ''),
            experiment_data.get('description', ''),
            experiment_data.get('researcher', ''),
            experiment_data.get('model_version', ''),
            experiment_data.get('dataset_version', ''),
            json.dumps(experiment_data.get('parameters', {}))
        ))
        
        self.conn.commit()
        return experiment_id
    
    def insert_prediction_batch(self, experiment_id: str, predictions: List[Dict]) -> int:
        """予測結果をバッチ挿入"""
        
        cursor = self.conn.cursor()
        
        prediction_data = []
        for pred in predictions:
            prediction_data.append((
                experiment_id,
                pred['image_id'],
                pred['predicted_category_id'],
                pred['confidence_score'],
                pred.get('processing_time', 0.0),
                json.dumps(pred.get('model_output', {}))
            ))
        
        cursor.executemany("""
        INSERT INTO predictions 
        (experiment_id, image_id, predicted_category_id, 
         confidence_score, processing_time, model_output)
        VALUES (?, ?, ?, ?, ?, ?)
        """, prediction_data)
        
        self.conn.commit()
        return len(predictions)
    
    def calculate_experiment_statistics(self, experiment_id: str) -> Dict[str, Any]:
        """実験統計を計算してDBに保存"""
        
        cursor = self.conn.cursor()
        
        # 基本統計を計算
        cursor.execute("""
        SELECT 
            COUNT(*) as total_predictions,
            AVG(confidence_score) as avg_confidence,
            COUNT(CASE WHEN p.predicted_category_id = i.true_category_id THEN 1 END) as correct_predictions
        FROM predictions p
        JOIN images i ON p.image_id = i.image_id
        WHERE p.experiment_id = ?
        """, (experiment_id,))
        
        stats = cursor.fetchone()
        
        if stats and stats['total_predictions'] > 0:
            accuracy = stats['correct_predictions'] / stats['total_predictions']
            
            # 統計をDBに保存
            statistics = [
                ('accuracy', accuracy),
                ('avg_confidence', stats['avg_confidence']),
                ('total_predictions', stats['total_predictions']),
                ('correct_predictions', stats['correct_predictions'])
            ]
            
            for metric_name, value in statistics:
                cursor.execute("""
                INSERT INTO experiment_statistics 
                (experiment_id, metric_name, metric_value)
                VALUES (?, ?, ?)
                """, (experiment_id, metric_name, float(value)))
            
            self.conn.commit()
            
            return {
                'experiment_id': experiment_id,
                'accuracy': accuracy,
                'avg_confidence': stats['avg_confidence'],
                'total_predictions': stats['total_predictions'],
                'correct_predictions': stats['correct_predictions']
            }
        
        return {}
    
    def generate_research_report(self, experiment_id: str) -> str:
        """研究レポートを自動生成"""
        
        # 実験データを取得
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT e.*, 
               es.metric_value as accuracy
        FROM experiments e
        LEFT JOIN experiment_statistics es ON e.experiment_id = es.experiment_id 
                                           AND es.metric_name = 'accuracy'
        WHERE e.experiment_id = ?
        """, (experiment_id,))
        
        experiment = cursor.fetchone()
        
        if not experiment:
            return "実験が見つかりません。"
        
        # カテゴリ別性能を取得
        cursor.execute("""
        SELECT 
            c.category_name,
            COUNT(*) as total,
            COUNT(CASE WHEN p.predicted_category_id = i.true_category_id THEN 1 END) as correct,
            AVG(p.confidence_score) as avg_confidence
        FROM predictions p
        JOIN images i ON p.image_id = i.image_id
        JOIN categories c ON i.true_category_id = c.category_id
        WHERE p.experiment_id = ?
        GROUP BY c.category_id, c.category_name
        ORDER BY c.category_name
        """, (experiment_id,))
        
        category_stats = cursor.fetchall()
        
        # レポート生成
        report = f"""
# 実験レポート: {experiment['experiment_name']}

## 実験概要
- **実験ID**: {experiment['experiment_id']}
- **研究者**: {experiment['researcher']}
- **モデルバージョン**: {experiment['model_version']}
- **実施日時**: {experiment['created_at']}
- **説明**: {experiment['description']}

## 全体的な性能
- **分類精度**: {experiment['accuracy']:.4f} ({experiment['accuracy']*100:.2f}%)

## カテゴリ別性能

| カテゴリ | 総数 | 正解数 | 精度 | 平均確信度 |
|---------|-----|-------|------|----------|
"""
        
        for cat in category_stats:
            accuracy = cat['correct'] / cat['total'] if cat['total'] > 0 else 0
            report += f"| {cat['category_name']} | {cat['total']} | {cat['correct']} | {accuracy:.4f} | {cat['avg_confidence']:.4f} |\n"
        
        report += f"""
## 統計的分析

生成日時: {datetime.now().isoformat()}
"""
        
        return report
    
    def compare_experiments(self, experiment_ids: List[str], 
                          comparison_name: str = "") -> Dict[str, Any]:
        """実験間の比較分析"""
        
        cursor = self.conn.cursor()
        
        comparison_results = {}
        
        for exp_id in experiment_ids:
            cursor.execute("""
            SELECT 
                e.experiment_name,
                es_acc.metric_value as accuracy,
                es_conf.metric_value as avg_confidence,
                es_total.metric_value as total_predictions
            FROM experiments e
            LEFT JOIN experiment_statistics es_acc ON e.experiment_id = es_acc.experiment_id 
                                                   AND es_acc.metric_name = 'accuracy'
            LEFT JOIN experiment_statistics es_conf ON e.experiment_id = es_conf.experiment_id 
                                                    AND es_conf.metric_name = 'avg_confidence'
            LEFT JOIN experiment_statistics es_total ON e.experiment_id = es_total.experiment_id 
                                                     AND es_total.metric_name = 'total_predictions'
            WHERE e.experiment_id = ?
            """, (exp_id,))
            
            result = cursor.fetchone()
            if result:
                comparison_results[exp_id] = {
                    'name': result['experiment_name'],
                    'accuracy': result['accuracy'] or 0,
                    'avg_confidence': result['avg_confidence'] or 0,
                    'total_predictions': result['total_predictions'] or 0
                }
        
        # 比較結果をDBに保存
        comparison_data = {
            'comparison_name': comparison_name or f"Comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'experiment_ids': experiment_ids,
            'results': comparison_results,
            'best_accuracy': max([r['accuracy'] for r in comparison_results.values()]),
            'worst_accuracy': min([r['accuracy'] for r in comparison_results.values()])
        }
        
        cursor.execute("""
        INSERT INTO experiment_comparisons 
        (comparison_name, experiment_ids, comparison_metrics)
        VALUES (?, ?, ?)
        """, (
            comparison_data['comparison_name'],
            json.dumps(experiment_ids),
            json.dumps(comparison_data)
        ))
        
        self.conn.commit()
        
        return comparison_data
    
    def export_experiment_data(self, experiment_id: str, format: str = 'json') -> str:
        """実験データをエクスポート"""
        
        cursor = self.conn.cursor()
        
        # 実験の全データを取得
        cursor.execute("""
        SELECT 
            e.*,
            GROUP_CONCAT(es.metric_name || ':' || es.metric_value) as statistics
        FROM experiments e
        LEFT JOIN experiment_statistics es ON e.experiment_id = es.experiment_id
        WHERE e.experiment_id = ?
        GROUP BY e.experiment_id
        """, (experiment_id,))
        
        experiment_data = cursor.fetchone()
        
        if not experiment_data:
            return "実験が見つかりません。"
        
        # 予測データを取得
        cursor.execute("""
        SELECT p.*, i.image_path, c.category_name as predicted_category
        FROM predictions p
        JOIN images i ON p.image_id = i.image_id
        JOIN categories c ON p.predicted_category_id = c.category_id
        WHERE p.experiment_id = ?
        ORDER BY p.prediction_timestamp
        """, (experiment_id,))
        
        predictions = cursor.fetchall()
        
        export_data = {
            'experiment': dict(experiment_data),
            'predictions': [dict(row) for row in predictions],
            'export_timestamp': datetime.now().isoformat()
        }
        
        if format.lower() == 'json':
            filename = f"experiment_{experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            return filename
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def close(self):
        """データベース接続を閉じる"""
        if self.conn:
            self.conn.close()


def demo_research_sql():
    """研究SQL機能のデモンストレーション"""
    
    print("🔬 研究特化SQL システム デモ")
    print("=" * 60)
    
    # システム初期化
    research_sql = ResearchSQLSystem("demo_research.db")
    
    # 1. サンプル実験データを挿入
    print("\n📝 サンプル実験データを作成中...")
    
    experiment_data = {
        'experiment_name': 'WordNet特化分類実験v1.0',
        'description': '8カテゴリ特化データセットを使用した分類性能評価',
        'researcher': 'Research Team',
        'model_version': 'CLIP-ViT-B/32',
        'dataset_version': 'Multi-Dataset-v1.0',
        'parameters': {
            'batch_size': 32,
            'learning_rate': 0.001,
            'epochs': 50
        }
    }
    
    exp_id = research_sql.insert_experiment_data(experiment_data)
    print(f"✅ 実験ID: {exp_id}")
    
    # 2. サンプル予測結果を挿入
    print("\n📊 サンプル予測結果を挿入中...")
    
    sample_predictions = [
        {'image_id': 'img_001', 'predicted_category_id': 1, 'confidence_score': 0.95, 'processing_time': 0.12},
        {'image_id': 'img_002', 'predicted_category_id': 2, 'confidence_score': 0.88, 'processing_time': 0.11},
        {'image_id': 'img_003', 'predicted_category_id': 1, 'confidence_score': 0.76, 'processing_time': 0.13},
        {'image_id': 'img_004', 'predicted_category_id': 3, 'confidence_score': 0.92, 'processing_time': 0.10},
        {'image_id': 'img_005', 'predicted_category_id': 2, 'confidence_score': 0.84, 'processing_time': 0.14},
    ]
    
    # サンプル画像データも挿入
    cursor = research_sql.conn.cursor()
    for i, pred in enumerate(sample_predictions, 1):
        cursor.execute("""
        INSERT OR IGNORE INTO images (image_id, image_path, true_category_id)
        VALUES (?, ?, ?)
        """, (pred['image_id'], f"/data/images/{pred['image_id']}.jpg", pred['predicted_category_id']))
    
    research_sql.conn.commit()
    
    inserted = research_sql.insert_prediction_batch(exp_id, sample_predictions)
    print(f"✅ {inserted}件の予測結果を挿入")
    
    # 3. 統計計算
    print("\n📈 実験統計を計算中...")
    stats = research_sql.calculate_experiment_statistics(exp_id)
    print(f"✅ 分類精度: {stats.get('accuracy', 0):.4f}")
    
    # 4. 自然言語からSQL生成のテスト
    print("\n🤖 自然言語SQL生成テスト:")
    
    test_queries = [
        "この実験の分類精度を取得",
        "カテゴリ別の性能を分析",
        "処理時間の統計を計算",
        "確信度が0.9以上の予測を取得"
    ]
    
    for query in test_queries:
        print(f"\n質問: {query}")
        result = research_sql.generate_research_query(query)
        if result.get('sql'):
            print(f"SQL: {result['sql'][:100]}...")
    
    # 5. レポート生成
    print("\n📄 実験レポート生成中...")
    report = research_sql.generate_research_report(exp_id)
    print(report[:500] + "...")
    
    # 6. データエクスポート
    print("\n💾 実験データエクスポート中...")
    exported_file = research_sql.export_experiment_data(exp_id)
    print(f"✅ エクスポート完了: {exported_file}")
    
    # クリーンアップ
    research_sql.close()
    
    print("\n🎉 研究SQL機能デモ完了！")


if __name__ == "__main__":
    demo_research_sql()