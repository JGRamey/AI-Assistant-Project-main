from utils import log_audit


def handle_stress_request(data, user_id):
    """Handles stress-related tasks."""
    task = data.get('task')
    try:
        if task == 'prompt':
            # Use Grok API for stress-relief prompts
            log_audit(user_id, 'stress_task', {'task': task})
            return {'prompt': 'Take a deep breath and visualize a calm beach.'}

        log_audit(user_id, 'stress_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'stress_task', {'error': str(e)})
        return {'error': str(e)}