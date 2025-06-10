import time
from src.utils.helpers import log_audit, store_shared_data, supabase



def handle_request(data, user_id):
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"financial_{int(time.time())}")
        response = {"status": "success", "result": {}, "task_id": task_id}

        if task == "create_retirement_plan":
            age = data.get("age", 30)
            retirement_age = data.get("retirement_age", 65)
            annual_income = data.get("annual_income", 50000)
            savings_rate = data.get("savings_rate", 0.15)
            expected_return = data.get("expected_return", 0.07)

            params = [age, retirement_age, annual_income, savings_rate,
                      expected_return]
            if any(v < 0 for v in params):
                return {
                    "status": "error",
                    "result": "Invalid input parameters",
                }

            years_to_retirement = retirement_age - age
            if years_to_retirement <= 0:
                msg = "Retirement age must be greater than current age"
                return {"status": "error", "result": msg}

            annual_savings = annual_income * savings_rate
            future_value = (
                annual_savings *
                (((1 + expected_return) ** years_to_retirement - 1) /
                 expected_return)
            )
            response["result"] = {
                "retirement_savings": round(future_value, 2),
                "years_to_retirement": years_to_retirement
            }

        elif task == "investment_strategy":
            risk_tolerance = data.get("risk_tolerance", "moderate").lower()
            investment_horizon = data.get("investment_horizon", 10)
            if investment_horizon <= 0:
                msg = "Investment horizon must be positive"
                return {"status": "error", "result": msg}

            portfolio = {
                "conservative": {"stocks": 30, "bonds": 60, "cash": 10},
                "moderate": {"stocks": 60, "bonds": 30, "cash": 10},
                "aggressive": {"stocks": 80, "bonds": 15, "cash": 5}
            }
            response["result"] = {
                "allocation": portfolio.get(risk_tolerance,
                                            portfolio["moderate"]),
                "horizon": investment_horizon
            }

        elif task == "create_budget":
            income = data.get("income", 0)
            expenses = data.get("expenses", [])
            if income < 0 or any(exp.get("amount", 0) < 0 for exp in expenses):
                msg = "Income and expenses cannot be negative"
                return {"status": "error", "result": msg}

            total_expenses = sum(exp.get("amount", 0) for exp in expenses)
            savings = income - total_expenses
            supabase.table('budgets').insert({
                'user_id': user_id,
                'income': income,
                'total_expenses': total_expenses,
                'savings': savings,
                'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }).execute()
            response["result"] = {
                "income": income,
                "total_expenses": total_expenses,
                "savings": savings
            }

        elif task == "track_expense":
            expense = data.get("expense", {})
            amount = expense.get('amount')
            if amount is None or amount < 0:
                return {"status": "error", "result": "Invalid expense amount"}

            supabase.table('expenses').insert({
                'user_id': user_id,
                'amount': amount,
                'category': expense.get('category', 'misc'),
                'description': expense.get('description', ''),
                'date': expense.get('date', time.strftime("%Y-%m-%d")),
                'created_at': time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }).execute()
            response["result"] = {"tracked": True}

        elif task == "list_expenses":
            expenses_query = (
                supabase.table('expenses')
                .select('*')
                .eq('user_id', user_id)
                .execute()
            )
            response["result"] = expenses_query.data or []

        elif task == "expense_summary":
            category = data.get("category")
            query = supabase.table('expenses').select('amount').eq('user_id',
                                                                   user_id)
            if category:
                query = query.eq('category', category)
            expenses = query.execute()
            total = sum(exp['amount'] for exp in expenses.data)
            response["result"] = {"total": total,
                                  "category": category or "all"}


        store_shared_data(f'financial_{task_id}', response["result"], user_id)
        log_audit(user_id, f"financial_{task}", response)
        return response
    except Exception as e:
        log_audit(user_id, "financial_task", {"error": str(e)})
        return {"status": "error", "result": str(e)}
