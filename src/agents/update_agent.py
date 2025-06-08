from utils import log_audit, encrypt_data
import sqlite3
import requests
import time

def handle_update_request(data, user_id):
    try:
        conn = sqlite3.connect('/tmp/update_notes.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS updates (user_id TEXT, update_id TEXT, notes TEXT, timestamp INTEGER)')
        
        if data.get('task') == 'log_update':
            update_id = f"update_{int(time.time())}"
            # Use Grok API to summarize changes
            response = requests.post(
                'https://api.x.ai/grok/summarize',
                json={'text': data.get('changes')}
            )
            notes = response.json().get('summary', data.get('changes'))
            encrypted_notes = encrypt_data(notes)
            c.execute('INSERT INTO updates VALUES (?, ?, ?, ?)',
                      (user_id, update_id, encrypted_notes, int(time.time())))
            conn.commit()
            return {'status': 'update_logged', 'update_id': update_id}
        elif data.get('task') == 'view_updates':
            c.execute('SELECT update_id, notes, timestamp FROM updates WHERE user_id = ?', (user_id,))
            updates = [{'id': r[0], 'notes': decrypt_data(r[1]), 'timestamp': r[2]} for r in c.fetchall()]
            return {'updates': updates}
        conn.close()
        log_audit(user_id, 'update_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'update_task', {'error': str(e)})
        return {'error': str(e)}