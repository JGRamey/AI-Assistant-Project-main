import json
import os
from core_platform.agent_registry import get_handler, get_agent_module, get_agent_handler
from workflows import execute_workflow
from utils import log_audit, parse_task

# Mock boto3 and missing modules for non-AWS environment
if os.getenv('TESTING') == 'True':
    import sys
    from unittest.mock import MagicMock
    sys.modules['boto3'] = MagicMock()


def lambda_handler(event, context):
    try:
        request_context = event.get('requestContext', {})
        authorizer = request_context.get('authorizer', {})
        claims = authorizer.get('claims', {})
        user_id = claims.get('sub', 'anonymous')
        action = event.get('action')
        data = json.loads(event.get('body', '{}'))

        if event.get('Records'):
            for record in event['Records']:
                message = json.loads(record.get('body', '{}'))
                agent_name = message.get('target_agent')
                agent_module = get_agent_module(agent_name)
                if agent_module:
                    agent_module.handle_message(message, user_id)
            response_body = json.dumps({'status': 'messages_processed'})
            return {'statusCode': 200, 'body': response_body}

        if action == 'delegate':
            task_plan = parse_task(data.get('request', ''), user_id)
            if task_plan.get('workflow'):
                workflow_params = {
                    'workflow': task_plan['workflow'], **task_plan['params']
                }
                result = execute_workflow(workflow_params, user_id)
            elif task_plan.get('agent'):
                agent_name = task_plan['agent']
                handler = get_agent_handler(agent_name)
                if handler:
                    result = handler(task_plan['params'], user_id)
                else:
                    result = {'error': f'Unknown agent: {agent_name}'}
            else:
                result = {'error': 'Invalid task'}
            return {'statusCode': 200, 'body': json.dumps(result)}

        handler = get_handler(action)
        if handler:
            result = handler(data, user_id)
        else:
            result = {'error': 'Invalid action'}
        log_audit(user_id, action, result)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        log_audit(user_id, action or 'unknown', {'error': str(e)})
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }