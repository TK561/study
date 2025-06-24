#!/usr/bin/env python3
"""
インタラクティブ研究分析ツール
Claude CodeとGeminiの併用による対話的分析
"""

import os
import json
from datetime import datetime
from research_analysis_system import ResearchAnalysisSystem

class InteractiveAnalysis:
    """対話的な研究分析インターフェース"""
    
    def __init__(self):
        self.system = ResearchAnalysisSystem()
        self.current_session = {
            "start_time": datetime.now().isoformat(),
            "analyses": []
        }
    
    def display_menu(self):
        """メニュー表示"""
        print("\n" + "="*60)
        print("🔬 研究考察分析システム - Claude Code + Gemini")
        print("="*60)
        print("1. 新規分析の実行")
        print("2. カスタム質問による分析")
        print("3. 比較分析レポートの生成")
        print("4. 分析結果の保存")
        print("5. 終了")
        print("="*60)
    
    def get_research_data(self):
        """研究データの入力取得"""
        print("\n研究データを入力してください:")
        data = {}
        
        # 簡易入力モード
        print("簡易入力モードを使用しますか？ (y/n): ", end="")
        if input().lower() == 'y':
            data["精度向上"] = input("精度向上率 (例: 25.9%): ")
            data["最適パラメータ"] = input("最適パラメータ (例: カテゴリ数16): ")
            data["統計的有意性"] = input("統計的有意性 (例: Cohen's d=1.2): ")
            data["モデル適合度"] = input("モデル適合度 (例: R²=0.96): ")
        else:
            # JSON入力モード
            print("JSONフォーマットでデータを入力してください (終了は空行):")
            json_lines = []
            while True:
                line = input()
                if not line:
                    break
                json_lines.append(line)
            
            try:
                data = json.loads('\n'.join(json_lines))
            except json.JSONDecodeError:
                print("❌ JSONパースエラー。デフォルトデータを使用します。")
                data = {
                    "サンプルデータ": "デフォルト値",
                    "精度": "未定義"
                }
        
        return data
    
    def execute_analysis(self):
        """新規分析の実行"""
        print("\n📊 新規分析を開始します")
        
        topic = input("研究テーマを入力してください: ")
        data = self.get_research_data()
        
        print("\n🤖 Claude Codeによる考察を入力できます (スキップする場合は空行):")
        claude_lines = []
        while True:
            line = input()
            if not line:
                break
            claude_lines.append(line)
        
        claude_analysis = '\n'.join(claude_lines) if claude_lines else None
        
        print("\n🔄 分析を実行中...")
        analysis = self.system.comparative_analysis(topic, data, claude_analysis)
        
        print("\n✅ 分析完了！")
        self._display_analysis_summary(analysis)
        
        self.current_session["analyses"].append(analysis)
        return analysis
    
    def custom_question_analysis(self):
        """カスタム質問による分析"""
        print("\n💭 カスタム質問分析モード")
        
        question = input("質問を入力してください: ")
        context = input("関連する文脈情報 (オプション): ")
        
        prompt = f"{question}"
        if context:
            prompt += f"\n\n文脈情報: {context}"
        
        print("\n🔄 Geminiに質問中...")
        result = self.system.analyze_with_gemini(prompt)
        
        if result['status'] == 'success':
            print("\n📝 Geminiの回答:")
            print("-" * 40)
            print(result['response'])
            print("-" * 40)
        else:
            print(f"\n❌ エラー: {result['error']}")
        
        # 分析履歴に追加
        custom_analysis = {
            "type": "custom_question",
            "question": question,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        self.current_session["analyses"].append(custom_analysis)
    
    def _display_analysis_summary(self, analysis):
        """分析結果のサマリー表示"""
        print("\n" + "="*50)
        print(f"📋 分析サマリー")
        print(f"テーマ: {analysis['topic']}")
        print(f"時刻: {analysis['timestamp']}")
        print("="*50)
        
        for model_name, result in analysis['analyses'].items():
            print(f"\n【{result['model']}】")
            if result['status'] == 'success':
                # 最初の200文字を表示
                preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
                print(preview)
            else:
                print(f"エラー: {result.get('error', 'Unknown error')}")
    
    def save_session(self):
        """セッション結果の保存"""
        if not self.current_session["analyses"]:
            print("❌ 保存する分析結果がありません")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.json"
        filepath = os.path.join("/mnt/c/Desktop/Research", filename)
        
        self.current_session["end_time"] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.current_session, f, ensure_ascii=False, indent=2)
        
        print(f"✅ セッションを保存しました: {filepath}")
        
        # 最新の分析についてレポートも生成
        if self.current_session["analyses"]:
            latest = self.current_session["analyses"][-1]
            if isinstance(latest, dict) and 'analyses' in latest:
                report = self.system.generate_comparative_report(latest)
                report_path = filepath.replace('.json', '_report.md')
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"📝 レポートも生成しました: {report_path}")
    
    def run(self):
        """メインループ"""
        print("🚀 インタラクティブ研究分析ツールを起動しました")
        
        while True:
            self.display_menu()
            choice = input("\n選択してください (1-5): ")
            
            if choice == '1':
                self.execute_analysis()
            elif choice == '2':
                self.custom_question_analysis()
            elif choice == '3':
                if self.current_session["analyses"]:
                    latest = self.current_session["analyses"][-1]
                    if isinstance(latest, dict) and 'analyses' in latest:
                        report = self.system.generate_comparative_report(latest)
                        print("\n📄 比較分析レポート:")
                        print(report)
                    else:
                        print("❌ 比較分析可能なデータがありません")
                else:
                    print("❌ 分析結果がありません")
            elif choice == '4':
                self.save_session()
            elif choice == '5':
                print("\n👋 終了します")
                self.save_session()
                break
            else:
                print("❌ 無効な選択です")

if __name__ == "__main__":
    app = InteractiveAnalysis()
    app.run()