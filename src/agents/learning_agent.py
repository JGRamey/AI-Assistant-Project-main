from utils import log_audit
import sqlite3

def handle_learning_request(data, user_id):
    try:
        conn = sqlite3.connect('/tmp/preferences.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS preferences (user_id TEXT, preference TEXT, weight REAL)')
        if data.get('task') == 'learn':
            c.execute('INSERT INTO preferences VALUES (?, ?, ?)',
                      (user_id, data.get('preference'), data.get('weight', 1.0)))
            conn.commit()
            return {'status': 'learned'}
        conn.close()
        log_audit(user_id, 'learning_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'learning_task', {'error': str(e)})
        return {'error': str(e)}