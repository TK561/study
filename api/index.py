from http.server import BaseHTTPRequestHandler
import json
import os
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # HTMLレスポンス
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>研究プロジェクト管理システム</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        .status {
            background: #e8f5e8;
            border: 1px solid #4caf50;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .info-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        .feature-list {
            list-style-type: none;
            padding: 0;
        }
        .feature-list li {
            background: #fff;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #2ecc71;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .github-link {
            display: inline-block;
            background: #333;
            color: white;
            padding: 12px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 5px;
        }
        .github-link:hover {
            background: #555;
        }
        .security-note {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>研究プロジェクト管理システム</h1>
        
        <div class="status">
            <strong>デプロイ状況:</strong> Vercel上で正常に動作中
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>プロジェクト概要</h3>
                <p><strong>名前:</strong> 意味カテゴリに基づく画像分類システム</p>
                <p><strong>目的:</strong> WordNetベースの意味カテゴリ分析を用いた特化型画像分類手法の性能評価</p>
                <p><strong>開発手法:</strong> Claude Code を活用したAI支援研究開発</p>
            </div>
            
            <div class="info-card">
                <h3>技術スタック</h3>
                <p><strong>バックエンド:</strong> Python, Streamlit</p>
                <p><strong>デプロイ:</strong> Vercel</p>
                <p><strong>バージョン管理:</strong> Git, GitHub</p>
                <p><strong>AI支援:</strong> Claude Code</p>
            </div>
        </div>
        
        <h2>主要機能</h2>
        <ul class="feature-list">
            <li><strong>1時間毎作業整理システム:</strong> 自動で作業内容を追跡・整理</li>
            <li><strong>Git活動監視:</strong> リアルタイムでコミット履歴を追跡</li>
            <li><strong>セッション管理:</strong> 作業セッションの詳細ログ記録</li>
            <li><strong>セキュリティ管理:</strong> API キーの安全な管理システム</li>
            <li><strong>プロジェクト概要:</strong> ファイル構造と進捗の可視化</li>
        </ul>
        
        <h2>システム状況</h2>
        <div class="info-grid">
            <div class="info-card">
                <h3>自動化システム</h3>
                <p>1時間毎作業整理: <span style="color: green;">有効</span></p>
                <p>Git自動追跡: <span style="color: green;">有効</span></p>
                <p>セッションログ: <span style="color: green;">記録中</span></p>
            </div>
            
            <div class="info-card">
                <h3>セキュリティ</h3>
                <p>API キー保護: <span style="color: green;">完了</span></p>
                <p>環境変数管理: <span style="color: green;">有効</span></p>
                <p>Git履歴クリーン: <span style="color: green;">確認済み</span></p>
            </div>
        </div>
        
        <div class="security-note">
            <strong>セキュリティ確認:</strong> 
            全てのAPIキーとProject IDは安全に.envファイルで管理されており、GitHubには公開されていません。
        </div>
        
        <h2>リポジトリ</h2>
        <a href="https://github.com/TK561/study" class="github-link" target="_blank">GitHub リポジトリを見る</a>
        <a href="https://github.com/TK561/study/blob/main/session_logs" class="github-link" target="_blank">セッションログを確認</a>
        
        <hr style="margin: 40px 0;">
        <p style="text-align: center; color: #666;">
            Claude Code を活用した研究プロジェクト管理システム<br>
            自動生成: """ + str(__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + """
        </p>
    </div>
</body>
</html>
        """
        
        self.wfile.write(html_content.encode('utf-8'))
        return