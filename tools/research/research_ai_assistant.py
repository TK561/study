#!/usr/bin/env python3
"""
研究AI アシスタント - メインインターフェース
GeminiとSQL機能を統合した研究支援システム
"""

import os
import sys
from typing import Dict, List, Optional, Any
from integrated_research_toolkit import IntegratedResearchToolkit
from research_sql_system import ResearchSQLSystem
from gemini_sql_toolkit import GeminiSQLToolkit

class ResearchAIAssistant:
    """研究AI アシスタント メインクラス"""
    
    def __init__(self):
        self.toolkit = IntegratedResearchToolkit()
        self.current_session = {
            'experiments': [],
            'analyses': [],
            'insights': []
        }
        
    def start_interactive_session(self):
        """インタラクティブセッションを開始"""
        
        print("\n🤖 研究AI アシスタント へようこそ！")
        print("=" * 60)
        print("🔬 Gemini×SQL powered 研究支援システム")
        print("=" * 60)
        print("\n利用可能なコマンド:")
        print("  📊 analyze <質問>     - データ分析・相談")
        print("  🧪 experiment <説明>  - 実験設計支援")
        print("  🔍 explore <目標>     - データ探索")
        print("  💡 insights <実験ID>  - 研究洞察生成")
        print("  📈 sql <自然言語>     - SQL生成")
        print("  📋 status            - 現在の状況確認")
        print("  💾 export <実験ID>    - データエクスポート")
        print("  🏃 quick <タスク>     - クイック実行")
        print("  ❓ help              - ヘルプ表示")
        print("  🚪 exit              - 終了")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🎯 研究AI> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    self._save_and_exit()
                    break
                
                self._process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 セッションを終了します。")
                self._save_and_exit()
                break
            except Exception as e:
                print(f"\n❌ エラー: {str(e)}")
    
    def _process_command(self, command: str):
        """コマンドを処理"""
        
        parts = command.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'analyze':
            self._handle_analyze(args)
        elif cmd == 'experiment':
            self._handle_experiment(args)
        elif cmd == 'explore':
            self._handle_explore(args)
        elif cmd == 'insights':
            self._handle_insights(args)
        elif cmd == 'sql':
            self._handle_sql(args)
        elif cmd == 'status':
            self._handle_status()
        elif cmd == 'export':
            self._handle_export(args)
        elif cmd == 'quick':
            self._handle_quick(args)
        elif cmd == 'help':
            self._show_detailed_help()
        else:
            print(f"❌ 不明なコマンド: {cmd}")
            print("💡 'help' で利用可能なコマンドを確認してください。")
    
    def _handle_analyze(self, request: str):
        """データ分析リクエストを処理"""
        
        if not request:
            print("❌ 分析内容を指定してください。例: analyze カテゴリ別の性能差")
            return
        
        print(f"\n🔍 分析中: {request}")
        print("⏳ Geminiと相談しています...")
        
        try:
            result = self.toolkit.analyze_research_data_with_gemini(request)
            
            print("\n📊 分析結果:")
            if isinstance(result, dict) and 'final_answer' in result:
                print(result['final_answer'][:1000] + "..." if len(result['final_answer']) > 1000 else result['final_answer'])
            else:
                print(str(result)[:1000] + "..." if len(str(result)) > 1000 else str(result))
            
            self.current_session['analyses'].append({
                'request': request,
                'result': result
            })
            
            print("\n💡 追加分析が必要な場合は、'explore' コマンドをお試しください。")
            
        except Exception as e:
            print(f"❌ 分析エラー: {str(e)}")
    
    def _handle_experiment(self, description: str):
        """実験設計支援を処理"""
        
        if not description:
            print("❌ 実験の説明を入力してください。例: experiment 新しいモデルの性能評価")
            return
        
        print(f"\n🧪 実験設計中: {description}")
        print("⏳ Geminiと実験設計を相談しています...")
        
        try:
            setup_result = self.toolkit.smart_experiment_setup(description)
            
            print("\n✨ 実験設計提案:")
            
            if 'consultation_result' in setup_result:
                consultation = setup_result['consultation_result']
                if isinstance(consultation, dict) and 'final_answer' in consultation:
                    print(consultation['final_answer'][:800] + "...")
                else:
                    print(str(consultation)[:800] + "...")
            
            if 'experiment_template' in setup_result:
                template = setup_result['experiment_template']
                print(f"\n📋 実験テンプレート:")
                print(f"  実験名: {template['experiment_name']}")
                print(f"  説明: {template['description']}")
                print(f"  パラメータ: {template['parameters']}")
            
            self.current_session['experiments'].append({
                'description': description,
                'setup_result': setup_result
            })
            
            print("\n💡 実験を開始するには、このテンプレートを使用してデータを投入してください。")
            
        except Exception as e:
            print(f"❌ 実験設計エラー: {str(e)}")
    
    def _handle_explore(self, goal: str):
        """データ探索を処理"""
        
        if not goal:
            print("❌ 探索目標を指定してください。例: explore 処理時間とカテゴリの関係")
            return
        
        print(f"\n🔍 データ探索: {goal}")
        print("⏳ 探索戦略を策定しています...")
        
        try:
            exploration_result = self.toolkit.intelligent_data_exploration(goal)
            
            print("\n📈 探索結果:")
            
            if 'executed_queries' in exploration_result:
                queries = exploration_result['executed_queries']
                print(f"\n実行されたクエリ数: {len(queries)}")
                
                for query_id, query_data in queries.items():
                    print(f"\n{query_id}:")
                    if 'error' in query_data:
                        print(f"  エラー: {query_data['error']}")
                    else:
                        print(f"  結果数: {query_data['row_count']}行")
                        if query_data['results']:
                            print(f"  サンプル: {query_data['results'][0]}")
            
            # 探索戦略の表示
            if 'exploration_strategy' in exploration_result:
                strategy = exploration_result['exploration_strategy']
                if isinstance(strategy, dict) and 'final_answer' in strategy:
                    print(f"\n🎯 探索戦略:\n{strategy['final_answer'][:600]}...")
            
        except Exception as e:
            print(f"❌ 探索エラー: {str(e)}")
    
    def _handle_insights(self, experiment_ids: str):
        """研究洞察生成を処理"""
        
        if not experiment_ids:
            # 利用可能な実験IDを表示
            cursor = self.toolkit.research_sql.conn.cursor()
            cursor.execute("SELECT experiment_id, experiment_name FROM experiments LIMIT 5")
            experiments = cursor.fetchall()
            
            if experiments:
                print("\n📋 利用可能な実験:")
                for exp in experiments:
                    print(f"  {exp['experiment_id']}: {exp['experiment_name']}")
                print("\n💡 例: insights exp_20250622_120000")
            else:
                print("❌ 利用可能な実験がありません。まず実験データを作成してください。")
            return
        
        exp_ids = [id.strip() for id in experiment_ids.split(',')]
        
        print(f"\n💡 研究洞察生成中: {len(exp_ids)}個の実験")
        print("⏳ 実験結果を分析しています...")
        
        try:
            insights = self.toolkit.generate_research_insights(exp_ids)
            
            print("\n🌟 研究洞察:")
            
            if 'research_insights' in insights:
                insight_result = insights['research_insights']
                if isinstance(insight_result, dict) and 'final_answer' in insight_result:
                    print(insight_result['final_answer'][:1200] + "...")
                else:
                    print(str(insight_result)[:1200] + "...")
            
            self.current_session['insights'].append({
                'experiment_ids': exp_ids,
                'insights': insights
            })
            
        except Exception as e:
            print(f"❌ 洞察生成エラー: {str(e)}")
    
    def _handle_sql(self, natural_request: str):
        """SQL生成を処理"""
        
        if not natural_request:
            print("❌ SQL生成したい内容を指定してください。例: sql 最新の実験結果を取得")
            return
        
        print(f"\n🤖 SQL生成: {natural_request}")
        
        try:
            result = self.toolkit.research_sql.generate_research_query(natural_request)
            
            if result.get('sql'):
                print(f"\n✨ 生成されたSQL:")
                print("=" * 50)
                print(result['sql'])
                print("=" * 50)
                
                # 実行するか確認
                execute = input("\nこのSQLを実行しますか？ (y/n): ").strip().lower()
                if execute == 'y':
                    try:
                        cursor = self.toolkit.research_sql.conn.cursor()
                        cursor.execute(result['sql'])
                        results = cursor.fetchall()
                        
                        print(f"\n📊 実行結果: {len(results)}行")
                        for i, row in enumerate(results[:5]):
                            print(f"  {i+1}: {dict(row)}")
                        
                        if len(results) > 5:
                            print(f"  ... 他 {len(results) - 5} 行")
                    
                    except Exception as e:
                        print(f"❌ SQL実行エラー: {str(e)}")
            else:
                print("❌ SQL生成に失敗しました。")
                if result.get('explanation'):
                    print(f"説明: {result['explanation'][:300]}...")
        
        except Exception as e:
            print(f"❌ SQL生成エラー: {str(e)}")
    
    def _handle_status(self):
        """現在の状況を表示"""
        
        print("\n📊 現在の研究状況")
        print("=" * 40)
        
        # データベース統計
        cursor = self.toolkit.research_sql.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM experiments")
        exp_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM predictions")
        pred_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(DISTINCT experiment_id) as count FROM experiment_statistics")
        stats_count = cursor.fetchone()['count']
        
        print(f"📁 データベース:")
        print(f"  実験数: {exp_count}")
        print(f"  予測数: {pred_count}")
        print(f"  統計済実験: {stats_count}")
        
        # セッション状況
        print(f"\n🔄 現在のセッション:")
        print(f"  分析数: {len(self.current_session['analyses'])}")
        print(f"  実験設計数: {len(self.current_session['experiments'])}")
        print(f"  洞察生成数: {len(self.current_session['insights'])}")
        
        # 最新の実験
        cursor.execute("""
        SELECT experiment_id, experiment_name, created_at 
        FROM experiments 
        ORDER BY created_at DESC 
        LIMIT 3
        """)
        
        recent_experiments = cursor.fetchall()
        
        if recent_experiments:
            print(f"\n🕐 最新の実験:")
            for exp in recent_experiments:
                print(f"  {exp['experiment_id']}: {exp['experiment_name']} ({exp['created_at']})")
    
    def _handle_export(self, experiment_id: str):
        """データエクスポートを処理"""
        
        if not experiment_id:
            print("❌ エクスポートする実験IDを指定してください。例: export exp_20250622_120000")
            return
        
        print(f"\n💾 エクスポート中: {experiment_id}")
        
        try:
            exported_file = self.toolkit.research_sql.export_experiment_data(experiment_id)
            print(f"✅ エクスポート完了: {exported_file}")
            
        except Exception as e:
            print(f"❌ エクスポートエラー: {str(e)}")
    
    def _handle_quick(self, task: str):
        """クイックタスクを処理"""
        
        if not task:
            print("❌ タスクを指定してください。例: quick 最新実験の精度チェック")
            return
        
        print(f"\n⚡ クイック実行: {task}")
        
        # 一般的なタスクのショートカット
        if '精度' in task or 'accuracy' in task.lower():
            cursor = self.toolkit.research_sql.conn.cursor()
            cursor.execute("""
            SELECT e.experiment_name, es.metric_value as accuracy
            FROM experiments e
            JOIN experiment_statistics es ON e.experiment_id = es.experiment_id
            WHERE es.metric_name = 'accuracy'
            ORDER BY e.created_at DESC
            LIMIT 5
            """)
            
            results = cursor.fetchall()
            if results:
                print("\n📈 最新実験の精度:")
                for result in results:
                    print(f"  {result['experiment_name']}: {result['accuracy']:.4f}")
            else:
                print("❌ 精度データが見つかりません。")
        
        elif 'カテゴリ' in task or 'category' in task.lower():
            cursor = self.toolkit.research_sql.conn.cursor()
            cursor.execute("""
            SELECT category_name, COUNT(*) as count
            FROM categories c
            JOIN predictions p ON c.category_id = p.predicted_category_id
            GROUP BY c.category_id, c.category_name
            ORDER BY count DESC
            """)
            
            results = cursor.fetchall()
            if results:
                print("\n📊 カテゴリ別予測数:")
                for result in results:
                    print(f"  {result['category_name']}: {result['count']}件")
            else:
                print("❌ カテゴリデータが見つかりません。")
        
        else:
            # 一般的な分析として処理
            self._handle_analyze(task)
    
    def _show_detailed_help(self):
        """詳細ヘルプを表示"""
        
        help_text = """
🤖 研究AI アシスタント - 詳細ヘルプ
════════════════════════════════════════════════════════════════

📊 analyze <質問>
    現在の研究データについてGeminiと相談しながら分析
    例: analyze カテゴリ別の性能差を調べたい
        analyze 処理時間の統計的特徴を知りたい

🧪 experiment <説明>
    新しい実験の設計をGeminiと相談して最適化
    例: experiment 新しいモデルの性能評価実験
        experiment データ拡張の効果を測定する実験

🔍 explore <目標>
    データベースから特定の目標に沿ってデータを探索
    例: explore 確信度と精度の関係を調べたい
        explore 処理時間のボトルネックを特定したい

💡 insights <実験ID>
    実験結果から研究的洞察をGeminiと協力して生成
    例: insights exp_20250622_120000
        insights exp_001,exp_002,exp_003

📈 sql <自然言語>
    自然言語から研究データ用のSQLを自動生成・実行
    例: sql 最新の実験結果を取得
        sql カテゴリ別の平均確信度を計算

📋 status
    現在のデータベース状況とセッション状況を表示

💾 export <実験ID>
    指定した実験のデータをJSONファイルにエクスポート

🏃 quick <タスク>
    よく使われるタスクのショートカット実行
    例: quick 最新実験の精度チェック
        quick カテゴリ別統計

❓ help
    このヘルプを表示

🚪 exit
    セッションを保存して終了

════════════════════════════════════════════════════════════════
💡 ヒント:
  - コマンドは部分入力でも認識されます
  - エラーが発生した場合は、別の表現で再試行してください
  - 長い結果は自動的に省略されます
        """
        
        print(help_text)
    
    def _save_and_exit(self):
        """セッションを保存して終了"""
        
        print("\n💾 セッションを保存中...")
        
        try:
            saved_file = self.toolkit.save_session_log()
            print(f"✅ セッション保存完了: {saved_file}")
        except Exception as e:
            print(f"⚠️ セッション保存エラー: {str(e)}")
        
        self.toolkit.close()
        print("\n👋 研究AI アシスタントを終了しました。")
        print("🚀 次回もぜひご利用ください！")


def main():
    """メイン関数"""
    
    if len(sys.argv) > 1:
        # コマンドライン引数がある場合
        command = ' '.join(sys.argv[1:])
        
        assistant = ResearchAIAssistant()
        
        if command.lower() in ['help', '--help', '-h']:
            assistant._show_detailed_help()
        elif command.startswith('sql '):
            assistant._handle_sql(command[4:])
        elif command.startswith('analyze '):
            assistant._handle_analyze(command[8:])
        elif command.startswith('quick '):
            assistant._handle_quick(command[6:])
        else:
            print(f"🤖 研究AI実行: {command}")
            assistant._handle_analyze(command)
        
        assistant.toolkit.close()
    
    else:
        # インタラクティブモード
        assistant = ResearchAIAssistant()
        assistant.start_interactive_session()


if __name__ == "__main__":
    main()