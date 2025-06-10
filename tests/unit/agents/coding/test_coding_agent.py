import unittest
from unittest.mock import patch, MagicMock
from src.agents.coding import coding_agent

class TestCodingAgent(unittest.TestCase):

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.send_message')
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_generate_rust(self, mock_log, mock_store, mock_send, mock_time):
        """Test rust code generation."""
        data = {'task': 'generate_rust', 'spec': 'hello_world'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        self.assertIn('fn main()', result['result']['code'])
        self.assertIn('hello_world', result['result']['code'])
        mock_send.assert_called_once()
        mock_store.assert_called()
        mock_log.assert_called()

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.send_message')
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_generate_python(self, mock_log, mock_store, mock_send, mock_time):
        """Test python code generation."""
        data = {'task': 'generate_python', 'spec': 'hello_world'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        self.assertIn('def main():', result['result']['code'])
        self.assertIn('hello_world', result['result']['code'])
        mock_send.assert_called_once()
        mock_store.assert_called()
        mock_log.assert_called()

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.send_message')
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_generate_solidity(self, mock_log, mock_store, mock_send, mock_time):
        """Test solidity code generation and message sending."""
        data = {'task': 'generate_solidity', 'spec': 'MyContract'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        self.assertIn('contract MyContract', result['result']['code'])
        self.assertEqual(mock_send.call_count, 2)
        mock_store.assert_called()
        mock_log.assert_called()

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.requests.post')
    @patch('src.agents.coding.coding_agent.get_config', return_value='test_api_key')
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_grok_suggest_success(self, mock_log, mock_store, mock_get_config, mock_post, mock_time):
        """Test grok code suggestion success."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'suggestions': ['suggestion1', 'suggestion2']}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        data = {'task': 'grok_suggest', 'code': 'print("hello")'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)

        mock_post.assert_called_once_with(
            "https://api.x.ai/grok/code_suggest",
            json={"code": 'print("hello")', "user_id": "test_user"},
            headers={'Authorization': 'Bearer test_api_key'},
            timeout=10
        )
        self.assertEqual(result['result']['suggestions'], ['suggestion1', 'suggestion2'])
        mock_store.assert_called()
        mock_log.assert_called()

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_save_session(self, mock_log, mock_store, mock_time):
        """Test saving a coding session."""
        data = {'task': 'save_session', 'session': {'code': 'test code'}, 'task_id': 'test_task_id'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        mock_store.assert_any_call('coding_session_test_task_id', {'code': 'test code'}, 'test_user')
        self.assertTrue(result['result']['saved'])
        mock_log.assert_called()

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.get_shared_data', return_value={'code': 'loaded code'})
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_load_session(self, mock_log, mock_store, mock_get, mock_time):
        """Test loading a coding session."""
        data = {'task': 'load_session', 'session_id': 'some_id'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        mock_get.assert_called_once_with('coding_session_some_id', 'test_user')
        self.assertEqual(result['result'], {'code': 'loaded code'})
        mock_store.assert_called()
        mock_log.assert_called()

    @patch('src.agents.coding.coding_agent.time.time', return_value=12345)
    @patch('src.agents.coding.coding_agent.store_shared_data')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_unknown_task(self, mock_log, mock_store, mock_time):
        """Test handling of an unknown task."""
        data = {'task': 'unknown'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        self.assertEqual(result['status'], 'success')
        mock_store.assert_called_once_with('coding_code_12345', {}, 'test_user')
        mock_log.assert_called_once_with('test_user', 'code_unknown', result)

    @patch('src.agents.coding.coding_agent.requests.post')
    @patch('src.agents.coding.coding_agent.get_config', return_value='test_api_key')
    @patch('src.agents.coding.coding_agent.log_audit')
    def test_api_exception(self, mock_log, mock_get_config, mock_post):
        """Test exception handling for API calls."""
        mock_post.side_effect = Exception("API is down")
        data = {'task': 'grok_suggest', 'code': 'print("hello")'}
        user_id = 'test_user'
        result = coding_agent.handle_code_request(data, user_id)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['result'], 'API is down')
        mock_log.assert_called_with('test_user', 'code_task', {'error': 'API is down'})

if __name__ == '__main__':
    unittest.main()
