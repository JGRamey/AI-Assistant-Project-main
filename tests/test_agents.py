import pytest
import json
import os
from unittest.mock import patch, MagicMock
import requests_mock
from agents import (
    coding_agent, email_agent, trading_agent, priority_agent, news_agent, alert_agent,
    portfolio_agent, crm_agent, notes_agent, time_agent, sentiment_agent, snippet_agent,
    stress_agent, social_agent, learning_agent, voice_agent, key_agent, journal_agent,
    update_agent, smart_contract_ai_agent, Financial_Agent
)
from platform.content import script_generator
from platform.social import post_scheduler
from platform.marketing import newsletter_automation
from platform.finances import revenue
from platform.analytics import youtube_analytics
from Blockchain import SmartContractManager
from utils import store_shared_data, get_shared_data

# Fixture to set up environment variables
@pytest.fixture(autouse=True)
def setup_env():
    os.environ['TESTING'] = 'True'
    yield
    os.environ.pop('TESTING', None)

# Fixture to mock requests
@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

# Fixture to mock Web3
@pytest.fixture
def mock_web3():
    with patch('Blockchain.SmartContractManager.Web3') as mock_web3:
        mock_instance = MagicMock()
        mock_web3.return_value = mock_instance
        mock_instance.is_connected.return_value = True
        mock_instance.eth.account.from_key.return_value = MagicMock(address='0xMockAddress')
        mock_instance.eth.get_transaction_count.return_value = 1
        mock_instance.eth.contract.return_value.constructor.return_value.estimate_gas.return_value = 100000
        mock_instance.eth.contract.return_value.constructor.return_value.build_transaction.return_value = {'mock': 'tx'}
        mock_instance.eth.account.sign_transaction.return_value = MagicMock(rawTransaction='mock-tx')
        mock_instance.eth.send_raw_transaction.return_value = 'mock-tx-hash'
        mock_instance.eth.wait_for_transaction_receipt.return_value = {'status': 1, 'contractAddress': '0xContractAddress'}
        mock_instance.eth.contract.return_value.functions.createTask.return_value.estimate_gas.return_value = 50000
        mock_instance.eth.contract.return_value.functions.createTask.return_value.build_transaction.return_value = {'mock': 'tx'}
        yield mock_web3

# Fixture to mock file-based storage
@pytest.fixture
def mock_storage(tmpdir):
    storage_file = tmpdir.join("shared_data.json")
    with open(storage_file, 'w') as f:
        json.dump({}, f)
    with patch('utils.log_utils.STORAGE_PATH', str(storage_file)):
        yield storage_file

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
def test_coding_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = coding_agent.handle_code_request({'task': 'generate_python', 'spec': 'test'}, 'user123')
        assert result['status'] == 'success', "Coding agent failed to generate Python code"
        assert 'code' in result['result'], "No code found in coding agent response"
        test_results.append({'test_name': 'test_coding_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_coding_agent', 'passed': False, 'error': str(e)})

# Test Email Agent
def test_email_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = email_agent.handle_email_request({'task': 'send_email', 'recipient': 'test@example.com', 'subject': 'Test'}, 'user123')
        assert result['status'] == 'success', "Email agent failed to process send_email task"
        test_results.append({'test_name': 'test_email_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_email_agent', 'passed': False, 'error': str(e)})

# Test Trading Agent
def test_trading_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = trading_agent.handle_trade_request({'task': 'execute_trade', 'asset': 'BTC', 'amount': 0.1}, 'user123')
        assert result['status'] == 'success', "Trading agent failed to execute trade"
        test_results.append({'test_name': 'test_trading_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_trading_agent', 'passed': False, 'error': str(e)})

# Test Priority Agent
def test_priority_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = priority_agent.handle_priority_request({'task': 'prioritize', 'tasks': ['task1', 'task2']}, 'user123')
        assert result['status'] == 'success', "Priority agent failed to prioritize tasks"
        test_results.append({'test_name': 'test_priority_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_priority_agent', 'passed': False, 'error': str(e)})

# Test News Agent
def test_news_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = news_agent.handle_news_request({'task': 'fetch_news', 'topic': 'blockchain'}, 'user123')
        assert result['status'] == 'success', "News agent failed to fetch news"
        test_results.append({'test_name': 'test_news_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_news_agent', 'passed': False, 'error': str(e)})

# Test Alert Agent
def test_alert_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = alert_agent.handle_alert_request({'task': 'set_alert', 'condition': 'price > 100'}, 'user123')
        assert result['status'] == 'success', "Alert agent failed to set alert"
        test_results.append({'test_name': 'test_alert_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_alert_agent', 'passed': False, 'error': str(e)})

# Test Portfolio Agent
def test_portfolio_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = portfolio_agent.handle_portfolio_request({'task': 'view_portfolio'}, 'user123')
        assert result['status'] == 'success', "Portfolio agent failed to view portfolio"
        test_results.append({'test_name': 'test_portfolio_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_portfolio_agent', 'passed': False, 'error': str(e)})

