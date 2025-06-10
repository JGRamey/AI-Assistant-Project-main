from utils import log_audit
import boto3


def handle_notes_request(data, user_id):
    """Handles notes-related tasks."""
    task = data.get('task')
    try:
        if task == 'save_note':
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket='my-ai-notes',
                Key=f"{user_id}/{data.get('note_id')}.txt",
                Body=data.get('content')
            )
            log_audit(user_id, 'notes_task', {'task': task})
            return {'status': 'note_saved'}

        log_audit(user_id, 'notes_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'notes_task', {'error': str(e)})
        return {'error': str(e)}