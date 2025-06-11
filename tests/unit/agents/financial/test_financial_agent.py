import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.financial.financial_agent import handle_request

class TestFinancialAgent(unittest.TestCase):

    def setUp(self):
        self.user_id = 'test_user'

    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    @patch('src.agents.financial.financial_agent.time')
    def test_create_retirement_plan_success(self, mock_time, mock_store_shared_data, mock_log_audit):
        data = {'task': 'create_retirement_plan', 'age': 30, 'retirement_age': 65, 'annual_income': 60000, 'savings_rate': 0.1, 'expected_return': 0.07}
        mock_time.time.return_value = 1234567890
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertAlmostEqual(result['result']['retirement_savings'], 829421.27, places=2)
        mock_store_shared_data.assert_called_once()
        mock_log_audit.assert_called_once()

    def test_create_retirement_plan_invalid_input(self):
        data = {'task': 'create_retirement_plan', 'age': -30}
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['result'], 'Invalid input parameters')

    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    def test_investment_strategy_success(self, mock_store_shared_data, mock_log_audit):
        data = {'task': 'investment_strategy', 'risk_tolerance': 'aggressive', 'investment_horizon': 20}
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result']['allocation']['stocks'], 80)
        mock_store_shared_data.assert_called_once()
        mock_log_audit.assert_called_once()

    def test_investment_strategy_invalid_horizon(self):
        data = {'task': 'investment_strategy', 'investment_horizon': -5}
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['result'], 'Investment horizon must be positive')

    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    @patch('src.agents.financial.financial_agent.supabase')
    @patch('src.agents.financial.financial_agent.time')
    def test_create_budget_success(self, mock_time, mock_supabase, mock_store_shared_data, mock_log_audit):
        mock_time.strftime.return_value = '2023-01-01T12:00:00Z'
        data = {'task': 'create_budget', 'income': 5000, 'expenses': [{'amount': 1000}, {'amount': 500}]}
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result']['savings'], 3500)
        mock_supabase.table.return_value.insert.assert_called_once()
        mock_store_shared_data.assert_called_once()
        mock_log_audit.assert_called_once()

    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    @patch('src.agents.financial.financial_agent.supabase')
    @patch('src.agents.financial.financial_agent.time')
    def test_track_expense_success(self, mock_time, mock_supabase, mock_store_shared_data, mock_log_audit):
        mock_time.strftime.return_value = '2023-01-01T12:00:00Z'
        data = {'task': 'track_expense', 'expense': {'amount': 100, 'category': 'food'}}
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertTrue(result['result']['tracked'])
        mock_supabase.table.return_value.insert.assert_called_once()
        mock_store_shared_data.assert_called_once()
        mock_log_audit.assert_called_once()

    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    @patch('src.agents.financial.financial_agent.supabase')
    def test_list_expenses(self, mock_supabase, mock_store_shared_data, mock_log_audit):
        data = {'task': 'list_expenses'}
        mock_expenses = [{'amount': 100}, {'amount': 200}]
        mock_supabase_response = MagicMock()
        mock_supabase_response.data = mock_expenses
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_supabase_response
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result'], mock_expenses)
        mock_supabase.table.assert_called_once_with('expenses')
        mock_store_shared_data.assert_called_once()
        mock_log_audit.assert_called_once()

    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    @patch('src.agents.financial.financial_agent.supabase')
    def test_expense_summary(self, mock_supabase, mock_store_shared_data, mock_log_audit):
        data = {'task': 'expense_summary', 'category': 'food'}
        mock_expenses = [{'amount': 50}, {'amount': 75}]
        mock_supabase_response = MagicMock()
        mock_supabase_response.data = mock_expenses
        mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_supabase_response
        result = handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result']['total'], 125)
        self.assertEqual(result['result']['category'], 'food')
        mock_supabase.table.assert_called_once_with('expenses')
        mock_store_shared_data.assert_called_once()
        mock_log_audit.assert_called_once()

if __name__ == '__main__':
    unittest.main()

    @patch('src.agents.financial.financial_agent.supabase')
    @patch('src.agents.financial.financial_agent.time')
    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    def test_list_expenses_success(self, mock_store, mock_log, mock_time, mock_supabase):
        mock_execute = MagicMock()
        mock_execute.data = [{'id': 1, 'amount': 100}]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_execute
        data = {'task': 'list_expenses'}
        result = financial_agent.handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['result']), 1)
        self.assertEqual(result['result'][0]['amount'], 100)

    @patch('src.agents.financial.financial_agent.supabase')
    @patch('src.agents.financial.financial_agent.time')
    @patch('src.agents.financial.financial_agent.log_audit')
    @patch('src.agents.financial.financial_agent.store_shared_data')
    def test_expense_summary_success(self, mock_store, mock_log, mock_time, mock_supabase):
        mock_execute = MagicMock()
        mock_execute.data = [{'amount': 100}, {'amount': 150}]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_execute
        data = {'task': 'expense_summary'}
        result = financial_agent.handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result']['total'], 250)

    @patch('src.agents.financial.financial_agent.store_shared_data')
    @patch('src.agents.financial.financial_agent.log_audit')
    def test_general_exception(self, mock_log, mock_store):
        data = {'task': 'create_retirement_plan', 'annual_income': None}
        # Missing required data will cause a TypeError
        result = financial_agent.handle_request(data, self.user_id)
        self.assertEqual(result['status'], 'error')
        self.assertIn("'<' not supported between instances of 'NoneType' and 'int'", result['result'])
        mock_log.assert_called_once()

if __name__ == '__main__':
    unittest.main()
