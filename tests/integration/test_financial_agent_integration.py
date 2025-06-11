import unittest
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.agents.financial.financial_agent import handle_request
from src.utils.helpers import supabase

class TestFinancialAgentIntegration(unittest.TestCase):

    def setUp(self):
        self.user_id = "integration_test_user"
        # Clean up previous test data
        supabase.table('expenses').delete().eq('user_id', self.user_id).execute()
        supabase.table('budgets').delete().eq('user_id', self.user_id).execute()

    def test_financial_agent_integration(self):
        # 1. Create a budget
        budget_data = {
            'task': 'create_budget',
            'income': 5000,
            'expenses': [
                {'category': 'rent', 'amount': 1500},
                {'category': 'utilities', 'amount': 200}
            ]
        }
        budget_result = handle_request(budget_data, self.user_id)
        self.assertEqual(budget_result['status'], 'success')
        self.assertEqual(budget_result['result']['savings'], 3300)

        # 2. Track expenses
        expense1_data = {'task': 'track_expense', 'expense': {'amount': 50, 'category': 'groceries'}}
        expense2_data = {'task': 'track_expense', 'expense': {'amount': 75, 'category': 'transport'}}
        handle_request(expense1_data, self.user_id)
        handle_request(expense2_data, self.user_id)

        # 3. List expenses
        list_data = {'task': 'list_expenses'}
        list_result = handle_request(list_data, self.user_id)
        self.assertEqual(list_result['status'], 'success')
        self.assertEqual(len(list_result['result']), 2)

        # 4. Get expense summary
        summary_data = {'task': 'expense_summary'}
        summary_result = handle_request(summary_data, self.user_id)
        self.assertEqual(summary_result['status'], 'success')
        self.assertEqual(summary_result['result']['total'], 125)

if __name__ == '__main__':
    unittest.main()
