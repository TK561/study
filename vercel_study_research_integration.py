#!/usr/bin/env python3
"""
Vercel study-research統合システム
現在の独立プロジェクトをstudy-researchプロジェクトに統合
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from core.google_drive_utils import get_base_path, safe_save, timer

class VercelStudyResearchIntegrator:
    def __init__(self):
        self.base_path = get_base_path()
        self.current_project_id = "prj_RQylNerESGq4Q9liVAw7GEsAtaSH"
        self.current_domain = "study-research-final.vercel.app"
        
        # study-researchプロジェクトの情報（想定）
        self.target_project_name = "study-research"
        self.target_domain = "study-research.vercel.app"
        
        self.integration_plan = {
            "current_status": {
                "project_id": self.current_project_id,
                "domain": self.current_domain,
                "content_type": "WordNet画像分類研究",
                "structure": "独立プロジェクト"
            },
            "target_integration": {
                "project_name": self.target_project_name,
                "integration_type": "subdirectory",
                "path_prefix": "/research",
                "domain_strategy": "subdomain_or_path"
            }
        }
        
    def analyze_current_setup(self):
        """現在のVercel設定を分析"""
        print("🔍 現在のVercel設定分析中...")
        
        analysis = {
            "vercel_config": {},
            "project_structure": {},
            "deployment_assets": [],
            "routing_rules": []
        }
        
        # vercel.json分析
        vercel_config_path = self.base_path / "web_deployment" / "vercel.json"
        if vercel_config_path.exists():
            with open(vercel_config_path, 'r', encoding='utf-8') as f:
                analysis["vercel_config"] = json.load(f)
        
        # public/構造分析
        public_dir = self.base_path / "public"
        if public_dir.exists():
            for item in public_dir.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(public_dir)
                    analysis["deployment_assets"].append(str(relative_path))
        
        # ルーティング分析
        if "rewrites" in analysis["vercel_config"]:
            analysis["routing_rules"] = analysis["vercel_config"]["rewrites"]
        
        print(f"📊 分析結果:")
        print(f"  - デプロイアセット: {len(analysis['deployment_assets'])}個")
        print(f"  - ルーティング規則: {len(analysis['routing_rules'])}個")
        print(f"  - 現在のドメイン: {self.current_domain}")
        
        return analysis
    
    def design_integration_strategy(self):
        """統合戦略を設計"""
        print("🎯 study-research統合戦略設計中...")
        
        strategies = {
            "strategy_1_subdirectory": {
                "name": "サブディレクトリ統合",
                "description": "study-research.vercel.app/research/ として統合",
                "pros": [
                    "既存study-researchプロジェクトと統合",
                    "単一ドメインでの管理",
                    "SEO・ブランディング統一"
                ],
                "cons": [
                    "ルーティング設定の複雑化",
                    "既存URLの変更必要"
                ],
                "implementation": {
                    "path_prefix": "/research",
                    "domain": "study-research.vercel.app",
                    "routing_changes": "Required"
                }
            },
            "strategy_2_subdomain": {
                "name": "サブドメイン統合",
                "description": "research.study-research.vercel.app として統合",
                "pros": [
                    "独立性維持",
                    "ルーティング設定簡単",
                    "既存URL保持可能"
                ],
                "cons": [
                    "追加ドメイン設定必要",
                    "管理の複雑化"
                ],
                "implementation": {
                    "subdomain": "research",
                    "domain": "research.study-research.vercel.app",
                    "routing_changes": "Minimal"
                }
            },
            "strategy_3_project_merge": {
                "name": "プロジェクト完全統合",
                "description": "study-researchプロジェクトに完全統合",
                "pros": [
                    "管理の単純化",
                    "リソース効率化",
                    "統一されたデプロイ"
                ],
                "cons": [
                    "既存構造の大幅変更",
                    "移行時のリスク"
                ],
                "implementation": {
                    "merge_type": "full",
                    "target_structure": "/research_content",
                    "routing_changes": "Complete"
                }
            }
        }
        
        # 推奨戦略の選択
        recommended = "strategy_1_subdirectory"
        
        print(f"📋 統合戦略オプション:")
        for key, strategy in strategies.items():
            status = "🎯 推奨" if key == recommended else "📝"
            print(f"  {status} {strategy['name']}: {strategy['description']}")
        
        return strategies, recommended
    
    def create_integrated_vercel_config(self, strategy="subdirectory"):
        """統合後のvercel.json設定作成"""
        print("⚙️ 統合vercel.json設定作成中...")
        
        if strategy == "subdirectory":
            # サブディレクトリ統合設定
            integrated_config = {
                "version": 2,
                "name": "study-research",
                "buildCommand": "echo 'Building unified study-research site'",
                "outputDirectory": "public",
                "routes": [
                    {
                        "src": "/(.*)",
                        "dest": "/public/$1"
                    }
                ],
                "rewrites": [
                    # メインstudy-researchページ
                    {
                        "source": "/",
                        "destination": "/public/index.html"
                    },
                    # 研究セクション（新規統合部分）
                    {
                        "source": "/research",
                        "destination": "/public/research/index.html"
                    },
                    {
                        "source": "/research/main-system",
                        "destination": "/public/research/main-system/index.html"
                    },
                    {
                        "source": "/research/confidence-feedback",
                        "destination": "/public/research/confidence_feedback/index.html"
                    },
                    {
                        "source": "/research/pptx-systems",
                        "destination": "/public/research/pptx_systems/index.html"
                    },
                    {
                        "source": "/research/enhanced-features",
                        "destination": "/public/research/enhanced_features/index.html"
                    },
                    # レガシーURL対応（リダイレクト）
                    {
                        "source": "/main-system",
                        "destination": "/public/research/main-system/index.html"
                    },
                    {
                        "source": "/confidence_feedback",
                        "destination": "/public/research/confidence_feedback/index.html"
                    },
                    {
                        "source": "/pptx_systems",
                        "destination": "/public/research/pptx_systems/index.html"
                    }
                ],
                "headers": [
                    {
                        "source": "/(.*)",
                        "headers": [
                            {
                                "key": "Cache-Control",
                                "value": "public, max-age=3600"
                            }
                        ]
                    }
                ],
                "redirects": [
                    {
                        "source": "/main-system",
                        "destination": "/research/main-system",
                        "permanent": True
                    },
                    {
                        "source": "/confidence_feedback",
                        "destination": "/research/confidence-feedback", 
                        "permanent": True
                    },
                    {
                        "source": "/pptx_systems",
                        "destination": "/research/pptx-systems",
                        "permanent": True
                    }
                ]
            }
        
        elif strategy == "subdomain":
            # サブドメイン統合設定
            integrated_config = {
                "version": 2,
                "name": "study-research-unified",
                "buildCommand": "echo 'Building unified study-research with research subdomain'",
                "outputDirectory": "public",
                "routes": [
                    {
                        "src": "/(.*)",
                        "dest": "/public/$1"
                    }
                ],
                "rewrites": [
                    {
                        "source": "/",
                        "destination": "/public/index.html"
                    },
                    {
                        "source": "/main-system",
                        "destination": "/public/main-system/index.html"
                    },
                    {
                        "source": "/confidence_feedback",
                        "destination": "/public/confidence_feedback/index.html"
                    },
                    {
                        "source": "/pptx_systems",
                        "destination": "/public/pptx_systems/index.html"
                    }
                ],
                "headers": [
                    {
                        "source": "/(.*)",
                        "headers": [
                            {
                                "key": "Cache-Control",
                                "value": "public, max-age=3600"
                            }
                        ]
                    }
                ]
            }
        
        # 設定ファイル保存
        config_path = self.base_path / "web_deployment" / "vercel_integrated.json"
        safe_save(json.dumps(integrated_config, indent=2), config_path)
        
        print(f"✅ 統合vercel.json作成完了: {config_path}")
        return integrated_config, config_path
    
    def create_public_structure_migration(self, strategy="subdirectory"):
        """public/構造の移行計画作成"""
        print("📁 public/構造移行計画作成中...")
        
        current_public = self.base_path / "public"
        migration_plan = {
            "source_structure": [],
            "target_structure": [],
            "migration_commands": []
        }
        
        # 現在の構造調査
        if current_public.exists():
            for item in current_public.rglob('*'):
                if item.is_file():
                    relative_path = str(item.relative_to(current_public))
                    migration_plan["source_structure"].append(relative_path)
        
        if strategy == "subdirectory":
            # サブディレクトリ統合の場合
            for source_path in migration_plan["source_structure"]:
                if source_path == "index.html":
                    # メインindex.htmlは research/index.html に移動
                    target_path = f"research/{source_path}"
                else:
                    # その他のファイルは research/ 以下に移動
                    target_path = f"research/{source_path}"
                
                migration_plan["target_structure"].append(target_path)
                migration_plan["migration_commands"].append({
                    "action": "move",
                    "source": f"public/{source_path}",
                    "target": f"public/{target_path}"
                })
            
            # 新しいメインindex.htmlの作成が必要
            migration_plan["migration_commands"].append({
                "action": "create",
                "target": "public/index.html",
                "content_type": "main_landing_page"
            })
        
        elif strategy == "subdomain":
            # サブドメイン統合の場合（構造変更なし）
            migration_plan["target_structure"] = migration_plan["source_structure"].copy()
            migration_plan["migration_commands"].append({
                "action": "none",
                "note": "Subdomain strategy requires no public/ structure changes"
            })
        
        print(f"📊 移行計画:")
        print(f"  - 移行ファイル数: {len(migration_plan['source_structure'])}")
        print(f"  - 移行コマンド数: {len(migration_plan['migration_commands'])}")
        
        return migration_plan
    
    def create_main_landing_page(self):
        """統合後のメインランディングページ作成"""
        print("🏠 メインランディングページ作成中...")
        
        main_page_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study Research - 総合研究プラットフォーム</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 60px;
            color: white;
        }}
        .header h1 {{
            font-size: 3.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.3rem;
            opacity: 0.9;
        }}
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }}
        .project-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .project-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }}
        .project-card h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }}
        .project-card p {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .project-links {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }}
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        .btn-secondary {{
            background: #f8f9fa;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        .btn-secondary:hover {{
            background: #667eea;
            color: white;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 50px 0;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .stat-label {{
            color: #666;
            font-weight: 500;
        }}
        .footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Study Research</h1>
            <p>総合研究プラットフォーム - AI・機械学習・学術研究の統合環境</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">5+</div>
                <div class="stat-label">研究プロジェクト</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">87.1%</div>
                <div class="stat-label">最高精度達成</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">15+</div>
                <div class="stat-label">実装システム</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">自動化率</div>
            </div>
        </div>
        
        <div class="projects-grid">
            <!-- WordNet画像分類研究 -->
            <div class="project-card">
                <h2>🔬 WordNet画像分類研究</h2>
                <p>WordNet階層構造とCLIPを統合した革新的な画像分類システム。ベースライン手法を大幅に上回る87.1%の精度を達成。</p>
                <div class="project-links">
                    <a href="/research/" class="btn btn-primary">研究詳細</a>
                    <a href="/research/main-system/" class="btn btn-secondary">分類システム</a>
                    <a href="/research/confidence-feedback/" class="btn btn-secondary">信頼度システム</a>
                </div>
            </div>
            
            <!-- その他の研究プロジェクト（将来追加予定） -->
            <div class="project-card">
                <h2>🧠 AI統合システム</h2>
                <p>複数のAI技術を統合した包括的研究プラットフォーム。Google Drive/Colab環境での最適化された研究開発。</p>
                <div class="project-links">
                    <a href="/research/enhanced-features/" class="btn btn-primary">システム詳細</a>
                    <a href="/research/pptx-systems/" class="btn btn-secondary">プレゼン生成</a>
                </div>
            </div>
            
            <div class="project-card">
                <h2>📊 研究データ分析</h2>
                <p>実験結果の可視化・分析・レポート生成システム。統計的有意性検証とエラーケース分析を自動化。</p>
                <div class="project-links">
                    <a href="/research/" class="btn btn-primary">分析結果</a>
                    <a href="#" class="btn btn-secondary">Coming Soon</a>
                </div>
            </div>
            
            <div class="project-card">
                <h2>🌐 Webシステム統合</h2>
                <p>Vercel自動デプロイ・Google Drive統合・Colab環境最適化による完全自動化された研究開発環境。</p>
                <div class="project-links">
                    <a href="#" class="btn btn-primary">システム概要</a>
                    <a href="#" class="btn btn-secondary">ドキュメント</a>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <h3>🚀 継続的な研究開発</h3>
            <p>最新のAI技術と研究手法を統合し、学術的価値と実用性を両立した研究成果を創出</p>
            <p style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
                Last updated: {datetime.now().strftime('%Y年%m月%d日')} | Powered by Claude Code & Vercel
            </p>
        </div>
    </div>
</body>
</html>"""
        
        main_page_path = self.base_path / "public_integrated" / "index.html"
        main_page_path.parent.mkdir(exist_ok=True)
        safe_save(main_page_content, main_page_path)
        
        print(f"✅ メインランディングページ作成完了: {main_page_path}")
        return main_page_path
    
    def execute_integration_migration(self, strategy="subdirectory"):
        """統合移行を実行"""
        print("🚀 study-research統合移行実行中...")
        
        # 1. バックアップ作成
        backup_dir = self.base_path / f"vercel_integration_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(exist_ok=True)
        
        # 現在のpublic/をバックアップ
        current_public = self.base_path / "public"
        if current_public.exists():
            shutil.copytree(current_public, backup_dir / "public_original")
            print(f"💾 原本バックアップ: {backup_dir}")
        
        if strategy == "subdirectory":
            # 2. 新しいpublic/構造作成
            new_public = self.base_path / "public_integrated"
            new_public.mkdir(exist_ok=True)
            
            # 3. メインランディングページ作成
            self.create_main_landing_page()
            
            # 4. 研究コンテンツをresearch/以下に移動
            research_dir = new_public / "research"
            if current_public.exists():
                shutil.copytree(current_public, research_dir)
                print(f"📁 研究コンテンツ移動: {research_dir}")
            
            # 5. 統合vercel.json作成
            integrated_config, config_path = self.create_integrated_vercel_config("subdirectory")
            
            # 6. 統合用vercel.jsonをweb_deployment/に配置
            final_config_path = self.base_path / "web_deployment" / "vercel.json"
            shutil.copy2(config_path, final_config_path)
            
            print("✅ サブディレクトリ統合完了")
            
        elif strategy == "subdomain":
            # サブドメイン統合（構造変更最小）
            integrated_config, config_path = self.create_integrated_vercel_config("subdomain")
            print("✅ サブドメイン統合準備完了")
        
        # 7. 移行レポート作成
        migration_report = {
            "integration_timestamp": datetime.now().isoformat(),
            "strategy": strategy,
            "backup_location": str(backup_dir),
            "changes_made": [
                f"統合戦略: {strategy}",
                "vercel.json設定更新",
                "public/構造最適化" if strategy == "subdirectory" else "設定のみ更新",
                "メインランディングページ作成" if strategy == "subdirectory" else "既存構造保持"
            ],
            "next_steps": [
                "Vercelプロジェクト設定更新",
                "ドメイン設定変更",
                "デプロイテスト実行",
                "DNS設定確認"
            ]
        }
        
        report_path = self.base_path / f"vercel_integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        safe_save(json.dumps(migration_report, indent=2), report_path)
        
        print(f"📋 移行レポート作成: {report_path}")
        return migration_report, backup_dir
    
    def create_deployment_instructions(self):
        """デプロイ手順書作成"""
        print("📖 デプロイ手順書作成中...")
        
        instructions = f"""# 🌐 Vercel study-research統合デプロイ手順

## 📋 統合概要
- **統合前**: study-research-final.vercel.app (独立プロジェクト)
- **統合後**: study-research.vercel.app/research/ (サブディレクトリ統合)

## 🚀 デプロイ手順

### 1. 事前準備
```bash
# Google Drive/Colab環境で実行
cd /content/drive/MyDrive/research
```

### 2. 統合設定の適用
```bash
# 統合後のpublic/構造を使用
cp -r public_integrated/* public/

# 統合vercel.json設定を適用
cp web_deployment/vercel.json ./vercel.json
```

### 3. Vercelプロジェクト設定更新
```bash
# Vercel CLI経由でプロジェクト名変更
vercel --name study-research

# または新規プロジェクトとして作成
vercel --name study-research --force
```

### 4. ドメイン設定
```bash
# 既存ドメインの更新
vercel domains add study-research.vercel.app

# 古いドメインからのリダイレクト設定
vercel alias study-research-final.vercel.app study-research.vercel.app
```

### 5. デプロイ実行
```bash
# 本番デプロイ
vercel --prod --yes
```

### 6. 動作確認
```bash
# 主要URLの確認
curl -I https://study-research.vercel.app/
curl -I https://study-research.vercel.app/research/
curl -I https://study-research.vercel.app/research/main-system/
```

## 🔧 トラブルシューティング

### ドメイン競合の場合
```bash
# 一意なプロジェクト名を使用
vercel --name study-research-unified

# カスタムドメインの設定
vercel domains add your-custom-domain.com
```

### ルーティングエラーの場合
```bash
# vercel.json設定確認
cat vercel.json

# キャッシュクリア後再デプロイ
vercel --force --prod
```

## 📊 統合後のURL構造

### メインサイト
- `https://study-research.vercel.app/` - 統合ランディングページ

### 研究セクション
- `https://study-research.vercel.app/research/` - WordNet研究メイン
- `https://study-research.vercel.app/research/main-system/` - 分類システム
- `https://study-research.vercel.app/research/confidence-feedback/` - 信頼度システム
- `https://study-research.vercel.app/research/pptx-systems/` - プレゼンシステム
- `https://study-research.vercel.app/research/enhanced-features/` - 拡張機能

### レガシーURL（自動リダイレクト）
- `/main-system/` → `/research/main-system/`
- `/confidence_feedback/` → `/research/confidence-feedback/`
- `/pptx_systems/` → `/research/pptx-systems/`

## 🎯 統合後の利点

1. **統一ブランディング**: 単一study-researchブランド
2. **SEO最適化**: 統合ドメインでの権威性向上  
3. **管理効率化**: プロジェクト統合による運用簡素化
4. **拡張性**: 将来の研究プロジェクト追加容易

---
生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
"""
        
        instructions_path = self.base_path / "VERCEL_STUDY_RESEARCH_INTEGRATION_GUIDE.md"
        safe_save(instructions, instructions_path)
        
        print(f"✅ デプロイ手順書作成完了: {instructions_path}")
        return instructions_path
    
    def run_integration_process(self, strategy="subdirectory"):
        """統合プロセス全体実行"""
        print("🌐 Vercel study-research統合プロセス開始")
        print("=" * 60)
        
        # 1. 現状分析
        with timer("現状分析"):
            current_analysis = self.analyze_current_setup()
        
        # 2. 統合戦略設計
        with timer("統合戦略設計"):
            strategies, recommended = self.design_integration_strategy()
            print(f"🎯 採用戦略: {strategy}")
        
        # 3. 統合移行実行
        with timer("統合移行実行"):
            migration_report, backup_dir = self.execute_integration_migration(strategy)
        
        # 4. デプロイ手順書作成
        with timer("手順書作成"):
            instructions_path = self.create_deployment_instructions()
        
        print("=" * 60)
        print("✅ Vercel study-research統合準備完了！")
        print(f"💾 バックアップ: {backup_dir}")
        print(f"📖 手順書: {instructions_path}")
        print(f"🎯 統合戦略: {strategy}")
        
        print("\n📋 次のステップ:")
        print("1. 統合設定の確認")
        print("2. Vercelプロジェクト設定更新")
        print("3. ドメイン設定変更")
        print("4. 本番デプロイ実行")
        print("5. 動作確認・テスト")
        
        return migration_report, backup_dir, instructions_path

def main():
    """メイン実行"""
    integrator = VercelStudyResearchIntegrator()
    return integrator.run_integration_process("subdirectory")

if __name__ == "__main__":
    main()