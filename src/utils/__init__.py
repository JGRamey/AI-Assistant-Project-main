"""
Utility functions and helpers for the AI Assistant Project.

This module provides various utility functions including logging, data storage,
and configuration management.
"""

# Re-export commonly used functions
from .helpers import (
    log_audit,
    store_shared_data,
    get_shared_data,
    send_message,
    supabase,
)
from .log_utils import parse_task, encrypt_data, decrypt_data
from .config_manager import get_config

__all__ = [
    'log_audit',
    'store_shared_data',
    'get_shared_data',
    'send_message',
    'supabase',
    'parse_task',
    'encrypt_data',
    'decrypt_data',
    'get_config',
]
