#!/usr/bin/env python3
"""
GitHub Personal Access Token Auto Git Manager
Claude Codeで作成・編集したファイルを自動的にGitHubにコミット・プッシュするスクリプト

機能:
1. Git初期化とリモートリポジトリ設定
2. Personal Access Token認証設定
3. 自動git add、commit、push機能
4. コミットメッセージ自動生成
5. VS Codeタスクとの連携
6. エラーハンドリングとログ出力
"""

import os
import sys
import subprocess
import json
import logging
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import configparser
import getpass

class AutoGitManager:
    """自動Git管理クラス"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.config_file = self.repo_path / ".git_config.ini"
        self.log_file = self.repo_path / "git_auto_manager.log"
        
        # ログ設定
        self.setup_logging()
        
        # 設定読み込み
        self.config = self.load_config()
        
        self.logger.info(f"AutoGitManager initialized for: {self.repo_path}")
    
    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> configparser.ConfigParser:
        """設定ファイル読み込み"""
        config = configparser.ConfigParser()
        
        if self.config_file.exists():
            config.read(self.config_file, encoding='utf-8')
            self.logger.info("Configuration loaded from file")
        else:
            self.logger.info("No config file found, will create new one")
        
        return config
    
    def save_config(self):
        """設定ファイル保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
        self.logger.info(f"Configuration saved to {self.config_file}")
    
    def run_git_command(self, command: List[str]) -> Tuple[bool, str, str]:
        """Gitコマンド実行"""
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            
            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            if success:
                self.logger.debug(f"Git command succeeded: {' '.join(command)}")
                if stdout:
                    self.logger.debug(f"Output: {stdout}")
            else:
                self.logger.error(f"Git command failed: {' '.join(command)}")
                self.logger.error(f"Error: {stderr}")
            
            return success, stdout, stderr
            
        except Exception as e:
            self.logger.error(f"Exception running git command: {e}")
            return False, "", str(e)
    
    def setup_git_credentials(self, username: str, token: str, email: str):
        """Git認証情報設定"""
        try:
            # ユーザー情報設定
            success1, _, _ = self.run_git_command(['git', 'config', 'user.name', username])
            success2, _, _ = self.run_git_command(['git', 'config', 'user.email', email])
            
            if success1 and success2:
                # 設定保存
                if 'git' not in self.config:
                    self.config.add_section('git')
                
                self.config['git']['username'] = username
                self.config['git']['email'] = email
                self.config['git']['token'] = token  # 注意: 本番環境では暗号化推奨
                
                self.save_config()
                self.logger.info("Git credentials configured successfully")
                return True
            else:
                self.logger.error("Failed to configure git user info")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up git credentials: {e}")
            return False
    
    def initialize_repository(self, remote_url: str) -> bool:
        """リポジトリ初期化"""
        try:
            # Git初期化チェック
            if not (self.repo_path / '.git').exists():
                success, _, _ = self.run_git_command(['git', 'init'])
                if not success:
                    return False
                self.logger.info("Git repository initialized")
            
            # リモートリポジトリ設定
            success, stdout, _ = self.run_git_command(['git', 'remote', 'get-url', 'origin'])
            
            if not success:
                # Personal Access Tokenを使用したURL作成
                username = self.config.get('git', 'username', fallback='')
                token = self.config.get('git', 'token', fallback='')
                
                if username and token:
                    # https://username:token@github.com/user/repo.git 形式
                    if remote_url.startswith('https://github.com/'):
                        auth_url = remote_url.replace('https://github.com/', f'https://{username}:{token}@github.com/')
                    else:
                        auth_url = remote_url
                    
                    success, _, _ = self.run_git_command(['git', 'remote', 'add', 'origin', auth_url])
                    if success:
                        self.logger.info(f"Remote repository added: {remote_url}")
                    else:
                        return False
                else:
                    self.logger.error("Username or token not configured")
                    return False
            else:
                self.logger.info(f"Remote repository already configured: {stdout}")
            
            # 設定保存
            if 'repository' not in self.config:
                self.config.add_section('repository')
            self.config['repository']['remote_url'] = remote_url
            self.save_config()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing repository: {e}")
            return False
    
    def get_changed_files(self) -> List[str]:
        """変更されたファイル一覧取得"""
        try:
            # ステージングエリアとワーキングディレクトリの変更
            success, stdout, _ = self.run_git_command(['git', 'status', '--porcelain'])
            
            if success:
                changed_files = []
                for line in stdout.split('\n'):
                    if line.strip():
                        # フォーマット: XY filename
                        status = line[:2]
                        filename = line[3:]
                        changed_files.append(filename)
                
                return changed_files
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting changed files: {e}")
            return []
    
    def generate_commit_message(self, changed_files: List[str]) -> str:
        """コミットメッセージ自動生成"""
        try:
            if not changed_files:
                return "Update files"
            
            # ファイル分析
            added_files = []
            modified_files = []
            deleted_files = []
            
            success, stdout, _ = self.run_git_command(['git', 'status', '--porcelain'])
            if success:
                for line in stdout.split('\n'):
                    if line.strip():
                        status = line[:2]
                        filename = line[3:]
                        
                        if 'A' in status or '??' in status:
                            added_files.append(filename)
                        elif 'M' in status:
                            modified_files.append(filename)
                        elif 'D' in status:
                            deleted_files.append(filename)
            
            # メッセージ構築
            message_parts = []
            
            if added_files:
                if len(added_files) == 1:
                    message_parts.append(f"Add {added_files[0]}")
                else:
                    message_parts.append(f"Add {len(added_files)} new files")
            
            if modified_files:
                if len(modified_files) == 1:
                    message_parts.append(f"Update {modified_files[0]}")
                else:
                    message_parts.append(f"Update {len(modified_files)} files")
            
            if deleted_files:
                if len(deleted_files) == 1:
                    message_parts.append(f"Delete {deleted_files[0]}")
                else:
                    message_parts.append(f"Delete {len(deleted_files)} files")
            
            if message_parts:
                base_message = " and ".join(message_parts)
            else:
                base_message = "Update repository"
            
            # Claude Code署名追加
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            commit_message = f"""{base_message}

🚀 Generated with [Claude Code](https://claude.ai/code)
📅 Auto-committed: {timestamp}

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            return commit_message
            
        except Exception as e:
            self.logger.error(f"Error generating commit message: {e}")
            return f"Auto-commit: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def auto_commit_push(self, commit_message: Optional[str] = None) -> bool:
        """自動コミット・プッシュ"""
        try:
            # 変更ファイル確認
            changed_files = self.get_changed_files()
            
            if not changed_files:
                self.logger.info("No changes to commit")
                return True
            
            self.logger.info(f"Found {len(changed_files)} changed files")
            for file in changed_files:
                self.logger.info(f"  - {file}")
            
            # ファイル追加
            success, _, _ = self.run_git_command(['git', 'add', '.'])
            if not success:
                self.logger.error("Failed to add files")
                return False
            
            # コミットメッセージ生成
            if not commit_message:
                commit_message = self.generate_commit_message(changed_files)
            
            # コミット
            success, _, stderr = self.run_git_command(['git', 'commit', '-m', commit_message])
            if not success:
                if "nothing to commit" in stderr:
                    self.logger.info("Nothing to commit")
                    return True
                else:
                    self.logger.error("Failed to commit")
                    return False
            
            # プッシュ
            success, _, stderr = self.run_git_command(['git', 'push', 'origin', 'master'])
            if not success:
                # masterブランチが存在しない場合はmainを試す
                success, _, _ = self.run_git_command(['git', 'push', 'origin', 'main'])
                if not success:
                    # 初回プッシュの場合
                    success, _, _ = self.run_git_command(['git', 'push', '-u', 'origin', 'master'])
                    if not success:
                        success, _, _ = self.run_git_command(['git', 'push', '-u', 'origin', 'main'])
            
            if success:
                self.logger.info("Successfully committed and pushed changes")
                return True
            else:
                self.logger.error("Failed to push changes")
                return False
            
        except Exception as e:
            self.logger.error(f"Error in auto commit/push: {e}")
            return False
    
    def create_vscode_tasks(self):
        """VS Code タスク設定作成"""
        try:
            vscode_dir = self.repo_path / '.vscode'
            vscode_dir.mkdir(exist_ok=True)
            
            tasks_file = vscode_dir / 'tasks.json'
            
            tasks_config = {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Git Auto Commit & Push",
                        "type": "shell",
                        "command": "python",
                        "args": ["auto_git_manager.py", "--auto-commit"],
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
                        "label": "Git Setup",
                        "type": "shell",
                        "command": "python",
                        "args": ["auto_git_manager.py", "--setup"],
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
                        "label": "Git Status",
                        "type": "shell",
                        "command": "python",
                        "args": ["auto_git_manager.py", "--status"],
                        "group": "test",
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
            
            with open(tasks_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"VS Code tasks created: {tasks_file}")
            
            # キーバインド設定も作成
            keybindings_file = vscode_dir / 'keybindings.json'
            keybindings_config = [
                {
                    "key": "ctrl+shift+g ctrl+shift+p",
                    "command": "workbench.action.tasks.runTask",
                    "args": "Git Auto Commit & Push"
                },
                {
                    "key": "ctrl+shift+g ctrl+shift+s",
                    "command": "workbench.action.tasks.runTask",
                    "args": "Git Status"
                }
            ]
            
            with open(keybindings_file, 'w', encoding='utf-8') as f:
                json.dump(keybindings_config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"VS Code keybindings created: {keybindings_file}")
            
        except Exception as e:
            self.logger.error(f"Error creating VS Code tasks: {e}")
    
    def setup_interactive(self):
        """対話式セットアップ"""
        try:
            print("🚀 Auto Git Manager セットアップ")
            print("=" * 50)
            
            # GitHub情報入力
            username = input("GitHub ユーザー名: ").strip()
            email = input("メールアドレス: ").strip()
            
            print("\n📝 Personal Access Token が必要です")
            print("GitHub → Settings → Developer settings → Personal access tokens で作成")
            print("必要な権限: repo, workflow")
            token = getpass.getpass("Personal Access Token: ").strip()
            
            repo_url = input("リポジトリURL (例: https://github.com/user/repo.git): ").strip()
            
            # 設定適用
            if self.setup_git_credentials(username, token, email):
                if self.initialize_repository(repo_url):
                    self.create_vscode_tasks()
                    print("\n✅ セットアップ完了!")
                    print("\nVS Codeで以下のタスクが利用可能です:")
                    print("- Ctrl+Shift+P → 'Tasks: Run Task' → 'Git Auto Commit & Push'")
                    print("- または: Ctrl+Shift+G Ctrl+Shift+P (ショートカット)")
                    return True
                else:
                    print("❌ リポジトリ初期化に失敗しました")
                    return False
            else:
                print("❌ Git認証設定に失敗しました")
                return False
                
        except KeyboardInterrupt:
            print("\n❌ セットアップがキャンセルされました")
            return False
        except Exception as e:
            self.logger.error(f"Setup error: {e}")
            print(f"❌ セットアップエラー: {e}")
            return False
    
    def show_status(self):
        """Git状態表示"""
        try:
            print("📊 Git リポジトリ状態")
            print("=" * 30)
            
            # ブランチ情報
            success, stdout, _ = self.run_git_command(['git', 'branch', '--show-current'])
            if success:
                print(f"現在のブランチ: {stdout}")
            
            # リモートリポジトリ
            success, stdout, _ = self.run_git_command(['git', 'remote', 'get-url', 'origin'])
            if success:
                print(f"リモートリポジトリ: {stdout}")
            
            # 変更ファイル
            changed_files = self.get_changed_files()
            if changed_files:
                print(f"\n変更ファイル数: {len(changed_files)}")
                for file in changed_files[:10]:  # 最大10件表示
                    print(f"  - {file}")
                if len(changed_files) > 10:
                    print(f"  ... and {len(changed_files) - 10} more files")
            else:
                print("\n変更ファイル: なし")
            
            # 最新コミット
            success, stdout, _ = self.run_git_command(['git', 'log', '--oneline', '-1'])
            if success:
                print(f"\n最新コミット: {stdout}")
            
        except Exception as e:
            self.logger.error(f"Error showing status: {e}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Auto Git Manager for Claude Code")
    parser.add_argument('--setup', action='store_true', help='対話式セットアップ実行')
    parser.add_argument('--auto-commit', action='store_true', help='自動コミット・プッシュ実行')
    parser.add_argument('--status', action='store_true', help='Git状態表示')
    parser.add_argument('--message', '-m', type=str, help='カスタムコミットメッセージ')
    parser.add_argument('--path', type=str, default='.', help='リポジトリパス')
    
    args = parser.parse_args()
    
    # AutoGitManager初期化
    manager = AutoGitManager(args.path)
    
    try:
        if args.setup:
            success = manager.setup_interactive()
            sys.exit(0 if success else 1)
        
        elif args.auto_commit:
            success = manager.auto_commit_push(args.message)
            if success:
                print("✅ 自動コミット・プッシュ完了")
            else:
                print("❌ 自動コミット・プッシュ失敗")
            sys.exit(0 if success else 1)
        
        elif args.status:
            manager.show_status()
            sys.exit(0)
        
        else:
            # デフォルト: ヘルプ表示
            parser.print_help()
            print("\n🚀 使用例:")
            print("  初回セットアップ:     python auto_git_manager.py --setup")
            print("  自動コミット・プッシュ: python auto_git_manager.py --auto-commit")
            print("  Git状態確認:         python auto_git_manager.py --status")
            print("  カスタムメッセージ:   python auto_git_manager.py --auto-commit -m 'Custom message'")
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n❌ 処理がキャンセルされました")
        sys.exit(1)
    except Exception as e:
        manager.logger.error(f"Unexpected error: {e}")
        print(f"❌ 予期しないエラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()