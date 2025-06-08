import os
import sys
import json
from unittest.mock import patch, MagicMock
import requests_mock
import traceback

# Add src to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import components to test
from Lambda.lambda_function import lambda_handler
from agents.coding_agent import handle_code_request
from agents.Financial_Agent import handle_request as financial_agent_handle
from agents.smart_contract_ai_agent import handle_smart_contract_request
from platform.content.script_generator import handle_script_request
from platform.finances.revenue import handle_revenue_request
from Blockchain.SmartContractManager import SmartContractManager
from utils import store_shared_data, get_shared_data

# Test results collector
test_results = []

def print_results():
    print("\n=== Keyless Test Results ===")
    for result in test_results:
        status = "PASS" if result['passed'] else "FAIL"
        print(f"Test: {result['test_name']} - Status: {status}")
        if not result['passed']:
            print(f"Issue: {result['error']}")
        print("-" * 50)
    passed = sum(1 for r in test_results if r['passed'])
    total = len(test_results)
    print(f"\nSummary: {passed}/{total} tests passed")
    if passed < total:
        print("Action: Review failed tests above and check code for issues (e.g., missing imports, syntax errors, or logic flaws).")

def run_test(test_name, test_func, *args, **kwargs):
    try:
        result = test_func(*args, **kwargs)
        test_results.append({'test_name': test_name, 'passed': True})
        return result
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        test_results.append({'test_name': test_name, 'passed': False, 'error': error_msg})
        return None

# Mock environment variables
@patch.dict(os.environ, {
    'SUPABASE_URL': 'https://mock.supabase.co',
    'SUPABASE_KEY': 'mock-key',
    'STRIPE_API_KEY': 'sk_test_mock',
    'ETH_RPC_URL': 'https://mock.eth',
    'ETH_PRIVATE_KEY': 'mock-private-key',
    'CHAIN_ID': '11155111',
    'SQS_QUEUE_URL': 'https://mock.sqs',
    'AWS_ACCESS_KEY_ID': 'mock-access-key',
    'AWS_SECRET_ACCESS_KEY': 'mock-secret-key',
    'YOUTUBE_API_KEY': 'mock-youtube-key'
})
# Mock external services
def run_tests():
    with requests_mock.Mocker() as m, \
         patch('utils.create_client') as mock_supabase, \
         patch('utils.boto3.client') as mock_sqs, \
         patch('utils.boto3.resource') as mock_dynamodb, \
         patch('Blockchain.SmartContractManager.Web3') as mock_web3:

        # Configure Supabase mock
        mock_supabase_instance = MagicMock()
        mock_supabase.return_value = mock_supabase_instance
        mock_supabase_instance.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{'id': 1}])
        mock_supabase_instance.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{'id': 1, 'content': '{"mock": "data"}'}])
        mock_supabase_instance.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(data={'id': 1, 'content': '{"mock": "data"}'})

        # Configure Stripe mock
        m.get('https://api.stripe.com/v1/charges', json={'data': [{'id': 'ch_1', 'amount': 10000}]})

        # Configure Web3 mock
        mock_web3_instance = MagicMock()
        mock_web3.return_value = mock_web3_instance
        mock_web3_instance.is_connected.return_value = True
        mock_web3_instance.eth.account.from_key.return_value = MagicMock(address='0xMockAddress')
        mock_web3_instance.eth.get_transaction_count.return_value = 1
        mock_web3_instance.eth.contract.return_value.constructor.return_value.estimate_gas.return_value = 100000
        mock_web3_instance.eth.contract.return_value.constructor.return_value.build_transaction.return_value = {'mock': 'tx'}
        mock_web3_instance.eth.account.sign_transaction.return_value = MagicMock(rawTransaction='mock-tx')
        mock_web3_instance.eth.send_raw_transaction.return_value = 'mock-tx-hash'
        mock_web3_instance.eth.wait_for_transaction_receipt.return_value = MagicMock(status=1, contractAddress='0xContractAddress')
        mock_web3_instance.eth.contract.return_value.functions.createTask.return_value.estimate_gas.return_value = 50000
        mock_web3_instance.eth.contract.return_value.functions.createTask.return_value.build_transaction.return_value = {'mock': 'tx'}

        # Configure SQS mock
        mock_sqs_instance = MagicMock()
        mock_sqs.return_value = mock_sqs_instance

        # Configure DynamoDB mock
        mock_dynamodb_instance = MagicMock()
        mock_dynamodb.return_value = mock_dynamodb_instance
        mock_dynamodb_instance.Table.return_value.put_item.return_value = {}
        mock_dynamodb_instance.Table.return_value.get_item.return_value = {'Item': {'key': 'mock:key', 'value': '{"mock": "data"}'}}

        # Test Lambda Handler
        def test_lambda_handler():
            event = {
                'agent': 'coding_agent',
                'data': {'task': 'generate_python', 'spec': 'test'},
                'user_id': 'test_user'
            }
            context = MagicMock()
            result = lambda_handler(event, context)
            assert result['status'] == 'success', "Lambda handler failed to route to coding agent"
            return result

        run_test('test_lambda_handler', test_lambda_handler)

        # Test Coding Agent
        def test_coding_agent():
            result = handle_code_request({'task': 'generate_python', 'spec': 'print("Hello")'}, 'test_user')
            assert result['status'] == 'success', "Coding agent failed to generate code"
            assert 'code' in result['result'], "No code in coding agent response"
            return result

        run_test('test_coding_agent', test_coding_agent)

        # Test Financial Agent
        def test_financial_agent():
            result = financial_agent_handle({'task': 'create_retirement_plan', 'age': 30}, 'test_user')
            assert result['status'] == 'success', "Financial agent failed to create retirement plan"
            return result

        run_test('test_financial_agent', test_financial_agent)

        # Test Smart Contract AI Agent
        def test_smart_contract_ai_agent():
            result = handle_smart_contract_request({'task': 'deploy_contract', 'contract_name': 'Test'}, 'test_user')
            assert result['status'] == 'success', "Smart contract AI agent failed to deploy contract"
            return result

        run_test('test_smart_contract_ai_agent', test_smart_contract_ai_agent)

        # Test Script Generator
        def test_script_generator():
            result = handle_script_request({'task': 'generate_script', 'keywords': 'blockchain', 'style': 'informal'}, 'test_user')
            assert result['status'] == 'success', "Script generator failed to create script"
            assert 'result' in result, 'result'['script'] in result['result'], "No script in generator response"
            return result

        run_test('test_script_generator', test_script_generator)

        # Test Revenue Module
        def test_revenue():
            result = handle_revenue_request({'task': 'fetch_youtube_revenue'}, 'test_user')
            assert result['status'] == 'success', "Revenue module failed to fetch YouTube revenue"
            return result

        run_test('test_revenue', test_revenue)

        # Test Smart Contract Manager
        def test_smart_contract_manager():
            manager = SmartContractManager()
            result = manager.deploy_contract('TestContract', [], 'mock-abi', 'mock-bytecode')
            assert result is not None, "SmartContractManager failed to deploy contract"
            return result

        run_test('test_smart_contract_manager', test_smart_contract_manager)

if __name__ == '__main__':
    run_tests()
    print_results()