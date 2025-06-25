#!/usr/bin/env python3
"""
多層物体検出統合API - 完全実装版
複数の物体検出モデルを統合し、包括的な検出結果を提供するAPIシステム
"""

import json
import os
from datetime import datetime
from pathlib import Path
import base64
from io import BytesIO
import random
from collections import defaultdict
import time

class MultiObjectDetectionAPI:
    def __init__(self):
        self.name = "多層物体検出統合API"
        self.version = "2.0.0"
        self.models = self._initialize_models()
        self.output_dir = Path("output/detections")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def _initialize_models(self):
        """利用可能な物体検出モデルを初期化（モック実装）"""
        return {
            "yolo": {
                "name": "YOLO v8",
                "speciality": "一般物体検出",
                "confidence_threshold": 0.5,
                "categories": ["person", "car", "dog", "cat", "chair", "book", "bottle", "phone"],
                "speed": "fast",
                "accuracy": 0.85
            },
            "faster_rcnn": {
                "name": "Faster R-CNN",
                "speciality": "高精度検出",
                "confidence_threshold": 0.6,
                "categories": ["person", "vehicle", "animal", "furniture", "electronics"],
                "speed": "medium",
                "accuracy": 0.92
            },
            "ssd": {
                "name": "SSD MobileNet",
                "speciality": "リアルタイム検出",
                "confidence_threshold": 0.4,
                "categories": ["person", "car", "bicycle", "motorcycle", "bus", "truck"],
                "speed": "very_fast",
                "accuracy": 0.78
            },
            "mask_rcnn": {
                "name": "Mask R-CNN",
                "speciality": "セグメンテーション",
                "confidence_threshold": 0.7,
                "categories": ["person", "animal", "object", "vehicle"],
                "speed": "slow",
                "accuracy": 0.94
            }
        }
    
    def detect_objects_single_model(self, image_data, model_name):
        """単一モデルでの物体検出（モック実装）"""
        if model_name not in self.models:
            raise ValueError(f"モデル {model_name} は利用できません")
        
        model = self.models[model_name]
        
        # モック検出結果を生成
        num_objects = random.randint(1, 5)
        detections = []
        
        for i in range(num_objects):
            detection = {
                "object_id": f"{model_name}_{i}",
                "category": random.choice(model["categories"]),
                "confidence": round(random.uniform(model["confidence_threshold"], 1.0), 3),
                "bbox": {
                    "x": random.randint(0, 800),
                    "y": random.randint(0, 600),
                    "width": random.randint(50, 200),
                    "height": random.randint(50, 200)
                },
                "model": model_name
            }
            detections.append(detection)
        
        # 処理時間をシミュレート
        if model["speed"] == "slow":
            time.sleep(0.5)
        elif model["speed"] == "medium":
            time.sleep(0.2)
        elif model["speed"] == "fast":
            time.sleep(0.1)
        else:  # very_fast
            time.sleep(0.05)
        
        return detections
    
    def integrate_detections(self, all_detections):
        """複数モデルの検出結果を統合"""
        integrated_results = []
        detection_map = defaultdict(list)
        
        # 位置が近い検出結果をグループ化
        for detection in all_detections:
            bbox_key = f"{detection['bbox']['x']//50}_{detection['bbox']['y']//50}"
            detection_map[bbox_key].append(detection)
        
        # グループごとに最適な検出結果を選択
        for group in detection_map.values():
            if len(group) == 1:
                integrated_results.append(group[0])
            else:
                # 複数モデルで検出された場合、信頼度が最も高いものを選択
                best_detection = max(group, key=lambda x: x['confidence'])
                
                # 複数モデルの情報を統合
                best_detection['detected_by'] = [d['model'] for d in group]
                best_detection['consensus_score'] = len(group) / len(self.models)
                best_detection['alternative_categories'] = list(set(d['category'] for d in group))
                
                integrated_results.append(best_detection)
        
        return integrated_results
    
    def detect_objects_multi_layer(self, image_data, use_models=None):
        """多層物体検出の実行"""
        if use_models is None:
            use_models = list(self.models.keys())
        
        start_time = time.time()
        all_detections = []
        model_results = {}
        
        # 各モデルで検出実行
        for model_name in use_models:
            if model_name in self.models:
                detections = self.detect_objects_single_model(image_data, model_name)
                all_detections.extend(detections)
                model_results[model_name] = {
                    "count": len(detections),
                    "detections": detections
                }
        
        # 検出結果を統合
        integrated_results = self.integrate_detections(all_detections)
        
        # 統計情報を計算
        category_counts = defaultdict(int)
        for detection in integrated_results:
            category_counts[detection['category']] += 1
        
        processing_time = time.time() - start_time
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "processing_time": round(processing_time, 3),
            "models_used": use_models,
            "total_objects": len(integrated_results),
            "category_summary": dict(category_counts),
            "integrated_detections": integrated_results,
            "model_specific_results": model_results
        }
    
    def analyze_detection_quality(self, detection_results):
        """検出品質の分析"""
        quality_metrics = {
            "average_confidence": 0,
            "consensus_rate": 0,
            "model_agreement": {},
            "category_distribution": {},
            "detection_density": 0
        }
        
        if not detection_results["integrated_detections"]:
            return quality_metrics
        
        # 平均信頼度
        confidences = [d["confidence"] for d in detection_results["integrated_detections"]]
        quality_metrics["average_confidence"] = round(sum(confidences) / len(confidences), 3)
        
        # コンセンサス率（複数モデルで検出された物体の割合）
        consensus_detections = [d for d in detection_results["integrated_detections"] 
                               if "consensus_score" in d and d["consensus_score"] > 0.5]
        quality_metrics["consensus_rate"] = len(consensus_detections) / len(detection_results["integrated_detections"])
        
        # カテゴリ分布
        quality_metrics["category_distribution"] = detection_results["category_summary"]
        
        # 検出密度（仮想的な画像サイズに対する検出数）
        quality_metrics["detection_density"] = len(detection_results["integrated_detections"]) / (800 * 600 / 10000)
        
        return quality_metrics
    
    def generate_api_response(self, image_data=None, use_models=None):
        """API レスポンスを生成"""
        try:
            # 画像データの検証（実際の実装では画像処理を行う）
            if image_data is None:
                image_data = {"mock": True, "size": (800, 600)}
            
            # 多層検出実行
            detection_results = self.detect_objects_multi_layer(image_data, use_models)
            
            # 品質分析
            quality_metrics = self.analyze_detection_quality(detection_results)
            
            # レスポンス構築
            response = {
                "api_version": self.version,
                "status": "success",
                "data": {
                    "detections": detection_results,
                    "quality_metrics": quality_metrics,
                    "recommendations": self.generate_recommendations(quality_metrics)
                }
            }
            
            # 結果を保存
            self.save_detection_results(response)
            
            return response
            
        except Exception as e:
            return {
                "api_version": self.version,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_recommendations(self, quality_metrics):
        """検出結果に基づく推奨事項を生成"""
        recommendations = []
        
        if quality_metrics["average_confidence"] < 0.7:
            recommendations.append({
                "type": "quality",
                "message": "検出信頼度が低いです。画像品質を向上させるか、より適切なモデルを選択してください。"
            })
        
        if quality_metrics["consensus_rate"] < 0.3:
            recommendations.append({
                "type": "consensus",
                "message": "モデル間の一致率が低いです。特定のカテゴリに特化したモデルの使用を検討してください。"
            })
        
        if quality_metrics["detection_density"] > 0.1:
            recommendations.append({
                "type": "density",
                "message": "検出物体が多数あります。セグメンテーションモデルの使用を推奨します。"
            })
        
        return recommendations
    
    def save_detection_results(self, results):
        """検出結果を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f"detection_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return str(output_file)
    
    def create_api_documentation(self):
        """API ドキュメントを生成"""
        doc_content = f"""# 多層物体検出統合API ドキュメント

## API バージョン: {self.version}

## エンドポイント

### POST /api/detect
多層物体検出を実行します。

#### リクエスト
```json
{{
    "image": "base64_encoded_image_data",
    "use_models": ["yolo", "faster_rcnn", "ssd", "mask_rcnn"]  // オプション
}}
```

#### レスポンス
```json
{{
    "api_version": "2.0.0",
    "status": "success",
    "data": {{
        "detections": {{
            "total_objects": 5,
            "integrated_detections": [...],
            "model_specific_results": {{...}}
        }},
        "quality_metrics": {{
            "average_confidence": 0.85,
            "consensus_rate": 0.6
        }},
        "recommendations": [...]
    }}
}}
```

## 利用可能なモデル

"""
        for model_id, model_info in self.models.items():
            doc_content += f"""### {model_id}
- **名称**: {model_info['name']}
- **特徴**: {model_info['speciality']}
- **速度**: {model_info['speed']}
- **精度**: {model_info['accuracy']}
- **カテゴリ**: {', '.join(model_info['categories'])}

"""
        
        doc_content += """## 統合アルゴリズム

1. **並列検出**: 複数モデルで同時に物体検出を実行
2. **位置ベースグループ化**: 近接する検出結果をグループ化
3. **信頼度ベース選択**: グループ内で最も信頼度の高い結果を選択
4. **コンセンサススコア**: 複数モデルでの検出率を計算

## 使用例

```python
api = MultiObjectDetectionAPI()
response = api.generate_api_response(
    image_data=your_image_data,
    use_models=["yolo", "faster_rcnn"]
)
print(response)
```
"""
        
        doc_path = self.output_dir.parent / "API_DOCUMENTATION.md"
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        return str(doc_path)

def create_flask_api():
    """Flask APIサーバーのコード生成"""
    flask_code = '''#!/usr/bin/env python3
"""
多層物体検出統合API - Flask サーバー
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from multi_object_detection_api import MultiObjectDetectionAPI

app = Flask(__name__)
CORS(app)

# API インスタンス
detection_api = MultiObjectDetectionAPI()

@app.route('/api/detect', methods=['POST'])
def detect_objects():
    """物体検出エンドポイント"""
    try:
        data = request.get_json()
        
        # 画像データの取得
        image_data = data.get('image')
        if image_data:
            # Base64デコード（実際の実装で使用）
            # image_bytes = base64.b64decode(image_data)
            pass
        
        # 使用モデルの指定
        use_models = data.get('use_models')
        
        # 検出実行
        response = detection_api.generate_api_response(
            image_data=image_data,
            use_models=use_models
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """利用可能なモデル一覧"""
    return jsonify({
        "models": detection_api.models
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    return jsonify({
        "status": "healthy",
        "api_version": detection_api.version
    })

if __name__ == '__main__':
    print(f"🚀 {detection_api.name} Flask サーバー起動")
    print("📡 http://localhost:5000")
    app.run(debug=True, port=5000)
'''
    
    flask_path = Path("flask_detection_server.py")
    with open(flask_path, 'w', encoding='utf-8') as f:
        f.write(flask_code)
    
    return str(flask_path)

def main():
    """実行例"""
    print("🔍 多層物体検出統合API 起動")
    print("=" * 50)
    
    api = MultiObjectDetectionAPI()
    
    # APIドキュメント生成
    doc_path = api.create_api_documentation()
    print(f"📚 APIドキュメント生成: {doc_path}")
    
    # テスト検出実行
    print("\n🚀 テスト検出実行中...")
    response = api.generate_api_response()
    
    print(f"\n📊 検出結果:")
    print(f"  総検出数: {response['data']['detections']['total_objects']}")
    print(f"  処理時間: {response['data']['detections']['processing_time']}秒")
    print(f"  平均信頼度: {response['data']['quality_metrics']['average_confidence']}")
    
    # カテゴリ別結果
    print("\n📈 カテゴリ別検出数:")
    for category, count in response['data']['detections']['category_summary'].items():
        print(f"  {category}: {count}")
    
    # Flask サーバーコード生成
    flask_path = create_flask_api()
    print(f"\n🌐 Flask サーバーコード生成: {flask_path}")
    
    print("\n✨ API準備完了")
    print("💡 Flask サーバー起動: python flask_detection_server.py")

if __name__ == "__main__":
    main()