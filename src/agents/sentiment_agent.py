from utils import log_audit
import requests


def handle_sentiment_request(data, user_id):
    """Handles sentiment analysis tasks."""
    task = data.get('task')
    try:
        if task == 'analyze':
            # Use Grok API for sentiment analysis
            response = requests.post(
                'https://api.x.ai/grok/analyze',
                json={'text': data.get('text')},
                timeout=10
            )
            response.raise_for_status()
            log_audit(user_id, 'sentiment_task', {'task': task})
            return {'sentiment': response.json()}

        log_audit(user_id, 'sentiment_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'sentiment_task', {'error': str(e)})
        return {'error': str(e)}
