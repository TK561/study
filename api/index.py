def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8'
        },
        'body': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Research Project</title>
</head>
<body>
    <h1>Research Project Management System</h1>
    <p>Status: Active</p>
    <p>WordNet-based semantic analysis for image classification</p>
</body>
</html>
'''
    }