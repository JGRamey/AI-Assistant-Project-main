import boto3
import time
import os
from typing import Dict, Any

from supabase import create_client, Client
from utils import log_audit, get_shared_data, store_shared_data


def render_dashboard(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Render or update the dashboard with user data.

    Args:
        data: Dictionary containing dashboard task and parameters
        user_id: User identifier

    Returns:
        Dictionary containing dashboard data or status/error message
    """
    try:
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')

        supabase = None
        if supabase_url and supabase_key:
            supabase: Client = create_client(supabase_url, supabase_key)

        task = data.get('task')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('DashboardData')

        if task == 'view':
            response = table.get_item(Key={'user_id': user_id})
            dashboard_data = response.get('Item', {})
            task_ids = data.get('task_ids', [])

            shared_results = {
                tid: get_shared_data(f'task_outcome_{tid}', user_id)
                for tid in task_ids
            }
            financial_data = get_shared_data(f'financial_{user_id}', user_id) or {}
            portfolio_data = get_shared_data(f'portfolio_{user_id}', user_id) or {}
            trading_data = get_shared_data(f'trading_{user_id}', user_id) or {}
            journal_data = get_shared_data(f'journal_{user_id}', user_id) or {}
            youtube_data = get_shared_data(f'youtube_{user_id}', user_id) or {}
            coding_data = get_shared_data(f'coding_{user_id}', user_id) or {}
            crm_data = get_shared_data(f'crm_{user_id}', user_id) or {}
            blockgnosis_data = get_shared_data(f'blockchain_{user_id}', user_id) or {}
            revenue_data = get_shared_data(f'revenue_{user_id}', user_id) or {}

            preferences = {}
            if supabase:
                preferences_data = supabase.table('user_preferences')\
                    .select('*')\
                    .eq('user_id', user_id)\
                    .execute()
                preferences = preferences_data.data[0] if preferences_data.data else {}

            dashboard_data.update({
                'shared_results': shared_results,
                'financial_data': financial_data,
                'portfolio_data': portfolio_data,
                'trading_data': trading_data,
                'journal_data': journal_data,
                'youtube_data': youtube_data,
                'coding_data': coding_data,
                'crm_data': crm_data,
                'blockgnosis_data': blockgnosis_data,
                'revenue_data': revenue_data,
                'preferences': preferences,
            })
            return dashboard_data

        elif task == 'update':
            if not supabase:
                return {"status": "error", "result": "Supabase not configured"}
            preferences = data.get('preferences', {})
            if not isinstance(preferences, dict):
                return {"status": "error", "result": "Preferences must be a dictionary"}

            supabase.table('user_preferences')\
                .upsert({
                    'user_id': user_id,
                    'preferences': preferences,
                    'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
                })\
                .execute()

            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET #attr = :val',
                ExpressionAttributeNames={'#attr': data.get('entity', 'data')},
                ExpressionAttributeValues={':val': data.get('value')}
            )

            store_shared_data(f'dashboard_{user_id}', {'updated': True}, user_id)
            return {'status': 'dashboard_updated'}

        elif task == 'fetch_tab_data':
            if not supabase:
                return {"status": "error", "result": "Supabase not configured"}
            tab = data.get('tab')
            if not tab:
                return {"status": "error", "result": "Tab not specified"}

            key = f'{tab}_{user_id}'
            tab_data = get_shared_data(key, user_id) or {}

            tab_data_supabase = supabase.table(tab)\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()

            tab_data.update({'supabase': tab_data_supabase.data or []})
            return tab_data

        log_audit(user_id, f'dashboard_{task}', {'task': task})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'dashboard_task', {'error': str(e)})
        return {'error': str(e)}


if __name__ == '__main__':
    pass
