# WeztermでShift+Enter改行設定ガイド

## 🎯 設定目的
Weztermでも他のターミナルと同様にShift+Enterで改行入力を可能にする

## 📁 設定ファイル場所
```
~/.wezterm.lua
```

## ⚙️ 設定内容

以下の内容を `~/.wezterm.lua` に作成または追加してください：

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

## 🔧 設定手順

1. **設定ファイル作成**
   ```bash
   touch ~/.wezterm.lua
   ```

2. **設定内容の追加**
   上記のコードを `~/.wezterm.lua` にコピー&ペースト

3. **Wezterm再起動**
   設定を反映させるためWeztermを再起動

## ✅ 動作確認

設定後、以下で動作確認：
- `Shift + Enter`: 改行が入力される
- `Enter`: 通常のコマンド実行

## 🔔 追加機能

### システムベル音有効化
Claude Codeのタスク完了時にシステム音で通知されます。

### カスタマイズ例

```lua
-- より詳細な設定例
local wezterm = require 'wezterm'
local config = {}

-- 外観設定
config.color_scheme = 'Tomorrow Night'
config.font_size = 14

-- システムベル音設定
config.audible_bell = "SystemBeep"
config.visual_bell = {
  fade_in_duration_ms = 75,
  fade_out_duration_ms = 75,
  target = "CursorColor",
}

-- キーバインド設定
config.keys = {
  -- Shift+Enterで改行
  {
    key = 'Enter',
    mods = 'SHIFT',
    action = wezterm.action.SendString('\n')
  },
  -- Ctrl+Shift+Cでコピー
  {
    key = 'c',
    mods = 'CTRL|SHIFT',
    action = wezterm.action.CopyTo 'Clipboard'
  },
  -- Ctrl+Shift+Vでペースト
  {
    key = 'v',
    mods = 'CTRL|SHIFT',
    action = wezterm.action.PasteFrom 'Clipboard'
  },
}

return config
```

## 🔄 既存設定との統合

既に `~/.wezterm.lua` が存在する場合：

1. 既存の `config.keys` テーブルに追加
2. または既存設定を保持しつつ新しいキーバインドを追加

```lua
-- 既存設定がある場合の統合例
local wezterm = require 'wezterm'
local config = {}

-- 既存の設定...
config.font_size = 16

-- キーバインドの追加
config.keys = {
  -- 既存のキーバインド...
  
  -- Shift+Enter追加
  {
    key = 'Enter',
    mods = 'SHIFT',
    action = wezterm.action.SendString('\n')
  },
}

-- システムベル追加
config.audible_bell = "SystemBeep"

return config
```

## 📋 トラブルシューティング

### 設定が反映されない場合
1. Wezterm完全再起動
2. 設定ファイルの構文エラーチェック
3. `wezterm ls-fonts` でフォント確認

### 改行が効かない場合
- `mods = 'SHIFT'` の記述確認
- キーバインドの競合チェック

## 🔗 関連ファイル

- `SHIFT_ENTER_SETUP.md` - 全般的なShift+Enter設定ガイド
- `terminal-setup.sh` - 自動セットアップスクリプト

---
*最終更新: 2025-07-02*  
*Claude Code統合ターミナル設定ガイド*