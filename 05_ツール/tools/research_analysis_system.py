#!/usr/bin/env python3
"""
研究考察用AI分析システム
GeminiとClaude Codeの併用による多角的分析を実現
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class ResearchAnalysisSystem:
    """研究考察用のAI分析統合システム"""
    
    def __init__(self):
        self.gemini_api_key = self._load_api_key()
        self.analysis_results = []
        
    def _load_api_key(self) -> str:
        """APIキーの読み込み"""
        env_file = '/mnt/c/Desktop/Research/.env'
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"')
        raise ValueError("GEMINI_API_KEY not found")
    
    def analyze_with_gemini(self, prompt: str) -> Dict[str, any]:
        """Gemini APIを使用した分析"""
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
                content = result['candidates'][0]['content']['parts'][0]['text']
                return {
                    "status": "success",
                    "model": "Gemini 1.5 Flash",
                    "response": content,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "model": "Gemini 1.5 Flash",
                    "error": f"API Error: {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "error",
                "model": "Gemini 1.5 Flash",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def create_research_prompt(self, topic: str, data: Dict) -> str:
        """研究考察用のプロンプト生成"""
        prompt = f"""
研究テーマ: {topic}

実験データ:
{json.dumps(data, indent=2, ensure_ascii=False)}

以下の観点から学術的な考察を行ってください：

1. 実験結果の意義と解釈
2. 理論的含意と既存研究との関連
3. 研究の限界と課題
4. 今後の研究展望
5. 実用的応用の可能性

各観点について具体的かつ簡潔に分析してください。
"""
        return prompt
    
    def comparative_analysis(self, topic: str, data: Dict, claude_analysis: str = None) -> Dict:
        """複数のAIモデルによる比較分析"""
        prompt = self.create_research_prompt(topic, data)
        
        # Geminiによる分析
        gemini_result = self.analyze_with_gemini(prompt)
        
        analysis = {
            "topic": topic,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "analyses": {
                "gemini": gemini_result
            }
        }
        
        # Claude分析が提供されている場合は追加
        if claude_analysis:
            analysis["analyses"]["claude"] = {
                "status": "success",
                "model": "Claude Code",
                "response": claude_analysis,
                "timestamp": datetime.now().isoformat()
            }
        
        self.analysis_results.append(analysis)
        return analysis
    
    def generate_comparative_report(self, analysis: Dict) -> str:
        """比較分析レポートの生成"""
        report = f"""
# 研究考察比較分析レポート

**研究テーマ**: {analysis['topic']}  
**分析日時**: {analysis['timestamp']}

## 実験データ
```json
{json.dumps(analysis['data'], indent=2, ensure_ascii=False)}
```

## AI分析結果

"""
        
        for model_name, result in analysis['analyses'].items():
            report += f"### {result['model']}による分析\n\n"
            if result['status'] == 'success':
                report += result['response'] + "\n\n"
            else:
                report += f"エラー: {result.get('error', 'Unknown error')}\n\n"
        
        report += """
## 総合考察

各AIモデルの分析結果を踏まえ、以下の点が重要と考えられます：

1. **共通見解**: 両モデルが一致して指摘している点
2. **相違点**: モデル間で異なる視点や解釈
3. **補完的洞察**: 各モデルの独自の観点による貢献

これらの多角的な分析により、研究の深い理解と新たな洞察が得られます。
"""
        
        return report
    
    def save_analysis(self, analysis: Dict, filename: str = None):
        """分析結果の保存"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.json"
        
        filepath = os.path.join("/mnt/c/Desktop/Research", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        # レポートも生成・保存
        report = self.generate_comparative_report(analysis)
        report_filename = filename.replace('.json', '_report.md')
        report_filepath = os.path.join("/mnt/c/Desktop/Research", report_filename)
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath, report_filepath

# 使用例
if __name__ == "__main__":
    # システムの初期化
    system = ResearchAnalysisSystem()
    
    # サンプルデータ
    sample_data = {
        "特化型手法精度向上": "25.9%",
        "最適カテゴリ数": 16,
        "統計的有意性": {
            "Cohen's d": 1.2,
            "Statistical Power": 0.95
        },
        "理論モデル適合度": {
            "R²": 0.96
        }
    }
    
    # 分析実行
    print("🔬 研究考察分析システム起動")
    print("="*50)
    
    analysis = system.comparative_analysis(
        topic="画像分類における特化型アプローチの有効性",
        data=sample_data
    )
    
    # 結果保存
    json_path, report_path = system.save_analysis(analysis)
    
    print(f"✅ 分析完了")
    print(f"📄 JSONファイル: {json_path}")
    print(f"📝 レポートファイル: {report_path}")