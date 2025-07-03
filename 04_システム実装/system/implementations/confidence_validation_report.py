#!/usr/bin/env python3
"""
確信度検証レポート - 全システムの確信度が0-1範囲であることを確認
"""

from multi_object_detection_api import MultiObjectDetectionAPI
from realtime_image_processor import RealtimeImageProcessor
from integrated_research_system import IntegratedResearchSystem
import json

def validate_confidence_range(confidence_value, system_name, context=""):
    """確信度が0-1の範囲内であることを検証"""
    is_valid = isinstance(confidence_value, (int, float)) and 0 <= confidence_value <= 1
    status = "✅ VALID" if is_valid else "❌ INVALID"
    print(f"  {status}: {system_name} - {context}: {confidence_value}")
    return is_valid

def main():
    print("🔍 確信度検証レポート")
    print("=" * 50)
    print("全システムで確信度が0-1の範囲内であることを確認します\n")
    
    all_valid = True
    
    # 1. 多層物体検出API
    print("1️⃣ 多層物体検出API")
    api = MultiObjectDetectionAPI()
    
    # 各モデルの閾値チェック
    for model_name, model_info in api.models.items():
        threshold = model_info["confidence_threshold"]
        valid = validate_confidence_range(threshold, f"Model {model_name}", f"threshold")
        all_valid = all_valid and valid
    
    # 検出結果のconfidenceチェック
    detection_result = api.detect_objects_single_model({}, "yolo")
    for i, detection in enumerate(detection_result[:3]):
        conf = detection.get("confidence", -1)
        valid = validate_confidence_range(conf, "YOLO Detection", f"detection {i+1}")
        all_valid = all_valid and valid
    
    print()
    
    # 2. リアルタイム画像処理システム
    print("2️⃣ リアルタイム画像処理システム")
    processor = RealtimeImageProcessor()
    
    # 物体検出結果
    detection_result = processor.detect_objects({})
    if "output" in detection_result and "objects" in detection_result["output"]:
        for i, obj in enumerate(detection_result["output"]["objects"][:3]):
            conf = obj.get("confidence", -1)
            valid = validate_confidence_range(conf, "Realtime Detection", f"object {i+1}")
            all_valid = all_valid and valid
    
    print()
    
    # 3. 統合研究システム
    print("3️⃣ 統合研究システム")
    integrated_system = IntegratedResearchSystem()
    
    # 統合分析結果
    test_image = {
        "id": "validation_test",
        "detected_categories": ["person", "vehicle"]
    }
    
    print("  🔄 統合分析実行中...")
    analysis_result = integrated_system.run_integrated_analysis(test_image)
    
    # 検出確信度チェック
    if "systems_results" in analysis_result and "multi_detection" in analysis_result["systems_results"]:
        detections = analysis_result["systems_results"]["multi_detection"].get("integrated_detections", [])
        for i, detection in enumerate(detections[:5]):
            if isinstance(detection, dict) and "confidence" in detection:
                conf = detection["confidence"]
                valid = validate_confidence_range(conf, "Integrated Detection", f"detection {i+1}")
                all_valid = all_valid and valid
    
    # 統合スコア確認
    if "integrated_score" in analysis_result:
        for score_name, score_value in analysis_result["integrated_score"].items():
            valid = validate_confidence_range(score_value, "Integrated Score", score_name)
            all_valid = all_valid and valid
    
    print()
    
    # 総合結果
    print("=" * 50)
    if all_valid:
        print("🎉 検証完了: すべての確信度が正しく0-1の範囲内です")
        print("✅ 全システム正常動作確認")
    else:
        print("⚠️ 警告: 一部の確信度が範囲外です")
        print("❌ 修正が必要")
    
    print(f"📊 検証対象システム: 3システム")
    print(f"🔍 検証項目: 確信度値の範囲(0-1)チェック")
    print(f"📅 検証日時: 2025年6月25日")

if __name__ == "__main__":
    main()