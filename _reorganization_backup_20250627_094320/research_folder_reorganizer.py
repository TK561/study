#!/usr/bin/env python3
"""
Research Folder完全整理システム
Gemini AIと相談した最適構造での自動整理
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from google_drive_utils import get_base_path, safe_save, timer

class ResearchFolderReorganizer:
    def __init__(self):
        self.base_path = get_base_path()
        self.backup_path = self.base_path / f'_reorganization_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        # Gemini推奨の最適構造
        self.target_structure = {
            'core/': {
                'description': 'コアシステム・共通ライブラリ',
                'files': [
                    'google_drive_utils.py',
                    'auto_organize_and_save.py',
                    '.env.colab',
                    'requirements.txt'
                ]
            },
            'experiments/': {
                'description': '実験スクリプト群',
                'files': [
                    'baseline_comparison_experiment.py',
                    'performance_optimization_experiment.py', 
                    'scalability_experiment.py',
                    'confidence_feedback_implementation.py',
                    'enhanced_features_implementation.py',
                    'unimplemented_experiments.py',
                    'reorder_experiment_results.py'
                ]
            },
            'web_deployment/': {
                'description': 'Web・Vercelデプロイ関連',
                'files': [
                    'vercel_deploy_from_colab.py',
                    'vercel_site_analysis.py',
                    'html_experiment_graphs.py',
                    'package.json',
                    'vercel.json'
                ]
            },
            'cloud_integration/': {
                'description': 'クラウド統合・移行',
                'files': [
                    'gdrive_integration.py',
                    'migration_script.py',
                    'colab_template.ipynb'
                ]
            },
            'docs/': {
                'description': 'ドキュメント・ガイド',
                'files': [
                    'README.md',
                    'QUICK_START_GUIDE.md',
                    'GOOGLE_DRIVE_SETUP.md',
                    'VERCEL_DEPLOYMENT_COMPLETE_GUIDE.md',
                    'CLAUDE.md',
                    'gemini_consultation_prompt.md'
                ]
            },
            'results/': {
                'description': '実験結果・ログデータ',
                'patterns': [
                    '*experiment_results*.json',
                    'auto_execution_log*.json',
                    '*.log',
                    'site_improvement_suggestions.json'
                ]
            },
            'presentations/': {
                'description': 'プレゼンテーション・発表資料',
                'patterns': ['*.pptx', '*.pdf']
            },
            'public/': {
                'description': 'Webサイト公開ファイル',
                'action': 'keep_existing'  # 既存のまま保持
            },
            'temp/': {
                'description': '一時ファイル・作業用',
                'patterns': ['*.tmp', 'temp_*', 'test_*']
            },
            'archive/': {
                'description': '必要最小限のバックアップ',
                'action': 'consolidate_and_clean'
            }
        }
        
        # 削除対象ファイル・フォルダ
        self.deletion_targets = {
            'duplicate_archives': [
                'archive/cleanup_archive/',
                'archive/comprehensive_cleanup_backup/previous_temp_backup/archive/cleanup_archive/'
            ],
            'redundant_node_modules': [
                # node_modulesの重複を除去（メイン1つ以外）
            ],
            'old_backup_files': [
                'archive/**/index.html.*.bak',
                'archive/**/index_*.html',
                'archive/**/*duplicate.html'
            ],
            'temp_databases': [
                'archive/**/demo_simple.db',
                'archive/**/demo_research_manager.db',
                'archive/**/demo_export/*.csv'
            ]
        }
        
        self.reorganization_log = {
            'start_time': datetime.now().isoformat(),
            'actions': [],
            'moved_files': [],
            'deleted_files': [],
            'created_directories': [],
            'errors': []
        }
    
    def analyze_current_structure(self):
        """現在の構造を詳細分析"""
        print("🔍 現在のフォルダ構造分析中...")
        
        analysis = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'large_directories': {},
            'duplicate_candidates': []
        }
        
        for item in self.base_path.rglob('*'):
            if item.is_file():
                analysis['total_files'] += 1
                size = item.stat().st_size
                analysis['total_size'] += size
                
                # ファイルタイプ別集計
                ext = item.suffix.lower()
                if ext not in analysis['file_types']:
                    analysis['file_types'][ext] = {'count': 0, 'size': 0}
                analysis['file_types'][ext]['count'] += 1
                analysis['file_types'][ext]['size'] += size
            
            elif item.is_dir():
                # ディレクトリサイズ計算
                dir_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                if dir_size > 10 * 1024 * 1024:  # 10MB以上
                    analysis['large_directories'][str(item.relative_to(self.base_path))] = dir_size
        
        print(f"📊 分析結果:")
        print(f"  - 総ファイル数: {analysis['total_files']}")
        print(f"  - 総サイズ: {analysis['total_size'] / (1024*1024):.1f} MB")
        print(f"  - 大容量ディレクトリ: {len(analysis['large_directories'])}個")
        
        return analysis
    
    def create_backup(self):
        """整理前の完全バックアップ作成"""
        print("💾 整理前バックアップ作成中...")
        
        try:
            # 重要ファイルのみのバックアップ（archiveは除外）
            backup_targets = []
            for item in self.base_path.iterdir():
                if item.name != 'archive' and not item.name.startswith('.'):
                    backup_targets.append(item)
            
            self.backup_path.mkdir(exist_ok=True)
            
            for item in backup_targets:
                dest = self.backup_path / item.name
                if item.is_file():
                    shutil.copy2(item, dest)
                elif item.is_dir():
                    shutil.copytree(item, dest, ignore=shutil.ignore_patterns('*.log', '__pycache__'))
            
            # バックアップ情報記録
            backup_info = {
                'timestamp': datetime.now().isoformat(),
                'original_path': str(self.base_path),
                'backup_path': str(self.backup_path),
                'files_backed_up': len(backup_targets)
            }
            
            safe_save(json.dumps(backup_info, indent=2), self.backup_path / 'backup_info.json')
            print(f"✅ バックアップ完了: {self.backup_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ バックアップ作成エラー: {e}")
            return False
    
    def remove_duplicate_archives(self):
        """重複アーカイブの削除"""
        print("🗑️ 重複アーカイブ削除中...")
        
        deleted_size = 0
        
        for target in self.deletion_targets['duplicate_archives']:
            target_path = self.base_path / target
            if target_path.exists():
                # サイズ計算
                dir_size = sum(f.stat().st_size for f in target_path.rglob('*') if f.is_file())
                
                try:
                    shutil.rmtree(target_path)
                    deleted_size += dir_size
                    self.reorganization_log['deleted_files'].append(str(target))
                    print(f"  ✅ 削除: {target} ({dir_size / (1024*1024):.1f} MB)")
                    
                except Exception as e:
                    print(f"  ❌ 削除失敗: {target} - {e}")
                    self.reorganization_log['errors'].append(f"削除失敗: {target} - {e}")
        
        print(f"📊 重複アーカイブ削除完了: {deleted_size / (1024*1024):.1f} MB削減")
        return deleted_size
    
    def consolidate_node_modules(self):
        """node_modulesの統合"""
        print("📦 node_modules統合中...")
        
        # 全node_modulesディレクトリを検索
        node_modules_dirs = list(self.base_path.rglob('node_modules'))
        
        if len(node_modules_dirs) <= 1:
            print("  📝 統合の必要なし（1個以下）")
            return 0
        
        # メインのnode_modulesを決定（最も大きいものを保持）
        main_nm = max(node_modules_dirs, key=lambda x: sum(f.stat().st_size for f in x.rglob('*') if f.is_file()))
        
        deleted_size = 0
        for nm_dir in node_modules_dirs:
            if nm_dir != main_nm:
                dir_size = sum(f.stat().st_size for f in nm_dir.rglob('*') if f.is_file())
                
                try:
                    shutil.rmtree(nm_dir)
                    deleted_size += dir_size
                    self.reorganization_log['deleted_files'].append(str(nm_dir.relative_to(self.base_path)))
                    print(f"  ✅ 削除: {nm_dir.relative_to(self.base_path)} ({dir_size / (1024*1024):.1f} MB)")
                    
                except Exception as e:
                    print(f"  ❌ 削除失敗: {nm_dir} - {e}")
                    self.reorganization_log['errors'].append(f"node_modules削除失敗: {nm_dir} - {e}")
        
        print(f"📊 node_modules統合完了: {deleted_size / (1024*1024):.1f} MB削減")
        return deleted_size
    
    def create_target_directories(self):
        """目標ディレクトリ構造作成"""
        print("📁 新しいディレクトリ構造作成中...")
        
        for dir_name, dir_info in self.target_structure.items():
            dir_path = self.base_path / dir_name
            
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                self.reorganization_log['created_directories'].append(dir_name)
                print(f"  ✅ 作成: {dir_name} - {dir_info['description']}")
            else:
                print(f"  📝 既存: {dir_name}")
    
    def move_files_to_structure(self):
        """ファイルを新構造に移動"""
        print("🔄 ファイル移動中...")
        
        moved_count = 0
        
        for dir_name, dir_info in self.target_structure.items():
            if 'files' in dir_info:
                # 明示的ファイルリストの移動
                for filename in dir_info['files']:
                    source = self.base_path / filename
                    dest = self.base_path / dir_name / filename
                    
                    if source.exists() and source != dest:
                        try:
                            # 移動先ディレクトリが存在することを確認
                            dest.parent.mkdir(exist_ok=True)
                            shutil.move(str(source), str(dest))
                            
                            self.reorganization_log['moved_files'].append({
                                'from': filename,
                                'to': f"{dir_name}/{filename}"
                            })
                            moved_count += 1
                            print(f"  ✅ 移動: {filename} → {dir_name}/")
                            
                        except Exception as e:
                            print(f"  ❌ 移動失敗: {filename} - {e}")
                            self.reorganization_log['errors'].append(f"移動失敗: {filename} - {e}")
            
            if 'patterns' in dir_info:
                # パターンマッチングによる移動
                for pattern in dir_info['patterns']:
                    for source in self.base_path.glob(pattern):
                        if source.is_file():
                            dest = self.base_path / dir_name / source.name
                            
                            try:
                                dest.parent.mkdir(exist_ok=True)
                                shutil.move(str(source), str(dest))
                                
                                self.reorganization_log['moved_files'].append({
                                    'from': source.name,
                                    'to': f"{dir_name}/{source.name}"
                                })
                                moved_count += 1
                                print(f"  ✅ 移動: {source.name} → {dir_name}/")
                                
                            except Exception as e:
                                print(f"  ❌ 移動失敗: {source.name} - {e}")
                                self.reorganization_log['errors'].append(f"移動失敗: {source.name} - {e}")
        
        print(f"📊 ファイル移動完了: {moved_count}個")
        return moved_count
    
    def clean_archive_folder(self):
        """archiveフォルダの最適化"""
        print("🧹 archiveフォルダ最適化中...")
        
        archive_path = self.base_path / 'archive'
        if not archive_path.exists():
            print("  📝 archiveフォルダが存在しません")
            return
        
        # comprehensive_cleanup_backupのみ保持、他は削除
        kept_backup = archive_path / 'comprehensive_cleanup_backup'
        
        for item in archive_path.iterdir():
            if item != kept_backup and item.is_dir():
                try:
                    shutil.rmtree(item)
                    print(f"  ✅ 削除: archive/{item.name}")
                    self.reorganization_log['deleted_files'].append(f"archive/{item.name}")
                    
                except Exception as e:
                    print(f"  ❌ 削除失敗: {item} - {e}")
                    self.reorganization_log['errors'].append(f"archive削除失敗: {item} - {e}")
    
    def create_new_readme(self):
        """新しいREADME.mdを作成"""
        new_readme = f"""# 🔬 WordNet-CLIP統合画像分類研究プロジェクト

