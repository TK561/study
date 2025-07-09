# Claude Code Status

VSCodeのステータスバーにClaude Codeの使用状況と料金を表示する拡張機能です。

## 機能

- 🤖 使用中のモデル名を表示
- 📊 トークン使用量をリアルタイム表示
- 💰 料金を日本円またはドルで表示
- 📈 1日あたりの推定料金を表示
- ⏰ Pro/MAX版の使用期限残り時間を表示
- 🔄 設定可能な自動更新間隔
- 👆 クリックでライブビューを開く

## 表示例

ステータスバーの表示例：
- 通常版: `🤖 sonnet-4 ➡️ 13.44K Tkns 💳 ¥347 📈 ¥759/day`
- Pro版: `⭐ Pro 🤖 sonnet-4 ➡️ 13.44K Tkns 💳 ¥347 📈 ¥759/day 🕐 29d 5h`
- MAX版: `⚡ MAX 🤖 opus-4 ➡️ 25.8K Tkns 💳 ¥1,245 📈 ¥2,890/day 🕐 14d 18h`

## 設定

VSCodeの設定から以下の項目をカスタマイズできます：

- `claudeCodeStatus.enabled`: 拡張機能の有効/無効（デフォルト: true）
- `claudeCodeStatus.interval`: 更新間隔（ミリ秒）（デフォルト: 30000）
- `claudeCodeStatus.showCurrency`: 表示通貨 USD/JPY（デフォルト: USD）
- `claudeCodeStatus.jpyRate`: 円ドル為替レート（デフォルト: 150）
- `claudeCodeStatus.command`: 実行コマンド（デフォルト: "npx ccusage@latest blocks"）
- `claudeCodeStatus.claudeConfigPath`: Claudeの設定ディレクトリパス（Windowsでエラーが出る場合に設定）
- `claudeCodeStatus.showTimeRemaining`: Pro/MAX版の残り時間表示（デフォルト: true）

### Windowsでのトラブルシューティング

ccusageがClaude Codeのデータディレクトリを見つけられない場合、以下のいずれかの方法で解決できます：

1. WSL環境でClaude Codeを使用している場合、`claudeConfigPath`に以下のようなパスを設定：
   - `/home/{username}/.config/claude`
   - `/home/{username}/.claude`

2. Windows環境の場合、環境変数 `CLAUDE_CONFIG_DIR` を設定するか、`claudeConfigPath`に以下のようなパスを設定：
   - `C:\Users\{username}\.config\claude`
   - `C:\Users\{username}\.claude`

## コマンド

- `Claude Code Status: Refresh`: 使用状況を手動で更新
- `Claude Code Status: Show Details`: ライブビューをターミナルで開く

## 必要条件

- ccusageがインストールされていること
- Claude CodeのAPIキーが設定されていること

## インストール

1. VSIXファイルをダウンロード
2. VSCodeでコマンドパレットを開く（Ctrl+Shift+P / Cmd+Shift+P）
3. `Extensions: Install from VSIX...` を選択
4. ダウンロードしたVSIXファイルを選択

## ライセンス

MIT