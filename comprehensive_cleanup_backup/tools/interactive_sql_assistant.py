#!/usr/bin/env python3
"""
インタラクティブSQL アシスタント - Geminiを使った対話型SQL生成
"""

import os
import json
import sqlite3
from typing import Dict, List, Optional, Any
from datetime import datetime
from gemini_to_sql_system import GeminiToSQLSystem
from advanced_gemini_sql_features import AdvancedGeminiSQLFeatures
from deep_consultation_system import DeepConsultationSystem

class InteractiveSQLAssistant:
    """対話型SQL生成アシスタント"""
    
    def __init__(self):
        self.base_system = GeminiToSQLSystem()
        self.advanced_system = AdvancedGeminiSQLFeatures()
        self.deep_consult = DeepConsultationSystem()
        self.session_history = []
        self.current_context = {}
        self.saved_queries = {}
        
    def start_session(self):
        """インタラクティブセッションを開始"""
        print("\n🤖 Gemini SQL Assistant へようこそ！")
        print("=" * 60)
        print("自然言語でデータベース操作を記述してください。")
        print("コマンド: /help, /schema, /history, /save, /load, /exit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n📝 SQL生成リクエスト> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                else:
                    self._process_request(user_input)
                    
            except KeyboardInterrupt:
                print("\n\n👋 セッションを終了します。")
                break
            except Exception as e:
                print(f"\n❌ エラー: {str(e)}")
    
    def _handle_command(self, command: str):
        """コマンドを処理"""
        cmd_parts = command.split()
        cmd = cmd_parts[0].lower()
        
        if cmd == '/help':
            self._show_help()
        elif cmd == '/schema':
            self._manage_schema()
        elif cmd == '/history':
            self._show_history()
        elif cmd == '/save':
            if len(cmd_parts) > 1:
                self._save_query(cmd_parts[1])
            else:
                print("❌ クエリ名を指定してください: /save <name>")
        elif cmd == '/load':
            if len(cmd_parts) > 1:
                self._load_query(cmd_parts[1])
            else:
                self._list_saved_queries()
        elif cmd == '/analyze':
            self._analyze_last_query()
        elif cmd == '/optimize':
            self._optimize_last_query()
        elif cmd == '/explain':
            self._explain_last_query()
        elif cmd == '/test':
            self._test_last_query()
        elif cmd == '/export':
            self._export_session()
        elif cmd == '/exit':
            raise KeyboardInterrupt
        else:
            print(f"❌ 不明なコマンド: {cmd}")
    
    def _show_help(self):
        """ヘルプを表示"""
        help_text = """
📚 利用可能なコマンド:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

基本コマンド:
  /help         - このヘルプを表示
  /exit         - セッションを終了
  
スキーマ管理:
  /schema       - スキーマを設定・表示
  
履歴・保存:
  /history      - 生成履歴を表示
  /save <name>  - 最後のクエリを保存
  /load <name>  - 保存したクエリを読み込み
  /export       - セッションをエクスポート
  
分析・最適化:
  /analyze      - 最後のクエリを分析
  /optimize     - 最後のクエリを最適化
  /explain      - 最後のクエリを詳しく説明
  /test         - 最後のクエリをテスト実行

使用例:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 基本的なクエリ生成:
   > ユーザーテーブルから東京在住の人を検索
   
2. 複雑なクエリ:
   > 過去3ヶ月の売上を商品カテゴリ別に集計して上位10件を表示
   
3. データ操作:
   > 在庫数が10未満の商品の価格を10%値上げ
   
4. テーブル作成:
   > 顧客の購買履歴を記録するテーブルを作成

高度な機能:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 自動的にスキーマ情報を考慮
- 複数のSQL方言に対応
- パフォーマンス最適化提案
- セキュリティチェック
- テストデータ生成
        """
        print(help_text)
    
    def _manage_schema(self):
        """スキーマ管理"""
        print("\n📊 スキーマ管理")
        print("1. 現在のスキーマを表示")
        print("2. 新しいテーブルを追加")
        print("3. スキーマをインポート")
        print("4. スキーマをリセット")
        
        choice = input("\n選択 (1-4): ").strip()
        
        if choice == '1':
            if self.current_context.get('schema'):
                print("\n現在のスキーマ:")
                print(json.dumps(self.current_context['schema'], 
                               ensure_ascii=False, indent=2))
            else:
                print("スキーマが設定されていません。")
        
        elif choice == '2':
            table_name = input("テーブル名: ").strip()
            columns = []
            
            print("カラムを追加 (空行で終了):")
            while True:
                col_def = input("カラム名 データ型 [制約]: ").strip()
                if not col_def:
                    break
                columns.append(col_def)
            
            if columns:
                if 'schema' not in self.current_context:
                    self.current_context['schema'] = {}
                
                self.current_context['schema'][table_name] = {
                    'columns': columns
                }
                print(f"✅ テーブル '{table_name}' を追加しました。")
        
        elif choice == '3':
            file_path = input("スキーマファイルのパス: ").strip()
            try:
                with open(file_path, 'r') as f:
                    self.current_context['schema'] = json.load(f)
                print("✅ スキーマをインポートしました。")
            except Exception as e:
                print(f"❌ インポート失敗: {str(e)}")
        
        elif choice == '4':
            self.current_context['schema'] = {}
            print("✅ スキーマをリセットしました。")
    
    def _process_request(self, request: str):
        """SQLリクエストを処理"""
        print("\n🔄 処理中...")
        
        # 深層相談を使うか確認
        use_deep = False
        if any(word in request for word in ['複雑', '詳細', '高度', '最適化']):
            response = input("\n🤔 詳細な相談を行いますか？ (y/n): ").strip().lower()
            use_deep = response == 'y'
        
        # SQL生成
        result = self.base_system.generate_sql(
            request, 
            self.current_context.get('schema'),
            use_deep_consultation=use_deep
        )
        
        # 結果を保存
        self.session_history.append({
            'request': request,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        # SQL表示
        if result.get('sql'):
            print("\n✨ 生成されたSQL:")
            print("=" * 60)
            print(result['sql'])
            print("=" * 60)
            
            # 検証結果
            if 'validation' in result:
                validation = result['validation']
                if validation.get('issues'):
                    print("\n⚠️  検証で問題が見つかりました:")
                    for issue in validation['issues']:
                        print(f"  - {issue}")
            
            # 説明の一部を表示
            if result.get('explanation'):
                lines = result['explanation'].split('\n')
                explanation_preview = '\n'.join(lines[:10])
                print(f"\n📖 説明:\n{explanation_preview}")
                
                if len(lines) > 10:
                    show_full = input("\n全文を表示しますか？ (y/n): ").strip().lower()
                    if show_full == 'y':
                        print(result['explanation'])
        else:
            print("\n❌ SQL生成に失敗しました。")
            print(result.get('explanation', 'エラーが発生しました。'))
    
    def _show_history(self):
        """履歴を表示"""
        if not self.session_history:
            print("\n履歴がありません。")
            return
        
        print("\n📜 生成履歴:")
        print("=" * 60)
        
        for i, item in enumerate(self.session_history[-10:], 1):
            print(f"\n[{i}] {item['timestamp']}")
            print(f"リクエスト: {item['request']}")
            if item['result'].get('sql'):
                sql_preview = item['result']['sql'].split('\n')[0][:50]
                print(f"SQL: {sql_preview}...")
    
    def _save_query(self, name: str):
        """クエリを保存"""
        if not self.session_history:
            print("保存するクエリがありません。")
            return
        
        last_item = self.session_history[-1]
        self.saved_queries[name] = last_item
        
        # ファイルに保存
        save_file = f"saved_queries_{datetime.now().strftime('%Y%m%d')}.json"
        with open(save_file, 'w', encoding='utf-8') as f:
            json.dump(self.saved_queries, f, ensure_ascii=False, indent=2)
        
        print(f"✅ クエリ '{name}' を保存しました。")
    
    def _load_query(self, name: str):
        """保存したクエリを読み込み"""
        if name in self.saved_queries:
            item = self.saved_queries[name]
            print(f"\n📂 保存されたクエリ '{name}':")
            print(f"リクエスト: {item['request']}")
            print(f"SQL:\n{item['result']['sql']}")
        else:
            print(f"❌ クエリ '{name}' が見つかりません。")
    
    def _list_saved_queries(self):
        """保存されたクエリ一覧"""
        if not self.saved_queries:
            print("\n保存されたクエリがありません。")
            return
        
        print("\n💾 保存されたクエリ:")
        for name, item in self.saved_queries.items():
            print(f"  - {name}: {item['request'][:50]}...")
    
    def _analyze_last_query(self):
        """最後のクエリを分析"""
        if not self.session_history:
            print("分析するクエリがありません。")
            return
        
        last_sql = self.session_history[-1]['result'].get('sql')
        if not last_sql:
            print("SQLが生成されていません。")
            return
        
        print("\n🔍 クエリ分析中...")
        analysis = self.advanced_system.analyze_query_plan(last_sql)
        
        print("\n📊 分析結果:")
        print(analysis['analysis'][:500])
        
        if analysis.get('optimization_suggestions'):
            print("\n💡 最適化提案:")
            for suggestion in analysis['optimization_suggestions']:
                print(f"  - {suggestion}")
    
    def _optimize_last_query(self):
        """最後のクエリを最適化"""
        if not self.session_history:
            print("最適化するクエリがありません。")
            return
        
        last_sql = self.session_history[-1]['result'].get('sql')
        if not last_sql:
            print("SQLが生成されていません。")
            return
        
        print("\n⚡ クエリ最適化中...")
        optimization = self.base_system.optimize_sql(
            last_sql, 
            self.current_context.get('schema')
        )
        
        print("\n✨ 最適化されたSQL:")
        print("=" * 60)
        print(optimization['optimized_sql'])
        print("=" * 60)
        
        if optimization['optimized_sql'] != last_sql:
            print("\n📈 改善点:")
            # 説明から改善点を抽出して表示
            explanation_lines = optimization['explanation'].split('\n')
            for line in explanation_lines:
                if any(keyword in line for keyword in ['改善', '最適化', '変更']):
                    print(f"  {line.strip()}")
    
    def _explain_last_query(self):
        """最後のクエリを詳しく説明"""
        if not self.session_history:
            print("説明するクエリがありません。")
            return
        
        last_sql = self.session_history[-1]['result'].get('sql')
        if not last_sql:
            print("SQLが生成されていません。")
            return
        
        print("\n📚 クエリの詳細説明:")
        explanation = self.base_system.explain_sql(last_sql)
        print(explanation)
    
    def _test_last_query(self):
        """最後のクエリをテスト実行"""
        if not self.session_history:
            print("テストするクエリがありません。")
            return
        
        last_sql = self.session_history[-1]['result'].get('sql')
        if not last_sql:
            print("SQLが生成されていません。")
            return
        
        print("\n🧪 テスト実行")
        print("注意: これはメモリ内SQLiteでの実行です。")
        
        try:
            # メモリ内SQLiteで実行
            conn = sqlite3.connect(':memory:')
            
            # 簡単なテストテーブルを作成
            if 'CREATE TABLE' not in last_sql.upper():
                # SELECTクエリの場合、ダミーテーブルを作成
                self._create_test_tables(conn)
            
            # クエリ実行
            cursor = conn.cursor()
            cursor.execute(last_sql)
            
            if last_sql.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                print(f"\n結果: {len(results)}行")
                if results:
                    # 最初の数行を表示
                    for i, row in enumerate(results[:5]):
                        print(f"  {row}")
                    if len(results) > 5:
                        print(f"  ... 他 {len(results) - 5} 行")
            else:
                conn.commit()
                print("✅ クエリが正常に実行されました。")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ 実行エラー: {str(e)}")
    
    def _create_test_tables(self, conn):
        """テスト用のダミーテーブルを作成"""
        # 一般的なテーブルを作成
        test_tables = [
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                age INTEGER,
                created_date DATETIME
            )
            """,
            """
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price DECIMAL(10,2),
                category TEXT,
                stock INTEGER
            )
            """,
            """
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                order_date DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            """
        ]
        
        cursor = conn.cursor()
        for table_sql in test_tables:
            try:
                cursor.execute(table_sql)
            except:
                pass  # テーブルが既に存在する場合は無視
        
        conn.commit()
    
    def _export_session(self):
        """セッションをエクスポート"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sql_session_{timestamp}.json"
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'schema': self.current_context.get('schema', {}),
            'history': self.session_history,
            'saved_queries': self.saved_queries
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ セッションを {filename} にエクスポートしました。")


def quick_sql(request: str, schema: Optional[Dict] = None):
    """クイックSQL生成関数"""
    system = GeminiToSQLSystem()
    result = system.generate_sql(request, schema, use_deep_consultation=False)
    
    if result.get('sql'):
        print(result['sql'])
        return result['sql']
    else:
        print("SQL生成に失敗しました。")
        return None


def main():
    """メイン関数"""
    import sys
    
    if len(sys.argv) > 1:
        # コマンドライン引数がある場合は、クイック実行
        request = ' '.join(sys.argv[1:])
        quick_sql(request)
    else:
        # インタラクティブモード
        assistant = InteractiveSQLAssistant()
        assistant.start_session()


if __name__ == "__main__":
    main()