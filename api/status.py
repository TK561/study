import json
import traceback
import sys

def handler(request):
    try:
        status_data = {
            "status": "running",
            "project": "Research Project Management System", 
            "platform": "Vercel Serverless",
            "timestamp": "2025-06-20",
            "features": {
                "hourly_summary": True,
                "git_tracking": True,
                "security_management": True
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(status_data, indent=2)
        }
        
    except Exception as e:
        # Log the error details
        error_info = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc(),
            'python_version': sys.version
        }
        
        print(f"ERROR in status handler: {error_info}")
        
        # Return error as JSON
        error_response = {
            "error": str(e),
            "type": type(e).__name__,
            "status": "error"
        }
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(error_response, indent=2)
        }