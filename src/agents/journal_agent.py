import time
import sqlite3
import boto3
import requests
from utils import log_audit, encrypt_data


def handle_journal_request(data, user_id):
    """Handles journal-related tasks."""
    task = data.get('task')
    try:
        if task == 'add_entry':
            with sqlite3.connect('/tmp/journal.db') as conn:
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS journal
                             (user_id TEXT, entry_id TEXT, content TEXT,
                              timestamp INTEGER)''')
                entry_id = f"entry_{int(time.time())}"
                content = data.get('content')
                encrypted_content = encrypt_data(content)
                c.execute('INSERT INTO journal VALUES (?, ?, ?, ?)',
                          (user_id, entry_id, encrypted_content,
                           int(time.time())))
            if data.get('audio'):
                s3 = boto3.client('s3')
                s3.put_object(
                    Bucket='my-ai-journal',
                    Key=f"{user_id}/{entry_id}.wav",
                    Body=bytes.fromhex(data.get('audio'))
                )
            log_audit(user_id, 'journal_task', {'task': task})
            return {'status': 'entry_added', 'entry_id': entry_id}

        elif task == 'voice_to_text':
            response = requests.post(
                'http://mimic3:59125/api/stt',
                data=bytes.fromhex(data.get('audio')),
                timeout=10
            )
            response.raise_for_status()
            text = response.json().get('text')
            log_audit(user_id, 'journal_task', {'task': task})
            return {'text': text}

        log_audit(user_id, 'journal_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'journal_task', {'error': str(e)})
        return {'error': str(e)}
