#!/bin/bash
# Wezterm Shift+Enter 設定自動セットアップスクリプト

echo "🔧 Wezterm Shift+Enter 設定セットアップ開始"

# ホームディレクトリのパス
HOME_DIR="$HOME"
WEZTERM_CONFIG="$HOME_DIR/.wezterm.lua"

# バックアップディレクトリ作成
BACKUP_DIR="$HOME_DIR/.config_backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 設定ファイル場所: $WEZTERM_CONFIG"

# 既存設定のバックアップ
if [ -f "$WEZTERM_CONFIG" ]; then
    echo "💾 既存設定をバックアップ: $BACKUP_DIR/wezterm.lua"
    cp "$WEZTERM_CONFIG" "$BACKUP_DIR/wezterm.lua"
fi

# Wezterm設定内容
cat > "$WEZTERM_CONFIG" << 'EOF'
local wezterm = require 'wezterm'
local config = {}

-- 外観設定
config.color_scheme = 'Tomorrow Night'
config.font_size = 14

-- システムベル音を有効化（Claude Codeのタスク完了通知用）
config.audible_bell = "SystemBeep"
config.visual_bell = {
  fade_in_duration_ms = 75,
  fade_out_duration_ms = 75,
  target = "CursorColor",
}

-- キーバインド設定
config.keys = {
  -- Shift+Enterで改行を送信
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

-- ウィンドウ設定
config.initial_rows = 30
config.initial_cols = 120

-- タブバー設定
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true

return config
EOF

echo "✅ Wezterm設定ファイルを作成/更新しました"

# 設定内容の確認
echo "📋 設定内容:"
echo "  - Shift+Enter: 改行入力"
  echo "  - Enter: コマンド実行"
echo "  - システムベル音: 有効"
echo "  - Ctrl+Shift+C: コピー"
echo "  - Ctrl+Shift+V: ペースト"

# 動作確認方法の表示
cat << 'EOF'

🔄 次の手順:

1. Weztermを再起動してください
2. 動作確認:
   - Shift+Enter で改行が入力されることを確認
   - Enter でコマンドが実行されることを確認

🔧 カスタマイズ:
設定ファイル場所: ~/.wezterm.lua
詳細な設定オプションはWeztermの公式ドキュメントを参照

💾 バックアップ:
既存設定はバックアップされています:
EOF

echo "   $BACKUP_DIR/wezterm.lua"

echo ""
echo "✅ Wezterm Shift+Enter 設定完了!"