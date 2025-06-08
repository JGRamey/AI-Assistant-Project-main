from utils import log_audit
import sqlite3

def handle_time_request(data, user_id):
    try:
        conn = sqlite3.connect('/tmp/time.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS time (user_id TEXT, task TEXT, duration INTEGER)')
        if data.get('task') == 'log_time':
            c.execute('INSERT INTO time VALUES (?, ?, ?)',
                      (user_id, data.get('task_name'), data.get('duration')))
            conn.commit()
            return {'status': 'time_logged'}
        conn.close()
        log_audit(user_id, 'time_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'time_task', {'error': str(e)})
        return {'error': str(e)}