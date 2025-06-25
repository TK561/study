#!/usr/bin/env python3
"""
シンプル研究SQL システム - Geminiなしの純粋SQL研究支援
画像分類研究データの管理・分析に特化
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

class SimpleResearchSQL:
    """Geminiなしの純粋研究SQLシステム"""
    
    def __init__(self, db_path: str = "simple_research.db"):
        self.db_path = db_path
        self.conn = None
        self._init_database()
        
    def _init_database(self):
        """研究データベースを初期化"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        
    def _create_tables(self):
        """研究用テーブルを作成"""
        
        cursor = self.conn.cursor()
        
        # 実験テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            researcher TEXT,
            model_type TEXT,
            dataset_name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'running'
        )
        """)
        
        # カテゴリテーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            dataset TEXT,
            description TEXT
        )
        """)
        
        # 画像テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id TEXT PRIMARY KEY,
            path TEXT NOT NULL,
            true_category INTEGER,
            FOREIGN KEY (true_category) REFERENCES categories (category_id)
        )
        """)
        
        # 予測結果テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT,
            image_id TEXT,
            predicted_category INTEGER,
            confidence REAL,
            processing_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (experiment_id) REFERENCES experiments (experiment_id),
            FOREIGN KEY (image_id) REFERENCES images (image_id),
            FOREIGN KEY (predicted_category) REFERENCES categories (category_id)
        )
        """)
        
        # 実験統計テーブル
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiment_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id TEXT,
            metric_name TEXT,
            value REAL,
            category_id INTEGER,
            calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (experiment_id) REFERENCES experiments (experiment_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
        """)
        
        self.conn.commit()
        self._insert_default_categories()
        
    def _insert_default_categories(self):
        """デフォルトカテゴリを挿入"""
        
        categories = [
            (1, 'Person', 'LFW', '人物・顔認識'),
            (2, 'Animal', 'ImageNet', '動物分類'),
            (3, 'Food', 'Food-101', '料理・食材認識'),
            (4, 'Landscape', 'Places365', 'シーン・環境認識'),
            (5, 'Building', 'OpenBuildings', '建築物認識'),
            (6, 'Furniture', 'Objects365', '家具・日用品認識'),
            (7, 'Vehicle', 'Pascal VOC', '車両認識'),
            (8, 'Plant', 'PlantVillage', '植物認識')
        ]
        
        cursor = self.conn.cursor()
        for cat_id, name, dataset, desc in categories:
            cursor.execute("""
            INSERT OR IGNORE INTO categories (category_id, name, dataset, description)
            VALUES (?, ?, ?, ?)
            """, (cat_id, name, dataset, desc))
        
        self.conn.commit()
    
    def create_experiment(self, name: str, description: str = "", 
                         researcher: str = "", model_type: str = "", 
                         dataset_name: str = "") -> str:
        """新しい実験を作成"""
        
        experiment_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO experiments (experiment_id, name, description, researcher, model_type, dataset_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (experiment_id, name, description, researcher, model_type, dataset_name))
        
        self.conn.commit()
        return experiment_id
    
    def add_prediction_batch(self, experiment_id: str, predictions: List[Dict]) -> int:
        """予測結果をバッチで追加"""
        
        cursor = self.conn.cursor()
        
        data = []
        for pred in predictions:
            data.append((
                experiment_id,
                pred['image_id'],
                pred['predicted_category'],
                pred['confidence'],
                pred.get('processing_time', 0.0)
            ))
        
        cursor.executemany("""
        INSERT INTO predictions (experiment_id, image_id, predicted_category, confidence, processing_time)
        VALUES (?, ?, ?, ?, ?)
        """, data)
        
        self.conn.commit()
        return len(predictions)
    
    def add_images(self, images: List[Dict]) -> int:
        """画像データを追加"""
        
        cursor = self.conn.cursor()
        
        data = [(img['image_id'], img['path'], img['true_category']) for img in images]
        
        cursor.executemany("""
        INSERT OR IGNORE INTO images (image_id, path, true_category)
        VALUES (?, ?, ?)
        """, data)
        
        self.conn.commit()
        return len(images)
    
    def calculate_accuracy(self, experiment_id: str) -> float:
        """実験の分類精度を計算"""
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN p.predicted_category = i.true_category THEN 1 END) as correct
        FROM predictions p
        JOIN images i ON p.image_id = i.image_id
        WHERE p.experiment_id = ?
        """, (experiment_id,))
        
        result = cursor.fetchone()
        
        if result and result['total'] > 0:
            accuracy = result['correct'] / result['total']
            
            # 統計として保存
            cursor.execute("""
            INSERT INTO experiment_stats (experiment_id, metric_name, value)
            VALUES (?, 'accuracy', ?)
            """, (experiment_id, accuracy))
            
            self.conn.commit()
            return accuracy
        
        return 0.0
    
    def get_category_performance(self, experiment_id: str) -> List[Dict]:
        """カテゴリ別の性能を取得"""
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT 
            c.name as category_name,
            COUNT(*) as total_predictions,
            COUNT(CASE WHEN p.predicted_category = i.true_category THEN 1 END) as correct_predictions,
            AVG(p.confidence) as avg_confidence
        FROM predictions p
        JOIN images i ON p.image_id = i.image_id
        JOIN categories c ON i.true_category = c.category_id
        WHERE p.experiment_id = ?
        GROUP BY c.category_id, c.name
        ORDER BY c.name
        """, (experiment_id,))
        
        results = []
        for row in cursor.fetchall():
            accuracy = row['correct_predictions'] / row['total_predictions'] if row['total_predictions'] > 0 else 0
            results.append({
                'category': row['category_name'],
                'total': row['total_predictions'],
                'correct': row['correct_predictions'],
                'accuracy': accuracy,
                'avg_confidence': row['avg_confidence']
            })
        
        return results
    
    def get_experiment_summary(self, experiment_id: str) -> Dict[str, Any]:
        """実験サマリーを取得"""
        
        cursor = self.conn.cursor()
        
        # 基本情報
        cursor.execute("""
        SELECT * FROM experiments WHERE experiment_id = ?
        """, (experiment_id,))
        
        experiment = cursor.fetchone()
        if not experiment:
            return {}
        
        # 統計情報
        cursor.execute("""
        SELECT 
            COUNT(*) as total_predictions,
            AVG(confidence) as avg_confidence,
            AVG(processing_time) as avg_processing_time,
            MIN(processing_time) as min_processing_time,
            MAX(processing_time) as max_processing_time
        FROM predictions
        WHERE experiment_id = ?
        """, (experiment_id,))
        
        stats = cursor.fetchone()
        
        # 精度を計算
        accuracy = self.calculate_accuracy(experiment_id)
        
        return {
            'experiment_id': experiment_id,
            'name': experiment['name'],
            'description': experiment['description'],
            'researcher': experiment['researcher'],
            'model_type': experiment['model_type'],
            'dataset_name': experiment['dataset_name'],
            'created_at': experiment['created_at'],
            'status': experiment['status'],
            'total_predictions': stats['total_predictions'] if stats else 0,
            'accuracy': accuracy,
            'avg_confidence': stats['avg_confidence'] if stats else 0,
            'avg_processing_time': stats['avg_processing_time'] if stats else 0,
            'min_processing_time': stats['min_processing_time'] if stats else 0,
            'max_processing_time': stats['max_processing_time'] if stats else 0
        }
    
    def compare_experiments(self, experiment_ids: List[str]) -> List[Dict[str, Any]]:
        """複数実験の比較"""
        
        comparison = []
        
        for exp_id in experiment_ids:
            summary = self.get_experiment_summary(exp_id)
            if summary:
                comparison.append(summary)
        
        return comparison
    
    def get_processing_time_stats(self, experiment_id: str) -> Dict[str, float]:
        """処理時間の統計を取得"""
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT 
            AVG(processing_time) as avg_time,
            MIN(processing_time) as min_time,
            MAX(processing_time) as max_time,
            COUNT(*) as count
        FROM predictions
        WHERE experiment_id = ?
        """, (experiment_id,))
        
        result = cursor.fetchone()
        
        return {
            'avg_time': result['avg_time'] if result else 0,
            'min_time': result['min_time'] if result else 0,
            'max_time': result['max_time'] if result else 0,
            'total_predictions': result['count'] if result else 0
        }
    
    def get_confidence_distribution(self, experiment_id: str) -> Dict[str, int]:
        """確信度の分布を取得"""
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT 
            CASE 
                WHEN confidence >= 0.9 THEN 'very_high'
                WHEN confidence >= 0.7 THEN 'high'
                WHEN confidence >= 0.5 THEN 'medium'
                WHEN confidence >= 0.3 THEN 'low'
                ELSE 'very_low'
            END as confidence_level,
            COUNT(*) as count
        FROM predictions
        WHERE experiment_id = ?
        GROUP BY confidence_level
        """, (experiment_id,))
        
        distribution = {
            'very_high': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'very_low': 0
        }
        
        for row in cursor.fetchall():
            distribution[row['confidence_level']] = row['count']
        
        return distribution
    
    def export_experiment_data(self, experiment_id: str, format: str = 'json') -> str:
        """実験データをエクスポート"""
        
        cursor = self.conn.cursor()
        
        # 実験情報
        experiment = self.get_experiment_summary(experiment_id)
        
        # 予測データ
        cursor.execute("""
        SELECT 
            p.*,
            i.path as image_path,
            c1.name as predicted_category_name,
            c2.name as true_category_name
        FROM predictions p
        JOIN images i ON p.image_id = i.image_id
        JOIN categories c1 ON p.predicted_category = c1.category_id
        JOIN categories c2 ON i.true_category = c2.category_id
        WHERE p.experiment_id = ?
        ORDER BY p.timestamp
        """, (experiment_id,))
        
        predictions = [dict(row) for row in cursor.fetchall()]
        
        # カテゴリ別性能
        category_performance = self.get_category_performance(experiment_id)
        
        export_data = {
            'experiment': experiment,
            'predictions': predictions,
            'category_performance': category_performance,
            'processing_time_stats': self.get_processing_time_stats(experiment_id),
            'confidence_distribution': self.get_confidence_distribution(experiment_id),
            'exported_at': datetime.now().isoformat()
        }
        
        if format.lower() == 'json':
            filename = f"research_export_{experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            return filename
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def generate_report(self, experiment_id: str) -> str:
        """実験レポートを生成"""
        
        summary = self.get_experiment_summary(experiment_id)
        if not summary:
            return "実験が見つかりません。"
        
        category_perf = self.get_category_performance(experiment_id)
        processing_stats = self.get_processing_time_stats(experiment_id)
        confidence_dist = self.get_confidence_distribution(experiment_id)
        
        report = f"""
