"""
Utility functions and helpers for the AI Assistant Project.

This module provides various utility functions including logging, data storage,
and configuration management.
"""

# Re-export commonly used functions
from .helpers import log_audit, store_shared_data, get_shared_data  # noqa: F401
from .log_utils import parse_task  # noqa: F401
from .config_manager import get_config  # noqa: F401

__all__ = [
    'log_audit',
    'store_shared_data',
    'get_shared_data',
    'parse_task',
    'get_config',
]
