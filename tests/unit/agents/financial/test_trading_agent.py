import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.agents.financial import trading_agent

class TestTradingAgent(unittest.TestCase):

    def setUp(self):
        self.user_id = 'test_user'
        self.api_data = {
            'api_key': 'test_key',
            'api_secret': 'test_secret'
        }

    @patch('src.agents.financial.trading_agent.add_all_ta_features')
    @patch('src.agents.financial.trading_agent.ccxt.coinbase')
    @patch('src.agents.financial.trading_agent.log_audit')
    def test_fetch_data_success(self, mock_log_audit, mock_coinbase, mock_add_ta):
        """
        Test that handle_trade_request successfully fetches and processes market data.
        """
        # Arrange
        mock_exchange = MagicMock()
        mock_coinbase.return_value = mock_exchange
        sample_ohlcv = [[1609459200000, 40000, 41000, 39000, 40500, 100]]
        mock_exchange.fetch_ohlcv.return_value = sample_ohlcv

        mock_df = pd.DataFrame(sample_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        mock_add_ta.return_value = mock_df # Simulate returning the dataframe with TA features

        data = {'task': 'fetch_data', 'symbol': 'BTC/USD', **self.api_data}

        # Act
        result = trading_agent.handle_trade_request(data, self.user_id)

        # Assert
        mock_coinbase.assert_called_once_with({'apiKey': 'test_key', 'secret': 'test_secret'})
        mock_exchange.fetch_ohlcv.assert_called_once_with('BTC/USD', '1d', limit=100)
        mock_add_ta.assert_called_once()
        self.assertEqual(result['data'], sample_ohlcv)
        self.assertIn('patterns', result)
        mock_log_audit.assert_called_once_with(self.user_id, 'trade_task', {'task': 'fetch_data'})

    @patch('src.agents.financial.trading_agent.ccxt.coinbase')
    @patch('src.agents.financial.trading_agent.log_audit')
    def test_execute_trade_success(self, mock_log_audit, mock_coinbase):
        """
        Test that handle_trade_request successfully executes a trade.
        """
        # Arrange
        mock_exchange = MagicMock()
        mock_coinbase.return_value = mock_exchange
        mock_order = {'id': '123', 'status': 'open'}
        mock_exchange.create_order.return_value = mock_order

        data = {
            'task': 'execute_trade',
            'symbol': 'BTC/USD',
            'type': 'limit',
            'side': 'buy',
            'amount': 1,
            'price': 40000,
            **self.api_data
        }

        # Act
        result = trading_agent.handle_trade_request(data, self.user_id)

        # Assert
        mock_exchange.create_order.assert_called_once_with(
            symbol='BTC/USD', type='limit', side='buy', amount=1, price=40000
        )
        self.assertEqual(result, {'order': mock_order})
        mock_log_audit.assert_called_once_with(self.user_id, 'trade_task', {'task': 'execute_trade'})

    @patch('src.agents.financial.trading_agent.log_audit')
    def test_unknown_task(self, mock_log_audit):
        """
        Test that handle_trade_request handles an unknown task.
        """
        # Arrange
        data = {'task': 'unknown'}

        # Act
        result = trading_agent.handle_trade_request(data, self.user_id)

        # Assert
        self.assertEqual(result, {'status': 'success'})
        mock_log_audit.assert_called_once_with(self.user_id, 'trade_task', {'task': 'unknown'})

    @patch('src.agents.financial.trading_agent.ccxt.coinbase')
    @patch('src.agents.financial.trading_agent.log_audit')
    def test_api_exception(self, mock_log_audit, mock_coinbase):
        """
        Test that handle_trade_request handles API exceptions.
        """
        # Arrange
        mock_coinbase.side_effect = Exception("API Error")
        data = {'task': 'fetch_data', **self.api_data}

        # Act
        result = trading_agent.handle_trade_request(data, self.user_id)

        # Assert
        self.assertEqual(result, {'error': 'API Error'})
        mock_log_audit.assert_called_once_with(self.user_id, 'trade_task', {'error': 'API Error'})

if __name__ == '__main__':
    unittest.main()
