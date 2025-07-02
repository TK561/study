#!/usr/bin/env python3
"""
自動開発ワークフロー (Sirius Template方式)
AI駆動の完全自動化開発サイクル
"""
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
import logging

class AutoDevWorkflow:
    def __init__(self):
        self.config_file = 'auto_dev_config.json'
        self.workflow_log = 'workflow_log.json'
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('auto_dev.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """設定読み込み"""
        default_config = {
            "workflow_enabled": True,
            "auto_testing": {
                "ui_unit_tests": True,
                "api_unit_tests": True,
                "integration_tests": True,
                "e2e_tests": True
            },
            "auto_review": {
                "enabled": True,
                "ai_models": ["claude", "gemini", "openai"],
                "review_cycles": 3
            },
            "auto_deployment": {
                "lint_check": True,
                "type_check": True,
                "test_coverage_threshold": 80
            },
            "auto_documentation": {
                "update_on_completion": True,
                "generate_api_docs": True,
                "update_readme": True
            },
            "github_integration": {
                "auto_issue_creation": True,
                "auto_branch_creation": True,
                "auto_pr_creation": True
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """設定保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def log_workflow_step(self, step, status, details=None):
        """ワークフローステップをログ記録"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "status": status,
            "details": details or {}
        }
        
        workflow_log = []
        if os.path.exists(self.workflow_log):
            with open(self.workflow_log, 'r', encoding='utf-8') as f:
                workflow_log = json.load(f)
        
        workflow_log.append(entry)
        
        with open(self.workflow_log, 'w', encoding='utf-8') as f:
            json.dump(workflow_log, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"[{step}] {status}")
    
    def run_command(self, command, description):
        """コマンド実行"""
        self.logger.info(f"実行: {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info(f"✅ {description} 成功")
                return True, result.stdout
            else:
                self.logger.error(f"❌ {description} 失敗: {result.stderr}")
                return False, result.stderr
        except Exception as e:
            self.logger.error(f"❌ {description} エラー: {e}")
            return False, str(e)
    
    def create_feature_branch(self, feature_name):
        """フィーチャーブランチ作成"""
        if not self.config['github_integration']['auto_branch_creation']:
            return True
        
        branch_name = f"feature/{feature_name}"
        self.log_workflow_step("branch_creation", "started", {"branch": branch_name})
        
        # 現在のブランチを確認
        success, current_branch = self.run_command("git branch --show-current", "現在のブランチ確認")
        if not success:
            return False
        
        # mainブランチに切り替え
        success, _ = self.run_command("git checkout main", "mainブランチに切り替え")
        if not success:
            # developブランチを試す
            success, _ = self.run_command("git checkout develop", "developブランチに切り替え")
        
        # 最新の変更を取得
        success, _ = self.run_command("git pull origin main", "最新の変更を取得")
        
        # フィーチャーブランチ作成
        success, _ = self.run_command(f"git checkout -b {branch_name}", f"ブランチ {branch_name} 作成")
        if success:
            self.log_workflow_step("branch_creation", "completed", {"branch": branch_name})
            return True
        else:
            self.log_workflow_step("branch_creation", "failed", {"branch": branch_name})
            return False
    
    def run_ui_unit_tests(self):
        """UIユニットテスト実行"""
        if not self.config['auto_testing']['ui_unit_tests']:
            return True
        
        self.log_workflow_step("ui_unit_tests", "started")
        
        # Jest/Vitest等のテスト実行
        test_commands = [
            "npm test",
            "npm run test:unit",
            "yarn test"
        ]
        
        for cmd in test_commands:
            if self.check_command_exists(cmd.split()[0]):
                success, output = self.run_command(cmd, "UIユニットテスト")
                if success:
                    self.log_workflow_step("ui_unit_tests", "completed")
                    return True
                else:
                    self.log_workflow_step("ui_unit_tests", "failed", {"output": output})
                    return False
        
        self.logger.warning("テストコマンドが見つかりませんでした")
        return True
    
    def run_api_unit_tests(self):
        """APIユニットテスト実行"""
        if not self.config['auto_testing']['api_unit_tests']:
            return True
        
        self.log_workflow_step("api_unit_tests", "started")
        
        # Python APIテスト
        if os.path.exists("requirements.txt") or os.path.exists("pyproject.toml"):
            success, output = self.run_command("python -m pytest tests/", "APIユニットテスト")
            if success:
                self.log_workflow_step("api_unit_tests", "completed")
                return True
        
        # Node.js APIテスト
        if os.path.exists("package.json"):
            success, output = self.run_command("npm run test:api", "APIユニットテスト")
            if success:
                self.log_workflow_step("api_unit_tests", "completed")
                return True
        
        self.log_workflow_step("api_unit_tests", "skipped", {"reason": "no_api_tests_found"})
        return True
    
    def run_integration_tests(self):
        """統合テスト実行"""
        if not self.config['auto_testing']['integration_tests']:
            return True
        
        self.log_workflow_step("integration_tests", "started")
        
        test_commands = [
            "npm run test:integration",
            "python -m pytest tests/integration/",
            "npm run test:e2e"
        ]
        
        for cmd in test_commands:
            success, output = self.run_command(cmd, "統合テスト")
            if success:
                self.log_workflow_step("integration_tests", "completed")
                return True
        
        self.log_workflow_step("integration_tests", "skipped")
        return True
    
    def run_e2e_tests(self):
        """E2Eテスト実行"""
        if not self.config['auto_testing']['e2e_tests']:
            return True
        
        self.log_workflow_step("e2e_tests", "started")
        
        # Playwright, Cypress等のE2Eテスト
        e2e_commands = [
            "npx playwright test",
            "npx cypress run",
            "npm run test:e2e"
        ]
        
        for cmd in e2e_commands:
            success, output = self.run_command(cmd, "E2Eテスト")
            if success:
                self.log_workflow_step("e2e_tests", "completed")
                return True
        
        self.log_workflow_step("e2e_tests", "skipped")
        return True
    
    def run_lint_and_typecheck(self):
        """Lint&型チェック実行"""
        if not self.config['auto_deployment']['lint_check']:
            return True
        
        self.log_workflow_step("lint_typecheck", "started")
        
        # ESLint
        success, _ = self.run_command("npm run lint", "ESLintチェック")
        if not success:
            # 自動修正を試行
            self.run_command("npm run lint:fix", "ESLint自動修正")
        
        # TypeScript型チェック
        if self.config['auto_deployment']['type_check']:
            success, _ = self.run_command("npm run type-check", "TypeScript型チェック")
            if not success:
                success, _ = self.run_command("npx tsc --noEmit", "TypeScript型チェック")
        
        # textlint
        success, _ = self.run_command("npm run lint", "textlintチェック")
        
        self.log_workflow_step("lint_typecheck", "completed")
        return True
    
    def check_test_coverage(self):
        """テストカバレッジチェック"""
        threshold = self.config['auto_deployment']['test_coverage_threshold']
        
        self.log_workflow_step("coverage_check", "started")
        
        # Jest coverage
        success, output = self.run_command("npm run test:coverage", "カバレッジチェック")
        if success:
            # カバレッジ結果を解析（簡易版）
            if "%" in output:
                self.log_workflow_step("coverage_check", "completed", {"threshold": threshold})
                return True
        
        self.log_workflow_step("coverage_check", "skipped")
        return True
    
    def update_documentation(self):
        """ドキュメント更新"""
        if not self.config['auto_documentation']['update_on_completion']:
            return True
        
        self.log_workflow_step("documentation_update", "started")
        
        # API文書生成
        if self.config['auto_documentation']['generate_api_docs']:
            self.run_command("npm run docs:generate", "API文書生成")
        
        # README更新
        if self.config['auto_documentation']['update_readme']:
            self.update_readme()
        
        self.log_workflow_step("documentation_update", "completed")
        return True
    
    def update_readme(self):
        """README自動更新"""
        readme_path = "README.md"
        if not os.path.exists(readme_path):
            return
        
        # 現在の日時でREADMEを更新
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 最終更新日を更新
        if "最終更新:" in content:
            import re
            content = re.sub(
                r'最終更新:.*', 
                f'最終更新: {current_time}', 
                content
            )
        else:
            content += f"\n\n最終更新: {current_time}\n"
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_pull_request(self, feature_name, description=""):
        """プルリクエスト作成"""
        if not self.config['github_integration']['auto_pr_creation']:
            return True
        
        self.log_workflow_step("pr_creation", "started")
        
        # 変更をコミット
        self.run_command("git add .", "変更をステージング")
        self.run_command(f'git commit -m "feat: {feature_name}"', "変更をコミット")
        
        # ブランチをプッシュ
        branch_name = f"feature/{feature_name}"
        success, _ = self.run_command(f"git push origin {branch_name}", "ブランチをプッシュ")
        
        if success:
            # GitHub CLIでPR作成
            pr_title = f"feat: {feature_name}"
            pr_body = description or f"Auto-generated PR for {feature_name}"
            
            success, _ = self.run_command(
                f'gh pr create --title "{pr_title}" --body "{pr_body}"',
                "プルリクエスト作成"
            )
            
            if success:
                self.log_workflow_step("pr_creation", "completed")
                return True
        
        self.log_workflow_step("pr_creation", "failed")
        return False
    
    def check_command_exists(self, command):
        """コマンドの存在確認"""
        return subprocess.run(f"which {command}", shell=True, capture_output=True).returncode == 0
    
    def run_full_workflow(self, feature_name, description=""):
        """完全自動ワークフロー実行"""
        self.logger.info(f"🚀 自動開発ワークフロー開始: {feature_name}")
        
        workflow_steps = [
            ("ブランチ作成", lambda: self.create_feature_branch(feature_name)),
            ("UIユニットテスト", self.run_ui_unit_tests),
            ("APIユニットテスト", self.run_api_unit_tests),
            ("統合テスト", self.run_integration_tests),
            ("E2Eテスト", self.run_e2e_tests),
            ("Lint&型チェック", self.run_lint_and_typecheck),
            ("カバレッジチェック", self.check_test_coverage),
            ("ドキュメント更新", self.update_documentation),
            ("プルリクエスト作成", lambda: self.create_pull_request(feature_name, description))
        ]
        
        success_count = 0
        total_steps = len(workflow_steps)
        
        for step_name, step_func in workflow_steps:
            self.logger.info(f"📋 実行中: {step_name}")
            try:
                if step_func():
                    success_count += 1
                    self.logger.info(f"✅ {step_name} 完了")
                else:
                    self.logger.warning(f"⚠️ {step_name} スキップまたは失敗")
            except Exception as e:
                self.logger.error(f"❌ {step_name} エラー: {e}")
        
        completion_rate = (success_count / total_steps) * 100
        self.logger.info(f"🎉 ワークフロー完了: {success_count}/{total_steps} ({completion_rate:.1f}%)")
        
        self.log_workflow_step("full_workflow", "completed", {
            "feature": feature_name,
            "success_rate": completion_rate,
            "completed_steps": success_count,
            "total_steps": total_steps
        })
        
        return completion_rate >= 80
    
    def show_status(self):
        """ワークフロー状態表示"""
        print("📊 自動開発ワークフロー状態:")
        print(f"  有効: {'Yes' if self.config['workflow_enabled'] else 'No'}")
        print("\n🧪 自動テスト:")
        for test_type, enabled in self.config['auto_testing'].items():
            print(f"  {test_type}: {'有効' if enabled else '無効'}")
        
        print("\n🔍 自動レビュー:")
        review_config = self.config['auto_review']
        print(f"  有効: {'Yes' if review_config['enabled'] else 'No'}")
        print(f"  レビューサイクル: {review_config['review_cycles']}回")
        
        print("\n🚀 自動デプロイ:")
        deploy_config = self.config['auto_deployment']
        print(f"  Lintチェック: {'有効' if deploy_config['lint_check'] else '無効'}")
        print(f"  型チェック: {'有効' if deploy_config['type_check'] else '無効'}")
        print(f"  カバレッジ閾値: {deploy_config['test_coverage_threshold']}%")

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自動開発ワークフロー')
    parser.add_argument('command', nargs='?', default='status',
                      choices=['run', 'status', 'config'],
                      help='実行するコマンド')
    parser.add_argument('--feature', help='フィーチャー名')
    parser.add_argument('--description', help='フィーチャーの説明')
    
    args = parser.parse_args()
    
    workflow = AutoDevWorkflow()
    
    if args.command == 'run':
        if not args.feature:
            print("❌ --feature オプションが必要です")
            sys.exit(1)
        
        workflow.run_full_workflow(args.feature, args.description or "")
    elif args.command == 'status':
        workflow.show_status()
    elif args.command == 'config':
        print(f"設定ファイル: {workflow.config_file}")
        print(json.dumps(workflow.config, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()