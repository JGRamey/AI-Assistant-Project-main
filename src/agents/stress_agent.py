from utils import log_audit

def handle_stress_request(data, user_id):
    try:
        if data.get('task') == 'prompt':
            # Use Grok API for stress-relief prompts
            return {'prompt': 'Take a deep breath and visualize a calm beach.'}
        log_audit(user_id, 'stress_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'stress_task', {'error': str(e)})
        return {'error': str(e)}