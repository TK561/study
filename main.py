from datetime import datetime

def handler(request):
    """Vercel serverless function handler"""
    if request.path == '/api/status':
        return {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "project": "研究プロジェクト管理システム",
            "features": {
                "hourly_summary": True,
                "git_tracking": True,
                "security": True,
                "session_logs": True
            }
        }
    
    # Default route - return HTML
    return get_html_response()

def get_html_response():
    """Generate HTML response"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究プロジェクト管理システム</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        
        .status-badge {
            display: inline-block;
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.9em;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        
        .card h2 {
            color: #2c3e50;
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
        }
        
        .feature-list li {
            padding: 12px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .feature-list li:last-child {
            border-bottom: none;
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            background: #28a745;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .info-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .info-item strong {
            color: #2c3e50;
            display: block;
            margin-bottom: 5px;
        }
        
        .links {
            margin-top: 30px;
            text-align: center;
        }
        
        .btn {
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            margin: 0 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .security-note {
            background: linear-gradient(45deg, #ffc107, #ff8c00);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 30px 0;
            text-align: center;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header {
                padding: 25px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>研究プロジェクト管理システム</h1>
            <p class="subtitle">WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価研究</p>
            <span class="status-badge">Vercel上で稼働中</span>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2><span class="icon">📊</span>プロジェクト概要</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>開発手法</strong>
                        Claude Code AI支援
                    </div>
                    <div class="info-item">
                        <strong>技術スタック</strong>
                        Python, Flask, Vercel
                    </div>
                    <div class="info-item">
                        <strong>バージョン管理</strong>
                        Git, GitHub
                    </div>
                    <div class="info-item">
                        <strong>デプロイ</strong>
                        Vercel Serverless
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2><span class="icon">⚡</span>自動化システム</h2>
                <ul class="feature-list">
                    <li>
                        <span class="status-indicator"></span>
                        <strong>1時間毎作業整理</strong> - 自動追跡・整理
                    </li>
                    <li>
                        <span class="status-indicator"></span>
                        <strong>Git活動監視</strong> - リアルタイム追跡
                    </li>
                    <li>
                        <span class="status-indicator"></span>
                        <strong>セッション管理</strong> - 詳細ログ記録
                    </li>
                    <li>
                        <span class="status-indicator"></span>
                        <strong>統合レポート</strong> - Markdown形式
                    </li>
                </ul>
            </div>
            
            <div class="card">
                <h2><span class="icon">🔒</span>セキュリティ管理</h2>
                <ul class="feature-list">
                    <li>
                        <span class="status-indicator"></span>
                        <strong>API キー保護</strong> - 環境変数管理
                    </li>
                    <li>
                        <span class="status-indicator"></span>
                        <strong>Project ID保護</strong> - .env暗号化
                    </li>
                    <li>
                        <span class="status-indicator"></span>
                        <strong>Git履歴クリーン</strong> - 機密情報なし
                    </li>
                    <li>
                        <span class="status-indicator"></span>
                        <strong>セキュリティガイド</strong> - 完全文書化
                    </li>
                </ul>
            </div>
            
            <div class="card">
                <h2><span class="icon">📈</span>システム状況</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>稼働状況</strong>
                        正常運転中
                    </div>
                    <div class="info-item">
                        <strong>最終更新</strong>
{current_time[:16]}
                    </div>
                    <div class="info-item">
                        <strong>デプロイ方式</strong>
                        Vercel Serverless
                    </div>
                    <div class="info-item">
                        <strong>監視システム</strong>
                        アクティブ
                    </div>
                </div>
            </div>
        </div>
        
        <div class="security-note">
            全てのAPIキーとProject IDは安全に管理されており、外部に漏洩することはありません
        </div>
        
        <div class="links">
            <a href="https://github.com/TK561/study" class="btn" target="_blank">GitHub リポジトリ</a>
            <a href="/api/status" class="btn" target="_blank">API ステータス</a>
        </div>
        
        <div class="footer">
            <p>Claude Code を活用した研究プロジェクト管理システム</p>
            <p>自動生成: {current_time}</p>
        </div>
    </div>
</body>
</html>
""".format(current_time=current_time)
    
    return html_content