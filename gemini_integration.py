#!/usr/bin/env python3
"""
Gemini AI 統合システム
研究ディスカッション記録の分析と提案生成
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

class GeminiIntegration:
    def __init__(self):
        self.research_root = Path(__file__).parent
        self.env_file = self.research_root / ".env"
        self.api_key = self.load_api_key()
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
    def load_api_key(self):
        """環境変数からGemini APIキーを読み込み"""
        # .envファイルから読み込み
        if self.env_file.exists():
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEY='):
                        return line.split('=', 1)[1].strip().strip('"')
        
        # 環境変数から読み込み
        return os.getenv('GEMINI_API_KEY', '')
    
    def generate_content(self, prompt, max_tokens=8192):
        """Gemini APIでコンテンツ生成"""
        if not self.api_key:
            return {"error": "Gemini API キーが設定されていません"}
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": max_tokens,
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return {
                        "content": result['candidates'][0]['content']['parts'][0]['text'],
                        "usage": result.get('usageMetadata', {}),
                        "success": True
                    }
                else:
                    return {"error": "有効な応答が生成されませんでした"}
            else:
                return {
                    "error": f"API呼び出しエラー: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {"error": f"リクエスト失敗: {str(e)}"}
    
    def analyze_research_progress(self):
        """研究進捗を分析"""
        summary_file = self.research_root / "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        
        if not summary_file.exists():
            return {"error": "研究記録ファイルが見つかりません"}
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            research_content = f.read()
        
        prompt = f"""
以下の研究進捗記録を分析して、詳細なフィードバックと提案を日本語で提供してください：

{research_content}

分析項目：
1. 研究の学術的価値と独創性
2. 技術的成果の評価
3. 今後の研究方向性の提案
4. 論文投稿戦略
5. 改善すべき点

各項目について具体的で建設的なフィードバックを提供してください。
"""
        
        return self.generate_content(prompt)
    
    def suggest_next_session_agenda(self):
        """次回セッションの議題提案"""
        summary_file = self.research_root / "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        
        if not summary_file.exists():
            return {"error": "研究記録ファイルが見つかりません"}
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            research_content = f.read()
        
        # 現在の日付を取得
        current_date = datetime.now().strftime('%Y年%m月%d日')
        
        prompt = f"""
以下の研究進捗記録に基づいて、次回ディスカッション（{current_date}以降）の詳細な議題を提案してください：

{research_content}

提案形式：
1. 主要議題（3-5項目）
2. 準備すべき資料・データ
3. 検討すべき技術的課題
4. 学術発表に向けた準備項目
5. 具体的なToDoリスト

実用的で実行可能な提案を日本語で提供してください。
"""
        
        return self.generate_content(prompt)
    
    def evaluate_presentation_strategy(self):
        """発表戦略の評価と提案"""
        summary_file = self.research_root / "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        
        if not summary_file.exists():
            return {"error": "研究記録ファイルが見つかりません"}
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            research_content = f.read()
        
        prompt = f"""
以下の研究記録に基づいて、学術発表戦略を評価・提案してください：

{research_content}

評価・提案項目：
1. 中間発表（8月）の発表内容・構成提案
2. 卒業発表（2月）に向けた準備戦略
3. 国際会議投稿の可能性と対象会議
4. 研究の差別化ポイントと強調すべき点
5. 想定される質問と回答準備

学術的な観点から実践的なアドバイスを日本語で提供してください。
"""
        
        return self.generate_content(prompt)
    
    def analyze_technical_achievements(self):
        """技術的成果の詳細分析"""
        summary_file = self.research_root / "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        
        if not summary_file.exists():
            return {"error": "研究記録ファイルが見つかりません"}
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            research_content = f.read()
        
        prompt = f"""
以下の研究記録の技術的成果を詳細分析してください：

{research_content}

分析項目：
1. 技術的ブレークスルーの評価
2. 精度向上（87.1%、27.3%向上）の技術的意義
3. WordNet階層システムの独創性
4. AI技術統合の技術的価値
5. 他研究との差別化要因
6. 技術的限界と改善の方向性

