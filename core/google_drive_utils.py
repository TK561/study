#!/usr/bin/env python3
"""
Google Drive & Colab環境用ユーティリティ
VSCodeからの移行をサポートする共通関数群
"""

import os
import sys
import json
import time
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

# ===== 環境検出 =====
def is_colab():
    """Colab環境かどうかを検出"""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def get_base_path():
    """環境に応じた基本パスを取得"""
    if is_colab():
        return Path('/content/drive/MyDrive/research')
    else:
        return Path.cwd()

# ===== パス管理 =====
class PathManager:
    """Google Drive/ローカル両対応のパス管理"""
    
    def __init__(self):
        self.base = get_base_path()
        self.setup_directories()
    
    def setup_directories(self):
        """標準ディレクトリ構造を作成"""
        self.dirs = {
            'data': self.base / 'data',
            'models': self.base / 'models',
            'results': self.base / 'results',
            'logs': self.base / 'logs',
            'public': self.base / 'public',
            'archive': self.base / 'archive',
            'sessions': self.base / 'sessions',
            'backups': self.base / 'backups',
            'temp': self.base / 'temp',
            'notebooks': self.base / 'notebooks'
        }
        
        for dir_path in self.dirs.values():
            dir_path.mkdir(exist_ok=True, parents=True)
    
    def get(self, key):
        """ディレクトリパスを取得"""
        return self.dirs.get(key, self.base)
    
    def resolve(self, relative_path):
        """相対パスを絶対パスに変換"""
        return self.base / relative_path

# グローバルインスタンス
paths = PathManager()