# 実験レポート: {summary['name']}

## 基本情報
- **実験ID**: {summary['experiment_id']}
- **研究者**: {summary['researcher']}
- **モデル**: {summary['model_type']}
- **データセット**: {summary['dataset_name']}
- **実施日時**: {summary['created_at']}
- **説明**: {summary['description']}

## 全体性能
- **総予測数**: {summary['total_predictions']:,}件
- **分類精度**: {summary['accuracy']:.4f} ({summary['accuracy']*100:.2f}%)
- **平均確信度**: {summary['avg_confidence']:.4f}

## 処理性能
- **平均処理時間**: {processing_stats['avg_time']:.4f}秒
- **最短処理時間**: {processing_stats['min_time']:.4f}秒
- **最長処理時間**: {processing_stats['max_time']:.4f}秒

## カテゴリ別性能

| カテゴリ | 予測数 | 正解数 | 精度 | 平均確信度 |
|---------|-------|-------|------|----------|
"""
        
        for cat in category_perf:
            report += f"| {cat['category']} | {cat['total']} | {cat['correct']} | {cat['accuracy']:.4f} | {cat['avg_confidence']:.4f} |\n"
        
        report += f"""
## 確信度分布

- **非常に高い (≥0.9)**: {confidence_dist['very_high']}件
- **高い (0.7-0.9)**: {confidence_dist['high']}件
- **中程度 (0.5-0.7)**: {confidence_dist['medium']}件
- **低い (0.3-0.5)**: {confidence_dist['low']}件
- **非常に低い (<0.3)**: {confidence_dist['very_low']}件

