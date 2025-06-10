import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_handler import lambda_function

@pytest.fixture
def mock_dependencies():
    with patch('lambda_handler.lambda_function.get_handler') as mock_get_handler, \
         patch('lambda_handler.lambda_function.get_agent_handler') as mock_get_agent_handler, \
         patch('lambda_handler.lambda_function.log_audit') as mock_log_audit, \
         patch('lambda_handler.lambda_function.execute_workflow') as mock_workflow, \
         patch('lambda_handler.lambda_function.parse_task') as mock_parse_task:

        mock_coding_agent_handler = MagicMock()
        mock_email_agent_handler = MagicMock()

        def get_handler_side_effect(action):
            if action == 'email':
                return mock_email_agent_handler
            if action == 'invalid':
                return None
            return MagicMock()

        def get_agent_handler_side_effect(agent_name):
            if agent_name == 'coding_agent':
                return mock_coding_agent_handler
            return None

        mock_get_handler.side_effect = get_handler_side_effect
        mock_get_agent_handler.side_effect = get_agent_handler_side_effect

        yield {
            "log_audit": mock_log_audit,
            "workflow": mock_workflow,
            "parse_task": mock_parse_task,
            "coding_agent_handler": mock_coding_agent_handler,
            "email_agent_handler": mock_email_agent_handler
        }

def test_lambda_handler_delegate_agent(mock_dependencies):
    mock_parse_task = mock_dependencies['parse_task']
    mock_coding_agent_handler = mock_dependencies['coding_agent_handler']

    mock_parse_task.return_value = {
        'agent': 'coding_agent',
        'params': {'task': 'generate_python', 'spec': 'test'}
    }
    mock_coding_agent_handler.return_value = {
        'status': 'success',
        'result': {'code': 'print("Hello")'}
    }
    event = {
        'action': 'delegate',
        'body': json.dumps({'request': 'generate python code'}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}}
    }
    context = {}
    response = lambda_function.lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body == {'status': 'success', 'result': {'code': 'print("Hello")'}}
    mock_coding_agent_handler.assert_called_with(
        {'task': 'generate_python', 'spec': 'test'}, 'user123'
    )

def test_lambda_handler_specific_action(mock_dependencies):
    mock_email_agent_handler = mock_dependencies['email_agent_handler']
    mock_email_agent_handler.return_value = {'status': 'success', 'result': 'Email queued'}
    event = {
        'action': 'email',
        'body': json.dumps({'recipient': 'test@example.com', 'subject': 'Test'}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}}
    }
    context = {}
    response = lambda_function.lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body == {'status': 'success', 'result': 'Email queued'}
    mock_email_agent_handler.assert_called_with(
        {'recipient': 'test@example.com', 'subject': 'Test'}, 'user123'
    )

def test_lambda_handler_invalid_action(mock_dependencies):
    mock_log_audit = mock_dependencies['log_audit']
    event = {
        'action': 'invalid',
        'body': json.dumps({}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}}
    }
    context = {}
    response = lambda_function.lambda_handler(event, context)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body == {'error': 'Invalid action'}
    mock_log_audit.assert_called_with(
        'user123', 'invalid', {'error': 'Invalid action'}
    )