#!/usr/bin/env python3
"""
研究自動実行トリガーシステム
特定の条件で研究を自動開始
"""
import os
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

class AutoResearchTrigger:
    def __init__(self):
        self.config_file = 'auto_research_config.json'
        self.log_file = 'auto_research_log.json'
        self.load_config()
        
    def load_config(self):
        """設定ファイルを読み込み"""
        default_config = {
            "auto_trigger_enabled": True,
            "trigger_conditions": {
                "new_images_uploaded": True,
                "schedule_based": False,
                "manual_request": True,
                "keyword_detection": True
            },
            "keywords": ["研究", "実験", "分析", "research", "experiment", "analyze"],
            "image_extensions": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
            "schedule": {
                "enabled": False,
                "time": "09:00",
                "days": ["monday", "wednesday", "friday"]
            },
            "colab_notebook_path": "Auto_Research_Colab.ipynb",
            "output_directory": "auto_research_outputs",
            "backup_to_drive": True
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """設定ファイルを保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def log_event(self, event_type, details):
        """イベントをログに記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # 直近100件のみ保持
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def detect_new_images(self, directory='.'):
        """新しい画像ファイルを検出"""
        image_files = []
        for ext in self.config['image_extensions']:
            pattern = f"*{ext}"
            image_files.extend(Path(directory).glob(pattern))
        
        # 最近追加されたファイル（5分以内）
        recent_images = []
        current_time = time.time()
        for img_file in image_files:
            if current_time - img_file.stat().st_mtime < 300:  # 5分以内
                recent_images.append(str(img_file))
        
        return recent_images
    
    def check_keyword_in_text(self, text):
        """テキスト内でキーワードを検出"""
        text_lower = text.lower()
        for keyword in self.config['keywords']:
            if keyword.lower() in text_lower:
                return True
        return False
    
    def is_colab_environment(self):
        """Google Colab環境かどうかを判定"""
        try:
            import google.colab
            return True
        except ImportError:
            return False
    
    def trigger_research_execution(self, trigger_reason="manual"):
        """研究実行をトリガー"""
        print(f"🚀 研究自動実行をトリガー: {trigger_reason}")
        
        # ログ記録
        self.log_event("research_triggered", {
            "reason": trigger_reason,
            "timestamp": datetime.now().isoformat()
        })
        
        # Colab環境の場合
        if self.is_colab_environment():
            print("📊 Google Colab環境で研究を実行中...")
            # Colabノートブックのセルを実行
            return self.execute_colab_research()
        else:
            print("💻 ローカル環境で研究を実行中...")
            return self.execute_local_research()
    
    def execute_colab_research(self):
        """Colab環境での研究実行"""
        try:
            # Colabでの自動実行
            from IPython.display import Javascript
            
            # 自動実行フラグを設定
            js_code = \"\"\"\n            window.AUTO_RESEARCH_TRIGGERED = true;\n            console.log('🚀 自動研究がトリガーされました');\n            \"\"\"\n            
            # JavaScript実行（Colab環境でのみ動作）\n            return Javascript(js_code)\n            \n        except Exception as e:\n            print(f\"❌ Colab実行エラー: {e}\")\n            return False\n    \n    def execute_local_research(self):\n        \"\"\"ローカル環境での研究実行\"\"\"\n        try:\n            # Pythonスクリプトとして実行\n            script_path = \"local_research_execution.py\"\n            if os.path.exists(script_path):\n                result = subprocess.run(['python', script_path], \n                                      capture_output=True, text=True)\n                print(f\"✅ ローカル研究実行完了: {result.returncode}\")\n                return result.returncode == 0\n            else:\n                print(f\"❌ 研究スクリプトが見つかりません: {script_path}\")\n                return False\n        except Exception as e:\n            print(f\"❌ ローカル実行エラー: {e}\")\n            return False\n    \n    def check_triggers(self):\n        \"\"\"トリガー条件をチェック\"\"\"\n        if not self.config['auto_trigger_enabled']:\n            return False\n        \n        triggers = self.config['trigger_conditions']\n        \n        # 新しい画像がアップロードされた場合\n        if triggers['new_images_uploaded']:\n            new_images = self.detect_new_images()\n            if new_images:\n                print(f\"📸 新しい画像を検出: {len(new_images)}個\")\n                return self.trigger_research_execution(\"new_images_detected\")\n        \n        # 手動リクエストの場合\n        if triggers['manual_request']:\n            if os.path.exists('trigger_research_now.txt'):\n                os.remove('trigger_research_now.txt')\n                return self.trigger_research_execution(\"manual_request\")\n        \n        return False\n    \n    def start_monitoring(self, interval=30):\n        \"\"\"監視を開始\"\"\"\n        print(f\"👁️ 研究自動実行監視を開始（{interval}秒間隔）\")\n        print(\"🔧 停止するには Ctrl+C を押してください\")\n        \n        try:\n            while True:\n                if self.check_triggers():\n                    print(\"🎯 研究が自動実行されました\")\n                    # 実行後は少し待機\n                    time.sleep(60)\n                \n                time.sleep(interval)\n                \n        except KeyboardInterrupt:\n            print(\"\\n⏹️ 監視を停止しました\")\n    \n    def manual_trigger(self):\n        \"\"\"手動で研究をトリガー\"\"\"\n        return self.trigger_research_execution(\"manual\")\n    \n    def enable_auto_trigger(self):\n        \"\"\"自動トリガーを有効化\"\"\"\n        self.config['auto_trigger_enabled'] = True\n        self.save_config()\n        print(\"✅ 自動トリガーを有効化しました\")\n    \n    def disable_auto_trigger(self):\n        \"\"\"自動トリガーを無効化\"\"\"\n        self.config['auto_trigger_enabled'] = False\n        self.save_config()\n        print(\"⏸️ 自動トリガーを無効化しました\")\n    \n    def show_status(self):\n        \"\"\"現在の状態を表示\"\"\"\n        print(\"📊 研究自動実行システム状態:\")\n        print(f\"  - 自動トリガー: {'有効' if self.config['auto_trigger_enabled'] else '無効'}\")\n        print(f\"  - 新画像検出: {'有効' if self.config['trigger_conditions']['new_images_uploaded'] else '無効'}\")\n        print(f\"  - 手動リクエスト: {'有効' if self.config['trigger_conditions']['manual_request'] else '無効'}\")\n        print(f\"  - Colab環境: {'Yes' if self.is_colab_environment() else 'No'}\")\n        \n        # 最近のログを表示\n        if os.path.exists(self.log_file):\n            with open(self.log_file, 'r', encoding='utf-8') as f:\n                logs = json.load(f)\n            \n            print(f\"\\n📝 最近のイベント（直近5件）:\")\n            for log in logs[-5:]:\n                timestamp = log['timestamp'][:19].replace('T', ' ')\n                print(f\"  - {timestamp}: {log['event_type']} - {log['details'].get('reason', 'N/A')}\")\n\ndef main():\n    \"\"\"メイン関数\"\"\"\n    import sys\n    \n    trigger = AutoResearchTrigger()\n    \n    if len(sys.argv) > 1:\n        command = sys.argv[1]\n        \n        if command == \"start\":\n            trigger.start_monitoring()\n        elif command == \"trigger\":\n            trigger.manual_trigger()\n        elif command == \"enable\":\n            trigger.enable_auto_trigger()\n        elif command == \"disable\":\n            trigger.disable_auto_trigger()\n        elif command == \"status\":\n            trigger.show_status()\n        else:\n            print(\"使用方法:\")\n            print(\"  python auto_research_trigger.py start    - 監視開始\")\n            print(\"  python auto_research_trigger.py trigger  - 手動実行\")\n            print(\"  python auto_research_trigger.py enable   - 自動トリガー有効\")\n            print(\"  python auto_research_trigger.py disable  - 自動トリガー無効\")\n            print(\"  python auto_research_trigger.py status   - 状態確認\")\n    else:\n        trigger.show_status()\n\nif __name__ == \"__main__\":\n    main()