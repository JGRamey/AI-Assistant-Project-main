from googleapiclient.discovery import build
import base64
from src.utils import log_audit


def handle_email_request(data, user_id):
    try:
        creds = data.get('credentials')  # Read-only scope
        service = build('gmail', 'v1', credentials=creds)
        task = data.get('task')
        if task == 'read':
            results = service.users().messages().list(userId='me').execute()
            log_audit(user_id, 'email_task', {'task': task})
            return {'emails': results.get('messages', [])}
        elif task == 'send':
            # Restricted write permission
            message = create_message(
                data.get('to'), data.get('subject'), data.get('body')
            )
            service.users().messages().send(
                userId='me', body=message
            ).execute()
            log_audit(user_id, 'email_task', {'task': task})
            return {'status': 'sent'}
        log_audit(user_id, 'email_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'email_task', {'error': str(e)})
        return {'error': str(e)}


def create_message(to, subject, body):
    message_text = f"To: {to}\nSubject: {subject}\n\n{body}".encode()
    encoded_message = base64.urlsafe_b64encode(message_text).decode()
    return {'raw': encoded_message}
