from utils import log_audit
import sqlite3


def handle_snippet_request(data, user_id):
    """Handles snippet-related tasks."""
    task = data.get('task')
    try:
        with sqlite3.connect('/tmp/snippets.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS snippets
                         (user_id TEXT, name TEXT, code TEXT)''')
            if task == 'save_snippet':
                c.execute('INSERT INTO snippets VALUES (?, ?, ?)',
                          (user_id, data.get('name'), data.get('code')))
                conn.commit()
                log_audit(user_id, 'snippet_task', {'task': task})
                return {'status': 'snippet_saved'}

        log_audit(user_id, 'snippet_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'snippet_task', {'error': str(e)})
        return {'error': str(e)}