from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Research Project</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Research Project Management System</h1>
    <p>Status: Working with BaseHTTPRequestHandler</p>
    <p>Vercel Project: prj_gm8o7yYpKf4fEf1ydU5oQwZGH5dV</p>
    <p>Fixed with Claude Code</p>
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))
        return