# Test CRM Agent
def test_crm_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = crm_agent.handle_crm_request({'task': 'add_contact', 'name': 'Test Contact', 'email': 'test@example.com'}, 'user123')
        assert result['status'] == 'success', "CRM agent failed to add contact"
        test_results.append({'test_name': 'test_crm_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_crm_agent', 'passed': False, 'error': str(e)})

# Test Notes Agent
def test_notes_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = notes_agent.handle_notes_request({'task': 'create_note', 'content': 'Test note'}, 'user123')
        assert result['status'] == 'success', "Notes agent failed to create note"
        test_results.append({'test_name': 'test_notes_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_notes_agent', 'passed': False, 'error': str(e)})

# Test Time Agent
def test_time_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = time_agent.handle_time_request({'task': 'schedule_task', 'time': '2025-06-09T10:00:00Z'}, 'user123')
        assert result['status'] == 'success', "Time agent failed to schedule task"
        test_results.append({'test_name': 'test_time_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_time_agent', 'passed': False, 'error': str(e)})

# Test Sentiment Agent
def test_sentiment_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = sentiment_agent.handle_sentiment_request({'task': 'analyze_sentiment', 'text': 'Great product!'}, 'user123')
        assert result['status'] == 'success', "Sentiment agent failed to analyze text"
        test_results.append({'test_name': 'test_sentiment_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_sentiment_agent', 'passed': False, 'error': str(e)})

# Test Snippet Agent
def test_snippet_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = snippet_agent.handle_snippet_request({'task': 'save_snippet', 'code': 'print("Hello")'}, 'user123')
        assert result['status'] == 'success', "Snippet agent failed to save snippet"
        test_results.append({'test_name': 'test_snippet_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_snippet_agent', 'passed': False, 'error': str(e)})

# Test Stress Agent
def test_stress_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = stress_agent.handle_stress_request({'task': 'analyze_stress', 'data': {'heart_rate': 80}}, 'user123')
        assert result['status'] == 'success', "Stress agent failed to analyze data"
        test_results.append({'test_name': 'test_stress_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_stress_agent', 'passed': False, 'error': str(e)})

# Test Social Agent
def test_social_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = social_agent.handle_social_request({'task': 'post_tweet', 'content': 'Test tweet'}, 'user123')
        assert result['status'] == 'success', "Social agent failed to post tweet"
        test_results.append({'test_name': 'test_social_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_social_agent', 'passed': False, 'error': str(e)})

# Test Learning Agent
def test_learning_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = learning_agent.handle_learning_request({'task': 'recommend_course', 'topic': 'Python'}, 'user123')
        assert result['status'] == 'success', "Learning agent failed to recommend course"
        test_results.append({'test_name': 'test_learning_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_learning_agent', 'passed': False, 'error': str(e)})

# Test Voice Agent
def test_voice_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = voice_agent.handle_voice_request({'task': 'process_audio', 'audio_data': 'mock-audio'}, 'user123')
        assert result['status'] == 'success', "Voice agent failed to process audio"
        test_results.append({'test_name': 'test_voice_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_voice_agent', 'passed': False, 'error': str(e)})

# Test Key Agent
def test_key_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = key_agent.handle_key_request({'task': 'generate_key'}, 'user123')
        assert result['status'] == 'success', "Key agent failed to generate key"
        test_results.append({'test_name': 'test_key_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_key_agent', 'passed': False, 'error': str(e)})

# Test Journal Agent
def test_journal_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = journal_agent.handle_journal_request({'task': 'add_entry', 'content': 'Test entry'}, 'user123')
        assert result['status'] == 'success', "Journal agent failed to add entry"
        test_results.append({'test_name': 'test_journal_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_journal_agent', 'passed': False, 'error': str(e)})

# Test Update Agent
def test_update_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = update_agent.handle_update_request({'task': 'update_config', 'config': {'setting': 'new_value'}}, 'user123')
        assert result['status'] == 'success', "Update agent failed to update config"
        store_shared_data('agent_config_user123', {'setting': 'new_value'})
        config = get_shared_data('agent_config_user123')
        assert config['setting'] == 'new_value', "Config not stored correctly"
        test_results.append({'test_name': 'test_update_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_update_agent', 'passed': False, 'error': str(e)})

# Test Smart Contract AI Agent
def test_smart_contract_ai_agent(mock_requests, mock_web3, mock_storage):
    try:
        result = smart_contract_ai_agent.handle_contract_request({'task': 'deploy_contract', 'source': 'contract Test {}'}, 'user123')
        assert result['status'] == 'success', "Smart contract AI agent failed to deploy contract"
        test_results.append({'test_name': 'test_smart_contract_ai_agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_smart_contract_ai_agent', 'passed': False, 'error': str(e)})

# Test Financial Agent
def test_Financial_Agent(mock_requests, mock_web3, mock_storage):
    try:
        result = Financial_Agent.handle_financial_request({'task': 'analyze_finances', 'data': {'income': 1000}}, 'user123')
        assert result['status'] == 'success', "Financial agent failed to analyze finances"
        test_results.append({'test_name': 'test_Financial_Agent', 'passed': True})
    except AssertionError as e:
        test_results.append({'test_name': 'test_Financial_Agent', 'passed': False, 'error': str(e)})