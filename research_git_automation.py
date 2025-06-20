#!/usr/bin/env python3
"""
研究プロジェクト用GitHub自動化システム
=====================================

Claude Codeを活用した研究プロジェクトのためのGit自動化ツール
研究データ、コード、論文作成支援を含む包括的な自動化機能

主な機能:
1. Gitリポジトリ初期化とリモート設定
2. Personal Access Token認証（変数参照方式）
3. Claude Code作業の自動コミット・プッシュ
4. 研究データとコードの自動バックアップ
5. コミットメッセージ自動生成（研究進捗ベース）
6. 実験ログ管理
7. データ管理とバックアップ
"""

import os
import sys
import subprocess
import json
import logging
import argparse
import datetime
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import hashlib

# 設定ファイルのインポート
try:
    import config
    CONFIG_AVAILABLE = True
except ImportError:
    print("❌ config.py が見つかりません。")
    print("📝 config.example.py をコピーして config.py を作成し、設定を入力してください:")
    print("   cp config.example.py config.py")
    sys.exit(1)

class ResearchGitAutomation:
    """研究プロジェクト用Git自動化クラス"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.config = config
        
        # ログ設定
        self.log_file = self.repo_path / "research_automation.log"
        self.setup_logging()
        
        # 設定検証
        self.validate_config()
        
        # 実験ログファイル
        self.experiment_log = self.repo_path / self.config.EXPERIMENT_LOG_FILE
        
        self.logger.info(f"ResearchGitAutomation initialized for: {self.repo_path}")
        self.logger.info(f"Project: {self.config.PROJECT_NAME}")
    
    def setup_logging(self):
        """ログ設定"""
        log_level = getattr(logging, self.config.LOG_LEVEL, logging.INFO)
        
        # ログファイルのローテーション
        if self.log_file.exists() and self.log_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
            backup_log = self.log_file.with_suffix('.log.bak')
            shutil.move(str(self.log_file), str(backup_log))
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout) if self.config.VERBOSE_LOGGING else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_config(self):
        """設定の妥当性チェック"""
        errors, warnings = config.validate_config()
        
        if errors:
            self.logger.error("設定エラーが見つかりました:")
            for error in errors:
                self.logger.error(f"  {error}")
            raise ValueError("設定ファイルを修正してください")
        
        if warnings:
            for warning in warnings:
                self.logger.warning(f"  {warning}")
    
    def run_git_command(self, command: List[str]) -> Tuple[bool, str, str]:
        """Gitコマンド実行"""
        try:
            if self.config.DEBUG_MODE:
                self.logger.debug(f"Executing: {' '.join(command)}")
            
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
                if self.config.DEBUG_MODE and stdout:
                    self.logger.debug(f"Output: {stdout}")
            else:
                self.logger.error(f"Git command failed: {' '.join(command)}")
                self.logger.error(f"Error: {stderr}")
            
            return success, stdout, stderr
            
        except Exception as e:
            self.logger.error(f"Exception running git command: {e}")
            return False, "", str(e)
    
    def setup_git_credentials(self):
        """Git認証情報設定"""
        try:
            # ユーザー情報設定
            success1, _, _ = self.run_git_command(['git', 'config', 'user.name', self.config.RESEARCHER_NAME or self.config.GITHUB_USERNAME])
            success2, _, _ = self.run_git_command(['git', 'config', 'user.email', self.config.GITHUB_EMAIL])
            
            if success1 and success2:
                self.logger.info("Git credentials configured successfully")
                return True
            else:
                self.logger.error("Failed to configure git user info")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting up git credentials: {e}")
            return False
    
    def initialize_repository(self) -> bool:
        """リポジトリ初期化"""
        try:
            # Git初期化チェック
            if not (self.repo_path / '.git').exists():
                success, _, _ = self.run_git_command(['git', 'init'])
                if not success:
                    return False
                self.logger.info("Git repository initialized")
            
            # Git credentials設定
            if not self.setup_git_credentials():
                return False
            
            # リモートリポジトリ設定
            remote_url = f"https://github.com/{self.config.GITHUB_USERNAME}/{self.config.REPOSITORY_NAME}.git"
            auth_url = f"https://{self.config.GITHUB_USERNAME}:{self.config.GITHUB_TOKEN}@github.com/{self.config.GITHUB_USERNAME}/{self.config.REPOSITORY_NAME}.git"
            
            success, stdout, _ = self.run_git_command(['git', 'remote', 'get-url', 'origin'])
            
            if not success:
                success, _, _ = self.run_git_command(['git', 'remote', 'add', 'origin', auth_url])
                if success:
                    self.logger.info(f"Remote repository added: {remote_url}")
                else:
                    return False
            else:
                self.logger.info(f"Remote repository already configured: {stdout}")
            
            # 研究プロジェクト用ディレクトリ構造作成
            self.create_research_structure()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing repository: {e}")
            return False
    
    def create_research_structure(self):
        """研究プロジェクト用ディレクトリ構造作成"""
        self.logger.info("Creating research project structure...")
        
        for name, path in self.config.DATA_STRUCTURE.items():
            dir_path = self.repo_path / path
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # .gitkeep ファイル作成（空ディレクトリ用）
            gitkeep = dir_path / '.gitkeep'
            if not gitkeep.exists():
                gitkeep.touch()
            
            self.logger.debug(f"Created directory: {path}")
        
        self.logger.info("Research project structure created")
    
    def get_changed_files(self) -> List[str]:
        """変更されたファイル一覧取得（研究プロジェクト用フィルタリング）"""
        try:
            success, stdout, _ = self.run_git_command(['git', 'status', '--porcelain'])
            
            if success:
                changed_files = []
                for line in stdout.split('\n'):
                    if line.strip():
                        filename = line[3:]
                        
                        # 拡張子フィルタリング
                        if any(filename.endswith(ext) for ext in self.config.TRACKED_EXTENSIONS):
                            # 除外ディレクトリチェック
                            if not any(excluded in filename for excluded in self.config.EXCLUDED_DIRECTORIES):
                                changed_files.append(filename)
                
                return changed_files
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting changed files: {e}")
            return []
    
    def analyze_changes(self, changed_files: List[str]) -> Dict[str, Any]:
        """変更内容の分析（研究コンテキスト）"""
        analysis = {
            'code_files': [],
            'data_files': [],
            'notebook_files': [],
            'doc_files': [],
            'config_files': [],
            'result_files': [],
            'change_type': 'unknown',
            'research_activity': 'general'
        }
        
        for file in changed_files:
            if file.endswith('.py'):
                analysis['code_files'].append(file)
            elif file.endswith('.ipynb'):
                analysis['notebook_files'].append(file)
            elif file.endswith(('.csv', '.json', '.pkl')):
                analysis['data_files'].append(file)
            elif file.endswith(('.md', '.tex', '.txt')):
                analysis['doc_files'].append(file)
            elif file.endswith(('.yml', '.yaml', '.ini')):
                analysis['config_files'].append(file)
            elif 'result' in file.lower() or 'output' in file.lower():
                analysis['result_files'].append(file)
        
        # 研究活動の推定
        if analysis['notebook_files']:
            analysis['research_activity'] = 'experiment'
        elif analysis['code_files'] and 'test' in str(analysis['code_files']):
            analysis['research_activity'] = 'testing'
        elif analysis['result_files']:
            analysis['research_activity'] = 'analysis'
        elif analysis['doc_files']:
            analysis['research_activity'] = 'documentation'
        elif analysis['code_files']:
            analysis['research_activity'] = 'development'
        
        # 変更タイプの推定
        success, stdout, _ = self.run_git_command(['git', 'status', '--porcelain'])
        if success:
            if any(line.startswith('A ') or line.startswith('??') for line in stdout.split('\n')):
                analysis['change_type'] = 'addition'
            elif any(line.startswith('M ') for line in stdout.split('\n')):
                analysis['change_type'] = 'modification'
            elif any(line.startswith('D ') for line in stdout.split('\n')):
                analysis['change_type'] = 'deletion'
        
        return analysis
    
    def generate_research_commit_message(self, changed_files: List[str], analysis: Dict[str, Any]) -> str:
        """研究進捗に基づくコミットメッセージ生成"""
        try:
            # ベースメッセージの決定
            activity_messages = {
                'experiment': '🧪 実験実施',
                'testing': '🧪 テスト実行',
                'analysis': '📊 結果分析',
                'documentation': '📝 文書更新',
                'development': '💻 コード開発',
                'general': '🔄 プロジェクト更新'
            }
            
            base_msg = activity_messages.get(analysis['research_activity'], '🔄 プロジェクト更新')
            
            # 詳細情報の追加
            details = []
            
            if analysis['code_files']:
                if len(analysis['code_files']) == 1:
                    details.append(f"コード: {Path(analysis['code_files'][0]).name}")
                else:
                    details.append(f"コード: {len(analysis['code_files'])}ファイル")
            
            if analysis['notebook_files']:
                if len(analysis['notebook_files']) == 1:
                    details.append(f"ノートブック: {Path(analysis['notebook_files'][0]).name}")
                else:
                    details.append(f"ノートブック: {len(analysis['notebook_files'])}ファイル")
            
            if analysis['data_files']:
                details.append(f"データ: {len(analysis['data_files'])}ファイル")
            
            if analysis['result_files']:
                details.append(f"結果: {len(analysis['result_files'])}ファイル")
            
            # メッセージ構築
            if details:
                title = f"{base_msg}: {', '.join(details[:2])}"
                if len(details) > 2:
                    title += f" 他{len(details)-2}項目"
            else:
                title = base_msg
            
            # タイムスタンプ
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 完全なコミットメッセージ
            commit_message = f"""{title}

