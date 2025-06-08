import pytest
import json
import os
import stripe
from unittest.mock import patch, MagicMock
import requests_mock
from src.agents import (
    coding_agent, email_agent, trading_agent, priority_agent, news_agent, alert_agent,
    portfolio_agent, crm_agent, notes_agent, time_agent, sentiment_agent, snippet_agent,
    stress_agent, social_agent, learning_agent, voice_agent, key_agent, journal_agent,
    update_agent, smart_contract_ai_agent, Financial_Agent
)
from src.platform.content import script_generator
from src.platform.social import post_scheduler
from src.platform.marketing import newsletter_automation
from src.platform.finances import revenue
from src.platform.analytics import youtube_analytics
from src.Blockchain import SmartContractManager
from src.utils import store_shared_data, get_shared_data

# Fixture to set up environment variables
@pytest.fixture(autouse=True)
def setup_env():
    os.environ['SUPABASE_URL'] = 'https://mock.supabase.co'
    os.environ['SUPABASE_KEY'] = 'mock-key'
    os.environ['STRIPE_API_KEY'] = 'sk_test_mock'
    os.environ['ETH_RPC_URL'] = 'https://mock.eth'
    os.environ['ETH_PRIVATE_KEY'] = 'mock-private-key'
    os.environ['CHAIN_ID'] = '11155111'
    os.environ['SQS_QUEUE_URL'] = 'https://mock.sqs'
    os.environ['AWS_ACCESS_KEY_ID'] = 'mock-access-key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'mock-secret-key'
    os.environ['YOUTUBE_API_KEY'] = 'mock-youtube-key'
    yield
    for key in ['SUPABASE_URL', 'SUPABASE_KEY', 'STRIPE_API_KEY', 'ETH_RPC_URL', 'ETH_PRIVATE_KEY', 'CHAIN_ID', 'SQS_QUEUE_URL', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'YOUTUBE_API_KEY']:
        os.environ.pop(key, None)

# Fixture to mock Supabase
@pytest.fixture
def mock_supabase():
    with patch('src.utils.create_client') as mock_client:
        mock_supabase = MagicMock()
        mock_client.return_value = mock_supabase
        mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{'id': 1}])
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{'id': 1, 'content': '{"mock": "data"}'}])
        mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MagicMock(data={'id': 1, 'content': '{"mock": "data"}'})
        yield mock_supabase

# Fixture to mock Stripe
@pytest.fixture
def mock_stripe():
    with requests_mock.Mocker() as m:
        m.get('https://api.stripe.com/v1/charges', json={'data': [{'id': 'ch_1', 'amount': 10000}]})
        yield m

# Fixture to mock Web3
@pytest.fixture
def mock_web3():
    with patch('src.Blockchain.SmartContractManager.Web3') as mock_web3:
        mock_instance = MagicMock()
        mock_web3.return_value = mock_instance
        mock_instance.is_connected.return_value = True
        mock_instance.eth.account.from_key.return_value = MagicMock(address='0xMockAddress')
        mock_instance.eth.get_transaction_count.return_value = 1
        mock_instance.eth.contract.return_value.constructor.return_value.estimate_gas.return_value = 100000
        mock_instance.eth.contract.return_value.constructor.return_value.build_transaction.return_value = {'mock': 'tx'}
        mock_instance.eth.account.sign_transaction.return_value = MagicMock(rawTransaction='mock-tx')
        mock_instance.eth.send_raw_transaction.return_value = 'mock-tx-hash'
        mock_instance.eth.wait_for_transaction_receipt.return_value = MagicMock(status=1, contractAddress='0xContractAddress')
        mock_instance.eth.contract.return_value.functions.createTask.return_value.estimate_gas.return_value = 50000
        mock_instance.eth.contract.return_value.functions.createTask.return_value.build_transaction.return_value = {'mock': 'tx'}
        yield mock_web3

