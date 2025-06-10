from src.utils.helpers import log_audit
import ccxt


def handle_portfolio_request(data, user_id):
    """Handles portfolio-related tasks."""
    task = data.get('task')
    try:
        if task == 'view_portfolio':
            exchange = ccxt.coinbase({
                'apiKey': data.get('api_key'),
                'secret': data.get('api_secret')
            })
            balance = exchange.fetch_balance()
            log_audit(user_id, 'portfolio_task', {'task': task})
            return {'portfolio': balance.get('total')}

        log_audit(user_id, 'portfolio_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'portfolio_task', {'error': str(e)})
        return {'error': str(e)}
