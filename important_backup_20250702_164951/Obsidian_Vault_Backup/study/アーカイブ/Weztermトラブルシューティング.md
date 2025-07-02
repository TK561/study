# Wezterm Shift+Enter トラブルシューティング

## 🔧 デバッグ設定を適用しました

現在の設定では、以下のキーバインドでテストできます：

### テスト方法

1. **Weztermを再起動**してください
2. **動作確認**：
   - `Shift + Enter`: 改行入力（メイン）
   - `Ctrl + Enter`: 改行入力（バックアップ1）
   - `Alt + Enter`: 改行入力（バックアップ2）
   - `Shift + Space`: `[WEZTERM_DEBUG]`が表示されるかテスト

### 問題が続く場合の確認事項

1. **Weztermのバージョン確認**
   ```bash
   wezterm --version
   ```

2. **設定ファイルの構文チェック**
   ```bash
   wezterm ls-fonts
   ```
   エラーが出る場合は設定ファイルに問題があります

3. **ログ確認**
   Weztermを起動時に`debug_key_events = true`でキーイベントがログに表示されます

### 代替解決策

もしWezterm設定で解決しない場合：

#### 方法1: シェル設定で対応
```bash
# ~/.bashrc または ~/.zshrc に追加
bind '"\e[13;2u": "\n"'  # Shift+Enter
```

#### 方法2: tmux/screen使用時
```bash
# ~/.tmux.conf に追加
bind-key -n S-Enter send-keys C-m
```

#### 方法3: Claude Code設定で対応
VS Codeまたはエディタ側で改行制御を設定

### 最終確認

1. `Shift + Space`を押して`[WEZTERM_DEBUG]`が表示されるか
2. 表示される場合：Weztermキーバインドは動作している
3. 表示されない場合：Wezterm設定に問題がある

### よくある問題

1. **キーバインドの競合**
   - 他のアプリケーションがShift+Enterを捕捉している
   
2. **シェルの設定**
   - bash/zsh/fishなどのシェル設定が干渉している
   
3. **ターミナルエミュレータの設定**
   - Weztermの他の設定が干渉している

### 成功した場合

いずれかの方法で改行が入力できた場合、その設定を維持してください。
デバッグ設定を通常設定に戻すには：

```bash
./setup_wezterm_shift_enter.sh
```

を再実行してください。