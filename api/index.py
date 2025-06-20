import traceback
import sys

def handler(request):
    try:
        # Basic response
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Research Project</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        .status { background: #4CAF50; color: white; padding: 20px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Research Project Management System</h1>
        <div class="status">Status: Active - Vercel Deployment Working</div>
        <p>WordNet-based semantic analysis for image classification</p>
        <p>Development: Claude Code AI-assisted</p>
    </div>
</body>
</html>'''

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8'
            },
            'body': html_content
        }
        
    except Exception as e:
        # Detailed error logging
        error_details = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc(),
            'python_version': sys.version
        }
        
        print(f"ERROR in handler: {error_details}")
        
        # Return error page instead of crashing
        error_html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Function Error</h1>
    <p>Error: {str(e)}</p>
    <p>Type: {type(e).__name__}</p>
    <pre>{traceback.format_exc()}</pre>
</body>
</html>'''
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8'
            },
            'body': error_html
        }