---
レポート生成日時: {datetime.now().isoformat()}
"""
        
        return report
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """実験一覧を取得"""
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
        SELECT 
            e.*,
            COUNT(p.id) as prediction_count,
            AVG(es.value) as accuracy
        FROM experiments e
        LEFT JOIN predictions p ON e.experiment_id = p.experiment_id
        LEFT JOIN experiment_stats es ON e.experiment_id = es.experiment_id AND es.metric_name = 'accuracy'
        GROUP BY e.experiment_id
        ORDER BY e.created_at DESC
        """)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def execute_custom_query(self, query: str) -> List[Dict[str, Any]]:
        """カスタムクエリを実行"""
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """データベース接続を閉じる"""
        if self.conn:
            self.conn.close()


class ResearchSQLCLI:
    """研究SQLのコマンドラインインターフェース"""
    
    def __init__(self):
        self.sql = SimpleResearchSQL()
        
    def start(self):
        """CLIを開始"""
        
        print("\n📊 シンプル研究SQL システム")
        print("=" * 50)
        print("利用可能なコマンド:")
        print("  new <実験名>        - 新しい実験を作成")
        print("  list               - 実験一覧を表示")
        print("  summary <実験ID>    - 実験サマリーを表示")
        print("  report <実験ID>     - レポートを生成")
        print("  compare <ID1,ID2>   - 実験を比較")
        print("  export <実験ID>     - データをエクスポート")
        print("  sql <クエリ>        - カスタムSQLを実行")
        print("  demo               - デモデータを作成")
        print("  exit               - 終了")
        print("=" * 50)
        
        while True:
            try:
                command = input("\n研究SQL> ").strip()
                
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    break
                
                self._process_command(command)
                
            except KeyboardInterrupt:
                print("\n終了します。")
                break
            except Exception as e:
                print(f"エラー: {str(e)}")
        
        self.sql.close()
    
    def _process_command(self, command: str):
        """コマンドを処理"""
        
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'new':
            self._new_experiment(args)
        elif cmd == 'list':
            self._list_experiments()
        elif cmd == 'summary':
            self._show_summary(args)
        elif cmd == 'report':
            self._generate_report(args)
        elif cmd == 'compare':
            self._compare_experiments(args)
        elif cmd == 'export':
            self._export_experiment(args)
        elif cmd == 'sql':
            self._execute_sql(args)
        elif cmd == 'demo':
            self._create_demo_data()
        else:
            print(f"不明なコマンド: {cmd}")
    
    def _new_experiment(self, name: str):
        """新しい実験を作成"""
        if not name:
            print("実験名を指定してください。")
            return
        
        researcher = input("研究者名 (任意): ").strip()
        model_type = input("モデルタイプ (任意): ").strip()
        description = input("実験説明 (任意): ").strip()
        
        exp_id = self.sql.create_experiment(name, description, researcher, model_type)
        print(f"✅ 実験を作成しました: {exp_id}")
    
    def _list_experiments(self):
        """実験一覧を表示"""
        experiments = self.sql.list_experiments()
        
        if not experiments:
            print("実験がありません。")
            return
        
        print("\n📋 実験一覧:")
        print("-" * 80)
        for exp in experiments:
            accuracy = exp['accuracy'] if exp['accuracy'] else 0
            print(f"{exp['experiment_id']}: {exp['name']}")
            print(f"  研究者: {exp['researcher']}, 予測数: {exp['prediction_count']}, 精度: {accuracy:.4f}")
            print(f"  作成日: {exp['created_at']}")
            print()
    
    def _show_summary(self, experiment_id: str):
        """実験サマリーを表示"""
        if not experiment_id:
            print("実験IDを指定してください。")
            return
        
        summary = self.sql.get_experiment_summary(experiment_id)
        if not summary:
            print("実験が見つかりません。")
            return
        
        print(f"\n📊 実験サマリー: {summary['name']}")
        print("-" * 50)
        print(f"実験ID: {summary['experiment_id']}")
        print(f"研究者: {summary['researcher']}")
        print(f"モデル: {summary['model_type']}")
        print(f"予測数: {summary['total_predictions']:,}件")
        print(f"精度: {summary['accuracy']:.4f} ({summary['accuracy']*100:.2f}%)")
        print(f"平均確信度: {summary['avg_confidence']:.4f}")
        print(f"平均処理時間: {summary['avg_processing_time']:.4f}秒")
    
    def _generate_report(self, experiment_id: str):
        """レポートを生成"""
        if not experiment_id:
            print("実験IDを指定してください。")
            return
        
        report = self.sql.generate_report(experiment_id)
        print(report)
    
    def _compare_experiments(self, experiment_ids: str):
        """実験を比較"""
        if not experiment_ids:
            print("実験IDをカンマ区切りで指定してください。")
            return
        
        ids = [id.strip() for id in experiment_ids.split(',')]
        comparison = self.sql.compare_experiments(ids)
        
        if not comparison:
            print("実験が見つかりません。")
            return
        
        print("\n📈 実験比較:")
        print("-" * 80)
        for exp in comparison:
            print(f"{exp['experiment_id']}: {exp['name']}")
            print(f"  精度: {exp['accuracy']:.4f}, 予測数: {exp['total_predictions']}")
        
        # 最高精度を表示
        best = max(comparison, key=lambda x: x['accuracy'])
        print(f"\n🏆 最高精度: {best['name']} ({best['accuracy']:.4f})")
    
    def _export_experiment(self, experiment_id: str):
        """実験をエクスポート"""
        if not experiment_id:
            print("実験IDを指定してください。")
            return
        
        filename = self.sql.export_experiment_data(experiment_id)
        print(f"✅ エクスポート完了: {filename}")
    
    def _execute_sql(self, query: str):
        """カスタムSQLを実行"""
        if not query:
            print("SQLクエリを指定してください。")
            return
        
        try:
            results = self.sql.execute_custom_query(query)
            print(f"\n結果: {len(results)}行")
            for i, row in enumerate(results[:10]):
                print(f"{i+1}: {dict(row)}")
            
            if len(results) > 10:
                print(f"... 他 {len(results) - 10} 行")
        
        except Exception as e:
            print(f"SQLエラー: {str(e)}")
    
    def _create_demo_data(self):
        """デモデータを作成"""
        print("デモデータを作成中...")
        
        # デモ実験を作成
        exp_id = self.sql.create_experiment(
            "WordNet特化分類デモ",
            "8カテゴリ特化データセットのデモ実験",
            "Demo Researcher",
            "CLIP-ViT-B/32"
        )
        
        # デモ画像データ
        demo_images = [
            {'image_id': f'demo_img_{i:03d}', 'path': f'/demo/images/img_{i:03d}.jpg', 'true_category': (i % 8) + 1}
            for i in range(50)
        ]
        
        self.sql.add_images(demo_images)
        
        # デモ予測データ
        demo_predictions = []
        for i in range(50):
            # 精度81.25%になるように調整
            true_cat = (i % 8) + 1
            predicted_cat = true_cat if i < 40 else ((i % 8) + 2) % 8 + 1  # 40/50 = 80%の精度
            
            demo_predictions.append({
                'image_id': f'demo_img_{i:03d}',
                'predicted_category': predicted_cat,
                'confidence': 0.75 + (i % 25) * 0.01,  # 0.75-0.99の範囲
                'processing_time': 0.10 + (i % 10) * 0.01  # 0.10-0.19秒の範囲
            })
        
        self.sql.add_prediction_batch(exp_id, demo_predictions)
        
        # 精度を計算
        accuracy = self.sql.calculate_accuracy(exp_id)
        
        print(f"✅ デモデータ作成完了")
        print(f"   実験ID: {exp_id}")
        print(f"   画像数: {len(demo_images)}")
        print(f"   予測数: {len(demo_predictions)}")
        print(f"   精度: {accuracy:.4f}")


