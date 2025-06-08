import os
import json
import boto3
import logging
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

# Initialize Supabase client
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

def log_audit(user_id: str, action: str, details: dict):
    """Log user actions to Supabase and logger."""
    try:
        if supabase:
            supabase.table('audit_logs').insert({
                'user_id': user_id,
                'action': action,
                'details': json.dumps(details),
                'timestamp': datetime.utcnow().isoformat()
            }).execute()
        logger.info(f"Audit log: user={user_id}, action={action}, details={details}")
    except Exception as e:
        logger.error(f"Failed to log audit: {str(e)}")

def store_shared_data(key: str, value: dict, user_id: str):
    """Store data in DynamoDB with user-specific key."""
    try:
        table = dynamodb.Table('SharedData')
        table.put_item(Item={
            'key': f'{user_id}:{key}',
            'value': json.dumps(value),
            'timestamp': datetime.utcnow().isoformat()
        })
        logger.info(f"Stored data: key={key}, user={user_id}")
    except Exception as e:
        logger.error(f"Failed to store data: {str(e)}")
        raise

def get_shared_data(key: str, user_id: str) -> dict:
    """Retrieve data from DynamoDB."""
    try:
        table = dynamodb.Table('SharedData')
        response = table.get_item(Key={'key': f'{user_id}:{key}'})
        if 'Item' in response:
            return json.loads(response['Item']['value'])
        return {}
    except Exception as e:
        logger.error(f"Failed to get data: {str(e)}")
        return {}

def send_message(message: dict):
    """Send message to SQS queue."""
    try:
        queue_url = os.environ.get('SQS_QUEUE_URL')
        if not queue_url:
            raise ValueError("SQS_QUEUE_URL not set")
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        logger.info(f"Sent message to SQS: {message}")
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        raise