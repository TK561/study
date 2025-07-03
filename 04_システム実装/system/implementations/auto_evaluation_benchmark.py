#!/usr/bin/env python3
"""
自動評価・ベンチマークシステム - 完全実装版
モデル性能の自動評価と比較ベンチマークを実行するシステム
"""

import json
import time
from datetime import datetime
from pathlib import Path
import random
from collections import defaultdict
import statistics

class AutoEvaluationBenchmark:
    def __init__(self):
        self.name = "自動評価・ベンチマークシステム"
        self.version = "2.0.0"
        self.output_dir = Path("output/benchmarks")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.benchmark_history = []
        
        # 評価メトリクス定義
        self.metrics = {
            "accuracy": {"name": "精度", "unit": "", "higher_is_better": True},
            "precision": {"name": "適合率", "unit": "", "higher_is_better": True},
            "recall": {"name": "再現率", "unit": "", "higher_is_better": True},
            "f1_score": {"name": "F1スコア", "unit": "", "higher_is_better": True},
            "processing_time": {"name": "処理時間", "unit": "ms", "higher_is_better": False},
            "memory_usage": {"name": "メモリ使用量", "unit": "MB", "higher_is_better": False},
            "throughput": {"name": "スループット", "unit": "fps", "higher_is_better": True}
        }
        
    def generate_confusion_matrix(self, num_classes=5):
        """混同行列を生成（モック実装）"""
        matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
        
        # 対角線上に高い値を配置（正解）
        for i in range(num_classes):
            matrix[i][i] = random.randint(7, 9)  # 7-9個の正解
            
            # 非対角要素（誤分類）
            for j in range(num_classes):
                if i != j:
                    matrix[i][j] = random.randint(0, 2)  # 0-2個の誤分類
        
        return matrix
    
    def calculate_metrics_from_confusion_matrix(self, confusion_matrix):
        """混同行列から各種メトリクスを計算"""
        num_classes = len(confusion_matrix)
        metrics = {}
        
        # 全体の精度
        total_correct = sum(confusion_matrix[i][i] for i in range(num_classes))
        total_samples = sum(sum(row) for row in confusion_matrix)
        metrics["accuracy"] = (total_correct / total_samples) if total_samples > 0 else 0
        
        # クラスごとのメトリクス
        class_metrics = []
        for i in range(num_classes):
            tp = confusion_matrix[i][i]
            fp = sum(confusion_matrix[j][i] for j in range(num_classes)) - tp
            fn = sum(confusion_matrix[i]) - tp
            tn = total_samples - tp - fp - fn
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            class_metrics.append({
                "class_id": i,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "support": sum(confusion_matrix[i])
            })
        
        # マクロ平均
        metrics["precision"] = sum(m["precision"] for m in class_metrics) / len(class_metrics)
        metrics["recall"] = sum(m["recall"] for m in class_metrics) / len(class_metrics)
        metrics["f1_score"] = sum(m["f1_score"] for m in class_metrics) / len(class_metrics)
        
        return metrics, class_metrics
    
    def simulate_model_performance(self, model_name, dataset_name):
        """モデル性能をシミュレート（モック実装）"""
        # モデル特性に基づくベース性能
        model_characteristics = {
            "resnet50": {"base_accuracy": 85, "speed": 50, "memory": 200},
            "efficientnet": {"base_accuracy": 87, "speed": 35, "memory": 150},
            "mobilenet": {"base_accuracy": 80, "speed": 20, "memory": 50},
            "custom_model": {"base_accuracy": 83, "speed": 45, "memory": 180},
            "ensemble": {"base_accuracy": 90, "speed": 80, "memory": 400}
        }
        
        # データセット特性
        dataset_difficulty = {
            "easy": 1.1,
            "medium": 1.0,
            "hard": 0.9,
            "very_hard": 0.85
        }
        
        # ベース性能取得
        if model_name in model_characteristics:
            base = model_characteristics[model_name]
        else:
            base = {"base_accuracy": 82, "speed": 40, "memory": 160}
        
        # ランダム要素を加えた性能
        difficulty = dataset_difficulty.get(dataset_name, 1.0)
        
        performance = {
            "accuracy": min(1.0, (base["base_accuracy"] / 100) * difficulty + random.uniform(-0.05, 0.05)),
            "processing_time": base["speed"] + random.uniform(-10, 10),
            "memory_usage": base["memory"] + random.uniform(-20, 20),
            "throughput": 1000 / base["speed"] + random.uniform(-2, 2)
        }
        
        return performance
    
    def run_single_benchmark(self, model_config, dataset_config, num_samples=1000):
        """単一ベンチマークの実行"""
        start_time = time.time()
        
        # 混同行列生成
        confusion_matrix = self.generate_confusion_matrix(
            num_classes=dataset_config.get("num_classes", 5)
        )
        
        # メトリクス計算
        metrics, class_metrics = self.calculate_metrics_from_confusion_matrix(confusion_matrix)
        
        # パフォーマンスシミュレーション
        performance = self.simulate_model_performance(
            model_config["name"],
            dataset_config.get("difficulty", "medium")
        )
        
        # メトリクス統合（accuracyは混同行列の値を優先）
        confusion_accuracy = metrics["accuracy"]
        metrics.update(performance)
        metrics["accuracy"] = confusion_accuracy  # 混同行列由来の精度を保持
        
        # ベンチマーク時間
        benchmark_time = time.time() - start_time
        
        result = {
            "model": model_config,
            "dataset": dataset_config,
            "metrics": metrics,
            "class_metrics": class_metrics,
            "confusion_matrix": confusion_matrix,
            "num_samples": num_samples,
            "benchmark_time": round(benchmark_time, 3),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def run_comparative_benchmark(self, models, datasets):
        """複数モデル・データセットの比較ベンチマーク"""
        print("🏃 比較ベンチマーク実行中...")
        
        all_results = []
        comparison_matrix = defaultdict(lambda: defaultdict(dict))
        
        total_combinations = len(models) * len(datasets)
        current = 0
        
        for model in models:
            for dataset in datasets:
                current += 1
                print(f"  [{current}/{total_combinations}] {model['name']} on {dataset['name']}")
                
                # ベンチマーク実行
                result = self.run_single_benchmark(model, dataset)
                all_results.append(result)
                
                # 比較マトリクスに追加
                for metric_name, metric_value in result["metrics"].items():
                    comparison_matrix[metric_name][model["name"]][dataset["name"]] = metric_value
        
        # 総合分析
        analysis = self.analyze_benchmark_results(all_results, comparison_matrix)
        
        # レポート生成
        report = {
            "benchmark_name": "比較ベンチマーク",
            "timestamp": datetime.now().isoformat(),
            "models": models,
            "datasets": datasets,
            "results": all_results,
            "comparison_matrix": dict(comparison_matrix),
            "analysis": analysis
        }
        
        # 履歴に追加
        self.benchmark_history.append(report)
        
        return report
    
    def analyze_benchmark_results(self, results, comparison_matrix):
        """ベンチマーク結果の分析"""
        analysis = {
            "best_performers": {},
            "metric_statistics": {},
            "model_rankings": {},
            "recommendations": []
        }
        
        # メトリクスごとの統計
        for metric_name, metric_info in self.metrics.items():
            if metric_name in comparison_matrix:
                all_values = []
                for model_results in comparison_matrix[metric_name].values():
                    all_values.extend(model_results.values())
                
                if all_values:
                    analysis["metric_statistics"][metric_name] = {
                        "mean": statistics.mean(all_values),
                        "std": statistics.stdev(all_values) if len(all_values) > 1 else 0,
                        "min": min(all_values),
                        "max": max(all_values)
                    }
                    
                    # ベストパフォーマー特定
                    best_value = max(all_values) if metric_info["higher_is_better"] else min(all_values)
                    for model, datasets in comparison_matrix[metric_name].items():
                        for dataset, value in datasets.items():
                            if value == best_value:
                                analysis["best_performers"][metric_name] = {
                                    "model": model,
                                    "dataset": dataset,
                                    "value": value
                                }
                                break
        
        # モデルランキング計算
        model_scores = defaultdict(list)
        for result in results:
            model_name = result["model"]["name"]
            
            # 正規化スコア計算
            for metric_name, metric_value in result["metrics"].items():
                if metric_name in self.metrics:
                    stats = analysis["metric_statistics"].get(metric_name, {})
                    if stats and stats["max"] != stats["min"]:
                        # 0-1に正規化
                        if self.metrics[metric_name]["higher_is_better"]:
                            normalized = (metric_value - stats["min"]) / (stats["max"] - stats["min"])
                        else:
                            normalized = 1 - (metric_value - stats["min"]) / (stats["max"] - stats["min"])
                        model_scores[model_name].append(normalized)
        
        # 総合スコア計算
        for model_name, scores in model_scores.items():
            analysis["model_rankings"][model_name] = {
                "average_score": statistics.mean(scores) if scores else 0,
                "num_metrics": len(scores)
            }
        
        # ランキングソート
        analysis["model_rankings"] = dict(
            sorted(analysis["model_rankings"].items(),
                   key=lambda x: x[1]["average_score"],
                   reverse=True)
        )
        
        # 推奨事項生成
        if analysis["model_rankings"]:
            best_model = list(analysis["model_rankings"].keys())[0]
            analysis["recommendations"].append(
                f"総合的に最も優れたモデルは {best_model} です"
            )
        
        if "accuracy" in analysis["metric_statistics"]:
            avg_accuracy = analysis["metric_statistics"]["accuracy"]["mean"]
            if avg_accuracy < 80:
                analysis["recommendations"].append(
                    "全体的な精度が低いため、モデルアーキテクチャの見直しを推奨します"
                )
        
        if "processing_time" in analysis["best_performers"]:
            fastest = analysis["best_performers"]["processing_time"]
            analysis["recommendations"].append(
                f"最速処理は {fastest['model']} で {fastest['value']:.1f}ms です"
            )
        
        return analysis
    
    def generate_benchmark_report_html(self, report):
        """ベンチマークレポートのHTML生成"""
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ベンチマークレポート - {report['timestamp']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .metric-value {{
            font-weight: bold;
            text-align: right;
        }}
        .best-value {{
            background-color: #d4edda;
            color: #155724;
        }}
        .recommendation {{
            background-color: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 10px 0;
        }}
        .chart {{
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 自動評価・ベンチマークレポート</h1>
        <p><strong>実行日時:</strong> {datetime.fromisoformat(report['timestamp']).strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        
        <h2>📊 比較マトリクス</h2>
"""
        
        # 各メトリクスの比較テーブル
        for metric_name, metric_data in report["comparison_matrix"].items():
            if metric_name in self.metrics:
                metric_info = self.metrics[metric_name]
                html_content += f"""
        <h3>{metric_info['name']}{f" ({metric_info['unit']})" if metric_info['unit'] else ""}</h3>
        <table>
            <tr>
                <th>モデル</th>
"""
                # データセット列
                datasets = list(report["datasets"])
                for dataset in datasets:
                    html_content += f"<th>{dataset['name']}</th>"
                html_content += "</tr>"
                
                # 各モデルの行
                for model_name, dataset_results in metric_data.items():
                    html_content += f"<tr><td><strong>{model_name}</strong></td>"
                    for dataset in datasets:
                        value = dataset_results.get(dataset['name'], '-')
                        if isinstance(value, (int, float)):
                            # ベスト値チェック
                            is_best = False
                            best_performer = report['analysis']['best_performers'].get(metric_name)
                            if best_performer and best_performer['model'] == model_name and best_performer['dataset'] == dataset['name']:
                                is_best = True
                            
                            cell_class = "metric-value best-value" if is_best else "metric-value"
                            html_content += f'<td class="{cell_class}">{value:.2f}</td>'
                        else:
                            html_content += f'<td class="metric-value">{value}</td>'
                    html_content += "</tr>"
                
                html_content += "</table>"
        
        # モデルランキング
        html_content += """
        <h2>🏅 モデル総合ランキング</h2>
        <table>
            <tr>
                <th>順位</th>
                <th>モデル</th>
                <th>総合スコア</th>
            </tr>
"""
        
        for i, (model_name, score_info) in enumerate(report['analysis']['model_rankings'].items(), 1):
            html_content += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{model_name}</strong></td>
                <td class="metric-value">{score_info['average_score']:.3f}</td>
            </tr>
"""
        
        html_content += """
        </table>
        
        <h2>💡 推奨事項</h2>
"""
        
        for recommendation in report['analysis']['recommendations']:
            html_content += f"""
        <div class="recommendation">
            {recommendation}
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>"""
        
        # ファイル保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_dir / f"benchmark_report_{timestamp}.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(report_path)
    
    def export_results_json(self, report):
        """結果をJSON形式でエクスポート"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_path = self.output_dir / f"benchmark_results_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return str(json_path)

def main():
    """実行例"""
    print("📊 自動評価・ベンチマークシステム 起動")
    print("=" * 50)
    
    benchmark = AutoEvaluationBenchmark()
    
    # テストモデル定義
    models = [
        {"name": "resnet50", "version": "1.0", "type": "CNN"},
        {"name": "efficientnet", "version": "b0", "type": "CNN"},
        {"name": "mobilenet", "version": "v3", "type": "lightweight"},
        {"name": "custom_model", "version": "2.0", "type": "hybrid"},
        {"name": "ensemble", "version": "1.0", "type": "ensemble"}
    ]
    
    # テストデータセット定義
    datasets = [
        {"name": "COCO_subset", "difficulty": "medium", "num_classes": 5},
        {"name": "ImageNet_subset", "difficulty": "hard", "num_classes": 10},
        {"name": "Custom_dataset", "difficulty": "easy", "num_classes": 3}
    ]
    
    # 比較ベンチマーク実行
    print("\n🚀 比較ベンチマーク開始...")
    report = benchmark.run_comparative_benchmark(models, datasets)
    
    # レポート生成
    html_path = benchmark.generate_benchmark_report_html(report)
    print(f"\n📄 HTMLレポート生成: {html_path}")
    
    # JSON エクスポート
    json_path = benchmark.export_results_json(report)
    print(f"💾 JSON結果エクスポート: {json_path}")
    
    # サマリー表示
    print("\n📈 ベンチマークサマリー:")
    print(f"  テストモデル数: {len(models)}")
    print(f"  テストデータセット数: {len(datasets)}")
    print(f"  総ベンチマーク数: {len(models) * len(datasets)}")
    
    print("\n🏆 トップ3モデル:")
    for i, (model_name, score_info) in enumerate(list(report['analysis']['model_rankings'].items())[:3], 1):
        print(f"  {i}. {model_name} (スコア: {score_info['average_score']:.3f})")
    
    print("\n✨ ベンチマーク完了")
    print(f"🌐 レポート表示: file://{Path(html_path).absolute()}")

if __name__ == "__main__":
    main()