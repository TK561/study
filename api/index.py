def handler(request):
    """
    Simple and reliable Vercel handler
    Generated with Claude Code Auto-Fix System
    """
    try:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8'
            },
            'body': '''<!DOCTYPE html>
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
        <div class="status">Status: Active - Auto-Fixed by Claude Code</div>
        <div class="card">
            <h3>Project Overview</h3>
            <p>WordNet-based semantic category analysis for image classification</p>
            <p><strong>Development:</strong> Claude Code AI-assisted with GitHub Actions</p>
        </div>
        <div class="card">
            <h3>Auto-Fix Applied</h3>
            <ul>
                <li>Simplified HTML structure</li>
                <li>Removed complex CSS that may cause issues</li>
                <li>Added proper error handling</li>
                <li>Minimal dependencies</li>
            </ul>
        </div>
        <div class="card">
            <h3>CI/CD Features</h3>
            <ul>
                <li>GitHub Actions auto-deployment</li>
                <li>Error detection and Issue creation</li>
                <li>Claude Code auto-fix system</li>
                <li>Continuous monitoring</li>
            </ul>
        </div>
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>Fixed by Claude Code Auto-Fix System</p>
            <p>Vercel Project: prj_gm8o7yYpKf4fEf1ydU5oQwZGH5dV</p>
        </div>
    </div>
</body>
</html>'''
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': f'Error: {str(e)}'
        }