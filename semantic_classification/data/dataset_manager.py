class DatasetManager:
    """データセット定義・管理"""
    
    def __init__(self, config):
        self.config = config
        self.category_mapping = config.CATEGORY_LABELS
        
        # データセット対応表
        self.dataset_mapping = {
            'person': 'Human-focused Classification',
            'animal': 'Animal-specialized Classification',
            'food': 'Food-specialized Classification',
            'landscape': 'Scene-specialized Classification',
            'building': 'Architecture-specialized Classification',
            'furniture': 'Object-specialized Classification',
            'vehicle': 'Vehicle-specialized Classification',
            'plant': 'Plant-specialized Classification',
            'general': 'General Classification (Baseline)'
        }
    
    def get_labels_for_category(self, category):
        """カテゴリに対応するラベル取得"""
        return self.category_mapping.get(category, self.category_mapping['general'])
    
    def get_dataset_info(self, category):
        """データセット情報取得"""
        return {
            'name': self.dataset_mapping.get(category, 'General Classification'),
            'labels': self.get_labels_for_category(category),
            'category': category
        }
    
    def get_all_categories(self):
        """全カテゴリ取得"""
        return list(self.category_mapping.keys())