def handler(request):
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
        <div class="status">Status: Active</div>
        <div class="card">
            <h3>Project Overview</h3>
            <p>WordNet-based semantic category analysis for image classification</p>
        </div>
        <div class="card">
            <h3>Features</h3>
            <ul>
                <li>Hourly work organization</li>
                <li>Git monitoring</li>
                <li>Security management</li>
            </ul>
        </div>
    </div>
</body>
</html>'''
    }