"""
完全統合システム
Complete integration system combining detection, semantic analysis, and classification
"""

import time
import numpy as np
import cv2
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from PIL import Image
import json
from pathlib import Path

from .detection_system import MultiLayerDetectionSystem, DetectedObject, DetectionResult
from .semantic_analyzer import SemanticAnalyzer, CategoryResult
from .classification_system import AdaptiveClassificationSystem, ClassificationResult


@dataclass
class ObjectProcessingResult:
    """個別物体の処理結果"""
    object_id: str
    bbox: Tuple[float, float, float, float]
    detected_class: str
    detector_layer: str
    
    # Semantic analysis results
    caption: str
    semantic_category: str
    category_confidence: float
    
    # Classification results
    specialized_dataset: str
    classification_result: ClassificationResult
    
    # Performance metrics
    improvement_score: float
    processing_time: float


@dataclass
class ProcessingResult:
    """完全処理結果"""
    image_path: str
    image_shape: Tuple[int, int, int]
    
    # Detection results
    detection_result: DetectionResult
    
    # Object-level results
    object_results: List[ObjectProcessingResult]
    
    # Scene-level analysis
    scene_summary: str
    dominant_categories: Dict[str, int]
    
    # Performance metrics
    total_processing_time: float
    average_improvement: float
    datasets_utilized: List[str]
    
    # System metadata
    processing_metadata: Dict[str, Any]