def main():
    """メイン関数"""
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        # CLIモード
        cli = ResearchSQLCLI()
        cli.start()
    else:
        # デモモード
        print("📊 シンプル研究SQL デモ")
        print("=" * 40)
        
        sql = SimpleResearchSQL("demo_simple.db")
        
        # デモ実験作成
        exp_id = sql.create_experiment(
            "テスト実験",
            "シンプルSQL機能のテスト",
            "Test User",
            "TestModel"
        )
        
        print(f"✅ 実験作成: {exp_id}")
        
        # デモデータ追加
        demo_images = [
            {'image_id': 'test_001', 'path': '/test/001.jpg', 'true_category': 1},
            {'image_id': 'test_002', 'path': '/test/002.jpg', 'true_category': 2},
            {'image_id': 'test_003', 'path': '/test/003.jpg', 'true_category': 1}
        ]
        
        sql.add_images(demo_images)
        
        demo_predictions = [
            {'image_id': 'test_001', 'predicted_category': 1, 'confidence': 0.95, 'processing_time': 0.12},
            {'image_id': 'test_002', 'predicted_category': 2, 'confidence': 0.88, 'processing_time': 0.15},
            {'image_id': 'test_003', 'predicted_category': 1, 'confidence': 0.92, 'processing_time': 0.11}
        ]
        
        sql.add_prediction_batch(exp_id, demo_predictions)
        
        # 結果表示
        summary = sql.get_experiment_summary(exp_id)
        print("\n📊 実験サマリー:")
        print(f"精度: {summary['accuracy']:.4f}")
        print(f"平均確信度: {summary['avg_confidence']:.4f}")
        
        # レポート生成
        report = sql.generate_report(exp_id)
        print("\n📄 実験レポート:")
        print(report[:500] + "...")
        
        sql.close()
        
        print("\n💡 CLIモードを使用するには: python3 simple_research_sql.py cli")


if __name__ == "__main__":
    main()