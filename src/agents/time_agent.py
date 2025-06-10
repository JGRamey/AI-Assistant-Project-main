from utils import log_audit
import sqlite3


def handle_time_request(data, user_id):
    """Handles time-tracking related tasks."""
    task = data.get('task')
    try:
        with sqlite3.connect('/tmp/time.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS time
                         (user_id TEXT, task TEXT, duration INTEGER)''')
            if task == 'log_time':
                c.execute(
                    'INSERT INTO time VALUES (?, ?, ?)',
                    (user_id, data.get('task_name'), data.get('duration'))
                )
                conn.commit()
                log_audit(user_id, 'time_task', {'task': task})
                return {'status': 'time_logged'}

        log_audit(user_id, 'time_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'time_task', {'error': str(e)})
        return {'error': str(e)}