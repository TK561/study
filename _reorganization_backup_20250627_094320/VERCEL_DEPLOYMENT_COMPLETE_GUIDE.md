# 🚀 Vercel完全デプロイガイド - Google Drive/Colab対応

Google Drive環境からVercelへの完璧なデプロイ手順です。

## 📋 現在のデプロイ状況

✅ **デプロイ済みサイト**: https://study-research-final.vercel.app  
✅ **静的サイト構成**: Python APIハンドラー不使用  
✅ **自動最適化システム**: AI支援デプロイ完備  
✅ **エラー対策システム**: 自動修復機能搭載  

## 🎯 Google Drive → Vercel デプロイ手順

### 1. 事前準備（Colab/Drive環境）

```python
# === Colab環境でのVercelデプロイ準備 ===

# 1. 環境セットアップ
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/research')

from google_drive_utils import *
paths, auto_sync = initialize_environment()

# 2. 現在のサイト状況確認
exec(open('vercel_site_analysis.py').read())
```

### 2. Vercel CLI設定（初回のみ）

```bash
# Colab環境でのVercel CLI設定
!npm install -g vercel

# Vercelアカウント認証（ブラウザで認証）
!vercel login

# プロジェクト初期化（既に設定済みの場合はスキップ）
!vercel --cwd /content/drive/MyDrive/research/public
```

### 3. 完全自動デプロイ（推奨）

```python
# === AI支援付き完全自動デプロイ ===

# 1. デプロイ前チェック・最適化
def prepare_deployment():
    """デプロイ前の完全チェック"""
    
    # publicディレクトリ確認
    public_dir = paths.get('public')
    if not public_dir.exists():
        print("❌ publicディレクトリが見つかりません")
        return False
    
    # 必須ファイル確認
    required_files = [
        'index.html',
        'main-system/index.html', 
        'confidence_feedback/index.html',
        'pptx_systems/index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (public_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 必須ファイル不足: {missing_files}")
        return False
    
    # vercel.json確認・作成
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "public/**/*",
                "use": "@vercel/static"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/public/$1"
            }
        ],
        "functions": {},
        "rewrites": [
            {
                "source": "/",
                "destination": "/public/index.html"
            },
            {
                "source": "/main-system",
                "destination": "/public/main-system/index.html"
            },
            {
                "source": "/confidence_feedback", 
                "destination": "/public/confidence_feedback/index.html"
            },
            {
                "source": "/pptx_systems",
                "destination": "/public/pptx_systems/index.html"
            }
        ]
    }
    
    # vercel.json保存
    vercel_path = paths.base_path / 'vercel.json'
    save_json(vercel_config, vercel_path)
    
    print("✅ デプロイ準備完了")
    return True

# 2. 自動デプロイ実行
def auto_deploy():
    """完全自動デプロイ"""
    
    if not prepare_deployment():
        return False
    
    # バックアップ作成
    backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = paths.get('backups') / f'pre_deploy_{backup_timestamp}'
    backup_dir.mkdir(exist_ok=True)
    
    import shutil
    shutil.copytree(paths.get('public'), backup_dir / 'public')
    print(f"💾 デプロイ前バックアップ: {backup_dir}")
    
    # Vercelデプロイ実行
    try:
        os.chdir(paths.base_path)
        
        # 本番デプロイ
        deploy_result = os.system('vercel --prod --yes')
        
        if deploy_result == 0:
            print("✅ Vercelデプロイ成功！")
            print("🌐 URL: https://study-research-final.vercel.app")
            
            # デプロイ成功ログ
            deploy_log = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'backup_location': str(backup_dir),
                'deployed_url': 'https://study-research-final.vercel.app'
            }
            save_json(deploy_log, paths.get('logs') / f'deploy_success_{backup_timestamp}.json')
            
            return True
        else:
            print("❌ デプロイ失敗")
            return False
            
    except Exception as e:
        print(f"❌ デプロイエラー: {e}")
        return False

# 実行
if prepare_deployment():
    auto_deploy()
```

### 4. 手動デプロイ（詳細制御が必要な場合）

```bash
# === 手動デプロイ手順 ===

# 1. 作業ディレクトリ移動
cd /content/drive/MyDrive/research

# 2. 本番デプロイ実行
vercel --prod --yes

# 3. カスタムドメイン設定（必要な場合）
vercel domains add study-research-final.vercel.app

# 4. 環境変数設定（必要な場合）
vercel env add PRODUCTION_MODE true production
```

### 5. デプロイ後の確認・最適化

```python
# === デプロイ後確認 ===

def verify_deployment():
    """デプロイ結果確認"""
    
    import requests
    
    # メインページ確認
    urls_to_check = [
        'https://study-research-final.vercel.app/',
        'https://study-research-final.vercel.app/main-system/',
        'https://study-research-final.vercel.app/confidence_feedback/',
        'https://study-research-final.vercel.app/pptx_systems/'
    ]
    
    results = {}
    
    for url in urls_to_check:
        try:
            response = requests.get(url, timeout=10)
            results[url] = {
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content),
                'success': response.status_code == 200
            }
            
            if response.status_code == 200:
                print(f"✅ {url} - OK ({response.elapsed.total_seconds():.2f}s)")
            else:
                print(f"❌ {url} - Error {response.status_code}")
                
        except Exception as e:
            results[url] = {'error': str(e), 'success': False}
            print(f"❌ {url} - Error: {e}")
    
    # 結果保存
    verification_log = {
        'timestamp': datetime.now().isoformat(),
        'verification_results': results,
        'overall_success': all(r.get('success', False) for r in results.values())
    }
    
    save_json(verification_log, paths.get('logs') / f'deployment_verification_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    return verification_log['overall_success']

# 実行
verify_deployment()
```

