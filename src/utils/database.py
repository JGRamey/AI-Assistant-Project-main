"""Handles database connections and operations for Supabase."""

import os
from supabase import create_client, Client
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from src.config_manager import get_config
from src.utils.logging_config import logger

def get_supabase_client() -> Optional[Client]:
    """Initializes and returns the Supabase client.

    Returns:
        A Supabase client instance if credentials are configured, otherwise None.
    """
    url = get_config('SUPABASE_URL')
    key = get_config('SUPABASE_ANON_KEY')

    if url and key:
        return create_client(url, key)
    
    logger.warning("Supabase credentials not found. Supabase client not initialized.")
    return None

supabase_client = get_supabase_client()

def log_audit(user_id: str, action: str, details: Dict[str, Any]) -> None:
    """Log user actions to Supabase and logger.
    
    Args:
        user_id: ID of the user performing the action
        action: Description of the action being performed
        details: Additional details about the action
    """
    try:
        if supabase_client:
            supabase_client.table('audit_logs').insert({
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
