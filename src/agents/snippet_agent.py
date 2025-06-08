from utils import log_audit
import sqlite3

def handle_snippet_request(data, user_id):
    try:
        conn = sqlite3.connect('/tmp/snippets.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS snippets (user_id TEXT, name TEXT, code TEXT)')
        if data.get('task') == 'save_snippet':
            c.execute('INSERT INTO snippets VALUES (?, ?, ?)',
                      (user_id, data.get('name'), data.get('code')))
            conn.commit()
            return {'status': 'snippet_saved'}
        conn.close()
        log_audit(user_id, 'snippet_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'snippet_task', {'error': str(e)})
        return {'error': str(e)}