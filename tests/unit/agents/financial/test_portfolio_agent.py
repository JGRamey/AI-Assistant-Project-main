import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.financial.portfolio_agent import handle_portfolio_request

class TestPortfolioAgent(unittest.TestCase):

    @patch('src.agents.financial.portfolio_agent.log_audit')
    @patch('src.agents.financial.portfolio_agent.ccxt')
    def test_handle_portfolio_request_view_portfolio(self, mock_ccxt, mock_log_audit):
        user_id = "test_user_123"
        data = {
            'task': 'view_portfolio',
            'api_key': 'test_api_key',
            'api_secret': 'test_api_secret'
        }

        mock_exchange = MagicMock()
        mock_exchange.fetch_balance.return_value = {'total': {'USD': 1000.0}}
        mock_ccxt.coinbase.return_value = mock_exchange

        result = handle_portfolio_request(data, user_id)

        self.assertEqual(result, {'portfolio': {'USD': 1000.0}})
        mock_ccxt.coinbase.assert_called_once_with({
            'apiKey': 'test_api_key',
            'secret': 'test_api_secret'
        })
        mock_exchange.fetch_balance.assert_called_once()
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'task': 'view_portfolio'})

    @patch('src.agents.financial.portfolio_agent.log_audit')
    def test_handle_portfolio_request_unknown_task(self, mock_log_audit):
        user_id = "test_user_123"
        data = {'task': 'unknown_task'}

        result = handle_portfolio_request(data, user_id)

        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'task': 'unknown_task'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.financial.portfolio_agent import handle_portfolio_request

class TestPortfolioAgent(unittest.TestCase):

    @patch('src.agents.financial.portfolio_agent.log_audit')
    @patch('src.agents.financial.portfolio_agent.ccxt')
    def test_handle_portfolio_request_view_portfolio(self, mock_ccxt, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {
            'task': 'view_portfolio',
            'api_key': 'test_api_key',
            'api_secret': 'test_api_secret'
        }

        mock_exchange = MagicMock()
        mock_exchange.fetch_balance.return_value = {'total': {'USD': 1000.0}}
        mock_ccxt.coinbase.return_value = mock_exchange

        # Act
        result = handle_portfolio_request(data, user_id)

        # Assert
        self.assertEqual(result, {'portfolio': {'USD': 1000.0}})
        mock_ccxt.coinbase.assert_called_once_with({
            'apiKey': 'test_api_key',
            'secret': 'test_api_secret'
        })
        mock_exchange.fetch_balance.assert_called_once()
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'task': 'view_portfolio'})

    @patch('src.agents.financial.portfolio_agent.log_audit')
    def test_handle_portfolio_request_unknown_task(self, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task': 'unknown_task'}

        # Act
        result = handle_portfolio_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'task': 'unknown_task'})

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch, MagicMock
from src.agents.financial import portfolio_agent

class TestPortfolioAgent(unittest.TestCase):

    @patch('src.agents.financial.portfolio_agent.ccxt.coinbase')
    @patch('src.agents.financial.portfolio_agent.log_audit')
    def test_view_portfolio_success(self, mock_log_audit, mock_coinbase):
        """
        Test that handle_portfolio_request successfully fetches the portfolio.
        """
        # Arrange
        mock_exchange = MagicMock()
        mock_coinbase.return_value = mock_exchange
        mock_exchange.fetch_balance.return_value = {'total': {'USD': 1000}}

        data = {
            'task': 'view_portfolio',
            'api_key': 'test_key',
            'api_secret': 'test_secret'
        }
        user_id = 'test_user'

        # Act
        result = portfolio_agent.handle_portfolio_request(data, user_id)

        # Assert
        mock_coinbase.assert_called_once_with({
            'apiKey': 'test_key',
            'secret': 'test_secret'
        })
        self.assertEqual(result, {'portfolio': {'USD': 1000}})
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'task': 'view_portfolio'})

    @patch('src.agents.financial.portfolio_agent.log_audit')
    def test_unknown_task(self, mock_log_audit):
        """
        Test that handle_portfolio_request handles an unknown task.
        """
        # Arrange
        data = {'task': 'unknown'}
        user_id = 'test_user'

        # Act
        result = portfolio_agent.handle_portfolio_request(data, user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'task': 'unknown'})

    @patch('src.agents.financial.portfolio_agent.ccxt.coinbase')
    @patch('src.agents.financial.portfolio_agent.log_audit')
    def test_api_exception(self, mock_log_audit, mock_coinbase):
        """
        Test that handle_portfolio_request handles API exceptions.
        """
        # Arrange
        mock_coinbase.side_effect = Exception("API Error")
        data = {
            'task': 'view_portfolio',
            'api_key': 'test_key',
            'api_secret': 'test_secret'
        }
        user_id = 'test_user'

        # Act
        result = portfolio_agent.handle_portfolio_request(data, user_id)

        # Assert
        self.assertEqual(result, {'error': 'API Error'})
        mock_log_audit.assert_called_once_with(user_id, 'portfolio_task', {'error': 'API Error'})

if __name__ == '__main__':
    unittest.main()
