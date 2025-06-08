from utils import log_audit
import ccxt

def handle_portfolio_request(data, user_id):
    try:
        exchange = ccxt.coinbasepro({
            'apiKey': data.get('api_key'),
            'secret': data.get('api_secret')
        })
        if data.get('task') == 'view_portfolio':
            balance = exchange.fetch_balance()
            return {'portfolio': balance.get('total')}
        log_audit(user_id, 'portfolio_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'portfolio_task', {'error': str(e)})
        return {'error': str(e)}