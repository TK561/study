# semantic_classification/config.py
# システム設定管理（構造修正版）

import os
import torch
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """モデル設定クラス"""
    blip_model_name: str = "Salesforce/blip-image-captioning-base"
    clip_model_name: str = "openai/clip-vit-base-patch32"
    blip_max_length: int = 50
    device: str = "cpu"

@dataclass
class DatasetConfig:
    """データセット設定クラス"""
    category_datasets: dict = None
    category_labels: dict = None
    
    def __post_init__(self):
        if self.category_datasets is None:
            self.category_datasets = {
                'person': 'LFW',
                'animal': 'ImageNet-Animals',
                'food': 'Food-101',
                'landscape': 'Places365',
                'building': 'OpenBuildings',
                'furniture': 'Objects365-Furniture',
                'vehicle': 'Pascal-VOC-Vehicle',
                'plant': 'PlantVillage',
                'general': 'COCO'
            }
        
        if self.category_labels is None:
            self.category_labels = {
                'person': [
                    "man", "woman", "child", "teenager", "elderly person",
                    "face", "portrait", "businessman", "professional", "team"
                ],
                'animal': [
                    "dog", "cat", "bird", "horse", "elephant", "tiger",
                    "lion", "bear", "puppy", "kitten", "wild animal", "pet"
                ],
                'food': [
                    "pizza", "hamburger", "sushi", "salad", "pasta", "cake",
                    "fruit", "vegetable", "meal", "dish", "cuisine", "dessert"
                ],
                'landscape': [
                    "beach", "mountain", "forest", "city", "desert", "lake",
                    "sunset", "nature", "outdoor", "scenery", "park", "garden"
                ],
                'building': [
                    "house", "skyscraper", "bridge", "temple", "stadium",
                    "church", "castle", "tower", "office", "architecture"
                ],
                'furniture': [
                    "chair", "table", "sofa", "bed", "desk", "lamp",
                    "refrigerator", "cabinet", "furniture", "interior"
                ],
                'vehicle': [
                    "car", "bus", "motorcycle", "bicycle", "airplane",
                    "train", "truck", "boat", "vehicle", "transportation"
                ],
                'plant': [
                    "tree", "flower", "grass", "crop", "vegetable",
                    "leaf", "garden", "forest", "plant", "botanical"
                ],
                'general': [
                    "person", "animal", "food", "vehicle", "furniture",
                    "plant", "building", "object"
                ]
            }

class Config:
    """システム設定クラス（統合版）"""
    
    def __init__(self):
        # デバイス設定
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        
        # サブ設定クラス
        self.models = ModelConfig(device=self.DEVICE)
        self.datasets = DatasetConfig()
        
        # 対応カテゴリ設定（後方互換性のため）
        self.SUPPORTED_CATEGORIES = [
            'person', 'animal', 'food', 'landscape', 
            'building', 'furniture', 'vehicle', 'plant', 'general'
        ]
        
        # 後方互換性のための属性
        self.CATEGORY_LABELS = self.datasets.category_labels
        self.BLIP_MODEL_NAME = self.models.blip_model_name
        self.CLIP_MODEL_NAME = self.models.clip_model_name
        
        # データセット対応設定
        self.DATASET_MAPPING = {
            'person': {
                'approach': 'LFW (Labeled Faces in the Wild)',
                'specialization': '顔認識・人物識別特化',
                'year': 2007
            },
            'animal': {
                'approach': 'ImageNet Animal Classes',
                'specialization': '動物分類・行動認識特化',
                'year': 2009
            },
            'food': {
                'approach': 'Food-101',
                'specialization': '料理・食材認識特化',
                'year': 2014
            },
            'landscape': {
                'approach': 'Places365',
                'specialization': 'シーン・環境認識特化',
                'year': 2017
            },
            'building': {
                'approach': 'OpenBuildings',
                'specialization': '建築物・構造物認識特化',
                'year': 2021
            },
            'furniture': {
                'approach': 'Objects365 Furniture Classes',
                'specialization': '家具・日用品認識特化',
                'year': 2019
            },
            'vehicle': {
                'approach': 'Pascal VOC Vehicle Classes',
                'specialization': '車両・交通認識特化',
                'year': 2012
            },
            'plant': {
                'approach': 'PlantVillage',
                'specialization': '植物・農作物認識特化',
                'year': 2016
            },
            'general': {
                'approach': 'COCO General',
                'specialization': '汎用物体認識',
                'year': 2014
            }
        }
        
        # 処理設定
        self.MAX_CAPTION_LENGTH = 50
        self.PROCESSING_TIMEOUT = 30
        self.BATCH_SIZE = 1
        self.CONFIDENCE_THRESHOLD = 0.3
        
        # 出力設定
        self.RESULTS_DIR = "results"
        self.GRAPHS_DIR = "results/graphs"
        self.LOGS_DIR = "results/logs"
        
        # ディレクトリ作成
        self._create_directories()
    
    def _create_directories(self):
        """必要なディレクトリを作成"""
        directories = [self.RESULTS_DIR, self.GRAPHS_DIR, self.LOGS_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_category_labels(self, category):
        """指定カテゴリのラベルを取得"""
        return self.CATEGORY_LABELS.get(category, self.CATEGORY_LABELS['general'])
    
    def get_dataset_info(self, category):
        """指定カテゴリのデータセット情報を取得"""
        return self.DATASET_MAPPING.get(category, self.DATASET_MAPPING['general'])
    
    def is_valid_category(self, category):
        """有効なカテゴリかチェック"""
        return category in self.SUPPORTED_CATEGORIES
    
    def get_device_info(self):
        """デバイス情報を取得"""
        device_info = {
            'device': self.DEVICE,
            'cuda_available': torch.cuda.is_available()
        }
        
        if torch.cuda.is_available():
            device_info['cuda_device_count'] = torch.cuda.device_count()
            device_info['cuda_device_name'] = torch.cuda.get_device_name(0)
        
        return device_info
    
    def __str__(self):
        """設定情報の文字列表現"""
        return f"Config(categories={len(self.SUPPORTED_CATEGORIES)}, device={self.DEVICE})"
    
    def __repr__(self):
        return self.__str__()


# デフォルト設定インスタンス
default_config = Config()

# 設定確認用関数
def verify_config():
    """設定の妥当性確認"""
    config = Config()
    
    checks = {
        'カテゴリ数': len(config.SUPPORTED_CATEGORIES) > 0,
        'ラベル定義': all(category in config.CATEGORY_LABELS for category in config.SUPPORTED_CATEGORIES),
        'データセット対応': all(category in config.DATASET_MAPPING for category in config.SUPPORTED_CATEGORIES),
        'デバイス設定': config.DEVICE in ['cpu', 'cuda'],
        'モデル設定': hasattr(config, 'models') and hasattr(config.models, 'blip_model_name'),
        'データセット設定': hasattr(config, 'datasets') and hasattr(config.datasets, 'category_labels')
    }
    
    all_passed = all(checks.values())
    
    print("設定確認結果:")
    for check_name, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
    
    return all_passed

if __name__ == "__main__":
    # 設定テスト実行
    print("Config クラステスト（構造修正版）")
    print("=" * 40)
    
    config = Config()
    print(f"設定インスタンス: {config}")
    print(f"対応カテゴリ: {config.SUPPORTED_CATEGORIES}")
    print(f"デバイス情報: {config.get_device_info()}")
    print(f"モデル設定: {config.models}")
    print(f"BLIPモデル名: {config.models.blip_model_name}")
    
    print("\n設定妥当性確認:")
    verify_config()