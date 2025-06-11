import unittest
import sys
import os
import requests
import requests_mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.agents.communication.voice_agent import handle_voice_request

class TestVoiceAgentIntegration(unittest.TestCase):

    @requests_mock.Mocker()
    def test_tts_integration(self, m):
        # Arrange
        user_id = "integration_test_user"
        data = {'task': 'tts', 'text': 'This is an integration test.'}
        m.post('http://mimic3:59125/api/tts', content=b'audio_data')

        # Act
        result = handle_voice_request(data, user_id)

        # Assert
        self.assertIn('audio', result)
        self.assertEqual(result['audio'], '617564696f5f64617461')

