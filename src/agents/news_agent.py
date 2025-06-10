import requests
from utils import log_audit


def handle_news_request(data, user_id):
    """Handles news-related tasks."""
    task = data.get('task')
    try:
        if task == 'fetch_news':
            response = requests.get(
                'https://api.coingecko.com/api/v3/news', timeout=10
            )
            response.raise_for_status()
            articles = response.json().get('data', [])
            filtered = [
                a for a in articles if 'crypto' in a.get('title', '').lower()
            ]
            log_audit(user_id, 'news_task', {'task': task})
            return {'news': filtered}
        elif task == 'fetch_m2':
            response = requests.get(
                'https://fred.stlouisfed.org/series/M2SL', timeout=10
            )
            response.raise_for_status()
            log_audit(user_id, 'news_task', {'task': task})
            return {'m2_data': response.text}

        log_audit(user_id, 'news_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'news_task', {'error': str(e)})
        return {'error': str(e)}
