import numpy as np

class AdaptiveClassifier:
    """CLIP分類・データセット選択"""
    
    def __init__(self, model_loader, dataset_manager):
        self.model_loader = model_loader
        self.dataset_manager = dataset_manager
        self.device = model_loader.device
    
    def classify_with_labels(self, image, labels, dataset_name):
        """指定ラベルでの分類"""
        if not self.model_loader.is_available():
            return self._generate_demo_results(labels, dataset_name)
        
        try:
            clip_processor = self.model_loader.get_clip_processor()
            clip_model = self.model_loader.get_clip_model()
            
            texts = [f"a photo of {label}" for label in labels]
            
            import torch
            inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = clip_model(**inputs)
                probs = outputs.logits_per_image.softmax(dim=1).cpu().numpy()[0]
            
            results = []
            for i, label in enumerate(labels):
                results.append({
                    'label': label,
                    'confidence': float(probs[i]),
                    'dataset': dataset_name,
                    'rank': i + 1
                })
            
            results.sort(key=lambda x: x['confidence'], reverse=True)
            
            # ランク更新
            for i, result in enumerate(results):
                result['rank'] = i + 1
            
            return results
            
        except Exception as e:
            print(f"分類エラー: {e}")
            return self._generate_demo_results(labels, dataset_name)
    
    def _generate_demo_results(self, labels, dataset_name):
        """デモ用結果生成"""
        results = []
        for i, label in enumerate(labels):
            confidence = 0.2 + (0.6 * np.random.random())
            if i == 0:
                confidence += 0.2
            results.append({
                'label': label,
                'confidence': confidence,
                'dataset': dataset_name,
                'rank': i + 1
            })
        
        results.sort(key=lambda x: x['confidence'], reverse=True)
        for i, result in enumerate(results):
            result['rank'] = i + 1
        
        return results
    
    def compare_results(self, general_results, specialized_results):
        """分類結果の比較"""
        general_top = general_results[0] if general_results else {'confidence': 0}
        specialized_top = specialized_results[0] if specialized_results else {'confidence': 0}
        
        general_conf = general_top['confidence']
        specialized_conf = specialized_top['confidence']
        
        improvement = specialized_conf - general_conf
        improvement_percent = (improvement / general_conf * 100) if general_conf > 0 else 0
        
        return {
            'general_top_confidence': general_conf,
            'specialized_top_confidence': specialized_conf,
            'improvement': improvement,
            'improvement_percent': improvement_percent,
            'general_top_label': general_top.get('label', 'unknown'),
            'specialized_top_label': specialized_top.get('label', 'unknown')
        }