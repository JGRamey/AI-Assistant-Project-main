import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.communication.notes_agent import handle_notes_request

class TestNotesAgent(unittest.TestCase):

    @patch('src.agents.communication.notes_agent.log_audit')
    @patch('src.agents.communication.notes_agent.boto3')
    def test_handle_notes_request_save_note(self, mock_boto3, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {
            'task': 'save_note',
            'note_id': 'test_note_789',
            'content': 'This is a test note.'
        }

        mock_s3_client = MagicMock()
        mock_boto3.client.return_value = mock_s3_client

        # Act
        result = handle_notes_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'note_saved'})
        mock_boto3.client.assert_called_once_with('s3')
        mock_s3_client.put_object.assert_called_once_with(
            Bucket='my-ai-notes',
            Key=f"{user_id}/{data['note_id']}.txt",
            Body=data['content']
        )
        mock_log_audit.assert_called_once_with(user_id, 'notes_task', {'task': 'save_note'})

    @patch('src.agents.communication.notes_agent.log_audit')
    def test_handle_notes_request_unknown_task(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'unknown_task'}

        # Act
        result = handle_notes_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'notes_task', {'task': 'unknown_task'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch, MagicMock
from src.agents.communication import notes_agent

class TestNotesAgent(unittest.TestCase):

    @patch('src.agents.communication.notes_agent.boto3.client')
    @patch('src.agents.communication.notes_agent.log_audit')
    def test_save_note_success(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_notes_request successfully saves a note to S3.
        """
        # Arrange
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client

        data = {
            'task': 'save_note',
            'note_id': 'note123',
            'content': 'This is a test note.'
        }
        user_id = 'test_user'

        # Act
        result = notes_agent.handle_notes_request(data, user_id)

        # Assert
        mock_boto_client.assert_called_once_with('s3')
        mock_s3_client.put_object.assert_called_once_with(
            Bucket='my-ai-notes',
            Key='test_user/note123.txt',
            Body='This is a test note.'
        )
        self.assertEqual(result, {'status': 'note_saved'})
        mock_log_audit.assert_called_once_with(user_id, 'notes_task', {'task': 'save_note'})

    @patch('src.agents.communication.notes_agent.boto3.client')
    @patch('src.agents.communication.notes_agent.log_audit')
    def test_unknown_task(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_notes_request handles an unknown task gracefully.
        """
        # Arrange
        data = {'task': 'some_other_task'}
        user_id = 'test_user'

        # Act
        result = notes_agent.handle_notes_request(data, user_id)

        # Assert
        mock_boto_client.assert_not_called()
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'notes_task', {'task': 'some_other_task'})

    @patch('src.agents.communication.notes_agent.boto3.client')
    @patch('src.agents.communication.notes_agent.log_audit')
    def test_s3_exception(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_notes_request handles exceptions from S3.
        """
        # Arrange
        mock_s3_client = MagicMock()
        mock_s3_client.put_object.side_effect = Exception("S3 is down")
        mock_boto_client.return_value = mock_s3_client

        data = {
            'task': 'save_note',
            'note_id': 'note123',
            'content': 'This is a test note.'
        }
        user_id = 'test_user'

        # Act
        result = notes_agent.handle_notes_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'S3 is down'})
        mock_log_audit.assert_called_once_with(user_id, 'notes_task', {'error': 'S3 is down'})

if __name__ == '__main__':
    unittest.main()