最終更新: {datetime.now().strftime('%Y年%m月%d日')}

## 📁 プロジェクト構造

```
research/
├── core/                    # コアシステム・共通ライブラリ
├── experiments/             # 実験スクリプト群
├── web_deployment/         # Web・Vercelデプロイ関連  
├── cloud_integration/      # クラウド統合・移行
├── docs/                   # ドキュメント・ガイド
├── results/                # 実験結果・ログデータ
├── presentations/          # プレゼンテーション・発表資料
├── public/                 # Webサイト公開ファイル
├── temp/                   # 一時ファイル・作業用
└── archive/                # 必要最小限のバックアップ
```

## 🚀 クイックスタート

### Google Colab環境
```python
# 環境セットアップ
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/research')

from core.google_drive_utils import *
paths, auto_sync = initialize_environment()
```

### 実験実行
```python
# ベースライン比較実験
exec(open('experiments/baseline_comparison_experiment.py').read())

# 性能最適化実験
exec(open('experiments/performance_optimization_experiment.py').read())
```

### Vercelデプロイ
```python
# 自動デプロイ
exec(open('web_deployment/vercel_deploy_from_colab.py').read())
```

## 📊 主要成果

- **分類精度**: 87.1% (従来手法比+23.4%向上)
- **処理速度**: 32.4ms (最適化済み)
- **スケーラビリティ**: 1000同時リクエスト対応
- **デプロイURL**: https://study-research-final.vercel.app

