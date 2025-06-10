import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.communication.voice_agent import handle_voice_request

class TestVoiceAgent(unittest.TestCase):

    @patch('src.agents.communication.voice_agent.log_audit')
    @patch('src.agents.communication.voice_agent.requests.post')
    def test_handle_voice_request_tts(self, mock_post, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'tts', 'text': 'Hello'}
        mock_response = MagicMock()
        mock_response.content = b'audio_data'
        mock_post.return_value = mock_response

        # Act
        result = handle_voice_request(data, user_id)

        # Assert
        self.assertEqual(result, {'audio': '617564696f5f64617461'})
        mock_post.assert_called_once_with(
            'http://mimic3:59125/api/tts',
            json={'text': 'Hello'},
            timeout=10
        )
        mock_response.raise_for_status.assert_called_once()
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'task': 'tts'})

    @patch('src.agents.communication.voice_agent.log_audit')
    def test_handle_voice_request_stt(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'stt'}

        # Act
        result = handle_voice_request(data, user_id)

        # Assert
        self.assertEqual(result, {'text': 'Transcribed text'})
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'task': 'stt'})

    @patch('src.agents.communication.voice_agent.log_audit')
    def test_handle_voice_request_unknown_task(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'unknown'}

        # Act
        result = handle_voice_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'task': 'unknown'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch, MagicMock
from src.agents.communication import voice_agent

class TestVoiceAgent(unittest.TestCase):

    @patch('src.agents.communication.voice_agent.requests.post')
    @patch('src.agents.communication.voice_agent.log_audit')
    def test_tts_success(self, mock_log_audit, mock_post):
        """
        Test that handle_voice_request successfully handles a TTS request.
        """
        # Arrange
        mock_response = MagicMock()
        mock_response.content = b'audio_bytes'
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        data = {'task': 'tts', 'text': 'Hello world'}
        user_id = 'test_user'

        # Act
        result = voice_agent.handle_voice_request(data, user_id)

        # Assert
        mock_post.assert_called_once_with(
            'http://mimic3:59125/api/tts',
            json={'text': 'Hello world'},
            timeout=10
        )
        self.assertEqual(result, {'audio': '617564696f5f6279746573'})
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'task': 'tts'})

    @patch('src.agents.communication.voice_agent.log_audit')
    def test_stt_success(self, mock_log_audit):
        """
        Test that handle_voice_request successfully handles an STT request.
        """
        # Arrange
        data = {'task': 'stt'}
        user_id = 'test_user'

        # Act
        result = voice_agent.handle_voice_request(data, user_id)

        # Assert
        self.assertEqual(result, {'text': 'Transcribed text'})
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'task': 'stt'})

    @patch('src.agents.communication.voice_agent.log_audit')
    def test_unknown_task(self, mock_log_audit):
        """
        Test that handle_voice_request handles an unknown task gracefully.
        """
        # Arrange
        data = {'task': 'some_other_task'}
        user_id = 'test_user'

        # Act
        result = voice_agent.handle_voice_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'task': 'some_other_task'})

    @patch('src.agents.communication.voice_agent.requests.post')
    @patch('src.agents.communication.voice_agent.log_audit')
    def test_api_exception(self, mock_log_audit, mock_post):
        """
        Test that handle_voice_request handles exceptions from the API.
        """
        # Arrange
        mock_post.side_effect = Exception("API Error")
        data = {'task': 'tts', 'text': 'Hello world'}
        user_id = 'test_user'

        # Act
        result = voice_agent.handle_voice_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'API Error'})
        mock_log_audit.assert_called_once_with(user_id, 'voice_task', {'error': 'API Error'})

if __name__ == '__main__':
    unittest.main()
