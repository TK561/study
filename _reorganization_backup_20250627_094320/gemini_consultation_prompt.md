# 🤖 Gemini AI相談プロンプト - Research Folder整理

## 📋 相談内容

私のresearchフォルダが散らばっており、以下の問題があります。Gemini AIに最適な整理方法を相談したいです。

## 🔍 現在の状況分析

### 📁 現在のフォルダ構造の問題点
1. **200MBのうち180MBがarchive重複データ**
2. **26個のnode_modulesディレクトリが重複**
3. **15個のPythonスクリプトが機能別にバラバラ**
4. **実験結果ファイルが散在**
5. **ドキュメントが目的別に整理されていない**

### 📊 ファイル分類
- **実験スクリプト**: 7個 (baseline, performance, scalability等)
- **統合システム**: 4個 (google_drive_utils, migration等)
- **Web/Vercel関連**: 3個 (deploy, analysis等)
- **ドキュメント**: 5個 (README, guides等)
- **設定ファイル**: 3個 (package.json, vercel.json等)
- **実験結果**: 7個 (JSON, ログファイル)
- **重複バックアップ**: 180MB (archiveフォルダ)

## 🎯 Gemini AIへの相談ポイント

### 質問1: 最適なディレクトリ構造
```
あなたは研究プロジェクト管理の専門家です。

以下の条件でWordNetベースの画像分類研究プロジェクトの
最適なフォルダ構造を提案してください：

【現在の問題】
- 15個のPythonスクリプトが散在
- 重複バックアップが180MB
- 機能別の整理ができていない
- Google Drive/Colab環境での作業性重視

【ファイル種類】
- 実験スクリプト(baseline, performance, scalability等)
- システム統合(Drive, Vercel, migration)
- ドキュメント(README, setup guides等)
- 実験結果データ(JSON, ログ)
- Web assets(public/)
- 設定ファイル

【要求】
- 論理的で直感的な構造
- 将来の拡張性
- Google Drive/Colab環境最適化
- 検索・管理の容易さ
- ストレージ効率化

最適なディレクトリ構造と移動計画を具体的に提案してください。
```

### 質問2: ファイル統合・削除判断
```
以下のファイル群の統合・削除について判断をお願いします：

【重複問題】
- archive/cleanup_archive/ vs archive/comprehensive_cleanup_backup/
  (同内容で90MB重複)
- 26個のnode_modulesディレクトリ
- 古いHTMLバックアップファイル群

【機能重複スクリプト】
- google_drive_utils.py vs gdrive_integration.py
- multiple vercel deployment scripts
- experimental result processing scripts

【判断基準】
- 機能の重複度
- 将来的な必要性
- メンテナンスコスト
- ストレージ効率

具体的にどのファイルを統合・削除すべきか教えてください。
```

### 質問3: 作業効率最適化
```
Google Drive/Colab環境での研究作業効率を最大化するための
ファイル整理戦略を教えてください：

【現在の作業パターン】
- Colabでの実験実行
- Vercelへのデプロイ
- 結果分析・レポート作成
- 継続的な機能追加

【改善したい点】
- ファイル検索時間の短縮
- 関連ファイルへの素早いアクセス
- 実験結果の系統的管理
- バックアップ・復元の効率化

【技術的制約】
- Google Driveの同期特性
- Colabの一時的な性質
- ストレージ容量制限

最適な整理方法と作業フローを提案してください。
```

## 🔄 期待する回答内容

### A. 構造提案
- 具体的なディレクトリツリー
- 各フォルダの目的・役割
- ファイル分類ルール

### B. 移行計画
- 段階的な整理手順
- 優先順位付け
- リスク回避方法

### C. 最適化戦略
- ストレージ効率化
- アクセス性向上
- 管理性強化

## 📝 Geminiに送信するプロンプト

```markdown
# 研究プロジェクトフォルダ整理の相談

あなたは研究プロジェクト管理とファイル整理の専門家です。

WordNetベースの画像分類研究プロジェクトのフォルダが散乱しており、
Google Drive/Colab環境での効率的な作業のために整理が必要です。

## 現在の問題状況
- 総容量200MBのうち180MBが重複バックアップ
- 15個のPythonスクリプトが機能別に散在
- 26個のnode_modulesディレクトリが重複
- 実験結果ファイルが系統的に整理されていない

## ファイル構成
**実験関連**: baseline_comparison_experiment.py, performance_optimization_experiment.py, scalability_experiment.py等
**システム統合**: google_drive_utils.py, gdrive_integration.py, migration_script.py等  
**Web/デプロイ**: vercel_deploy_from_colab.py, vercel_site_analysis.py等
**ドキュメント**: README.md, setup guides, deployment guides等
**結果データ**: experiment_results_*.json, execution logs等

## 要求
1. **最適なディレクトリ構造の提案**
   - 論理的で直感的な分類
   - Google Drive/Colab環境に最適化
   - 将来の拡張性考慮

2. **ファイル統合・削除の判断**
   - 重複ファイルの処理方針
   - 機能重複スクリプトの統合方法
   - 不要ファイルの特定

3. **作業効率最適化戦略**
   - 検索・アクセス性向上
   - バックアップ・復元効率化
   - ストレージ使用量削減

具体的で実践的な整理計画を段階的に提案してください。
```