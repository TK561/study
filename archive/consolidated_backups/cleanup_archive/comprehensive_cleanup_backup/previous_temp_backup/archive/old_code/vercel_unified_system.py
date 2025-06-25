#!/usr/bin/env python3
"""
Vercel統合管理システム
全てのVercel関連機能を一元化した高満足度システム
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import subprocess

# 既存システムのインポート
from vercel_deployment_manager import VercelDeploymentManager
from vercel_update_tracker import VercelUpdateTracker
from vercel_fix_assistant import VercelFixAssistant
from vercel_gemini_integration import VercelGeminiIntegration

class VercelUnifiedSystem:
    """
    Vercel関連の全機能を統合した包括的なシステム
    """
    
    def __init__(self):
        # コンポーネント初期化
        self.deployment_manager = VercelDeploymentManager()
        self.update_tracker = VercelUpdateTracker()
        self.fix_assistant = VercelFixAssistant()
        self.ai_integration = VercelGeminiIntegration()
        
        # 統合設定
        self.unified_config_file = "VERCEL_UNIFIED_CONFIG.json"
        self.workflow_history_file = "VERCEL_WORKFLOW_HISTORY.json"
        self.config = self._load_unified_config()
        
        # ワークフロー履歴
        self.workflow_history = self._load_workflow_history()
    
    def _load_unified_config(self) -> Dict:
        """統合設定を読み込む"""
        if os.path.exists(self.unified_config_file):
            with open(self.unified_config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # デフォルト設定
        default_config = {
            "auto_optimize": True,
            "auto_backup": True,
            "ai_analysis": True,
            "user_preferences": {
                "preferred_type": "static_html",
                "auto_fix_errors": True,
                "detailed_reports": True
            },
            "deployment_rules": {
                "require_backup": True,
                "min_success_rate": 70,
                "max_retry_attempts": 3
            }
        }
        
        self._save_unified_config(default_config)
        return default_config
    
    def _save_unified_config(self, config: Dict = None):
        """統合設定を保存"""
        if config:
            self.config = config
        with open(self.unified_config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _load_workflow_history(self) -> List[Dict]:
        """ワークフロー履歴を読み込む"""
        if os.path.exists(self.workflow_history_file):
            with open(self.workflow_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_workflow_history(self):
        """ワークフロー履歴を保存"""
        with open(self.workflow_history_file, 'w', encoding='utf-8') as f:
            json.dump(self.workflow_history, f, ensure_ascii=False, indent=2)
    
    def _record_workflow(self, action: str, result: Dict, duration: float):
        """ワークフローを記録"""
        workflow = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result,
            "duration_seconds": duration,
            "config_snapshot": self.config.copy()
        }
        self.workflow_history.append(workflow)
        self._save_workflow_history()
    
    async def smart_deploy_workflow(self) -> Dict:
        """
        スマートデプロイワークフロー
        AIと既存システムを組み合わせた最適なデプロイプロセス
        """
        start_time = datetime.now()
        print("🎯 Vercel統合スマートデプロイを開始")
        print("=" * 60)
        
        result = {
            "workflow_id": f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "steps": [],
            "success": False,
            "satisfaction_score": None
        }
        
        try:
            # Step 1: 環境診断
            print("\n📋 Step 1: 環境診断")
            diagnosis = self._diagnose_environment()
            result["steps"].append({
                "name": "環境診断",
                "status": "completed",
                "details": diagnosis
            })
            
            # Step 2: AI分析（有効な場合）
            if self.config["ai_analysis"]:
                print("\n🤖 Step 2: AI分析")
                ai_result = await self._ai_analysis_step()
                result["steps"].append({
                    "name": "AI分析",
                    "status": "completed",
                    "details": ai_result
                })
            
            # Step 3: 自動最適化
            if self.config["auto_optimize"]:
                print("\n🔧 Step 3: 自動最適化")
                optimization = self._optimize_configuration()
                result["steps"].append({
                    "name": "構成最適化",
                    "status": "completed",
                    "details": optimization
                })
            
            # Step 4: バックアップ
            if self.config["auto_backup"]:
                print("\n💾 Step 4: バックアップ作成")
                backup = self.deployment_manager.backup_current_deployment()
                result["steps"].append({
                    "name": "バックアップ",
                    "status": "completed",
                    "details": {"backup_path": backup}
                })
            
            # Step 5: デプロイ実行
            print("\n🚀 Step 5: デプロイ実行")
            deploy_result = await self._execute_deployment()
            result["steps"].append({
                "name": "デプロイ",
                "status": "completed" if deploy_result["success"] else "failed",
                "details": deploy_result
            })
            
            if deploy_result["success"]:
                result["success"] = True
                
                # Step 6: 成功パターン記録
                print("\n📝 Step 6: 成功パターン記録")
                pattern = self._record_success_pattern(deploy_result)
                result["steps"].append({
                    "name": "パターン記録",
                    "status": "completed",
                    "details": pattern
                })
            else:
                # エラー修復
                if self.config["user_preferences"]["auto_fix_errors"]:
                    print("\n🔧 エラー自動修復")
                    fix_result = await self._auto_fix_errors(deploy_result.get("error"))
                    result["steps"].append({
                        "name": "エラー修復",
                        "status": "completed" if fix_result["fixed"] else "failed",
                        "details": fix_result
                    })
            
            # Step 7: レポート生成
            if self.config["user_preferences"]["detailed_reports"]:
                print("\n📊 Step 7: 詳細レポート生成")
                report = self._generate_comprehensive_report(result)
                result["report"] = report
                print(report)
            
        except Exception as e:
            result["error"] = str(e)
            print(f"\n❌ ワークフローエラー: {e}")
        
        # ワークフロー記録
        duration = (datetime.now() - start_time).total_seconds()
        self._record_workflow("smart_deploy", result, duration)
        
        # ユーザー満足度収集
        if result["success"]:
            satisfaction = await self._collect_user_satisfaction(result)
            result["satisfaction_score"] = satisfaction
        
        return result
    
    def _diagnose_environment(self) -> Dict:
        """環境診断"""
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "checks": []
        }
        
        # ファイル構造チェック
        if os.path.exists("public/index.html"):
            diagnosis["checks"].append({
                "item": "静的HTMLファイル",
                "status": "OK",
                "path": "public/index.html"
            })
        elif os.path.exists("index.html"):
            diagnosis["checks"].append({
                "item": "HTMLファイル",
                "status": "要移動",
                "path": "index.html",
                "action": "public/ディレクトリへの移動推奨"
            })
        
        # vercel.json チェック
        if os.path.exists("vercel.json"):
            with open("vercel.json", 'r') as f:
                vercel_config = json.load(f)
                if vercel_config == {"version": 2}:
                    diagnosis["checks"].append({
                        "item": "vercel.json",
                        "status": "最適",
                        "config": vercel_config
                    })
                else:
                    diagnosis["checks"].append({
                        "item": "vercel.json",
                        "status": "要最適化",
                        "config": vercel_config,
                        "recommendation": {"version": 2}
                    })
        
        # 過去のエラー確認
        error_count = len([h for h in self.workflow_history 
                          if not h.get("result", {}).get("success", True)
                          and h.get("timestamp", "") > 
                          (datetime.now() - timedelta(days=7)).isoformat()])
        
        diagnosis["error_rate_7days"] = error_count
        diagnosis["health_score"] = 100 - (error_count * 10)  # エラー1件につき-10点
        
        return diagnosis
    
    async def _ai_analysis_step(self) -> Dict:
        """AI分析ステップ"""
        current_config = {
            "type": "static_html" if os.path.exists("public/index.html") else "unknown",
            "files": self._get_deployment_files()
        }
        
        # 成功率予測
        success_rate, factors = self.ai_integration.predict_deployment_success(current_config)
        
        # AI詳細分析（可能な場合）
        ai_insights = {}
        if self.ai_integration.model:
            try:
                ai_insights = await self.ai_integration.analyze_deployment_with_ai(current_config)
            except:
                ai_insights = {"available": False}
        
        return {
            "predicted_success_rate": success_rate,
            "success_factors": factors,
            "ai_insights": ai_insights
        }
    
    def _optimize_configuration(self) -> Dict:
        """構成を最適化"""
        optimizations = []
        
        # index.htmlの配置最適化
        if os.path.exists("index.html") and not os.path.exists("public/index.html"):
            os.makedirs("public", exist_ok=True)
            subprocess.run(["mv", "index.html", "public/"], check=True)
            optimizations.append("index.htmlをpublic/に移動")
        
        # vercel.json最適化
        optimal_vercel = {"version": 2}
        with open("vercel.json", "w") as f:
            json.dump(optimal_vercel, f, indent=2)
        optimizations.append("vercel.json最適化")
        
        # .gitignore確認
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w") as f:
                f.write(".env\n.vercel/\nnode_modules/\n")
            optimizations.append(".gitignore作成")
        
        return {
            "optimizations": optimizations,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_deployment(self) -> Dict:
        """デプロイメント実行"""
        try:
            # direct_vercel_deploy.pyを使用
            from direct_vercel_deploy import deploy_to_vercel
            success = deploy_to_vercel()
            
            if success:
                return {
                    "success": True,
                    "timestamp": datetime.now().isoformat(),
                    "url": "https://study-research-final.vercel.app"
                }
            else:
                return {
                    "success": False,
                    "error": "デプロイメント失敗"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _record_success_pattern(self, deploy_result: Dict) -> Dict:
        """成功パターンを記録"""
        pattern = self.deployment_manager.record_success_pattern(
            deployment_type="static_html",
            files_changed=self._get_deployment_files(),
            config_used=self.config,
            success_reason="統合システムによる最適化デプロイ",
            deploy_id=f"unified_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            url=deploy_result.get("url", "")
        )
        return pattern
    
    async def _auto_fix_errors(self, error: str) -> Dict:
        """エラー自動修復"""
        try:
            # 修正アシスタントを使用
            self.fix_assistant.apply_fix("static_html")
            
            # 再デプロイ試行
            retry_result = await self._execute_deployment()
            
            return {
                "fixed": retry_result["success"],
                "method": "static_html_conversion",
                "retry_result": retry_result
            }
        except Exception as e:
            return {
                "fixed": False,
                "error": str(e)
            }
    
    def _generate_comprehensive_report(self, workflow_result: Dict) -> str:
        """包括的レポート生成"""
        report = [f"# Vercel統合システムレポート"]
        report.append(f"**ワークフローID**: {workflow_result['workflow_id']}")
        report.append(f"**実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**結果**: {'✅ 成功' if workflow_result['success'] else '❌ 失敗'}\n")
        
        # ステップサマリー
        report.append("## 実行ステップ")
        for step in workflow_result["steps"]:
            status_icon = "✅" if step["status"] == "completed" else "❌"
            report.append(f"- {status_icon} {step['name']}")
        
        # 詳細情報
        report.append("\n## 詳細情報")
        
        # 環境診断結果
        diagnosis = next((s["details"] for s in workflow_result["steps"] 
                         if s["name"] == "環境診断"), None)
        if diagnosis:
            report.append(f"\n### 環境健全性スコア: {diagnosis.get('health_score', 0)}%")
        
        # AI分析結果
        ai_analysis = next((s["details"] for s in workflow_result["steps"] 
                           if s["name"] == "AI分析"), None)
        if ai_analysis:
            report.append(f"\n### AI予測成功率: {ai_analysis.get('predicted_success_rate', 0)}%")
        
        # 統計情報
        report.append("\n## 統計情報")
        total_deployments = len(self.update_tracker.get_all_updates())
        report.append(f"- 総デプロイメント数: {total_deployments}")
        
        recent_workflows = [w for w in self.workflow_history 
                           if w["timestamp"] > 
                           (datetime.now() - timedelta(days=30)).isoformat()]
        if recent_workflows:
            success_count = sum(1 for w in recent_workflows 
                               if w.get("result", {}).get("success", False))
            success_rate = (success_count / len(recent_workflows)) * 100
            report.append(f"- 30日間の成功率: {success_rate:.1f}%")
        
        return "\n".join(report)
    
    async def _collect_user_satisfaction(self, result: Dict) -> int:
        """ユーザー満足度を収集"""
        print("\n😊 デプロイメントの満足度を教えてください")
        print("5: とても満足")
        print("4: 満足") 
        print("3: 普通")
        print("2: 不満")
        print("1: とても不満")
        
        try:
            score = int(input("\nスコア (1-5): "))
            score = max(1, min(5, score))  # 1-5の範囲に制限
            
            # フィードバック収集
            feedback = input("改善点があれば教えてください（任意）: ")
            
            # 記録
            self.ai_integration.record_user_satisfaction(
                deployment_id=result["workflow_id"],
                satisfaction_score=score,
                feedback=feedback
            )
            
            # 低評価の場合は改善策を提示
            if score < 3:
                print("\n📝 ご意見ありがとうございます。以下の改善を検討します：")
                print("- デプロイプロセスの簡素化")
                print("- エラーメッセージの改善")
                print("- より詳細なガイダンス提供")
            
            return score
            
        except:
            return 3  # デフォルト値
    
    def _get_deployment_files(self) -> List[str]:
        """デプロイメントファイルリストを取得"""
        files = []
        if os.path.exists("public/index.html"):
            files.append("public/index.html")
        if os.path.exists("vercel.json"):
            files.append("vercel.json")
        return files
    
    def show_dashboard(self):
        """統合ダッシュボード表示"""
        print("\n" + "=" * 60)
        print("📊 Vercel統合システムダッシュボード")
        print("=" * 60)
        
        # 最新の更新情報
        latest_update = self.update_tracker.get_latest_update()
        if latest_update:
            print(f"\n📅 最新デプロイ: {latest_update['date']}")
            print(f"   バージョン: {latest_update['version']}")
            print(f"   URL: {latest_update['url']}")
        
        # 成功率
        recent_workflows = [w for w in self.workflow_history[-10:]]
        if recent_workflows:
            success_count = sum(1 for w in recent_workflows 
                               if w.get("result", {}).get("success", False))
            print(f"\n📈 直近10回の成功率: {(success_count/10)*100:.0f}%")
        
        # 満足度
        if os.path.exists(self.ai_integration.user_satisfaction_file):
            with open(self.ai_integration.user_satisfaction_file, 'r') as f:
                satisfaction = json.load(f)
                if satisfaction.get("average_score"):
                    stars = "⭐" * int(satisfaction["average_score"])
                    print(f"\n😊 平均満足度: {satisfaction['average_score']:.1f}/5.0 {stars}")
        
        # 利用可能なコマンド
        print("\n🔧 利用可能なコマンド:")
        print("1. スマートデプロイ: python3 vercel_unified_system.py deploy")
        print("2. 診断レポート: python3 vercel_unified_system.py diagnose")
        print("3. 修復アシスタント: python3 vercel_fix_assistant.py")
        print("4. 履歴確認: python3 vercel_update_tracker.py")
        
        print("\n" + "=" * 60)

async def main():
    """メイン実行関数"""
    import sys
    
    system = VercelUnifiedSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "deploy":
            # スマートデプロイ実行
            result = await system.smart_deploy_workflow()
            if result["success"]:
                print("\n✅ デプロイメント成功！")
            else:
                print("\n❌ デプロイメント失敗")
                
        elif command == "diagnose":
            # 診断のみ
            diagnosis = system._diagnose_environment()
            print(json.dumps(diagnosis, ensure_ascii=False, indent=2))
            
        elif command == "dashboard":
            # ダッシュボード表示
            system.show_dashboard()
            
        else:
            print(f"不明なコマンド: {command}")
            print("使用方法: python3 vercel_unified_system.py [deploy|diagnose|dashboard]")
    else:
        # デフォルトはダッシュボード表示
        system.show_dashboard()

if __name__ == "__main__":
    asyncio.run(main())