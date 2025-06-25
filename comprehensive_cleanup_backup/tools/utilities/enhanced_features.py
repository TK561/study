#!/usr/bin/env python3
"""
統合システム強化機能
Geminiとの相談で明らかになった改善点を実装
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class WorkflowAnalyzer:
    """作業パターン分析・最適化エンジン"""
    
    def __init__(self):
        self.analytics_dir = ".workflow_analytics"
        os.makedirs(self.analytics_dir, exist_ok=True)
        self.work_log_file = os.path.join(self.analytics_dir, "work_log.json")
        self.patterns_file = os.path.join(self.analytics_dir, "patterns.json")
        
    def log_work_action(self, action_type: str, details: Dict):
        """作業アクションをログ記録"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details,
            "day_of_week": datetime.now().strftime("%A"),
            "hour": datetime.now().hour
        }
        
        # ログファイルに追記
        work_log = self._load_work_log()
        work_log.append(log_entry)
        
        # 最新1000件のみ保持
        if len(work_log) > 1000:
            work_log = work_log[-1000:]
        
        with open(self.work_log_file, 'w', encoding='utf-8') as f:
            json.dump(work_log, f, ensure_ascii=False, indent=2)
    
    def analyze_work_patterns(self) -> Dict:
        """作業パターンの分析"""
        work_log = self._load_work_log()
        
        if not work_log:
            return {"patterns": [], "insights": "データ不足"}
        
        patterns = {
            "time_patterns": self._analyze_time_patterns(work_log),
            "action_sequences": self._analyze_action_sequences(work_log),
            "efficiency_periods": self._identify_efficiency_periods(work_log),
            "common_workflows": self._extract_common_workflows(work_log)
        }
        
        return patterns
    
    def _analyze_time_patterns(self, work_log: List[Dict]) -> Dict:
        """時間パターンの分析"""
        hourly_activity = defaultdict(int)
        daily_activity = defaultdict(int)
        
        for entry in work_log:
            hour = entry["hour"]
            day = entry["day_of_week"]
            
            hourly_activity[hour] += 1
            daily_activity[day] += 1
        
        # 最も活発な時間帯
        peak_hour = max(hourly_activity.items(), key=lambda x: x[1])[0] if hourly_activity else 12
        peak_day = max(daily_activity.items(), key=lambda x: x[1])[0] if daily_activity else "Monday"
        
        return {
            "peak_hour": peak_hour,
            "peak_day": peak_day,
            "hourly_distribution": dict(hourly_activity),
            "daily_distribution": dict(daily_activity)
        }
    
    def _analyze_action_sequences(self, work_log: List[Dict]) -> List[Dict]:
        """アクション順序パターンの分析"""
        sequences = []
        
        for i in range(len(work_log) - 1):
            current = work_log[i]
            next_action = work_log[i + 1]
            
            time_diff = (
                datetime.fromisoformat(next_action["timestamp"]) - 
                datetime.fromisoformat(current["timestamp"])
            ).total_seconds()
            
            if time_diff < 3600:  # 1時間以内の連続アクション
                sequences.append({
                    "from": current["action_type"],
                    "to": next_action["action_type"],
                    "duration": time_diff
                })
        
        # 頻出順序パターン
        sequence_counts = defaultdict(int)
        for seq in sequences:
            key = f"{seq['from']} → {seq['to']}"
            sequence_counts[key] += 1
        
        common_sequences = sorted(sequence_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return [{"pattern": pattern, "count": count} for pattern, count in common_sequences]
    
    def _identify_efficiency_periods(self, work_log: List[Dict]) -> Dict:
        """効率的な時間帯の特定"""
        # アクション密度で効率性を測定
        hourly_efficiency = defaultdict(list)
        
        # 1時間ウィンドウでのアクション数を計算
        for entry in work_log:
            hour = entry["hour"]
            hourly_efficiency[hour].append(1)
        
        efficiency_scores = {}
        for hour, actions in hourly_efficiency.items():
            efficiency_scores[hour] = len(actions)
        
        if efficiency_scores:
            best_hour = max(efficiency_scores.items(), key=lambda x: x[1])[0]
            worst_hour = min(efficiency_scores.items(), key=lambda x: x[1])[0]
        else:
            best_hour = worst_hour = 12
        
        return {
            "most_efficient_hour": best_hour,
            "least_efficient_hour": worst_hour,
            "efficiency_by_hour": efficiency_scores
        }
    
    def _extract_common_workflows(self, work_log: List[Dict]) -> List[Dict]:
        """共通ワークフローの抽出"""
        # 簡易実装：よく使われるアクションタイプ
        action_counts = defaultdict(int)
        
        for entry in work_log:
            action_counts[entry["action_type"]] += 1
        
        common_actions = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return [{"action": action, "frequency": count} for action, count in common_actions]
    
    def _load_work_log(self) -> List[Dict]:
        """作業ログの読み込み"""
        if os.path.exists(self.work_log_file):
            with open(self.work_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

class PerformanceTracker:
    """パフォーマンス追跡・最適化システム"""
    
    def __init__(self):
        self.metrics_file = ".workflow_analytics/performance_metrics.json"
        self.baseline_metrics = self._load_baseline_metrics()
    
    def track_session_performance(self, session_data: Dict) -> Dict:
        """セッションパフォーマンスの追跡"""
        metrics = {
            "session_duration": self._calculate_session_duration(session_data),
            "actions_per_hour": self._calculate_actions_per_hour(session_data),
            "file_operations_ratio": self._calculate_file_ops_ratio(session_data),
            "efficiency_score": self._calculate_efficiency_score(session_data)
        }
        
        # ベースラインとの比較
        improvements = self._compare_with_baseline(metrics)
        
        # メトリクス保存
        self._save_metrics(metrics)
        
        return {
            "current_metrics": metrics,
            "improvements": improvements,
            "recommendations": self._generate_performance_recommendations(metrics)
        }
    
    def _calculate_session_duration(self, session_data: Dict) -> float:
        """セッション時間の計算"""
        if not session_data.get('actions'):
            return 0
        
        start_time = datetime.fromisoformat(session_data.get('start_time', datetime.now().isoformat()))
        end_time = datetime.now()
        
        return (end_time - start_time).total_seconds() / 3600  # 時間単位
    
    def _calculate_actions_per_hour(self, session_data: Dict) -> float:
        """時間あたりアクション数"""
        duration = self._calculate_session_duration(session_data)
        actions_count = len(session_data.get('actions', []))
        
        return actions_count / max(duration, 0.1)  # ゼロ除算を避ける
    
    def _calculate_file_ops_ratio(self, session_data: Dict) -> float:
        """ファイル操作の割合"""
        actions = session_data.get('actions', [])
        if not actions:
            return 0
        
        file_ops = sum(1 for action in actions if action.get('type') == 'file_operation')
        return file_ops / len(actions)
    
    def _calculate_efficiency_score(self, session_data: Dict) -> float:
        """効率性スコア（0-10）"""
        actions_per_hour = self._calculate_actions_per_hour(session_data)
        file_ops_ratio = self._calculate_file_ops_ratio(session_data)
        
        # 簡易スコア計算
        score = min(10, (actions_per_hour * 0.5) + (file_ops_ratio * 5))
        return round(score, 1)
    
    def _compare_with_baseline(self, current_metrics: Dict) -> Dict:
        """ベースラインとの比較"""
        improvements = {}
        
        for metric, current_value in current_metrics.items():
            baseline_value = self.baseline_metrics.get(metric, current_value)
            
            if baseline_value > 0:
                improvement_pct = ((current_value - baseline_value) / baseline_value) * 100
                improvements[metric] = round(improvement_pct, 1)
            else:
                improvements[metric] = 0
        
        return improvements
    
    def _generate_performance_recommendations(self, metrics: Dict) -> List[str]:
        """パフォーマンス改善提案"""
        recommendations = []
        
        if metrics["actions_per_hour"] < 10:
            recommendations.append("⚡ 作業ペースが低下しています。休憩を取るか、タスクを細分化してみてください")
        
        if metrics["file_operations_ratio"] < 0.3:
            recommendations.append("📄 ファイル操作が少ないです。実装作業を進めることを検討してください")
        
        if metrics["efficiency_score"] < 5:
            recommendations.append("🎯 効率性スコアが低いです。作業フローの見直しを推奨します")
        
        if not recommendations:
            recommendations.append("✅ 良好なパフォーマンスです！この調子で続けてください")
        
        return recommendations
    
    def _load_baseline_metrics(self) -> Dict:
        """ベースラインメトリクスの読み込み"""
        if os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('baseline', {})
        
        # デフォルトベースライン
        return {
            "session_duration": 1.0,
            "actions_per_hour": 15.0,
            "file_operations_ratio": 0.4,
            "efficiency_score": 6.0
        }
    
    def _save_metrics(self, metrics: Dict):
        """メトリクスの保存"""
        data = {"baseline": self.baseline_metrics, "latest": metrics, "updated": datetime.now().isoformat()}
        
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class AutomationEngine:
    """自動化エンジン"""
    
    def __init__(self):
        self.automation_rules = []
        self.automation_log = []
    
    def suggest_automations(self, work_patterns: Dict) -> List[Dict]:
        """自動化提案の生成"""
        suggestions = []
        
        # 頻出アクション順序パターンから自動化を提案
        for sequence in work_patterns.get("action_sequences", []):
            if sequence["count"] >= 3:  # 3回以上のパターン
                suggestions.append({
                    "type": "sequence_automation",
                    "pattern": sequence["pattern"],
                    "frequency": sequence["count"],
                    "suggestion": f"「{sequence['pattern']}」の自動化を検討",
                    "estimated_time_saved": sequence["count"] * 2  # 分単位
                })
        
        # 時間パターンから通知提案
        time_patterns = work_patterns.get("time_patterns", {})
        if time_patterns.get("peak_hour"):
            suggestions.append({
                "type": "time_optimization",
                "peak_hour": time_patterns["peak_hour"],
                "suggestion": f"{time_patterns['peak_hour']}時が最も活発です。重要な作業をこの時間に集中させることを推奨",
                "estimated_productivity_gain": "15-20%"
            })
        
        return suggestions
    
    def implement_automation(self, automation_config: Dict):
        """自動化の実装"""
        # 実際の自動化実装はここで行う
        self.automation_rules.append(automation_config)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "automation": automation_config,
            "status": "implemented"
        }
        self.automation_log.append(log_entry)

# 統合機能のテスト用関数
def test_enhanced_features():
    """強化機能のテスト"""
    print("🧪 強化機能テスト開始")
    
    # ワークフロー分析テスト
    analyzer = WorkflowAnalyzer()
    
    # サンプルアクションをログ
    sample_actions = [
        {"action_type": "file_create", "details": {"file": "test1.py"}},
        {"action_type": "file_edit", "details": {"file": "test1.py"}},
        {"action_type": "consultation", "details": {"query": "テスト相談"}},
        {"action_type": "file_create", "details": {"file": "test2.py"}}
    ]
    
    for action in sample_actions:
        analyzer.log_work_action(action["action_type"], action["details"])
        time.sleep(0.1)  # 時間差をつける
    
    # パターン分析
    patterns = analyzer.analyze_work_patterns()
    print(f"📊 分析結果: {len(patterns.get('action_sequences', []))}個のパターンを検出")
    
    # パフォーマンス追跡テスト
    tracker = PerformanceTracker()
    
    session_data = {
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "actions": sample_actions
    }
    
    performance = tracker.track_session_performance(session_data)
    print(f"⚡ 効率性スコア: {performance['current_metrics']['efficiency_score']}/10")
    
    # 自動化提案テスト
    automation = AutomationEngine()
    suggestions = automation.suggest_automations(patterns)
    print(f"🤖 自動化提案: {len(suggestions)}件")
    
    return {
        "patterns": patterns,
        "performance": performance,
        "automation_suggestions": suggestions
    }

if __name__ == "__main__":
    results = test_enhanced_features()
    print("\n✅ 強化機能テスト完了")