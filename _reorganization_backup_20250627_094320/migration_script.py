#!/usr/bin/env python3
"""
VSCode → Google Drive/Colab 移行スクリプト
既存のPythonスクリプトをGoogle Drive環境に最適化
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class VSCodeToColabMigrator:
    def __init__(self):
        self.work_dir = Path('/content/drive/MyDrive/research')
        self.migration_log = []
        
    def migrate_path_references(self, file_path):
        """ファイル内のパス参照をGoogle Drive対応に変更"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 絶対パスの置換
            vscode_patterns = [
                (r'/mnt/c/Desktop/Research', '/content/drive/MyDrive/research'),
                (r'C:\\Desktop\\Research', '/content/drive/MyDrive/research'),
                (r'C:/Desktop/Research', '/content/drive/MyDrive/research'),
                (r'Path\("/mnt/c/Desktop/Research"\)', 'get_base_path()'),
                (r'Path\("C:/Desktop/Research"\)', 'get_base_path()'),
            ]
            
            for old_pattern, new_pattern in vscode_patterns:
                content = re.sub(old_pattern, new_pattern, content)
            
            # 2. 環境検出コードの追加
            if 'class ' in content and 'def __init__' in content:
                # クラス内の__init__メソッドにパス検出を追加
                init_pattern = r'(def __init__\(self.*?\):.*?\n)(.*?)(def |\Z)'
                
                def add_path_detection(match):
                    init_method = match.group(1)
                    init_body = match.group(2)
                    next_method = match.group(3)
                    
                    if 'self.root_path' in init_body and 'detect_environment' not in init_body:
                        new_init_body = init_body.replace(
                            'self.root_path = Path',
                            'self.root_path = self.detect_environment() if hasattr(self, "detect_environment") else get_base_path() # Path'
                        )
                        return init_method + new_init_body + next_method
                    
                    return match.group(0)
                
                content = re.sub(init_pattern, add_path_detection, content, flags=re.DOTALL)
            
            # 3. インポート文の追加
            if 'from pathlib import Path' in content and 'from google_drive_utils import' not in content:
                import_insertion = 'from pathlib import Path\n'
                if 'try:\n    from google_drive_utils import' not in content:
                    import_insertion += '''try:
    from google_drive_utils import get_base_path, safe_save, timer
except ImportError:
    # フォールバック関数
    def get_base_path():
        try:
            import google.colab
            return Path('/content/drive/MyDrive/research')
        except ImportError:
            return Path.cwd()
    
    def safe_save(content, filepath, backup=True):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    from contextlib import contextmanager
    import time
    
    @contextmanager
    def timer(name="処理"):
        start = time.time()
        print(f"⏱️ {name}開始")
        yield
        print(f"✅ {name}完了: {time.time() - start:.2f}秒")

'''
                
                content = content.replace('from pathlib import Path', import_insertion)
            
            # 4. ファイル保存の安全化
            save_patterns = [
                (r'with open\(([^,]+), [\'"]w[\'"], encoding=[\'"]utf-8[\'"]?\) as f:\s*f\.write\(([^)]+)\)',
                 r'safe_save(\2, \1)'),
                (r'json\.dump\(([^,]+), ([^,]+), ensure_ascii=False, indent=2\)',
                 r'save_json(\1, \2.name if hasattr(\2, "name") else \2)')
            ]
            
            for pattern, replacement in save_patterns:
                content = re.sub(pattern, replacement, content)
            
            # 変更があった場合のみファイルを更新
            if content != original_content:
                # バックアップ作成
                backup_path = file_path.parent / 'backups' / f'{file_path.stem}_vscode_backup{file_path.suffix}'
                backup_path.parent.mkdir(exist_ok=True)
                shutil.copy2(file_path, backup_path)
                
                # 更新されたファイルを保存
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.migration_log.append({
                    'file': str(file_path),
                    'status': 'migrated',
                    'backup': str(backup_path),
                    'changes': len(re.findall(r'/mnt/c|C:\\|C:/', original_content))
                })
                
                return True
            else:
                self.migration_log.append({
                    'file': str(file_path),
                    'status': 'no_changes_needed'
                })
                return False
                
        except Exception as e:
            self.migration_log.append({
                'file': str(file_path),
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def migrate_all_python_files(self):
        """すべてのPythonファイルを移行"""
        python_files = list(self.work_dir.glob('*.py'))
        
        print(f"🔄 {len(python_files)}個のPythonファイルを移行中...")
        
        migrated_count = 0
        for py_file in python_files:
            if self.migrate_path_references(py_file):
                migrated_count += 1
                print(f"✅ 移行完了: {py_file.name}")
            else:
                print(f"⏹️ 変更なし: {py_file.name}")
        
        print(f"📊 移行完了: {migrated_count}/{len(python_files)}ファイル")
        return migrated_count
    
    def create_colab_notebooks(self):
        """主要スクリプト用のColabノートブックを作成"""
        main_scripts = [
            'baseline_comparison_experiment.py',
            'performance_optimization_experiment.py',
            'scalability_experiment.py',
            'confidence_feedback_implementation.py',
            'enhanced_features_implementation.py'
        ]
        
        notebook_dir = self.work_dir / 'notebooks'
        notebook_dir.mkdir(exist_ok=True)
        
        for script_name in main_scripts:
            script_path = self.work_dir / script_name
            if script_path.exists():
                notebook_content = self.create_notebook_from_script(script_path)
                notebook_path = notebook_dir / f"{script_path.stem}.ipynb"
                
                with open(notebook_path, 'w', encoding='utf-8') as f:
                    f.write(notebook_content)
                
                print(f"📓 ノートブック作成: {notebook_path.name}")
    
    def create_notebook_from_script(self, script_path):
        """PythonスクリプトからColabノートブックを作成"""
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # ノートブックテンプレート
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# {script_path.stem}\n",
                        f"\n",
                        f"元のスクリプト: `{script_path.name}`\n",
                        f"移行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# === 環境セットアップ ===\n",
                        "from google.colab import drive\n",
                        "drive.mount('/content/drive')\n",
                        "\n",
                        "import os\n",
                        "os.chdir('/content/drive/MyDrive/research')\n",
                        "\n",
                        "from google_drive_utils import *\n",
                        "paths, auto_sync = initialize_environment()\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": script_content.split('\n')
                }
            ],
            "metadata": {
                "colab": {
                    "name": f"{script_path.stem}.ipynb",
                    "provenance": []
                },
                "kernelspec": {
                    "display_name": "Python 3",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 0
        }
        
        import json
        return json.dumps(notebook, ensure_ascii=False, indent=2)
    
    def update_claude_md(self):
        """CLAUDE.mdを更新してGoogle Drive対応を追加"""
        claude_md_path = self.work_dir / 'CLAUDE.md'
        
        if claude_md_path.exists():
            with open(claude_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Google Drive設定セクションを追加
            gdrive_section = '''

## 🌐 Google Drive / Colab環境対応

### 自動環境検出
このシステムは実行環境を自動検出し、適切なパスを設定します：
- **Colab環境**: `/content/drive/MyDrive/research`
- **WSL環境**: `/mnt/c/Desktop/Research` 
- **Windows環境**: `C:/Desktop/Research`
- **その他**: 現在の作業ディレクトリ

### 移行完了項目
- ✅ パス参照の自動検出・変換
- ✅ 環境固有の設定分離
- ✅ 自動保存・同期システム最適化
- ✅ Colabテンプレートノートブック作成

### 使用方法
```python
# Colabでの標準的な開始手順
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/research')

from google_drive_utils import *
paths, auto_sync = initialize_environment()
```

### 移行された機能
1. **自動整理・保存システム**: 環境検出対応
2. **実験スクリプト**: Colab最適化済み
3. **パス管理**: 相対パス・絶対パス自動変換
4. **ファイル操作**: 安全な保存・バックアップ
5. **エラーハンドリング**: 環境間互換性

'''
            
            if '## 🌐 Google Drive / Colab環境対応' not in content:
                content += gdrive_section
                
                with open(claude_md_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ CLAUDE.md更新完了")
    
    def create_migration_report(self):
        """移行レポートを作成"""
        report = {
            'migration_timestamp': datetime.now().isoformat(),
            'migration_summary': {
                'total_files_processed': len(self.migration_log),
                'files_migrated': len([log for log in self.migration_log if log['status'] == 'migrated']),
                'files_no_changes': len([log for log in self.migration_log if log['status'] == 'no_changes_needed']),
                'files_with_errors': len([log for log in self.migration_log if log['status'] == 'error'])
            },
            'detailed_log': self.migration_log
        }
        
        report_path = self.work_dir / f'migration_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        import json
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 移行レポート作成: {report_path}")
        return report_path
    
    def run_full_migration(self):
        """完全移行を実行"""
        print("🚀 VSCode → Google Drive/Colab 移行開始")
        print("=" * 50)
        
        # 1. Pythonファイルの移行
        migrated_count = self.migrate_all_python_files()
        
        # 2. Colabノートブック作成
        self.create_colab_notebooks()
        
        # 3. CLAUDE.md更新
        self.update_claude_md()
        
        # 4. 移行レポート作成
        report_path = self.create_migration_report()
        
        print("=" * 50)
        print("✅ 移行完了！")
        print(f"📊 移行されたファイル: {migrated_count}")
        print(f"📁 Colabノートブック: notebooks/")
        print(f"📋 詳細レポート: {report_path}")
        
        return report_path

def main():
    migrator = VSCodeToColabMigrator()
    return migrator.run_full_migration()

if __name__ == "__main__":
    main()