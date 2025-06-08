import ccxt
import requests
from utils import encrypt_data, log_audit, analyze_patterns

def handle_trade_request(data, user_id):
    try:
        exchange = ccxt.coinbasepro({
            'apiKey': data.get('api_key'),
            'secret': data.get('api_secret')
        })
        if data.get('task') == 'fetch_data':
            symbol = data.get('symbol', 'BTC/USD')
            historical_data = exchange.fetch_ohlcv(symbol, '1d', limit=100)
            patterns = analyze_patterns(historical_data)
            return {'data': historical_data, 'patterns': patterns}
        elif data.get('task') == 'execute_trade':
            # Restricted write
            order = exchange.create_order(
                symbol=data.get('symbol'),
                type=data.get('type'),
                side=data.get('side'),
                amount=data.get('amount'),
                price=data.get('price')
            )
            return {'order': order}
        log_audit(user_id, 'trade_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'trade_task', {'error': str(e)})
        return {'error': str(e)}