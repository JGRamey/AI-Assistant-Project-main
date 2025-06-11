import ccxt
import pandas as pd
from ta import add_all_ta_features
from src.utils.helpers import log_audit


def handle_trade_request(data, user_id):
    """Handles trading-related tasks."""
    task = data.get('task')
    try:
        if task in ['fetch_data', 'execute_trade']:
            exchange = ccxt.coinbase({
                'apiKey': data.get('api_key'),
                'secret': data.get('api_secret')
            })
            if task == 'fetch_data':
                symbol = data.get('symbol', 'BTC/USD')
                ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=100)
                df = pd.DataFrame(
                    ohlcv,
                    columns=[
                        'timestamp', 'open', 'high', 'low', 'close', 'volume'
                    ]
                )
                df_with_ta = add_all_ta_features(
                    df, open="open", high="high", low="low", close="close",
                    volume="volume", fillna=True
                )
                patterns = df_with_ta.to_dict(orient='records')
                log_audit(user_id, 'trade_task', {'task': task})
                return {'data': ohlcv, 'patterns': patterns}

            elif task == 'execute_trade':
                # Restricted write
                order = exchange.create_order(
                    symbol=data.get('symbol'),
                    type=data.get('type'),
                    side=data.get('side'),
                    amount=data.get('amount'),
                    price=data.get('price')
                )
                log_audit(user_id, 'trade_task', {'task': task})
                return {'order': order}

        log_audit(user_id, 'trade_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'trade_task', {'error': str(e)})
        return {'error': str(e)}
