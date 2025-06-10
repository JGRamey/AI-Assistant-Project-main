from utils import log_audit
import googleapiclient.discovery


def handle_priority_request(data, user_id):
    """Handles priority-related tasks."""
    task = data.get('task')
    try:
        if task == 'prioritize':
            creds = data.get('credentials')
            service = googleapiclient.discovery.build(
                'calendar', 'v3', credentials=creds
            )
            events = service.events().list(calendarId='primary').execute()
            tasks = sorted(
                events.get('items', []),
                key=lambda x: x.get('start', {}).get('dateTime')
            )
            log_audit(user_id, 'priority_task', {'task': task})
            return {'tasks': tasks[:data.get('limit', 5)]}

        log_audit(user_id, 'priority_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'priority_task', {'error': str(e)})
        return {'error': str(e)}
