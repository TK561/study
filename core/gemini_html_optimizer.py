#!/usr/bin/env python3
"""
Gemini AI HTML最適化システム
AIによる知的なHTMLコンテンツ最適化とバッジ生成
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# オプションの依存関係
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GeminiHTMLOptimizer:
    def __init__(self):
        # Gemini API設定
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.gemini_enabled = True
        else:
            self.model = None
            self.gemini_enabled = False
        
        # 学習データファイル
        self.learning_data_file = "logs/gemini_html_learning.json"
        self.learning_data = self._load_learning_data()
        
    def _load_learning_data(self) -> Dict:
        """AIの学習データを読み込み"""
        if os.path.exists(self.learning_data_file):
            try:
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "badge_history": [],
            "optimization_patterns": [],
            "user_feedback": [],
            "success_metrics": {}
        }
    
    def _save_learning_data(self):
        """AIの学習データを保存"""
        os.makedirs(os.path.dirname(self.learning_data_file), exist_ok=True)
        try:
            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"学習データ保存エラー: {e}")
    
    def analyze_git_context(self, commit_message: str, changed_files: List[str] = None) -> Dict:
        """Gitのコンテキストを分析してAI最適化のヒントを生成"""
        if not self.gemini_enabled:
            return self._fallback_analysis(commit_message, changed_files)
        
        # 過去の成功パターンを取得
        recent_badges = self.learning_data["badge_history"][-10:]
        
        prompt = f"""
        Gitコミット情報を分析して、Webサイトの状態に最適なステータスバッジを提案してください。

        コミットメッセージ: "{commit_message}"
        変更ファイル: {changed_files or "不明"}
        
        過去の成功バッジ例:
        {json.dumps(recent_badges, ensure_ascii=False, indent=2)}

        以下のJSON形式で回答してください:
        {{
            "recommended_badge": "提案するバッジテキスト",
            "confidence": 0.0-1.0,
            "reasoning": "選択理由",
            "alternative_badges": ["代替案1", "代替案2"],
            "project_status": "プロジェクトの現在状態の分析"
        }}
        
        バッジは簡潔で分かりやすく、プロジェクトの進展を適切に表現してください。
        """
        
        try:
            response = self.model.generate_content(prompt)
            analysis = json.loads(response.text)
            
            # 学習データに記録
            self.learning_data["badge_history"].append({
                "timestamp": datetime.now().isoformat(),
                "commit": commit_message,
                "ai_recommendation": analysis,
                "files_changed": changed_files
            })
            
            # 最新100件のみ保持
            if len(self.learning_data["badge_history"]) > 100:
                self.learning_data["badge_history"] = self.learning_data["badge_history"][-100:]
            
            self._save_learning_data()
            return analysis
            
        except Exception as e:
            print(f"Gemini AI分析エラー: {e}")
            return self._fallback_analysis(commit_message, changed_files)
    
    def _fallback_analysis(self, commit_message: str, changed_files: List[str] = None) -> Dict:
        """Gemini AI利用不可時のフォールバック分析"""
        commit_lower = commit_message.lower()
        
        # 基本的なパターンマッチング
        if "discussion" in commit_lower or "ディスカッション" in commit_lower:
            badge = "ディスカッションサイト統合完了"
            confidence = 0.8
        elif "ui" in commit_lower or "design" in commit_lower:
            badge = "UI改善完了"
            confidence = 0.7
        elif "feature" in commit_lower or "機能" in commit_lower:
            badge = "新機能追加完了"
            confidence = 0.7
        elif "deploy" in commit_lower or "デプロイ" in commit_lower:
            badge = "自動デプロイ完了"
            confidence = 0.9
        elif "fix" in commit_lower or "修正" in commit_lower:
            badge = "バグ修正完了"
            confidence = 0.8
        else:
            badge = "最新版リリース完了"
            confidence = 0.5
        
        return {
            "recommended_badge": badge,
            "confidence": confidence,
            "reasoning": f"パターンマッチングによる分析: '{commit_message}'",
            "alternative_badges": ["システム更新完了", "開発進行中"],
            "project_status": "継続的な開発・改善段階"
        }
    
    def optimize_html_metadata(self, html_content: str, git_info: Dict) -> Tuple[str, Dict]:
        """Gemini AIによるHTML メタデータの最適化"""
        if not self.gemini_enabled:
            return html_content, {"optimization_applied": False, "reason": "Gemini AI未設定"}
        
        # 現在のタイトルと説明を抽出
        title_match = re.search(r'<title>([^<]+)</title>', html_content)
        description_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
        
        current_title = title_match.group(1) if title_match else "不明"
        current_desc = description_match.group(1) if description_match else "なし"
        
        prompt = f"""
        研究プロジェクトのHTMLページのメタデータを最適化してください。

        現在のタイトル: "{current_title}"
        現在の説明: "{current_desc}"
        最新コミット: "{git_info.get('message', '')}"
        プロジェクト状況: 意味カテゴリ画像分類システムの研究成果サイト

        以下のJSON形式で最適化提案をしてください:
        {{
            "optimized_title": "SEO最適化されたタイトル",
            "optimized_description": "検索エンジン向け説明文（160文字以内）",
            "keywords": ["キーワード1", "キーワード2"],
            "reasoning": "最適化の理由",
            "seo_score": 0.0-1.0
        }}
        
        学術的で専門性をアピールしつつ、一般にも理解しやすい表現を心がけてください。
        """
        
        try:
            response = self.model.generate_content(prompt)
            optimization = json.loads(response.text)
            
            # HTMLに最適化を適用
            optimized_html = html_content
            
            # タイトル更新
            if title_match and optimization.get("optimized_title"):
                optimized_html = optimized_html.replace(
                    title_match.group(0),
                    f'<title>{optimization["optimized_title"]}</title>'
                )
            
            # 説明文追加・更新
            if optimization.get("optimized_description"):
                meta_desc = f'<meta name="description" content="{optimization["optimized_description"]}">'
                
                if description_match:
                    optimized_html = optimized_html.replace(description_match.group(0), meta_desc)
                else:
                    # headタグ内に追加
                    optimized_html = optimized_html.replace(
                        '<meta name="viewport"',
                        f'{meta_desc}\n    <meta name="viewport"'
                    )
            
            # キーワード追加
            if optimization.get("keywords"):
                keywords_meta = f'<meta name="keywords" content="{", ".join(optimization["keywords"])}">'
                optimized_html = optimized_html.replace(
                    '<meta name="viewport"',
                    f'{keywords_meta}\n    <meta name="viewport"'
                )
            
            # 最適化履歴を記録
            self.learning_data["optimization_patterns"].append({
                "timestamp": datetime.now().isoformat(),
                "type": "metadata_optimization",
                "original_title": current_title,
                "optimized_title": optimization.get("optimized_title"),
                "seo_score": optimization.get("seo_score", 0),
                "git_context": git_info
            })
            
            self._save_learning_data()
            
            return optimized_html, {
                "optimization_applied": True,
                "changes": optimization,
                "seo_improvement": True
            }
            
        except Exception as e:
            print(f"HTML最適化エラー: {e}")
            return html_content, {"optimization_applied": False, "error": str(e)}
    
    def generate_performance_report(self) -> str:
        """パフォーマンスレポートを生成"""
        report = ["# Gemini AI HTML最適化レポート\n"]
        report.append(f"**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # バッジ生成統計
        if self.learning_data["badge_history"]:
            recent_badges = self.learning_data["badge_history"][-30:]
            badge_types = {}
            for entry in recent_badges:
                badge = entry.get("ai_recommendation", {}).get("recommended_badge", "不明")
                badge_types[badge] = badge_types.get(badge, 0) + 1
            
            report.append("## 📊 バッジ生成統計（最近30件）\n")
            for badge, count in sorted(badge_types.items(), key=lambda x: x[1], reverse=True):
                report.append(f"- **{badge}**: {count}回")
            report.append("")
        
        # 最適化パターン
        if self.learning_data["optimization_patterns"]:
            recent_opts = self.learning_data["optimization_patterns"][-10:]
            avg_seo_score = sum(opt.get("seo_score", 0) for opt in recent_opts) / len(recent_opts)
            
            report.append("## 🚀 最適化パフォーマンス\n")
            report.append(f"- **平均SEOスコア**: {avg_seo_score:.2f}/1.0")
            report.append(f"- **最適化実行回数**: {len(self.learning_data['optimization_patterns'])}回")
            report.append("")
        
        # システム状態
        report.append("## ⚙️ システム状態\n")
        report.append(f"- **Gemini AI**: {'有効' if self.gemini_enabled else '無効'}")
        report.append(f"- **学習データ件数**: {len(self.learning_data['badge_history'])}件")
        report.append(f"- **最適化パターン数**: {len(self.learning_data['optimization_patterns'])}件")
        
        return "\n".join(report)
    
    def record_user_feedback(self, badge_text: str, rating: int, feedback: str = ""):
        """ユーザーフィードバックを記録"""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "badge_text": badge_text,
            "rating": rating,  # 1-5
            "feedback": feedback
        }
        
        self.learning_data["user_feedback"].append(feedback_entry)
        
        # フィードバックを分析してSUCCESS METRICSを更新
        ratings = [f["rating"] for f in self.learning_data["user_feedback"]]
        if ratings:
            self.learning_data["success_metrics"] = {
                "average_rating": sum(ratings) / len(ratings),
                "total_feedback": len(ratings),
                "satisfaction_rate": len([r for r in ratings if r >= 4]) / len(ratings)
            }
        
        self._save_learning_data()

def main():
    """テスト用メインプログラム"""
    print("🤖 Gemini AI HTML最適化システム テスト")
    print("=" * 50)
    
    optimizer = GeminiHTMLOptimizer()
    
    # バッジ生成テスト
    test_commit = "Auto deploy - 2025-06-24 20:21:01"
    analysis = optimizer.analyze_git_context(test_commit, ["index.html", "vercel.json"])
    
    print("📋 AI分析結果:")
    print(f"  推奨バッジ: {analysis['recommended_badge']}")
    print(f"  信頼度: {analysis['confidence']:.2f}")
    print(f"  理由: {analysis['reasoning']}")
    
    # パフォーマンスレポート
    print("\n" + optimizer.generate_performance_report())

if __name__ == "__main__":
    main()