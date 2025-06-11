import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from src.agents.financial.expense_report import generate_report

class TestExpenseReport(unittest.TestCase):

    @patch('src.agents.financial.expense_report.log_audit')
    @patch('src.agents.financial.expense_report.store_shared_data')
    @patch('src.agents.financial.expense_report.supabase')
    def test_generate_report(self, mock_supabase, mock_store_shared_data, mock_log_audit):
        # Arrange
        user_id = "test_user_123"
        data = {'task_id': 'test_task_456'}
        
        mock_expenses_data = [
            {'user_id': user_id, 'category': 'Food', 'amount': 75.50},
            {'user_id': user_id, 'category': 'Transport', 'amount': 120.00},
            {'user_id': user_id, 'category': 'Food', 'amount': 25.00},
            {'user_id': user_id, 'category': 'Utilities', 'amount': 150.25},
            {'user_id': user_id, 'category': 'Transport', 'amount': 30.50},
        ]

        mock_supabase_response = MagicMock()
        mock_supabase_response.data = mock_expenses_data
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_supabase_response

        # Act
        result = generate_report(data, user_id)

        # Assert
        expected_summary = {
            'Food': 100.50,
            'Transport': 150.50,
            'Utilities': 150.25
        }
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result'], expected_summary)
        self.assertEqual(result['task_id'], 'test_task_456')

        # Verify calls
        mock_supabase.table.assert_called_once_with('expenses')
        mock_supabase.table.return_value.select.assert_called_once_with('*')
        mock_supabase.table.return_value.select.return_value.eq.assert_called_once_with('user_id', user_id)
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.assert_called_once()

        mock_store_shared_data.assert_called_once_with('report_test_task_456', expected_summary, user_id)
        mock_log_audit.assert_called_once_with(user_id, 'expense_report', expected_summary)

if __name__ == '__main__':
    unittest.main()