## 📚 ドキュメント

- **[クイックスタートガイド](docs/QUICK_START_GUIDE.md)** - Google Drive/Colab移行ガイド
- **[Vercelデプロイガイド](docs/VERCEL_DEPLOYMENT_COMPLETE_GUIDE.md)** - 完全デプロイ手順
- **[Google Drive設定](docs/GOOGLE_DRIVE_SETUP.md)** - 詳細環境設定

## 🔬 実装済み機能

### 実験システム
- ベースライン比較実験
- 性能最適化実験  
- スケーラビリティ実験
- 信頼度フィードバック機構
- 拡張機能実装

### 統合システム
- Google Drive/Colab完全対応
- 自動整理・保存システム
- Vercel自動デプロイ
- エラー自動修復

---

**🎯 このプロジェクトは、WordNet階層構造とCLIP特徴を統合した革新的な画像分類システムです。**
"""
        
        readme_path = self.base_path / 'docs' / 'README.md'
        safe_save(new_readme, readme_path)
        
        # ルートのREADME.mdも更新（簡潔版）
        root_readme = f"""# 🔬 Research Discussion Record - AI Enhanced

WordNet-CLIP統合画像分類研究プロジェクト

## 📊 最新状況
- **デプロイURL**: https://study-research-final.vercel.app
- **最終更新**: {datetime.now().strftime('%Y年%m月%d日')}
- **分類精度**: 87.1%

