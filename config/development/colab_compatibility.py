#!/usr/bin/env python3
"""
Colab互換性ユーティリティ
既存のPythonスクリプトをColabでも動作させるための関数集
"""
import os
import sys
import json
import subprocess
from pathlib import Path

def is_colab():
    """Google Colab環境かどうかを判定"""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def get_work_dir():
    """環境に応じた作業ディレクトリを取得"""
    if is_colab():
        return '/content/research_project'
    else:
        return os.getcwd()

def setup_path():
    """Pythonパスの設定"""
    work_dir = get_work_dir()
    if work_dir not in sys.path:
        sys.path.insert(0, work_dir)

def safe_import(module_name, package_name=None):
    """安全なモジュールインポート（Colabでは自動インストール）"""
    if package_name is None:
        package_name = module_name
    
    try:
        return __import__(module_name)
    except ImportError:
        if is_colab():
            print(f"Installing {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "-q"])
            return __import__(module_name)
        else:
            raise

def get_file_path(relative_path):
    """環境に応じたファイルパスを取得"""
    work_dir = get_work_dir()
    return os.path.join(work_dir, relative_path)

def ensure_directory(dir_path):
    """ディレクトリの存在を確認し、なければ作成"""
    full_path = get_file_path(dir_path)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    return full_path

def load_json_file(file_path):
    """JSONファイルの読み込み（パス解決付き）"""
    full_path = get_file_path(file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json_file(data, file_path):
    """JSONファイルの保存（パス解決付き）"""
    full_path = get_file_path(file_path)
    ensure_directory(os.path.dirname(full_path))
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run_command(command, shell=True):
    """コマンド実行（環境差分を吸収）"""
    if is_colab():
        # Colabではサブプロセスの出力を適切に処理
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode == 0
    else:
        # ローカルでは通常通り実行
        return subprocess.run(command, shell=shell).returncode == 0

def upload_files_interactive():
    """Colabでファイルをインタラクティブにアップロード"""
    if not is_colab():
        print("This function is only available in Google Colab")
        return []
    
    from google.colab import files
    uploaded = files.upload()
    
    uploaded_paths = []
    for filename, content in uploaded.items():
        file_path = get_file_path(filename)
        with open(file_path, 'wb') as f:
            f.write(content)
        uploaded_paths.append(file_path)
        print(f"Uploaded: {filename}")
    
    return uploaded_paths

def download_file(file_path):
    """Colabからファイルをダウンロード"""
    if not is_colab():
        print("This function is only available in Google Colab")
        return
    
    from google.colab import files
    full_path = get_file_path(file_path)
    if os.path.exists(full_path):
        files.download(full_path)
        print(f"Downloaded: {file_path}")
    else:
        print(f"File not found: {file_path}")

def mount_drive():
    """Google Driveをマウント（Colabのみ）"""
    if is_colab():
        from google.colab import drive
        drive.mount('/content/drive')
        return True
    return False

def get_drive_path(relative_path=''):
    """Google Drive内のパスを取得"""
    if is_colab() and os.path.exists('/content/drive/MyDrive'):
        return os.path.join('/content/drive/MyDrive', relative_path)
    return None

def backup_to_drive(source_path, drive_folder='research_backup'):
    """ファイルをGoogle Driveにバックアップ"""
    if not is_colab():
        return False
    
    drive_base = get_drive_path()
    if not drive_base:
        print("Google Drive not mounted")
        return False
    
    backup_dir = os.path.join(drive_base, drive_folder)
    ensure_directory(backup_dir)
    
    import shutil
    source_full = get_file_path(source_path)
    if os.path.exists(source_full):
        dest = os.path.join(backup_dir, os.path.basename(source_path))
        shutil.copy2(source_full, dest)
        print(f"Backed up to Drive: {dest}")
        return True
    return False

# 環境初期化
def init_colab_env():
    """Colab環境の初期化"""
    setup_path()
    
    if is_colab():
        print("🚀 Initializing Colab environment...")
        ensure_directory('')
        ensure_directory('sessions')
        ensure_directory('public')
        print("✅ Colab environment initialized")
    else:
        print("📍 Running in local environment")

# 自動実行
if __name__ == "__main__":
    init_colab_env()