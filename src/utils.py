import json
import boto3
import os
import time
from cryptography.fernet import Fernet
from supabase import create_client, Client
import stripe

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
queue_url = os.environ.get('SQS_QUEUE_URL')

def encrypt_data(data):
    try:
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted = f.encrypt(json.dumps(data).encode())
        return encrypted, key
    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")

def decrypt_data(encrypted, key):
    try:
        f = Fernet(key)
        decrypted = f.decrypt(encrypted).decode()
        return json.loads(decrypted)
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def log_audit(user_id, action, result):
    try:
        table = dynamodb.Table('AuditLog')
        table.put_item(Item={
            'user_id': user_id,
            'action': action,
            'result': json.dumps(result),
            'timestamp': int(time.time())
        })
    except Exception as e:
        print(f"Audit log failed: {str(e)}")

def send_message(message, target_agent, user_id):
    try:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'target_agent': target_agent,
                'message': message,
                'user_id': user_id
            })
        )
    except Exception as e:
        raise RuntimeError(f"Failed to send message: {str(e)}")

def receive_messages():
    try:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        return response.get('Messages', [])
    except Exception as e:
        print(f"Failed to receive messages: {str(e)}")
        return []

def parse_task(request, user_id):
    if not request.strip():
        return {'error': 'Empty request'}
    return {'agent': 'Financial_Agent', 'params': {'task': request}}

def store_shared_data(key, value, user_id):
    try:
        table = dynamodb.Table('SharedData')
        table.put_item(Item={
            'key': f'{user_id}:{key}',
            'value': json.dumps(value),
            'user_id': user_id
        })
    except Exception as e:
        raise RuntimeError(f"Failed to store shared data: {str(e)}")

def get_shared_data(key, user_id):
    try:
        table = dynamodb.Table('SharedData')
        response = table.get_item(Key={'key': f'{user_id}:{key}'})
        return json.loads(response['Item']['value']) if 'Item' in response else None
    except Exception as e:
        print(f"Failed to get shared data: {str(e)}")
        return None

def handle_stripe_error(e):
    return {
        'status': 'error',
        'error': str(e),
        'code': getattr(e, 'code', None)
    }