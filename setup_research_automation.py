#!/usr/bin/env python3
"""
研究プロジェクト自動化セットアップスクリプト
=======================================

このスクリプトは研究プロジェクトのGitHub自動化システムを
一括でセットアップするためのヘルパースクリプトです。

機能:
1. 設定ファイルの準備と検証
2. Git リポジトリの初期化
3. GitHub Actions ワークフローの設定
4. VS Code タスクの設定
5. 研究プロジェクト構造の作成
6. 初回コミット・プッシュ
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json

def print_header(title: str):
    """ヘッダー表示"""
    print(f"\n{'='*60}")
    print(f"🔬 {title}")
    print('='*60)

def print_step(step: str):
    """ステップ表示"""
    print(f"\n📋 {step}")
    print("-" * 40)

def run_command(command: list, description: str = "") -> bool:
    """コマンド実行"""
    if description:
        print(f"▶️ {description}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_prerequisites():
    """前提条件チェック"""
    print_step("前提条件チェック")
    
    # Python バージョンチェック
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8以上が必要です")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Git チェック
    if not run_command(['git', '--version'], "Git version check"):
        print("❌ Gitがインストールされていません")
        return False
    
    # 必要なPythonパッケージチェック
    required_packages = ['requests']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} package available")
        except ImportError:
            print(f"⚠️ {package} package not found, will install")
            if not run_command([sys.executable, '-m', 'pip', 'install', package], f"Installing {package}"):
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def setup_config_file():
    """設定ファイルのセットアップ"""
    print_step("設定ファイルセットアップ")
    
    config_file = Path('config.py')
    example_file = Path('config.example.py')
    
    if config_file.exists():
        print("✅ config.py already exists")
        return True
    
    if not example_file.exists():
        print("❌ config.example.py not found")
        return False
    
    # config.py をテンプレートから作成
    try:
        shutil.copy(example_file, config_file)
        print("✅ config.py created from template")
        print("📝 Please edit config.py with your actual values:")
        print("   - GITHUB_TOKEN")
        print("   - GITHUB_USERNAME") 
        print("   - REPOSITORY_NAME")
        print("   - GITHUB_EMAIL")
        print("   - ANTHROPIC_API_KEY (optional)")
        print("   - RESEARCH_INSTITUTION")
        print("   - RESEARCHER_NAME")
        
        response = input("\n設定完了後、Enterキーを押してください...")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create config.py: {e}")
        return False

def validate_config():
    """設定検証"""
    print_step("設定検証")
    
    try:
        import config
        errors, warnings = config.validate_config()
        
        if errors:
            print("❌ 設定エラー:")
            for error in errors:
                print(f"   {error}")
            return False
        
        if warnings:
            print("⚠️ 設定警告:")
            for warning in warnings:
                print(f"   {warning}")
        
        print("✅ 設定検証完了")
        return True
        
    except ImportError:
        print("❌ config.py が読み込めません")
        return False
    except Exception as e:
        print(f"❌ 設定検証エラー: {e}")
        return False

def initialize_git_repo():
    """Git リポジトリ初期化"""
    print_step("Git リポジトリ初期化")
    
    # 研究自動化スクリプト実行
    if not run_command([sys.executable, 'research_git_automation.py', '--setup'], 
                       "Initializing research Git automation"):
        print("❌ Research automation setup failed")
        return False
    
    print("✅ Git repository initialized with research automation")
    return True

def setup_github_actions():
    """GitHub Actions セットアップ"""
    print_step("GitHub Actions セットアップ")
    
    workflows_dir = Path('.github/workflows')
    
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    required_workflows = [
        'claude-review.yml'
    ]
    
    missing_workflows = []
    for workflow in required_workflows:
        workflow_path = workflows_dir / workflow
        if workflow_path.exists():
            print(f"✅ {workflow} exists")
        else:
            missing_workflows.append(workflow)
    
    if missing_workflows:
        print(f"❌ Missing workflows: {missing_workflows}")
        return False
    
    print("✅ GitHub Actions workflows configured")
    return True

def setup_vscode_integration():
    """VS Code 統合セットアップ"""
    print_step("VS Code 統合セットアップ")
    
    vscode_dir = Path('.vscode')
    
    if not vscode_dir.exists():
        print("❌ .vscode directory not found")
        return False
    
    required_files = ['tasks.json']
    
    for file in required_files:
        file_path = vscode_dir / file
        if file_path.exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    print("✅ VS Code integration configured")
    print("📱 Available VS Code tasks:")
    print("   - Ctrl+Shift+P → 'Tasks: Run Task' → '🚀 Research Commit: Auto Commit & Push'")
    print("   - Ctrl+Shift+P → 'Tasks: Run Task' → '📊 Research Status: Project Overview'")
    print("   - Ctrl+Shift+P → 'Tasks: Run Task' → '🔄 Full Research Workflow'")
    
    return True

def create_initial_structure():
    """初期プロジェクト構造作成"""
    print_step("研究プロジェクト構造作成")
    
    try:
        import config
        
        # データ構造作成
        for name, path in config.DATA_STRUCTURE.items():
            dir_path = Path(path)
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # .gitkeep ファイル作成
            gitkeep = dir_path / '.gitkeep'
            if not gitkeep.exists():
                gitkeep.touch()
            
            print(f"✅ Created: {path}")
        
        # README.md の更新
        readme_path = Path('README.md')
        if readme_path.exists():
            print("✅ README.md already exists")
        else:
            # 基本的なREADME作成
            readme_content = f"""# {config.PROJECT_NAME}

