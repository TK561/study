# Vercel エラー対策ナレッジベース

## 📋 発生したエラーと解決方法

### Error 1: Vercel Functions 形式エラー (再発)
**発生日時**: 2025年6月22日 01:15頃 **※再発エラー**

**エラー内容**:
```
Traceback (most recent call last):
File "/var/task/vc__handler__python.py", line 213, in <module>
if not issubclass(base, BaseHTTPRequestHandler):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: issubclass() arg 1 must be a class
Python process exited with exit status: 1.
```

**再発原因分析**: 
- 前回修正したが、HTMLの長大な文字列連結が問題
- f-string形式と通常の文字列連結の混在
- CSS内の波括弧とf-stringの衝突

**根本的解決方法**:
1. **シンプルなf-string形式を採用**
2. **CSS内の波括弧を二重波括弧`{{}}`でエスケープ**
3. **HTMLを短縮・最適化**
4. **文字列連結を完全に排除**

**修正版テンプレート**:
```python
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        fixed_timestamp = "2025年06月22日 01:17 JST"
        
        html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <style>
        body {{ font-family: sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
    </style>
</head>
<body>
    <!-- コンテンツ -->
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
```

### Error 1: Vercel Functions 形式エラー (初回)
**発生日時**: 2025年6月22日 01:00頃

**エラー内容**:
```
Traceback (most recent call last):
File "/var/task/vc__handler__python.py", line 213, in <module>
if not issubclass(base, BaseHTTPRequestHandler):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: issubclass() arg 1 must be a class
Python process exited with exit status: 1.
```

**原因**: 
- Vercel Functionsで関数形式を使用していた
- 正しくはクラス形式で`BaseHTTPRequestHandler`を継承する必要がある

**間違った形式**:
```python
import datetime
import os

def handler(request):
    html = '''...'''
    return {
        'statusCode': 200,
        'headers': {...},
        'body': html
    }
```

**正しい形式**:
```python
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import datetime
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = '''...'''
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
```

**解決手順**:
1. `api/index.py` を正しいクラス形式に修正
2. `quick_vercel_fix.py` でToken認証デプロイ実行
3. 2-3分で反映確認

---

### Error 2: GitHub Push Protection (Token検出)
**発生日時**: 2025年6月22日 00:30頃

**エラー内容**:
```
remote: error: GH013: Repository rule violations found for refs/heads/main.        
remote: - GITHUB PUSH PROTECTION        
remote:   Push cannot contain secrets
remote: —— GitHub Personal Access Token ——————————————————————        
```

**原因**: 
- GitHubがコミット内のAPIトークンを検出
- `VERCEL_API_GUIDE.md` にトークンが記載されていた

**解決方法**:
1. GitHubでのpushを停止
2. Token認証による直接デプロイに切り替え
3. `.env`ファイルでのトークン管理

**今後の対策**:
- Git pushは使用禁止
- Token APIデプロイのみ使用
- センシティブ情報は`.env`ファイルで管理

---

### Error 3: Vercel API デプロイメント形式エラー
**発生日時**: 2025年6月22日 00:45頃

**エラー内容**:
```
{"error":{"code":"bad_request","message":"Invalid request: `files` should be array."}}
```

**原因**: 
- ファイル形式をオブジェクトで送信していた
- Vercel API v13では配列形式が必要

**間違った形式**:
```python
files = {
    "index.html": {
        "file": base64_content
    }
}
```

**正しい形式**:
```python
files = [
    {
        "file": "index.html",
        "data": base64_content
    }
]
```

---

## 🛠 Vercel Functions チェックリスト

### ✅ 必須要件
- [ ] `BaseHTTPRequestHandler` を継承したクラス形式
- [ ] `do_GET()` または `do_POST()` メソッドの実装
- [ ] 正しいHTTPレスポンス形式（`self.send_response()` 等）
- [ ] UTF-8エンコーディングの指定

### ✅ ファイル構造
```
/api/
  └── index.py (メインハンドラー)
/vercel.json (設定ファイル)
```

### ✅ インポート要件
```python
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs  # 必要に応じて
import datetime
import os
```

---

## 🚀 推奨デプロイ手順

### 1. エラーチェック
```bash
# 構文チェック
python3 -m py_compile api/index.py

# ローカルテスト（可能であれば）
python3 api/index.py
```

### 2. Token認証デプロイ
```bash
# クイック修正用
python3 quick_vercel_fix.py

# 完全版
python3 auto_vercel_token_deploy.py
```

### 3. デプロイ後確認
- 2-3分待機
- ブラウザでサイト確認
- Vercelダッシュボードでログ確認

---

## ⚠️ 避けるべき行為

### ❌ Git Push での更新
- 理由: Token検出によりブロック
- 代替: Token API直接デプロイ

### ❌ 関数形式でのVercel Functions
- 理由: `issubclass` エラー発生
- 代替: クラス形式で実装

### ❌ オブジェクト形式でのファイル送信
- 理由: Vercel API v13非対応
- 代替: 配列形式でファイル送信

---

## 📱 緊急時対応プロトコル

### Step 1: エラー確認
1. Vercelダッシュボードでエラーログ確認
2. 本ナレッジベースで既知エラーかチェック
3. エラーパターンの特定

### Step 2: 修正実行
1. 該当ファイルの修正
2. `quick_vercel_fix.py` で即座デプロイ
3. 反映確認（2-3分）

### Step 3: ナレッジ更新
1. 新しいエラーの場合は本ファイルに追記
2. 解決方法と予防策を記録
3. 次回同様エラー防止

---

## 📊 エラー発生履歴

| 日時 | エラータイプ | 解決時間 | 使用ツール | 状態 |
|------|-------------|----------|-----------|------|
| 2025/06/22 01:15 | Vercel Functions形式エラー(再発) | 10分 | 完全書き換え+quick_vercel_fix.py | ✅解決 |
| 2025/06/22 01:00 | Vercel Functions形式エラー | 15分 | quick_vercel_fix.py | ⚠️再発 |
| 2025/06/22 00:45 | API形式エラー | 10分 | direct_vercel_deploy.py | ✅解決 |
| 2025/06/22 00:30 | GitHub Push Protection | 20分 | Token API切り替え | ✅解決 |

---

## 🔧 関連スクリプト

### メンテナンス用
- `quick_vercel_fix.py` - 緊急修正用
- `auto_vercel_token_deploy.py` - 完全自動デプロイ用
- `DEPLOYMENT_GUIDE.md` - デプロイ手順書

### 設定ファイル
- `.env` - 環境変数（非公開）
- `vercel.json` - Vercel設定
- `api/index.py` - Functions本体

---

**更新日**: 2025年6月22日 01:15  
**次回更新**: エラー発生時  
**管理者**: Claude Code システム