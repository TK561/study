# 🚀 Google Colab での研究プロジェクト実行ガイド

このガイドでは、研究プロジェクトをGoogle Colabで実行する方法を説明します。

## 📋 事前準備

### 1. 必要なアカウント
- **Google アカウント**: Colab へのアクセス用
- **GitHub アカウント**: コードの管理用（オプション）
- **Vercel アカウント**: デプロイ用（オプション）

### 2. Colab環境の制限事項
- **セッション時間**: 最大12時間（Pro版は24時間）
- **RAM**: 12GB（Pro版は25GB）
- **ストレージ**: 一時的（セッション終了時に削除）
- **GPU**: 使用可能（Pro版で優先アクセス）

## 🎯 クイックスタート

### 方法1: ノートブックを直接使用

1. **ノートブックをColabで開く**
   ```
   https://colab.research.google.com/
   ```

2. **プロジェクトファイルをアップロード**
   - `Research_Project_Colab.ipynb` をアップロード
   - または GitHub から直接開く

3. **セルを順番に実行**
   - 環境セットアップ
   - ファイルアップロード
   - メインスクリプト実行

### 方法2: GitHubから直接開く

1. **GitHub URL を使用**
   ```
   https://colab.research.google.com/github/yourusername/research-project/blob/main/Research_Project_Colab.ipynb
   ```

2. **リポジトリをクローン**
   ```python
   !git clone https://github.com/yourusername/research-project.git
   %cd research-project
   ```

## 🔧 セットアップ手順

### 1. 環境確認
```python
# Colab環境かどうかの確認
try:
    import google.colab
    print("✅ Google Colab環境で実行中")
    IN_COLAB = True
except:
    print("❌ ローカル環境で実行中")
    IN_COLAB = False
```

### 2. 依存関係のインストール
```python
# 自動セットアップスクリプトの実行
exec(open('colab_setup.py').read())
```

または手動で：
```python
!pip install numpy pandas matplotlib seaborn plotly beautifulsoup4 requests
```

### 3. Google Driveのマウント
```python
from google.colab import drive
drive.mount('/content/drive')
```

### 4. プロジェクトファイルのアップロード
```python
from google.colab import files

# ファイルを選択してアップロード
uploaded = files.upload()

# または複数ファイルを一括アップロード
# ZIPファイルをアップロードして展開
!unzip project.zip
```

## 📁 ファイル構成（Colab用）

```
/content/research_project/
├── Research_Project_Colab.ipynb  # メインノートブック
├── colab_setup.py                # 環境セットアップ
├── colab_compatibility.py        # 互換性ユーティリティ
├── public/                       # Webファイル
├── sessions/                     # セッション記録
└── backups/                      # バックアップ
```

## 🔄 自動保存・バックアップ

### 1. セッション保存
```python
# 自動保存の実行
from colab_compatibility import auto_organize_and_save_colab
auto_organize_and_save_colab()
```

### 2. Google Driveへのバックアップ
```python
# Driveにバックアップ
from colab_compatibility import backup_to_drive
backup_to_drive('sessions/', 'research_backup')
```

### 3. 定期自動保存（Pro版推奨）
```python
# 30分ごとの自動保存
from colab_compatibility import periodic_save
periodic_save(30)
```

## 📊 Vercel デプロイ（Colab版）

### 1. Vercel CLI のインストール
```python
!npm install -g vercel
```

### 2. 認証設定
```python
# Vercel トークンの設定
import os
os.environ['VERCEL_TOKEN'] = 'your_vercel_token_here'
```

### 3. デプロイ実行
```python
# 設定確認
!vercel --version

# デプロイ
!vercel --prod
```

## 🛠️ トラブルシューティング

### セッション切断対策
```python
# 定期的にダミー処理を実行してセッションを維持
import time
import threading

def keep_alive():
    while True:
        time.sleep(300)  # 5分ごと
        print("⏰ Keep alive")

# バックグラウンドで実行
threading.Thread(target=keep_alive, daemon=True).start()
```

### メモリ不足対策
```python
# メモリ使用量の確認
!free -h

# 不要な変数をクリア
import gc
gc.collect()

# 大きなデータを削除
del large_variable
```

### ファイルダウンロード
```python
# 単一ファイルのダウンロード
from google.colab import files
files.download('result.html')

# プロジェクト全体をZIPでダウンロード
import shutil
shutil.make_archive('research_project', 'zip', '/content/research_project')
files.download('research_project.zip')
```

## 📚 使用例

### 基本的な実行フロー
```python
# 1. 環境セットアップ
exec(open('colab_setup.py').read())

# 2. 互換性ライブラリの読み込み
from colab_compatibility import *

# 3. プロジェクトの初期化
init_colab_env()

# 4. メインスクリプトの実行
exec(open('auto_organize_and_save.py').read())

# 5. 結果の保存
auto_organize_and_save_colab()

# 6. ファイルのダウンロード
download_file('sessions/AUTO_SESSION_SAVE_2024-12-23.md')
```

### データ処理と可視化
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# データの読み込み
df = pd.read_csv('data.csv')

# 可視化
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='date', y='value')
plt.title('Research Results')
plt.show()

# 結果をHTMLに出力
html_output = df.to_html()
with open('results.html', 'w') as f:
    f.write(html_output)
```

## 🎯 Pro Tips

### 1. 効率的なファイル管理
- 定期的にGoogle Driveにバックアップ
- 重要なファイルは複数の場所に保存
- セッション終了前に必ずダウンロード

### 2. リソース管理
- 不要な変数は削除してメモリを節約
- 大きなファイルはGoogle Driveに保存
- GPU使用時は適切に解放

### 3. 共同作業
- GitHub連携でバージョン管理
- Colab共有機能でリアルタイム協力
- コメント機能で議論を記録

## 🔗 関連リンク

- [Google Colab 公式ドキュメント](https://colab.research.google.com/)
- [Colab Pro 機能比較](https://colab.research.google.com/signup)
- [GitHub - Colab 連携](https://colab.research.google.com/github)
- [Vercel ドキュメント](https://vercel.com/docs)

---

**注意**: このガイドは研究プロジェクト専用に作成されています。使用前に最新の情報を確認してください。