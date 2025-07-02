#!/usr/bin/env python3
"""
textlint定期実行スケジューラー
指定した時刻に自動的にtextlintチェックを実行
"""
import os
import json
import time
import subprocess
import schedule
from datetime import datetime
import threading
import signal
import sys

class TextlintScheduler:
    def __init__(self):
        self.config_file = 'textlint_scheduler_config.json'
        self.report_dir = 'textlint_reports'
        self.load_config()
        self.running = True
        
    def load_config(self):
        """設定を読み込み"""
        default_config = {
            "enabled": True,
            "schedules": [
                {"time": "09:00", "auto_fix": False, "scope": "all"},
                {"time": "13:00", "auto_fix": False, "scope": "sessions"},
                {"time": "18:00", "auto_fix": True, "scope": "all"}
            ],
            "daily_report": True,
            "report_time": "20:00",
            "notification_email": None,
            "slack_webhook": None
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def ensure_report_dir(self):
        """レポートディレクトリを確保"""
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def run_textlint_check(self, scope="all", auto_fix=False):
        """textlintチェックを実行"""
        print(f"\n🔍 定期チェック開始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  スコープ: {scope}")
        print(f"  自動修正: {'有効' if auto_fix else '無効'}")
        
        # コマンド構築
        cmd = ['npx', 'textlint']
        if auto_fix:
            cmd.append('--fix')
        
        # スコープに応じてファイルパターンを追加
        if scope == "all":
            cmd.extend(['**/*.md', '**/*.txt'])
        elif scope == "sessions":
            cmd.append('sessions/*.md')
        elif scope == "docs":
            cmd.extend(['*.md', 'docs/*.md'])
        else:
            cmd.append(scope)
        
        # フォーマットオプション
        cmd.extend(['--format', 'json'])
        
        try:
            # textlint実行
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # 結果を解析
            if result.stdout:
                try:
                    json_result = json.loads(result.stdout)
                    return self.analyze_results(json_result, scope, auto_fix)
                except json.JSONDecodeError:
                    # JSON以外の出力の場合
                    return {
                        'success': result.returncode == 0,
                        'scope': scope,
                        'auto_fix': auto_fix,
                        'timestamp': datetime.now().isoformat(),
                        'raw_output': result.stdout + result.stderr
                    }
            else:
                return {
                    'success': result.returncode == 0,
                    'scope': scope,
                    'auto_fix': auto_fix,
                    'timestamp': datetime.now().isoformat(),
                    'message': 'No issues found' if result.returncode == 0 else 'Check failed'
                }
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return {
                'success': False,
                'scope': scope,
                'auto_fix': auto_fix,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def analyze_results(self, json_result, scope, auto_fix):
        """結果を分析"""
        total_errors = 0
        total_warnings = 0
        file_count = len(json_result)
        
        issues_by_rule = {}
        
        for file_result in json_result:
            for message in file_result.get('messages', []):
                if message['severity'] == 2:
                    total_errors += 1
                else:
                    total_warnings += 1
                
                rule_id = message.get('ruleId', 'unknown')
                if rule_id not in issues_by_rule:
                    issues_by_rule[rule_id] = 0
                issues_by_rule[rule_id] += 1
        
        result = {
            'success': total_errors == 0,
            'scope': scope,
            'auto_fix': auto_fix,
            'timestamp': datetime.now().isoformat(),
            'file_count': file_count,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'issues_by_rule': issues_by_rule
        }
        
        # 結果を表示
        print(f"\n📊 チェック結果:")
        print(f"  ファイル数: {file_count}")
        print(f"  エラー: {total_errors}")
        print(f"  警告: {total_warnings}")
        
        if issues_by_rule:
            print(f"\n  ルール別:")
            for rule, count in sorted(issues_by_rule.items(), key=lambda x: x[1], reverse=True):
                print(f"    {rule}: {count}件")
        
        # レポートを保存
        self.save_report(result)
        
        return result
    
    def save_report(self, result):
        """レポートを保存"""
        self.ensure_report_dir()
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = os.path.join(self.report_dir, f'textlint_report_{date_str}.json')
        
        # 既存のレポートを読み込み
        reports = []
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                reports = json.load(f)
        
        reports.append(result)
        
        # レポートを保存
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
    
    def generate_daily_report(self):
        """日次レポートを生成"""
        print(f"\n📈 日次レポート生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = os.path.join(self.report_dir, f'textlint_report_{date_str}.json')
        
        if not os.path.exists(report_file):
            print("本日のチェックデータがありません")
            return
        
        with open(report_file, 'r', encoding='utf-8') as f:
            reports = json.load(f)
        
        # 統計を計算
        total_checks = len(reports)
        total_errors = sum(r.get('total_errors', 0) for r in reports)
        total_warnings = sum(r.get('total_warnings', 0) for r in reports)
        auto_fixed = sum(1 for r in reports if r.get('auto_fix', False))
        
        # サマリーを作成
        summary = f"""
# textlint 日次レポート - {date_str}

## 📊 サマリー
- チェック実行回数: {total_checks}回
- 検出エラー総数: {total_errors}件
- 検出警告総数: {total_warnings}件
- 自動修正実行: {auto_fixed}回

## 📈 時系列データ
"""
        
        for report in reports:
            time_str = datetime.fromisoformat(report['timestamp']).strftime('%H:%M')
            summary += f"\n### {time_str} - {report['scope']}"
            summary += f"\n- エラー: {report.get('total_errors', 0)}件"
            summary += f"\n- 警告: {report.get('total_warnings', 0)}件"
            if report.get('auto_fix'):
                summary += "\n- 🔧 自動修正実行"
        
        # 最も多い問題
        all_issues = {}
        for report in reports:
            for rule, count in report.get('issues_by_rule', {}).items():
                if rule not in all_issues:
                    all_issues[rule] = 0
                all_issues[rule] += count
        
        if all_issues:
            summary += "\n\n## 🔍 頻出問題TOP5"
            for i, (rule, count) in enumerate(sorted(all_issues.items(), 
                                                    key=lambda x: x[1], 
                                                    reverse=True)[:5], 1):
                summary += f"\n{i}. {rule}: {count}件"
        
        # レポートを保存
        summary_file = os.path.join(self.report_dir, f'daily_summary_{date_str}.md')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ 日次レポートを生成しました: {summary_file}")
        
        # 通知（設定されている場合）
        self.send_notification(summary)
    
    def send_notification(self, message):
        """通知を送信（実装は環境に応じて）"""
        # ここでSlackやメール通知を実装可能
        pass
    
    def schedule_job(self, schedule_config):
        """ジョブをスケジュール"""
        time_str = schedule_config['time']
        scope = schedule_config.get('scope', 'all')
        auto_fix = schedule_config.get('auto_fix', False)
        
        schedule.every().day.at(time_str).do(
            self.run_textlint_check, scope=scope, auto_fix=auto_fix
        )
        
        print(f"📅 スケジュール登録: {time_str} - {scope} {'(自動修正)' if auto_fix else ''}")
    
    def setup_schedules(self):
        """すべてのスケジュールを設定"""
        print("⏰ textlintスケジューラーを起動しています...")
        
        # 定期チェックのスケジュール
        for schedule_config in self.config['schedules']:
            self.schedule_job(schedule_config)
        
        # 日次レポート
        if self.config['daily_report']:
            report_time = self.config['report_time']
            schedule.every().day.at(report_time).do(self.generate_daily_report)
            print(f"📅 日次レポート: {report_time}")
        
        print("\n✅ スケジューラー起動完了")
        print("停止するには Ctrl+C を押してください\n")
    
    def signal_handler(self, signum, frame):
        """シグナルハンドラー"""
        print("\n⏹️ スケジューラーを停止しています...")
        self.running = False
        sys.exit(0)
    
    def run(self):
        """スケジューラーを実行"""
        # シグナルハンドラー設定
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.setup_schedules()
        
        # 次回実行時刻を表示
        self.show_next_runs()
        
        while self.running:
            schedule.run_pending()
            time.sleep(30)  # 30秒ごとにチェック
    
    def show_next_runs(self):
        """次回実行予定を表示"""
        print("📅 次回実行予定:")
        jobs = schedule.get_jobs()
        for job in jobs[:5]:  # 最初の5件のみ表示
            print(f"  - {job.next_run}")

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='textlint定期実行スケジューラー')
    parser.add_argument('command', nargs='?', default='start',
                      choices=['start', 'check', 'report', 'config'],
                      help='実行するコマンド')
    parser.add_argument('--scope', default='all', help='チェック範囲')
    parser.add_argument('--fix', action='store_true', help='自動修正を有効化')
    
    args = parser.parse_args()
    
    scheduler = TextlintScheduler()
    
    if args.command == 'start':
        scheduler.run()
    elif args.command == 'check':
        # 今すぐチェック実行
        scheduler.run_textlint_check(scope=args.scope, auto_fix=args.fix)
    elif args.command == 'report':
        # 今すぐレポート生成
        scheduler.generate_daily_report()
    elif args.command == 'config':
        print(f"設定ファイル: {scheduler.config_file}")
        print(json.dumps(scheduler.config, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()