#!/usr/bin/env python3
"""
Vercel Webサイト構成詳細分析システム
"""

import os
import json
from pathlib import Path
from datetime import datetime
import re

class VercelSiteAnalyzer:
    def __init__(self):
        self.public_dir = Path("public")
        self.analysis_result = {}
        
    def analyze_site_structure(self):
        """サイト構造を詳細分析"""
        print("📊 Vercel Webサイト構成分析開始...")
        
        structure = {
            "pages": {},
            "assets": {},
            "features": {},
            "total_files": 0,
            "total_size": 0
        }
        
        # 各HTMLページを分析
        for html_file in self.public_dir.rglob("*.html"):
            relative_path = html_file.relative_to(self.public_dir)
            file_size = html_file.stat().st_size
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                line_count = len(content.split('\n'))
                
            # コンテンツ分析
            features = self.analyze_page_features(content)
            
            structure["pages"][str(relative_path)] = {
                "size": file_size,
                "lines": line_count,
                "features": features,
                "last_modified": datetime.fromtimestamp(html_file.stat().st_mtime).isoformat()
            }
            
            structure["total_files"] += 1
            structure["total_size"] += file_size
        
        # 静的アセット分析
        for asset_file in self.public_dir.rglob("*"):
            if asset_file.is_file() and not asset_file.name.endswith('.html'):
                relative_path = asset_file.relative_to(self.public_dir)
                file_size = asset_file.stat().st_size
                
                extension = asset_file.suffix
                if extension not in structure["assets"]:
                    structure["assets"][extension] = {"count": 0, "total_size": 0}
                
                structure["assets"][extension]["count"] += 1
                structure["assets"][extension]["total_size"] += file_size
        
        self.analysis_result = structure
        return structure
    
    def analyze_page_features(self, content):
        """ページの機能を分析"""
        features = {
            "interactive_elements": 0,
            "charts": False,
            "forms": False,
            "navigation": False,
            "responsive": False,
            "animations": False,
            "external_apis": [],
            "frameworks": []
        }
        
        # インタラクティブ要素
        features["interactive_elements"] = len(re.findall(r'onclick|addEventListener|function\s+\w+', content))
        
        # チャート・グラフ
        if "Chart.js" in content or "chart" in content.lower():
            features["charts"] = True
            
        # フォーム要素
        if "<form" in content or "<input" in content:
            features["forms"] = True
            
        # ナビゲーション
        if "nav" in content.lower() or "menu" in content.lower():
            features["navigation"] = True
            
        # レスポンシブ
        if "@media" in content or "viewport" in content:
            features["responsive"] = True
            
        # アニメーション
        if "animation" in content or "transition" in content or "@keyframes" in content:
            features["animations"] = True
        
        # 外部API
        external_apis = re.findall(r'https?://[^"\s]+(?:api|cdn|jsdelivr)[^"\s]*', content)
        features["external_apis"] = list(set(external_apis))
        
        # フレームワーク検出
        if "Chart.js" in content:
            features["frameworks"].append("Chart.js")
        if "bootstrap" in content.lower():
            features["frameworks"].append("Bootstrap")
        if "react" in content.lower():
            features["frameworks"].append("React")
            
        return features
    
    def generate_analysis_report(self):
        """分析レポート生成"""
        report = f"""# 📊 Vercel Webサイト構成詳細分析レポート
生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 🌐 サイト全体概要
- **総ファイル数**: {self.analysis_result['total_files']}個
- **総サイズ**: {self.analysis_result['total_size'] / 1024:.1f} KB
- **ページ数**: {len(self.analysis_result['pages'])}ページ

## 📄 ページ別詳細分析

"""
        
        for page_path, page_info in self.analysis_result['pages'].items():
            report += f"""### 📋 {page_path}
- **サイズ**: {page_info['size']} bytes ({page_info['lines']} lines)
- **最終更新**: {page_info['last_modified'][:19]}
- **機能概要**:
  - インタラクティブ要素: {page_info['features']['interactive_elements']}個
  - チャート/グラフ: {'✅' if page_info['features']['charts'] else '❌'}
  - フォーム: {'✅' if page_info['features']['forms'] else '❌'}
  - ナビゲーション: {'✅' if page_info['features']['navigation'] else '❌'}
  - レスポンシブ: {'✅' if page_info['features']['responsive'] else '❌'}
  - アニメーション: {'✅' if page_info['features']['animations'] else '❌'}
  - 使用フレームワーク: {', '.join(page_info['features']['frameworks']) if page_info['features']['frameworks'] else 'なし'}

"""
        
        report += "## 📦 アセット分析\n"
        for ext, info in self.analysis_result['assets'].items():
            report += f"- **{ext}**: {info['count']}ファイル ({info['total_size']} bytes)\n"
        
        return report
    
    def identify_improvement_areas(self):
        """改善すべきエリアを特定"""
        improvements = {
            "missing_features": [],
            "enhancement_opportunities": [],
            "new_page_suggestions": [],
            "technical_improvements": []
        }
        
        # 各ページの機能チェック
        for page_path, page_info in self.analysis_result['pages'].items():
            features = page_info['features']
            
            # 欠けている機能を特定
            if not features['charts'] and 'experiment' not in page_path:
                improvements["missing_features"].append(f"{page_path}: グラフ・チャート機能")
                
            if not features['forms'] and 'main-system' in page_path:
                improvements["missing_features"].append(f"{page_path}: ユーザー入力フォーム")
                
            if features['interactive_elements'] < 3:
                improvements["enhancement_opportunities"].append(f"{page_path}: インタラクティブ性向上")
        
        # 新ページ提案
        existing_pages = set(self.analysis_result['pages'].keys())
        
        suggested_pages = [
            "api-documentation/index.html",
            "research-timeline/index.html", 
            "comparison-tools/index.html",
            "dataset-explorer/index.html",
            "real-time-demo/index.html",
            "publication-tracker/index.html",
            "collaboration-hub/index.html"
        ]
        
        for page in suggested_pages:
            if page not in existing_pages:
                improvements["new_page_suggestions"].append(page)
        
        # 技術的改善
        improvements["technical_improvements"] = [
            "Progressive Web App (PWA) 対応",
            "API エンドポイント追加",
            "リアルタイムデータ連携",
            "ユーザー認証システム",
            "データベース統合",
            "検索機能追加",
            "フィルタリング機能",
            "エクスポート機能"
        ]
        
        return improvements

def main():
    analyzer = VercelSiteAnalyzer()
    
    # サイト構造分析
    structure = analyzer.analyze_site_structure()
    
    # 分析レポート生成
    report = analyzer.generate_analysis_report()
    
    # 改善エリア特定
    improvements = analyzer.identify_improvement_areas()
    
    # レポート保存
    with open("vercel_site_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 改善提案保存
    with open("site_improvement_suggestions.json", 'w', encoding='utf-8') as f:
        json.dump(improvements, f, indent=2, ensure_ascii=False)
    
    print("✅ Vercel サイト分析完了")
    print(f"📄 分析レポート: vercel_site_analysis_report.md")
    print(f"💡 改善提案: site_improvement_suggestions.json")
    
    # 主要統計表示
    print(f"\n📊 主要統計:")
    print(f"  - ページ数: {len(structure['pages'])}")
    print(f"  - 総サイズ: {structure['total_size'] / 1024:.1f} KB")
    print(f"  - 改善提案: {len(improvements['new_page_suggestions'])}ページ")
    
    return structure, improvements

if __name__ == "__main__":
    main()