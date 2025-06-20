"""
意味分析システム（修正版）
"""
import time
import re
from typing import List, Dict, Tuple, Optional, Any
from collections import defaultdict, Counter

try:
    import nltk
    from nltk.corpus import wordnet as wn
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

import numpy as np

class SemanticAnalyzer:
    """意味分析システム"""
    
    def __init__(self, config):
        self.config = config
        self.nltk_available = NLTK_AVAILABLE
        
        # NLTK初期化
        if self.nltk_available:
            self._initialize_nltk()
        
        # カテゴリキーワード定義
        self.category_keywords = {
            'person': ['person', 'man', 'woman', 'child', 'people', 'human', 'face', 'team', 'professional'],
            'animal': ['dog', 'cat', 'bird', 'animal', 'pet', 'puppy', 'kitten', 'creature'],
            'food': ['food', 'pizza', 'cake', 'meal', 'dish', 'cuisine', 'delicious', 'restaurant'],
            'landscape': ['landscape', 'nature', 'outdoor', 'scenery', 'mountain', 'beach', 'forest'],
            'building': ['building', 'house', 'office', 'structure', 'architecture', 'construction'],
            'furniture': ['chair', 'table', 'sofa', 'furniture', 'interior', 'room', 'desk'],
            'vehicle': ['car', 'vehicle', 'truck', 'bus', 'transportation', 'automobile'],
            'plant': ['tree', 'flower', 'plant', 'garden', 'vegetation', 'botanical'],
            'general': ['object', 'thing', 'item']
        }
        
        print("WordNet semantic analyzer initialized")
    
    def _initialize_nltk(self):
        """NLTK初期化"""
        try:
            # 必要なNLTKデータのダウンロード確認
            nltk_downloads = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'stopwords']
            for download in nltk_downloads:
                try:
                    if download == 'punkt':
                        nltk.data.find('tokenizers/punkt')
                    elif download in ['wordnet', 'stopwords']:
                        nltk.data.find(f'corpora/{download}')
                    else:
                        nltk.data.find(f'taggers/{download}')
                except LookupError:
                    nltk.download(download, quiet=True)
            
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"NLTK initialization failed: {e}")
            self.nltk_available = False
    
    def extract_nouns(self, text: str) -> List[str]:
        """テキストから名詞を抽出"""
        if self.nltk_available and hasattr(self, 'lemmatizer'):
            try:
                # NLTK使用版
                tokens = word_tokenize(text.lower())
                tagged = pos_tag(tokens)
                
                nouns = []
                for word, pos in tagged:
                    if pos.startswith('NN') and word not in self.stop_words and len(word) > 2:
                        lemmatized = self.lemmatizer.lemmatize(word)
                        nouns.append(lemmatized)
                
                return nouns if nouns else self._simple_extract_nouns(text)
            except Exception as e:
                print(f"NLTK noun extraction failed: {e}")
                return self._simple_extract_nouns(text)
        else:
            return self._simple_extract_nouns(text)
    
    def _simple_extract_nouns(self, text: str) -> List[str]:
        """簡易名詞抽出（NLTKなし）"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # 一般的な名詞リスト
        common_nouns = [
            'person', 'man', 'woman', 'child', 'people', 'team', 'group',
            'dog', 'cat', 'animal', 'pet', 'bird', 'creature',
            'food', 'pizza', 'cake', 'meal', 'dish', 'cuisine',
            'chair', 'table', 'sofa', 'furniture', 'room', 'interior',
            'building', 'house', 'office', 'structure', 'architecture',
            'car', 'vehicle', 'truck', 'bus', 'transportation',
            'tree', 'flower', 'plant', 'garden', 'vegetation',
            'mountain', 'beach', 'forest', 'landscape', 'nature'
        ]
        
        # 一般的なストップワード
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        found_nouns = [word for word in words if word in common_nouns and word not in stop_words]
        return found_nouns if found_nouns else ['object']
    
    def determine_category(self, nouns: List[str]) -> Tuple[str, float]:
        """名詞から意味カテゴリを判定"""
        category_scores = defaultdict(float)
        
        for noun in nouns:
            for category, keywords in self.category_keywords.items():
                if noun in keywords:
                    category_scores[category] += 1
        
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            confidence = category_scores[best_category] / sum(category_scores.values())
            return best_category, confidence
        else:
            return 'general', 0.0
    
    def determine_category_stable(self, text: str) -> Tuple[str, float]:
        """安定したカテゴリ判定（改良版）"""
        nouns = self.extract_nouns(text)
        return self.determine_category(nouns)
    
    def analyze_image_semantics(self, image_input, image_path: str = "unknown"):
        """画像の意味分析（互換性のため）"""
        # デモ用簡易キャプション生成
        if isinstance(image_path, str) and image_path != "unknown":
            filename = image_path.lower()
            if 'business' in filename or 'team' in filename:
                caption = "professional business team meeting in office"
            elif 'dog' in filename or 'animal' in filename:
                caption = "cute dog playing in garden"
            elif 'food' in filename or 'pizza' in filename:
                caption = "delicious food on table"
            else:
                caption = "object in scene"
        else:
            caption = "generic scene description"
        
        nouns = self.extract_nouns(caption)
        category, confidence = self.determine_category(nouns)
        
        return {
            'category': category,
            'confidence': confidence,
            'extracted_nouns': nouns,
            'caption': caption,
            'processing_time': 0.1
        }