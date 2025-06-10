import unittest
from unittest.mock import patch, MagicMock
from src.agents import alert_agent

class TestAlertAgent(unittest.TestCase):

    @patch('src.agents.alert_agent.boto3.client')
    @patch('src.agents.alert_agent.log_audit')
    def test_handle_alert_request_set_alert(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_alert_request sends an SNS alert when task is 'set_alert'.
        """
        # Arrange
        mock_sns_client = MagicMock()
        mock_boto_client.return_value = mock_sns_client

        data = {
            'task': 'set_alert',
            'topic_arn': 'arn:aws:sns:us-east-1:123456789012:MyTopic',
            'message': 'Test alert message'
        }
        user_id = 'test_user'

        # Act
        result = alert_agent.handle_alert_request(data, user_id)

        # Assert
        mock_boto_client.assert_called_once_with('sns')
        mock_sns_client.publish.assert_called_once_with(
            TopicArn='arn:aws:sns:us-east-1:123456789012:MyTopic',
            Message='Trade Alert: Test alert message'
        )
        self.assertEqual(result, {'status': 'alert_sent'})
        mock_log_audit.assert_not_called()

    @patch('src.agents.alert_agent.boto3.client')
    @patch('src.agents.alert_agent.log_audit')
    def test_handle_alert_request_other_task(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_alert_request handles other tasks gracefully.
        """
        # Arrange
        data = {'task': 'some_other_task'}
        user_id = 'test_user'

        # Act
        result = alert_agent.handle_alert_request(data, user_id)

        # Assert
        mock_boto_client.assert_called_once_with('sns')
        mock_boto_client.return_value.publish.assert_not_called()
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'alert_task', {'task': 'some_other_task'})

    @patch('src.agents.alert_agent.boto3.client')
    @patch('src.agents.alert_agent.log_audit')
    def test_handle_alert_request_exception(self, mock_log_audit, mock_boto_client):
        """
        Test that handle_alert_request handles exceptions and logs them.
        """
        # Arrange
        mock_sns_client = MagicMock()
        mock_sns_client.publish.side_effect = Exception("SNS is down")
        mock_boto_client.return_value = mock_sns_client

        data = {
            'task': 'set_alert',
            'topic_arn': 'arn:aws:sns:us-east-1:123456789012:MyTopic',
            'message': 'Test alert message'
        }
        user_id = 'test_user'

        # Act
        result = alert_agent.handle_alert_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'SNS is down'})
        mock_log_audit.assert_called_once_with(user_id, 'alert_task', {'error': 'SNS is down'})

if __name__ == '__main__':
    unittest.main()
