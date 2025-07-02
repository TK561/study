#!/usr/bin/env python3
"""
Google Colab環境セットアップスクリプト
"""
import subprocess
import sys
import os

def is_colab():
    """Google Colab環境かどうかを判定"""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def setup_colab():
    """Colab環境の初期設定"""
    if not is_colab():
        print("This script is designed for Google Colab environment")
        return False
    
    print("🚀 Setting up Google Colab environment...")
    
    # 必要なパッケージのインストール
    packages = [
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly',
        'chart.js',
        'beautifulsoup4',
        'requests',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
    
    # Colabのドライブマウント
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive mounted successfully")
    except Exception as e:
        print(f"⚠️ Could not mount Google Drive: {e}")
    
    # 作業ディレクトリの設定
    work_dir = '/content/research_project'
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
        print(f"✅ Created working directory: {work_dir}")
    
    # 環境変数の設定
    os.environ['PYTHONPATH'] = work_dir
    os.environ['RESEARCH_HOME'] = work_dir
    
    print("✅ Colab setup completed!")
    return True

def clone_repository(repo_url=None):
    """GitHubリポジトリをクローン"""
    if not is_colab():
        print("This function is for Colab environment only")
        return
    
    if repo_url:
        print(f"Cloning repository: {repo_url}")
        subprocess.run(["git", "clone", repo_url, "/content/research_project"])
    else:
        print("Please provide a repository URL")

if __name__ == "__main__":
    if is_colab():
        setup_colab()
    else:
        print("This script is designed for Google Colab. Run it in a Colab notebook.")