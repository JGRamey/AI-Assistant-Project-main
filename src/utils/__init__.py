"""
Utility functions and helpers for the AI Assistant Project.

This module provides various utility functions including logging, data storage,
and configuration management.
"""

# Re-export commonly used functions
from .aws_clients import dynamodb, sqs, store_shared_data, get_shared_data, send_message
from .config_manager import get_config
from .database import supabase_client, log_audit
from .encryption import encrypt_data, decrypt_data
from .logging_config import logger

__all__ = [
    'dynamodb',
    'sqs',
    'store_shared_data',
    'get_shared_data',
    'send_message',
    'get_config',
    'supabase_client',
    'log_audit',
    'encrypt_data',
    'decrypt_data',
    'logger',
]
