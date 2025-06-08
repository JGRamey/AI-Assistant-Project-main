import logging
import json
import os
from cryptography.fernet import Fernet

# Configure logging
LOG_FILE = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Storage path for shared data
STORAGE_PATH = "shared_data.json"

# Encryption key (for testing, generate a static key; in production, store securely)
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

def log_audit(user, event_type, data):
    """
    Log an audit event to file and console.
    
    Args:
        user (str): User identifier
        event_type (str): Type of event
        data (dict): Event data
    """
    log_message = f"User: {user}, Event: {event_type}, Data: {data}"
    logging.info(log_message)

def store_shared_data(key, data):
    """
    Store data in a local JSON file.
    
    Args:
        key (str): Data identifier
        data (dict): Data to store
    """
    try:
        shared_data = {}
        if os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, 'r') as f:
                shared_data = json.load(f)
        shared_data[key] = data
        with open(STORAGE_PATH, 'w') as f:
            json.dump(shared_data, f, indent=2)
        logging.info(f"Stored data with key: {key}")
    except Exception as e:
        logging.error(f"Failed to store data: {str(e)}")

def get_shared_data(key):
    """
    Retrieve data from local JSON file.
    
    Args:
        key (str): Data identifier
    
    Returns:
        dict: Stored data or None if not found
    """
    try:
        if os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, 'r') as f:
                shared_data = json.load(f)
                return shared_data.get(key)
        return None
    except Exception as e:
        logging.error(f"Failed to retrieve data: {str(e)}")
        return None

def encrypt_data(data):
    """
    Encrypt data using Fernet.
    
    Args:
        data (dict): Data to encrypt
    
    Returns:
        bytes: Encrypted data
    """
    return cipher.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted_data):
    """
    Decrypt data using Fernet.
    
    Args:
        encrypted_data (bytes): Encrypted data
    
    Returns:
        dict: Decrypted data
    """
    return json.loads(cipher.decrypt(encrypted_data).decode())

def send_message(queue_url, message_body):
    """
    Mock sending a message to a queue (for non-AWS testing).
    
    Args:
        queue_url (str): Queue URL
        message_body (dict): Message body
    """
    log_audit("system", "send_message", {"queue_url": queue_url, "message_body": message_body})
    return {"MessageId": "mock_message_id"}

def receive_messages(queue_url):
    """
    Mock receiving messages from a queue (for non-AWS testing).
    
    Args:
        queue_url (str): Queue URL
    
    Returns:
        list: Mock messages
    """
    log_audit("system", "receive_messages", {"queue_url": queue_url})
    return [{"Body": json.dumps({"mock": "message"})}]

def parse_task(request, user_id):
    """
    Parse a task request into agent or workflow.
    
    Args:
        request (str): Task request
        user_id (str): User ID
    
    Returns:
        dict: Task plan
    """
    # Simplified mock parsing for testing
    if "code" in request.lower():
        return {"agent": "coding_agent", "params": {"task": "generate_python", "spec": request}}
    return {"workflow": "default", "params": {"request": request}}