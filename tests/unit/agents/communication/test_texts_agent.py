import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.communication.texts_agent import handle_texts_request

class TestTextsAgent(unittest.TestCase):

    @patch('src.agents.communication.texts_agent.log_audit')
    def test_handle_texts_request(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'send_message'}

        # Act
        result = handle_texts_request(data, user_id)

        # Assert
        self.assertEqual(result, {
            'status': 'success',
            'message': 'Text message functionality not yet implemented.'
        })
        mock_log_audit.assert_called_once_with(user_id, 'texts_task', {'task': 'send_message'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch
from src.agents.communication import texts_agent

class TestTextsAgent(unittest.TestCase):

    @patch('src.agents.communication.texts_agent.log_audit')
    def test_handle_texts_request(self, mock_log_audit):
        """
        Test that handle_texts_request returns the placeholder message.
        """
        # Arrange
        data = {'task': 'send_text'}
        user_id = 'test_user'

        # Act
        result = texts_agent.handle_texts_request(data, user_id)

        # Assert
        self.assertEqual(result, {
            'status': 'success',
            'message': 'Text message functionality not yet implemented.'
        })
        mock_log_audit.assert_called_once_with(user_id, 'texts_task', {'task': 'send_text'})

    @patch('src.agents.communication.texts_agent.log_audit')
    def test_handle_texts_request_unknown_task(self, mock_log_audit):
        """
        Test that handle_texts_request handles an unknown task.
        """
        # Arrange
        data = {'task': None}
        user_id = 'test_user'

        # Act
        result = texts_agent.handle_texts_request(data, user_id)

        # Assert
        self.assertEqual(result, {
            'status': 'success',
            'message': 'Text message functionality not yet implemented.'
        })
        mock_log_audit.assert_called_once_with(user_id, 'texts_task', {'task': 'unknown'})

if __name__ == '__main__':
    unittest.main()
