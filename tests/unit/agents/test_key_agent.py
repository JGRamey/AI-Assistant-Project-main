import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.agents.key_agent import handle_key_request

class TestKeyAgent(unittest.TestCase):

    @patch('src.agents.key_agent.time')
    @patch('src.agents.key_agent.log_audit')
    @patch('src.agents.key_agent.encrypt_data')
    @patch('src.agents.key_agent.generate_new_key')
    @patch('src.agents.key_agent.boto3')
    def test_handle_key_request_refresh_key(self, mock_boto3, mock_generate_new_key, mock_encrypt_data, mock_log_audit, mock_time):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'refresh_key'}
        
        mock_ssm_client = MagicMock()
        mock_boto3.client.return_value = mock_ssm_client
        mock_generate_new_key.return_value = 'new-api-key-123'
        mock_encrypt_data.return_value = 'encrypted-key'
        mock_time.time.return_value = 1234567890

        # Act
        result = handle_key_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'key_refreshed', 'timestamp': 1234567890})
        mock_boto3.client.assert_called_once_with('ssm')
        mock_ssm_client.put_parameter.assert_called_once_with(
            Name=f'/my-ai-assistant/{user_id}/api-key',
            Value='encrypted-key',
            Type='SecureString',
            Overwrite=True
        )
        mock_log_audit.assert_called_once_with(user_id, 'key_task', {'task': 'refresh_key'})

    @patch('src.agents.key_agent.log_audit')
    def test_handle_key_request_unknown_task(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'unknown_task'}

        # Act
        result = handle_key_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'key_task', {'task': 'unknown_task'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch, MagicMock
import time
from src.agents import key_agent

class TestKeyAgent(unittest.TestCase):

    @patch('src.agents.key_agent.time.time')
    @patch('src.agents.key_agent.encrypt_data')
    @patch('src.agents.key_agent.generate_new_key')
    @patch('src.agents.key_agent.boto3.client')
    @patch('src.agents.key_agent.log_audit')
    def test_refresh_key_success(self, mock_log_audit, mock_boto_client, mock_generate_key, mock_encrypt_data, mock_time):
        """
        Test that handle_key_request successfully refreshes and stores a new key.
        """
        # Arrange
        mock_ssm_client = MagicMock()
        mock_boto_client.return_value = mock_ssm_client
        mock_generate_key.return_value = 'new-api-key-123'
        mock_encrypt_data.return_value = 'encrypted-key'
        mock_time.return_value = 1234567890

        data = {'task': 'refresh_key'}
        user_id = 'test_user'

        # Act
        result = key_agent.handle_key_request(data, user_id)

        # Assert
        mock_boto_client.assert_called_once_with('ssm')
        mock_generate_key.assert_called_once()
        mock_encrypt_data.assert_called_once_with('new-api-key-123')
        mock_ssm_client.put_parameter.assert_called_once_with(
            Name='/my-ai-assistant/test_user/api-key',
            Value='encrypted-key',
            Type='SecureString',
            Overwrite=True
        )
        mock_log_audit.assert_called_once_with(user_id, 'key_task', {'task': 'refresh_key'})
        self.assertEqual(result, {'status': 'key_refreshed', 'timestamp': 1234567890})

    @patch('src.agents.key_agent.log_audit')
    def test_unknown_task(self, mock_log_audit):
        """
        Test that handle_key_request handles an unknown task gracefully.
        """
        # Arrange
        data = {'task': 'some_other_task'}
        user_id = 'test_user'

        # Act
        result = key_agent.handle_key_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'key_task', {'task': 'some_other_task'})

    @patch('src.agents.key_agent.boto3.client')
    @patch('src.agents.key_agent.log_audit')
    def test_ssm_exception(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_key_request handles exceptions from SSM.
        """
        # Arrange
        mock_boto_client.side_effect = Exception("SSM is down")

        data = {'task': 'refresh_key'}
        user_id = 'test_user'

        # Act
        result = key_agent.handle_key_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'SSM is down'})
        mock_log_audit.assert_called_once_with(user_id, 'key_task', {'error': 'SSM is down'})

if __name__ == '__main__':
    unittest.main()
