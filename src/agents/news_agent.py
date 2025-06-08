import requests
from utils import log_audit

def handle_news_request(data, user_id):
    try:
        if data.get('task') == 'fetch_news':
            response = requests.get('https://api.coingecko.com/api/v3/news')
            articles = response.json().get('data', [])
            filtered = [a for a in articles if 'crypto' in a.get('title', '').lower()]
            return {'news': filtered}
        elif data.get('task') == 'fetch_m2':
            response = requests.get('https://fred.stlouisfed.org/series/M2SL')
            return {'m2_data': response.text}
        log_audit(user_id, 'news_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'news_task', {'error': str(e)})
        return {'error': str(e)}