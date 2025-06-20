# CLAUDE.md - 研究プロジェクト用ガイドライン

Claude Code を使用した研究プロジェクトの開発・管理ガイドライン

## プロジェクト概要

**プロジェクト名**: 意味カテゴリに基づく画像分類システム  
**研究目的**: WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価  
**開発手法**: Claude Code を活用したAI支援研究開発  

## 自動初期化システム (NEW!)

### **Claude Code起動時の自動実行**
```bash
# Claude Code起動時に自動実行される
python .claude_code_init.py
```

#### **自動で実行される機能**
- 1時間毎レポートシステム自動起動
- プロジェクト検出・環境設定  
- セッション管理開始
- Git活動追跡開始

#### **動作確認**
```bash
# システム状態確認
cat session_logs/current_session.json

# デーモン制御
python scripts/enhanced_hourly_daemon.py --daemon  # 起動
python scripts/enhanced_hourly_daemon.py --stop    # 停止
```

## 1時間毎自動レポート機能

### **完全自動実行**
- **トリガー**: Claude Code起動時
- **実行間隔**: 1時間毎
- **動作方式**: バックグラウンドデーモン
- **ログ保存**: `session_logs/session_YYYYMMDD_HHMMSS.json`

### **レポート内容**
- ファイル変更追跡: 新規作成・更新ファイル一覧
- Git活動記録: コミット・ブランチ状況
- 作業時間計測: セッション開始からの経過時間
- 進捗サマリー: 完了タスクと次のステップ

## Claude Code 活用方針

### 1. 基本原則
- **透明性**: すべてのAI生成コードに適切な署名とコメントを付与
- **再現性**: 実験手順とコードを詳細に記録
- **検証性**: AI生成コードの品質と正確性を人間が検証
- **継続性**: Claude Code の能力を活用した持続的な研究開発

### 2. 推奨される使用方法

#### コード生成
```python
# Claude Code で生成されたコードには以下の署名を追加
"""
Generated with Claude Code
Date: YYYY-MM-DD
Purpose: [目的の説明]
Verified: [検証済み/要検証]
"""
```

#### 実験ノートブック
- Jupyter Notebook の各セルに実行目的を記載
- 結果の解釈と考察を Claude Code と協力して作成
- 再現性を確保するためのシード値設定

#### ドキュメント作成
- README.md の自動生成・更新
- API ドキュメントの生成
- 研究レポートの構造化

##  開発環境設定

### 必要なツール
- **Python 3.8+**: 主要開発言語
- **Jupyter Notebook**: 実験とデータ分析
- **Git**: バージョン管理
- **VS Code/Cursor**: Claude Code 統合開発環境

### 推奨パッケージ
```python
# 機械学習・画像処理
torch>=1.11.0
torchvision>=0.12.0
transformers>=4.20.0
opencv-python>=4.5.0
pillow>=8.3.0

# データ処理・可視化
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0

# 自然言語処理
nltk>=3.7.0

# 実験管理
mlflow>=1.24.0
wandb>=0.12.0

# コード品質
black>=22.0.0
flake8>=4.0.0
pytest>=7.0.0
```

##  プロジェクト構造

```
research-project/
├── data/                    # データファイル
│   ├── raw/                # 元データ
│   ├── processed/          # 処理済みデータ
│   └── external/           # 外部データ
├── notebooks/              # Jupyter Notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_development.ipynb
│   └── 03_evaluation.ipynb
├── src/                    # ソースコード
│   ├── data/              # データ処理
│   ├── models/            # モデル定義
│   ├── evaluation/        # 評価・メトリクス
│   └── utils/             # ユーティリティ
├── results/               # 実験結果
│   ├── figures/           # グラフ・図表
│   ├── models/            # 学習済みモデル
│   └── reports/           # レポート
├── docs/                  # ドキュメント
├── tests/                 # テストコード
├── config/                # 設定ファイル
├── scripts/               # 実行スクリプト・自動化
├── session_logs/          # セッション記録（自動生成）
├── experiments/           # 実験ログ
└── .claude_code_init.py   # 自動初期化スクリプト
```

