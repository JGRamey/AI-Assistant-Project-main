import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.agents.financial import expense_report

class TestExpenseReport(unittest.TestCase):

    @patch('src.agents.financial.expense_report.supabase')
    @patch('src.agents.financial.expense_report.store_shared_data')
    @patch('src.agents.financial.expense_report.log_audit')
    def test_generate_report(self, mock_log_audit, mock_store_shared_data, mock_supabase):
        """Test that the expense report is generated correctly."""
        # Arrange: Mock the data returned from Supabase
        mock_expense_data = [
            {'category': 'Food', 'amount': 50},
            {'category': 'Transport', 'amount': 30},
            {'category': 'Food', 'amount': 25},
            {'category': 'Utilities', 'amount': 100},
            {'category': 'Transport', 'amount': 20},
        ]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = mock_expense_data

        user_id = 'test_user_123'
        data = {'task_id': 'test_task_456'}

        # Act: Call the function to be tested
        result = expense_report.generate_report(data, user_id)

        # Assert: Check that the summary is calculated correctly
        expected_summary = {
            'Food': 75,
            'Transport': 50,
            'Utilities': 100
        }
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['result'], expected_summary)

        # Assert: Check that the helper functions were called correctly
        mock_store_shared_data.assert_called_once_with('report_test_task_456', expected_summary, user_id)
        mock_log_audit.assert_called_once_with(user_id, 'expense_report', expected_summary)

if __name__ == '__main__':
    unittest.main()
