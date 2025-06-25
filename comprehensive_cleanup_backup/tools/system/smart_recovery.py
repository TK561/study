#!/usr/bin/env python3
"""
スマート復元システム
作業内容を理解しやすくまとめて表示
"""

import os
import json
from datetime import datetime
from collections import defaultdict
from deep_consultation_system import deep_consult

def analyze_session_context(session):
    """セッションの内容を分析して文脈を理解"""
    
    # ファイル操作を分析
    file_groups = defaultdict(list)
    for action in session.get('actions', []):
        if action['type'] == 'file_operation':
            file_path = action['details']['file_path']
            file_name = os.path.basename(file_path)
            
            # ファイルタイプで分類
            if file_name.endswith('.py'):
                if 'gemini' in file_name.lower():
                    file_groups['Gemini統合'].append(action)
                elif 'recovery' in file_name.lower() or 'session' in file_name.lower():
                    file_groups['復元システム'].append(action)
                elif 'vercel' in file_name.lower():
                    file_groups['Vercelデプロイ'].append(action)
                else:
                    file_groups['Pythonスクリプト'].append(action)
            elif file_name.endswith('.md'):
                file_groups['ドキュメント'].append(action)
            elif file_name.endswith('.json'):
                file_groups['設定・データ'].append(action)
    
    return file_groups

def smart_recover():
    """スマートな復元と作業内容の要約"""
    from session_recovery_system import get_recovery_system
    system = get_recovery_system()
    session = system.recover_last_session()
    
    if "error" in session:
        print("復元可能なセッションがありません")
        return
    
    print("✅ セッション復元完了\n")
    
    # セッション期間
    start_time = datetime.fromisoformat(session.get('start_time', ''))
    last_time = datetime.fromisoformat(session.get('last_updated', ''))
    duration = last_time - start_time
    
    print(f"📅 作業期間: {start_time.strftime('%Y年%m月%d日 %H:%M')} ～ {last_time.strftime('%H:%M')}")
    print(f"⏱️ 作業時間: 約{int(duration.total_seconds() / 60)}分\n")
    
    # 作業内容を分析
    file_groups = analyze_session_context(session)
    
    # 今日の作業内容をGeminiに分析してもらう
    work_summary = []
    
    if 'Vercelデプロイ' in file_groups:
        work_summary.append("🌐 Vercelへのデプロイ作業")
        files = [os.path.basename(a['details']['file_path']) for a in file_groups['Vercelデプロイ']]
        work_summary.append(f"   関連ファイル: {', '.join(set(files))}")
    
    if 'Gemini統合' in file_groups:
        work_summary.append("🤖 Gemini API統合システムの構築")
        files = [os.path.basename(a['details']['file_path']) for a in file_groups['Gemini統合']]
        work_summary.append(f"   関連ファイル: {', '.join(set(files))}")
    
    if '復元システム' in file_groups:
        work_summary.append("🔄 セッション復元システムの実装")
        files = [os.path.basename(a['details']['file_path']) for a in file_groups['復元システム']]
        work_summary.append(f"   関連ファイル: {', '.join(set(files))}")
    
    # まとめを表示
    print("📋 実施した作業内容:")
    for item in work_summary:
        print(item)
    
    # 詳細な内容をGeminiで分析（必要に応じて）
    if len(session.get('actions', [])) > 10:
        print("\n🔍 作業の詳細分析中...")
        
        # ファイル名リストを作成
        all_files = []
        for action in session.get('actions', []):
            if action['type'] == 'file_operation':
                all_files.append(os.path.basename(action['details']['file_path']))
        
        analysis_prompt = f"""
以下のファイルを作成・編集した作業セッションがあります：
{', '.join(set(all_files))}

これらのファイル名から、どのような作業を行ったか簡潔に3行でまとめてください。
技術的な詳細ではなく、何を目的として何を実装したかを説明してください。
"""
        
        try:
            from claude_gemini_auto import auto_consult
            gemini_summary = auto_consult(analysis_prompt)
            print("\n💡 作業内容の要約:")
            print(gemini_summary)
        except:
            pass
    
    print(f"\n📊 統計: {len(session.get('actions', []))}件のアクション")
    
    # 続きから作業する場合のヒント
    if file_groups:
        last_group = list(file_groups.keys())[-1]
        print(f"\n💭 最後は「{last_group}」の作業をしていたようです")

if __name__ == "__main__":
    smart_recover()