##  実験管理ガイドライン

### 1. 実験設計
- **仮説の明確化**: 各実験の目的と期待される結果を記載
- **パラメータ管理**: ハイパーパラメータの体系的管理
- **ベースライン設定**: 比較対象となるベースライン手法の定義

### 2. 実験実行
```python
# 実験テンプレート（Claude Code 推奨）
def run_experiment(config):
    """
    実験実行関数
    
    Generated with Claude Code
    Purpose: [実験の目的]
    """
    # シード設定（再現性確保）
    set_seed(config.seed)
    
    # データ読み込み
    data = load_data(config.data_path)
    
    # モデル初期化
    model = initialize_model(config.model_config)
    
    # 学習実行
    results = train_model(model, data, config.training_config)
    
    # 評価実行
    metrics = evaluate_model(model, data.test, config.eval_config)
    
    # 結果記録
    log_experiment(config, results, metrics)
    
    return results, metrics
```

### 3. 結果記録
- **MLflow**: 実験パラメータとメトリクスの追跡
- **Weights & Biases**: リアルタイム実験監視
- **手動ログ**: 重要な発見や問題点の記録
- **自動セッションログ**: 1時間毎の進捗自動記録

##  データ管理

### 1. データの分類
- **Raw Data**: 変更不可の元データ
- **Processed Data**: 前処理済みデータ
- **Intermediate Data**: 中間処理結果
- **Final Data**: 最終的な学習・評価用データ

### 2. データ処理原則
```python
def process_data(raw_data_path, output_path):
    """
    データ処理関数
    
    Generated with Claude Code
    Purpose: 画像データの前処理とカテゴリ分類
    """
    # 処理ログの記録
    logger.info(f"Processing data from {raw_data_path}")
    
    # 前処理実行
    processed_data = preprocess_images(raw_data_path)
    
    # 品質チェック
    validate_data_quality(processed_data)
    
    # 保存
    save_processed_data(processed_data, output_path)
    
    logger.info(f"Data processing completed: {output_path}")
```

### 3. データ版数管理
- データセットの変更履歴を記録
- 実験結果との対応関係を明確化
- データの整合性チェック

##  品質保証

### 1. コード品質
```python
# Claude Code 生成コードの品質チェックリスト
def quality_check_template():
    """
    Generated with Claude Code
    Quality Checklist:
    - [ ] 型ヒント追加済み
    - [ ] docstring 記述済み
    - [ ] エラーハンドリング実装済み
    - [ ] ログ出力追加済み
    - [ ] テストケース作成済み
    - [ ] 人間による検証完了
    """
    pass
```

### 2. テスト戦略
- **Unit Tests**: 個別関数のテスト
- **Integration Tests**: モジュール間連携のテスト
- **End-to-End Tests**: 全体フローのテスト

### 3. 継続的検証
- GitHub Actions による自動テスト
- コードレビューの実施
- 実験結果の相互検証

##  ドキュメント管理

### 1. コード文書化
```python
def semantic_classification(image_path: str, model_config: dict) -> dict:
    """
    意味カテゴリに基づく画像分類
    
    Generated with Claude Code
    Date: 2024-01-15
    Purpose: WordNet階層を利用した特化型分類の実装
    
    Args:
        image_path (str): 入力画像のパス
        model_config (dict): モデル設定パラメータ
        
    Returns:
        dict: 分類結果と信頼度スコア
        
    Example:
        >>> result = semantic_classification("test.jpg", config)
        >>> print(result['category'], result['confidence'])
    """
    # 実装内容
    pass
```

### 2. 研究ノート
- 日々の研究進捗をMarkdownで記録
- 実験結果の解釈と考察
- 問題点と解決策の文書化
- **自動生成**: 1時間毎の進捗記録

