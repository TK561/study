#!/usr/bin/env python3
"""
Vercelサイト統一デザイン相談システム
Geminiと相談してサイト全体の書式・配置を統一する
"""

import json
import os
from datetime import datetime
import google.generativeai as genai

def setup_gemini():
    """Gemini APIの設定"""
    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDBjeBJSQo12rtBz0Q-XOa6Ju1cPT3H-nU')
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def analyze_current_site_structure():
    """現在のサイト構造を分析"""
    site_analysis = {
        "main_pages": {
            "index.html": {
                "path": "/",
                "description": "メインランディングページ",
                "current_style": "グラデーション背景、カード式レイアウト、統計情報表示",
                "issues": ["ナビゲーションバーなし", "一貫性のないスタイル"]
            },
            "main-system/index.html": {
                "path": "/main-system/",
                "description": "メイン分類システム",
                "current_style": "異なる色配置、独自ヘッダー",
                "issues": ["メインページと異なるデザイン", "フォントサイズ不統一"]
            },
            "discussion-site/index.html": {
                "path": "/discussion-site/",
                "description": "ディスカッション記録",
                "current_style": "別のレイアウトシステム",
                "issues": ["完全に異なるデザイン言語", "ナビゲーション不統一"]
            },
            "experiment_timeline/index.html": {
                "path": "/experiment_timeline/",
                "description": "実験タイムライン",
                "current_style": "Chart.js統合、独自スタイル",
                "issues": ["他ページとの視覚的一貫性なし"]
            },
            "experiment_results/experiment_graphs.html": {
                "path": "/experiment_results/",
                "description": "実験結果グラフ",
                "current_style": "最新の統一デザイン適用済み",
                "issues": ["比較的統一されているが他ページとの整合性要確認"]
            }
        },
        "design_issues": [
            "各ページで異なるナビゲーションシステム",
            "カラーパレット不統一",
            "フォントサイズ・ファミリー不統一", 
            "レイアウトグリッド不統一",
            "ボタンスタイル不統一",
            "アニメーション・トランジション不統一"
        ],
        "target_users": [
            "研究者・学術関係者",
            "AI・機械学習エンジニア",
            "卒業研究評価者"
        ]
    }
    return site_analysis

def create_design_consultation_prompt():
    """Gemini相談用のプロンプトを作成"""
    site_analysis = analyze_current_site_structure()
    
    consultation_prompt = f"""
# Vercelサイト統一デザイン相談

## 🎯 相談目的
WordNet階層構造画像分類研究のVercelサイトが、各ページでデザインがバラバラになっています。
統一感があり、プロフェッショナルで使いやすいサイトにするための統一デザインシステムを提案してください。

## 📊 現在のサイト構造分析
{json.dumps(site_analysis, ensure_ascii=False, indent=2)}

## 🎨 求める統一デザイン要素

### 1. カラーパレット統一
- メインカラー: #667eea (現在のグラデーション基調)
- サブカラー: #764ba2 
- アクセントカラー提案
- テキストカラー階層

### 2. タイポグラフィ統一
- 見出しフォント階層 (H1-H6)
- 本文フォントサイズ
- 行間・文字間隔

### 3. レイアウトシステム
- 共通ナビゲーションバー
- グリッドシステム
- カードコンポーネント
- ボタンスタイル

### 4. インタラクション統一
- ホバーエフェクト
- トランジション
- アニメーション

## 🔍 特別考慮事項
- Chart.js グラフとの調和
- 学術的・プロフェッショナルな印象
- レスポンシブ対応
- アクセシビリティ準拠

## 📋 期待する回答
1. **統一カラーパレット** (具体的なHEX値)
2. **CSS変数システム** (実装可能な形)
3. **コンポーネント設計** (再利用可能な要素)
4. **ナビゲーション統一案**
5. **実装優先順位**

統一感があり、使いやすく、研究内容を効果的に伝えるデザインシステムを提案してください。
"""
    return consultation_prompt

def consult_gemini_for_design():
    """Geminiにデザイン統一について相談"""
    try:
        model = setup_gemini()
        prompt = create_design_consultation_prompt()
        
        print("🤖 Geminiに相談中...")
        response = model.generate_content(prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 相談結果を保存
        consultation_result = {
            "timestamp": timestamp,
            "consultation_type": "design_unification",
            "prompt": prompt,
            "gemini_response": response.text,
            "status": "success"
        }
        
        # JSONファイルに保存
        output_file = f"design_consultation_result_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(consultation_result, f, ensure_ascii=False, indent=2)
        
        # マークダウンファイルにも保存
        md_file = f"design_consultation_summary_{timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🎨 Vercelサイト統一デザイン相談結果\n\n")
            f.write(f"**相談日時**: {timestamp}\n\n")
            f.write(f"## 🤖 Geminiからの提案\n\n")
            f.write(response.text)
        
        print(f"✅ 相談完了: {output_file}")
        print(f"📄 要約保存: {md_file}")
        
        return consultation_result
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def main():
    """メイン実行関数"""
    print("🎨 Vercelサイト統一デザイン相談システム開始")
    print("=" * 50)
    
    # サイト分析
    analysis = analyze_current_site_structure()
    print(f"📊 分析対象ページ: {len(analysis['main_pages'])}ページ")
    print(f"🔍 検出された問題: {len(analysis['design_issues'])}項目")
    
    # Gemini相談実行
    result = consult_gemini_for_design()
    
    if result:
        print("\n🎉 Gemini相談が完了しました！")
        print("次のステップ:")
        print("1. 生成されたマークダウンファイルを確認")
        print("2. 提案された統一デザインシステムを実装")
        print("3. 各ページに順次適用")
    else:
        print("\n❌ 相談に失敗しました。")

if __name__ == "__main__":
    main()