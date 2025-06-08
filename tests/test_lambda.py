import pytest
import json
from src.lambda_function import lambda_handler

def test_lambda_handler_valid():
    event = {
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}},
        'action': 'code',
        'body': json.dumps({'task': 'generate_solidity', 'spec': 'test'})
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
    assert 'code' in json.loads(response['body'])['result']

def test_lambda_handler_delegate():
    event = {
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}},
        'action': 'delegate',
        'body': json.dumps({'request': 'generate a video on blockchain'})
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
    assert 'status' in json.loads(response['body'])

def test_lambda_handler_dashboard():
    event = {
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}},
        'action': 'dashboard',
        'body': json.dumps({'task': 'view', 'task_ids': ['task1']})
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
    assert 'shared_results' in json.loads(response['body'])

def test_lambda_handler_sqs():
    event = {
        'Records': [
            {
                'body': json.dumps({
                    'target_agent': 'Financial_Agent',
                    'data': 'test_task',
                    'user_id': 'user123'
                })
            }
        ]
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
    assert 'messages_processed' in json.loads(response['body'])

def test_lambda_handler_blockchain():
    event = {
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}},
        'action': 'blockchain_token',
        'body': json.dumps({'task': 'deploy'})
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200

def test_lambda_handler_revenue():
    event = {
        'requestContext': {'authorizer': {'claims': {'sub': 'user123'}}},
        'action': 'token_manage',
        'body': json.dumps({'task': 'generate_financial_report'})
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
    assert 'net_profit' in json.loads(response['body'])['result']