# ===== ファイル操作 =====
def safe_save(content, filepath, backup=True):
    """安全なファイル保存（自動バックアップ付き）"""
    filepath = Path(filepath)
    
    # バックアップ作成
    if backup and filepath.exists():
        backup_dir = paths.get('backups') / filepath.parent.name
        backup_dir.mkdir(exist_ok=True, parents=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
        backup_path = backup_dir / backup_name
        
        shutil.copy2(filepath, backup_path)
        print(f"📁 バックアップ作成: {backup_path}")
    
    # ファイル保存
    filepath.parent.mkdir(exist_ok=True, parents=True)
    
    if isinstance(content, str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        with open(filepath, 'wb') as f:
            f.write(content)
    
    print(f"💾 ファイル保存完了: {filepath}")
    return filepath

def load_json(filepath, default=None):
    """JSONファイルの安全な読み込み"""
    filepath = Path(filepath)
    if not filepath.exists():
        return default if default is not None else {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ JSON読み込みエラー: {e}")
        return default if default is not None else {}

def save_json(data, filepath, backup=True):
    """JSONファイルの保存"""
    content = json.dumps(data, ensure_ascii=False, indent=2)
    return safe_save(content, filepath, backup=backup)

# ===== 自動同期 =====
class AutoSync:
    """Google Drive自動同期システム"""
    
    def __init__(self, watch_patterns=None):
        self.watch_patterns = watch_patterns or ['*.py', '*.ipynb', '*.json', '*.md']
        self.file_hashes = {}
        self.sync_interval = 300  # 5分
        self.last_sync = time.time()
    
    def calculate_hash(self, filepath):
        """ファイルのハッシュ値計算"""
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def check_changes(self):
        """変更されたファイルを検出"""
        changed_files = []
        base_path = get_base_path()
        
        for pattern in self.watch_patterns:
            for filepath in base_path.rglob(pattern):
                if filepath.is_file() and 'backups' not in str(filepath):
                    try:
                        current_hash = self.calculate_hash(filepath)
                        
                        if str(filepath) in self.file_hashes:
                            if self.file_hashes[str(filepath)] != current_hash:
                                changed_files.append(filepath)
                        
                        self.file_hashes[str(filepath)] = current_hash
                    except Exception as e:
                        print(f"⚠️ ハッシュ計算エラー: {filepath} - {e}")
        
        return changed_files
    
    def sync_now(self):
        """今すぐ同期を実行"""
        changed = self.check_changes()
        if changed:
            print(f"🔄 {len(changed)}個のファイルが変更されました")
            
            # セッション記録
            session_file = paths.get('sessions') / f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            sync_data = {
                'timestamp': datetime.now().isoformat(),
                'changed_files': [str(f) for f in changed],
                'total_files': len(self.file_hashes)
            }
            save_json(sync_data, session_file, backup=False)
            
        self.last_sync = time.time()
        return changed

# ===== Colab専用機能 =====
if is_colab():
    from IPython.display import display, HTML, Javascript
    
    def setup_colab_env():
        """Colab環境の初期設定"""
        # オートセーブ有効化
        display(Javascript('IPython.notebook.set_autosave_interval(60000)'))  # 1分ごと
        
        # 作業ディレクトリ設定
        os.chdir(get_base_path())
        
        # ナビゲーションメニュー作成
        create_navigation_menu()
        
        print("✅ Colab環境セットアップ完了")
    
    def create_navigation_menu():
        """Colab用ナビゲーションメニュー"""
        html = """
        <style>
            .nav-menu {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                color: white;
            }
            .nav-menu a {
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                margin: 0 5px;
                background: rgba(255,255,255,0.2);
                border-radius: 5px;
                display: inline-block;
            }
            .nav-menu a:hover {
                background: rgba(255,255,255,0.3);
            }
        </style>
        <div class="nav-menu">
            <h3 style="margin: 0 0 10px 0;">🚀 Quick Navigation</h3>
            <a href="#" onclick="document.querySelector('[title=\"ファイル\"]').click(); return false;">📁 Files</a>
            <a href="#" onclick="document.querySelector('[title=\"目次\"]').click(); return false;">📑 Contents</a>
            <a href="#" onclick="window.open('/content/drive/MyDrive/research', '_blank'); return false;">📂 Open in Drive</a>
            <a href="#" onclick="location.reload(); return false;">🔄 Refresh</a>
        </div>
        """
        display(HTML(html))
    
    def save_notebook_state():
        """現在のノートブックの状態を保存"""
        from google.colab import files
        
        state = {
            'timestamp': datetime.now().isoformat(),
            'notebook_name': 'current_notebook',
            'environment': {
                'python_version': sys.version,
                'colab': True,
                'gpu_available': torch.cuda.is_available() if 'torch' in sys.modules else False
            }
        }
        
        state_file = paths.get('sessions') / f"notebook_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_json(state, state_file)
        
        return state_file

# ===== 実行時間計測 =====
@contextmanager
def timer(name="処理"):
    """実行時間を計測するコンテキストマネージャ"""
    start_time = time.time()
    print(f"⏱️ {name}開始: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        print(f"✅ {name}完了: {elapsed:.2f}秒")

# ===== プログレスロガー =====
class ProgressLogger:
    """進捗状況のログ記録"""
    
    def __init__(self, total_steps, name="処理"):
        self.total_steps = total_steps
        self.current_step = 0
        self.name = name
        self.start_time = time.time()
        self.log_file = paths.get('logs') / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def update(self, message="", increment=1):
        """進捗を更新"""
        self.current_step += increment
        progress = (self.current_step / self.total_steps) * 100
        elapsed = time.time() - self.start_time
        
        log_message = f"[{self.current_step}/{self.total_steps}] {progress:.1f}% - {message} ({elapsed:.1f}秒)"
        print(log_message)
        
        # ログファイルに記録
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} {log_message}\n")
    
    def complete(self):
        """完了処理"""
        total_time = time.time() - self.start_time
        print(f"🎉 {self.name}完了！ 総時間: {total_time:.2f}秒")

# ===== エラーハンドリング =====
def safe_execute(func, *args, **kwargs):
    """関数の安全な実行"""
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        error_log = paths.get('logs') / 'errors.log'
        
        with open(error_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Function: {func.__name__}\n")
            f.write(f"Error: {str(e)}\n")
            f.write(f"Args: {args}\n")
            f.write(f"Kwargs: {kwargs}\n")
            
            import traceback
            f.write(f"Traceback:\n{traceback.format_exc()}\n")
        
        print(f"❌ エラー発生: {str(e)}")
        print(f"詳細は {error_log} を確認してください")
        
        return False, None

# ===== データ可視化ヘルパー =====
def setup_plot_style():
    """matplotlib/seabornのスタイル設定"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # 基本設定
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['font.size'] = 12
        
        # 日本語フォント設定（Colab環境）
        if is_colab():
            os.system('apt-get -y install fonts-ipafont-gothic > /dev/null 2>&1')
            plt.rcParams['font.family'] = 'IPAGothic'
        
        # Seabornスタイル
        sns.set_style('whitegrid')
        sns.set_palette('husl')
        
        print("📊 グラフスタイル設定完了")
        
    except ImportError:
        print("⚠️ matplotlib/seabornがインストールされていません")

# ===== 初期化関数 =====
def initialize_environment():
    """環境の完全初期化"""
    print("🚀 Google Drive環境初期化中...")
    
    # パス設定
    paths = PathManager()
    
    # Colab固有の設定
    if is_colab():
        setup_colab_env()
    
    # プロットスタイル設定
    setup_plot_style()
    
    # 自動同期システム初期化
    auto_sync = AutoSync()
    
    print(f"✅ 作業ディレクトリ: {get_base_path()}")
    print("✅ 環境初期化完了！")
    
    return paths, auto_sync

# ===== 便利な定数 =====
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
TODAY = datetime.now().strftime('%Y%m%d')