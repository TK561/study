# 📁 提案する新しいプロジェクト構造

## 🎯 設計原則
1. **機能別分離**: 研究・自動化・Web・設定を明確に分離
2. **階層化**: 3層以内の浅い構造
3. **一貫性**: 統一された命名規則
4. **保守性**: 容易な検索・管理

## 📂 新しいディレクトリ構造

```
/mnt/c/Desktop/Research/
├── 📖 CORE FILES (ルート - 最重要ファイルのみ)
│   ├── README.md
│   ├── CLAUDE.md
│   ├── package.json
│   ├── requirements.txt
│   └── vercel.json
│
├── 🔬 research/ (研究関連)
│   ├── notebooks/
│   │   ├── Auto_Research_Colab.ipynb
│   │   ├── Research_Colab_Simple.ipynb
│   │   ├── Research_Project_Colab.ipynb
│   │   └── Colab_Research_Integration.ipynb
│   ├── experiments/
│   │   ├── baseline_comparison_experiment.py
│   │   ├── performance_optimization_experiment.py
│   │   ├── scalability_experiment.py
│   │   └── unimplemented_experiments.py
│   ├── implementations/
│   │   ├── confidence_feedback_implementation.py
│   │   ├── enhanced_features_implementation.py
│   │   └── pptx_system_implementation.py
│   ├── analysis/
│   │   └── (既存のstudyディレクトリの内容)
│   └── reports/
│       ├── confidence_feedback_implementation_report.md
│       ├── enhanced_features_report.md
│       └── pptx_systems_implementation_report.md
│
├── 🤖 automation/ (自動化システム)
│   ├── core/
│   │   ├── auto_organize_and_save.py
│   │   ├── claude_auto_restore.py
│   │   ├── auto_system_coordinator.py
│   │   └── coordinated_startup.py
│   ├── development/
│   │   ├── auto_dev_workflow.py
│   │   ├── github_actions_automation.py
│   │   └── auto_research_trigger.py
│   ├── text/
│   │   ├── textlint_auto_runner.py
│   │   ├── textlint_scheduler.py
│   │   └── textlint_watcher.py
│   ├── deployment/
│   │   ├── deploy.sh
│   │   └── direct_vercel_deploy.py
│   └── monitoring/
│       └── (既存のautomationディレクトリの内容)
│
├── 🌐 web/ (Web関連)
│   ├── public/
│   │   └── (既存のpublicディレクトリの内容)
│   ├── components/
│   └── utils/
│       ├── html_experiment_graphs.py
│       ├── reorder_experiment_results.py
│       └── vercel_site_analysis.py
│
├── ⚙️ config/ (設定・スクリプト)
│   ├── environment/
│   │   ├── setup-shift-enter.sh
│   │   ├── setup_textlint_hooks.sh
│   │   ├── terminal-setup.sh
│   │   └── recovery-test.sh
│   ├── ci-cd/
│   │   └── .github/ (既存の.githubディレクトリ)
│   ├── development/
│   │   ├── .vscode/
│   │   ├── colab_compatibility.py
│   │   └── colab_setup.py
│   └── startup/
│       ├── claude_startup_integration.py
│       └── start_textlint_auto.sh
│
├── 📚 docs/ (ドキュメント)
│   ├── guides/
│   │   ├── COLAB_USAGE.md
│   │   ├── SHIFT_ENTER_SETUP.md
│   │   ├── SIRIUS_AUTOMATION_USAGE.md
│   │   ├── TEXTLINT_USAGE.md
│   │   └── TEXTLINT_AUTO_USAGE.md
│   ├── summaries/
│   │   ├── SESSION_COMPLETION_SUMMARY.md
│   │   ├── VERCEL_DEPLOYMENT_SUMMARY.md
│   │   └── vercel_site_analysis_report.md
│   └── legacy/ (既存のdocsディレクトリ内容)
│
├── 🔧 tools/ (ユーティリティ)
│   ├── research/
│   │   └── research_analysis_system.py
│   ├── deployment/
│   │   └── vercel_quick_deploy.sh
│   └── maintenance/
│       ├── クイック整理.py
│       ├── フォルダ整理ツール.py
│       ├── プロジェクト整理.py
│       └── 包括的整理システム.py
│
├── 📝 sessions/ (セッション記録)
│   └── (既存の内容)
│
├── 📦 system/ (システム実装)
│   └── implementations/ (既存の内容)
│
└── 🗄️ data/ (一時的・生成データ)
    ├── logs/
    ├── cache/
    ├── backups/
    └── temp/
```

## 🔄 移行計画

### Phase 1: ディレクトリ作成
- 新しいディレクトリ構造を作成
- 既存ファイルはそのまま保持

### Phase 2: ファイル移動
- カテゴリ別にファイルを段階的に移動
- 移動後に動作確認

### Phase 3: 参照更新
- スクリプト内のパス参照を更新
- 設定ファイルのパス更新

### Phase 4: 検証・最適化
- 全システムの動作確認
- ドキュメント更新

## 🎯 期待される効果

1. **可読性向上**: ファイルの役割が明確
2. **保守性向上**: 関連ファイルが集約
3. **拡張性向上**: 新機能の追加が容易
4. **協業性向上**: チーム開発に適した構造
5. **自動化向上**: CI/CDとの親和性

## ⚠️ 注意事項

- 移行は段階的に実施
- 重要なファイルは事前バックアップ
- 各段階で動作確認を実施
- CLAUDE.mdの設定を最優先で保持