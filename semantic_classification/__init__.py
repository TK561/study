"""
Semantic Classification System
Complete Object Detection Integration for Semantic Category-based Classification
"""

from .__version__ import __version__, __version_info__

# Core modules
try:
    from .core.main_system import SemanticClassificationSystem
    from .core.semantic_analyzer import SemanticAnalyzer
    from .core.classifier import AdaptiveClassifier
    from .core.image_processor import ImageProcessor
    from .config import Config
    from .models.model_loader import ModelLoader
    from .data.dataset_manager import DatasetManager
    
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some modules could not be imported: {e}")
    MODULES_AVAILABLE = False

# Public API
__all__ = [
    '__version__',
    '__version_info__',
    'SemanticClassificationSystem',
    'SemanticAnalyzer',
    'AdaptiveClassifier',
    'ImageProcessor',
    'Config',
    'ModelLoader',
    'DatasetManager',
    'MODULES_AVAILABLE',
    'quick_info',
    'get_system_status'
]

def quick_info():
    """Display system information"""
    print(f"Semantic Classification System v{__version__}")
    print(f"Modules available: {MODULES_AVAILABLE}")
    if MODULES_AVAILABLE:
        print("Core components loaded successfully")
    else:
        print("Running in basic mode")
    return {'version': __version__, 'modules_available': MODULES_AVAILABLE}

def get_system_status():
    """Get system status information"""
    return {
        'version': __version__,
        'modules_available': MODULES_AVAILABLE,
        'components': {
            'semantic_analyzer': 'SemanticAnalyzer' in globals(),
            'classifier': 'AdaptiveClassifier' in globals(),
            'image_processor': 'ImageProcessor' in globals(),
            'model_loader': 'ModelLoader' in globals(),
            'dataset_manager': 'DatasetManager' in globals()
        }
    }