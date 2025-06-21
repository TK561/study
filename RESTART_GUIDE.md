# 🔄 Claude Code 再起動ガイド

## 📋 次回起動時の即座実行可能項目

### ✅ 自動認識される設定
1. **日本語モード**: `shared_resources/CLAUDE.md` 自動読込
2. **Git設定**: origin/main リモート連携済み
3. **Vercel設定**: プロジェクト `study-research-final` 連携済み
4. **同義コマンド**: 15個すべて認識・実行可能

### 🚀 即座に使用可能なコマンド
```bash
# Vercel自動デプロイ (すべて同じ動作)
"vercelに適応して"
"vercelに反映して" 
"サイトを更新して"
"オンライン版を更新"
"vercel緊急修正"
# ... 他10個も利用可能
```

### 🔗 重要URL
- **本番サイト**: https://study-research-final.vercel.app/
- **研究内容**: WordNet + CLIP 特化型画像分類 (16カテゴリ、27.3%向上)

## 📂 プロジェクト構造確認
```bash
# プロジェクト全体確認
ls -la /mnt/c/Desktop/Research/

# 核心ファイル確認  
cat /mnt/c/Desktop/Research/shared_resources/CLAUDE.md
cat /mnt/c/Desktop/Research/api/index.py
```

## 🛠 標準作業フロー

### 研究内容更新 → デプロイ
```bash
# 1. ファイル編集
edit api/index.py

# 2. デプロイ実行 (30秒で完了)
"vercelに適応して"

# 3. 結果確認
curl https://study-research-final.vercel.app/
```

### Git状態確認
```bash
git status
git log --oneline -5
```

## 🔍 トラブルシューティング

### もしVercelデプロイが失敗した場合
```bash
# Git状態確認
git status

# 手動プッシュ
git add .
git commit -m "Manual update"
git push origin main

# 30秒待機後確認
curl -I https://study-research-final.vercel.app/
```

### 設定確認方法
```bash
# CLAUDE.md設定確認
grep -A 5 "Vercel自動デプロイ同義コマンド" shared_resources/CLAUDE.md

# Vercel設定確認
cat vercel.json

# Git設定確認
git remote -v
```

## 📊 継続性保証

**保存済み設定**:
- ✅ 日本語モード設定
- ✅ 15個同義コマンド
- ✅ GitHub自動デプロイ設定
- ✅ Vercel連携設定
- ✅ 研究成果表示ページ

**継続性テスト**: 2025年6月21日実行済み ✅

---

**🤖 Claude Code 継続性確保システム**  
**次回起動時: このガイドに従って即座に作業再開可能**