# 🚀 Auto Git Manager - 使用方法

GitHub Personal Access Tokenを使用してClaude Codeで作成・編集したファイルを自動的にGitHubにコミット・プッシュするシステムです。

## 📋 事前準備

### 1. GitHub Personal Access Token の作成

1. GitHub にログイン
2. **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token** をクリック
4. 以下の権限を選択：
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
5. トークンをコピーして保存（**再表示されません**）

### 2. 必要な環境

- Python 3.6以上
- Git がインストールされていること
- VS Code（推奨）

## 🛠️ セットアップ手順

### 方法1: バッチファイル使用（Windows）

```bash
# 初回セットアップ
setup_git.bat

# クイックコミット
auto_commit.bat
```

### 方法2: シェルスクリプト使用（Linux/Mac）

```bash
# 初回セットアップ
./setup_git.sh

# クイックコミット  
./auto_commit.sh
```

### 方法3: Python直接実行

```bash
# 初回セットアップ
python auto_git_manager.py --setup

# 自動コミット・プッシュ
python auto_git_manager.py --auto-commit

# Git状態確認
python auto_git_manager.py --status
```

## 📝 セットアップ時の入力項目

セットアップ実行時に以下の情報を入力してください：

1. **GitHub ユーザー名**: あなたのGitHubユーザー名
2. **メールアドレス**: Gitコミット用のメールアドレス
3. **Personal Access Token**: 上記で作成したトークン
4. **リポジトリURL**: `https://github.com/ユーザー名/リポジトリ名.git`

### 入力例:
```
GitHub ユーザー名: TK561
メールアドレス: tk561@example.com
Personal Access Token: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
リポジトリURL: https://github.com/TK561/study.git
```

## 🎮 VS Code での使用方法

セットアップ完了後、VS Code で以下のタスクが利用可能になります：

### タスク実行方法:
1. **Ctrl+Shift+P** → 「Tasks: Run Task」を選択
2. 以下のタスクから選択：
   - **Git Auto Commit & Push** - 自動コミット・プッシュ
   - **Git Setup** - セットアップ再実行
   - **Git Status** - Git状態確認

### ショートカットキー:
- **Ctrl+Shift+G Ctrl+Shift+P** - 自動コミット・プッシュ
- **Ctrl+Shift+G Ctrl+Shift+S** - Git状態確認

## 🔧 高度な使用方法

### カスタムコミットメッセージ

```bash
python auto_git_manager.py --auto-commit -m "カスタムメッセージ"
```

### 特定のパスで実行

```bash
python auto_git_manager.py --auto-commit --path /path/to/repository
```

### 生成される設定ファイル

- `.git_config.ini` - Git設定情報
- `git_auto_manager.log` - 実行ログ
- `.vscode/tasks.json` - VS Codeタスク設定
- `.vscode/keybindings.json` - VS Codeキーバインド設定

## 📊 自動生成されるコミットメッセージ

システムは変更内容を分析して自動的にコミットメッセージを生成します：

### 例:
```
Add semantic_classification_system.py and Update requirements.txt

🚀 Generated with [Claude Code](https://claude.ai/code)
📅 Auto-committed: 2024-01-15 14:30:25

Co-Authored-By: Claude <noreply@anthropic.com>
```

### ファイル変更タイプ別メッセージ:
- **新規ファイル**: `Add filename.py`
- **変更ファイル**: `Update filename.py`  
- **削除ファイル**: `Delete filename.py`
- **複数ファイル**: `Add 3 new files and Update 2 files`

## 🛡️ セキュリティについて

### 注意事項:
1. **Personal Access Token** は `.git_config.ini` に保存されます
2. このファイルを他人と共有しないでください
3. `.git_config.ini` を `.gitignore` に追加することを推奨します

### トークンの権限:
- `repo` 権限のみで十分です
- 必要以上の権限を付与しないでください

## 🔍 トラブルシューティング

### よくある問題:

#### 1. 認証エラー
```
Error: Authentication failed
```
**解決方法**: Personal Access Token が正しいか確認

#### 2. リモートリポジトリが見つからない
```
Error: remote repository not found
```
**解決方法**: リポジトリURLが正しいか確認

#### 3. プッシュ権限エラー
```
Error: permission denied
```
**解決方法**: トークンに `repo` 権限があるか確認

### ログファイル確認:
```bash
cat git_auto_manager.log  # Linux/Mac
type git_auto_manager.log  # Windows
```

## 📈 ワークフロー例

### 日常的な開発フロー:

1. **Claude Code で作業**
   - ファイルの作成・編集
   - コードの改善

2. **自動コミット実行**
   ```bash
   # 方法A: バッチファイル
   auto_commit.bat
   
   # 方法B: VS Codeタスク
   Ctrl+Shift+G Ctrl+Shift+P
   
   # 方法C: コマンドライン
   python auto_git_manager.py --auto-commit
   ```

3. **結果確認**
   - GitHub でコミット履歴確認
   - ログファイルで実行結果確認

### プロジェクト共有フロー:

1. **初回セットアップ**
   ```bash
   setup_git.bat  # Windows
   ./setup_git.sh  # Linux/Mac
   ```

2. **定期的なバックアップ**
   ```bash
   # 1日1回など定期実行
   python auto_git_manager.py --auto-commit
   ```

3. **状態確認**
   ```bash
   python auto_git_manager.py --status
   ```

## 📞 サポート

### エラーが発生した場合:

1. `git_auto_manager.log` ファイルを確認
2. Personal Access Token の権限を確認  
3. リポジトリURL が正しいか確認
4. ネットワーク接続を確認

### セットアップ再実行:
```bash
python auto_git_manager.py --setup
```

---

**🎉 これで Claude Code で作成したファイルを自動的に GitHub に同期できます！**

Cursor での開発がより効率的になります。