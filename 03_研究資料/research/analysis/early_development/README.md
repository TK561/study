# 初期開発段階ファイル（第0-2回）

## 📋 概要
研究の初期段階（第0回～第2回）で開発・使用された画像処理基盤ファイルを保管しています。

---

## 📄 ファイル一覧

### gazo-shori_main.py
**使用期間**: 第0-2回（2024年3月21日～2025年4月3日）  
**主要使用**: 第1回画像処理基盤構築時  
**目的**: 基本的な画像処理機能の実装  

**主要機能**:
- 画像の範囲選択機能
- 選択範囲内の分析・塗りつぶし処理
- グラフ作成機能
- 日本語パス対応の画像読み込み・保存

**技術仕様**:
- OpenCV (cv2) を使用
- Tkinter による GUI
- NumPy による画像処理
- BGR形式での画像読み込み

### gazo-shori_sub.py
**使用期間**: 第0-2回（2024年3月21日～2025年4月3日）  
**主要使用**: 第2回半自動化機能導入時  
**目的**: YOLOモデル統合による半自動化  

**主要機能**:
- YOLOv8 モデル統合
- 範囲選択の半自動化
- 手動選択から自動検出への移行開始
- UI/UX向上

**技術仕様**:
- Ultralytics YOLO を使用
- YOLOv8n.pt モデル読み込み
- PIL (Python Imaging Library) 統合
- ファイル選択ダイアログ

---

## 🔄 研究進展との関連

### 第0回（2024/3/21）：基礎環境構築
- Python実行環境の準備
- 画像読み込み・処理・表示の基本機能実装目標設定
- **ファイル準備**: `gazo-shori_main.py`, `gazo-shori_sub.py` の初期版

### 第1回（2025/3/27）：画像処理基盤の構築
- **成果**: `gazo-shori_main.py` による基本機能実装
- **技術内容**: 選択範囲内の分析・塗りつぶし処理
- **UI改善**: グラフ作成機能の追加

### 第2回（2025/4/3）：半自動化機能の導入
- **成果**: `gazo-shori_sub.py` による半自動化実装
- **技術的進歩**: 手動選択から自動検出への移行開始
- **基盤技術**: UI/UX向上とユーザビリティ改善

### 第3回以降の発展
- マルチモデル統合の検討
- システム統合とエラー対応
- AI技術統合による精度向上
- 最終的に87.1%の精度達成

---

## 🎯 技術的価値

### 基盤技術として
- 研究の出発点となった重要なファイル
- 画像処理の基本機能を確立
- 後の高度なAI統合システムの基礎

### 学習価値として
- 単純な画像処理から複雑なAIシステムへの発展過程
- 段階的な技術向上の実例
- 問題解決アプローチの変遷

### 保存理由
- 研究の完全な記録として
- 初期アプローチの参照用
- 技術発展の軌跡保存

---

## ⚠️ 注意事項

### 依存関係
- OpenCV (cv2)
- Tkinter
- NumPy
- Ultralytics YOLO
- PIL (Pillow)

### 実行環境
- Python 3.x
- YOLOv8モデル（yolov8n.pt）が必要

### 現在の状態
- アーカイブ目的で保存
- 現在の研究では使用されていない
- 参考・学習目的での参照可能

---

**保存日**: 2025年6月25日  
**保存理由**: 研究初期段階の重要な技術基盤として  
**関連記録**: `/study/research_discussions/WEEKLY_DISCUSSION_SUMMARY.md` 第1-2回参照