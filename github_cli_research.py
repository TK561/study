#!/usr/bin/env python3
"""
GitHub CLI 研究プロジェクト連携スクリプト
======================================

研究プロジェクトのためのGitHub CLI (gh) ラッパー
Personal Access Token または GitHub CLI 認証を使用
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class GitHubCLIResearch:
    """研究プロジェクト用 GitHub CLI ラッパー"""
    
    def __init__(self):
        self.check_gh_cli()
        self.check_authentication()
        
    def check_gh_cli(self):
        """GitHub CLI インストールチェック"""
        try:
            result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ GitHub CLI: {result.stdout.strip()}")
            else:
                raise Exception("GitHub CLI not found")
        except:
            print("❌ GitHub CLI がインストールされていません")
            print("📥 インストール方法:")
            print("   Windows: winget install --id GitHub.cli")
            print("   macOS: brew install gh")
            print("   Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md")
            sys.exit(1)
    
    def check_authentication(self):
        """認証状態チェック"""
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI が認証されていません")
            print("🔐 認証方法:")
            print("   gh auth login")
            print("   または")
            print("   export GH_TOKEN=your_personal_access_token")
            sys.exit(1)
        print("✅ GitHub CLI 認証済み")
    
    def run_gh_command(self, args: List[str]) -> Tuple[bool, str]:
        """GitHub CLI コマンド実行"""
        try:
            result = subprocess.run(['gh'] + args, capture_output=True, text=True, check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def create_repository(self, name: str, description: str, private: bool = False):
        """リポジトリ作成"""
        print(f"\n📁 リポジトリ作成: {name}")
        
        args = ['repo', 'create', name]
        if private:
            args.append('--private')
        else:
            args.append('--public')
        
        args.extend(['--description', description])
        args.append('--clone')
        
        success, output = self.run_gh_command(args)
        if success:
            print(f"✅ リポジトリ作成完了: {name}")
            print(f"📂 ローカルにクローン済み")
        else:
            print(f"❌ エラー: {output}")
    
    def setup_research_repo(self, repo_name: str):
        """研究リポジトリのセットアップ"""
        print(f"\n🔬 研究リポジトリセットアップ: {repo_name}")
        
        # 基本的な研究プロジェクト構造を作成
        dirs = ['data', 'notebooks', 'src', 'results', 'docs', 'tests']
        
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)
            gitkeep = Path(dir_name) / '.gitkeep'
            gitkeep.touch()
        
        # README.md 作成
        readme_content = f"""# {repo_name}

研究プロジェクトリポジトリ

## 📁 構造

- `data/` - 研究データ
- `notebooks/` - Jupyter Notebooks
- `src/` - ソースコード
- `results/` - 実験結果
- `docs/` - ドキュメント
- `tests/` - テストコード

## 🚀 使用方法

```bash
# 環境構築
pip install -r requirements.txt

# 実行
python main.py
```

---
*Generated with Claude Code*
"""
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 初期コミット
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', '🎉 Initial research project setup'])
        subprocess.run(['git', 'push'])
        
        print("✅ 研究リポジトリセットアップ完了")
    
    def create_issue(self, title: str, body: str, labels: List[str] = None):
        """Issue 作成"""
        print(f"\n📋 Issue 作成: {title}")
        
        args = ['issue', 'create', '--title', title, '--body', body]
        
        if labels:
            args.extend(['--label', ','.join(labels)])
        
        success, output = self.run_gh_command(args)
        if success:
            print(f"✅ Issue 作成完了")
            print(f"🔗 {output.strip()}")
        else:
            print(f"❌ エラー: {output}")
    
    def create_research_pr(self, title: str, experiment_details: str):
        """研究用 Pull Request 作成"""
        print(f"\n🔬 研究 PR 作成: {title}")
        
        body = f"""## 🧪 実験概要

{experiment_details}

## 📊 結果

- [ ] 実験完了
- [ ] 結果分析完了
- [ ] ドキュメント更新

## 📝 変更内容

- 新しい実験手法の実装
- データ処理の改善
- 結果の可視化

