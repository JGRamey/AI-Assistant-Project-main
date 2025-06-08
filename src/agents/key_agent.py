from utils import log_audit, encrypt_data
import boto3
import time

def handle_key_request(data, user_id):
    try:
        ssm = boto3.client('ssm')
        if data.get('task') == 'refresh_key':
            new_key = generate_new_key()
            encrypted_key = encrypt_data(new_key)
            ssm.put_parameter(
                Name=f'/my-ai-assistant/{user_id}/api-key',
                Value=encrypted_key,
                Type='SecureString',
                Overwrite=True
            )
            return {'status': 'key_refreshed', 'timestamp': int(time.time())}
        log_audit(user_id, 'key_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'key_task', {'error': str(e)})
        return {'error': str(e)}

def generate_new_key():
    # Placeholder for key generation
    return 'new-api-key-123'