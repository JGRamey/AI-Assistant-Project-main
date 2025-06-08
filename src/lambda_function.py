import json
import boto3
from agents import coding_agent, email_agent, trading_agent, priority_agent, news_agent, alert_agent
from agents import portfolio_agent, crm_agent, notes_agent, time_agent, sentiment_agent, snippet_agent
from agents import stress_agent, social_agent, learning_agent, voice_agent, key_agent
from agents import journal_agent, update_agent, smart_contract_ai_agent, Financial_Agent
from Blockchain import SmartContractManager
from platform.content import script_generator
from platform.social import post_scheduler
from platform.marketing import newsletter_automation
from platform.finances import revenue
from platform.analytics import youtube_analytics
from dashboard import render_dashboard
from utils import encrypt_data, decrypt_data, log_audit, send_message, receive_messages, parse_task
from workflows import execute_workflow

def lambda_handler(event, context):
    try:
        user_id = event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('sub', 'anonymous')
        action = event.get('action')
        data = json.loads(event.get('body', '{}'))

        if event.get('Records'):
            for record in event['Records']:
                message = json.loads(record.get('body', '{}'))
                agent = message.get('target_agent')
                if agent in globals():
                    globals()[agent].handle_message(message, user_id)
            return {'statusCode': 200, 'body': json.dumps({'status': 'messages_processed'})}

        if action == 'delegate':
            task_plan = parse_task(data.get('request', ''), user_id)
            if task_plan.get('workflow'):
                result = execute_workflow({'workflow': task_plan['workflow'], **task_plan['params']}, user_id)
            elif task_plan.get('agent'):
                agent = task_plan['agent']
                if agent in globals():
                    result = globals()[agent].handle_request(task_plan['params'], user_id)
                else:
                    result = {'error': f'Unknown agent: {agent}'}
            else:
                result = {'error': 'Invalid task'}
            return {'statusCode': 200, 'body': json.dumps(result)}

        handlers = {
            'coordinate': lambda: execute_workflow(data, user_id),
            'code': lambda: coding_agent.handle_code_request(data, user_id),
            'email': lambda: email_agent.handle_email_request(data, user_id),
            'trade': lambda: trading_agent.handle_trade_request(data, user_id),
            'priority': lambda: priority_agent.handle_priority_request(data, user_id),
            'news': lambda: news_agent.handle_news_request(data, user_id),
            'alert': lambda: alert_agent.handle_alert_request(data, user_id),
            'portfolio': lambda: portfolio_agent.handle_portfolio_request(data, user_id),
            'crm': lambda: crm_agent.handle_crm_request(data, user_id),
            'notes': lambda: notes_agent.handle_notes_request(data, user_id),
            'time': lambda: time_agent.handle_time_request(data, user_id),
            'sentiment': lambda: sentiment_agent.handle_sentiment_request(data, user_id),
            'snippet': lambda: snippet_agent.handle_snippet_request(data, user_id),
            'stress': lambda: stress_agent.handle_stress_request(data, user_id),
            'expense': lambda: Financial_Agent.handle_request(data, user_id),
            'social': lambda: social_agent.handle_social_request(data, user_id),
            'learn': lambda: learning_agent.handle_learning_request(data, user_id),
            'voice': lambda: voice_agent.handle_voice_request(data, user_id),
            'key': lambda: key_agent.handle_key_request(data, user_id),
            'journal': lambda: journal_agent.handle_journal_request(data, user_id),
            'update': lambda: update_agent.handle_update_request(data, user_id),
            'dashboard': lambda: render_dashboard(data, user_id),
            'store': lambda: SmartContractManager.handle_request({'task': 'create_task', **data}, user_id),
            'retrieve': lambda: SmartContractManager.handle_request({'task': 'get_task', **data}, user_id),
            'content_script': lambda: script_generator.handle_script_request(data, user_id),
            'social_post': lambda: post_scheduler.handle_post_request(data, user_id),
            'newsletter': lambda: newsletter_automation.handle_newsletter_request(data, user_id),
            'token_manage': lambda: revenue.handle_revenue_request(data, user_id),
            'youtube_analytics': lambda: youtube_analytics.handle_analytics_request(data, user_id),
            'blockchain_token': lambda: SmartContractManager.handle_request(data, user_id),
            'smart_contract': lambda: smart_contract_ai_agent.handle_request(data, user_id),
            'financial_plan': lambda: Financial_Agent.handle_request(data, user_id)
        }

        result = handlers.get(action, lambda: {'error': 'Invalid action'})()
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