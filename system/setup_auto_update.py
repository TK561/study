#!/usr/bin/env python3
"""
自動更新システム セットアップスクリプト
研究ディスカッション記録の自動更新システムを簡単にセットアップ・管理
"""

import os
import json
import subprocess
from pathlib import Path

class AutoUpdateSetup:
    def __init__(self):
        self.research_root = Path(__file__).parent
        self.auto_update_script = self.research_root / "auto_update_system.py"
        self.service_file = self.research_root / ".auto_update_service.json"
        
    def create_aliases(self):
        """便利なエイリアスを作成"""
        bashrc_path = Path.home() / ".bashrc"
        
        aliases = [
            "# 研究ディスカッション記録 自動更新システム",
            f"alias discussion-check='python3 {self.auto_update_script} check'",
            f"alias discussion-monitor='python3 {self.auto_update_script} monitor'",
            f"alias discussion-config='python3 {self.auto_update_script} config'",
            f"alias discussion-setup='python3 {self.research_root}/setup_auto_update.py'",
            ""
        ]
        
        # 既存のエイリアスをチェック
        existing_content = ""
        if bashrc_path.exists():
            with open(bashrc_path, 'r') as f:
                existing_content = f.read()
        
        # エイリアスが既に存在するかチェック
        if "discussion-check" not in existing_content:
            with open(bashrc_path, 'a') as f:
                f.write("\n".join(aliases))
            print("✅ エイリアスを .bashrc に追加しました")
            print("次回ターミナル起動時から以下のコマンドが使用可能です:")
            print("  discussion-check   # 1回チェック")
            print("  discussion-monitor # 継続監視")
            print("  discussion-config  # 設定表示")
            print("  discussion-setup   # セットアップ管理")
        else:
            print("📝 エイリアスは既に設定済みです")
    
    def create_systemd_service(self):
        """systemd サービスファイルを作成（Linux用）"""
        service_content = f"""[Unit]
Description=研究ディスカッション記録 自動更新監視
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={self.research_root}
ExecStart=/usr/bin/python3 {self.auto_update_script} monitor 60
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        service_path = Path("/etc/systemd/system/discussion-auto-update.service")
        
        try:
            # root権限が必要
            with open("discussion-auto-update.service", 'w') as f:
                f.write(service_content)
            
            print("📄 サービスファイルを作成しました")
            print("管理者権限でインストールするには:")
            print(f"  sudo mv discussion-auto-update.service {service_path}")
            print("  sudo systemctl daemon-reload")
            print("  sudo systemctl enable discussion-auto-update")
            print("  sudo systemctl start discussion-auto-update")
            
        except Exception as e:
            print(f"❌ サービスファイル作成エラー: {e}")
    
    def create_cron_job(self):
        """cron ジョブを作成"""
        cron_command = f"*/5 * * * * cd {self.research_root} && python3 {self.auto_update_script} check"
        
        print("⏰ cron ジョブの設定:")
        print("以下のコマンドを実行してcron設定に追加してください:")
        print(f"  crontab -e")
        print(f"そして以下の行を追加:")
        print(f"  {cron_command}")
        print("（5分ごとにチェックを実行）")
    
    def test_system(self):
        """システムのテスト"""
        print("🔍 自動更新システムのテスト中...")
        
        # スクリプトファイルの存在確認
        if not self.auto_update_script.exists():
            print("❌ auto_update_system.py が見つかりません")
            return False
        
        # Pythonスクリプトの実行テスト
        try:
            result = subprocess.run(
                ["python3", str(self.auto_update_script), "config"],
                capture_output=True,
                text=True,
                cwd=self.research_root
            )
            
            if result.returncode == 0:
                print("✅ スクリプトの実行テスト成功")
                print("📋 現在の設定:")
                print(result.stdout)
                return True
            else:
                print(f"❌ スクリプト実行エラー: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ テスト実行エラー: {e}")
            return False
    
    def setup_vscode_tasks(self):
        """VS Code タスクを設定"""
        vscode_dir = self.research_root / ".vscode"
        tasks_file = vscode_dir / "tasks.json"
        
        vscode_dir.mkdir(exist_ok=True)
        
        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Discussion: Check Updates",
                    "type": "shell",
                    "command": "python3",
                    "args": ["auto_update_system.py", "check"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Discussion: Start Monitoring",
                    "type": "shell",
                    "command": "python3",
                    "args": ["auto_update_system.py", "monitor", "30"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": True,
                        "panel": "dedicated"
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Discussion: Show Config",
                    "type": "shell",
                    "command": "python3",
                    "args": ["auto_update_system.py", "config"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                }
            ]
        }
        
        # 既存のtasks.jsonがある場合は統合
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r') as f:
                    existing_tasks = json.load(f)
                
                # 既存のタスクに追加
                if "tasks" in existing_tasks:
                    existing_tasks["tasks"].extend(tasks_config["tasks"])
                else:
                    existing_tasks = tasks_config
                    
                tasks_config = existing_tasks
            except:
                # 既存ファイルの読み込みに失敗した場合は新規作成
                pass
        
        with open(tasks_file, 'w') as f:
            json.dump(tasks_config, f, indent=2)
        
        print("✅ VS Code タスクを設定しました")
        print("VS Code の Command Palette (Ctrl+Shift+P) から以下が実行可能:")
        print("  Tasks: Run Task > Discussion: Check Updates")
        print("  Tasks: Run Task > Discussion: Start Monitoring")
        print("  Tasks: Run Task > Discussion: Show Config")

def main():
    """メイン関数"""
    import sys
    
    setup = AutoUpdateSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "aliases":
            setup.create_aliases()
        elif command == "systemd":
            setup.create_systemd_service()
        elif command == "cron":
            setup.create_cron_job()
        elif command == "test":
            setup.test_system()
        elif command == "vscode":
            setup.setup_vscode_tasks()
        elif command == "all":
            print("🚀 自動更新システム 完全セットアップ")
            print("=" * 50)
            setup.test_system()
            print("\n" + "=" * 50)
            setup.create_aliases()
            print("\n" + "=" * 50)
            setup.setup_vscode_tasks()
            print("\n" + "=" * 50)
            setup.create_cron_job()
            print("\n" + "=" * 50)
            print("✅ セットアップ完了!")
        else:
            print("❌ 不明なコマンド")
            print_usage()
    else:
        print_usage()

def print_usage():
    """使用方法を表示"""
    print("🔧 自動更新システム セットアップ")
    print("=" * 40)
    print("使用法:")
    print("  python3 setup_auto_update.py <command>")
    print("")
    print("コマンド:")
    print("  all      # 完全セットアップ（推奨）")
    print("  test     # システムテスト")
    print("  aliases  # エイリアス作成")
    print("  vscode   # VS Code タスク設定")
    print("  cron     # cron ジョブ設定（手動）")
    print("  systemd  # systemd サービス作成")
    print("")
    print("推奨:")
    print("  python3 setup_auto_update.py all")

if __name__ == "__main__":
    main()