📂 プロジェクト: {self.config.PROJECT_NAME}
🔬 研究活動: {analysis['research_activity']}
📅 実行日時: {timestamp}

変更サマリー:
"""
            
            if analysis['code_files']:
                commit_message += f"• Pythonコード: {len(analysis['code_files'])}ファイル\n"
            if analysis['notebook_files']:
                commit_message += f"• Jupyter Notebook: {len(analysis['notebook_files'])}ファイル\n"
            if analysis['data_files']:
                commit_message += f"• データファイル: {len(analysis['data_files'])}ファイル\n"
            if analysis['doc_files']:
                commit_message += f"• ドキュメント: {len(analysis['doc_files'])}ファイル\n"
            if analysis['result_files']:
                commit_message += f"• 実験結果: {len(analysis['result_files'])}ファイル\n"
            
            commit_message += f"""
🚀 Generated with [Claude Code](https://claude.ai/code)
🎓 Research automation system

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            return commit_message
            
        except Exception as e:
            self.logger.error(f"Error generating commit message: {e}")
            return f"🔄 研究プロジェクト更新: {timestamp}"
    
    def log_experiment(self, analysis: Dict[str, Any], commit_hash: str = None):
        """実験ログの記録"""
        try:
            # 実験ログデータ
            experiment_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'commit_hash': commit_hash,
                'research_activity': analysis['research_activity'],
                'change_type': analysis['change_type'],
                'files_modified': {
                    'code': len(analysis['code_files']),
                    'notebooks': len(analysis['notebook_files']),
                    'data': len(analysis['data_files']),
                    'results': len(analysis['result_files']),
                    'docs': len(analysis['doc_files'])
                },
                'project_metadata': self.config.EXPERIMENT_METADATA
            }
            
            # 既存ログの読み込み
            experiments = []
            if self.experiment_log.exists():
                try:
                    with open(self.experiment_log, 'r', encoding='utf-8') as f:
                        experiments = json.load(f)
                except json.JSONDecodeError:
                    self.logger.warning("Experiment log corrupted, creating new log")
                    experiments = []
            
            # 新しい実験データを追加
            experiments.append(experiment_data)
            
            # ログファイルの保存
            with open(self.experiment_log, 'w', encoding='utf-8') as f:
                json.dump(experiments, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Experiment logged: {analysis['research_activity']}")
            
        except Exception as e:
            self.logger.error(f"Error logging experiment: {e}")
    
    def auto_backup(self):
        """研究データの自動バックアップ"""
        if not self.config.AUTO_BACKUP_ENABLED:
            return True
        
        try:
            backup_dir = self.repo_path / 'backups' / datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            backed_up_files = 0
            
            for directory in self.config.BACKUP_DIRECTORIES:
                src_dir = self.repo_path / directory
                if src_dir.exists():
                    dst_dir = backup_dir / directory
                    try:
                        shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns('*.tmp', '__pycache__'))
                        backed_up_files += sum(1 for _ in dst_dir.rglob('*') if _.is_file())
                        self.logger.debug(f"Backed up: {directory}")
                    except Exception as e:
                        self.logger.warning(f"Failed to backup {directory}: {e}")
            
            if backed_up_files > 0:
                # バックアップサマリーファイル作成
                summary_file = backup_dir / 'backup_summary.json'
                summary_data = {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'files_count': backed_up_files,
                    'directories': self.config.BACKUP_DIRECTORIES,
                    'project_name': self.config.PROJECT_NAME
                }
                
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary_data, f, ensure_ascii=False, indent=2)
                
                self.logger.info(f"Backup completed: {backed_up_files} files backed up to {backup_dir}")
            else:
                # 空のバックアップディレクトリを削除
                shutil.rmtree(backup_dir)
                self.logger.info("No files to backup")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during backup: {e}")
            return False
    
    def auto_commit_push(self, custom_message: Optional[str] = None) -> bool:
        """自動コミット・プッシュ（研究プロジェクト用）"""
        try:
            # 変更ファイル確認
            changed_files = self.get_changed_files()
            
            if not changed_files:
                self.logger.info("No research files to commit")
                return True
            
            self.logger.info(f"Found {len(changed_files)} changed research files")
            for file in changed_files:
                self.logger.info(f"  - {file}")
            
            # 変更内容分析
            analysis = self.analyze_changes(changed_files)
            
            # バックアップ実行
            self.auto_backup()
            
            # ファイル追加
            success, _, _ = self.run_git_command(['git', 'add', '.'])
            if not success:
                self.logger.error("Failed to add files")
                return False
            
            # コミットメッセージ生成
            if custom_message:
                commit_message = f"{custom_message}\n\n🚀 Generated with [Claude Code](https://claude.ai/code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
            else:
                commit_message = self.generate_research_commit_message(changed_files, analysis)
            
            # コミット
            success, stdout, stderr = self.run_git_command(['git', 'commit', '-m', commit_message])
            if not success:
                if "nothing to commit" in stderr:
                    self.logger.info("Nothing to commit")
                    return True
                else:
                    self.logger.error("Failed to commit")
                    return False
            
            # コミットハッシュ取得
            commit_hash = None
            success, stdout, _ = self.run_git_command(['git', 'rev-parse', 'HEAD'])
            if success:
                commit_hash = stdout[:8]  # 短縮ハッシュ
            
            # 実験ログ記録
            self.log_experiment(analysis, commit_hash)
            
            # プッシュ
            success, _, stderr = self.run_git_command(['git', 'push', 'origin', 'main'])
            if not success:
                # masterブランチを試す
                success, _, _ = self.run_git_command(['git', 'push', 'origin', 'master'])
                if not success:
                    # 初回プッシュの場合
                    success, _, _ = self.run_git_command(['git', 'push', '-u', 'origin', 'main'])
                    if not success:
                        success, _, _ = self.run_git_command(['git', 'push', '-u', 'origin', 'master'])
            
            if success:
                self.logger.info(f"Successfully committed and pushed research changes (commit: {commit_hash})")
                
                # 通知送信（設定されている場合）
                if self.config.ENABLE_NOTIFICATIONS:
                    self.send_notification(analysis, commit_hash)
                
                return True
            else:
                self.logger.error("Failed to push changes")
                return False
            
        except Exception as e:
            self.logger.error(f"Error in auto commit/push: {e}")
            return False
    
    def send_notification(self, analysis: Dict[str, Any], commit_hash: str = None):
        """通知送信（Slack/Discord等）"""
        if not self.config.NOTIFICATION_WEBHOOK:
            return
        
        try:
            import requests
            
            message = f"""
🔬 研究プロジェクト更新通知

📂 プロジェクト: {self.config.PROJECT_NAME}
🎯 活動: {analysis['research_activity']}
💾 コミット: {commit_hash or 'unknown'}
📅 時刻: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

変更内容:
• コード: {len(analysis['code_files'])}ファイル
• ノートブック: {len(analysis['notebook_files'])}ファイル
• データ: {len(analysis['data_files'])}ファイル
• 結果: {len(analysis['result_files'])}ファイル
"""
            
            payload = {'text': message}
            response = requests.post(self.config.NOTIFICATION_WEBHOOK, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("Notification sent successfully")
            else:
                self.logger.warning(f"Notification failed: {response.status_code}")
                
        except Exception as e:
            self.logger.warning(f"Failed to send notification: {e}")
    
    def show_research_status(self):
        """研究プロジェクトの状態表示"""
        try:
            print("🔬 研究プロジェクト状態")
            print("=" * 50)
            
            # プロジェクト情報
            print(f"📂 プロジェクト: {self.config.PROJECT_NAME}")
            print(f"🏛️ 所属機関: {self.config.RESEARCH_INSTITUTION}")
            print(f"👨‍🔬 研究者: {self.config.RESEARCHER_NAME}")
            print()
            
            # Git情報
            success, stdout, _ = self.run_git_command(['git', 'branch', '--show-current'])
            if success:
                print(f"🌿 現在のブランチ: {stdout}")
            
            success, stdout, _ = self.run_git_command(['git', 'remote', 'get-url', 'origin'])
            if success:
                # URLからトークンを除去して表示
                clean_url = re.sub(r'https://[^@]+@', 'https://', stdout)
                print(f"🔗 リモートリポジトリ: {clean_url}")
            
            # 変更ファイル
            changed_files = self.get_changed_files()
            if changed_files:
                print(f"\n📝 変更ファイル数: {len(changed_files)}")
                analysis = self.analyze_changes(changed_files)
                print(f"🎯 推定活動: {analysis['research_activity']}")
                
                if analysis['code_files']:
                    print(f"  💻 コード: {len(analysis['code_files'])}ファイル")
                if analysis['notebook_files']:
                    print(f"  📔 ノートブック: {len(analysis['notebook_files'])}ファイル")
                if analysis['data_files']:
                    print(f"  📊 データ: {len(analysis['data_files'])}ファイル")
                if analysis['result_files']:
                    print(f"  📈 結果: {len(analysis['result_files'])}ファイル")
            else:
                print("\n📝 変更ファイル: なし")
            
            # 実験履歴
            if self.experiment_log.exists():
                try:
                    with open(self.experiment_log, 'r', encoding='utf-8') as f:
                        experiments = json.load(f)
                    
                    print(f"\n🧪 実験履歴: {len(experiments)}回")
                    if experiments:
                        recent = experiments[-1]
                        print(f"  最新: {recent['research_activity']} ({recent['timestamp'][:10]})")
                except:
                    print("\n🧪 実験履歴: 読み込みエラー")
            else:
                print("\n🧪 実験履歴: なし")
            
            # 最新コミット
            success, stdout, _ = self.run_git_command(['git', 'log', '--oneline', '-1'])
            if success:
                print(f"\n💾 最新コミット: {stdout}")
            
        except Exception as e:
            self.logger.error(f"Error showing status: {e}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="Research Project Git Automation")
    parser.add_argument('--setup', action='store_true', help='初期セットアップ実行')
    parser.add_argument('--auto-commit', action='store_true', help='自動コミット・プッシュ実行')
    parser.add_argument('--status', action='store_true', help='プロジェクト状態表示')
    parser.add_argument('--backup', action='store_true', help='手動バックアップ実行')
    parser.add_argument('--message', '-m', type=str, help='カスタムコミットメッセージ')
    parser.add_argument('--path', type=str, default='.', help='プロジェクトパス')
    parser.add_argument('--validate-config', action='store_true', help='設定検証')
    
    args = parser.parse_args()
    
    # 設定検証のみ
    if args.validate_config:
        config.print_config_status()
        return
    
    # ResearchGitAutomation初期化
    try:
        automation = ResearchGitAutomation(args.path)
    except ValueError as e:
        print(f"❌ 設定エラー: {e}")
        print("🔧 config.py ファイルを確認してください")
        sys.exit(1)
    
    try:
        if args.setup:
            print("🚀 研究プロジェクト Git自動化システム セットアップ")
            print("=" * 60)
            
            success = automation.initialize_repository()
            if success:
                print("✅ セットアップ完了!")
                print(f"📂 プロジェクト: {config.PROJECT_NAME}")
                print(f"🔗 リポジトリ: https://github.com/{config.GITHUB_USERNAME}/{config.REPOSITORY_NAME}")
                
                # 初回コミット実行確認
                response = input("\n初回コミットを実行しますか？ (y/N): ")
                if response.lower() in ['y', 'yes']:
                    automation.auto_commit_push("🎉 研究プロジェクト初期セットアップ完了")
            else:
                print("❌ セットアップ失敗")
                sys.exit(1)
        
        elif args.auto_commit:
            success = automation.auto_commit_push(args.message)
            if success:
                print("✅ 自動コミット・プッシュ完了")
            else:
                print("❌ 自動コミット・プッシュ失敗")
                sys.exit(1)
        
        elif args.backup:
            success = automation.auto_backup()
            if success:
                print("✅ バックアップ完了")
            else:
                print("❌ バックアップ失敗")
                sys.exit(1)
        
        elif args.status:
            automation.show_research_status()
        
        else:
            # デフォルト: ヘルプ表示
            parser.print_help()
            print("\n🔬 研究プロジェクト用Git自動化システム")
            print("=" * 40)
            print("使用例:")
            print("  初回セットアップ:        python research_git_automation.py --setup")
            print("  自動コミット・プッシュ:   python research_git_automation.py --auto-commit")
            print("  プロジェクト状態確認:     python research_git_automation.py --status")
            print("  手動バックアップ:        python research_git_automation.py --backup")
            print("  設定検証:              python research_git_automation.py --validate-config")
            print("  カスタムメッセージ:       python research_git_automation.py --auto-commit -m 'メッセージ'")
    
    except KeyboardInterrupt:
        print("\n❌ 処理がキャンセルされました")
        sys.exit(1)
    except Exception as e:
        automation.logger.error(f"Unexpected error: {e}")
        print(f"❌ 予期しないエラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()