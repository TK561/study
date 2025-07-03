#!/usr/bin/env python3
"""
多層物体検出統合API - Flask サーバー
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from multi_object_detection_api import MultiObjectDetectionAPI

app = Flask(__name__)
CORS(app)

# API インスタンス
detection_api = MultiObjectDetectionAPI()

@app.route('/api/detect', methods=['POST'])
def detect_objects():
    """物体検出エンドポイント"""
    try:
        data = request.get_json()
        
        # 画像データの取得
        image_data = data.get('image')
        if image_data:
            # Base64デコード（実際の実装で使用）
            # image_bytes = base64.b64decode(image_data)
            pass
        
        # 使用モデルの指定
        use_models = data.get('use_models')
        
        # 検出実行
        response = detection_api.generate_api_response(
            image_data=image_data,
            use_models=use_models
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """利用可能なモデル一覧"""
    return jsonify({
        "models": detection_api.models
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェック"""
    return jsonify({
        "status": "healthy",
        "api_version": detection_api.version
    })

if __name__ == '__main__':
    print(f"🚀 {detection_api.name} Flask サーバー起動")
    print("📡 http://localhost:5000")
    app.run(debug=True, port=5000)