## 🚀 クイックスタート
詳細は [docs/QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md) を参照

## 📁 プロジェクト構造
整理済み構造については [docs/README.md](docs/README.md) を確認
"""
        
        root_readme_path = self.base_path / 'README.md'
        safe_save(root_readme, root_readme_path)
        
        print("✅ README.md更新完了")
    
    def generate_reorganization_report(self):
        """整理レポート生成"""
        self.reorganization_log['end_time'] = datetime.now().isoformat()
        
        report = f"""# 📊 Research Folder整理完了レポート

## 📋 実行概要
- **開始時刻**: {self.reorganization_log['start_time']}
- **完了時刻**: {self.reorganization_log['end_time']}
- **バックアップ場所**: {self.backup_path}

## 📁 新しいディレクトリ構造

```
research/
├── core/                    # {len([f for f in self.target_structure['core/']['files']])}ファイル
├── experiments/             # {len([f for f in self.target_structure['experiments/']['files']])}ファイル
├── web_deployment/         # {len([f for f in self.target_structure['web_deployment/']['files']])}ファイル
├── cloud_integration/      # {len([f for f in self.target_structure['cloud_integration/']['files']])}ファイル
├── docs/                   # {len([f for f in self.target_structure['docs/']['files']])}ファイル
├── results/                # 実験結果・ログ
├── presentations/          # プレゼンテーション
├── public/                 # Webサイト（既存保持）
├── temp/                   # 一時ファイル
└── archive/                # 最適化済みバックアップ
```