## 🔧 トラブルシューティング

### よくある問題と解決法

#### 1. Build Error
```bash
# エラーログ確認
vercel logs https://study-research-final.vercel.app

# 設定確認
cat vercel.json

# 再デプロイ
vercel --prod --yes --force
```

#### 2. 404 Error
```python
# ルーティング確認・修正
def fix_routing():
    vercel_config = load_json('vercel.json')
    
    # 正しいルーティング設定
    vercel_config['rewrites'] = [
        {"source": "/", "destination": "/public/index.html"},
        {"source": "/main-system/(.*)", "destination": "/public/main-system/$1"},
        {"source": "/confidence_feedback/(.*)", "destination": "/public/confidence_feedback/$1"},
        {"source": "/pptx_systems/(.*)", "destination": "/public/pptx_systems/$1"}
    ]
    
    save_json(vercel_config, 'vercel.json')
    print("✅ ルーティング修正完了")

fix_routing()
```

#### 3. Performance Issues
```python
# 最適化実行
def optimize_for_vercel():
    """Vercel最適化"""
    
    # 1. HTMLの最小化
    public_dir = paths.get('public')
    
    for html_file in public_dir.rglob('*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基本的な最小化
        import re
        content = re.sub(r'\s+', ' ', content)  # 余分な空白削除
        content = re.sub(r'>\s+<', '><', content)  # タグ間空白削除
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # 2. メタデータ追加
    for html_file in public_dir.rglob('index.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # パフォーマンス向上メタタグ
        perf_meta = '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#667eea">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="dns-prefetch" href="https://fonts.gstatic.com">
        '''
        
        if '<head>' in content and perf_meta not in content:
            content = content.replace('<head>', f'<head>{perf_meta}')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("✅ Vercel最適化完了")

optimize_for_vercel()
```

## 🚀 高度な機能

### 1. 自動デプロイ（Git Push連携）

```bash
# Git設定（初回のみ）
git init
git remote add origin https://github.com/yourusername/research-project.git

# .gitignore設定
echo "*.log
*.pyc
__pycache__/
.env
backups/
temp/" > .gitignore

# 自動デプロイ設定
vercel git connect
```

### 2. 環境変数管理

```bash
# 本番環境変数設定
vercel env add API_KEY "your-api-key" production
vercel env add DEBUG_MODE "false" production
vercel env add CACHE_ENABLED "true" production
```

### 3. カスタムドメイン

```bash
# カスタムドメイン追加
vercel domains add your-custom-domain.com

# SSL証明書自動設定（Vercelが自動実行）
```

## 📊 デプロイ状況監視

### リアルタイム監視スクリプト

```python
def monitor_deployment():
    """デプロイ状況の継続監視"""
    
    import time
    
    while True:
        try:
            response = requests.get('https://study-research-final.vercel.app/', timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {datetime.now().strftime('%H:%M:%S')} - サイト正常稼働")
            else:
                print(f"⚠️ {datetime.now().strftime('%H:%M:%S')} - エラー {response.status_code}")
                
        except Exception as e:
            print(f"❌ {datetime.now().strftime('%H:%M:%S')} - 接続エラー: {e}")
        
        time.sleep(300)  # 5分間隔

# バックグラウンド監視開始
# monitor_deployment()
```

## 🎯 完璧なワークフロー

### Google Drive → Vercel 完全自動化

```python
def perfect_deployment_workflow():
    """完璧なデプロイワークフロー"""
    
    print("🚀 完全自動デプロイワークフロー開始")
    
    # 1. 環境初期化
    from google_drive_utils import *
    paths, auto_sync = initialize_environment()
    
    # 2. ファイル同期
    changed = auto_sync.sync_now()
    if changed:
        print(f"🔄 {len(changed)}個のファイルを同期")
    
    # 3. デプロイ前最適化
    optimize_for_vercel()
    
    # 4. 自動デプロイ
    success = auto_deploy()
    
    # 5. デプロイ後確認
    if success:
        verify_deployment()
        print("✅ 完全自動デプロイ成功！")
        return True
    else:
        print("❌ デプロイ失敗")
        return False

# 実行
# perfect_deployment_workflow()
```

## 📝 クイックリファレンス

### 必須コマンド

```bash
# 基本デプロイ
vercel --prod --yes

# ログ確認
vercel logs

# 設定確認
vercel ls

# ドメイン管理
vercel domains

# 環境変数
vercel env
```

### Python統合

```python
# 簡単デプロイ
from google_drive_utils import *
exec(open('vercel_site_analysis.py').read())

# 自動最適化デプロイ
perfect_deployment_workflow()
```

---

**🎉 これで完璧！** Google Drive/Colab環境からVercelへの完全なデプロイ体制が整いました。

**現在のURL**: https://study-research-final.vercel.app  
**管理状況**: 完全自動化済み  
**最適化**: AI支援デプロイ対応