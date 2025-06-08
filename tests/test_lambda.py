import pytest
import json
from unittest.mock import patch
from Lambda import lambda_function

@pytest.fixture
def mock_dependencies():
    with patch('Lambda.lambda_function.boto3'), \
         patch('Lambda.lambda_function.log_audit') as mock_log_audit, \
         patch('Lambda.lambda_function.execute_workflow') as mock_workflow, \
         patch('Lambda.lambda_function.parse_task') as mock_parse_task:
        yield mock_log_audit, mock_workflow, mock_parse_task

def test_lambda_handler_delegate_agent(mock_dependencies):
    mock_log_audit, mock_workflow, mock_parse_task = mock_dependencies
    mock_parse_task.return_value = {'agent': 'coding_agent', 'params': {'task': 'generate_python', 'spec': 'test'}}
    with patch('Lambda.lambda_function.coding_agent.handle_code_request') as mock_coding:
        mock_coding.return_value = {'status': 'success', 'result': {'code': 'print("Hello")'}}
        event = {
            'action': 'delegate',
            'body': json.dumps({'request': 'generate python code'}),
            'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}}
        }
        context = {}
        response = lambda_function.lambda_handler(event, context)
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == {'status': 'success', 'result': {'code': 'print("Hello")'}}
        mock_coding.assert_called_with({'task': 'generate_python', 'spec': 'test'}, 'user123')

def test_lambda_handler_specific_action(mock_dependencies):
    mock_log_audit, mock_workflow, mock_parse_task = mock_dependencies
    with patch('Lambda.lambda_function.email_agent.handle_email_request') as mock_email:
        mock_email.return_value = {'status': 'success', 'result': 'Email queued'}
        event = {
            'action': 'email',
            'body': json.dumps({'recipient': 'test@example.com', 'subject': 'Test'}),
            'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}}
        }
        context = {}
        response = lambda_function.lambda_handler(event, context)
        assert response['statusCode'] == 200
        assert json.loads(response['body']) == {'status': 'success', 'result': 'Email queued'}
        mock_email.assert_called_with({'recipient': 'test@example.com', 'subject': 'Test'}, 'user123')

def test_lambda_handler_invalid_action(mock_dependencies):
    mock_log_audit, mock_workflow, mock_parse_task = mock_dependencies
    event = {
        'action': 'invalid',
        'body': json.dumps({}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}}
    }
    context = {}
    response = lambda_function.lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'error': 'Invalid action'}
    mock_log_audit.assert_called_with('user123', 'invalid', {'error': 'Invalid action'})