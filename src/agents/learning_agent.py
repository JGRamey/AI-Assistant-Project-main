from utils import log_audit
import sqlite3


def handle_learning_request(data, user_id):
    """Handles learning-related tasks."""
    task = data.get('task')
    try:
        with sqlite3.connect('/tmp/preferences.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS preferences
                         (user_id TEXT, preference TEXT, weight REAL)''')
            if task == 'learn':
                c.execute('INSERT INTO preferences VALUES (?, ?, ?)',
                          (user_id, data.get('preference'),
                           data.get('weight', 1.0)))
                conn.commit()
                log_audit(user_id, 'learning_task', {'task': task})
                return {'status': 'learned'}

        log_audit(user_id, 'learning_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'learning_task', {'error': str(e)})
        return {'error': str(e)}