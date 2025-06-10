import pytest
from unittest.mock import patch, MagicMock
from agents import priority_agent, news_agent, alert_agent, crm_agent
from agents.coding import coding_agent
from agents.communication import email_agent
from agents.financial import trading_agent
from agents.financial.expense_report import generate_report

@patch('agents.coding.coding_agent.log_audit')
@patch('agents.coding.coding_agent.send_message')
@patch('agents.coding.coding_agent.store_shared_data')
def test_coding_agent_handle_code_request(
    mock_store_shared_data: MagicMock,
    mock_send_message: MagicMock,
    mock_log_audit: MagicMock,
) -> None:
    """Test the handle_code_request function of the coding agent for code generation."""

    # Arrange
    user_id = "user123"
    task_data = {
        'task': 'generate_python',
        'spec': 'a simple function'
    }

    # Act
    result = coding_agent.handle_code_request(task_data, user_id)

    # Assert
    assert result['status'] == 'success'
    assert 'def main():' in result['result']['code']
    mock_store_shared_data.assert_called()
    mock_send_message.assert_called_once()
    mock_log_audit.assert_called_once()

@patch('agents.communication.email_agent.build')
@patch('agents.communication.email_agent.log_audit')
def test_email_agent_handle_email_request(
    mock_log_audit: MagicMock,
    mock_build: MagicMock,
) -> None:
    """Test the handle_email_request function of the email agent."""

    # Arrange
    user_id = "user456"
    mock_service = MagicMock()
    mock_build.return_value = mock_service

    # Test sending an email
    send_data = {
        'task': 'send',
        'to': 'test@example.com',
        'subject': 'Hello',
        'body': 'This is a test.',
        'credentials': MagicMock()  # Mock credentials
    }

    # Act
    result_send = email_agent.handle_email_request(send_data, user_id)

    # Assert
    assert result_send['status'] == 'sent'
    mock_service.users().messages().send.assert_called_once()
    mock_log_audit.assert_called_with(user_id, 'email_task', {'task': 'send'})

@patch('agents.financial.trading_agent.ccxt.coinbase')
@patch('agents.financial.trading_agent.log_audit')
def test_trading_agent_handle_trade_request(
    mock_log_audit: MagicMock,
    mock_coinbase: MagicMock,
) -> None:
    """Test the handle_trade_request function of the trading agent."""

    # Arrange
    user_id = "user789"
    mock_exchange = MagicMock()
    mock_coinbase.return_value = mock_exchange
    mock_exchange.create_order.return_value = {
        'id': '12345',
        'status': 'open'
    }

    trade_data = {
        'task': 'execute_trade',
        'symbol': 'BTC/USD',
        'type': 'limit',
        'side': 'buy',
        'amount': 1,
        'price': 50000,
        'api_key': 'test_key',
        'api_secret': 'test_secret'
    }

    # Act
    result = trading_agent.handle_trade_request(trade_data, user_id)

    # Assert
    assert result['order']['id'] == '12345'
    mock_coinbase.assert_called_once_with({
        'apiKey': 'test_key',
        'secret': 'test_secret'
    })
    mock_exchange.create_order.assert_called_once_with(
        symbol='BTC/USD',
        type='limit',
        side='buy',
        amount=1,
        price=50000
    )
    mock_log_audit.assert_called_with(user_id, 'trade_task', {
        'task': 'execute_trade'
    })

@patch('agents.priority_agent.googleapiclient.discovery.build')
@patch('agents.priority_agent.log_audit')
def test_priority_agent_handle_priority_request(
    mock_log_audit: MagicMock,
    mock_build: MagicMock,
) -> None:
    """Test the handle_priority_request function of the priority agent."""
    # Arrange
    user_id = "user101"
    mock_service = MagicMock()
    mock_build.return_value = mock_service
    
    mock_events = {
        'items': [
            {'summary': 'Task 2', 'start': {'dateTime': '2025-01-01T10:00:00Z'}},
            {'summary': 'Task 1', 'start': {'dateTime': '2025-01-01T09:00:00Z'}},
            {'summary': 'Task 3', 'start': {'dateTime': '2025-01-01T11:00:00Z'}},
        ]
    }
    mock_service.events().list().execute.return_value = mock_events

    priority_data = {
        'task': 'prioritize',
        'credentials': MagicMock()
    }

    # Act
    result = priority_agent.handle_priority_request(priority_data, user_id)

    # Assert
    assert len(result['tasks']) == 3
    assert result['tasks'][0]['summary'] == 'Task 1'
    assert result['tasks'][1]['summary'] == 'Task 2'
    assert result['tasks'][2]['summary'] == 'Task 3'
    mock_log_audit.assert_called_with(user_id, 'priority_task', {'task': 'prioritize'})