# Fixture to mock SQS
@pytest.fixture
def mock_sqs():
    with patch('src.utils.boto3.client') as mock_boto:
        mock_sqs = MagicMock()
        mock_boto.return_value = mock_sqs
        yield mock_sqs

# Fixture to mock DynamoDB
@pytest.fixture
def mock_dynamodb():
    with patch('src.utils.boto3.resource') as mock_boto:
        mock_dynamodb = MagicMock()
        mock_boto.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value.put_item.return_value = {}
        mock_dynamodb.Table.return_value.get_item.return_value = {'Item': {'key': 'mock:key', 'value': '{"mock": "data"}'}}
        yield mock_dynamodb

# Test results collector
test_results = []

def pytest_terminal_summary(terminalreporter):
    terminalreporter.write("\n=== Test Results Summary ===\n")
    for result in test_results:
        status = "PASS" if result['passed'] else "FAIL"
        terminalreporter.write(f"Test: {result['test_name']} - Status: {status}\n")
        if not result['passed']:
            terminalreporter.write(f"Issue: {result['error']}\n")
        terminalreporter.write("-" * 50 + "\n")

# Test Coding Agent
def test_coding_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = coding_agent.handle_code_request({'task': 'generate_python', 'spec': 'test'}, 'user123')
        assert result['status'] == 'success', "Coding agent failed to generate Python code"
        assert 'code' in result['result'], "No code found in coding agent response"
        test_results.append({'test_name': 'test_coding_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_coding_agent', 'passed': False, 'error': str(e)})

# Test Email Agent (Mock implementation)
def test_email_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = email_agent.handle_email_request({'task': 'send_email', 'recipient': 'test@example.com', 'subject': 'Test'}, 'user123')
        assert result['status'] == 'success', "Email agent failed to process send_email task; check recipient or subject validation"
        test_results.append({'test_name': 'test_email_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_email_agent', 'passed': False, 'error': str(e)})

# Test Trading Agent (Mock implementation)
def test_trading_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = trading_agent.handle_trade_request({'task': 'execute_trade', 'asset': 'BTC', 'amount': 0.1}, 'user123')
        assert result['status'] == 'success', "Trading agent failed to execute trade; check asset or amount validation"
        test_results.append({'test_name': 'test_trading_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_trading_agent', 'passed': False, 'error': str(e)})

# Test Priority Agent (Mock implementation)
def test_priority_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = priority_agent.handle_priority_request({'task': 'prioritize', 'tasks': ['task1', 'task2']}, 'user123')
        assert result['status'] == 'success', "Priority agent failed to prioritize tasks; check task list format"
        test_results.append({'test_name': 'test_priority_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_priority_agent', 'passed': False, 'error': str(e)})

# Test News Agent (Mock implementation)
def test_news_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = news_agent.handle_news_request({'task': 'fetch_news', 'topic': 'blockchain'}, 'user123')
        assert result['status'] == 'success', "News agent failed to fetch news; check topic validation"
        test_results.append({'test_name': 'test_news_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_news_agent', 'passed': False, 'error': str(e)})

# Test Alert Agent (Mock implementation)
def test_alert_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = alert_agent.handle_alert_request({'task': 'set_alert', 'condition': 'price > 100'}, 'user123')
        assert result['status'] == 'success', "Alert agent failed to set alert; check condition format"
        test_results.append({'test_name': 'test_alert_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_alert_agent', 'passed': False, 'error': str(e)})

# Test Portfolio Agent (Mock implementation)
def test_portfolio_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = portfolio_agent.handle_portfolio_request({'task': 'view_portfolio'}, 'user123')
        assert result['status'] == 'success', "Portfolio agent failed to view portfolio; check data retrieval"
        test_results.append({'test_name': 'test_portfolio_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_portfolio_agent', 'passed': False, 'error': str(e)})

# Test CRM Agent (Mock implementation)
def test_crm_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = crm_agent.handle_crm_request({'task': 'add_contact', 'name': 'Test Contact', 'email': 'test@example.com'}, 'user123')
        assert result['status'] == 'success', "CRM agent failed to add contact; check name or email validation"
        test_results.append({'test_name': 'test_crm_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_crm_agent', 'passed': False, 'error': str(e)})