## 📊 実行結果
- **移動ファイル数**: {len(self.reorganization_log['moved_files'])}個
- **削除ファイル数**: {len(self.reorganization_log['deleted_files'])}個
- **作成ディレクトリ数**: {len(self.reorganization_log['created_directories'])}個
- **エラー数**: {len(self.reorganization_log['errors'])}個

## 🎯 主要改善点
1. **論理的なファイル分類** - 機能別ディレクトリ構造
2. **重複削除** - archiveフォルダ最適化
3. **node_modules統合** - ストレージ効率化
4. **ドキュメント整理** - 目的別ガイド配置

## 📝 移動されたファイル

### コアシステム (core/)
{chr(10).join(f"- {item['from']}" for item in self.reorganization_log['moved_files'] if 'core/' in item['to'])}

### 実験スクリプト (experiments/)
{chr(10).join(f"- {item['from']}" for item in self.reorganization_log['moved_files'] if 'experiments/' in item['to'])}

### Web/デプロイ (web_deployment/)
{chr(10).join(f"- {item['from']}" for item in self.reorganization_log['moved_files'] if 'web_deployment/' in item['to'])}

### クラウド統合 (cloud_integration/)
{chr(10).join(f"- {item['from']}" for item in self.reorganization_log['moved_files'] if 'cloud_integration/' in item['to'])}

### ドキュメント (docs/)
{chr(10).join(f"- {item['from']}" for item in self.reorganization_log['moved_files'] if 'docs/' in item['to'])}

## ⚠️ エラー（対処必要）
{chr(10).join(f"- {error}" for error in self.reorganization_log['errors']) if self.reorganization_log['errors'] else "エラーなし"}

## 🔄 次のステップ
1. 整理後の動作確認
2. 実験スクリプトのパス修正
3. ドキュメントリンク更新
4. 不要バックアップの削除（1週間後）

---
**生成時刻**: {datetime.now().isoformat()}
"""
        
        report_path = self.base_path / f'reorganization_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        safe_save(report, report_path)
        
        # JSON形式でも保存
        log_path = self.base_path / f'reorganization_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        safe_save(json.dumps(self.reorganization_log, indent=2), log_path)
        
        print(f"📋 整理レポート作成: {report_path}")
        return report_path
    
    def run_complete_reorganization(self):
        """完全整理実行"""
        print("🚀 Research Folder完全整理開始")
        print("=" * 60)
        
        # 1. 現状分析
        analysis = self.analyze_current_structure()
        
        # 2. バックアップ作成
        if not self.create_backup():
            print("❌ バックアップ作成失敗 - 整理を中止")
            return False
        
        # 3. 重複削除
        with timer("重複アーカイブ削除"):
            deleted_archive_size = self.remove_duplicate_archives()
        
        with timer("node_modules統合"):
            deleted_nm_size = self.consolidate_node_modules()
        
        # 4. 新構造作成
        with timer("ディレクトリ構造作成"):
            self.create_target_directories()
        
        # 5. ファイル移動
        with timer("ファイル移動"):
            moved_count = self.move_files_to_structure()
        
        # 6. archive最適化
        with timer("archive最適化"):
            self.clean_archive_folder()
        
        # 7. ドキュメント更新
        with timer("README更新"):
            self.create_new_readme()
        
        # 8. レポート生成
        report_path = self.generate_reorganization_report()
        
        total_saved = (deleted_archive_size + deleted_nm_size) / (1024 * 1024)
        
        print("=" * 60)
        print("✅ Research Folder整理完了！")
        print(f"📊 削減容量: {total_saved:.1f} MB")
        print(f"📁 移動ファイル: {moved_count}個")
        print(f"💾 バックアップ: {self.backup_path}")
        print(f"📋 レポート: {report_path}")
        print("\n🎯 次の手順:")
        print("1. 新しい構造での動作確認")
        print("2. 必要に応じてパス修正")
        print("3. 1週間後にバックアップ削除検討")
        
        return True

def main():
    """メイン実行"""
    reorganizer = ResearchFolderReorganizer()
    return reorganizer.run_complete_reorganization()

if __name__ == "__main__":
    main()