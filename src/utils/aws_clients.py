"""Initializes and configures AWS clients for the application."""

import boto3
import json
from datetime import datetime, timezone
from typing import Dict, Any
from src.utils.logging_config import logger
from src.config_manager import get_config
from src.config_manager import get_config

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

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
        logger.error("Failed to retrieve data for key=%s, user=%s: %s", key, user_id, str(e))
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