# Test Notes Agent (Mock implementation)
def test_notes_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = notes_agent.handle_notes_request({'task': 'create_note', 'content': 'Test note'}, 'user123')
        assert result['status'] == 'success', "Notes agent failed to create note; check content validation"
        test_results.append({'test_name': 'test_notes_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_notes_agent', 'passed': False, 'error': str(e)})

# Test Time Agent (Mock implementation)
def test_time_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = time_agent.handle_time_request({'task': 'schedule_task', 'time': '2025-06-09T10:00:00Z'}, 'user123')
        assert result['status'] == 'success', "Time agent failed to schedule task; check time format"
        test_results.append({'test_name': 'test_time_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_time_agent', 'passed': False, 'error': str(e)})

# Test Sentiment Agent (Mock implementation)
def test_sentiment_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = sentiment_agent.handle_sentiment_request({'task': 'analyze_sentiment', 'text': 'Great product!'}, 'user123')
        assert result['status'] == 'success', "Sentiment agent failed to analyze text; check text input"
        test_results.append({'test_name': 'test_sentiment_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_sentiment_agent', 'passed': False, 'error': str(e)})

# Test Snippet Agent (Mock implementation)
def test_snippet_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = snippet_agent.handle_snippet_request({'task': 'save_snippet', 'code': 'print("Hello")'}, 'user123')
        assert result['status'] == 'success', "Snippet agent failed to save snippet; check code input"
        test_results.append({'test_name': 'test_snippet_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_snippet_agent', 'passed': False, 'error': str(e)})

# Test Stress Agent (Mock implementation)
def test_stress_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = stress_agent.handle_stress_request({'task': 'analyze_stress', 'data': {'heart_rate': 80}}, 'user123')
        assert result['status'] == 'success', "Stress agent failed to analyze data; check data format"
        test_results.append({'test_name': 'test_stress_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_stress_agent', 'passed': False, 'error': str(e)})

# Test Social Agent (Mock implementation)
def test_social_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = social_agent.handle_social_request({'task': 'post_tweet', 'content': 'Test tweet'}, 'user123')
        assert result['status'] == 'success', "Social agent failed to post tweet; check content validation"
        test_results.append({'test_name': 'test_social_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_social_agent', 'passed': False, 'error': str(e)})

# Test Learning Agent (Mock implementation)
def test_learning_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = learning_agent.handle_learning_request({'task': 'recommend_course', 'topic': 'Python'}, 'user123')
        assert result['status'] == 'success', "Learning agent failed to recommend course; check topic input"
        test_results.append({'test_name': 'test_learning_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_learning_agent', 'passed': False, 'error': str(e)})

# Test Voice Agent (Mock implementation)
def test_voice_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = voice_agent.handle_voice_request({'task': 'process_audio', 'audio_data': 'mock-audio'}, 'user123')
        assert result['status'] == 'success', "Voice agent failed to process audio; check audio data"
        test_results.append({'test_name': 'test_voice_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_voice_agent', 'passed': False, 'error': str(e)})

# Test Key Agent (Mock implementation)
def test_key_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = key_agent.handle_key_request({'task': 'generate_key'}, 'user123')
        assert result['status'] == 'success', "Key agent failed to generate key"
        test_results.append({'test_name': 'test_key_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_key_agent', 'passed': False, 'error': str(e)})

# Test Journal Agent (Mock implementation)
def test_journal_agent(mock_supabase, mock_sqs, mock_dynamodb):
    try:
        result = journal_agent.handle_journal_request({'task': 'add_entry', 'content': 'Test entry'}, 'user123')
        assert result['status'] == 'success', "Journal agent failed to add entry; check content validation"
        test_results.append({'test_name': 'test_journal_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_journal_agent', 'passed': False, 'error': str(e)})

# Test Update Agent (Mock implementation)
def test_update_agent(mock_supabase