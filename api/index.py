from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return '''<!DOCTYPE html>
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Research Project Management System</h1>
        <div class="status">Status: Active - Vercel Deployment</div>
        <div class="card">
            <h3>Project Overview</h3>
            <p>WordNet-based semantic category analysis for image classification</p>
            <p><strong>Development:</strong> Claude Code AI-assisted</p>
        </div>
        <div class="card">
            <h3>Features</h3>
            <ul>
                <li>Hourly work organization system</li>
                <li>Git activity monitoring</li>
                <li>Security management</li>
                <li>Session logs</li>
            </ul>
        </div>
        <div class="card">
            <h3>Security</h3>
            <p>All API keys and project IDs are securely managed</p>
        </div>
    </div>
</body>
</html>'''
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run()