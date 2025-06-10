import json
import os
import boto3
from botocore.exceptions import ClientError


class ConfigManager:
    def __init__(self, config_path='config/config.json'):  # Default config path
        self.config = self._load_config_from_file(config_path)
        self._load_secrets()

    def _load_config_from_file(self, config_path):
        """Loads configuration from a JSON file."""
        base_dir = os.path.dirname(os.path.abspath(__file__))  # .../src
        project_root = os.path.dirname(base_dir)  # .../
        abs_config_path = os.path.join(project_root, config_path)

        try:
            with open(abs_config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {abs_config_path}. Using default values.")
            return {}
        except json.JSONDecodeError:  # Invalid JSON format
            print(f"Warning: Could not decode JSON from {abs_config_path}. Using default values.")
            return {}

    def _load_secrets(self):
        """
        Loads secrets from AWS SSM Parameter Store if in a Lambda environment,
        otherwise falls back to environment variables.
        """
        ssm_parameter_names = self.config.get('ssm_parameters', [])
        if ssm_parameter_names and os.getenv('AWS_LAMBDA_FUNCTION_NAME'):  # Check if in Lambda
            self._load_from_ssm(ssm_parameter_names)
        else:
            self._load_from_env()

    def _load_from_ssm(self, parameter_names):
        """Loads parameters from AWS SSM Parameter Store."""
        ssm = boto3.client('ssm')
        try:
            response = ssm.get_parameters(
                Names=parameter_names,
                WithDecryption=True
            )
            for parameter in response['Parameters']:
                key = parameter['Name'].split('/')[-1]
                self.config[key] = parameter['Value']
            print("Successfully loaded secrets from SSM Parameter Store.")
        except ClientError as e:
            print(f"Error loading secrets from SSM: {e}. Falling back to environment variables.")
            self._load_from_env()

    def _load_from_env(self):
        """Loads secrets from environment variables (for local dev)."""
        secret_keys = self.config.get('secret_keys', [])
        for key in secret_keys:  # Process each secret key
            value = os.getenv(key)
            if value:
                self.config[key] = value
        print("Loaded secrets from environment variables.")

    def get(self, key, default=None):
        """Gets a configuration value."""
        return self.config.get(key, default)


_config_manager = None


def get_config_manager():
    """Get the singleton instance of ConfigManager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config(key, default=None):
    """Get a configuration value using the singleton ConfigManager."""
    return get_config_manager().get(key, default)
