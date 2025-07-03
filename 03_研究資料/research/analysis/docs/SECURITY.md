# 🔒 セキュリティガイド

##  重要な安全対策

### 🚨 APIキーの保護

**絶対にコミットしてはいけないファイル:**
- `config.py` - APIキーが含まれる設定ファイル
- `.env` - 環境変数ファイル
- `secrets.json` - 機密情報ファイル
- `credentials.json` - 認証情報ファイル

###  安全な設定方法

#### 1. 環境変数を使用（推奨）
```bash
# .env ファイルを作成（.env.example をコピー）
cp .env.example .env

# .env ファイルを編集して実際の値を設定
GITHUB_TOKEN=ghp_your_token_here
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

#### 2. セキュアな設定読み込み
```python
# secure_config.py を使用
from secure_config import GITHUB_TOKEN, ANTHROPIC_API_KEY
```

###  .gitignore 設定

以下のパターンが `.gitignore` に含まれています：
```
# Sensitive Configuration Files (NEVER COMMIT)
config.py
.env
*.env
.env.*
secrets.json
credentials.json
api_keys.txt
private_*
```

###  漏洩チェック方法

#### 1. コミット前チェック
```bash
# 機密情報がステージングされていないか確認
git status
git diff --cached

# 機密ファイルがコミットされていないか確認
git log --name-only | grep -E "(config\.py|\.env|secrets|credentials)"
```

#### 2. リモートリポジトリチェック
```bash
# GitHubで機密情報が公開されていないか確認
curl -s "https://api.github.com/repos/USERNAME/REPO/contents/" | grep -E "(config\.py|\.env)"
```

### 🚨 漏洩発生時の対応

#### 1. 即座にAPIキーを無効化
- GitHub: Settings → Developer settings → Personal access tokens → Delete
- Claude: Console → API Keys → Revoke

#### 2. Git履歴から完全削除
```bash
# 履歴から機密ファイルを削除
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch config.py' --prune-empty --tag-name-filter cat -- --all

# 強制プッシュ
git push --force-with-lease origin main
```

#### 3. 新しいAPIキーを生成
- 新しいトークン/キーを生成
- `.env` ファイルに安全に保存
- 公開されていないことを確認

###  ベストプラクティス

#### 1. 設定ファイルの分離
```
 .env.example     - テンプレート（コミット可）
 secure_config.py - セキュア読み込み（コミット可）
 .env            - 実際の値（コミット禁止）
 config.py       - 生値含む（コミット禁止）
```

#### 2. 環境別設定
```
.env.development  - 開発環境
.env.production   - 本番環境
.env.test        - テスト環境
```

#### 3. 定期的なチェック
```bash
# 週1回実行
git log --all --grep="token\|key\|secret\|password" --oneline
```

### 📱 GitHub Actions でのシークレット

```yaml
# .github/workflows/claude-review.yml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**設定方法:**
1. GitHub → Settings → Secrets and variables → Actions
2. New repository secret
3. シークレット名と値を入力

### 🔐 チームでの共有

#### 安全な共有方法
-  1Password、Bitwarden等のパスワードマネージャー
-  暗号化されたプライベートチャット
-  社内のセキュアな認証情報管理システム

#### 危険な共有方法
-  メール
-  Slack/Discord等のチャット
-  GitHub Issues/PRのコメント
-  Google Docs/Sheets

### 📞 インシデント報告

APIキーが漏洩した場合：
1. **即座に無効化**（最優先）
2. **Git履歴から削除**
3. **新しいキーを生成**
4. **影響範囲の確認**
5. **再発防止策の実装**

---

** セキュリティは最優先事項です。疑問があれば、常に安全な方法を選択してください。**