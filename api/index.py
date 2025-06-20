from http.server import BaseHTTPRequestHandler
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>研究プロジェクト管理システム</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }}
        h1 {{ color: #333; text-align: center; }}
        .status {{ background: #4CAF50; color: white; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }}
        .card {{ background: #f9f9f9; padding: 20px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
        .btn {{ display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>研究プロジェクト管理システム</h1>
        
        <div class="status">
            Vercel上で稼働中 - {current_time}
        </div>
        
        <div class="card">
            <h3>プロジェクト概要</h3>
            <p>WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価研究</p>
            <p><strong>開発手法:</strong> Claude Code AI支援開発</p>
            <p><strong>技術スタック:</strong> Python, Vercel Serverless</p>
        </div>
        
        <div class="card">
            <h3>自動化機能</h3>
            <ul>
                <li>1時間毎作業整理システム</li>
                <li>Git活動監視</li>
                <li>セッション管理</li>
                <li>セキュリティ管理</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>セキュリティ状況</h3>
            <p>全てのAPIキーとProject IDは安全に管理されており、外部に漏洩することはありません</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="https://github.com/TK561/study" class="btn">GitHub Repository</a>
            <a href="/api/status" class="btn">System Status</a>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>Claude Code による AI支援開発</p>
            <p>最終更新: {current_time}</p>
        </div>
    </div>
</body>
</html>'''
            
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            error_msg = f"Server Error: {str(e)}"
            self.wfile.write(error_msg.encode('utf-8'))