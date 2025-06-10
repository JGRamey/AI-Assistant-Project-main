"""Logging and utility functions for the AI Assistant Project.

This module provides logging, data storage, and encryption utilities
that are used throughout the application.
"""

import json
import logging
import os
from typing import Any, Dict, Optional

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


def log_audit(user: str, event_type: str, data: Dict[str, Any]) -> None:
    """Log an audit event to file and console.
    
    Args:
        user: User identifier
        event_type: Type of event
        data: Event data to be logged
    """
    log_message = f"User: {user}, Event: {event_type}, Data: {data}"
    logging.info(log_message)


def store_shared_data(key: str, data: Dict[str, Any]) -> None:
    """Store data in a local JSON file.
    
    Args:
        key: Data identifier
        data: Data to store (must be JSON-serializable)
    """
    try:
        shared_data = {}
        if os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
                shared_data = json.load(f)
        shared_data[key] = data
        with open(STORAGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(shared_data, f, indent=2)
        logging.info("Stored data with key: %s", key)
    except Exception as e:
        logging.error("Failed to store data: %s", str(e))


def get_shared_data(key: str) -> Optional[Dict[str, Any]]:
    """Retrieve data from local JSON file.
    
    Args:
        key: Data identifier
    
    Returns:
        Stored data or None if not found
    """
    try:
        if os.path.exists(STORAGE_PATH):
            with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
                shared_data = json.load(f)
                return shared_data.get(key)
        return None
    except Exception as e:
        logging.error("Failed to retrieve data: %s", str(e))
        return None


def encrypt_data(data: Dict[str, Any]) -> bytes:
    """Encrypt data using Fernet.
    
    Args:
        data: Data to encrypt (must be JSON-serializable)
    
    Returns:
        Encrypted data as bytes
    """
    return cipher.encrypt(json.dumps(data).encode())


def decrypt_data(encrypted_data: bytes) -> Dict[str, Any]:
    """Decrypt data using Fernet.
    
    Args:
        encrypted_data: Encrypted data as bytes
    
    Returns:
        Decrypted data as a dictionary
    """
    return json.loads(cipher.decrypt(encrypted_data).decode())


def send_message(queue_url: str, message_body: Dict[str, Any]) -> Dict[str, str]:
    """Mock sending a message to a queue (for non-AWS testing).
    
    Args:
        queue_url: Queue URL
        message_body: Message body to send (must be JSON-serializable)
    
    Returns:
        Dictionary containing a mock message ID
    """
    log_audit(
        "system",
        "send_message",
        {"queue_url": queue_url, "message_body": message_body}
    )
    return {"MessageId": "mock_message_id"}


def receive_messages(queue_url: str) -> list:
    """Mock receiving messages from a queue (for non-AWS testing).
    
    Args:
        queue_url: Queue URL to receive messages from
    
    Returns:
        List of mock messages
    """
    log_audit("system", "receive_messages", {"queue_url": queue_url})
    return [{"Body": json.dumps({"mock": "message"})}]


def parse_task(request: str, user_id: str) -> Dict[str, Any]:
    """Parse a task request into agent or workflow.
    
    Args:
        request: Task request string
        user_id: User ID making the request
    
    Returns:
        Dictionary containing task plan with agent/workflow and parameters
    """
    if "code" in request.lower():
        return {
            "agent": "coding_agent",
            "params": {"task": "generate_python", "spec": request}
        }
    return {"workflow": "default", "params": {"request": request}}


if __name__ == "__main__":
    pass