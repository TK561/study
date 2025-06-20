#!/usr/bin/env python3
"""
Claude Code起動時に自動で1時間毎整理システムを開始
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from hourly_summary_system import HourlySummarySystem
    
    def start_system():
        """システムを開始"""
        print("🚀 Claude Code セッション開始")
        print("⏰ 1時間毎作業整理システムを起動中...")
        
        # システム初期化
        system = HourlySummarySystem()
        
        print("""
✅ 整理システムが開始されました！

📋 機能:
- 🕐 1時間毎に自動で作業をまとめます
- 📊 Git活動、ファイル変更を追跡
- 📝 セッションログを自動保存

💡 使用方法:
- Python環境で以下を実行:
  >>> from start_hourly_system import get_current_system
  >>> system = get_current_system()
  >>> system.manual_summary()  # 手動まとめ
  >>> print(system.get_session_report())  # レポート表示

🎯 このシステムはバックグラウンドで動作し続けます
""")
        
        return system
    
    # グローバル変数として保持
    _current_system = None
    
    def get_current_system():
        """現在のシステムインスタンスを取得"""
        global _current_system
        if _current_system is None:
            _current_system = start_system()
        return _current_system
    
    # 自動起動
    if __name__ == "__main__":
        get_current_system()
        
        # 対話モード
        try:
            system = get_current_system()
            while True:
                cmd = input("\n📋 (m:手動まとめ / r:レポート / s:ステータス / q:終了): ").strip().lower()
                
                if cmd == 'm':
                    system.manual_summary()
                elif cmd == 'r':
                    print(system.get_session_report())
                elif cmd == 's':
                    print(f"⏰ セッション継続中 - 次回まとめ: {system.last_summary.strftime('%H:%M:%S')}から1時間後")
                elif cmd == 'q':
                    print("👋 セッションを終了します")
                    break
                else:
                    print("❓ 無効なコマンド: m(まとめ) / r(レポート) / s(ステータス) / q(終了)")
                    
        except KeyboardInterrupt:
            print("\n👋 セッションを終了します")
    
    else:
        # インポート時に自動起動
        get_current_system()

except ImportError as e:
    print(f"❌ システム起動エラー: {e}")
    print("💡 必要な依存関係がインストールされていない可能性があります")
except Exception as e:
    print(f"❌ 予期しないエラー: {e}")
    print("💡 システムログを確認してください")