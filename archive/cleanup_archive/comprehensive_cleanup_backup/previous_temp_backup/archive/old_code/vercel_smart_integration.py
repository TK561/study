#!/usr/bin/env python3
"""
Vercelスマート統合システム
既存のコマンドをフックして自動実行を実現
"""

import os
import sys
import subprocess
import json
import asyncio
from datetime import datetime
from typing import List, Dict

class VercelSmartIntegration:
    """
    既存のVercelコマンドを自動的にフックして統合システムを実行
    """
    
    def __init__(self):
        self.integration_file = "VERCEL_INTEGRATION_STATUS.json"
        self.status = self._load_status()
        
    def _load_status(self) -> Dict:
        """統合状態を読み込む"""
        if os.path.exists(self.integration_file):
            with open(self.integration_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "hooks_installed": False,
            "auto_trigger_enabled": False,
            "last_integration": None
        }
    
    def _save_status(self):
        """統合状態を保存"""
        with open(self.integration_file, 'w', encoding='utf-8') as f:
            json.dump(self.status, f, ensure_ascii=False, indent=2)
    
    def create_command_wrappers(self):
        """コマンドラッパーを作成"""
        print("🔧 Vercelコマンドラッパーを作成中...")
        
        wrappers = {
            # Vercel CLIラッパー
            "vercel_smart": """#!/bin/bash
# Vercelスマートラッパー

echo "🚀 Vercelスマート統合システム実行中..."

# 元のvercelコマンドを実行
if command -v vercel &> /dev/null; then
    vercel "$@"
    VERCEL_EXIT_CODE=$?
else
    echo "⚠️ Vercel CLIが見つかりません"
    VERCEL_EXIT_CODE=1
fi

# 統合システムを自動実行
echo "🤖 AI統合システムを実行中..."
python3 vercel_auto_trigger.py --trigger "vercel_command: $*"

exit $VERCEL_EXIT_CODE
""",
            
            # Git pushラッパー
            "git_smart": """#!/bin/bash
# Gitスマートプッシュラッパー

echo "📤 Gitスマートプッシュ実行中..."

# 元のgit pushを実行
git "$@"
GIT_EXIT_CODE=$?

# pushが成功した場合のみ自動デプロイ
if [ $GIT_EXIT_CODE -eq 0 ] && [[ "$*" == *"push"* ]]; then
    echo "🚀 プッシュ成功 - 自動デプロイを開始..."
    python3 vercel_auto_trigger.py --trigger "git_push"
fi

exit $GIT_EXIT_CODE
""",
            
            # npm runラッパー
            "npm_smart": """#!/bin/bash
# NPMスマートラッパー

echo "📦 NPMスマート実行中..."

# 元のnpmコマンドを実行
npm "$@"
NPM_EXIT_CODE=$?

# buildまたはdevの場合は自動実行
if [[ "$*" == *"build"* ]] || [[ "$*" == *"dev"* ]]; then
    echo "🤖 ビルド完了 - AI統合システムを実行..."
    python3 vercel_auto_trigger.py --trigger "npm_$*"
fi

exit $NPM_EXIT_CODE
"""
        }
        
        # ラッパーファイルを作成
        wrapper_dir = ".vercel_wrappers"
        os.makedirs(wrapper_dir, exist_ok=True)
        
        for name, content in wrappers.items():
            wrapper_path = os.path.join(wrapper_dir, name)
            with open(wrapper_path, 'w') as f:
                f.write(content)
            os.chmod(wrapper_path, 0o755)
            print(f"✅ 作成: {wrapper_path}")
        
        # PATHに追加するための設定ファイル
        path_setup = f"""# Vercelスマート統合システム
# このファイルを .bashrc または .zshrc に追加してください

export PATH="{os.path.abspath(wrapper_dir)}:$PATH"

# エイリアス設定
alias vercel="{os.path.abspath(os.path.join(wrapper_dir, 'vercel_smart'))}"
alias git_push="{os.path.abspath(os.path.join(wrapper_dir, 'git_smart'))} push"
alias npm_build="{os.path.abspath(os.path.join(wrapper_dir, 'npm_smart'))}"

echo "🚀 Vercelスマート統合システムが有効です"
"""
        
        with open("vercel_smart_setup.sh", 'w') as f:
            f.write(path_setup)
        
        print("\n📋 セットアップ完了!")
        print("以下のコマンドでシェル統合を有効にしてください:")
        print("source vercel_smart_setup.sh")
        
        return True
    
    def setup_shell_integration(self):
        """シェル統合をセットアップ"""
        print("🐚 シェル統合をセットアップ中...")
        
        # .bashrc / .zshrc に追加する設定
        shell_config = '''
# Vercelスマート統合システム
vercel_smart_deploy() {
    echo "🚀 Vercelスマートデプロイ実行中..."
    python3 vercel_unified_system.py deploy
}

vercel_smart_status() {
    echo "📊 Vercelシステム状態:"
    python3 vercel_unified_system.py dashboard
}

vercel_smart_fix() {
    echo "🔧 Vercel自動修復実行中..."
    python3 vercel_fix_assistant.py
}

# エイリアス
alias vsd="vercel_smart_deploy"
alias vss="vercel_smart_status"  
alias vsf="vercel_smart_fix"
alias vst="python3 vercel_auto_trigger.py start"

# 自動フック関数
vercel_auto_hook() {
    if [[ "$1" == *"vercel"* ]] || [[ "$1" == *"deploy"* ]]; then
        echo "🤖 Vercel操作検出 - 統合システムを実行..."
        python3 vercel_auto_trigger.py --trigger "shell_command: $1"
    fi
}

# プロンプトコマンドに追加（bash）
if [ -n "$BASH_VERSION" ]; then
    export PROMPT_COMMAND="vercel_auto_hook \\"\\$BASH_COMMAND\\"; $PROMPT_COMMAND"
fi

# プロンプトコマンドに追加（zsh）
if [ -n "$ZSH_VERSION" ]; then
    preexec() {
        vercel_auto_hook "$1"
    }
fi
'''
        
        # 設定ファイルに保存
        with open("vercel_shell_integration.sh", 'w') as f:
            f.write(shell_config)
        
        print("✅ シェル統合設定を作成しました")
        print("\n📋 使用方法:")
        print("1. source vercel_shell_integration.sh")
        print("2. 以下のコマンドが利用可能になります:")
        print("   - vsd: スマートデプロイ")
        print("   - vss: システム状態確認") 
        print("   - vsf: 自動修復")
        print("   - vst: 自動監視開始")
        
        return True
    
    def create_vscode_integration(self):
        """VS Code統合を作成"""
        print("🎨 VS Code統合をセットアップ中...")
        
        vscode_dir = ".vscode"
        os.makedirs(vscode_dir, exist_ok=True)
        
        # タスク設定
        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Vercel Smart Deploy",
                    "type": "shell",
                    "command": "python3",
                    "args": ["vercel_unified_system.py", "deploy"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "new"
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Vercel Status",
                    "type": "shell", 
                    "command": "python3",
                    "args": ["vercel_unified_system.py", "dashboard"],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "Vercel Auto Monitor",
                    "type": "shell",
                    "command": "python3", 
                    "args": ["vercel_auto_trigger.py", "start"],
                    "group": "test",
                    "isBackground": True,
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "panel": "new"
                    }
                }
            ]
        }
        
        with open(os.path.join(vscode_dir, "tasks.json"), 'w') as f:
            json.dump(tasks_config, f, indent=2)
        
        # キーバインド設定
        keybindings = [
            {
                "key": "ctrl+shift+v ctrl+shift+d",
                "command": "workbench.action.tasks.runTask",
                "args": "Vercel Smart Deploy"
            },
            {
                "key": "ctrl+shift+v ctrl+shift+s", 
                "command": "workbench.action.tasks.runTask",
                "args": "Vercel Status"
            }
        ]
        
        with open(os.path.join(vscode_dir, "keybindings.json"), 'w') as f:
            json.dump(keybindings, f, indent=2)
        
        print("✅ VS Code統合設定を作成しました")
        print("📋 使用可能なタスク:")
        print("  - Ctrl+Shift+V, Ctrl+Shift+D: スマートデプロイ")
        print("  - Ctrl+Shift+V, Ctrl+Shift+S: システム状態")
        print("  - コマンドパレット > Tasks: Run Task")
        
        return True
    
    def setup_file_watcher(self):
        """ファイル監視をセットアップ"""
        print("👁️ ファイル監視をセットアップ中...")
        
        # systemdサービス設定（Linux）
        if os.path.exists("/etc/systemd/system"):
            systemd_service = f"""[Unit]
Description=Vercel Auto Trigger Service
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'root')}
WorkingDirectory={os.getcwd()}
ExecStart=/usr/bin/python3 {os.path.join(os.getcwd(), 'vercel_auto_trigger.py')} start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
            service_file = "vercel-auto-trigger.service"
            with open(service_file, 'w') as f:
                f.write(systemd_service)
            
            print(f"✅ systemdサービスファイルを作成: {service_file}")
            print("📋 サービス有効化:")
            print(f"  sudo cp {service_file} /etc/systemd/system/")
            print("  sudo systemctl enable vercel-auto-trigger")
            print("  sudo systemctl start vercel-auto-trigger")
        
        # launchd設定（macOS）
        if os.path.exists("/System/Library/LaunchDaemons"):
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vercel.auto-trigger</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{os.path.join(os.getcwd(), 'vercel_auto_trigger.py')}</string>
        <string>start</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{os.getcwd()}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
            plist_file = "com.vercel.auto-trigger.plist"
            with open(plist_file, 'w') as f:
                f.write(plist_content)
            
            print(f"✅ launchdサービスファイルを作成: {plist_file}")
            print("📋 サービス有効化:")
            print(f"  cp {plist_file} ~/Library/LaunchAgents/")
            print("  launchctl load ~/Library/LaunchAgents/com.vercel.auto-trigger.plist")
        
        return True
    
    def comprehensive_setup(self):
        """包括的なセットアップ"""
        print("🚀 Vercelスマート統合システム包括的セットアップ")
        print("=" * 60)
        
        setup_results = {}
        
        # 1. コマンドラッパー
        print("\n1️⃣ コマンドラッパー作成...")
        setup_results["command_wrappers"] = self.create_command_wrappers()
        
        # 2. シェル統合
        print("\n2️⃣ シェル統合セットアップ...")
        setup_results["shell_integration"] = self.setup_shell_integration()
        
        # 3. VS Code統合
        print("\n3️⃣ VS Code統合セットアップ...")
        setup_results["vscode_integration"] = self.create_vscode_integration()
        
        # 4. ファイル監視
        print("\n4️⃣ ファイル監視セットアップ...")
        setup_results["file_watcher"] = self.setup_file_watcher()
        
        # 5. 自動トリガーセットアップ
        print("\n5️⃣ 自動トリガーセットアップ...")
        from vercel_auto_trigger import VercelAutoTrigger
        trigger = VercelAutoTrigger()
        trigger.setup_git_hooks()
        setup_results["auto_trigger"] = True
        
        # 状態を保存
        self.status.update({
            "hooks_installed": True,
            "auto_trigger_enabled": True,
            "last_integration": datetime.now().isoformat(),
            "setup_results": setup_results
        })
        self._save_status()
        
        # 完了報告
        print("\n" + "=" * 60)
        print("✅ 包括的セットアップ完了!")
        print("=" * 60)
        
        print("\n📋 有効化された機能:")
        for feature, status in setup_results.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {feature}")
        
        print("\n🎯 次のステップ:")
        print("1. source vercel_shell_integration.sh  # シェル統合有効化")
        print("2. python3 vercel_auto_trigger.py start  # 監視開始")
        print("3. vsd  # スマートデプロイテスト")
        
        print("\n🔧 利用可能なコマンド:")
        print("  - vsd: スマートデプロイ")
        print("  - vss: システム状態確認")
        print("  - vsf: 自動修復")
        print("  - vst: 自動監視開始")
        
        return setup_results

def main():
    import sys
    
    integration = VercelSmartIntegration()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            integration.comprehensive_setup()
        elif command == "wrappers":
            integration.create_command_wrappers()
        elif command == "shell":
            integration.setup_shell_integration()
        elif command == "vscode":
            integration.create_vscode_integration()
        elif command == "watcher":
            integration.setup_file_watcher()
        elif command == "status":
            print(json.dumps(integration.status, ensure_ascii=False, indent=2))
        else:
            print(f"不明なコマンド: {command}")
            print("使用方法:")
            print("  python3 vercel_smart_integration.py setup     # 包括的セットアップ")
            print("  python3 vercel_smart_integration.py wrappers # コマンドラッパー")
            print("  python3 vercel_smart_integration.py shell    # シェル統合")
            print("  python3 vercel_smart_integration.py vscode   # VS Code統合")
            print("  python3 vercel_smart_integration.py watcher  # ファイル監視")
            print("  python3 vercel_smart_integration.py status   # 状態確認")
    else:
        # デフォルトは包括的セットアップ
        integration.comprehensive_setup()

if __name__ == "__main__":
    main()