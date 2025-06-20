#!/usr/bin/env python3
"""
セキュアな設定読み込みモジュール
環境変数から設定を読み込み、APIキーの漏洩を防止
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env ファイルを読み込み
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print("✅ .env file loaded")
else:
    print("⚠️ .env file not found. Using environment variables only.")

# GitHub設定
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', '')
REPOSITORY_NAME = os.getenv('REPOSITORY_NAME', 'study')
GITHUB_EMAIL = os.getenv('GITHUB_EMAIL', '')

# Claude API設定
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Vercel設定
VERCEL_PROJECT_ID = os.getenv('VERCEL_PROJECT_ID', '')

# 研究プロジェクト設定
PROJECT_NAME = "意味カテゴリに基づく画像分類システム"
RESEARCH_INSTITUTION = os.getenv('RESEARCH_INSTITUTION', '')
RESEARCHER_NAME = os.getenv('RESEARCHER_NAME', '')

PROJECT_DESCRIPTION = """
WordNetベースの意味カテゴリ分析を用いた
特化型画像分類手法の性能評価研究
"""

# 自動化設定
AUTO_COMMIT_ENABLED = True
AUTO_BACKUP_ENABLED = True
DAILY_COMMIT_TIME = "09:00"

# ファイル追跡設定
TRACKED_EXTENSIONS = [
    '.py', '.ipynb', '.md', '.txt', '.csv', '.json', '.yml', '.yaml'
]

EXCLUDED_DIRECTORIES = [
    '__pycache__', '.git', 'venv', '.venv', 'node_modules', 
    'output', 'temp', '.ipynb_checkpoints', 'models', 'data/raw'
]

# データ構造
DATA_STRUCTURE = {
    'raw_data': 'data/raw/',
    'processed_data': 'data/processed/',
    'results': 'results/',
    'figures': 'figures/',
    'notebooks': 'notebooks/',
    'scripts': 'scripts/',
    'docs': 'docs/',
    'papers': 'papers/',
}

# バックアップ設定
BACKUP_DIRECTORIES = [
    'data/processed', 'results', 'figures', 'notebooks', 'scripts', 'docs'
]

# 実験管理
EXPERIMENT_LOG_FILE = "experiments.json"
RESULTS_SUMMARY_FILE = "results_summary.md"

EXPERIMENT_METADATA = {
    'dataset_version': '1.0',
    'model_version': '1.0',
    'evaluation_metrics': ['accuracy', 'precision', 'recall', 'f1-score'],
    'baseline_models': ['general_clip', 'specialized_clip'],
}

# 通知設定
ENABLE_NOTIFICATIONS = True
NOTIFICATION_WEBHOOK = os.getenv('NOTIFICATION_WEBHOOK', '')

# デバッグ設定
DEBUG_MODE = False
VERBOSE_LOGGING = True
LOG_LEVEL = "INFO"

# セキュリティ設定
SENSITIVE_FILE_PATTERNS = [
    '**/config.py', '**/.env', '**/secrets.*', '**/private_*',
    '**/credentials.*', '**/api_keys.*'
]

def validate_config():
    """設定値の妥当性チェック"""
    errors = []
    warnings = []
    
    # 必須項目チェック
    required_fields = [
        ('GITHUB_TOKEN', GITHUB_TOKEN),
        ('GITHUB_USERNAME', GITHUB_USERNAME),
        ('REPOSITORY_NAME', REPOSITORY_NAME),
        ('GITHUB_EMAIL', GITHUB_EMAIL),
    ]
    
    for field_name, field_value in required_fields:
        if not field_value or field_value.strip() == "":
            errors.append(f"❌ {field_name} が設定されていません")
    
    # オプション項目チェック
    optional_fields = [
        ('ANTHROPIC_API_KEY', ANTHROPIC_API_KEY, "Claude API機能が使用できません"),
        ('RESEARCH_INSTITUTION', RESEARCH_INSTITUTION, "所属機関情報が設定されていません"),
        ('RESEARCHER_NAME', RESEARCHER_NAME, "研究者名が設定されていません"),
    ]
    
    for field_name, field_value, warning_msg in optional_fields:
        if not field_value or field_value.strip() == "":
            warnings.append(f"⚠️ {field_name}: {warning_msg}")
    
    return errors, warnings

def print_config_status():
    """設定状況の表示（セキュア版）"""
    print("🔧 研究プロジェクト設定状況")
    print("=" * 40)
    
    errors, warnings = validate_config()
    
    if not errors:
        print("✅ 必須設定: 完了")
    else:
        print("❌ 必須設定: 不完全")
        for error in errors:
            print(f"   {error}")
    
    if warnings:
        print("⚠️ 推奨設定:")
        for warning in warnings:
            print(f"   {warning}")
    
    print(f"\n📊 プロジェクト情報:")
    print(f"   名前: {PROJECT_NAME}")
    print(f"   リポジトリ: {GITHUB_USERNAME}/{REPOSITORY_NAME}")
    print(f"   GitHub Token: {'✅ 設定済み' if GITHUB_TOKEN else '❌ 未設定'}")
    print(f"   Claude API: {'✅ 設定済み' if ANTHROPIC_API_KEY else '❌ 未設定'}")

if __name__ == "__main__":
    print_config_status()