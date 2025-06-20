import os
import time
from PIL import Image

class ImageProcessor:
    """画像処理・キャプション生成"""
    
    def __init__(self, model_loader):
        self.model_loader = model_loader
        self.device = model_loader.device
    
    def generate_caption(self, image_path):
        """画像からキャプション生成"""
        if not self.model_loader.is_available():
            return self._generate_demo_caption(image_path)
        
        try:
            # 画像読み込み・検証
            if not self.validate_image(image_path):
                raise ValueError(f"無効な画像ファイル: {image_path}")
            
            image = self.preprocess_image(image_path)
            
            # BLIP処理
            blip_processor = self.model_loader.get_blip_processor()
            blip_model = self.model_loader.get_blip_model()
            
            import torch
            inputs = blip_processor(image, return_tensors="pt")
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = blip_model.generate(**inputs, max_length=50)
            
            caption = blip_processor.decode(outputs[0], skip_special_tokens=True)
            return caption, image
            
        except Exception as e:
            print(f"キャプション生成エラー: {e}")
            return self._generate_demo_caption(image_path)
    
    def preprocess_image(self, image_path):
        """画像前処理"""
        image = Image.open(image_path).convert('RGB')
        return image
    
    def validate_image(self, image_path):
        """画像ファイル検証"""
        if not os.path.exists(image_path):
            return False
        
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except:
            return False
    
    def _generate_demo_caption(self, image_path):
        """デモ用キャプション（AI無効時）"""
        filename = os.path.basename(image_path).lower()
        
        if any(word in filename for word in ['business', 'team', 'person', 'man', 'woman']):
            return "business team standing in office", self.preprocess_image(image_path)
        elif any(word in filename for word in ['dog', 'cat', 'animal']):
            return "a cute animal in natural setting", self.preprocess_image(image_path)
        elif any(word in filename for word in ['food', 'pizza', 'cake']):
            return "delicious food on a plate", self.preprocess_image(image_path)
        else:
            return f"image of {os.path.splitext(filename)[0]}", self.preprocess_image(image_path)