---
*Generated with Claude Code*
"""
        
        args = ['pr', 'create', '--title', title, '--body', body, '--draft']
        
        success, output = self.run_gh_command(args)
        if success:
            print(f"✅ PR 作成完了")
            print(f"🔗 {output.strip()}")
        else:
            print(f"❌ エラー: {output}")
    
    def list_workflows(self):
        """ワークフロー一覧表示"""
        print("\n📋 GitHub Actions ワークフロー一覧")
        
        success, output = self.run_gh_command(['workflow', 'list'])
        if success:
            print(output)
        else:
            print(f"❌ エラー: {output}")
    
    def run_workflow(self, workflow_name: str):
        """ワークフロー実行"""
        print(f"\n🚀 ワークフロー実行: {workflow_name}")
        
        args = ['workflow', 'run', workflow_name]
        
        success, output = self.run_gh_command(args)
        if success:
            print(f"✅ ワークフロー開始")
            
            # 実行状態確認
            self.view_workflow_runs(workflow_name, limit=1)
        else:
            print(f"❌ エラー: {output}")
    
    def view_workflow_runs(self, workflow_name: str = None, limit: int = 5):
        """ワークフロー実行履歴表示"""
        print(f"\n📊 ワークフロー実行履歴")
        
        args = ['run', 'list']
        if workflow_name:
            args.extend(['--workflow', workflow_name])
        args.extend(['--limit', str(limit)])
        
        success, output = self.run_gh_command(args)
        if success:
            print(output)
        else:
            print(f"❌ エラー: {output}")
    
    def create_release(self, tag: str, title: str, notes: str):
        """リリース作成"""
        print(f"\n📦 リリース作成: {tag}")
        
        args = ['release', 'create', tag, '--title', title, '--notes', notes]
        
        success, output = self.run_gh_command(args)
        if success:
            print(f"✅ リリース作成完了")
            print(f"🔗 {output.strip()}")
        else:
            print(f"❌ エラー: {output}")
    
    def clone_repo(self, repo: str):
        """リポジトリクローン"""
        print(f"\n📥 リポジトリクローン: {repo}")
        
        success, output = self.run_gh_command(['repo', 'clone', repo])
        if success:
            print(f"✅ クローン完了")
        else:
            print(f"❌ エラー: {output}")
    
    def view_repo_info(self, repo: str = None):
        """リポジトリ情報表示"""
        print(f"\n📊 リポジトリ情報")
        
        args = ['repo', 'view']
        if repo:
            args.append(repo)
        
        success, output = self.run_gh_command(args)
        if success:
            print(output)
        else:
            print(f"❌ エラー: {output}")
    
    def sync_fork(self):
        """フォークの同期"""
        print("\n🔄 フォーク同期")
        
        success, output = self.run_gh_command(['repo', 'sync'])
        if success:
            print(f"✅ 同期完了")
        else:
            print(f"❌ エラー: {output}")
    
    def setup_secrets(self, secret_name: str, secret_value: str):
        """シークレット設定"""
        print(f"\n🔐 シークレット設定: {secret_name}")
        
        args = ['secret', 'set', secret_name, '--body', secret_value]
        
        success, output = self.run_gh_command(args)
        if success:
            print(f"✅ シークレット設定完了")
        else:
            print(f"❌ エラー: {output}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="GitHub CLI 研究プロジェクト連携")
    
    subparsers = parser.add_subparsers(dest='command', help='コマンド')
    
    # repo create
    repo_create = subparsers.add_parser('repo-create', help='リポジトリ作成')
    repo_create.add_argument('name', help='リポジトリ名')
    repo_create.add_argument('--description', '-d', default='Research project', help='説明')
    repo_create.add_argument('--private', action='store_true', help='プライベートリポジトリ')
    
    # repo setup
    repo_setup = subparsers.add_parser('repo-setup', help='研究リポジトリセットアップ')
    repo_setup.add_argument('name', help='リポジトリ名')
    
    # issue create
    issue_create = subparsers.add_parser('issue', help='Issue作成')
    issue_create.add_argument('title', help='タイトル')
    issue_create.add_argument('--body', '-b', default='', help='本文')
    issue_create.add_argument('--labels', '-l', nargs='+', help='ラベル')
    
    # pr create
    pr_create = subparsers.add_parser('pr', help='PR作成')
    pr_create.add_argument('title', help='タイトル')
    pr_create.add_argument('--details', '-d', default='', help='実験詳細')
    
    # workflow
    workflow = subparsers.add_parser('workflow', help='ワークフロー操作')
    workflow.add_argument('action', choices=['list', 'run', 'view'], help='アクション')
    workflow.add_argument('--name', '-n', help='ワークフロー名')
    workflow.add_argument('--limit', '-l', type=int, default=5, help='表示数')
    
    # release
    release = subparsers.add_parser('release', help='リリース作成')
    release.add_argument('tag', help='タグ')
    release.add_argument('--title', '-t', required=True, help='タイトル')
    release.add_argument('--notes', '-n', default='', help='リリースノート')
    
    # clone
    clone = subparsers.add_parser('clone', help='リポジトリクローン')
    clone.add_argument('repo', help='リポジトリ名')
    
    # info
    info = subparsers.add_parser('info', help='リポジトリ情報')
    info.add_argument('--repo', '-r', help='リポジトリ名')
    
    # sync
    sync = subparsers.add_parser('sync', help='フォーク同期')
    
    # secret
    secret = subparsers.add_parser('secret', help='シークレット設定')
    secret.add_argument('name', help='シークレット名')
    secret.add_argument('value', help='シークレット値')
    
    args = parser.parse_args()
    
    # GitHub CLI インスタンス作成
    gh = GitHubCLIResearch()
    
    # コマンド実行
    if args.command == 'repo-create':
        gh.create_repository(args.name, args.description, args.private)
    
    elif args.command == 'repo-setup':
        gh.setup_research_repo(args.name)
    
    elif args.command == 'issue':
        gh.create_issue(args.title, args.body, args.labels)
    
    elif args.command == 'pr':
        gh.create_research_pr(args.title, args.details)
    
    elif args.command == 'workflow':
        if args.action == 'list':
            gh.list_workflows()
        elif args.action == 'run':
            if args.name:
                gh.run_workflow(args.name)
            else:
                print("❌ ワークフロー名を指定してください")
        elif args.action == 'view':
            gh.view_workflow_runs(args.name, args.limit)
    
    elif args.command == 'release':
        gh.create_release(args.tag, args.title, args.notes)
    
    elif args.command == 'clone':
        gh.clone_repo(args.repo)
    
    elif args.command == 'info':
        gh.view_repo_info(args.repo)
    
    elif args.command == 'sync':
        gh.sync_fork()
    
    elif args.command == 'secret':
        gh.setup_secrets(args.name, args.value)
    
    else:
        parser.print_help()
        print("\n📚 使用例:")
        print("  リポジトリ作成:    python github_cli_research.py repo-create my-research")
        print("  Issue作成:        python github_cli_research.py issue '実験結果の分析'")
        print("  PR作成:          python github_cli_research.py pr '新機能追加'")
        print("  ワークフロー実行:  python github_cli_research.py workflow run -n claude-review.yml")
        print("  リポジトリ情報:    python github_cli_research.py info")

if __name__ == "__main__":
    main()