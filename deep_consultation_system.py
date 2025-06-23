#!/usr/bin/env python3
"""
深層相談システム - Claude CodeとGeminiの自動対話
納得いくまで自動的に質問を重ねて精度を向上
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class DeepConsultationSystem:
    """深層相談システム - 自動的に対話を重ねる"""
    
    def __init__(self):
        self.gemini_api_key = self._load_api_key()
        self.conversation_history = []
        self.max_depth = 5  # 最大相談回数
        
    def _load_api_key(self) -> str:
        env_file = '/mnt/c/Desktop/Research/.env'
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"')
        raise ValueError("GEMINI_API_KEY not found")
    
    def _call_gemini(self, prompt: str) -> str:
        """Gemini APIを呼び出す"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"エラー: {response.status_code}"
        except Exception as e:
            return f"接続エラー: {str(e)}"
    
    def _generate_followup_question(self, response: str, depth: int) -> str:
        """回答に基づいて追加質問を生成"""
        followup_prompt = f"""
以下の回答を分析し、より深い理解のための追加質問を1つ生成してください：

回答:
{response}

追加質問の条件:
1. 具体的な数値や根拠を求める
2. 実用的な応用方法を探る
3. 潜在的な問題点や限界を明確にする
4. 代替案や比較対象を検討する

深さレベル: {depth}/5
より本質的な質問を生成してください。
"""
        return self._call_gemini(followup_prompt)
    
    def _check_convergence(self, responses: List[str]) -> bool:
        """回答が収束したかチェック"""
        if len(responses) < 2:
            return False
        
        # 最新2つの回答を比較
        check_prompt = f"""
以下の2つの回答を比較し、十分な深さと具体性に達したか判定してください：

回答1:
{responses[-2][:500]}

回答2:
{responses[-1][:500]}

以下の基準で判定:
1. 具体的な数値や事例が含まれているか
2. 実践的な提案があるか
3. 限界や注意点が明確か

十分な深さに達した場合は「収束」、さらに深掘りが必要な場合は「継続」と回答してください。
"""
        
        result = self._call_gemini(check_prompt)
        return "収束" in result
    
    def deep_consult(self, initial_query: str, context: Dict = None) -> Dict:
        """深層相談を実行"""
        self.conversation_history = []
        responses = []
        questions = [initial_query]
        
        # 初期コンテキストを含める
        if context:
            current_query = f"{initial_query}\n\nコンテキスト: {json.dumps(context, ensure_ascii=False)}"
        else:
            current_query = initial_query
        
        print(f"🔍 深層相談開始: {initial_query}")
        
        for depth in range(self.max_depth):
            print(f"\n📊 深度 {depth + 1}/{self.max_depth}")
            
            # Geminiに質問
            response = self._call_gemini(current_query)
            responses.append(response)
            
            # 会話履歴に追加
            self.conversation_history.append({
                "depth": depth + 1,
                "question": current_query,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"💭 質問: {current_query[:100]}...")
            print(f"💡 回答: {response[:200]}...")
            
            # 収束チェック
            if depth >= 1 and self._check_convergence(responses):
                print("✅ 十分な深さに到達しました")
                break
            
            # 次の質問を生成
            if depth < self.max_depth - 1:
                followup = self._generate_followup_question(response, depth + 1)
                questions.append(followup)
                
                # 会話の文脈を含めた質問
                current_query = f"""
これまでの議論:
質問: {questions[-2]}
回答: {response[:300]}...

追加質問: {followup}
"""
        
        # 最終的な統合分析
        final_analysis = self._create_final_analysis(self.conversation_history)
        
        return {
            "initial_query": initial_query,
            "context": context,
            "conversation_depth": len(self.conversation_history),
            "conversation_history": self.conversation_history,
            "final_analysis": final_analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_final_analysis(self, history: List[Dict]) -> str:
        """対話履歴から最終分析を生成"""
        summary_prompt = f"""
以下の対話履歴から、重要なポイントを統合した最終分析を作成してください：

{json.dumps(history, ensure_ascii=False, indent=2)}

以下の形式でまとめてください：
1. 主要な発見
2. 実践的な推奨事項
3. 注意すべき制約
4. 今後の検討事項
"""
        
        return self._call_gemini(summary_prompt)
    
    def save_consultation(self, result: Dict, filename: str = None):
        """相談結果を保存"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"deep_consultation_{timestamp}.json"
        
        filepath = os.path.join("/mnt/c/Desktop/Research", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # レポートも生成
        report = self._generate_report(result)
        report_path = filepath.replace('.json', '_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath, report_path
    
    def _generate_report(self, result: Dict) -> str:
        """相談結果のレポート生成"""
        report = f"""# 深層相談レポート

**初期質問**: {result['initial_query']}  
**相談深度**: {result['conversation_depth']}回  
**実施日時**: {result['timestamp']}

## 対話の流れ

"""
        
        for item in result['conversation_history']:
            report += f"### 深度 {item['depth']}\n\n"
            report += f"**質問**: {item['question']}\n\n"
            report += f"**回答**: {item['response']}\n\n"
            report += "---\n\n"
        
        report += f"""## 最終統合分析

{result['final_analysis']}

## まとめ

この深層相談により、初期の質問から{result['conversation_depth']}段階の深掘りを行い、
より具体的で実践的な洞察を得ることができました。
"""
        
        return report

# グローバルインスタンス
_deep_system = None

def get_deep_system():
    global _deep_system
    if _deep_system is None:
        _deep_system = DeepConsultationSystem()
    return _deep_system

def deep_consult(query: str, context: Dict = None) -> Dict:
    """簡易インターフェース"""
    system = get_deep_system()
    return system.deep_consult(query, context)

# 使用例
if __name__ == "__main__":
    # テスト実行
    result = deep_consult(
        "画像分類の特化型アプローチで25.9%の精度向上を達成しました。この結果の意味は？",
        context={"カテゴリ数": 16, "統計的有意性": "Cohen's d=1.2"}
    )
    
    print("\n" + "="*60)
    print("🎯 最終統合分析:")
    print(result["final_analysis"])