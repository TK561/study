local wezterm = require 'wezterm'
local config = {}

-- 外観設定
config.color_scheme = 'Tomorrow Night'
config.font_size = 14

-- システムベル音を有効化（Claude Codeのタスク完了通知用）
config.audible_bell = "SystemBeep"

-- デバッグ用の複数の改行方法
config.keys = {
  -- 方法1: Shift+Enterで改行（\r\n）
  {
    key = 'Enter',
    mods = 'SHIFT',
    action = wezterm.action.SendString('\r\n')
  },
  
  -- 方法2: Ctrl+Enterで改行（バックアップ）
  {
    key = 'Enter',
    mods = 'CTRL',
    action = wezterm.action.SendString('\n')
  },
  
  -- 方法3: Alt+Enterで改行（バックアップ2）
  {
    key = 'Enter',
    mods = 'ALT',
    action = wezterm.action.SendString('\n')
  },
  
  -- デバッグ用：Shift+Space でテスト文字列
  {
    key = 'Space',
    mods = 'SHIFT',
    action = wezterm.action.SendString('[WEZTERM_DEBUG]')
  },
  
  -- 通常のコピー&ペースト
  {
    key = 'c',
    mods = 'CTRL|SHIFT',
    action = wezterm.action.CopyTo 'Clipboard'
  },
  {
    key = 'v',
    mods = 'CTRL|SHIFT',
    action = wezterm.action.PasteFrom 'Clipboard'
  },
}

-- ウィンドウ設定
config.initial_rows = 30
config.initial_cols = 120

-- タブバー設定
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true

-- デバッグ設定
config.debug_key_events = true

return config