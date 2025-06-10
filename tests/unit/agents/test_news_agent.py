import unittest
from unittest.mock import patch, MagicMock
import requests
from src.agents import news_agent

class TestNewsAgent(unittest.TestCase):

    @patch('src.agents.news_agent.requests.get')
    @patch('src.agents.news_agent.log_audit')
    def test_fetch_news_success(self, mock_log_audit, mock_requests_get):
        """
        Test that handle_news_request successfully fetches and filters news.
        """
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': [
                {'title': 'Big news for crypto!', 'content': '...'}, 
                {'title': 'Something else happened', 'content': '...'},
                {'title': 'Another crypto story', 'content': '...'}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        data = {'task': 'fetch_news'}
        user_id = 'test_user'

        # Act
        result = news_agent.handle_news_request(data, user_id)

        # Assert
        mock_requests_get.assert_called_once_with('https://api.coingecko.com/api/v3/news', timeout=10)
        self.assertEqual(len(result['news']), 2)
        self.assertEqual(result['news'][0]['title'], 'Big news for crypto!')
        self.assertEqual(result['news'][1]['title'], 'Another crypto story')
        mock_log_audit.assert_called_once_with(user_id, 'news_task', {'task': 'fetch_news'})

    @patch('src.agents.news_agent.requests.get')
    @patch('src.agents.news_agent.log_audit')
    def test_fetch_m2_success(self, mock_log_audit, mock_requests_get):
        """
        Test that handle_news_request successfully fetches M2 data.
        """
        # Arrange
        mock_response = MagicMock()
        mock_response.text = 'M2 data text'
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        data = {'task': 'fetch_m2'}
        user_id = 'test_user'

        # Act
        result = news_agent.handle_news_request(data, user_id)

        # Assert
        mock_requests_get.assert_called_once_with('https://fred.stlouisfed.org/series/M2SL', timeout=10)
        self.assertEqual(result, {'m2_data': 'M2 data text'})
        mock_log_audit.assert_called_once_with(user_id, 'news_task', {'task': 'fetch_m2'})

    @patch('src.agents.news_agent.requests.get')
    @patch('src.agents.news_agent.log_audit')
    def test_unknown_task(self, mock_log_audit, mock_requests_get):
        """
        Test that handle_news_request handles an unknown task.
        """
        # Arrange
        data = {'task': 'unknown_task'}
        user_id = 'test_user'

        # Act
        result = news_agent.handle_news_request(data, user_id)

        # Assert
        mock_requests_get.assert_not_called()
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'news_task', {'task': 'unknown_task'})

    @patch('src.agents.news_agent.requests.get')
    @patch('src.agents.news_agent.log_audit')
    def test_request_exception(self, mock_log_audit, mock_requests_get):
        """
        Test that handle_news_request handles a request exception.
        """
        # Arrange
        mock_requests_get.side_effect = requests.exceptions.RequestException('API is down')

        data = {'task': 'fetch_news'}
        user_id = 'test_user'

        # Act
        result = news_agent.handle_news_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'API is down'})
        mock_log_audit.assert_called_once_with(user_id, 'news_task', {'error': 'API is down'})

if __name__ == '__main__':
    unittest.main()