{config.PROJECT_DESCRIPTION}

## 🎯 プロジェクト概要

**研究機関**: {config.RESEARCH_INSTITUTION}
**研究者**: {config.RESEARCHER_NAME}

## 🚀 使用方法

### 環境構築
```bash
pip install -r requirements.txt
```

### メインシステム実行
```bash
python semantic_classification_system.py
```

### 研究自動化
```bash
# 自動コミット・プッシュ
python research_git_automation.py --auto-commit

# プロジェクト状態確認
python research_git_automation.py --status
```

## 📁 プロジェクト構造

- `data/`: 研究データ
- `notebooks/`: Jupyter Notebook
- `results/`: 実験結果
- `figures/`: グラフ・図表
- `docs/`: ドキュメント

## 🔬 研究ガイドライン

詳細は [CLAUDE.md](CLAUDE.md) を参照してください。

---
*Generated with Claude Code - Research Automation System*
"""
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print("✅ README.md created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating project structure: {e}")
        return False

def perform_initial_commit():
    """初回コミット実行"""
    print_step("初回コミット・プッシュ")
    
    response = input("初回コミット・プッシュを実行しますか？ (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("⏭️ 初回コミットをスキップ")
        return True
    
    commit_message = "🎉 研究プロジェクト自動化システム初期セットアップ完了"
    
    if not run_command([sys.executable, 'research_git_automation.py', '--auto-commit', '-m', commit_message],
                       "Performing initial commit and push"):
        print("❌ Initial commit failed")
        return False
    
    print("✅ Initial commit and push completed")
    return True

def display_final_summary():
    """最終サマリー表示"""
    print_header("セットアップ完了")
    
    try:
        import config
        
        print("🎉 研究プロジェクト自動化システムのセットアップが完了しました！")
        print()
        print(f"📂 プロジェクト: {config.PROJECT_NAME}")
        print(f"🔗 リポジトリ: https://github.com/{config.GITHUB_USERNAME}/{config.REPOSITORY_NAME}")
        print(f"🏛️ 研究機関: {config.RESEARCH_INSTITUTION}")
        print(f"👨‍🔬 研究者: {config.RESEARCHER_NAME}")
        print()
        print("🛠️ 利用可能な機能:")
        print("   ✅ 自動Git管理")
        print("   ✅ GitHub Actions ワークフロー")
        print("   ✅ VS Code タスク統合")
        print("   ✅ 研究データ自動バックアップ")
        print("   ✅ Claude Code 統合")
        print()
        print("🚀 次のステップ:")
        print("   1. VS Code でプロジェクトを開く")
        print("   2. Ctrl+Shift+P → 'Tasks: Run Task' でタスク実行")
        print("   3. semantic_classification_system.py でメインシステム実行")
        print("   4. 研究作業後は自動コミット・プッシュで変更を保存")
        print()
        print("📚 詳細情報:")
        print("   - 研究ガイドライン: CLAUDE.md")
        print("   - 使用方法: README.md")
        print("   - ワークフロー説明: .github/WORKFLOWS_README.md")
        
    except Exception as e:
        print(f"⚠️ サマリー表示エラー: {e}")

def main():
    """メイン関数"""
    print_header("研究プロジェクト自動化システム セットアップ")
    
    print("このスクリプトは以下をセットアップします:")
    print("• 設定ファイルの準備")
    print("• Git リポジトリ初期化")
    print("• GitHub Actions ワークフロー")
    print("• VS Code タスク統合")
    print("• 研究プロジェクト構造")
    print("• 初回コミット・プッシュ")
    
    response = input("\n続行しますか？ (Y/n): ")
    if response.lower() in ['n', 'no']:
        print("セットアップをキャンセルしました")
        return
    
    # セットアップ手順実行
    steps = [
        ("前提条件チェック", check_prerequisites),
        ("設定ファイルセットアップ", setup_config_file),
        ("設定検証", validate_config),
        ("Git リポジトリ初期化", initialize_git_repo),
        ("GitHub Actions セットアップ", setup_github_actions),
        ("VS Code 統合セットアップ", setup_vscode_integration),
        ("研究プロジェクト構造作成", create_initial_structure),
        ("初回コミット・プッシュ", perform_initial_commit)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print(f"\n❌ {step_name} に失敗しました")
                response = input("続行しますか？ (y/N): ")
                if response.lower() not in ['y', 'yes']:
                    break
        except KeyboardInterrupt:
            print("\n\n❌ セットアップがキャンセルされました")
            return
        except Exception as e:
            print(f"\n❌ {step_name} でエラーが発生: {e}")
            response = input("続行しますか？ (y/N): ")
            if response.lower() not in ['y', 'yes']:
                break
    
    # 結果表示
    if success_count == len(steps):
        display_final_summary()
    else:
        print(f"\n⚠️ セットアップが部分的に完了しました ({success_count}/{len(steps)})")
        print("手動で残りの設定を完了してください")

if __name__ == "__main__":
    main()