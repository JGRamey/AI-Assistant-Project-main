"""
Configuration management for the AI Assistant Project.

This module provides a centralized way to manage configuration settings
and secrets across different environments (local, Lambda, etc.).
"""

import json
import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError



class ConfigManager:
    """Manages application configuration and secrets.
    
    This class handles loading configuration from files, environment variables,
    and AWS SSM Parameter Store, with appropriate fallbacks.
    """

    def __init__(self, config_path: str = 'config/config.json') -> None:
        self.config = self._load_config_from_file(config_path)
        self._load_secrets()

    def _load_config_from_file(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from a JSON file.
        
        Args:
            config_path: Relative path to the config file
            
        Returns:
            Dict containing the loaded configuration
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(base_dir))
        abs_config_path = os.path.join(project_root, config_path)

        try:
            with open(abs_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(
                f"Warning: Config file not found at {abs_config_path}. "
                "Using default values."
            )
            return {}
        except json.JSONDecodeError:
            print(
                f"Warning: Could not decode JSON from {abs_config_path}. "
                "Using default values."
            )
            return {}

    def _load_secrets(self) -> None:
        """Load secrets from the appropriate source.
        
        Tries to load from AWS SSM Parameter Store if in a Lambda environment,
        otherwise falls back to environment variables.
        """
        ssm_parameter_names = self.config.get('ssm_parameters', [])
        # AWS_LAMBDA_FUNCTION_NAME is a reserved env var in Lambda
        if ssm_parameter_names and os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
            self._load_from_ssm(ssm_parameter_names)
        else:
            self._load_from_env()

    def _load_from_ssm(self, parameter_names: List[str]) -> None:
        """Loads parameters from AWS SSM Parameter Store."""
        # Ensure region is configured, e.g., via AWS_REGION env var
        ssm = boto3.client('ssm')
        try:
            response = ssm.get_parameters(Names=parameter_names, WithDecryption=True)
            for parameter in response['Parameters']:
                # Store by the base name (e.g., /my-app/API_KEY -> API_KEY)
                key = parameter['Name'].split('/')[-1]
                self.config[key] = parameter['Value']
            print("Successfully loaded secrets from SSM Parameter Store.")
        except ClientError as e:
            print(
                f"Error loading secrets from SSM: {e}. "
                "Falling back to environment variables."
            )
            self._load_from_env()

    def _load_from_env(self) -> None:
        """Load secrets from environment variables.
        
        This is primarily used for local development when SSM is not available.
        """
        # A list of expected secret keys can be defined in config.json
        secret_keys = self.config.get('secret_keys', [])
        for key in secret_keys:
            value = os.getenv(key)
            if value:
                self.config[key] = value
        print("Loaded secrets from environment variables.")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.
        
        Args:
            key: The configuration key to retrieve
            default: Default value if key is not found
            
        Returns:
            The configuration value or the default if not found
        """
        return self.config.get(key, default)


# Singleton instance for easy access across the application
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get or create the singleton ConfigManager instance.
    
    Returns:
        The singleton ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config(key: str, default: Any = None) -> Any:
    """Convenience function to access the config manager.
    
    Args:
        key: The configuration key to retrieve
        default: Default value if key is not found
        
    Returns:
        The configuration value or the default if not found
    """
    return get_config_manager().get(key, default)
