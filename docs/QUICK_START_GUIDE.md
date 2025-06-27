# 🚀 Google Drive/Colab クイックスタートガイド

VSCodeからGoogle Drive/Colabへの移行が完了しました。このガイドで素早く開始できます。

## 📋 移行完了内容

✅ **環境自動検出システム**  
✅ **パス参照の自動変換**  
✅ **Colab専用ユーティリティ**  
✅ **自動保存・同期システム**  
✅ **Google Drive統合機能**  
✅ **移行スクリプト一式**  

## 🎯 今すぐ始める手順

### 1. Colabでの基本セットアップ

新しいColabノートブックを開いて以下を実行：

```python
# === 必須：最初のセルで実行 ===
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/research')

# 共通ユーティリティ読み込み
from google_drive_utils import *
paths, auto_sync = initialize_environment()
```

### 2. テンプレートノートブックを使用

```bash
# 準備済みテンプレートをコピー
cp colab_template.ipynb my_new_project.ipynb
```

### 3. 既存スクリプトの移行（必要な場合）

```python
# 移行スクリプトの実行
python migration_script.py
```

## 📁 重要なファイル

| ファイル | 説明 |
|---------|------|
| `google_drive_utils.py` | 共通ユーティリティ（必須） |
| `colab_template.ipynb` | Colabテンプレート |
| `GOOGLE_DRIVE_SETUP.md` | 詳細セットアップガイド |
| `migration_script.py` | 既存ファイル移行用 |
| `gdrive_integration.py` | Drive統合機能 |
| `.env.colab` | 環境設定ファイル |

## 🔧 よく使う機能

### ファイルの安全な保存
```python
# 自動バックアップ付き保存
safe_save(content, 'output.json')

# JSONデータの保存
save_json(data, 'results.json')
```

### 実行時間の計測
```python
with timer("実験実行"):
    # 時間のかかる処理
    pass
```

### 進捗の記録
```python
progress = ProgressLogger(100, "データ処理")
for i in range(100):
    # 処理
    progress.update(f"処理中: {i+1}")
```

### 自動同期
```python
# 変更ファイルの検出・同期
changed = auto_sync.sync_now()
```

## 🌐 Google Drive特有機能

### リアルタイム同期設定
```python
from gdrive_integration import GoogleDriveIntegration
gdi = GoogleDriveIntegration()
gdi.setup_real_time_sync()
```

### 自動バックアップ設定
```python
gdi.setup_automated_backup()
```

### ファイル検索
```python
# 検索インデックス作成
exec(open('search_indexer.py').read())

# ファイル検索実行
results = search_files("experiment")
```

## 📊 既存プロジェクトの活用

### 実験スクリプトの実行
```python
# ベースライン比較実験
exec(open('baseline_comparison_experiment.py').read())

# 性能最適化実験  
exec(open('performance_optimization_experiment.py').read())

# スケーラビリティ実験
exec(open('scalability_experiment.py').read())
```

### Webサイトの確認
```python
# サイト分析
exec(open('vercel_site_analysis.py').read())
```

## 🎮 便利なショートカット

### ナビゲーションメニュー表示
```python
create_navigation_menu()
```

### 最近のファイル表示
```python
recent_files = list_recent_files()
for file_info in recent_files[:10]:
    print(f"{file_info['path']} - {file_info['modified']}")
```

### システム情報確認
```python
from colab_extensions import get_system_info
info = get_system_info()
print(f"CPU: {info['cpu_percent']}%")
print(f"Memory: {info['memory_percent']}%")
print(f"GPU: {info['gpu_percent']}%")
```

## 🔄 定期的なメンテナンス

### 週次実行推奨
```python
# 1. 自動整理・保存
exec(open('auto_organize_and_save.py').read())

# 2. 検索インデックス更新
exec(open('search_indexer.py').read())

# 3. バックアップ作成
exec(open('automated_backup.py').read())
```

## 🚨 トラブルシューティング

### マウントエラーの場合
```python
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
```

### パスエラーの場合
```python
import os
print(f"現在のディレクトリ: {os.getcwd()}")
os.chdir('/content/drive/MyDrive/research')
```

### ライブラリエラーの場合
```python
!pip install -q pandas numpy matplotlib seaborn google-generativeai
```

## 📞 ヘルプとサポート

- **詳細ガイド**: `GOOGLE_DRIVE_SETUP.md`
- **設定リファレンス**: `.env.colab`
- **API統合**: `gdrive_integration.py`
- **エラーログ**: `logs/errors.log`

## 🎉 次のステップ

1. **既存実験の実行**: 移行された実験スクリプトを実行
2. **新機能の探索**: Google Drive統合機能を試用
3. **カスタマイズ**: 自分のワークフローに合わせて設定調整
4. **共有・協力**: Driveの共有機能を活用

---

**🎯 重要**: 初回セットアップ後は、各Colabノートブックで最初のセルを実行するだけで環境が整います！