import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_handler import lambda_function

@pytest.fixture
def mock_dependencies():
    with patch('core_platform.agent_registry.get_handler') as mock_get_handler, \
         patch('core_platform.agent_registry.get_agent_module') as mock_get_agent_module, \
         patch('lambda_handler.lambda_function.log_audit') as mock_log_audit, \
         patch('lambda_handler.lambda_function.execute_workflow') as mock_workflow, \
         patch('lambda_handler.lambda_function.parse_task') as mock_parse_task:

        mock_coding_agent = MagicMock()
        mock_email_agent = MagicMock()

        def get_handler_side_effect(action):
            if action == 'email':
                return mock_email_agent.handle_request
            if action == 'invalid':
                return None
            return MagicMock()

        mock_get_handler.side_effect = get_handler_side_effect
        mock_get_agent_module.return_value = mock_coding_agent

        yield {
            "log_audit": mock_log_audit,
            "workflow": mock_workflow,
            "parse_task": mock_parse_task,
            "coding_agent": mock_coding_agent,
            "email_agent": mock_email_agent
        }

def test_lambda_handler_delegate_agent(mock_dependencies):
    mock_parse_task = mock_dependencies['parse_task']
    mock_coding_agent = mock_dependencies['coding_agent']

    mock_parse_task.return_value = {
        'agent': 'coding_agent',
        'params': {'task': 'generate_python', 'spec': 'test'}
    }
    mock_coding_agent.handle_request.return_value = {
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
    mock_coding_agent.handle_request.assert_called_with(
        {'task': 'generate_python', 'spec': 'test'}, 'user123'
    )

def test_lambda_handler_specific_action(mock_dependencies):
    mock_email_agent = mock_dependencies['email_agent']
    mock_email_agent.handle_request.return_value = {'status': 'success', 'result': 'Email queued'}
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
    mock_email_agent.handle_request.assert_called_with(
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