import json
import time
from supabase import create_client, Client
import os
from utils import log_audit, store_shared_data

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def generate_report(data, user_id):
    task_id = data.get('task_id', f"report_{int(time.time())}")
    period = data.get('period', 'monthly')
    expenses = supabase.table('expenses').select('*').eq('user_id', user_id).execute().data
    summary = {}
    for exp in expenses:
        category = exp['category']
        summary[category] = summary.get(category, 0) + exp['amount']
    store_shared_data(f'report_{task_id}', summary, user_id)
    log_audit(user_id, 'expense_report', summary)
    return {"status": "success", "result": summary, "task_id": task_id}