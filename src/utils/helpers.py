"""Helper functions for common operations across the application.

This module provides utility functions for logging, data storage, and
messaging that are used throughout the AI Assistant Project.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3
from supabase import create_client, Client

from config_manager import get_config

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

# Initialize Supabase client
supabase_url = get_config('endpoints', {}).get('supabase')
supabase_key = get_config('SUPABASE_ANON_KEY')
supabase: Optional[Client] = None
if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)

def log_audit(user_id: str, action: str, details: Dict[str, Any]) -> None:
    """Log user actions to Supabase and logger.
    
    Args:
        user_id: ID of the user performing the action
        action: Description of the action being performed
        details: Additional details about the action
    """
    try:
        if supabase:
            supabase.table('audit_logs').insert({
                'user_id': user_id,
                'action': action,
                'details': json.dumps(details),
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }).execute()
        logger.info(
            "Audit log: user=%s, action=%s, details=%s",
            user_id, action, details
        )
    except Exception as e:
        logger.error("Failed to log audit: %s", str(e))


def store_shared_data(key: str, value: Dict[str, Any], user_id: str) -> None:
    """Store data in DynamoDB with user-specific key.
    
    Args:
        key: The key under which to store the data
        value: The data to store (must be JSON-serializable)
        user_id: ID of the user the data belongs to
        
    Raises:
        Exception: If there's an error storing the data
    """
    try:
        table = dynamodb.Table('SharedData')
        table.put_item(Item={
            'key': f'{user_id}:{key}',
            'value': json.dumps(value),
            'timestamp': datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Stored data: key=%s, user=%s", key, user_id)
    except Exception as e:
        logger.error("Failed to store data: %s", str(e))
        raise


def get_shared_data(key: str, user_id: str) -> Dict[str, Any]:
    """Retrieve data from DynamoDB.
    
    Args:
        key: The key of the data to retrieve
        user_id: ID of the user the data belongs to
        
    Returns:
        The retrieved data or an empty dict if not found
    """
    try:
        table = dynamodb.Table('SharedData')
        response = table.get_item(Key={'key': f'{user_id}:{key}'})
        if 'Item' in response:
            return json.loads(response['Item']['value'])
        return {}
    except Exception as e:
        logger.error("Failed to get data: %s", str(e))
        return {}


def send_message(message: Dict[str, Any]) -> None:
    """Send message to SQS queue.
    
    Args:
        message: The message to send (must be JSON-serializable)
        
    Raises:
        ValueError: If SQS queue URL is not configured
        Exception: If there's an error sending the message
    """
    try:
        queue_url = get_config('endpoints', {}).get('sqs_queue')
        if not queue_url:
            raise ValueError("SQS queue URL not set in config")
            
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        logger.info("Sent message to SQS: %s", message)
    except Exception as e:
        logger.error("Failed to send message: %s", str(e))
        raise