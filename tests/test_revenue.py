import os
import json
import stripe
from utils import log_audit, store_shared_data

def handle_revenue_request(data: dict, user_id: str) -> dict:
    try:
        task = data.get('task')
        task_id = data.get('task_id', f"revenue_{int(os.time())}")
        response = {"status": "SUCCESS", "description": "", "result": {}, "task_id": task_id}

        if task == 'fetch_youtube_tasks':
            # Mocked for testing (replace with real YouTube API in production)
            revenue_data = {"total_views": 1000, "estimated_revenue": 100.50}
            response["result"] = revenue_data
            store_shared_data(f'youtube_revenue_{task_id}', revenue_data, user_id)

        elif task == 'fetch_stripe_tasks':
            stripe.api_key = os.environ.get('STRIPE_API_KEY')
            if not stripe.api_key:
                return {"status": "ERROR", "description": "Stripe API key not set", "task_id": task_id}
            try:
                charges = stripe.Charge.list_objects(limit=100)
                total_revenue = sum(charge.amount for charge in charges.data) / 100  # Convert cents to dollars
                revenue_data = {"total_revenue": total_revenue, "charge_count": len(charges.data)}
                response["result"] = revenue_data
                store_shared_data(f'stripe_revenue_{task_id}', revenue_data, user_id)
            except stripe.error.StripeError as e:
                return {"status": "ERROR", "description": f"Stripe error: {str(e)}", "task_id": task_id}

        elif task == 'fetch_all_revenue':
            # Combine mocked YouTube and Stripe data
            youtube_data = {"total_views": 1000, "estimated_revenue": 100.50}
            stripe_data = {"total_revenue": 0, "charge_count": 0}
            if os.environ.get('STRIPE_API_KEY'):
                try:
                    charges = stripe.Charge.list_objects(limit=100)
                    stripe_data = {
                        "total_revenue": sum(charge.amount for charge in charges.data) / 100,
                        "charge_count": len(charges.data)
                    }
                except stripe.error.StripeError:
                    pass
            combined_data = {
                "youtube": youtube_data,
                "stripe": stripe_data,
                "total": youtube_data["estimated_revenue"] + stripe_data["total_revenue"]
            }
            response["result"] = combined_data
            store_shared_data(f'all_revenue_{task_id}', combined_data, user_id)

        else:
            return {"status": "ERROR", "description": "Invalid task", "task_id": task_id}

        log_audit(user_id, f"revenue_{task}", response)
        return response

    except Exception as e:
        error_response = {"status": "ERROR", "description": f"Error: {str(e)}", "task_id": task_id}
        log_audit(user_id, "revenue_task", error_response)
        return error_response