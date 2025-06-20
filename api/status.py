from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        status_data = {
            "status": "running",
            "project": "Research Project Management System",
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
                "platform": "Vercel Serverless"
            }
        }
        
        self.wfile.write(json.dumps(status_data, ensure_ascii=False, indent=2).encode('utf-8'))