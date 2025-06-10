import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.communication.social_agent import handle_social_request

class TestSocialAgent(unittest.TestCase):

    @patch('src.agents.communication.social_agent.log_audit')
    @patch('src.agents.communication.social_agent.tweepy')
    def test_handle_social_request_post(self, mock_tweepy, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {
            'task': 'post',
            'consumer_key': 'test_ck',
            'consumer_secret': 'test_cs',
            'access_token': 'test_at',
            'access_secret': 'test_as',
            'content': 'Hello, world!'
        }

        mock_api = MagicMock()
        mock_auth = MagicMock()
        mock_tweepy.OAuthHandler.return_value = mock_auth
        mock_tweepy.API.return_value = mock_api

        # Act
        result = handle_social_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'posted'})
        mock_tweepy.OAuthHandler.assert_called_once_with('test_ck', 'test_cs')
        mock_auth.set_access_token.assert_called_once_with('test_at', 'test_as')
        mock_api.update_status.assert_called_once_with('Hello, world!')
        mock_log_audit.assert_called_once_with(user_id, 'social_task', {'task': 'post'})

    @patch('src.agents.communication.social_agent.log_audit')
    def test_handle_social_request_unknown_task(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'unknown_task'}

        # Act
        result = handle_social_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'social_task', {'task': 'unknown_task'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch, MagicMock
from src.agents.communication import social_agent

class TestSocialAgent(unittest.TestCase):

    @patch('src.agents.communication.social_agent.tweepy')
    @patch('src.agents.communication.social_agent.log_audit')
    def test_post_success(self, mock_log_audit, mock_tweepy):
        """
        Test that handle_social_request successfully posts a status.
        """
        # Arrange
        mock_api = MagicMock()
        mock_auth_handler = MagicMock()
        mock_tweepy.OAuthHandler.return_value = mock_auth_handler
        mock_tweepy.API.return_value = mock_api

        data = {
            'task': 'post',
            'consumer_key': 'ckey',
            'consumer_secret': 'csecret',
            'access_token': 'atoken',
            'access_secret': 'asecret',
            'content': 'Hello Twitter!'
        }
        user_id = 'test_user'

        # Act
        result = social_agent.handle_social_request(data, user_id)

        # Assert
        mock_tweepy.OAuthHandler.assert_called_once_with('ckey', 'csecret')
        mock_auth_handler.set_access_token.assert_called_once_with('atoken', 'asecret')
        mock_tweepy.API.assert_called_once_with(mock_auth_handler)
        mock_api.update_status.assert_called_once_with('Hello Twitter!')
        self.assertEqual(result, {'status': 'posted'})
        mock_log_audit.assert_called_once_with(user_id, 'social_task', {'task': 'post'})

    @patch('src.agents.communication.social_agent.log_audit')
    def test_unknown_task(self, mock_log_audit):
        """
        Test that handle_social_request handles an unknown task.
        """
        # Arrange
        data = {'task': 'unknown'}
        user_id = 'test_user'

        # Act
        result = social_agent.handle_social_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'social_task', {'task': 'unknown'})

    @patch('src.agents.communication.social_agent.tweepy')
    @patch('src.agents.communication.social_agent.log_audit')
    def test_api_exception(self, mock_log_audit, mock_tweepy):
        """
        Test that handle_social_request handles API exceptions.
        """
        # Arrange
        mock_tweepy.OAuthHandler.side_effect = Exception("API Error")
        data = {
            'task': 'post',
            'consumer_key': 'ckey',
            'consumer_secret': 'csecret',
            'access_token': 'atoken',
            'access_secret': 'asecret',
            'content': 'Hello Twitter!'
        }
        user_id = 'test_user'

        # Act
        result = social_agent.handle_social_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'API Error'})
        mock_log_audit.assert_called_once_with(user_id, 'social_task', {'error': 'API Error'})

if __name__ == '__main__':
    unittest.main()
