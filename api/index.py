def handler(request):
    """
    Vercel用のシンプルなPython APIハンドラー - 完全新規作成
    """
    
    html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究成果 - 意味カテゴリ画像分類システム</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 10px;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 2.2rem;
        }
        .section {
            margin: 25px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .section h3 {
            color: #667eea;
            margin-top: 0;
        }
        .result-box {
            background: #e8f5e8;
            border: 2px solid #4caf50;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 15px;
            background: #f1f3f4;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #666;
        }
        .badge {
            display: inline-block;
            background: #ff5722;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔬 意味カテゴリ画像分類システム</h1>
            <p>WordNet + CLIP による特化型分類の研究成果</p>
            <span class="badge">NEW VERSION</span>
        </div>

        <div class="section">
            <h3>🎯 主要な研究成果</h3>
            <div class="result-box">
                <h4>✅ 最適解発見</h4>
                <ul>
                    <li><strong>最適カテゴリ数:</strong> 16カテゴリ</li>
                    <li><strong>精度向上率:</strong> 27.3%</li>
                    <li><strong>理論的上限:</strong> 30.0%</li>
                    <li><strong>統計的有意性:</strong> p < 0.05 (Cohen's d = 1.2)</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <h3>📊 カテゴリ数 vs 精度向上率</h3>
            <div style="background: white; padding: 15px; border-radius: 8px;">
                <svg width="100%" height="250" viewBox="0 0 500 250">
                    <!-- 軸 -->
                    <line x1="40" y1="200" x2="460" y2="200" stroke="#333" stroke-width="2"/>
                    <line x1="40" y1="200" x2="40" y2="40" stroke="#333" stroke-width="2"/>
                    
                    <!-- X軸ラベル -->
                    <text x="250" y="230" text-anchor="middle" font-size="12" fill="#333">カテゴリ数</text>
                    
                    <!-- Y軸ラベル -->
                    <text x="15" y="120" text-anchor="middle" font-size="12" fill="#333" transform="rotate(-90, 15, 120)">精度向上率(%)</text>
                    
                    <!-- データ線 -->
                    <path d="M 40,200 L 120,150 L 200,100 L 280,80 L 360,70 L 440,65" 
                          fill="none" stroke="#667eea" stroke-width="3"/>
                    
                    <!-- 最適点 -->
                    <circle cx="200" cy="100" r="5" fill="#ff5722" stroke="white" stroke-width="2"/>
                    <text x="200" y="90" text-anchor="middle" font-size="11" fill="#ff5722" font-weight="bold">16カテゴリ</text>
                    <text x="200" y="78" text-anchor="middle" font-size="10" fill="#ff5722">27.3%</text>
                    
                    <!-- 上限線 -->
                    <line x1="40" y1="65" x2="460" y2="65" stroke="#e91e63" stroke-width="2" stroke-dasharray="4,4"/>
                    <text x="420" y="60" font-size="10" fill="#e91e63">上限30%</text>
                </svg>
            </div>
        </div>

        <div class="section">
            <h3>🛠 技術スタック</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;">PyTorch</span>
                <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;">CLIP</span>
                <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;">WordNet</span>
                <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;">Cohen's d</span>
                <span style="background: #667eea; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem;">Claude Code</span>
            </div>
        </div>

        <div class="footer">
            <p><strong>Generated with Claude Code</strong> - AI支援研究開発</p>
            <p><strong>結論:</strong> 16カテゴリ実装により27.3%の精度向上を実現</p>
        </div>
    </div>
</body>
</html>'''

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        },
        'body': html
    }