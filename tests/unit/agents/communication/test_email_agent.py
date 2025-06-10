import unittest
from unittest.mock import patch, MagicMock
import base64
from src.agents.communication import email_agent

class TestEmailAgent(unittest.TestCase):

    @patch('src.agents.communication.email_agent.build')
    @patch('src.agents.communication.email_agent.log_audit')
    def test_read_email_success(self, mock_log_audit, mock_build):
        """
        Test that handle_email_request successfully reads emails.
        """
        # Arrange
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.users().messages().list().execute.return_value = {'messages': ['email1', 'email2']}

        data = {'task': 'read', 'credentials': 'dummy_creds'}
        user_id = 'test_user'

        # Act
        result = email_agent.handle_email_request(data, user_id)

        # Assert
        mock_build.assert_called_once_with('gmail', 'v1', credentials='dummy_creds')
        self.assertEqual(result, {'emails': ['email1', 'email2']})
        mock_log_audit.assert_called_once_with(user_id, 'email_task', {'task': 'read'})

    @patch('src.agents.communication.email_agent.build')
    @patch('src.agents.communication.email_agent.log_audit')
    def test_send_email_success(self, mock_log_audit, mock_build):
        """
        Test that handle_email_request successfully sends an email.
        """
        # Arrange
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        data = {
            'task': 'send',
            'credentials': 'dummy_creds',
            'to': 'recipient@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
        user_id = 'test_user'

        # Act
        result = email_agent.handle_email_request(data, user_id)

        # Assert
        mock_service.users().messages().send.assert_called_once()
        self.assertEqual(result, {'status': 'sent'})
        mock_log_audit.assert_called_once_with(user_id, 'email_task', {'task': 'send'})

    @patch('src.agents.communication.email_agent.build')
    @patch('src.agents.communication.email_agent.log_audit')
    def test_unknown_task(self, mock_log_audit, mock_build):
        """
        Test that handle_email_request handles an unknown task.
        """
        # Arrange
        data = {'task': 'unknown', 'credentials': 'dummy_creds'}
        user_id = 'test_user'

        # Act
        result = email_agent.handle_email_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'email_task', {'task': 'unknown'})

    @patch('src.agents.communication.email_agent.build')
    @patch('src.agents.communication.email_agent.log_audit')
    def test_api_exception(self, mock_log_audit, mock_build):
        """
        Test that handle_email_request handles API exceptions.
        """
        # Arrange
        mock_build.side_effect = Exception("API Error")
        data = {'task': 'read', 'credentials': 'dummy_creds'}
        user_id = 'test_user'

        # Act
        result = email_agent.handle_email_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'API Error'})
        mock_log_audit.assert_called_once_with(user_id, 'email_task', {'error': 'API Error'})

    def test_create_message(self):
        """
        Test the create_message helper function.
        """
        # Arrange
        to = 'recipient@example.com'
        subject = 'Test Subject'
        body = 'Test Body'

        # Act
        message = email_agent.create_message(to, subject, body)
        expected_content = f"To: {to}\nSubject: {subject}\n\n{body}".encode()
        expected_encoded = base64.urlsafe_b64encode(expected_content).decode()

        # Assert
        self.assertEqual(message, {'raw': expected_encoded})

if __name__ == '__main__':
    unittest.main()
