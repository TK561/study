# ⌨️ Shift+Enter改行設定ガイド

## 🎯 概要
Shift+Enterで改行し、Enterで実行する設定方法をまとめています。

## 💻 環境別設定

### 1. **VS Code Integrated Terminal**
VS Codeの統合ターミナルを使用している場合：

#### 設定方法
1. **設定を開く**: `Ctrl+,` または `File > Preferences > Settings`
2. **検索**: `terminal.integrated.commandsToSkipShell`
3. **設定**: 以下を追加
```json
{
    "terminal.integrated.commandsToSkipShell": [
        "workbench.action.terminal.sendSequence"
    ],
    "terminal.integrated.allowChords": false
}
```

#### キーバインド設定
1. **キーバインドを開く**: `Ctrl+K Ctrl+S`
2. **検索**: `terminal.integrated.sendSequence`
3. **追加**:
```json
{
    "key": "shift+enter",
    "command": "workbench.action.terminal.sendSequence",
    "args": {"text": "\n"},
    "when": "terminalFocus"
}
```

### 2. **Claude Code Extension**
Claude Code拡張機能を使用している場合：

#### 設定ファイル
`.vscode/settings.json` を作成または編集：
```json
{
    "claude.terminal.multilineInput": true,
    "claude.terminal.submitOnEnter": true,
    "claude.terminal.newlineOnShiftEnter": true
}
```

### 3. **Wezterm Terminal**
Weztermを使用している場合：

#### 設定ファイル場所
```
~/.wezterm.lua
```

#### 設定内容
```lua
local wezterm = require 'wezterm'
local config = {}

-- システムベル音を有効化（Claude Codeのタスク完了通知用）
config.audible_bell = "SystemBeep"

-- Shift+Enterで改行を送信
config.keys = {
  {
    key = 'Enter',
    mods = 'SHIFT',
    action = wezterm.action.SendString('\n')
  },
}

return config
```

#### 設定手順
1. `~/.wezterm.lua` ファイルを作成
2. 上記設定をコピー&ペースト
3. Wezterm再起動

### 4. **Windows Terminal**
Windows Terminalを使用している場合：

#### settings.json設定
```json
{
    "actions": [
        {
            "command": "sendInput",
            "keys": "shift+enter",
            "input": "\n"
        }
    ]
}
```

### 4. **PowerShell ISE / PowerShell**
PowerShell環境での設定：

#### PSReadLine設定
```powershell
# プロファイルに追加 ($PROFILE)
Set-PSReadLineKeyHandler -Key "Shift+Enter" -Function AddLine
Set-PSReadLineKeyHandler -Key "Enter" -Function AcceptLine
```

### 5. **Bash/Zsh Terminal**
通常のBash/Zshターミナルでの設定：

#### .inputrc設定
```bash
# ~/.inputrc に追加
"\e[27;2;13~": "\n"  # Shift+Enter
```

#### readline設定
```bash
# .bashrc または .zshrc に追加
bind '"\e[27;2;13~": "\n"'
```

## 🛠️ 現在の環境用設定スクリプト

### VS Code設定スクリプト
```bash
./setup-shift-enter.sh vscode
```

### 汎用設定スクリプト
```bash
./setup-shift-enter.sh generic
```

## 📋 テスト方法

### 1. **基本テスト**
ターミナルで以下を試してください：
- `Shift+Enter` を押す → 改行のみ
- `Enter` を押す → コマンド実行

### 2. **複数行入力テスト**
```bash
echo "line1" \
[Shift+Enter]
echo "line2" \
[Shift+Enter]  
echo "line3"
[Enter] # 実行
```

### 3. **スクリプト入力テスト**
```bash
if [ true ]; then
[Shift+Enter]
    echo "test"
[Shift+Enter]
fi
[Enter] # 実行
```

## 🔧 トラブルシューティング

### よくある問題

#### 1. **Shift+Enterが効かない**
- ターミナルアプリケーションの設定を確認
- キーバインドの競合をチェック
- 権限設定を確認

#### 2. **設定が反映されない**
```bash
# 設定リロード
source ~/.bashrc
# または
exec $SHELL
```

#### 3. **VS Codeで効かない**
- 拡張機能の競合をチェック
- ワークスペース設定を確認
- 開発者ツールでキーイベントを確認

#### 4. **Claude Code固有の問題**
- Claude Code拡張の設定を確認
- VS Code設定との競合をチェック

## ⚙️ カスタマイズ

### 1. **異なるキー組み合わせ**
```json
{
    "key": "ctrl+shift+enter",
    "command": "workbench.action.terminal.sendSequence",
    "args": {"text": "\n"},
    "when": "terminalFocus"
}
```

### 2. **特定のコマンドでのみ有効**
```json
{
    "key": "shift+enter",
    "command": "workbench.action.terminal.sendSequence",
    "args": {"text": "\n"},
    "when": "terminalFocus && !suggestWidgetVisible"
}
```

## 🎯 推奨設定

### 研究プロジェクト用
```json
{
    "terminal.integrated.enableMultiLinePasteWarning": false,
    "terminal.integrated.rightClickBehavior": "paste",
    "claude.terminal.multilineInput": true,
    "claude.terminal.submitOnEnter": true
}
```

## 📞 サポート

設定がうまくいかない場合：
1. 使用している環境を確認（VS Code、Windows Terminal、etc.）
2. エラーメッセージをチェック
3. 代替方法を試行

---

**注意**: 環境によって設定方法が異なります。使用している具体的なツールに応じて適切な設定を選択してください。