#!/usr/bin/env python3
"""
重複ファイル分析ツール
類似・重複機能を持つファイルを特定して整理提案
"""

import os
import glob
from collections import defaultdict

def analyze_file_duplicates():
    """重複・類似ファイルの分析"""
    
    # ファイルグループ分類
    file_groups = {
        "自動整理系": [
            "auto_cleanup_on_exit.py",
            "auto_cleanup_permanent.py", 
            "complete_auto_cleanup.py"
        ],
        "自動保存系": [
            "auto_save_today.py",
            "auto_save_hook.py"
        ],
        "復元系": [
            "session_recovery_system.py",
            "smart_recovery.py",
            "claude_auto_restore.py",
            "recover_claude_session.py"
        ],
        "意図記録系": [
            "intent_knowledge_system.py",
            "universal_intent_system.py",
            "auto_intent_hook.py"
        ],
        "Gemini統合系": [
            "claude_gemini_auto.py",
            "deep_consultation_system.py",
            "research_analysis_system.py",
            "interactive_analysis.py"
        ],
        "統合システム系": [
            "unified_claude_system.py",
            "claude_master_system.py",
            "enhanced_features.py"
        ],
        "引き継ぎチェック系": [
            "auto_handover_check.py"
        ],
        "ガイド・ドキュメント系": [
            "CLAUDE_GEMINI_USAGE.md",
            "CLAUDE_RECOVERY_GUIDE.md", 
            "STARTUP_GUIDE.md",
            "QUICK_START_GUIDE.md",
            "CURRENT_PROJECT_STRUCTURE.md"
        ]
    }
    
    print("📊 重複・類似ファイル分析結果")
    print("="*60)
    
    consolidation_plan = {}
    
    for group_name, files in file_groups.items():
        print(f"\n📁 {group_name} ({len(files)}ファイル)")
        for file in files:
            if os.path.exists(file):
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (存在しない)")
        
        # 統合提案
        if len(files) > 1:
            consolidation_plan[group_name] = suggest_consolidation(group_name, files)
    
    print("\n" + "="*60)
    print("🔧 統合・整理提案")
    print("="*60)
    
    for group_name, suggestion in consolidation_plan.items():
        print(f"\n📁 {group_name}:")
        print(f"  💡 提案: {suggestion['action']}")
        print(f"  📄 統合後ファイル: {suggestion['target']}")
        if suggestion.get('delete'):
            print(f"  🗑️ 削除対象: {', '.join(suggestion['delete'])}")
    
    return consolidation_plan

def suggest_consolidation(group_name, files):
    """統合提案の生成"""
    
    suggestions = {
        "自動整理系": {
            "action": "complete_auto_cleanup.py を統一版として採用、他は削除",
            "target": "complete_auto_cleanup.py",
            "delete": ["auto_cleanup_on_exit.py", "auto_cleanup_permanent.py"]
        },
        "復元系": {
            "action": "smart_recovery.py をメインとし、他は統合",
            "target": "smart_recovery.py", 
            "delete": ["claude_auto_restore.py", "recover_claude_session.py"]
        },
        "意図記録系": {
            "action": "universal_intent_system.py をメインとし、他はヘルパー",
            "target": "universal_intent_system.py",
            "delete": ["intent_knowledge_system.py"]
        },
        "Gemini統合系": {
            "action": "deep_consultation_system.py をメインとし、他は特化用途で保持",
            "target": "deep_consultation_system.py",
            "delete": ["claude_gemini_auto.py"]
        },
        "統合システム系": {
            "action": "claude_master_system.py を最終版として採用",
            "target": "claude_master_system.py",
            "delete": ["unified_claude_system.py"]
        },
        "ガイド・ドキュメント系": {
            "action": "QUICK_START_GUIDE.md に統合、他は削除",
            "target": "QUICK_START_GUIDE.md",
            "delete": ["STARTUP_GUIDE.md", "CLAUDE_GEMINI_USAGE.md"]
        }
    }
    
    return suggestions.get(group_name, {
        "action": "要検討",
        "target": files[0] if files else "不明"
    })

def execute_consolidation():
    """統合実行プラン"""
    plan = analyze_file_duplicates()
    
    print("\n" + "="*60)
    print("🚀 統合実行プラン")
    print("="*60)
    
    delete_files = []
    keep_files = []
    
    for group_name, suggestion in plan.items():
        if suggestion.get('delete'):
            delete_files.extend(suggestion['delete'])
        keep_files.append(suggestion['target'])
    
    print(f"📄 保持ファイル ({len(keep_files)}件):")
    for file in keep_files:
        print(f"  ✅ {file}")
    
    print(f"\n🗑️ 削除候補 ({len(delete_files)}件):")
    for file in delete_files:
        print(f"  ❌ {file}")
    
    # 削除対象の詳細分析
    print(f"\n📊 削除による効果:")
    print(f"  - ファイル数削減: {len(delete_files)}件")
    print(f"  - 保守対象の明確化")
    print(f"  - システム構造の簡素化")
    
    return {
        "delete_candidates": delete_files,
        "keep_files": keep_files,
        "consolidation_plan": plan
    }

if __name__ == "__main__":
    result = execute_consolidation()
    
    print(f"\n🎯 分析完了: {len(result['delete_candidates'])}件の重複ファイル特定")