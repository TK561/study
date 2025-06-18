"""
適応分類システム
Adaptive classification system with dynamic dataset selection
"""

import time
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from PIL import Image
import torch

try:
    from transformers import CLIPProcessor, CLIPModel
    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False


@dataclass
class ClassificationResult:
    """分類結果"""
    object_id: str
    category: str
    specialized_dataset: str
    general_results: Dict[str, float]
    specialized_results: Dict[str, float]
    improvement_score: float
    confidence: float
    processing_time: float
    metadata: Dict[str, Any]


class DatasetManager:
    """データセット管理システム"""
    
    def __init__(self, config):
        self.config = config
        self.dataset_info = self._initialize_dataset_info()
        self.category_datasets = config.datasets.category_datasets
        self.category_labels = config.datasets.category_labels
    
    def _initialize_dataset_info(self) -> Dict[str, Dict[str, Any]]:
        """データセット情報の初期化"""
        return {
            "LFW": {
                "full_name": "Labeled Faces in the Wild",
                "year": 2007,
                "size": "13,000+ images",
                "specialization": "顔認識・人物識別特化",
                "advantages": [
                    "顔の表情・角度の多様性に対応",
                    "自然環境での人物認識に最適化",
                    "年齢・性別・表情の細分化分類"
                ]
            },
            "ImageNet-Animals": {
                "full_name": "ImageNet Animal Classes",
                "year": 2009,
                "size": "1.2M+ animal images",
                "specialization": "動物分類・行動認識特化",
                "advantages": [
                    "豊富な動物種カバレッジ（1000+種）",
                    "動物の行動・ポーズの多様性",
                    "自然環境での動物認識"
                ]
            },
            "Food-101": {
                "full_name": "Food-101 Dataset",
                "year": 2014,
                "size": "101,000 images",
                "specialization": "料理・食材認識特化",
                "advantages": [
                    "料理の視覚的特徴を最適化",
                    "食材・調理法の細分化",
                    "文化的料理の多様性対応"
                ]
            },
            "Places365": {
                "full_name": "Places365 Scene Dataset",
                "year": 2017,
                "size": "10M+ scene images",
                "specialization": "シーン・環境認識特化",
                "advantages": [
                    "環境の文脈理解（季節・時間）",
                    "地理的・気候的多様性",
                    "シーンの意味的理解"
                ]
            },
            "OpenBuildings": {
                "full_name": "Open Buildings Dataset",
                "year": 2021,
                "size": "1B+ building footprints",
                "specialization": "建築物・構造物認識特化",
                "advantages": [
                    "建築様式の詳細分類",
                    "構造的特徴の認識",
                    "文化的・歴史的建築の理解"
                ]
            },
            "Objects365-Furniture": {
                "full_name": "Objects365 Furniture Classes",
                "year": 2019,
                "size": "2M+ object instances",
                "specialization": "家具・日用品認識特化",
                "advantages": [
                    "室内環境の理解",
                    "家具の機能的分類",
                    "生活空間の認識"
                ]
            },
            "Pascal-VOC-Vehicle": {
                "full_name": "Pascal VOC Vehicle Classes",
                "year": 2012,
                "size": "Vehicle-focused subset",
                "specialization": "車両・交通手段認識特化",
                "advantages": [
                    "交通環境での認識最適化",
                    "車両タイプの細分化",
                    "動的な物体追跡"
                ]
            },
            "PlantVillage": {
                "full_name": "PlantVillage Dataset",
                "year": 2016,
                "size": "50,000+ plant images",
                "specialization": "植物・農作物認識特化",
                "advantages": [
                    "植物の健康診断",
                    "農業・園芸への実用応用",
                    "病気・害虫の早期発見"
                ]
            },
            "COCO": {
                "full_name": "Common Objects in Context",
                "year": 2014,
                "size": "330K+ images",
                "specialization": "汎用物体認識",
                "advantages": [
                    "幅広いカテゴリカバレッジ",
                    "標準的なベンチマーク",
                    "バランスの取れた分布"
                ]
            }
        }
    
    def get_specialized_dataset(self, category: str) -> str:
        """カテゴリに対応する特化データセットを取得"""
        return self.category_datasets.get(category, "COCO")
    
    def get_specialized_labels(self, category: str) -> List[str]:
        """カテゴリに対応する特化ラベルを取得"""
        return self.category_labels.get(category, self.category_labels["general"])
    
    def get_dataset_info(self, dataset_name: str) -> Dict[str, Any]:
        """データセット情報を取得"""
        return self.dataset_info.get(dataset_name, {})
    
    def calculate_specialization_advantage(self, category: str, specialized_confidence: float, general_confidence: float) -> Dict[str, Any]:
        """特化データセットの優位性を計算"""
        dataset_name = self.get_specialized_dataset(category)
        dataset_info = self.get_dataset_info(dataset_name)
        
        improvement = specialized_confidence - general_confidence
        improvement_percent = (improvement / general_confidence * 100) if general_confidence > 0 else 0
        
        return {
            "dataset_name": dataset_name,
            "dataset_info": dataset_info,
            "improvement_absolute": improvement,
            "improvement_percent": improvement_percent,
            "specialized_confidence": specialized_confidence,
            "general_confidence": general_confidence,
            "advantages": dataset_info.get("advantages", [])
        }


