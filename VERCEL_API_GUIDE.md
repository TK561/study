# 🚀 Vercel API 使用ガイド

## 📋 API設定手順

### 1. **新しいVercel APIトークン作成**
```bash
# 手順:
1. https://vercel.com/account/tokens にアクセス
2. "Create Token" をクリック
3. Token名: "Research-Project-2025" 推奨
4. 生成されたトークンをコピー
```

### 2. **環境変数設定**
```bash
# .env ファイル編集
nano /mnt/c/Desktop/Research/.env

# VERCEL_TOKEN の行を変更:
VERCEL_TOKEN="your_actual_token_here"
```

### 3. **API接続テスト**
```bash
# 基本テスト
python vercel_api_setup.py

# ステータス確認
python vercel_api_setup.py status

# デプロイ実行
python vercel_api_setup.py deploy
```

## 🔧 Vercel API 機能

### **vercel_api_setup.py** の主要機能

#### 1. **接続テスト**
```python
api.test_connection()
# ✅ Vercel API接続成功: TK561
```

#### 2. **プロジェクト情報取得**
```python
api.get_project_info()
# 📂 プロジェクト: study-research-final
# 🌐 URL: https://study-research-final.vercel.app
```

#### 3. **直接デプロイ**
```python
api.deploy_project()
# ✅ デプロイ成功: https://study-research-final-abc123.vercel.app
```

#### 4. **デプロイメント履歴**
```python
api.list_deployments()
# 📋 最新デプロイメント:
# ✅ study-research-final-abc123.vercel.app - READY
```

## 📊 現在の設定情報

### 復元済み設定
```
プロジェクトID: prj_yt8CeSOyuRcskyogkyA9KTfV6L1C
組織ID: team_kA5nnv3rcMaRsXQJ9vdYQ0nR
プロジェクト名: study-research-final
GitHub連携: 有効
```

### .env ファイル構成
```bash
GITHUB_TOKEN="[GitHubトークンを設定してください]"
VERCEL_PROJECT_ID="prj_yt8CeSOyuRcskyogkyA9KTfV6L1C"
VERCEL_TOKEN="[設定してください]"
VERCEL_ORG_ID="team_kA5nnv3rcMaRsXQJ9vdYQ0nR"
```

## 🚀 使用例

### **Claude Code同義コマンドとAPI連携**
```bash
# 通常のGit方式（現在）
"vercelに適応して" → Git → GitHub → Vercel (30秒)

# API方式（設定後）
"vercel API デプロイ" → 直接API → Vercel (10秒)
```

### **API使用のメリット**
- ⚡ **高速**: Git経由不要で直接デプロイ（10秒）
- 🎯 **制御**: デプロイ状況の詳細確認
- 📊 **監視**: リアルタイムステータス取得
- 🔧 **管理**: デプロイ履歴・ロールバック

## ⚠️ セキュリティ注意事項

### 安全な管理
```bash
# .env は .gitignore で除外済み
# 実際のトークンはローカルのみ保存
# GitHub等への流出防止済み
```

### トークン権限
```
推奨権限: Deploy, Project Read
避ける権限: Billing, Team Management
```

## 🔄 次のステップ

1. **Vercel APIトークン作成・設定**
2. **`python vercel_api_setup.py` で接続確認**
3. **`python vercel_api_setup.py deploy` でAPI経由デプロイテスト**
4. **Claude Code同義コマンドの拡張**

---

**🤖 Vercel API Integration with Claude Code**  
**設定完了後**: 「vercel APIデプロイ」等の新コマンドが利用可能