"""
バージョン情報管理
Version information for semantic classification system
"""

# Version information
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Build information
__build_date__ = "2025-06-05"
__build_type__ = "release"

# System information
__system_name__ = "Semantic Classification System"
__system_description__ = "Complete Object Detection Integration for Semantic Category-based Classification"

# API version
__api_version__ = "1.0"

# Supported components version
__component_versions__ = {
    "detection_system": "1.0.0",
    "semantic_analyzer": "1.0.0", 
    "classification_system": "1.0.0",
    "integration_system": "1.0.0",
    "model_manager": "1.0.0",
    "dataset_manager": "1.0.0",
}

# Minimum required versions for dependencies
__required_versions__ = {
    "python": "3.8.0",
    "torch": "1.11.0",
    "transformers": "4.20.0",
    "opencv-python": "4.5.0",
    "numpy": "1.20.0",
    "nltk": "3.7.0",
}

def get_version():
    """バージョン文字列を取得"""
    return __version__

def get_version_info():
    """詳細バージョン情報を取得"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "build_date": __build_date__,
        "build_type": __build_type__,
        "system_name": __system_name__,
        "api_version": __api_version__,
        "components": __component_versions__,
        "requirements": __required_versions__,
    }

def check_compatibility():
    """依存関係の互換性チェック"""
    import sys
    import pkg_resources
    
    compatibility_report = {
        "python": {
            "required": __required_versions__["python"],
            "current": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "compatible": sys.version_info >= tuple(map(int, __required_versions__["python"].split(".")))
        }
    }
    
    for package, required_version in __required_versions__.items():
        if package == "python":
            continue
            
        try:
            current_version = pkg_resources.get_distribution(package).version
            compatibility_report[package] = {
                "required": required_version,
                "current": current_version,
                "compatible": pkg_resources.parse_version(current_version) >= pkg_resources.parse_version(required_version)
            }
        except pkg_resources.DistributionNotFound:
            compatibility_report[package] = {
                "required": required_version,
                "current": "Not installed",
                "compatible": False
            }
    
    return compatibility_report

def print_version_info():
    """バージョン情報を表示"""
    info = get_version_info()
    print(f"{info['system_name']} v{info['version']}")
    print(f"Build: {info['build_date']} ({info['build_type']})")
    print(f"API Version: {info['api_version']}")
    print("\nComponent Versions:")
    for component, version in info['components'].items():
        print(f"  {component}: {version}")
