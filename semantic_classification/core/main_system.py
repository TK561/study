import os
import time
from datetime import datetime

class SemanticClassificationSystem:
    """メインシステム - 全モジュール統合"""
    
    def __init__(self, config=None):
        from ..config import Config
        from ..models import ModelLoader
        from ..data import DatasetManager
        
        self.config = config or Config()
        
        # モジュール初期化
        self.model_loader = ModelLoader(self.config)
        self.dataset_manager = DatasetManager(self.config)
        
        # 核心モジュール初期化
        from .image_processor import ImageProcessor
        from .semantic_analyzer import SemanticAnalyzer
        from .classifier import AdaptiveClassifier
        
        self.image_processor = ImageProcessor(self.model_loader)
        self.semantic_analyzer = SemanticAnalyzer(self.config)
        self.classifier = AdaptiveClassifier(self.model_loader, self.dataset_manager)
        
        self.results = []
        print("Semantic Classification System 初期化完了")
    
    def process_single_image(self, image_path):
        """単一画像処理"""
        print(f"\n画像処理開始: {os.path.basename(image_path)}")
        start_time = time.time()
        
        try:
            # 1. 画像処理・キャプション生成
            caption, image = self.image_processor.generate_caption(image_path)
            print(f"キャプション: {caption}")
            
            # 2. 意味分析・カテゴリ判定
            nouns = self.semantic_analyzer.extract_nouns(caption)
            category, confidence = self.semantic_analyzer.determine_category(nouns)
            print(f"判定カテゴリ: {category} (確信度: {confidence:.2f})")
            
            # 3. データセット情報取得
            general_info = self.dataset_manager.get_dataset_info('general')
            specialized_info = self.dataset_manager.get_dataset_info(category)
            
            print(f"汎用データセット: {general_info['name']}")
            print(f"特化データセット: {specialized_info['name']}")
            
            # 4. 分類実行
            general_results = self.classifier.classify_with_labels(
                image, general_info['labels'], general_info['name']
            )
            specialized_results = self.classifier.classify_with_labels(
                image, specialized_info['labels'], specialized_info['name']
            )
            
            # 5. 結果比較
            comparison = self.classifier.compare_results(general_results, specialized_results)
            
            processing_time = time.time() - start_time
            
            print(f"汎用最高確信度: {comparison['general_top_confidence']:.4f} ({comparison['general_top_label']})")
            print(f"特化最高確信度: {comparison['specialized_top_confidence']:.4f} ({comparison['specialized_top_label']})")
            print(f"改善率: {comparison['improvement_percent']:.2f}%")
            print(f"処理時間: {processing_time:.2f}秒")
            
            # 6. 結果構造化
            result = {
                'image_name': os.path.basename(image_path),
                'image_path': image_path,
                'caption': caption,
                'nouns': nouns,
                'category': category,
                'category_confidence': confidence,
                'general_results': general_results,
                'specialized_results': specialized_results,
                'comparison': comparison,
                'processing_time': processing_time,
                'timestamp': datetime.now().isoformat()
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            print(f"処理エラー: {e}")
            return None
    
    def process_multiple_images(self, image_paths):
        """複数画像処理"""
        print(f"\n複数画像処理開始: {len(image_paths)}枚")
        
        results = []
        for i, image_path in enumerate(image_paths):
            print(f"\n進捗: {i+1}/{len(image_paths)}")
            result = self.process_single_image(image_path)
            if result:
                results.append(result)
        
        return results
    
    def get_summary(self):
        """処理結果のサマリー"""
        if not self.results:
            return "処理結果がありません"
        
        improvements = [r['comparison']['improvement_percent'] for r in self.results]
        avg_improvement = sum(improvements) / len(improvements)
        
        return f"""
処理結果サマリー:
- 処理画像数: {len(self.results)}枚
- 平均改善率: {avg_improvement:.2f}%
- 成功した画像: {len([r for r in self.results if r['comparison']['improvement_percent'] > 0])}枚
"""