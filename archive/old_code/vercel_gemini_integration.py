#!/usr/bin/env python3
"""
Vercel × Gemini AI 統合デプロイメントシステム
AIによる自動最適化と予測的デプロイメント管理
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# オプションの依存関係
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("📝 Note: Gemini AI機能を使用するには 'pip install google-generativeai' を実行してください")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("📝 Note: .env機能を使用するには 'pip install python-dotenv' を実行してください")

# 既存システムのインポート
from vercel_deployment_manager import VercelDeploymentManager
from vercel_update_tracker import VercelUpdateTracker
from vercel_fix_assistant import VercelFixAssistant

class VercelGeminiIntegration:
    def __init__(self):
        # Gemini API設定
        self.gemini_api_key = os.getenv('GEMINI_API_KEY') if 'os' in globals() else None
        
        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            if not GEMINI_AVAILABLE:
                print("📝 Gemini AI機能は無効です（オプション）")
            elif not self.gemini_api_key:
                print("📝 Gemini APIキーが設定されていません（オプション）")
        
        # 既存システムの統合
        self.deployment_manager = VercelDeploymentManager()
        self.update_tracker = VercelUpdateTracker()
        self.fix_assistant = VercelFixAssistant()
        
        # AI学習データ
        self.ai_insights_file = "VERCEL_AI_INSIGHTS.json"
        self.user_satisfaction_file = "VERCEL_USER_SATISFACTION.json"
        self.ai_insights = self._load_ai_insights()
    
    def _load_ai_insights(self) -> Dict:
        """AI洞察データを読み込む"""
        if os.path.exists(self.ai_insights_file):
            with open(self.ai_insights_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "deployment_patterns": [],
            "optimization_history": [],
            "user_preferences": {},
            "success_factors": []
        }
    
    def _save_ai_insights(self):
        """AI洞察データを保存"""
        with open(self.ai_insights_file, 'w', encoding='utf-8') as f:
            json.dump(self.ai_insights, f, ensure_ascii=False, indent=2)
    
    async def analyze_deployment_with_ai(self, deployment_config: Dict) -> Dict:
        """Gemini AIでデプロイメント構成を分析"""
        if not self.model:
            return {"ai_available": False, "reason": "Gemini API未設定"}
        
        # 過去の成功パターンを取得
        success_patterns = self.deployment_manager.success_patterns.get("patterns", [])
        
        # AIプロンプト構築
        prompt = f"""
        Vercelデプロイメント構成を分析してください。

        現在の構成:
        {json.dumps(deployment_config, ensure_ascii=False, indent=2)}

        過去の成功パターン:
        {json.dumps(success_patterns[-3:], ensure_ascii=False, indent=2)}

        以下の観点で分析してください：
        1. 成功確率の予測（0-100%）
        2. 潜在的な問題点
        3. 最適化の提案
        4. ユーザー体験の改善点
        5. 推奨される構成変更

        JSON形式で回答してください。
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            analysis = json.loads(response.text)
            
            # AI洞察を記録
            self.ai_insights["deployment_patterns"].append({
                "timestamp": datetime.now().isoformat(),
                "config": deployment_config,
                "ai_analysis": analysis
            })
            self._save_ai_insights()
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ AI分析エラー: {e}")
            return {"ai_available": False, "error": str(e)}
    
    def predict_deployment_success(self, config: Dict) -> Tuple[float, List[str]]:
        """デプロイメント成功率を予測"""
        success_rate = 0.0
        factors = []
        
        # 基本チェック
        if config.get("type") == "static_html":
            success_rate += 40
            factors.append("静的HTMLサイト（+40%）")
        
        if "api/" not in str(config.get("files", [])):
            success_rate += 20
            factors.append("API不使用（+20%）")
        
        # 過去の成功パターンとの類似性
        similar_pattern = self.deployment_manager.find_similar_success_pattern(config)
        if similar_pattern:
            success_rate += 30
            factors.append(f"類似成功パターンあり（+30%）")
        
        # 最近のエラー履歴確認
        if hasattr(self.fix_assistant, 'error_history'):
            recent_errors = len([e for e in self.fix_assistant.error_history 
                               if e.get("timestamp", "") > 
                               (datetime.now() - timedelta(hours=24)).isoformat()])
            if recent_errors == 0:
                success_rate += 10
                factors.append("24時間エラーなし（+10%）")
        
        return min(success_rate, 100), factors
    
    def optimize_deployment_config(self, current_config: Dict) -> Dict:
        """デプロイメント構成を最適化"""
        optimized = current_config.copy()
        optimizations = []
        
        # 静的サイト最適化
        if current_config.get("type") != "static_html" and "api/" in str(current_config.get("files", [])):
            optimized["type"] = "static_html"
            optimized["recommendation"] = "静的HTMLサイトへの移行を推奨"
            optimizations.append("APIを静的HTMLに変換")
        
        # vercel.json最適化
        if "vercel.json" in current_config.get("files", []):
            optimized["vercel_config"] = {"version": 2}
            optimizations.append("vercel.json簡素化")
        
        # キャッシュ設定追加
        optimized["cache_headers"] = {
            "Cache-Control": "public, max-age=3600",
            "X-Optimized-By": "Vercel-Gemini-Integration"
        }
        optimizations.append("キャッシュヘッダー最適化")
        
        optimized["optimizations"] = optimizations
        return optimized
    
    def record_user_satisfaction(self, deployment_id: str, satisfaction_score: int, feedback: str = ""):
        """ユーザー満足度を記録"""
        if os.path.exists(self.user_satisfaction_file):
            with open(self.user_satisfaction_file, 'r', encoding='utf-8') as f:
                satisfaction_data = json.load(f)
        else:
            satisfaction_data = {"records": [], "average_score": 0}
        
        record = {
            "deployment_id": deployment_id,
            "timestamp": datetime.now().isoformat(),
            "score": satisfaction_score,  # 1-5
            "feedback": feedback
        }
        
        satisfaction_data["records"].append(record)
        
        # 平均スコア計算
        scores = [r["score"] for r in satisfaction_data["records"]]
        satisfaction_data["average_score"] = sum(scores) / len(scores)
        
        with open(self.user_satisfaction_file, 'w', encoding='utf-8') as f:
            json.dump(satisfaction_data, f, ensure_ascii=False, indent=2)
        
        # AI学習用データに追加
        self.ai_insights["user_preferences"][deployment_id] = {
            "score": satisfaction_score,
            "feedback": feedback
        }
        self._save_ai_insights()
    
    def generate_deployment_report(self) -> str:
        """統合デプロイメントレポート生成"""
        report = ["# Vercel × Gemini 統合デプロイメントレポート\n"]
        report.append(f"**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 成功率統計
        if self.ai_insights["deployment_patterns"]:
            recent_patterns = self.ai_insights["deployment_patterns"][-10:]
            success_predictions = [p.get("ai_analysis", {}).get("success_probability", 0) 
                                 for p in recent_patterns 
                                 if "ai_analysis" in p]
            if success_predictions:
                avg_prediction = sum(success_predictions) / len(success_predictions)
                report.append(f"## 📊 AI予測成功率\n")
                report.append(f"- **平均予測成功率**: {avg_prediction:.1f}%")
                report.append(f"- **分析済みデプロイメント**: {len(success_predictions)}件\n")
        
        # ユーザー満足度
        if os.path.exists(self.user_satisfaction_file):
            with open(self.user_satisfaction_file, 'r', encoding='utf-8') as f:
                satisfaction = json.load(f)
                if satisfaction.get("average_score"):
                    report.append(f"## 😊 ユーザー満足度\n")
                    report.append(f"- **平均スコア**: {satisfaction['average_score']:.1f}/5.0")
                    report.append(f"- **評価件数**: {len(satisfaction.get('records', []))}件\n")
        
        # 最適化提案
        report.append("## 🚀 AI最適化提案\n")
        if self.ai_insights.get("optimization_history"):
            recent_opts = self.ai_insights["optimization_history"][-3:]
            for opt in recent_opts:
                report.append(f"- {opt.get('suggestion', 'N/A')}")
        else:
            report.append("- 静的HTMLサイトへの移行を推奨")
            report.append("- vercel.json最小構成の維持")
            report.append("- 定期的なバックアップ実施")
        
        # 成功要因
        report.append("\n## ✅ 成功要因分析\n")
        success_factors = self.deployment_manager.success_patterns.get("metadata", {}).get("common_issues", [])
        if success_factors:
            for factor in success_factors:
                report.append(f"- **{factor['issue']}**: {factor['solution']}")
        
        return "\n".join(report)
    
    async def intelligent_deploy(self, auto_optimize: bool = True) -> Dict:
        """AI支援による知的デプロイメント"""
        print("🤖 AI支援デプロイメントを開始...")
        
        # 現在の構成を分析
        current_config = {
            "type": "static_html" if os.path.exists("public/index.html") else "unknown",
            "files": ["public/index.html", "vercel.json"] if os.path.exists("public/index.html") else []
        }
        
        # 成功率予測
        success_rate, factors = self.predict_deployment_success(current_config)
        print(f"\n📊 予測成功率: {success_rate}%")
        for factor in factors:
            print(f"  - {factor}")
        
        # AI分析（利用可能な場合）
        if self.model:
            print("\n🔍 Gemini AIによる詳細分析中...")
            ai_analysis = await self.analyze_deployment_with_ai(current_config)
            if ai_analysis.get("ai_available", False):
                print(f"  - AI推奨事項: {ai_analysis.get('recommendations', 'なし')}")
        
        # 最適化実行
        if auto_optimize and success_rate < 80:
            print("\n🔧 構成を最適化中...")
            optimized_config = self.optimize_deployment_config(current_config)
            for opt in optimized_config.get("optimizations", []):
                print(f"  - {opt}")
            
            # 最適化を適用
            if "静的HTMLに変換" in str(optimized_config.get("optimizations", [])):
                self.fix_assistant.apply_fix("static_html")
        
        # バックアップ作成
        backup_path = self.deployment_manager.backup_current_deployment()
        print(f"\n💾 バックアップ作成: {backup_path}")
        
        # デプロイ実行
        try:
            from direct_vercel_deploy import deploy_to_vercel
            success = deploy_to_vercel()
            
            if success:
                # 成功パターン記録
                pattern = self.deployment_manager.record_success_pattern(
                    deployment_type="static_html",
                    files_changed=["public/index.html", "vercel.json"],
                    config_used=current_config,
                    success_reason="AI最適化によるデプロイメント成功",
                    deploy_id=f"ai_deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    url="https://study-research-final.vercel.app"
                )
                
                return {
                    "success": True,
                    "pattern_id": pattern["id"],
                    "success_rate": success_rate,
                    "optimizations": optimized_config.get("optimizations", [])
                }
            else:
                # 失敗時の自動修復
                print("\n❌ デプロイ失敗 - 自動修復を開始...")
                self.fix_assistant.apply_fix("static_html")
                return {
                    "success": False,
                    "auto_fixed": True,
                    "message": "自動修復を実行しました"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "backup_available": backup_path
            }

# 便利な関数
async def smart_deploy():
    """スマートデプロイ実行"""
    integration = VercelGeminiIntegration()
    result = await integration.intelligent_deploy(auto_optimize=True)
    
    # ユーザー満足度を尋ねる
    if result.get("success"):
        print("\n📝 デプロイメントの満足度を教えてください (1-5):")
        try:
            score = int(input("スコア: "))
            feedback = input("フィードバック（任意）: ")
            integration.record_user_satisfaction(
                deployment_id=result.get("pattern_id", "unknown"),
                satisfaction_score=score,
                feedback=feedback
            )
            print("✅ フィードバックを記録しました")
        except:
            pass
    
    # レポート生成
    print("\n" + integration.generate_deployment_report())
    
    return result

if __name__ == "__main__":
    import asyncio
    
    print("🚀 Vercel × Gemini 統合システム")
    print("=" * 50)
    
    # 非同期実行
    asyncio.run(smart_deploy())