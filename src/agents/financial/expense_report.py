import time
from src.utils.helpers import log_audit, store_shared_data, supabase


def generate_report(data, user_id):
    task_id = data.get('task_id', f"report_{int(time.time())}")
    expenses_query = (
        supabase.table('expenses')
        .select('*')
        .eq('user_id', user_id)
        .execute()
    )
    expenses = expenses_query.data
    summary = {}
    for exp in expenses:
        category = exp['category']
        summary[category] = summary.get(category, 0) + exp['amount']
    store_shared_data(f'report_{task_id}', summary, user_id)
    log_audit(user_id, 'expense_report', summary)
    return {"status": "success", "result": summary, "task_id": task_id}
