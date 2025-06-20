# 意味カテゴリに基づく統合画像分類システム

学術研究用の画像分類システムです。YOLO物体検出、SAMセグメンテーション、CLIP分類を統合し、意味カテゴリに基づいて最適な分類アプローチを自動選択します。

##  主な機能

- **画像キャプション自動生成**: BLIP(Bootstrapping Language-Image Pre-training)を使用
- **意味カテゴリ自動判定**: WordNetを活用した意味論的分析
- **物体検出**: YOLOv8による高精度物体検出
- **画像セグメンテーション**: SAM(Segment Anything Model)による精密セグメンテーション
- **特化型分類**: カテゴリ別に最適化された分類アプローチ
- **性能比較**: 汎用アプローチとの定量的性能比較
- **統計分析・可視化**: 実験結果の詳細分析とグラフ生成

##  技術スタック

### 深層学習フレームワーク
- **PyTorch**: 深層学習の基盤フレームワーク
- **Transformers**: BLIP、CLIPモデルの実行
- **CLIP**: OpenAI Contrastive Language-Image Pre-training
- **YOLOv8**: 最新の物体検出モデル
- **SAM**: Meta AI Segment Anything Model

### 自然言語処理
- **NLTK**: 自然言語処理ライブラリ
- **WordNet**: 意味論的語彙データベース

### データ処理・可視化
- **NumPy**: 数値計算
- **Pandas**: データ分析
- **Matplotlib**: グラフ作成
- **OpenCV**: 画像処理

##  必要な環境

- Python 3.8以上
- CUDA対応GPU（推奨、CPUでも動作可能）
- メモリ: 8GB以上推奨

##  インストール方法

1. **リポジトリのクローン**
```bash
git clone <repository-url>
cd study
```

2. **仮想環境の作成（推奨）**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\\Scripts\\activate  # Windows
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **必要なモデルファイルの準備**
- YOLOv8モデル: 初回実行時に自動ダウンロード
- SAMモデル: `models/sam_vit_b.pth`に配置（オプション）

##  使用方法

### GUIモードで実行
```bash
python semantic_classification_system.py
```

### 主な処理フロー

1. **画像選択**: GUI経由で単一または複数画像を選択
2. **キャプション生成**: BLIPによる自動キャプション作成
3. **意味カテゴリ判定**: WordNetを用いた意味解析
4. **分類アプローチ選択**: カテゴリに基づく最適手法選択
5. **物体検出・セグメンテーション**: YOLO+SAMによる詳細解析
6. **分類実験**: 汎用vs特化アプローチの性能比較
7. **結果分析・可視化**: 統計分析とグラフ生成

##  対応カテゴリと特化アプローチ

| カテゴリ | 特化アプローチ | 対象ラベル例 |
|---------|---------------|-------------|
| person | Human-focused Classification | man, woman, child, face |
| animal | Animal-specialized Classification | dog, cat, bird, horse |
| food | Food-specialized Classification | pizza, sushi, fruit, cake |
| landscape | Scene-specialized Classification | beach, mountain, forest |
| building | Architecture-specialized Classification | house, bridge, temple |
| vehicle | Vehicle-specialized Classification | car, airplane, bicycle |
| furniture | Object-specialized Classification | chair, table, sofa |
| plant | Plant-specialized Classification | tree, flower, garden |

##  出力ファイル

### 画像処理結果
- `output/masks/`: セグメンテーションマスク画像
- `output/results.csv`: 検出結果詳細データ

### 分析結果
- `results/detailed_results.csv`: 全画像の詳細分析結果
- `results/summary_results.json`: 統計サマリー
- `results/graphs/`: 可視化グラフ（改善率分布、カテゴリ別性能等）

##  実験設計

本システムは以下の研究仮説を検証します：

**仮説**: 「画像の意味内容に応じて特化された分類アプローチを選択することで、汎用的なアプローチよりも高い分類精度を達成できる」

### 評価指標
- **確信度改善率**: 特化アプローチと汎用アプローチの確信度差
- **カテゴリ別性能**: 意味カテゴリごとの改善度分析
- **統計的有意性**: 改善効果の統計的検証

## 🎛 システム設定

### モデル設定
```python
# デバイス設定（自動検出）
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# モデルパス
YOLO_MODEL = "yolov8n.pt"
SAM_MODEL = "models/sam_vit_b.pth"
```

### 出力ディレクトリ
```
study/
├── output/           # 画像処理結果
│   └── masks/       # セグメンテーションマスク
├── results/         # 分析結果
│   ├── graphs/      # 可視化グラフ
│   └── images/      # 結果画像
└── models/          # モデルファイル（オプション）
```

## 🐛 トラブルシューティング

### よくある問題

1. **GPU認識エラー**
   - CUDA対応PyTorchがインストールされているか確認
   - GPU仕様とCUDAバージョンの互換性を確認

2. **メモリ不足エラー**
   - バッチサイズを小さくする
   - 画像サイズを縮小する
   - CPUモードで実行する

3. **モデルダウンロードエラー**
   - インターネット接続を確認
   - プロキシ設定が正しいか確認

4. **NLTK データエラー**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('wordnet')
   nltk.download('averaged_perceptron_tagger')
   ```

## 📚 参考文献・使用ライブラリ

- [BLIP: Bootstrapping Language-Image Pre-training](https://github.com/salesforce/BLIP)
- [CLIP: Contrastive Language-Image Pre-training](https://github.com/openai/CLIP)
- [YOLOv8: Ultralytics](https://github.com/ultralytics/ultralytics)
- [SAM: Segment Anything](https://github.com/facebookresearch/segment-anything)
- [WordNet: NLTK](https://www.nltk.org/howto/wordnet.html)

##  ライセンス

本プロジェクトは教育・研究目的で作成されたオリジナル実装です。使用しているオープンソースライブラリはそれぞれのライセンスに従います。

## 🤝 貢献

学術研究プロジェクトです。改善提案やバグレポートは歓迎します。

## 📞 サポート

技術的な質問や問題については、Issueを作成してください。