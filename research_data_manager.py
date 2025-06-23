#!/usr/bin/env python3
"""
研究データマネージャー - 画像分類研究専用のデータ管理システム
Geminiなしの純粋なデータベース機能のみ
"""

import os
import json
import sqlite3
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any
from simple_research_sql import SimpleResearchSQL

class ResearchDataManager:
    """研究データ管理の統合システム"""
    
    def __init__(self, db_path: str = "research_data.db"):
        self.sql = SimpleResearchSQL(db_path)
        self.import_log = []
        
    def import_experiment_from_python(self, experiment_data: Dict[str, Any]) -> str:
        """Pythonの実験結果から直接インポート"""
        
        # 実験作成
        exp_id = self.sql.create_experiment(
            name=experiment_data.get('name', '未命名実験'),
            description=experiment_data.get('description', ''),
            researcher=experiment_data.get('researcher', ''),
            model_type=experiment_data.get('model_type', ''),
            dataset_name=experiment_data.get('dataset_name', '')
        )
        
        # 画像データがある場合
        if 'images' in experiment_data:
            self.sql.add_images(experiment_data['images'])
            self.import_log.append(f"画像データ {len(experiment_data['images'])}件をインポート")
        
        # 予測結果がある場合
        if 'predictions' in experiment_data:
            self.sql.add_prediction_batch(exp_id, experiment_data['predictions'])
            self.import_log.append(f"予測結果 {len(experiment_data['predictions'])}件をインポート")
        
        self.import_log.append(f"実験 {exp_id} を作成")
        
        return exp_id
    
    def import_from_csv(self, predictions_csv: str, images_csv: Optional[str] = None) -> str:
        """CSVファイルからデータをインポート"""
        
        # CSVから予測結果を読み込み
        predictions = []
        experiment_name = f"CSV_Import_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        with open(predictions_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                predictions.append({
                    'image_id': row['image_id'],
                    'predicted_category': int(row['predicted_category']),
                    'confidence': float(row['confidence']),
                    'processing_time': float(row.get('processing_time', 0.0))
                })
        
        # 実験作成
        exp_id = self.sql.create_experiment(
            name=experiment_name,
            description=f"CSVからインポート: {predictions_csv}",
            researcher="CSV Import"
        )
        
        # 画像データがある場合
        if images_csv and os.path.exists(images_csv):
            images = []
            with open(images_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    images.append({
                        'image_id': row['image_id'],
                        'path': row['path'],
                        'true_category': int(row['true_category'])
                    })
            
            self.sql.add_images(images)
            self.import_log.append(f"画像データ {len(images)}件をCSVからインポート")
        
        # 予測結果を追加
        self.sql.add_prediction_batch(exp_id, predictions)
        self.import_log.append(f"予測結果 {len(predictions)}件をCSVからインポート")
        
        return exp_id
    
    def create_wordnet_experiment(self, results_data: Dict[str, Any]) -> str:
        """WordNet画像分類研究の結果を登録"""
        
        # 研究特化の実験を作成
        exp_id = self.sql.create_experiment(
            name=f"WordNet特化実験_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description="WordNetベースの意味カテゴリ分析を用いた特化型画像分類",
            researcher=results_data.get('researcher', 'WordNet研究チーム'),
            model_type="BLIP+WordNet+CLIP",
            dataset_name="8カテゴリ特化データセット"
        )
        
        # テストケースデータを変換
        if 'test_cases' in results_data:
            images = []
            predictions = []
            
            for i, test_case in enumerate(results_data['test_cases']):
                image_id = f"wordnet_test_{i:03d}"
                
                # カテゴリ名をIDに変換
                category_mapping = {
                    'Person': 1, 'Animal': 2, 'Food': 3, 'Landscape': 4,
                    'Building': 5, 'Furniture': 6, 'Vehicle': 7, 'Plant': 8
                }
                
                true_category = category_mapping.get(test_case.get('wordnet_category'), 1)
                predicted_category = category_mapping.get(test_case.get('predicted_category'), 1)
                
                images.append({
                    'image_id': image_id,
                    'path': test_case.get('image_path', f'/wordnet/test_{i:03d}.jpg'),
                    'true_category': true_category
                })
                
                predictions.append({
                    'image_id': image_id,
                    'predicted_category': predicted_category,
                    'confidence': test_case.get('confidence', 0.0),
                    'processing_time': test_case.get('processing_time', 0.0)
                })
            
            self.sql.add_images(images)
            self.sql.add_prediction_batch(exp_id, predictions)
            
            self.import_log.append(f"WordNetテストケース {len(images)}件を登録")
        
        # 統計データを直接登録
        if 'overall_accuracy' in results_data:
            cursor = self.sql.conn.cursor()
            cursor.execute("""
            INSERT INTO experiment_stats (experiment_id, metric_name, value)
            VALUES (?, 'accuracy', ?)
            """, (exp_id, results_data['overall_accuracy']))
            
            self.sql.conn.commit()
            self.import_log.append(f"全体精度 {results_data['overall_accuracy']:.4f} を登録")
        
        return exp_id
    
    def bulk_import_experiments(self, experiments_dir: str) -> List[str]:
        """複数の実験結果を一括インポート"""
        
        imported_experiments = []
        
        for filename in os.listdir(experiments_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(experiments_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        experiment_data = json.load(f)
                    
                    exp_id = self.import_experiment_from_python(experiment_data)
                    imported_experiments.append(exp_id)
                    self.import_log.append(f"ファイル {filename} から実験 {exp_id} をインポート")
                    
                except Exception as e:
                    self.import_log.append(f"ファイル {filename} のインポートに失敗: {str(e)}")
        
        return imported_experiments
    
    def export_for_analysis(self, experiment_ids: List[str], output_dir: str = "analysis_export") -> Dict[str, str]:
        """分析用にデータをエクスポート"""
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        exported_files = {}
        
        for exp_id in experiment_ids:
            # JSON形式でエクスポート
            json_file = self.sql.export_experiment_data(exp_id)
            
            # CSV形式でも出力
            cursor = self.sql.conn.cursor()
            
            # 予測結果CSV
            cursor.execute("""
            SELECT 
                p.image_id,
                p.predicted_category,
                p.confidence,
                p.processing_time,
                i.true_category,
                c1.name as predicted_category_name,
                c2.name as true_category_name
            FROM predictions p
            JOIN images i ON p.image_id = i.image_id
            JOIN categories c1 ON p.predicted_category = c1.category_id
            JOIN categories c2 ON i.true_category = c2.category_id
            WHERE p.experiment_id = ?
            """, (exp_id,))
            
            results = cursor.fetchall()
            
            csv_filename = os.path.join(output_dir, f"{exp_id}_predictions.csv")
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                if results:
                    writer = csv.DictWriter(f, fieldnames=results[0].keys())
                    writer.writeheader()
                    for row in results:
                        writer.writerow(dict(row))
            
            exported_files[exp_id] = {
                'json': json_file,
                'csv': csv_filename
            }
        
        self.import_log.append(f"{len(experiment_ids)}個の実験を {output_dir} にエクスポート")
        
        return exported_files
    
    def create_analysis_summary(self, experiment_ids: List[str]) -> Dict[str, Any]:
        """複数実験の分析サマリーを作成"""
        
        summaries = []
        for exp_id in experiment_ids:
            summary = self.sql.get_experiment_summary(exp_id)
            if summary:
                summaries.append(summary)
        
        if not summaries:
            return {}
        
        # 統計的サマリーを計算
        accuracies = [s['accuracy'] for s in summaries if s['accuracy'] > 0]
        confidences = [s['avg_confidence'] for s in summaries if s['avg_confidence'] > 0]
        processing_times = [s['avg_processing_time'] for s in summaries if s['avg_processing_time'] > 0]
        
        analysis_summary = {
            'total_experiments': len(summaries),
            'accuracy_stats': {
                'mean': sum(accuracies) / len(accuracies) if accuracies else 0,
                'max': max(accuracies) if accuracies else 0,
                'min': min(accuracies) if accuracies else 0,
                'count': len(accuracies)
            },
            'confidence_stats': {
                'mean': sum(confidences) / len(confidences) if confidences else 0,
                'max': max(confidences) if confidences else 0,
                'min': min(confidences) if confidences else 0
            },
            'processing_time_stats': {
                'mean': sum(processing_times) / len(processing_times) if processing_times else 0,
                'max': max(processing_times) if processing_times else 0,
                'min': min(processing_times) if processing_times else 0
            },
            'experiments': summaries,
            'best_experiment': max(summaries, key=lambda x: x['accuracy']) if summaries else None,
            'analysis_date': datetime.now().isoformat()
        }
        
        return analysis_summary
    
    def generate_comparative_report(self, experiment_ids: List[str]) -> str:
        """比較レポートを生成"""
        
        analysis = self.create_analysis_summary(experiment_ids)
        
        if not analysis:
            return "分析するデータがありません。"
        
        report = f"""
# 研究実験比較レポート

## 分析概要
- **分析実験数**: {analysis['total_experiments']}
- **分析日時**: {analysis['analysis_date']}

## 精度統計
- **平均精度**: {analysis['accuracy_stats']['mean']:.4f}
- **最高精度**: {analysis['accuracy_stats']['max']:.4f}
- **最低精度**: {analysis['accuracy_stats']['min']:.4f}

## 確信度統計
- **平均確信度**: {analysis['confidence_stats']['mean']:.4f}
- **最高確信度**: {analysis['confidence_stats']['max']:.4f}
- **最低確信度**: {analysis['confidence_stats']['min']:.4f}

## 処理時間統計
- **平均処理時間**: {analysis['processing_time_stats']['mean']:.4f}秒
- **最短処理時間**: {analysis['processing_time_stats']['min']:.4f}秒
- **最長処理時間**: {analysis['processing_time_stats']['max']:.4f}秒

## 実験詳細

| 実験ID | 実験名 | 精度 | 確信度 | 処理時間 | 予測数 |
|--------|--------|------|--------|----------|--------|
"""
        
        for exp in analysis['experiments']:
            report += f"| {exp['experiment_id']} | {exp['name']} | {exp['accuracy']:.4f} | {exp['avg_confidence']:.4f} | {exp['avg_processing_time']:.4f} | {exp['total_predictions']} |\n"
        
        if analysis['best_experiment']:
            best = analysis['best_experiment']
            report += f"""
## 最高性能実験
- **実験ID**: {best['experiment_id']}
- **実験名**: {best['name']}
- **精度**: {best['accuracy']:.4f}
- **研究者**: {best['researcher']}
- **モデル**: {best['model_type']}
"""
        
        report += f"""
---
レポート生成日時: {datetime.now().isoformat()}
"""
        
        return report
    
    def get_import_log(self) -> List[str]:
        """インポートログを取得"""
        return self.import_log.copy()
    
    def clear_import_log(self):
        """インポートログをクリア"""
        self.import_log.clear()
    
    def close(self):
        """リソースを解放"""
        self.sql.close()


def demo_research_data_manager():
    """研究データマネージャーのデモ"""
    
    print("📊 研究データマネージャー デモ")
    print("=" * 50)
    
    manager = ResearchDataManager("demo_research_manager.db")
    
    # 1. WordNet研究結果の登録
    print("\n1. WordNet研究結果を登録中...")
    
    wordnet_results = {
        'researcher': 'WordNet研究チーム',
        'overall_accuracy': 0.8125,
        'test_cases': [
            {
                'image_path': '/wordnet/person_001.jpg',
                'wordnet_category': 'Person',
                'predicted_category': 'Person',
                'confidence': 0.95,
                'processing_time': 0.12
            },
            {
                'image_path': '/wordnet/animal_001.jpg',
                'wordnet_category': 'Animal',
                'predicted_category': 'Animal',
                'confidence': 0.88,
                'processing_time': 0.11
            },
            {
                'image_path': '/wordnet/food_001.jpg',
                'wordnet_category': 'Food',
                'predicted_category': 'Animal',  # 誤分類
                'confidence': 0.76,
                'processing_time': 0.13
            },
            {
                'image_path': '/wordnet/landscape_001.jpg',
                'wordnet_category': 'Landscape',
                'predicted_category': 'Landscape',
                'confidence': 0.92,
                'processing_time': 0.10
            }
        ]
    }
    
    wordnet_exp_id = manager.create_wordnet_experiment(wordnet_results)
    print(f"✅ WordNet実験を登録: {wordnet_exp_id}")
    
    # 2. 比較実験の作成
    print("\n2. 比較実験を作成中...")
    
    comparison_data = {
        'name': '従来手法比較実験',
        'description': '汎用モデルとの性能比較',
        'researcher': 'Comparison Team',
        'model_type': 'Generic CLIP',
        'images': [
            {'image_id': 'comp_001', 'path': '/comp/001.jpg', 'true_category': 1},
            {'image_id': 'comp_002', 'path': '/comp/002.jpg', 'true_category': 2},
            {'image_id': 'comp_003', 'path': '/comp/003.jpg', 'true_category': 3},
            {'image_id': 'comp_004', 'path': '/comp/004.jpg', 'true_category': 4}
        ],
        'predictions': [
            {'image_id': 'comp_001', 'predicted_category': 1, 'confidence': 0.82, 'processing_time': 0.15},
            {'image_id': 'comp_002', 'predicted_category': 3, 'confidence': 0.75, 'processing_time': 0.14},  # 誤分類
            {'image_id': 'comp_003', 'predicted_category': 3, 'confidence': 0.89, 'processing_time': 0.16},
            {'image_id': 'comp_004', 'predicted_category': 4, 'confidence': 0.91, 'processing_time': 0.12}
        ]
    }
    
    comparison_exp_id = manager.import_experiment_from_python(comparison_data)
    print(f"✅ 比較実験を作成: {comparison_exp_id}")
    
    # 3. 比較分析
    print("\n3. 比較分析を実行中...")
    
    experiment_ids = [wordnet_exp_id, comparison_exp_id]
    comparative_report = manager.generate_comparative_report(experiment_ids)
    
    print("📄 比較レポート:")
    print(comparative_report[:800] + "...")
    
    # 4. データエクスポート
    print("\n4. 分析用データをエクスポート中...")
    
    exported_files = manager.export_for_analysis(experiment_ids, "demo_export")
    
    for exp_id, files in exported_files.items():
        print(f"✅ {exp_id}: JSON={files['json']}, CSV={files['csv']}")
    
    # 5. インポートログ確認
    print("\n5. インポートログ:")
    for log_entry in manager.get_import_log():
        print(f"  - {log_entry}")
    
    # クリーンアップ
    manager.close()
    
    print("\n🎉 研究データマネージャー デモ完了！")
    
    print("\n📋 提供機能:")
    print("  📥 実験データの統合インポート")
    print("  📊 複数実験の比較分析")
    print("  📈 統計的サマリー生成")
    print("  💾 分析用データエクスポート")
    print("  📄 自動レポート生成")


if __name__ == "__main__":
    demo_research_data_manager()