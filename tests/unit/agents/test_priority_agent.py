import unittest
from unittest.mock import patch, MagicMock
from src.agents import priority_agent

class TestPriorityAgent(unittest.TestCase):

    @patch('src.agents.priority_agent.googleapiclient.discovery.build')
    @patch('src.agents.priority_agent.log_audit')
    def test_prioritize_success(self, mock_log_audit, mock_build):
        """
        Test that handle_priority_request successfully prioritizes tasks from Google Calendar.
        """
        # Arrange
        mock_service = MagicMock()
        mock_events = MagicMock()
        mock_list = MagicMock()
        
        # Sample events, out of order
        mock_list.execute.return_value = {
            'items': [
                {'summary': 'Event 2', 'start': {'dateTime': '2025-06-11T10:00:00Z'}},
                {'summary': 'Event 1', 'start': {'dateTime': '2025-06-11T09:00:00Z'}},
                {'summary': 'Event 3', 'start': {'dateTime': '2025-06-11T11:00:00Z'}},
            ]
        }
        mock_events.list.return_value = mock_list
        mock_service.events.return_value = mock_events
        mock_build.return_value = mock_service

        data = {
            'task': 'prioritize',
            'credentials': 'dummy_creds',
            'limit': 2
        }
        user_id = 'test_user'

        # Act
        result = priority_agent.handle_priority_request(data, user_id)

        # Assert
        mock_build.assert_called_once_with('calendar', 'v3', credentials='dummy_creds')
        mock_service.events().list(calendarId='primary').execute.assert_called_once()
        
        self.assertEqual(len(result['tasks']), 2)
        self.assertEqual(result['tasks'][0]['summary'], 'Event 1')
        self.assertEqual(result['tasks'][1]['summary'], 'Event 2')
        
        mock_log_audit.assert_called_once_with(user_id, 'priority_task', {'task': 'prioritize'})

    @patch('src.agents.priority_agent.googleapiclient.discovery.build')
    @patch('src.agents.priority_agent.log_audit')
    def test_unknown_task(self, mock_log_audit, mock_build):
        """
        Test that handle_priority_request handles an unknown task gracefully.
        """
        # Arrange
        data = {'task': 'some_other_task'}
        user_id = 'test_user'

        # Act
        result = priority_agent.handle_priority_request(data, user_id)

        # Assert
        mock_build.assert_not_called()
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'priority_task', {'task': 'some_other_task'})

    @patch('src.agents.priority_agent.googleapiclient.discovery.build')
    @patch('src.agents.priority_agent.log_audit')
    def test_api_exception(self, mock_log_audit, mock_build):
        """
        Test that handle_priority_request handles exceptions from the Google API.
        """
        # Arrange
        mock_build.side_effect = Exception("API Error")
        data = {
            'task': 'prioritize',
            'credentials': 'dummy_creds'
        }
        user_id = 'test_user'

        # Act
        result = priority_agent.handle_priority_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'API Error'})
        mock_log_audit.assert_called_once_with(user_id, 'priority_task', {'error': 'API Error'})

if __name__ == '__main__':
    unittest.main()
