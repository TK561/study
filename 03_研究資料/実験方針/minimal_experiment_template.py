"""
最小単位実験テンプレート
1実験 = 1パラメータ変更の原則に基づく実験フレームワーク
"""

import json
import time
from datetime import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

class MinimalExperimentRunner:
    """最小単位実験の実行管理クラス"""
    
    def __init__(self, base_config=None):
        self.base_config = base_config or self.get_default_config()
        self.results = []
        self.experiment_log = []
        
    def get_default_config(self):
        """デフォルト設定"""
        return {
            "confidence_threshold": 0.75,
            "num_categories": 16,
            "sample_size": 30,
            "learning_rate": 0.001,
            "batch_size": 32,
            "epochs": 10
        }
    
    def run_single_experiment(self, param_name, param_value, experiment_id=None):
        """
        最小単位の実験を実行
        1つのパラメータのみを変更して実験
        """
        if experiment_id is None:
            experiment_id = f"EXP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n{'='*50}")
        print(f"実験ID: {experiment_id}")
        print(f"変更パラメータ: {param_name} = {param_value}")
        print(f"開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        # 設定をコピーして1つのパラメータのみ変更
        config = self.base_config.copy()
        config[param_name] = param_value
        
        # 実験開始時刻
        start_time = time.time()
        
        # 実験実行（ここでは仮の結果を生成）
        result = self.execute_experiment(config)
        
        # 実行時間
        execution_time = time.time() - start_time
        
        # 結果の記録
        experiment_data = {
            "experiment_id": experiment_id,
            "timestamp": datetime.now().isoformat(),
            "parameter_changed": {param_name: param_value},
            "base_config": self.base_config,
            "result": result,
            "execution_time_seconds": round(execution_time, 2)
        }
        
        # 結果を保存
        self.save_experiment(experiment_data)
        self.results.append(experiment_data)
        
        # 結果の表示
        print(f"\n実験結果:")
        print(f"  確信度: {result['confidence']:.4f}")
        print(f"  精度: {result['accuracy']:.4f}")
        print(f"  実行時間: {execution_time:.2f}秒")
        
        return result
    
    def execute_experiment(self, config):
        """
        実際の実験処理（モック実装）
        実際の実装では、ここで画像分類などの処理を行う
        """
        # シミュレーション結果の生成
        base_confidence = 0.75
        base_accuracy = 0.85
        
        # パラメータによる影響をシミュレート
        if "confidence_threshold" in config:
            impact = (config["confidence_threshold"] - 0.75) * 0.2
            base_confidence += impact
            
        if "num_categories" in config:
            impact = (config["num_categories"] - 16) * -0.001
            base_accuracy += impact
            
        # ノイズを加えて現実的に
        confidence = np.clip(base_confidence + np.random.normal(0, 0.02), 0, 1)
        accuracy = np.clip(base_accuracy + np.random.normal(0, 0.01), 0, 1)
        
        return {
            "confidence": float(confidence),
            "accuracy": float(accuracy),
            "precision": float(np.random.uniform(0.8, 0.95)),
            "recall": float(np.random.uniform(0.75, 0.90)),
            "f1_score": float(np.random.uniform(0.77, 0.92))
        }
    
    def save_experiment(self, experiment_data):
        """実験結果をファイルに保存"""
        # 保存ディレクトリの作成
        save_dir = Path("experiment_results")
        save_dir.mkdir(exist_ok=True)
        
        # 個別実験ファイル
        filename = save_dir / f"{experiment_data['experiment_id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(experiment_data, f, indent=2, ensure_ascii=False)
        
        print(f"結果を保存: {filename}")
    
    def run_parameter_sweep(self, param_name, param_values):
        """
        パラメータスイープ実験
        1つのパラメータを段階的に変更
        """
        print(f"\nパラメータスイープ開始: {param_name}")
        print(f"テスト値: {param_values}")
        
        sweep_results = {}
        
        for value in param_values:
            result = self.run_single_experiment(param_name, value)
            sweep_results[value] = result
            
            # 短い待機時間（実際の実験では不要かも）
            time.sleep(1)
        
        # 結果の可視化
        self.plot_sweep_results(param_name, sweep_results)
        
        return sweep_results
    
    def plot_sweep_results(self, param_name, results):
        """スイープ結果の可視化"""
        values = sorted(results.keys())
        confidences = [results[v]['confidence'] for v in values]
        accuracies = [results[v]['accuracy'] for v in values]
        
        plt.figure(figsize=(10, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(values, confidences, 'b-o', markersize=8)
        plt.xlabel(param_name)
        plt.ylabel('確信度')
        plt.title(f'{param_name}と確信度の関係')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(values, accuracies, 'r-s', markersize=8)
        plt.xlabel(param_name)
        plt.ylabel('精度')
        plt.title(f'{param_name}と精度の関係')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'sweep_{param_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        plt.show()
    
    def run_minimal_optimization(self):
        """
        最小単位での最適化実験
        各パラメータを個別に最適化
        """
        optimization_sequence = [
            {
                "param": "confidence_threshold",
                "values": [0.70, 0.72, 0.74, 0.76, 0.78, 0.80],
                "metric": "confidence"
            },
            {
                "param": "num_categories", 
                "values": [8, 12, 16, 20, 24, 32],
                "metric": "accuracy"
            },
            {
                "param": "sample_size",
                "values": [10, 20, 30, 40, 50],
                "metric": "f1_score"
            }
        ]
        
        optimal_params = {}
        
        for opt_config in optimization_sequence:
            param_name = opt_config["param"]
            param_values = opt_config["values"]
            metric = opt_config["metric"]
            
            print(f"\n最適化: {param_name} (評価指標: {metric})")
            
            best_value = None
            best_score = -1
            
            for value in param_values:
                result = self.run_single_experiment(param_name, value)
                score = result[metric]
                
                if score > best_score:
                    best_score = score
                    best_value = value
                
                time.sleep(0.5)  # 短い待機
            
            optimal_params[param_name] = best_value
            self.base_config[param_name] = best_value  # 最適値で更新
            
            print(f"\n{param_name}の最適値: {best_value} (スコア: {best_score:.4f})")
        
        return optimal_params


# 使用例
if __name__ == "__main__":
    # 実験ランナーの初期化
    runner = MinimalExperimentRunner()
    
    # 1. 単一パラメータの実験
    print("=== 単一パラメータ実験 ===")
    result = runner.run_single_experiment("confidence_threshold", 0.77)
    
    # 2. パラメータスイープ
    print("\n=== パラメータスイープ実験 ===")
    sweep_results = runner.run_parameter_sweep(
        "confidence_threshold",
        [0.70, 0.75, 0.80, 0.85, 0.90]
    )
    
    # 3. 段階的最適化
    print("\n=== 段階的最適化実験 ===")
    optimal_params = runner.run_minimal_optimization()
    
    print("\n=== 最終的な最適パラメータ ===")
    for param, value in optimal_params.items():
        print(f"{param}: {value}")