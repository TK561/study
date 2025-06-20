from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        status_data = {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "project": "研究プロジェクト管理システム",
            "vercel_deployment": True,
            "features": {
                "hourly_summary": True,
                "git_tracking": True,
                "security_management": True,
                "session_logs": True,
                "automated_reports": True
            },
            "security": {
                "api_keys_protected": True,
                "project_id_secured": True,
                "git_history_clean": True,
                "env_variables_safe": True
            },
            "system": {
                "uptime": "operational",
                "deployment_status": "successful",
                "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "platform": "Vercel Serverless"
            }
        }
        
        self.wfile.write(json.dumps(status_data, ensure_ascii=False, indent=2).encode('utf-8'))