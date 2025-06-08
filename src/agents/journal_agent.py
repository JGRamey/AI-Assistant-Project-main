import time
from utils import log_audit, encrypt_data
import boto3
import requests
import sqlite3

def handle_journal_request(data, user_id):
    try:
        s3 = boto3.client('s3')
        conn = sqlite3.connect('/tmp/journal.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS journal (user_id TEXT, entry_id TEXT, content TEXT, timestamp INTEGER)')
        
        if data.get('task') == 'add_entry':
            entry_id = f"entry_{int(time.time())}"
            content = data.get('content')
            encrypted_content = encrypt_data(content)
            c.execute('INSERT INTO journal VALUES (?, ?, ?, ?)',
                      (user_id, entry_id, encrypted_content, int(time.time())))
            conn.commit()
            # Store audio if provided
            if data.get('audio'):
                s3.put_object(
                    Bucket='my-ai-journal',
                    Key=f"{user_id}/{entry_id}.wav",
                    Body=bytes.fromhex(data.get('audio'))
                )
            return {'status': 'entry_added', 'entry_id': entry_id}
        elif data.get('task') == 'voice_to_text':
            response = requests.post(
                'http://mimic3:59125/api/stt',
                data=bytes.fromhex(data.get('audio'))
            )
            text = response.json().get('text')
            return {'text': text}
        conn.close()
        log_audit(user_id, 'journal_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'journal_task', {'error': str(e)})
        return {'error': str(e)}