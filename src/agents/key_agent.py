from src.utils.helpers import log_audit, encrypt_data
import boto3
import time


def handle_key_request(data, user_id):
    try:
        task = data.get('task')
        if task == 'refresh_key':
            ssm = boto3.client('ssm')
            new_key = generate_new_key()
            encrypted_key = encrypt_data(new_key)
            ssm.put_parameter(
                Name=f'/my-ai-assistant/{user_id}/api-key',
                Value=encrypted_key,
                Type='SecureString',
                Overwrite=True
            )
            log_audit(user_id, 'key_task', {'task': task})
            return {'status': 'key_refreshed', 'timestamp': int(time.time())}

        log_audit(user_id, 'key_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'key_task', {'error': str(e)})
        return {'error': str(e)}


def generate_new_key():
    # Placeholder for key generation
    return 'new-api-key-123'
