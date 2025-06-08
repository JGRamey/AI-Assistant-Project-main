import json
import os
import time
import stripe
from supabase import create_client, Client
from utils import log_audit, store_shared_data, get_shared_data, handle_stripe_error
from agents.Financial_Agent import handle_request as financial_handle
from Blockchain import SmartContractManager

stripe.api_key = os.environ.get('STRIPE_API_KEY')
if not stripe.api_key:
    raise ValueError("STRIPE_API_KEY not set")

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def handle_revenue_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"revenue_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if task == "fetch_sales":
            try:
                start_date = data.get('start_date')
                end_date = data.get('end_date')
                params = {}
                if start_date and end_date:
                    params['created'] = {'gte': start_date, 'lte': end_date}
                charges = stripe.Charge.list(**params, limit=100)
                total = sum(charge.amount / 100 for charge in charges.data)
                supabase.table('revenue').insert({
                    'user_id': user_id,
                    'source': 'stripe',
                    'amount': total,
                    'date': time.strftime("%Y-%m-%d"),
                    'details': json.dumps([charge.to_dict() for charge in charges.data]),
                    'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }).execute()
                response["result"] = {"total": total, "charges": len(charges.data)}
            except stripe.error.StripeError as e:
                return handle_stripe_error(e)

        elif task == "fetch_youtube_revenue":
            youtube_data = get_shared_data(f'youtube_{user_id}', user_id) or {}
            estimated_revenue = youtube_data.get('analytics', {}).get('estimatedRevenue', 0)
            supabase.table('revenue').insert({
                'user_id': user_id,
                'source': 'youtube',
                'amount': estimated_revenue,
                'date': time.strftime("%Y-%m-%d"),
                'details': json.dumps(youtube_data.get('analytics', {})),
                'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }).execute()
            response["result"] = {"estimated_revenue": estimated_revenue}

        elif task == "generate_financial_report":
            revenue_data = supabase.table('revenue').select('*').eq('user_id', user_id).execute().data or []
            expense_data = financial_handle({'task': 'list_expenses'}, user_id)['result']
            total_revenue = sum(r['amount'] for r in revenue_data)
            total_expenses = sum(e['amount'] for e in expense_data)
            net_profit = total_revenue - total_expenses
            response["result"] = {
                "total_revenue": total_revenue,
                "total_expenses": total_expenses,
                "net_profit": net_profit,
                "revenue_breakdown": revenue_data
            }

        elif task == "investment_opportunities":
            net_profit = data.get('net_profit', 0)
            if net_profit < 0:
                return {"status": "error", "result": "Net profit cannot be negative"}
            risk_tolerance = data.get('risk_tolerance', 'moderate').lower()
            financial_result = financial_handle({
                'task': 'investment_strategy',
                'risk_tolerance': risk_tolerance,
                'investment_horizon': data.get('horizon', 10)
            }, user_id)
            if financial_result['status'] == 'error':
                return financial_result
            opportunities = {
                "portfolio_allocation": financial_result['result']['allocation'],
                "suggested_investment": net_profit * 0.5
            }
            response["result"] = opportunities

        elif task == "allocate_blockchain_rewards":
            amount = data.get('amount', 0)
            if amount <= 0:
                return {"status": "error", "result": "Amount must be positive"}
            agent_address = data.get('agent_address', '0x' + '0' * 40)
            contract_result = SmartContractManager.handle_request({
                'task': 'create_task',
                'agent_address': agent_address,
                'input': f"Reward allocation: {amount}",
                'task_id': task_id
            }, user_id)
            response["result"] = contract_result['result']

        store_shared_data(f'revenue_{task_id}', response["result"], user_id)
        log_audit(user_id, f"revenue_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "revenue_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}