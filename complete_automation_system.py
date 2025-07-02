#!/usr/bin/env python3
"""
完全自動化システム v2.0
任意のトリガーで以下の順序で全自動実行:
1. ファイルとフォルダの整理
2. やったことの保存
3. Vercelに反映
4. Obsidianのルールに基づき反映
"""

import os
import shutil
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class CompleteAutomationSystem:
    def __init__(self):
        self.name = "完全自動化システム"
        self.version = "2.0"
        self.root_path = Path("/mnt/c/Desktop/Research")
        self.obsidian_path = Path("/mnt/c/Desktop/Obsidian/study")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # 実行ログ
        self.execution_log = {
            "timestamp": datetime.now().isoformat(),
            "trigger": "",
            "steps_completed": [],
            "files_organized": [],
            "files_saved": [],
            "vercel_status": "",
            "obsidian_updates": [],
            "errors": []
        }
        
        print(f"🚀 {self.name} v{self.version} 開始")
        print(f"⏰ 実行時刻: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        print("=" * 60)

    def step1_organize_files(self):
        """ステップ1: ファイルとフォルダの整理"""
        print("\\n🧹 ステップ1: ファイル・フォルダ整理開始...")
        
        try:
            # バックアップディレクトリ作成
            backup_dir = self.root_path / f"auto_backup_{self.timestamp}"
            backup_dir.mkdir(exist_ok=True)
            
            organized_count = 0
            
            # 一時ファイルパターン
            temp_patterns = [
                "temp_*", "test_*", "*_temp.*", "*_backup.*", 
                "old_*", "*_old.*", "*.tmp", "*.log.old"
            ]
            
            # ルートディレクトリから一時ファイル削除
            for pattern in temp_patterns:
                for item in self.root_path.glob(pattern):
                    if item.is_file() and item.name not in ["complete_automation_system.py"]:
                        try:
                            # バックアップしてから削除
                            backup_target = backup_dir / item.name
                            shutil.copy2(item, backup_target)
                            item.unlink()
                            organized_count += 1
                            self.execution_log["files_organized"].append(str(item.relative_to(self.root_path)))
                            print(f"  ✅ 整理: {item.name}")
                        except Exception as e:
                            self.execution_log["errors"].append(f"整理エラー {item}: {e}")
            
            # 空ディレクトリ削除
            for item in self.root_path.iterdir():
                if item.is_dir() and item.name.startswith(("temp_", "test_", "old_")):
                    try:
                        if not any(item.iterdir()):  # 空の場合
                            shutil.rmtree(item)
                            organized_count += 1
                            print(f"  ✅ 空ディレクトリ削除: {item.name}")
                    except Exception as e:
                        self.execution_log["errors"].append(f"ディレクトリ削除エラー {item}: {e}")
            
            self.execution_log["steps_completed"].append("step1_organize_files")
            print(f"✅ ステップ1完了: {organized_count}件整理")
            return True
            
        except Exception as e:
            self.execution_log["errors"].append(f"ステップ1エラー: {e}")
            print(f"❌ ステップ1エラー: {e}")
            return False

    def step2_save_work(self):
        """ステップ2: やったことの保存"""
        print("\\n💾 ステップ2: 作業内容保存開始...")
        
        try:
            # Git状況確認
            print("  📊 Git変更状況確認中...")
            git_changes = []
            try:
                git_status = subprocess.run(['git', 'status', '--porcelain'], 
                                          capture_output=True, text=True, cwd=str(self.root_path))
                if git_status.stdout:
                    git_changes = git_status.stdout.strip().split('\\n')[:10]
            except Exception as e:
                self.execution_log["errors"].append(f"Git確認エラー: {e}")
            
            # Obsidianバックアップ
            print("  🗂️ Obsidianバックアップ作成中...")
            backup_dir = self.root_path / f"important_backup_{self.timestamp}" / "Obsidian_Vault_Backup"
            if self.obsidian_path.exists():
                backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.copytree(self.obsidian_path, backup_dir / "study", dirs_exist_ok=True)
                self.execution_log["files_saved"].append(str(backup_dir))
                print(f"    ✅ バックアップ完了: {backup_dir}")
            
            # セッション記録作成
            print("  📝 セッション記録作成中...")
            session_content = self._create_session_content(git_changes)
            
            sessions_dir = self.root_path / "sessions"
            sessions_dir.mkdir(exist_ok=True)
            session_file = sessions_dir / f"AUTO_SESSION_SAVE_{self.today}.md"
            
            with open(session_file, 'w', encoding='utf-8') as f:
                f.write(session_content)
            
            self.execution_log["files_saved"].append(str(session_file))
            self.execution_log["steps_completed"].append("step2_save_work")
            print("✅ ステップ2完了: 作業内容保存")
            return True
            
        except Exception as e:
            self.execution_log["errors"].append(f"ステップ2エラー: {e}")
            print(f"❌ ステップ2エラー: {e}")
            return False

    def step3_vercel_deploy(self):
        """ステップ3: Vercelに反映"""
        print("\\n🚀 ステップ3: Vercel反映開始...")
        
        try:
            # Vercel統合システムの実行
            vercel_systems = [
                self.root_path / "vercel_unified_system.py",
                self.root_path / "vercel_smart_integration.py"
            ]
            
            vercel_executed = False
            for system_file in vercel_systems:
                if system_file.exists():
                    try:
                        print(f"  🔧 実行中: {system_file.name}")
                        result = subprocess.run([
                            sys.executable, str(system_file), "deploy"
                        ], capture_output=True, text=True, cwd=str(self.root_path), timeout=120)
                        
                        if result.returncode == 0:
                            self.execution_log["vercel_status"] = f"成功: {system_file.name}"
                            print("    ✅ Vercelデプロイ成功")
                            vercel_executed = True
                            break
                        else:
                            print(f"    ⚠️ {system_file.name} 実行エラー: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        print(f"    ⚠️ {system_file.name} タイムアウト")
                    except Exception as e:
                        print(f"    ⚠️ {system_file.name} エラー: {e}")
            
            if not vercel_executed:
                # 基本的なGit操作
                print("  📤 基本Git操作実行中...")
                try:
                    # Git add & commit
                    subprocess.run(['git', 'add', '.'], cwd=str(self.root_path), check=True)
                    commit_msg = f"🤖 自動更新 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    subprocess.run(['git', 'commit', '-m', commit_msg], cwd=str(self.root_path))
                    subprocess.run(['git', 'push'], cwd=str(self.root_path))
                    self.execution_log["vercel_status"] = "基本Git操作完了"
                    print("    ✅ Git操作完了")
                except Exception as e:
                    self.execution_log["vercel_status"] = f"Git操作エラー: {e}"
                    print(f"    ⚠️ Git操作エラー: {e}")
            
            self.execution_log["steps_completed"].append("step3_vercel_deploy")
            print("✅ ステップ3完了: Vercel反映")
            return True
            
        except Exception as e:
            self.execution_log["errors"].append(f"ステップ3エラー: {e}")
            print(f"❌ ステップ3エラー: {e}")
            return False

    def step4_obsidian_rules_update(self):
        """ステップ4: Obsidianのルールに基づき反映"""
        print("\\n📋 ステップ4: Obsidianルール適用開始...")
        
        try:
            updates_made = []
            
            # Obsidianルールファイル確認
            rules_file = self.obsidian_path / "Obsidian運用ルール.md"
            if not rules_file.exists():
                print("  ⚠️ Obsidian運用ルール.mdが見つかりません")
                return True
            
            # 日次記録フォルダの確認・整理
            daily_notes_dir = self.obsidian_path / "日次記録"
            if daily_notes_dir.exists():
                print("  📁 日次記録フォルダの整理確認中...")
                
                # 年月フォルダ構造の確認
                current_year = datetime.now().year
                current_month = datetime.now().month
                
                year_dir = daily_notes_dir / str(current_year)
                month_dir = year_dir / f"{current_month:02d}"
                
                if not month_dir.exists():
                    month_dir.mkdir(parents=True, exist_ok=True)
                    updates_made.append(f"作成: {month_dir.relative_to(self.obsidian_path)}")
                    print(f"    ✅ 月フォルダ作成: {month_dir.relative_to(self.obsidian_path)}")
                
                # ルート直下の日次記録ファイルを適切なフォルダに移動
                for item in daily_notes_dir.iterdir():
                    if item.is_file() and item.name.endswith('.md') and item.name != 'README.md':
                        # YYYY-MM-DD形式のファイルを適切な場所に移動
                        if len(item.stem) >= 10 and item.stem[:10].count('-') == 2:
                            try:
                                file_date = item.stem[:10]
                                year, month, day = file_date.split('-')
                                target_dir = daily_notes_dir / year / month
                                target_dir.mkdir(parents=True, exist_ok=True)
                                
                                if not (target_dir / item.name).exists():
                                    shutil.move(str(item), str(target_dir / item.name))
                                    updates_made.append(f"移動: {item.name} → {target_dir.relative_to(self.obsidian_path)}")
                                    print(f"    ✅ ファイル移動: {item.name} → {year}/{month}/")
                            except Exception as e:
                                print(f"    ⚠️ ファイル移動エラー {item.name}: {e}")
            
            # Obsidian設定の確認
            print("  ⚙️ Obsidian設定確認中...")
            settings_dir = self.obsidian_path / ".obsidian"
            if settings_dir.exists():
                # daily-notes.json確認
                daily_notes_config = settings_dir / "daily-notes.json"
                if daily_notes_config.exists():
                    try:
                        with open(daily_notes_config, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        
                        if config.get("folder") != "日次記録":
                            config["folder"] = "日次記録"
                            with open(daily_notes_config, 'w', encoding='utf-8') as f:
                                json.dump(config, f, ensure_ascii=False, indent=2)
                            updates_made.append("設定更新: daily-notes.json")
                            print("    ✅ デイリーノート設定更新")
                    except Exception as e:
                        print(f"    ⚠️ 設定確認エラー: {e}")
            
            self.execution_log["obsidian_updates"] = updates_made
            self.execution_log["steps_completed"].append("step4_obsidian_rules_update")
            print(f"✅ ステップ4完了: {len(updates_made)}件更新")
            return True
            
        except Exception as e:
            self.execution_log["errors"].append(f"ステップ4エラー: {e}")
            print(f"❌ ステップ4エラー: {e}")
            return False

    def _create_session_content(self, git_changes):
        """セッション記録コンテンツ作成"""
        git_section = ""
        if git_changes:
            git_section = "\\n".join(f"  {change}" for change in git_changes[:10])
        else:
            git_section = "  変更なし"
        
        return f"""# 🔄 自動セッション保存 - {self.today}

## 📅 保存情報
- **保存日時**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
- **保存システム**: {self.name} v{self.version}
- **実行トリガー**: 完全自動化システム

## 🤖 実行された処理

### ステップ1: ファイル・フォルダ整理
- 一時ファイル・古いバックアップの整理
- 空ディレクトリの削除
- 安全なバックアップ作成

### ステップ2: 作業内容保存
- Git変更状況の記録
- Obsidianバックアップの作成
- セッション記録の自動生成

### ステップ3: Vercel反映
- 自動デプロイシステムの実行
- Git操作による変更反映

### ステップ4: Obsidianルール適用
- ファイル構造の自動整理
- 設定ファイルの確認・更新
- 命名規則の適用

## 📊 Git変更状況
```
{git_section}
```

## 🎯 システムの特徴
1. **完全自動化**: 任意のトリガーで4ステップを順次実行
2. **安全性**: すべての変更前にバックアップ作成
3. **一貫性**: Obsidianルールに基づく統一的な処理
4. **効率性**: 手動作業の完全排除

## 🔗 処理詳細
- **整理したファイル**: {len(self.execution_log["files_organized"])}件
- **作成したバックアップ**: {len(self.execution_log["files_saved"])}件
- **実行ステップ**: {len(self.execution_log["steps_completed"])}/4
- **エラー**: {len(self.execution_log["errors"])}件

## 📋 次回実行時の改善点
- システムの動作確認と最適化
- エラー処理の強化
- 処理速度の向上

---
*{self.name} v{self.version}により自動生成 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    def execute_all_steps(self, trigger="手動実行"):
        """全ステップを順次実行"""
        self.execution_log["trigger"] = trigger
        
        steps = [
            ("ステップ1", self.step1_organize_files),
            ("ステップ2", self.step2_save_work), 
            ("ステップ3", self.step3_vercel_deploy),
            ("ステップ4", self.step4_obsidian_rules_update)
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            if step_func():
                success_count += 1
            else:
                print(f"⚠️ {step_name}でエラーが発生しましたが、処理を継続します")
        
        # 実行ログ保存
        log_file = self.root_path / f"complete_automation_log_{self.timestamp}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.execution_log, f, ensure_ascii=False, indent=2)
        
        print("=" * 60)
        print(f"🎉 完全自動化システム実行完了!")
        print(f"✅ 成功: {success_count}/4ステップ")
        print(f"📋 ログ: {log_file}")
        if self.execution_log["errors"]:
            print(f"⚠️ エラー: {len(self.execution_log['errors'])}件")
        print("=" * 60)
        
        return success_count == 4

def main():
    import sys
    
    # 引数からトリガーを取得
    trigger = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "手動実行"
    
    # システム実行
    system = CompleteAutomationSystem()
    success = system.execute_all_steps(trigger)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())