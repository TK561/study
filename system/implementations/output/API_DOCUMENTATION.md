# 多層物体検出統合API ドキュメント

## API バージョン: 2.0.0

## エンドポイント

### POST /api/detect
多層物体検出を実行します。

#### リクエスト
```json
{
    "image": "base64_encoded_image_data",
    "use_models": ["yolo", "faster_rcnn", "ssd", "mask_rcnn"]  // オプション
}
```

#### レスポンス
```json
{
    "api_version": "2.0.0",
    "status": "success",
    "data": {
        "detections": {
            "total_objects": 5,
            "integrated_detections": [...],
            "model_specific_results": {...}
        },
        "quality_metrics": {
            "average_confidence": 0.85,
            "consensus_rate": 0.6
        },
        "recommendations": [...]
    }
}
```

## 利用可能なモデル

### yolo
- **名称**: YOLO v8
- **特徴**: 一般物体検出
- **速度**: fast
- **精度**: 0.85
- **カテゴリ**: person, car, dog, cat, chair, book, bottle, phone

### faster_rcnn
- **名称**: Faster R-CNN
- **特徴**: 高精度検出
- **速度**: medium
- **精度**: 0.92
- **カテゴリ**: person, vehicle, animal, furniture, electronics

### ssd
- **名称**: SSD MobileNet
- **特徴**: リアルタイム検出
- **速度**: very_fast
- **精度**: 0.78
- **カテゴリ**: person, car, bicycle, motorcycle, bus, truck

### mask_rcnn
- **名称**: Mask R-CNN
- **特徴**: セグメンテーション
- **速度**: slow
- **精度**: 0.94
- **カテゴリ**: person, animal, object, vehicle

## 統合アルゴリズム

1. **並列検出**: 複数モデルで同時に物体検出を実行
2. **位置ベースグループ化**: 近接する検出結果をグループ化
3. **信頼度ベース選択**: グループ内で最も信頼度の高い結果を選択
4. **コンセンサススコア**: 複数モデルでの検出率を計算

## 使用例

```python
api = MultiObjectDetectionAPI()
response = api.generate_api_response(
    image_data=your_image_data,
    use_models=["yolo", "faster_rcnn"]
)
print(response)
```
