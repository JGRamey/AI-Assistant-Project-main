import json
import time
from utils import log_audit, store_shared_data, get_shared_data

def handle_analytics_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"youtube_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if task == 'fetch_analytics':
            analytics = {
                'views': 1000,
                'likes': 50,
                'comments': 10,
                'estimatedRevenue': 100.00
            }
            store_shared_data(f'youtube_{user_id}', {'analytics': analytics}, user_id)
            response["result"] = analytics

        elif task == 'fetch_schedule':
            response["result"] = {
                'schedule': ['Video 1: 2025-06-10', 'Video 2: 2025-06-15']
            }

        elif task == 'generate_ideas':
            keywords = data.get('keywords', '')
            if not keywords.strip():
                return {"status": "error", "result": "Keywords cannot be empty"}
            response["result"] = {
                'ideas': [f"Video about {keywords} trend", f"Tutorial on {keywords}"]
            }

        store_shared_data(f'youtube_{task_id}', response["result"], user_id)
        log_audit(user_id, f"youtube_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "youtube_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}