from utils import log_audit
import googleapiclient.discovery

def handle_priority_request(data, user_id):
    try:
        creds = data.get('credentials')
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
        if data.get('task') == 'prioritize':
            events = service.events().list(calendarId='primary').execute()
            tasks = sorted(events.get('items', []), key=lambda x: x.get('start', {}).get('dateTime'))
            return {'tasks': tasks[:data.get('limit', 5)]}
        log_audit(user_id, 'priority_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'priority_task', {'error': str(e)})
        return {'error': str(e)}