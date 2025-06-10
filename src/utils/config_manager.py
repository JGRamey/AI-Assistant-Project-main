"""
Configuration management for the AI Assistant Project.

This module provides a centralized way to manage configuration settings
and secrets across different environments (local, Lambda, etc.).
"""

import json
import logging
import os
from typing import Any, Dict, List

import boto3
from botocore.exceptions import ClientError


class ConfigManager:
    """Manages application configuration and secrets.

    This class handles loading configuration from files, environment variables,
    and AWS SSM Parameter Store, with appropriate fallbacks.
    """

    def __init__(self, config_path: str = 'config/config.json') -> None:
        """Initialize the ConfigManager with optional custom config path.

        Args:
            config_path: Path to the configuration JSON file
                (default: config/config.json)
        """
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
        """Load parameters from AWS SSM Parameter Store.

        Args:
            parameter_names: List of parameter names to load
        """
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

    def load_from_ssm(self, path_prefix):
        """Load configuration from AWS SSM Parameter Store.

        Args:
            path_prefix: Path prefix for SSM parameters

        Returns:
            dict: Configuration loaded from SSM
        """
        try:
            ssm = boto3.client('ssm')
            response = ssm.get_parameters_by_path(
                Path=path_prefix,
                Recursive=True,
                WithDecryption=True
            )
            config = {}
            for param in response['Parameters']:
                key = param['Name'].replace(path_prefix, '').lstrip('/')
                config[key] = param['Value']
            return config
        except Exception as e:
            logging.error(f"Error loading config from SSM: {e}")
            return {}

    def get_config(self, section=None, key=None):
        """Get configuration value for a specific section and key.

        Args:
            section: Configuration section name
            key: Configuration key within the section

        Returns:
            Any: Configuration value if found, None otherwise
        """
        if section and key:
            return self.config.get(section, {}).get(key)
        elif section:
            return self.config.get(section, {})
        return self.config

    def set_config(self, section, key, value):
        """Set or update a configuration value.

        Args:
            section: Configuration section name
            key: Configuration key within the section
            value: Value to set

        Returns:
            bool: True if value was set, False otherwise
        """
        if not section or not key:
            return False
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        return True

    def save_to_ssm(self, path_prefix: str, region_name: str = 'us-east-1') -> bool:
        """Save configuration to AWS SSM Parameter Store.

        Args:
            path_prefix: Path prefix for SSM parameters

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            ssm = boto3.client('ssm', region_name=region_name)
            for section, values in self.config.items():
                for key, value in values.items():
                    param_path = f"{path_prefix}/{section}/{key}"
                    ssm.put_parameter(
                        Name=param_path,
                        Value=str(value),
                        Type='SecureString',
                        Overwrite=True
                    )
            return True
        except Exception as e:
            logging.error(f"Error saving config to SSM: {e}")
            return False

    def load_from_environment(self):
        """Load configuration from environment variables.

        Returns:
            dict: Configuration loaded from environment
        """
        config = {}
        for var in os.environ:
            if var.startswith('APP_'):
                keys = var[4:].lower().split('__')
                current = config
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                current[keys[-1]] = os.environ[var]

        return config

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


if __name__ == '__main__':
    pass
