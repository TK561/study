"""
AIモデル管理システム（修正版）
"""
import os
from typing import Optional, Dict, Any

try:
    import torch
    from transformers import (
        BlipProcessor, BlipForConditionalGeneration,
        CLIPProcessor, CLIPModel
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    torch = None

class ModelLoader:
    """AIモデルローダー"""
    
    def __init__(self, config):
        self.config = config
        self.device = self._determine_device()
        self.models_loaded = False
        
        # モデル格納
        self.blip_processor = None
        self.blip_model = None
        self.clip_processor = None
        self.clip_model = None
        
        # 初期化実行
        if TRANSFORMERS_AVAILABLE:
            self._initialize_models()
    
    def _determine_device(self) -> str:
        """デバイス決定"""
        if TRANSFORMERS_AVAILABLE and torch and torch.cuda.is_available():
            return "cuda"
        return "cpu"
    
    def _initialize_models(self):
        """モデル初期化"""
        try:
            print("AIモデル初期化中...")
            
            # BLIP
            self.blip_processor = BlipProcessor.from_pretrained(
                self.config.BLIP_MODEL_NAME
            )
            self.blip_model = BlipForConditionalGeneration.from_pretrained(
                self.config.BLIP_MODEL_NAME
            )
            
            # CLIP
            self.clip_processor = CLIPProcessor.from_pretrained(
                self.config.CLIP_MODEL_NAME
            )
            self.clip_model = CLIPModel.from_pretrained(
                self.config.CLIP_MODEL_NAME
            )
            
            # GPU転送
            if self.device == "cuda":
                self.blip_model.to(self.device)
                self.clip_model.to(self.device)
            
            self.models_loaded = True
            print(f"AIモデル初期化完了 (デバイス: {self.device})")
            
        except Exception as e:
            print(f"AIモデル初期化失敗: {e}")
            self.models_loaded = False
    
    def is_ready(self) -> bool:
        """モデル準備状況確認"""
        return self.models_loaded
    
    def get_blip_model(self):
        """BLIPモデル取得"""
        return self.blip_model
    
    def get_blip_processor(self):
        """BLIPプロセッサ取得"""
        return self.blip_processor
    
    def get_clip_model(self):
        """CLIPモデル取得"""
        return self.clip_model
    
    def get_clip_processor(self):
        """CLIPプロセッサ取得"""
        return self.clip_processor
    
    def get_device(self) -> str:
        """使用デバイス取得"""
        return self.device
    
    def is_available(self) -> bool:
        """利用可能性確認（互換性のため）"""
        return self.is_ready()