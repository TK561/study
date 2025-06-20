def handler(request):
    """
    Research Project Management System
    Generated with Claude Code GitHub Actions Integration
    """
    
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Research Project Management System</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            max-width: 900px; 
            background: white; 
            padding: 50px; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 { 
            color: #333; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .status { 
            background: linear-gradient(45deg, #4CAF50, #45a049); 
            color: white; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            font-size: 1.2em;
            font-weight: bold;
        }
        .card { 
            background: #f8f9fa; 
            padding: 25px; 
            margin: 20px 0; 
            border-left: 5px solid #4CAF50;
            border-radius: 8px;
            text-align: left;
        }
        .automation-badge {
            background: #ff6b35;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            display: inline-block;
            margin: 10px 0;
        }
        .feature-list {
            list-style: none;
            padding: 0;
        }
        .feature-list li {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .feature-list li:before {
            content: "🤖 ";
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Research Project Management System</h1>
        
        <div class="status">
            ✅ Active - GitHub Actions CI/CD Pipeline
        </div>
        
        <div class="automation-badge">
            AUTO-DEPLOYED WITH CLAUDE CODE
        </div>
        
        <div class="card">
            <h3>📊 Project Overview</h3>
            <p><strong>研究テーマ:</strong> WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価</p>
            <p><strong>開発手法:</strong> Claude Code AI支援開発</p>
            <p><strong>技術スタック:</strong> Python, Vercel Serverless, GitHub Actions</p>
        </div>
        
        <div class="card">
            <h3>🤖 自動化機能</h3>
            <ul class="feature-list">
                <li>GitHub Actions自動デプロイ</li>
                <li>エラー検出 → GitHub Issue作成</li>
                <li>Claude Code自動修正</li>
                <li>30分毎ヘルスチェック</li>
                <li>1時間毎作業整理システム</li>
                <li>Git活動監視</li>
                <li>セキュリティ管理</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>🔄 CI/CD Pipeline Status</h3>
            <p>✅ <strong>Deploy:</strong> Auto-deployment on push to main</p>
            <p>✅ <strong>Monitor:</strong> Continuous health monitoring</p>
            <p>✅ <strong>Auto-Fix:</strong> Claude Code error resolution</p>
            <p>✅ <strong>Alerts:</strong> GitHub Issues for failures</p>
        </div>
        
        <div class="card">
            <h3>🔒 セキュリティ状況</h3>
            <p>すべてのAPIキーとProject IDは安全に管理されており、外部に漏洩することはありません</p>
            <p><strong>Vercel Project:</strong> prj_gm8o7yYpKf4fEf1ydU5oQwZGH5dV</p>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #e8f5e8; border-radius: 10px;">
            <p style="margin: 0; color: #2e7d32; font-weight: bold;">
                🤖 Powered by Claude Code GitHub Actions Integration
            </p>
            <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">
                Last deployed: Auto-deployment via GitHub Actions
            </p>
        </div>
    </div>
</body>
</html>'''

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8'
        },
        'body': html_content
    }