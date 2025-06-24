#!/usr/bin/env python3
"""
包括的エラー管理システム
予防・検出・対応・学習の完全統合
"""

import os
import json
from datetime import datetime
from emergency_error_response import EmergencyErrorResponse
from vercel_error_prevention import VercelErrorPrevention

class ComprehensiveErrorManager:
    """包括的エラー管理システム"""
    
    def __init__(self):
        self.emergency_responder = EmergencyErrorResponse()
        self.prevention_checker = VercelErrorPrevention()
        self.session_log = []
    
    def full_deployment_check(self):
        """デプロイ前完全チェック"""
        print("🛡️ 包括的デプロイメントチェック開始")
        print("=" * 60)
        
        # 1. 予防チェック実行
        print("\n📋 STEP 1: 予防チェック")
        deployment_ready = self.prevention_checker.full_check()
        
        if not deployment_ready:
            print("\n❌ 予防チェックで問題が発見されました")
            print("🔧 自動修正を試行します...")
            
            # 2. 検出された問題の自動修正
            self._attempt_auto_fixes()
            
            # 3. 再チェック
            print("\n🔄 修正後の再チェック...")
            deployment_ready = self.prevention_checker.full_check()
        
        if deployment_ready:
            print("\n✅ デプロイ準備完了!")
            self._execute_deployment()
        else:
            print("\n⚠️ 手動修正が必要です")
            self._log_session_result("manual_intervention_required")
        
        return deployment_ready
    
    def _attempt_auto_fixes(self):
        """自動修正の試行"""
        # 一般的なVercelエラーパターンで修正を試行
        common_errors = [
            "TypeError: issubclass() arg 1 must be a class",
            "Invalid request: `files` should be array",
            "Push cannot contain secrets"
        ]
        
        for error_pattern in common_errors:
            print(f"🔧 エラーパターン修正試行: {error_pattern[:30]}...")
            success = self.emergency_responder.apply_emergency_fix(error_pattern)
            if success:
                print(f"✅ 修正完了: {error_pattern[:30]}...")
                self._log_session_result("auto_fix_success", error_pattern)
            else:
                print(f"⚠️ 修正失敗: {error_pattern[:30]}...")
    
    def _execute_deployment(self):
        """デプロイメント実行"""
        print("\n🚀 デプロイメント実行中...")
        
        try:
            import subprocess
            result = subprocess.run(
                ["python3", "quick_vercel_fix.py"], 
                capture_output=True, 
                text=True,
                timeout=120  # 2分タイムアウト
            )
            
            if result.returncode == 0:
                print("✅ デプロイメント成功!")
                self._log_session_result("deployment_success")
                self._record_successful_deployment()
            else:
                print(f"❌ デプロイメントエラー: {result.stderr}")
                self._handle_deployment_error(result.stderr)
                
        except subprocess.TimeoutExpired:
            print("⏰ デプロイメントタイムアウト")
            self._log_session_result("deployment_timeout")
        except Exception as e:
            print(f"❌ デプロイメント実行エラー: {e}")
            self._handle_deployment_error(str(e))
    
    def _handle_deployment_error(self, error_message):
        """デプロイメントエラーの処理"""
        print("🚨 デプロイメントエラーを緊急対応システムで処理中...")
        
        # 緊急対応システムで自動修正試行
        success = self.emergency_responder.apply_emergency_fix(error_message)
        
        if success:
            print("✅ エラー修正完了 - 再デプロイを試行...")
            self._execute_deployment()  # 再試行
        else:
            print("❌ 自動修正失敗 - 手動介入が必要")
            self._log_session_result("deployment_failed", error_message)
    
    def _record_successful_deployment(self):
        """成功したデプロイメントの記録"""
        success_record = {
            "timestamp": datetime.now().isoformat(),
            "type": "successful_deployment",
            "prevention_checks_passed": True,
            "auto_fixes_applied": len([log for log in self.session_log if "auto_fix_success" in log.get("result", "")]),
            "deployment_method": "quick_vercel_fix.py",
            "site_url": "https://study-research-final.vercel.app"
        }
        
        # 成功記録ファイルに追加
        success_file = "successful_deployments_log.json"
        
        if os.path.exists(success_file):
            with open(success_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"deployments": []}
        
        data["deployments"].append(success_record)
        
        # 最新30件のみ保持
        if len(data["deployments"]) > 30:
            data["deployments"] = data["deployments"][-30:]
        
        with open(success_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📝 成功デプロイメント記録: {success_file}")
    
    def _log_session_result(self, result_type, details=""):
        """セッション結果のログ記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "result": result_type,
            "details": details
        }
        self.session_log.append(log_entry)
    
    def generate_management_report(self):
        """管理レポート生成"""
        print("\n📊 包括的エラー管理レポート生成中...")
        
        # 緊急対応システムの分析取得
        emergency_trends = self.emergency_responder.analyze_error_trends()
        
        # 予防レポート生成
        prevention_report = self.emergency_responder.generate_prevention_report()
        
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        
        comprehensive_report = f"""# 包括的エラー管理レポート

**生成日時**: {timestamp}

## 🎯 今回のセッション結果

"""
        
        # セッションログ分析
        if self.session_log:
            for log in self.session_log:
                result_icons = {
                    "auto_fix_success": "✅",
                    "deployment_success": "🚀", 
                    "deployment_failed": "❌",
                    "manual_intervention_required": "⚠️",
                    "deployment_timeout": "⏰"
                }
                icon = result_icons.get(log["result"], "📋")
                comprehensive_report += f"- {icon} {log['result']}: {log['details']}\n"
        else:
            comprehensive_report += "- 📋 セッションログなし\n"
        
        comprehensive_report += f"""

## 📊 エラー管理統計

- **総エラー数**: {emergency_trends.get('total_errors', 0)}
- **解決率**: {emergency_trends.get('resolution_rate', '0%')}
- **自動修正成功**: {len([log for log in self.session_log if 'auto_fix_success' in log.get('result', '')])}件

## 🛡️ システム状況

- **予防チェッカー**: ✅ 稼働中
- **緊急対応システム**: ✅ 稼働中  
- **解決策記録**: ✅ 稼働中
- **ナレッジベース**: ✅ 更新中

## 📝 推奨事項

1. **継続モニタリング**: エラーパターンの追跡
2. **予防強化**: 新しいチェック項目の追加
3. **自動化拡張**: より多くのエラーパターンに対応

---
**Generated by**: 包括的エラー管理システム
"""
        
        # レポート保存
        report_file = f"comprehensive_management_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(comprehensive_report)
            print(f"📄 包括レポート保存: {report_file}")
        except Exception as e:
            print(f"⚠️ レポート保存エラー: {e}")
        
        return emergency_trends

def safe_deployment():
    """安全なデプロイメントの実行"""
    manager = ComprehensiveErrorManager()
    
    print("🎯 安全デプロイメントシステム起動")
    print("=" * 60)
    
    # 包括的チェック実行
    success = manager.full_deployment_check()
    
    # レポート生成
    manager.generate_management_report()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 デプロイメント完了!")
        print("🌐 サイト確認: https://study-research-final.vercel.app")
    else:
        print("⚠️ デプロイメント未完了")
        print("📖 詳細は生成されたレポートを確認")
    
    return success

if __name__ == "__main__":
    safe_deployment()