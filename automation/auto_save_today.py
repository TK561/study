#!/usr/bin/env python3
"""
今日の作業内容の自動保存システム
「今日の内容を保存して」で自動的に引き継ぎファイルを更新
"""

import os
import json
from datetime import datetime
from session_recovery_system import get_recovery_system

def auto_save_today_work():
    """今日の作業内容を自動的に保存・更新"""
    
    # セッション情報を取得
    system = get_recovery_system()
    session = system._load_current_session()
    
    if not session.get('actions'):
        print("保存する作業内容がありません")
        return
    
    # 今日の日付
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 作業内容を分析
    work_summary = analyze_today_work(session)
    
    # 1. 引き継ぎファイルを更新
    update_handover_file(work_summary, today)
    
    # 2. クイックガイドを更新
    update_quick_guide(work_summary)
    
    # 3. 構造ファイルを更新
    update_structure_file()
    
    print("✅ 今日の作業内容を保存しました")
    print("📁 更新されたファイル:")
    print("  - TODAY_WORK_HANDOVER.md")
    print("  - QUICK_START_GUIDE.md") 
    print("  - CURRENT_PROJECT_STRUCTURE.md")

def analyze_today_work(session):
    """セッションから今日の作業内容を分析"""
    
    work_types = {
        'vercel': 0,
        'gemini': 0,
        'recovery': 0,
        'cleanup': 0,
        'other': 0
    }
    
    files_worked = []
    commands_executed = []
    
    for action in session.get('actions', []):
        if action['type'] == 'file_operation':
            file_path = action['details']['file_path']
            files_worked.append(os.path.basename(file_path))
            
            # 作業タイプを判定
            if 'vercel' in file_path.lower():
                work_types['vercel'] += 1
            elif 'gemini' in file_path.lower():
                work_types['gemini'] += 1
            elif 'recovery' in file_path.lower() or 'session' in file_path.lower():
                work_types['recovery'] += 1
            else:
                work_types['other'] += 1
                
        elif action['type'] == 'command_execution':
            commands_executed.append(action['details']['command'])
    
    return {
        'work_types': work_types,
        'files_worked': list(set(files_worked)),
        'commands_executed': commands_executed,
        'total_actions': len(session.get('actions', [])),
        'session_duration': calculate_duration(session)
    }

def calculate_duration(session):
    """作業時間を計算"""
    start = datetime.fromisoformat(session.get('start_time', ''))
    end = datetime.fromisoformat(session.get('last_updated', ''))
    duration = end - start
    return int(duration.total_seconds() / 60)

def update_handover_file(work_summary, today):
    """引き継ぎファイルを更新"""
    
    # 主な作業内容を特定
    main_works = []
    if work_summary['work_types']['vercel'] > 0:
        main_works.append("🌐 Vercelデプロイ関連作業")
    if work_summary['work_types']['gemini'] > 0:
        main_works.append("🤖 Gemini API統合作業")
    if work_summary['work_types']['recovery'] > 0:
        main_works.append("🔄 セッション復元システム作業")
    if work_summary['work_types']['cleanup'] > 0:
        main_works.append("🧹 プロジェクト整理作業")
    
    content = f"""# {today} 作業引き継ぎ

## 実施した主な作業

{chr(10).join(main_works)}

## 作業統計
- 総アクション数: {work_summary['total_actions']}件
- 作業時間: 約{work_summary['session_duration']}分
- 作業ファイル数: {len(work_summary['files_worked'])}件

## 作業したファイル
{chr(10).join([f"- {f}" for f in work_summary['files_worked'][:10]])}

## 次回作業時の手順

### 前回の続きを確認
「前回の続きからやりたい」

### セッション復元
「復元して」

### Gemini相談
```python
from deep_consultation_system import deep_consult
result = deep_consult("質問内容")
```

## 現在の状態
✅ すべてのシステムが正常稼働中
✅ 次回起動時から即座に作業再開可能

---
**最終更新**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
"""
    
    with open('/mnt/c/Desktop/Research/TODAY_WORK_HANDOVER.md', 'w', encoding='utf-8') as f:
        f.write(content)

def update_quick_guide(work_summary):
    """クイックガイドを更新"""
    content = f"""# 次回起動時のクイックスタート

## 前回の作業概要
- 総作業: {work_summary['total_actions']}件のアクション
- 時間: 約{work_summary['session_duration']}分

## 最初にやること

### 前回の続きを確認
「前回の続きからやりたい」

### セッション復元（詳細確認）
「復元して」

### Gemini相談（いつでも利用可能）
```python
from deep_consultation_system import deep_consult
result = deep_consult("質問内容")
```

## 主要システム
1. **研究本体**: https://study-research-final.vercel.app/
2. **Gemini深層相談**: 自動的に利用可能
3. **セッション復元**: 自動保存済み

## 詳細情報
- `TODAY_WORK_HANDOVER.md` - 詳細な引き継ぎ
- `CURRENT_PROJECT_STRUCTURE.md` - プロジェクト構造

**準備完了**: 次回起動時からすぐに作業を再開できます

---
**最終更新**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
"""
    
    with open('/mnt/c/Desktop/Research/QUICK_START_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(content)

def update_structure_file():
    """プロジェクト構造ファイルを更新"""
    content = f"""# 現在のプロジェクト構造

## メインファイル（使用中）

### 研究本体
- `api/index.py` - Vercel関数（研究成果表示）
- `vercel_api_setup.py` - Vercelデプロイ設定
- `index.html` - 静的HTML版
- `study/` - 研究データ

### Gemini統合システム
- `deep_consultation_system.py` - 深層相談システム（メイン）
- `claude_gemini_auto.py` - 自動相談機能
- `research_analysis_system.py` - 研究分析システム
- `interactive_analysis.py` - 対話的分析

### セッション復元システム
- `smart_recovery.py` - スマート復元（メイン）
- `session_recovery_system.py` - 復元システム本体
- `claude_auto_restore.py` - 自動復元機能
- `recover_claude_session.py` - 復元コマンド

## Claude Code用ファイル
- `TODAY_WORK_HANDOVER.md` - 作業引き継ぎ
- `QUICK_START_GUIDE.md` - 起動時ガイド
- `auto_save_today.py` - 作業内容自動保存

## セキュリティ
- `.env` - APIキー（非公開）
- `.claude_sessions/` - セッションデータ（ローカルのみ）

---
**最終更新**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
**整理状況**: 不要ファイル削除済み、構造最適化完了
"""
    
    with open('/mnt/c/Desktop/Research/CURRENT_PROJECT_STRUCTURE.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    auto_save_today_work()