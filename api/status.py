from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def status():
    try:
        return jsonify({
            "status": "running",
            "project": "Research Project Management System",
            "vercel_deployment": True,
            "features": {
                "hourly_summary": True,
                "git_tracking": True,
                "security_management": True
            },
            "system": {
                "uptime": "operational",
                "platform": "Vercel Serverless"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()