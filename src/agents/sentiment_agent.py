from utils import log_audit
import requests

def handle_sentiment_request(data, user_id):
    try:
        if data.get('task') == 'analyze':
            # Use Grok API for sentiment analysis
            response = requests.post(
                'https://api.x.ai/grok/analyze',
                json={'text': data.get('text')}
            )
            return {'sentiment': response.json()}
        log_audit(user_id, 'sentiment_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'sentiment_task', {'error': str(e)})
        return {'error': str(e)}