class CLIPClassifier:
    """CLIP分類エンジン"""
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32", device: str = "auto"):
        self.model_name = model_name
        self.device = self._determine_device(device)
        self.processor = None
        self.model = None
        self.is_loaded = False
    
    def _determine_device(self, device: str) -> str:
        """最適なデバイスを決定"""
        if device == "auto":
            if CLIP_AVAILABLE and torch:
                return "cuda" if torch.cuda.is_available() else "cpu"
            return "cpu"
        return device
    
    def load_model(self) -> bool:
        """CLIPモデルを読み込み"""
        try:
            if CLIP_AVAILABLE:
                print(f"Loading CLIP model: {self.model_name}")
                self.processor = CLIPProcessor.from_pretrained(self.model_name)
                self.model = CLIPModel.from_pretrained(self.model_name)
                
                if self.device == "cuda":
                    self.model.to(self.device)
                
                self.is_loaded = True
                print(f"CLIP model loaded on {self.device}")
            else:
                print("CLIP not available, using simulation mode")
                self.is_loaded = True
            return True
        except Exception as e:
            print(f"Failed to load CLIP model: {e}")
            self.is_loaded = False
            return False
    
    def classify_image(self, image: Image.Image, labels: List[str]) -> Dict[str, float]:
        """画像をラベルで分類"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            if CLIP_AVAILABLE and self.model and self.processor:
                # Real CLIP classification
                texts = [f"a photo of {label}" for label in labels]
                
                inputs = self.processor(
                    text=texts, 
                    images=image, 
                    return_tensors="pt", 
                    padding=True
                )
                
                if self.device == "cuda":
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    logits_per_image = outputs.logits_per_image
                    probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
                
                return {labels[i]: float(probs[i]) for i in range(len(labels))}
            else:
                # Simulation mode
                return self._simulate_classification(labels)
                
        except Exception as e:
            print(f"CLIP classification error: {e}")
            return self._simulate_classification(labels)
    
    def _simulate_classification(self, labels: List[str]) -> Dict[str, float]:
        """分類シミュレーション"""
        # Generate random but realistic scores
        scores = {}
        for i, label in enumerate(labels):
            # First label gets slightly higher score
            base_score = 0.3 if i == 0 else 0.1
            random_score = np.random.uniform(0.1, 0.4)
            scores[label] = base_score + random_score
        
        # Normalize scores
        total = sum(scores.values())
        return {label: score / total for label, score in scores.items()}


class AdaptiveClassificationSystem:
    """適応分類システム"""
    
    def __init__(self, config):
        self.config = config
        
        # コンポーネント初期化
        self.dataset_manager = DatasetManager(config)
        self.clip_classifier = CLIPClassifier(
            model_name=config.models.clip_model_name,
            device=config.models.device
        )
        
        # 処理履歴
        self.classification_history = []
    
    def classify_adaptive(self, image: Image.Image, category: str, object_id: str = "unknown") -> ClassificationResult:
        """適応的分類の実行"""
        start_time = time.time()
        
        print(f"Starting adaptive classification for object: {object_id}")
        print(f"  Category: {category}")
        
        # 1. データセット選択
        specialized_dataset = self.dataset_manager.get_specialized_dataset(category)
        specialized_labels = self.dataset_manager.get_specialized_labels(category)
        general_labels = self.dataset_manager.get_specialized_labels("general")
        
        print(f"  Specialized dataset: {specialized_dataset}")
        print(f"  Specialized labels: {len(specialized_labels)}")
        print(f"  General labels: {len(general_labels)}")
        
        # 2. 汎用分類実行
        print("  Performing general classification...")
        general_results = self.clip_classifier.classify_image(image, general_labels)
        
        # 3. 特化分類実行
        print("  Performing specialized classification...")
        specialized_results = self.clip_classifier.classify_image(image, specialized_labels)
        
        # 4. 改善スコア計算
        improvement_score = self._calculate_improvement_score(specialized_results, general_results)
        
        # 5. 最高確信度取得
        general_confidence = max(general_results.values()) if general_results else 0.0
        specialized_confidence = max(specialized_results.values()) if specialized_results else 0.0
        
        processing_time = time.time() - start_time
        
        # 6. 結果構築
        result = ClassificationResult(
            object_id=object_id,
            category=category,
            specialized_dataset=specialized_dataset,
            general_results=general_results,
            specialized_results=specialized_results,
            improvement_score=improvement_score,
            confidence=specialized_confidence,
            processing_time=processing_time,
            metadata={
                "general_confidence": general_confidence,
                "specialized_confidence": specialized_confidence,
                "dataset_info": self.dataset_manager.get_dataset_info(specialized_dataset),
                "labels_used": {
                    "general": general_labels,
                    "specialized": specialized_labels
                }
            }
        )
        
        self.classification_history.append(result)
        
        print(f"  General top confidence: {general_confidence:.4f}")
        print(f"  Specialized top confidence: {specialized_confidence:.4f}")
        print(f"  Improvement: {improvement_score:.2f}%")
        print(f"  Processing time: {processing_time:.3f}s")
        
        return result
    
    def _calculate_improvement_score(self, specialized_results: Dict[str, float], 
                                   general_results: Dict[str, float]) -> float:
        """改善スコア計算"""
        if not specialized_results or not general_results:
            return 0.0
        
        specialized_max = max(specialized_results.values())
        general_max = max(general_results.values())
        
        if general_max > 0:
            improvement = ((specialized_max - general_max) / general_max) * 100
            return max(0.0, improvement)
        
        return 0.0
    
    def batch_classify(self, image_category_pairs: List[Tuple[Image.Image, str]], 
                      progress_callback=None) -> List[ClassificationResult]:
        """バッチ分類処理"""
        results = []
        total_pairs = len(image_category_pairs)
        
        print(f"Starting batch adaptive classification: {total_pairs} images")
        
        for i, (image, category) in enumerate(image_category_pairs):
            try:
                object_id = f"batch_object_{i+1}"
                result = self.classify_adaptive(image, category, object_id)
                results.append(result)
                
                if progress_callback:
                    progress_callback(i + 1, total_pairs)
                
                print(f"  Progress: {i+1}/{total_pairs}")
                
            except Exception as e:
                print(f"  Error processing image {i+1}: {e}")
                continue
        
        print(f"Batch classification complete: {len(results)}/{total_pairs} successful")
        return results
    
    def analyze_performance(self) -> Dict[str, Any]:
        """性能分析"""
        if not self.classification_history:
            return {"message": "No classification history available"}
        
        # 基本統計
        total_classifications = len(self.classification_history)
        avg_processing_time = sum(r.processing_time for r in self.classification_history) / total_classifications
        avg_improvement = sum(r.improvement_score for r in self.classification_history) / total_classifications
        
        # カテゴリ別分析
        category_performance = {}
        for result in self.classification_history:
            category = result.category
            if category not in category_performance:
                category_performance[category] = {
                    'count': 0,
                    'improvements': [],
                    'confidence_gains': []
                }
            
            category_performance[category]['count'] += 1
            category_performance[category]['improvements'].append(result.improvement_score)
            
            general_conf = result.metadata.get('general_confidence', 0)
            specialized_conf = result.metadata.get('specialized_confidence', 0)
            category_performance[category]['confidence_gains'].append(specialized_conf - general_conf)
        
        # カテゴリ別統計計算
        for category, data in category_performance.items():
            data['avg_improvement'] = np.mean(data['improvements'])
            data['avg_confidence_gain'] = np.mean(data['confidence_gains'])
            data['positive_improvements'] = sum(1 for imp in data['improvements'] if imp > 0)
            data['improvement_rate'] = data['positive_improvements'] / data['count'] * 100
        
        # データセット使用統計
        dataset_usage = {}
        for result in self.classification_history:
            dataset = result.specialized_dataset
            if dataset not in dataset_usage:
                dataset_usage[dataset] = {
                    'count': 0,
                    'avg_improvement': 0,
                    'categories': set()
                }
            dataset_usage[dataset]['count'] += 1
            dataset_usage[dataset]['categories'].add(result.category)
        
        # データセット別平均改善率
        for dataset in dataset_usage:
            dataset_results = [r for r in self.classification_history if r.specialized_dataset == dataset]
            dataset_usage[dataset]['avg_improvement'] = np.mean([r.improvement_score for r in dataset_results])
            dataset_usage[dataset]['categories'] = list(dataset_usage[dataset]['categories'])
        
        return {
            'total_classifications': total_classifications,
            'average_processing_time': avg_processing_time,
            'average_improvement': avg_improvement,
            'positive_improvements': sum(1 for r in self.classification_history if r.improvement_score > 0),
            'improvement_rate': sum(1 for r in self.classification_history if r.improvement_score > 0) / total_classifications * 100,
            'category_performance': category_performance,
            'dataset_usage': dataset_usage,
            'performance_summary': {
                'best_category': max(category_performance.items(), key=lambda x: x[1]['avg_improvement'])[0] if category_performance else None,
                'best_dataset': max(dataset_usage.items(), key=lambda x: x[1]['avg_improvement'])[0] if dataset_usage else None,
                'overall_success_rate': sum(1 for r in self.classification_history if r.improvement_score > 5) / total_classifications * 100
            }
        }
    
    def get_dataset_recommendations(self, category: str) -> Dict[str, Any]:
        """カテゴリに対するデータセット推薦"""
        specialized_dataset = self.dataset_manager.get_specialized_dataset(category)
        dataset_info = self.dataset_manager.get_dataset_info(specialized_dataset)
        
        # 過去の性能データがあれば活用
        historical_performance = None
        if self.classification_history:
            category_results = [r for r in self.classification_history if r.category == category]
            if category_results:
                avg_improvement = np.mean([r.improvement_score for r in category_results])
                historical_performance = {
                    'sample_size': len(category_results),
                    'average_improvement': avg_improvement,
                    'success_rate': sum(1 for r in category_results if r.improvement_score > 0) / len(category_results) * 100
                }
        
        return {
            'recommended_dataset': specialized_dataset,
            'dataset_info': dataset_info,
            'historical_performance': historical_performance,
            'expected_advantages': dataset_info.get('advantages', []),
            'confidence': 'high' if historical_performance and historical_performance['success_rate'] > 80 else 'medium'
        }
    
    def export_results(self, filepath: str, format: str = "json"):
        """結果をエクスポート"""
        if format == "json":
            import json
            export_data = {
                'classification_results': [
                    {
                        'object_id': r.object_id,
                        'category': r.category,
                        'specialized_dataset': r.specialized_dataset,
                        'improvement_score': r.improvement_score,
                        'confidence': r.confidence,
                        'processing_time': r.processing_time,
                        'general_results': r.general_results,
                        'specialized_results': r.specialized_results
                    }
                    for r in self.classification_history
                ],
                'performance_analysis': self.analyze_performance(),
                'export_metadata': {
                    'total_results': len(self.classification_history),
                    'export_timestamp': time.time()
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        elif format == "csv":
            import pandas as pd
            df_data = []
            for r in self.classification_history:
                df_data.append({
                    'object_id': r.object_id,
                    'category': r.category,
                    'specialized_dataset': r.specialized_dataset,
                    'improvement_score': r.improvement_score,
                    'confidence': r.confidence,
                    'processing_time': r.processing_time,
                    'general_top_confidence': r.metadata.get('general_confidence', 0),
                    'specialized_top_confidence': r.metadata.get('specialized_confidence', 0)
                })
            
            df = pd.DataFrame(df_data)
            df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"Results exported to: {filepath}")


def create_classification_demo():
    """分類システムのデモ"""
    from ..config import get_demo_config
    
    config = get_demo_config()
    system = AdaptiveClassificationSystem(config)
    
    print("Adaptive Classification System Demo")
    print("=" * 50)
    
    # デモ用画像とカテゴリのペア（シミュレーション）
    demo_cases = [
        ("business_person.jpg", "person"),
        ("golden_retriever.jpg", "animal"),
        ("italian_pizza.jpg", "food"),
        ("modern_office.jpg", "building"),
        ("leather_sofa.jpg", "furniture"),
        ("sports_car.jpg", "vehicle"),
        ("cherry_tree.jpg", "plant"),
        ("mountain_view.jpg", "landscape")
    ]
    
    print(f"Demo cases: {len(demo_cases)}")
    
    # 各ケースを処理
    for i, (image_name, category) in enumerate(demo_cases, 1):
        print(f"\nDemo case {i}: {image_name}")
        
        # ダミー画像（実際の実装では実画像を使用）
        dummy_image = Image.new('RGB', (224, 224), color='white')
        
        try:
            result = system.classify_adaptive(dummy_image, category, f"demo_object_{i}")
            
            print(f"  Category: {result.category}")
            print(f"  Dataset: {result.specialized_dataset}")
            print(f"  Improvement: {result.improvement_score:.1f}%")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # 性能分析
    print(f"\nPerformance Analysis:")
    analysis = system.analyze_performance()
    print(f"  Total classifications: {analysis['total_classifications']}")
    print(f"  Average improvement: {analysis['average_improvement']:.1f}%")
    print(f"  Success rate: {analysis['improvement_rate']:.1f}%")
    
    # 結果エクスポート
    system.export_results("demo_classification_results.json")
    
    return system, analysis


if __name__ == "__main__":
    demo_system, demo_analysis = create_classification_demo()
