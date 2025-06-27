# 🌐 Google Drive環境セットアップガイド

このガイドは、VSCodeからGoogle Drive + Colabへの移行をサポートします。

## 📋 目次
1. [初期セットアップ](#初期セットアップ)
2. [Colab環境設定](#colab環境設定)
3. [自動同期システム](#自動同期システム)
4. [ファイル管理](#ファイル管理)
5. [便利な機能](#便利な機能)

## 🚀 初期セットアップ

### 1. Google Driveマウント（Colabで実行）
```python
from google.colab import drive
drive.mount('/content/drive')

# 作業ディレクトリ設定
import os
os.chdir('/content/drive/MyDrive/research')
print(f"現在の作業ディレクトリ: {os.getcwd()}")
```

### 2. 基本環境確認
```python
# 環境情報表示
!python --version
!pwd
!ls -la
```

### 3. 必要なライブラリインストール
```python
# 基本ライブラリ
!pip install -q pandas numpy matplotlib seaborn
!pip install -q google-generativeai
!pip install -q python-dotenv

# 追加ライブラリ（必要に応じて）
!pip install -q pillow
!pip install -q tqdm
```

## 🔧 Colab環境設定

### 1. 自動実行セル（各ノートブックの最初に配置）
```python
# === Google Drive自動設定セル ===
# このセルを最初に実行してください

import sys
import os
from pathlib import Path

# Google Driveマウント
try:
    from google.colab import drive
    drive.mount('/content/drive', force_remount=True)
    IN_COLAB = True
except:
    IN_COLAB = False
    print("ローカル環境で実行中")

# 作業ディレクトリ設定
if IN_COLAB:
    WORK_DIR = Path('/content/drive/MyDrive/research')
else:
    WORK_DIR = Path.cwd()

os.chdir(WORK_DIR)
sys.path.append(str(WORK_DIR))

print(f"✅ 作業ディレクトリ: {WORK_DIR}")
print(f"✅ Colab環境: {IN_COLAB}")

# 共通関数読み込み
if (WORK_DIR / 'google_drive_utils.py').exists():
    from google_drive_utils import *
```

### 2. 環境変数設定
```python
# .env.colabファイルから環境変数読み込み
import os
from pathlib import Path

env_file = Path('.env.colab')
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
```

## 💾 自動同期システム

### 1. ファイル変更監視
```python
# google_drive_file_watcher.py
import time
import hashlib
from pathlib import Path
from datetime import datetime

class GoogleDriveFileWatcher:
    def __init__(self, watch_dir='/content/drive/MyDrive/research'):
        self.watch_dir = Path(watch_dir)
        self.file_hashes = {}
        self.last_check = datetime.now()
        
    def calculate_hash(self, filepath):
        """ファイルのハッシュ値計算"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def check_changes(self):
        """ファイル変更検出"""
        changed_files = []
        
        for file_path in self.watch_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                current_hash = self.calculate_hash(file_path)
                
                if file_path in self.file_hashes:
                    if self.file_hashes[file_path] != current_hash:
                        changed_files.append(file_path)
                
                self.file_hashes[file_path] = current_hash
        
        return changed_files
    
    def auto_backup_changed_files(self):
        """変更ファイルの自動バックアップ"""
        changed = self.check_changes()
        
        if changed:
            backup_dir = self.watch_dir / 'backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            for file_path in changed:
                relative_path = file_path.relative_to(self.watch_dir)
                backup_path = backup_dir / relative_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                
                import shutil
                shutil.copy2(file_path, backup_path)
                
            print(f"✅ {len(changed)}個のファイルをバックアップしました: {backup_dir}")
```

### 2. 定期自動保存
```python
# auto_save_colab.py
import time
from datetime import datetime
from pathlib import Path

class ColabAutoSave:
    def __init__(self):
        self.save_interval = 300  # 5分ごと
        self.last_save = time.time()
        
    def save_notebook_output(self):
        """ノートブックの出力を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path('notebook_outputs')
        output_dir.mkdir(exist_ok=True)
        
        # 現在のセッション情報を保存
        session_info = {
            'timestamp': timestamp,
            'runtime_type': self.get_runtime_info(),
            'executed_cells': self.get_executed_cells()
        }
        
        import json
        with open(output_dir / f'session_{timestamp}.json', 'w') as f:
            json.dump(session_info, f, indent=2)
        
        print(f"💾 セッション自動保存完了: {timestamp}")
    
    def get_runtime_info(self):
        """ランタイム情報取得"""
        try:
            import subprocess
            gpu_info = subprocess.getoutput('nvidia-smi --query-gpu=name --format=csv,noheader')
            return {
                'gpu': gpu_info if gpu_info else 'CPU',
                'python_version': sys.version.split()[0]
            }
        except:
            return {'gpu': 'Unknown', 'python_version': sys.version.split()[0]}
    
    def get_executed_cells(self):
        """実行済みセルの情報取得"""
        # Colabでは実装が複雑なため、簡易版
        return []
```

## 📁 ファイル管理

### 1. パス管理ユーティリティ
```python
# path_utils.py
from pathlib import Path
import os

class GoogleDrivePathManager:
    def __init__(self):
        self.is_colab = 'COLAB_GPU' in os.environ
        
        if self.is_colab:
            self.base_path = Path('/content/drive/MyDrive/research')
        else:
            self.base_path = Path.cwd()
        
        # 共通ディレクトリ
        self.dirs = {
            'data': self.base_path / 'data',
            'models': self.base_path / 'models',
            'results': self.base_path / 'results',
            'logs': self.base_path / 'logs',
            'public': self.base_path / 'public',
            'archive': self.base_path / 'archive',
            'sessions': self.base_path / 'sessions',
            'backups': self.base_path / 'backups'
        }
        
        # ディレクトリ作成
        for dir_path in self.dirs.values():
            dir_path.mkdir(exist_ok=True)
    
    def get_path(self, key):
        """キーに基づくパス取得"""
        return self.dirs.get(key, self.base_path)
    
    def resolve_path(self, relative_path):
        """相対パスを絶対パスに変換"""
        return self.base_path / relative_path
```

### 2. ファイル操作ヘルパー
```python
# file_helpers.py
import shutil
from pathlib import Path
from datetime import datetime

def safe_save(content, filename, backup=True):
    """安全なファイル保存（バックアップ付き）"""
    file_path = Path(filename)
    
    # バックアップ作成
    if backup and file_path.exists():
        backup_name = f"{file_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
        backup_path = file_path.parent / 'backups' / backup_name
        backup_path.parent.mkdir(exist_ok=True)
        shutil.copy2(file_path, backup_path)
    
    # ファイル保存
    if isinstance(content, str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        with open(file_path, 'wb') as f:
            f.write(content)
    
    print(f"✅ ファイル保存完了: {file_path}")
    return file_path

def list_recent_files(directory, days=7):
    """最近のファイル一覧取得"""
    from datetime import datetime, timedelta
    
    cutoff_time = datetime.now() - timedelta(days=days)
    recent_files = []
    
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime > cutoff_time:
                recent_files.append({
                    'path': file_path,
                    'modified': mtime,
                    'size': file_path.stat().st_size
                })
    
    return sorted(recent_files, key=lambda x: x['modified'], reverse=True)
```

## 🎯 便利な機能

### 1. Colab専用ショートカット
```python
# colab_shortcuts.py
from IPython.display import display, HTML
import pandas as pd

def create_navigation_menu():
    """ナビゲーションメニュー作成"""
    html = """
    <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h3>🔗 クイックリンク</h3>
        <a href="#" onclick="document.querySelector('[title=\"ファイル\"]').click(); return false;" style="margin-right: 15px;">📁 ファイル</a>
        <a href="#" onclick="document.querySelector('[title=\"目次\"]').click(); return false;" style="margin-right: 15px;">📑 目次</a>
        <a href="#" onclick="document.querySelector('[title=\"検索と置換\"]').click(); return false;" style="margin-right: 15px;">🔍 検索</a>
        <a href="#" onclick="window.open('/content/drive/MyDrive/research', '_blank'); return false;">📂 Driveで開く</a>
    </div>
    """
    display(HTML(html))

def show_dataframe_interactive(df):
    """インタラクティブなデータフレーム表示"""
    from google.colab import data_table
    data_table.enable_dataframe_formatter()
    display(df)

def quick_plot_setup():
    """グラフ設定の初期化"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.family'] = 'sans-serif'
    sns.set_style('whitegrid')
    
    # 日本語フォント設定
    !apt-get -y install fonts-ipafont-gothic
    plt.rcParams['font.family'] = 'IPAGothic'
```

### 2. 実行時間計測
```python
# timing_utils.py
import time
from contextlib import contextmanager
from datetime import datetime

@contextmanager
def timer(name="処理"):
    """実行時間計測コンテキストマネージャ"""
    start_time = time.time()
    print(f"⏱️ {name}開始: {datetime.now().strftime('%H:%M:%S')}")
    
    yield
    
    elapsed_time = time.time() - start_time
    print(f"✅ {name}完了: {elapsed_time:.2f}秒")

class ProgressLogger:
    """進捗ログ記録"""
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        
    def update(self, message=""):
        self.current_step += 1
        progress = self.current_step / self.total_steps * 100
        elapsed = time.time() - self.start_time
        
        print(f"[{self.current_step}/{self.total_steps}] {progress:.1f}% - {message} ({elapsed:.1f}秒)")
```

### 3. エラーハンドリング
```python
# error_handling.py
import traceback
from datetime import datetime

def safe_execute(func, *args, **kwargs):
    """安全な関数実行"""
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'function': func.__name__,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        
        # エラーログ保存
        error_log = Path('logs/errors.log')
        error_log.parent.mkdir(exist_ok=True)
        
        with open(error_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"{error_info['timestamp']}\n")
            f.write(f"Function: {error_info['function']}\n")
            f.write(f"Error: {error_info['error']}\n")
            f.write(f"{error_info['traceback']}\n")
        
        print(f"❌ エラー発生: {error_info['error']}")
        return False, error_info
```

## 🔄 移行チェックリスト

- [ ] Google Driveをマウント
- [ ] 作業ディレクトリを設定
- [ ] 必要なライブラリをインストール
- [ ] 環境変数を設定（.env.colab）
- [ ] 自動保存システムを有効化
- [ ] パス管理ユーティリティを読み込み
- [ ] エラーハンドリングを設定

## 📝 使用例

```python
# === 標準的なColabノートブックの開始テンプレート ===

# 1. 環境セットアップ
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/research')

# 2. 共通ユーティリティ読み込み
from google_drive_utils import *
from path_utils import GoogleDrivePathManager
from file_helpers import safe_save, list_recent_files
from colab_shortcuts import create_navigation_menu, quick_plot_setup

# 3. 初期設定
path_manager = GoogleDrivePathManager()
create_navigation_menu()
quick_plot_setup()

# 4. 自動保存設定
auto_saver = ColabAutoSave()

print("✅ Google Drive環境セットアップ完了！")
```