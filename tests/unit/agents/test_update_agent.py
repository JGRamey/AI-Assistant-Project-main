import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.agents import update_agent

class TestUpdateAgent(unittest.TestCase):

    @patch('src.agents.update_agent.time.time')
    @patch('src.agents.update_agent.encrypt_data')
    @patch('src.agents.update_agent.requests.post')
    @patch('src.agents.update_agent.sqlite3.connect')
    @patch('src.agents.update_agent.log_audit')
    def test_log_update_success(self, mock_log_audit, mock_connect, mock_post, mock_encrypt, mock_time):
        """
        Test that handle_update_request successfully logs an update.
        """
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_response = MagicMock()
        mock_response.json.return_value = {'summary': 'Summarized changes'}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        mock_encrypt.return_value = 'encrypted_notes'
        mock_time.return_value = 1234567890

        data = {'task': 'log_update', 'changes': 'Some detailed changes'}
        user_id = 'test_user'

        # Act
        result = update_agent.handle_update_request(data, user_id)

        # Assert
        mock_post.assert_called_once_with('https://api.x.ai/grok/summarize', json={'text': 'Some detailed changes'})
        mock_encrypt.assert_called_once_with('Summarized changes')
        mock_cursor.execute.assert_any_call('INSERT INTO updates VALUES (?, ?, ?, ?)', ('test_user', 'update_1234567890', 'encrypted_notes', 1234567890))
        mock_conn.commit.assert_called_once()
        mock_log_audit.assert_called_once_with(user_id, 'update_task', {'task': 'log_update'})
        self.assertEqual(result, {'status': 'update_logged', 'update_id': 'update_1234567890'})

    @patch('src.agents.update_agent.decrypt_data')
    @patch('src.agents.update_agent.sqlite3.connect')
    @patch('src.agents.update_agent.log_audit')
    def test_view_updates_success(self, mock_log_audit, mock_connect, mock_decrypt):
        """
        Test that handle_update_request successfully views updates.
        """
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('update1', 'encrypted1', 123), ('update2', 'encrypted2', 456)]
        mock_decrypt.side_effect = ['decrypted1', 'decrypted2']

        data = {'task': 'view_updates'}
        user_id = 'test_user'

        # Act
        result = update_agent.handle_update_request(data, user_id)

        # Assert
        mock_cursor.execute.assert_called_with('SELECT update_id, notes, timestamp FROM updates WHERE user_id = ?', ('test_user',))
        self.assertEqual(len(result['updates']), 2)
        self.assertEqual(result['updates'][0]['notes'], 'decrypted1')
        self.assertEqual(result['updates'][1]['notes'], 'decrypted2')
        mock_log_audit.assert_called_once_with(user_id, 'update_task', {'task': 'view_updates'})

    @patch('src.agents.update_agent.log_audit')
    def test_unknown_task(self, mock_log_audit):
        """
        Test that handle_update_request handles an unknown task gracefully.
        """
        # Arrange
        data = {'task': 'some_other_task'}
        user_id = 'test_user'

        # Act
        result = update_agent.handle_update_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'update_task', {'task': 'some_other_task'})

    @patch('src.agents.update_agent.sqlite3.connect')
    @patch('src.agents.update_agent.log_audit')
    def test_db_exception(self, mock_log_audit, mock_connect):
        """
        Test that handle_update_request handles database exceptions.
        """
        # Arrange
        mock_connect.side_effect = sqlite3.Error("DB is down")
        data = {'task': 'log_update', 'changes': 'Some changes'}
        user_id = 'test_user'

        # Act
        result = update_agent.handle_update_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'DB is down'})
        mock_log_audit.assert_called_once_with(user_id, 'update_task', {'error': 'DB is down'})

if __name__ == '__main__':
    unittest.main()
