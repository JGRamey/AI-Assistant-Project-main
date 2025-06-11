import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.communication.texts_agent import handle_texts_request

class TestTextsAgent(unittest.TestCase):

    @patch('src.agents.communication.texts_agent.log_audit')
    def test_handle_texts_request_send_task(self, mock_log_audit):
        """
        Test that handle_texts_request returns the placeholder message for a send task.
        """
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

    @patch('src.agents.communication.texts_agent.log_audit')
    def test_handle_texts_request_unknown_task(self, mock_log_audit):
        """
        Test that handle_texts_request handles an unknown task.
        """
        # Arrange
        data = {'task': None}
        user_id = 'test_user'

        # Act
        result = handle_texts_request(data, user_id)

        # Assert
        self.assertEqual(result, {
            'status': 'success',
            'message': 'Text message functionality not yet implemented.'
        })
        mock_log_audit.assert_called_once_with(user_id, 'texts_task', {'task': 'unknown'})

if __name__ == '__main__':
    unittest.main()