### 3. 論文作成支援
- LaTeX テンプレートの準備
- 図表の自動生成コード
- 参考文献管理

##  デプロイメント・共有

### 1. モデル共有
```python
def save_model_for_sharing(model, metadata: dict, output_path: str):
    """
    研究成果の共有用モデル保存
    
    Generated with Claude Code
    Purpose: 再現可能な形でのモデル保存
    """
    # モデル保存
    torch.save(model.state_dict(), f"{output_path}/model.pth")
    
    # メタデータ保存
    metadata.update({
        'created_with': 'Claude Code',
        'framework': 'PyTorch',
        'timestamp': datetime.now().isoformat()
    })
    
    with open(f"{output_path}/metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
```

### 2. 結果の公開
- GitHub Pages での結果公開
- インタラクティブデモの作成
- 研究データセットの公開準備

## 🤝 Claude Code とのコラボレーション

### 1. 効果的な質問の仕方
```
良い例:
"WordNetの階層構造を利用して、画像分類の特化型ラベルセットを
動的に生成するPython関数を作成してください。
入力は画像キャプション、出力は関連する特化ラベルのリストです。"

悪い例:
"画像分類のコードを書いて"
```

### 2. コード改善の依頼
- 具体的な改善点を明示
- 性能要件や制約条件を明確化
- テストケースの例を提供

### 3. 研究支援の活用
- 論文のアウトライン作成
- 実験設計の相談
- 結果解釈の支援

##  成果評価

### 1. 定量的評価
- 分類精度の改善度
- 計算時間の効率化
- メモリ使用量の最適化

### 2. 定性的評価
- コードの可読性・保守性
- 研究プロセスの効率化
- 新しい知見の発見

### 3. 研究貢献度
- 学術的新規性
- 実用的価値
- 再現可能性

##  トラブルシューティング

### よくある問題と解決策

#### 1. モデル学習の不安定性
```python
# Claude Code 推奨解決策
def stable_training_setup():
    """安定した学習環境の設定"""
    # シード固定
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)
    
    # 決定的アルゴリズム使用
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

#### 2. メモリ不足
- バッチサイズの調整
- グラディエント蓄積の使用
- データローダーの最適化

#### 3. 実験の再現不可能性
- 環境設定の明確化
- 依存関係の固定
- データ処理過程の記録

## 📞 サポートとコミュニケーション

### 1. 問題報告
- 具体的なエラーメッセージ
- 実行環境の情報
- 再現手順の詳細

### 2. 改善提案
- 現在の問題点の明確化
- 期待される改善効果
- 実装の優先度

### 3. 研究ディスカッション
- 定期的な進捗レビュー
- 新しいアイデアの共有
- 文献調査の結果共有

---

** Claude Code を活用した効率的で高品質な研究開発を実現しましょう！**

##  GitHub Actions CI/CD Integration

### 自動化システム概要
完全自動化されたGitHub Actions + Vercel + Claude Code統合システム

#### ワークフロー
1. **`vercel-deploy.yml`**: プッシュ時の自動デプロイ
2. **`claude-autofix.yml`**: エラー時の自動修正
3. **`monitoring.yml`**: 30分毎の監視

#### 必要なシークレット
```bash
# GitHub Repositoryの設定で追加
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id  
VERCEL_PROJECT_ID=prj_gm8o7yYpKf4fEf1ydU5oQwZGH5dV
```

#### 自動修正機能
- Vercel設定エラー → 自動修正
- Python関数エラー → 自動修正  
- デプロイ失敗 → GitHub Issue作成 → 自動修正
- 監視アラート → 自動復旧

#### 使用方法
```bash
# 手動で自動修正をトリガー
gh workflow run claude-autofix.yml -f error_type=deployment_failure

# 監視状況確認
gh run list --workflow=monitoring.yml
```

---

*Generated with Claude Code - Research Project Guidelines*  
*Last Updated: 2025-06-20 (Auto-Initialization System Added)*