class CompleteIntegratedSystem:
    """完全統合システムのメインクラス"""
    
    def __init__(self, config):
        self.config = config
        
        # サブシステム初期化
        self.detection_system = MultiLayerDetectionSystem(config)
        self.semantic_analyzer = SemanticAnalyzer(config)
        self.classification_system = AdaptiveClassificationSystem(config)
        
        # 処理履歴
        self.processing_history = []
        
        print("Complete Integrated System initialized")
    
    def process_image(self, image_path: str, image: Optional[np.ndarray] = None) -> ProcessingResult:
        """画像の完全統合処理"""
        start_time = time.time()
        
        print(f"Starting complete integrated processing: {image_path}")
        
        # 1. 画像読み込み
        if image is None:
            image = self._load_image(image_path)
        
        # 2. 4層統合物体検出
        print("Phase 1: Multi-layer object detection")
        detection_result = self.detection_system.detect_comprehensive(image, image_path)
        
        # 3. 各物体の個別処理
        print("Phase 2: Object-level semantic classification")
        object_results = []
        
        for i, detected_obj in enumerate(detection_result.detected_objects):
            print(f"  Processing object {i+1}/{len(detection_result.detected_objects)}: {detected_obj.class_name}")
            
            # 物体領域抽出
            object_region = self._extract_object_region(image, detected_obj)
            
            # 個別物体処理
            obj_result = self._process_single_object(detected_obj, object_region, image_path)
            object_results.append(obj_result)
        
        # 4. シーン全体分析
        print("Phase 3: Scene-level analysis")
        scene_analysis = self._analyze_scene(object_results)
        
        # 5. 統合結果構築
        total_time = time.time() - start_time
        
        result = ProcessingResult(
            image_path=image_path,
            image_shape=image.shape,
            detection_result=detection_result,
            object_results=object_results,
            scene_summary=scene_analysis['summary'],
            dominant_categories=scene_analysis['categories'],
            total_processing_time=total_time,
            average_improvement=self._calculate_average_improvement(object_results),
            datasets_utilized=list(set(obj.specialized_dataset for obj in object_results)),
            processing_metadata={
                'detection_layers_used': len(self.detection_system.detectors),
                'objects_processed': len(object_results),
                'semantic_analyzer_available': self.semantic_analyzer.caption_generator.is_loaded,
                'clip_classifier_available': self.classification_system.clip_classifier.is_loaded,
                'processing_timestamp': time.time()
            }
        )
        
        self.processing_history.append(result)
        
        print(f"Complete processing finished: {total_time:.2f}s")
        self._display_summary(result)
        
        return result
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """画像読み込み"""
        try:
            if isinstance(image_path, str) and Path(image_path).exists():
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError(f"Failed to load image: {image_path}")
                return image
            else:
                # Generate dummy image for demo
                print(f"Generating dummy image for: {image_path}")
                return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        except Exception as e:
            print(f"Image loading error: {e}")
            return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    def _extract_object_region(self, image: np.ndarray, detected_obj: DetectedObject) -> np.ndarray:
        """物体領域抽出"""
        x1, y1, x2, y2 = detected_obj.bbox
        h, w = image.shape[:2]
        
        # Denormalize coordinates
        x1, y1, x2, y2 = int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h)
        
        # Ensure coordinates are within image bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        # Extract region
        region = image[y1:y2, x1:x2]
        
        # Ensure minimum size
        if region.size == 0:
            region = image[h//4:3*h//4, w//4:3*w//4]
        
        return region
    
    def _process_single_object(self, detected_obj: DetectedObject, object_region: np.ndarray, 
                             image_path: str) -> ObjectProcessingResult:
        """単一物体の完全処理"""
        obj_start_time = time.time()
        
        # 1. 意味分析（キャプション生成 + カテゴリ判定）
        category_result = self.semantic_analyzer.analyze_image_semantics(
            object_region, 
            f"{image_path}_{detected_obj.object_id}"
        )
        
        # 2. 適応分類
        pil_image = Image.fromarray(cv2.cvtColor(object_region, cv2.COLOR_BGR2RGB))
        classification_result = self.classification_system.classify_adaptive(
            pil_image, 
            category_result.category, 
            detected_obj.object_id
        )
        
        processing_time = time.time() - obj_start_time
        
        # 3. 結果統合
        return ObjectProcessingResult(
            object_id=detected_obj.object_id,
            bbox=detected_obj.bbox,
            detected_class=detected_obj.class_name,
            detector_layer=detected_obj.detector_layer,
            caption=category_result.metadata['caption'],
            semantic_category=category_result.category,
            category_confidence=category_result.confidence,
            specialized_dataset=classification_result.specialized_dataset,
            classification_result=classification_result,
            improvement_score=classification_result.improvement_score,
            processing_time=processing_time
        )
    
    def _analyze_scene(self, object_results: List[ObjectProcessingResult]) -> Dict[str, Any]:
        """シーン全体分析"""
        if not object_results:
            return {
                'summary': 'No objects detected in the scene',
                'categories': {},
                'scene_type': 'empty'
            }
        
        # カテゴリ分布
        categories = {}
        for obj_result in object_results:
            category = obj_result.semantic_category
            categories[category] = categories.get(category, 0) + 1
        
        # シーンタイプ推定
        scene_type = self._determine_scene_type(categories)
        
        # シーン要約生成
        object_summary = ', '.join([f"{cat}({count}個)" for cat, count in categories.items()])
        scene_summary = f"{scene_type}: {object_summary}を含む複雑な視覚シーン"
        
        return {
            'summary': scene_summary,
            'categories': categories,
            'scene_type': scene_type
        }
    
    def _determine_scene_type(self, categories: Dict[str, int]) -> str:
        """シーンタイプ判定"""
        if 'person' in categories and 'furniture' in categories:
            return "室内人物活動シーン"
        elif 'vehicle' in categories and 'building' in categories:
            return "都市交通シーン"
        elif 'plant' in categories and 'landscape' in categories:
            return "自然環境シーン"
        elif 'food' in categories and 'person' in categories:
            return "食事・料理シーン"
        else:
            return "複合オブジェクトシーン"
    
    def _calculate_average_improvement(self, object_results: List[ObjectProcessingResult]) -> float:
        """平均改善率計算"""
        if not object_results:
            return 0.0
        
        improvements = [obj.improvement_score for obj in object_results]
        return sum(improvements) / len(improvements)
    
    def _display_summary(self, result: ProcessingResult):
        """結果サマリー表示"""
        print(f"\nProcessing Summary:")
        print(f"  Total objects: {len(result.object_results)}")
        print(f"  Processing time: {result.total_processing_time:.2f}s")
        print(f"  Average improvement: {result.average_improvement:.1f}%")
        print(f"  Datasets utilized: {len(result.datasets_utilized)}")
        print(f"  Scene: {result.scene_summary}")
        
        if result.object_results:
            print(f"\nTop object results:")
            for i, obj in enumerate(result.object_results[:3], 1):
                print(f"    {i}. {obj.detected_class} -> {obj.semantic_category}")
                print(f"       Dataset: {obj.specialized_dataset}")
                print(f"       Improvement: {obj.improvement_score:.1f}%")
    
    def batch_process(self, image_paths: List[str], progress_callback=None) -> List[ProcessingResult]:
        """バッチ処理"""
        results = []
        total_images = len(image_paths)
        
        print(f"Starting batch processing: {total_images} images")
        
        for i, image_path in enumerate(image_paths):
            try:
                print(f"\nBatch {i+1}/{total_images}: {Path(image_path).name}")
                
                result = self.process_image(image_path)
                results.append(result)
                
                if progress_callback:
                    progress_callback(i + 1, total_images)
                
            except Exception as e:
                print(f"  Error processing {image_path}: {e}")
                continue
        
        print(f"\nBatch processing complete: {len(results)}/{total_images} successful")
        self._display_batch_statistics(results)
        
        return results
    
    def _display_batch_statistics(self, results: List[ProcessingResult]):
        """バッチ統計表示"""
        if not results:
            return
        
        total_objects = sum(len(r.object_results) for r in results)
        total_time = sum(r.total_processing_time for r in results)
        avg_improvement = sum(r.average_improvement for r in results) / len(results)
        
        all_datasets = set()
        for result in results:
            all_datasets.update(result.datasets_utilized)
        
        print(f"\nBatch Statistics:")
        print(f"  Images processed: {len(results)}")
        print(f"  Total objects detected: {total_objects}")
        print(f"  Total processing time: {total_time:.2f}s")
        print(f"  Average time per image: {total_time/len(results):.2f}s")
        print(f"  Processing throughput: {total_objects/total_time:.1f} objects/s")
        print(f"  System average improvement: {avg_improvement:.1f}%")
        print(f"  Unique datasets utilized: {len(all_datasets)}")
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """システム統計取得"""
        if not self.processing_history:
            return {"message": "No processing history available"}
        
        # 基本統計
        total_images = len(self.processing_history)
        total_objects = sum(len(r.object_results) for r in self.processing_history)
        total_time = sum(r.total_processing_time for r in self.processing_history)
        
        # 改善率統計
        all_improvements = []
        for result in self.processing_history:
            for obj in result.object_results:
                all_improvements.append(obj.improvement_score)
        
        # カテゴリ統計
        category_stats = {}
        for result in self.processing_history:
            for obj in result.object_results:
                category = obj.semantic_category
                if category not in category_stats:
                    category_stats[category] = {
                        'count': 0,
                        'improvements': [],
                        'datasets': set()
                    }
                category_stats[category]['count'] += 1
                category_stats[category]['improvements'].append(obj.improvement_score)
                category_stats[category]['datasets'].add(obj.specialized_dataset)
        
        # カテゴリ別平均計算
        for category, stats in category_stats.items():
            stats['avg_improvement'] = np.mean(stats['improvements'])
            stats['datasets'] = list(stats['datasets'])
        
        # データセット統計
        dataset_stats = {}
        for result in self.processing_history:
            for obj in result.object_results:
                dataset = obj.specialized_dataset
                if dataset not in dataset_stats:
                    dataset_stats[dataset] = {
                        'usage_count': 0,
                        'improvements': [],
                        'categories': set()
                    }
                dataset_stats[dataset]['usage_count'] += 1
                dataset_stats[dataset]['improvements'].append(obj.improvement_score)
                dataset_stats[dataset]['categories'].add(obj.semantic_category)
        
        # データセット別平均計算
        for dataset, stats in dataset_stats.items():
            stats['avg_improvement'] = np.mean(stats['improvements'])
            stats['categories'] = list(stats['categories'])
        
        return {
            'overall_statistics': {
                'total_images_processed': total_images,
                'total_objects_detected': total_objects,
                'total_processing_time': total_time,
                'average_objects_per_image': total_objects / total_images,
                'average_processing_time_per_image': total_time / total_images,
                'processing_throughput': total_objects / total_time if total_time > 0 else 0
            },
            'improvement_statistics': {
                'overall_average_improvement': np.mean(all_improvements) if all_improvements else 0,
                'improvement_std': np.std(all_improvements) if all_improvements else 0,
                'positive_improvements': sum(1 for imp in all_improvements if imp > 0),
                'improvement_rate': sum(1 for imp in all_improvements if imp > 0) / len(all_improvements) * 100 if all_improvements else 0
            },
            'category_statistics': category_stats,
            'dataset_statistics': dataset_stats,
            'system_performance': {
                'detection_system_active': len(self.detection_system.detectors),
                'semantic_analyzer_active': self.semantic_analyzer.caption_generator.is_loaded,
                'classification_system_active': self.classification_system.clip_classifier.is_loaded
            }
        }
    
    def save_results(self, output_path: str, include_detailed: bool = True):
        """結果保存"""
        save_data = {
            'system_info': {
                'name': 'Complete Integrated System',
                'version': self.config.version,
                'timestamp': time.time(),
                'configuration': {
                    'detection_layers': len(self.detection_system.detectors),
                    'supported_categories': len(self.config.semantic.supported_categories),
                    'specialized_datasets': len(self.config.datasets.category_datasets)
                }
            },
            'processing_summary': self.get_system_statistics()
        }
        
        if include_detailed:
            save_data['detailed_results'] = []
            for result in self.processing_history:
                detailed_result = {
                    'image_path': result.image_path,
                    'image_shape': result.image_shape,
                    'total_processing_time': result.total_processing_time,
                    'scene_summary': result.scene_summary,
                    'dominant_categories': result.dominant_categories,
                    'average_improvement': result.average_improvement,
                    'datasets_utilized': result.datasets_utilized,
                    'object_results': [
                        {
                            'object_id': obj.object_id,
                            'detected_class': obj.detected_class,
                            'detector_layer': obj.detector_layer,
                            'semantic_category': obj.semantic_category,
                            'category_confidence': obj.category_confidence,
                            'specialized_dataset': obj.specialized_dataset,
                            'improvement_score': obj.improvement_score,
                            'processing_time': obj.processing_time
                        }
                        for obj in result.object_results
                    ],
                    'detection_metadata': {
                        'total_detected': len(result.detection_result.detected_objects),
                        'layer_contributions': result.detection_result.layer_contributions
                    }
                }
                save_data['detailed_results'].append(detailed_result)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"Results saved to: {output_path}")
    
    def create_performance_report(self) -> str:
        """性能レポート生成"""
        stats = self.get_system_statistics()
        
        if 'message' in stats:
            return "No data available for performance report"
        
        overall = stats['overall_statistics']
        improvement = stats['improvement_statistics']
        
        report = f"""
# Complete Integrated System Performance Report

## Overall Performance
- **Images Processed**: {overall['total_images_processed']}
- **Objects Detected**: {overall['total_objects_detected']}
- **Average Objects per Image**: {overall['average_objects_per_image']:.1f}
- **Processing Throughput**: {overall['processing_throughput']:.1f} objects/second

## Improvement Analysis
- **Average Improvement**: {improvement['overall_average_improvement']:.1f}%
- **Positive Improvements**: {improvement['positive_improvements']} objects
- **Success Rate**: {improvement['improvement_rate']:.1f}%

## Category Performance
"""
        
        if 'category_statistics' in stats:
            for category, cat_stats in stats['category_statistics'].items():
                report += f"### {category.title()} Category\n"
                report += f"- Objects processed: {cat_stats['count']}\n"
                report += f"- Average improvement: {cat_stats['avg_improvement']:.1f}%\n"
                report += f"- Datasets used: {', '.join(cat_stats['datasets'])}\n\n"
        
        report += "## Dataset Utilization\n"
        if 'dataset_statistics' in stats:
            for dataset, ds_stats in stats['dataset_statistics'].items():
                report += f"### {dataset}\n"
                report += f"- Usage count: {ds_stats['usage_count']}\n"
                report += f"- Average improvement: {ds_stats['avg_improvement']:.1f}%\n"
                report += f"- Categories: {', '.join(ds_stats['categories'])}\n\n"
        
        return report
    
    def export_performance_analysis(self, output_dir: str = "results"):
        """性能分析エクスポート"""
        import os
        from datetime import datetime
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON統計
        stats_file = os.path.join(output_dir, f"system_statistics_{timestamp}.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.get_system_statistics(), f, ensure_ascii=False, indent=2)
        
        # レポート
        report_file = os.path.join(output_dir, f"performance_report_{timestamp}.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(self.create_performance_report())
        
        # 詳細結果
        detailed_file = os.path.join(output_dir, f"detailed_results_{timestamp}.json")
        self.save_results(detailed_file, include_detailed=True)
        
        print(f"Performance analysis exported to: {output_dir}")
        print(f"  - Statistics: {stats_file}")
        print(f"  - Report: {report_file}")
        print(f"  - Detailed results: {detailed_file}")


def create_integration_demo():
    """統合システムデモ"""
    from ..config import get_demo_config
    
    config = get_demo_config()
    system = CompleteIntegratedSystem(config)
    
    print("Complete Integrated System Demo")
    print("=" * 60)
    
    # デモ用テストケース
    test_images = [
        "demo_office_meeting.jpg",
        "demo_kitchen_cooking.jpg",
        "demo_street_scene.jpg",
        "demo_living_room.jpg"
    ]
    
    print(f"Demo test cases: {len(test_images)}")
    
    # 単一画像処理デモ
    print(f"\nSingle Image Processing Demo:")
    single_result = system.process_image(test_images[0])
    
    # バッチ処理デモ
    print(f"\nBatch Processing Demo:")
    batch_results = system.batch_process(test_images)
    
    # 性能分析
    print(f"\nPerformance Analysis:")
    stats = system.get_system_statistics()
    if 'overall_statistics' in stats:
        overall = stats['overall_statistics']
        improvement = stats['improvement_statistics']
        
        print(f"  Total images: {overall['total_images_processed']}")
        print(f"  Total objects: {overall['total_objects_detected']}")
        print(f"  Average improvement: {improvement['overall_average_improvement']:.1f}%")
        print(f"  Success rate: {improvement['improvement_rate']:.1f}%")
    
    # 結果エクスポート
    system.export_performance_analysis("demo_results")
    
    return system, batch_results


if __name__ == "__main__":
    demo_system, demo_results = create_integration_demo()
