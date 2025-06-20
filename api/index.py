from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Research Project Management System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        .status { background: #4CAF50; color: white; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }
        .card { background: #f9f9f9; padding: 20px; margin: 10px 0; border-left: 4px solid #4CAF50; }
        .btn { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Research Project Management System</h1>
        
        <div class="status">
            Vercel Serverless - Status: Active
        </div>
        
        <div class="card">
            <h3>Project Overview</h3>
            <p>WordNet-based semantic category analysis for specialized image classification performance evaluation</p>
            <p><strong>Development Method:</strong> Claude Code AI-assisted development</p>
            <p><strong>Tech Stack:</strong> Python, Vercel Serverless</p>
        </div>
        
        <div class="card">
            <h3>Automation Features</h3>
            <ul>
                <li>Hourly work organization system</li>
                <li>Git activity monitoring</li>
                <li>Session management</li>
                <li>Security management</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>Security Status</h3>
            <p>All API keys and Project IDs are securely managed and will never be exposed externally</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="https://github.com/TK561/study" class="btn">GitHub Repository</a>
            <a href="/api/status" class="btn">System Status</a>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>AI-assisted development with Claude Code</p>
        </div>
    </div>
</body>
</html>'''
        
        self.wfile.write(html.encode('utf-8'))