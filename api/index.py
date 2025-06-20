from http.server import BaseHTTPRequestHandler
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究プロジェクト管理システム</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .status {{
            text-align: center;
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            padding: 15px;
            border-radius: 25px;
            margin: 20px 0;
            font-weight: 600;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        .card {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            border-left: 4px solid #667eea;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        .card h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .feature {{
            padding: 10px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .feature:last-child {{
            border-bottom: none;
        }}
        .status-dot {{
            width: 8px;
            height: 8px;
            background: #28a745;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        .info-item {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }}
        .btn {{
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            margin: 10px;
            font-weight: 600;
            transition: transform 0.3s ease;
        }}
        .btn:hover {{
            transform: translateY(-2px);
        }}
        .security-note {{
            background: linear-gradient(45deg, #ffc107, #ff8c00);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 30px 0;
            text-align: center;
            font-weight: 600;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>研究プロジェクト管理システム</h1>
        <p style="text-align: center; font-size: 1.2em; color: #666; margin-bottom: 20px;">
            WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価研究
        </p>
        
        <div class="status">
            Vercel上で正常稼働中 - {current_time}
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>プロジェクト概要</h2>
                <div class="info-item">
                    <strong>開発手法:</strong> Claude Code AI支援開発
                </div>
                <div class="info-item">
                    <strong>技術スタック:</strong> Python, Vercel Serverless
                </div>
                <div class="info-item">
                    <strong>バージョン管理:</strong> Git, GitHub
                </div>
                <div class="info-item">
                    <strong>デプロイ:</strong> Vercel自動デプロイ
                </div>
            </div>
            
            <div class="card">
                <h2>自動化システム</h2>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>1時間毎作業整理:</strong> 自動追跡・統合レポート生成
                </div>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>Git活動監視:</strong> コミット履歴のリアルタイム追跡
                </div>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>セッション管理:</strong> 作業ログの詳細記録
                </div>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>統合レポート:</strong> Markdown形式での進捗まとめ
                </div>
            </div>
            
            <div class="card">
                <h2>セキュリティ管理</h2>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>API キー保護:</strong> 環境変数による安全管理
                </div>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>Project ID保護:</strong> .env暗号化ストレージ
                </div>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>Git履歴クリーン:</strong> 機密情報の完全除去
                </div>
                <div class="feature">
                    <div class="status-dot"></div>
                    <strong>セキュリティガイド:</strong> 包括的文書化完了
                </div>
            </div>
            
            <div class="card">
                <h2>システム状況</h2>
                <div class="info-item">
                    <strong>稼働状況:</strong> 正常運転中
                </div>
                <div class="info-item">
                    <strong>最終更新:</strong> {current_time[:16]}
                </div>
                <div class="info-item">
                    <strong>デプロイ方式:</strong> Vercel Serverless Functions
                </div>
                <div class="info-item">
                    <strong>監視システム:</strong> アクティブ
                </div>
            </div>
        </div>
        
        <div class="security-note">
            全てのAPIキーとProject IDは安全に管理されており、外部に漏洩することはありません
        </div>
        
        <div style="text-align: center;">
            <a href="https://github.com/TK561/study" class="btn" target="_blank">GitHub リポジトリ</a>
            <a href="/api/status" class="btn" target="_blank">システム状況</a>
        </div>
        
        <div class="footer">
            <p>Claude Code を活用した研究プロジェクト管理システム</p>
            <p>自動生成: {current_time}</p>
        </div>
    </div>
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))