@patch('agents.news_agent.requests.get')
@patch('agents.news_agent.log_audit')
def test_news_agent_handle_news_request(
    mock_log_audit: MagicMock,
    mock_requests_get: MagicMock,
) -> None:
    """Test the handle_news_request function of the news agent."""
    # Arrange
    user_id = "user112"
    mock_response_news = MagicMock()
    mock_response_news.json.return_value = {
        'data': [
            {'title': 'Big Crypto News'},
            {'title': 'Some other news'},
            {'title': 'Another piece on crypto'}
        ]
    }
    mock_response_news.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response_news

    news_data = {'task': 'fetch_news'}

    # Act
    result_news = news_agent.handle_news_request(news_data, user_id)

    # Assert
    assert len(result_news['news']) == 2
    assert result_news['news'][0]['title'] == 'Big Crypto News'
    mock_requests_get.assert_called_with('https://api.coingecko.com/api/v3/news', timeout=10)
    mock_log_audit.assert_called_with(user_id, 'news_task', {'task': 'fetch_news'})

@patch('agents.alert_agent.boto3.client')
@patch('agents.alert_agent.log_audit')
def test_alert_agent_handle_alert_request(
    mock_log_audit: MagicMock,
    mock_boto3_client: MagicMock,
) -> None:
    """Test the handle_alert_request function of the alert agent."""
    # Arrange
    user_id = "user113"
    mock_sns_client = MagicMock()
    mock_boto3_client.return_value = mock_sns_client

    alert_data = {
        'task': 'set_alert',
        'topic_arn': 'arn:aws:sns:us-east-1:123456789012:MyTopic',
        'message': 'Price of BTC has reached $55,000'
    }

    # Act
    result = alert_agent.handle_alert_request(alert_data, user_id)

    # Assert
    assert result['status'] == 'alert_sent'
    mock_boto3_client.assert_called_once_with('sns')
    mock_sns_client.publish.assert_called_once_with(
        TopicArn='arn:aws:sns:us-east-1:123456789012:MyTopic',
        Message='Trade Alert: Price of BTC has reached $55,000'
    )

@patch('agents.crm_agent.supabase')
@patch('agents.crm_agent.log_audit')
@patch('agents.crm_agent.send_message')
@patch('agents.crm_agent.store_shared_data')
def test_crm_agent_handle_crm_request(
    mock_store_shared_data: MagicMock,
    mock_send_message: MagicMock,
    mock_log_audit: MagicMock,
    mock_supabase: MagicMock,
) -> None:
    """Test the handle_crm_request function of the crm agent."""
    # Arrange
    user_id = "user_crm_123"
    
    # Mock Supabase client
    mock_supabase_client = MagicMock()
    mock_supabase.table.return_value = mock_supabase_client

    # Test adding a contact
    add_contact_data = {
        'task': 'add_contact',
        'contact': {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '1234567890'}
    }
    mock_supabase_client.insert.return_value.execute.return_value = None

    # Act
    result_add = crm_agent.handle_crm_request(add_contact_data, user_id)

    # Assert
    assert result_add['status'] == 'success'
    assert result_add['result']['added'] is True
    mock_supabase.table.assert_called_with('crm_contacts')
    mock_supabase_client.insert.assert_called_once_with({
        'user_id': user_id,
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890'
    })
    mock_log_audit.assert_called()

@patch('agents.financial.expense_report.log_audit')
@patch('agents.financial.expense_report.store_shared_data')
@patch('agents.financial.expense_report.supabase')
def test_expense_report_generate_report(
    mock_log_audit: MagicMock,
    mock_store_shared_data: MagicMock,
    mock_supabase: MagicMock,
) -> None:
    """Test the generate_report function of the expense report agent."""
    # Arrange
    user_id: str = "user123"
    task_data: dict = {'task': 'generate_expense_report'}
    mock_expenses: list = [
        {'category': 'Food', 'amount': 100},
        {'category': 'Travel', 'amount': 250},
        {'category': 'Food', 'amount': 50},
    ]

    mock_supabase_response = MagicMock()
    mock_supabase_response.data = mock_expenses
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_supabase_response

    # Act
    result = generate_report(task_data, user_id)

    # Assert
    expected_summary = {'Food': 150, 'Travel': 250}
    assert result['status'] == 'success'
    assert result['result'] == expected_summary
    mock_store_shared_data.assert_called_once()
    mock_log_audit.assert_called_with(user_id, 'expense_report', expected_summary)