技術的専門性を重視した分析を日本語で提供してください。
"""
        
        return self.generate_content(prompt)
    
    def chat_with_gemini(self, user_question):
        """Geminiとの対話"""
        summary_file = self.research_root / "study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md"
        
        context = ""
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                context = f.read()[:3000]  # 文脈として最初の3000文字
        
        prompt = f"""
研究コンテキスト：
{context}

質問：{user_question}

上記の研究記録を参考にして、質問に対して専門的で建設的な回答を日本語で提供してください。
"""
        
        return self.generate_content(prompt)
    
    def save_analysis_result(self, analysis_type, result):
        """分析結果を保存"""
        if not result.get('success'):
            return False
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"gemini_analysis_{analysis_type}_{timestamp}.md"
        output_file = self.research_root / f"ai_analysis/{filename}"
        
        # ディレクトリ作成
        output_file.parent.mkdir(exist_ok=True)
        
        content = f"""# Gemini AI 分析結果 - {analysis_type}

**生成日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}  
**分析タイプ**: {analysis_type}

---

{result['content']}

---

**使用量情報**:
- プロンプトトークン: {result.get('usage', {}).get('promptTokenCount', 'N/A')}
- 生成トークン: {result.get('usage', {}).get('candidatesTokenCount', 'N/A')}
- 合計トークン: {result.get('usage', {}).get('totalTokenCount', 'N/A')}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_file)

def main():
    """メイン関数"""
    import sys
    
    gemini = GeminiIntegration()
    
    if not gemini.api_key:
        print("❌ Gemini APIキーが設定されていません")
        print("📝 .envファイルにGEMINI_API_KEY=<your_key>を追加してください")
        return
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "progress":
            print("🔍 研究進捗を分析中...")
            result = gemini.analyze_research_progress()
            
        elif command == "agenda":
            print("📋 次回セッション議題を生成中...")
            result = gemini.suggest_next_session_agenda()
            
        elif command == "presentation":
            print("🎯 発表戦略を評価中...")
            result = gemini.evaluate_presentation_strategy()
            
        elif command == "technical":
            print("🔬 技術的成果を分析中...")
            result = gemini.analyze_technical_achievements()
            
        elif command == "chat":
            if len(sys.argv) > 2:
                question = " ".join(sys.argv[2:])
                print(f"💬 質問: {question}")
                result = gemini.chat_with_gemini(question)
            else:
                print("❌ 質問を入力してください")
                print("使用例: python3 gemini_integration.py chat '研究の次のステップは？'")
                return
                
        else:
            print("❌ 不明なコマンド")
            print_usage()
            return
    else:
        print_usage()
        return
    
    # 結果表示
    if result.get('success'):
        print("✅ 分析完了\n")
        print("=" * 80)
        print(result['content'])
        print("=" * 80)
        
        # 結果保存
        if len(sys.argv) > 1:
            saved_file = gemini.save_analysis_result(sys.argv[1], result)
            if saved_file:
                print(f"\n📄 分析結果を保存: {saved_file}")
        
        # 使用量表示
        if 'usage' in result:
            usage = result['usage']
            print(f"\n📊 使用量: プロンプト{usage.get('promptTokenCount', 0)} + "
                  f"生成{usage.get('candidatesTokenCount', 0)} = "
                  f"合計{usage.get('totalTokenCount', 0)}トークン")
    else:
        print(f"❌ エラー: {result.get('error')}")

def print_usage():
    """使用方法を表示"""
    print("🤖 Gemini AI 統合システム")
    print("=" * 40)
    print("使用法:")
    print("  python3 gemini_integration.py <command> [args]")
    print("")
    print("コマンド:")
    print("  progress     # 研究進捗分析")
    print("  agenda       # 次回セッション議題提案")
    print("  presentation # 発表戦略評価")
    print("  technical    # 技術的成果分析")
    print("  chat <質問>   # 対話形式質問")
    print("")
    print("例:")
    print("  python3 gemini_integration.py progress")
    print("  python3 gemini_integration.py chat '研究の強みは何ですか？'")

if __name__ == "__main__":
    main()